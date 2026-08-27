---
type: concept
status: verified
area: [language-models, pretraining-data, packing, attention-mask]
node_id: LM-22
aliases: [Sequence packing, Packed attention, 文档拼接]
prerequisites: ["[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]", "[[预训练语料来源、许可、隐私与文档单位合同]]"]
related: ["[[数据混合、温度采样、重加权与域损失]]", "[[Prefill、Decode、KV Cache 与 Continuous Batching]]"]
sources: ["[[S-2021-Krell-Sequence-Packing]]", "[[S-2018-Radford-GPT]]"]
exercises: ["[[习题 - Packing、文档边界、Position ID 与 Loss Mask]]"]
solutions: ["[[解答 - Packing、文档边界、Position ID 与 Loss Mask]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-data-packing-mask-position-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Packing、文档边界、Position ID 与 Loss Mask

> [!abstract] 一句话结论
> Packing 是先把变长序列装进定长 bin 的系统算法，再用 document-aware relation、position IDs 和边界 labels 保持统计语义。利用率提高只证明 padding 减少；若任一语义层遗漏，模型会跨文档读取或预测不应存在的 next token。

## 一、装箱问题与利用率

给文档 token 长度 $\ell_1,\ldots,\ell_N$ 与最大窗口 $C$，将文档分配到 bins，使每 bin 总长度不超过 $C$，并尽量减少 padding/截断。这是 bin packing 类组合问题。

对 batch bins $b=1,ldots,B$，packing utilization：

$$
U=\frac{\sum_i\ell_i}{BC}.
$$

提高 $U$ 可减少无效 padding activation，但不直接等于 FLOP 或 wall-time 增益：kernel 支持、稀疏/block masks、length sorting、编译与 memory access 都影响实际速度。

Best-fit、first-fit decreasing、histogram packing 等算法决定哪个文档共 bin。若 batch composition 影响 normalization、optimizer 或随机 seed，装箱策略也可能影响训练动力学。

## 二、三种常被混称为 packing 的方案

### 1. Padding batching

每个 sequence 独立，只补齐到 batch 最大长度；无跨样本 relation，语义简单但浪费。

### 2. Concatenated stream

文档以 EOS/分隔符拼成连续语料流，普通 causal relation 允许后文读前文。这里跨文档 context 是**目标的一部分**，不是泄漏，只要训练/评测/部署同样声明。

### 3. Contamination-free packing

多个独立样本共用物理张量，但 attention 与 loss 阻断跨文档。目标是与分别计算这些样本数学等价，同时减少 padding。

三者性能与数据利用不同，不能都只写 `packing=True`。

## 三、正确 relation：因果与同文档取交集

令 $d(i)$ 为 packed position $i$ 的 document id。对 CLM：

$$
R_{ij}=\mathbf 1\{j\le i\}\mathbf 1\{d(j)=d(i)\}\mathbf 1\{i,j\text{ valid}\}.
$$

这形成多个下三角 block。若只用全局下三角，第二篇文档的 query 能读第一篇全部 key；即使第一篇 labels ignore，hidden states仍传递信息。

对于 encoder/MLM，每文档 block 内可双向；对于 Prefix LM，每个 document 内再应用自己的 prefix 分界。Packing relation 是 task relation 与 document relation 的交集，不是固定一种三角。

## 四、Position ID 有两种合法合同

### Reset per document

每篇从 0 开始：`0,1,2 | 0,1 | 0,1,2,3`。更接近独立 forward，尤其对绝对位置 embedding；但 kernel/cache 必须支持重复 positions。

### Continuous within bin

`0,1,2 | 3,4 | 5,6,7,8`。即使 attention 被 block，后文档表示仍依赖前面文档的**长度/装箱位置**，不与独立从 0 开始完全等价。它可能训练位置平移鲁棒性，也可能产生 packing-layout dependence。

RoPE/相对位置也不能一句“与绝对位置无关”带过：reset 会改变旋转相位/相对坐标，连续位置在 block 内的相对差相同但绝对/长度外推接口可能不同。必须用 full-vs-packed logit test 判断所求等价。

## 五、边界 token 与 next-label 政策

独立文档 $x^{(1)}$ 与 $x^{(2)}$ 相邻时，文档 1 最后一个 logit 的 next label 不能静默变成文档 2 首 token。常见政策：

1. 每文档显式 EOS，训练最后内容 token→EOS；EOS 位置之后的跨文档 label ignore；
2. 没有 EOS 时，最后内容位置 loss ignore；
3. 连续语料流目标才允许 EOS/边界→下一文档首 token，并让下一文档读取过去。

设 shifted labels 为 $y_i=x_{i+1}$，有效 mask：

$$
m_i=\mathbf 1\{d(i)=d(i+1)\}
$$

（若 EOS 已在每文档内部，则其相应预测仍按 tokenization 合同计分）。实际 API 需对 BOS/EOS 细化，核心是不让物理相邻自动成为统计 next event。

## 六、与未 packed 数学等价的条件

在 eval、无跨样本随机耦合时，对每篇文档 $d$，packed logits 与单独 forward 对齐需要至少：

- input tokens 相同；
- 每层 relation 的祖先图相同；
- position/segment IDs 相同；
- normalization 不跨 sequence 聚合；
- dropout RNG 若要求 bitwise 对齐需相同映射；
- labels、loss mask、reduction 权重相同；
- truncation 与 special tokens 相同。

如果只要求优化 estimand 等价而不要求 bitwise logits，随机 dropout 可不同但期望合同仍需论证。论文所说“no performance impact”是特定实现实验，不自动认证你的 kernel。

## 七、Packing 怎样改变权重

若每 bin loss 先平均、再对 bins 等权，短文档塞得多的 bin 与单长文档 bin 权重相同，文档/token 权重可能改变。推荐全 batch 保存

$$
N=\sum_{b,t}m_{bt}ell_{bt},\qquad D=\sum_{b,t}m_{bt},\qquad L=N/D.
$$

若目标是每文档等权，应显式为每个 document 先平均再聚合，而不是寄希望于 packer。Mixture sampler 与 packer交互：按域抽文档后，长度分布影响每域进入 bins 的比例和等待队列。

## 八、图：物理同 bin 不等于统计同序列

先看图回答：右边全局下三角中的红格会造成什么条件分布变化？

![[00-知识库管理/_assets/figures/language-models/fig-lm-data-packing-mask-position-v1.svg|900]]

> [!figure] 图 LM-22　装箱、块因果 relation 与边界 label
> 上方三色文档装入 12-token bin；左下对比正确块因果与错误全局因果；右侧检查文档边界 next label。来源：本课程依据 sequence packing 与 CLM 合同独立绘制。

**怎样读图**：先看颜色/document id，再逐格检验 same-document，最后沿 shift 表核对边界 label 和 score policy。

**图没有证明什么**：图不决定 position reset/continuous 谁更好，不保证 block mask kernel 更快，也不表示所有训练都必须阻断跨文档 context。

## 九、最小测试套件

1. 两文档 toy pack，逐格比对 $R_{ij}$；
2. 改文档 A token，文档 B logits 在 block 模式下不变；
3. packed 与逐文档 forward logits 对齐（相同 position 合同）；
4. 边界 label 不预测下一文档首 token；
5. 每个有效 target 恰计一次，$D$ 与未 packed 相同；
6. reset/continuous positions 分别打印，不让默认值漂移；
7. 空/超长/恰满窗口/EOS-only 文档行为明确；
8. 报 utilization、实际 FLOPs、tokens/s、peak memory 与质量，而非只报 padding ratio。

## 十、本节出口

你应能将 packed tensor 还原为 document bins，写出 task∧document relation、position IDs 与 boundary loss，设计 packed/unpacked 等价测试。下一节[[Curriculum、持续预训练与域适配数据路径]]把静态 mixture 扩展为随训练时间变化的数据路径。

## 练习与独立解答

- [[习题 - Packing、文档边界、Position ID 与 Loss Mask]]
- [[解答 - Packing、文档边界、Position ID 与 Loss Mask]]
