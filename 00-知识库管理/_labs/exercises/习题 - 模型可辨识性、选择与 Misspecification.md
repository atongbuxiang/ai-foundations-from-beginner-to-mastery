---
type: exercise
status: draft
area: [learning-theory/identifiability, misspecification, model-selection]
topic: "[[模型可辨识性、选择与 Misspecification]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[模型可辨识性、选择与 Misspecification]]"]
related: ["[[解答 - 模型可辨识性、选择与 Misspecification]]", "[[正则化、交叉验证与模型选择]]"]
solution: "[[解答 - 模型可辨识性、选择与 Misspecification]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - 模型可辨识性、选择与 Misspecification

> [!abstract] 训练目标
> 能从 model map与equivalence class判断可辨识性，推导错设 MLE 的 KL target和sandwich covariance，并依据真正科学目标区分 AIC、BIC、CV与confirmatory evaluation。

## A. 识别与复述

### LT-IDM-A01

区分 global、local、generic与practical identifiability；分别给出一句数学或统计判据。

### LT-IDM-A02

区分 correct specification、pseudo-true parameter、parameter consistency、prediction consistency与mechanism recovery。

### LT-IDM-A03

说明 AIC、BIC 与 cross-validation的主要selection target、经典条件与最常见误读。

## B. 手算与数值判断

### LT-IDM-B01

证明 softmax logits (a) 与 (a+c\mathbf1) 给出相同概率。对 (a=(1,2,3))，分别写出 sum-to-zero与last-logit-zero的等价representatives。

### LT-IDM-B02

用 Gaussian family拟合一个mean为1、variance为4但非Gaussian的分布。求 pseudo-true (\mu,\sigma^2)，并指出哪些target不能由此自动保证。

### LT-IDM-B03

model 1有 (d_1=2,\ell_1=-100)，model 2有 (d_2=5,\ell_2=-96)，(n=100)。分别计算 AIC/BIC并给出选择；解释结果不同为何不矛盾。

## C. 推导与证明

### LT-IDM-C01

证明 (P_\theta=P_{\theta'}) 定义 equivalence relation，并说明 quotient (\Theta/\!\sim) 为什么比任意parameter representative更接近data可识别对象。

### LT-IDM-C02

从 expected log-likelihood推导 pseudo-true set等于 (D_{\rm KL}(P_0\|P_\theta)) minimizers；写出需要的support/finite expectation caveat。

### LT-IDM-C03

从 sample score equation的一阶Taylor expansion推导
$$
\sqrt n(\widehat\theta-\theta^\star)\Rightarrow N(0,H^{-1}JH^{-1}).
$$
何时它退化为inverse Fisher information？

## D. 边界、反例与纠错

### LT-IDM-D01

给出 structural identifiable但practically weakly identified的例子。为什么更多optimizer iterations无济于事？

### LT-IDM-D02

给出 parameter不可辨识但prediction可辨识的线性回归例子，并指出对哪些test inputs预测又不可辨识。

### LT-IDM-D03

反驳“在几十个architecture中选择validation最优者后，用同一validation score就是最终无偏性能”。设计合法修复。

## E. AI 迁移

### LT-IDM-E01

为多个LLM checkpoints/decoding policies的选择写协议：target utility、groups/time split、adaptive search log、inner selection、outer evaluation、calibration与shift。

### LT-IDM-E02

大型生成模型必然错设时，怎样报告 uncertainty？至少区分sandwich式sampling uncertainty、model uncertainty、selection uncertainty与distribution shift。

### LT-IDM-E03

有人声称“某个hidden neuron就是模型的事实核验模块”。使用 permutation/scaling symmetry 与 intervention要求审计该mechanistic claim。
