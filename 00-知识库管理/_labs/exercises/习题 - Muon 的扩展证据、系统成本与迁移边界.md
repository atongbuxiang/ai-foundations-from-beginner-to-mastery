---
type: exercise
status: verified
area: [training, optimization, muon, systems, reproducibility]
topic: "[[Muon 的扩展证据、系统成本与迁移边界]]"
solution: "[[解答 - Muon 的扩展证据、系统成本与迁移边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Muon 的扩展证据、系统成本与迁移边界

> [!abstract] 训练目标
> 能把数学身份、算法原型、大规模主证据、框架产品化与跨组织复现分级；用多成本分母设计公平 benchmark，并建立可回滚的 AdamW→Muon 迁移门。

## A. 识别与复述

### TRN32-A01
给出 L0—L4 Muon 证据阶梯；每一级能支持什么声明，不能支持什么声明？

### TRN32-A02
区分 quality-vs-tokens、model FLOPs、optimizer-inclusive FLOPs、wall-clock、energy 与 dollar cost。

### TRN32-A03
列出 AdamW→Muon 迁移的三类核心不兼容：state、learning-rate meaning 与 parameter ownership，并各给一个失败例。

## B. 手算与构造

### TRN32-B01
baseline 每步 1.00 s，需要 100k steps 达标；Muon 每步因 NS 增至 1.08 s，但只需 80k steps。计算 wall-clock speedup、step efficiency improvement 与 optimizer overhead，说明三个百分比为何不能混写。

### TRN32-B02
某模型有 8B 个 Muon 参数、4B 个 AdamW fallback 参数，所有 state 用 FP32，参数本身用 BF16。假设 Muon 一个 FP32 momentum，AdamW 两个 FP32 moments，不计分片与临时量，计算 optimizer persistent state bytes；再说明真实 peak 还缺什么。

### TRN32-B03
五个 seeds 的 target-loss 时间为 AdamW $[100,102,98,101,99]$ 小时，Muon $[82,84,80,150,81]$ 小时。比较 mean、median、failure-tail 解释；为什么只报 best/median 会隐藏风险？

## C. 推导与证明

### TRN32-C01
给出一个因子分解：
$$
\frac{T_{base}}{T_{new}}
=\frac{N_{base}}{N_{new}}
\cdot\frac{t_{step,base}}{t_{step,new}},
$$
其中 $N$ 为达标 steps、$t_{step}$ 为 step time。解释它如何把 optimization efficiency 与 systems efficiency 分账。

### TRN32-C02
证明仅凭框架收录不能构成跨任务效果证明：用“软件可用性命题”与“经验风险差异命题”的逻辑对象不同来表述。

### TRN32-C03
设计一个同调参预算比较：给定总搜索 compute $C$，说明如何为 AdamW 与 Muon 分配 trials、early stopping 和 final confirmation，避免 winner's curse。

## D. 边界、反例与纠错

### TRN32-D01
把“Moonlight 证明 Muon 训练任何 LLM 都快两倍”改写为准确、不越界的证据陈述。

### TRN32-D02
反驳“tokens-to-quality 更优就必然 wall-clock 更优”。给出 optimizer kernel 或 communication 足够慢的数值反例。

### TRN32-D03
反驳“切换 optimizer 时把 Adam first moment 复制给 Muon buffer 就是无缝迁移”。指出 scale、second moment、group、clock 与 transient 问题。

## E. AI 迁移

### TRN32-E01
写一份三阶段迁移计划：offline replay、controlled small run、shadow-scale。每阶段给出输入、指标、gate 与 rollback artifact。

### TRN32-E02
设计多横轴实验报告模板，要求同时容纳成功/失败 runs、trial search cost、P95 step time、peak memory、network bytes 与 checkpoint reliability。

### TRN32-E03
审计一个 2026 Muon 新变体。写出从来源日期、数学不变量、公开代码、数值 residual、系统成本到跨任务复现的分层判定表。

## 作答与复盘

每题记录 independent / hinted / copied / blocked / careless。任何“更快”必须同时写 quality target、分母与失败运行；之后打开 [[解答 - Muon 的扩展证据、系统成本与迁移边界]]。
