---
type: exercise
status: draft
area: [generative-models, continuous-normalizing-flows]
topic: "[[Continuous Normalizing Flow、Liouville 与 FFJORD]]"
solution: "[[解答 - Continuous Normalizing Flow、Liouville 与 FFJORD]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Continuous Normalizing Flow、Liouville 与 FFJORD
## A. 识别与复述
### GEN39-A01
写出 CNF 状态 ODE 与 instantaneous change-of-variables。
### GEN39-A02
理论 ODE flow 可逆需要哪些核心条件？
### GEN39-A03
解释 NFE、solver step 与“一次 forward”的区别。
## B. 手算与建模
### GEN39-B01
$\dot z=2z$，区间长度 $0.5$。求生成尺度和 log-density change。
### GEN39-B02
二维 $f(z)=(az_1,bz_2)$。求 divergence 和长度 $T$ 的 log-density change。
### GEN39-B03
$J=\operatorname{diag}(1,3)$，算 Rademacher probe 的 $v^TJv$，并说明方差。
## C. 推导与证明
### GEN39-C01
从 $\log\det(I+\Delta tJ)$ 一阶展开推导 instantaneous formula。
### GEN39-C02
说明 ODE 轨迹为何在唯一性条件下不能相交。
### GEN39-C03
写出反向评价 data density 时的状态与 log-density积分合同。
## D. 边界、反例与纠错
### GEN39-D01
反驳“连续动力学可逆，所以 Euler 离散程序精确可逆”。
### GEN39-D02
反驳“Hutchinson trace 无偏，所以最终 CNF likelihood 无偏”。
### GEN39-D03
说明 stiffness 如何让固定模型的 NFE 激增。
## E. AI 迁移
### GEN39-E01
设计 CNF tolerance sweep。
### GEN39-E02
比较 continuous adjoint 与 backprop through solver 的审计项。
### GEN39-E03
审计“free-form continuous dynamics 无架构限制”的说法。
## 解答入口
[[解答 - Continuous Normalizing Flow、Liouville 与 FFJORD]]

