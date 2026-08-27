---
type: concept
status: verified
area: [language-models, rag, data-contracts]
node_id: LM-42
aliases: [RAG 索引合同, Chunking 与元数据]
prerequisites: ["[[参数记忆、外部记忆与 RAG 潜变量分解]]", "[[预训练语料来源、许可、隐私与文档单位合同]]"]
related: ["[[BM25、Dense Retrieval、Hybrid 与 Score Fusion]]", "[[Model、API、Tokenizer、Template 版本与复现合同]]"]
sources: ["[[S-2017-Johnson-Douze-Jegou-FAISS]]", "[[S-2021-Petroni-KILT]]"]
exercises: ["[[习题 - Chunk、Metadata、Embedding 与 Index 合同]]"]
solutions: ["[[解答 - Chunk、Metadata、Embedding 与 Index 合同]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-rag-data-lineage-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Chunk、Metadata、Embedding 与 Index 合同

> [!abstract] 一句话结论
> 检索对象不是原始文档，而是经过解析、切分、标注、编码和索引后的版本化单元。若不能从命中的向量条目反查原文 span、权限与时间，系统即使“搜到了”也不可复现、不可删除、不可引用。

## 一、文档单位为什么先于 embedding

原始文件 $d$ 经过解析器 $P_v$ 得到规范文本，再由切分器 $S_\phi$ 形成

$$
S_\phi(P_v(d))=\{c_1,\ldots,c_m\}.
$$

每个 chunk 应至少带

$$
c_i=(\text{chunk-id},\text{doc-id},[a_i,b_i),\text{text},
\text{metadata},\text{acl},\text{valid-time},\text{version}).
$$

若只保存 chunk text，重复段落无法回到唯一来源；若没有字符或 token span，引用无法精确定位；若 ACL 没随 chunk 进入查询过滤，检索可能泄漏无权访问的内容。

## 二、切分是带偏差的测量设计

固定窗口长度 $L$、重叠 $O$ 时，步长为 $L-O$。一篇长度 $N$ 的 token 序列，在 $N>L$ 时近似产生

$$
m=1+\left\lceil\frac{N-L}{L-O}\right\rceil
$$

个 chunk。增加 overlap 能减少答案跨边界被切断，却会：

- 扩大索引与重复候选；
- 让相邻 chunk 高度相关；
- 消耗上下文预算；
- 夸大“命中文档数”而不增加独立证据。

语义切分、标题层级切分、句子边界切分也不是天然更好。它们改变的是单元长度分布和答案覆盖概率，必须在目标查询上比较。

## 三、父子单元与证据 span

常见设计是小 chunk 检索、大 parent 阅读。检索单元 $c$ 与展示单元 $p(c)$ 分开：

$$
\text{retrieve}(q)\to c,\qquad
\text{context}(q)\leftarrow p(c).
$$

它兼顾局部匹配与完整语境，但可能把无关 parent 大段带入上下文。需要保存 child→parent 映射，并让引用最终落到支持命题的最小 span，而不是笼统指向整个 parent。

## 四、metadata 不是装饰

元数据参与至少四类操作：

1. 过滤：租户、权限、语言、地域、文档类型；
2. 排序：时效、权威度、版本状态；
3. 分片：按 tenant/domain 路由到不同索引；
4. 评估：对来源、时间、长度和权限切片。

过滤有先后顺序差异。若先 ANN top-$K$ 再做 ACL 过滤，允许文档被剔除后可能不足 $K$；若先按 ACL 建子索引，召回与成本又不同。协议必须说明 pre-filter 还是 post-filter。

## 五、embedding 合同

向量条目是

$$
v_i=f_{\psi}(T_\tau(c_i)),
$$

其中 $T_\tau$ 包含 query/document prefix、截断与 tokenizer。必须保存：

- encoder checkpoint/hash、tokenizer 与 normalization；
- query/document 是否共享编码器；
- pooling、维度 $d$、输出是否 L2-normalize；
- similarity 是 inner product、cosine 还是 squared distance；
- 输入最大长度与截断侧；
- 数值 dtype、量化和批处理版本。

若 $\|q\|=\|v\|=1$，则

$$
\|q-v\|_2^2=2-2q^\top v,
$$

所以 cosine、inner product 与 Euclidean 排序等价；未归一化时不成立，向量范数会进入排序。

## 六、index 合同与可复现删除

索引 manifest 还需记录：corpus/chunk manifest hash、build time、算法、距离、精确或近似、参数、随机种子、shards、replicas、tombstone、压缩和运行库版本。

版本关系应满足

$$
\text{index-version}
\longrightarrow
(\text{corpus-version},\text{chunker-version},\text{encoder-version}).
$$

删除文档必须沿 doc→chunks→vectors→replicas→cache 传播。只在关系库标记删除、却保留向量索引和检索缓存，不算完成遗忘。

## 七、覆盖率与污染率

给 gold evidence spans $G_i$ 和 chunks $C_i$，可定义 oracle chunk coverage

$$
\operatorname{Coverage}
=\frac1n\sum_i\mathbf 1\{\exists c\in C_i:
c\text{ 覆盖 }G_i\}.
$$

这一步完全不运行 retriever。若 coverage 已低，继续调 embedding 不会修复被切断的证据。

还应测重复率、空 chunk、解析乱码、metadata 缺失、ACL 违规和时间冲突。索引规模不是质量指标。

## 八、图解：从原文到可引用向量

**读图问题**：Chunk、metadata、embedding 与 index 数据血缘中的对象、箭头和比较分母怎样对应正文定义，读者应先核对哪一层？

![[00-知识库管理/_assets/figures/language-models/fig-lm-rag-data-lineage-v1.svg|900]]

> [!figure] 图 LM-42　RAG 数据血缘与双向追溯
> 图由本库按文档—span—chunk—embedding—index 合同绘制，不复刻外部图。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：正向路径保证可构建，反向路径保证一个检索结果能回到原始字节、授权和有效时间；红色断点是最常见的不可审计接口。

**图没有证明什么**：拥有完整 manifest 不保证 embedding 有效，只保证实验对象可识别、可重建。

## 九、最小 ingestion 测试

- 同一输入和版本产生相同 chunk IDs；
- Unicode、表格、页眉页脚和 OCR 有固定规范；
- gold span 跨边界样本进入回归集；
- ACL pre/post filter 的候选数可解释；
- 旧版本删除后，精确搜索、ANN、replica 和 cache 均不返回；
- 从 citation 定位原始文件页/段落，从原文反查所有派生 chunk。

## 十、常见错误与出口标准

常见错误包括：按字符切分却用 token 预算解释；更改 encoder 后复用旧索引；把 cosine 与 dot product 混用；只记录数据库产品名；chunk ID 依赖不稳定行号；引用 parent 页面却不标支持 span。

完成本节后，应能设计一个可逆数据血缘，手算窗口数量和归一化距离关系，先测 oracle chunk coverage，再讨论 retriever，并写出删除/更新跨索引传播测试。

## 十一、来源与练习

- [[S-2017-Johnson-Douze-Jegou-FAISS]]：向量检索、近似与压缩系统接口；
- [[S-2021-Petroni-KILT]]：固定知识快照与 provenance；
- [[习题 - Chunk、Metadata、Embedding 与 Index 合同]]；
- [[解答 - Chunk、Metadata、Embedding 与 Index 合同]]。
