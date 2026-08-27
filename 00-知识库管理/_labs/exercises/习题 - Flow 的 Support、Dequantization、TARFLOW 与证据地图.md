---
type: exercise
status: draft
area: [generative-models, normalizing-flows]
topic: "[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"
solution: "[[解答 - Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Flow 的 Support、Dequantization、TARFLOW 与证据地图
## A. 识别与复述
### GEN40-A01
写出 continuous density 诱导离散 bin mass 的公式。
### GEN40-A02
写出 uniform 与 variational dequantization lower bound。
### GEN40-A03
TARFlow 的 core、augmentation、denoise、guidance 分别改变什么？
## B. 手算与建模
### GEN40-B01
一维 bin $[0,1)$ 上 $p_c(y)=2y$。求离散 mass 与 $y=1/2$ 的 density，说明二者差异。
### GEN40-B02
两维离散 log-mass 为 $-4\log2$。求 bpd。
### GEN40-B03
$q(u\mid x)=2u$、$p_c(x+u)=3u^2$，$u\in[0,1]$。写出一份 Monte Carlo lower-bound integrand 并求期望。
## C. 推导与证明
### GEN40-C01
用 Jensen 推导 uniform dequantization 下界。
### GEN40-C02
用 importance identity 推导 variational dequantization 下界。
### GEN40-C03
证明 full-support base 经全空间 diffeomorphism 后仍 full support。
## D. 边界、反例与纠错
### GEN40-D01
反驳“高 likelihood 必然给更好的语义样本”。
### GEN40-D02
反驳“post-denoise 后样本仍直接由 core flow likelihood 评价”。
### GEN40-D03
反驳“TARFlow 是一步，所以 sampling 没有串行瓶颈”。
## E. AI 迁移
### GEN40-E01
建立跨 flow 论文 bpd 比较清单。
### GEN40-E02
设计 TARFlow 四组件消融与分布账。
### GEN40-E03
如何把 TARFlow、STARFlow、iTARFlow 的结论放入证据时间线而不倒灌？
## 解答入口
[[解答 - Flow 的 Support、Dequantization、TARFLOW 与证据地图]]

