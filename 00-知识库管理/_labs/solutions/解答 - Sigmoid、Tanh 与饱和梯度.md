---
type: solution
status: draft
area: [neural-networks/activations, sigmoid, tanh]
topic: "[[Sigmoid、Tanh 与饱和梯度]]"
exercise: "[[习题 - Sigmoid、Tanh 与饱和梯度]]"
sources: ["[[S-2010-Glorot-Bengio-Training-Difficulty]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Sigmoid、Tanh 与饱和梯度

## A

### NN-SAT-A01
$\sigma:\mathbb R\to(0,1)$，$\sigma'=\sigma(1-\sigma)\in(0,1/4]$，满足 $\sigma(-x)=1-\sigma(x)$ 而非 odd。$\tanh:\mathbb R\to(-1,1)$，$\tanh'=1-\tanh^2\in(0,1]$，是 odd。关系为 $\tanh x=2\sigma(2x)-1$；两者都严格单调、$C^\infty$、两端饱和。

### NN-SAT-A02
数学饱和可表述为 $x\to\pm\infty$ 时输出趋有限端点且 $\phi'(x)\to0$；更实用地可声明阈值 $|\phi'(x)|<\varepsilon$ 的区域。浮点端点是计算值因 rounding/underflow 恰为 0、1 或 $\pm1$；它可能比精确函数达到给定小斜率更早，依 dtype 和 kernel 而变。

### NN-SAT-A03
对关于 0 对称的 preactivation，sigmoid 输出均值为 $1/2$，下一层因此收到正均值并可能产生偏移/饱和；tanh 则在该条件下均值 0。但 gate 正需要 $(0,1)$ 的连续开关，Bernoulli link 正需要 probability support；这些任务语义足以保留 sigmoid，只应使用稳定 logits-domain loss 并诊断 gate saturation。

## B

### NN-SAT-B01
$h=\sigma(2)\approx0.880797$，$L=-\log h$。分离路线：$dL/dh=-1/h$、$dh/dz=h(1-h)$，乘得 $h-1\approx-0.119203$。fused 路线：$L=\operatorname{softplus}(-z)$，导数 $-\sigma(-z)=\sigma(z)-1$，同样为 $-0.119203$。fused 路线避免极端 probability 取 log。

### NN-SAT-B02
若每层 preactivation 为 0 且没有额外权重 gain，每层 derivative 为 $1/4$，故总 derivative 为 $4^{-L}$。$L=10$ 时为 $4^{-10}=2^{-20}=1/1{,}048{,}576\approx9.53674\times10^{-7}$。

### NN-SAT-B03
$\sigma_\tau'(x)=\tau^{-1}\sigma(x/\tau)(1-\sigma(x/\tau))$，中心斜率为 $1/(4\tau)$：$\tau=2,1,1/2$ 分别为 $1/8,1/4,1/2$。固定输出区间对应的输入宽度与 $\tau$ 成正比，所以温度越小，过渡越窄、中心越陡、远离中心越快饱和。

## C

### NN-SAT-C01
$2\sigma(2x)-1=2/(1+e^{-2x})-1=(1-e^{-2x})/(1+e^{-2x})=(e^x-e^{-x})/(e^x+e^{-x})=\tanh x$。求导得 $2\cdot2\sigma(2x)(1-\sigma(2x))$；代入 $\sigma(2x)=(1+\tanh x)/2$，化为 $1-\tanh^2x$。

### NN-SAT-C02
若 $Z\overset d=-Z$，则 $E\sigma(Z)=E\sigma(-Z)=E[1-\sigma(Z)]$，故为 $1/2$。tanh 为 odd，所以 $E\tanh Z=-E\tanh Z=0$。两函数有界，因此期望自动存在；推广到非有界 odd function 时需 $E|\phi(Z)|<\infty$。

### NN-SAT-C03
$\log\sigma(x)=-\log(1+e^{-x})=-\operatorname{softplus}(-x)$。又 $1-\sigma(x)=1/(1+e^x)=\sigma(-x)$，故 $\log(1-\sigma(x))=\log\sigma(-x)=-\operatorname{softplus}(x)$。稳定库用 logaddexp/softplus 分支避免 overflow。

## D

### NN-SAT-D01
取两层 scalar weights 都为 $1/2$ 且所有 preactivation 近 0；tanh slope 近 1，但每层总 derivative 近 $1/2$，深度 $L$ 后为 $2^{-L}$。即使 weights 为 1，训练中的 bias/mean drift 可使 $|z|$ 大、tanh slope 接近 0。中心单点斜率不控制实际状态分布与矩阵乘积。

### NN-SAT-D02
大负 $x$ 使 $-x$ 很大，朴素式先算 $e^{-x}$，可能 overflow。若 $x\ge0$ 用 $1/(1+e^{-x})$，指数参数非正；若 $x<0$ 用 $e^x/(1+e^x)$，指数参数也非正。第二式由分子分母同乘 $e^x$ 得到，数学等价且指数不超过 1。

### NN-SAT-D03
取 $Z\equiv1$，则 $E\tanh Z=\tanh1>0$，虽 tanh 是 zero-centered/odd activation。正确含义是函数值域和对称性允许正负输出，且对称零中心输入会给零输出均值；它不保证任意实际 preactivation distribution 的 sample/population mean 为 0。

## E

### NN-SAT-E01
逐层/逐 gate 记录 logits quantiles、$\sigma(g)$ 接近 0/1 的比例、$\sigma'(g)$ quantiles、gate bias、state retention 与 gradient-to-gate norm；按 sequence position 和 time lag 分层。用 counterfactual bias/input perturbation 测 gate 是否能离开端点；若饱和伴随任务所需长期 retention 且其他路径有梯度，可能有意；若 loss 高、gate gradient 长期低且扰动可改善，则是 optimization failure。

### NN-SAT-E02
在 FP64 reference 下扫描 logits $[-10^4,10^4]$ 与 labels，检查 fused BCE logits loss/gradient finite、单调且极限正确；比较 BF16 forward/backward 的 absolute error，禁止 probability-clamp 掩盖错误。probability 仅为展示另算稳定 sigmoid，并允许极端值舍入到 0/1；训练结论以 logits loss 为准。再测 reduction、mask、loss scaling 与 distributed count。

### NN-SAT-E03
仅替换 ordinary hidden activation，并提供共同 initialization 与 activation-aware initialization 两轨，独立调 LR；匹配 depth/width/parameters/FLOPs，记录 saturation/dead rate、moments、gradients、速度与多 seeds。sigmoid gates 和 output likelihood links 保持任务正确的原定义，否则同时改变 architecture/likelihood，无法把差异归因于 hidden activation。
