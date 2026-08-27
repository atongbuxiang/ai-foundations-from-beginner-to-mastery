---
type: source
status: verified
area: [sources, mechanistic-interpretability, induction-heads]
source_type: research-article
title: "In-context Learning and Induction Heads"
author: "Catherine Olsson et al."
year: 2022
url: "https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/"
accessed: 2026-08-26
source_tier: P1
license: "Transformer Circuits; independent summary"
scope_role: mechanistic-evidence
related: ["[[Induction Head、机制回路与因果干预边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Induction Head：模式复制回路与证据层级

> [!abstract] 来源定位
> 研究以重复随机 token 定义 prefix matching 与 copying 行为，在两层 attention-only 模型中解析 previous-token head 加 induction head 回路，并用训练期共现、ablation 等证据讨论大模型 ICL。

小模型中的精确机制证据不能原样升级到含 MLP 的大模型；attention pattern、相关共现和单头消融分别是不同强度的证据。
