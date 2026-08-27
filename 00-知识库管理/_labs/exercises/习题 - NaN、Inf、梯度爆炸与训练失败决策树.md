---
type: exercise
status: verified
area: [training, debugging, numerical-stability]
topic: "[[NaN、Inf、梯度爆炸与训练失败决策树]]"
solution: "[[解答 - NaN、Inf、梯度爆炸与训练失败决策树]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - NaN、Inf、梯度爆炸与训练失败决策树

## A. 识别与复述

### TRN66-A01
定义 symptom、first bad event、trigger、proximate mechanism、contributing condition 与 control gap。

### TRN66-A02
写出 data→forward→backward→optimizer→system 五道检查边界。

### TRN66-A03
发现 NaN 后现场冻结六件套是什么？

## B. 手算与构造

### TRN66-B01
正常 checkpoint 在 step 12000，NaN 在 12512。逐步查需至多 512 次；理想确定重放的二分至多需要多少次区间判定？

### TRN66-B02
直接计算 $\log(e^{1000}+e^{999})$ 会 overflow。用 log-sum-exp 重写并给出近似值。

### TRN66-B03
历史 grad norm 中位数为 4，MAD 为 0.5，本步为 11。按 robust z-score 分母 $1.4826\,MAD$ 计算异常分数。

## C. 推导与证明

### TRN66-C01
说明 All-Reduce 后才检查 NaN 为什么可能丢失来源 rank；设计 per-rank→global consensus 检查。

### TRN66-C02
证明 global clipping 可让记录的 post-clip norm 恒定，却掩盖 pre-clip explosion；写出应补的 telemetry。

### TRN66-C03
解释“FP32 不崩、FP16 崩”只识别 precision bundle 相关，不能单独证明 Attention 舍入是根因。

## D. 边界、反例与纠错

### TRN66-D01
反驳：“第一个 NaN tensor 就是根因。”构造更早的有限但异常 update。

### TRN66-D02
反驳：“降低 LR 后不崩，所以 LR 过大就是根因。”给出至少两种替代解释。

### TRN66-D03
反驳：“删除失败 seed 后比较成功 runs 更公平。”说明 collider/survivor bias。

## E. AI 迁移

### TRN66-E01
为 mixed-precision DDP 的偶发 NaN 写一步一步的决策树。

### TRN66-E02
设计 replay-A、replay-B、control-C、quality-D 四格验证一个“增大 epsilon”的候选修复。

### TRN66-E03
写一个训练事故记录的最小字段，并区分 mitigation 与 permanent fix。
