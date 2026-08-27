---
type: exercise
status: draft
area: [generative-models, evaluation]
topic: "[[Likelihood、FID、KID、Precision–Recall 与人类评估]]"
solution: "[[解答 - Likelihood、FID、KID、Precision–Recall 与人类评估]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Likelihood、FID、KID、Precision–Recall 与人类评估
## A. 识别与复述
### GEN71-A01
FID 在哪个空间、对什么 fitted distributions 计算？
### GEN71-A02
KID 的“无偏”具体指什么，不指什么？
### GEN71-A03
为什么生成评价中的 precision/recall 必须注明方法版本？
## B. 手算与建模
### GEN71-B01
一维 Gaussian features：真实 $(\mu,\sigma^2)=(0,1)$、生成 $(2,4)$。求 FID。
### GEN71-B02
线性 kernel $k(x,y)=xy$，真实样本 $(0,2)$、生成样本 $(1,3)$。计算 unbiased MMD$^2$。
### GEN71-B03
数据 NLL 为 100 nats、维度 64，求 BPD。
## C. 推导与证明
### GEN71-C01
说明 FID 为何只使用一二阶 moments，并给相同 moments 不同分布例子。
### GEN71-C02
写出 KID/MMD 的 U-statistic 并解释为何排除同集合 diagonal。
### GEN71-C03
解释 plug-in FID 有 finite-sample bias 的 Jensen/非线性原因。
## D. 边界、反例与纠错
### GEN71-D01
反驳“低 FID 保证没有 mode dropping”。
### GEN71-D02
解释不同 resize pipeline 的 FID 为什么不可直接横比。
### GEN71-D03
反驳“看 20 张作者精选样本就是人类评估”。
## E. AI 迁移
### GEN71-E01
为条件图像生成设计最小评价面板。
### GEN71-E02
设计盲化配对人评并指定统计单位。
### GEN71-E03
设计 train/test nearest-neighbor copy audit。
## 解答入口
[[解答 - Likelihood、FID、KID、Precision–Recall 与人类评估]]
