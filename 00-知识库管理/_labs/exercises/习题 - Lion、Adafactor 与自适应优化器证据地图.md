---
type: exercise
status: verified
area: [training, optimization, evidence]
topic: "[[Lion、Adafactor 与自适应优化器证据地图]]"
solution: "[[解答 - Lion、Adafactor 与自适应优化器证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Lion、Adafactor 与自适应优化器证据地图

> [!abstract] 训练目标
> 从状态、更新和资源合同理解 Lion 与 Adafactor；能计算状态量、检验因子重建，并用四道证据门审计“更好”的声明。

## A. 识别与复述

### TRN16-A01
写出一种标准 Lion 更新的两次线性组合、sign update 与持久状态；两个 $\beta$ 各作用在哪里？

### TRN16-A02
Adafactor 对矩阵二阶矩保存哪些因子？相对 Adam 的状态复杂度从什么量级降到什么量级？

### TRN16-A03
列出算法门、资源门、调参门和统计门各回答的问题。

## B. 手算与构造

### TRN16-B01
Lion 一维取 $m_0=0,g_1=2,\beta_1=0.9,\beta_2=0.99,\eta=0.1$，无 decay。按“先用 $\beta_1$ 组合取 sign，再用 $\beta_2$ 更新 momentum”的合同计算一步。

### TRN16-B02
一个 $4096\times4096$ 矩阵有多少元素？Adam 两份矩状态与 Adafactor 行列二阶状态分别需多少 FP32 bytes，给出理想比值。

### TRN16-B03
矩阵平方梯度
$$A=\begin{pmatrix}1&3\\2&6\end{pmatrix}.$$
取行和 $r$、列和 $c$，用 $\hat A=rc^\top/\sum r$ 重建并检验是否精确。

## C. 推导与证明

### TRN16-C01
证明若非负矩阵恰为 rank-one $A=ab^\top$，则行列边际重建 $rc^\top/\sum r$ 恢复 $A$。

### TRN16-C02
对一般非负矩阵，证明上述重建保持行和与列和；为什么这仍不保证元素级准确？

### TRN16-C03
推导矩阵参数 $n\times m$ 时 Adam 二阶状态与 Adafactor factor state 的元素数比，并讨论 $n=m=d$ 的渐近结果。

## D. 边界、反例与纠错

### TRN16-D01
给出一个 $2\times2$ 非负矩阵，其行列边际重建与原矩阵明显不同。

### TRN16-D02
反驳：“Lion 只存一份状态，所以训练显存一定减半。”

### TRN16-D03
为什么同一训练 loss 下比较 optimizer wall time 仍可能不公平？

## E. AI 迁移

### TRN16-E01
为 AdamW、Lion、Adafactor 的大模型对比设计最小报告表，至少含质量、状态 bytes、峰值显存、吞吐、搜索预算和 seed。

### TRN16-E02
一个新优化器论文只报告“相同默认 LR 下更好”。用四道证据门给出拒收理由与补充实验。

### TRN16-E03
模型含矩阵、向量、稀疏 embedding 和共享参数。如何建立逐参数 optimizer-state 清单，避免用一个 $O(P)$ 口号掩盖实际内存？

## 作答与复盘

先重建 state transition 和 byte ledger，再评价算法。独立完成后打开 [[解答 - Lion、Adafactor 与自适应优化器证据地图]]。
