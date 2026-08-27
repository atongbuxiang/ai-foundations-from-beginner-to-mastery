---
type: solution
status: draft
area: [learning-theory/empirical-process, learning-theory/loss-composition]
topic: "[[习题 - 收缩引理与 Lipschitz 损失复合]]"
prerequisites: ["[[收缩引理与 Lipschitz 损失复合]]", "[[Rademacher 复杂度与经验复杂度]]"]
related: ["[[范数约束线性类的复杂度]]", "[[分类间隔、Margin Bound 与 SVM 接口]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - 收缩引理与 Lipschitz 损失复合

> [!warning] 常数约定
> 本解答沿用正文的 signed、$1/m$ empirical Rademacher complexity，以及 factor-$2$ coordinate-wise contraction 安全版本。若换用对称类、absolute complexity 或更尖锐的 contraction theorem，常数可能不同；不能只替换结论里的数字。

## A. 识别与复述

### LT-CON-A01

令 $A\subseteq\mathbb R^m$，并令每个坐标映射 $\phi_i:\mathbb R\to\mathbb R$ 满足

$$
\phi_i(0)=0,
\qquad
|\phi_i(u)-\phi_i(v)|\le L|u-v|.
$$

正文采用的安全版本是

$$
\boxed{
\mathbb E_\sigma\sup_{a\in A}
\frac1m\sum_{i=1}^m\sigma_i\phi_i(a_i)
\le
2L\,
\mathbb E_\sigma\sup_{a\in A}
\frac1m\sum_{i=1}^m\sigma_i a_i.}
$$

对函数类 $\mathcal F$，取

$$
A=\{(f(X_1),\ldots,f(X_m)):f\in\mathcal F\},
$$

就得到 loss-composed class 的 complexity bound。

### LT-CON-A02

定义 $\psi_i(t)=\phi_i(t)-\phi_i(0)$。固定 signs 时，

$$
\sup_f\frac1m\sum_i\sigma_i\phi_i(f(X_i))
=
\sup_f\frac1m\sum_i\sigma_i\psi_i(f(X_i))
+\frac1m\sum_i\sigma_i\phi_i(0).
$$

最后一项不依赖 $f$，所以可以移出 supremum；再对 signs 取期望，因 $\mathbb E\sigma_i=0$ 而消失。故中心化不改变 signed empirical complexity，同时使 $\psi_i(0)=0$。

### LT-CON-A03

- **Loss Lipschitz：**控制 prediction 改变时 loss value 的一阶差分，$|\ell(u,y)-\ell(v,y)|\le L|u-v|$；这是 contraction 所需条件。
- **Gradient Lipschitz / smoothness：**控制梯度变化，$|\ell'(u)-\ell'(v)|\le\beta|u-v|$；它主要服务优化、stability 或二阶近似，并不自动给出 loss 本身全局 Lipschitz。
- **Bounded loss：**要求 $\ell\in[a,b]$，通常用于 concentration；Lipschitz 函数在无界输入域上仍可能无界。
- **Calibrated surrogate：**说明 surrogate excess risk 能否控制目标任务 excess risk；它是 population decision-theoretic 性质，不由 contraction 自动推出。

## B. 手算与数值判断

### LT-CON-B01

1. 绝对损失：reverse triangle inequality 给出 $L=1$。
2. Hinge：$t\mapsto(1-yt)_+$ 在 $y\in\{-1,1\}$ 时斜率绝对值不超过 $1$，故 $L=1$。
3. Binary logistic margin loss：

$$
\ell(t,y)=\log(1+e^{-yt}),
\qquad
\left|\frac{\partial\ell}{\partial t}\right|
=\frac1{1+e^{yt}}\le1,
$$

所以 $L=1$。这里给的是对 scalar score 的常数，不等同于 multiclass softmax 对某个向量范数的常数。

### LT-CON-B02

若 $|u|,|v|,|y|\le B=3$，则

$$
\frac{|(u-y)^2-(v-y)^2|}{|u-v|}
=|u+v-2y|
\le4B=12.
$$

所以可取 $L=12$。按正文 factor-$2$ contraction，

$$
\widehat{\mathfrak R}(\ell\circ\mathcal F)
\le2L\widehat{\mathfrak R}(\mathcal F)
=2\times12\times0.02
=\boxed{0.48}.
$$

这只是 complexity 项；若要风险证书，还需 loss range/tail 与 confidence 项。

### LT-CON-B03

margin ramp 的 Lipschitz constant 为 $L=1/\gamma$。当 $\gamma=0.25$ 时，$L=4$，因此

$$
2L\widehat{\mathfrak R}(\mathcal F)
=2\times4\times0.03
=\boxed{0.24}.
$$

若 $\gamma$ 减半到 $0.125$，则 $L$ 加倍为 $8$，上界也加倍为 $0.48$。更窄的 margin transition 更接近 $0$-$1$ loss，却提高 uniform convergence 代价，这正是 approximation–estimation trade-off。

## C. 推导与证明

### LT-CON-C01

由 $\phi_i=\psi_i+\phi_i(0)$，固定 $S,\sigma$ 后有

$$
\begin{aligned}
&\sup_f\frac1m\sum_i\sigma_i\phi_i(f(X_i))\\
&=\sup_f\left[
\frac1m\sum_i\sigma_i\psi_i(f(X_i))
+\frac1m\sum_i\sigma_i\phi_i(0)
\right]\\
&=\sup_f\frac1m\sum_i\sigma_i\psi_i(f(X_i))
+\frac1m\sum_i\sigma_i\phi_i(0).
\end{aligned}
$$

第二个等号成立是因为后项与 $f$ 无关。对 $\sigma$ 取期望：

$$
\mathbb E_\sigma\frac1m\sum_i\sigma_i\phi_i(0)
=\frac1m\sum_i\phi_i(0)\mathbb E\sigma_i=0.
$$

于是两种 composed class 的 signed empirical complexity 相等。

### LT-CON-C02

固定除 $\sigma_i$ 外的 signs，并把其余坐标贡献记作 $C_a$。对第 $i$ 个 sign 平均后，表达式包含

$$
\frac12\sup_a(C_a+\phi_i(a_i))
+\frac12\sup_a(C_a-\phi_i(a_i)).
$$

选择两项的近似 maximizers $a^+,a^-$，非线性部分只以

$$
\phi_i(a_i^+)-\phi_i(a_i^-)
$$

出现。Lipschitz 性给出

$$
|\phi_i(a_i^+)-\phi_i(a_i^-)|
\le L|a_i^+-a_i^-|.
$$

安全版本再把 absolute difference 用两个可能的 signed linear comparisons 控制，因此支付 factor $2$。逐坐标 induction 把所有 $\phi_i(a_i)$ 替换为线性坐标并得到定理。factor $2$ 来自这一步的一般 signed-coordinate 比较；在附加对称性或更尖锐 lemma 下可以改善。

### LT-CON-C03

设 loss class

$$
\mathcal G=\{(x,y)\mapsto\ell(f(x),y):f\in\mathcal F\}
$$

的函数值落在 $[0,1]$。经验 Rademacher 风险定理给出：以至少 $1-\delta$ 的概率，对所有 $f$，

$$
P\ell_f
\le P_m\ell_f
+2\widehat{\mathfrak R}_S(\mathcal G)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
$$

若对每个固定 label 的 scalar map $t\mapsto\ell(t,y)$ 都是 $L$-Lipschitz，则先中心化，再用 factor-$2$ contraction：

$$
\widehat{\mathfrak R}_S(\mathcal G)
\le2L\widehat{\mathfrak R}_{S_X}(\mathcal F).
$$

代回即得

$$
\boxed{
P\ell_f
\le P_m\ell_f
+4L\widehat{\mathfrak R}_{S_X}(\mathcal F)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.}
$$

所需条件包括：样本 iid；函数类与样本单位定义明确；loss range 为 $[0,1]$（或先按区间长度重标度）；相关 prediction 值域上的统一 $L$；与 theorem 相同的 complexity convention；且 scalar composition 适用。若 loss 无界或 logits 为向量，需要替换 concentration/contraction 工具。

## D. 边界、反例与纠错

### LT-CON-D01

平方损失取 $y=0$、$u=T+1$、$v=T$，则

$$
\frac{|u^2-v^2|}{|u-v|}
=2T+1.
$$

给定任意候选全局常数 $L$，只要取 $T>(L-1)/2$，差商就大于 $L$。所以 squared loss 在全实轴上不可能全局 Lipschitz；必须限制 prediction/label range，或使用局部化、moment/tail 工具。

### LT-CON-D02

对 logits $z\in\mathbb R^K$，softmax cross-entropy 是

$$
\ell(z,y)=\log\sum_{k=1}^K e^{z_k}-z_y.
$$

它不是 $K$ 个互不相干 scalar losses 的和：

- **Vector geometry：**Lipschitz constant 取决于输入使用 $\ell_2$、$\ell_\infty$ 或其他 norm，dual gradient norm也随之改变；
- **Class coupling：**$\log\sum e^{z_k}$ 把所有类别坐标耦合，不能给每坐标单独选一个 predictor 后再相加；
- **Range/shift：**CE 对共同 logit shift 不变，但 logit differences、temperature 和 score-class range 决定有效几何；高概率界还需处理 loss range/tail。

因此应使用 vector contraction 或 multiclass-specific complexity，而不是机械地对 $K$ 个坐标套 scalar lemma。

### LT-CON-D03

contraction 能证明“整个 surrogate loss class 的 population–empirical gap 小”，却没有说明 surrogate risk 与 $0$-$1$ risk 的定量关系。即便

$$
R_\ell(f)-\inf_gR_\ell(g)
$$

很小，若没有 classification calibration / Bayes consistency theorem，就不能推出

$$
R_{01}(f)-R_{01}^*
$$

也小。缺少的是 calibration function（常写作 $\psi$-transform）或 task-specific regret-transfer theorem；它与 generalization bound 是两段独立接口。

## E. AI 迁移

### LT-CON-E01

若 loss 作用于 $t/\tau$，链式差分使 prediction-to-loss Lipschitz constant 通常变为原来的 $L/\tau$。因此较低 temperature $\tau$ 会按 $1/\tau$ 放大 contraction complexity 项。对 softmax 还要指定 logit norm 并使用 vector contraction；不能只写“温度越低越难泛化”，因为 realized margins、optimization 与 representation 也会同时改变。

### LT-CON-E02

gradient clipping 限制的是训练更新或 per-example parameter gradient，例如

$$
g\leftarrow g\min\{1,C/\|g\|\},
$$

而 contraction 所需 $L$ 限制的是 prediction $t$ 到 loss value 的函数差。二者一般没有直接蕴含关系。若要通过 stability 建立联系，需另外证明：参数更新对单样本替换敏感度受控；objective 对参数 smooth/strongly convex 或迭代映射 nonexpansive；参数扰动再通过 model Jacobian 转成 prediction/loss 扰动。审计时应分别记录 clipping norm/threshold、optimizer dynamics、model Jacobian bound 与 loss Lipschitz constant。

### LT-CON-E03

对一个 anchor 及 batch candidates，可把 scores 写成向量

$$
s=(s_1,\ldots,s_B),
$$

单项 InfoNCE map 为

$$
\Phi_y(s)
=-\frac{s_y}{\tau}
+\log\sum_{j=1}^B\exp\left(\frac{s_j}{\tau}\right).
$$

应用 contraction 前至少要固定：

1. score vector 上的 norm 与对应 dual norm；
2. temperature $\tau$，因为 Lipschitz scale 通常含 $1/\tau$；
3. batch sampling unit——负样本是 iid、without-replacement、in-batch dependent，还是 memory bank；
4. vector-valued score class 的 complexity；
5. 同一 example 在 batch 内多次参与造成的 dependency 与 effective sample size。

因此 InfoNCE 需要 batch/vector-level theorem，不能把每个 pair 当独立 scalar observation 后直接套正文公式。
