---
type: experiment
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/numerical-analysis, ai/generative-modeling]
topic: "反向时间、score恒等式与扩散采样误差"
prerequisites: ["[[时间反演、score 与扩散生成动力学]]", "[[Fokker-Planck 方程与概率流 ODE]]"]
related: ["[[习题 - 时间反演、score 与扩散生成动力学]]", "[[推导与实验 MOC]]"]
code: "[[00-知识库管理/_labs/code/reverse_time_score_diffusion_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/dynamics/plot-reverse-time-score-diffusion-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - 反向时间、score恒等式与扩散采样误差审计

> [!abstract] 实验问题
> 反向扩散至少有三道独立数学关：backward conditional 的小时间均值是否收敛到正确 reverse drift；可采样的 conditional denoising target 是否真的回归 marginal score；减小步长究竟消除 solver error，还是能错误地“修复”score、terminal prior 与 drift coefficient。实验用一维闭式模型逐项隔离。

先看图判断：reverse drift 极限、DSM/Tweedie 恒等式、solver convergence 与 score/prior/coefficient 偏差分别需要什么参照？

![[00-知识库管理/_assets/plots/dynamics/plot-reverse-time-score-diffusion-v2.svg|880]]

> [!figure] 实验图｜反向漂移、score 恒等式与扩散误差地板
> A 从 finite-$h$ backward conditional 收敛到含 $D\nabla\log p_t$ 的 reverse drift；B 在 Gaussian mixture 上核对 DSM 与 Tweedie；C 比较 exact-score SDE/PF solver 阶和 score、terminal prior、half-coefficient 三种误差地板。生成脚本：[[reverse_time_score_diffusion_audit.py]]；闭式矩递推、无 Monte Carlo noise，并对全部恒等式和地板设断言。

**怎样读图。** A 说明反向不是简单把 $dt$ 改负号；B 必须同时核对 score 与 posterior denoiser；C 只有蓝/绿曲线随 $h$ 下降，水平地板对应 model/specification error。

**适用边界（图没有证明什么）。** 一维 Gaussian mixture 与闭式 mean/variance sampler 只隔离机制；图不证明 learned score 的泛化、高维 reverse SDE 的稳定性或任意 prior mismatch 的量级。

> [!question] 本实验的判别问题
> 如何通过 refinement test 区分 solver error 与不会随步长消失的 score、prior 和反向漂移系数错误？

## 一、复现合同

运行：

~~~bash
python3 00-知识库管理/_labs/code/reverse_time_score_diffusion_audit.py
~~~

环境：

- Python 3 standard library；
- 无 NumPy/SciPy/PyTorch；
- 无外部数据；
- 所有 reference 都是 Gaussian/mixture 闭式；
- sampler 轨道直接递推 mean/variance，避免 Monte Carlo noise；
- 图由同一脚本确定性生成。

Canonical SVG SHA-256：

~~~text
1ad7447f60e6d035f4b149b1231053ead4ec80d70b418ab3db8e376ab3e9b0a7
~~~

脚本在 reverse-drift order、DSM/Tweedie identity、reverse SDE/PF solver order、fine-grid error 或三类 bias floor 任一越界时非零退出。

## 二、轨道 A：有限时间 backward conditional 收敛到 reverse drift

### 2.1 Forward VP model

使用 constant-$\beta$ VP：

$$
dX_t=-\frac\beta2X_tdt+\sqrt\beta dW_t,
$$

参数：

$$
\beta=2,
\quad
X_0\sim\mathcal N(1.2,0.3).
$$

其 moments 为

$$
m_t=e^{-\beta t/2}m_0,
$$

$$
v_t=1+(v_0-1)e^{-\beta t}.
$$

score：

$$
s_t(x)=-\frac{x-m_t}{v_t}.
$$

forward-$s$ reverse drift：

$$
b_{\rm rev}(t,x)
=\frac\beta2x+\beta s_t(x).
$$

### 2.2 Exact finite-$h$ backward conditional

在物理时刻 $t=1.2$，联合 Gaussian 给

$$
\mathbb E[X_{t-h}\mid X_t=x]
=m_{t-h}
+\frac{e^{-\beta h/2}v_{t-h}}{v_t}(x-m_t).
$$

定义 finite-$h$ drift：

