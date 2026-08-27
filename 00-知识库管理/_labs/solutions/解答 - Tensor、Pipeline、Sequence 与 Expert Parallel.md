---
type: solution
status: verified
area: [training, distributed-systems, model-parallelism]
topic: "[[Tensor、Pipeline、Sequence 与 Expert Parallel]]"
exercise: "[[习题 - Tensor、Pipeline、Sequence 与 Expert Parallel]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Tensor、Pipeline、Sequence 与 Expert Parallel

> [!warning] 使用边界
> 并行名称不是实现：只有 tensor shape、mesh group、collective、schedule 与 topology 都写出后，成本和语义才可计算。

## A. 识别与复述

### TRN62-A01
DP 切样本并归约 gradient；TP 切层内 hidden/head/weight，常用 All-Reduce/All-Gather/Reduce-Scatter；PP 切层 stage，用 P2P 传 activation/gradient；sequence/context 切 token，依算子做 gather/scatter 或 attention exchange；EP 切 experts，用 All-to-All dispatch/combine routed tokens。

### TRN62-A02
sequence parallel 常把可逐 token 的 norm/dropout 等沿 sequence 切分，并与 TP 的 replicated activation 去冗余；context parallel 要让一次 attention 跨多个 token blocks，必须处理全局 K/V 依赖、causal mask 与 softmax statistics。术语随框架有差异，所以应写具体算子和通信，而非仅写 SP/CP。

### TRN62-A03
process mesh 给每个 rank 坐标 $(d,t,p,e,\ldots)$；某 axis 的 group 固定其他坐标、只遍历该轴。replicated axis 表示该对象在该轴复制。只写乘积无法知道 EP 是否复用 DP ranks、collective 在哪些 ranks 内发生，甚至无法验证 degree 与 shape 是否整除。

## B. 手算与构造

### TRN62-B01
按 $K$ 列切：$W_r\in\mathbb R^{H\times K/4}$，每 rank 得 $Y_r\in\mathbb R^{B\times K/4}$；下游若接受 shard 可不 gather，否则 All-Gather。按 $H$ 行切：$X_r\in\mathbb R^{B\times H/4}$、$W_r\in\mathbb R^{H/4\times K}$，局部 $Z_r=X_rW_r\in\mathbb R^{B\times K}$，需 All-Reduce sum 得 $Y=\sum_rZ_r$。

### TRN62-B02
$$
\eta_{pipe}=\frac{32}{32+8-1}=\frac{32}{39}\approx0.8205,\qquad
bubble\approx17.95\%.
$$
这是等时 stage、简化 forward schedule 的教学上界，不含 backward、通信和不均衡。

### TRN62-B03
均匀期望为 $4096/8=512$ tokens/expert；capacity 为 $1.25\times512=640$。收到 900 的 expert 超出 260 tokens；实现必须 drop、reroute 或排队，每种都改变质量或延迟合同。

## C. 推导与证明

### TRN62-C01
column split 写 $W=[W_1,\ldots,W_P]$，于是 $XW=[XW_1,\ldots,XW_P]$，输出天然按列拼接。row split 写 $X=[X_1,\ldots,X_P]$、$W=[W_1^T,\ldots,W_P^T]^T$，则 $XW=\sum_rX_rW_r$，每 rank 只有部分和，必须做 sum collective。

### TRN62-C02
第一个 micro-batch 填满 $P$ stages 需 $P-1$ 个额外槽，之后每槽完成一个；总槽数 $M+P-1$，有用完成数 $M$，故效率 $M/(M+P-1)$。增 $M$ 摊薄 fill/drain，但可增加在途 activation、减小单 micro-batch kernel 效率并改变 accumulation/optimizer 时钟。

### TRN62-C03
输入 token 表 $X\in\mathbb R^{T\times H}$ 经 router 得 expert id；按目的 rank pack 后 All-to-All，rank-local experts 计算不同长度块，再逆 All-to-All 按原 token 顺序 combine。payload 约随 routed token×hidden×bytes 增长，但热点 expert 决定最大 local compute/queue，最慢 rank 可把全组拖入 barrier。

## D. 边界、反例与纠错

### TRN62-D01
还要 $H,K,heads,experts,layers$ 对对应 degree 可切；每 stage 显存与时间需平衡；rank 必须组成无重叠/正确嵌套 groups；activation/临时 buffer 要能放下；网络 topology 要支持 collective。512 只是乘法结果，不是可运行证明。

### TRN62-D02
micro-batch 过小会降低 GEMM occupancy、提高 kernel launch/通信占比；数量多会保留更多 activation 或增加 schedule bookkeeping；还可能改变 normalization/随机性/gradient normalization。故吞吐常先升后降，而非单调。

### TRN62-D03
若路由器把大量 tokens 发往同一 expert，该 rank 接收更多 All-to-All payload、执行更多 expert compute，其他 ranks 等待；capacity drop 又改变 token estimator 与质量。稀疏 FLOPs 不保证规则通信或无 straggler。

## E. AI 迁移

### TRN62-E01
若 EP 是独立 mesh 轴，总设备 $8\times4\times2\times2=128$；若 EP group 从 DP axis 中切出/复用，其物理设备可能仍是 $8\times4\times2=64$，但有效数据复制度要重定义。manifest 必须列 rank→$(d,t,p,e)$ 映射、每轴 group、weight/activation shape、All-Reduce/All-to-All/P2P 与全局 batch，不能只写四个数字。

### TRN62-E02
TP 可切 heads/hidden，减单设备 weight/activation，但层内 collective 随层频繁；CP 切长 sequence，直接减每 rank KV/attention memory，却需交换 K/V 或 softmax statistics并处理 causal order。用真实长序列 shape 比 peak memory、bytes/ready time、attention kernel efficiency、RNG/mask一致性和 matched quality，而非只比理论 FLOPs。

### TRN62-E03
表的每行至少是：layer/op；global input/output shape；mesh axis/group；local shard shape；local compute；collective/P2P；payload dtype/bytes；依赖/ready timestamp；能否 overlap；同步/数值 reduction；输出布局。沿表串成 DAG 才能识别 exposed communication tail。

## 无提示重做

- [ ] 48 小时后从 $Y=XW$ 重推两种 TP。
- [ ] 一周后独立画一个四轴 rank/group 映射。
