---
type: exercise
status: draft
area: [generative-models, ddcm, evidence-map]
topic: "[[DDCM、离散生成路线比较与证据地图]]"
solution: "[[解答 - DDCM、离散生成路线比较与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - DDCM、离散生成路线比较与证据地图
## A. 识别与复述
### GEN64-A01
DDCM 离散化的对象是什么？与 D3PM/VQ 各差在哪里？
### GEN64-A02
写出 per-step noise codebook sampler 与名义 index bits。
### GEN64-A03
解释 I/T/E/H/O 五级证据在 DDCM 中的例子。
## B. 手算与建模
### GEN64-B01
$T=100,K=64$，忽略其它开销，求 nominal bits/image。
### GEN64-B02
给 codes $(1,0),(0,1),(-1,0),(0,-1)$ 和残差 $(2,-1)$，求 max-inner-product code。
### GEN64-B03
对同一 codes、target mean $m=(1,.5)$，写出 density-weighted 未归一权重。
## C. 推导与证明
### GEN64-C01
从 $N(m,I)$ 密度推导有限 codebook softmax 权重；等模时化简为内积 logits。
### GEN64-C02
为什么 $K^T$ 是名义 index sequences 数，却不是 distinct high-quality images 数？
### GEN64-C03
说明 deterministic argmax 在 $K\to\infty$ 时为何不自动恢复 Gaussian random sampling。
## D. 边界、反例与纠错
### GEN64-D01
纠正“DDCM 免训练，所以编码几乎免费”。
### GEN64-D02
为什么减少 $T$ 同时是 sampler acceleration 和码率/重构改变？
### GEN64-D03
反驳“DDCM indices 天然是一组局部语义 image tokens”。
## E. AI 迁移
### GEN64-E01
列出 DDCM codec 的最小可复现字段。
### GEN64-E02
设计 shared vs per-step codebook 的公平实验。
### GEN64-E03
给四条路线设计对象—训练—码率—误差—系统的选择决策表。
## 解答入口
[[解答 - DDCM、离散生成路线比较与证据地图]]
