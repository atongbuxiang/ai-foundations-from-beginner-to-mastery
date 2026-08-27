---
type: concept
status: verified
area: [language-models, information-retrieval, ann, reranking]
node_id: LM-44
aliases: [近似近邻与重排, 两阶段检索]
prerequisites: ["[[BM25、Dense Retrieval、Hybrid 与 Score Fusion]]", "[[随机化低秩近似与随机 SVD]]"]
related: ["[[Retriever 训练、Negative Sampling 与 Query-Document 目标]]", "[[Test-time Compute、Search、Verifier 与预算]]"]
sources: ["[[S-2018-Malkov-Yashunin-HNSW]]", "[[S-2017-Johnson-Douze-Jegou-FAISS]]", "[[S-2020-Khattab-ColBERT]]", "[[S-2022-Su-9336-CUR检索]]"]
exercises: ["[[习题 - ANN Recall、Latency、Reranker 与两阶段检索]]"]
solutions: ["[[解答 - ANN Recall、Latency、Reranker 与两阶段检索]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-rag-ann-rerank-funnel-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# ANN Recall、Latency、Reranker 与两阶段检索

> [!abstract] 一句话结论
> 近似近邻解决的是“在固定向量与距离下，近似找回精确 top-$K$”，不是语义相关性的全部；两阶段系统必须分别测 exact retriever 的任务召回、ANN 对 exact 候选的保真、reranker 的排序增益和完整延迟分布。

## 一、三个 recall 不可混写

设精确向量搜索 top-$K$ 为 $E_K(q)$，ANN 返回 $A_K(q)$，gold 证据集合为 $G(q)$。

**ANN recall**：

$$
R_{\mathrm{ANN}}@K
=\frac{|A_K(q)\cap E_K(q)|}{K}.
$$

**任务 evidence recall**：

$$
R_{\mathrm{task}}@K
=\mathbf 1\{A_K(q)\cap G(q)\neq\varnothing\}.
$$

**chunk oracle coverage** 则问语料切分后是否存在覆盖 gold 的单元，甚至不运行检索。

ANN recall 高而任务 recall 低，说明 embedding/score 不把真证据排在前面；任务 recall 高而 ANN recall 不满，可能 ANN 漏掉的只是无关 exact 邻居。二者回答不同问题。

## 二、为什么需要 ANN

精确 dense 检索对 $N$ 个 $d$ 维向量计算相似度，粗略代价为 $O(Nd)$。ANN 用图、倒排量化或聚类缩小访问集合，以空间、构建时间和近似误差换查询速度。

HNSW 的直觉是多层图：

1. 高层只有少量节点，做长距离导航；
2. 逐层下降，在更密图上局部改进；
3. 搜索宽度增大通常提高 recall，也增加距离计算与延迟；
4. 构建连接数影响内存、构建成本和图可导航性。

这不是“调一个 ef 就完事”。维度、距离、数据聚簇、删除、并发和 cache 都会改变曲线。

## 三、压缩与量化

将向量量化为较低精度或 product quantization codes，可降低内存和带宽，但排序可能变化。需区分：

- encoder 本身的表示误差；
- float→quantized 的近似误差；
- index traversal 的候选近似；
- 最终 top-$K$ 截断误差。

正确实验应保留 exact float 检索作为 oracle，再逐项加入量化与 ANN。

## 四、两阶段检索

第一阶段用便宜模型从 $N$ 中取 $K_1$：

$$
C_{K_1}(q)=\operatorname{TopK}_{d}s_1(q,d).
$$

第二阶段用昂贵模型重排并取 $K_2<K_1$：

$$
R_{K_2}(q)=\operatorname{TopK}_{d\in C_{K_1}(q)}s_2(q,d).
$$

无论 $s_2$ 多强，只要 gold 不在 $C_{K_1}$，reranker 无法恢复。因此

$$
\Pr(G\cap R_{K_2}\neq\varnothing)
\le \Pr(G\cap C_{K_1}\neq\varnothing).
$$

这就是 candidate recall 上界。

## 五、cross-encoder、late interaction 与矩阵近似

cross-encoder 联合编码 $(q,d)$，可让每个 query token 与 document token 深度交互，精度高但文档表示不能直接复用。

dual encoder 只在最终向量交互，快但压缩严重。

ColBERT 采用晚交互，典型分数为

$$
s(q,d)=\sum_{i\in q}\max_{j\in d}
E_q(q_i)^\top E_d(d_j),
$$

保留 token 级匹配且可预计算文档 token 向量，但索引/存储更大。

科学空间的 CUR 条目展示另一视角：近似整个 query—document cross-encoder score matrix，以少量行列构造可检索近似，再用原 scorer 重排。无论哪种方案，都必须测“近似 top-$K$ 是否覆盖精确高分项”。

## 六、延迟不是一个平均数

端到端延迟可分

$$
T=T_{\text{query-encode}}+T_{\text{ANN}}
+T_{\text{fetch}}+T_{\text{rerank}}
+T_{\text{context}}+T_{\text{generate}}.
$$

至少报告 p50/p95/p99、冷启动、并发、batch、硬件、索引驻留状态与候选数。平均值可能掩盖少量极慢查询；仅报 ANN kernel 时间又会忽略 fetch 和 rerank。

成本曲线应以 $K_1$、搜索宽度、压缩、reranker batch 为自变量，输出 ANN recall、evidence recall、nDCG、尾延迟、吞吐和内存。

## 七、图解：精确 oracle 到最终上下文的漏斗

**读图问题**：ANN recall、候选漏斗、reranker 与 latency中的对象、箭头和比较分母怎样对应正文定义，读者应先核对哪一层？

![[00-知识库管理/_assets/figures/language-models/fig-lm-rag-ann-rerank-funnel-v1.svg|900]]

> [!figure] 图 LM-44　ANN—候选—重排漏斗与延迟账
> 图由本库依据 HNSW、Faiss、ColBERT 与两阶段检索关系绘制。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：每层同时观察候选数、gold 是否仍在集合和新增延迟；红色丢失一旦发生，下游不可恢复。

**图没有证明什么**：该图只解释ANN recall、候选漏斗、reranker 与 latency的结构和本节样例，不证明任意模型、数据、语言或部署环境都会得到同一性能；真实结论仍需独立实验、区间与版本化工件。


**图没有证明什么**：更昂贵 reranker 不保证在域外或含冲突证据时排序更好。

## 八、消融矩阵

至少比较：

1. exact float vs exact quantized；
2. exact vs ANN，不变 encoder 与 $K$；
3. ANN 不同搜索宽度；
4. first-stage only vs reranker；
5. $K_1$ sweep 与固定 $K_2$；
6. 单查询与生产并发下 p95/p99；
7. 新增/删除后索引一致性；
8. relevance slice：罕见词、多语、长文、时间过滤。

## 九、常见错误与出口标准

错误包括：用任务 recall 代替 ANN recall；用 exact 搜索调出的阈值直接宣称 ANN 性能；reranker 改善 top-5 后不报告 candidate oracle；比较不同硬件的平均延迟；只测静态索引不测删除。

完成本节后，应能写出三种 recall，证明 reranker 的候选上界，推导 ColBERT MaxSim，画出全链路延迟账，并设计 exact→quantized→ANN→rerank 的逐项消融。

## 十、来源与练习

- [[S-2018-Malkov-Yashunin-HNSW]]；
- [[S-2017-Johnson-Douze-Jegou-FAISS]]；
- [[S-2020-Khattab-ColBERT]]；
- [[S-2022-Su-9336-CUR检索]]；
- [[习题 - ANN Recall、Latency、Reranker 与两阶段检索]]；
- [[解答 - ANN Recall、Latency、Reranker 与两阶段检索]]。