$$
b_h(x)
=\frac{
\mathbb E[X_{t-h}\mid X_t=x]-x
}{h}.
$$

在21个 $x\in[-2,3]$ 网格点上计算

$$
\operatorname{RMSE}(b_h-b_{\rm rev}).
$$

### 2.3 结果

| $h$ | reverse-drift RMSE |
|---:|---:|
| 0.200000 | $1.4956149161\times10^{-1}$ |
| 0.100000 | $7.7173867622\times10^{-2}$ |
| 0.050000 | $3.9212430473\times10^{-2}$ |
| 0.025000 | $1.9766063301\times10^{-2}$ |
| 0.012500 | $9.9234327131\times10^{-3}$ |

Observed order：

$$
0.97925982.
$$

这验证了 reverse drift 是 backward conditional mean 的局部极限，而不是任意添加的修正方向。

> [!warning] 局部极限不等于完整定理
> 本轨道使用一维 nondegenerate Gaussian Markov diffusion。它不证明任意 state-dependent、degenerate 或有边界系统的 path-law reversal。

## 三、轨道 B：DSM 与 Tweedie 在双峰分布上逐点一致

### 3.1 Data 与 corruption

$$
X_0
\sim\frac12\mathcal N(-2,0.16)
+\frac12\mathcal N(2,0.16),
$$

$$
X_t=0.75X_0+0.8\varepsilon.
$$

每个 noisy component 的方差：

$$
V=0.75^2\times0.16+0.8^2=0.73.
$$

对 component $k\in\{-1,+1\}$，

$$
p_t(x\mid k)=\mathcal N(1.5k,0.73).
$$

### 3.2 两条独立计算路径

路径一：直接对 mixture density 求 score：

$$
s_t(x)
=\sum_kr_k(x)
\left[-\frac{x-1.5k}{0.73}\right].
$$

路径二：先做 component Gaussian conditioning，得到

$$
\mathbb E[X_0\mid X_t=x],
$$

再计算 conditional target average：

$$
\mathbb E\left[
-\frac{x-0.75X_0}{0.8^2}
\mid X_t=x
\right].
$$

同时以

$$
\frac{x+0.8^2s_t(x)}{0.75}
$$

计算 Tweedie posterior mean。

### 3.3 结果

在181个 $x\in[-4.5,4.5]$ 网格点上：

~~~text
DSM identity max error     = 1.7763568394e-15
Tweedie identity max error = 8.8817841970e-16
~~~

误差处于 binary64 roundoff 水平。

这条实验同时说明：

1. 单个 conditional target $-(x_t-\alpha x_0)/\sigma^2$ 不等于 marginal score；
2. 对 $X_0\mid X_t=x$ 取条件平均后才等于 marginal score；
3. score 与 posterior-mean denoiser 是可换算对象；
4. 对称 mixture 的 $x=0$ 处，posterior mean 可以为0，即使 clean modes 位于两侧。

## 四、轨道 C：solver convergence 与三类模型误差地板

### 4.1 Reverse SDE 与 PF ODE

仍用轨道 A 的 VP Gaussian，终止时间

$$
T=2.
$$

精确 terminal law 为

$$
p_T=\mathcal N(m_T,v_T).
$$

reverse SDE：

$$
dY_s
=\left[
\frac\beta2Y_s+\beta s_t(Y_s)
\right]ds
+\sqrt\beta d\bar W_s.
$$

PF ODE：

$$
\frac{dY_s}{ds}
=\frac\beta2Y_s+\frac\beta2s_t(Y_s).
$$

因为二者都是 affine Gaussian dynamics，可直接递推数值 scheme 的 mean/variance，不需要抽有限条路径。

误差指标：

$$
E_h
=\sqrt{(\widehat m_0-m_0)^2+(\widehat v_0-v_0)^2}.
$$

### 4.2 Refinement 结果

