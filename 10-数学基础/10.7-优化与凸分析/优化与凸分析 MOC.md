---
type: moc
status: active
area: [math/optimization, math/convex-analysis, ai/training]
aliases: [优化理论 MOC, 凸优化 MOC, Optimization MOC]
prerequisites: ["[[线性代数完整学习路线与掌握标准]]", "[[多元微积分、矩阵微分与自动微分 MOC]]", "[[概率论与数理统计 MOC]]"]
related: ["[[数学基础 MOC]]", "[[数学基础完整课程地图与掌握标准]]", "[[练习与测验 MOC]]", "[[推导与实验 MOC]]"]
sources: ["Boyd-Vandenberghe-2004-Convex-Optimization", "MIT-6.253-Convex-Analysis-Optimization", "Stanford-EE364A-Convex-Optimization", "Stanford-EE364B-Convex-Optimization-II", "Rockafellar-1970-Convex-Analysis", "Nesterov-2018-Lectures-Convex-Optimization", "Bubeck-2015-Convex-Optimization", "Beck-2017-First-Order-Methods", "Parikh-Boyd-2014-Proximal-Algorithms", "Beck-Teboulle-2009-FISTA", "Amari-1998-Natural-Gradient", "Martens-2020-Natural-Gradient", "Nocedal-Wright-2006-Numerical-Optimization", "Bertsekas-1999-Nonlinear-Programming", "Liu-Nocedal-1989-LBFGS", "Polyak-1964-Heavy-Ball", "Robbins-Monro-1951-Stochastic-Approximation", "Bottou-Curtis-Nocedal-2018-Large-Scale-ML", "Duchi-Hazan-Singer-2011-AdaGrad", "Kingma-Ba-2015-Adam", "Reddi-et-al-2018-AMSGrad", "Loshchilov-Hutter-2019-AdamW", "Lee-et-al-2016-Gradient-Descent-Saddles", "Jin-et-al-2017-Escape-Saddles", "Karimi-et-al-2016-PL", "Ge-Jin-Zheng-2017-Low-Rank-Landscape", "Laurent-von-Brecht-2018-Deep-Linear", "Dinh-et-al-2017-Sharpness", "Garipov-et-al-2018-Mode-Connectivity", "Su-9070-LogSumExp-Inequalities", "Su-5655-SGD-Momentum", "Su-7521-Sampling-Optimization", "Su-7787-Finite-Learning-Rate", "Su-10588-Hessian-Adaptive-LR", "Su-3552-Maximum-Entropy", "Su-10592-Muon", "Su-11215-Manifold-Steepest"]
created: 2026-08-19
updated: 2026-08-27
---

# 优化与凸分析 MOC

> [!abstract] 本卷的核心任务
> 把“训练模型”还原成一个定义完整、几何清楚、证书可检查的数学问题：谁是变量，什么固定，哪些点可行，什么叫解，算法输出距离所需解概念还有多远。凸分析提供少数真正强大的结构——局部最优等于全局最优、分离超平面、对偶下界和可计算的一阶方法；深度学习通常非凸，因此本卷既学习这些定理，也学习它们在哪一层仍可调用、在哪一层已经失效。

### 当前教学迁移路线

> [!important] 材料状态与学习状态分开
> 下表检查“课程位置—两遍路线—问题链—统一算例—对象账本—公式七问—停靠线”是否补齐。`regression-passed` 只表示仓库材料和确定性计算通过回归；16 篇正文 frontmatter 的 `draft` 与卷末 `not-attempted` 仍表示尚无个人口试、闭卷、订正和延迟复做证据。

| 波次 | ID 范围 | 认知主线 | 材料迁移 |
|---|---|---|---|
| A | OPT-01—04 | 问题契约 → 凸集/投影/分离 → 凸函数/Jensen → 次梯度/共轭/Fenchel | `regression-passed` |
| B | OPT-05—08 | 曲率上下界 → 梯度下降 → 加速/动量 → 随机梯度 | `regression-passed` |
| C | OPT-09—12 | 自适应度量 → 二阶模型 → 投影方向 → KKT | `regression-passed` |
| D | OPT-13—16 | 强对偶 → proximal → mirror/Fisher → 非凸地形 | `pending` |
| CUM | OPT-CUM | 卷级路线—口试—题解—实验—回归 | `pending` |

