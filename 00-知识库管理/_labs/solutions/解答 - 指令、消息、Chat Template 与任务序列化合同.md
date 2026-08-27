---
type: solution
status: verified
area: [language-models, instruction-tuning, chat-template]
topic: "[[指令、消息、Chat Template 与任务序列化合同]]"
exercise: "[[习题 - 指令、消息、Chat Template 与任务序列化合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 指令、消息、Chat Template 与任务序列化合同

## A. 识别与复述

### LM25-A01
语义任务是人要完成的目标；messages 是 role/content/tool 等结构记录；rendered text 是模板产出的字符序列；token IDs 是 tokenizer 后真正输入模型的整数；generation boundary 指条件前缀结束、模型开始续写的位置及停止/解析规则。前者相同不保证后四者相同。

### LM25-A02
模板决定 role markers、消息顺序、BOS/EOS/EOT、空白、escaping、tool schema 和 generation prefix，这些都改变 $p_\theta(y\mid x)$ 中的精确 $x$。它还需与训练模板匹配并可版本化，所以是编译器/模型接口，不是视觉排版。

### LM25-A03
Add-generation-prompt 在现有消息后追加“下一条 assistant 消息开始”的控制前缀；continue-final-message 把最后一条已有消息当未结束内容继续。前者开启新消息，后者续写同一消息；具体互斥和输出依 template/library 版本。

## B. 手算与构造

### LM25-B01
一种显式编译为 [BOS,SYSTEM,:,s,EOT,USER,:,q,EOT,ASSISTANT,:,a,EOT]。回答内容起点是 ASSISTANT 与冒号之后、token a 的位置。推理前缀应为 [BOS,SYSTEM,:,s,EOT,USER,:,q,EOT,ASSISTANT,:]。

### LM25-B02
若 tokenizer 再包一层，得到 [BOS_auto,BOS_template,…,EOS_template,EOS_auto]。双 BOS/EOS 改变训练前缀和停止概率；应让模板或 tokenizer 只有一方拥有插入权，并以最终 IDs 断言次数/位置。

### LM25-B03
最小路径：system? → user(content) → assistant(tool_call{id,name,args}) → tool(tool_call_id,result) → assistant(final content)。需验证 call ID 对应、schema 合法、tool result 不孤立，最后回答才进入普通 assistant 输出。

## C. 推导与证明

### LM25-C01
可写 $M_{in}\xrightarrow{T_\phi,z}s\xrightarrow{Tok_\psi}x\xrightarrow{p_\theta,\mathcal D}\hat y\xrightarrow{P_\omega}\hat M_{out}$。版本对象含 template bytes/hash 与 flags $z$、tokenizer/special map $\psi$、model $\theta$、sampler/stop $\mathcal D$、parser/schema $\omega$。

### LM25-C02
设训练编译后的回答首位置为 $b$，推理编译序列为 $x^{infer}$。断言 $x^{train}_{0:b}=x^{infer}$，并同时断言 $b=|x^{infer}|$、assistant marker 只出现预期次数。对每个 golden message 保存实际 IDs，不只比字符串。

### LM25-C03
Tokenizer revision、normalization、added-token table、special-token flag 或 byte fallback 可不同；同一 Unicode string 会被分成不同 IDs。甚至相同整数序列在不同 vocabulary 版本可映射不同 token。故还需 tokenizer hash/special map 与 encode output。

## D. 边界、反例与纠错

### LM25-D01
模型名只标权重家族；模板 A/B 产生不同 control tokens、position 和 generation prefix，条件事件不同。差分性能混入模板效应。应固定模板或做交叉 template sensitivity，并保存完整 IDs。

### LM25-D02
设 marker 是控制序列 ASSISTANT-MARK，user content 可要求原样输出同一字符序列。未 escape 的 delimiter parser 会把后半段误当 assistant message。应使用 tokenizer-recognized control token、escaping/length framing，并做 round-trip adversarial case。

### LM25-D03
最终字符串丢失原 role/name/tool-call ID、字段边界、模板源码、flags 和结构验证失败；也未保存 tokenizer/IDs。它可复现一部分 bytes，却不能恢复消息语义或证明训练/推理编译一致。

## E. AI 迁移

### LM25-E01
准备单轮、多轮、空 content、Unicode、marker-in-content、tool call、truncation cases；保存 messages→text→IDs→offsets golden；decode/parse 后检查结构；升级库/template/tokenizer 时生成逐 token diff，只有审阅后更新 golden。

### LM25-E02
无法判断 role markers、BOS/EOS、assistant prefix、tokenization、tool serialization 和 generation boundary；同一 system prompt 可对应不同 $x$。结论只能归于未完整指定的 model-system，不能复现为纯模型能力。

### LM25-E03
至少含 messages schema/version、tool schema/hash、call/result IDs、template bytes/hash、flags、tokenizer/revision/special map、rendered bytes、input IDs、assistant/tool offsets、loss mask、truncation、parser version、source/license/privacy 与 run hash。

## 无提示重做

- [ ] 手工编译一段 messages，并标训练/推理前缀边界。
- [ ] 写出 template、tokenizer、model、sampler、parser 五版本复合。