| $N$ | reverse SDE mean | reverse SDE var | $E_h^{\rm SDE}$ | PF mean | PF var | $E_h^{\rm PF}$ |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 1.177981811 | 0.440652401 | $1.423653703\times10^{-1}$ | 1.153052673 | 0.369756861 | $8.408371516\times10^{-2}$ |
| 32 | 1.189733281 | 0.364354005 | $6.516781015\times10^{-2}$ | 1.177447165 | 0.334082041 | $4.086827499\times10^{-2}$ |
| 64 | 1.195044381 | 0.330521459 | $3.092115132\times10^{-2}$ | 1.188971230 | 0.316773261 | $2.007426368\times10^{-2}$ |
| 128 | 1.197565237 | 0.314833589 | $1.503208037\times10^{-2}$ | 1.194549094 | 0.308311022 | $9.939088077\times10^{-3}$ |
| 256 | 1.198793185 | 0.307309087 | $7.408047122\times10^{-3}$ | 1.197290565 | 0.304135562 | $4.944078421\times10^{-3}$ |
| 512 | 1.199399208 | 0.303627555 | $3.676969603\times10^{-3}$ | 1.198649302 | 0.302062667 | $2.465558435\times10^{-3}$ |

Observed orders：

$$
p_{\rm reverse\ SDE}=1.05217767,
$$

$$
p_{\rm PF}=1.01757101.
$$

两条 exact-score 一阶方法均按约一阶收敛。

### 4.3 三个不会被步长修复的错误

固定

$$
N=4096
$$

并分别改变一个对象：

| 设置 | terminal moment error |
|---|---:|
| exact score、exact $p_T$ | $4.566604532\times10^{-4}$ |
| score 乘 $1.10$ | $4.948863821\times10^{-2}$ |
| 从 $\mathcal N(0,1)$ 而非 exact $p_T$ 启动 | $6.767308137\times10^{-3}$ |
| noisy reverse SDE 错用半个 score | $1.558975879$ |

解释：

- exact-score fine-grid error 是 solver residue；
- score $+10\%$ 是 learned continuous drift bias；
- terminal prior mismatch 是 initial-law bias；
- half-score noisy SDE 是 generator coefficient error。

后三者都不会仅靠 $h\to0$ 自动消失。

## 五、实验结论

~~~text
reverse drift order             = 0.97925982
DSM identity max error          = 1.7763568394e-15
Tweedie identity max error      = 8.8817841970e-16
reverse SDE Euler moment order  = 1.05217767
PF Euler moment order           = 1.01757101
fine exact-score error          = 4.566604532e-04
score +10% bias floor           = 4.948863821e-02
terminal-prior mismatch floor   = 6.767308137e-03
half-score noisy-SDE floor      = 1.558975879e+00
svg_sha256                      = 1ad7447f60e6d035f4b149b1231053ead4ec80d70b418ab3db8e376ab3e9b0a7
~~~

由此分别验收：

1. backward conditional → reverse drift；
2. conditional denoising target → marginal score；
3. score → Tweedie posterior mean；
4. exact-score solver refinement；
5. solver、score、terminal 与 coefficient error 分账。

## 六、改参复现任务

至少完成两项：

1. 将 $T$ 从2改成0.5、1、3，测 terminal prior mismatch；
2. 将 $v_0$ 改成1，解释哪些 terminal/moment误差消失；
3. 把 score perturbation 设为只在 $t<0.1$ 出现；
4. 将 score scale 扫描为 $0.8$ 到 $1.2$；
5. 在 reverse SDE 中比较 full-score、half-score 与 zero-score；
6. 给 mixture 增加不平衡权重，检查 $x=0$ denoiser；
7. 用 Monte Carlo path simulation复核解析 moment recursion；
8. 对 reverse SDE 使用 shared Brownian refinement，测 strong error；
9. 把 PF Euler 改成 Heun，验证二阶区间；
10. 将 constant $\beta$ 改为线性 schedule，并重新推导 $\alpha(t)$。

## 七、解释边界

本实验提供：

- 一维 Gaussian diffusion 的 exact reverse-drift local limit；
- 双峰 Gaussian mixture 的 exact DSM/Tweedie identity；
- 线性 reverse SDE/PF 的 noise-free moment convergence audit；
- 三种非 solver error floor 的受控反例。

本实验不提供：

- 一般 time-reversal theorem；
- state-dependent/degenerate diffusion 的验证；
- neural network approximation guarantee；
- 高维图像 sampler 排名；
- FID、感知质量或 guidance 结论；
- 学习者 mastered 证据。

## 八、复现记录

> [!check] 2026-08-19 canonical run
> 两次独立复跑输出与 SVG SHA-256 完全一致；全部 assertions、两幅 SVG 的 XML 解析和 Sharp PNG 视觉终检均已通过。
