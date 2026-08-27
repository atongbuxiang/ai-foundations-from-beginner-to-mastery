---
type: solution
status: draft
topic: "[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]"
exercise: "[[习题 - Autoregressive Flow、MAF 与 IAF 的方向权衡]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Autoregressive Flow、MAF 与 IAF 的方向权衡
## A. 识别与复述
### GEN36-A01
$z_i=(x_i-\mu_i(x_{<i}))/\sigma_i(x_{<i})$，编码 logdet $-\sum_i\log\sigma_i$。给完整 $x$ 时参数和 $z$ 可并行；从 $z$ 恢复 $x$ 需按 $i$ 串行。
### GEN36-A02
$x_i=\mu_i(z_{<i})+\sigma_i(z_{<i})z_i$，生成 logdet $\sum_i\log\sigma_i$。给完整 $z$ 时可并行变换；从 $x$ 反求 $z$ 通常串行。
### GEN36-A03
Inverse relation 不记录计算图中何时知道 conditioner inputs。Latency 还由串行深度、每次网络成本、缓存、序列维数、batch、hardware 和 kernel 决定。
## B. 手算与建模
### GEN36-B01
$z_1=3,z_2=(11-3)/2=4$。Jacobian 对角为 $(1,1/2)$，编码 logdet $-\log2$。
### GEN36-B02
$x=(3,11)$；生成 Jacobian 对角 $(1,2)$，logdet $\log2$。
### GEN36-B03
$x_1=1$；$x_2=z_2+x_1=3$；$x_3=z_3+x_1+x_2=8$。后一步依赖前一步结果，不能并行假装已知。
## C. 推导与证明
### GEN36-C01
$z_i$ 只依赖 $x_{\le i}$，所以 $\partial z_i/\partial x_j=0$ 对 $j>i$；对角是 $1/\sigma_i$。三角 determinant 为对角乘积，取 log 得 $-\sum_i\log\sigma_i$。
### GEN36-C02
第 $i$ 个参数只依赖 $z_{<i}$，而整向量 $z$ 在调用前已知。因果 mask 可在一次矩阵运算中为所有位置屏蔽未来坐标并输出全部参数；不需要先生成 $x_i$ 再作为条件。
### GEN36-C03
Coupling 将变量分为 A/B：A 原样，B 的每个输出都只依赖全部 A 而不依赖 B 内前序坐标。于是三角结构更粗，B 内可并行 forward/inverse；代价是 A 本层不变。
## D. 边界、反例与纠错
### GEN36-D01
MAF 可按 $x_i=\mu_i(x_{<i})+\sigma_i(x_{<i})z_i$ 依次生成；只是 critical path 长，不是数学上不能采样。
### GEN36-D02
IAF 若只变换 $q(z\mid x)$，它让变分后验 density 可算；decoder marginal $p(x)=\int p(z)p(x\mid z)dz$ 仍需积分，ELBO 仍可能有 inference gap。
### GEN36-D03
Autoregressive inverse 可能需要序列长度次 Transformer calls；CNF 一次 solver call 也可能有很多 NFE。没有 diffusion grid 只删去一种步数，不删依赖和内部计算。
## E. AI 迁移
### GEN36-E01
需要大量 data log-density evaluation 时选 MAF，因为给定 $x$ 可一次 masked forward。高维 VAE posterior transform 需要并行 samples 时选 IAF，因为 base noise 已知；同时声明其 data inverse 不便宜。
### GEN36-E02
统一参数量、层数、dtype、编译、batch、hardware 和 warmup；分别测 per-sample density 与 sampling，报告吞吐、P50/P95 latency、network calls、显存和 NLL。两任务都测，避免只展示擅长方向。
### GEN36-E03
报告 patch/sequence length、autoregressive inverse calls、每 call Transformer 规模、batch/hardware/dtype、wall time、Gaussian augmentation、post-denoise 次数、guidance calls，以及 core 与部署分布的质量/覆盖/likelihood。`one-step` 不能代替这些量。

