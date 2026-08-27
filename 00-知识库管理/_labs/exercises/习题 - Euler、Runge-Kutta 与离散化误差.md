---
type: exercise
status: draft
area: [math/ode, math/numerical-analysis, ai/neural-ode, ai/generative-modeling]
topic: "Euler、Runge-Kutta 与离散化误差"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Euler、Runge-Kutta 与离散化误差]]", "[[常微分方程、初值问题与解的存在唯一性]]", "[[Taylor 展开与余项]]"]
related: ["[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[误差传播、条件估计与停止准则]]"]
solution: "[[解答 - Euler、Runge-Kutta 与离散化误差]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - Euler、Runge–Kutta 与离散化误差

> [!abstract] 训练目标
> 从“会把公式写进循环”升级为能证明、诊断和审计的 ODE numerical analyst：明确 exact flow 与 computed path，区分 local/global error、order/stability/tolerance，能从 Taylor expansion 构造 RK 方法，并能判断 Neural ODE、ResNet 与 finite-step generator 中究竟对哪个离散或连续对象作出结论。

> [!warning] 作答约定
> 每次写“误差 $O(h^p)$”必须声明是 exact-start defect、normalized truncation error、global grid error还是task error；每次写“稳定”必须声明 finite-horizon perturbation stability还是absolute stability；每次写“gradient正确”必须声明它是 $\nabla J$ 还是 $\nabla J_h$。

## A. 识别、定义与公式结构

### DYN-RK-A01

对 IVP

$$
y'=f(t,y),\qquad y(t_0)=y_0,
$$

定义或区分：

1. exact trajectory、exact flow step、numerical grid state、dense output；
2. one-step method与increment function；
3. exact-start one-step defect $d_{n+1}$；
4. normalized local truncation error $\tau_{n+1}$；
5. global grid error $e_n$；
6. consistency、order、convergence；
7. finite-horizon perturbation stability与absolute stability；
8. NFE、accepted step、rejected step；
9. model error、discretization error与roundoff。

解释为什么“Euler local error是 $O(h)$”和“Euler local error是 $O(h^2)$”可能都来自规范文献，但必须查看定义。

### DYN-RK-A02

完整写出：

1. Forward Euler；
2. Heun / explicit trapezoidal；
3. explicit midpoint；
4. classical RK4；
5. 一般 $s$-stage Runge–Kutta method；
6. Butcher tableau中 $A,b,c$ 的含义；
7. explicit RK对 $A$ 的结构要求；
8. internal consistency $c=A\mathbf1$；
9. 一、二、三、四阶的标准order conditions；
10. RK stability function

$$
R(z)=1+zb^\top(I-zA)^{-1}\mathbf1.
$$

最后解释：为什么“四个stages”不自动意味着“四阶”？

### DYN-RK-A03

围绕 adaptive solver 建立术语图：

1. embedded pair与local estimator；
2. atol、rtol、component scale与weighted RMS norm；
3. accept/reject、safety factor、clipping与PI controller；
4. dense output、event root与maximum step；
5. FSAL与NFE；
6. tolerance sweep与reference solution；
7. continuous sensitivity、continuous adjoint、discrete adjoint与checkpoint。

回答：为什么 $\operatorname{err}\le1$、solver返回success、NFE较少、task loss较低四件事都不能互相替代？

## B. 手算、构造与数值量级

### DYN-RK-B01

对

$$
y'=y,\qquad y(0)=1,\qquad 0\le t\le1,
$$

取 $h=1/N$。

1. 写出 exact solution；
2. 计算 Euler 的 exact-start one-step defect并展开到 $h^3$；
3. 求 Euler endpoint

$$
y_N=(1+h)^N;
$$

4. 利用

$$
\log(1+h)=h-\frac{h^2}{2}+\frac{h^3}{3}+O(h^4)
$$

证明

$$
e-y_N=\frac e2h+O(h^2);
$$

5. 解释local $O(h^2)$与global $O(h)$如何同时出现；
6. 分别写出Heun、midpoint、RK4的stability polynomial；
7. 对 $h=1/2$ 手算三种方法到 $T=1$ 的endpoint和absolute error。

### DYN-RK-B02

考虑一般两stage explicit RK：

$$
\begin{array}{c|cc}
0&0&0\\
a&a&0\\
\hline
&b_1&b_2
\end{array}.
$$

1. 从一、二阶conditions推出

$$
b_1+b_2=1,\qquad ab_2=\frac12;
$$

2. 分别构造 Heun、explicit midpoint 与 Ralston $(a=2/3)$ 的系数；
3. 对 nonlinear IVP

$$
y'=y^2,\qquad y(0)=1
$$

做一个step，证明任意上述二阶family都有

$$
y_1=1+h+h^2+\frac a2h^3;
$$

4. 与 exact

$$
y(h)=\frac1{1-h}
=1+h+h^2+h^3+O(h^4)
$$

比较local leading error；
5. 哪个 $a$ 使这个特定问题的 $h^3$ coefficient最接近exact？这是否证明它对所有ODE都最好？

