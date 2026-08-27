---
type: derivation
status: verified
area: [training, optimization, learning-rate, schedule]
node_id: TRN-35
aliases: [学习率调度总账, Learning Rate Schedule Ledger]
prerequisites: ["[[学习率、局部损失变化与相对更新尺度]]", "[[Warmup、早期曲率与优化器状态建立]]", "[[数列、极限与完备性的直觉]]"]
related: ["[[训练时域、Restart、Schedule-Free 与末端学习率]]", "[[权重衰减、尺度不变性与 Weight RMS 动力学]]", "[[训练控制器的联合实验、消融与证据地图]]"]
sources: ["[[S-2017-Loshchilov-Hutter-SGDR]]", "[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2024-Hu-MiniCPM-WSD]]", "[[S-2025-Su-11404-AdamW-Weight-RMS-Dynamic]]", "[[S-2025-Su-11459-WD-LR-Memory]]"]
exercises: ["[[习题 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]"]
solutions: ["[[解答 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-learning-rate-schedule-endpoint-area-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度

> [!abstract] 一句话结论
> 一个学习率 schedule 不是曲线名字，而是函数、端点、时钟、horizon、warmup、最低值与 step 推进规则的完整合同。比较 schedule 时，必须先区分“形状”“总面积”“末端温度”“是否依赖预定停止时刻”和它与 decay/averaging 的联动。

## 一、统一记号：先把 Warmup 与主调度分开

设：

- $t=0,1,\dots,T$：成功 optimizer update 的索引；
- $T_w$：warmup 终点；
- $T$：计划 horizon；
- $\eta_0$：初始 LR；
- $\eta_p$：peak LR；
- $\eta_f$：final/minimum LR。

warmup 可写成

$$
\eta_t
=\eta_0+(\eta_p-\eta_0)\frac{t}{T_w},
\qquad 0\le t\le T_w.
\tag{1}
$$

主调度用归一化进度

$$
s_t=\frac{t-T_w}{T-T_w}\in[0,1]
\tag{2}
$$

表示。若实现用 $t/T$、epoch、sample 或 token，曲线会改变；必须把实际定义写出来。

> [!warning] 离散端点
> 连续公式写 $s\in[0,1]$ 不自动解决离散代码的 off-by-one：最后一次用于更新的 LR 是 $\eta_{T-1}$ 还是 $\eta_T$？scheduler 在 optimizer.step 前还是后推进？恢复 checkpoint 后计数器是否一致？这些都会改变真实序列。

## 二、Constant：最简单，也最能暴露噪声地板

warmup 后

$$
\eta(s)=\eta_p.
\tag{3}
$$

优点：

- 不依赖未来 horizon；
- 便于研究 stationary dynamics、噪声地板和 anytime performance；
- 延长训练不改变过去使用过的 LR。

代价：

- 随机优化可能停在与 $\eta_p$ 有关的稳态邻域；
- normalized/sign-like update 在梯度变小时仍保持有限方向尺度；
- 若最终需要低噪声解，常要 cooldown、averaging 或显式停止选择。

连续“面积”是

$$
\mathcal A_{\mathrm{const}}
=\int_0^T\eta(t)\,dt
=T\eta_p
\tag{4}
$$

（暂忽略 warmup）。面积可以衡量累计标量步长，但不能识别方向翻转、曲率、噪声和 optimizer state。

## 三、Linear Decay：端点清楚，horizon 依赖直接

$$
\eta(s)=\eta_p+(\eta_f-\eta_p)s.
\tag{5}
$$

若 $\eta_f=0$，则平均 LR 与面积为

$$
\bar\eta=\frac{\eta_p}{2},
\qquad
\mathcal A_{\mathrm{linear}}=\frac{T\eta_p}{2}.
\tag{6}
$$

一般端点下：

$$
\mathcal A_{\mathrm{linear}}
=T\frac{\eta_p+\eta_f}{2}.
\tag{7}
$$

Linear 的斜率在端点不为零。若训练在 $T$ 之后继续，必须声明：

- 保持 $\eta_f$；
- 继续线性下降而变成负值（通常不允许）；
- 重新定义 $T$ 并重算整条 schedule；
- 从 checkpoint 开启新阶段。

这四者是不同算法。

## 四、Cosine：同面积不等于同轨迹

单周期 cosine annealing：

$$
\eta(s)
=\eta_f
+\frac{\eta_p-\eta_f}{2}
\left(1+\cos(\pi s)\right).
\tag{8}
$$

它满足

$$
\eta(0)=\eta_p,\qquad
\eta(1)=\eta_f,
\qquad
\eta'(0)=\eta'(1)=0.
$$

连续面积仍是

$$
\mathcal A_{\mathrm{cos}}
=T\frac{\eta_p+\eta_f}{2},
\tag{9}
$$

与相同端点的 linear 一样；但 cosine 前期保持更高 LR、末期更缓慢靠近 floor。因此面积相同不能说明优化轨迹相同。

[[S-2017-Loshchilov-Hutter-SGDR]] 还允许周期结束后 warm restart。注意重启 LR phase 不自动重置 optimizer state。

## 五、Inverse-Sqrt：必须声明尺度常数和转折点

一个常见 piecewise 版本是

$$
\eta_t
=
\begin{cases}
\eta_p\,t/T_w, & 0<t\le T_w,\\[4pt]
\eta_p\sqrt{T_w/t}, & t>T_w.
\end{cases}
\tag{10}
$$

它在 $t=T_w$ 连续，之后按 $t^{-1/2}$ 衰减。Transformer 原始配方常写成

$$
\eta_t
=d_{\mathrm{model}}^{-1/2}
\min\left(t^{-1/2},\,tT_w^{-3/2}\right),
\tag{11}
$$

这把模型维度尺度、warmup 和 peak LR 绑在一起。将它机械改写成“peak LR + inverse sqrt”时，必须检查是否仍等价。

忽略离散误差，$T>T_w$ 的尾部面积为

$$
\int_{T_w}^{T}
\eta_p\sqrt{\frac{T_w}{t}}\,dt
=2\eta_p\sqrt{T_w}\left(\sqrt T-\sqrt{T_w}\right).
\tag{12}
$$

总面积随 $\sqrt T$ 增长而非趋于常数；“LR 趋零”不等于“之后累计移动有限”。

## 六、WSD：Warmup–Stable–Decay 是三个阶段

令 $T_s$ 是 stable 段终点：

$$
\eta_t=
\begin{cases}
\eta_{\mathrm{warm}}(t), & 0\le t\le T_w,\\
\eta_p, & T_w<t\le T_s,\\
\eta_{\mathrm{decay}}\!\left(\dfrac{t-T_s}{T-T_s}\right),
& T_s<t\le T.
\end{cases}
\tag{13}
$$

WSD 的关键不是某个唯一 decay 函数，而是：

1. 一个较短 warmup；
2. 可延长、可保存 checkpoint 的 stable 主干；
3. 在选定 horizon 附近分叉的 cooldown。

[[S-2024-Hu-MiniCPM-WSD]] 用这个结构支持持续预训练、域适配与不同数据 horizon 的研究。它相对 full-horizon cosine 的一个工程优势是：延长 stable 段不会重写过去的 LR。

但必须记录：

- $T_w,T_s,T$ 的 step/token 口径；
- cooldown 是 linear、cosine、exponential 还是其他；
- decay ratio 与 final LR；
- cooldown 段数据混合是否改变；
- 从哪个 optimizer/checkpoint state 分叉；
- 不同分支是否匹配额外训练 compute。

## 七、端点、面积、平方面积与“温度”

对随机递推，常同时关心

$$
\sum_t\eta_t
\quad\text{和}\quad
\sum_t\eta_t^2.
\tag{14}
$$

前者影响累计漂移量级，后者在许多 stochastic approximation 界中控制噪声累积。经典收敛条件常出现

$$
\sum_t\eta_t=\infty,
\qquad
\sum_t\eta_t^2<\infty,
\tag{15}
$$

但有限 horizon 深网训练不满足“直接套用即得最优”的前提。式 (15) 只是提醒：

- 两条 schedule 即使 $\sum\eta_t$ 相同，$\sum\eta_t^2$ 也可不同；
- 末端 LR 决定最后迭代附近的噪声尺度；
- averaging 可改变输出估计器而不改变训练轨迹。

## 八、Schedule 与 Weight Decay 联动

AdamW 型 decoupled decay：

$$
\theta_{t+1}
=(1-\eta_t\lambda_t)\theta_t
-\eta_tu_t.
\tag{16}
$$

初始化残留系数是

$$
\prod_{i=0}^{t}(1-\eta_i\lambda_i)
\approx
\exp\left(-\sum_{i=0}^{t}\eta_i\lambda_i\right).
\tag{17}
$$

因此只改 LR schedule，即使 $\lambda_t$ 数值不变，也改变累计 shrinkage 和历史 update 的记忆核。[[S-2025-Su-11459-WD-LR-Memory]] 与 [[S-2025-Su-11404-AdamW-Weight-RMS-Dynamic]] 提供了这条中文推导入口。

> [!warning] 常见混杂
> “cosine 比 constant 泛化好”可能同时意味着末端 LR 更低、累计 decay 不同、最后 checkpoint 噪声更小、best-checkpoint selection 不同。若不分账，不能把差异归因给曲线形状。

## 九、同名 Schedule 的实现歧义

至少核对：

| 字段 | 可能歧义 |
|---|---|
| total steps | 数据 epoch 推算、显式 max_steps、成功 update 数 |
| warmup | steps、ratio、tokens；是否包含 peak 点 |
| final LR | 0、绝对 floor、peak ratio |
| scheduler order | optimizer.step 前/后 |
| resume | 恢复 scheduler state 还是重建 |
| accumulation | microstep 是否推进 |
| overflow | skipped update 是否推进 |
| parameter groups | 是否共享 progress、不同 peak/floor |
| restarts | 只重启 LR，还是同时重置其他状态 |

## 十、图：五条曲线必须连同合同一起比较

先看图回答：Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 在端点、面积、horizon 依赖和可延长性上有何不同？

![[00-知识库管理/_assets/figures/training-optimization/fig-learning-rate-schedule-endpoint-area-ledger-v1.svg|880]]

> [!figure] 图 TRN-35　Schedule 端点—面积—时域总账
> 上半比较五条归一化曲线，下半按 horizon dependency、末端 LR、累计面积与分叉能力整理合同。曲线为教学示意，不代表最优超参。来源：依据 [[S-2017-Loshchilov-Hutter-SGDR]]、[[S-2017-Vaswani-Transformer复杂度]] 与 [[S-2024-Hu-MiniCPM-WSD]] 原创绘制。

**怎样读图**：先看横轴是完整 horizon 还是 stable 主干，再看 final LR；随后比较 $\sum\eta_t$、$\sum\eta_t^2$，最后检查 schedule 是否与 decay/averaging 共同改变。

**图没有证明什么**：它没有证明任何一条曲线普遍更好；相同归一化形状在不同 optimizer、batch、数据和总 token 下仍是不同实验。

## 十一、初学者自检

1. 相同端点的 linear 与 cosine 为什么面积相同但轨迹不同？
2. inverse-sqrt LR 趋零，为何累计面积仍可无限增长？
3. 把 cosine 的 horizon 从 $T$ 改为 $2T$，前半段 LR 会不会保持不变？
4. WSD 的 stable checkpoint 为什么适合多 horizon 分叉？
5. 固定 weight decay 数值、只改 LR schedule，为什么总 shrinkage 仍会变？

## 十二、本节出口

你应能把任何 schedule 写成

$$
(\text{clock},T_w,T_s,T,
\eta_0,\eta_p,\eta_f,
\text{piecewise function},
\text{advance rule},
\text{group contract}),
$$

并手算端点、面积、平方面积与累计 decay。

## 练习与独立解答

- [[习题 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]
- [[解答 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]
