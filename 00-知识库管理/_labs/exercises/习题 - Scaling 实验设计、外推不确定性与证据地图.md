---
type: exercise
status: verified
area: [training, scaling-laws, experimental-design]
topic: "[[Scaling 实验设计、外推不确定性与证据地图]]"
solution: "[[解答 - Scaling 实验设计、外推不确定性与证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Scaling 实验设计、外推不确定性与证据地图

> [!abstract] 训练目标
> 把 scaling 研究组织为预注册、尺度分块、失败留痕、函数族比较、区间外预测和决策后悔的完整证据流水线。

## A. 识别与复述

### TRN56-A01
一条可证伪 scaling claim 至少应包含哪些字段？为什么“更大通常更好”不合格？

### TRN56-A02
区分训练随机性、测量不确定性、参数估计不确定性与结构/函数族不确定性。

### TRN56-A03
什么是 failure denominator？为什么只分析成功运行会同时偏置性能、成本与稳定性结论？

## B. 手算与构造

### TRN56-B01
共有尺度 $N=(1,2,4,8,16,32,64,128)$。给出 calibration、validation、held-out-scale 三段切分，使最终测试真正位于区间外。

### TRN56-B02
计划 30 次运行，成功 24 次；成功运行平均 loss 2.0，失败按预注册惩罚 loss 5.0。计算 success-only 与 intention-to-run 平均 loss。

### TRN56-B03
策略 A 预测最优配置的实际 loss 为 1.90，同预算可行集合中的真实最优为 1.84。计算 decision regret；若基线策略 loss 为 2.00，A 消除了多少基线后悔？

## C. 推导与证明

### TRN56-C01
解释 hierarchical block bootstrap 如何依次重采样 scale cell、seed 与 checkpoint；为什么不能把所有 checkpoint 当 iid 样本？

### TRN56-C02
证明若随机拆分同一尺度的 checkpoint 到训练与测试集，测试误差不能估计跨尺度外推误差。

### TRN56-C03
给出 power law、offset power law 与 broken power law 的选择流程，包含 complexity penalty、validation 与 held-out evaluation；为什么最终测试不能反复用于调族？

## D. 边界、反例与纠错

### TRN56-D01
反驳：“有 1000 个 checkpoint，所以 scaling fit 的样本量是 1000。”

### TRN56-D02
反驳：“删除 divergence 运行只是数据清洗，不影响结论。”

### TRN56-D03
为什么单个 bootstrap 置信区间仍可能漏掉结构不确定性？举出两个同区间拟合、异区间外预测的函数族。

## E. AI 迁移

### TRN56-E01
写一份 scaling 实验预注册清单：至少覆盖 claim、grid、预算、调参、失败、拟合族、切分与停止规则。

### TRN56-E02
设计完整结果表，使读者能同时看到点估计、区间、失败率、外推误差、资源账本与决策后悔。

### TRN56-E03
按 E0–E5 证据等级，为“曲线内插良好”“未见规模外失效”“可指导十倍预算决策”分别选择合适措辞。

## 作答与复盘

先锁定 scale-level split 和 failure policy，再查看 [[解答 - Scaling 实验设计、外推不确定性与证据地图]]。
