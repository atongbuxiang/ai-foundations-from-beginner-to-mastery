---
type: source
status: verified
area: [sources, neural-networks, tokenization, special-tokens, huggingface]
source_type: official-docs
title: "Transformers Tokenizer and Special Tokens"
author: "Hugging Face Contributors"
year: 2026
url: "https://huggingface.co/docs/transformers/main_classes/tokenizer"
accessed: 2026-08-26
source_tier: B
license: "Hugging Face official documentation；本库仅保存独立摘要、接口事实与链接"
scope_role: implementation-contract
temporal_role: current-api
related: ["[[Padding、Mask、特殊符号与词表边界]]"]
created: 2026-08-24
updated: 2026-08-26
---

# Hugging Face：Tokenizer、Padding 与 Special Tokens

> [!abstract] 来源定位
> 当前官方文档描述 tokenizer 的 token/id 转换、padding/truncation、attention mask、special token registration 与 vocabulary resize 边界。它承担工具链事实；BOS/EOS/PAD 等角色的模型语义仍由具体 architecture、training objective 和 generation protocol 定义。

## 当前接口事实

- tokenizer 管理 BOS、EOS、UNK、SEP、PAD、CLS、MASK 与额外 model-specific special tokens；
- padding side、truncation side、是否自动添加 special tokens 都是显式配置；
- 增加新 token 后，模型 embedding table 必须同步 resize；
- 把 token 标记为 special 会影响拆分/解码等 tokenizer 行为，不自动定义 attention 或 loss mask；
- `attention_mask` 是模型输入之一，其 0/1 convention 应由具体模型接口确认。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| HFT-C1 | 添加词表项后必须同步模型 embedding 尺寸 | API | 使用新增 ID | 成立 |
| HFT-C2 | token 被注册为 special 就自动从 loss 移除 | 语义外推 | loss labels/mask 另行构造 | 错误 |
| HFT-C3 | PAD、EOS 可以任意交换而无部署影响 | 角色混淆 | generation stop 与 batching 不同 | 错误 |
| HFT-C4 | padding/truncation side 是模型无关细节 | 部署外推 | position/generation contract 依赖 | 不成立 |
