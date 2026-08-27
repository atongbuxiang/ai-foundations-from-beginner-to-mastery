---
type: derivation
status: verified
area: [training, scaling-laws, statistics, extrapolation]
node_id: TRN-49
aliases: [Empirical Scaling Laws, Power Law with Irreducible Loss]
prerequisites: ["[[渐近记号、增长率与复杂度]]", "[[统计模型、估计量与偏差方差]]", "[[正则化、交叉验证与模型选择]]"]
related: ["[[Kaplan 参数数据律、联合拟合与有限区间]]", "[[Broken Scaling、涌现表象与优化架构数据分解]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
sources: ["[[S-2020-Kaplan-语言模型尺度定律]]", "[[S-2020-Henighan-Autoregressive-Scaling]]", "[[S-2022-Alabdulmohsin-Revisiting-Neural-Scaling-Laws]]", "[[S-2025-Choshen-Hitchhikers-Scaling-Law]]", "[[S-2023-Su-9607-量子化假设与尺度定律]]", "[[S-2026-Su-11833-解构ScalingLaw]]"]
exercises: ["[[习题 - 经验 Scaling Law、幂律拟合与不可约项]]"]
solutions: ["[[解答 - 经验 Scaling Law、幂律拟合与不可约项]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-scaling-offset-window-slope-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 经验 Scaling Law、幂律拟合与不可约项

> [!abstract] 一句话结论
> Scaling Law 首先是一个有限观测窗口中的统计模型：必须同时声明横轴对象、损失地板、误差模型、拟合窗口和外推目标。只有 excess loss $L-E$ 服从幂律时，raw loss $L$ 的 log–log 斜率才会随接近地板而变平；把这种弯曲误判成 exponent 改变，是初学者最常见的错误之一。

## 一、先问“什么随什么变化”

经验式

$$
L(x)\approx E+A x^{-\alpha}
\tag{1}
$$

看似只有四个符号，实际上需要一张对象合同。

| 符号 | 必须声明 |
|---|---|
| $x$ | total/non-embedding/active 参数、unique/seen tokens、model FLOPs、wall time，还是别的尺度 |
| $L$ | train/validation/test cross-entropy、per-token nats、per-byte bits，还是下游指标 |
| $E$ | 在固定数据分布与 loss 下的不可约项或经验地板 |
| $A$ | 单位、数据、架构、优化协议共同决定的系数 |
| $\alpha$ | 当前模型族与尺度窗口中的经验指数 |

若横轴从参数量换成 FLOPs，或 loss 从 nats/token 换成 accuracy，式 (1) 的系数、指数乃至函数族都可能改变。因此“指数是多少”必须排在“对象是什么”之后。

[[S-2020-Kaplan-语言模型尺度定律]] 在特定 Transformer、数据和训练制度中观察到参数、数据与 compute 的经验幂律；这不是对任意神经网络的渐近定理。

## 二、为什么要有不可约项 $E$

对真实分布 $P$ 和模型 $Q_\theta$，cross-entropy 可写为

$$
H(P,Q_\theta)=H(P)+D_{\mathrm{KL}}(P\Vert Q_\theta).
\tag{2}
$$

若模型与优化最终逼近 $P$，$H(P)$ 给出一个信息论地板入口。因此 [[S-2020-Henighan-Autoregressive-Scaling]] 使用 power-law-plus-constant 描述多个自回归生成域。

但要谨慎：

- 真实 $P$ 不可直接获得；
- validation set 只是目标分布的有限样本；
- tokenizer、预处理与 support 会改变 per-token loss；
- misspecification、优化不足和数据 shift 会让经验地板不等于 $H(P)$。

所以课程把 $E$ 称为“拟合中的不可约/渐近项”，只有在附加条件下才解释为真实熵。

## 三、Raw Log–Log 斜率为什么会弯

若式 (1) 精确成立，则 excess loss

$$
R(x)=L(x)-E=A x^{-\alpha}
\tag{3}
$$

满足

$$
\log R=\log A-\alpha\log x,
\tag{4}
$$

是一条斜率 $-\alpha$ 的直线。

但 raw loss 的局部 log slope 是

$$
\frac{d\log L}{d\log x}
=\frac{xL'(x)}{L(x)}
=-\alpha\frac{A x^{-\alpha}}{E+A x^{-\alpha}}
=-\alpha\left(1-\frac{E}{L(x)}\right).
\tag{5}
$$

当 $A x^{-\alpha}\gg E$ 时，它接近 $-\alpha$；当 $L\to E$ 时，它趋于 0。于是：

> 同一个固定 exponent 加上 offset，就能在 raw log–log 图中产生“斜率越来越平”的曲线。

这并不自动说明机制或 exponent 改变。

## 四、两点斜率不是完整拟合

若已知 $E$，两点 $(x_1,L_1),(x_2,L_2)$ 给

$$
\widehat\alpha
=-\frac{
\log(L_2-E)-\log(L_1-E)
}{
\log x_2-\log x_1
}.
\tag{6}
$$

若把 $E$ 错设为 0，估计会系统偏小；若 $E$ 接近某个 $L_i$，微小 loss 误差又会被 $\log(L_i-E)$ 放大。

例：真实

$$
L(x)=1+4x^{-1/2}.
\tag{7}
$$

在 $x=4,16$ 时，loss 分别为 3 和 2。忽略 $E$ 得

$$
\widehat\alpha_{\rm raw}
=-\frac{\log2-\log3}{\log16-\log4}
\approx0.292,
\tag{8}
$$

而对 excess loss 拟合得到正确的 $0.5$。这不是数值小误差，而是模型设定错误。

## 五、在原尺度拟合还是在对数尺度拟合

两种常见目标是

$$
\min_\theta\sum_i
\left[L_i-\widehat L(x_i;\theta)\right]^2
\tag{9}
$$

和

$$
\min_\theta\sum_i
\left[\log(L_i-E)-\log A+\alpha\log x_i\right]^2.
\tag{10}
$$

它们隐含不同噪声模型：

- 式 (9) 更接近原尺度同方差 Gaussian error；
- 式 (10) 更接近 excess loss 的相对/乘性误差；
- 若不同尺度的 seed variance 不同，应使用权重或分层模型；
- 若 $E$ 未知，式 (10) 还是非线性拟合，不能先任意减一个常数。

“取对数再线性回归”只是某个误差模型下的方法，不是幂律拟合的定义。

## 六、有限窗口中的不可识别性

在窄窗口 $[x_{\min},x_{\max}]$ 内，许多三元组 $(E,A,\alpha)$ 可以产生几乎相同曲线。原因是：

1. $E$ 上调可由 $A$ 与 $\alpha$ 补偿；
2. 相邻尺度点高度相关；
3. 单 seed 的训练噪声可大于不同函数族的差；
4. 较小模型可能仍受优化或输出层 compute 混杂。

因此参数置信区间不能只由回归软件的局部 Hessian 给出。至少需要：

- seeds 或重复训练；
- held-out scales；
- 多个候选函数族；
- 对 scale point 而非单条日志行做 block resampling；
- 报告预测区间，不只报告 coefficient standard error。

[[S-2022-Alabdulmohsin-Revisiting-Neural-Scaling-Laws]] 主张用 extrapolation loss 选择估计方法；[[S-2025-Choshen-Hitchhikers-Scaling-Law]] 进一步显示 intermediate checkpoints 与接近 target 的尺度点常有价值。

## 七、局部指数是诊断量

定义 excess-loss elasticity

$$
\alpha_{\rm local}(x)
=-\frac{d\log(L-E)}{d\log x}.
\tag{11}
$$

若单一幂律成立，它应在误差范围内近似常数。离散估计可用相邻点

$$
\widehat\alpha_{i+1/2}
=-\frac{
\log(L_{i+1}-E)-\log(L_i-E)
}{
\log x_{i+1}-\log x_i
}.
\tag{12}
$$

局部指数漂移可能来自：

- $E$ 错误；
- finite-window correction；
- optimizer 未调好；
- 数据/架构改变；
- 真正的 broken scaling；
- 测量噪声或选择偏差。

它是报警器，不是机制标签。

## 八、假设驱动的幂律解释

[[S-2023-Su-9607-量子化假设与尺度定律]] 从“能力单元的难度/频率 tail”出发，把未学能力的 tail sum 近似为积分，从而得到幂律。这条逻辑是：

$$
\text{能力分解与 tail 假设}
\Rightarrow
\text{tail sum}
\Rightarrow
\text{幂律}.
\tag{13}
$$

它训练了一个重要习惯：理论解释必须列出中间假设。但真实网络是否存在独立能力单元、tail 是否稳定、学习阈值怎样随优化器变化，都不是式 (13) 自动证明的。

[[S-2026-Su-11833-解构ScalingLaw]] 又把 loss gap 按数据、优化和架构组织起来；课程把这当作候选分解与实验地图，不把单调性直接升级为幂律。

## 九、最小拟合与外推协议

1. 预注册 $x,L$、单位、模型族、训练时域和 target scale；
2. 保存每个 scale 的全部 seeds、失败和 intermediate checkpoints；
3. 候选至少含 constant-free、plus-offset、finite-correction 或 broken model；
4. calibration scales 拟合，validation scales 选函数，最大 held-out scale 只做一次检验；
5. 报告 interpolation residual、held-out error、prediction interval 与局部 slope；
6. 改动窗口、参数口径或剔除点时，作为 sensitivity analysis 单列；
7. 没有 held-out scale 时，只称“观测窗口内描述良好”。

## 十、图：Offset、窗口与斜率是同一个问题

先看图回答：为什么左侧 raw loss 会弯，而右侧减去正确地板后变直？若只看到中间三个点，$E$ 与 $\alpha$ 是否能被唯一识别？

![[00-知识库管理/_assets/figures/training-optimization/fig-scaling-offset-window-slope-v1.svg|900]]

> [!figure] 图 TRN-49-01　Power law、offset 与 finite-window slope
> 来源：课程原创教材图；左栏比较 $L=E+Ax^{-\alpha}$ 的 raw loss 与地板；中栏显示 excess loss 的 log–log 直线；右栏把 raw/local slope、函数族和 held-out scale 放入同一审计链。概念依据：[[S-2020-Henighan-Autoregressive-Scaling]]、[[S-2022-Alabdulmohsin-Revisiting-Neural-Scaling-Laws]]。

**怎样读图**：先区分 raw 与 excess loss，再看 calibration window 是否覆盖曲率，最后检查 held-out scale 是否落在预测区间。

**图没有证明什么**：示意曲线不证明任意真实模型服从幂律，也不提供 Kaplan/Chinchilla 的具体指数；它只揭示 offset 与有限窗口怎样制造斜率错觉。

## 十一、初学者自检

- 能否不用“更大模型更好”来定义 Scaling Law，而写出式 (1) 的完整对象合同？
- 能否从式 (1) 独立推导 raw slope 式 (5)？
- 能否解释原尺度与 log 尺度最小二乘对应的误差模型不同？
- 能否在没有 held-out scale 时主动降低结论强度？

如果第四问做不到，就还没有从“画直线”进入统计外推。
