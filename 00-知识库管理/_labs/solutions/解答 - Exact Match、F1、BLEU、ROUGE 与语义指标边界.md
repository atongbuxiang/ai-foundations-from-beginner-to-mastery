---
type: solution
status: verified
area: [language-models, evaluation, metrics]
topic: "[[Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"
exercise: "[[习题 - Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Exact Match、F1、BLEU、ROUGE 与语义指标边界

## A. 识别与复述

### LM58-A01
Normalization 决定大小写、Unicode、标点、冠词与空白是否被视为差异；tokenization 决定计数原子；reference set 决定哪些答案被承认为正确。因此它们改变 $m(y,r)$ 本身，不是无关实现细节。必须版本化并在查看 test 之前固定。

### LM58-A02
Token F1 匹配离散 token 的多重集合；BLEU 匹配裁剪后的局部 $n$-gram precision 并加长度惩罚；ROUGE-L 用最长公共子序列保留顺序但允许间隔；contextual similarity 用编码器表示做软对齐。匹配单位越柔性，词面同义改写越容易得分，但事实正确性仍不是自动保证。

### LM58-A03
Corpus BLEU 先在全语料累加各阶 clipped counts 与候选长度，再取几何平均和一次 BP。这是“比值和再非线性变换”；逐句先做非线性再平均一般不交换，而且短句零 $n$-gram 的 smoothing 会进一步改变结果。

## B. 手算与构造

### LM58-B01
Reference 计数 $a:2,b:1,c:1$；candidate 为 $a:1,b:2,d:1$。重叠为 $\min(2,1)+\min(1,2)=2$。故 $P=2/4=.5$，$R=2/4=.5$，$F_1=.5$。

### LM58-B02
因 $c<r$，
$$
BP=\exp(1-r/c)=\exp(1-8/6)=e^{-1/3}\approx .7165.
$$
它只惩罚总体过短，不能替代内容覆盖审计。

### LM58-B03
一个 LCS 是 $(b,c,e)$，长度为 3。以候选第二序列为预测，有 $P=3/4=.75$，以第一序列为 reference，有 $R=3/5=.6$，
$$F_1=\frac{2(.75)(.6)}{.75+.6}=\frac23\approx.6667.$$

## C. 推导与证明

### LM58-C01
令 $o=\sum_t\min(c_C(t),c_R(t))$。则 $P=o/|C|$、$R=o/|R|$，代入调和平均：
$$
F_1=\frac{2PR}{P+R}
=\frac{2o^2/(|C||R|)}{o/|C|+o/|R|}
=\frac{2o}{|C|+|R|}.
$$
若 $o=0$，按约定取零。

### LM58-C02
当 $c=r$ 时 $BP=1$；当 $c<r$ 时 $1-r/c<0$，故 $0<BP<1$；$c\to r^-$ 时连续趋于 1，$c\to0^+$ 时趋于 0。候选越短惩罚越强。$c\ge r$ 时设 1，避免仅因更长获得奖励。

### LM58-C03
例如 reference “The physician bought the automobile”，candidate “The doctor purchased the car”。若 normalization 不含同义词映射，整串不同所以 EM=0，但语义可接近。反向推论无效：contextual encoder 可能忽略否定、数值或实体细节，也可能受领域外表示误差影响。

## D. 边界、反例与纠错

### LM58-D01
Reference：“药物使死亡风险降低 20%”；candidate：“药物使死亡风险提高 20%”。绝大多数 token 重合，F1 很高，但“降低/提高”使事实含义相反。词面 overlap 不应充当 entailment。

### LM58-D02
BERTScore 测 contextual token 表示的相似对齐，不检查来源、时点或世界状态。流畅地把数字 12 改成 21 仍可能很相似。因此它可补充 lexical metric，却不能独立证明 factuality。

### LM58-D03
在 test references 上尝试许多 normalization/metric，取最有利者，相当于以 test 标签选择测量函数；最高结果含 winner's curse。应在方法开发集固定规则，完整披露候选方法，test 只做一次确认或做选择校正。

## E. AI 迁移

### LM58-E01
测试应覆盖 Unicode NFC/NFKC 选择、全半角、大小写、连续空白、首尾空白、标点、冠词、数字格式与非拉丁文字。每例明确输入、预期输出和为何允许/禁止等价；保存 normalization 版本 hash。

### LM58-E02
至少报告 ROUGE 或 lexical coverage、BERTScore 等语义相似、claim-level factual precision/attribution、人工 coherence/utility；另报长度、失败与 slice。不要无依据加权成一个总分，而应观察各坐标及冲突。

### LM58-E03
对每个 document 保留 A/B 两系统分数或充分计数；以 document 为配对单位有放回重采样，重算完整 corpus metric 与差值，重复足够次数形成 percentile/BCa 区间。不能重采样单个 token，也不能把两系统拆成独立样本。
