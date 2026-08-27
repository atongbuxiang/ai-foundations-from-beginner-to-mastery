---
type: concept
status: verified
area: [training, telemetry, observability, diagnostics]
course_id: TRN-65
prerequisites: ["[[训练系统的对象、状态与一步更新合同]]", "[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
related: ["[[NaN、Inf、梯度爆炸与训练失败决策树]]", "[[Update-to-Weight Ratio、谱与尺度诊断]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2026-PyTorch-Profiler]]", "[[S-2023-Google-Deep-Learning-Tuning-Playbook]]", "[[S-2026-PyTorch-Reproducibility]]", "[[S-2025-Su-11267-Adam-Update-RMS]]", "[[S-2025-Su-11404-AdamW-Weight-RMS-Dynamic]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 训练 Telemetry、损失梯度更新与激活总账

> [!abstract] 本节目标
> 把“看一条 loss 曲线”升级为多时钟、分层、可回放的训练观测系统。学完后，你应能设计一个开销可控的最小 dashboard，分清数据、前向、反向、更新与系统信号，并知道 telemetry 能定位什么、不能证明什么。

## 一、为什么一条 loss 曲线远远不够

训练是一个闭环：数据批次进入模型，前向产生 loss，反向产生梯度，优化器结合内部状态给出更新，参数变化又影响下一批数据的响应。与此同时，混合精度、分布式归约、编译器和硬件调度改变实际执行路径。

只观察训练 loss，至少会混淆四类问题：

1. **数据问题**：坏样本、mask/label shift、packing 比例变化；
2. **模型问题**：activation 饱和、归一化统计漂移、attention collapse；
3. **优化问题**：梯度、预条件器、裁剪或实际 update 异常；
4. **系统问题**：skipped step、rank 卡顿、OOM 重试、输入空转或 kernel 改变。

相同的 loss spike 可以由四条不同路径产生；相反，严重风险也可能在 loss 明显恶化前先出现在 activation、gradient 或 optimizer state 中。因此 telemetry 的目标不是“画更多曲线”，而是保留足以区分竞争解释的证据。

## 二、先统一五个时钟

设一次 optimizer update 由 $K_t$ 个 microbatch 累积而来，第 $t$ 次更新消费的有效 token 数为 $n_t$。常见时钟是：

| 时钟 | 记号 | 回答的问题 |
|---|---:|---|
| sample/token clock | $N_t=\sum_{s\le t}n_s$ | 学过多少真实、非 padding 数据？ |
| microstep clock | $m$ | 前反向执行了多少次？ |
| optimizer-step clock | $t$ | 参数实际更新了多少次？ |
| scheduler clock | $q_t$ | LR/WD/warmup 根据什么推进？ |
| wall-clock | $\tau$ | 花了多少真实时间、何时发生系统事件？ |

如果 gradient accumulation 从 4 改到 8，而横轴仍只写 `step`，两条曲线可能比较的是不同 token 预算。若 overflow 导致 scaler 跳过更新，microstep 增加而 optimizer step 不增加。正确记录至少是

$$
(\tau,m,t,N_t,q_t,\text{checkpoint id},\text{data cursor}).
\tag{1}
$$

> [!warning] “第 1000 步”不是完整坐标
> 必须说明它是 microstep、optimizer step、scheduler step 还是 evaluation step，并同时保存累计有效 token 与 wall-clock。

## 三、一条训练事件的六本账

把第 $t$ 次更新写成

$$
g_t=\frac{1}{K_t}\sum_{k=1}^{K_t}\nabla_\theta \ell(B_{t,k};\theta_t),
\qquad
u_t=U(g_t,s_t;h_t),
\qquad
\theta_{t+1}=\theta_t+\Delta_t,
\tag{2}
$$

其中 $s_t$ 是 optimizer state，$h_t$ 是 LR、decay、clipping、loss scale 等控制量，$\Delta_t$ 是**真正写回参数的位移**。由此建立六本账：

### 3.1 数据账

- dataset/version、shard、sample/token IDs、sampler cursor；
- sequence length、padding/mask 比例、label/class/domain 组成；
- decode/tokenize/augment 失败数与输入等待时间；
- batch loss 分布，而不只记录 batch mean。

### 3.2 目标与输出账

- train/eval loss 及各 component；
- numerator、denominator 与 reduction 规则；
- accuracy/perplexity 等派生 metric 的原始计数；
- logits/概率的范围、entropy、margin、saturation 与非有限比例。

### 3.3 梯度账

对参数组 $G$，至少记录

$$
\|g_G\|_2,
\quad
\operatorname{RMS}(g_G)=\frac{\|g_G\|_2}{\sqrt{|G|}},
\quad
g_{\max,G}=\max_i|g_i|,
\tag{3}
$$

再加 zero/nonfinite 比例、clipping 前后 norm、跨 microbatch/worker 方差。global norm 健康并不保证某层健康，故需保留 layer/parameter-group 分层。

### 3.4 更新与 optimizer-state 账

必须区分 raw gradient、moment/preconditioned direction、decay 和 realized update：

$$
\Delta_t
=\Delta_t^{\text{grad}}
+\Delta_t^{\text{decay}}
+\Delta_t^{\text{other}}.
\tag{4}
$$

记录 LR、moment RMS、second-moment RMS、epsilon-dominated 比例、trust ratio、clip fraction、loss scale、skipped step、update RMS 和 update-to-weight ratio。若只记 gradient norm，就看不到 Adam 分母塌缩或 decay 主导。

### 3.5 参数与激活账

参数记录 norm/RMS、最大值、零/非有限比例和低频谱探针；activation 记录分位数、RMS、mean/std、稀疏率、饱和率、norm/attention entropy 等结构化指标。必要时按 layer、token position、head、expert 或 domain 切片。

### 3.6 系统账

- step time 的 p50/p90/p99，input/compute/communication/idle 分解；
- device memory 的 current/peak/reserved，OOM、retry 与 checkpoint 时间；
- world size、rank、collective、kernel/backend、compile/cache 状态；
- GPU 利用率只是线索，critical path 需 trace 验证。

[[S-2026-PyTorch-Profiler]] 可采 operator 时间、memory 与 trace；它定位执行成本，不自动说明质量变化来自哪个机制。

## 四、统计量不是越多越好：要保留分布和尺度

对一组值 $x_1,\dots,x_n$，mean 与 RMS 分别回答偏置和能量：

$$
\bar x=\frac1n\sum_i x_i,
\qquad
\operatorname{RMS}(x)=\sqrt{\frac1n\sum_i x_i^2}.
\tag{5}
$$

若少数 outlier 很关键，还需 quantile、amax 和 exceedance rate。对非平稳训练，滑动窗口均值

$$
\hat \mu_t=(1-\beta)x_t+\beta\hat\mu_{t-1}
\tag{6}
$$

的有效记忆约为 $1/(1-\beta)$ 次观测，但若 logging 每 100 step 一次，其物理记忆就是约 $100/(1-\beta)$ step。必须连同采样率解释。

推荐分三级采集：

- **L0 每步廉价标量**：loss、LR、token、step time、global grad/update norm、loss scale/skip；
- **L1 低频分层摘要**：layer RMS/quantile、activation、optimizer state、memory；
- **L2 触发式重诊断**：完整 trace、tensor slice、anomaly detection、checkpoint replay。

这样既不让 telemetry 改写训练，又能在预警后放大观察。

## 五、给新手的最小 dashboard

一个可用的第一版只需四个面板，但每个面板有明确判别任务：

| 面板 | 最小曲线 | 首要问题 |
|---|---|---|
| 进展 | train/eval loss 对 token 与 wall time | 学习是否发生，成本如何？ |
| 优化 | grad RMS、update RMS、UWR、clip/skip rate | 梯度是否真正变成合理更新？ |
| 表征 | 关键 layer activation RMS/quantiles/entropy | 信号是否饱和、塌缩或漂移？ |
| 系统 | step time、input/comm tail、peak memory | 训练轨迹是否被执行事件改变？ |

再附 manifest：run/config/code/data/environment hash、seed hierarchy、precision/distribution policy。没有 manifest，曲线即使漂亮也难以回放。

## 六、从告警到诊断：阈值必须有参照系

告警可以写成绝对阈值、相对基线或变化点。例如：

$$
z_t=\frac{x_t-\operatorname{median}(x_{t-w:t-1})}
{1.4826\operatorname{MAD}(x_{t-w:t-1})+\varepsilon}.
\tag{7}
$$

但深度学习曲线非平稳，warmup、decay、curriculum 和 length change 都会合法改变分布。因此更稳妥的是：

1. 为不同 phase 建独立 baseline；
2. 同时看 level、slope、persistence 和跨指标先后顺序；
3. 告警只触发调查，不直接宣判根因；
4. 将 false positive/negative 也纳入 telemetry 设计。

## 七、三个不变量比一百条曲线更有价值

建议为训练 loop 写机器可验的不变量：

1. **计数守恒**：累计有效 token 等于各 rank/microbatch 的去重和；
2. **更新一致**：未 skipped 时 $\theta_{t+1}-\theta_t$ 与记录的 $\Delta_t$ 在容差内；
3. **有限性**：进入 optimizer 的梯度、state 与写回参数满足预设 finite policy；
4. **归约语义**：DDP average、loss reduction、accumulation 除数与 global batch 定义一致；
5. **恢复连续**：resume 后 data cursor、scheduler、optimizer、scaler 与 RNG 不发生未声明跳变。

这些不变量直接排除整类 bug；普通相关曲线往往只能提示“哪里不对劲”。

## 八、一个贯穿例子：loss 平滑，训练却已经坏了

假设训练 loss 在 20k—22k step 仍缓慢下降，但 validation 停滞。总账显示：

- activation RMS 在第 20,140 step 首先升高；
- grad RMS 仍稳定，因为 global clipping 每步触发；
- realized update RMS 明显下降，Adam second moment 持续抬升；
- step time 同时改变，因为 sequence-length curriculum 启动；
- domain mix 也在同一版本切换。

单看 loss 会说“继续训练”；单看 clip rate 会说“梯度爆炸”。真正结论只能是：存在表征尺度、预条件器与数据/长度切换的竞争解释，需要在固定数据和 schedule 下做反事实重放。Telemetry 给出了候选时间线，却尚未给出因果答案。

## 九、科学空间研读框：RMS 是坐标，不是健康证书

[[S-2025-Su-11267-Adam-Update-RMS]] 与 [[S-2025-Su-11404-AdamW-Weight-RMS-Dynamic]] 给出 update/weight RMS 的条件性估算。这些推导很适合提出 telemetry：

- 实测 RMS 是否随 LR、decay 和 optimizer clock 按预测变化？
- ratio-of-expectations、stationarity、weak correlation 在何处失效？
- aggregate RMS 是否隐藏 layer、rank 或 singular direction 的异常？

课程把理论估算当 baseline model；偏离模型是值得解释的信号，不自动等于训练故障。

## 十、图解：多时钟观测栈

带着一个问题读图：**一次 loss spike 出现时，如何沿数据—前向—反向—更新—系统时间线找到最早证据？**

![[00-知识库管理/_assets/figures/training-optimization/fig-training-telemetry-ledger-v1.svg|880]]

> [!figure] 图 TRN-65-01　训练 Telemetry 的时钟与六本账
> 来源：自绘机制图；profiler 边界依据 [[S-2026-PyTorch-Profiler]]，复现边界依据 [[S-2026-PyTorch-Reproducibility]]。

**怎样读图**：先用底部五个时钟对齐事件，再从廉价 L0 指标进入分层 L1，最后只在窄窗口启用 L2；纵向比较数据、loss、gradient、update、activation 与 system 的 first-change time。

**图没有证明什么**：指标先变化只是时间先后，不自动等于因果先行；采样率和聚合窗口也可能改变观测顺序。

## 十一、核心结论

训练可观测性的最小单位不是一条曲线，而是带有多时钟、对象层级、统计窗口和 manifest 的事件。Telemetry 的价值在于压缩竞争解释、保留重放入口和触发精细诊断；它不能代替随机化、干预和统计推断。
