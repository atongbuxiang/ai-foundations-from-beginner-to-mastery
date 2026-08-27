---
type: source
status: verified
area: [sources, reliability, incident-response, ml-systems]
source_type: official-book-chapter
title: "Postmortem Culture: Learning from Failure"
author: "Google Site Reliability Engineering"
year: 2026
url: "https://sre.google/sre-book/postmortem-culture/"
accessed: 2026-08-26
source_tier: B
scope_role: incident-workflow
temporal_role: current-access
related: ["[[NaN、Inf、梯度爆炸与训练失败决策树]]", "[[训练实验协议、事故记录与因果证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Google SRE：Blameless Postmortem

> [!abstract] 来源定位
> SRE 的 postmortem 将 impact、detection、timeline、mitigation、root/contributing causes 和 action items 固化为可学习记录。本卷把这一结构迁移到训练事故。

## 本卷调用

- 保存 first signal、first bad event、影响范围、处置和恢复时间线；
- 区分 trigger、proximate mechanism、contributing condition 与 latent control gap；
- 行动项需有 owner、验证方法和到期条件；
- blameless 表示关注系统条件，不表示取消可证伪性和责任边界。

## 边界

postmortem 是组织学习结构，不自动证明 root cause；根因断言仍需日志、重放与干预证据。
