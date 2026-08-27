---
type: exercise
status: draft
area: [generative-models, evidence]
topic: "[[EBM、Score、GAN 与 Diffusion 的接口和证据地图]]"
solution: "[[解答 - EBM、Score、GAN 与 Diffusion 的接口和证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - EBM、Score、GAN 与 Diffusion 的接口和证据地图
## A. 识别与复述
### GEN32-A01
列出 energy—score、denoiser—score、GAN logit—density ratio 的精确条件。
### GEN32-A02
为什么 diffusion 更自然地是一族 time-indexed scores，而非单一静态 energy？
### GEN32-A03
用“定义恒等式、总体最优等价、算法接口、经验类比”给四种关系各举一例。
## B. 手算与建模
### GEN32-B01
$p_*=N(0,1),p_g=N(1,1)$。求最优 GAN logit $\log p_* -\log p_g$，并指出它是否等于 $\log p_*$。
### GEN32-B02
向量场 $s(x,y)=(-y,x)$ 是否能在 $\mathbb R^2$ 写成 $-\nabla E$？用 mixed partial/curl 判断。
### GEN32-B03
对 $E(x)=x^2/2$，写出 score、一步 ULA 与对应 one-pass generator 的差异。
## C. 推导与证明
### GEN32-C01
证明可微 EBM 的 $s=-\nabla E$，并说明加法 gauge 对 score 的影响。
### GEN32-C02
从最优 GAN 判别器推导 log-density ratio。
### GEN32-C03
在单连通区域，说明对称 Jacobian 是光滑向量场可表示为 gradient 的必要条件；为什么仅在有限样本点检查不充分？
## D. 边界、反例与纠错
### GEN32-D01
反驳“任意 learned score 都对应一个 normalized EBM”。
### GEN32-D02
反驳“GAN、EBM 和 diffusion 都在下降 energy，所以训练等价”。
### GEN32-D03
反驳“一个方法 FID 更低，便证明其 density/score 理论更准确”。
## E. AI 迁移
### GEN32-E01
为一篇声称“生成模型=能量模型”的论文建立 claim-evidence ledger。
### GEN32-E02
设计跨 EBM、GAN 与 score model 的 compute/quality/coverage 公平比较。
### GEN32-E03
解释科学空间四篇主文分别承担什么教学角色，以及必须由一级来源补什么。
## 解答入口
[[解答 - EBM、Score、GAN 与 Diffusion 的接口和证据地图]]

