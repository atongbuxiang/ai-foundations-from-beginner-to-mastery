---
type: exercise
status: verified
area: [training, optimization, generalization]
topic: "[[Critical Batch、隐式偏置与 SGD 证据地图]]"
solution: "[[解答 - Critical Batch、隐式偏置与 SGD 证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Critical Batch、隐式偏置与 SGD 证据地图

## A. 识别与复述

### TRN08-A01
区分 step、sample/token、compute 和 wall-clock efficiency。

### TRN08-A02
解释 critical batch 是收益递减尺度而非稳定硬上限。

### TRN08-A03
陈述 separable linear logistic regression 的 max-margin implicit-bias 结论及至少五项条件。

## B. 手算与构造

### TRN08-B01
$B_{noise}=256$。用经验模型计算 $B=64,256,1024$ 时 $S/S_{min}$ 与 $E/E_{min}$。

### TRN08-B02
数据集 $N=10^6$、epochs=10，比较 $B=1000$ 与 $10000$ 的 optimizer steps；说明固定 epoch 造成的混杂。

### TRN08-B03
构造 ReLU 两层网络的正尺度重参数化，使函数不变但参数 Hessian/sharpness 改变。

## C. 推导与证明

### TRN08-C01
由 $S/S_{min}=1+B_n/B$ 和 $E=BS$ 推出 $E/E_{min}=1+B/B_n$（确定 $E_{min}$）。

### TRN08-C02
证明两条归一化开销的 excess product 为 1，并解释 $B=B_n$ 的交点。

### TRN08-C03
把“小 batch→noise→flat→generalize”拆成三条可证伪假设，为每条指定最低证据类型。

## D. 边界、反例与纠错

### TRN08-D01
用 Dinh 等的重参数化思想反驳 raw parameter sharpness 的 invariance。

### TRN08-D02
反驳：“large-batch gap 证明 batch noise 是唯一原因。”列出 update count、BN、schedule、调参预算等混杂。

### TRN08-D03
说明为什么一个 task 的 $B_{critical}$ 不能直接迁移到另一模型/训练阶段。

## E. AI 迁移

### TRN08-E01
设计四臂实验隔离 optimizer batch、update count 与 BN statistics。

### TRN08-E02
给出大 batch 论文的 compute-matched 结果表字段，至少含 steps、tokens、FLOPs、wall time、metric 与多 seed interval。

### TRN08-E03
把“我们的模型处在 edge of stability，因此泛化好”改写为可检验、不过度因果化的研究假设。

## 作答与复盘

完成独立尝试后打开 [[解答 - Critical Batch、隐式偏置与 SGD 证据地图]]。
