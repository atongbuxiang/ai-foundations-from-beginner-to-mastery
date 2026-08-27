---
type: exercise
status: draft
area: [generative-models, normalizing-flows]
topic: "[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]"
solution: "[[解答 - Autoregressive Flow、MAF 与 IAF 的方向权衡]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Autoregressive Flow、MAF 与 IAF 的方向权衡
## A. 识别与复述
### GEN36-A01
写出 MAF 的编码式、logdet 与两个方向的并行性。
### GEN36-A02
写出 IAF 的生成式、logdet 与两个方向的并行性。
### GEN36-A03
为什么“MAF 与 IAF 互为逆”不能回答 latency？
## B. 手算与建模
### GEN36-B01
$z_1=x_1,z_2=(x_2-x_1)/2$。输入 $(3,11)$，求 $z$ 和编码 logdet。
### GEN36-B02
$x_1=z_1,x_2=2z_2+z_1$，输入 $z=(3,4)$，求 $x$ 和生成 logdet。
### GEN36-B03
三维 unit-scale MAF：$z_1=x_1,z_2=x_2-x_1,z_3=x_3-x_1-x_2$。由 $z=(1,2,4)$ 串行恢复 $x$。
## C. 推导与证明
### GEN36-C01
证明 MAF 的 $\partial z/\partial x$ 为三角矩阵并得到 logdet。
### GEN36-C02
证明 IAF 给定完整 $z$ 可一次 masked forward 生成全部 conditioner 参数。
### GEN36-C03
说明 coupling 如何作为更粗粒度的 autoregressive flow 特例。
## D. 边界、反例与纠错
### GEN36-D01
反驳“MAF 不能采样”。
### GEN36-D02
反驳“IAF 用在 VAE 后就得到 exact data likelihood”。
### GEN36-D03
反驳“没有 diffusion time steps 的 flow 就是一次网络调用”。
## E. AI 迁移
### GEN36-E01
为 density estimation 与高吞吐 posterior sampling 分别选择 MAF/IAF，并说明理由。
### GEN36-E02
设计公平比较 MAF、IAF、coupling latency 的协议。
### GEN36-E03
审计 TARFlow 的“one-step sampling”主张应报告哪些对象？
## 解答入口
[[解答 - Autoregressive Flow、MAF 与 IAF 的方向权衡]]

