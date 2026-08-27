---
type: source
status: verified
area: [sources, multilingual, pretraining-data, data-mixture]
source_type: paper
title: "mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer"
author: "Linting Xue et al."
year: 2021
url: "https://aclanthology.org/2021.naacl-main.41/"
accessed: 2026-08-26
source_tier: P1
license: "ACL paper; independent summary"
scope_role: multilingual-mixture
temporal_role: modern-foundation
related: ["[[数据混合、温度采样、重加权与域损失]]", "[[解析、语言识别、质量过滤与数据偏差]]"]
created: 2026-08-26
updated: 2026-08-26
---

# mT5：多语言数据采样

> [!abstract] 来源定位
> mT5 在 mC4 的 101 种语言上使用 $p(L)\propto n_L^\alpha$ 调整资源不平衡，并在论文设置中选用特定 $\alpha$。课程用它推导温度/幂次采样与 exposure epoch，不把低资源 oversampling 自动等同于公平或无过拟合。

语言识别错误、页面与 token 单位、tokenizer fertility 会使名义 language share 与有效 loss share 不同。

