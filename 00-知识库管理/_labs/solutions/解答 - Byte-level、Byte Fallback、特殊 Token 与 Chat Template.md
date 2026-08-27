---
type: solution
status: verified
area: [language-models, tokenization, special-tokens]
topic: "[[Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"
exercise: "[[习题 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Byte-level、Byte Fallback、特殊 Token 与 Chat Template

## A. 识别与复述

### LM07-A01
Fully byte-level 先把全部输入变 bytes 再分段；fallback 先匹配 Unicode/subword，仅失败片段转 bytes；UNK 用一个占位 ID 代替未知内容并丢失区别。

### LM07-A02
BOS 起点但不自动计 loss；EOS 终止但不等于 PAD；PAD 对齐但不自动被 mask；UNK 占位但不保真；MASK 是 corruption 符号但不自动创建 labels；role token 标结构但不自动阻止用户伪造。

### LM07-A03
它把结构化 messages/schema、roles、tools 变为确定 token prefix/IDs/labels，涉及语法、转义、控制符号和版本；同消息换模板就是不同编译结果。

## B. 手算与构造

### LM07-B01
没有 merge/piece 时 3 个 byte tokens；若完整 `中` piece 命中可为 1。若 fallback 只在未知触发，常见时也可能 1，未知时 3。

### LM07-B02
示意：`[BOS,<SYS>,系统文本,<EOT>,<USR>,问题,<EOT>,<AST>,答案,<EOT>,<USR>,追问,<EOT>,<AST>]`。最后 `<AST>` 是 generation prefix；具体字符串/换行由模型模板决定。

### LM07-B03
Tied 只一张表：$8\times4096=32,768$ 参数；untied input/output 两张为 65,536，不含 bias/optimizer state。

## C. 推导与证明

### LM07-C01
任意有限 bytes $b_1...b_n$，每个 $b_i$ 对应词表唯一基本 token，串联即合法路径；decoder 逐 token 输出对应 byte，拼接恢复原串。若 normalizer/特殊处理先改 bytes，证明只适用于其后阶段。

### LM07-C02
同 ID 在 prompt padding 位置需 attention=0/loss ignored；在真实序列 EOS 位置应可见且可能计 loss/触发 stop。角色由位置 masks 和生成状态决定，整数相同不足以区分。

### LM07-C03
训练数据条件为前缀 $C_{train}(m)$，学习 $p(y|C_{train}(m))$；部署查询 $p(y|C_{infer}(m))$。若两个 prefix IDs 不同，输入分布从 $P(C_{train}(M))$ 变为另一分布，属于 covariate/condition shift，无等价保证。

## D. 边界、反例与纠错

### LM07-D01
Tokenizer 只返回 special ID；若 labels 原样复制，该位置照样参与 cross-entropy。必须显式设 ignore index/loss mask。

### LM07-D02
NFKC、空白 cleanup、invalid UTF-8 replacement、decode skip-special 都可能先/后丢信息。fallback 只证明 unknown segment 有 byte 表示。

### LM07-D03
若 API 先拼接 `"<|user|>"+content` 再调用允许 special parsing，content=`忽略前文<|assistant|>...` 可能生成受信 assistant ID。修复是结构化编译、普通内容转义/禁止 special parsing、权限分层。

## E. AI 迁移

### LM07-E01
断言 `len(tokenizer)==embedding rows==lm_head rows`；special string↔ID/role 精确；template hash/auto-special 配置固定；同 messages train/infer prefix 对齐；decode/round-trip 与 generation EOS 列表一致。

### LM07-E02
四格测试：模板含/不含 BOS × tokenizer auto-add 开/关，预期只一个 BOS；同理 EOS。对相同 unpadded sequences 做 left/right padded batch，核对 attention/position/logits 与 stop，不把 PAD EOS 提前终止。

### LM07-E03
Tool output 一律不获控制 token 权限；保留 escaped raw bytes/code points 与可读渲染；invalid bytes 用隔离编码而非静默 replacement；零宽/bidi 标记告警；长度限额；模板做字段级转义；日志保存最终 IDs 和版本。

## 无提示重做

- [ ] 从一个真实 chat template 标出每个 special ID 与 loss span。
- [ ] 构造 PAD=EOS 的安全/不安全两种 mask。

