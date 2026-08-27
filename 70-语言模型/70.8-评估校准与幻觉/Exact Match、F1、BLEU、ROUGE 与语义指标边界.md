---
type: concept
status: verified
area: [language-models, evaluation, metrics]
node_id: LM-58
aliases: [文本生成指标, 字符串与语义指标]
prerequisites: ["[[语言模型评估对象、任务单位与 Benchmark 合同]]"]
related: ["[[Hallucination、Factuality、Grounding 与 Attribution 分解]]", "[[LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"]
sources: ["[[S-2002-Papineni-BLEU]]", "[[S-2004-Lin-ROUGE]]", "[[S-2020-Zhang-BERTScore]]"]
exercises: ["[[习题 - Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"]
solutions: ["[[解答 - Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-eval-metric-anatomy-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Exact Match、F1、BLEU、ROUGE 与语义指标边界

> [!abstract] 一句话结论
> 指标是“输出—参考—规范化—匹配—聚合”的完整程序。EM、token F1、BLEU、ROUGE 与 embedding metric 使用不同匹配单位和归纳偏置；任何一个高分都不自动等于语义正确、事实可靠或用户偏好更高。

## 一、先固定 normalization 与 reference

令原输出 $y$、参考集 $\mathcal R=\{r_1,\ldots,r_K\}$、规范化函数 $N$。大小写、Unicode、标点、冠词、空白、数字、单位与同义答案怎样处理，必须版本化。

Exact Match 常写为

$$
\operatorname{EM}(y,\mathcal R)
=\max_{r\in\mathcal R}\mathbf1[N(y)=N(r)].
$$

EM 清晰但脆弱：“4”“four”“4.0”是否等价完全取决于 $N$。过度 normalization 又会把“not safe”与“safe”之类关键差别抹掉。

## 二、Token F1 的多重集合

把候选与参考 token 视为 multiset，交集计数

$$
M=\sum_w\min(c_y(w),c_r(w)).
$$

于是

$$
P=\frac{M}{|y|},\qquad
R=\frac{M}{|r|},\qquad
F_1=\frac{2PR}{P+R}.
$$

若候选或参考为空，要预先定义 $0/0$。多参考可取最大 F1 或其他聚合。Token F1 忽略顺序：候选把词完全打乱仍可能得满分；重复 token 由 multiset count 截断，不应按 set 计算。

## 三、BLEU 的四个部件

BLEU 的 modified n-gram precision 对每个 n-gram 的候选计数按多参考最大计数 clip：

$$
p_n=
\frac{\sum_g\min(c_y(g),\max_{r\in\mathcal R}c_r(g))}
{\sum_gc_y(g)}.
$$

再取加权几何平均并乘 brevity penalty：

$$
\operatorname{BLEU}
=BP\exp\left(\sum_{n=1}^Nw_n\log p_n\right),
$$

$$
BP=
\begin{cases}
1,&c>r,\\
\exp(1-r/c),&c\le r.
\end{cases}
$$

$c$ 是候选 corpus 长度，$r$ 是按规则选取的有效参考长度。若任一 $p_n=0$，无 smoothing 时整体为 0。原始 BLEU 是 corpus-level 设计；sentence BLEU、smoothing、effective order、tokenizer/case 会显著改变小样本分数。

## 四、ROUGE-N 与 ROUGE-L

ROUGE-N 的经典方向偏 recall：

$$
\operatorname{ROUGE\mbox{-}N}
=\frac{\sum_{r\in\mathcal R}\sum_{g\in r}
\min(c_y(g),c_r(g))}
{\sum_{r\in\mathcal R}\sum_{g\in r}c_r(g)}.
$$

具体实现的多参考聚合可能不同。ROUGE-L 使用 longest common subsequence 长度 $LCS(y,r)$：

$$
P_{LCS}=\frac{LCS(y,r)}{|y|},
\quad
R_{LCS}=\frac{LCS(y,r)}{|r|},
$$

再算带 $\beta$ 的 F measure。LCS 保留顺序但不要求连续；两个文本可共享长骨架却在否定词、数字或实体上相反。

## 五、Contextual similarity

BERTScore 一类指标取上下文化 token embedding，相似矩阵

$$
s_{ij}=\cos(e_i^y,e_j^r),
$$

候选 precision 常对每个候选 token 取最大参考相似，recall 反向取最大，再合成 F。它允许 paraphrase 软匹配，但结果依 encoder、layer、tokenizer、IDF、baseline rescaling 和版本。

语义相似仍不等于 entailment。句子“药物降低风险”与“药物不降低风险”多数词和 embedding 都很近，但事实极性相反。

## 六、匹配单位决定盲区

| 指标 | 匹配单位 | 捕捉 | 主要盲区 |
|---|---|---|---|
| EM | 规范化全串 | 严格答案一致 | 合法释义 |
| Token F1 | 无序 token multiset | 局部词覆盖 | 顺序、关系、否定 |
| BLEU | clipped n-grams | 局部精确与流畅片段 | 长距离语义、事实 |
| ROUGE-N/L | n-gram recall / LCS | 内容覆盖、顺序骨架 | 冗余、矛盾、释义 |
| BERTScore | contextual embedding | 软语义相似 | 逻辑、数字、来源支持 |

指标不应按“旧→新”排成淘汰序列。对于精确实体 QA，EM 可能比语义 metric 更可审计；对多样摘要，单参考 EM 几乎无意义。

## 七、聚合、配对与显著性

保留 per-example score $m_i^A,m_i^B$，比较差值 $d_i=m_i^A-m_i^B$，对任务单位做 paired bootstrap/cluster bootstrap。不要只给两个总体均值各自的区间。

若一篇报告尝试多个 tokenizer、normalization、metric、prompt 后只选择最有利的组合，就产生 researcher degrees of freedom。Primary metric、版本与方向应在 test 前冻结，其他指标作为解释性 panel。

## 八、图解：同一候选如何被五种尺测量

**读图问题**：同一个包含释义、换序、否定和长度差的候选，五种指标分别看见哪些匹配、又会漏掉哪些决定性语义？

![[00-知识库管理/_assets/figures/language-models/fig-lm-eval-metric-anatomy-v1.svg|900]]

> [!figure] 图 LM-58　从规范化字符到 contextual token matching
> **生成：**本库按 EM/F1/BLEU/ROUGE-L/BERTScore 的定义重绘同一教学候选；标色表示匹配单位，不表示人类质量。

**怎样读图**：先核对 normalization 后的全串与 multiset，再看 n-gram clipping 和 LCS 对顺序的处理，最后观察 embedding 软匹配为何能接住释义、却可能忽略否定与数字。

**图没有证明什么**：某一行匹配更多不证明该指标更接近所有人类判断；教学例也不能给出指标的跨任务相关性，更不能把语义相似直接解释为事实或来源支持。

## 九、常见错误与出口标准

错误包括：不披露 normalization；set 代 multiset；sentence BLEU 不写 smoothing；ROUGE 只写名字不写 N/L 与方向；embedding metric 不写模型版本；用相关性替代一致性；以单一指标定总冠军。

完成本节后，应能手算 EM/token F1/BLEU BP/ROUGE-L，解释 soft matching，构造每种指标的反例，并写一份包含 parser、reference、版本、聚合与 paired CI 的 metric card。

## 十、来源与练习

- [[S-2002-Papineni-BLEU]]；
- [[S-2004-Lin-ROUGE]]；
- [[S-2020-Zhang-BERTScore]]；
- [[习题 - Exact Match、F1、BLEU、ROUGE 与语义指标边界]]；
- [[解答 - Exact Match、F1、BLEU、ROUGE 与语义指标边界]]。
