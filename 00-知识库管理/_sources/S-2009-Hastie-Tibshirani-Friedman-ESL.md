---
type: source
status: active
area: [sources, learning-theory, statistical-learning, classical-models]
source_type: book
title: "The Elements of Statistical Learning: Data Mining, Inference, and Prediction"
author: [Trevor Hastie, Robert Tibshirani, Jerome Friedman]
year: 2009
url: "https://hastie.su.domains/ElemStatLearn/"
accessed: 2026-08-23
source_tier: A
license: "Springer book; official author-hosted corrected PDF, retain citation and independent derivations"
edition: "Second Edition; corrected 12th printing, 2017"
scope_role: primary-textbook
temporal_role: classical-foundation
related: ["[[偏差—方差—噪声分解]]", "[[正则化、交叉验证与模型选择]]", "[[线性回归的统计学习理论]]", "[[逻辑回归、复合损失与概率分类]]"]
created: 2026-08-23
updated: 2026-08-23
---

# The Elements of Statistical Learning

> [!abstract] 来源定位
> ESL 是本卷经典统计学习模型的正式教材骨架：平方损失的 bias–variance decomposition、test error estimation、cross-validation、linear methods、logistic regression、trees、ensembles、kernel 与 unsupervised learning 均在同一 risk 语言下组织。

## 元数据与纳入

- 官方主页：[Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/)；
- 官方 PDF：主页提供 corrected 12th printing 下载；
- 正式引用：Hastie, T., Tibshirani, R. & Friedman, J. (2009), Springer；
- 证据角色：本卷定义顺序、经典推导、模型比较和实践接口；
- 边界：书中的 Fixed-X 直觉由 [[S-2020-Rosset-Tibshirani-Fixed-Random-X]] 进一步分层；现代高维、选择复用与深网边界另由原论文承担。

## 本库调用的断言

1. squared prediction error 可在明确随机性下分成 noise、squared bias 与 variance；
2. regularization、subset selection 与 smoothing 通过改变 effective flexibility 影响 error；
3. cross-validation 估计 procedure 的 prediction error，fold size 与依赖结构影响 bias/variance；
4. least squares、ridge 与 logistic regression 必须同时从 statistical target、optimization 与 evaluation 理解；
5. training error 不是 test error，选择过程需要独立评价。

