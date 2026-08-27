---
type: exercise
status: verified
area: [language-models, deployment, monitoring, drift, incidents]
topic: "[[线上监控、Drift、反馈回路与 Incident 记录]]"
solution: "[[解答 - 线上监控、Drift、反馈回路与 Incident 记录]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 线上监控、Drift、反馈回路与 Incident 记录

## A. 识别与复述

### LM71-A01
区分 SLI、SLO、alert 与 release gate。

### LM71-A02
列出 traffic、RAG/tool、model behavior、system outcome、impact 五层监控各一个指标。

### LM71-A03
区分 covariate、label/prior、concept、measurement/policy 与 system shift。

## B. 手算与构造

### LM71-B01
离散基线 $P=(.5,.3,.2)$，当前 $Q=(.4,.35,.25)$，计算总变差 TV。

### LM71-B02
基线 $P=(.5,.5)$，当前 $Q=(.6,.4)$，按 $\mathrm{PSI}(P,Q)=\sum_j(p_j-q_j)\log(p_j/q_j)$ 计算 PSI。

### LM71-B03
一个 7 天窗有 2000 个 eligible 请求，其中 14 个确认坏事件；另有 50 个 parser failure 被错误剔除。分别计算剔除和按坏事件计入时的 SLI。

## C. 推导与证明

### LM71-C01
说明只观察 $P_t(X)$ 不能一般识别 $P_t(Y\mid X)$ 是否变化。

### LM71-C02
构造拒答导致 label missing-not-at-random 的反馈路径。

### LM71-C03
解释 canary rollout 为何应按用户/组织稳定随机而不是逐请求随机。

## D. 边界、反例与纠错

### LM71-D01
构造“drift 很大但质量不降”和“drift 很小但高危风险上升”的例子。

### LM71-D02
反驳“点赞率上升，所以模型质量提升”。

### LM71-D03
一次事故时间线上新版本发布与坏例同时出现。为什么还不能直接称新版本为 root cause？

## E. AI 迁移

### LM71-E01
为 RAG agent 写含分母、窗口、slice、CI 和 owner 的三个 SLO。

### LM71-E02
设计告警后的 triage、rollback 与证据保存 runbook。

### LM71-E03
写一个 blameless 但可问责的 postmortem 行动项。

独立完成后查看[[解答 - 线上监控、Drift、反馈回路与 Incident 记录]]。
