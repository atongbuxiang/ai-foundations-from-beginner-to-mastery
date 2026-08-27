---
type: source
status: verified
area: [sources, pretraining-data, c4, filtering-bias]
source_type: paper
title: "Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus"
author: "Jesse Dodge et al."
year: 2021
url: "https://aclanthology.org/2021.emnlp-main.98/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: corpus-audit
temporal_role: c4-audit
related: ["[[解析、语言识别、质量过滤与数据偏差]]", "[[Benchmark 污染、时间截止与成员重叠审计]]"]
created: 2026-08-26
updated: 2026-08-26
---

# C4 文档化审计

> [!abstract] 来源定位
> 论文追踪 C4 来源、内容和过滤影响，并展示基于词表的过滤可能不成比例地删除与少数群体相关文本。课程调用其方法论：对每个 filter 同时保存 retained/rejected slice，不能把“清洁”当无群体代价的标量。

论文观察绑定一版 C4 snapshot/filter；后续 web crawl、词表和 parser 变化必须重新测量。

