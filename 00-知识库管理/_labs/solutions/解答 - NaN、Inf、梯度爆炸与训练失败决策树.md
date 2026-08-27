---
type: solution
status: verified
area: [training, debugging, numerical-stability]
topic: "[[NaN、Inf、梯度爆炸与训练失败决策树]]"
exercise: "[[习题 - NaN、Inf、梯度爆炸与训练失败决策树]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - NaN、Inf、梯度爆炸与训练失败决策树

## A. 识别与复述

### TRN66-A01
Symptom 是被观察到的失败；first bad event 是相对合同最早可复现违约；trigger 是启动事故的具体事件；proximate mechanism 是直接产生症状的局部机制；contributing condition 放大或允许事故；control gap 是测试、监控、设计或恢复合同未阻止它的系统缺口。它们可重合但不应默认相同。

### TRN66-A02
数据边界查 ID/shape/mask/target；前向查 activation、算子定义域与 loss；反向查 grad、scale/unscale 与 custom derivative；optimizer 查 state、step、decay、clip 和 actual delta；系统查 rank/collective/restart/backend。每道都查 shape/dtype/device/finite/range/semantic invariant。

### TRN66-A03
最后正常与首异常 checkpoints；触发 batch/data cursor；model/optimizer/scheduler/scaler/EMA state；全部 RNG/sampler state；code/config/data/env/backend hashes；异常前后 telemetry 与 per-rank trace。

## B. 手算与构造

### TRN66-B01
区间长度 512=$2^9$，理想二分至多 9 次判定定位到相邻 step。实际还需验证端点和 replay 稳定性；不可复现时不能声称确定边界。

### TRN66-B02
取 $m=1000$：$1000+\log(1+e^{-1})\approx1000+0.3133=1000.3133$。稳定重写避免直接形成 $e^{1000}$，但若输入已是 Inf 仍不能修复。

### TRN66-B03
$z=(11-4)/(1.4826\times0.5)\approx7/0.7413\approx9.44$。它是相对历史的强异常线索，不是根因判决。

## C. 推导与证明

### TRN66-C01
若 rank 3 先产生 NaN，归约后所有 rank 都是 NaN，来源信息被扩散。每 rank 先计算 finite flag、first tensor/op 和 checksum，All-Reduce `min(all_finite)` 作一致跳步；只有异常 rank 保存重诊断 artifact，同时所有 rank 以同一控制流跳过。

### TRN66-C02
global clipping 输出 $g'=g\min(1,c/\|g\|)$，当 $\|g\|>c$ 时 $\|g'\|=c$，无论原 norm 是 $2c$ 还是 $10^6c$。必须记录 pre/post norm、scale factor、clip fraction、layer/unit pre-clip 分布和触发时钟。

### TRN66-C03
切 FP32 同时改变 multiply、accumulate、reduction、kernel、scale/skip 甚至性能/数据顺序；观察只支持这个 bundle 与失败相关。需单独操纵 Attention rounding/accumulation/scale并检查局部误差→集中→gradient→loss 的中介顺序及 negative controls。

## D. 边界、反例与纠错

### TRN66-D01
step $t$ 的有限 update 将 weight 从 1 推到 $10^{20}$，本步所有量仍 finite；step $t+1$ 的 exp overflow 才产生 Inf/NaN。第一个 NaN 是后果，first bad event 可定义为 UWR/amax 越过合同。

### TRN66-D02
降低 LR 可能只是让坏 label 的影响不再立即 overflow；也可能抵消错误 reduction 因子或过小 optimizer epsilon；还可能改变 checkpoint/data timing，使触发 batch 未出现。需固定现场重放和竞争修复。

### TRN66-D03
success 同时受方法和 seed/硬件难度影响，条件化 success 打开 $A\to C\leftarrow U\to Y$ 路径。应以 launched run 为分母，联合报告 failure，并对 time-to-quality 处理删失。

## E. AI 迁移

### TRN66-E01
先冻结现场并确认 all-rank consensus；二分 checkpoint 找 step；依次检查输入、forward、backward scaled/unscaled gradient、optimizer state/actual delta、collective；用低开销 hooks 缩 module 后才启用 anomaly；与 FP32/reference 对照；构造最小候选干预并做四格验证。

### TRN66-E02
A：原 epsilon+触发 batch，必须复现 first bad；B：仅增 epsilon+同 checkpoint/batch/RNG，first bad 消失；C：原 epsilon+matched control batch，不失败；D：新 epsilon 在正常流和多 seeds 下质量、速度、update 分布不过界。若 A 不复现，B 的成功不能确认修复。

### TRN66-E03
字段含 ID/impact/detection/timeline、正常—异常边界、trigger/mechanism/contributors/control gap、artifact/replay、mitigation、permanent fix、反事实、owner/due/verification、unresolved risks。Mitigation 如临时切 FP32/降 LR；permanent fix 如修正归约合同、添加 invariant 和回归测试。
