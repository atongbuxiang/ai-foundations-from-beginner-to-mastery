---
type: source
status: active
area: [sources, online-learning, online-to-batch, generalization]
source_type: paper
title: "On the Generalization Ability of On-Line Learning Algorithms"
author: [Nicolò Cesa-Bianchi, Alex Conconi, Claudio Gentile]
year: 2004
url: "https://doi.org/10.1109/TIT.2004.833339"
accessed: 2026-08-23
source_tier: A
license: "Scholarly source; retain citation and theorem conditions"
venue: "IEEE Transactions on Information Theory 50(9)"
scope_role: primary
temporal_role: foundational
related: ["[[Online-to-Batch Conversion]]", "[[Perceptron Mistake Bound 与 Margin]]"]
created: 2026-08-23
updated: 2026-08-23
---
# On the Generalization Ability of On-Line Learning Algorithms
> [!abstract] 来源定位
> 把任意在线分类/回归算法转为带 data-dependent tail bound 的 batch predictor。本库调用 prequential、randomized/selected iterate 与 tail-risk 接口。
## 本库调用
1. online-to-batch protocol；
2. fresh-example evaluation；
3. risk tail bounds；
4. online algorithm aggregation/selection；
5. iid 与依赖序列边界。
