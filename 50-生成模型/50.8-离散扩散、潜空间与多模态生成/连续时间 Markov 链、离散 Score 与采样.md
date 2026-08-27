---
type: derivation
status: verified
area: [generative-models, discrete-diffusion, ctmc, score-modeling]
node_id: GEN-59
prerequisites: ["[[Categorical Diffusion、转移矩阵与离散后验]]", "[[矩阵函数与矩阵指数]]", "[[随机过程、Brownian 运动与二次变差]]", "[[时间反演、score 与扩散生成动力学]]"]
related: ["[[Absorbing-state、Mask Diffusion 与并行迭代生成]]", "[[Diffusion、Flow、速度参数化与统一证据地图]]"]
sources: ["[[S-2022-Campbell-Discrete-CTMC]]", "[[S-2024-Lou-SEDD]]", "[[S-2022-Su-9085-从重参数看离散概率分布]]"]
exercises: ["[[习题 - 连续时间 Markov 链、离散 Score 与采样]]"]
solutions: ["[[解答 - 连续时间 Markov 链、离散 Score 与采样]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-discrete-ctmc-reverse-ratio-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 连续时间 Markov 链、离散 Score 与采样

> [!abstract] 一句话结论
> 离散状态的连续时间扩散不是 SDE，而是跳跃过程。它用 generator $R_t$ 的非对角跳跃率描述 infinitesimal transition。精确反向 rate 等于 forward reverse-edge rate 乘上边缘概率比 $p_t(i)/p_t(j)$；这个 ratio 扮演离散 score。模型误差、时间离散误差与随机事件模拟成本必须分开。

## 一、从离散时间转移矩阵取连续极限

在很小时间 $h>0$ 上，设 transition matrix 有展开

$$
Q_{t,t+h}=I+hR_t+o(h).
$$

对 $i\ne j$，

$$
P(X_{t+h}=j\mid X_t=i)=hR_t[i,j]+o(h),
$$

所以 $R_t[i,j]\ge0$ 是单位时间跳跃率。行和必须为零：

$$
R_t[i,i]=-\sum_{j\ne i}R_t[i,j].
$$

对角元通常为负；它不是“留在原状态的负概率”，而是总离开率的负数。小步保持概率是

$$
P(X_{t+h}=i\mid X_t=i)
=1-h\lambda_t(i)+o(h),
\qquad \lambda_t(i)=\sum_{j\ne i}R_t[i,j].
$$

## 二、Kolmogorov forward equation

令 $p_t$ 是行分布。由全概率公式

$$
p_{t+h}=p_t(I+hR_t)+o(h).
$$

移项除以 $h$ 并令 $h\downarrow0$：

$$
\boxed{\frac{d}{dt}p_t=p_tR_t.}
$$

第 $j$ 个分量可写成流入减流出：

$$
\frac{d}{dt}p_t(j)
=\sum_{i\ne j}p_t(i)R_t[i,j]
-p_t(j)\sum_{k\ne j}R_t[j,k].
$$

这就是离散状态的 continuity equation：没有空间散度，只有图边上的 probability flux。

若 $R$ 常数，则

$$p_t=p_0e^{tR}.$$

这里 matrix exponential 是 stochastic semigroup；数值上直接 `expm` 适合小状态空间，巨大词表通常利用稀疏结构、uniformization 或事件模拟。

## 三、反向跳跃率的逐步推导

固定正向时间 $t$，考察很小区间 $[t-h,t]$。若正向在这段从 $i$ 跳到 $j$，联合概率的一阶项为

$$
P(X_{t-h}=i,X_t=j)
=p_{t-h}(i)hR_t[i,j]+o(h).
$$

给定末端 $X_t=j$，反向在 $h$ 内跳到 $i$ 的概率是

$$
P(X_{t-h}=i\mid X_t=j)
=hR_t[i,j]\frac{p_t(i)}{p_t(j)}+o(h),
$$

其中 $p_{t-h}(i)=p_t(i)+o(1)$。因此反向时钟下的 off-diagonal rate 为

$$
\boxed{
R_t^{rev}[j,i]
=R_t[i,j]\frac{p_t(i)}{p_t(j)},
\qquad i\ne j.}
$$

反向 diagonal 再由行和为零确定。公式包含三件事：

1. 必须存在正向反边 $i\to j$；
2. forward rate 给局部几何；
3. probability ratio 把边缘密度偏好加入反向生成。

若 $p_t(j)=0$，条件事件无定义。实际 noising process 通常设计成在训练时间内提供足够支持，或只在可达边上估计 ratios。

## 四、为什么离散 score 是 ratio 而不是梯度

连续空间 score 是

$$s_t(x)=\nabla_x\log p_t(x).$$

它比较 $x$ 邻域内 log density 的相对变化。离散 alphabet 没有默认无穷小位移，因此更自然的局部对象是有向边 $(j,i)$ 上的比值

$$
s_t(j\to i)=\frac{p_t(i)}{p_t(j)},
$$

或 log-ratio

$$
\ell_t(j\to i)=\log p_t(i)-\log p_t(j).
$$

两者关系是 $s=e^\ell$。ratio 直接乘到 reverse rate；log-ratio 数值更稳定且满足 cycle consistency：对闭环 $i_0\to i_1\to\cdots\to i_0$，真实 log-ratios 的和为零。

任意神经网络输出的 edge scores 未必满足这种全局一致性。生成只需局部 reverse rates 可用，但若声称“它来自某个全局 $p_t$”，就要额外检查 integrability/cycle constraints。

## 五、SEDD 学什么

[[S-2024-Lou-SEDD]] 的主线是直接估计 data-noised marginal 的 probability ratios，并设计 score entropy objective。课程保留三层：

- **population target**：真实 $p_t(i)/p_t(j)$；
- **network parameterization**：输入 noisy state、time 和 candidate transition，输出正值 ratio/log-ratio；
- **training estimator**：用已知 corruption conditional 构造可采样的 objective。

这与预测 $x_0$ 后再通过 Bayes 组装 reverse kernel 不同。两者在无限函数类下可能表示同一精确 reverse process，但有限模型的输出结构、归一化、方差和计算量不同。

## 六、两状态例子

设

$$
R=
\begin{bmatrix}
-a&a\\
b&-b
\end{bmatrix},
\qquad a,b>0.
$$

从 1 到 2 的 rate 是 $a$，从 2 到 1 是 $b$。若当前 marginal 为 $p_t=(0.8,0.2)$，则反向从 2 到 1 的 rate 是正向反边 $1\to2$ 的 rate 乘概率比：

$$
R_t^{rev}[2,1]=a\frac{0.8}{0.2}=4a.
$$

反向从 1 到 2 是

$$
R_t^{rev}[1,2]=b\frac{0.2}{0.8}=0.25b.
$$

概率大的状态在 reverse time 中更有吸引力。若 $p_t$ 恰为 stationary distribution $\pi=(b/(a+b),a/(a+b))$，则反向 rates 恢复原 rates，这正对应 detailed balance。

## 七、怎样模拟 CTMC

### 7.1 精确事件模拟的局部形式

若当前状态为 $i$，总离开率

$$\lambda_t(i)=\sum_{j\ne i}R_t[i,j].$$

时间齐次时，等待时间 $\Delta\sim\operatorname{Exp}(\lambda(i))$；发生跳跃后，目标状态按

$$P(J=j\mid\text{jump from }i)=\frac{R[i,j]}{\lambda(i)}$$

采样。这是 Gillespie 思想。时间非齐次时 rate 随时间变化，需要积分 hazard、thinning 或小步近似。

### 7.2 Tau-leaping / Euler 式近似

取小步 $h$，用

$$Q_h(i,\cdot)\approx e_i+hR_t[i,\cdot]$$

采下一状态。必须满足 $h\lambda_t(i)\le1$ 才保持非负；即使合法，一步最多一次跳跃，忽略了 $O(h^2)$ 多跳事件。

### 7.3 Uniformization

若选 $\Lambda\ge\max_i\lambda(i)$，令

$$P=I+R/\Lambda,$$

则可用 rate-$\Lambda$ Poisson clock 和离散转移 $P$ 模拟；其中 self-loop 是虚拟事件。它把 continuous time 和 discrete Markov kernel 连接起来，也便于建立误差/成本审计。

## 八、三本误差账

| 误差 | 来源 | 不能被哪项掩盖 |
|---|---|---|
| ratio/model | $s_\theta(j\to i,t)$ 偏离真实 probability ratio | 减小步长不能修复系统模型偏差 |
| time/event solver | tau-leap、thinning、有限事件截断 | exact network 不等于 exact sampler |
| terminal/reference | forward 终点尚未到易采 prior | 更精确反向率不能消除 prior mismatch |

network evaluation 次数、实际 jump 次数和 wall-clock 也要分别报告；一次网络可能同时输出大量邻边 rates。

## 九、科学空间接口

[[S-2022-Su-9085-从重参数看离散概率分布]] 从 iid additive noise + argmax 构造一次离散 choice probability，强调概率只依赖 logit 差。CTMC ratio 则描述时间 $t$ 上相邻状态的边缘质量比。两者共同说明“离散概率更自然地通过相对量来描述”，但前者不是 CTMC reverse-time theorem，后者也不需要把跳跃写成 Gumbel argmax 才成立。

## 十、图：forward flux 如何翻成 reverse rate

先看图回答：为什么反向从 $j$ 到 $i$ 要使用正向的 $i\to j$ rate？为什么 ratio 的分母必须是当前反向起点 $p_t(j)$？

![[00-知识库管理/_assets/figures/generative-models/fig-discrete-ctmc-reverse-ratio-v1.svg|900]]

> [!figure] 图 50.8-03　CTMC 的 flux、reverse rate 与离散 score
> 左侧由 $Q=I+hR$ 识别 rate，中间按 joint flux 做 Bayes，右侧把 probability ratio 放进 sampler 与误差账。来源：据 Campbell et al.、SEDD 与本节推导独立绘制。

**怎样读图**：跟踪一份 infinitesimal mass $p_t(i)R_t[i,j]h$；反向条件化时除以终点质量 $p_t(j)$，得到单位反向时间的跳率。

**图没有证明什么**：图不证明任意 learned edge ratios 来自全局一致分布，不证明 tau-leaping 无偏，也不证明 continuous-time discrete diffusion 在所有数据和预算下优于离散时间 D3PM。

## 十一、本节回顾与训练

- generator 非对角元是 rate、对角元是负总离开率；
- forward law 是 $p'_t=p_tR_t$；
- reverse rate = forward reverse-edge rate × marginal probability ratio；
- 离散 score 是边上的 ratio/log-ratio，不是类别 ID 的欧氏梯度；
- 模型、event solver 与 terminal prior 三本误差账不能相互抵消；
- [[习题 - 连续时间 Markov 链、离散 Score 与采样]]
- [[解答 - 连续时间 Markov 链、离散 Score 与采样]]
