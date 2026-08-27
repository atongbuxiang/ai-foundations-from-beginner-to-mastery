---
type: concept
status: verified
area: [language-models, tokenization, bpe]
node_id: LM-04
aliases: [BPE Tokenizer, 子词 BPE]
prerequisites: ["[[Tokenizer 作为码本、分段路径与压缩接口]]"]
related: ["[[WordPiece、词表构建与最长匹配边界]]", "[[Unigram LM、Viterbi、EM 与 Subword Regularization]]", "[[Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]"]
sources: ["[[S-2016-Sennrich-BPE-NMT]]", "[[S-2018-Kudo-Richardson-SentencePiece]]"]
exercises: ["[[习题 - BPE、合并规则与确定性编码解码]]"]
solutions: ["[[解答 - BPE、合并规则与确定性编码解码]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-bpe-merges-tie-contract-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# BPE、合并规则与确定性编码解码

> [!abstract] 一句话结论
> 子词 BPE 从基本符号开始，反复把语料中最高频的相邻 pair 合成新符号。真正可复现的模型是“预切分与边界规则 + 初始字母表 + 加权语料 + 并列规则 + 有序 merge 列表”，不是只有一个 vocab 集合。

## 一、算法从哪一个对象开始

设语料先被切成 pre-tokens。每个不同 pre-token $w$ 有频数 $c(w)$，初始表示为基本符号序列 $s(w)=(a_1,\ldots,a_k)$，常加入词尾或空格标记。

第 $r$ 轮对相邻 pair $(u,v)$ 计数：

$$
C_r(u,v)=\sum_w c(w)\sum_{i=1}^{|s_r(w)|-1}
\mathbf 1\{s_r(w)_i=u,s_r(w)_{i+1}=v\}.
$$

选择

$$
(u_r,v_r)=\operatorname*{argmax}_{(u,v)}C_r(u,v),
$$

创建新 token $u_rv_r$，并在所有序列中以**不重叠**方式替换该 pair。重复到词表大小或 merge 数达到预算。

> [!warning] `argmax` 可能不唯一
> 若多个 pair 同频，遍历顺序、lexicographic rule 或稳定 heap 规则会决定第一条 merge；第一步不同会改变后续全部计数。并列规则属于模型版本。

## 二、手算一个小语料

语料（为教学简化）为：

```text
low  ×5  → l o w </w>
lower×2  → l o w e r </w>
newest×6 → n e w e s t </w>
```

初始 pair 计数中，`(e,s)` 与 `(s,t)` 都因 `newest ×6` 出现 6 次；`(l,o)` 与 `(o,w)` 各有 7 次，因为 `low` 和 `lower` 共享前缀。若先合并 `(l,o)→lo`：

```text
lo w </w>       ×5
lo w e r </w>   ×2
n e w e s t </w>×6
```

下一轮 `(lo,w)` 计数为 7。注意计数按**语料频数加权**；若只对 unique word type 计数，算法已改变。

## 三、重叠 pair 怎样替换

对序列 `a a a`，pair `(a,a)` 有两个位置重叠。一次 merge 不能同时把两对都合并成两个 token，因为中间 `a` 被重复使用。常见左到右不重叠替换得到 `aa a`。不同重叠处理会改变语料状态，必须固定。

## 四、训练得到的不是无序词表

设 merges 为

```text
rank 0: e s   → es
rank 1: es t  → est
rank 2: l o   → lo
```

编码新 pre-token 时，从基本符号开始，只应用词内当前可用且 rank 最小的 merge，直到不可合并。最终 token 集相同但 rank 不同，可能产生不同分段。

### 一个 rank 反例

初始 `a b c`，词表同时含 `ab` 与 `bc`：

- 若 `(a,b)` rank 更小：`ab c`；
- 若 `(b,c)` rank 更小：`a bc`。

因此 `vocab.json` 不能唯一恢复 BPE encoder。

## 五、BPE、byte-level BPE 与 BytePair compression 不是同一合同

- 原始 compression BPE 在 byte sequence 上替换高频 digram；
- NLP subword BPE 常从字符/预切分词内部开始，带词边界标记；
- byte-level BPE 先把 UTF-8 bytes 映为可显示基本符号，再学习 merges；
- 某些实现仍有 regex pre-tokenizer，不允许 merge 跨其边界。

“byte-level”保证基本 byte 可表示，不代表 normalization、invalid byte、special token 或 decode 全部自动无损。

## 六、复杂度与工程结构

最朴素实现每轮重扫全部语料并重算 pair，代价很高。实际系统使用：

- pair→frequency 的哈希表；
- pair→occurrence positions 的倒排索引；
- 带 lazy invalidation 的 priority queue；
- 并行计数、分片归并与 deterministic reduction。

性能优化不得改变并列与替换语义。浮点权重、分布式规约顺序或非稳定容器都可能使近似同频 pair 分叉。

## 七、图：合并与并列分叉

先看图回答：为什么同样的目标词表大小仍可能得到不同 tokenizer？

![[00-知识库管理/_assets/figures/language-models/fig-lm-bpe-merges-tie-contract-v1.svg|900]]

> [!figure] 图 LM-04　BPE 的 pair 计数、全局重写与同频分叉
> A 展示加权语料计数，B 展示有序 merge 重放，C 展示同频 pair 的不同选择产生不同分段。来源：本课程依据 Sennrich 等的子词 BPE 算法独立绘制。

**怎样读图**：先核对频数是否乘入计数，再检查 merge rank，最后追踪 tie 如何改变后续语料状态。

**图没有证明什么**：示例不证明某个 tie-break 更好，也不代表所有库对词边界、重叠和 byte mapping 使用相同规则。

## 八、BPE 的归纳偏置与边界

BPE 偏好把高频局部共现固化为单 token。这可缩短常见片段，但：

- 高频不等于语义完整；token 可能跨词素或代码结构；
- 稀有拼写会被切得很长；
- 语料频率与领域、语言比例强耦合；
- 一旦 merge，标准 BPE 不会在后续训练中主动拆除低效 token；
- deterministic segmentation 缺少 Unigram sampling 的分段噪声。

这些是归纳偏置，不是算法错误。是否有害必须由压缩、训练预算、下游质量和公平切片共同判断。

## 九、最小模型卡与复现门

必须保存：

```yaml
corpus_hash: ...
normalization: NFC / identity / ...
pretokenizer: regex + version
initial_alphabet: codepoints / byte-map
word_boundary: ...
count_weight: document/token frequency
tie_break: lexical / stable-first / ...
overlap_rule: left-to-right non-overlap
merges: ordered list + hash
special_tokens: ids and roles
implementation_version: ...
```

最小测试包含重复符号、同频 pair、空格、组合字符、emoji、未知 byte 与特殊 token；断言 encode 确定、decode 满足承诺的 round-trip。

## 十、本节出口

[[S-2016-Sennrich-BPE-NMT]]提供开放词表 NMT 的历史主线，但其任务结果不证明 BPE 普适最优。下一节[[WordPiece、词表构建与最长匹配边界]]将看到“词表如何学”和“给定词表怎样编码”可以是不同算法。

## 练习与独立解答

- [[习题 - BPE、合并规则与确定性编码解码]]
- [[解答 - BPE、合并规则与确定性编码解码]]