### DYN-RK-B03

用 Euler–Heun embedded pair处理

$$
y'=-2y,\qquad y_n=1,\qquad h=0.1.
$$

取Euler为低阶值、Heun为高阶值：

1. 计算 $y^{[1]}_{n+1}$、$y^{[2]}_{n+1}$ 与 $\delta$；
2. 取

$$
\operatorname{atol}=10^{-3},
\qquad
\operatorname{rtol}=10^{-2},
$$

并用

$$
s=\operatorname{atol}
+\operatorname{rtol}
\max(|y_n|,|y_{n+1}^{[2]}|)
$$

计算scaled error；
3. 判断step是否accepted；
4. lower order为 $q=1$，取safety $0.9$，不做clipping，计算

$$
h_{\rm new}
=0.9h\,\operatorname{err}^{-1/2};
$$

5. 若100维state中只有一个component normalized error为 $9$，其余为 $0$，weighted RMS是否accept？max norm如何判断？
6. 解释为什么以上计算仍不能保证endpoint global error小于 $10^{-2}$。

## C. 证明、阶条件与可微求解

### DYN-RK-C01

设one-step method

$$
y_{n+1}=y_n+h\Psi(t_n,y_n,h)
$$

满足：

$$
\|\Psi(t,u,h)-\Psi(t,v,h)\|
\le L_\Psi\|u-v\|,
$$

$$
\|d_{n+1}\|\le Ch^{p+1}
$$

在包含exact与numerical trajectories的region上一致成立。

1. 从error recurrence推导

$$
\|e_{n+1}\|
\le(1+hL_\Psi)\|e_n\|+Ch^{p+1};
$$

2. 用几何和或discrete Grönwall证明，若 $e_0=0$，

$$
\|e_n\|
\le
\frac C{L_\Psi}
\left(e^{L_\Psi(t_n-t_0)}-1\right)h^p
$$

（并处理 $L_\Psi=0$）；
3. 明确proof中fixed horizon、smoothness、invariant region与exact arithmetic各在哪里使用；
4. 推广到variable steps $h_n$，令 $H=\max h_n$；
5. 说明为什么该证明不能直接替multistep method完成全部convergence理论。

### DYN-RK-C02

1. 从一般RK stage expansion推导

$$
b^\top\mathbf1=1,
\qquad
b^\top c=\frac12;
$$

2. 对classical RK4逐项验证一至四阶conditions；
3. 对test equation $y'=\lambda y$ 推导

$$
R_4(z)
=1+z+\frac{z^2}{2}
+\frac{z^3}{6}
+\frac{z^4}{24};
$$

4. 说明 $R_4(z)$ 是 $e^z$ 的四阶Taylor polynomial，但为什么这不等于对所有 $z$ 都准确或stable；
5. 在negative real axis上比较 $z=-1,-2,-3$ 时Euler、RK2与RK4的 $|R(z)|$，判断哪些衰减；
6. 把“order条件”和“absolute stability条件”写成两列不可混用的验收表。

### DYN-RK-C03

考虑scalar parameterized ODE

$$
y'=\theta y,\qquad y(0)=1,
\qquad
J(\theta)=\frac12(y(T)-c)^2.
$$

1. 求exact $y(T)$ 与continuous gradient $dJ/d\theta$；
2. 用 $N$ 步Euler、$h=T/N$ 得到

$$
y_N=(1+h\theta)^N;
$$

3. 求computed objective

$$
J_h(\theta)=\frac12(y_N-c)^2
$$

的exact derivative；
4. 从Euler computation graph推导discrete adjoint recursion与parameter-gradient sum，并证明等于第3问；
5. 展开证明 $y_N-y(T)=O(h)$，并在非退化条件下说明 $\nabla J_h-\nabla J=O(h)$；
6. 用central finite difference of $J_h$ 应该验证哪一个gradient？
7. 解释continuous adjoint、discrete adjoint与“反向重新积分但不复用forward path”三者的对象和数值风险。

## D. 反例、错误诊断与系统审计

### DYN-RK-D01

判断下列说法真伪，错误者给出反例或缺失条件：

1. Euler的local error是 $O(h^2)$，所以endpoint global error也是 $O(h^2)$。
2. 任意consistent one-step method在fixed smooth IVP上都自动convergent，不需要任何perturbation control。
3. RK4有四个stages，所以任意四stage explicit RK都是四阶。
4. 两个method order相同，则相同step下error相同。
5. $\operatorname{err}\le1$ 意味着每个component都在其atol/rtol尺度内。
6. solver success意味着global error达到requested tolerance。
7. Exact solution positive且stable，则Euler approximation也positive且stable。
8. Dense output由高阶solver产生，所以自动与grid method同阶。
9. Continuous objective gradient与finite-step solver objective gradient在任意step下相同。
10. NFE更少意味着Neural ODE更准确、更快且task performance更好。

### DYN-RK-D02

构造并分析五类失败：

