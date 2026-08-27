---
type: derivation
status: verified
area: [training, optimization, kfac, kronecker]
node_id: TRN-22
aliases: [Kronecker-factored Approximate Curvature, KFAC]
prerequisites: ["[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[Kronecker 积、向量化与矩阵方程]]", "[[自然梯度、KL 局部几何与坐标不变性]]"]
related: ["[[Shampoo、逆矩阵根与 Kronecker 预条件]]", "[[Hessian-vector Product、共轭梯度与隐式二阶步]]", "[[随机化低秩近似与随机 SVD]]"]
sources: ["[[S-2015-Martens-Grosse-KFAC]]", "[[S-2020-Martens-Natural-Gradient-Curvature]]", "[[S-2006-Nocedal-Wright-Numerical-Optimization]]"]
exercises: ["[[习题 - K-FAC、Kronecker 分块与阻尼合同]]"]
solutions: ["[[解答 - K-FAC、Kronecker 分块与阻尼合同]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-kfac-factor-damping-contract-v1.svg]]"
created: 2026-08-26
updated: 2026-08-27
---

# K-FAC、Kronecker 分块与阻尼合同

## 零、本页在课程中的位置

- **承接**：[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]定义了曲率对象；[[自然梯度、KL 局部几何与坐标不变性]]说明了为什么要解 Fisher 线性系统；[[Kronecker 积、向量化与矩阵方程]]提供本页使用的矩阵恒等式。
- **中心问题**：完整 Fisher block 大到无法存储时，K-FAC 怎样利用线性层梯度的结构，把一次巨大求解近似成两个较小矩阵的求解？
- **去向**：下一节[[Shampoo、逆矩阵根与 Kronecker 预条件]]会继续利用张量轴结构，但它积累的统计量、矩阵函数和几何解释与 K-FAC 不同。

> [!warning] 阅读门槛
> 如果还不能解释 Fisher block 为什么是 $\mathbb E[gg^T]$，或不知道 column-major `vec` 怎样堆叠矩阵列，请先复习上面的三个前置节点。本页会重新手算最小例子，但不会重新建立 Fisher 和 Kronecker 积的全部理论。

> [!abstract] 一句话结论
> K-FAC 不是“把 Fisher 拆成两个矩阵”这么简单：它先按层删去跨层 blocks，再利用线性层样本 gradient 的 Kronecker 结构，把乘积的期望近似为期望的乘积。可逆性来自小 factor 的分解，但 damping、EMA、inverse refresh、weight sharing 和分布式通信共同定义最终算法。

## 一、线性层为何自然出现 Kronecker 积

### 1.1 先看计算困难

设一层权重 $W\in\mathbb R^{d_{out}\times d_{in}}$，参数量为

$$
P=d_{out}d_{in}.
$$

如果直接为这一层保存完整 Fisher block，就需要一个 $P\times P$ 矩阵，也就是 $P^2$ 个数。若 $d_{in}=d_{out}=4096$，则 $P\approx1.68\times10^7$，完整 block 约有 $2.81\times10^{14}$ 个元素；即使用 FP32，也约需 $1.13$ PB 存储。问题不是“求逆技巧还不够快”，而是对象根本放不进常规训练系统。

K-FAC 的入口问题因此是：这 $P\times P$ 个二阶相关量里，是否存在可以分离的层结构？答案来自单样本梯度的外积形式。

### 1.2 对象与符号

| 符号 | 类型/维度 | 含义 |
|---|---|---|
| $a\in\mathbb R^{d_{in}}$ | 列向量 | 本层输入激活；可附加常数 1 表示 bias |
| $W\in\mathbb R^{d_{out}\times d_{in}}$ | 矩阵 | 本层权重 |
| $s=Wa\in\mathbb R^{d_{out}}$ | 列向量 | pre-activation |
| $\ell$ | 标量 | 当前样本损失 |
| $\delta=\partial\ell/\partial s\in\mathbb R^{d_{out}}$ | 列向量 | 反向传播到 pre-activation 的梯度 |
| $G=\nabla_W\ell\in\mathbb R^{d_{out}\times d_{in}}$ | 矩阵 | 单样本权重梯度 |
| $g=\operatorname{vec}(G)\in\mathbb R^P$ | 列向量 | 按列堆叠的参数梯度 |
| $A=\mathbb E[aa^T]$ | $d_{in}\times d_{in}$ | activation 二阶矩 factor |
| $S=\mathbb E[\delta\delta^T]$ | $d_{out}\times d_{out}$ | backprop 二阶矩 factor |

现在从单个元素开始推导，避免直接背诵 $\nabla_W\ell=\delta a^T$。

考虑线性/仿射层

$$
s=Wa,\qquad W\in\mathbb R^{d_{out}\times d_{in}},
$$

其中 $a$ 可已附加常数 1 以包含 bias。令

$$
\delta=\frac{\partial\ell}{\partial s}\in\mathbb R^{d_{out}}.
$$

样本 gradient 是 outer product：

$$
s_i=\sum_{j=1}^{d_{in}}W_{ij}a_j,
$$

因此对任意元素 $W_{ij}$，链式法则给出

$$
\begin{aligned}
\frac{\partial\ell}{\partial W_{ij}}
&=\sum_{k=1}^{d_{out}}
\frac{\partial\ell}{\partial s_k}
\frac{\partial s_k}{\partial W_{ij}}\\
&=\frac{\partial\ell}{\partial s_i}a_j
&&\text{因为只有 }s_i\text{ 含 }W_{ij},\\
&=\delta_i a_j.
\end{aligned}
$$

把所有 $(i,j)$ 元素排回矩阵，才得到

$$
\nabla_W\ell=\delta a^T.
$$

形状检查为

$$
(d_{out}\times1)(1\times d_{in})
=d_{out}\times d_{in},
$$

与 $W$ 的形状一致。

采用 column-major `vec` convention，

$$
\operatorname{vec}(\delta a^T)=a\otimes\delta.
$$

以 $d_{in}=d_{out}=2$ 为例：

$$
\delta a^T=
\begin{pmatrix}
\delta_1a_1&\delta_1a_2\\
\delta_2a_1&\delta_2a_2
\end{pmatrix},
$$

按列堆叠后

$$
\operatorname{vec}(\delta a^T)
=\begin{pmatrix}
\delta_1a_1\\
\delta_2a_1\\
\delta_1a_2\\
\delta_2a_2
\end{pmatrix}
=a\otimes\delta.
$$

若使用 row-major convention，因子顺序和后续恒等式会改变；所以 `vec` convention 是算法合同，不是排版细节。

其 outer product 为

$$
(a\otimes\delta)(a\otimes\delta)^T
=(aa^T)\otimes(\delta\delta^T).
$$

这一步使用两条 Kronecker 规则：

$$
(a\otimes\delta)^T=a^T\otimes\delta^T,
$$

以及 mixed-product identity

$$
(B\otimes C)(D\otimes E)=(BD)\otimes(CE).
$$

于是

$$
(a\otimes\delta)(a^T\otimes\delta^T)
=(aa^T)\otimes(\delta\delta^T).
$$

这一步是 exact algebra；近似尚未发生。

> [!intuition] 这一节真正得到什么
> 每个样本的巨大 $P\times P$ 梯度外积不是任意矩阵，而是一个 $d_{in}\times d_{in}$ activation 外积与一个 $d_{out}\times d_{out}$ backprop 外积的 Kronecker 积。K-FAC 的结构机会正来自这里。

## 二、Exact layer block 与 K-FAC factorization

上一节只处理了单个样本。曲率 block 需要对数据、标签采样或模型采样取期望；近似恰好在“取期望以后还能否保持分离”这一步出现。

对应的 Fisher/GGN layer block 形如

$$
F_W=\mathbb E[(aa^T)\otimes(\delta\delta^T)].
$$

K-FAC 用

$$
\boxed{
F_W\approx A\otimes S,\qquad
A=\mathbb E[aa^T],\qquad S=\mathbb E[\delta\delta^T]
}
$$

替代。关键近似是

$$
\mathbb E[X\otimes Y]\approx\mathbb E[X]\otimes\mathbb E[Y],
$$

也就是忽略 activation factor 与 backprop factor 的某些统计依赖。再加上 block diagonal 近似时，还删除了不同层参数 gradient 之间的 Fisher blocks。

这两类近似必须分账：

1. **跨层 block 删除**：把完整 Fisher 按层近似成 block diagonal；
2. **层内 moment factorization**：把 $\mathbb E[(aa^T)\otimes(\delta\delta^T)]$ 近似成两个期望的 Kronecker 积。

即使第二步在某层非常准确，第一步删除的跨层相关仍可能显著；反之亦然。对矩阵随机量而言，误差可写成

$$
\mathbb E\!\left[
(aa^T-A)\otimes(\delta\delta^T-S)
\right],
$$

因此“两个 factor 的均值都估得准”并不自动表示它们的乘积期望也分离得准。

> [!warning] “Activation 与 gradient 独立”是简写
> 实际 $\delta$ 由 forward activation 和 label 共同决定，严格独立通常不成立。K-FAC 使用的是有用的 moment factorization approximation；不能把名称写成已经验证的生成模型独立性。

## 三、如何应用 inverse block

结构近似的价值不只是减少存储，还在于 Kronecker 逆可以化成左右两个小 solve。

Kronecker 恒等式

$$
(A\otimes S)^{-1}=A^{-1}\otimes S^{-1}
$$

以及

$$
(A^{-1}\otimes S^{-1})\operatorname{vec}(G)
=\operatorname{vec}(S^{-1}GA^{-T})
$$

把 $d_{out}d_{in}$ 维 solve 降成两个较小矩阵的 solve 与两次 matrix multiply。

形状逐项检查：

$$
S^{-1}GA^{-T}:
(d_{out}\times d_{out})
\cdot(d_{out}\times d_{in})
\cdot(d_{in}\times d_{in}),
$$

结果仍是 $d_{out}\times d_{in}$。若 $A$ 是对称二阶矩，则 $A^{-T}=A^{-1}$；保留转置是为了准确对应一般 `vec` 恒等式。

### 3.1 对角数值例

令

$$
A=\operatorname{diag}(4,1),\qquad
S=\operatorname{diag}(9,1),\qquad
G=\begin{pmatrix}6&2\\3&1\end{pmatrix}.
$$

则

$$
S^{-1}GA^{-1}
=\begin{pmatrix}1/9&0\\0&1\end{pmatrix}
G
\begin{pmatrix}1/4&0\\0&1\end{pmatrix}
=\begin{pmatrix}1/6&2/9\\3/4&1\end{pmatrix}.
$$

同一计算也能在完整向量空间检查。此时

$$
A\otimes S=\operatorname{diag}(36,4,9,1),
\qquad
\operatorname{vec}(G)=\begin{pmatrix}6\\3\\2\\1\end{pmatrix}.
$$

逐坐标除以对角元得到

$$
(A\otimes S)^{-1}\operatorname{vec}(G)
=\begin{pmatrix}1/6\\3/4\\2/9\\1\end{pmatrix},
$$

重新排成 $2\times2$ 矩阵，正好等于 $S^{-1}GA^{-1}$。这同时检查了数值结果、`vec` 顺序和左右乘方向。

输入/输出两侧的 correlation scale 分别被校正；这不是逐元素 Adam。

## 四、状态、rank 与内存

理论上只保存两个 factor，并不表示实现只有这两块内存。要从公式走到优化器，还必须登记随时间变化的状态。

完整 block 有 $(d_{in}d_{out})^2$ 元素；K-FAC factors 只需 $d_{in}^2+d_{out}^2$。但还要计：

- factor EMA 与 inverse/eigendecomposition cache；
- momentum/update buffer；
- convolution spatial statistics；
- block splitting、padding 与 distributed replicas/shards；
- factor computation 和 communication temporary buffers。

当 $d$ 很大时 $d^2$ 仍昂贵；K-FAC 不是 $O(P)$ 状态的普遍保证。

## 五、Damping：最常被抄错的地方

即使 $A$ 和 $S$ 可逆，有限样本估计也可能病态或秩亏。Damping 的目的，是让局部求解更稳定，并限制不可信方向上的步长；但“给完整 block 加阻尼”和“分别给两个 factor 加阻尼”不是同一个矩阵。

希望的是

$$
(A\otimes S+\lambda I)^{-1}.
$$

但一般

$$
A\otimes S+\lambda I
\ne(A+\alpha I)\otimes(S+\beta I).
$$

右侧展开为

$$
A\otimes S
+\beta A\otimes I
+\alpha I\otimes S
+\alpha\beta I.
$$

即使 $\alpha\beta=\lambda$，仍多出两个 cross terms。因此 factored Tikhonov damping 是额外近似；$\pi$-adjustment 用 factor trace/average eigenvalue 平衡两侧尺度，不能称为 exact block damping。

若

$$
A=Q\operatorname{diag}(a_j)Q^T,
\qquad
S=R\operatorname{diag}(s_i)R^T,
$$

那么 $A\otimes S$ 的特征值是所有乘积 $a_js_i$。在 Kronecker eigenbasis 中，精确阻尼对应逐项除以

$$
a_js_i+\lambda,
$$

而不是除以 $(a_j+\alpha)(s_i+\beta)$。这条路径能精确处理当前近似 block 的 $+\lambda I$，但 eigendecomposition、刷新频率和有限精度成本仍属于实现合同。

## 六、三个时钟与 stale state

到目前为止的公式像是在同一时刻拥有精确 $A$、$S$ 和逆。真实训练中，统计量更新、矩阵分解和参数更新通常运行在不同频率上。

生产 K-FAC 常有：

1. 每步/每若干步更新 factor statistics；
2. 更低频计算 inverse/eigendecomposition；
3. 每个 optimizer step 应用最近的 preconditioner。

若 factor decay 为 $\rho$、inverse refresh period 为 $K$，则 preconditioner 同时有 EMA lag 与 refresh staleness。日志只写 `damping` 和 `lr` 不足以复现。

## 七、Weight sharing、卷积与序列

普通全连接层中，一个参数矩阵每个样本只调用一次；卷积和 attention 会在空间或 token 位置反复复用同一参数，于是“哪些位置算作样本”成为新的 reduction 选择。

卷积/attention 中同一参数在多个空间/token 位置复用。必须明确：

- 将位置视为额外样本还是保留 cross-location terms；
- padding/mask denominator；
- batch、sequence、spatial 三个轴如何 reduction；
- bias 是否与 activation 拼接；
- tied embedding/output weight 如何去重 state。

不同 convention 会改变 $A,S$ 的尺度，从而改变有效 LR 和 damping。

## 八、参数化性质的准确说法

Exact natural gradient 对一般光滑可逆重参数化有 infinitesimal 性质。K-FAC 在其特定 factorization 下可保留某些 layer-wise affine reparameterization 的近似/精确性质，但 block deletion、damping、EMA、finite step 和 clipping 都可能破坏。不能简写为“K-FAC 完全参数化不变”。

## 九、图：exact outer product 到近似可逆 block

先看图回答：哪一步是 vectorization 恒等式，哪一步才引入统计近似？factored damping 又额外加入什么？

![[00-知识库管理/_assets/figures/training-optimization/fig-kfac-factor-damping-contract-v1.svg|900]]

> [!figure] 图 TRN-22　K-FAC layer block、moment factorization 与 damping
> 左侧从 $\delta a^T$ 精确推出 Kronecker outer product；中间把 expectation of product 近似为 product of expectations；右侧对比 exact $A\otimes S+\lambda I$ 与 factored damping 的 cross terms，并列三种更新时钟。来源：依据 [[S-2015-Martens-Grosse-KFAC]] 独立绘制。

**怎样读图**：先把 exact algebra 和 statistical approximation 分色，再看 numerical/system approximation；三个层级的误差不能合并成一个“近似 Fisher”。

**图没有证明什么**：图不证明 activation/backprop factor 在真实网络独立，也不保证 K-FAC 的少 iteration 能抵消 factor/inverse/communication 成本。

## 十、AI 验收字段

至少保存 curvature type/label sampling、factor shapes、reduction axes、EMA、damping method/$\pi$、factor/inverse refresh、eigenvalue floors、norm constraint、momentum、parameter groups、state bytes、communication、model ratio 与 time-to-quality。

### 10.1 数学对象到训练系统的映射

| 数学对象 | 神经网络中的对象 | 最容易出错的地方 |
|---|---|---|
| $a$ | 进入当前线性层的激活 | bias 拼接、mask、token/spatial reduction |
| $\delta$ | 对 pre-activation 的反向梯度 | loss reduction、label/Fisher 采样定义 |
| $A,S$ | 两侧二阶矩及其 EMA | 归一化分母、dtype、跨设备聚合 |
| $S^{-1}GA^{-T}$ | 当前层的预条件更新方向 | damping、逆刷新、transpose/vec convention |
| $\lambda,\alpha,\beta$ | block 或 factor damping | 把 factored damping 误报为 exact damping |
| refresh clocks | 优化器的多时间尺度状态 | 日志只记录 learning rate，无法复现 |

## 十一、本节回顾与下一节接口

完成本节后，应能按顺序重建：

1. 为什么完整 layer Fisher block 的 $O(P^2)$ 存储不可承受；
2. 怎样从元素级链式法则推出 $\nabla_W\ell=\delta a^T$；
3. column-major `vec` 怎样把梯度变成 $a\otimes\delta$；
4. 哪一步是 exact Kronecker algebra，哪两步才引入 K-FAC 近似；
5. 为什么 $(A\otimes S)^{-1}$ 能化成 $S^{-1}GA^{-T}$；
6. 为什么 exact block damping 不等于 factored damping；
7. EMA、inverse refresh、weight sharing 和通信怎样改变可执行算法。

下一节[[Shampoo、逆矩阵根与 Kronecker 预条件]]也会为张量的两个轴维护矩阵状态，但它不从 Fisher layer block 的 activation/backprop moment factorization 出发。比较两者时，先比较统计对象，再比较矩阵函数，最后比较系统成本。

## 练习与独立解答

- [[习题 - K-FAC、Kronecker 分块与阻尼合同]]
- [[解答 - K-FAC、Kronecker 分块与阻尼合同]]
