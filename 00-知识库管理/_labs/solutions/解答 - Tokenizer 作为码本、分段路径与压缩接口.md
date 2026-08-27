---
type: solution
status: verified
area: [language-models, tokenization, information-theory]
topic: "[[Tokenizer 作为码本、分段路径与压缩接口]]"
exercise: "[[习题 - Tokenizer 作为码本、分段路径与压缩接口]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Tokenizer 作为码本、分段路径与压缩接口

## A. 识别与复述

### LM03-A01
$N$ 规范化/预切分，$\Sigma$ 是基本单元，$V$ 是普通 token 字符串，$C$ 是控制 token，$A$ 从合法分段中选路径，$id$ 映整数，$D$ 解码。任一项改变都可能改变 IDs 或可逆性。

### LM03-A02
完备覆盖只要求每个输入有编码路径；UNK 让函数总返回却多对一；无损 round-trip 还要求 decode(encode(x)) 在承诺层次等于 x。byte fallback 可覆盖且保留，UNK 通常不保留。

### LM03-A03
同词表可配 longest-match、最少 token、BPE rank、Viterbi score 或随机后验，输出路径不同；normalizer/pretokenizer 与 special handling 也可不同。

## B. 手算与构造

### LM03-B01
路径：`[a,b,c]`、`[ab,c]`、`[a,bc]`、`[abc]`，共 4 条。

### LM03-B02
A：3 bytes/token、1/3 token/byte；B：4 bytes/token、1/4 token/byte。固定宽 ID 下界分别 $\log_2 256=8$ bits/token 与 $\log_2 1024=10$ bits/token；每原始 byte 下界 A 为 $8/3$ bits，B 为 $10/4=2.5$ bits。注意这不是含码本的完整压缩率。

### LM03-B03
新增词表 18,000；untied 两张矩阵新增 $2\times18000\times512=18,432,000$ 参数，不含 bias/optimizer states。

## C. 推导与证明

### LM03-C01
若 A 是从字符串域到 token 序列像集的一一映射，D=A^{-1}，把 $P_Z$ 推回字符串即可定义 $P_X(x)=P_Z(A(x))$，归一化由双射保持。随机分段时一个 x 对多个 z，需 $\sum_zP(z,A\text{ maps to }x)$；normalization/UNK 多对一时还需对原像分配质量，简单等式不唯一。

### LM03-C02
自然 NLL $L=-\ln p(z)$，换成 bits 除以 $\ln2$，再除 raw byte 数 B：$BPB=L/(B\ln2)$。

### LM03-C03
pairwise $O(T^2d)\to O(r^2T^2d)$；投影/FFN $O(Td^2)\to O(rTd^2)$。softmax 随词表、padding/batch 和硬件改变，不能说总 FLOPs 必为 $r^2$。

## D. 边界、反例与纠错

### LM03-D01
令 N 把连续空格折成一个，A/D 对 normalized text 无损。原始 `a␠␠b` 编码解码为 `a␠b`，满足 D(A(x))=N(x) 但不等于 x 的 bytes。

### LM03-D02
一个把整篇文档作为单 token 的词表令 T=1，却词表无限、无法泛化、embedding 巨大且新文档 OOV。实际需在覆盖、参数、统计、计算和任务质量间权衡。

### LM03-D03
PPL 是平均每 token NLL 的指数，token 长度/字母表不同使分母不同。一个 tokenizer 可用更长 token 得到较低数值而字符串概率未改善；应在相同 bytes 上比较 total NLL/BPB。

## E. AI 迁移

### LM03-E01
训练语料/hash、encoding/Unicode/normalization、pretokenizer、basic alphabet、algorithm/objective/tie、vocab/merges/scores、special IDs、fallback/UNK、decoder cleanup、chat template、库版本/license、评估切片与 hashes。

### LM03-E02
固定 raw bytes：相同内容，比较 token/FLOPs/质量，compute 不同；固定 token budget：训练 steps/序列相同，但原始内容量不同。前者估计每原始数据的效率，后者估计每 token 预算行为。

### LM03-E03
按 code/中文/emoji 与混合边界分组；测 round-trip、UNK/fallback、tokens/byte/grapheme 的 median/P95/P99/max、截断、特殊/控制字符；保留最差样例并验证 decode 和日志一致。

## 无提示重做

- [ ] 给新词表画 `abc` lattice 并分别求最短/最大概率路径。
- [ ] 从词表与 token 长度估计 embedding 与 attention 的相反成本。

