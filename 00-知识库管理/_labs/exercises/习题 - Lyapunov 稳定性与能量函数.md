---
type: exercise
status: draft
area: [math/ode, math/dynamical-systems, ai/optimization, ai/safety]
topic: "Lyapunov 稳定性与能量函数"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Lyapunov 稳定性与能量函数]]", "[[相图、平衡点与局部稳定性]]", "[[二次型与正定矩阵]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[Kronecker 积、向量化与矩阵方程]]"]
solution: "[[解答 - Lyapunov 稳定性与能量函数]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Lyapunov 稳定性与能量函数

> [!abstract] 训练目标
> 把“能量好像在下降”升级为可审计的稳定性证书。每一题都必须明确：系统、平衡点、验证区域、函数正定性、沿流导数、解的存在区间、结论强度，以及结论究竟针对连续流、离散更新还是学习到的近似模型。

> [!warning] 作答公约
> 只写 $\dot V\le 0$ 不算完整答案。必须继续回答它能推出 stability、set convergence、point convergence、asymptotic stability 还是 exponential stability；若调用 LaSalle，必须求 largest invariant subset；若声称 global，必须核查 properness、forward completeness 或等价的有界性条件；若声称指数稳定，必须给出 $V$ 与状态距离的上下界。

## A. 识别、定义与定理边界

### DYN-LYAP-A01

围绕自治系统

$$
\dot x=f(x),\qquad f(x_*)=0,
$$

定义或解释下列对象，并逐项说明它在 Lyapunov 证明中扮演什么角色：

1. positive definite、positive semidefinite、negative definite；
2. locally positive definite 与 globally positive definite；
3. radially unbounded / proper；
4. class-$\mathcal K$ 与 class-$\mathcal K_\infty$ function；
5. Lie derivative $L_fV$；
6. sublevel set $\Omega_c=\{x:V(x)\le c\}$；
7. forward invariant set；
8. basin of attraction 与其 certified inner approximation。

最后判断并证明或反驳：

> 任意连续、全局正定的 $V:\mathbb R^n\to\mathbb R$ 都是 proper 的。

### DYN-LYAP-A02

完整复述并比较下列三条结果：

1. Lyapunov direct method 的 local stability 结论；
2. strict decrease 给 local asymptotic stability 的结论；
3. LaSalle invariance principle 的 regional 版本。

要求回答：

- 每条定理对 $f,V$、区域与解有什么条件？
- $E=\{x:\dot V(x)=0\}$ 与其中 largest invariant subset $M$ 有什么差别？
- 为什么 $\dot V\le 0$ 一般只说明 $V(x(t))$ 不增，而不能自动说明 $x(t)\to x_*$？
- 什么时候 LaSalle 只能得到到集合的距离趋于零？

### DYN-LYAP-A03

建立下面三类证书对象的对照表：

$$
\text{continuous ODE: }L_fV(x),
\qquad
\text{discrete map: }\Delta V(x)=V(F(x))-V(x),
$$

$$
\text{SDE: }\mathcal LV(x)
=\nabla V(x)^\top b(x)
+\frac12\operatorname{tr}\!\bigl(\sigma(x)\sigma(x)^\top\nabla^2V(x)\bigr).
$$

对每类对象说明：

1. 演化对象和稳定性概念；
2. 需要验证的 inequality；
3. step size、diffusion 与 sample loss 分别会带来什么额外问题；
4. continuous-time Neural ODE 上的 $L_fV<0$ 为什么不自动证明其数值 solver 的一步映射也满足 $\Delta V<0$；
5. energy-based model 中的“能量”为什么不自动是 Lyapunov function。

## B. 手算、构造与定量界

### DYN-LYAP-B01

考虑标量系统

$$
\dot x=-x+x^3=x(x^2-1),
\qquad
V(x)=\frac12x^2.
$$

1. 求 $\dot V$ 及其符号区域；
2. 对 $0<c<1/2$，证明 $\Omega_c$ compact 且 forward invariant；
3. 用 direct method 证明原点 local asymptotically stable；
4. 求原点的精确 basin of attraction；
5. 解释为什么 $c=1/2$ 的闭子水平集不能直接作为“所有点都收敛到原点”的证书；
6. 说明 $V$ 虽然 proper，为什么仍不能由这一个 $V$ 得到原点 global asymptotic stability；
7. 对任意给定 $r\in(0,1)$，在 $|x|\le r$ 上给出形如

