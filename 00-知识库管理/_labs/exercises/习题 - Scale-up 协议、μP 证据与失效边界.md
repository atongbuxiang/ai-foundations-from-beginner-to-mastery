---
type: exercise
status: verified
area: [training, optimization, mup, scale-up, experimentation]
topic: "[[Scale-up 协议、μP 证据与失效边界]]"
solution: "[[解答 - Scale-up 协议、μP 证据与失效边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Scale-up 协议、μP 证据与失效边界

> [!abstract] 训练目标
> 能把“实现正确、机制稳定、超参数可迁移、目标规模有效、预算诚实”拆成独立证据；能设计不会把 target 信息偷偷带回 proxy 选择的 scale-up 协议。

## A. 识别与复述

### TRN48-A01
复述 Shape、Coordinate、Spectral/Depth、Training Safety、Transfer 五类 failure gate。为什么通过其中一类不能代替其他四类？

### TRN48-A02
解释 E0—E5 证据等级各自允许支持什么措辞。为什么 E2 的水平 coord plot 不能直接支持“超参数已在目标模型零样本迁移成功”？

### TRN48-A03
解释
$$
C_{total}=C_{train}+C_{tune}+C_{select}+C_{eval}+C_{confirm}
$$
五个账户。target health check、rescue run 与为选 checkpoint 多跑的验证分别记在哪里？

## B. 手算与构造

### TRN48-B01
target 上三个候选学习率的验证 loss 为
$$
F_n(10^{-4})=2.10,\quad
F_n(3\!\times\!10^{-4})=1.94,\quad
F_n(10^{-3})=2.02.
$$
proxy 选择 $10^{-4}$。计算 transfer regret；当 $\tau=0.10$ 时写出 near-optimal set，并判断 proxy 选择是否在其中。

### TRN48-B02
某配置发起 20 个 seeds：12 个完成，其中 9 个达到指标；3 个 NaN，2 个 OOM，2 个 timeout，1 个被人工中止。分别计算“只在完成 run 中的成功率”和“原配置分母上的成功率”。哪一个适合训练安全结论？

### TRN48-B03
telescoping ladder 的四级搜索成本分别为 40、24、12、4 GPU-hours，target confirm 另需 8 GPU-hours。计算 $C_{tune}^{tel}$ 与该流程至少暴露的 tuning+confirm 成本。为什么不能只报告最后一级 4 GPU-hours？

## C. 推导与证明

### TRN48-C01
证明或反驳：若 optimum drift 很大，则 transfer regret 必然很大；若 transfer regret 很小，则两个 near-optimal set 必然有交集。明确超参数距离、$\tau$ 与是否使用同一 proxy 选择的条件。

### TRN48-C02
设计一个最小 factorial 子实验，区分 width、depth 与 attention head path 对 coord/spectral stability 的主效应和交互。写出因子、levels、重复单位、固定项与要估计的交互。

### TRN48-C03
把 reverse μTransfer 写成一个诊断决策树：target 事故能在较小模型复现与不能复现时，各自优先检查什么？为什么两个分支都不能构成单独的因果证明？

## D. 边界、反例与纠错

### TRN48-D01
构造一个 target loss 很好、但不能据此声称 μP 正确的实验。至少指出两个替代解释。

### TRN48-D02
团队在 target 上扫了 20 个学习率，再报告其中最佳点，并称“μTransfer 零样本成功”。问题在哪里？如何重新命名结论并诚实核算成本？

### TRN48-D03
构造一个 activation RMS 与 update RMS 跨 width 都近似水平、但 spectral gate 失败的例子。应增加哪些遥测？

## E. AI 迁移

### TRN48-E01
写一个可复现 scale-up report 的最小目录与 manifest：覆盖模型、参数化、数据时钟、搜索选择、失败分母、预算、软件环境、遥测和原始结果。

### TRN48-E02
target 在 step 1 readout 爆炸、attention entropy 正常、hidden activation RMS 正常。写出“观察—首要假说—区分实验—停止门—允许结论”的诊断表。

### TRN48-E03
把“μP 普遍解决了大模型调参”改写为三个证据边界逐步更强、但都可由数据检验的 claim：分别对应 E2、E3、E4。

## 作答与复盘

查看 [[解答 - Scale-up 协议、μP 证据与失效边界]] 前，为每道题写出“证据支持什么”和“证据尚未支持什么”两栏。
