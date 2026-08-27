---
type: derivation
status: verified
area: [training, optimization, weight-decay, scale-invariance]
node_id: TRN-38
aliases: [Weight RMS 动力学, Weight Decay and Scale-Invariant Dynamics]
prerequisites: ["[[L2 正则、Coupled Decay 与 AdamW]]", "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]", "[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]"]
related: ["[[参数 EMA、SWA 与 Checkpoint Averaging]]", "[[BatchNorm 反向传播、尺度不变性与噪声]]", "[[Update-to-Weight Ratio、谱与尺度诊断]]"]
sources: ["[[S-2019-Loshchilov-Hutter-AdamW]]", "[[S-2020-Su-7681-L2正则与尺度不变性]]", "[[S-2025-Su-11307-AdamW-Weight-RMS]]", "[[S-2025-Su-11404-AdamW-Weight-RMS-Dynamic]]", "[[S-2025-Su-11459-WD-LR-Memory]]"]
exercises: ["[[习题 - 权重衰减、尺度不变性与 Weight RMS 动力学]]"]
solutions: ["[[解答 - 权重衰减、尺度不变性与 Weight RMS 动力学]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-weight-rms-decay-memory-dynamics-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 权重衰减、尺度不变性与 Weight RMS 动力学

> [!abstract] 一句话结论
> 在 AdamW 型递推中，learning rate 与 weight decay 共同决定参数对初始化和历史更新的记忆核；在归一化/尺度不变层中，权重范数还会反过来改变有效角学习率。Weight RMS 因而不是无关紧要的日志，而是 LR、decay、update statistics 和参数化共同形成的动态状态。

## 一、从精确 AdamW 型递推开始

对某个参数组统一写成

$$
\theta_{t+1}
=a_t\theta_t-\eta_tu_t,
\qquad
a_t=1-\eta_t\lambda_t,
\tag{1}
$$

其中 $u_t$ 已包含 optimizer 方向，但不含 decoupled decay。

展开得到

$$
\theta_t
=
\left(\prod_{j=0}^{t-1}a_j\right)\theta_0
-\sum_{i=0}^{t-1}
\eta_i
\left(\prod_{j=i+1}^{t-1}a_j\right)
u_i.
\tag{2}
$$

这是一条精确恒等式。它说明当前参数由：

1. 初始化残留；
2. 每个历史 update；
3. 从 update 发生后到当前的乘法衰减；

共同组成。

若 $\eta,\lambda$ 为常数：

$$
\theta_t
=a^t\theta_0
-\eta\sum_{i=0}^{t-1}a^{t-1-i}u_i,
\qquad a=1-\eta\lambda.
\tag{3}
$$

历史权重按几何级数衰减。小 $\eta\lambda$ 下：

$$
a^k\approx e^{-\eta\lambda k},
\tag{4}
$$

e-folding step time 约为

$$
\tau_{\mathrm{decay}}\approx\frac{1}{\eta\lambda}.
\tag{5}
$$

## 二、为什么只改 LR 也会改变 Weight Decay

动态 schedule 下，初始化权重近似

$$
\prod_{j=0}^{t-1}(1-\eta_j\lambda_j)
\approx
\exp\left(-\sum_{j=0}^{t-1}\eta_j\lambda_j\right).
\tag{6}
$$

因此：

- 固定 $\lambda$、用 cosine 降低 $\eta_t$，末段 decay 也同步变弱；
- fixed LR 与 linear/cosine 即使 peak 相同，累计 shrinkage 不同；
- skipped optimizer step 是否执行 decay、是否推进 scheduler 会改变记忆核；
- 若希望每 token decay 相同，batch/accumulation 改变后需重新定义 $\lambda$ 或时钟。

[[S-2025-Su-11459-WD-LR-Memory]] 把式 (2) 解释为历史 update 的滑动记忆。课程采用乘积核恒等式，但“模型记住多少数据”仍是解释假说，不是信息论容量定理。

## 三、Weight RMS 的二阶矩递推

令参数维度为 $d$：

$$
q_t=\frac1d\mathbb E\lVert\theta_t\rVert_2^2.
\tag{7}
$$

由 (1)：

$$
q_{t+1}
=a_t^2q_t
+\eta_t^2r_t
-2a_t\eta_tc_t,
\tag{8}
$$

其中

$$
r_t=\frac1d\mathbb E\lVert u_t\rVert^2,
\qquad
c_t=\frac1d\mathbb E\langle\theta_t,u_t\rangle.
\tag{9}
$$

式 (8) 是在期望存在时的精确分账：

- $a_t^2q_t$：旧参数保留；
- $\eta_t^2r_t$：update 注入能量；
- $-2a_t\eta_tc_t$：参数—更新相关交叉项。

### 平均场近似平衡

若 $\eta,\lambda,r$ 近似常数，且 $c_t\approx0$：

$$
q_\star
=\frac{\eta^2r}{1-(1-\eta\lambda)^2}
=\frac{\eta r}{2\lambda-\eta\lambda^2}.
\tag{10}
$$

当 $\eta\lambda\ll1$：

$$
q_\star\approx\frac{\eta r}{2\lambda},
\qquad
\operatorname{RMS}(\theta)
\approx\sqrt{\frac{\eta r}{2\lambda}}.
\tag{11}
$$

若 normalized update 满足 $r\approx1$，就得到常见

$$
\operatorname{RMS}(\theta)\approx\sqrt{\frac{\eta}{2\lambda}}.
\tag{12}
$$

[[S-2025-Su-11307-AdamW-Weight-RMS]] 提供这条估计的中文推导。

## 四、哪些条件一破，平方根律就会偏离

式 (11) 不是逐层恒等式。偏离来源包括：

1. $c_t\ne0$：update 与参数有径向相关；
2. $r_t$ 随训练、层、epsilon、clip 或 shape 改变；
3. $\eta_t,\lambda_t$ 变化速度接近或快于 $\tau_{\mathrm{decay}}$；
4. 初始化残留尚未消失；
5. 参数维数小，RMS 平均不稳定；
6. normalization symmetry 使 loss gradient 与参数正交；
7. bias/norm/embedding/readout 使用不同 parameter group；
8. optimizer state 切换或 resume 不完整。

[[S-2025-Su-11404-AdamW-Weight-RMS-Dynamic]] 强调动态 schedule 下 Weight RMS 有滞后；“瞬时平衡” $\sqrt{\eta_t/(2\lambda_t)}$ 只有 schedule 变化足够慢时才可能近似。

## 五、尺度不变层：Weight Norm 会反过来改变有效 LR

若某层满足正尺度不变：

$$
L(cw)=L(w),
\qquad c>0,
\tag{13}
$$

对 $c$ 求导可得

$$
w^\top\nabla_wL(w)=0.
\tag{14}
$$

梯度在一阶上与权重正交，只改变方向而不改变半径。

进一步由尺度关系：

$$
\nabla L(cw)=\frac1c\nabla L(w).
\tag{15}
$$

对 SGD，小步角更新量级

$$
\Delta\phi
\approx
\frac{\eta\lVert\nabla L(w)\rVert}{\lVert w\rVert}.
\tag{16}
$$

结合 (15)，在同一函数点的重参数化轨道上：

$$
\Delta\phi\propto\frac{\eta}{\lVert w\rVert^2}.
\tag{17}
$$

所以权重范数变大，会降低 SGD 的有效角学习率。Weight decay 虽不直接改变尺度不变函数值，却通过缩小 $\lVert w\rVert$ 提高未来角更新。

> [!warning] Adam/normalized update 的指数不同
> 若 optimizer 方向幅值对 gradient scale 近似不变，则角更新更接近 $\eta/\lVert w\rVert$，而不是 $\eta/\lVert w\rVert^2$。必须从实际 $u_t$ 推导，不能把 SGD 结论机械套到 Adam/Muon。

## 六、径向与切向分账

把更新分解为

$$
u_t=u_{\parallel,t}+u_{\perp,t},
\tag{18}
$$

其中

$$
u_{\parallel,t}
=\frac{\langle\theta_t,u_t\rangle}
{\lVert\theta_t\rVert^2}\theta_t.
\tag{19}
$$

- decoupled decay 是纯径向收缩；
- scale-invariant loss 的 exact gradient 是切向；
- finite precision、optimizer preconditioning、epsilon 和非完全尺度不变会产生径向分量；
- clip/AGC 可能改变径向—切向比例。

监控时应同时记录：

$$
\operatorname{RMS}(\theta),\quad
\operatorname{RMS}(\Delta\theta),\quad
\frac{\lVert\Delta\theta_\perp\rVert}{\lVert\theta\rVert},\quad
\frac{\langle\theta,\Delta\theta\rangle}{\lVert\theta\rVert^2}.
\tag{20}
$$

## 七、Decoupled Decay 不等于所有情况下的 L2 正则

SGD 对

$$
L(\theta)+\frac{\lambda}{2}\lVert\theta\rVert^2
$$

做一步梯度下降：

$$
\theta_{t+1}
=(1-\eta\lambda)\theta_t-\eta\nabla L(\theta_t),
\tag{21}
$$

与 decoupled decay 形式相同。

但对 adaptive optimizer，若把 $\lambda\theta$ 加入梯度再预条件：

$$
u_t=P_t(\widehat g_t+\lambda\theta_t),
\tag{22}
$$

decay 也被 $P_t$ 扭曲；这与先形成 data-gradient direction、再做 $(1-\eta\lambda)\theta$ 不同。[[S-2019-Loshchilov-Hutter-AdamW]] 的核心正是分离这两条路径。

## 八、参数组与排除规则

常见配置不对 bias、normalization scale 或某些 embedding/readout 做 decay。理由可能包括：

- 参数不代表可缩放 weight matrix；
- 接近零或低维，relative effect 过大；
- normalization 参数的函数语义不同；
- 延续经验 recipe。

这些是可检验设计选择，不是普适定理。必须记录每组：

$$
(\eta_t,\lambda_t,r_t,c_t,q_t,\text{scale symmetry},\text{dtype}).
\tag{23}
$$

## 九、图：Weight RMS 是带记忆的动态平衡

先看图回答：LR、decay、update energy 和尺度不变性怎样共同决定 Weight RMS 与有效角学习率？

![[00-知识库管理/_assets/figures/training-optimization/fig-weight-rms-decay-memory-dynamics-v1.svg|880]]

> [!figure] 图 TRN-38　Weight RMS、历史记忆核与角学习率
> 上排由 AdamW 递推展开历史 kernel，中排展示 $q_{t+1}=a^2q_t+\eta^2r-2a\eta c$ 的三项能量账，下排对比 SGD 与 normalized update 在尺度不变层上的角学习率。来源：依据 [[S-2019-Loshchilov-Hutter-AdamW]]、[[S-2025-Su-11307-AdamW-Weight-RMS]]、[[S-2025-Su-11404-AdamW-Weight-RMS-Dynamic]] 原创绘制。

**怎样读图**：先看累计 $\sum\eta\lambda$ 决定记忆衰减，再检查 update energy 和交叉项；最后根据 optimizer 是否归一化，选择 $\eta/\lVert w\rVert^2$ 或 $\eta/\lVert w\rVert$ 的角尺度入口。

**图没有证明什么**：它不证明真实网络每层都会达到平方根稳态，也不把 Weight RMS 与泛化质量画等号。

## 十、科学空间研读框

[[S-2025-Su-11307-AdamW-Weight-RMS]]、[[S-2025-Su-11404-AdamW-Weight-RMS-Dynamic]] 和 [[S-2025-Su-11459-WD-LR-Memory]] 构成一条很好的中文推导链：常 LR 稳态 → 动态 schedule 滞后 → 历史权重核。课程保留精确递推与平均场条件，并用 $r_t,c_t$ 两个账户显式标出真实训练偏离。

## 十一、初学者自检

1. 为什么固定 $\lambda$、只改 LR schedule 也会改变累计 decay？
2. 式 (8) 的交叉项 $c_t$ 表示什么？
3. $\sqrt{\eta/(2\lambda)}$ 近似需要哪些条件？
4. 尺度不变层中，weight norm 为什么改变 SGD 的有效角 LR？
5. coupled L2 与 decoupled AdamW 在 adaptive preconditioner 下为何不同？

## 十二、本节出口

你应能从 (1) 推到 (2)、(8) 和 (11)，并把训练日志中的 Weight RMS 解释为：

$$
\text{history kernel}
+\text{update energy}
+\text{radial correlation}
+\text{scale geometry},
$$

而不是孤立标量。

## 练习与独立解答

- [[习题 - 权重衰减、尺度不变性与 Weight RMS 动力学]]
- [[解答 - 权重衰减、尺度不变性与 Weight RMS 动力学]]
