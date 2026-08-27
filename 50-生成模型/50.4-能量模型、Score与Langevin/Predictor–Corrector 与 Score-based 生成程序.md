---
type: concept
status: verified
area: [generative-models, score-based-models, samplers]
node_id: GEN-31
prerequisites: ["[[Langevin、ULA、MALA 与平稳分布]]", "[[时间反演、score 与扩散生成动力学]]"]
related: ["[[多噪声尺度、退火去噪与 Score 网络]]", "[[SDE、概率流 ODE 与 Flow Matching MOC]]"]
sources: ["[[S-2021-Song-Score-SDE]]", "[[S-2019-Song-Ermon-NCSN]]"]
exercises: ["[[习题 - Predictor–Corrector 与 Score-based 生成程序]]"]
solutions: ["[[解答 - Predictor–Corrector 与 Score-based 生成程序]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-score-predictor-corrector-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Predictor–Corrector 与 Score-based 生成程序

> [!abstract] 本节主问题
> Predictor 沿 reverse-time dynamics 把样本从一个噪声时刻推进到下一个；Corrector 在当前时刻冻结 noise level，用 score-based MCMC 调整当前 marginal。二者针对不同误差。PC 是一个数值—统计组合框架，不是“corrector 一定把 predictor 错误纠正为零”的保证。

## 一、最小连续背景

考虑 forward SDE

$$
dX_t=f(X_t,t)dt+g(t)dW_t,
$$

其 marginal density 为 $p_t$。在正则条件下，reverse-time SDE 的 drift 依赖

$$
s_t(x)=\nabla_x\log p_t(x).
$$

若用反向时钟从 $T$ 积到 $0$，常见形式写作

$$
dX_t=[f(X_t,t)-g(t)^2s_t(X_t)]dt+g(t)d\bar W_t,
\qquad dt<0.
$$

符号必须连同“时间积分方向”书写；把 $dt<0$ 忽略会把 drift 符号读反。严格 reverse-time theorem 留给 50.7，本节只研究有限步算法合同。

## 二、Predictor 做什么

给时间网格 $T=t_N>\cdots>t_0=0$，predictor 使用 Euler–Maruyama、reverse-diffusion discretization 或更高阶 solver，从 $t_i$ 推进到 $t_{i-1}$：

$$
x_{i-1}^{P}
=\operatorname{Predict}
(x_i,t_i,t_{i-1};s_\theta,\xi_i).
$$

它近似的是跨时间 transition/density evolution。误差包括：

- time discretization；
- learned score bias；
- stochastic noise realization；
- stiffness 与 schedule；
- 参数化/preconditioning 数值误差。

## 三、Corrector 做什么

在固定 $t_{i-1}$，目标 marginal 暂时视为 $p_{t_{i-1}}$，其 score 为 $s_{t_{i-1}}$。用若干步 Langevin：

$$
x\leftarrow x+\epsilon_i s_\theta(x,t_{i-1})
+\sqrt{2\epsilon_i}\,z.
$$

若 score 精确、连续过程/合适 kernel 运行足够久，$p_{t_{i-1}}$ 是其不变分布。实践只运行 $M_i$ 步，因此 corrector 是有限 MCMC relaxation；它不能看到“真实 predictor error vector”，也不保证完全到 equilibrium。

## 四、为什么二者互补而不冗余

- 只有 corrector：冻结在一个 noise level，不能把 $p_T$ 变成 $p_0$；
- 只有 predictor：可以沿路径推进，但有限网格误差与 score error 累积；
- PC：predictor 做 transport，corrector 在局部 noise level 重新平衡。

这类似“先跨温度搬运，再在当前温度搅拌”，但搅拌次数有限。

## 五、一个明确伪代码

```text
x ~ p_T                      # 已知易采样先验
for i = N, ..., 1:
    x = predictor(x, t_i -> t_{i-1}, score=s_theta)
    repeat M_i times:
        z ~ N(0, I)
        x = x + eps_i*s_theta(x,t_{i-1}) + sqrt(2*eps_i)*z
return optional_denoise(x)
```

复现实验必须把 predictor 每步 score calls、$M_i$、corrector 步长、最后 denoise 一起计入 NFE；不能只报时间网格长度。

## 六、SNR 自适应步长的口径

一些实现用当前 score norm 与 noise norm 调整 $\epsilon_i$，试图维持目标 signal-to-noise ratio：

$$
\frac{\|\epsilon_i s\|}{\|\sqrt{2\epsilon_i}z\|}
\approx r.
$$

解得 $\epsilon_i$ 与 $r^2\|z\|^2/\|s\|^2$ 成比例（常数依具体约定）。这是 batch-dependent heuristic；score norm 很小或估计不准时需 clipping。它不是 MALA acceptance，也不恢复 finite-step exactness。

## 七、误差与预算矩阵

| 调整项 | 主要影响 | 代价/风险 |
|---|---|---|
| 更多 predictor steps | time discretization | NFE 上升、误差仍受 score 限制 |
| 更高阶 predictor | 局部截断误差 | 每步多次 score、随机高阶复杂 |
| 更多 corrector steps | local mixing | NFE 上升、可能过度随机化 |
| 更大 corrector step | 移动更快 | ULA bias/instability 增大 |
| MALA corrector | invariant-law 校正 | 接受率、两端 score/energy 与分支成本 |
| 最后 denoise | 残余 smoothing | 改变输出分布与 coverage |

## 八、与 Annealed Langevin 的关系

NCSN 的 annealed Langevin 可看成离散 noise ladder 上主要由 corrector 组成的早期方案；SDE PC 框架加入明确的 reverse dynamics predictor。历史连续性不等于算法逐步相同，尤其 noise schedule、drift、时间参数与步长缩放不同。

## 九、图：搬运与局部重平衡

先看图回答：如果 predictor 已将样本放到当前 marginal 的高密度区域，corrector 为什么仍可能有用？如果 predictor 把所有样本放错到同一模式，少量 corrector 又为何未必救得回来？

![[00-知识库管理/_assets/figures/generative-models/fig-score-predictor-corrector-ledger-v1.svg|900]]

> [!figure] 图 50.4-07　Predictor 的跨时间推进与 Corrector 的固定层 MCMC
> 左侧沿时间网格移动 marginal；中间放大一个时间层，区分 predictor landing error 与 corrector relaxation；右侧给 NFE/误差账。来源：依据 Song et al. 2021 PC 框架独立重绘。

**怎样读图**：横向箭头改变 noise time，环形箭头冻结时间作 Markov moves。Corrector 的目标是当前 learned marginal，不是直接访问未知真样本。

**图没有证明什么**：图不证明有限 corrector steps 已混合，不证明 PC 必优于同 NFE 的高阶 solver，也不证明 learned score 是可积的 exact vector field。

## 十、本节回顾

- predictor 近似 reverse-time evolution；corrector 近似固定层 MCMC；
- 二者误差来源不同，不能笼统叫“去噪两次”；
- finite corrector 不保证 equilibrium；
- SNR 步长是实现 heuristic，不是 MH 校正；
- 公平比较必须使用总 score evaluations、wall time 与相同输出处理。

## 十一、练习与独立详解

- [[习题 - Predictor–Corrector 与 Score-based 生成程序]]
- [[解答 - Predictor–Corrector 与 Score-based 生成程序]]