第一波统一使用“把越界目标投回三角形”的问题：

$$
a=\begin{pmatrix}1\\1\end{pmatrix},
\qquad
C=\operatorname{conv}\{0,e_1,e_2\},
\qquad
\min_{x\in C}\frac12\|x-a\|_2^2.
$$

OPT-01 先把 $a$、decision variable $x$、objective $q$、feasible set $C$、optimal value $p^*$ 与 solution set $X^*$ 分层，并用平方和下界得到

$$
x^*=\begin{pmatrix}1/2\\1/2\end{pmatrix},
\qquad
p^*=\frac14.
$$

OPT-02 把残差 $r=a-x^*=(1/2,1/2)^T$ 同时读作 projection residual、normal 与 separating-hyperplane 法向，并逐点闭合

$$
\langle r,z-x^*\rangle\le0,
\qquad \forall z\in C.
$$

OPT-03 用精确恒等式

$$
\theta q(x)+(1-\theta)q(y)
-q(\theta x+(1-\theta)y)
=\frac{\theta(1-\theta)}2\|x-y\|^2
$$

贯通 chord、Jensen、一阶支撑和 Hessian；OPT-04 再把同一个 $r$ 写成 $r\in N_C(x^*)=\partial\delta_C(x^*)$，手算

$$
\delta_C^*(y)=\max\{0,y_1,y_2\},
\qquad
q^*(y)=a^Ty+\frac12\|y\|^2,
$$

并在 $y^*=r$ 处得到 primal value = dual value = $1/4$。这条链的作用不是让四章共享几个小数，而是让同一个对象依次获得建模、几何、曲率和证书四种解释。正式回归入口：[[optimization_teaching_contract_audit.py|OPT-01—04 教学合同与精确模型回归]]。

> [!success] 第一波停靠线
> 合上四篇正文后，应能在一张纸上重建 $C,a,x^*,r$；分别解释 $p^*$、projection VI、Jensen gap、support function 与 duality gap 的对象类型；最后说明“目标对 mixture weights 凸”为什么不能推出“产生这些权重的深网参数问题凸”。做不到时，先回到第一个对象断点，不进入收敛率章节。

第二波把问题换成可精确谱分解的椭圆 quadratic：

$$
f(x)=\frac12x^THx,
\qquad
H=\operatorname{diag}(1,4),
\qquad
x_0=(1,1)^T.
$$

OPT-05 从 Hessian 端点得到

$$
\mu=1,
\qquad
L=4,
\qquad
\kappa=4,
$$

并用

$$
\frac12\|y-x\|^2
\le f(y)-f(x)-\nabla f(x)^T(y-x)
\le2\|y-x\|^2
$$

把 strong-convex lower model 与 smooth upper model 夹在同一个一阶近似两侧。OPT-06 将 GD 分成 factors $1-\eta$ 与 $1-4\eta$：稳定区间是 $0<\eta<1/2$；$\eta=1/4$ 一步消去 stiff mode，而 $\eta=2/5$ 把两个端点平衡为 $\pm3/5$。OPT-07 再把一阶 factor 升级为 heavy-ball polynomial；取

$$
\eta=\frac49,
\qquad
\beta=\frac19
$$

时，两个谱端点分别成为 $(r-1/3)^2$ 与 $(r+1/3)^2$，从而明确区分 Hessian eigenvalue、recurrence root 与 function-value rate。OPT-08 最后令

$$
g_k=Hx_k+\bar\xi_k,
\qquad
\operatorname{Cov}(\bar\xi_k\mid\mathcal F_k)=\frac{\sigma^2}{B}I,
$$

在 $\eta=1/4$ 下得到单步 noise injection $5\sigma^2/(32B)$，并由两个 AR(1) modes 算出 stationary objective floor

$$
\mathbb E[f(x_\infty)]=\frac{11\sigma^2}{56B}.
$$

这条链把“曲率—确定性收缩—带记忆根—随机稳态”逐层增加新对象：后一个结论不能反过来抹掉前一个结论所需的 norm、谱、初始化、抽样与条件期望合同。

