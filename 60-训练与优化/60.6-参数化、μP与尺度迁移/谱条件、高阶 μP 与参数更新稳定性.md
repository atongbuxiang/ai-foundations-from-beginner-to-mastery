---
type: derivation
status: verified
area: [training, optimization, mup, spectral-norm, width-depth]
node_id: TRN-47
aliases: [Spectral μP, 高阶 μP]
prerequisites: ["[[Embedding、Readout、Attention 与特殊参数组缩放]]", "[[矩阵范数]]", "[[矩阵梯度、谱核范数对偶与 Matrix Sign]]"]
related: ["[[模型尺度、稳定性指标与 Width-Depth 对象合同]]", "[[Scale-up 协议、μP 证据与失效边界]]", "[[权重衰减、尺度不变性与 Weight RMS 动力学]]"]
sources: ["[[S-2025-Su-10795-高阶MuP]]", "[[S-2025-Su-11340-MuP之上1]]", "[[S-2026-Su-11605-MuP之上2]]", "[[S-2026-Su-11647-MuP之上3]]", "[[S-2026-Su-11729-MuP之上4]]", "[[S-2026-Su-11549-各向同性]]", "[[S-2026-Zheng-Spectral-MuP-Width-Depth]]"]
exercises: ["[[习题 - 谱条件、高阶 μP 与参数更新稳定性]]"]
solutions: ["[[解答 - 谱条件、高阶 μP 与参数更新稳定性]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-spectral-mup-width-depth-stability-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 谱条件、高阶 μP 与参数更新稳定性

> [!abstract] 一句话结论
> 坐标 RMS/方差回答“典型随机方向如何缩放”，谱范数回答“最坏输入方向能被放大多少”。高阶 μP 试图让权重和每步更新在 operator geometry 中同时保持正确 width/aspect/depth 尺度；它能发现均方账本漏掉的低秩对齐与极端形状风险，但不能替代数据分布、有限宽和训练结果证据。

## 一、从向量 RMS 推到矩阵谱条件

仍用行向量约定

$$
y=xW,
\qquad
W\in\mathbb R^{d_{in}\times d_{out}}.
\tag{1}
$$

若输入坐标 RMS 为 $O(1)$，则

$$
\lVert x\rVert_2=\Theta(\sqrt{d_{in}}).
\tag{2}
$$

若希望输出坐标 RMS 也为 $O(1)$，则目标输出向量尺度是

$$
\lVert y\rVert_2=\Theta(\sqrt{d_{out}}).
\tag{3}
$$

由

$$
\lVert xW\rVert_2
\le\lVert x\rVert_2\lVert W\rVert_2,
\tag{4}
$$

一个自然 operator 比率是

$$
\lVert W\rVert_2
=\Theta\!\left(
\sqrt{\frac{d_{out}}{d_{in}}}
\right).
\tag{5}
$$

同理，若希望一步 feature update $x\Delta W$ 也具有输出向量的正确量级，可要求

$$
\lVert\Delta W\rVert_2
=\Theta\!\left(
\sqrt{\frac{d_{out}}{d_{in}}}
\right)
\tag{6}
$$

乘一个与 width 无关、可由 base LR 调节的常数。

[[S-2025-Su-10795-高阶MuP]] 用这一类谱条件统一整理线性层；“$\Theta$”仍绑定输入输出 RMS 约定、矩阵方向和固定 aspect-ratio 路径。

## 二、从 Gaussian 初始化反推 Entry Std

对 $m\times n$ iid Gaussian matrix，典型谱范数近似同阶于

$$
\lVert W\rVert_2
\asymp \sigma(\sqrt m+\sqrt n),
\tag{7}
$$

其中 $\sigma$ 是 entry standard deviation。取 $m=d_{in},n=d_{out}$，若要匹配式 (5)，可令

$$
\sigma
\asymp
\frac{
\sqrt{d_{out}/d_{in}}
}{
\sqrt{d_{in}}+\sqrt{d_{out}}
}.
\tag{8}
$$

当 $d_{in}\asymp d_{out}\asymp n$ 时，式 (8) 仍是 $\Theta(n^{-1/2})$，与 fan-in variance 同阶；但当 aspect ratio 极端时，常数和比例行为不同。

> [!warning] 式 (7) 的身份
> 它是随机矩阵典型尺度，不是任意确定矩阵的等式；有限尺寸、非 Gaussian、结构化矩阵和训练后相关性都需另外检查。

## 三、同样的 Entry RMS 可以有完全不同的谱风险

考虑两个 $n\times n$ 矩阵。

### Rank-one 对齐矩阵

$$
A=\frac1n\mathbf1\mathbf1^\top.
\tag{9}
$$

每个 entry 都是 $1/n$，所以

$$
\operatorname{RMS}_{entry}(A)=1/n,
\tag{10}
$$

但唯一非零奇异值为 1：

$$
\lVert A\rVert_2=1.
\tag{11}
$$

### 随机符号矩阵

令 $B_{ij}=\varepsilon_{ij}/n$，$\varepsilon_{ij}\in\{-1,1\}$ iid。它也有 entry RMS $1/n$，但典型

$$
\lVert B\rVert_2=\Theta(n^{-1/2}).
\tag{12}
$$

两者的 entry RMS 完全一样，operator norm 相差 $\sqrt n$。梯度外积更新天然偏低秩和对齐，所以只看 entry RMS 很容易低估 feature worst-case change。

这也解释为何“更新每个坐标是 $1/n$”不能独立保证谱更新正确；还要看 rank、奇异谱和输入所处子空间。

## 四、Typical 与 Worst-case 不是竞争关系

设输入 covariance 为

$$
\Sigma_x=\mathbb E[x^\top x].
\tag{13}
$$

平均输出能量为

$$
\mathbb E\lVert xW\rVert_2^2
=\operatorname{tr}(W^\top\Sigma_xW).
\tag{14}
$$

若 $\Sigma_x\approx cI$，它更接近 Frobenius/平均奇异值控制；若数据集中在 top singular vector，operator norm 决定实际放大。于是至少分三层：

1. entry/vector RMS：坐标典型尺度；
2. data-weighted quadratic：数据分布上的平均尺度；
3. spectral norm：所有单位输入上的 supremum。

[[S-2026-Su-11549-各向同性]] 的几何接口说明：当 feature covariance 近似 isotropic，参数-space 与 feature-space 的最速方向更可能对齐；但有限 batch rank、非零谱和梯度子空间必须明示。

## 五、谱更新与 Norm-dependent Steepest Descent

若允许更新满足

$$
\lVert\Delta W\rVert_2\le\rho,
\tag{15}
$$

局部线性目标是

$$
\min_{\lVert\Delta W\rVert_2\le\rho}
\langle G,\Delta W\rangle_F.
\tag{16}
$$

谱范数的对偶是核范数，因此最优值为

$$
-\rho\lVert G\rVert_*,
\tag{17}
$$

一个最速方向由 $G=U\Sigma V^\top$ 的 polar/矩阵符号型因子给出：

$$
\Delta W^*=-\rho UV^\top
\tag{18}
$$

（秩亏时在相应子空间理解）。[[S-2026-Su-11605-MuP之上2]] 把这种谱几何与 MuP-style shape scale 相连。

但要严格区分：

- μP：跨宽度 parameterization/update-scale 合同；
- Muon/msign：一种矩阵更新 direction geometry；
- shape multiplier：把 direction 调到式 (6) 的 operator scale；
- 有限步 Newton–Schulz：近似该 direction 的数值算法。

它们可以组合，却不是同一个对象。

## 六、训练中参数范数也会漂移

初始化满足式 (5) 不代表

$$
\lVert W_t\rVert_2
=\Theta\!\left(\sqrt{d_{out}/d_{in}}\right)
\tag{19}
$$

对整个训练时域成立，因为

$$
W_t=W_0+\sum_{s<t}\Delta W_s.
\tag{20}
$$

即使每步 $\lVert\Delta W_s\rVert_2$ 有界，同向累积仍可随 $t$ 线性增长；相消时则可能只按 $\sqrt t$ 或更慢增长。

[[S-2026-Su-11729-MuP之上4]] 提出两类候选干预：

- Post Clip：先更新，再把参数投影/裁剪回允许集合；
- Pre Decay：在更新前用 decay 抵消逼近边界的径向分量。

谱版本可涉及 singular-value clipping 或 spectral weight decay。课程把它们视为需实验验证的控制器，因为：

- 精确投影可能昂贵；
- 近似谱估计有误差和滞后；
- 投影会改变 optimizer 动力学和隐式偏置；
- 范数稳定不自动提高 loss 或泛化。

## 七、Width–Depth 联合条件

对 residual network

$$
h_{\ell+1}=h_\ell+\alpha_{L}F_\ell(h_\ell;W_\ell),
\tag{21}
$$

单层谱条件还要经过 $L$ 层累积。粗略最坏界为

$$
\lVert\Delta h_L\rVert
\lesssim
\sum_{\ell=1}^L
\alpha_L
\lVert J_{\ell+1:L}\rVert_2
\lVert\Delta F_\ell\rVert.
\tag{22}
$$

因此需要同时控制：

- branch update 的 width scale；
- residual multiplier $\alpha_L$；
- downstream Jacobian products；
- 不同层更新的相关性；
- training step 随 $L,n$ 的变化。

[[S-2026-Zheng-Spectral-MuP-Width-Depth]] 在特定 residual/GPT-2-style 设置中提出统一谱 width–depth 条件，并映射到若干 optimizer。它是 2026 前沿预印本：正文采用其问题分解和论文内结果，但不外推为 MoE、所有 attention/norm、任意深度路径和长期训练的既定定理。

## 八、谱条件的有限宽遥测

对每个矩阵参数组，至少记录：

$$
S_W=\frac{\lVert W\rVert_2}
{\sqrt{d_{out}/d_{in}}},
\qquad
S_\Delta=\frac{\lVert\Delta W\rVert_2}
{\sqrt{d_{out}/d_{in}}},
\tag{23}
$$

$$
r_{eff}(W)=
\frac{\lVert W\rVert_F^2}{\lVert W\rVert_2^2},
\qquad
\rho_{top}=\frac{\sigma_1^2}{\sum_i\sigma_i^2}.
\tag{24}
$$

并与

$$
\operatorname{RMS}_{entry}(W),
\quad
\operatorname{RMS}_{entry}(\Delta W),
\quad
\operatorname{RMS}(x\Delta W)
\tag{25}
$$

一起看。若 entry update 水平而 $S_\Delta$ 随 width 增长，说明低秩/对齐谱风险被 RMS 隐藏。

谱范数可用 SVD 或 power iteration 估计；报告 iteration、residual、warm start、dtype 和失败，不把单步估计当真值。

## 九、图：RMS、谱与深度累积的三道门

先看图回答：为什么所有层的 update-entry RMS 都水平，深网仍可能随 width/depth 失稳？

![[00-知识库管理/_assets/figures/training-optimization/fig-spectral-mup-width-depth-stability-v1.svg|880]]

> [!figure] 图 TRN-47　坐标尺度、谱尺度与 Width–Depth 累积
> 左侧用 rank-one 与随机符号矩阵展示相同 entry RMS、不同 operator norm；中间将 $\lVert W\rVert_2$ 与 $\lVert\Delta W\rVert_2$ 归一到输入输出维度比；右侧把 residual multiplier、Jacobian 与层间相关性加入 depth 累积。来源：依据 [[S-2025-Su-10795-高阶MuP]]、[[S-2026-Su-11605-MuP之上2]] 与 [[S-2026-Zheng-Spectral-MuP-Width-Depth]] 原创绘制。

**怎样读图**：先用 coordinate/data-weighted 统计描述典型输入，再用 spectral norm 检查最坏方向，最后沿 depth 路径检查这些更新怎样累积；任一层通过都不能替代另外两层。

**图没有证明什么**：谱条件有界不是训练性能或泛化的充分条件；2026 width–depth 扩展仍限定于其论文模型与假设。

## 十、常见错误

1. **Entry RMS 稳定即 operator 稳定**：rank-one 反例否定；
2. **谱范数越小越好**：过小会导致表示/更新消失；
3. **固定 aspect ratio 规则外推极端矩形**：需重算式 (5)—(8)；
4. **每步有界即长期有界**：同向累积可增长；
5. **Muon 等于 μP**：更新方向与参数化分层；
6. **初始化谱正确即训练谱正确**：记录 $W_t$ 与 $\Delta W_t$；
7. **投影不影响训练**：它改变轨迹和 estimator；
8. **近期预印本即普遍定理**：标记架构/optimizer/时域边界。

## 十一、初学者自检

1. 式 (5) 怎样由输入、输出向量的自然 Euclidean 尺度得到？
2. 为什么 rank-one $A$ 与随机符号 $B$ 的 entry RMS 相同而谱范数不同？
3. data-weighted quadratic 与 operator supremum 分别回答什么？
4. 谱范数球下最速方向为什么与核范数对偶有关？
5. 单步 $\lVert\Delta W\rVert_2$ 有界为何不保证 $\lVert W_t\rVert_2$ 长期有界？
6. width–depth 联合扩展为何必须加入 residual/Jacobian 累积？

## 十二、本节出口

你应能建立三层稳定账：

$$
\text{coordinate RMS}
\to\text{data-weighted feature change}
\to\text{operator worst case}
\to\text{depth accumulation},
$$

并把“谱稳定”“参数稳定”“训练更好”写成三个不同证据等级。
