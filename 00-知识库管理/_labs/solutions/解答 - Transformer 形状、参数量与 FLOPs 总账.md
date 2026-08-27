---
type: solution
status: draft
area: [architecture, transformer, shapes, parameters, compute]
topic: "[[Transformer 形状、参数量与 FLOPs 总账]]"
exercise: "[[习题 - Transformer 形状、参数量与 FLOPs 总账]]"
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Transformer 形状、参数量与 FLOPs 总账

## A. 识别与复述

### ARCH-COST-A01
$B$ batch，$T$ 长度，$d$ residual/model width，$h$ query heads，$d_h$ 每头宽，$d_{ff}$ FFN hidden width，$L$ 层数，$V$ vocabulary。标准 dense MHA常取 $hd_h=d$；GQA/MQA 的 KV heads另设。

### ARCH-COST-A02
参数量是可学习标量数；MAC/FLOP是一次执行的算术工作；activation memory是前向/反向中间张量；KV cache是自回归跨步持久状态；wall-clock是硬件、kernel、带宽、并行和shape共同产生的实测时间。它们量纲不同。

### ARCH-COST-A03
训练并行处理全序列并保存反向激活；prefill一次处理已知prompt并建立cache；decode每步只算新token但读增长的cache。相同模型在三阶段的batch、算术强度、memory traffic和latency目标都不同，不能用一条平均数替代。

## B. 手算与建模

### ARCH-COST-B01
$d^2=589{,}824$。MHA为
$$
4d^2=2{,}359{,}296.
$$
普通FFN为
$$
2dd_{ff}=2\cdot768\cdot3072=4{,}718{,}592.
$$
标准block合计 $7{,}077{,}888$ 主权重，未计bias/norm。

### ARCH-COST-B02
投影：
$$
4BTd^2=2{,}415{,}919{,}104.
$$
QK/AV：
$$
2BT^2d=805{,}306{,}368.
$$
FFN：
$$
2BTdd_{ff}=4{,}831{,}838{,}208.
$$
单位为MAC；若按乘/加各一FLOP，主矩阵乘约再乘2。

### ARCH-COST-B03
一张 embedding或output matrix为
$$
Vd=50{,}000\cdot1024=51{,}200{,}000.
$$
Tied时两者共享这一份；untied再增加同规模output head，所以差额约 51.2M 参数。$L$ 不影响这项差额。

## C. 推导与证明

### ARCH-COST-C01
拼接所有 heads前，$W_Q,W_K,W_V,W_O$ 都是 $d\times d$，总参数 $4d^2$。分头只是把输出末维 $d$ reshape为 $(h,d_h)$；因 $hd_h=d$，逐头相加也为 $h\cdot d d_h=d^2$ 每类投影，不能再乘一次 $h$。

### ARCH-COST-C02
Pairwise与四投影比较：
$$
2BT^2d=4BTd^2\Rightarrow T=2d.
$$
与普通FFN比较：
$$
2BT^2d=2BTdd_{ff}\Rightarrow T=d_{ff}.
$$
这是只比较主MAC项的交叉点；softmax、带宽、kernel和硬件可移动实测交叉点。

### ARCH-COST-C03
Cross Q投影 $BT_td^2$，K/V $2BT_sd^2$，O $BT_td^2$，QK/AV $2BT_tT_sd$，合计
$$
2BT_td^2+2BT_sd^2+2BT_tT_sd.
$$
固定 encoder memory和权重下，K/V项可在生成前每层算一次并跨target steps复用；每个新Q/O及其对source的pairwise项仍需计算。

## D. 边界、反例与纠错

### ARCH-COST-D01
完整标准block还有 $4BTd^2$ projections与 $2BTdd_{ff}$ FFN；在 $T\ll d,d_{ff}$ 时它们可主导算术。还有norm/softmax/activation/data movement。$O(T^2d)$只描述pairwise attention渐近项，且没有参数、显存、训练反向或decode账。

### ARCH-COST-D02
数学relation仍要求每个合法 query-key pair参与softmax归一化。Flash-style算法分块加载Q/K/V，在线维护max与normalizer并重算，避免把完整 $(B,h,T,T)$ scores/weights写入主存，因此activation memory下降；dense pair arithmetic仍是all-pairs量级，语义也仍是exact dense attention。

### ARCH-COST-D03
一个理论上少FLOPs的细粒度稀疏attention若使用不规则gather/scatter、低occupancy和未融合小kernels，在小batch GPU上可能受memory/launch限制；高度优化的dense kernel虽算更多却更快。故需同硬件、shape、软件版本实测。

## E. AI 迁移

### ARCH-COST-E01
参数卡：embedding、每层MHA/FFN、norm/head、tying。训练卡：batch/length分布、forward/backward/optimizer口径、tokens与checkpoint。Prefill卡：prompt length、batch、latency/throughput。Decode卡：output length、cache、逐token latency。Memory卡：weights/optimizer/activations/cache/temporary bytes。附dtype、硬件、kernel版本与公式—实测差异。

### ARCH-COST-E02
为多个 $(B,T,d)$ 生成无padding和真实paddingbatch；用shape公式算主MAC并注明1 MAC口径，再用profiler记录kernel FLOPs、时间、bytes和峰值memory。分别开关fused attention/FFN、checkpoint与padding removal。将理论有效tokens、实际paddedtokens、profiler计数和wall-clock四列对账，不用时间反推唯一FLOP。

### ARCH-COST-E03
设 query heads $h$、KV heads $g$。Q/O仍约 $2d^2$；K/V参数从 MHA 的 $2d^2$ 变为 $2d(gd_h)$，cache从 $2LBT(hd_h)$ 变为 $2LBT(gd_h)$；MQA为 $g=1$。比较时固定总参数/训练预算或补足差额，报告质量、长context、prefill/decode latency、带宽、cache bytes和kernel成熟度。
