---
type: concept
status: verified
area: [language-models, information-retrieval, hybrid-retrieval]
node_id: LM-43
aliases: [混合检索, BM25 与稠密检索]
prerequisites: ["[[Chunk、Metadata、Embedding 与 Index 合同]]", "[[条件概率、全概率与 Bayes 公式]]", "[[联合分布、边缘分布与独立性]]"]
related: ["[[ANN Recall、Latency、Reranker 与两阶段检索]]", "[[Retriever 训练、Negative Sampling 与 Query-Document 目标]]"]
sources: ["[[S-2009-Robertson-Zaragoza-BM25]]", "[[S-2020-Karpukhin-DPR]]", "[[S-2009-Cormack-RRF]]"]
exercises: ["[[习题 - BM25、Dense Retrieval、Hybrid 与 Score Fusion]]"]
solutions: ["[[解答 - BM25、Dense Retrieval、Hybrid 与 Score Fusion]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-rag-ranking-fusion-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# BM25、Dense Retrieval、Hybrid 与 Score Fusion

> [!abstract] 一句话结论
> 稀疏检索善于精确词项与罕见标识，稠密检索学习语义邻近；混合检索的核心不是把两个未经校准的分数随手相加，而是明确分析器、相似度、候选集合、归一化和排序融合的估计对象。

## 一、检索到底在排序什么

给 query $q$ 与语料单元 $d\in\mathcal C$，retriever 产生分数 $s(q,d)$ 并返回前 $K$：

$$
\operatorname{TopK}_{d\in\mathcal C}s(q,d).
$$

分数可以是词项匹配、学习向量相似度或 cross-encoder 相关性。除非专门校准，它通常不是 $P(d\text{ relevant}\mid q)$。

## 二、BM25 的三个部件

一种常见 BM25 写法为

$$
s_{\mathrm{BM25}}(q,d)
=\sum_{t\in q}
\operatorname{IDF}(t)
\frac{f(t,d)(k_1+1)}
{f(t,d)+k_1\left(1-b+b\frac{|d|}{\operatorname{avgdl}}\right)}.
$$

其中 $f(t,d)$ 是词频，$|d|$ 是文档长度，$k_1$ 控制词频饱和，$b$ 控制长度归一化。

一类平滑 IDF 是

$$
\operatorname{IDF}(t)
=\log\frac{N-n_t+0.5}{n_t+0.5},
$$

$N$ 为文档数，$n_t$ 为含词项 $t$ 的文档数。不同实现可能加一、截断负值或采用不同 query term weighting，所以“BM25”仍需版本化 analyzer 与公式。

当 $f\to\infty$ 时，词频部分趋向 $k_1+1$，这就是饱和；同一词重复一百次不会贡献一百倍。$b=0$ 不做长度校正，$b=1$ 使用完整的平均长度比例。

## 三、dense dual encoder

双编码器给

$$
s_{\mathrm{dense}}(q,d)
=f_{\eta_q}(q)^\top f_{\eta_d}(d).
$$

文档向量可预计算，查询只需编码一次再做最大内积搜索。它能匹配不共享表面词形的语义，但容易：

- 对罕见编号、拼写、代码符号失真；
- 受训练域、负样本和查询措辞影响；
- 把语义相关误作答案支持；
- 在 embedding 更新后要求全量重建。

BM25 与 dense 不是老旧/先进的单向替代关系，它们使用不同归纳偏置。

## 四、为什么 raw score 不能直接相加

设 BM25 分数范围为 $[0,30]$，dense cosine 为 $[-1,1]$。直接

$$
s=\alpha s_{\mathrm{BM25}}+(1-\alpha)s_{\mathrm{dense}}
$$

会让量纲决定权重。min-max、z-score、softmax 或 learned calibration 可以变换，但它们都依赖查询和候选分布；必须说明是在单 query 内还是全局估计。

## 五、RRF：在名次空间融合

若多个检索器给排序集合 $\mathcal R$，Reciprocal Rank Fusion 定义

$$
s_{\mathrm{RRF}}(d)
=\sum_{r\in\mathcal R}
\frac{1}{k_0+\operatorname{rank}_r(d)}.
$$

没有出现在某一路截断列表的文档不贡献该项。$k_0$ 缓和头部名次差，候选深度也影响结果。RRF 避免假设原始分数同尺度，但丢失了分数间隔信息。

### 手算例子

取 $k_0=60$。文档 A 在 BM25 第 1、dense 第 10：

$$
s(A)=1/61+1/70\approx0.03068.
$$

文档 B 在两路都第 3：

$$
s(B)=2/63\approx0.03175.
$$

因此稳定中高排名的 B 可超过单路第一但另一路靠后的 A。

## 六、union、intersection 与召回上界

两路 top-$K$ 集合为 $B_K,D_K$。候选 union

$$
U=B_K\cup D_K
$$

通常提高覆盖但增加 rerank 成本；intersection 提高一致性却可能损失互补命中。融合后的最大可能效果受 union 中是否含 gold 限制：

$$
\text{end-to-end success}\le
\Pr(G\cap U\neq\varnothing).
$$

应同时报告 lexical-only、dense-only、union oracle 与 fused ranking，才能知道收益来自互补覆盖还是排序。

## 七、图解：三种打分如何汇合

**读图问题**：BM25、dense retrieval、hybrid 与 rank fusion中的对象、箭头和比较分母怎样对应正文定义，读者应先核对哪一层？

![[00-知识库管理/_assets/figures/language-models/fig-lm-rag-ranking-fusion-v1.svg|900]]

> [!figure] 图 LM-43　词频饱和、向量相似与名次融合
> 图由本库依据 BM25、DPR 与 RRF 的公式绘制；曲线与排序为教学算例。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：左侧看 BM25 随词频逐渐饱和；中间看双编码器把 query/document 映射到同一空间；右侧只用 rank 做 RRF，并保留各路候选来源。

**图没有证明什么**：该图只解释BM25、dense retrieval、hybrid 与 rank fusion的结构和本节样例，不证明任意模型、数据、语言或部署环境都会得到同一性能；真实结论仍需独立实验、区间与版本化工件。


**图没有证明什么**：两路互补是待测经验假设，不保证 hybrid 必然更好。

## 八、评估设计

固定 corpus、chunk 与 gold 后比较：

- Recall@1/5/20/100 与 MRR/nDCG；
- exact string、entity、semantic 与人工 relevance 的不同标签；
- rare identifier、paraphrase、长 query、否定、时间、语言切片；
- 候选 union 的 oracle recall；
- fusion 超参数只在验证集选择；
- top-$K$、索引大小、查询吞吐与尾延迟。

## 九、常见错误与出口标准

错误包括：把 answer string 出现在 chunk 当完美 relevance；用测试集调 $\alpha$；未记录 analyzer；把 cosine 当校准概率；只比较最终答案；候选深度不同却比较延迟。

完成本节后，应能手算 BM25 各部件、dual-encoder score 与 RRF；解释 raw score 量纲；以 union oracle 分离“检索互补”与“融合排序”收益。

## 十、来源与练习

- [[S-2009-Robertson-Zaragoza-BM25]]；
- [[S-2020-Karpukhin-DPR]]；
- [[S-2009-Cormack-RRF]]；
- [[习题 - BM25、Dense Retrieval、Hybrid 与 Score Fusion]]；
- [[解答 - BM25、Dense Retrieval、Hybrid 与 Score Fusion]]。
