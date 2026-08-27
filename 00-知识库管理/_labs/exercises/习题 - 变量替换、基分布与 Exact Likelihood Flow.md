---
type: exercise
status: draft
area: [generative-models, normalizing-flows]
topic: "[[变量替换、基分布与 Exact Likelihood Flow]]"
solution: "[[解答 - 变量替换、基分布与 Exact Likelihood Flow]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 变量替换、基分布与 Exact Likelihood Flow
## A. 识别与复述
### GEN33-A01
固定生成方向 $x=g(z)$、编码方向 $z=f(x)$，分别写出两种 log-density 公式。
### GEN33-A02
`exact likelihood` 在本卷中精确承诺什么？列出三件它不承诺的事。
### GEN33-A03
为什么经典 diffeomorphic flow 通常要求 latent 与 data 同维？
## B. 手算与建模
### GEN33-B01
$Z\sim\mathcal N(0,1)$，$X=3Z-2$。求 $f(x)$、$p_X(x)$ 和 $\log p_X(1)$。
### GEN33-B02
$x=Az+b$，$A=\operatorname{diag}(2,3)$，$z=(1,-1)^\top$。求 $x$、生成 logdet 与编码 logdet。
### GEN33-B03
三层编码 flow 的 logdet 依次为 $0.4,-0.2,1.1$，base log-density 为 $-3.5$。求 data log-density。
## C. 推导与证明
### GEN33-C01
从概率质量守恒和局部线性化推导多元 change-of-variables。
### GEN33-C02
证明复合 flow 的总 logdet 等于各层 logdet 之和，并标明每层的评价点。
### GEN33-C03
证明若 $p_Z>0$ 处处成立且 $g$ 是全空间 diffeomorphism，则 $p_X>0$ 处处成立。
## D. 边界、反例与纠错
### GEN33-D01
纠正“生成映射扩大体积，所以 density 乘 $|\det J_g|$”。
### GEN33-D02
给出可逆但数值病态的二维线性 flow，并说明 round-trip 风险。
### GEN33-D03
反驳“continuous density 可直接当 8-bit pixel 的 probability mass”。
## E. AI 迁移
### GEN33-E01
为 $B\times d$ tabular flow 写出训练 forward 的形状与 log-density 合同。
### GEN33-E02
设计检查 Jacobian 符号错误的三个独立单元测试。
### GEN33-E03
审计一篇宣称“exact likelihood 因而生成质量最优”的论文，需要哪些证据账？
## 解答入口
[[解答 - 变量替换、基分布与 Exact Likelihood Flow]]

