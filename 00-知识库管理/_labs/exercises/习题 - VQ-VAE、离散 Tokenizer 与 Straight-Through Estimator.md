---
type: exercise
status: draft
area: [generative-models, vector-quantization]
topic: "[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"
solution: "[[解答 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator
## A. 识别与复述
### GEN60-A01
写出 nearest-code assignment、lookup vector 与 STE expression。
### GEN60-A02
解释 reconstruction、codebook、commitment 三项分别更新谁。
### GEN60-A03
为什么 tokenizer autoencoder 之外还需 learned prior 才能生成？
## B. 手算与建模
### GEN60-B01
对 codes $(0,0),(2,0),(0,2)$ 与 $z=(1.4,.3)$，计算 assignment。
### GEN60-B02
若 decoder 回传 $g=(.7,-.2)$，标准 STE 给 encoder 什么梯度？真实 hard map cell 内梯度呢？
### GEN60-B03
token grid 为 $32\times32$、$K=8192$。求 nominal bits/image；为什么它不是实际压缩码率？
## C. 推导与证明
### GEN60-C01
证明 $z_q=z+\operatorname{sg}(q-z)$ 的前向值和代理 Jacobian。
### GEN60-C02
推导 EMA codebook update 与在线 K-means center 的对应。
### GEN60-C03
说明增大 $K$ 为什么同时影响 quantization distortion 与 prior difficulty。
## D. 边界、反例与纠错
### GEN60-D01
纠正“STE 是 nearest-neighbor 的真实导数”。
### GEN60-D02
构造 tokenizer 重构好但 prior 生成差的情形。
### GEN60-D03
为什么 code utilization 高不保证语义好或 sample 好？
## E. AI 迁移
### GEN60-E01
列出 VQ checkpoint 必须保存的 tokenizer 与 optimizer 合同。
### GEN60-E02
设计 dead-code、entropy、quantization error 与 rFID 的联合审计。
### GEN60-E03
比较 gradient codebook update 与 EMA 时，怎样做公平实验？
## 解答入口
[[解答 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]
