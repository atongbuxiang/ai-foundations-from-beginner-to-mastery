---
type: derivation
status: verified
area: [training, optimization, adamw, regularization]
node_id: TRN-15
aliases: [AdamW 与 L2, Decoupled Weight Decay]
prerequisites: ["[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]", "[[网络级正则化的交互、消融与证据地图]]", "[[正则化、交叉验证与模型选择]]"]
related: ["[[权重衰减、尺度不变性与 Weight RMS 动力学]]", "[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]", "[[参数 EMA、SWA 与 Checkpoint Averaging]]"]
sources: ["[[S-2019-Loshchilov-Hutter-AdamW]]", "[[S-2025-Su-11307-AdamW-Weight-RMS]]", "[[S-2025-Su-11459-WD-LR-Memory]]", "[[S-2020-Su-7681-L2正则与尺度不变性]]", "[[S-2026-Framework-Adaptive-Optimizer-Semantics]]"]
exercises: ["[[习题 - L2 正则、Coupled Decay 与 AdamW]]"]
solutions: ["[[解答 - L2 正则、Coupled Decay 与 AdamW]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-adamw-decay-paths-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# L2 正则、Coupled Decay 与 AdamW

> [!abstract] 一句话结论
> 把 $\frac\lambda2\|\theta\|^2$ 加进 loss 会把 $\lambda\theta$ 送入 gradient、momentum 和 adaptive denominator；AdamW 则把乘法收缩直接作用于参数，不污染 $m,v$。无 momentum 的普通 SGD 中二者可按系数等价，带状态或逐坐标预条件后一般不同；“decoupled”说明更新位置，不自动说明最佳正则化或参数组。

## 一、先区分三个数学对象

### 1.1 Loss-side L2 penalty

优化

$$
F_{reg}(\theta)=F(\theta)+\frac\lambda2\|\theta\|_2^2
$$

会得到 gradient

$$
g_t^{reg}=g_t+\lambda\theta_{t-1}.
$$

### 1.2 Coupled optimizer update

把 $g_t^{reg}$ 交给 Adam：

$$
\begin{aligned}
m_t&=\beta_1m_{t-1}+(1-\beta_1)(g_t+\lambda\theta_{t-1}),\\
v_t&=\beta_2v_{t-1}+(1-\beta_2)(g_t+\lambda\theta_{t-1})^2.
\end{aligned}
$$

正则项不仅改变当前方向，还进入两份历史状态，并被逐坐标预条件。

### 1.3 Decoupled weight decay

AdamW 让 moments 只读取 task gradient $g_t$，参数另做

$$
\boxed{
\theta_t
=(1-\eta_t\lambda_t)\theta_{t-1}-\eta_tu_t
},
\qquad
u_t=\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon}.
$$

decay 是 isotropic multiplicative shrink；不会进入 $m_t,v_t$。

## 二、为什么 plain SGD 中可以等价

无 momentum、无预条件的 SGD 对 regularized objective 更新：

$$
\theta_t
=\theta_{t-1}-\eta_t(g_t+\lambda\theta_{t-1})
=(1-\eta_t\lambda)\theta_{t-1}-\eta_tg_t.
$$

这与 LR-scaled multiplicative decay 完全相同。若实现把 decay 写成 $\theta\leftarrow(1-\lambda)\theta$ 而不乘 LR，则需要重新换算参数，不能只比较同名 `weight_decay`。

一旦加入 momentum，coupled $\lambda\theta$ 会进入 buffer；decoupled shrink 不进入，所以即使是 SGDM 也一般不再逐步等价。[[S-2019-Loshchilov-Hutter-AdamW]]的“SGD 等价”必须理解为无额外状态差异的标准情形。

## 三、二维例子看自适应非等价

设当前 task gradient 为零，$\theta=(1,1)$，把 Adam 当作给定对角 preconditioner

$$P=\operatorname{diag}(1,0.1).$$

Coupled L2 的一步是

$$
\Delta\theta_{L2}=-\eta P(\lambda\theta)
=-\eta\lambda(1,0.1).
$$

Decoupled decay 的一步是

$$
\Delta\theta_{WD}=-\eta\lambda\theta
=-\eta\lambda(1,1).
$$

前者让第二坐标收缩慢十倍，后者两坐标保持同一相对收缩。真实 Adam 的 $P_t$ 还随 coupled gradient 更新，因此差异会进入未来。

## 四、AdamW 的 decay 时标

只有 decay、无 task update 时：

$$
\theta_T
=\left[\prod_{t=1}^{T}(1-\eta_t\lambda_t)\right]\theta_0.
$$

当每步 $\eta_t\lambda_t$ 很小：

$$
\prod_t(1-\eta_t\lambda_t)
\approx
\exp\!\left(-\sum_t\eta_t\lambda_t\right).
$$

所以 cumulative decay 由 $\sum_t\eta_t\lambda_t$ 控制，而不只由 nominal $\lambda$。更换 LR schedule、总步数或 gradient accumulation 后，即使 `weight_decay` 数字不变，也未必是同一正则化动力学。

常数 $\eta,\lambda$ 下 e-folding 时标约为

$$
\tau_{wd}\approx\frac1{\eta\lambda}.
$$

