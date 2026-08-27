---
type: exercise
status: verified
area: [training, optimization, mup, mutransfer]
topic: "[[μTransfer、Base Shape 与超参数零样本迁移]]"
solution: "[[解答 - μTransfer、Base Shape 与超参数零样本迁移]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - μTransfer、Base Shape 与超参数零样本迁移

> [!abstract] 训练目标
> 能设计 base/delta/target shape oracle，区分严格 zero-shot、target confirmation 与 telescoping，并用整条目标曲线而非单个最佳点讨论迁移。

## A. 识别与复述

### TRN45-A01
区分 base model、delta model、proxy model 与 target model 的角色。哪些模型必须训练，哪些只提供 shape？

### TRN45-A02
给出“zero-shot hyperparameter transfer”的严格定义，并列出四件它不表示的事。

### TRN45-A03
将候选超参数分为参数化/优化相关、regularization、可实验跨越但有 caveat 的尺度轴；每类给三例。

## B. 手算与构造

### TRN45-B01
某参数 base shape 为 $(256,1024)$，delta 为 $(512,2048)$，target 为 $(1536,4096)$。标记两个维度 finite/infinite，并计算相对 base multiplier。若 delta 第二维仍为 1024，会造成什么误判？

### TRN45-B02
Transformer base 为 $(d,h,d_h,d_{ff})=(256,4,64,1024)$。设计两套 delta：A 固定 $d_h$ 增 head，B 固定 head 墍 $d_h$。分别写形状并说明 oracle 得到的 scale path。

### TRN45-B03
目标 HP 网格 $h\in\{1,2,4\}$，proxy loss 为 $(1.1,0.8,0.9)$，target loss 为 $(1.0,0.82,0.78)$。求 proxy/target argmin、optimum drift（用 $\log_2h$ 距离）与 transfer regret。

## C. 推导与证明

### TRN45-C01
证明：若 $F_n$ 在紧致 $\mathcal H$ 上一致收敛到 $F_\infty$，且 $F_\infty$ 有唯一 separated minimizer $h^*$，则任意 exact minimizer $h_n^*$ 收敛到 $h^*$。

### TRN45-C02
构造 pointwise $F_n\to F$、但 minimizer 不收敛到 $F$ minimizer 的“移动窄谷”例子，说明 uniform convergence 为什么关键。

### TRN45-C03
定义 near-optimal set 与 transfer regret。证明即使 argmin grid point 改变，只要 proxy 选择仍在 target 的 $\tau$-near-optimal set，target regret 就不超过 $\tau$。

## D. 边界、反例与纠错

### TRN45-D01
反驳：“base 越小越好，因为调参越便宜。”给出至少四种极小 proxy 导致 HP 曲线失真的机制。

### TRN45-D02
某团队 target 失败后连续试了 8 个 LR，最后称“zero-shot μTransfer 成功”。指出方法命名与预算报告应怎样纠正。

### TRN45-D03
为什么 dropout/weight decay 不应由 width-μP 自动宣告迁移？构造 train loss 迁移、validation optimum 却漂移的场景。

## E. AI 迁移

### TRN45-E01
写一份八步 μTransfer runbook，必须含 family lock、shape oracle、coord check、proxy ladder、HP search、target confirm 与预算。

### TRN45-E02
设计 scheduler 与 checkpoint-resume 的实现测试，防止 refined group LR 被绝对覆盖或 infshape metadata 丢失。

### TRN45-E03
给一次从 40M proxy 到 4B target 的结论写证据边界；若中间增加 200M/1B 邻域搜索，应怎样改名和计账？

## 作答与复盘

先完成 B03 与 C01，再查看 [[解答 - μTransfer、Base Shape 与超参数零样本迁移]]。复盘时把每次使用 target information 的位置圈出。