1. Local defect小但large step下absolute instability；
2. 一步内发生两次event crossing，端点sign相同而被漏检；
3. weighted RMS接受但关键单component严重超标；
4. discontinuous forcing使classical high-order Taylor argument失效；
5. truncation error下降到roundoff/reference floor后，继续减step不再改善。

第2问可取

$$
g(t)=(t-\tfrac14)(t-\tfrac34)
$$

并让solver从 $0$ 一步跨到 $1$。第3问使用100维、单component normalized error $9$。每个反例都要说明修复策略及修复后仍不能声称什么。

### DYN-RK-D03

某团队报告：

> 我们用默认RK45训练Neural ODE。Solver全部success，平均NFE从80降到20，验证loss也下降，因此continuous model、forward trajectory和gradient都已达到 $10^{-3}$ 相对精度，且新模型更稳定。

逐层审计：

1. 默认method/version、rtol/atol与component scales是否记录？
2. Success flag实际证明什么？
3. NFE下降有哪些互相冲突的解释？
4. 应怎样做tolerance、method、precision与max-step sweep？
5. Endpoint、max-trajectory、dense output、event与task error如何分账？
6. Continuous stability、solver absolute stability与training stability如何区分？
7. 使用continuous adjoint、discrete adjoint还是checkpoint adjoint？
8. 如何用finite difference与forward-state reuse审计gradient？
9. Adaptive accept/reject branch如何影响computed map？
10. 给出一份最小可复现solver card，并把团队现有证据放到正确层级。

## E. AI迁移、综合推导与研究设计

### DYN-RK-E01

设一族depth-$N$ residual models：

$$
h_{k+1}^{(N)}
=h_k^{(N)}
+\frac TN
F_k^{(N)}(h_k^{(N)}).
$$

假设存在共同vector field $f(t,h)$，它在相关region对state为 $L$-Lipschitz，并且

$$
\sup_{k,h}
\|F_k^{(N)}(h)-f(kT/N,h)\|
\le\varepsilon_N.
$$

1. 把模型视为perturbed Euler method；
2. 推导fixed-time error bound，展示

$$
\max_k
\|h_k^{(N)}-y(kT/N)\|
\le C_T\left(N^{-1}+\varepsilon_N\right);
$$

3. 说明需要哪些smoothness、bounded-region与initial alignment条件；
4. 若 $\varepsilon_N\not\to0$，还能否声称收敛到该ODE？
5. Untied arbitrary blocks、BatchNorm、dropout与hard routing分别破坏或改变哪些假设？
6. 设计一个depth-refinement实验，避免把“同一网络简单加层”冒充共同refinement family。

### DYN-RK-E02

设计一个 Neural ODE solver benchmark，同时比较：

- fixed Euler、Heun、RK4；
- embedded adaptive RK；
- discrete backprop；
- continuous/checkpoint adjoint。

要求明确：

1. 至少一个有exact solution的nonstiff IVP；
2. 一组fixed-step refinement；
3. 一组rtol/atol sweep；
4. endpoint、max-trajectory、NFE、rejection与wall time；
5. finite-difference gradient reference；
6. forward/reverse trajectory mismatch；
7. task metric与trajectory metric分账；
8. float32/float64或mixed-precision对照；
9. event/dense-output测试；
10. 预注册acceptance与failure criteria；
11. 如何避免reference solver与被测solver共享同一偏差；
12. 结论如何限制在nonstiff、smooth、指定region与指定实现内。

### DYN-RK-E03

研究finite-NFE diffusion/flow generation中的三种对象：

$$
\text{instantaneous field }v_\theta(t,x),
$$

$$
\text{step-conditioned average velocity }
\bar v_{\theta,h}(t,x),
$$

$$
\text{finite-step map }F_{\theta,h}(x).
$$

1. 写出三者的理想关系；
2. 说明为什么固定大step下它们不能无条件互换；
3. 比较“高阶积分instantaneous field”“直接学习average velocity”“distill finite-step map”的误差账本；
4. 分析semigroup consistency

$$
F_{h_1+h_2}
\stackrel{?}{=}
F_{h_2}\circ F_{h_1};
$$

5. 设计step-size-conditioned training与unseen-step evaluation；
6. 把model error、quadrature error、solver error与score/velocity estimation error分开；
7. 说明continuous likelihood或probability-flow claim何时仍成立；
8. 加入discrete adjoint/gradient audit；
9. 报告NFE–quality Pareto frontier；
10. 给出一份不夸大的theorem/empirical claim模板。

## 提交检查表

- [ ] 15个稳定ID均已作答，A—E每层3题
- [ ] Local defect与global error没有混用
- [ ] RK stages、weights与time arguments完整
- [ ] Order与absolute stability分账
- [ ] atol/rtol声明了component scale与norm
- [ ] Rejected steps与NFE计入成本
- [ ] Dense output、event与discontinuity单独审计
- [ ] Continuous objective与computed discrete objective分开
- [ ] Gradient通过finite difference或独立实现检查
- [ ] AI结论包含solver/version/tolerance/precision/domain

