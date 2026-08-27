---
type: exercise
status: draft
area: [learning-theory/dataset-shift]
topic: "[[Covariate、Label 与 Concept Shift]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Covariate、Label 与 Concept Shift]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Covariate、Label 与 Concept Shift
## A. 识别与复述
### LT-SHF-A01
用 joint factorization 定义 covariate、label 与 concept shift。
### LT-SHF-A02
为什么 label shift 通常改变 $P(Y\mid X)$？什么因子保持？
### LT-SHF-A03
区分 detection、diagnosis、correction 与 target evaluation。
## B. 手算与局部推导
### LT-SHF-B01
二分类 source priors $(0.8,0.2)$、target priors $(0.5,0.5)$，且 $p(x\mid y)$ 不变。写 posterior odds 的 source→target 修正因子。
### LT-SHF-B02
给 $C_s=\begin{pmatrix}.8&.2\\.2&.8\end{pmatrix}$、target prediction frequency $\mu_t=(.62,.38)^T$，求 target class priors。
### LT-SHF-B03
构造集合 $A$ 满足 target 有质量、source 无质量，说明任何 finite density ratio 的失败。
## C. 证明与反例
### LT-SHF-C01
证明 covariate shift 与 label shift 一般互不蕴含。
### LT-SHF-C02
构造 prediction-positive rate 相同但 underlying shift 不同的两个 target worlds。
### LT-SHF-C03
构造 covariate、label 与 concept shift 同时发生的例子。
## D. 审计与诊断
### LT-SHF-D01
仅有 source labels 与 target inputs 时，哪些 shift 假设可直接检查，哪些不可？
### LT-SHF-D02
审计随机打乱的时间部署 benchmark，并给正确 split 与 label-delay protocol。
### LT-SHF-D03
黑盒 label-shift estimator 的 confusion matrix 近奇异。诊断识别与数值问题。
## E. 研究与迁移
### LT-SHF-E01
为医院部署设计 feature、prior、diagnosis-rule 与 policy-feedback 四层监控。
### LT-SHF-E02
为推荐系统画 prediction→exposure→future label 的反馈数据合同。
### LT-SHF-E03
写 shift claim card：可观察证据、稳定假设、overlap、校正与 locked target test。
