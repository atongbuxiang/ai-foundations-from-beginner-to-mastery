---
type: derivation
status: verified
area: [training, optimization, horizon, schedule-free]
node_id: TRN-36
aliases: [训练 Horizon 与 Schedule-Free, Training Horizon and Schedule-Free Optimization]
prerequisites: ["[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]", "[[Momentum、EMA、偏差修正与框架约定]]", "[[在线学习协议、Regret 与 Comparator]]"]
related: ["[[参数 EMA、SWA 与 Checkpoint Averaging]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]", "[[训练控制器的联合实验、消融与证据地图]]"]
sources: ["[[S-2017-Loshchilov-Hutter-SGDR]]", "[[S-2024-Hu-MiniCPM-WSD]]", "[[S-2024-Defazio-Schedule-Free]]", "[[S-2019-Dodge-Show-Your-Work]]"]
exercises: ["[[习题 - 训练时域、Restart、Schedule-Free 与末端学习率]]"]
solutions: ["[[解答 - 训练时域、Restart、Schedule-Free 与末端学习率]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-horizon-restart-schedule-free-state-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 训练时域、Restart、Schedule-Free 与末端学习率

> [!abstract] 一句话结论
> 预先写入总步数 $T$ 的 schedule 会让“何时停止”进入算法定义：延长 horizon 可能改写过去本应使用的 LR。WSD、restart 和 Schedule-Free 分别用“稳定主干+末段分叉”“周期重启”“在线平均状态”处理时域问题，但它们都不是无状态、无选择规则或无末端语义。

## 一、Horizon 不是日志字段，而可能是算法输入

设 full-horizon cosine 为

$$
\eta_t(T)
=\eta_f
+\frac{\eta_p-\eta_f}{2}
\left(1+\cos\frac{\pi t}{T}\right).
\tag{1}
$$

在同一个绝对 step $t<T$：

$$
\eta_t(2T)>\eta_t(T)
\qquad (0<t<T).
\tag{2}
$$

所以一开始计划训练 $T$ 步与一开始计划训练 $2T$ 步，不只是“后者多跑一段”；它们从早期就使用不同 LR。

Linear decay 也有同样问题：

$$
\eta_t(T)=\eta_p-(\eta_p-\eta_f)\frac{t}{T}.
\tag{3}
$$

如果训练到 $0.8T$ 时才决定把 horizon 延长到 $2T$：

- 保持已经发生的历史，再从当前 LR 重新规划，是 piecewise 新算法；
- 假装从一开始就用 $2T$ cosine，无法追溯重写已有轨迹；
- 从旧 checkpoint 重新训练整段，才是严格的 $2T$ baseline。

## 二、四种“延长训练”必须分开

### 1. Continue

保留参数、optimizer state、scheduler state、data cursor 与 RNG，按原规则继续。若原 schedule 在 $T$ 后未定义，必须新增 continuation rule。

### 2. Resume

目标是从中断点逐步复现同一轨迹。除了参数，还需恢复：

$$
(s_t,\text{scheduler counter},\text{loss scale},
\text{data order},\text{RNG},\text{EMA/SWA state}).
\tag{4}
$$

只加载 model weights 不叫严格 resume。

### 3. Restart

有意重置某些状态并开启新阶段。必须列出 reset mask：

| 状态 | keep / reset / transform |
|---|---|
| model parameters |  |
| momentum / Adam moments |  |
| optimizer step counter |  |
| scheduler phase |  |
| weight EMA/SWA |  |
| loss scaler |  |
| data cursor / RNG |  |
| normalization running stats |  |

### 4. Fine-tune / Domain-adapt

数据分布、目标、参数组或正则改变。即使 LR 曲线连续，也不是原预训练实验的简单延长。

## 三、Warm Restart：重启了什么

SGDR 的 cosine 周期 $i$ 内：

$$
\eta_t
=\eta_{\min}^{(i)}
+\frac{\eta_{\max}^{(i)}-\eta_{\min}^{(i)}}{2}
\left(1+\cos\frac{\pi T_{\mathrm{cur}}}{T_i}\right).
\tag{5}
$$

当 $T_{\mathrm{cur}}=T_i$ 后，把 phase 置回 0，并可令

$$
T_{i+1}=T_{\mathrm{mult}}T_i.
\tag{6}
$$

“warm” 表示保留模型参数继续训练，不是把网络随机重初始化。

必须区分：

- 只重启 LR phase；
- 同时改变 $\eta_{\max}$ 或周期长度；
- 是否重置 momentum/Adam moments；
- 周期端点的 checkpoint 是 raw、EMA 还是 averaged；
- 周期之间数据是否继续无缝流动。

> [!warning] 机制边界
> LR 上升可能改变噪声与探索范围，但“restart 帮助逃离局部极小”是解释假说，不是从 cosine 公式自动推出的定理。

## 四、WSD：把 horizon 依赖推迟到 cooldown 分支

WSD 的 stable 主干在 $T_w<t\le T_s$ 使用常数 peak LR。若在 token $D_1,D_2,D_3$ 都想得到可部署模型，可以：

1. 训练一条共同 stable trunk；
2. 在不同 checkpoint 复制完整训练状态；
3. 分别运行 cooldown branch；
4. 对每个 branch 匹配额外 token、数据混合和 selection rule。

相较 full-horizon cosine，这避免为每个未来 horizon 从头重跑完整主干。

但它没有消除 horizon：

- cooldown 仍需一个终点；
- branch 起点和长度仍是选择；
- final LR 和 decay shape 仍影响结果；
- 主干 checkpoint 若被反复查看验证集，会产生选择偏差。

## 五、Schedule-Free 的核心问题：在线平均怎样替代预定衰减

很多依赖 $T$ 的理论/实践策略最终输出某种加权平均迭代。Schedule-Free 的思想是把这个平均过程做成在线状态，从而不必预先知道停止时刻。

先看一般在线加权平均。给定候选点 $z_t$ 和非负权重 $w_t$：

$$
W_t=\sum_{i=1}^t w_i,
\qquad
x_t=\frac{1}{W_t}\sum_{i=1}^t w_i z_i.
\tag{7}
$$

它可递推为

$$
x_t
=(1-c_t)x_{t-1}+c_tz_t,
\qquad
c_t=\frac{w_t}{W_t}.
\tag{8}
$$

一个教学化的 schedule-free 原型同时维护：

- $z_t$：由梯度更新的快速/优化点；
- $x_t$：在线平均点；
- $y_t$：用于求梯度的插值点。

概念性写成

$$
y_t=(1-\beta)x_t+\beta z_t,
\qquad
g_t=\nabla L(y_t),
\tag{9}
$$

$$
z_{t+1}=z_t-\gamma_t g_t,
\qquad
x_{t+1}=(1-c_{t+1})x_t+c_{t+1}z_{t+1}.
\tag{10}
$$

式 (9)—(10) 用来理解“三个点”的角色，不替代 [[S-2024-Defazio-Schedule-Free]] 或具体库版本的精确伪代码。生产算法还包含 momentum、warmup、权重选择、AdamW 状态和 train/eval 切换等细节。

## 六、“Schedule-Free”不等于没有时间依赖

名称容易造成四个误解。

### 误解 1：LR 恒定且什么都不变

实际仍有 base LR、warmup、momentum、averaging weights $w_t$ 和状态年龄。

### 误解 2：没有额外状态

至少有平均点/快速点及 optimizer moments。checkpoint 必须保存全部状态，否则 resume 轨迹改变。

### 误解 3：训练点就是评估点

某些实现训练时在插值点求梯度，评估时切换到不同组合。忘记 train/eval mode 转换，会比较错误对象。

### 误解 4：任意停止都同样好

虽然不需预先输入 $T$，输出仍取决于停止时刻、验证选择、数据已见量和平均权重。horizon-free 不是 performance-free。

## 七、末端学习率为何单独重要

对局部强凸随机递推，常数 LR 下 last iterate 在最优点附近形成稳态波动。把 $\eta_t$ 降低可能：

- 减小参数噪声方差；
- 提高训练 loss 的最后收敛精度；
- 改变 basin/feature 的继续漂移；
- 同时削弱有限 LR 的隐式正则或探索。

因此 final LR 是独立实验因子，不能只由“cosine/linear”名字代替。

需要区分三个输出：

$$
\theta_T
\quad\text{last iterate},
\qquad
\theta_{t^\star}
\quad\text{selected checkpoint},
\qquad
\bar\theta_T
\quad\text{averaged iterate}.
\tag{11}
$$

三者的训练 loss、验证表现与复现成本可以不同。

## 八、Checkpoint Selection 会把时域变成统计问题

若在 $K$ 个 checkpoint 上反复查看同一验证集并取最好者，选择规则本身带来乐观偏差。比较 schedule 时必须匹配：

- checkpoint 频率；
- 可选择窗口；
- early-stopping patience；
- 评估次数；
- 最后一次还是最好一次；
- 每次评估的样本与随机性；
- raw/EMA/SWA 哪个权重进入选择。

[[S-2019-Dodge-Show-Your-Work]] 进一步要求把超参数搜索预算和 expected best validation performance 纳入报告。一个 schedule 有更多 horizon/decay 分支，就有更大的选择空间。

## 九、时域不变性的最小实验

若声称方法“便于任意延长”，至少做：

1. 在 $T_1$ 时停止并评估；
2. 同一 run 从 $T_1$ 继续到 $T_2$；
3. 从一开始按 $T_2$ 配置训练 baseline；
4. 从 $T_1$ 的完整状态和 weights-only 两种 checkpoint 分别恢复；
5. 比较参数差、状态差、LR 序列、已见 token、validation selection。

对 WSD 还应比较 stable trunk + cooldown 与 full-horizon cosine；对 Schedule-Free 还要核对 train/eval state transformation。

## 十、图：三种解决 Horizon 问题的方法

先看图回答：Full-horizon decay、WSD/restart 与 Schedule-Free 分别把“未来停止时刻”放在什么状态里？

![[00-知识库管理/_assets/figures/training-optimization/fig-horizon-restart-schedule-free-state-v1.svg|880]]

> [!figure] 图 TRN-36　Horizon、分支与在线平均状态机
> 左栏显示 full-horizon cosine 在改变 $T$ 时重写早期 LR；中栏显示 WSD stable trunk 与 cooldown branches、SGDR phase restart；右栏显示 schedule-free 原型的 $z/x/y$ 三点和 train/eval 输出语义。来源：依据 [[S-2017-Loshchilov-Hutter-SGDR]]、[[S-2024-Hu-MiniCPM-WSD]]、[[S-2024-Defazio-Schedule-Free]] 原创绘制。

**怎样读图**：先判断过去的 LR 是否依赖未来 $T$；再核对分支时复制了哪些状态；最后确认训练求梯度点与部署评估点是否相同。

**图没有证明什么**：图不证明 WSD、restart 或 Schedule-Free 普遍优于 full-horizon decay，也不把教学原型当官方实现伪代码。

## 十一、初学者自检

1. 为什么把 cosine 的 $T$ 延长一倍会改变早期 LR？
2. restart 与 resume 的本质差别是什么？
3. WSD 为什么只是把 horizon 依赖推迟，而不是消除？
4. Schedule-Free 至少需要保存哪些新增状态？
5. last、best 和 averaged checkpoint 为什么不是同一个 estimator？

## 十二、本节出口

你应能对任何训练延长方案写出

$$
\text{past LR dependency}
\to
\text{state copy/reset mask}
\to
\text{future schedule/averaging}
\to
\text{stop and selection rule},
$$

并判断它是 continue、resume、restart、branch 还是新实验。

## 练习与独立解答

- [[习题 - 训练时域、Restart、Schedule-Free 与末端学习率]]
- [[解答 - 训练时域、Restart、Schedule-Free 与末端学习率]]
