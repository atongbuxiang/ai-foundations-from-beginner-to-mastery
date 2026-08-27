---
type: theorem
status: draft
area: [learning-theory/algorithmic-stability, regularization, convex-optimization]
aliases: [Regularized ERM Stability, Strong Convexity Stability, RERM]
node_id: LT-34
prerequisites: ["[[算法稳定性与替换一个样本]]", "[[光滑性、强凸性与条件数]]", "[[凸函数、Jensen 不等式与上图集]]"]
related: ["[[随机梯度算法的稳定性接口]]", "[[结构风险最小化与非一致可学习性]]", "[[范数、平坦性、Sharpness 与参数化不变性]]", "[[核岭回归与 Gaussian Process 接口]]"]
sources: ["[[S-2002-Bousquet-Elisseeff-Stability-Generalization]]", "[[S-2020-Su-7681-L2正则与尺度不变性]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
exercises: ["[[习题 - 正则化 ERM 的稳定性]]"]
solutions: ["[[解答 - 正则化 ERM 的稳定性]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-regularized-erm-curvature-stability-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 正则化 ERM 的稳定性

> [!abstract] 本章主问题
> 对 convex、$L$-Lipschitz per-example loss，考虑
> $$
> F_S(w)=\frac1m\sum_{i=1}^m\ell(w,Z_i)+\frac\lambda2\|w\|_2^2.
> $$
> 二次正则使 $F_S$ 成为 $\lambda$-strongly convex。相邻数据集的两个最优性不等式相加后，$m-1$ 个共享样本项和 regularizer 全部抵消，只剩两项 Lipschitz loss difference。于是
> $$
> \|w_S-w_{S'}\|_2\le\frac{2L}{\lambda m},
> \qquad
> \beta_m\le\frac{2L^2}{\lambda m}.
> $$
> 这是“curvature $\to$ parameter stability $\to$ loss stability”的标准证明链。常数完全依赖本章采用的 replace-one adjacency 与 $\lambda\|w\|^2/2$ 归一化。

> [!question] 初学者读完必须能回答
> 1. strong convexity 怎样把 objective gap 变成 minimizer distance？
> 2. 为什么把两个不等式相加后，共享样本恰好抵消？
> 3. $L$-Lipschitz 与 smoothness 在证明中各扮演什么角色？
> 4. approximate optimizer 会给稳定性多加哪一项？
> 5. 为什么深网里加 weight decay 不足以直接调用本定理？

## 一、学习目标

1. 固定 regularized ERM 的归一化与邻接 convention；
2. 使用 strong convexity 的 minimizer inequality；
3. 逐行完成 cancellation proof；
4. 从 parameter displacement 推出 test-loss stability；
5. 推广到一般 norm/dual norm 与 strongly convex regularizer；
6. 处理 logistic loss、squared loss、kernel method 与 approximate optimization；
7. 审计 $\lambda$ 的 bias–stability tradeoff、data-dependent tuning 与尺度不变网络。

## 二、问题设置与全部假设

令 $\mathcal W\subseteq\mathbb R^d$ 为 convex set。假设对每个 $z\in\mathcal Z$：

1. $w\mapsto\ell(w,z)$ convex；
2. $w\mapsto\ell(w,z)$ 关于 $\|\cdot\|_2$ 为 $L$-Lipschitz：
   $$
   |\ell(w,z)-\ell(v,z)|\le L\|w-v\|_2;
   $$
3. regularization strength $\lambda>0$；
4. exact minimizer 存在。

定义

$$
F_S(w)
=\frac1m\sum_{j=1}^m\ell(w,Z_j)
+\frac\lambda2\|w\|_2^2,
\qquad
w_S\in\arg\min_{w\in\mathcal W}F_S(w).
$$

因为 convex loss 之和是 convex，而 $\lambda\|w\|^2/2$ 是 $\lambda$-strongly convex，$F_S$ 是 $\lambda$-strongly convex。因此 minimizer 唯一；可直接写 $w_S$。

> [!warning] 归一化决定常数
> 若 objective 写成 $\sum_i\ell_i+\lambda\|w\|^2$、$m^{-1}\sum_i\ell_i+\lambda\|w\|^2$ 或其他形式，$m$、$2$ 与 $\lambda$ 的位置都会改变。不能只记结论 $O(1/(\lambda m))$ 后照抄常数。

## 三、Strong Convexity 的 Minimizer Inequality

若 $F$ 为 $\lambda$-strongly convex，且 $w^*$ 是其 constrained minimizer，则对任意 $v\in\mathcal W$，

$$
\boxed{
F(v)-F(w^*)
\ge\frac\lambda2\|v-w^*\|_2^2.}
$$

### 3.1 为什么成立

无约束可微情形中，strong convexity 给出

$$
F(v)\ge F(w^*)
+\langle\nabla F(w^*),v-w^*\rangle
+\frac\lambda2\|v-w^*\|^2.
$$

由 $\nabla F(w^*)=0$ 得结论。convex constraint 下，一阶最优性变为

$$
\langle g^*,v-w^*\rangle\ge0,
\qquad g^*\in\partial F(w^*),
$$

线性项仍非负，所以同一不等式成立。

## 四、图解：曲率、抵消与正则权衡

先回答：**为什么证明必须把 $F_S(w_{S'})-F_S(w_S)$ 与 $F_{S'}(w_S)-F_{S'}(w_{S'})$ 相加，而不是只看其中一个？**

![[00-知识库管理/_assets/figures/learning-theory/fig-regularized-erm-curvature-stability-v2.svg|900]]

> [!figure] 图 20.5.2｜正则化 ERM 的 strong-convexity cancellation
> 左栏显示相邻数据集产生两个邻近极小点；中栏表示两个强凸下界相加后共享样本抵消；右栏强调增大 $\lambda$ 改善 stability 却可能增加 bias。来源：依据 Bousquet–Elisseeff regularization 主线独立绘制；确定性 SVG，由 [[plot_stability_compression_v2.py]] 生成。

**怎样读图。** strong convexity 给左边一个二次量 $\lambda\|\Delta\|^2$；replace-one 与 Lipschitzness 只让右边付线性量 $2L\|\Delta\|/m$。二次与线性平衡后得到 $1/(\lambda m)$ displacement。

**图没有证明什么。** 图没有证明深网 objective strong convex、squared loss global Lipschitz、approximate optimizer 足够精确，或 data-tuned $\lambda$ 免费保持同一置信度。

## 五、核心定理：Replace-One Stability

设

$$
S=(Z_1,\ldots,Z_i,\ldots,Z_m),
\qquad
S'=(Z_1,\ldots,Z_i',\ldots,Z_m),
$$

并记

$$
w=w_S,
\qquad
w'=w_{S'},
\qquad
\Delta=w'-w.
$$

### 5.1 对两个目标分别用 strong convexity

因为 $w$ 最小化 $F_S$：

$$
F_S(w')-F_S(w)
\ge\frac\lambda2\|\Delta\|^2.
$$

因为 $w'$ 最小化 $F_{S'}$：

$$
F_{S'}(w)-F_{S'}(w')
\ge\frac\lambda2\|\Delta\|^2.
$$

相加得到

$$
\lambda\|\Delta\|^2
\le
F_S(w')-F_S(w)
+F_{S'}(w)-F_{S'}(w').
$$

### 5.2 展开右边并逐项抵消

把 objective 展开。regularizer 部分为

$$
\frac\lambda2(\|w'\|^2-\|w\|^2)
+\frac\lambda2(\|w\|^2-\|w'\|^2)
=0.
$$

对每个共享坐标 $j\ne i$，loss 部分为

$$
\ell(w',Z_j)-\ell(w,Z_j)
+\ell(w,Z_j)-\ell(w',Z_j)
=0.
$$

因此只剩被替换的坐标：

$$
\lambda\|\Delta\|^2
\le\frac1m\Big(
\ell(w',Z_i)-\ell(w,Z_i)
+\ell(w,Z_i')-\ell(w',Z_i')
\Big).
$$

### 5.3 用 Lipschitzness 控制两项

每一项都至多为 $L\|\Delta\|$，所以

$$
\lambda\|\Delta\|^2
\le\frac{2L}{m}\|\Delta\|.
$$

若 $\Delta=0$，结论显然；否则除以 $\|\Delta\|$：

$$
\boxed{
\|w_S-w_{S'}\|
\le\frac{2L}{\lambda m}.}
$$

最后对任意 test point $z$ 再用一次 Lipschitzness：

$$
|\ell(w_S,z)-\ell(w_{S'},z)|
\le L\|w_S-w_{S'}\|
\le\frac{2L^2}{\lambda m}.
$$

所以

$$
\boxed{
\beta_m\le\frac{2L^2}{\lambda m}.}
$$

## 六、证明中没有使用 Smoothness

exact RERM proof 使用了：

- convexity；
- strong convexity；
- loss Lipschitzness；
- exact optimality；
- replace-one decomposability。

它没有使用 gradient Lipschitzness/smoothness。smoothness 常在下列地方进入：

- 用 gradient descent/SGD 近似求解；
- 建立 update map nonexpansiveness；
- 用 Hessian/condition number 控制 optimization error；
- 分析 second-order sensitivity。

所以“loss 不 smooth”不一定破坏 exact-minimizer stability；但它可能影响求解器和 approximate-output stability。

## 七、一般 Norm 与 Dual Norm 版本

设 $\Omega(w)$ 关于 norm $\|\cdot\|$ 是 $\lambda$-strongly convex，loss 满足

$$
|\ell(w,z)-\ell(v,z)|
\le L\|w-v\|.
$$

同样的证明给出

$$
\|w_S-w_{S'}\|
\le\frac{2L}{\lambda m},
\qquad
\beta_m\le\frac{2L^2}{\lambda m}.
$$

可微时，$L$-Lipschitz 等价于适当条件下的 dual-gradient bound：

$$
\|\nabla_w\ell(w,z)\|_*
\le L.
$$

这说明几何必须配对：$ell_1$ parameter geometry 对应 $\ell_\infty$ dual gradient，matrix trace norm 对应 spectral norm 等。

## 八、例一：有界特征的 Logistic Regression

令 $y\in\{-1,+1\}$，

$$
\ell(w,(x,y))
=\log\left(1+e^{-y\langle w,x\rangle}\right),
\qquad
\|x\|_2\le R.
$$

其梯度为

$$
\nabla_w\ell
=-\frac{yx}{1+e^{y\langle w,x\rangle}},
$$

故

$$
\|\nabla_w\ell\|_2\le\|x\|_2\le R.
$$

所以 $L=R$，带 $\lambda\|w\|^2/2$ 的 logistic RERM 满足

$$
\boxed{
\beta_m\le\frac{2R^2}{\lambda m}.}
$$

维数 $d$ 没有显式出现，但并不代表 bound 总是 tight：$R$、$\lambda$、empirical risk 和 feature normalization 可能使它仍然很松。

## 九、例二：Squared Loss 为什么不能直接套

平方损失

$$
\ell(w,(x,y))
=(\langle w,x\rangle-y)^2
$$

的梯度为

$$
\nabla_w\ell
=2(\langle w,x\rangle-y)x.
$$

即使 $\|x\|\le R$，若 $w$ 或 $y$ 无界，gradient norm 仍无统一上界，所以 squared loss 不是 global Lipschitz。

要调用本定理，至少需要一种额外控制：

- 限制 $\|w\|\le B$ 且 $|y|\le Y$；
- 使用 clipped prediction/loss；
- 从 objective comparison 先证明 $w_S$ 落在有界球；
- 或改用专门利用 smoothness、moments 与 local curvature 的 stability theorem。

“有 L2 正则”本身不等于“平方损失已全局 Lipschitz”。

## 十、Approximate Minimizer 的额外账本

实际算法往往输出 $\widetilde w_S$，只满足

$$
F_S(\widetilde w_S)-F_S(w_S)
\le\varepsilon_{\rm opt}.
$$

strong convexity 给出

$$
\frac\lambda2
\|\widetilde w_S-w_S\|^2
\le\varepsilon_{\rm opt},
$$

故

$$
\|\widetilde w_S-w_S\|
\le\sqrt{\frac{2\varepsilon_{\rm opt}}\lambda}.
$$

对相邻 $S,S'$，三角不等式给

$$
\|\widetilde w_S-\widetilde w_{S'}\|
\le
2\sqrt{\frac{2\varepsilon_{\rm opt}}\lambda}
+\frac{2L}{\lambda m}.
$$

于是 approximate-output loss stability 可界为

$$
\boxed{
\widetilde\beta_m
\le
\frac{2L^2}{\lambda m}
+2L\sqrt{\frac{2\varepsilon_{\rm opt}}\lambda}.}
$$

若希望第二项不压过 $1/m$，optimization tolerance 必须随 $m$ 充分下降；“目标函数看起来收敛”必须量化到 theorem 需要的尺度。

## 十一、$\lambda$ 的 Bias–Stability Tradeoff

增大 $\lambda$ 会：

- 增加 curvature；
- 减小 parameter displacement；
- 改善 stability term $2L^2/(\lambda m)$；
- 但更强地偏向小 norm hypothesis，可能增加 approximation/bias error。

一个 schematic 总体账本是

$$
\text{population risk}
\approx
\text{regularized empirical fit}
+\text{stability penalty}
+\text{regularization bias}
+\text{optimization error}.
$$

不能通过令 $\lambda\to\infty$ 把 stability 界做成 0 后宣布学习成功，因为此时算法可能退化为几乎固定输出。

### 11.1 数据选择的 $\lambda$ 不是固定算法

若在同一个 validation set 上尝试 $K$ 个 $\lambda$ 后选择最好者，最终 pipeline 包含一个 adaptive selection algorithm。对每个固定 $\lambda$ 的 stability theorem 不会自动免费覆盖选后输出；应使用独立 validation、union/selection correction 或直接分析完整 tuning procedure。

## 十二、Kernel / RKHS 接口

在 RKHS $\mathcal H_k$ 中考虑

$$
F_S(f)
=\frac1m\sum_i\ell(f,Z_i)
+\frac\lambda2\|f\|_{\mathcal H_k}^2.
$$

若 $k(x,x)\le\kappa^2$，evaluation functional 满足

$$
|f(x)-g(x)|
\le\kappa\|f-g\|_{\mathcal H_k}.
$$

若 scalar prediction loss 对第一变量为 $\sigma$-Lipschitz，则 composite loss 关于 RKHS norm 为 $L=\sigma\kappa$。代入得到

$$
\beta_m
\le\frac{2\sigma^2\kappa^2}{\lambda m}
$$

（按本章归一化）。这就是 kernel ridge/SVM stability 的 function-space 几何入口。

## 十三、为什么 Deep Weight Decay 不能直接调用本定理

深网常违反本章的多个条件：

1. objective 非凸；
2. prediction loss 未必 global Lipschitz in parameters；
3. BatchNorm/LayerNorm 与 positive homogeneity 产生尺度等价；
4. weight decay 不一定等价于 function norm control；
5. optimizer 只得到 path-dependent approximate stationary point；
6. data augmentation 与 minibatch state 使 per-example decomposition 更复杂。

科学空间关于 L2 正则与尺度不变性的讨论提醒我们：某些网络中缩放参数可改变 weight norm，却不相应改变函数。此时 parameter-space curvature 或 norm penalty 的解释必须回到 function/output geometry；不能只看到配置中 `weight_decay > 0` 就套 $2L^2/(\lambda m)$。

## 十四、Strong Convexity、Uniqueness 与 Stability 不完全等价

- strong convexity 是本章的充分机制，不是 stability 的必要条件；
- averaging、bagging、local rules 也可能稳定而不来自强凸；
- unique minimizer 不代表 quantitatively stable：曲率可极小；
- data-dependent curvature 若接近 0，替换一条样本仍可造成大位移；
- parameter stability 还需 test loss 对相同 norm Lipschitz 才能转成 loss stability。

## 十五、AI 模型的 RERM 审计协议

1. 写出**实际**优化目标及 $1/m$、$1/2$ 的位置；
2. 明确 parameter/function space 与 norm；
3. 证明每个 per-example loss convex；
4. 给出 global 或局部 $L$，说明其 dependence；
5. 给出 regularizer 的 strong-convexity modulus；
6. 声明 exact/approximate optimizer 与 $\varepsilon_{\rm opt}$；
7. 推出 parameter displacement；
8. 再推出 test-loss sensitivity；
9. 报告 $2L^2/(\lambda m)$ 的实际数值；
10. 把 hyperparameter selection、preprocessing 与 random seeds 纳入完整 algorithm。

## 十六、常见误区

1. **“加 L2 就一定 $\lambda$-strongly convex。”** 总 objective 是 strong convex，但只有在线性 parameter space/合法 convex domain 等合同下能直接使用；非凸 network loss 加二次项未必整体 convex。
2. **“smoothness 等于 strong convexity。”** 一个控制 gradient 变化上界，一个提供 curvature 下界。
3. **“unique minimizer 等于 $1/m$ 稳定。”** 还需 quantitative curvature 与 Lipschitzness。
4. **“squared loss 是 smooth，所以也是 Lipschitz。”** 无界域上错误。
5. **“$\lambda$ 越大越好。”** 忽略 bias 与 fit。
6. **“训练到近似 stationary 就等于 objective gap 小。”** 非凸或 ill-conditioned 情形不成立。

## 十七、与相邻节点的接口

- [[算法稳定性与替换一个样本]]：把 $\beta_m$ 转成 expected/high-probability gap；
- [[随机梯度算法的稳定性接口]]：不等待 exact minimizer，直接分析 update path；
- [[局部 Rademacher 复杂度与快收敛率]]：regularization/curvature 也可通过 localized complexity 产生另一类证书；
- [[核岭回归与 Gaussian Process 接口]]：RKHS norm 与 effective dimension；
- [[正则化、交叉验证与模型选择]]：选择 $\lambda$ 后的合法性。

## 十八、小结

1. $\lambda\|w\|^2/2$ 给 convex empirical loss 增加 $\lambda$-strong convexity；
2. 两个 minimizer inequalities 相加后，共享样本与 regularizer 抵消；
3. quadratic curvature 与 linear Lipschitz perturbation 平衡，得到 $2L/(\lambda m)$ parameter displacement；
4. test-loss Lipschitzness 再给 $\beta_m\le2L^2/(\lambda m)$；
5. approximate optimization 增加 $2L\sqrt{2\varepsilon_{\rm opt}/\lambda}$ 量级；
6. deep weight decay、squared loss、adaptive tuning 与 scale invariance 都必须单独审计。

## 来源与延伸

- [[S-2002-Bousquet-Elisseeff-Stability-Generalization]]
- [[S-2020-Su-7681-L2正则与尺度不变性]]
- [[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]
- [[光滑性、强凸性与条件数]]
