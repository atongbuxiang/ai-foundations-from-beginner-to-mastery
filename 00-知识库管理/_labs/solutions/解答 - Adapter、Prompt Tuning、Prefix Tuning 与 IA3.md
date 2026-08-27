---
type: solution
status: verified
area: [language-models, peft, adapters, prompts, ia3]
topic: "[[Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"
exercise: "[[习题 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Adapter、Prompt Tuning、Prefix Tuning 与 IA3

## A. 识别与复述

### LM31-A01
Prompt tuning 加输入 embeddings；LoRA 改选定线性权重增量；Adapter 插入 residual bottleneck module；Prefix tuning 加各层 attention K/V 状态；IA3 以向量缩放 K/V/FFN channels。共同点只是大部分 base frozen。

### LM31-A02
Prompt 只在输入层提供 $p$ 个 virtual embeddings，后续层状态由模型传播；Prefix 可直接给每层 attention 注入任务专属 K/V。后者通常更大、占每层 KV，表达接口更深。

### LM31-A03
Prompt/prefix 占 context/KV/prefill；Adapter 增每层非线性 FLOPs；unmerged LoRA 增 matmuls并需动态权重路由；IA3 需 gates/kernel。Task switching、cache、batch fragmentation 可能主导服务。

## B. 手算与构造

### LM31-B01
Prompt $pd=5\cdot100=500$。Per-layer KV prefix $2Lpd=2\cdot4\cdot5\cdot100=4000$。每层一个 bottleneck adapter（忽略 bias）$2Ldr=2\cdot4\cdot100\cdot2=1600$。

### LM31-B02
$h\in\mathbb R^d$；$W_{down}\in\mathbb R^{r\times d}$ 得 $u=W_{down}h\in\mathbb R^r$；激活不改 shape；$W_{up}\in\mathbb R^{d\times r}$ 得 $v\in\mathbb R^d$；输出 $h+v\in\mathbb R^d$。

### LM31-B03
若 $K,V\in\mathbb R^{B\times H\times L\times d_h}$，$l_k,l_v\in\mathbb R^{d_h}$ 可沿最后轴广播；若 $h_{ff}\in\mathbb R^{B\times L\times d_{ff}}$，$l_{ff}\in\mathbb R^{d_{ff}}$ 沿最后轴广播。具体 IA3 实现可能选另一轴，必须列 tensor layout。

## C. 推导与证明

### LM31-C01
若 adapter 无 activation/bias，$h+W_{up}W_{down}h=(I+W_{up}W_{down})h$，是 rank-$r$ 增量，可在相邻纯线性且无分支条件时折叠。加入非线性、norm、residual placement 或共享路径后一般不能写为固定单矩阵。

### LM31-C02
每层每个 prefix token 各有 K、V 两个 $d$ 维 state，故 $2pd$ 元素；$L$ 层为 $2Lpd$。Batch 中可共享参数但 runtime cache/broadcast 的实际 residency 依实现。

### LM31-C03
参数维数只给参数流形维数上界；注入位置和非线性不同。500 个 input embeddings 经 frozen network的影响，与500个 channel gates或低秩权重方向不同；函数映射的 Jacobian/可达子空间不相同。

## D. 边界、反例与纠错

### LM31-D01
Soft prompt 是连续向量，未必等于任何 token embedding 或可逆语言；最近邻 token 逐个替换会改变向量和函数。可视化近邻是解释 proxy，不是“翻译出真实 prompt”。

### LM31-D02
一个 gate 向量元素若把关键 FFN channel 从 1 放大到 100 或翻负，可改变大量 logits；少量参数也可控制高影响方向。功能变化需 probe/task 测量，不由维数保证。

### LM31-D03
LoRA：动态选择/融合 A,B 与额外 matmul、batch 同任务性；Prefix：每请求/层 KV、context 与 cache；Adapter：每层额外 module、kernel dispatch 与路由。瓶颈分别可能是 weight bandwidth、KV memory、compute/latency。

## E. AI 迁移

### LM31-E01
同 base/data/targets/FLOPs/search budget；每法扫合理 rank/prompt length；报 trainable params、artifact bytes、grads/opt/activation/peak、train throughput、context/KV、single/mixed-task latency、in/OOD/old/safety/calibration，多 seed画 Pareto。

### LM31-E02
保存 p、embedding/KV shapes、注入层、position IDs、attention relation、context loss、per-layer KV bytes、batch sharing、cache key/invalidations、prefill/decode latency；比较无 prompt/prefix与不同 input length。

### LM31-E03
默认 LR、rank/p、insertion 与 initialization 的成熟度不同，单点排名混入调参。需同 search budget、预注册 selection 和 sensitivity curves；否则只能报告这些具体默认配置结果。

## 无提示重做

- [ ] 由 d、L、p、r 手算五类 PEFT 的状态量。
- [ ] 从计算图说明参数、context、KV 与额外 FLOPs的差别。

