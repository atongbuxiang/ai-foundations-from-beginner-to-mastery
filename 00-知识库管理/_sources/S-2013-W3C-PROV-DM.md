---
type: source
status: verified
area: [sources, provenance, data-lineage, standard]
source_type: standard
title: "PROV-DM: The PROV Data Model"
author: "W3C Provenance Working Group"
year: 2013
url: "https://www.w3.org/TR/2013/REC-prov-dm-20130430/"
accessed: 2026-08-26
source_tier: P0
license: "W3C Recommendation; independent summary"
scope_role: provenance-model
temporal_role: stable-standard
related: ["[[数据版本、Provenance、有效 Token 与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# W3C PROV-DM

> [!abstract] 来源定位
> PROV-DM 用 Entity、Activity、Agent 及 generation/use/derivation/attribution relation 表示 provenance。课程将 raw WARC、parsed text、filtered corpus、dedup cluster、tokenized shard 和 checkpoint 建成内容寻址实体，以 pipeline run 作 activity、责任主体作 agent。

PROV graph 表达“由谁经何活动产生”，不自动验证记录真实、许可兼容或 hash 未碰撞；仍需签名、访问控制、审计和领域约束。