[[S-2025-Su-11459-WD-LR-Memory]]把它解释为历史 update 的滑动记忆时标；乘积权重是代数事实，“等于模型记忆数据能力”则只是研究假说。

## 五、Weight RMS 平衡从哪里来

把 AdamW 写成

$$
\theta_t=(1-\eta\lambda)\theta_{t-1}-\eta u_t.
$$

若 $u_t$ 近似零均值、各向同性、与 $\theta_{t-1}$ 相关项可忽略，并设

$$q=\mathbb E[\operatorname{RMS}(u_t)^2],$$

则平方 RMS 近似满足

$$
s_t^2\approx(1-\eta\lambda)^2s_{t-1}^2+\eta^2q.
$$

稳态解为

$$
s_\infty^2
\approx
\frac{\eta^2q}{1-(1-\eta\lambda)^2}
\approx\frac{\eta q}{2\lambda}.
$$

若进一步把 normalized total contribution 取 $q\approx1$，得到

$$
\operatorname{RMS}(\theta)_\infty
\approx\sqrt{\frac{\eta}{2\lambda}}.
$$

[[S-2025-Su-11307-AdamW-Weight-RMS]]给出更完整的平均场推导。该式不是一般 identity：非零 mean update、变化 schedule、归一化尺度对称、不同参数组、初始化未衰减和训练未达稳态都会改变它。

## 六、L2 penalty 与 weight decay 的语义差异

| 问题 | L2 penalty | Decoupled decay |
|---|---|---|
| 是否对应显式正则化 objective | 是，$F+\lambda\|\theta\|^2/2$ | 一般是 optimizer dynamics，不必等于某个静态 objective |
| 是否进入 $m,v$ | coupled 实现会 | 不会 |
| 是否被逐坐标预条件 | 会 | 通常不，直接 isotropic shrink |
| 与 LR schedule 的耦合 | 经 optimizer 与 schedule | 每步 shrink 显式含 $\eta_t\lambda_t$ |
| Bayesian prior 解释 | 在特定 likelihood/prior/MAP 条件下 | 不能自动继承 |

所以“AdamW 是更正确的 L2”也不准确；它恢复的是 decoupled decay 动力学，不是证明某个 prior 更正确。

## 七、哪些参数要 decay

工程上常对 matrix weights decay，而对 bias、LayerNorm/RMSNorm scale、某些 embedding 不 decay。这是常见 recipe，不是普适定理。需要逐组记录：

- 是否存在尺度不变性或正齐次重参数化；
- weight norm 是否影响 effective function-space learning rate；
- 参数是否稀疏、共享或有显式约束；
- 公平比较是否保持参数组、LR 与调参预算一致。

在 scale-invariant layer 中，weight norm 改变可能不改前向函数，却改变 gradient 与有效角速度；decay 的作用不只是“防过拟合”。这部分在 [[权重衰减、尺度不变性与 Weight RMS 动力学]]展开。

## 八、当前框架合同

根据 [[S-2026-Framework-Adaptive-Optimizer-Semantics]]：

- PyTorch Adam 的 `weight_decay` 默认仍是 coupled L2-style；当前可用 `decoupled_weight_decay=True` 切换；
- PyTorch AdamW 明确 decay 不进入 momentum/variance；
- checkpoint 迁移要保存类名之外的实际 flag、param groups、LR schedule 与 step；
- fused/foreach 路径不应改变高层合同，但可能改变内存、性能和末位数值。

## 九、图：同一个 lambda 走了两条不同路径

先看图回答：$\lambda\theta$ 是否进入 $m,v$？二维 preconditioner 下两个坐标的相对收缩是否相同？

![[00-知识库管理/_assets/figures/training-optimization/fig-adamw-decay-paths-v1.svg|900]]

> [!figure] 图 TRN-15　Loss-side L2、coupled Adam 与 decoupled AdamW
> 左侧追踪 $\lambda\theta$ 进入 gradient/moments 的 coupled 路径；中间展示 AdamW 的独立乘法 shrink；右侧分账 cumulative decay、Weight RMS 近似与参数组边界。来源：据 [[S-2019-Loshchilov-Hutter-AdamW]] 及两篇科学空间来源独立绘制。

**怎样读图**：先沿箭头检查 decay 是否污染 optimizer state，再比较两坐标 shrink，最后把 exact product 与 mean-field equilibrium 分层。

**图没有证明什么**：图不证明 AdamW 在所有任务上泛化更好，也不证明 $\sqrt{\eta/(2\lambda)}$ 对每层精确成立。

## 十、本节回顾

- L2 是 objective-side gradient，AdamW 是 optimizer-side decoupled shrink；
- plain SGD 无状态时可等价，momentum/adaptation 后一般不同；
- cumulative decay 看 $\sum\eta_t\lambda_t$；
- Weight RMS 公式是带稳态/零均值/平均场条件的尺度估计；
- 下一节 [[Lion、Adafactor 与自适应优化器证据地图]]比较状态内存与实验公平性。

## 练习与独立解答

- [[习题 - L2 正则、Coupled Decay 与 AdamW]]
- [[解答 - L2 正则、Coupled Decay 与 AdamW]]
- 卷级复现：[[实验 - 自适应优化器状态、尺度与反例数值审计]]
