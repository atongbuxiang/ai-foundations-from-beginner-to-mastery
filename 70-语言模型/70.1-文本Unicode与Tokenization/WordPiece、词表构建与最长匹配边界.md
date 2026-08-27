---
type: concept
status: verified
area: [language-models, tokenization, wordpiece]
node_id: LM-05
aliases: [WordPiece Tokenizer, 最长匹配分词]
prerequisites: ["[[Tokenizer 作为码本、分段路径与压缩接口]]", "[[BPE、合并规则与确定性编码解码]]"]
related: ["[[Unigram LM、Viterbi、EM 与 Subword Regularization]]", "[[Masked LM 的 Corruption Law、伪似然与 BERT]]"]
sources: ["[[S-2012-Schuster-Nakajima-WordPiece]]", "[[S-2019-Devlin-BERT]]"]
exercises: ["[[习题 - WordPiece、词表构建与最长匹配边界]]"]
solutions: ["[[解答 - WordPiece、词表构建与最长匹配边界]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-wordpiece-longest-match-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# WordPiece、词表构建与最长匹配边界

> [!abstract] 一句话结论
> WordPiece 应拆成两件事：从语料选择子词词表，以及用给定词表执行带位置约束的最长匹配。历史论文和现代库并没有给出一份跨实现完全统一的训练规范，因此任何似然增益评分、续接前缀与 unknown 行为都要绑定具体实现。

## 一、先纠正“WordPiece 就是另一种 BPE”

BPE 的核心对象是**有序 merge 列表**；常见 WordPiece encoder 的核心对象是**带词首/续接约束的词表**和 longest-match-first。两者可能得到相似子词，但训练与编码合同不同：

| 问题 | BPE 常见回答 | WordPiece 常见回答 |
|---|---|---|
| 怎样学词表 | 合并最高频 pair | 选择能改善语言/训练目标的 piece 或近似评分 |
| 怎样编码 | 按 merge rank 重放 | 从当前位置取最长合法词表项 |
| 是否需 continuation marker | 可用词尾/空格标记 | 常见 `##` 标记非词首 piece |
| 无法覆盖 | byte/char 保底或 unknown | 常见整词 `[UNK]`，但实现可变 |

`##` 是词表命名与位置约束，不是原文本真的包含两个井号。

## 二、词表学习：一个常用直觉而非唯一规范

许多教学材料用下面的关联评分说明候选合并：

$$
score(a,b)=\frac{p(ab)}{p(a)p(b)}
\quad\text{或其对数}\quad
\log p(ab)-\log p(a)-\log p(b).
$$

如果 $a,b$ 各自很常见但只偶尔相邻，分数低；若它们强关联，分数高。这比纯 pair frequency 更强调“合并是否解释了额外关联”。然而：

> [!warning] 不把二手伪代码冒充唯一 WordPiece 标准
> 早期来源[[S-2012-Schuster-Nakajima-WordPiece]]与后续生产系统的细节并不完全公开统一。上述评分是有用的建模桥梁，但正式复现必须引用库源码、trainer 版本、目标和 tie-break。

## 三、Longest-match-first 的精确定义

对一个 pre-token $x$，当前位置为 $i$：

1. 枚举终点 $j$ 从 $|x|$ 向 $i+1$ 递减；
2. 构造候选 $x_{i:j}$；若 $i>0$，按合同加 continuation prefix，如 `##`；
3. 选择第一个在词表中的候选；
4. 输出其 ID，令 $i\leftarrow j$；
5. 若没有候选，执行 unknown/fallback 合同。

伪代码：

```text
i = 0
while i < len(x):
    found = false
    for j = len(x), ..., i+1:
        piece = x[i:j] if i==0 else "##" + x[i:j]
        if piece in vocab:
            emit(piece); i = j; found = true; break
    if not found: return unknown_policy(x)
```

若用 trie，可把每个起点的查找从重复 substring 查询改为沿 trie 行走，实际复杂度依最大 piece 长度和 Unicode/pretoken 单位。

## 四、手算：`playing`

词表含

```text
play, player, ##er, ##ing, [UNK]
```

编码 `playing`：

- 词首从 `playing`、`playin`……向短匹配，首先命中 `play`；
- 当前位置移到 `i=4`，续接候选使用 `##ing`，命中；
- 结果为 `[play, ##ing]`。

编码 `player` 时可直接命中词首 token `player`；最长匹配不会继续拆为 `[play, ##er]`。两种分段都合法不代表算法会全局比较概率。

## 五、贪心可能走入死路

词表：`a, ab, ##bc`，输入 `abc`。

- 贪心第一步选最长词首 `ab`；余下 `c` 没有 `##c`，失败；
- 全局存在分段 `[a, ##bc]`。

所以 longest-match-first 不是“在所有合法分段中找 token 最少”的动态规划。许多真实 WordPiece 词表含基本字符以减少此类死路，但 unknown/fallback 策略仍需声明。

## 六、`[UNK]` 的作用域是重大语义差异

失败后至少有三种策略：

1. 整个 pre-token 输出一个 `[UNK]`；
2. 只把失败片段输出 `[UNK]`，保留已匹配部分；
3. 回退到字符/byte token，避免内容丢失。

若 `[UNK]` 把多个输入映射为同一 ID，则 decode 无法恢复原文。模型也无法区分这些输入。对低资源文字、emoji、代码和恶意 Unicode，这既是公平问题，也是安全问题。

## 七、图：局部最长与全局可行

先看图回答：为什么 `[player]` 会压过 `[play, ##er]`，而 `[ab]` 又可能导致 `abc` 失败？

![[00-知识库管理/_assets/figures/language-models/fig-lm-wordpiece-longest-match-v1.svg|900]]

> [!figure] 图 LM-05　WordPiece 的位置词表、最长匹配与贪心边界
> A 展示词首/续接 token，B 手算 `player/playing`，C 给出局部贪心失败而全局路径存在的反例。来源：本课程独立绘制。

**怎样读图**：先区分词首 token 与 `##` token，再逐位置执行最长匹配；最后用 C 检查是否错误地把贪心当全局最优。

**图没有证明什么**：反例说明算法性质，不说明真实 BERT 词表必然频繁失败；coverage 要在实际词表和语料上测量。

## 八、与 BERT 的关系

[[S-2019-Devlin-BERT]]使用 WordPiece 作为输入接口，并以 `[CLS] [SEP] [MASK]` 等特殊 token 构造任务。但：

- WordPiece 不是 BERT 架构定义；
- `[MASK]` 的 MLM 语义来自 corruption/loss 合同，不是 tokenizer 自动赋予；
- 增加 token 后必须同步 embedding/output head；
- `do_lower_case`、accent stripping、Chinese character splitting 等属于具体 tokenizer 版本。

## 九、研究与实现验收

必须记录 trainer 的实际目标、词频单位、初始 alphabet、continuation prefix、最大字符数、unknown 作用域、normalizer、pretokenizer、词表顺序/ID 和库版本。最小单测包含：

- 可被一个长 token 或多个短 token 覆盖的词；
- 贪心死路；
- 非拉丁文字、combining mark、emoji；
- 超长 pre-token；
- `[UNK]`、`[CLS]` 等字面文本与真正 special token 的区别。

下一节[[Unigram LM、Viterbi、EM 与 Subword Regularization]]将用全局路径概率替代局部最长匹配。

## 练习与独立解答

- [[习题 - WordPiece、词表构建与最长匹配边界]]
- [[解答 - WordPiece、词表构建与最长匹配边界]]

