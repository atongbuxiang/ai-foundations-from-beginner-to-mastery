---
type: concept
status: draft
area: [architecture, attention, failure-analysis, evidence]
aliases: [Attention Failure Modes, Attention Evidence Map]
node_id: ARCH-32
prerequisites: ["[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[Attention Mask、因果性与可见性合同]]", "[[Multi-Head Attention、投影子空间与参数量]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[科学空间 - 第四章专题来源地图]]", "[[表示与模型架构完整课程地图与掌握标准]]"]
sources: ["[[S-2019-Jain-Wallace-Attention-Explanation]]", "[[S-2019-Michel-Head-Pruning]]", "[[S-2020-Yun-Transformer-Universal-Approximation]]", "[[S-2021-Dong-Pure-Attention-RankCollapse]]", "[[S-2023-Su-9859-KeyNorm长度外推]]", "[[S-2023-Su-9889-Attention集中性]]", "[[S-2023-Su-9529-DecoderOnly低秩猜想]]", "[[S-2021-Su-8610-线性Transformer反例]]"]
exercises: ["[[习题 - Attention 失效模式、反例与证据地图]]"]
solutions: ["[[解答 - Attention 失效模式、反例与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-failure-evidence-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Attention 失效模式、反例与证据地图

> [!abstract] 本节主问题
> Attention 可能在对象、shape、mask、数值、表达、优化、长度泛化、解释或系统层面失败。一个症状——例如低 entropy、头可剪、rank 下降或长文本性能跌落——不能自动确定机制。本节把每类主张配到最小反例、诊断、干预和 `I/T/E/H/O` 证据等级。

## 一、先分清九类失败

| 层级 | 典型失败 | 最先检查 |
|---|---|---|
| 对象语义 | Q/K/V 来源或候选轴错 | shape + role ledger |
| Mask | future/padding 泄漏、全遮蔽 | 极端 score 单元测试 |
| 数值 | overflow、NaN、低精度饱和 | finite ratio、logit range |
| 统计尺度 | norm/temperature 漂移 | q/k norm、row entropy |
| 表达 | head width/feature rank 瓶颈 | 构造可达性反例 |
| 深度优化 | token uniformity、梯度/路由失衡 | layerwise spectra、ablation |
| 长度泛化 | 训练外长度崩溃 | length sweep + controls |
| 解释 | 权重与因果贡献不一致 | counterfactual intervention |
| 系统 | 渐近更优却 wall-clock 更差 | versioned kernel benchmark |

先定位层级，才知道需要数学证明、单元测试还是受控实验。

## 二、反例 1：可见不等于会用

Dense self-attention 给每个 query 到所有可见 keys 的直接路径，但模型仍可能：

- logits 近均匀，远程信号被平均稀释；
- 过尖地锁定错误 shortcut；
- value projection 丢掉目标信息；
- 多层混合后信号被 residual/MLP 覆盖；
- 训练分布从未要求该依赖。

所以 graph distance 为 1 只是计算路径事实 `I`，不是远程依赖任务成功 `E`。

## 三、反例 2：低 Rank Logit 不等于低 Rank Weight

[[Attention 矩阵的秩、瓶颈与有效秩]] 已给出

$$
L=\begin{bmatrix}0&0\\0&1\end{bmatrix},\quad \operatorname{rank}L=1,
$$

而 $\operatorname{softmax}_{row}(L)$ 满秩。任何“softmax attention 因 $d_k<T$ 所以权重必低秩”的论证到此即失败。反过来，feature-factorized linear attention 的 affinity 确有 $r$ 维 rank 界；两类参数化不可混用。

## 四、反例 3：严格满秩不等于有效信息充分

Inclusive causal attention 因正对角下三角而严格满秩；但可令对角元素极小，奇异值谱高度集中，条件数很差。[[S-2023-Su-9529-DecoderOnly低秩猜想]] 中“满秩”事实为 `I`，以此解释 decoder-only 流行只是 `H`，还需 objective、数据、缓存与规模实验。

## 五、反例 4：权重不是自动的忠实解释

一行 attention 权重确实记录某层某头怎样混合 values；但最终预测还经过 value 内容、其他 heads、$W_O$、residual、MLP 与后续层。两组差异很大的权重可能产生相同 $AV$：若 $v_1=v_2$，在两者间重新分配质量完全不改变输出。

[[S-2019-Jain-Wallace-Attention-Explanation]] 在所研究 NLP 设置中发现权重与其他 importance 信号相关性有限，且可构造不同 attention 分布保持近似预测。正确结论是：**忠实解释需要额外验证**，而不是“attention 永远不能解释”。

### 解释目标必须先定义

- 内部描述：该层实际读取了什么；
- 局部敏感性：小扰动对输出的影响；
- 反事实充分性/必要性；
- 人类语义合理性；
- 全局机制。

不同目标需要不同实验，热力图只适合提出假说。

## 六、Head 可剪不等于多头无用

[[S-2019-Michel-Head-Pruning]] 的结果属于训练后特定 checkpoint 的 `E`：很多 heads 在所测任务中可移除且性能降幅小。可能机制包括过参数化、替代路径、任务未使用、单头与联合效应不同。

最小审计：

1. 单头 zeroing curve；
2. 联合剪枝 curve；
3. 是否重新训练/微调；
4. 多 seed/checkpoint；
5. in-distribution 与 OOD；
6. 真实 latency/memory，而非只报 head 数。

训练后冗余不等于训练过程不需要冗余，也不等于理论表达类等价。

## 七、Pure Attention 退化与完整 Transformer

[[S-2021-Dong-Pure-Attention-RankCollapse]] 给出条件化 `T`：无 skip/MLP 的 pure self-attention 堆叠会快速趋向 token uniformity/rank-one。它支持 residual/MLP 对避免该退化的重要性。

不得外推为：

- 任意 causal/bidirectional Transformer 必秩坍缩；
- 有 LayerNorm 后仍满足同一递推；
- 某层低 effective rank 就由该定理造成；
- 增加 MLP 一定解决所有深度问题。

验证实际模型要同时测 attention branch、residual stream 和 block output。

## 八、通用逼近也不是能力终点

[[S-2020-Yun-Transformer-Universal-Approximation]] 给出条件化存在性结果，是对“Attention 根本无法表达复杂序列函数”的反驳。但通用逼近定理不提供：有限资源、训练可达、样本效率、算法长度外推、数值稳定或硬件效率。

负面秩退化定理与正面通用逼近定理不矛盾：它们研究的模型类、组件、假设和问题不同。

## 九、长度外推：先找尺度漂移

训练长度到测试长度变化时，可见 key 数、位置范围和数据统计同时变。症状可能包括：

- logit max 随候选数的极值效应变化；
- Q/K norm 或 position interaction 漂移；
- row entropy/effective support 改变；
- 远程位置未训练；
- mask/window/cache 语义改变；
- 数值累积或 kernel 切换。

[[S-2023-Su-9859-KeyNorm长度外推]] 在小型 GAU（约一亿参数、训练长 512、测试到 4096）的设置报告 KNA/CosA 改进。这是值得复现的 `E`，不是大模型 `T`。原文对 scale-up 亦保留，课程将未验证部分标 `O`。

### 长度扫描最小记录

对 $T\in\{T_{train},2T_{train},4T_{train},\ldots\}$ 报告：loss/accuracy、logit std/max、Q/K norm、entropy/top-k mass、spectral metrics、latency/memory；对照 normalization、temperature、position scheme、training-length curriculum。

## 十、线性 Attention：渐近式不是裁决

[[S-2021-Su-8610-线性Transformer反例]] 指出 feature width/低秩可能使线性 Attention 为保持效果付出额外宽度；[[S-2021-Su-8338-Performer到线性Attention]] 则给出结合律主线。两者合起来形成正确问题：

$$
\text{真实收益}=f(T,r,d,\text{mask},\text{kernel},\text{dtype},\text{quality target}).
$$

不能从 $O(T)$ 推出所有有限 $T$ 更快，也不能从某次效果差推出线性 Attention 不可能有用。需要 crossover curve，而非一个长度点。

## 十一、集中性不是单一优劣指标

[[S-2023-Su-9889-Attention集中性]] 促使我们用 entropy、top-k mass、$\ell_2$ concentration 等量化“注意力集中”。但：

- 指标依可见位置数与分布假设；
- 低 entropy 可是正确选择，也可是错误饱和；
- 高 entropy 可是有用平均，也可是无法区分；
- 集中性与解释忠实性是不同轴。

最有力的证据是“测量 + 干预”：改变 temperature/norm/候选数，观察集中指标和任务输出是否按机制预测共同变化。

## 十二、证据等级与措辞

| 等级 | 内容 | Attention 示例 | 合格措辞 |
|---|---|---|---|
| `I` | 可直接复算的恒等/shape | rank$(QK^T)\le d_k$、causal determinant | “由……直接推出” |
| `T` | 带假设的定理 | pure attention rank collapse、通用逼近 | “在……假设下” |
| `E` | 版本化实验 | head pruning、KNA 长度扫描 | “在该模型/数据/长度下观察到” |
| `H` | 机制解释 | 低秩解释 decoder-only 优势 | “一种待验证解释是” |
| `O` | 尚未测量的外推 | 更大模型/更长上下文是否保持 | “仍待验证” |

最常见学术错误是从 `I` 跳到 `H` 后用定理语气，或从一个 `E` 跳到全称结论。

## 十三、标准 Attention Evidence Card

任何“Attention 更好/更差/更快/更可解释”至少记录：

```text
claim:
evidence_level: I / T / E / H / O
architecture + checkpoint:
Q/K/V source and shapes:
mask + position contract:
task + data + split:
train/test length:
parameter/FLOP/memory/kernel/dtype:
metric + seed + uncertainty:
counterexample or intervention:
supported conclusion:
unsupported extrapolation:
```

## 十四、图：从症状到证据

先看图回答：head pruning curve 属于哪个证据等级？若层间 singular spectrum 下降，为什么移除 residual/MLP 的干预必须谨慎？

![[00-知识库管理/_assets/figures/architecture/fig-attention-failure-evidence-v1.svg|900]]

> [!figure] 图 40.4-08　Attention 失效症状、诊断—干预对与证据阶梯
> 左栏分列常见症状，中栏将测量配到最小干预，右栏区分 I/T/E/H/O。来源：依据本卷反例、解释与秩文献独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_attention_v1.py]] 生成。