> [!success] 第二波停靠线
> 不看正文，能从 $H$ 写出 $\mu,L,\kappa$；分别算出 GD 在 $\eta=1/4,2/5,1/2$ 下的两个 factors；从 heavy-ball 更新重建两个双根 $\pm1/3$；最后推导 batch covariance、$5/(32B)$ 单步注入与 $11/(56B)$ 稳态平台。还必须能解释 spectral radius、function gap、oracle complexity 与 wall-clock 为什么不是同一种“更快”。

第三波在同一个 $H$ 上加入线性项与第一波的三角形约束：

$$
f(x)=\frac12x^THx-b^Tx,
\qquad
H=\operatorname{diag}(1,4),
\qquad
b=(1,5/2)^T,
$$

$$
C=\{x\in\mathbb R^2:x_1\ge0,\ x_2\ge0,\ x_1+x_2\le1\}.
$$

OPT-09 在 $x_0=0$ 比较 identity metric、exact $H$ metric 与首步 gradient-square metric，三者分别给出

$$
(1,5/2)^T,
\qquad
u=H^{-1}b=(1,5/8)^T,
\qquad
(1,1)^T,
$$

从最小反例说明 diagonal adaptivity 不等于 Newton curvature。OPT-10 进一步验证 exact Newton 从任意点一步到 $u$，Newton decrement square 为 $41/16$；再用 $A=\operatorname{diag}(1,2),c=(1,5/4)^T$ 把目标写成 affine least squares，使 Gauss–Newton 精确等于 $H$，并用 $s=(1,1)^T,y=(1,4)^T$ 闭合 secant curvature $s^Ty=5$。

由于 $\mathbf1^Tu=13/8>1$，OPT-11 必须加入约束几何。Euclidean projection 与 $H$-metric projection 分别是

$$
\Pi_C^I(u)=(11/16,5/16)^T,
\qquad
\Pi_C^H(u)=x^*=(1/2,1/2)^T.
$$

在 $x^*$，$-\nabla f(x^*)=(1/2,1/2)^T$ 属于预算 face 的 normal cone，故 projected-gradient mapping 为零而原始 gradient 非零。OPT-12 最后把 normal 展开成三条 inequality 的 multipliers：

$$
\lambda^*=(1/2,0,0)^T,
\qquad
f(x^*)=-9/8,
$$

并逐项闭合 primal feasibility、dual feasibility、stationarity 与 complementary slackness；Slater point $(1/4,1/4)^T$ 又说明本例的 convex KKT 足以证明唯一 global optimum。预算 constraint 缩放 2 倍时 multiplier 缩为 $1/4$，提醒读者 multiplier 与 residual 都有 units/scale contract。

> [!success] 第三波停靠线
> 不看正文，能解释 movement metric、objective Hessian 与 gradient-square state 的区别；从任意点重建 Newton one-step；分别算出 $I$-metric 与 $H$-metric projection；写出 tangent/normal、gradient mapping 和 $\lambda^*=(1/2,0,0)$ 的四组 KKT。还必须能说明 inner solve residual、projection residual、KKT residual 与 deployment constraint violation 不是一个量。

## 一、范围与边界

### 本卷包含

- 优化问题的变量、目标、约束、domain、可行集、最优值与解集；
- 凸集、凸锥、相对内部、投影、分离与支撑超平面；
- 凸函数、epigraph、Jensen、一阶/二阶判据和保凸运算；
- 次梯度、Fenchel 共轭、光滑性、强凸性和条件数；
- 梯度下降、加速、随机梯度、自适应方法与二阶方法；
- 投影、KKT、Lagrange 对偶、Slater、proximal 与 mirror geometry；
- 非凸驻点、鞍点、局部几何以及深度网络优化声明的边界。

### 本卷不替代

- 多元微积分：梯度、Hessian、链式法则、JVP/VJP 与隐式微分见 10.4；
- 数值分析：浮点、线性求解、Krylov、停止准则和混合精度见 10.8；
- 统计学习理论：小训练目标不自动给 population generalization；
- 因果或决策理论：优化给定目标不证明目标本身正确；
- 任意深度学习经验配方：定理保证必须保留凸性、光滑性、噪声、步长和 oracle 条件。

## 二、先固定五层对象

