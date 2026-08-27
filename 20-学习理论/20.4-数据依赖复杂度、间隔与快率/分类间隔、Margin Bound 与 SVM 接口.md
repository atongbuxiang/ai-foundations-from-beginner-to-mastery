---
type: theorem
status: draft
area: [learning-theory/margin, classification/svm]
aliases: [Margin Bound, 分类间隔泛化界, Large-Margin Certificate]
node_id: LT-29
prerequisites: ["[[收缩引理与 Lipschitz 损失复合]]", "[[范数约束线性类的复杂度]]", "[[损失、总体风险与经验风险]]"]
related: ["[[支持向量机、最大间隔与核方法]]", "[[Boosting、弱学习与指数损失]]", "[[神经网络容量与 Norm-Based Bound]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
sources: ["[[S-2002-Koltchinskii-Panchenko-Empirical-Margins]]", "[[S-2002-Bartlett-Mendelson-Rademacher-Gaussian]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]"]
exercises: ["[[习题 - 分类间隔、Margin Bound 与 SVM 接口]]"]
solutions: ["[[解答 - 分类间隔、Margin Bound 与 SVM 接口]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-margin-ramp-risk-certificate-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 分类间隔、Margin Bound 与 SVM 接口

> [!abstract] 本章主问题
> 二分类器不仅可以问“符号是否正确”，还可以问 signed score 离决策阈值多远。对 $Y\in\{-1,+1\}$ 与 score $f$，functional margin 是
> $$
> \rho_f(X,Y)=Yf(X).
> $$
> 误分类事件是 $\{\rho_f\le0\}$。用宽度 $\gamma>0$ 的 ramp loss 把不连续 $0$-$1$ loss 上包住，再使用 Rademacher contraction，可得一条安全版本：以至少 $1-\delta$ 的概率，对所有 $f\in\mathcal F$，
> $$
> \boxed{
> P(Yf(X)\le0)
> \le
> P_m(Yf(X)\le\gamma)
> +\frac4\gamma\widehat{\mathfrak R}_{S_X}(\mathcal F)
> +3\sqrt{\frac{\log(2/\delta)}{2m}}.}
> $$
> 三项分别读取经验低间隔比例、尺度相关容量和 confidence。SVM 通过“单位 functional margin 下最小化权重范数”最大化 geometric margin，但优化问题、风险定理和 surrogate calibration 是三层不同结论。

> [!question] 初学者读完必须能回答
> 1. $Yf(X)>0$ 与 $Yf(X)\ge\gamma$ 分别说明什么？
> 2. functional margin 为什么随 score rescaling 改变，geometric margin 为什么不变？
> 3. ramp loss 怎样把 $0$-$1$ event、经验 margin distribution 与 contraction 接起来？
> 4. 为什么不能在看完数据后任意挑最漂亮的 $\gamma$ 而不付代价？
> 5. SVM 的 primal constraint 与 margin certificate 在哪里连接，又在哪里断开？

## 一、学习目标

1. 定义 signed/functional/geometric margin；
2. 证明 ramp-loss sandwich 与 $1/\gamma$-Lipschitz 性；
3. 从 Rademacher risk theorem 逐步推出 margin bound；
4. 将 norm-constrained linear complexity 代入得到显式 $BR/(\gamma\sqrt m)$ 项；
5. 推导 hard-/soft-margin SVM 的几何含义；
6. 区分 minimum margin、margin distribution 与 average surrogate loss；
7. 处理数据后选择 $\gamma$、多分类 margin 与 adversarial margin 的额外合同；
8. 识别 parameter rescaling、representation learning 与深网 norm bound 的边界。

## 二、从正确分类到 Signed Margin

设 score predictor

$$
f:\mathcal X\to\mathbb R,
$$

分类规则为

$$
h_f(x)=\operatorname{sign}(f(x)).
$$

对标签 $Y\in\{-1,+1\}$，定义

$$
\rho_f(X,Y)=Yf(X).
$$

于是：

| 情形 | 数学事件 | 含义 |
|---|---|---|
| 负 margin | $Yf(X)<0$ | 符号预测错误 |
| 零 margin | $Yf(X)=0$ | 位于决策阈值；tie convention 必须声明 |
| 小正 margin | $0<Yf(X)<\gamma$ | 分对，但轻微 score 扰动就可能翻转 |
| 大 margin | $Yf(X)\ge\gamma$ | 在 score 坐标中至少离阈值 $\gamma$ |

若把 tie 也算错，分类风险是

$$
R_{01}(f)=P(Yf(X)\le0).
$$

> [!important] Margin 是 score-dependent
> 两个函数若只给出相同符号分类器，仍可能有完全不同的 functional margin。margin theorem 控制的是带 score 结构的函数类，不只是 binary decision set。

## 三、Functional Margin 与 Geometric Margin

对 affine linear score

$$
f_{w,b}(x)=\langle w,x\rangle+b,
$$

functional margin 是

$$
\rho_i^{\rm fun}=y_i(\langle w,x_i\rangle+b).
$$

点 $x_i$ 到超平面 $\langle w,x\rangle+b=0$ 的有向欧氏距离为

$$
\rho_i^{\rm geo}
=\frac{y_i(\langle w,x_i\rangle+b)}{\|w\|_2},
\qquad w\ne0.
$$

### 3.1 为什么要除以 $\|w\|_2$

对任意 $c>0$，

$$
\operatorname{sign}(cf_{w,b}(x))
=\operatorname{sign}(f_{w,b}(x)),
$$

但 functional margin 变成

$$
c\rho_i^{\rm fun}.
$$

如果不控制 scale，可以通过把参数整体乘以巨大 $c$ 伪造任意大的 functional margin。geometric margin 则保持不变：

$$
\frac{y_i(c\langle w,x_i\rangle+cb)}{\|cw\|_2}
=\rho_i^{\rm geo}.
$$

所以 large-margin theory 必须同时有以下至少一种归一化：

- 固定 weight norm；
- 固定最小 functional margin 为 1；
- 直接使用 scale-invariant ratio $\rho/\|w\|$；
- 对一般网络使用与 score rescaling 相容的 function/norm complexity。

## 四、Ramp Loss：从不连续事件到可收缩损失

定义宽度 $\gamma>0$ 的 ramp：

$$
\phi_\gamma(u)=
\begin{cases}
1, & u\le0,\\
1-u/\gamma, & 0<u<\gamma,\\
0, & u\ge\gamma.
\end{cases}
$$

它满足两个关键性质。

### 4.1 Sandwich

逐点有

$$
\boxed{
\mathbf1\{u\le0\}
\le\phi_\gamma(u)
\le\mathbf1\{u\le\gamma\}.}
$$

证明分三段检查：

- $u\le0$：三者左两项都为 1；
- $0<u<\gamma$：左侧为 0，中间在 $(0,1)$，右侧为 1；
- $u\ge\gamma$：ramp 为 0；当 $u=\gamma$ 时右侧按“$\le$”为 1，但上界仍成立。

因此

$$
P(Yf(X)\le0)
\le P\phi_\gamma(Yf(X)).
$$

经验上又有

$$
P_m\phi_\gamma(Yf(X))
\le P_m(Yf(X)\le\gamma).
$$

### 4.2 Lipschitz constant

ramp 的各段 slope 为 $0,-1/\gamma,0$，连接处连续，所以

$$
|\phi_\gamma(u)-\phi_\gamma(v)|
\le\frac1\gamma|u-v|.
$$

这就是 complexity penalty 中出现 $1/\gamma$ 的来源。

## 五、图解：三个风险项如何组成

先回答：**把 $\gamma$ 调小，会让图中哪一项更有利、哪一项更不利？**

![[00-知识库管理/_assets/figures/learning-theory/fig-margin-ramp-risk-certificate-v2.svg|900]]

> [!figure] 图 20.4.5｜Signed margin、ramp contract 与风险证书
> 左栏区分分对与远离边界；中栏展示 ramp 对 $0$-$1$ event 的上包络及 $1/\gamma$ slope；右栏把经验低间隔率、复杂度和 confidence 分账。来源：依据 margin-distribution/Rademacher 主线独立绘制；确定性 SVG，由 [[plot_rademacher_advanced_v2.py]] 生成。

**怎样读图。** 较小 $\gamma$ 通常减少训练集中 $Y_if(X_i)\le\gamma$ 的比例，却按 $1/\gamma$ 放大 complexity penalty。定理不是“margin 越大越好”的单变量口号，而是对整条 empirical margin curve 进行 trade-off。

**适用边界（图没有证明什么）。** 图没有证明 SVM 一定最优、测试 margin distribution 与训练完全相同、deep network norm 可计算，或 adversarial/shifted distribution 下仍保持相同证书。

## 六、Margin Bound 的逐步推导

定义 margin class

$$
\mathcal M
=\{(x,y)\mapsto yf(x):f\in\mathcal F\}.
$$

由于固定样本上的 $y_i\in\{-1,+1\}$，

$$
(\sigma_i y_i)_{i=1}^m
$$

仍是一组 iid Rademacher signs。因此

$$
\widehat{\mathfrak R}_{S}(\mathcal M)
=\widehat{\mathfrak R}_{S_X}(\mathcal F).
$$

令 composed loss class

$$
\Phi_\gamma\circ\mathcal M
=\{(x,y)\mapsto\phi_\gamma(yf(x)):f\in\mathcal F\}.
$$

它落在 $[0,1]$。Rademacher risk theorem 给出：以至少 $1-\delta$ 的概率，对所有 $f$，

$$
P\phi_\gamma(yf(x))
\le
P_m\phi_\gamma(yf(x))
+2\widehat{\mathfrak R}_S(\Phi_\gamma\circ\mathcal M)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
$$

正文采用 factor-$2$ contraction 安全版本。因 $\phi_\gamma$ 为 $1/\gamma$-Lipschitz，中心化后

$$
\widehat{\mathfrak R}_S(\Phi_\gamma\circ\mathcal M)
\le\frac2\gamma
\widehat{\mathfrak R}_{S_X}(\mathcal F).
$$

连同 sandwich：

$$
\begin{aligned}
P(Yf(X)\le0)
&\le P\phi_\gamma(Yf(X))\\
&\le P_m\phi_\gamma(Yf(X))
+\frac4\gamma\widehat{\mathfrak R}_{S_X}(\mathcal F)
+3\sqrt{\frac{\log(2/\delta)}{2m}}\\
&\le
P_m(Yf(X)\le\gamma)
+\frac4\gamma\widehat{\mathfrak R}_{S_X}(\mathcal F)
+3\sqrt{\frac{\log(2/\delta)}{2m}}.
\end{aligned}
$$

> [!warning] 常数合同
> 使用 sharper scalar contraction 时，$4$ 可改善；使用不同 Rademacher convention 时又会改变。课程保留安全常数，重点是每一步对象与量词可核对。

## 七、把线性范数界代入

若

$$
\mathcal F_B
=\{x\mapsto\langle w,x\rangle:\|w\|_2\le B\},
$$

且样本上 $\|X_i\|_2\le R$，则

$$
\widehat{\mathfrak R}_{S_X}(\mathcal F_B)
\le\frac{BR}{\sqrt m}.
$$

于是

$$
\boxed{
P(Y\langle w,X\rangle\le0)
\le
P_m(Y\langle w,X\rangle\le\gamma)
+\frac{4BR}{\gamma\sqrt m}
+3\sqrt{\frac{\log(2/\delta)}{2m}}.}
$$

这里真正 scale-invariant 的组合是 $B/\gamma$：若 $w\mapsto cw$，则合理比较的 margin threshold 也应 $\gamma\mapsto c\gamma$，比值不变。

### 7.1 Affine bias

若还允许 $|b|\le B_0$，复杂度额外加约 $B_0/\sqrt m$，因此 margin penalty 也多出约

$$
\frac{B_0}{\gamma\sqrt m}.
$$

不能把 unbounded bias 悄悄并入“线性类”。

## 八、Hard-Margin SVM 的几何推导

假设训练数据线性可分。几何目标是最大化最小 geometric margin：

$$
\max_{w,b}
\min_i
\frac{y_i(\langle w,x_i\rangle+b)}{\|w\|_2}.
$$

由于 positive rescaling 不改变分类器与 geometric margin，可选择规范化

$$
\min_i y_i(\langle w,x_i\rangle+b)=1.
$$

在这个规范下，最小 geometric margin 是 $1/\|w\|_2$。最大化它等价于

$$
\boxed{
\min_{w,b}\frac12\|w\|_2^2
\quad\text{s.t.}\quad
y_i(\langle w,x_i\rangle+b)\ge1, \forall i.}
$$

等号成立的点是 support vectors；它们决定最优分离超平面的 active constraints。

### 8.1 为什么目标写 $\frac12\|w\|^2$

$\|w\|$ 与 $\frac12\|w\|^2$ 有相同 minimizer，但平方范数可微且导数为 $w$，便于 Lagrange dual 与数值优化。

## 九、Soft-Margin SVM 与 Hinge Loss

不可分或含噪时，引入 slack $\xi_i\ge0$：

$$
\begin{aligned}
\min_{w,b,\xi}\quad
&\frac12\|w\|_2^2+C\sum_{i=1}^m\xi_i\\
\text{s.t.}\quad
&y_i(\langle w,x_i\rangle+b)\ge1-\xi_i.
\end{aligned}
$$

对固定 $(w,b)$，最小可行 slack 为

$$
\xi_i=(1-y_if_{w,b}(x_i))_+.
$$

所以等价于 regularized hinge ERM：

$$
\min_{w,b}
\frac12\|w\|_2^2
+C\sum_i(1-y_if_{w,b}(x_i))_+.
$$

> [!important] 三层分账
> - optimization：解哪个 convex program；
> - generalization：函数类、margin distribution 与 confidence 给什么界；
> - calibration：hinge excess risk 怎样转成 $0$-$1$ excess risk。
>
> 任意一层成立都不自动替代另外两层。

## 十、为什么要看整条 Margin Distribution

最小训练 margin

$$
\min_iY_if(X_i)
$$

可能被一个异常点完全控制。margin bound 使用

$$
\widehat F_f(\gamma)
=P_m(Yf(X)\le\gamma),
$$

即 empirical margin CDF。它回答每个 $\gamma$ 下有多少样本处于错误或脆弱区域。

两个 classifier 可能：

- 最小 margin 相同，但一个有大量小正 margin；
- training error 都为 0，但 margin curve 差异很大；
- average hinge loss 相同，但 tail 的低 margin 比例不同。

因此应报告 margin quantiles/curve，而非只报 mean 或 minimum。

## 十一、选择 $\gamma$ 的统计代价

固定 $\gamma$ 的定理不允许看完同一数据后无成本挑选最有利阈值。若预先声明有限网格

$$
\Gamma=\{\gamma_1,\ldots,\gamma_K\},
$$

对每个阈值使用 failure probability $\delta/K$，union bound 给出 simultaneous certificate，confidence term 变为

$$
3\sqrt{\frac{\log(2K/\delta)}{2m}}.
$$

此时可以在同一训练样本上取所有网格 bound 的最小值。连续自适应阈值需要 peeling、结构化网格或专门 margin-distribution theorem。

## 十二、多分类 Margin

对 logits $f(x)\in\mathbb R^K$，常用 margin 是

$$
\rho_f(x,y)
=f_y(x)-\max_{k\ne y}f_k(x).
$$

分类正确等价于 $\rho_f>0$（忽略 ties）。但这里出现：

- vector-valued function class；
- 类别坐标间的 max coupling；
- 选用 $\ell_2/\ell_\infty$ logit geometry 时不同的 Lipschitz constant；
- $K$ 可能通过 vector contraction 或 multiclass dimension 进入 complexity。

所以 binary proof 不能只把 $Yf$ 替换成上式而保留所有常数。

## 十三、Adversarial Margin 接口

若 score 对输入 norm 是 $L_x$-Lipschitz：

$$
|f(x+\Delta)-f(x)|
\le L_x\|\Delta\|,
$$

且 clean signed margin 满足

$$
Yf(x)>L_x\varepsilon,
$$

则对所有 $\|\Delta\|\le\varepsilon$，

$$
Yf(x+\Delta)>0.
$$

这是 pointwise robust-margin sufficient condition。但要形成 robust population certificate，还需：

- 对 perturbation set 取 supremum 后的 robust loss class；
- 审计 $L_x$ bound 是否真实、是否过松；
- 处理 attack model、input constraints 与 sampling；
- 区分 certified robustness 与有限攻击实验。

## 十四、AI 应用审计

### 14.1 Frozen Embedding + Linear Head

最干净的接口是固定 encoder $h$，令

$$
f_w(x)=\langle w,h(x)\rangle.
$$

需记录：

1. encoder 是否独立于 probe sample；
2. $\|h(X_i)\|$ 的经验/总体上界；
3. head norm 与 bias；
4. empirical margin curve；
5. $\gamma$ grid 与 confidence budget；
6. loss/risk 是 binary、multiclass 还是 multilabel。

### 14.2 End-to-End Deep Network

若 representation 也由同一数据学习，复杂度属于整个网络类。仅把最后层 $w$ norm 代入线性 bound 会忽略 feature-selection capacity。现代 deep margin bounds 往往还含 layer spectral/Frobenius norms、depth、input radius 或 PAC-Bayes KL；数值是否 nonvacuous 必须实际计算。

### 14.3 Temperature 与 Logit Rescaling

把 logits 除以 temperature $\tau$ 会按 $1/\tau$ 放大 functional margin，同时也改变 loss Lipschitz/smoothness 与 calibration。若 complexity 同样随 score scale 增长，单独报告“margin 变大”没有意义；应检查 scale-invariant ratio。

## 十五、常见误区

> [!danger] 误区 1：训练误差为零就有大 margin
> 零误差只说明 $Y_if(X_i)>0$；它允许所有 margin 任意接近 0。

> [!danger] 误区 2：把参数乘 100 就改善 margin bound
> functional margin 与 function-class radius一起缩放；合适的 $B/\gamma$ 不变。

> [!danger] 误区 3：SVM 最大化 margin，所以测试误差必最小
> SVM 给定 class、regularization 和 sample 上的 optimization property；总体最优还依赖 data law、kernel/feature choice、noise 与 hyperparameter selection。

> [!danger] 误区 4：margin bound 解释了深网为何泛化
> 若 complexity 项巨大或条件不可验证，bound 可能 vacuous。形式上可套不等于给出有信息量的机制解释。

> [!danger] 误区 5：只看 minimum margin
> 一个 outlier 可主宰 minimum；定理读取的是 thresholded empirical distribution 与 complexity trade-off。

## 十六、本节最小闭环

给定一个 binary score model，应能完成：

1. 写出 $\rho_i=Y_if(X_i)$；
2. 画/算 empirical margin CDF；
3. 声明 function-class complexity 与 score scale；
4. 在预声明 $\gamma$ grid 上计算三项 bound；
5. 若为 linear/SVM，区分 functional 与 geometric margin；
6. 若为 multiclass/deep/robust，明确需要替换的 vector/full-class theorem；
7. 不把优化成功、surrogate calibration 与 generalization 混为一条结论。

## 十七、连接

- 前置：[[收缩引理与 Lipschitz 损失复合]]、[[范数约束线性类的复杂度]]；
- 下一节：[[覆盖数、Metric Entropy 与 Chaining 入口]]；
- 模型：[[支持向量机、最大间隔与核方法]]、[[Boosting、弱学习与指数损失]]；
- 深网接口：[[神经网络容量与 Norm-Based Bound]]；
- 训练：[[习题 - 分类间隔、Margin Bound 与 SVM 接口]]；
- 解答：[[解答 - 分类间隔、Margin Bound 与 SVM 接口]]。
