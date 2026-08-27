---
type: theorem
status: draft
area: [learning-theory/empirical-process, learning-theory/loss-composition]
aliases: [Rademacher Contraction Lemma, Talagrand Contraction, Lipschitz Contraction]
node_id: LT-27
prerequisites: ["[[Rademacher 复杂度与经验复杂度]]", "[[光滑性、强凸性与条件数]]", "[[损失、总体风险与经验风险]]"]
related: ["[[范数约束线性类的复杂度]]", "[[分类间隔、Margin Bound 与 SVM 接口]]", "[[Fat-Shattering、回归与 Lipschitz 风险]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
sources: ["[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]"]
exercises: ["[[习题 - 收缩引理与 Lipschitz 损失复合]]"]
solutions: ["[[解答 - 收缩引理与 Lipschitz 损失复合]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-contraction-lipschitz-loss-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 收缩引理与 Lipschitz 损失复合

> [!abstract] 本章主问题
> Rademacher complexity 常先对 score/prediction class $\mathcal F$ 可计算，而风险属于 loss class
> $$
> \Phi\circ\mathcal F
> =\{z_i\mapsto\phi_i(f(z_i)):f\in\mathcal F\}.
> $$
> 若每个 $\phi_i$ 在相关值域上 $L$-Lipschitz，中心化后 contraction lemma 给出一条安全版本
> $$
> \widehat{\mathfrak R}_S(\Phi\circ\mathcal F)
> \le2L\widehat{\mathfrak R}_S(\mathcal F).
> $$
> 某些统一 scalar map、symmetric/absolute convention 下可把常数 2 sharpen 为 1；本课程不跨 convention 偷换常数。绝对损失、hinge 与 logistic margin loss 有全局有限 Lipschitz 常数；平方损失只在 bounded predictions/labels 上 Lipschitz；softmax cross-entropy 是 vector-valued composition，需要 logit geometry 与向量收缩。

> [!question] 初学者读完必须能回答
> 1. 为什么必须先把 $\phi_i(0)$ 减掉，减掉后复杂度为何不变？
> 2. Lipschitz constant 控制的是函数值差，怎样限制随机 signs 的最大相关？
> 3. hinge、logistic、absolute 与 squared loss 的 $L$ 分别是多少或依赖什么？
> 4. margin ramp 为什么支付 $1/\gamma$？
> 5. scalar contraction 为什么不能直接用于 $K$ 维 logits 的 softmax CE？

## 一、学习目标

1. 陈述 coordinate-wise contraction lemma 并对齐 convention；
2. 解释 centering 与 translation invariance；
3. 将 score-class complexity 合法传递到 loss class；
4. 计算常见 scalar losses 的 Lipschitz 常数；
5. 识别 bounded interval 与 global Lipschitz 的差异；
6. 由 contraction + Rademacher risk bound 推出显式风险证书；
7. 区分 generalization of surrogate 与 task-risk calibration；
8. 说明 vector contraction、tail control 与 shift 不由 scalar lemma负责。

## 二、为什么 Prediction Complexity 还不够

设监督样本

$$
S=((X_1,Y_1),\ldots,(X_m,Y_m)).
$$

score class

$$
\mathcal F\subseteq\mathbb R^{\mathcal X}
$$

的 empirical complexity 使用 $f(X_i)$。但风险使用

$$
\ell(f(X_i),Y_i).
$$

条件于样本，可把每个 label 固定进 coordinate map：

$$
\phi_i(t)=\ell(t,Y_i).
$$

loss restriction vector 是

$$
(\phi_1(f(X_1)),\ldots,\phi_m(f(X_m))).
$$

我们要回答：对同一个 $f$ 的逐坐标 Lipschitz 变换会把 sign-fitting capacity 放大多少？

## 三、正式收缩引理

设 $A\subseteq\mathbb R^m$ 是 score restriction set：

$$
A=\{(f(X_1),\ldots,f(X_m)):f\in\mathcal F\}.
$$

对每个 $i$，令 $\phi_i:\mathbb R\to\mathbb R$ 满足

$$
|\phi_i(u)-\phi_i(v)|\le L|u-v|.
$$

> [!lemma] Coordinate-wise contraction（本课程安全常数版）
> 若 $\phi_i(0)=0$，则在 signed $1/m$ convention 下，
> $$
> \boxed{
> \mathbb E_\sigma\sup_{a\in A}
> \frac1m\sum_i\sigma_i\phi_i(a_i)
> \le
> 2L\,
> \mathbb E_\sigma\sup_{a\in A}
> \frac1m\sum_i\sigma_i a_i.
> }
> $$

因此

$$
\widehat{\mathfrak R}_S(\Phi\circ\mathcal F)
\le2L\widehat{\mathfrak R}_{S_X}(\mathcal F).
$$

### 3.1 关于常数 2

若使用统一 scalar contraction、absolute/symmetric class 或更强版本的 contraction principle，常可写成 $L$ 而非 $2L$。本节选择 $2L$ 是为了覆盖一般 coordinate maps 和 signed convention。应用时可以引用更 sharp lemma，但必须把完整假设和定义一起替换。

## 四、为什么可以中心化

若 $\phi_i(0)\ne0$，定义

$$
\psi_i(t)=\phi_i(t)-\phi_i(0).
$$

则 $\psi_i(0)=0$，且 Lipschitz constant 不变。对固定样本：

$$
\begin{aligned}
&\mathbb E_\sigma\sup_f
\frac1m\sum_i\sigma_i\phi_i(f(X_i))\\
&=
\mathbb E_\sigma\sup_f
\left[
\frac1m\sum_i\sigma_i\psi_i(f(X_i))
+\frac1m\sum_i\sigma_i\phi_i(0)
\right].
\end{aligned}
$$

第二项不依赖 $f$，可移出 supremum，其 $\sigma$ expectation 为 0。因此

$$
\widehat{\mathfrak R}_S(\Phi\circ\mathcal F)
=
\widehat{\mathfrak R}_S(\Psi\circ\mathcal F).
$$

centering 不改变 signed complexity，却使 contraction lemma 的零点条件成立。

## 五、证明机制：逐坐标替换

完整 contraction proof 常用 induction/conditioning。核心一坐标步骤如下。

固定除 $\sigma_i$ 外的 signs。对每个 restriction $a\in A$，把其他坐标贡献记为

$$
C_a=\sum_{j\ne i}\sigma_j\phi_j(a_j).
$$

对 $\sigma_i$ 平均的 supremum 为

$$
\frac12\sup_a(C_a+\phi_i(a_i))
+\frac12\sup_a(C_a-\phi_i(a_i)).
$$

分别取近似 maximizers $a^+,a^-$。两项相加时，$i$ 坐标只通过

$$
\phi_i(a_i^+)-\phi_i(a_i^-)
$$

出现；Lipschitz 性把它上界为

$$
L|a_i^+-a_i^-|.
$$

再用正负线性坐标比较把 absolute difference 拆成至多两个 signed linear choices，产生安全因子 2。对 $i=1,\ldots,m$ 逐坐标替换 $\phi_i(a_i)$ 为 $L a_i$，得到结论。

> [!important] 证明真正使用的对象
> contraction 不要求 $\phi$ 凸或可微；核心是逐坐标 Lipschitz difference。若使用更特殊的 convex/monotone lemma，可得到不同常数与方向，但不能倒推一般情形。

## 六、图解：从 Score 到 Loss

先回答：**右栏哪一种 loss 的 Lipschitz 常数不能在全实轴上固定？**

![[00-知识库管理/_assets/figures/learning-theory/fig-contraction-lipschitz-loss-v2.svg|900]]

> [!figure] 图 20.4.3｜Score class、Lipschitz distortion 与常见损失合同
> 左栏表示原 score restrictions；中栏用 Lipschitz slope 控制逐坐标变换；右栏对 absolute、hinge、logistic、squared 与 softmax CE 分别标出所需条件。来源：依据 Rademacher contraction principle 独立绘制；确定性 SVG，由 [[plot_rademacher_core_v2.py]] 生成。

**怎样读图。** 收缩不是说 loss 数值变小，而是说任意两组 score 的 loss difference 不会超过 $L$ 倍 score difference，因此类追随随机 signs 的自由度不会无控制膨胀。

**适用边界（图没有证明什么）。** 图没有处理无界 loss 的 concentration、vector-valued contraction、surrogate calibration、localized Lipschitz constant 或 distribution shift；常数 2 依赖本节 convention。

## 七、常见 Scalar Loss 的 Lipschitz 常数

### 7.1 绝对损失

$$
\ell(t,y)=|t-y|.
$$

由 reverse triangle inequality：

$$
||u-y|-|v-y||\le|u-v|,
$$

故对 $t$ 是 1-Lipschitz，无需 $y$ 有界来证明 Lipschitz；但 high-probability bounded-loss theorem 仍需 loss range/tail。

### 7.2 Hinge loss

对 $y\in\{-1,+1\}$，

$$
\ell_{\rm hinge}(t,y)=(1-yt)_+.
$$

$u\mapsto u_+$ 为 1-Lipschitz，且 $t\mapsto1-yt$ slope 绝对值 1，所以 hinge 对 $t$ 1-Lipschitz。

### 7.3 Logistic margin loss

$$
\ell_{\log}(t,y)=\log(1+e^{-yt}).
$$

导数

$$
\frac{\partial\ell}{\partial t}
=-\frac{y}{1+e^{yt}},
$$

绝对值至多 1，故全局 1-Lipschitz。

### 7.4 Squared loss

$$
\ell(t,y)=(t-y)^2.
$$

差分：

$$
|(u-y)^2-(v-y)^2|
=|u-v|\,|u+v-2y|.
$$

若 $|u|,|v|,|y|\le B$，则

$$
|u+v-2y|\le4B,
$$

所以相关区间上是 $4B$-Lipschitz。若无边界，它不是全局 Lipschitz。

### 7.5 Clipped/ramp margin loss

定义 margin $u=yf(x)$，对 $\gamma>0$：

$$
\phi_\gamma(u)=
\begin{cases}
1,&u\le0,\\
1-u/\gamma,&0<u<\gamma,\\
0,&u\ge\gamma.
\end{cases}
$$

最大 slope 绝对值为 $1/\gamma$，故

$$
\widehat{\mathfrak R}(\phi_\gamma\circ y\mathcal F)
\le\frac{2}{\gamma}\widehat{\mathfrak R}(\mathcal F).
$$

$\gamma$ 越小，surrogate 越接近 0–1 indicator，却支付更大 complexity。这是 margin bound 的核心 trade-off。

## 八、从 Loss Complexity 到 Risk Bound

假设 loss 已缩放到 $[0,1]$，记

$$
\mathcal L
=\{(x,y)\mapsto\ell(f(x),y):f\in\mathcal F\}.
$$

Rademacher risk theorem 给出以至少 $1-\delta$ 的概率，对所有 $f$：

$$
P\ell_f
\le P_m\ell_f
+2\widehat{\mathfrak R}_S(\mathcal L)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
$$

若 coordinate loss 对 score 是 $L$-Lipschitz，应用本节安全收缩：

$$
\widehat{\mathfrak R}_S(\mathcal L)
\le2L\widehat{\mathfrak R}_{S_X}(\mathcal F).
$$

所以

$$
P\ell_f
\le P_m\ell_f
+4L\widehat{\mathfrak R}_{S_X}(\mathcal F)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
$$

这是有效但未必最 sharp 的 convention-consistent bound。若调用 factor-1 contraction，可把 $4L$ 改成 $2L$；必须整条证明一起更新。

## 九、乘以 Binary Label 不改变 Complexity

margin class

$$
y\mathcal F
=\{(x,y)\mapsto yf(x):f\in\mathcal F\}
$$

在固定 sample 上满足

$$
\widehat{\mathfrak R}_S(y\mathcal F)
=
\mathbb E_\sigma\sup_f\frac1m\sum_i\sigma_iY_if(X_i).
$$

因为固定 $Y_i\in\{-1,+1\}$ 时 $(\sigma_iY_i)$ 仍是 iid Rademacher signs，

$$
\widehat{\mathfrak R}_S(y\mathcal F)
=\widehat{\mathfrak R}_{S_X}(\mathcal F).
$$

这允许先分析 real-valued score class，再用 margin loss contraction。

## 十、Softmax Cross-Entropy 为什么不同

multiclass score 是向量

$$
f(x)=(f_1(x),\ldots,f_K(x))\in\mathbb R^K.
$$

cross-entropy

$$
\ell(f(x),y)
=-f_y(x)+\log\sum_{k=1}^Ke^{f_k(x)}
$$

是 $\mathbb R^K\to\mathbb R$ 的 map。scalar contraction lemma只处理每坐标一个实数 $f(X_i)$，不能直接忽略 $K$ 个相关 scores。

需要：

- vector contraction inequality；
- 选择 $\ell_2/\ell_\infty$ 等 score norm 与 Lipschitz constant；
- 控制 vector-valued function class；
- 处理 logit shift invariance；
- 若 logits 无界，额外 range/tail control。

## 十一、Surrogate Generalization 不等于 Task Calibration

即使证明

$$
R_{\rm surrogate}(f)
-\inf_{g\in\mathcal F}R_{\rm surrogate}(g)
$$

很小，也不能自动推出 0–1/task excess 小。还需 calibration function，例如某些 binary proper/convex losses满足

$$
R_{01}(h_f)-R_{01}^*
\le\Psi^{-1}\left(
R_{\rm surr}(f)-R_{\rm surr}^*
\right).
$$

contraction 只承担 empirical-to-population 的 complexity 传递，不承担 surrogate-to-task 的 decision-theoretic bridge。

## 十二、Local Lipschitz 与范围审计

若 loss 只在模型实际输出区间 $[-B,B]$ 上 Lipschitz，可：

1. 证明所有候选 outputs 确实落在该区间；
2. 显式 clip outputs，并把 clipping bias 计入；
3. 使用 high-probability output envelope 与额外 failure budget；
4. 采用 local contraction/variance-sensitive 工具。

不能从训练样本上观察到 logits 都不大，就无条件宣称整个 class 在 sample 外有同一 range。

## 十三、AI 中的对象映射

### 13.1 Robust regression

Huber loss 在中心区平方、尾部线性。其全局 Lipschitz constant由 clipping threshold 控制，但 bounded loss/concentration 仍需 residual tail 或 loss clipping。

### 13.2 Contrastive loss

InfoNCE 一个样本项依赖 batch 内多个 scores，且 log-sum-exp 是 vector map。需要定义 batch-level function class和 vector contraction，不能逐 pair 套 scalar lemma。

### 13.3 Temperature

若 logits 除以 temperature $\tau$，Lipschitz constant通常按 $1/\tau$ 放大。更低温度提高 margin sharpness，也提高 complexity/concentration sensitivity；这是一项可审计数学代价。

### 13.4 Gradient clipping

optimizer gradient clipping 不等于 loss 对 predictions 的 Lipschitz constant。一个是训练动态操作，一个是函数值几何；需要 stability theorem 才能连接。

## 十四、常见错误

> [!warning] “可微且导数有限于训练点，所以全局 Lipschitz”
> 错。需在整个候选输出区间有统一导数/差分上界。

> [!warning] “平方损失是光滑的，所以是全局 Lipschitz”
> 错。smoothness 控制梯度差，Lipschitz loss 控制函数值差；平方损失梯度随 residual 无界。

> [!warning] “Contraction bound 已经控制 0–1 error”
> 它控制指定 surrogate loss class 的 generalization；task risk 还需 calibration/margin bridge。

> [!warning] “Softmax CE 对每个 logit 分别 Lipschitz，所以逐坐标套 scalar lemma”
> 多坐标共享 log-sum-exp，需 vector-valued contraction与 joint score complexity。

## 十五、本节回顾

1. $\phi_i(0)$ 为什么可减去？
2. coordinate contraction 的对象集合 $A$ 是什么？
3. safe factor 2 从哪种 general convention 来？
4. absolute、hinge、logistic 的 Lipschitz 常数为何至多 1？
5. squared loss 的 $4B$ 怎样推导？
6. margin ramp 为什么产生 $1/\gamma$？
7. surrogate risk 与 task risk 之间还缺什么？
8. temperature 怎样进入 Lipschitz/complexity ledger？

## 十六、来源与后继

- complexity 与 contraction 主线：[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]；
- 教材常数与应用：[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]；
- 下一步：[[范数约束线性类的复杂度]]给出 score complexity 的显式 dual-norm 计算；
- 训练闭环：[[习题 - 收缩引理与 Lipschitz 损失复合]]与[[解答 - 收缩引理与 Lipschitz 损失复合]]。
