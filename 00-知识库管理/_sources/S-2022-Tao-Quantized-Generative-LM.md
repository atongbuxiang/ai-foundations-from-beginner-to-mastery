---
type: source
status: active
area: [sources, neural-networks, language-modeling, quantization, embedding-compression]
source_type: paper
title: "Compression of Generative Pre-trained Language Models via Quantization"
author: "Chaofan Tao; Lu Hou; Wei Zhang; Lifeng Shang; Xin Jiang; Qun Liu; Ping Luo; Ngai Wong"
year: 2022
url: "https://aclanthology.org/2022.acl-long.331/"
doi: "https://doi.org/10.18653/v1/2022.acl-long.331"
venue: "ACL 2022"
accessed: 2026-08-29
source_tier: A
license: "ACL Anthology paper（CC BY 4.0）；本库仅保存独立摘要、必要数字与链接"
scope_role: quantization-evidence
temporal_role: modern
related: ["[[Embedding 初始化、缩放、分解与量化接口]]"]
created: 2026-08-24
updated: 2026-08-29
---

# Tao et al.：生成式语言模型量化与 Embedding 边界

> [!abstract] 来源定位
> 论文研究生成式预训练模型量化，指出低容量下 word embeddings 同质化与模块权重分布差异带来的困难，并以 token-level contrastive distillation、module-wise dynamic scaling 改进。它承担“embedding 量化误差具有任务/模块结构”的经验来源；本库的标量误差界与存储账由独立推导承担。

## 证据边界

- 论文在指定 GPT-2/BART 设置中报告约 14.4x/13.4x 压缩与可比性能；
- 压缩率包含论文具体量化与训练方案，不能直接当作任意模型承诺；
- generative loss 对 output embedding/logit perturbation 的敏感性不同于只做 encoder classification；
- PTQ、QAT、distillation 与 module-wise scale 是不同干预。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| QLM-C1 | 量化可显著减少模型权重存储 | 表示 | bits/metadata/kernel 计入 | 成立 |
| QLM-C2 | 相同 bit-width 对所有模块误差相同 | 分布外推 | 动态范围与角色不同 | 错误 |
| QLM-C3 | 生成任务的 embedding 几何可能成为量化瓶颈 | 经验 | 论文模型与方法 | 原论文范围成立 |
| QLM-C4 | 论文压缩倍数保证任意 LLM 无质量损失 | 经验外推 | 模型、任务与校准依赖 | 不成立 |