**怎样读图**：从左栏选一个症状，必须在中栏找到可复现的量和干预，再把得到的结论放到右栏恰当等级；若缺少干预，最多保留为相关性实验或机制假说。

**图没有证明什么**：它没有给出所有失败的完备分类，也没有证明某个诊断量唯一对应某个机制；不同失效可以同时发生。

## 十五、常见错误

1. 以直接可见替代任务成功；
2. 把 logit rank、weight rank 与 hidden rank 混用；
3. 用 full rank 宣称条件良好或架构优越；
4. 用 heatmap 宣称因果解释；
5. 用 head 剪枝结果否定多头训练价值；
6. 把 pure attention theorem 外推完整 Transformer；
7. 用通用逼近定理回答 SGD/样本/效率；
8. 把小模型长度实验写成 scale-up 定律；
9. 用渐近复杂度替代 kernel benchmark；
10. 把集中性、稀疏性、准确率与解释性当一条轴。

## 十六、掌握标准

> [!summary]
> - Attention 的失败须按对象、mask、数值、表达、优化、泛化、解释和系统分层；
> - 症状不唯一确定机制，需“测量 + 最小干预 + 反例”；
> - rank collapse、通用逼近、head pruning、长度外推分别属于不同证据；
> - 科学空间适合提出新问题和反例直觉，正式定理与规模结论必须回查一级来源/实验。

能识别证据等级（A/B）、重建本卷四个核心反例（C/D），并为一条真实 Attention 声明写完整 evidence card、复现和否证方案（E）。

## 十七、练习与独立详解

- [[习题 - Attention 失效模式、反例与证据地图]]
- [[解答 - Attention 失效模式、反例与证据地图]]

## 参考来源

- [[S-2019-Jain-Wallace-Attention-Explanation]]
- [[S-2019-Michel-Head-Pruning]]
- [[S-2020-Yun-Transformer-Universal-Approximation]]
- [[S-2021-Dong-Pure-Attention-RankCollapse]]
- [[S-2023-Su-9859-KeyNorm长度外推]]
- [[S-2023-Su-9889-Attention集中性]]
- [[S-2023-Su-9529-DecoderOnly低秩猜想]]
- [[S-2021-Su-8610-线性Transformer反例]]
