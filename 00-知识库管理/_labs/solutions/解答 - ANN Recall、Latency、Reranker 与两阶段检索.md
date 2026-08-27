---
type: solution
status: verified
area: [language-models, ann, reranking]
topic: "[[ANN Recall、Latency、Reranker 与两阶段检索]]"
exercise: "[[习题 - ANN Recall、Latency、Reranker 与两阶段检索]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - ANN Recall、Latency、Reranker 与两阶段检索

## A. 识别与复述

### LM44-A01
ANN recall 比较 ANN 与同向量/距离的 exact top-$K$；task recall 比较返回与 gold evidence；chunk coverage 问固定切分中是否存在可用 gold 单元。前者测近似算法，第二测检索任务，第三测 ingestion 上界。

### LM44-A02
稀疏高层用长边快速接近查询区域，逐层下降到更密图再局部搜索。搜索宽度越大通常访问更多节点、recall 更高、延迟更大；连接数影响内存、构建与可导航性。

### LM44-A03
Dual encoder 把整段压成单向量后交互；late interaction 独立编码 token 并在末端做 MaxSim；cross-encoder 从输入起联合编码 query-document，表达强但每对都需昂贵计算。

## B. 手算与构造

### LM44-B01
交集为 $\{a,c,e\}$，大小 3；ANN recall@5 为 $3/5=0.6$。

### LM44-B02
Reranker 只能从不含 gold 的候选中选择，因此 Recall@5 上界为 0。扩大候选或修复第一阶段才可能恢复。

### LM44-B03
若严格串行且这些 p95 可直接相加，总和 $8+12+5+35+90=150$ ms。但“各组件 p95 之和=总 p95”一般不成立，因为分位数不可直接相加、阶段可能并行或相关；应实测端到端 p95。

## C. 推导与证明

### LM44-C01
重排输出 $R_{K_2}\subseteq C_{K_1}$。若 $G\cap C_{K_1}=\varnothing$，则 $G\cap R_{K_2}=\varnothing$；逐 query 指示量不超过 candidate 指示量，取平均仍成立。

### LM44-C02
$$s(q,d)=\sum_i\max_j E_q(q_i)^\top E_d(d_j).$$
$E_d(d_j)$ 只依赖文档，可离线计算；查询时计算 query tokens、查找候选 token 向量并做 MaxSim。多向量索引和存储是代价。

### LM44-C03
先以 exact float 为基准；exact quantized 与它的差是表示/量化误差；ANN quantized 与 exact quantized 的差是遍历/候选近似；把候选截到 $K$ 又引入截断。逐项冻结其余变量才能归因。

## D. 边界、反例与纠错

### LM44-D01
Exact top-5 中漏掉一个无关文档、以另一个无关文档替代，ANN recall 从 1 降到 .8；若 gold 仍在 top-5，task recall 保持 1。

### LM44-D02
平均值会藏掉尾部拥塞、cache miss、索引分页和冷启动；在线体验/超时通常由 p95/p99 决定。还要报告并发、batch、硬件与 index residency。

### LM44-D03
比较同时改变硬件、候选 $K$、batch 与 scorer，无法把速度差归因于架构，也不公平比较质量上界。需同硬件、同候选/质量点或画 Pareto 曲线，并报告全链路而非 kernel。

## E. AI 迁移

### LM44-E01
固定 encoder/corpus/query：exact float→exact quantized→ANN quantized→同候选 reranker。每步保存 candidate IDs，计算相邻阶段集合保真、gold recall、nDCG、延迟和内存。

### LM44-E02
网格化 M、efConstruction、efSearch（或对应参数）；列 build time、index bytes、Recall exact@K、task Recall@K、QPS、p50/p95/p99。以同硬件和并发画 Pareto frontier。

### LM44-E03
新增后查询新内容；更新后旧/新事实区分；删除后 exact、ANN、replica、cache 均不得命中。记录传播时延，并对高连接节点和过滤子集做回归。
