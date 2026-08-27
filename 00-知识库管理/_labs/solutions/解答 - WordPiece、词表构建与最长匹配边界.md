---
type: solution
status: verified
area: [language-models, tokenization, wordpiece]
topic: "[[WordPiece、词表构建与最长匹配边界]]"
exercise: "[[习题 - WordPiece、词表构建与最长匹配边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - WordPiece、词表构建与最长匹配边界

## A. 识别与复述

### LM05-A01
词表学习决定哪些 piece/位置形式进入 $V$，可能用似然增益近似或专有 trainer；编码是给定 $V$ 后从每个位置取最长合法项。二者可独立变化。

### LM05-A02
`##ing` 表示该 piece 只允许出现在 pre-token 非首位置；它不是原文的井号，也不自动表示英语词素或空格。

### LM05-A03
历史论文给出早期方法/应用，但现代 BERT/Hugging Face 等在 normalization、continuation、unknown、训练评分上有具体版本。把二手统一描述投射回历史会制造伪规范。

## B. 手算与构造

### LM05-B01
`player` 首步最长直接命中 `[player]`。`playing` 无整词，词首最长命中 `play`，余串在非首位置命中 `##ing`，结果 `[play,##ing]`。

### LM05-B02
Greedy 先取 `ab`，余 `c` 需要 `##c`，不存在而失败/UNK。全局路径 `[a,##bc]` 合法。

### LM05-B03
score $=.3/(.4\cdot.5)=1.5$；自然 log-score $\ln1.5\approx0.4055$。这只是给定评分定义的手算，不证明真实 trainer 使用它。

## C. 推导与证明

### LM05-C01
上题即反例：最少 token 的可行路径 `[a,##bc]` 有 2 个，而 greedy 选择 `ab` 后死路。只要较长局部 prefix 阻断后缀、较短 prefix 与长 continuation 可覆盖，就产生此结构。

### LM05-C02
每个当前位置沿 trie 最多走 $L$ 个基本单元；输出 piece 后前进至少 1，最坏约 $O(nL)$，空间为 trie 词表字符总量。若回退/substring 构造额外复制，实际界会变。

### LM05-C03
若未知词 `x\ne y` 都编码为单 ID `[UNK]`，则 A(x)=A(y)。任何确定 decoder 对 `[UNK]` 只能给同一输出，不能同时等于 x 与 y，故不可逆。

## D. 边界、反例与纠错

### LM05-D01
不同 trainer 可用不同 likelihood approximation、候选生成、词频、剪枝甚至未公开细节；现代库也可实现自己的 WordPiece trainer。必须引用版本源码，不能把教学 score 当定义。

### LM05-D02
“所有 Unicode 字符”依赖 Unicode 版本且词表有限；pretokenizer 可能生成超长/受限单元，normalizer 可产生新序列，invalid bytes 不是 Unicode 字符，continuation-position 形式也可能缺失。

### LM05-D03
整词策略把全部变 `[UNK]`；局部策略可能保留已匹配 prefix；byte fallback 保留原内容但长度增加。模型可见信息、token 数、decode 和安全日志都不同。

## E. AI 迁移

### LM05-E01
读取 Unicode/clean text/lowercase/accent/Chinese split、whitespace/control、pretokenizer、continuation prefix、max chars per word、UNK scope、vocab/IDs、CLS/SEP/MASK/PAD/BOS/EOS、自动添加规则、decode cleanup 与库版本。

### LM05-E02
用 `V={a,ab,##bc}` 断言 `abc` 的预期 unknown；加入基本 continuation 后再测。构造长度超过 max chars 的 `a...a`，检查是整词 UNK、分块、报错还是 byte fallback，并测复杂度上界。

### LM05-E03
固定 raw corpus、Unicode/pretoken 边界、词表大小、模型架构/参数、训练 FLOPs/steps、seed 与评估；分别报告 tokenizer 静态指标和下游结果。最好交叉：同算法多词表、同词表预算多算法，避免单一 checkpoint 归因。

## 无提示重做

- [ ] 对新词表逐字符执行 longest-match。
- [ ] 构造第二个 greedy 失败但 DP 成功的例子。

