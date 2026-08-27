---
type: source
status: verified
area: [sources, scientific-spaces, t5, pegasus, denoising]
source_type: blog
title: "T5 PEGASUS：开源一个中文生成式预训练模型"
author: "苏剑林"
year: 2021
url: "https://spaces.ac.cn/archives/8209"
accessed: 2026-08-26
source_tier: P3
license: "科学空间 CC BY-NC-SA；本库仅保存独立摘要与链接"
scope_role: exposition-experiment
temporal_role: objective-hybrid
related: ["[[Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]", "[[Mixture-of-Denoisers、UL2 与多目标采样]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 科学空间：T5 PEGASUS

> [!abstract] 来源定位
> 文章以 mT5 为基座，使用 PEGASUS 式伪摘要预训练构建中文生成模型。课程把它作为“corruption law 应贴近下游信息结构”的案例；结果绑定中文语料、gap-sentence 选择、基座和生成评估，不能外推为所有任务的最佳 denoiser。

页面引用信息：2021-03-03。课程需另外回查 T5 与 PEGASUS 原论文，区分 sentinel span reconstruction、gap-sentence generation 和最终模型实现。