| 层 | 核心问题 | 常见错误 |
|---|---|---|
| 建模 | 变量、数据、目标、约束和随机性是什么？ | 把 hyperparameter、batch 或部署指标漏出问题定义 |
| 几何 | domain/feasible set/level set 是否凸、闭、有界？ | 看公式像“平方”就宣布整个问题凸 |
| 最优性 | 要 global、local、stationary、saddle 还是 approximate solution？ | loss 不再下降就称已达到最优 |
| 算法 | 用什么 oracle、步长、初始化、精度和停止规则？ | 把更新式与收敛定理视为同一件事 |
| 统计/部署 | empirical objective 与 population/decision risk 如何连接？ | 把 optimization gap 当成全部误差 |

## 三、16 个核心节点与依赖图

~~~mermaid
flowchart LR
    O1["OPT-01 问题 / 可行域 / 解"] --> O2["OPT-02 凸集 / 分离"]
    O1 --> O3["OPT-03 凸函数 / Jensen"]
    O2 --> O3
    O3 --> O4["OPT-04 次梯度 / 共轭"]
    O3 --> O5["OPT-05 光滑 / 强凸"]
    O5 --> O6["OPT-06 梯度下降"]
    O6 --> O7["OPT-07 加速 / 动量"]
    O6 --> O8["OPT-08 随机梯度"]
    O8 --> O9["OPT-09 自适应方法"]
    O5 --> O10["OPT-10 Newton / GGN / BFGS"]
    O2 --> O11["OPT-11 投影 / 可行方向"]
    O11 --> O12["OPT-12 Lagrange / KKT"]
    O4 --> O13["OPT-13 对偶 / Slater"]
    O12 --> O13
    O4 --> O14["OPT-14 proximal / composite"]
    O4 --> O15["OPT-15 mirror / natural geometry"]
    O8 --> O16["OPT-16 非凸 / 鞍点 / 深网"]
    O10 --> O16
~~~

| ID | 节点 | 必须回答的问题 | 状态 |
|---|---|---|---|
| OPT-01 | [[优化问题、可行域与局部最优]] | 变量、目标、约束、最优值和解概念怎样完整定义？ | draft |
| OPT-02 | [[凸集、凸组合与分离超平面]] | 哪些可行域保持线段，投影和分离为何能产生证书？ | draft |
| OPT-03 | [[凸函数、Jensen 不等式与上图集]] | 函数的 chord、epigraph、导数与 Jensen 判据如何统一？ | draft |
| OPT-04 | [[次梯度、共轭函数与 Fenchel 对偶]] | 不可微凸函数如何线性支撑并进入对偶？ | draft |
| OPT-05 | [[光滑性、强凸性与条件数]] | 曲率上下界如何控制目标差距与优化速度？ | draft |
| OPT-06 | [[一阶最优性条件与梯度下降]] | 负梯度何时下降，步长和迭代复杂度怎样推出？ | draft |
| OPT-07 | [[加速梯度、动量与下界]] | 惯性怎样改善凸问题最坏情形，何时导致振荡？ | draft |
| OPT-08 | [[随机梯度与小批量估计]] | 无偏/有偏噪声、方差和采样怎样改变收敛？ | draft |
| OPT-09 | [[自适应优化方法]] | AdaGrad、RMSProp、Adam 的坐标几何和证明边界是什么？ | draft |
| OPT-10 | [[Newton 法、Gauss-Newton 与拟 Newton 法]] | Hessian、曲率近似和线性求解怎样形成可靠二阶步？ | draft |
| OPT-11 | [[投影、约束与可行方向]] | 更新离开可行域后，投影/切锥怎样恢复可行性？ | draft |
| OPT-12 | [[Lagrange 乘子与 KKT 条件]] | 约束资格下，梯度平衡和互补松弛如何刻画局部最优？ | draft |
| OPT-13 | [[弱对偶、强对偶与 Slater 条件]] | 对偶函数为何给下界，何时 gap 为零？ | draft |
| OPT-14 | [[近端算子、复合优化与稀疏正则]] | 光滑损失与不可微正则怎样分开计算？ | draft |
| OPT-15 | [[镜像下降、Bregman 几何与自然梯度]] | 非欧氏单位球、Bregman geometry 与 Fisher metric 怎样改变一步？ | draft |
| OPT-16 | [[非凸优化、鞍点与深度网络损失地形]] | 没有全局凸性时还能保证什么、测量什么、不能声称什么？ | draft |

