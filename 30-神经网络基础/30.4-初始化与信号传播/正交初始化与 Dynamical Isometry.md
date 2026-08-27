---
type: derivation
status: draft
area: [neural-networks/initialization, orthogonal-initialization, dynamical-isometry]
aliases: [Orthogonal Initialization, Dynamical Isometry]
node_id: NN-30
prerequisites: ["[[奇异值分解]]", "[[内积空间|正交矩阵、酉矩阵与长度保持]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[相关传播、Edge of Chaos 与临界初始化]]"]
related: ["[[条件数]]", "[[局部微分、Jacobian、JVP 与 VJP]]", "[[LSUV、Fixup 与现代初始化诊断]]"]
sources: ["[[S-2014-Saxe-Deep-Linear-Dynamics]]", "[[S-2017-Pennington-Dynamical-Isometry]]", "[[S-2026-PyTorch-NN-Init]]", "[[S-2020-Su-7180-初始化几何]]"]
exercises: ["[[习题 - 正交初始化与 Dynamical Isometry]]"]
solutions: ["[[解答 - 正交初始化与 Dynamical Isometry]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-orthogonal-dynamical-isometry-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---
# 正交初始化与 Dynamical Isometry

> [!abstract] 本章主问题
> 方差递推只控制随机方向的平均平方长度；最坏方向仍可能被压到几乎 0 或放大很多倍。正交初始化把单个线性层的非零 singular values 精确设成同一 gain，提供最干净的校准基线；dynamical isometry 则要求整个输入—输出 Jacobian 的全部 relevant singular values 集中在 1 附近。两者相关，但在非线性、矩形、卷积和残差网络中绝不等价。

## 一、先从有限维 Isometry 定义开始

线性映射 $W:\mathbb R^n\to\mathbb R^m$ 是 isometry，若

$$
\|Wx\|_2=\|x\|_2
\qquad\text{对所有 }x\in\mathbb R^n.
$$

平方并比较二次型：

$$
x^TW^TWx=x^Tx\quad\forall x
\iff
\boxed{W^TW=I_n}.
$$

这要求 $m\ge n$。若 $m<n$，rank–nullity 保证存在非零 $x\in\ker W$，不可能保留所有输入方向。

## 二、方阵与矩形层的三种情形

设 $W\in\mathbb R^{m\times n}$。

| 形状 | 可满足的正交关系 | 几何含义 |
|---|---|---|
| $m=n$ | $W^TW=WW^T=I$ | 所有方向双向保长 |
| $m>n$ | $W^TW=I_n$ | columns orthonormal；嵌入保长 |
| $m<n$ | $WW^T=I_m$ | rows orthonormal；只在 row space 上保长 |

后两者常称 semi-orthogonal 或 partial isometry。不能笼统说“矩形正交矩阵保长”，必须注明保的是输入空间、输出空间还是某个子空间。

## 三、Gain 把 Singular Values 平移到 $g$

若 $Q$ 的非零 singular values 全为 1，令

$$
W=gQ,
$$

则非零 singular values 全为 $|g|$。因此

$$
\|Wx\|_2=|g|\|x\|_2
$$

只在 $Q$ 的 isometric domain 上成立。框架 API 中 `gain` 不是额外 variance correction 的模糊名称，而是直接缩放 singular spectrum；对 deep linear product，它会以 $|g|^L$ 进入尺度。

## 四、怎样生成随机正交初值

常见路线是先抽 Gaussian matrix $A$，再作 QR 或 SVD：

$$
A=QR,
$$

并修正 $R$ 对角符号，使 $Q$ 的分布不受任意 QR 符号约定影响。矩形时选具有所需 shape 的 orthonormal rows/columns。实现审计至少包括：

1. 权重张量如何 reshape 成二维矩阵；
2. 哪一边是 fan-in、哪一边是 fan-out；
3. gain 乘在哪一步；
4. 卷积 kernel 的二维 reshape 是否代表真实 convolution operator。

## 五、Deep Linear Network 的精确校准

对方阵线性深网

$$
f(x)=W_LW_{L-1}\cdots W_1x,
$$

其 Jacobian 就是

$$
J=W_LW_{L-1}\cdots W_1.
$$

若每个 $W_\ell$ 都正交且 gain 为 1，则

$$
J^TJ
=W_1^T\cdots W_L^TW_L\cdots W_1
=I.
$$

所以所有 singular values 精确等于 1。Saxe et al. 的深线性结果说明这一特殊初值可避免随 depth 增长的额外学习延迟；但这是校准模型，不是任意 nonlinear architecture 的自动结论。

## 六、非线性为什么打断精确正交性

对

$$
h^{(\ell)}=\phi(W_\ell h^{(\ell-1)}+b_\ell),
$$

局部 Jacobian 为

$$
J_\ell=D_\ell W_\ell,
\qquad
D_\ell=\operatorname{diag}(\phi'(z^{(\ell)})).
$$

全 Jacobian 是

$$
\boxed{J= D_LW_L\cdots D_1W_1}.
$$

即使每个 $W_\ell$ 正交，$D_\ell$ 也通常不是。Sigmoid/tanh 的 derivative 不同于 1；ReLU 的 $D_\ell$ 含 0/1，对 inactive units 直接删去方向。矩形 bottleneck 还会带来不可避免的 rank loss。

## 七、Dynamical Isometry 的严格层级

设 $s_1(J)\ge\cdots\ge s_r(J)>0$ 是 relevant nonzero singular values。可区分：

1. **平均平方稳定**

$$
\frac1r\sum_{i=1}^r s_i(J)^2\approx1.
$$

2. **条件数可控**

$$
\kappa(J)=\frac{s_{\max}(J)}{s_{\min}(J)}
$$

不太大。

3. **Dynamical isometry**

$$
s_i(J)\approx1
\qquad\text{对全部 relevant }i.
$$

第三条最强。例子

$$
J=\operatorname{diag}(\sqrt{2-\varepsilon^2},\varepsilon)
$$

满足平均平方 singular value 等于 1，却在 $\varepsilon\to0$ 时条件数发散。

## 八、“全部 Singular Values”也要声明子空间

若输入维度 $n$ 大于输出维度 $m$，$J\in\mathbb R^{m\times n}$ 至少有 $n-m$ 个 null directions。此时不能要求所有 $n$ 个输入方向的 singular value 都接近 1；应明确：

- 只讨论 $min(m,n)$ 个非零 singular values；
- 还是讨论数据 tangent subspace 上的 restricted Jacobian；
- 还是架构本身就设计为 dimension-preserving。

否则“dynamical isometry”会掩盖 bottleneck 的结构性信息丢失。

## 九、Orthogonal Weight 不等于 Orthogonal Convolution

卷积 kernel 常有 shape

$$
C_{\mathrm{out}}\times C_{\mathrm{in}}\times k_h\times k_w.
$$

把它 reshape 为 $C_{\mathrm{out}}\times(C_{\mathrm{in}}k_hk_w)$ 后做 orthogonal initialization，只保证这个 kernel matrix 的行/列关系；真实卷积是带 padding、stride、boundary 和 weight sharing 的巨大线性算子，其 Fourier/Toeplitz spectrum 未必 isometric。必须对实际 operator 做 JVP/VJP 或频域审计。

## 十、训练会离开 Orthogonal Manifold

普通 SGD 更新

$$
W^+=W-\eta G
$$

一般不保持 $(W^+)^TW^+=I$。因此“orthogonal initialization”只描述 $t=0$。若任务要求训练过程中保持正交，需要 retraction、Cayley/exponential parameterization 或显式 regularization；这属于优化/约束问题，不应偷渡进初始化结论。

## 十一、图：从单层谱到深层 Jacobian

先看图回答：哪一步把“每层权重正交”变成了“不足以保证全网 isometry”？平均平方 singular value 为 1 时，图中哪种病态仍可能存在？

![[00-知识库管理/_assets/figures/neural-networks/fig-orthogonal-dynamical-isometry-v2.svg|900]]

> [!figure] 图 30.4-06　Partial Isometry、非线性 Jacobian 与谱证据层级
> 左栏比较方阵、tall 与 wide semi-orthogonal map；中栏显示 $D_\ell W_\ell$ 如何把正交权重变成非平坦的全谱；右栏区分 mean-square、extreme singular values 与 dynamical isometry。来源：依据 Saxe et al. 2014、Pennington et al. 2017、PyTorch `orthogonal_` 语义及科学空间 7180 独立绘制；由 [[00-知识库管理/_labs/code/plot_initialization_advanced_v2.py]] 确定性生成。

**怎样读图**：先看矩形层究竟在哪个子空间保长，再沿中栏乘积定位 derivative mask，最后不要用右栏第一阶统计替代最小/最大 singular value。

**图没有证明什么**：图没有证明任意正交初始化都加速训练，没有证明 reshape-orthogonal convolution 是算子等距，也没有证明初始化时的谱会在 SGD 后保持。

## 十二、可复现谱诊断

对小网络可显式形成 Jacobian 并 SVD；对大网络使用 matrix-free 路线：

- JVP 估计随机方向 $\|Jv\|/\|v\|$；
- VJP 与 power iteration 估计 $s_{\max}$；
- Lanczos/随机 trace 估计 $J^TJ$ 的谱 moments；
- inverse iteration 只有在可稳定求解时才估计 $s_{\min}$；
- 按 depth、width、activation、gain、seed 与数据 batch 分层报告。

至少比较 Gaussian-Xavier、orthogonal-gain、Kaiming 与结构化 residual initialization；同时显示 mean、quantiles、extremes 与 rank，不能只给一个平均 norm。

> [!summary]
> 正交初始化精确控制单个线性矩阵的非零 singular values；dynamical isometry 控制整个输入—输出 Jacobian 的完整 relevant spectrum。非线性 derivative、矩形 bottleneck、卷积 operator 与训练更新是四个必须重新证明的断点。

- [[习题 - 正交初始化与 Dynamical Isometry]]
- [[解答 - 正交初始化与 Dynamical Isometry]]
