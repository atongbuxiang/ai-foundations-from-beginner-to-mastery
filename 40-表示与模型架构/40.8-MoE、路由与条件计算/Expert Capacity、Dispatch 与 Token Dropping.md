---
type: concept
status: draft
area: [architecture, moe, capacity, dispatch]
aliases: [Expert Capacity, Token Dispatch, Token Dropping, Dropless MoE]
node_id: ARCH-59
prerequisites: ["[[Router、Gate、Top-k 与稀疏组合]]"]
related: ["[[MoE 负载均衡辅助损失与偏置]]", "[[Expert Parallel、All-to-All 与通信成本]]"]
sources: ["[[S-2020-Lepikhin-GShard]]", "[[S-2021-Fedus-Switch-Transformer]]", "[[S-2022-Zhou-Expert-Choice]]", "[[S-2022-Gale-MegaBlocks]]"]
exercises: ["[[习题 - Expert Capacity、Dispatch 与 Token Dropping]]"]
solutions: ["[[解答 - Expert Capacity、Dispatch 与 Token Dropping]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-moe-capacity-dispatch-dropless-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Expert Capacity、Dispatch 与 Token Dropping

> [!abstract] 核心问题
> Top-k 只决定每个 token 想去哪里；真正执行前还要把不规则选择变成各专家可处理的批次。capacity 是专家队列的硬上限或调度参数。一旦发生 token dropping，它不再只是系统优化，而会改变网络函数。

## 一、用 assignment matrix 描述路由

把一个路由组内的 $T$ 个 token 与 $E$ 个专家写成二值矩阵

$$
A\in\{0,1\}^{T\times E},
\qquad A_{tj}=1\iff \text{token }t\text{ 被分给 expert }j.
$$

标准 token-choice Top-k 满足

$$
\sum_{j=1}^{E}A_{tj}=k.
$$

专家 $j$ 的到达负载为

$$
n_j=\sum_{t=1}^{T}A_{tj},
$$

总 assignment 数为

$$
\sum_{j=1}^{E}n_j=Tk.
$$

注意：即使每个 token 都有恰好 $k$ 条边，各 $n_j$ 也可能极不均匀。Top-k 是逐 token 局部决策，capacity 是 batch/路由组层面的资源约束。

## 二、capacity factor 的定义

常见固定槽位容量写成

$$
C=\left\lceil \alpha\frac{Tk}{E}\right\rceil,
$$

其中 $\alpha$ 是 capacity factor。$Tk/E$ 是完全均匀时的平均负载；$\alpha>1$ 留出偏斜余量。

若 $T=8,E=3,k=1$，平均负载为 $8/3$。取 $C=3$，而实际负载 $[4,2,2]$，第一个专家就溢出一个 token。总槽位 $EC=9$，即使只有一个溢出，其他专家仍有 $1+1$ 个空槽。

这说明 overflow 和 padding 可同时发生。

## 三、三种处理语义

### 1. Drop

只保留每专家前 $C$ 个 assignment。令

$$
\tilde A_{tj}=A_{tj}M_{tj},\qquad M_{tj}\in\{0,1\}
$$

表示是否进入容量。被丢 token 可能只走 residual path、转到备选专家或得到零 expert output。不同实现对应不同模型函数。

### 2. Pad

为每个专家分配固定 $C$ 个槽，不足时填充 dummy token。形状规整、kernel 友好，但计算的真实/槽位利用率为

$$
u=\frac{\sum_j\min(n_j,C)}{EC}.
$$

在 $[4,2,2],C=3$ 中，实际处理 $3+2+2=7$，利用率 $7/9$，且丢一个。

### 3. Dropless

所有 assignment 都执行，专家 batch 为变长。[[S-2022-Gale-MegaBlocks]] 用 block-sparse 方法让不规则专家批次更高效，避免因固定 capacity 丢 token。

“dropless”只保证不因容量删 assignment；它不保证负载均衡、通信均衡或没有 padding。块大小对齐仍可产生内部碎片，最忙专家仍决定尾延迟。

## 四、Dispatch 是一次置换加分组

概念上，每个 assignment 生成记录

$$
(j,t,w_{tj},x_t),
$$

按 expert id $j$ 排序后形成专家连续批次。专家计算

$$
o_{tj}=f_j(x_t),
$$

再按 token id 逆置换并 combine：

$$
y_t=\sum_{j:A_{tj}=1}w_{tj}o_{tj}.
$$

实现还需保存 permutation、offset、expert counts、gate weights 与 inverse permutation。若 Expert Parallel，排序之后还要把记录发送给专家 owner。

## 五、先到先得为何可能有偏

固定 capacity 下，“前 $C$ 个”由 token 顺序决定。若 batch 按 sequence 排列，后部 token 可能更容易被 drop；不同 data packing 或设备分片也会改变谁先到。

可以按 Router score 保留最高的 $C$ 个，也可以随机打散或使用优先级，但每种策略都改变：

- 被执行的 assignment；
- 训练梯度覆盖；
- 排序成本；
- 可复现性。

所以 drop policy 不是无关紧要的工程细节。

## 六、Token-choice 与 Expert-choice

token-choice 约束每个 token 恰好选 $k$ 个专家，却不保证每专家容量。Expert Choice 则让每个专家从 token 中选择固定数量：

$$
\sum_t A_{tj}=C.
$$

它天然固定专家 batch，但每 token 的被选次数

$$
r_t=\sum_j A_{tj}
$$

可能为 0、1 或多个。因而它不是“更平衡的同一个 Top-k”，而是另一模型合同。若 token 没被任何专家选中，必须定义 residual/兜底路径。

## 七、Capacity 与训练稳定性

早期训练 Router 尚未均衡时，drop rate 可能高。被 drop token 对相关专家无梯度，可能进一步形成“热门专家更热门、冷门专家更冷”的反馈。增大 $\alpha$ 会减少 drop，却增加 padding 和显存；辅助均衡可减少拥塞，却会修改优化目标。

因此至少记录：

$$
\text{drop rate},\quad \max_j n_j,\quad
\operatorname{CV}(n)=\frac{\operatorname{std}(n)}{\operatorname{mean}(n)},
\quad u.
$$

平均负载本身会隐藏尾部，应同时报告 max、p95 与时间序列。

## 八、正式图：从选择到执行

这张图回答什么问题？同一个 Top-k assignment 在 drop、pad、dropless 与 expert-choice 下为什么会变成不同计算？

![[00-知识库管理/_assets/figures/architecture/fig-moe-capacity-dispatch-dropless-v1.svg|900]]

> [!figure] 图 1｜Token-choice 队列、capacity policy 与 Expert Choice 的合同差异。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_moe_v1.py]] 生成；未复制 GShard、Switch、Expert Choice 或 MegaBlocks 原图。

