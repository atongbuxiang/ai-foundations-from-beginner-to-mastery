---
type: exercise
status: draft
area: [generative-models, latent-diffusion]
topic: "[[Latent Diffusion、压缩瓶颈与两阶段误差]]"
solution: "[[解答 - Latent Diffusion、压缩瓶颈与两阶段误差]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Latent Diffusion、压缩瓶颈与两阶段误差
## A. 识别与复述
### GEN62-A01
写出 LDM 的 first stage、latent forward noising 与生成路径。
### GEN62-A02
区分 continuous latent、VQ clean latent 与 categorical noisy state。
### GEN62-A03
列出 representation、prior、sampler、decoder/evaluation 四本误差账。
## B. 手算与建模
### GEN62-B01
$H=W=512,f=8,c=4$。求 pixel/latent spatial sites 与 dimension ratio $chw/(3HW)$。
### GEN62-B02
若 latent 每维标准差为 5，想缩放到单位标准差，$s$ 取多少？生成后 decoder 前怎样处理？
### GEN62-B03
VQ latent grid $64\times64,K=16384$，求 nominal bits/image；与 continuous $64\times64\times4$ float16 字节数比较。
## C. 推导与证明
### GEN62-C01
用三角不等式写出 representation floor 与 latent-generation error 的上界分解。
### GEN62-C02
证明若 $E(x_a)=E(x_b)$ 且 decoder 确定，则不可能同时无误重构 $x_a\ne x_b$。
### GEN62-C03
推导 spatial downsampling 的位置数比，并解释为什么不是 wall-clock 定理。
## D. 边界、反例与纠错
### GEN62-D01
纠正“latent diffusion 就是离散 token diffusion”。
### GEN62-D02
为什么更好的 latent denoiser不能恢复 encoder 丢掉的 instance-specific bit？
### GEN62-D03
为什么感知更锐利的重构可能有更大 pixel distortion？
## E. AI 迁移
### GEN62-E01
列出 LDM checkpoint 的完整 first/second-stage 配置。
### GEN62-E02
设计 compression factor sweep，公平比较计算与重构/生成。
### GEN62-E03
给出 latent scale 错配的自动诊断与 assertion。
## 解答入口
[[解答 - Latent Diffusion、压缩瓶颈与两阶段误差]]
