---
type: source
status: verified
area: [sources, ai/transformers, ai/language-modeling]
source_type: paper
title: "Improving Language Understanding by Generative Pre-Training"
author: "Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever"
year: 2018
url: "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
accessed: 2026-08-26
source_tier: A
license: "OpenAI paper; independent summary only"
scope_role: foundational
temporal_role: decoder-only-transfer
related: ["[[Transformer Decoder 与自回归因果结构]]", "[[Decoder-Only、Prefix 与架构家族比较]]"]
created: 2026-08-24
updated: 2026-08-26
---

# GPT：生成式预训练与 Decoder-only 接口

> [!abstract] 来源定位
> 论文以带 causal masked self-attention 的 Transformer decoder 做生成式语言模型预训练，再用任务感知输入变换和监督微调迁移。课程用它建立 decoder-only 的早期正式实例；现代 LLM 的规模、数据、tokenizer、normalization 与推理系统不能由该论文直接代表。

## 核心合同

$$
p(x_{1:T})=\prod_{t=1}^{T}p(x_t\mid x_{<t}).
$$

训练输入必须与 next-token targets 错位，causal mask 禁止未来可见。相同 backbone 可通过输入序列化与输出 head 进入多类任务，这说明“decoder-only”描述可见性/计算骨架，不等于任务只能是自由生成。

## 证据边界

- 架构与目标定义为 `I`；
- 原论文任务与消融为 2018 设置下的 `E`；
- “生成式预训练对所有任务最优”不成立；
- decoder-only 的现代主导地位还涉及规模、统一接口、数据、缓存与系统生态，须另立证据。
