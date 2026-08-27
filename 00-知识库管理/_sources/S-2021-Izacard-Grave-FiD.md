---
type: source
status: verified
area: [sources, language-models, rag]
source_type: paper
title: "Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering"
author: "Gautier Izacard; Edouard Grave"
year: 2021
url: "https://arxiv.org/abs/2007.01282"
accessed: 2026-08-26
source_tier: P1
license: "Paper; independent summary"
scope_role: context-fusion
related: ["[[Context Construction、Citation、Grounding 与冲突证据]]"]
created: 2026-08-26
updated: 2026-08-26
---

# FiD：独立编码 passage、在 decoder 中融合

> [!abstract] 来源定位
> Fusion-in-Decoder 将 question 与各 passage 分别编码，再让 decoder 对拼接的编码状态做交叉注意力。课程用它说明上下文融合位置会改变计算量与证据交互方式。

增加 passage 数的收益是论文中的经验结果；噪声、截断与注意力预算仍可能使更多上下文有害。
