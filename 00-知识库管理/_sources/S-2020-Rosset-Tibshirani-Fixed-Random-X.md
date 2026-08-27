---
type: source
status: active
area: [sources, learning-theory, regression, bias-variance, random-design]
source_type: paper
title: "From Fixed-X to Random-X Regression: Bias-Variance Decompositions, Covariance Penalties, and Prediction Error Estimation"
author: [Saharon Rosset, Ryan J. Tibshirani]
year: 2020
url: "https://doi.org/10.1080/01621459.2018.1424632"
accessed: 2026-08-23
source_tier: A
license: "JASA article; retain citation, independent derivations, author PDF and correction link"
venue: "Journal of the American Statistical Association 115(529), 138–151"
scope_role: primary
temporal_role: modern-clarification
related: ["[[偏差—方差—噪声分解]]", "[[线性回归的统计学习理论]]", "[[正则化、交叉验证与模型选择]]"]
created: 2026-08-23
updated: 2026-08-23
---

# From Fixed-X to Random-X Regression

> [!abstract] 来源定位
> Rosset 与 Tibshirani 将 Fixed-X、Same-X 与 Random-X prediction error 明确分开，并分析新 covariates 带来的 excess bias/variance。它提醒本库：训练设计矩阵上的 fitted-value uncertainty 不等于部署到新 \(X_0\) 的 prediction risk。

## 元数据与纳入

- DOI：[JASA](https://doi.org/10.1080/01621459.2018.1424632)；
- 作者全文：[PDF](https://www.stat.cmu.edu/~ryantibs/papers/randomx-jasa.pdf)；
- 2022 correction：[DOI](https://doi.org/10.1080/01621459.2021.2016420)；
- 正式引用：Rosset, S. & Tibshirani, R. J. (2020), *JASA* 115, 138–151；
- 证据角色：Fixed-X/Same-X/Random-X object separation、random-design prediction error 与 CV training-size boundary；
- 本库不移植未经条件核对的 covariance-penalty 常数。

## 本库调用的断言

1. Fixed-X 把 training covariates 视作固定并常在相同 design points 评价；
2. Same-X 允许 training design 随机，但仍在相同 \(X_i\) 的 fresh responses 上评价；
3. Random-X 在独立新 \((X_0,Y_0)\) 上评价，最接近一般部署；
4. new-covariate randomness 可增加额外 bias/variance components；
5. leave-one-out CV 训练在 \(n-1\) 个样本上，因此只近似 full-\(n\) procedure risk。

