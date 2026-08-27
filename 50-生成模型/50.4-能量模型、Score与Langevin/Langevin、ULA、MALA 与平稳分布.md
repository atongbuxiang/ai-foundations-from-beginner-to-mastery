---
type: concept
status: verified
area: [generative-models, langevin, mcmc, numerical-analysis]
node_id: GEN-30
prerequisites: ["[[Fokker-Planck 方程与概率流 ODE]]", "[[MCMC 与随机模拟诊断]]"]
related: ["[[多噪声尺度、退火去噪与 Score 网络]]", "[[Predictor–Corrector 与 Score-based 生成程序]]"]
sources: ["[[S-2019-Su-6612-生成模型等于能量模型]]", "[[S-1996-Roberts-Tweedie-Langevin]]", "[[S-2019-Du-Mordatch-EBM]]"]
exercises: ["[[习题 - Langevin、ULA、MALA 与平稳分布]]"]
solutions: ["[[解答 - Langevin、ULA、MALA 与平稳分布]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-langevin-continuous-ula-mala-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Langevin、ULA、MALA 与平稳分布

> [!abstract] 本节主问题
> 连续 overdamped Langevin 在适当条件下以目标 density 为不变分布；Euler 离散得到 ULA，通常改变不变分布；MALA 再用 Metropolis–Hastings 接受拒绝恢复精确 invariant law。即便不变分布正确，有限时间、混合、多峰和自相关仍决定样本是否可用。

## 一、统一采用一套尺度约定

设目标

$$
\pi(x)=Z^{-1}e^{-E(x)}.
$$

本节采用

$$
\boxed{dX_t=-\nabla E(X_t)dt+\sqrt2,dW_t}
$$

等价写成 $dX_t=\nabla\log\pi(X_t)dt+\sqrt2dW_t$。有些文献写 $\frac12\nabla\log\pi,dt+dW_t$；那只是时间缩放。离散公式必须与所选约定一致，不能把 $1/2$ 和噪声方差拼错。

## 二、为什么 $\pi$ 是平稳密度

Fokker–Planck 方程为

$$
\partial_tp_t
=\nabla\cdot(p_t\nabla E)+\Delta p_t
=-\nabla\cdot J_t,
$$

其中 probability current

$$
J_t=-p_t\nabla E-\nabla p_t.
$$

代入 $p_t=\pi$，由于 $\nabla\pi=-\pi\nabla E$，得到 $J=0$，故 $\partial_t\pi=0$。这是 zero-current/reversibility 证明。

但“$\pi$ 不随时间变化”只说明 invariant：若 $X_0\sim\pi$，则 $X_t\sim\pi$。从任意初值收敛到 $\pi$ 还需非爆炸、不可约、recurrence、Poincaré/log-Sobolev 或 Lyapunov 等条件；收敛速度在多峰中可能极慢。

## 三、ULA：Euler–Maruyama 不是原过程

步长 $h>0$ 的 unadjusted Langevin algorithm：

$$
\boxed{
X_{k+1}=X_k-h\nabla E(X_k)+\sqrt{2h}\,\xi_k,
\quad\xi_k\sim N(0,I).}
$$

它是一个离散 Markov chain。即便连续 SDE 的 invariant law 是 $\pi$，ULA 的 invariant law 一般是 $\pi_h\ne\pi$。

### 3.1 标准正态反例可完全手算

取 $E(x)=x^2/2$，则

$$
X_{k+1}=(1-h)X_k+\sqrt{2h}\xi_k.
$$

这是 AR(1)。当 $|1-h|<1$，即 $0<h<2$，存在平稳方差 $v_h$：

$$
v_h=(1-h)^2v_h+2h,
$$

所以

$$
\boxed{v_h=\frac1{1-h/2}.}
$$

除 $h\to0$ 外不等于目标方差 1；$h\ge2$ 时失稳。这一个例子已足以反驳“连续过程正确，所以任意有限步离散也正确”。

## 四、MALA：用接受拒绝校正离散偏差

ULA proposal density 是

$$
q_h(y\mid x)
=N(y;x-h\nabla E(x),2hI).
$$

MALA 先提出 $Y\sim q_h(\cdot\mid X_k)$，再以

$$
\alpha(x,y)
=1\wedge
\frac{\pi(y)q_h(x\mid y)}{\pi(x)q_h(y\mid x)}
$$

接受，否则保持 $X_{k+1}=X_k$。由于 $\pi(y)/\pi(x)=e^{-E(y)+E(x)}$，未知 $Z$ 消去。

满足标准 MH 条件时，MALA 对任意固定 $h$ 保持 $\pi$ 不变；但若 $h$ 太大，拒绝率高、chain 几乎不动。exact invariant 不等于 independent samples，也不等于快速 mixing。

## 五、四个性质必须分开

| 性质 | 问题 | 典型证据 |
|---|---|---|
| invariance | 若已在 $\pi$，一步后仍在吗？ | detailed balance/current |
| ergodicity | 从广泛初值是否趋于唯一 $\pi$？ | irreducibility + recurrence 等 |
| mixing rate | 需要多久接近？ | spectral gap/coupling/functional inequality |
| finite-sample quality | 当前预算下误差多大？ | multiple chains、ESS、autocorrelation、ground-truth toy |

只展示能量下降轨迹不能回答任何一项完整问题，因为随机噪声和模式覆盖都被省略。

## 六、Burn-in、thinning 与有效样本量

- burn-in 丢弃初始 transient，但长度不能凭习惯常数决定；
- thinning 通常丢信息，除非存储/下游成本有明确理由；
- autocorrelation time 决定 $n$ 个相关 state 相当于多少独立样本；
- 多链从过度分散初值出发有助于发现 mode trapping，但诊断不构成绝对收敛证明；
- neural EBM 训练中 target 本身随 $\theta_t$ 变化，传统固定目标诊断更难直接解释。

## 七、Replay buffer 与短链训练

[[S-2019-Du-Mordatch-EBM]]采用 replay buffer、随机重启和有限步 Langevin。它们分别改善 warm start、覆盖新区域与计算成本，但模型负样本来自随训练变化的非平稳链。训练能成功是重要实验事实，却不把负相估计变成无偏，也不保证测试时同预算混合。

## 八、图：连续正确、离散有偏、MH 校正

先看图回答：哪一个箭头保证不变分布，哪一个箭头只是一阶数值近似？

![[00-知识库管理/_assets/figures/generative-models/fig-langevin-continuous-ula-mala-v1.svg|900]]

> [!figure] 图 50.4-06　Langevin diffusion、ULA 偏差与 MALA 接受拒绝的层级
> 左侧以 Fokker–Planck zero current 验证连续 invariant law；中间给 Gaussian ULA 的方差偏差；右侧用 proposal ratio 做 MH 校正。来源：依据 Langevin/MH 定义与 Gaussian AR(1) 独立计算。

**怎样读图**：连续曲线的正确性不能跨过“Euler”箭头自动传给 ULA。MALA 的接受门恢复 invariant law，却可能因频繁拒绝降低移动效率。

**图没有证明什么**：图不证明多峰高维 MALA 快速混合，不给 burn-in 长度，也不证明 replay-buffer short-run chains 近似 equilibrium。

## 九、本节回顾

- 连续 Langevin 的 Gibbs invariant law来自 Fokker–Planck/current；
- invariant、ergodic、fast mixing 与 finite-budget accuracy 不同；
- ULA 通常有步长偏差，甚至可能失稳；
- MALA 校正 invariant law，但增加拒绝与计算成本；
- neural EBM 的非平稳短链必须单独审计。

## 十、练习与独立详解

- [[习题 - Langevin、ULA、MALA 与平稳分布]]
- [[解答 - Langevin、ULA、MALA 与平稳分布]]
