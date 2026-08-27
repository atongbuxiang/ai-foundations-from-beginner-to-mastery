---
type: solution
status: draft
area: [math/probability, math/statistics, ai/uncertainty]
topic: "中心极限定理与 Delta 方法"
exercise: "[[习题 - 中心极限定理与 Delta 方法]]"
prerequisites: ["[[中心极限定理与 Delta 方法]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
sources: ["MIT-6.436J-Lecture-17-LLN-CLT-Berry-Esseen", "MIT-18.655-Lecture-16-17-Delta"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 中心极限定理与 Delta 方法

> [!warning] 使用边界
> 每个答案都保留“$\xrightarrow d$”与“$\approx$”的区别。若闭卷时只会说“样本大了就正态”，应回到定理条件与标准化重新学习。

## A. 识别与复述

### PROB-CLT-A01

设 $X_1,X_2,\dots$ iid，

$$
\mathbb E[X_1]=\mu,
\qquad
0<\operatorname{Var}(X_1)=\sigma^2<\infty.
$$

令 $S_n=\sum_{i=1}^nX_i$。和形式：

$$
\frac{S_n-n\mu}{\sigma\sqrt n}
\xrightarrow d\mathcal N(0,1).
$$

样本平均形式：

$$
\sqrt n(\overline X_n-\mu)
\xrightarrow d\mathcal N(0,\sigma^2).
$$

二者由 $S_n=n\bar X_n$ 等价。

$\sigma^2<\infty$ 保证标准的 $\sqrt n$ 波动尺度与二阶特征函数展开；$\sigma^2>0$ 保证标准化分母非零。若方差为零，$X_i=\mu$ a.s.，误差恒为零而非非退化标准 Gaussian。

### PROB-CLT-A02

| 工具 | 研究对象 | 结论 | 不提供 |
|---|---|---|---|
| LLN | $\bar X_n$ | 收敛到 $\mu$ | 放大误差形状 |
| CLT | $\sqrt n(\bar X_n-\mu)$ | 渐近 Gaussian law | 当前 $n$ 严格尾界 |
| Gaussian 闭包 | Gaussian 变量的线性组合 | 有限 $n$ 精确 Gaussian | 非 Gaussian 输入的精确性 |
| Berry–Esseen | 标准化和的 CDF | 与 $\Phi$ 的最大绝对差上界 | 极端尾部相对误差 |
| 浓缩 | 有限 $n$ 偏离事件 | 显式概率上界 | 中央区域的完整 law |

关键区分：渐近分布、有限样本精确分布与有限样本不等式是三类声明。

### PROB-CLT-A03

**一维：** 若

$$
\sqrt n(T_n-\theta)\xrightarrow d Z
$$

且 $g$ 在 $\theta$ 可微，则

$$
\sqrt n[g(T_n)-g(\theta)]
\xrightarrow d g'(\theta)Z.
$$

**多元：** 若 $T_n\in\mathbb R^d$、$g:\mathbb R^d\to\mathbb R^k$，

$$
\sqrt n(T_n-\theta)
\xrightarrow d\mathcal N_d(0,\Sigma),
$$

则

$$
\sqrt n[g(T_n)-g(\theta)]
\xrightarrow d
\mathcal N_k(0,J\Sigma J^\top),
$$

其中 $J=J_g(\theta)\in\mathbb R^{k\times d}$。

若 $g'(\theta)=0$，一阶极限退化，应检查二阶项与 $n$ 尺度；边界处可能没有双侧可微邻域；不可微时没有统一线性余项，普通 Delta 证明的关键步骤断裂。

## B. 手算与构造

### PROB-CLT-B01

Binomial 均值和标准差为

$$
\mu=100\times0.5=50,
\qquad
\sigma=\sqrt{100\times0.5\times0.5}=5.
$$

整数区间 $45\le S\le55$ 做连续性修正为 $44.5\le Y\le55.5$。标准化：

$$
z_L=\frac{44.5-50}{5}=-1.1,
\qquad
z_U=\frac{55.5-50}{5}=1.1.
$$

所以

$$
P(45\le S\le55)
\approx\Phi(1.1)-\Phi(-1.1)
=2\Phi(1.1)-1.
$$

使用 $\Phi(1.1)\approx0.8643$：

$$
P(45\le S\le55)\approx0.7286.
$$

这是正态近似，不是精确 Binomial 和。

### PROB-CLT-B02

Exponential(rate $\lambda$) 有

$$
\mu=\frac1\lambda,
\qquad
\operatorname{Var}(X_i)=\frac1{\lambda^2}=\mu^2.
$$

CLT：

$$
\sqrt n(\bar X_n-\mu)
\xrightarrow d\mathcal N(0,\mu^2).
$$

取 $g(x)=\log x$，$g'(\mu)=1/\mu$。Delta：

$$
\sqrt n(\log\bar X_n-\log\mu)
\xrightarrow d\mathcal N(0,1).
$$

因此

$$
\operatorname{SE}(\log\bar X_n)\approx\frac1{\sqrt n}.
$$

数学上 Exponential 样本严格为正 a.s.，故 $\bar X_n>0$ a.s.；实现中极端 rate、低精度或数据预处理仍可能产生数值零。若把同一公式迁移到一般均值估计，必须重新确认正值定义域。

### PROB-CLT-B03

$$
g(a,b)=\frac ab,
\qquad
\nabla g(a,b)=
\begin{bmatrix}1/b\\-a/b^2\end{bmatrix}.
$$

在 $(2,4)$：

$$
v=\nabla g(2,4)=
\begin{bmatrix}1/4\\-1/8\end{bmatrix}.
$$

渐近方差为

$$
\begin{aligned}
v^\top\Sigma v
&=\left(\frac14\right)^2 4
+\left(-\frac18\right)^2 9
+2\left(\frac14\right)\left(-\frac18\right)1\\
&=\frac14+\frac9{64}-\frac1{16}\\
&=\frac{16+9-4}{64}\\
&=\frac{21}{64}.
\end{aligned}
$$

所以

$$
\sqrt n\left(\frac{A_n}{B_n}-\frac12\right)
\xrightarrow d\mathcal N\left(0,\frac{21}{64}\right).
$$

$A_n/B_n$ 的有限样本近似方差为 $21/(64n)$。若漏掉协方差交叉项，会错误得到 $25/64$。

## C. 推导与证明

### PROB-CLT-C01

设 $Y_i$ iid、均值 0、方差 1，

$$
Z_n=\frac1{\sqrt n}\sum_{i=1}^nY_i.
$$

有限二阶矩给零点附近展开

$$
\varphi_Y(u)=1-\frac{u^2}{2}+o(u^2).
$$

代入 $u=t/\sqrt n$：

$$
\varphi_Y(t/\sqrt n)
=1-\frac{t^2}{2n}+o(1/n).
$$

独立性使和的特征函数为乘积，同分布使每个因子相同：

$$
\varphi_{Z_n}(t)
=\left[\varphi_Y(t/\sqrt n)\right]^n
=\left[1-\frac{t^2}{2n}+o(1/n)\right]^n.
$$

可取对数验证极限：

$$
n\log\left(1-\frac{t^2}{2n}+o(1/n)\right)
\to-\frac{t^2}{2}.
$$

故

$$
\varphi_{Z_n}(t)\to e^{-t^2/2}.
$$

右侧是标准 Gaussian 特征函数。由 Lévy 连续性定理，$Z_n\xrightarrow d\mathcal N(0,1)$。

### PROB-CLT-C02

令

$$
Z_n=\sqrt n(\bar X_n-\mu)\in\mathbb R^d.
$$

对任意固定 $a\in\mathbb R^d$，

$$
a^\top Z_n
=\sqrt n\left[
\frac1n\sum_{i=1}^na^\top X_i-a^\top\mu
\right].
$$

标量 $a^\top X_i$ iid，均值

$$
\mathbb E[a^\top X_i]=a^\top\mu,
$$

方差

$$
\operatorname{Var}(a^\top X_i)=a^\top\Sigma a.
$$

若 $a^\top\Sigma a>0$，标量 CLT 给

$$
a^\top Z_n\xrightarrow d
\mathcal N(0,a^\top\Sigma a).
$$

若 $a^\top\Sigma a=0$，则投影中心化后为 0 a.s.，结论退化为点质量 0，也与退化 Gaussian 投影一致。

所有线性投影都趋向 $\mathcal N_d(0,\Sigma)$ 对应投影，Cramér–Wold 装置给

$$
Z_n\xrightarrow d\mathcal N_d(0,\Sigma).
$$

### PROB-CLT-C03

可微性给

$$
g(T_n)-g(\theta)
=g'(\theta)(T_n-\theta)
+r_n(T_n-\theta),
$$

其中 $r_n\xrightarrow P0$，因为 $T_n\xrightarrow P\theta$。乘 $\sqrt n$：

$$
\sqrt n[g(T_n)-g(\theta)]
=\left[g'(\theta)+r_n\right]
\sqrt n(T_n-\theta).
$$

由 Slutsky，若第二因子 $\xrightarrow dZ$，则整体 $\xrightarrow dg'(\theta)Z$。

若 $g'(\theta)=0$、$g''(\theta)\ne0$，二阶展开：

$$
g(T_n)-g(\theta)
=\frac12g''(\theta)(T_n-\theta)^2
+o_P((T_n-\theta)^2).
$$

乘 $n$：

$$
n[g(T_n)-g(\theta)]
=\frac12g''(\theta)
[\sqrt n(T_n-\theta)]^2+o_P(1).
$$

连续映射与 Slutsky 给

$$
n[g(T_n)-g(\theta)]
\xrightarrow d\frac12g''(\theta)Z^2.
$$

尺度从 $\sqrt n$ 变为 $n$，极限通常非 Gaussian。

## D. 边界、反例与纠错

### PROB-CLT-D01

若 $X_i$ iid 标准 Cauchy，其特征函数为 $e^{-|t|}$。和的特征函数：

$$
\varphi_{S_n}(t)=e^{-n|t|},
$$

所以 $S_n$ 是 scale $n$ 的 Cauchy。平均的特征函数为

$$
\varphi_{S_n/n}(t)
=\varphi_{S_n}(t/n)
=e^{-|t|},
$$

故

$$
\bar X_n\overset d=X_1
$$

对每个 $n$ 成立。它既不集中到有限均值，也不按 $\sqrt n$ 标准化趋于 Gaussian。经典 CLT 失效条件是均值/方差不存在，特别是方差无限。

### PROB-CLT-D02

$T_n=1/n>0$，所以对所有 $n$，

$$
g(T_n)=1.
$$

但

$$
g(0)=0.
$$

因此 $g(T_n)\to1$，不趋于 $g(0)$。$g$ 在 0 不连续，更不可能在 0 可微；连续映射定理与 Delta 方法的关键条件均失败。

这也说明“输入确定性收敛”仍不能穿过极限点的不连续后处理。

### PROB-CLT-D03

原断言至少有以下缺口：

1. **边缘不等于联合：** 每个坐标近似 Gaussian 不决定联合 copula；
2. **不等于独立：** 梯度坐标可有强协方差 $\Sigma_g$；
3. **不等于各向同性：** isotropic 要求 $\Sigma_g=cI$，需单独验证；
4. **固定维不等于高维：** $p$ 随 batch/模型增长时，最大值和范数需要高维 CLT；
5. **直方图不控制尾部：** 中央区看似 Gaussian 可同时有重尾或异常点；
6. **固定参数不等于训练全程：** $\theta_t$ 变化使噪声非同分布；
7. **样本可能相关：** 数据重复、增强和序列结构破坏条件 iid；
8. **有限矩可能失败：** 单样本梯度可重尾或被 clipping 改写。

可辩护的弱结论应限定固定 $\theta$、固定方向 $v$、明确抽样条件与有限协方差。

## E. AI 迁移

### PROB-CLT-E01

令

$$
\bar g_B=\frac1B\sum_{i=1}^Bg_i(\theta).
$$

固定方向 $v$ 下，单项均值和方差为

$$
\mathbb E[v^\top g_i\mid\theta]
=v^\top\nabla R(\theta),
$$

$$
\operatorname{Var}(v^\top g_i\mid\theta)
=v^\top\Sigma_gv.
$$

若该方差为正，标量 CLT：

$$
\frac{
\sqrt B\,v^\top(\bar g_B-\nabla R(\theta))
}{\sqrt{v^\top\Sigma_gv}}
\xrightarrow d\mathcal N(0,1).
$$

等价地，未标准化极限方差为 $v^\top\Sigma_gv$。

它不能自动推出：有限 $B$ 精确 Gaussian、所有方向同时近似、坐标独立、$\Sigma_g$ 各向同性、跨训练步同分布、重尾尾部准确或优化轨迹由简单 SDE 精确描述。

### PROB-CLT-E02

设

$$
\sqrt n(\bar\ell-\ell)
\xrightarrow d\mathcal N(0,\tau^2).
$$

取 $g(x)=e^x$，$g'(\ell)=e^\ell=P$。Delta 给

$$
\sqrt n(e^{\bar\ell}-e^\ell)
\xrightarrow d\mathcal N(0,P^2\tau^2).
$$

所以

$$
\operatorname{SE}(\widehat P)
\approx\widehat P\,\operatorname{SE}(\bar\ell).
$$

同一文档 token 共享主题、长度和上下文，不能视作独立样本；用 token 数会低估方差。修正方向：

1. 把文档当 cluster，使用 cluster-robust/sandwich long-run covariance；
2. 以文档为重采样单位做 cluster bootstrap；
3. 若有顺序依赖，也可估计 HAC/long-run variance。

还要明确指标是 micro token mean 还是 macro document mean，两者目标不同。

### PROB-CLT-E03

给定确定输入 $x^{(d)}$，令

$$
Y_{d,i}=W_ix_i,
\qquad
s_d^2=\sum_{i=1}^d\operatorname{Var}(Y_{d,i}).
$$

一组足够条件是：

- $W_i$ 独立、中心化；
- $0<s_d^2<\infty$，按 $s_d$ 标准化；
- Lindeberg 条件：对任意 $\varepsilon>0$，
  $$
  s_d^{-2}\sum_i
  \mathbb E[Y_{d,i}^2
  \mathbf1_{\{|Y_{d,i}|>\varepsilon s_d\}}]
  \to0;
  $$
- 常见易查充分直觉是最大单项方差占比趋零，并有适当高阶矩控制。

**单项支配反例：** 令 $x_1=1$、$x_i=0$（$i>1$），$W_1$ 为非 Gaussian、均值 0 方差 1。则

$$
h_d=W_1
$$

对所有 $d$ 不变，最大方差占比为 1，不会趋于 Gaussian。

单输入标量 CLT 只给一个 $h_d(x)$ 的边缘极限。多输入 GP 极限还需证明任意有限输入集合的联合线性组合收敛、递归传播协方差核、处理跨层依赖/非线性，并在需要函数过程收敛时加入 tightness。

## 常见错误模式

| 错误 | 为什么错 | 回链 |
|---|---|---|
| 分母用 $n$ 而非 $\sqrt n$ | 独立和的标准差按 $\sqrt n$ 增长 | [[中心极限定理与 Delta 方法#一、为什么必须中心化与标准化]] |
| CLT 当有限样本尾界 | 渐近 CDF 近似不是严格偏离上界 | [[中心极限定理与 Delta 方法#四、LLN、CLT、精确 Gaussian 与浓缩的分工]] |
| Delta 漏掉协方差交叉项 | 非线性依赖 joint 渐近 law | [[中心极限定理与 Delta 方法#十三、多元 Delta 方法]] |
| $g'(\theta)=0$ 仍报告零标准误 | 一阶退化后需二阶尺度 | [[中心极限定理与 Delta 方法#十二、导数为零：二阶 Delta 方法]] |

## 无提示重做

- [ ] 48 小时后重做 `B03/C01/C03`；
- [ ] 一周后从空白纸推导 Cauchy 反例和二阶 Delta；
- [ ] 对一个真实 AI 指标写出 cluster 单位与 Delta Jacobian。

