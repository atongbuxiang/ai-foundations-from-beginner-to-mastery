---
type: experiment
status: draft
area: [math/probability, math/stochastic-processes, math/numerical-analysis, ai/generative-modeling]
topic: "Brownian增量、二次变差与时间耦合"
prerequisites: ["[[随机过程、Brownian 运动与二次变差]]", "[[联合分布、边缘分布与独立性]]", "[[协方差、相关性与条件期望]]"]
related: ["[[习题 - 随机过程、Brownian 运动与二次变差]]", "[[推导与实验 MOC]]", "[[Itô 引理与随机微分方程]]"]
code: "[[00-知识库管理/_labs/code/brownian_quadratic_variation_coupling_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/dynamics/plot-brownian-quadratic-variation-coupling-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - Brownian 增量、路径粗糙性与时间耦合审计

> [!abstract] 实验问题
> Brownian motion 至少需要通过三种互不替代的校准：跨时间 joint Gaussian law 是否正确；nested refinement 下平方增量是否收敛而绝对增量是否增长；只有 fixed-time marginals 相同的不同 couplings 是否会产生完全不同的局部路径尺度。本实验把三者分开，防止用一组正确 histogram 冒充正确随机过程。

先看图回答：正确的 fixed-time Gaussian marginals、跨时间 covariance、quadratic variation 与 increment scaling 哪些可以互推，哪些不能？

![[00-知识库管理/_assets/plots/dynamics/plot-brownian-quadratic-variation-coupling-v2.svg|880]]

> [!figure] 实验图｜Brownian 联合律、路径粗糙性与时间耦合
> A 核对 nested Brownian path 的均值、方差与跨时刻协方差；B 展示平方变差趋于 1 而绝对变差按 $N^{1/2}$ 增长；C 构造相同 one-time marginals 但增量 MSE 阶为 1、2、0 的三种 coupling。生成脚本：[[brownian_quadratic_variation_coupling_audit.py]]；固定 seed 和 nested increments，并对联合矩与理论斜率设断言。

**怎样读图。** A 不能只验终点 histogram；B 将 quadratic variation 与 total variation 分开；C 的三条曲线在每个固定时刻分布相同，却因跨时间联合律不同产生不同局部尺度。

**适用边界（图没有证明什么）。** 有限路径 Monte Carlo 只校准指定 seed、样本数和分辨率；图不证明 Brownian 定义、几乎处处路径性质或任意 stochastic process 的 coupling theorem。

> [!question] 本实验的判别问题
> 为什么生成模型在每个时间点匹配 histogram，仍不足以说明它匹配了真实随机过程的 path law？

## 一、复现合同

运行：

~~~bash
python3 00-知识库管理/_labs/code/brownian_quadratic_variation_coupling_audit.py
~~~

环境：

- Python 3 standard library；
- seed：$20260819$；
- $T=1$；
- 最细网格 $N_{\max}=4096$；
- 768 条 Brownian paths；
- 所有粗网格由同一最细 increments 求和得到；
- coupling-order实验每个 $h$ 使用40000个样本；
- 无 NumPy/SciPy/PyTorch 依赖。

当前 canonical SVG SHA-256：

~~~text
990cff3391547f79127820059b94c667ba5ee9b6785c6706ab5744fd0677b8ae
~~~

脚本在 marginal variance、covariance kernel、不重叠increment covariance、Gaussian fourth moment、quadratic-variation mean/RMSE、total-variation scaling和三种coupling orders任一越界时非零退出。

## 二、轨道 A：Brownian joint-law audit

### 2.1 构造

最细网格 increments 独立采样：

$$
\Delta W_k
=\sqrt{\Delta t}\,Z_k,
\qquad
Z_k\overset{iid}\sim\mathcal N(0,1),
\qquad
\Delta t=1/4096.
$$

记录

$$
t=(0.25,0.50,0.75,1.00)
$$

