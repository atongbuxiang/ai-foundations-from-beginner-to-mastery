---
type: exercise
status: verified
area: [training, distributed-systems, model-parallelism]
topic: "[[Tensor、Pipeline、Sequence 与 Expert Parallel]]"
solution: "[[解答 - Tensor、Pipeline、Sequence 与 Expert Parallel]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Tensor、Pipeline、Sequence 与 Expert Parallel

> [!abstract] 训练目标
> 能由 tensor shape 推导 TP/SP/CP/EP 通信，由流水线时间表计算 bubble，并把 hybrid parallelism 写成有坐标、group 与 collective 的 process mesh。

## A. 识别与复述

### TRN62-A01
分别说明 data、tensor、pipeline、sequence/context 与 expert parallel 切分什么对象，并各列一个典型 collective。

### TRN62-A02
区分 sequence parallel 与 context parallel：它们都切 token 维时，局部算子与 attention 的跨块依赖有什么差别？

### TRN62-A03
为什么 parallel degree 不能只写一个乘积？定义 process-mesh 坐标、communication group 与 replicated axis。

## B. 手算与构造

### TRN62-B01
线性层 $Y=XW$，$X\in\mathbb R^{B\times H}$、$W\in\mathbb R^{H\times K}$，TP=4。分别给出按 $K$ 列切 $W$ 与按 $H$ 行切 $W$ 时每 rank 的 weight/output shape 和所需 collective。

### TRN62-B02
GPipe 有 $P=8$ 个均衡 stage、$M=32$ 个 micro-batch，忽略 backward 差异。用效率 $M/(M+P-1)$ 计算理想 pipeline 利用率与 bubble fraction。

### TRN62-B03
一批 4096 tokens 被路由到 8 个 experts，capacity factor 1.25。按均匀期望求每 expert capacity；若一个 expert 收到 900 tokens，会有多少超出容量？

## C. 推导与证明

### TRN62-C01
推导 column-parallel linear 与 row-parallel linear 的代数：说明前者为什么自然产生切分输出，后者为什么需要对部分输出求和。

### TRN62-C02
从 pipeline 的 fill、steady、drain 时间槽推导 $M/(M+P-1)$；说明 $M$ 增大为何降低 bubble 却可能增加 activation/调度压力。

### TRN62-C03
对 MoE 写出 token dispatch→expert compute→combine 的 shape 流，并说明 All-to-All payload 与负载不均如何进入 step critical path。

## D. 边界、反例与纠错

### TRN62-D01
反驳：“TP=8、PP=8、DP=8，所以只要有 512 GPU 就一定能运行。”列出 divisibility、layer placement、group 与 capacity 缺口。

### TRN62-D02
反驳：“micro-batch 越多，pipeline 总是越快。”指出 kernel efficiency、activation、通信、调度和优化语义边界。

### TRN62-D03
反驳：“MoE 每 token 只激活少量 expert，所以通信与 dense model 一样规则。”构造热点路由与 straggler。

## E. AI 迁移

### TRN62-E01
为一个 DP=8、TP=4、PP=2、EP=2 的 job 写 mesh manifest：总设备数的两种可能解释、group 定义、被切 shape 与 collective。

### TRN62-E02
给定长上下文 Transformer，设计 TP、sequence/context parallel 两个候选并比较 activation、attention 通信、kernel shape 和复现风险。

### TRN62-E03
画一个每层 communication contract 表，至少含 input/output shape、local operator、collective、bytes、ready time、group 与是否在关键路径。

## 作答与复盘

每题先写 tensor shape 再说并行名称，之后查看 [[解答 - Tensor、Pipeline、Sequence 与 Expert Parallel]]。若没有写 collective 和 group，方案仍不可执行。
