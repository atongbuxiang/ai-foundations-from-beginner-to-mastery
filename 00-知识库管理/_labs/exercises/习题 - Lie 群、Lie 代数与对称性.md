---
type: exercise
status: draft
area: [math/lie-theory, math/group-theory, ai/equivariant-learning]
topic: "Lie 群、Lie 代数与对称性"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Lie 群、Lie 代数与对称性]]", "[[光滑流形、切空间与余切空间]]", "[[矩阵函数与矩阵指数]]"]
related: ["[[几何、泛函分析、核与算子基础 MOC]]", "[[练习与测验 MOC]]", "[[实验 - Lie 指数、BCH 与群平均等变审计]]"]
solution: "[[解答 - Lie 群、Lie 代数与对称性]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Lie 群、Lie 代数与对称性

> [!abstract] 训练目标
> 从“旋转不改变物体”直觉升级为可审计的 Lie theory 与 equivariant learning：能写 group/action/representation 的对象合同，能从 matrix constraint 求 algebra，能用 exponential、bracket 与 BCH 连接局部—全局，能证明 convolution、group averaging、attention 的 symmetry，并能诊断 disconnected group、boundary、sampling 与 parameter symmetry 的失效边界。

> [!warning] 作答合同
> 每次声称 invariant/equivariant，必须写出 group、input action、output action、量词范围与 residual norm；每次使用 $\exp$，必须注明 Lie/matrix/Riemannian 类型；每次从 algebra 推 global result，必须检查 connectedness、regularity 与 disconnected components。

## A. 定义、对象与边界

### GEO-LIE-A01

建立以下对象的“domain—codomain—所需结构—局部/全局边界—AI 对应物”表：

1. group multiplication/inversion；
2. Lie group left translation；
3. Lie algebra 与 bracket；
4. one-parameter subgroup 与 Lie exponential；
5. group action；
6. orbit 与 stabilizer；
7. representation 与 differential representation；
8. invariant/equivariant map；
9. Haar averaging；
10. parameter symmetry orbit。

判断并纠错：

1. 每个 group 都有非平凡 Lie algebra；
2. $\exp_G$ 总是 global bijection；
3. invariant map 不是 equivariant map；
4. 若 generator identity 成立，则对任意 disconnected group 都 global equivariant；
5. data augmentation 是 exact equivariance proof；
6. 同一 Lie algebra 唯一决定 global Lie group。

### GEO-LIE-A02

比较下列概念，每组给一个最小例子或反例：

1. abstract group、topological group、Lie group、matrix Lie group；
2. subgroup、normal subgroup、Lie subgroup；
3. faithful、free、transitive、proper action；
4. coordinate change、global symmetry、local gauge transformation；
5. input symmetry、output symmetry、parameter symmetry；
6. exact equivariance、numerical approximate equivariance、empirical robustness。

特别解释：为什么 $SO(3)$ 作用于 $S^2$ 是 transitive/effective 但不是 free？

### GEO-LIE-A03

分别为下列任务写完整 symmetry object contract：

1. rotated-image classification；
2. 3D point cloud 的 scalar energy 与 vector force prediction；
3. unordered set classification；
4. causal language modeling；
5. ReLU network 的 hidden-unit rescaling。

每项必须写：domain、group、action、feature representation、target invariant/equivariant relation、可能破缺源，以及“强制该 symmetry 是否合理”。

## B. Matrix Lie group、指数与手算

### GEO-LIE-B01

令

$$
SO(2)=\{Q\in\mathbb R^{2\times2}:Q^\top Q=I,\det Q=1\}.
$$

1. 从约束曲线 $Q(t)$ 推导 $\mathfrak{so}(2)=\operatorname{span}\{J\}$；
2. 由幂级数推导 $e^{\theta J}=R(\theta)$；
3. 证明 $R(a)R(b)=R(a+b)$、$R(\theta)^{-1}=R(-\theta)$；
4. 求 $d\exp_0$；
5. 描述 $\exp:\mathbb R J\to SO(2)$ 的 kernel，并解释不 injective；
6. 构造 local logarithm 的 branch，并说明在 $-I$ 附近的问题；
7. 给 $SO(2)$ 配 standard bi-invariant metric 时比较 Lie/Riemannian exponential。

### GEO-LIE-B02

使用 hat map $\omega\mapsto\widehat\omega$：

