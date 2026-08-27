---
type: solution
status: verified
area: [language-models, peft, qlora, memory]
topic: "[[QLoRA、量化基座与适配显存总账]]"
exercise: "[[习题 - QLoRA、量化基座与适配显存总账]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - QLoRA、量化基座与适配显存总账

## A. 识别与复述

### LM30-A01
Storage dtype 编码持久 base codes；compute dtype 是反量化后 matmul operand；accumulation dtype 是乘加/reduction 精度；optimizer dtype 是 LoRA moments/master state。四者可分别为 4-bit、bf16、fp32、fp32。

### LM30-A02
Quantized base codes/metadata 冻结，LoRA A/B 更新。前向把 base 反量化参与计算；backprop 需通过这些线性运算传播 activation gradients 到 adapters/早层，但不为 base codes 建 optimizer update。

### LM30-A03
NF4 是面向近似正态权重的非均匀 4-bit codebook；double quantization 再压缩 block scales/constants；paged optimizer 管理瞬时显存 spikes/迁移。它们分别处理量化误差、metadata bytes 和峰值 residency。

## B. 手算与构造

### LM30-B01
1B×4 bit =4B bits=0.5B bytes，按十进制约 0.5 GB。Metadata 0.1 byte/parameter 再加 0.1 GB，总 0.6 GB；尚不含未量化层、alignment、runtime。

### LM30-B02
10M bf16 weights=20MB；bf16 grads=20MB；两份 fp32 moments=$10M\times2\times4=80$MB；合计 120MB，即约 0.12GB 十进制，未含 master weights 或 allocator。

### LM30-B03
账面和 $.5+.1+.12+1.4+.5=2.62$GB。它是这些项同时驻留时的上界/例；不同 buffers 生命周期可能不重叠，reserved/fragmentation/driver 又可使实测 peak 更高，必须采样 profiler。

## C. 推导与证明

### LM30-C01
前向 $y=D(q,c)x+sBAx$。峰值账为 $M_q+M_{meta}+M_{adapter-param}+M_{grad}+M_{opt}+M_{act}+M_{temp/kernel}+M_{runtime}$，并为每项记录 dtype、shape、lifetime/residency。

### LM30-C02
STE 用于把不可微 quantizer 的梯度近似传给待更新的 full-precision/base weights。QLoRA 不更新 $q,c/W_0$；只需对输入/adapter 求常规导数，反量化权重在该步是常量，所以无 base-quantizer STE 需求。

### LM30-C03
Runtime adapter 算 $D(q,c)+sBA$；merge-requantize 算 $D(Q'(D(q,c)+sBA))$。量化 $Q'$ 是多对一舍入，一般 $D(Q'(W_*))\ne W_*$，除非所有元素恰落 codebook/scale 可精确表示。

## D. 边界、反例与纠错

### LM30-D01
只有 base codes 是 4-bit；scales、LoRA weights/grads、Adam moments、activations、dequant tiles、accumulators 可为 8/16/32-bit。总 peak 可能被 activation 而非 base 主导。

### LM30-D02
Paging 改变 optimizer state 在 device/host 的驻留与峰值，不删除 state；迁移/page faults 可增加延迟。是否更快依访问模式、内存压力、互连与 kernel，应分别报 OOM avoidance 和 throughput。

### LM30-D03
若 quantized base zero-shot 已比 fp base 低 5 点，只比较 fp LoRA 80 与 QLoRA 75，就可能说“QLoRA adaptation 差 5 点”；但差异或全部来自起点。需先报 fp base 与 quant base，再比较各自 adaptation gain。

## E. AI 迁移

### LM30-E01
四臂共享 data/template/eval：FP-base no tune、Q-base no tune、FP-base+LoRA、Q-base+LoRA；按 effective targets/FLOPs/search budget匹配，多 seed。分解 base quantization gap、LoRA gain、interaction，并测 pre/post merge。

### LM30-E02
固定 model revision、sequence/batch/packing/checkpointing/optimizer；写 quant format/group/dtypes/kernel/library；每硬件 warmup 后采 allocated/reserved/peak、tokens/s、wall time、power/OOM，注明 offload/paging 与通信，禁止跨设置直接比。

### LM30-E03
“单卡”缺 GPU 型号/容量、base storage、batch、sequence、gradient accumulation、checkpointing、offload、kernel 和 peak 定义；不能复算显存或吞吐。只能接受为存在性陈述，不能外推普通单卡条件。

## 无提示重做

- [ ] 列出 QLoRA 全部 dtype 与峰值内存项。
- [ ] 解释 runtime adapter 与 merge-requantize 的函数差。