## 四、四阶段学习路线

### 阶段 A：先把问题和几何写对

1. [[优化问题、可行域与局部最优]]；
2. [[凸集、凸组合与分离超平面]]；
3. [[凸函数、Jensen 不等式与上图集]]。

验收：能把一个 AI 训练描述改写成数学 problem contract；能判断常见集合/函数的凸性；能区分 attained optimum、infimum、local/global/stationary；能用图、定义和导数三种方式证明凸性。

### 阶段 B：一阶几何与算法

4. 次梯度与共轭；
5. 光滑、强凸与条件数；
6. 梯度下降；
7. 加速/动量；
8. 随机梯度；
9. 自适应方法。

验收：能从 oracle 假设逐行推出下降和复杂度界，分清 deterministic/stochastic、last/average iterate、convex/nonconvex guarantee。

### 阶段 C：二阶、约束与对偶

10. Newton/Gauss–Newton/拟 Newton；
11. 投影与可行方向；
12. KKT；
13. 对偶与 Slater。

验收：能画 primal/dual 对象，检查 constraint qualification，报告 primal feasibility、dual feasibility、stationarity、complementarity 与 linear-solve residual。

### 阶段 D：结构化复合问题与非凸深网

14. proximal；
15. mirror/natural geometry；
16. 非凸与鞍点。

验收：能从 regularizer/geometry 推出算子而非背更新式；能把深网实验的经验观察与真正 theorem 分开。

## 五、全卷必须维持的区分

| 容易混淆 | 正确区分 |
|---|---|
| objective vs metric | 优化目标是算法直接求解的标量；部署 metric 可能不可导、延迟或多目标 |
| domain vs feasible set | domain 使函数有定义；feasible set 还同时满足全部约束 |
| infimum vs minimum | infimum 可不被任何点取得；minimum 必须有 optimizer |
| local optimum vs stationary point | 可微内点局部最优通常 stationary；反向不成立 |
| convex set vs convex function | 前者约束点之间的线段；后者约束图像相对 chord 的位置 |
| convex parameterization vs convex output set | 输出属于凸集，不表示用深网参数优化就是凸问题 |
| strict vs strong convexity | strict 给解唯一性但不一定给统一曲率；strong 给二次下界 |
| optimization gap vs generalization gap | 前者相对经验目标最优值；后者比较经验与 population |
| convergence of values vs iterates | $f(x_k)\to f^*$ 不总推出 $x_k$ 收敛或靠近唯一点 |
| theorem vs diagnostic | gradient norm、KKT residual、loss plateau 都要在相应假设下解释 |

## 六、AI 调用地图

| 场景 | 正式优化对象 | 首要边界 |
|---|---|---|
| linear/logistic regression | convex empirical risk，可能加 convex regularizer | 数据分离、不可达最小值、conditioning、统计错设 |
| deep network training | 非凸 finite-sum/stochastic objective | 对称性、鞍点、batch noise、优化与泛化不等价 |
| adversarial training | min–max / robust optimization | inner maximization 未解、threat set、surrogate mismatch |
| constrained generation | inequality/equality/conic constraints | feasibility、constraint qualification、relaxation gap |
| sparse/low-rank learning | composite/proximal 或 nonconvex factorization | convex penalty 与因子化不是同一几何 |
| attention/probability | simplex、entropy、logsumexp | mask/domain、temperature、数值稳定与非严格方向 |
| fairness/privacy | constrained multi-objective empirical problem | estimand、sampling、infeasibility 与 subgroup shift |
| bilevel/meta-learning | outer objective through inner solution map | inner solve residual、nonuniqueness、implicit-gradient bias |

## 七、证据分工

