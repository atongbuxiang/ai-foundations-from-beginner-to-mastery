---
type: solution
status: verified
area: [language-models, tokenization, bpe]
topic: "[[BPE、合并规则与确定性编码解码]]"
exercise: "[[习题 - BPE、合并规则与确定性编码解码]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - BPE、合并规则与确定性编码解码

## A. 识别与复述

### LM04-A01
编码从基本符号开始按 rank 应用 merge。若 `ab`、`bc` 都在词表，`abc` 可成 `[ab,c]` 或 `[a,bc]`；无序集合不告诉先合哪个。

### LM04-A02
需固定：原文本如何预切分；基本是字符还是 byte-map；是否有词首/尾/空格标记；pair count 是否乘词频；同频如何打破；`aaa` 中重叠 pair 如何非重叠替换。任一项改变 merges。

### LM04-A03
Subword BPE 是 NLP 分词适配，常在 pre-token 内合并；byte-level 从 UTF-8 byte 映射起步但可仍有 pretokenizer；原始 compression BPE 是一般 byte digram 替换，不含 NLP special/word boundary 合同。

## B. 手算与构造

### LM04-B01
`aa×2` 贡献 `(a,a)` 两次（每个词一次×2），`ab×1` 贡献 `(a,b)` 一次；选 `(a,a)`，新 token `aa`，语料 `aa×2, a b×1`。

### LM04-B02
rank0 合 `(b,c)` 得 `[a,bc]`，此时 `(a,b)` 不再可用。交换后先合 `(a,b)` 得 `[ab,c]`。

### LM04-B03
`a a a a` 左到右不重叠得到 `[aa,aa]`，发生两次替换。若序列 `aaa` 则只得到 `[aa,a]`。

## C. 推导与证明

### LM04-C01
每替换一个非重叠 pair，用一个新符号代替两个，长度减 1；未出现则不变。选择的 pair 在训练语料计数正，因此至少一次，严格减少其非重叠 occurrence 数。

### LM04-C02
取 `abc`，`ab` 与 `bc` 同频。先合 `ab` 会删除该位置上的 `bc` occurrence，并新建 `ab,c`；反之删除 `ab` 并新建 `a,bc`。下一轮候选集合已不同，递归导致最终分叉。

### LM04-C03
$C(u,v)=\sum_wc(w)\sum_i1\{s_i=u,s_{i+1}=v\}$。若 `aa` 频数 100、`bc` 频数 1，type 等权给两 pair 各 1，token frequency 给 100 vs 1；argmax 可改变。

## D. 边界、反例与纠错

### LM04-D01
词表 `{a,b,c,ab,bc}` 相同，merges 顺序 `(a,b)<(b,c)` 与相反顺序分别编码 `[ab,c]`、`[a,bc]`。

### LM04-D02
若 byte-level 前先 NFKC/折空格，或 decoder cleanup 改空格，decode 只恢复处理后 bytes；若 invalid UTF-8 被替换也丢信息。byte alphabet 覆盖不是全管线可逆证明。

### LM04-D03
并行 shard 的哈希遍历/规约顺序可在同频候选中变化；lazy heap 更新和 occurrence replacement 也可能非稳定。需要精确 tie key、确定规约、语料顺序与 merges hash，不只 seed。

## E. AI 迁移

### LM04-E01
同频 tie 固定；重复符号 overlap；rank 冲突 `abc`；空格/word boundary；Unicode/byte round-trip；还可加 special token 字面串与 unknown bytes。

### LM04-E02
禁止跨空格使词边界稳定、词表更可解释，但代码中的空格/缩进模式不能合并；允许跨空格可压缩常见短语/代码格式，却更绑定语料排版并增加 prompt/control 边界风险。用相同语料分组测长度与下游质量。

### LM04-E03
序列线性项约降 15%，attention pairwise 部分约降 $1-.85^2=27.75\%$，但大词表增加 embedding/output softmax、参数/通信/缓存；batch packing/kernel 也变。必须实测总 FLOPs、wall time、显存和质量，不能线性推出 15%。

## 无提示重做

- [ ] 手算一个含同频与 overlap 的三轮 BPE。
- [ ] 仅给 vocab/merges，判断还缺哪些文本接口字段。
