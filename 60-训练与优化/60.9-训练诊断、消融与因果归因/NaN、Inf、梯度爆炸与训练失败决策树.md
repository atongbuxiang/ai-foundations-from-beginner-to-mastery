---
type: concept
status: verified
area: [training, debugging, numerical-stability, incident-response]
course_id: TRN-66
prerequisites: ["[[训练 Telemetry、损失梯度更新与激活总账]]", "[[浮点数与舍入误差]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]"]
related: ["[[Update-to-Weight Ratio、谱与尺度诊断]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2026-PyTorch-Autograd-Anomaly]]", "[[S-2026-PyTorch-Profiler]]", "[[S-2026-Google-SRE-Postmortem]]", "[[S-2023-Koloskova-Gradient-Clipping-Bias]]", "[[S-2025-Su-11371-低精度Attention舍入偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# NaN、Inf、梯度爆炸与训练失败决策树

> [!abstract] 本节目标
> 掌握“first bad event”原则：先冻结现场，再沿数据、前向、反向、更新和系统边界定位第一个违反合同的对象。你将学会区分症状、触发器、近因和根因，并用 checkpoint 二分与最小反事实验证修复。

## 一、NaN 往往是最后一声警报

`loss = NaN` 很少告诉你错误发生在哪里。可能的链条包括：

$$
\text{坏 token/label}
\to \text{非法算子输入}
\to \text{activation Inf}
\to \text{backward NaN}
\to \text{optimizer state NaN}
\to \text{parameter NaN}
\to \text{下一步 loss NaN}.
\tag{1}
$$

也可能全程没有非有限值：有限但巨大的 update 将参数推入坏区域，下一批才 overflow。因此要找的不是“第一个被看见的 NaN”，而是：

> **first bad event：相对于预先声明的数值、shape、语义或统计合同，第一个可复现的违约事件。**

它可以是非有限值，也可以是突然越界的 amax、错误 mask、一次未预期的 skipped update、错误归约因子或 rank 数据重复。

## 二、先停止污染：现场冻结六件套

发现异常时，不要立刻只改 LR 重跑。先保存：

1. 最后一个已知正常 checkpoint 与第一个异常 checkpoint；
2. 触发 batch 的 sample/token IDs、原始/处理后输入与 data cursor；
3. model、optimizer、scheduler、scaler、EMA 等全部 state；
4. Python/framework/device RNG state 与 distributed sampler state；
5. code/config/data/environment/kernel/backend hash；
6. 事件前后固定窗口的 telemetry 与 rank trace。

若隐私或体积不允许保存原始 batch，至少保存可重建引用、hash、shape、统计摘要与权限路径。没有现场，后续“修复成功”可能只是随机性让故障暂时消失。

## 三、第一层决策：故障在哪个阶段首次出现

令一次训练更新分成五道边界：

$$
B_t
\xrightarrow{\text{data}}
x_t
\xrightarrow{\text{forward}}
(a_t,\ell_t)
\xrightarrow{\text{backward}}
g_t
\xrightarrow{\text{optimizer}}
\Delta_t
\xrightarrow{\text{write}}
\theta_{t+1}.
\tag{2}
$$

在每道边界检查 `shape/dtype/device/finite/range/semantic invariant`：

| 首次违约位置 | 优先竞争解释 | 第一组检查 |
|---|---|---|
| 输入/目标 | decode、token、mask、label、length、augment | offending IDs、raw→processed diff、denominator |
| forward activation/loss | log/exp/div/sqrt、softmax、norm、overflow | module 输入输出、FP32 reference、amax/zero |
| backward | unstable derivative、custom op、loss scale、reduction | per-module grad、unscale 时序、anomaly traceback |
| optimizer/state | epsilon、moment、decay、clip、step counter | 分项 update、state finite、actual delta |
| distributed/system | collective mismatch、stale rank、retry、OOM | per-rank checksum、timeline、world/config hash |

先定位边界，再讨论根因；否则很容易在 optimizer 中修补源于数据的错误。

## 四、第二层决策：非有限，还是有限但危险

### 4.1 非有限路径

对每个关键 tensor 记录

$$
r_{nf}=\frac{\#\{i:\neg\operatorname{isfinite}(x_i)\}}{|x|},
\qquad
a_{max}=\max_i|x_i|.
\tag{3}
$$

如果输入有限、output 非有限，缩小到具体 module/op；如果 output 有限、gradient 非有限，则检查导数定义、saved tensor 和 backward kernel。[[S-2026-PyTorch-Autograd-Anomaly]] 的 `detect_anomaly(check_nan=True)` 能给 failing backward 对应的 forward traceback，但开销大，应在已缩小的窗口启用。

### 4.2 有限但危险路径

“梯度爆炸”应写成尺度相对于参照系增长，而不是只看一个大数：

$$
R_g(t)=\frac{\|g_t\|}{\operatorname{median}(\|g_{t-w:t-1}\|)+\varepsilon},
\quad
R_u(t)=\frac{\|\Delta_t\|}{\|\theta_t\|+\varepsilon}.
\tag{4}
$$

还需 layer/unit ratio 与 top singular/Hessian direction。global norm 平稳可能只是 clipping 把异常压平；clip fraction 从 1% 跳到 100% 才是更早信号。

## 五、Checkpoint 二分：在时间轴上找第一步

若故障在 step $b$ 被发现，且 checkpoint $a<b$ 正常，可以：

1. 从 $a$ 恢复并固定数据/RNG/环境；
2. 在中点 $m=\lfloor(a+b)/2\rfloor$ 保存和检查；
3. 若 $m$ 正常，令 $a=m$；否则令 $b=m$；
4. 重复到单 step 窗口，再对 module/op 做空间二分。

时间定位约需 $O(\log_2(b-a))$ 次区间检查，而逐步 dump 可能昂贵得多。前提是 replay 足够稳定；若不可逐比特复现，则用容差 invariant 和多次复现概率定位，不要伪造一个确定断点。

## 六、模块与张量级的空间定位

建议按以下顺序增加仪器：

1. module input/output 的 finite、amax、RMS；
2. backward gradient input/output；
3. 关键复合算子拆解前后的中间量；
4. 与 FP32 或简单 reference kernel 对照；
5. 最后才保存完整 tensor。

对 `logsumexp`、softmax、normalization、division、square root 等高风险算子，检查数学定义域和稳定实现。例如

$$
\log\sum_i e^{z_i}
=m+\log\sum_i e^{z_i-m},\qquad m=\max_i z_i
\tag{5}
$$

避免直接指数 overflow；但稳定公式也无法修复所有输入已经是 Inf 的情况。

## 七、低精度与 loss scaling 的专用分支

混合精度时需逐项确认：

- 哪些 tensor/算子为 FP16/BF16/FP32，accumulation dtype 是什么；
- scale 后 loss、scaled gradient、unscaled gradient 何时检查 finite；
- overflow 时 optimizer 与 scheduler 是否都跳过；
- master weight/state 是否已被污染；
- scale growth/backoff 是否与事件时间线一致。

“改成 FP32 后不崩”只支持数值路径相关，不说明具体是 input rounding、accumulation、reduction、state 还是 update 引起。[[S-2025-Su-11371-低精度Attention舍入偏差]] 提醒我们还要问：局部低精度误差是崩溃的因，还是 attention 已集中后才放大的果。

## 八、分布式训练的专用分支

单 rank 正常、多 rank 失败时检查：

- 每个 rank 的 batch count、loss numerator/denominator 与 gradient checksum；
- collective 调用序列、shape/dtype、process group 与 timeout；
- uneven input、drop-last、join、gradient accumulation 和 bucket ready order；
- 某 rank OOM/retry 后是否继续用了 stale state；
- restart 是否恢复相同 global checkpoint 与 data cursor。

只在 rank 0 检查 finite 会漏掉其他 rank 的 first bad tensor；All-Reduce 后 NaN 已扩散，来源 rank 丢失。

## 九、不要把“止血”误写成“根因修复”

常见止血措施包括降低 LR、增大 epsilon、加 clipping、切 FP32、跳过坏 batch。它们有三种可能作用：

1. 真正移除触发机制；
2. 只缩小症状，使根因仍存在；
3. 改变训练问题，牺牲质量换稳定。

因此修复需做最小反事实矩阵：

| 运行 | 原配置 | 候选修复 | 触发 batch | 期望判别 |
|---|---:|---:|---:|---|
| replay-A | ✓ | ✗ | ✓ | 故障复现 |
| replay-B | ✗ | ✓ | ✓ | first bad event 消失 |
| control-C | ✓ | ✗ | 对照 batch | 不故障 |
| quality-D | ✗ | ✓ | 正常流 | 质量/成本不越界 |

若 replay-A 不复现，就不能只凭 replay-B 成功宣称修复。

## 十、触发器、近因、促成条件和根因

一个严谨事故陈述可以是：

- **trigger**：某长度 32k、极低有效 label 数的 batch；
- **proximate mechanism**：FP16 reduction overflow，unscale 前出现 Inf；
- **contributing conditions**：loss denominator 未按有效 token 归一、缺少 per-rank finite 检查；
- **control gap/root cause**：训练合同没有覆盖极端 length/label 组合，测试与监控均未设 invariant。

根因不是“最后改了哪个参数”，也不应写成某个人“粗心”。[[S-2026-Google-SRE-Postmortem]] 的 blameless 结构强调系统学习，同时要求时间线和行动项可验证。

## 十一、训练事故包的最小字段

- 事故 ID、影响、开始/发现/缓解/恢复时间；
- first signal 与 first bad event，正常/异常边界；
- 完整 timeline 和每个推断的证据链接；
- trigger、mechanism、contributing factors、root/control gap；
- reproduction recipe 与最小 failing case；
- mitigation 与 permanent fix 的分离；
- 修复前后反事实结果、回归测试；
- owner、due date、验证条件与未解问题。

失败 run 不能从分母删除。它既影响方法的 failure probability，也可能揭示只在尾部发生的机制。

## 十二、图解：first-bad-event 决策树

带着一个问题读图：**loss 首次 NaN 后，怎样避免在错误层级上盲目改超参数？**

![[00-知识库管理/_assets/figures/training-optimization/fig-first-bad-event-tree-v1.svg|880]]

> [!figure] 图 TRN-66-01　训练失败的时间二分与阶段决策树
> 来源：自绘机制图；anomaly tracing 依据 [[S-2026-PyTorch-Autograd-Anomaly]]，事故结构依据 [[S-2026-Google-SRE-Postmortem]]。

**怎样读图**：先冻结现场并在 checkpoint 时间轴二分，再沿 data→forward→backward→optimizer→system 边界找首次违约；最后用 replay/control/quality 四格验证候选修复。

**图没有证明什么**：最早被采样到的异常仍可能晚于真正机制；重放不稳定时，单次成功或失败都不能构成充分证据。

## 十三、核心结论

高质量调试的顺序是：冻结现场、定义违约、定位 first bad event、构造竞争解释、做最小反事实、验证质量与成本、沉淀事故测试。NaN 是一个观测值，不是根因；“不再崩”是必要结果，也不是完整证明。