1. 证明 $\widehat\omega v=\omega\times v$；
2. 证明 $[\widehat\omega,\widehat\nu]=\widehat{\omega\times\nu}$；
3. 推导 $\widehat u^2=uu^\top-I$ 与 $\widehat u^3=-\widehat u$；
4. 从指数级数推 Rodrigues formula；
5. 对 $X=a\widehat e_1,Y=a\widehat e_2$ 写出 $[X,Y]$；
6. 展开到二阶，说明 $e^Xe^Y$ 与 $e^{X+Y}$ 的首个差异；
7. 解释 axis-angle 在 $\theta=0$、$\pi$ 和 $2\pi$ 附近的不同数值/拓扑问题。

### GEO-LIE-B03

令 $SE(2)$ 用 homogeneous matrices 表示：

$$
T(\theta,t)=
\begin{bmatrix}
R(\theta)&t\\0&1
\end{bmatrix}.
$$

1. 推导 group product 与 inverse；
2. 证明 translation subgroup normal，而 embedded $SO(2)$ subgroup 一般不 normal；
3. 从 $T(s)$ 的单位元曲线求 $\mathfrak{se}(2)$ 一般形式；
4. 计算两个 twists 的 commutator；
5. 解释 $SE(2)$ 为什么是 semidirect 而非 direct product；
6. 写出其对 point $x\in\mathbb R^2$ 的 infinitesimal generator；
7. 找出 origin 的 stabilizer，并比较一般非零点的 stabilizer。

## C. 定理与证明链

### GEO-LIE-C01

证明以下链条：

1. Lie group 中 $L_g,R_g$ 是 diffeomorphisms；
2. 每个 $\xi\in T_eG$ 唯一对应 left-invariant vector field；
3. left-invariant fields 对 vector-field bracket 封闭；
4. 因而 $T_eG$ 获得 Lie bracket；
5. 对 matrix group，此 bracket 等于 commutator；
6. $\operatorname{Ad}_{gh}=\operatorname{Ad}_g\operatorname{Ad}_h$；
7. $\operatorname{ad}_X(Y)=[X,Y]$。

逐步注明用了 group law、smoothness、associativity 还是 flow/differential 性质。

### GEO-LIE-C02

设 $G$ connected，smoothly 作用于 $X,Y$，$F:X\to Y$ smooth。

1. 从 global equivariance 推导
   $$dF_x(\xi_X(x))=\xi_Y(F(x));$$
2. 解释为什么它是一族 first-order differential constraints；
3. 在线性表示下化成 Jacobian equation；
4. 给出沿 one-parameter flow 的反向证明框架；
5. 明确列出反向所需的 regularity/domain 条件；
6. 用 $O(1)$ 或 $O(n)/SO(n)$ 证明仅验 algebra 不足以检查 disconnected component；
7. 设计一个同时检查 generators 与 reflection 的数值 audit。

### GEO-LIE-C03

令 finite group $G$ 在 $V_X,V_Y$ 上有 orthogonal representations，定义

$$
\mathcal P(L)=\frac1{|G|}\sum_{g\in G}
\rho_Y(g)^{-1}L\rho_X(g).
$$

1. 证明 $\mathcal P(L)$ equivariant；
2. 证明 $\mathcal P^2=\mathcal P$；
3. 在 Frobenius inner product 下证明 $\mathcal P$ self-adjoint；
4. 推出它是到 intertwiner subspace 的 orthogonal projector；
5. 对 cyclic-shift representation 证明 image 恰为 circulant matrices；
6. 分析只平均 $m<|G|$ 个元素时为何通常不 exact；
7. 解释 compact continuous group 如何改用 normalized Haar integral，noncompact group 哪里断裂。

## D. 反例、全局边界与数值审计

### GEO-LIE-D01

构造并解释以下反例：

1. 同一 Lie algebra 对应非同构 global groups；
2. Lie exponential 非 injective；
3. connected matrix Lie group 中 exponential 非必全局 surjective 的现象（可引用并解释一个标准例子）；
4. $[X,Y]\ne0$ 导致 $e^{X+Y}\ne e^Xe^Y$；
5. transitive action 非 free；
6. effective action 非 faithful representation术语混用的修正；
7. infinitesimal equivariance vacuous 但 reflection equivariance 失败。

每例说明被否定命题缺少哪项条件。

### GEO-LIE-D02

