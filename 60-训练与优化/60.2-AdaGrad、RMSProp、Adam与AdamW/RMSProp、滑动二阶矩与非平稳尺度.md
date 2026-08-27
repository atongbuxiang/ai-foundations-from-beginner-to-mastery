---
type: derivation
status: verified
area: [training, optimization, rmsprop]
node_id: TRN-10
aliases: [RMSProp 时标, 滑动平方梯度]
prerequisites: ["[[AdaGrad、累计平方梯度与稀疏几何]]", "[[Momentum、EMA、偏差修正与框架约定]]", "[[期望、方差与矩]]"]
related: ["[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]", "[[Momentum、EMA、偏差修正与框架约定]]"]
sources: ["[[S-2012-Hinton-RMSProp-Lecture]]", "[[S-2026-Framework-Adaptive-Optimizer-Semantics]]"]
exercises: ["[[习题 - RMSProp、滑动二阶矩与非平稳尺度]]"]
solutions: ["[[解答 - RMSProp、滑动二阶矩与非平稳尺度]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-rmsprop-timescale-response-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# RMSProp、滑动二阶矩与非平稳尺度

> [!abstract] 一句话结论
> RMSProp 把 AdaGrad 的永久累计改成梯度平方的指数滑动平均，使 denominator 能遗忘旧尺度。遗忘因子同时决定响应延迟、估计噪声和短暂过冲；centered、momentum、bias correction 与 epsilon placement 会产生不同算法，不能用一个名字覆盖。

## 一、从“总历史”改为“近期历史”

经典未居中 RMSProp 写成

$$
v_t=\rho v_{t-1}+(1-\rho)g_t^2,
\qquad
\theta_{t+1}=\theta_t-\eta\frac{g_t}{\sqrt{v_t}+\epsilon},
$$

其中平方、开根和除法逐坐标进行。与 AdaGrad 的

$$G_t=G_{t-1}+g_t^2$$

相比，旧梯度平方在 $v_t$ 中的权重每步乘 $\rho$，因此尺度改变后可以恢复。

展开递推（$v_0=0$）得

$$
v_t=(1-\rho)\sum_{s=1}^{t}\rho^{t-s}g_s^2.
$$

权重和是 $1-\rho^t$，所以早期 $v_t$ 向零偏。RMSProp 是否显式做 $v_t/(1-\rho^t)$ 修正，取决于定义与框架；不能把 Adam 的 bias correction 自动移植过来。

## 二、三个可解释时标

几何核 $\rho^k$ 至少有三种常见口径：

1. **e-folding time**

$$
\tau_e=-\frac1{\log\rho};
$$

2. **half-life**

$$
\tau_{1/2}=\frac{\log(1/2)}{\log\rho};
$$

3. i.i.d. 样本下均值估计的近似有效样本量

$$
N_{\mathrm{eff}}\approx\frac{1+\rho}{1-\rho}.
$$

当 $\rho=0.99$，$\tau_e\approx99.5$ 步、half-life 约 69 步，而 $N_{eff}\approx199$。三者回答不同问题，不能都口头叫“窗口大小 100”。

## 三、尺度突变时的精确响应

设突变前长期梯度平方为 $a^2$，所以 $v_T\approx a^2$；突变后每步梯度幅值固定为 $b$。经过 $k$ 步：

$$
\boxed{
v_{T+k}=\rho^ka^2+(1-\rho^k)b^2
}.
$$

若 $b\gg a$，初期 denominator 仍接近 $a$，所以 normalized update

$$
\frac{b}{\sqrt{v_{T+k}}+\epsilon}
$$

可能暂时大于稳态值 1，形成过冲；若 $b\ll a$，旧大尺度令更新暂时过小。这正是 forgetting 太慢的代价。

减小 $\rho$ 会更快跟踪新尺度，但 $v_t$ 本身更嘈杂；增大 $\rho$ 会平滑 estimator，却提高非平稳滞后。这里没有无条件最优的 $\rho$。

## 四、RMS 与标准差不是一回事

未居中版本估计的是 raw second moment

$$
\mathbb E[g^2]=\operatorname{Var}(g)+\mathbb E[g]^2.
$$

Centered RMSProp 另存一阶 EMA $a_t$：

$$
a_t=\rho a_{t-1}+(1-\rho)g_t,
\qquad
\widetilde v_t=v_t-a_t^2,
$$

再除以 $\sqrt{\widetilde v_t}+\epsilon$。它试图估计局部 variance，而不是 RMS。代价是多一份状态，且有限精度下 $v_t-a_t^2$ 可能出现很小的负值，需要 clamp/实现约定。

> [!warning] “centered 更统计正确”不是结论
> 优化器需要的是合适的 update geometry，不一定是无偏 variance estimator。减掉均值可能在高 SNR 坐标上显著放大步长；是否更好是算法与实验问题。

## 五、momentum 放在哪里

一种常见组合是先形成 normalized gradient

$$d_t=\frac{g_t}{\sqrt{v_t}+\epsilon},$$

再更新 momentum buffer

$$b_t=\mu b_{t-1}+d_t,\qquad
\theta_{t+1}=\theta_t-\eta b_t.
$$

另一种写法先对 raw gradient 做 momentum，再用 RMS denominator。两者一般不等价，因为 division 是非线性且 denominator 随时间变化。框架参数 `momentum` 只有在更新顺序明确后才有数学含义。

## 六、epsilon placement 是不同的响应函数

PyTorch 当前 RMSprop 文档使用

$$
\frac{g_t}{\sqrt{v_t}+\epsilon},
$$

并明确指出 TensorFlow RMSProp 交换开根和加 epsilon 的次序。另一形式是

$$
\frac{g_t}{\sqrt{v_t+\epsilon}}.
$$

前者的 epsilon 与 gradient 同单位，后者与 gradient square 同单位；同样写 `eps=1e-8` 并不是同一个 floor。[[Adam 的 Epsilon、数值稳定与实现分歧]]会系统比较响应曲线。

## 七、两步手算

取 $\rho=0.75,\eta=0.1,\epsilon=0$，$v_0=0$，梯度 $g_1=2,g_2=0$。

第一步：

$$
v_1=0.25\cdot4=1,
\qquad d_1=2,
\qquad\Delta\theta_1=-0.2.
$$

第二步：

$$
v_2=0.75,
\qquad d_2=0,
\qquad\Delta\theta_2=0.
$$

虽然当前梯度为零，二阶状态仍记得过去；若第三步来一个小梯度，其有效步长会被这份记忆压低。状态不更新参数时也可能继续演化，取决于 gradient 是零、缺失还是 step 被跳过。

## 八、图：一次尺度冲击怎样穿过 EMA

先看图回答：为什么慢 estimator 既更平滑，又可能在尺度跳升时制造过大 normalized update？

![[00-知识库管理/_assets/figures/training-optimization/fig-rmsprop-timescale-response-v1.svg|900]]

> [!figure] 图 TRN-10　RMSProp 的核权重、尺度阶跃与实现分叉
> 左侧比较永久累计与指数遗忘；中间画出梯度尺度突变后不同 $\rho$ 的 $v_t$ 响应；右侧分账 uncentered/centered、epsilon placement 与 momentum order。来源：依据 [[S-2012-Hinton-RMSProp-Lecture]] 和当前框架文档独立绘制。

**怎样读图**：先从核权重读记忆长度，再用阶跃响应判断 lag，最后检查右侧公式是否与自己的框架一致。

**图没有证明什么**：图不证明小 $\rho$ 或大 $\rho$ 普遍更优，也不把 $v_t$ 等同 Hessian；它展示的是 estimator dynamics。

## 九、AI 训练接口

- 在 curriculum、domain shift、RL/non-stationary reward 中，旧 $v_t$ 可能来自已经改变的分布；
- gradient accumulation 只在 optimizer step 时更新 $v_t$，所以 $\rho$ 的时间单位通常是 optimizer steps，不是 micro-steps 或 tokens；
- overflow 跳过 step 时，$v_t$ 和 step counter 是否推进必须明确；
- parameter group 的 $\rho,\epsilon$ 不同会产生不同适应时标；
- 在低精度中，state storage dtype 与 reduction accumulation dtype 决定小平方增量是否保留。

## 十、本节回顾

- RMSProp 用有限记忆换取对非平稳尺度的适应；
- $\rho$ 同时控制 estimator variance 与 lag；
- raw RMS、centered variance、momentum order 和 epsilon placement 是不同算法；
- 下一节 [[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]把一阶 EMA 与二阶 EMA 合在一个完整状态机中。

## 练习与独立解答

- [[习题 - RMSProp、滑动二阶矩与非平稳尺度]]
- [[解答 - RMSProp、滑动二阶矩与非平稳尺度]]
- 卷级复现：[[实验 - 自适应优化器状态、尺度与反例数值审计]]
