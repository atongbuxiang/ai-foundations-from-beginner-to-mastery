---
type: solution
status: verified
area: [language-models, supervised-finetuning, teacher-forcing]
topic: "[[监督微调、Teacher Forcing 与 Response-only Loss]]"
exercise: "[[习题 - 监督微调、Teacher Forcing 与 Response-only Loss]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 监督微调、Teacher Forcing 与 Response-only Loss

## A. 识别与复述

### LM26-A01
Teacher forcing 在预测 $y_t$ 时条件于 gold $y^*_{<t}$；自由生成条件于模型此前采样的 $\hat y_{<t}$。训练可并行计算 shifted token NLL，推理的错误会改变后续历史。这个定义差不自动识别某性能错误的原因。

### LM26-A02
Input 是模型读取的 token；shifted label 是每 input position 要预测的下一 token；attention relation 决定 query 能读哪些 keys；loss mask 决定哪些 label errors 计入 numerator/denominator。四者可共享 shape，却语义不同。

### LM26-A03
Full-sequence 估计整段序列的 token risk，包括 system/user/template；response-only 估计给定 prompt/history 时 assistant target 的条件 risk。后者仍需定义 marker、EOS、tool、rationale、多轮和归一化。

## B. 手算与构造

### LM26-B01
Inputs 为 [U,q,A,a,b]；labels 为 [q,A,a,b,EOS]。只监督 a、b、EOS 时 mask 为 [0,0,1,1,1]，第一个 1 位于 input A 预测 label a 的位置。

### LM26-B02
Global target mean 为 $(12+9)/(6+3)=21/9=7/3\approx2.3333$。等设备 mean 为 $(12/6+9/3)/2=(2+3)/2=2.5$；后者让第二设备每 token 权重更大。

### LM26-B03
Per-token mean 为 $(4+6)/(4+2)=10/6=5/3\approx1.6667$。Per-turn mean 为 $(4/4+6/2)/2=(1+3)/2=2$。不同因为第二轮短但均值高。

## C. 推导与证明

### LM26-C01
$p(y\mid x)=\prod_{t=1}^np(y_t\mid x,y_{<t})$；取负对数把乘积变和：$-\log p(y\mid x)=\sum_t-\log p(y_t\mid x,y_{<t})$。把 prompt positions 的 mask 设 0、response labels 设 1，就得到 response-only token NLL。

### LM26-C02
$N/D=\sum_i m_i\ell_i/\sum_i m_i$。对每个 $m_i=1$ 的 target，其系数都是 $1/D$；无效位置系数 0。Per-device/turn 先求 mean 再平均时，系数变成 $1/(K D_k)$，除非各 $D_k$ 相等。

### LM26-C03
Loss mask 只乘在 error 上；attention forward 已先产生 logits。Assistant query 通常需要读 system/user，response-only 正是条件于它们。若要隔离不同 conversations，需另写 block-causal relation，不能靠 prompt mask。

## D. 边界、反例与纠错

### LM26-D01
若目标包含学习严格 role/template grammar，full loss 可提供控制 token 监督；response-only 可能漏 user-side format。反之长 prompts 会使 full loss 偏重模仿输入。哪个合适依 deployment estimand，需 matched experiment。

### LM26-D02
超长 prompt 占满窗口，assistant response 全被右截断，所有 mask 为 0，故 $D=0$。应在 collator 前拒绝、重新截断/保留 response，或记录为空监督样本；不得静默除零或算作已训练 example。

### LM26-D03
分布差是必要描述，却未说明错误是否来自 exposure、模型容量、数据、sampler、stop 或评估。需 controlled history corruption/sequence-level intervention 与 matched baselines；单个失败输出不识别因果。

## E. AI 迁移

### LM26-E01
固定短序列，手写 expected inputs/labels/mask/relation/per-position NLL；断言只 shift 一次。构造两设备不同 $D$，断言 all-reduce $N,D$ 后为 $7/3$，并故意验证设备均值为 2.5 的错误分叉。

### LM26-E02
Epoch 不说明 examples、target masks、response lengths、repeats、packing 或 global denominator；无法比较学习信号。应补 unique conversations、turn draws、model tokens、effective targets、loss sum、FLOPs 和 truncation/$D=0$。

### LM26-E03
固定 raw conversations/template/tokenizer/base/order；两臂按 unique examples、effective targets、FLOPs 分别给视图；同 optimizer/search budget/seed；测回答、格式、旧域、安全，冻结 checkpoint selection 与 inference sampler。

## 无提示重做

- [ ] 对多轮序列写四张量和 global $N,D$。
- [ ] 用条件历史解释 teacher forcing 与自由生成。

