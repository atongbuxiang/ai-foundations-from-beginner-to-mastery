---
type: exercise
status: draft
area: [generative-models, quantization, frontier]
topic: "[[Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"
solution: "[[解答 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ
## A. 识别与复述
### GEN61-A01
区分 dead codes、低 assignment entropy、representation collapse 与高 quantization error。
### GEN61-A02
FSQ、Rotation、SimVQ、DiVeQ 分别改哪一层？
### GEN61-A03
为什么“无 Aux Loss”“无 learned codebook”“高 utilization”是不同性质？
## B. 手算与建模
### GEN61-B01
FSQ levels 为 $(8,8,8,5,5)$。求隐式 $K$ 与 nominal bits/token。
### GEN61-B02
若 Rotation 的 $\|q\|/\|z\|=.05$，忽略旋转方向时 reconstruction gradient norm 缩放多少？
### GEN61-B03
assignment frequencies 为 $(.5,.25,.125,.125)$。求 entropy、perplexity 与 usage。
## C. 推导与证明
### GEN61-C01
解释 $E=QW$ 为什么函数上可合并、训练时不等价。
### GEN61-C02
验证 DiVeQ-detach 前向等于 $q$，并指出反向新增来自何处。
### GEN61-C03
证明 FSQ 名义 codebook 是各维 levels 的笛卡尔积。
## D. 边界、反例与纠错
### GEN61-D01
构造 100% utilization 但重构很差的 quantizer。
### GEN61-D02
为什么 Rotation 原论文平均改善与科学空间作者未复现改善可以同时成立？
### GEN61-D03
反驳“FSQ 没有 codebook collapse，所以组合 codes 必然均匀使用”。
## E. AI 迁移
### GEN61-E01
设计五种 quantizer 的 matched-budget benchmark 表。
### GEN61-E02
给出 gradient norm ratio 与 initialization 的诊断实验。
### GEN61-E03
怎样把机制解释标为可证伪假说，而不是事后故事？
## 解答入口
[[解答 - Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]
