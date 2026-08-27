---
type: concept
status: verified
area: [language-models, dense-retrieval, contrastive-learning]
node_id: LM-45
aliases: [检索器训练, 负样本与对比检索]
prerequisites: ["[[BM25、Dense Retrieval、Hybrid 与 Score Fusion]]", "[[对比学习、InfoNCE 与密度比]]"]
related: ["[[ANN Recall、Latency、Reranker 与两阶段检索]]", "[[参数记忆、外部记忆与 RAG 潜变量分解]]"]
sources: ["[[S-2020-Karpukhin-DPR]]", "[[S-2021-Xiong-ANCE]]", "[[S-2020-Guu-REALM]]"]
exercises: ["[[习题 - Retriever 训练、Negative Sampling 与 Query-Document 目标]]"]
solutions: ["[[解答 - Retriever 训练、Negative Sampling 与 Query-Document 目标]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-rag-negative-geometry-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Retriever 训练、Negative Sampling 与 Query-Document 目标

> [!abstract] 一句话结论
> 检索器学到的不是抽象“语义”，而是训练查询、正例定义、负样本分布、相似度和候选机制共同定义的排序任务。负样本过易没有梯度，过难又可能是漏标正例；训练索引与部署索引的差异也会造成目标错位。

## 一、正例首先是一项标注假设

训练数据常写成三元组 $(q,d^+,d^-)$，但 $d^+$ 可表示：

- 包含答案字符串；
- 人工判断相关；
- 支持完整答案命题；
- 被用户点击；
- 与原问题同一页面；
- 由教师模型判为高分。

这些定义不等价。包含答案字符串可能只是偶然出现；点击混入展示偏差；同页不保证当前 chunk 支持命题。必须保存 positive provenance 与标注规则。

## 二、InfoNCE / softmax 排序目标

对一个 query、一个正例和候选集合 $\mathcal D_q$，令

$$
s_\eta(q,d)=f_q(q)^\top f_d(d).
$$

温度为 $\tau$ 的损失是

$$
\mathcal L_q
=-\log
\frac{\exp(s(q,d^+)/\tau)}
{\sum_{d\in\mathcal D_q}\exp(s(q,d)/\tau)}.
$$

记候选 softmax 概率为 $\pi(d\mid q)$，则

$$
\frac{\partial\mathcal L}{\partial s(q,d)}
=\frac{1}{\tau}
\left[\pi(d\mid q)-\mathbf 1\{d=d^+\}\right].
$$

正例分数被上推，负例按当前概率被下推；高分负例梯度更大。较小 $\tau$ 放大分数差与梯度，也更敏感于 false negatives。

## 三、in-batch negatives

一个 batch 含 $B$ 对 $(q_i,d_i^+)$ 时，可将其他 $d_j^+$ 当 $q_i$ 的负例：

$$
\mathcal L
=-\frac1B\sum_{i=1}^{B}
\log\frac{e^{s(q_i,d_i^+)/\tau}}
{\sum_{j=1}^{B}e^{s(q_i,d_j^+)/\tau}}.
$$

它廉价地得到 $B-1$ 个负例，但依赖 batch composition。若两个 query 共享有效证据，彼此正例会成为 false negative；若 batch 主题完全不同，负例又可能太容易。跨设备 all-gather 增加 negatives，同时改变有效 batch 和通信成本，必须记录。

## 四、随机、BM25 与模型困难负样本

| 类型 | 优点 | 主要风险 |
|---|---|---|
| 随机 | 便宜、覆盖全库 | 太易，梯度很小 |
| BM25 hard | 词面相似、常含混淆项 | 对 lexical pattern 过拟合 |
| model-mined | 针对当前决策边界 | false negative、索引陈旧 |
| cross-encoder mined | 质量较高 | 教师偏差与计算昂贵 |

ANCE 用近似近邻索引从全库寻找当前模型的高分负例，并异步刷新文档向量。训练状态包含

$$
(\eta_t,\ \text{document-index built from }\eta_{t-\Delta}).
$$

当 $\Delta$ 大，negative distribution 滞后；刷新太频繁又成本高。这是优化—系统耦合，不应只记作一个 sampler 名称。

## 五、false negative 审计

高分未标注文档可能是真负例、替代证据、只主题相关、时间/权限不匹配，或因 parent/chunk 粒度造成的标注错位。人工抽样、多个标注者、cross-encoder、答案与 entailment 检查都可辅助，但任何自动过滤器也有误差。

多正例目标可写为

$$
\mathcal L_q
=-\log
\frac{\sum_{d\in P_q}e^{s(q,d)/\tau}}
{\sum_{d\in P_q\cup N_q}e^{s(q,d)/\tau}}.
$$

它避免把已知替代证据当负例，但仍依赖正例覆盖。报告中应给 mined pool 各错误类型的抽样比例。

## 六、query 与 document 的域

训练 query 可能是自然问题，部署 query 却是关键词、对话省略句或模型生成的中间查询。document 可能来自 Wikipedia，而部署是表格、代码、扫描 PDF。需按 query 长度/语言/拼写/对话依赖，doc 类型/结构/时间/领域，answerable、多跳、罕见实体、ACL 等切片。

训练损失下降不代表部署 Recall@K 提升。

## 七、端到端训练的识别边界

若只用答案 likelihood 训练潜 retriever，generator 可能凭参数记忆完成任务，使 retriever 缺乏唯一监督；若只用 gold passage 训练，则优化 passage relevance，不直接优化最终答案。

常见目标组合：

$$
\mathcal L
=\lambda_r\mathcal L_{\text{retrieval}}
+\lambda_g\mathcal L_{\text{generation}}
+\lambda_a\mathcal L_{\text{attribution}}.
$$

$\lambda$ 定义系统优先级。应分别报告各目标对应指标，而非只报加权总损失。

## 八、图解：负样本如何塑造表示空间

**读图问题**：Retriever 对比目标、negative 几何与梯度中的对象、箭头和比较分母怎样对应正文定义，读者应先核对哪一层？

![[00-知识库管理/_assets/figures/language-models/fig-lm-rag-negative-geometry-v1.svg|900]]

> [!figure] 图 LM-45　随机、词面困难、模型困难与漏标正例
> 图由本库依据 DPR/ANCE 的训练机制绘制，点位为教学示意。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：观察 query 附近不同负样本产生的 softmax 权重；离决策边界近的点梯度大，但红边圈出的“未标替代证据”不应被强推远。

**图没有证明什么**：该图只解释Retriever 对比目标、negative 几何与梯度的结构和本节样例，不证明任意模型、数据、语言或部署环境都会得到同一性能；真实结论仍需独立实验、区间与版本化工件。


**图没有证明什么**：二维投影不等于真实高维几何，也不能凭距离判断文档是否蕴含答案。

## 九、训练报告合同

必须记录：positive rule、negative sources/ratios、batch/global batch、temperature、normalization、loss、optimizer、encoder revision、max lengths、mining frequency/index lag、false-negative audit、corpus snapshot、validation metric 与 deployment slices。

## 十、常见错误与出口标准

错误包括：把所有未标注文档当真负例；只增加 batch 不检查共享正例；用同一 index 挑 negatives 和做最终测试而无版本记录；只报训练 loss；把 cross-encoder 教师当真值。

完成本节后，应能推导 softmax loss 梯度，比较四类 negatives，识别 false negative 与 stale index，并设计训练—部署分布和多目标审计。

## 十一、来源与练习

- [[S-2020-Karpukhin-DPR]]；
- [[S-2021-Xiong-ANCE]]；
- [[S-2020-Guu-REALM]]；
- [[习题 - Retriever 训练、Negative Sampling 与 Query-Document 目标]]；
- [[解答 - Retriever 训练、Negative Sampling 与 Query-Document 目标]]。
