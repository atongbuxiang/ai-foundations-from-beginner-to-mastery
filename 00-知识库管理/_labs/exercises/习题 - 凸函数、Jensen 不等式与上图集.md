---
type: exercise
status: draft
area: [math/convex-analysis, math/inequalities, ai/loss-functions]
topic: "凸函数、Jensen 不等式与上图集"
difficulty: [A, B, C, D, E]
prerequisites: ["[[凸函数、Jensen 不等式与上图集]]"]
related: ["[[优化与凸分析 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 凸函数、Jensen 不等式与上图集]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 凸函数、Jensen 不等式与上图集

> [!abstract] 训练目标
> 能在 chord、epigraph、line、gradient、Hessian 与 Jensen 六种语言之间切换；所有 AI 结论必须说明 convexity 相对于哪个变量成立。

## A. 识别与复述

### OPT-FUNC-A01

定义 convex、strictly convex、$\mu$-strongly convex 与 concave function。说明 effective domain 为什么必须写入定义，并比较 strict 与 strong convexity。

### OPT-FUNC-A02

陈述 epigraph、sublevel set、quasiconvex function。哪些蕴含成立，哪些反向不成立？解释 equality constraint $f(x)=0$ 为什么不能仅凭 $f$ convex 就断言可行集 convex。

### OPT-FUNC-A03

陈述 line、first-order、second-order 三种 convexity characterization，各自需要什么 domain、differentiability 条件。说明随机 direction/Hessian sampling 为什么只是诊断而非证明。

## B. 手算与构造

### OPT-FUNC-B01

分别用合适判据判断 convexity，并写 domain：

1. $e^x$；
2. $-\log x$；
3. $x^4$；
4. $f(x)=\frac12x^TQx+b^Tx+c$；
5. $\|Ax-b\|_2$；
6. $\min\{(x-1)^2,(x+1)^2\}$。

### OPT-FUNC-B02

令 $P(X=-1)=P(X=1)=1/2$。

1. 对 $f(x)=x^2$ 计算 Jensen 两侧与 gap；
2. 对 $f(x)=e^x$ 计算两侧；
3. 给一个非退化 $X$ 和非严格 convex $f$，使 Jensen equality 成立；
4. 解释 gap 与 variance/curvature 的关系何时只是近似。

### OPT-FUNC-B03

对 $x=(0,0)$：

1. 计算 $\operatorname{LSE}(x)$、softmax gradient 和 Hessian；
2. 求 Hessian eigenvalues/eigendirections；
3. 对 target class 1 的 cross-entropy 求 loss 与 gradient；
4. 验证 constant-shift direction 为什么不是 strict convex direction。

## C. 推导与证明

### OPT-FUNC-C01

双向证明：$f$ convex 当且仅当 $\operatorname{epi}f$ convex。再推出 convex function 的每个 sublevel set convex，并说明反向为何只对应 quasiconvex。

### OPT-FUNC-C02

对 differentiable $f$ 在 open convex domain 上，双向证明

$$
f\text{ convex}
\Longleftrightarrow
f(y)\ge f(x)+\nabla f(x)^T(y-x).
$$

由此证明 stationary point global optimal，以及 convex feasible set 上 local minimum global。

### OPT-FUNC-C03

证明以下保凸规则并写清条件：nonnegative weighted sum、affine precomposition、pointwise supremum、convex nondecreasing outer composed with convex inner。再证明 perspective $t f(x/t)$ convex 的 epigraph/变量替换骨架。

## D. 反例与失败边界

### OPT-FUNC-D01

用 $x^3$ 说明所有 sublevel sets convex 不推出 function convex。再给一个 strictly convex 但不 globally strongly convex 的函数，并算 Hessian/二阶导。

### OPT-FUNC-D02

分别构造：两个 convex functions 的 composition 非凸；两个 convex functions 的 pointwise minimum 非凸；convex function 经 nonlinear reparameterization 后非凸。每个反例都要算出关键二阶导或违反 chord 的点。

### OPT-FUNC-D03

给一个 loss 对 logits convex、对最后线性层 convex、但对两层参数非凸的标量例子。明确变量偷换发生在哪里，并说明 Hessian 一处 indefiniteness 即足以否定 global convexity。

## E. AI 迁移

### OPT-FUNC-E01

审计 checkpoint/model ensemble 的 Jensen 叙事：分别定义 parameter averaging、logit averaging、probability averaging 和 loss averaging。指出在哪些 convexity/linearity 条件下可比较，设计 held-out calibration 与 shift 验证。

### OPT-FUNC-E02

围绕 temperature logsumexp/softmax 写实验协议：验证 max approximation bound、gradient concentration、Hessian eigenvalues、数值 overflow/stable shift 和 small-temperature precision。不得把平滑 max 误称为 exact max。

### OPT-FUNC-E03

把一个含 logistic loss、$\ell_1$ penalty、group maximum 和 affine constraints 的问题写成 DCP 风格。逐 atom 标注 curvature/sign/monotonicity；列出 solver acceptance 之后仍要检查的 feasibility、duality、conditioning 与 population evidence。

