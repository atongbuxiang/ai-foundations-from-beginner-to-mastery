---
type: exercise
status: draft
area: [learning-theory/covariate-shift, importance-weighting]
topic: "[[重要性加权与 Covariate Shift 校正]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 重要性加权与 Covariate Shift 校正]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - 重要性加权与 Covariate Shift 校正
## A. 识别与复述
### LT-IW-A01
写 target-risk identity 的条件、ratio 与结论。
### LT-IW-A02
区分 true、estimated、clipped 与 self-normalized weights。
### LT-IW-A03
为什么 estimator 无偏不等于 learned predictor 的 target risk 小？
## B. 手算与局部推导
### LT-IW-B01
weights $(1,1,1,7)$、losses $(0,1,0,1)$，计算 unnormalized weighted mean、self-normalized risk 与 ESS。
### LT-IW-B02
balanced domain classifier 给 $r(x)=0.8$，求 $p_t(x)/p_s(x)$；若 target sampling prior $\rho=0.2$ 再求。
### LT-IW-B03
对 $0\le\ell\le L$ 推导 clipping bias bound，并解释 tail mass。
## C. 证明与反例
### LT-IW-C01
逐积分证明 covariate-shift change-of-measure identity。
### LT-IW-C02
构造 true-weight estimator 无偏但方差随稀有区域概率爆炸的例子。
### LT-IW-C03
构造 concept shift，使 perfect $p_t(x)/p_s(x)$ weighting 仍给错误 target risk。
## D. 审计与诊断
### LT-IW-D01
设计 ratio cross-fitting、weighted validation 与 locked target test。
### LT-IW-D02
报告只给 mean weight=1。还必须报告哪些 tail/overlap diagnostics？
### LT-IW-D03
比较 domain-classifier odds、KMM 与 explicit density estimation 的假设和失败。
## E. 研究与迁移
### LT-IW-E01
为医疗 site shift 设计 clip-threshold × ESS × target-risk sensitivity study。
### LT-IW-E02
为推荐曝光 propensity weighting 说明 overlap 与 feedback 边界。
### LT-IW-E03
写 importance-weighting claim card，拒绝哪些 concept/support 外推？
