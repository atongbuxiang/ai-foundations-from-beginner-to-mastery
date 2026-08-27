---
type: source
status: verified
area: [sources, language-models, chat-templates, implementation]
source_type: official-docs
title: "Chat templates"
author: "Hugging Face Transformers"
year: 2026
url: "https://huggingface.co/docs/transformers/chat_templating"
accessed: 2026-08-26
source_tier: P0
license: "Official documentation; independent summary"
scope_role: executable-serialization-contract
temporal_role: versioned-current-docs
related: ["[[指令、消息、Chat Template 与任务序列化合同]]", "[[监督微调、Teacher Forcing 与 Response-only Loss]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Hugging Face Chat Templates

> [!abstract] 来源定位
> 官方文档定义 role/content 消息如何由 tokenizer 绑定的 Jinja template 编译为字符串或 token IDs，并区分 add_generation_prompt、continue_final_message、special token 与 tokenize 步骤。课程把 template 文本、tokenizer 版本、调用参数和输出 IDs 视为同一可执行合同。

文档随 Transformers 版本变化；任何实验需保存库版本、模型仓库 revision、chat_template 内容、special-token map 与实际序列，而不能只写模型家族名。