$$
\dot V\le-\alpha_r V
$$

的最大常数 $\alpha_r$，并由此给出状态衰减界。

### DYN-LYAP-B02

考虑阻尼振子

$$
\dot q=p,\qquad
\dot p=-q-\gamma p,\qquad \gamma>0.
$$

1. 对物理能量

$$
E(q,p)=\frac12(q^2+p^2)
$$

计算 $\dot E$，用 LaSalle 证明原点 global asymptotically stable；
2. 解释为何 $\dot E=0$ 的直线 $p=0$ 不是 invariant set；
3. 构造带交叉项的候选函数

$$
V_\varepsilon(q,p)
=\frac12(q^2+p^2)+\varepsilon qp.
$$

求出一个显式的 $\varepsilon$ 范围，使 $V_\varepsilon$ positive definite 且 $\dot V_\varepsilon$ negative definite；
4. 把结果写成

$$
m_\varepsilon\|(q,p)\|^2
\le V_\varepsilon(q,p)
\le M_\varepsilon\|(q,p)\|^2,
\qquad
\dot V_\varepsilon\le-\beta_\varepsilon\|(q,p)\|^2,
$$

并给出一个可计算的指数收敛界；
5. 比较 $E$ 与 $V_\varepsilon$：为什么前者更自然，却需要 LaSalle；后者较“人工”，却能直接给速率？

### DYN-LYAP-B03

考虑非正规线性系统

$$
\dot x=Ax,\qquad
A=
\begin{pmatrix}
-1&6\\
0&-2
\end{pmatrix}.
$$

1. 证明 $A$ Hurwitz；
2. 取 $Q=I$，解连续 Lyapunov 方程

$$
A^\top P+PA=-I
$$

并验证

$$
P=
\begin{pmatrix}
\frac12&1\\
1&\frac{13}{4}
\end{pmatrix};
$$

3. 证明 $P\succ0$，对 $V=x^\top Px$ 求 $\dot V$；
4. 从 $\lambda_{\min}(P),\lambda_{\max}(P)$ 推出一个显式状态指数界；
5. 对 $x_0=2^{-1/2}(1,1)^\top$，计算

$$
\left.\frac d{dt}\|x(t)\|_2^2\right|_{t=0},
$$

说明欧氏范数为何会暂态增长；
6. 解释“某个范数暂态增长”和“存在严格 Lyapunov function”为什么不矛盾。

## C. 证明、推广与结构联系

### DYN-LYAP-C01

设 $x_*=0$，$f$ locally Lipschitz，$V\in C^1$ 在原点某邻域 $D$ 上 positive definite，且

$$
L_fV(x)\le0.
$$

1. 用 sphere minimum

$$
m_\varepsilon=\min_{\|x\|=\varepsilon}V(x)
$$

重建 Lyapunov stability 的完整 $\varepsilon$–$\delta$ 证明；
2. 明确指出为什么要让相应 sublevel set 留在 $D$ 内；
3. 若进一步在 $D\setminus\{0\}$ 上 $L_fV<0$，用 compact annulus 论证轨道不能永远停留在

$$
\eta\le\|x(t)\|\le\varepsilon
$$

中，从而证明 attraction；
4. 解释该证明在哪一步仍然只是 local 的；
5. 给出把结论升级为 global asymptotic stability 的一组充分条件。

### DYN-LYAP-C02

证明连续时间 Lyapunov theorem：

> 对实方阵 $A$，以下命题等价：
>
> 1. $A$ Hurwitz；
> 2. 对每个 $Q\succ0$，存在唯一 $P\succ0$ 满足 $A^\top P+PA=-Q$；
> 3. 存在某对 $P\succ0,Q\succ0$ 满足该方程。

要求：

1. 从 $A$ Hurwitz 出发，用

$$
P=\int_0^\infty e^{A^\top t}Qe^{At}\,dt
$$

证明收敛、正定性与矩阵方程；
2. 用 homogeneous Lyapunov equation 或 Sylvester spectrum 证明 uniqueness；
3. 从某个 $P,Q\succ0$ 出发，证明所有解指数趋零，因而 $A$ Hurwitz；
4. 给出