审计 finite image grid 上的 translation/rotation equivariance：

1. 证明 circular convolution 对 cyclic translations exact；
2. 给出 zero padding 破坏 equivariance 的最小一维例子；
3. 分析 stride-2 只与哪些 shifts 相容；
4. 解释 arbitrary-angle rotation 为何需要 interpolation；
5. 区分 continuous-domain theorem 与 sampled-grid implementation；
6. 提出 absolute/relative residual、group sampling 和 boundary-separated report；
7. 说明只报告平均 residual 可能隐藏什么 worst-case failure。

### GEO-LIE-D03

比较下面三种 symmetry enforcement：

1. exact equivariant architecture；
2. group-averaged/symmetrized predictor；
3. stochastic data augmentation。

对每种分析 function class、compute cost、continuous/noncompact group、finite sampling、boundary、optimization 与 task misspecification。构造一个 labels 不 invariant 的任务，证明强制 invariance 会产生不可消除误差；再构造一个 labels invariant 的任务，说明 augmentation 仍不自动给 pointwise exact invariance。

## E. AI 迁移与研究型综合

### GEO-LIE-E01

完整推导无 positional information、无 asymmetric mask 的 single-head self-attention 的 permutation equivariance：

1. 写 $X,Q,K,V$ 形状；
2. 证明 score 的 conjugation law；
3. 证明 row-softmax 的 permutation law；
4. 推出 output law；
5. 说明 multi-head、pointwise MLP、residual、per-token LayerNorm 哪些条件下保持；
6. 区分 full-sequence equivariance、fixed-query 对 key-value pairs 的 invariance、pooled classification invariance；
7. 分析 causal mask、absolute encoding、relative bias、RoPE 分别修改了何种 symmetry。

### GEO-LIE-E02

把 RoPE 组织为 representation 问题：

1. 证明 $R(m)=e^{m\theta J}$ 是 $\mathbb Z$ 的 orthogonal representation；
2. 推导 $R(m)^\top R(n)=R(n-m)$；
3. 推到多个 frequency blocks；
4. 给出二维 position $(x,y)$ 使用 commuting generators 的一种构造；
5. 说明若两个 generators 不 commute，直接写 $e^{xA+yB}$ 与分步乘积的关系；
6. 讨论 aliasing/periodicity、finite precision 与 extrapolation 边界；
7. 设计一个数值实验区分 algebraic relative property 与 downstream attention behavior。

### GEO-LIE-E03

选择一个 3D molecular、robotics pose、point-cloud 或 physical-field 任务，完成 research design memo：

1. 在 $SO(3),SE(3),O(3),E(3)$ 中选择 group，并论证是否保留 chirality/reflection；
2. 列出 input/output feature types 与 representations；
3. 写每层的 intertwiner/nonlinearity/readout contract；
4. 区分 global frame symmetry 与 local gauge/frame choice；
5. 设计 exact proof、numerical equivariance audit 与 empirical task evaluation 三层证据；
6. 纳入 sampling、neighbor graph、cutoff、boundary 与 precision；
7. 给出错误 symmetry 的反事实 baseline；
8. 解释 parameter permutation/rescaling symmetry 会怎样影响 optimization/uncertainty，但为何不等于 data equivariance。

## 作答与复盘记录

| 题号 | 首次用时 | 状态 | 主要断点 | 48 小时重做 | 14 天迁移 |
|---|---:|---|---|---|---|
| A01 |  | not-attempted |  |  |  |
| A02 |  | not-attempted |  |  |  |
| A03 |  | not-attempted |  |  |  |
| B01 |  | not-attempted |  |  |  |
| B02 |  | not-attempted |  |  |  |
| B03 |  | not-attempted |  |  |  |
| C01 |  | not-attempted |  |  |  |
| C02 |  | not-attempted |  |  |  |
| C03 |  | not-attempted |  |  |  |
| D01 |  | not-attempted |  |  |  |
| D02 |  | not-attempted |  |  |  |
| D03 |  | not-attempted |  |  |  |
| E01 |  | not-attempted |  |  |  |
| E02 |  | not-attempted |  |  |  |
| E03 |  | not-attempted |  |  |  |

> [!important] 状态语义
> 本题集已 `composed`，但学习状态仍为 `not-attempted`。只有保留首次闭卷原稿、核对独立详解、完成重做和至少一道陌生迁移题，才可据此升级正文节点状态。