的 levels，并检查：

$$
\mathbb E[W_t]=0,
\qquad
\operatorname{Var}(W_t)=t,
$$

$$
\operatorname{Cov}(W_s,W_t)=\min(s,t),
$$

以及

$$
\operatorname{Cov}(W_{0.25},W_{0.5}-W_{0.25})=0.
$$

### 2.2 结果

Empirical means：

~~~text
+0.00209445, +0.03343261, +0.05735991, +0.09816779
~~~

Empirical variances：

~~~text
0.23479445, 0.48420430, 0.71424746, 0.94615396
~~~

进一步得到：

~~~text
covariance kernel max error = 5.38460362e-02
disjoint increment cov      = -3.81326751e-03
E[W_1^4]                    = 2.71791649
~~~

理论 fourth moment 为3。768条path下这些偏差属于可见的 Monte Carlo波动；网格点 Brownian FDD本身由Gaussian increment construction精确给出，不存在 time-discretization bias。

> [!important] 解释
> 单看四个variance仍不足以验收process；covariance matrix和不重叠increments才检查跨时间coupling。实验不是用“均值接近0”证明Brownian，而是把definition-level identities组合起来。

## 三、轨道 B：nested quadratic/total variation

### 3.1 为什么必须 nested

对每条最细 path，把相邻fine increments求和形成

$$
N=32,64,\ldots,4096
$$

的粗increments。这样各分辨率共享同一 underlying Brownian path；变化来自partition，而不是重新抽样。

计算

$$
Q_N=\sum_{i=1}^N(\Delta_iW)^2,
$$

$$
V_N=\sum_{i=1}^N|\Delta_iW|.
$$

理论上

$$
\mathbb E[Q_N]=1,
\qquad
\operatorname{RMSE}(Q_N)=\sqrt{2/N},
$$

$$
\mathbb E[V_N]=\sqrt{2N/\pi}.
$$

### 3.2 结果

| $N$ | mean $Q_N$ | RMSE$(Q_N-1)$ | mean $V_N$ |
|---:|---:|---:|---:|
| 32 | 0.98254629 | 0.23871222 | 4.47039182 |
| 64 | 0.99329824 | 0.17131159 | 6.35726769 |
| 128 | 1.00270996 | 0.12205359 | 9.04320576 |
| 256 | 1.00022982 | 0.09012020 | 12.76753325 |
| 512 | 0.99904473 | 0.06433979 | 18.05235662 |
| 1024 | 1.00097287 | 0.04398688 | 25.53847864 |
| 2048 | 0.99808715 | 0.03151579 | 36.08067592 |
| 4096 | 0.99857398 | 0.02165528 | 51.03651103 |

Log-log slopes：

~~~text
total variation mean slope = +0.50128738
QV RMSE slope             = -0.49229759
~~~

理论分别是 $+1/2$ 与 $-1/2$。这同时复现：

1. quadratic variation收敛到有限非零的1；
2. 单路径realized QV仍有 $N^{-1/2}$ 随机误差；
3. partition total variation按 $\sqrt N$ 发散。

### 3.3 不能从图中声称什么

- 不能由有限8档partition证明所有path almost surely theorem；
- 不能把 $Q_N$ 接近1理解为每步 $(\Delta W)^2=\Delta t$；
- 不能由total variation增长的有限范围估计唯一roughness exponent；
- 不能把同一path refinement的correlated误差当作independent regression samples；
- 不能把linear plotting interpolation当成网格间Brownian bridge。

## 四、轨道 C：同 marginals，不同时间 coupling

### 4.1 三个过程

固定 $t_0=0.5$，比较：

$$
B_t=W_t,
$$

$$
S_t=\sqrt t\,Z,
$$

$$
I_t=\sqrt t\,Z_t,
$$

其中 $S$ 的整条path共用一个 $Z$，$I$ 在两个时刻使用独立Gaussian。