$$
\|x(t)\|_2
\le
\sqrt{\frac{\lambda_{\max}(P)}{\lambda_{\min}(P)}}
\exp\!\left(
-\frac{\lambda_{\min}(Q)}
{2\lambda_{\max}(P)}t
\right)\|x(0)\|_2;
$$

5. 说明 $P$ 的 condition number 对证书给出的 transient prefactor 有什么影响。

### DYN-LYAP-C03

考虑机械系统

$$
\dot q=v,\qquad
\dot v=-\nabla U(q)-\gamma v,
\qquad \gamma>0,
$$

其中 $q,v\in\mathbb R^d$，$U\in C^1$。

1. 令

$$
E(q,v)=U(q)-U(q_*)+\frac12\|v\|^2.
$$

计算 $\dot E$；
2. 假设 $q_*$ 是 $U$ 的唯一 critical point，$U(q)-U(q_*)$ positive definite 且 proper，证明 $(q_*,0)$ global asymptotically stable；
3. 证明时必须写出 compact sublevel、forward completeness 与 largest invariant subset 三步；
4. 去掉“唯一 critical point”后，LaSalle 至多给出什么集合结论？
5. 取一维 double-well

$$
U(q)=\frac14(q^2-1)^2,
$$

列出所有 equilibria，说明 energy decrease 为什么不能保证从任意初值到同一个 global minimizer。

## D. 诊断、反例与证书审计

### DYN-LYAP-D01

判断下列说法真伪。错误者给出反例或缺失条件，正确者给出最短严谨证明。

1. $V(x)>0$ 且 $\dot V(x)\le0$ 对所有 $x\ne0$，必有 $x(t)\to0$。
2. 若 $V$ positive definite 且 proper，则每个 $\Omega_c$ 都 compact。
3. $\dot V<0$ automatically implies exponential stability。
4. 若 $A$ 的所有 eigenvalues 实部为负，则 $\|e^{At}\|_2$ 单调下降。
5. 若 $A$ Hurwitz，则对任意 $Q\succ0$ 均有唯一 $P\succ0$ 解连续 Lyapunov equation。
6. continuous gradient flow 中 objective 单调下降，所以参数一定收敛到唯一 minimizer。
7. $V(F(x))-V(x)<0$ 是 discrete-time 对应的 strict Lyapunov condition。
8. 同一个 $V$ 对不确定参数族中的每个系统都下降，可给 uniform robust stability。
9. 在有限训练样本上均有 $L_fV<0$，就证明了整个连续区域上的 inequality。
10. EBM 的低 energy state 必是其 sampling dynamics 的 asymptotically stable equilibrium。

### DYN-LYAP-D02

逐一构造并分析以下“缺条件就失败”的反例：

1. positive semidefinite $V$ 无法控制完整状态距离；
2. $\dot V=0$ 但系统只有 Lyapunov stability，没有 attraction；
3. $V$ 全局 positive definite、$\dot V\le0$，但因不 proper 且解可逃向无穷，不能推出 global stability/convergence；
4. 连续系统 asymptotically stable，但 explicit Euler 因步长过大而不稳定；
5. 一组有限 sample 上 inequality 全部通过，但 samples 之间仍存在 violation。

第 3 小题可研究

$$
\dot x=x(x^2-1),
\qquad
V(x)=x^2e^{-x^2}.
$$

第 5 小题要求你给出一个具体连续函数 $g:[-1,1]\to\mathbb R$ 和有限 sample set $S$，使 $g(s)<0$ 对所有 $s\in S$，但某个未采样点 $x$ 有 $g(x)>0$。随后说明，若 $g=L_fV$，还需要什么全区域验证工具或解析 bound。

### DYN-LYAP-D03

某 Neural ODE 团队报告：

> 我们联合训练了 neural vector field $f_\theta$ 与 neural Lyapunov candidate $V_\phi$。在 $10^6$ 个训练点上，$V_\phi(x)>0$ 且 $\nabla V_\phi(x)^\top f_\theta(x)<0$；RK4 仿真也未发散，所以模型已被证明 globally exponentially stable。

请做一份逐层审计：