**怎样读图**：A 将 8 个 token 的路由边汇入三个专家，得到 $[4,2,2]$；B 固定 $C=3$ 后分别看 drop、pad 和 dropless 对函数/布局/成本的影响；C 把“每 token 选固定数”换成“每 expert 选固定 bucket”，观察逐 token 激活数不再固定。

**图没有证明什么**：图没有证明 dropless 一定更快，也没有证明 Expert Choice 的质量优于 token-choice。二者的真实结果依 block kernel、网络、兜底路径、训练预算与任务。

## 九、最小实现测试

构造 $T=4,E=2,k=1,C=1$，强制三个 token 选择 expert 0、一个选择 expert 1。逐项验证：

1. load 为 $[3,1]$；
2. drop policy 下恰有两个 assignment 溢出；
3. padded buffer shape 为 $[E,C,d]$；
4. dropless 下处理数仍为 4；
5. inverse permutation 恢复原 token 顺序；
6. gate weight 与 token 不错位；
7. backward 只流向实际执行的专家；
8. batch 重排是否改变 drop 身份。

## 十、证据边界与学习出口

- assignment/load/capacity/利用率公式：`I`；
- 给定随机负载模型的 overflow 概率界：`T`；
- MegaBlocks 等 kernel 的吞吐：指定硬件上的 `E`；
- “dropless 改善质量是因为更多 token 得到专家计算”：需消融的 `H`；
- 不同路由合同的跨规模 Pareto：`O`。

学完本节，应能从一个小型 assignment matrix 手算负载、容量、drop 与 padding，解释 dropless 的精确定义，并指出 Expert Choice 改变了哪条行/列约束。

