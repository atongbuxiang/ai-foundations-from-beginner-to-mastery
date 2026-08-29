---
type: derivation
status: draft
area: [neural-networks/residual-stability, ode, numerical-analysis]
aliases: [ResNet as Euler Method, Continuous-Depth Networks]
node_id: NN-43
prerequisites: ["[[残差块 Jacobian 与梯度直通]]", "[[常微分方程、初值问题与解的存在唯一性]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
related: ["[[线性 ODE 与矩阵指数]]", "[[刚性系统、绝对稳定域与隐式方法]]", "[[流映射、Liouville 公式与连续正规化流]]", "[[残差缩放、Lipschitz 界与深度稳定性]]"]
sources: ["[[S-2018-Lu-Numerical-ODE-Networks]]", "[[S-2018-Chen-Neural-ODE]]", "[[S-2018-Haber-Ruthotto-Stable-Architectures]]"]
exercises: ["[[习题 - ResNet 的 ODE 与离散动力系统视角]]"]
solutions: ["[[解答 - ResNet 的 ODE 与离散动力系统视角]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-resnet-euler-stability-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---

# ResNet 的 ODE 与离散动力系统视角

> [!abstract] 本章主问题
> $x_{k+1}=x_k+h f(x_k,t_k)$ 同时是显式 Euler 步和带 scale 的 residual block。这一同形关系能把 step size、稳定域、局部/全局误差和伴随方法引入架构分析；但只有在固定时间区间、残差为 $O(h)$、向量场族一致且满足正则/稳定条件时，“网络加深”才是一个 ODE 极限，而不是把任意 ResNet 改名为微分方程。

## 课程位置与两遍学习路线

- **承接什么：** NN-41—42 已把 $\mathcal R_\square$ 写成四个 $I+hA$ 的 residual/Jacobian 乘积；
- **本页解决什么：** 固定 horizon $T=1$，把 $h=T/N$ 恢复到公式中，比较离散状态、exact flow、局部 defect 与绝对稳定条件；
- **后续为何需要：** NN-44 将把 Euler/variational product 改写成 depth-uniform Lipschitz 与 forcing 界，后续 Neural ODE/CNF 则需要区分离散反传和连续 adjoint。

**第一遍只做深度加密表。** 对两个 eigen-directions 分别算 $N=1,2,4,10$ 的 Euler multiplier，并与 $e^{\lambda T}$ 比较；看清加深必须同时缩小 $h$。

**第二遍再检查 ODE 极限。** 审计向量场族、固定 horizon、local/global error、zero/absolute stability、shape topology、自适应 solver 与 backward discretization。

### 问题链

1. residual branch $F_k$ 在什么条件下可写成 $h f(x_k,t_k)$？
2. 深度翻倍但每层 update 不缩小，为什么通常不是同一 ODE 的网格加密？
3. local $O(h^2)$ defect 怎样在 Lipschitz 条件下累积成 global $O(h)$ error？
4. 连续系统 $\operatorname{Re}\lambda<0$ 为何仍可能被显式 Euler 离散得不稳定？
5. discrete backprop 与 continuous adjoint 在什么极限/误差控制下才可比较？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal R_\square$ 中算出 $N=4$ 的 Euler 值 $(1.21550625,0.0625)$，与 exact flow $(e^{1/5},e^{-2})$ 比较，并解释第二方向的 multiplier 为 $1-2/N$，就已掌握本页主干。

## 符号与对象账本

| 对象 | 定义 | 数值分析身份 | 常见偷换 |
|---|---|---|---|
| $T$ | 固定 depth-time horizon | 比较不同网格的共同区间 | 随网络深度一起增长 |
| $N,h=T/N$ | steps 与 step size | 网格分辨率 | 把 $h$ 隐去并固定为 1 |
| $f(x,t)$ | 连续向量场 | ODE 生成元 | 任意互不相关的 layer family |
| $F_k=h f_k$ | residual increment | Euler 单步增量 | 未缩放的完整映射 |
| $\tau_k$ | exact solution 代入一步所得 defect | local truncation error | global terminal error |
| $1+h\lambda$ | Euler test-equation multiplier | 离散稳定判据 | continuous multiplier $e^{h\lambda}$ |

### 贯穿算例 $\mathcal R_\square$：同一 horizon 上加密深度

考虑线性 ODE

$$
\dot x=Ax,
\qquad
A=\operatorname{diag}\left(\frac15,-2\right),
\qquad
x(0)=(1,1)^{\mathsf T},
\qquad
T=1.
$$

exact flow 是

$$
x(1)=e^Ax(0)
=\left(e^{1/5},e^{-2}\right)
\approx(1.221403,0.135335).
$$

$N$ 层 Euler/ResNet 使用 $h=1/N$：

$$
x_N
=\left(I+\frac AN\right)^N x_0
=\left(\left(1+\frac1{5N}\right)^N,
\left(1-\frac2N\right)^N\right).
$$

| $N$ | expanding direction | dissipative direction |
|---:|---:|---:|
| 1 | $1.2$ | $-1$ |
| 2 | $1.21$ | $0$ |
| 4 | $1.21550625$ | $0.0625$ |
| 10 | $1.21899442$ | $0.10737418$ |
| exact | $1.22140276$ | $0.13533528$ |

$N=4$ 正是 NN-41—42 的 residual chain：每层 matrix 为 $I+A/4=\operatorname{diag}(21/20,1/2)$。两个方向都在趋向 exact flow，但速度和离散行为不同；耗散方向在粗网格上甚至出现翻转或被一步压成 0。

若把 depth 从 4 增到 8，却仍让每层使用 $I+A/4$，得到的是

$$
\left(I+\frac A4\right)^8x_0,
$$

对应 horizon 约从 1 延长到 2，而不是在 $[0,1]$ 上把网格加密。因此“更多 residual layers”只有在 scale 与参数族同时受控时才支持 continuous-depth 解释。

## 核心公式七问：Euler–ResNet 对应

$$
\boxed{
x_{k+1}=x_k+h f(x_k,t_k),
\qquad
h=\frac TN
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 用离散 residual increments 近似固定时间区间上的连续 flow |
| 对象 | 一族共享 horizon、step-aware、正则受控的 depth-indexed networks |
| 来路 | 对 ODE 积分式在每个网格区间使用左端点矩形近似 |
| 步骤 | 固定 $T$→选 $N,h$→在 $t_k$ 评估 vector field→加 $hf$→重复 |
| 读法 | residual branch 是带单位的 increment $hf$；$f$ 本身不是直接相加的 state |
| 检查 | 网格加密收敛、local defect、test-equation stability、discrete/continuous gradient 对比 |
| 去路 | Neural ODE、continuous adjoint、CNF、stable architectures 与 depth-scaling laws |

### AI / 系统对应

把 ResNet 看成数值格式有助于设计 step scale、稳定 block 和 adaptive computation，但 wall-clock 并不按“函数评估次数”以外的理论量自动改善。Neural ODE 的 tolerance、rejected steps、event handling、adjoint重算和非确定 kernel 都应进入成本/误差账；任务 accuracy 也不能由 solver order 单独推出。

## 一、学习目标

读完本节，你应能：

1. 建立 residual layer 与 explicit Euler 的带单位对应；
2. 解释为什么固定 $h=1$ 的加深不等于网格加密；
3. 从 local truncation error 推导 Euler global $O(h)$ 界；
4. 用 test equation 画出绝对稳定条件；
5. 区分一致性、零稳定性、绝对稳定性与动力系统稳定性；
6. 说明 time-dependent parameters、shape change 与 stochastic layer 的 ODE 边界；
7. 区分 discrete backprop 与 continuous adjoint；
8. 审计 solver tolerance、adaptive steps、可逆性和真实计算成本。

## 二、从 residual block 到 Euler step

考虑初值问题

$$
\dot x(t)=f(x(t),t;\theta(t)),
\qquad
x(0)=x_0,
\qquad
t\in[0,T].
$$

取均匀网格

$$
t_k=kh,
\qquad
h=\frac{T}{N},
$$

显式 Euler 为

$$
\boxed{
x_{k+1}=x_k+h f(x_k,t_k;\theta_k)
}.
$$

把

$$
F_k(x)=h f(x,t_k;\theta_k)
$$

代入，就得到 residual block $x_{k+1}=x_k+F_k(x_k)$。

## 三、单位与尺度不能消失

若 $x$ 带“state 单位”，$t$ 带“depth-time 单位”，则 $f=dx/dt$，$hf$ 才与 $x$ 同单位。深度从 $N$ 增到 $2N$、但仍固定每层 update 大小，相当于：

- 固定 $h$、把终止时间从 $T$ 延长到 $2T$；或
- 同时改变向量场；

而不是自动在同一 $[0,T]$ 上把 step 减半。

要研究固定 horizon 的连续极限，通常需要

$$
h=\frac{T}{N},
\qquad
\|F_k\|=O(1/N).
$$

## 四、time-dependent network 是允许的

每层参数不同并不阻止 ODE 解释；它可对应 piecewise-constant 时间函数

$$
\theta_N(t)=\theta_k,
\qquad t\in[t_k,t_{k+1}).
$$

但当 $N$ 改变时，需要一族 $\theta_N(t)$ 有一致界、正则或某种收敛性，才能谈“趋向同一个 $f(x,t)$”。任意重训两个不同深度模型，只因 block 形式相似，并不能证明它们是同一连续系统的两个网格。

## 五、local truncation error

把 exact solution 代入 Euler update，定义单步 defect

$$
\tau_k
=x(t_{k+1})-x(t_k)-h f(x(t_k),t_k).
$$

若 $x$ 二次可微，由 Taylor 公式

$$
x(t_k+h)
=x(t_k)+h\dot x(t_k)+\frac{h^2}{2}\ddot x(\xi_k),
$$

所以

$$
\|\tau_k\|
\le Ch^2,
\qquad
C=\frac12\sup_{t\in[0,T]}\|\ddot x(t)\|.
$$

这是 local $O(h^2)$，还不是最终时刻 global error。

## 六、从 local 到 global：离散 Gronwall

令数值解为 $x_k$，误差

$$
e_k=x(t_k)-x_k.
$$

若 $f$ 对 state 是 $L_f$-Lipschitz，

$$
\begin{aligned}
e_{k+1}
&=e_k+h\left[f(x(t_k),t_k)-f(x_k,t_k)\right]+\tau_k,\\
\|e_{k+1}\|
&\le(1+hL_f)\|e_k\|+Ch^2.
\end{aligned}
$$

若 $e_0=0$，几何级数给出

$$
\|e_k\|
\le
Ch^2\frac{(1+hL_f)^k-1}{hL_f}.
$$

用 $(1+hL_f)^k\le e^{L_ft_k}$，得到

$$
\boxed{
\|e_k\|
\le
\frac{C}{L_f}(e^{L_ft_k}-1)h
}.
$$

因此在这些条件下 Euler global error 是 $O(h)$。误差界里的指数因子也提醒：一致性小不等于长时间误差一定小。

## 七、线性 test equation 与稳定域

考虑

$$
\dot x=\lambda x.
$$

exact solution 为

$$
x(t)=e^{\lambda t}x_0.
$$

若 $\operatorname{Re}\lambda<0$，连续系统衰减。Euler update 是

$$
x_{k+1}=(1+h\lambda)x_k.
$$

离散衰减需要

$$
\boxed{|1+h\lambda|<1}.
$$

这在复平面中是以 $-1$ 为圆心、1 为半径的圆盘内部。连续稳定的 $\lambda$ 若 step 太大，仍可能落到 Euler 稳定域之外。

## 八、一个深度加密手算

取

$$
\dot x=-2x,
\qquad
x(0)=1,
\qquad
T=1.
$$

exact value 是

$$
x(1)=e^{-2}\approx0.135335.
$$

Euler 深度 $N$ 的结果为

$$
x_N=\left(1-\frac2N\right)^N.
$$

| $N$ | $h$ | multiplier | $x_N$ |
|---:|---:|---:|---:|
| 1 | 1 | $-1$ | $-1$ |
| 2 | $1/2$ | $0$ | $0$ |
| 4 | $1/4$ | $1/2$ | $0.0625$ |
| 10 | $0.1$ | $0.8$ | $0.107374$ |

深度增加且 $h=T/N$ 时才逐步逼近 exact flow。若每层仍用 multiplier $1-2=-1$，加深只是延长交替振荡。

## 九、四种“稳定”不要混写

### 9.1 连续动力稳定

相邻初值的 exact trajectories 是否靠近。

### 9.2 数值绝对稳定

对 test equation，离散 multiplier 是否落在 stability region。

### 9.3 离散扰动稳定

有限层 map 对 state/roundoff/branch error 的放大是否受控。

### 9.4 优化稳定

参数更新、loss 与梯度是否在训练中受控。

一个结论不能自动替代另一个。例如 forward map contraction 不保证 parameter optimization convex；训练 loss 平稳也不证明 solver global error 小。

## 十、Euler Jacobian 与 residual Jacobian

Euler step 的 state Jacobian 是

$$
I+hJ_f(x_k,t_k),
$$

正是 residual Jacobian。连续 variational equation 是

$$
\dot V(t)=J_f(x(t),t)V(t),
\qquad
V(0)=I.
$$

离散 Jacobian product

$$
\prod_k(I+hJ_f(x_k,t_k))
$$

在适当条件下近似连续 fundamental matrix，但有限 $h$ 时二者不是同一个对象。

## 十一、discrete backprop 与 continuous adjoint

对已离散网络，精确 reverse mode 是离散 step Jacobian 的转置乘积：

$$
a_k=(I+hJ_f(x_k,t_k))^\mathsf Ta_{k+1}.
$$

连续 ODE 的 adjoint 满足

$$
\dot a(t)=-J_f(x(t),t)^\mathsf Ta(t)
$$

并从终点反向积分。以下两条路线通常不同：

1. **discretize then differentiate**：对 solver 实际离散图求导；
2. **differentiate then discretize**：先写连续 adjoint，再用另一个数值轨迹求解。

有限 tolerance、trajectory reconstruction、adaptive step 和浮点误差都可能造成 gradient mismatch。内存少不是“梯度自动精确”。

## 十二、自适应 solver 改变了什么

Neural ODE 用 error estimator 选择步长时：

- function evaluation 次数依输入、参数和 tolerance 变化；
- latency 不再仅由名义 depth 决定；
- rejected steps 仍消耗算力；
- 控制流对参数的导数语义需明确；
- 更小 tolerance 通常更贵，但不保证训练目标单调改善；
- stiff dynamics 可能迫使 explicit solver 取极小步。

因此应报告 `rtol/atol`、solver、最大步数、function evaluations、失败率、dtype 与 gradient route。

## 十三、shape 与 topology 边界

经典 ODE state 维度固定。普通 ResNet 会下采样、改 channel、拼接或投影，这些点可解释为 hybrid jump 或不同 state space 间的 map，但不再是一条单纯光滑 ODE flow。

在唯一性条件下，同维 exact ODE flow 对不同初值保持 injective；一般 Euler residual map 未必如此。例如

$$
F(x)=-x
$$

配 $h=1$ 时

$$
x^+=x+F(x)=0,
$$

所有输入塌到一点。反过来，加入 augmented dimensions、projection 或离散非可逆操作也会改变 topology 合同。

## 十四、ODE 类比什么时候有用

它适合回答：

1. residual scale 相当于多大 step；
2. depth 是 horizon 还是 resolution；
3. 线性化 eigenvalues 是否落在离散稳定域；
4. perturbation 怎样由 Gronwall 累积；
5. 是否值得使用多步、隐式、可逆或结构保持更新；
6. solver tolerance 与 compute 如何交换。

它不直接回答：

- 哪个架构在某数据集最好；
- SGD 是否收敛到全局最优；
- 离散网络是否泛化；
- 连续模型是否比 residual block 更有表达力。

## 十五、图：Euler 对应、稳定域与证据梯子

先看图回答：固定 horizon 时深度与 step size 怎样绑定？连续衰减为什么可能被 Euler 放大？从“公式同形”到“ODE 极限”还缺哪些门？

![[00-知识库管理/_assets/figures/neural-networks/fig-resnet-euler-stability-v2.svg|900]]

> [!figure] 图 30.6-03　ResNet–Euler 对应只有带上 step、horizon 与稳定条件才完整
> 左栏把 $x_{k+1}=x_k+hf_k(x_k)$ 放在深度网格上；中栏给出 $|1+h\lambda|<1$ 的稳定圆盘和 stable ODE / unstable Euler 反例；右栏从公式同形、一致参数族、local defect、离散 Gronwall 到任务实验逐级列门。来源：依据 Lu et al. 2018、Chen et al. 2018、Haber–Ruthotto 2018 与数值分析推导绘制；由 [[00-知识库管理/_labs/code/plot_residual_foundations_v2.py]] 确定性生成。

**怎样读图**：先固定 $T$，确认 $h=T/N$ 是否真的进入 branch；再在中栏检查离散 multiplier，而不是只看连续 $\operatorname{Re}\lambda$；最后按右栏逐门确认能否声称 ODE limit。

**图没有证明什么**：图没有证明任意已训练 ResNet 收敛到唯一 ODE，也没有证明更高阶 solver 对任务 loss、wall time 或泛化更好。

## 十六、可执行 ODE 审计表

| 项目 | 必须记录 |
|---|---|
| state | shape、单位、是否跨层变化 |
| time | horizon $T$、grid、$h$ |
| field | $f(x,t;\theta)$、参数共享/插值 |
| regularity | state Lipschitz、时间正则、解存在区间 |
| scheme | Euler/RK/implicit/multistep、order |
| stability | test spectrum、stability region、stiffness |
| error | local defect、global error、reference |
| gradient | discrete/continuous/checkpoint adjoint |
| system | tolerance、NFE、reject、dtype、latency |

## 十七、最小验收

1. 从 ODE 写出 Euler residual block；
2. 解释 $h=1$ 与 $h=T/N$ 的差别；
3. 推导 local defect $O(h^2)$；
4. 用离散 Gronwall 推出 global $O(h)$；
5. 画出 Euler stability disk；
6. 复算 $\dot x=-2x$ 的四个深度；
7. 区分四类 stability；
8. 写出 discrete VJP 与 continuous adjoint；
9. 给出非 injective Euler residual 反例；
10. 列出声称 ODE limit 的全部条件。

> [!summary]
> ResNet 与 Euler 的联系是精确的更新模板对应；把它提升为连续极限，则需要 $h\to0$、固定 horizon、$O(h)$ residual、一致向量场和稳定/正则条件。ODE 视角的价值在于暴露这些缺失合同，并把深度问题转化为可计算的 step、误差、稳定域和伴随问题。

- [[残差连接、深度与稳定性 MOC]]
- [[习题 - ResNet 的 ODE 与离散动力系统视角]]
- [[解答 - ResNet 的 ODE 与离散动力系统视角]]
