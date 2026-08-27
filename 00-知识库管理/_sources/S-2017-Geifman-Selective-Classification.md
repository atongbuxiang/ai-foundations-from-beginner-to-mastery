---
type: source
status: verified
area: [sources, uncertainty, selective-prediction]
source_type: paper
title: "Selective Classification for Deep Neural Networks"
author: "Yonatan Geifman, Ran El-Yaniv"
year: 2017
url: "https://papers.nips.cc/paper_files/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html"
accessed: 2026-08-26
source_tier: P1
license: "NeurIPS paper; independent summary"
scope_role: risk-coverage-foundation
related: ["[[Proper Scoring、Calibration、ECE 与 Selective Generation]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Selective Classification：拒答换覆盖率

> [!abstract] 来源定位
> 论文研究带 reject option 的分类器：用 confidence threshold 只回答一部分样本，以 coverage 换 selective risk。本库把 risk-coverage 曲线迁移到语言模型答案事件，同时明确原论文的分类设定不能自动解决开放生成的语义分组与错误判定。

阈值必须在 validation 选择，test 只评一次；低风险若以极低 coverage 获得，不能被描述为“模型更可靠”而不披露拒答比例。