- Boyd–Vandenberghe 与 Stanford EE364A：面向工程和 AI 的 convex sets/functions/problems、recognition、optimality 与 duality主线；
- MIT 6.253 与 Bertsekas：relative interior、closure、recession、separation、conjugacy 和存在性的严格证明层；
- Rockafellar：凸分析的经典完整理论与 extended-value 语言；
- Nesterov、Bubeck 与 Beck：一阶/加速/复合方法的 oracle 假设和复杂度；
- [[S-2022-Su-9070-logsumexp不等式]]：logsumexp、平滑 max 与 Jensen 的中文 AI 入口；Hessian/epigraph/保凸定理由正式教材承担；
- [[S-2018-Su-5655-SGD到动量加速]]、[[S-2020-Su-7521-从采样看优化]]、[[S-2020-Su-7787-有限学习率与隐式正则]]、[[S-2024-Su-10588-Hessian近似与自适应学习率]]、Muon 与流形最速下降文章：现代优化问题入口；不单独承担一般收敛率、Hessian 等价或全局最优定理；
- Lee/Jin：严格鞍点的渐近避免与有限时间扰动逃逸；Karimi：PL 条件；Ge/Laurent：带模型族条件的 benign landscape；Dinh/Garipov：参数化 sharpness 与 mode-connectivity 的经验边界。它们共同约束 OPT-16 的非凸结论阶梯。

## 八、当前稳定结论与缺口

| 节点 | 已建立 | 仍需验收 |
|---|---|---|
| [[优化问题、可行域与局部最优]] | standard form、domain/feasible set、inf/min/argmin、local/global/stationary、存在性与三类误差、AI problem contract | 闭卷分类问题状态，构造反例，给真实模型写变量—目标—约束—证书 |
| [[凸集、凸组合与分离超平面]] | convex/affine/conic hull、常见集合、保凸运算、relative interior、投影、点集分离与支撑超平面 | 闭卷证明投影唯一与分离，手算 simplex/PSD/球，审计 relaxation/parameterization |
| [[凸函数、Jensen 不等式与上图集]] | chord/epigraph/line/gradient/Hessian 判据、Jensen、保凸 calculus、logsumexp 与 AI objective 边界 | 闭卷从三种判据证明凸性，手算 Jensen gap/LSE Hessian，识别 composition 方向 |
| [[次梯度、共轭函数与 Fenchel 对偶]] | subdifferential geometry/calculus、Fermat、conjugate examples、Fenchel–Young/biconjugate 与 basic dual template | 闭卷手算次微分/共轭，证明 equality，审计 qualification 与 variational critic gap |
| [[光滑性、强凸性与条件数]] | 三类 Lipschitz、descent lemma、strong convexity、cocoercivity、gap–distance–gradient 与 $\kappa$ | 闭卷推导证书链，计算 least-squares/logistic/LSE 常数，审计 point/region/global curvature |
| [[一阶最优性条件与梯度下降]] | variational inequality、finite-step descent、nonconvex stationarity、convex $O(1/k)$、strong-convex geometric rate 与 quadratic spectrum | 闭卷完成 telescoping/rate，手算 stable step，复现 learning-rate stability map |
| [[加速梯度、动量与下界]] | HB eigenmode/Jury stability、quadratic optimal parameters、NAG potential、$O(1/k^2)$、$\sqrt\kappa$ rate 与 oracle lower bound | 闭卷重建 roots/potential/lower-bound 条件，复现 momentum root map 与 restart 审计 |
| [[随机梯度与小批量估计]] | conditional oracle、iid/相关/无放回 batch variance、convex/nonconvex rate、strong-convex noise floor、accumulation/DDP contract | 闭卷推导三类 bound，实测 noise covariance、batch scaling 与 Lyapunov floor |
| [[自适应优化方法]] | variable metric、AdaGrad regret、RMSProp/Adam states、bias correction、AMSGrad、AdamW/L2 边界与 Hessian heuristic | 闭卷手算 states/证明 regret，复现 Adam failure，并审计真实 framework contract |
| [[Newton 法、Gauss-Newton 与拟 Newton 法]] | 二次模型/decrement、damped/trust-region Newton、inexact Newton–CG、GN/LM、BFGS/SR1/L-BFGS 与曲率对象审计 | 闭卷证明局部二次收敛/BFGS SPD，复现 residual/rank/negative-curvature 三类边界 |
| [[投影、约束与可行方向]] | tangent/linearized/normal cone、projection 定理、simplex/PSD/affine 算法、gradient mapping 与 PGD 下降 | 闭卷证明 firm nonexpansive/PGD descent，审计 adversarial PGD 与 inexact projection |
| [[Lagrange 乘子与 KKT 条件]] | equality/active-normal 推导、四组 KKT、LICQ/MFCQ/Slater 分工、critical-cone 二阶条件、KKT system 与 SVM/MaxEnt | 闭卷构造 CQ failure/证明 convex sufficiency，手算 scale-aware residual 与 AI 约束证书 |
| [[弱对偶、强对偶与 Slater 条件]] | weak/strong duality、value/attainment、relative-interior Slater、separation、Fenchel/Lasso dual、Farkas 与 positive-gap/nonattainment 反例 | 闭卷推导三角形 Max-Cut gap、构造合法 primal–dual certificate，审计 inexact dual bound |
| [[近端算子、复合优化与稀疏正则]] | prox/resolvent、firm nonexpansiveness、Moreau、常见 closed forms、ISTA/FISTA、gradient mapping 与 splitting boundary | 闭卷证明下降/rate，手算 threshold/Moreau，审计 inexact/nonconvex prox 与部署稀疏收益 |
| [[镜像下降、Bregman 几何与自然梯度]] | Bregman/three-point/regret、entropy update、Fisher trust region、invariance、exact/empirical Fisher/GGN 与 Muon 分界 | 闭卷推 regret/invariance，数值核对 actual KL，审计 damping、K-FAC、采样分布与 spectral geometry |
| [[非凸优化、鞍点与深度网络损失地形]] | FOSP/SOSP、strict/degenerate saddle、stable-manifold 与 perturbed-GD 条件、negative curvature、非凸 PL、benign landscape、深网 symmetry/sharpness/mode connectivity | 闭卷重建 theorem 条件和三个反例；完成 HVP/Lanczos 研究协议与累计复现门 |

