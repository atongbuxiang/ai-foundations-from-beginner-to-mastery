---
type: concept
status: draft
area: [architecture, attention, multi-head, complexity]
aliases: [Multi-Head Attention, MHA, Attention Heads]
node_id: ARCH-29
prerequisites: ["[[Self-Attention、Cross-Attention 与张量形状]]", "[[线性映射]]", "[[渐近记号、增长率与复杂度]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]", "[[Attention 失效模式、反例与证据地图]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2020-Bhojanapalli-LowRank-Attention]]", "[[S-2019-Michel-Head-Pruning]]", "[[S-2022-Su-8934-FLASH-GLU-GAU]]"]
exercises: ["[[习题 - Multi-Head Attention、投影子空间与参数量]]"]
solutions: ["[[解答 - Multi-Head Attention、投影子空间与参数量]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-multihead-budget-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Multi-Head Attention、投影子空间与参数量

> [!abstract] 本节主问题
> Multi-head attention 让多个投影后的子空间各自计算寻址，再拼接混合。它不是“同一张 attention 图重复 $h$ 次”，也不是免费增加表达力：固定 $d_{model}$ 时，更多 heads 通常意味着更窄的每头维度；标准投影参数量的主项不依 head 数，但 score 存储、kernel 调度与训练后有效利用率会改变。

## 一、定义：每个 Head 有自己的投影

对第 $r$ 个 head，

$$
Q_r=X_qW_Q^{(r)},\qquad
K_r=X_mW_K^{(r)},\qquad
V_r=X_mW_V^{(r)},
$$

并计算

$$
H_r=\operatorname{Attn}(Q_r,K_r,V_r;M_r)
\in\mathbb R^{T_q\times d_v^{(r)}}.
$$

最后

$$
\operatorname{MHA}(X_q,X_m)
=\operatorname{Concat}(H_1,\ldots,H_h)W_O.
$$

不同 head 可以有不同 Q/K/V 投影，因而学习不同的匹配双线性形式和 value 通道。通常 mask 的可见关系相同，但某些架构也可给不同 heads 不同结构 mask。

## 二、实现中的 Packed Projection

实际代码常不保存 $h$ 组小矩阵，而用大矩阵一次投影：

$$
W_Q\in\mathbb R^{d_{model}\times(hd_k)},
$$

先得到 $(B,T_q,hd_k)$，再 reshape/transposition 为 $(B,h,T_q,d_k)$。K/V 同理。这个 reshape 不复制数学信息，但 stride/layout 可能影响 kernel。

标准 score 与输出形状为

$$
S:(B,h,T_q,T_k),\qquad
H:(B,h,T_q,d_v),
$$

拼接后为 $(B,T_q,hd_v)$，再由 $W_O$ 回到 $d_{model}$。

## 三、标准参数量为何约为 $4d_{model}^2$

采用常见约定

$$
hd_k=hd_v=d_{model}=d.
$$

则三个 packed projection 的参数量分别为 $d\cdot d$：

$$
N_{QKV}=3d^2.
$$

输出投影

$$
W_O\in\mathbb R^{d\times d},\qquad N_O=d^2.
$$

所以忽略 bias：

$$
N_{MHA}=4d^2.
$$

$h$ 在 $h(d/h)=d$ 中消去。于是从 8 heads 改为 16 heads、保持总宽 $d$，主投影参数量不变；每头宽从 $d/8$ 降为 $d/16$。

> [!warning] 必须重算的变体
> GQA/MQA 共享 K/V heads；cross-attention 的输入宽可不同；某些实现 $d_k\ne d_v$；有 bias、gating、head-specific output 或 low-rank projection。此时不能套 $4d^2$。

## 四、Work、存储与 Head 数

Dense score 的乘加约为

$$
O(BhT_qT_kd_k).
$$

固定 $hd_k=d$ 后为 $O(BT_qT_kd)$，主阶 work 对 $h$ 消去。但显式 score/weight 元素数

$$
B h T_qT_k
$$

随 $h$ 线性增加。即使 FlashAttention 类 kernel 不物化全部矩阵，head 数仍会改变 tile、occupancy、小矩阵宽度、launch 与 fusion 行为。

因此要分开报告：

- 参数；
- FLOP/乘加；
- 峰值中间存储；
- activation/backward；
- kernel wall-clock；
- KV cache（后续专卷）。

## 五、为何多个子空间可能有用

单个 head 使用一个 score geometry 与一组 value projection。多个 heads 可同时：

- 用不同双线性形式寻找不同关系；
- 在不同 value 子空间传输信息；
- 让某些头局部、某些头远程；
- 通过 concat 保留多个摘要，再由 $W_O$ 联合使用。

但这些是能力与设计直觉，不是每个训练结果都实现的保证。若所有 $W_Q^{(r)},W_K^{(r)},W_V^{(r)}$ 学成近似相同，多头会功能重复；若每头过窄，又可能出现表示瓶颈。

## 六、固定总宽下的表达权衡

增加 $h$ 同时带来：

1. 更多独立 attention distributions；
2. 更小 per-head $d_k,d_v$；
3. 每个 logit matrix $Q_rK_r^\top$ 更低的线性代数秩上界；
4. 更多 score rows/tensors 与系统开销；
5. head permutation 对称性更大。

[[S-2020-Bhojanapalli-LowRank-Attention]] 研究 head projection dimension 与可表示 attention pattern 的条件。正确表述是“某些目标 attention matrices 在 head dimension 太小时不可达”，而不是错误的“softmax 后 attention matrix 的秩永远不超过 $d_k$”。后者将在 [[Attention 矩阵的秩、瓶颈与有效秩]] 用反例否定。

## 七、Head 的不可辨识与对称性

若同步置换 head 顺序，并相应置换 $W_O$ 的输入块，函数不变。因此 head 1、head 2 的编号没有跨 checkpoint 的固有语义。另有线性子空间中的基变换、缩放等参数等价。

所以比较“第 7 头”跨 seed 的图案通常没有意义，除非先做 matching/alignment；head 专门化应以函数干预和可重复统计支持。

## 八、Head 剪枝证据怎样读

[[S-2019-Michel-Head-Pruning]] 在所研究模型/任务中发现许多训练后 heads 可移除而只造成有限性能下降。这支持：训练后功能利用可能冗余，head importance 不均。

它不证明：

- 架构在训练前只需一个 head；
- 任意模型、任务或长度都能剪同样比例；
- 单头独立移除的影响可相加；
- 剪枝后无分布外/鲁棒/延迟代价；
- “热图相似”就等于功能冗余。

实验必须区分 zeroing、结构删除、联合剪枝、是否微调和 latency 是否真正下降。

## 九、GAU/FLASH 是另一种设计点

[[S-2022-Su-8934-FLASH-GLU-GAU]] 讨论 gated attention unit 与高效组合，说明多头不是 Attention 设计空间的唯一坐标。课程采用其架构问题入口与实验线索，但不会用某一设置的效果证明“单头/门控普遍优于 MHA”。比较时需对齐参数、训练预算、sequence length、kernel 和任务。

## 十、图：多头预算

先看图回答：固定 $d_{model}=512$ 时从 8 头改 16 头，投影参数量和每头宽分别怎样变？哪项存储仍随 $h$ 增加？

![[00-知识库管理/_assets/figures/architecture/fig-attention-multihead-budget-v1.svg|900]]

> [!figure] 图 40.4-05　多头投影、拼接与参数/存储预算
> 左栏展示分头后拼接，中央推导标准四投影参数，右栏列出 head 数改变的资源。来源：依据 Transformer MHA 定义与独立 shape audit 绘制；由 [[00-知识库管理/_labs/code/plot_architecture_attention_v1.py]] 生成。

**怎样读图**：先把 $d_{model}$ 切成 $h$ 个 $d_h$ 通道，再检查 concat 恢复总宽；中央只算 projection parameters，右栏另列 score storage 与 kernel，避免把四种账混成一个数字。

**图没有证明什么**：它没有证明更多头总更强、所有 head 都有独立语义，也没有覆盖 GQA/MQA/MLA 等非标准参数化。

## 十一、常见错误

1. 把多头说成同一 attention map 的复制；
2. 固定总宽时仍让每头宽不变，却声称参数量不变；
3. 只算 $QK^\top$，漏掉 Q/K/V/O 投影；
4. 因 FLOP 主阶对 $h$ 消去，就说 memory/latency 不变；
5. 把 head 编号当可跨 seed 比较的语义；
6. 用单头剪枝实验证明所有头理论冗余；
7. 把 attention heatmap 多样性等同功能多样性；
8. 对 GQA/MQA 沿用 $4d^2$ 而不重算。

## 十二、掌握标准

> [!summary]
> - MHA 是独立投影、逐头寻址、拼接和输出混合；
> - 标准固定总宽参数量约 $4d^2$，不随 $h$ 主阶增长；
> - 每头宽、score 存储、kernel 与训练后利用率仍随 head 设计变化；
> - 表达瓶颈与剪枝结果都必须保留模型和实验条件。

能写出 packed shapes（A/B）、推导参数/FLOP/memory（C）、构造“更多头反而每头过窄”的边界（D），并设计 head pruning/function audit（E）。

## 十三、练习与独立详解

- [[习题 - Multi-Head Attention、投影子空间与参数量]]
- [[解答 - Multi-Head Attention、投影子空间与参数量]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2020-Bhojanapalli-LowRank-Attention]]
- [[S-2019-Michel-Head-Pruning]]
- [[S-2022-Su-8934-FLASH-GLU-GAU]]