三者对每个固定 $t$ 都有

$$
\mathcal N(0,t)
$$

marginal，但increment MSE分别是

$$
\mathbb E|\Delta B|^2=h,
$$

$$
\mathbb E|\Delta S|^2
=(\sqrt{t_0+h}-\sqrt{t_0})^2
\sim\frac{h^2}{4t_0},
$$

$$
\mathbb E|\Delta I|^2=2t_0+h.
$$

### 4.2 结果

对

$$
h=2^{-3},\ldots,2^{-8}
$$

拟合 log-log order：

~~~text
Brownian / shared / independent
0.99676190 / 1.97365536 / 0.03178409
~~~

理论是

~~~text
1 / 2 / 0
~~~

最小 $h=1/256$ 的increment MSE：

~~~text
Brownian   = 3.93982423e-03
shared     = 7.52255318e-06
independent= 9.95256647e-01
~~~

因此：

- Brownian增量按 $\sqrt h$；
- shared-noise path在 $t_0>0$ 附近像普通smooth random curve；
- independent-time samples在相邻时刻仍相差 $O(1)$，不具连续性。

### 4.3 AI 解释

扩散训练式

$$
X_t=\alpha_tX_0+\sigma_t\varepsilon
$$

只作为fixed-time reparameterization时完全合法。但若把它直接解释成multi-time process：

- 每个 $t$ 重采独立 $\varepsilon_t$，可能得到不连续coupling；
- 所有 $t$ 共用同一 $\varepsilon$，可能得到过度相关、zero-QV coupling；
- 声称forward SDE必须另外给transition/local covariance。

这不是实现细节，而是数学对象不同。

## 五、失败注入

### 5.1 忘记 $\sqrt{\Delta t}$

若使用

$$
\Delta W_k=Z_k,
$$

则 $N$ 步终点方差为 $N$，随refinement发散。

若错误使用

$$
\Delta W_k=\Delta t\,Z_k,
$$

终点方差为 $N\Delta t^2=T\Delta t\to0$，diffusion消失。

### 5.2 粗细网格独立抽样

独立粗/细 Brownian endpoints之差方差为 $2T$，不会随step缩小；它会把path mismatch冒充solver error。

### 5.3 多维流复用同一stream

若两个声称独立的components使用同一increments，则cross variation趋近 $T$ 而非0。只查每个component marginal variance无法发现。

## 六、复现实验的声明边界

本实验支持：

- 标准库increment generator在指定网格与seed下通过了Brownian moment/covariance检查；
- nested realized QV、QV RMSE和total variation符合解析scaling；
- 三个相同marginal couplings具有不同increment orders。

本实验不证明：

- 任意PRNG、任意precision或任意device scheduling都正确；
- 有限样本验证可替代Brownian existence/path theorem；
- 任意SDE solver具有指定strong/weak order；
- 任意diffusion model学到了true score；
- reverse SDE与probability-flow ODE已满足正式条件；
- endpoint sample quality可证明path law正确。

## 七、学习者复现门

在不看结果表时完成：

1. 先预测 $Q_N$ mean、RMSE和 $V_N$ slope；
2. 把所有coarse resolutions改成独立seed，观察pathwise difference；
3. 使用非均匀deterministic partition；
4. 将两个Brownian components的stream从独立改成复用，测cross variation；
5. 把noise scale从 $\sqrt{\Delta t}$ 改为1和 $\Delta t$；
6. 将 $t_0$ 改为0.1和2，解释independent/shared曲线；
7. 增减path count并给Monte Carlo interval；
8. 记录至少一个失败断言与修复原因。

| 日期 | 环境 | 结果 | 状态 |
|---|---|---|---|
| 2026-08-19 | Python 3 standard library | 全部断言通过，canonical SVG hash固定 | composed / not-attempted by learner |

只有完成独立预测、改参、失败注入与解释后，实验状态才可升级为 reproduced。
