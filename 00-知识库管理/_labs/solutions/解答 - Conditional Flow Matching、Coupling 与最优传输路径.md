---
type: solution
status: draft
topic: "[[Conditional Flow Matching、Coupling 与最优传输路径]]"
exercise: "[[习题 - Conditional Flow Matching、Coupling 与最优传输路径]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Conditional Flow Matching、Coupling 与最优传输路径
## A. 识别与复述
### GEN54-A01
coupling $\pi(x_0,x_1)$ 是 joint law，满足 $\int\pi dx_1=p_0(x_0)$、$\int\pi dx_0=p_1(x_1)$。同一对 marginals 通常有许多 couplings。
### GEN54-A02
independent coupling 取 $p_0p_1$，忽略几何配对，优点是直接采样。quadratic OT 在合法 couplings 中最小化 $E\|X_1-X_0\|^2$，但需解 transport problem，且结果依赖所选 cost/空间。
### GEN54-A03
它改变 endpoint joint、conditional path 样本、displacement $U$、中间 $p_t$、marginal velocity、$\operatorname{Var}(U|X_t,t)$、gradient noise、场复杂度与 finite solver 难度；端点 marginals 仍可相同。
## B. 手算与建模
### GEN54-B01
identity coupling 有 $X_1=X_0$，故 $U=0$、中点 target 均值/方差均 0。swap coupling 有 $U=-2X_0\in\{-2,+2\}$，且所有路径在中点 $X_{1/2}=0$；条件均值 0、variance 4。
### GEN54-B02
同序：$0\to1$ 成本 1，$3\to4$ 成本 1，总成本 2。交叉：$0\to4$ 成本 16，$3\to1$ 成本 4，总成本 20。同一 endpoints，coupling cost 相差十倍。
### GEN54-B03
对角 assignment 成本 $1+0=1$；非对角为 $9+4=13$，故选对角。它只是在这两个经验点上、此 cost 下的 batch optimum，不证明 population OT plan 或下一 batch 的配对。
## C. 推导与证明
### GEN54-C01
$X_t=(1-t)X_0+tX_1$。$t=0$ 时 $X_t=X_0$，其 law 是 coupling 第一边缘 $p_0$；$t=1$ 时等于 $X_1$，law 是第二边缘 $p_1$。中间 law 仍依赖完整 joint，不由 endpoints 单独决定。
### GEN54-C02
$C_\pi$ 是 conditional target 对生成时可见输入的不可约 variance。$U,X_t$ 都由 $\pi$ 与 path 构造，换 coupling 即换该 joint，故常数可变。它不改给定 coupling 下 CFM/FM 的 population minimizer，但影响 SGD 方差与有限容量折中。
### GEN54-C03
在 quadratic cost、有限二阶矩，并通常要求 source 绝对连续等条件下，optimal map/coupling 的 displacement interpolation 给 $W_2$ geodesic；Benamou–Brenier 公式把 $W_2^2$ 表为满足连续性方程的动能积分最小值。离散/奇异情形可能 plan 非唯一，不能省略条件。
## D. 边界、反例与纠错
### GEN54-D01
minibatch 只对经验测度求 assignment，配对依赖 batch composition/size、regularization 和 solver。它可能是有用 estimator/design，却不等于全分布上的 plan；更不能不加条件地继承 population OT theorem。
### GEN54-D02
短 endpoint displacement 只控制一个静态 cost。learned velocity 的 Jacobian、time variation、network error 与 solver stability 仍可能很差；semantic metric 也可能与 Euclidean cost 不同。必须实测轨迹曲率和 equal-NFE error。
### GEN54-D03
交换 endpoint 名称；令 $t_{course}=1-t_{code}$；velocity 乘 $-1$ 并把系数时间参数换元；solver 网格方向翻转；训练 target/conditioning 的端点角色同步换。只改数据变量名而不改 velocity 会生成相反方向。
## E. AI 迁移
### GEN54-E01
统一数据、端点 marginals、网络、参数量、optimizer、steps、time sampler 和总 wall time；唯一主变量是 coupling。报告 coupling construction cost，并在 equal training compute 与 equal total compute 两个口径比较。测 CFM loss、target variance、曲率、NFE-error、likelihood/质量/覆盖和多 seed。
### GEN54-E02
batch size、ground cost 与预处理、assignment/OT solver、entropic/unbalanced regularization、迭代/tolerance、hard/soft plan、pair sampling、stop-gradient、跨 batch cache、随机 seed、额外 wall time/显存及 endpoint direction。
### GEN54-E03
二维 toy 中画端点连线，在时间切片用局部邻域收集 $U$ 箭头；数值报告 $E\operatorname{tr}\operatorname{Cov}(U|X_t\in bin)$、交叉/近邻方向夹角、平均 displacement 与 learned field residual。不同 bin width 做稳定性检查。