## 九、当前进度与下一步

OPT-01—16 已形成完整教学卷：16 篇正文、16 幅机制图、240 道 A—E 节点题与独立详解，正文覆盖为 **16/16**。卷末另有[[阶段测验 - 优化与凸分析（10.7）|OPT-CUM-01 100 分闭卷题卷]]、[[阶段测验解答 - 优化与凸分析（10.7）|逐题评分详解]]和[[实验 - 优化与凸分析累计复现门|三轨计算复现门]]。当前语义为 **composed / not-attempted**：所有节点仍为 `draft`，因为尚无真实闭卷原稿、参数干预、评分和间隔复测证据。

### 卷末累计验收

| 组件 | 已组成内容 | 通过条件 |
|---|---|---|
| `OPT-CUM-01` | 210 分钟、100 分，A—E 五区覆盖 OPT-01—16 | 总分至少 80 且各区达线，三道主证明不得为 0 |
| 独立详解 | 定义、手算、证明、反例和研究合同逐项评分 | 正式作答前不得打开；错题必须回链节点 |
| 计算门 | strict-saddle escape、nonconvex PL、scale-sharpness 三轨 | canonical hash、随机手算轨、参数干预与 48 小时重建均通过 |

截至 2026-08-27，OPT-01—12 已按当前初学者教学合同完成前三波静态迁移并通过精确计算与图像回归；正文学习状态保持 `draft`。下一施工点为 OPT-13—16：从当前 KKT 证书进入 dual function/Slater，再用 composite prox、mirror/Fisher geometry 与非凸地形完成正文迁移收束。

### 2026-08-23 图像标准化进度

OPT-01—16 的主图已按最新版图文规范完成迁移，当前进度为 **16/16**：

- OPT-01—04 已建立 optimization contract、凸集/凸函数与 Fenchel 证书的教材式机制图；OPT-05—08 已建立曲率夹逼、梯度下降、加速/动量与随机梯度的“假设—算法—速率—噪声”连续图组；OPT-09—12 已建立 variable metric、二阶曲率对象、投影锥几何与 KKT 的“几何—子问题—证书”图组；OPT-13—16 已用对偶证书、近端算子、镜像/Fisher 几何和非凸地形完成全卷收束；
- 每幅图均补齐“图要回答的问题—对象与结论—来源或脚本—怎样读图—图没有证明什么”的完整图文单元；
- 16 幅图由四个 `v2` 生成脚本可复现生成；章级检查确认 `v1=0`、相对路径 `=0`、`|880=16/16`，全部通过 SVG 规范、XML、1200 px 渲染与人工视觉检查；
- 图像标准化施工已完成。下一章转入 10.8 数值计算，优先清理其 19 处相对路径，并把误差—稳定性—算法实验图统一为同一规范。