1. candidate 的归一化、平衡点与 differentiability 是否明确？
2. positivity 与 derivative inequality 的验证 domain 是什么？
3. samples、optimizer success 与 formal region-wide proof 有什么差别？
4. 如何用 counterexample-guided falsifier 改进训练？
5. 若网络为 ReLU、smooth activation 或含 normalization，verification 难点分别是什么？
6. 如何从 positive/negative margin 升级到 exponential state bound？
7. continuous vector field、RK4 map、finite precision implementation 分别需验证什么？
8. global claim 还缺 properness、forward completeness 或哪些结构？
9. 若存在 input/disturbance，应把结论改写成哪类 robust/ISS claim？
10. 给出从最弱到最强的六级证据阶梯，并把团队现有证据放到正确层级。

## E. AI 迁移、综合推导与研究设计

### DYN-LYAP-E01

考虑 gradient flow

$$
\dot\theta=-\nabla L(\theta),
\qquad
V(\theta)=L(\theta)-L_*.
$$

1. 证明 $\dot V=-\|\nabla L(\theta)\|^2$；
2. 若满足 Polyak–Łojasiewicz inequality

$$
\frac12\|\nabla L(\theta)\|^2
\ge\mu\bigl(L(\theta)-L_*\bigr),
$$

证明 objective gap 的 exponential decay；
3. PL 是否自动给参数到唯一 minimizer 的距离收敛？说明缺什么；
4. 若 $L$ 为 $\mu$-strongly convex 且 $L_s$-smooth，推导参数距离界；
5. 对 $L(\theta)=\theta^4/4$ 解出 gradient flow，证明原点 asymptotically stable 但不是 exponentially stable；
6. 对 preconditioned flow

$$
\dot\theta=-G(\theta)^{-1}\nabla L(\theta)
$$

给出保证 $L$ 不增的条件，并解释其与 natural gradient / geometry 的联系；
7. 说明训练 loss 下降与 test performance、parameter convergence、flat-minimum selection 之间不能互相替代。

### DYN-LYAP-E02

研究带动量的非凸优化动力学

$$
\dot q=v,\qquad
\dot v=-\nabla L(q)-\gamma v,
\qquad \gamma>0.
$$

1. 构造 mechanical energy 并求导；
2. 在 $L$ lower bounded 且其 sublevel sets compact 时，证明轨道有界；
3. 用 LaSalle 说明 $\omega$-limit set 落在

$$
\{(q,0):\nabla L(q)=0\};
$$

4. 为什么这不保证到 global minimizer，也不自动保证到某个单点？
5. 对 $L(q)=\frac14(q^2-1)^2$ 分析三个 equilibria 的局部性质与可能极限；
6. 设计一个带交叉项的 local quadratic Lyapunov candidate，解释它如何连接 Hessian 与 linearized heavy-ball system；
7. 比较“objective decrease”“total energy decrease”“parameter norm decrease”三种完全不同的陈述。

### DYN-LYAP-E03

设计一个可审计的“稳定 learned dynamics”研究方案。对象可以是 Neural ODE、continuous-depth residual model、learned controller 或 equilibrium model。方案必须包括：

1. 明确 state、equilibrium/target set、domain 与 autonomous/time-varying 假设；
2. 选择 analytic、SOS、quadratic 或 neural candidate 的理由；
3. positivity 与 Lie derivative 的 quantitative margins；
4. learner–falsifier–formal verifier 闭环；
5. regional sublevel 与 basin inner estimate；
6. continuous-time certificate 到离散 solver 的单独验证；
7. data shift、disturbance 与 model error 下的 robust inequality；
8. 需要时采用 common Lyapunov function、time-varying $V$ 或 stochastic generator；
9. ablation：无证书、sample-only、formal regional、formal + discrete 四层；
10. 失败案例、counterexamples 与不确定结论的报告规范；
11. 与 task metric 的接口；
12. 一份不夸大结论的 theorem statement 模板。

要求最后给出一页 certificate card，使第三方能仅凭卡片复查“证明了什么、没证明什么、在哪个区域、针对哪个演化对象”。

## 提交检查表

- [ ] 15 个题号均已作答，且 A—E 每层 3 题
- [ ] 每个 stability claim 都声明 local / regional / global
- [ ] 每个 convergence claim 都区分 point / set / objective / state
- [ ] 每个 LaSalle 题都求了 largest invariant subset
- [ ] 每个 exponential claim 都展示 energy–state 上下界
- [ ] 连续 ODE、离散更新、SDE 与 sample loss 没有混用
- [ ] AI 审计包含 domain、margin、verifier、solver 与 task metric
- [ ] 没把“实验未失败”写成“定理已证明”
