---
type: source
status: verified
area: [sources, nlp, machine-translation, metrics]
source_type: paper
title: "BLEU: a Method for Automatic Evaluation of Machine Translation"
author: "Kishore Papineni et al."
year: 2002
url: "https://aclanthology.org/P02-1040/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: bleu-definition
related: ["[[Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# BLEU：Modified Precision、几何平均与长度惩罚

> [!abstract] 来源定位
> BLEU 以多参考译文下的 clipped n-gram precision、几何平均和 corpus-level brevity penalty 评价机器翻译。本库调用精确定义、分母与 corpus 聚合；sentence BLEU 的 smoothing、tokenization 与有效阶数必须另行声明。

BLEU 衡量参考重叠，不直接判断事实、语义充分、文风或因果正确；不同 tokenizer/case/normalization 的分数不可裸比较。
