---
type: source
status: verified
area: [sources, language-modeling, unilm, attention-mask]
source_type: paper
title: "Unified Language Model Pre-training for Natural Language Understanding and Generation"
author: "Li Dong et al."
year: 2019
url: "https://arxiv.org/abs/1905.03197"
accessed: 2026-08-26
source_tier: P1
license: "论文；本库仅保存独立摘要、公式与链接"
scope_role: primary
temporal_role: unified-mask-objectives
related: ["[[Prefix LM、UniLM 与序列到序列 Mask 合同]]"]
created: 2026-08-26
updated: 2026-08-26
---

# UniLM：用 Attention Mask 统一多类语言目标

> [!abstract] 来源定位
> UniLM 在共享 Transformer 上用不同 self-attention mask 实现单向、双向和 sequence-to-sequence 预训练。课程以它说明 architecture stack、visibility relation 与 loss objective 是可分离对象；原论文任务分数绑定 2019 年模型、数据和微调协议。

## 课程调用

- 单向：位置只读给定方向前缀；
- 双向：有效 token 间全可见，但 masked targets 另由 corruption/loss 定义；
- seq2seq：source/prefix 双向，target/suffix 读全部 source 与过去 target；
- segment/position/mask convention 必须与 prediction targets 一起记录。

“一套参数可实现多 relation”是构造事实 `I`；“因而比所有独立架构更优”不是无条件结论。

