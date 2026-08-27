---
type: moc
status: active
area: [generative-models, diffusion, flow-matching, sde, ode]
aliases: [生成模型第七卷, 连续时间生成课程地图]
prerequisites: ["[[DDPM、DDIM 与离散时间扩散 MOC]]", "[[时间反演、score 与扩散生成动力学]]", "[[连续性方程与守恒律]]", "[[Fokker-Planck 方程与概率流 ODE]]"]
related: ["[[生成模型 MOC]]", "[[生成模型完整课程地图与掌握标准]]", "[[科学空间 - 第五章生成模型专题来源地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# SDE、概率流 ODE 与 Flow Matching MOC

> [!abstract] 分卷目标
> 本卷把离散扩散提升为连续时间随机动力学：先由局部条件矩识别 VP、VE 与 sub-VP SDE，再严谨处理 reverse-time SDE 与 probability-flow ODE。随后从连续性方程进入 Flow Matching，以条件期望统一 score regression、conditional vector-field regression、coupling 与 Rectified Flow。全卷的核心纪律是：**同边缘、同路径律、同总体最优点、同训练程序和同有限步采样器是不同命题。**

## 一、八个核心节点

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| GEN-49 | [[从离散扩散到 VP、VE 与 sub-VP SDE]] | 从局部均值/协方差推出三类 forward SDE 与闭式边缘 | verified |
| GEN-50 | [[Reverse-time SDE、时间反演与 Score Drift]] | 在明确时间方向下写对 reverse drift，并解释 score correction | verified |
| GEN-51 | [[Probability-flow ODE 与共享边缘分布]] | 由 Fokker–Planck 配平 canonical velocity，并限定 same marginals | verified |
| GEN-52 | [[Marginal Score、Conditional Score 与去噪等价]] | 证明条件 score 投影恒等式和 loss 常数差 | verified |
| GEN-53 | [[连续性方程、概率路径与 Flow Matching]] | 从弱连续性方程推出 simulation-free velocity regression | verified |
| GEN-54 | [[Conditional Flow Matching、Coupling 与最优传输路径]] | 证明 conditional-to-marginal field，并审计 coupling 方差 | verified |
| GEN-55 | [[Rectified Flow、ReFlow 与轨迹直化]] | 区分直线 teacher segment 与 learned marginal trajectory | verified |
| GEN-56 | [[Diffusion、Flow、速度参数化与统一证据地图]] | 用证据层级统一 diffusion、PF ODE、FM 与 stochastic interpolant | verified |

## 二、全卷统一方向与符号

固定 $t\in[0,1]$：$t=0$ 是数据端，$t=1$ 是噪声/参考分布端。forward SDE 写作

$$
dX_t=f(X_t,t)\,dt+g(t)\,dW_t,
\qquad X_0\sim p_{data}.
$$

本卷默认 $g$ 是与空间无关的标量；一般矩阵扩散 $G(x,t)$ 必须额外保留 $D=GG^\top$ 的散度项。生成时有两种合法记法：

1. 保持变量 $t$，从 $1$ 积到 $0$，于是 $dt<0$；
2. 令反向时钟 $\tau=1-t$，再把全部 drift 符号转换后从 $0$ 积到 $1$。

正文不混用两种记法。若在第一种记法中写 reverse SDE，则

$$
dX_t=\left[f(X_t,t)-g(t)^2\nabla_x\log p_t(X_t)\right]dt
+g(t)d\bar W_t,
\qquad t:1\downarrow0.
$$

probability-flow ODE 为

$$
\frac{dX_t}{dt}=f(X_t,t)-\frac12g(t)^2\nabla_x\log p_t(X_t).
$$

这里的 $1$ 与 $1/2$ 不矛盾：reverse SDE 仍有扩散通量，PF ODE 则把全部密度变化编码进确定性速度。

## 三、等价主张六级表

| 层级 | 精确定义 | 本卷允许的说法 | 不能推出 |
|---|---|---|---|
| E1 同单时刻边缘 | 对每个 $t$，$\mathcal L(X_t)=p_t$ | SDE 与 PF ODE 共享 one-time marginals | 同 transition/path law |
| E2 同密度方程 | 满足同一个 FP/continuity equation | 两个动力学在所列正则条件下运输同一 $p_t$ | 轨迹逐样本相同 |
| E3 同总体最优点 | 两个 population loss 的函数空间 minimizer 相同 | conditional regression 可替代不可得 marginal target | loss 数值相等、有限网训练相同 |
| E4 相差常数 | $L_1(\theta)=L_2(\theta)+C$ 且 $C$ 与 $\theta$ 无关 | population gradient 相同 | Monte Carlo estimator 方差相同 |
| E5 同连续解 | exact score/velocity 与 exact integration 给同端点 law | 可比较理想连续模型 | 同有限 NFE 输出 |
| E6 同程序表现 | 数据、模型、优化、solver、NFE 与随机数均受控后经验接近 | 受控实验结论 | 一般定理或历史优先权 |

## 四、科学空间研读主线

| 文章 | 本卷作用 | 必须补严的边界 |
|---|---|---|
| [[S-2022-Su-9209-扩散模型SDE篇]] | 离散到 SDE、反向 score drift 的中文入口 | 时间方向、反向扩散定理假设 |
| [[S-2022-Su-9228-概率流ODE]] | Fokker–Planck 到 PF ODE | same marginals 不等于 same paths |
| [[S-2022-Su-9280-硬刚扩散ODE]] | Jacobian、density Taylor 与 continuity 的推导桥 | 一阶形式推导不替代全局 flow/PDE 定理 |
| [[S-2022-Su-9305-万有引力到扩散模型]] | PFGM 与增广场线的替代直觉 | 不是 FM/扩散统一定理 |
| [[S-2022-Su-9370-构建ODE一般步骤上]] | spacetime divergence 与速度场不唯一性 | Green function 构造的正则/边界条件 |
| [[S-2022-Su-9379-构建ODE一般步骤中]] | conditional path 到 marginal field | 直线条件路径不等于直线群体轨迹 |
| [[S-2023-Su-9467-W距离与得分匹配]] | Wasserstein–score 界及证明缺口示范 | 回查原定理假设，不补写不存在的证明 |
| [[S-2023-Su-9497-构建ODE一般步骤下]] | Rectified Flow/ReFlow 中文入口 | OT、convex cost 与直化结论回查原论文 |
| [[S-2023-Su-9509-得分匹配与条件得分匹配]] | 条件期望与平方损失投影 | “=”不是逐样本或数值相等 |

一级证据由 [[S-1982-Anderson-Reverse-Time-Diffusion]]、[[S-2021-Song-Score-SDE]]、[[S-2023-Lipman-Flow-Matching]]、[[S-2022-Liu-Rectified-Flow]]、[[S-2024-Tong-Conditional-Flow-Matching]]、[[S-2025-Albergo-Stochastic-Interpolants]] 与 [[S-2022-Kwon-Wasserstein-Score]] 承担。

## 五、四本误差账

| 账 | 对象 | 典型问题 |
|---|---|---|
| model | $s_\theta$ 或 $v_\theta$ 与 population target 的差 | 函数类、数据、权重、优化是否改变近似？ |
| process | 选了哪条 SDE、probability path 或 endpoint coupling | 只定 marginals 还是定完整 joint law？ |
| solver | Euler/Heun/adaptive ODE/SDE discretization | NFE、强/弱误差、容差和末步噪声怎样记？ |
| evaluation | finite samples 与指标 | score loss、Wasserstein、likelihood、FID 是否同一口径？ |

## 六、当前出口

- 前置卷：[[DDPM、DDIM 与离散时间扩散 MOC]]
- 数学底座：[[ODE、动力系统与 SDE MOC]]
- 数值审计：[[实验 - 连续扩散、Flow Matching 与 Rectified Flow 最小数值审计]]
- 本卷累计门：[[50.7 分卷累计测验与复现门]]
- 后继：[[生成模型完整课程地图与掌握标准#十一、50.8 离散扩散、潜空间与多模态生成（GEN-57—64）|50.8 离散与潜空间生成]]
