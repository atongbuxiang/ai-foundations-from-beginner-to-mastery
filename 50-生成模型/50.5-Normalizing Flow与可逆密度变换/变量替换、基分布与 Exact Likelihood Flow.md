---
type: concept
status: verified
area: [generative-models, normalizing-flows, probability]
node_id: GEN-33
prerequisites: ["[[随机变量变换与密度换元]]", "[[多重积分、换元公式与积分变换]]", "[[显式密度、隐式分布与可计算性三角]]"]
related: ["[[Coupling Layer、NICE 与 RealNVP]]", "[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"]
sources: ["[[S-2018-Su-5776-NICE流模型]]", "[[S-2015-Rezende-Mohamed-Normalizing-Flows]]"]
exercises: ["[[习题 - 变量替换、基分布与 Exact Likelihood Flow]]"]
solutions: ["[[解答 - 变量替换、基分布与 Exact Likelihood Flow]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-flow-change-of-variables-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 变量替换、基分布与 Exact Likelihood Flow

> [!abstract] 一句话结论
> 一个经典 flow 用同维双射把简单基分布搬到数据空间。生成方向与编码方向是同一映射的两面，但换元公式中的 Jacobian 符号相反；所谓 exact likelihood，只是对已经声明的连续模型和预处理能够按公式评价，并不自动等于真实离散概率、数值无误差或高语义质量。

## 一、先用一维伸缩验方向

令 $Z\sim\mathcal N(0,1)$，生成映射为

$$X=g(Z)=2Z+3.$$

它的逆为 $f(x)=(x-3)/2$。区间 $[z,z+dz]$ 被拉长为约 $2dz$，概率质量不变，所以单位长度的密度变为一半：

$$
p_X(x)=p_Z\!\left(\frac{x-3}{2}\right)\frac12.
$$

若在 $x=3$ 处，$z=0$，故 $p_X(3)=p_Z(0)/2$。这是一条极好用的符号检查：空间被生成映射放大，生成密度应降低。

## 二、对象与两个等价公式

设 $Z\in\mathbb R^d$ 有相对于 Lebesgue measure 的密度 $p_Z$。令

$$
g_\theta:\mathbb R^d\to\mathbb R^d
$$

是可微双射，且逆 $f_\theta=g_\theta^{-1}$ 也可微；这种映射称为 diffeomorphism。定义 $X=g_\theta(Z)$。对任意数据点 $x$，令 $z=f_\theta(x)$，多元换元给出

$$
\boxed{\log p_X(x)=\log p_Z(f_\theta(x))+
\log\left|\det J_{f_\theta}(x)\right|.}
$$

因为 $J_f(x)=J_g(z)^{-1}$，也可写为

$$
\boxed{\log p_X(g_\theta(z))=
\log p_Z(z)-\log\left|\det J_{g_\theta}(z)\right|.}
$$

第一式适合“给定 $x$ 算 density”；第二式适合“已知生成路径 $z\mapsto x$ 记账”。绝对值不能省略，因为 orientation reversal 仍给非负密度。

### 2.1 为什么行列式出现

在小邻域内，$g$ 近似为线性映射

$$g(z+\Delta z)\approx g(z)+J_g(z)\Delta z.$$

$d$ 维微小体积被乘以 $|\det J_g(z)|$。同一概率质量分摊到更大体积，密度便除以该因子。这是“质量守恒 + 局部体积变化”，不是人为加进 loss 的 regularizer。

## 三、多层 flow 的 logdet 为什么可加

令 $h_K\circ\cdots\circ h_1$ 组成编码方向 $f$，并记 $u_0=x,u_k=h_k(u_{k-1})$。链式法则给出

$$J_f(x)=J_{h_K}(u_{K-1})\cdots J_{h_1}(x).$$

利用 $\det(AB)=\det A\det B$，

$$
\log|\det J_f(x)|=
\sum_{k=1}^K\log|\det J_{h_k}(u_{k-1})|.
$$

因此每层只要同时满足“可逆”和“便宜 logdet”，整条链便可训练。一般 dense $d\times d$ Jacobian 的 determinant 是 $O(d^3)$；flow 架构正是为绕开这个瓶颈而设计。

## 四、完整手算：二维仿射 flow

令 $z\sim\mathcal N(0,I_2)$，$x=Az+b$，其中

$$A=\begin{pmatrix}2&0\\0&1/2\end{pmatrix},\qquad b=\binom{1}{-1}.$$

$\det A=1$，所以它改变形状但保持面积。取 $x=(3,0)^\top$，

$$
z=A^{-1}(x-b)=
\begin{pmatrix}1/2&0\\0&2\end{pmatrix}
\binom{2}{1}=\binom11.
$$

于是

$$
\log p_X(x)=-\log(2\pi)-\frac12(1^2+1^2)-\log|\det A|
=-\log(2\pi)-1.
$$

检查：协方差为 $AA^\top=\operatorname{diag}(4,1/4)$，其 determinant 仍是 1，与面积守恒一致。

## 五、`exact` 究竟承诺什么

> [!definition] 本卷使用的 exact likelihood
> 给定连续变量模型、确定预处理和可逆层，log-density 可由有限个已声明的解析 logdet 组成，不需要 ELBO 或 MCMC 配分函数估计。它是模型内的可计算性陈述。

它不承诺：

- 量化像素的真实 pmf 已被精确评价；这需要[[Flow 的 Support、Dequantization、TARFLOW 与证据地图|dequantization]]；
- 浮点 determinant、inverse 和 round-trip 没有误差；
- 参数由有限数据学到真实 $p_{data}$；
- 高 likelihood 对应人类语义、良好 OOD 检测或清晰样本；
- residual/CNF 中使用近似 inverse、trace 或 solver 后仍是逐位 exact。

## 六、同维、支持与复合约束

经典 diffeomorphic flow 要求 base/data 的维度相同。若 base density 在整个 $\mathbb R^d$ 严格为正，且 $g$ 是全空间 diffeomorphism，则 $p_X(x)$ 也处处为正。它可以把不需要的区域压到极低密度，却不能得到带真正空洞或低维 support 的严格分布。这是拓扑/测度边界，不是“网络不够大”一句话可消去。

## 七、计算与实现合同

对一个 batch $x\in\mathbb R^{B\times d}$，实现至少输出：

1. latent $z=f(x)$，形状 $B\times d$；
2. 每样本 base log-density，形状 $B$；
3. 每层每样本 logdet，累加后形状 $B$；
4. `log_px = log_pz + logdet_encode`；
5. $\|g(f(x))-x\|$ 和 $\|f(g(z))-z\|$；
6. scale extrema、最小奇异值或等价条件性指标。

不能只检查 loss 下降；一个符号错的模型也可能优化出某种数值趋势。

## 八、科学空间研读框

[[S-2018-Su-5776-NICE流模型]]用“简单分布经可逆变换复杂化”进入 flow，并自然引出 coupling。课程在此补上基准测度、两个方向的严格符号、diffeomorphism 条件和 exact 的语义边界。历史方法入口还可见[[S-2015-Rezende-Mohamed-Normalizing-Flows]]。

## 九、图：一份质量—体积双向账

先看图回答：为什么生成方向的体积放大，对应编码公式中的正 logdet，却对应生成公式中的负 logdet？

![[00-知识库管理/_assets/figures/generative-models/fig-flow-change-of-variables-ledger-v1.svg|900]]

> [!figure] 图 50.5-01　Base、双射、数据密度与 Jacobian 的方向账
> 左侧小体积经 $g$ 搬到右侧；下方分别列出编码和生成公式。来源：依据多元变量替换公式独立绘制。

**怎样读图**：沿上方箭头从 $z$ 到 $x$ 看体积变化，再沿下方反向箭头用 $f$ 回到密度评价。两条公式在对应点完全等价，符号差来自 inverse determinant。

**图没有证明什么**：图只示意局部体积，不证明任意神经网络是全局双射，也不证明有限精度 inverse 稳定或模型逼近了真实数据分布。

## 十、本节回顾

- 先固定生成方向 $g$ 和编码方向 $f=g^{-1}$，再写公式；
- determinant 表示局部体积比，绝对值保证 density 非负；
- 多层 logdet 由 determinant 乘法性变成求和；
- exact likelihood 是模型内可计算性，不是数据、数值或语义的万能证书；
- 下一节用 coupling 让 Jacobian 变成块三角。

## 十一、练习与独立详解

- [[习题 - 变量替换、基分布与 Exact Likelihood Flow]]
- [[解答 - 变量替换、基分布与 Exact Likelihood Flow]]

