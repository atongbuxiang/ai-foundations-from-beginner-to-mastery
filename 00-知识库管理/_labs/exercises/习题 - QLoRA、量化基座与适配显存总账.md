---
type: exercise
status: verified
area: [language-models, peft, qlora, memory]
topic: "[[QLoRA、量化基座与适配显存总账]]"
solution: "[[解答 - QLoRA、量化基座与适配显存总账]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - QLoRA、量化基座与适配显存总账

## A. 识别与复述

### LM30-A01
区分 storage、compute、accumulation 与 optimizer dtype。

### LM30-A02
QLoRA 中哪些对象冻结，梯度又经过哪里？

### LM30-A03
NF4、double quantization 与 paged optimizer 各解决什么？

## B. 手算与构造

### LM30-B01
1B 参数理想 4-bit codes 为多少 GB；metadata 0.1 byte/param 后多少？

### LM30-B02
10M LoRA 参数 bf16、bf16 grads、两份 fp32 Adam moments，算合计 bytes。

### LM30-B03
给 codes=.5GB、meta=.1、adapter states=.12、activations=1.4、temp=.5，算账面和并说明 peak 边界。

## C. 推导与证明

### LM30-C01
写 QLoRA 前向与完整峰值内存分项。

### LM30-C02
说明 frozen 4-bit base 为何不需要通过量化器更新的 STE。

### LM30-C03
说明 merge→requantize 为何一般不与 runtime adapter 精确等价。

## D. 边界、反例与纠错

### LM30-D01
反驳“4-bit training 表示所有训练状态都是 4-bit”。

### LM30-D02
反驳“paged optimizer 让 optimizer state 消失并必然更快”。

### LM30-D03
构造 base quantization 退化被误归因 LoRA 的比较。

## E. AI 迁移

### LM30-E01
设计 fp base/quant base/fp LoRA/QLoRA 四臂消融。

### LM30-E02
写跨硬件显存/吞吐比较合同。

### LM30-E03
审计“65B 单卡训练”但无 sequence/batch/checkpointing/kernel 的主张。

独立完成后查看[[解答 - QLoRA、量化基座与适配显存总账]]。

