---
type: experiment
status: draft
area: [math/probability, math/stochastic-processes, math/sde, math/numerical-analysis, ai/neural-differential-equations]
topic: "Itô和、SDE强弱误差与离散梯度"
prerequisites: ["[[Itô 引理与随机微分方程]]", "[[随机过程、Brownian 运动与二次变差]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
related: ["[[习题 - Itô 引理与随机微分方程]]", "[[推导与实验 MOC]]", "[[Fokker-Planck 方程与概率流 ODE]]"]
code: "[[00-知识库管理/_labs/code/ito_sde_numerics_gradient_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/dynamics/plot-ito-sde-numerics-gradient-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - Itô 和、SDE 强弱误差与离散梯度审计

> [!abstract] 实验问题
> 同一个随机微分方程至少有三类不能互相替代的验收：随机积分的取样约定是否留下正确 quadratic-variation correction；finite-step sampler 对同一 Brownian path 的 strong error 与对期望的 weak error是否按各自阶收敛；训练程序得到的是离散目标 $J_h$ 的梯度还是连续目标 $J$ 的梯度。本实验用一个 standard-library 脚本把三道门分开。

先看图判断：随机积分取样约定、strong/weak error 和离散梯度各自绑定的是路径、分布还是目标函数？

![[00-知识库管理/_assets/plots/dynamics/plot-ito-sde-numerics-gradient-v2.svg|880]]

> [!figure] 实验图｜Itô 修正、SDE 强弱阶与离散梯度
> A 比较左端点 Itô 和与 $1/2$ 二次变差修正；B 在相同 nested Brownian paths 上报告 EM strong endpoint error 与 weak mean bias；C 分开 pathwise gradient gap 和离散 tangent 对 finite difference 的一致性。生成脚本：[[plot_stochastic_experiments_v2.py]]，计算合同来自 [[ito_sde_numerics_gradient_audit.py]]；固定 seed，并保留原强弱阶与梯度断言。

**怎样读图。** A 的修正来自 quadratic variation；B 的 strong error 必须同路径耦合，weak error 只比较期望；C 中 finite-difference 吻合只验证同一 $J_h$，而红线才测 $J_h$ 梯度趋近连续目标的速度。

**适用边界（图没有证明什么）。** 只使用 GBM、Euler–Maruyama 和 terminal mean loss；有限差分不证明一般 pathwise differentiation、弱解存在或训练稳定性，也不覆盖高阶 SDE integrator。

> [!question] 本实验的判别问题
> 为什么 strong、weak 和 gradient consistency 必须使用不同 coupling 与误差对象，不能由一条采样曲线统一代表？

## 一、复现合同

运行：

~~~bash
python3 00-知识库管理/_labs/code/ito_sde_numerics_gradient_audit.py
~~~

环境与固定参数：

- Python 3 standard library；
- seed：$20260819$；
- $T=1$；
- paths：6000；
- finest grid：$N_{\max}=512$；
- resolutions：$N=8,16,32,64,128,256,512$；
- 所有 coarse increments 由同一 finest Brownian increments 分块求和；
- GBM 参数：$X_0=1,\mu=0.35,\sigma=0.8$；
- terminal loss target：$y=1.4$；
- centered finite-difference step：$10^{-5}$；
- 无 NumPy/SciPy/PyTorch 依赖。

Canonical SVG SHA-256：

~~~text
67165c8a06da0210d5de7c64ccd385794c62aafba23c3b2c89bfffde29bda5ee
~~~

脚本会在 Itô order、EM strong/weak order、gradient-gap order、Stratonovich telescope identity、Itô/Stratonovich correction 或 discrete-tangent/FD agreement 越界时非零退出。

## 二、共同 Brownian coupling

先采 finest increments：

$$
\delta W_k
=\sqrt{1/512}\,Z_k,
\qquad
Z_k\overset{iid}{\sim}\mathcal N(0,1).
$$

对 $N<512$，每个 coarse increment 是相邻 block 的和：

$$
\Delta W_j^{(N)}
=
\sum_{k\in\mathcal B_j}\delta W_k.
$$

因此：

1. 每个 resolution 的 increment law 精确为 $\mathcal N(0,1/N)$；
2. 同一 path 在所有 resolutions 有共同 endpoint $W_T$；
3. strong difference 只包含 discretization difference；
4. finite difference 的正负参数扰动也复用同一 noise。

> [!warning] 固定 seed 不等于 coupling
> 若不同 grid 的循环消耗不同数量的随机数，即使 seed 一样也会得到不同 path。显式 nested aggregation 是实验合同的一部分。

## 三、轨道 A：Itô 左端点与 Stratonovich 对称和

### 3.1 Algebraic identities

对每条 path 和每个 partition：

$$
L_N
=\sum_iW_{t_i}\Delta_iW
=\frac12\left(W_T^2-Q_N\right),
$$

$$
S_N
=\sum_i\frac{W_{t_i}+W_{t_{i+1}}}{2}\Delta_iW
=\frac12W_T^2,
$$

其中

$$
Q_N=\sum_i(\Delta_iW)^2.
$$

Itô target 为

$$
I_T=\frac12(W_T^2-T),
$$

所以

$$
L_N-I_T=\frac12(T-Q_N).
$$

误差完全由 realized quadratic variation 控制，理论 RMSE 为 $O(N^{-1/2})$。

### 3.2 结果

| $N$ | Itô left-sum RMSE | mean$(S_N-L_N)$ |
|---:|---:|---:|
| 8 | $2.48505316\times10^{-1}$ | 0.49691293 |
| 16 | $1.77905113\times10^{-1}$ | 0.50133277 |
| 32 | $1.26577563\times10^{-1}$ | 0.50010481 |
| 64 | $8.88082531\times10^{-2}$ | 0.49959160 |
| 128 | $6.27760364\times10^{-2}$ | 0.50047919 |
| 256 | $4.43960575\times10^{-2}$ | 0.49906424 |
| 512 | $3.06043698\times10^{-2}$ | 0.49931847 |

Log–log observed order：

$$
0.50290522.
$$

梯形和与 $W_T^2/2$ 的最大 floating-point RMSE 为0，因为脚本直接使用同一 algebraic identity。实验说明的不是“Stratonovich 更准确”，而是两种 sums 目标不同。

## 四、轨道 B：GBM 的 EM strong/weak error

### 4.1 Exact 与 discrete process

Itô GBM：

$$
dX_t=\mu X_tdt+\sigma X_tdW_t.
$$

Exact terminal：

$$
X_T
=
X_0\exp\left[
(\mu-\sigma^2/2)T+\sigma W_T
\right].
$$

EM：

$$
X_{n+1}
=
X_n(1+\mu h+\sigma\Delta W_n).
$$

Strong endpoint RMSE：

$$
e_{\rm strong}(h)
=
\left(
\frac1M\sum_{r=1}^M
|X_{T,r}^{h}-X_{T,r}^{\rm exact}|^2
\right)^{1/2}.
$$

Weak mean bias 使用解析式，避免 Monte Carlo noise：

$$
e_{\rm weak}(h)
=
\left|
X_0(1+\mu h)^{T/h}
-
X_0e^{\mu T}
\right|.
$$

### 4.2 结果

| $N$ | strong endpoint RMSE | weak mean bias |
|---:|---:|---:|
| 8 | $3.17894560\times10^{-1}$ | $1.05187163\times10^{-2}$ |
| 16 | $2.37223717\times10^{-1}$ | $5.34433437\times10^{-3}$ |
| 32 | $1.68896610\times10^{-1}$ | $2.69397914\times10^{-3}$ |
| 64 | $1.13502740\times10^{-1}$ | $1.35251588\times10^{-3}$ |
| 128 | $7.91106978\times10^{-2}$ | $6.77648833\times10^{-4}$ |
| 256 | $5.62167919\times10^{-2}$ | $3.39173314\times10^{-4}$ |
| 512 | $3.95025654\times10^{-2}$ | $1.69674029\times10^{-4}$ |

Observed orders：

$$
p_{\rm strong}=0.50979058,
$$

$$
p_{\rm weak,mean}=0.99318241.
$$

这与 standard smooth/Lipschitz theory 的 EM strong $1/2$、weak1相符。

### 4.3 不能混合的结论

- weak mean order1不表示 pathwise order1；
- strong terminal RMSE 不自动控制 hitting event；
- analytic mean bias 不包含 Monte Carlo standard error；
- 此实验只覆盖 GBM 的一个 parameter regime；
- finite-step EM 可变负，exact GBM 保持正值；
- observed slope 不是对任意 non-Lipschitz/neural SDE 的证明。

## 五、轨道 C：离散 sensitivity 与连续 gap

### 5.1 Discrete tangent

对 $\sigma$ 求导。记

$$
S_n=\frac{\partial X_n}{\partial\sigma}.
$$

EM factor 为

$$
F_n=1+\mu h+\sigma\Delta W_n.
$$

递推：

$$
X_{n+1}=X_nF_n,
$$

$$
S_{n+1}=S_nF_n+X_n\Delta W_n,
\qquad S_0=0.
$$

Terminal loss：

$$
J_h(\sigma)
=
\mathbb E\left[
\frac12(X_N-y)^2
\right].
$$

Discrete pathwise gradient sample：

$$
G_h=(X_N-y)S_N.
$$

### 5.2 同一 $J_h$ 的 finite difference

使用相同 Brownian increments：

$$
g_{\rm FD}
=
\frac{
\widehat J_h(\sigma+\varepsilon)
-
\widehat J_h(\sigma-\varepsilon)
}{2\varepsilon}.
$$

各 resolution 的 tangent-vs-FD absolute error：

| $N$ | absolute error |
|---:|---:|
| 8 | $1.60929048\times10^{-10}$ |
| 16 | $3.69104747\times10^{-10}$ |
| 32 | $5.50336221\times10^{-10}$ |
| 64 | $4.14141166\times10^{-10}$ |
| 128 | $4.12470058\times10^{-10}$ |
| 256 | $4.61821692\times10^{-10}$ |
| 512 | $4.92026864\times10^{-10}$ |

最大值：

$$
5.50336221\times10^{-10}.
$$

这说明 sensitivity recursion 与 centered finite difference 对同一 floating-point discrete objective 一致。

### 5.3 Continuous-reference gap

Exact GBM sensitivity：

$$
S_T^{\rm exact}
=
X_T^{\rm exact}(W_T-\sigma T).
$$

Exact gradient integrand：

$$
G=(X_T^{\rm exact}-y)S_T^{\rm exact}.
$$

实验计算 pathwise RMSE：

$$
e_G(h)
=
\left(
\mathbb E|G_h-G|^2
\right)^{1/2}.
$$

结果：

| $N$ | gradient-integrand RMSE |
|---:|---:|
| 8 | $1.40881594\times10^{1}$ |
| 16 | $1.16525943\times10^{1}$ |
| 32 | $8.51620942$ |
| 64 | $5.36209684$ |
| 128 | $2.53363819$ |
| 256 | $1.72422460$ |
| 512 | $1.51916574$ |

Observed order：

$$
0.60363071.
$$

GBM 的 lognormal tail 使 gradient-integrand RMSE 的 finite-sample fluctuation明显，因此该 slope 不应解释为新的 universal theorem。重要的是：FD error 已在 $10^{-10}$ 量级时，continuous-reference gap 仍然可见。

## 六、结果总表

~~~text
Ito left-sum order      = 0.50290522
EM strong order         = 0.50979058
EM weak mean order      = 0.99318241
gradient gap order      = 0.60363071
max trapezoid identity  = 0.00000000e+00
max tangent-vs-FD error = 5.50336221e-10
svg_sha256              = 67165c8a06da0210d5de7c64ccd385794c62aafba23c3b2c89bfffde29bda5ee
~~~

## 七、改参复现实验

学习者应至少完成两项：

1. 把 $\sigma$ 从0.8改为0.3，比较 strong 与 gradient-gap variance；
2. 把 resolutions 扩到 $N=1024$，增加 paths 并检查 slope 稳定性；
3. 增加 Milstein，验证 GBM strong order 接近1；
4. 增加 $\varphi(x)=x^2$ 的 analytic weak bias；
5. 记录 EM negative-step probability；
6. 把 FD step 从 $10^{-2}$ 扫到 $10^{-8}$，观察 truncation/cancellation U 形曲线；
7. 故意对每个 resolution 独立重抽 path，观察“strong error”不收敛；
8. 加入 OU exact transition，比较长期 stationary variance bias。

## 八、验收边界

本实验提供：

- fixed implementation 的 deterministic reproduction；
- Itô/Stratonovich correction 的计算证据；
- GBM 上 EM strong/weak order 的受控例子；
- discrete tangent 与 FD 的同目标验收；
- discrete/continuous gradient gap 的可见证据。

本实验不提供：

- Itô integral 或 SDE theorem 的证明替代；
- 任意 coefficient 下的 convergence guarantee；
- adaptive solver/Brownian tree 的实现认证；
- multidimensional Lévy area 处理；
- hitting-time error；
- reverse-time diffusion 或 score sampler 正确性；
- 学习者独立复现与 mastered 状态。

## 九、复现记录

> [!check] 2026-08-19 canonical run
> 两次独立运行 stdout 与 SVG hash 一致；全部脚本 assertions 通过。机制图与实验图均已用 Sharp 渲染为1200×430 PNG并完成文字、裁切、曲线与图例视觉终检；源 SVG 保留为 Obsidian 可嵌入资产。
