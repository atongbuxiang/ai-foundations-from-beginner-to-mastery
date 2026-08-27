---
type: concept
status: verified
area: [language-models, rag, evaluation]
node_id: LM-48
aliases: [RAG 评估地图, 检索生成归因联合评估]
prerequisites: ["[[Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]", "[[随机种子、配对比较、置信区间与序贯决策]]"]
related: ["[[70.8 评估校准与幻觉 MOC]]", "[[Context Construction、Citation、Grounding 与冲突证据]]"]
sources: ["[[S-2021-Petroni-KILT]]", "[[S-2023-Gao-ALCE]]", "[[S-2018-Yang-HotpotQA]]", "[[S-2020-Lewis-RAG]]", "[[S-2024-Asai-Self-RAG]]"]
exercises: ["[[习题 - RAG 的 Retrieval—Generation—Attribution 评估地图]]"]
solutions: ["[[解答 - RAG 的 Retrieval—Generation—Attribution 评估地图]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-rag-evaluation-cube-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# RAG 的 Retrieval—Generation—Attribution 评估地图

> [!abstract] 一句话结论
> RAG 评估至少有三个正交轴：有没有取回证据、答案是否正确、答案是否被所引证据支持。单一最终分数会掩盖补偿效应；最有诊断力的是分层指标、oracle 干预、联合事件和成本匹配曲线。

## 一、三轴不是同一件事

对样本 $i$ 定义

$$
R_i=\mathbf 1\{\text{检索集合覆盖 gold evidence}\},
$$

$$
G_i=\mathbf 1\{\text{最终答案正确}\},
$$

$$
A_i=\mathbf 1\{\text{所有需验证 claims 有正确支持}\}.
$$

会出现：$R=0,G=1$（参数记忆/猜测答对）；$R=1,G=0$（有证据但生成失败）；$G=1,A=0$（答案对但引用错）；以及完整成功。

联合成功率

$$
\widehat P(R\land G\land A)
=\frac1n\sum_i R_iG_iA_i
$$

不能由三个边缘平均数唯一决定。

## 二、检索指标

若相关集合为 $G_q$，排序前 $K$ 为 $\pi_{1:K}$：

$$
\operatorname{Recall@K}
=\frac{|G_q\cap\{\pi_1,\ldots,\pi_K\}|}{|G_q|},
\quad
\operatorname{Precision@K}
=\frac{|G_q\cap\{\pi_1,\ldots,\pi_K\}|}{K}.
$$

只有一个相关文档时

$$
RR=\frac{1}{\operatorname{rank}(\text{first relevant})},
\qquad MRR=\frac1n\sum_q RR_q.
$$

多等级 relevance 用

$$
DCG@K=\sum_{j=1}^{K}
\frac{2^{rel_j}-1}{\log_2(j+1)},
\qquad
nDCG@K=\frac{DCG@K}{IDCG@K}.
$$

答案字符串命中、页面级 gold、span-level support 与人工 relevance 会给不同指标，必须标明标注单位。

## 三、生成指标

短答案可用 EM、token F1；长答案还需 claim-level correctness、coverage、contradiction、abstention。表面重叠不能单独判断事实支持。

对不可回答问题，正确行为可能是 abstain。应分别测

$$
\Pr(\text{answer}\mid\text{answerable}),
\qquad
\Pr(\text{abstain}\mid\text{unanswerable}),
$$

以及风险—覆盖率曲线。

## 四、归因与引用指标

至少包含 citation correctness、citation completeness、source quality、citation localization 与 claim segmentation reliability。

自动 NLI/LLM judge 应在人类标注子集上验证，并报告 judge version、prompt、顺序敏感性与不确定样本。

## 五、oracle 干预定位根因

对同一 query 运行：

1. closed-book：无检索；
2. retrieved context：正常系统；
3. exact-retrieval oracle：移除 ANN 误差；
4. gold context：直接给 gold evidence；
5. gold context + gold layout：固定位置、引用映射与去噪；
6. human answer from retrieved context：估计 context 可用性。

若 normal→gold context 大涨，瓶颈在知识/检索/构造；gold context 仍低，瓶颈在 generator、任务定义或 gold 本身。exact oracle 只改变 ANN，不应同时改 encoder 和 $K$。

## 六、故障树

按顺序审计：

1. corpus 中是否有时点正确、权限可用证据？
2. chunk 是否覆盖完整证据？
3. exact retriever 是否排入候选？
4. ANN 是否保住 exact 候选？
5. fusion/reranker 是否保住或提升？
6. context 是否保留、正确排序且无冲突污染？
7. generator 是否利用证据并正确 abstain？
8. citation verifier 是否连接 claim 与 span？

根因可多标签，但“最早失败层”有助于修复优先级。

## 七、统计与成本匹配

比较系统 A/B 时用配对差

$$
\hat\Delta=\frac1n\sum_i(m_i^A-m_i^B).
$$

对 query 有放回 bootstrap，并保留同一 query 内所有 stages。

成本向量

$$
C=(\text{index bytes},\text{build time},\text{query calls},
\text{retrieved tokens},\text{latency p50/p95/p99},
\text{generator tokens},\text{energy/cost}).
$$

只在相同或显式给定成本预算下比较质量。更大的 $K$、更强 reranker 或更多 hops 不是免费改进。

## 八、切片与压力测试

至少按 answerable、未来更新、撤回文档、罕见实体、paraphrase、single/multi-hop、冲突来源、prompt injection、语言/领域/OCR、ACL 与尾延迟切片。

反事实包括删除 gold、替换日期、交换来源权威、加入语义相似假证据、打乱位置。输出变化用于诊断证据依赖，不能单独证明完整 faithfulness。

## 九、图解：评估立方体与故障投影

**读图问题**：R×G×A 评估立方与失败分母中的对象、箭头和比较分母怎样对应正文定义，读者应先核对哪一层？

![[00-知识库管理/_assets/figures/language-models/fig-lm-rag-evaluation-cube-v1.svg|900]]

> [!figure] 图 LM-48　Retrieval × Generation × Attribution 评估立方体
> 图由本库依据 KILT、ALCE、HotpotQA 的评估思想重新组织；不是外部论文原图。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：每个样本先落入三轴单元，再沿故障树投影到最早失败层；旁侧成本轴要求比较同预算系统。

**图没有证明什么**：一个 benchmark 的联合分数不能代表所有领域，也不能消除 gold evidence 不完整与 judge 偏差。

## 十、最小评估表

| 层 | 指标 | 必要对照 |
|---|---|---|
| corpus/chunk | answerable、oracle coverage | 人工 gold/span |
| retriever | Recall@K、MRR、nDCG | BM25/dense/exact |
| ANN | ANN recall、latency/memory | exact same-vector |
| reranker | nDCG、candidate oracle | first-stage |
| context | gold retention、noise/position | gold-only |
| generator | EM/F1、claim correctness、abstain | closed-book/gold |
| attribution | correctness/completeness | human audit |
| end-to-end | $R\land G\land A$、cost | paired CI |

## 十一、常见错误与出口标准

错误包括：只报最终 EM；把边缘指标相乘当联合率；用不完整 gold 惩罚替代证据；judge 无独立审计集；不同 $K$/成本直接比较；只分析平均样本。

完成本节后，应能手算 Recall/MRR/nDCG 与联合事件，设计六级 oracle 干预、配对区间和成本向量，并把错误定位到八类根因。

## 十二、来源与练习

- [[S-2021-Petroni-KILT]]；
- [[S-2023-Gao-ALCE]]；
- [[S-2018-Yang-HotpotQA]]；
- [[S-2020-Lewis-RAG]]；
- [[S-2024-Asai-Self-RAG]]；
- [[习题 - RAG 的 Retrieval—Generation—Attribution 评估地图]]；
- [[解答 - RAG 的 Retrieval—Generation—Attribution 评估地图]]。
