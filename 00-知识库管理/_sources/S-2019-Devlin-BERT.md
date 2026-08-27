---
type: source
status: verified
area: [sources, masked-language-modeling, transformers, self-supervision]
source_type: paper
title: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
author: [Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova]
year: 2019
url: "https://aclanthology.org/N19-1423/"
accessed: 2026-08-26
source_tier: A
license: "ACL Anthology open paper; retain citation and method conditions"
venue: "NAACL-HLT 2019"
scope_role: primary
temporal_role: modern-foundation
related: ["[[遮蔽预测、Teacher–Student 与自监督目标]]", "[[Transformer Encoder 与双向表示]]", "[[Decoder-Only、Prefix 与架构家族比较]]"]
created: 2026-08-23
updated: 2026-08-26
---

# BERT

> [!abstract] 来源定位
> 建立 masked language modeling 的经典程序：对 corruption 后上下文预测原 token，并在下游微调。本库调用其 mask law、conditional cross-entropy 与 pretrain–finetune mismatch，而不把 token recovery 等同于完整语言理解。

## 本库调用

1. clean sequence、mask set、corrupted input 与 target 必须分开；
2. MLM population optimum 是被遮蔽 token 的条件分布；
3. only-mask loss 的归一化决定 estimand；
4. corruption recipe 会产生 train–downstream mismatch；
5. pretext likelihood 只能由下游协议检验迁移价值。
