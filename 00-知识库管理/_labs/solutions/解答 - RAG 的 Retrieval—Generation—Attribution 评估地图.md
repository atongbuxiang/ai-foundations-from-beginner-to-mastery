---
type: solution
status: verified
area: [language-models, rag, evaluation]
topic: "[[RAG 的 Retrieval—Generation—Attribution 评估地图]]"
exercise: "[[习题 - RAG 的 Retrieval—Generation—Attribution 评估地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - RAG 的 Retrieval—Generation—Attribution 评估地图

## A. 识别与复述

### LM48-A01
$R$ 表示候选覆盖证据，$G$ 表示答案正确，$A$ 表示需验证 claims 被所引证据正确支持。$R=0,G=1$ 可由参数记忆；$R=1,G=0$ 是生成/构造失败；$G=1,A=0$ 是归因失败。

### LM48-A02
依次为 corpus、chunk、exact retriever、ANN、fusion/reranker、context、generator、citation verifier。最早失败层决定下游能否恢复。

### LM48-A03
边缘只给每个事件单独频率，不给它们在同一样本上的相关结构。成功可能集中在同一批样本，也可能互相错开，故 $P(R\cap G\cap A)$ 不由三边缘唯一确定。

## B. 手算与构造

### LM48-B01
Recall@5 $=1/2=0.5$；Precision@5 $=1/5=0.2$。

### LM48-B02
RR 为 $1,1/2,0$，MRR $=(1+0.5+0)/3=0.5$。

### LM48-B03
$$DCG@3=(2^3-1)/\log_2 2+(2^2-1)/\log_2 3+0
=7+3/1.58496\approx8.893.$$

## C. 推导与证明

### LM48-C01
取两样本。数据集甲为 $(R,G,A)=(1,1,1),(0,0,0)$，三边缘都 .5，联合 .5；乙为 $(1,1,0),(0,0,1)$，边缘仍各 .5，联合 0。可复制样本形成任意更大集合。

### LM48-C02
同一 query 的 corpus、retrieval、generation、citation 结果相关。若逐 stage 独立重采样，会拼出不存在的人工系统并低估/扭曲方差。应抽 query 索引后连同该 query 的所有 stage 与 A/B 配对一起重算。

### LM48-C03
Exact oracle 只移除 ANN 误差；若改善则近似搜索有责。Gold context 再绕过 encoder/ranking，测 context+generator。Gold layout 进一步移除去重、顺序、截断和 citation map，隔离 generator/任务。顺序每次只放宽一层。

## D. 边界、反例与纠错

### LM48-D01
字符串可能出现在否定句、列表、旧版本或无关实体中；完整 claim 还含关系、时间和范围。需要 span-level entailment/人工支持，而非 substring。

### LM48-D02
最终 EM 不显示检索与引用瓶颈；B 的更大 $K$ 增加召回、token、延迟与成本，比较不在同预算。应报告分层指标与成本曲线，或在相同 $K$/token/latency 下配对比较。

### LM48-D03
Judge 可能有领域偏差、位置/措辞敏感、与被评模型共享错误，且版本漂移。人工子集可估 precision/recall、一致性和不确定区间，决定自动指标能否用于该任务。

## E. AI 迁移

### LM48-E01
让系统输出答案或 abstain 及置信/支持分。按阈值改变覆盖率，计算已回答样本错误风险；分别报告 answerable 的回答率、unanswerable 的拒答率和高风险 false-answer。

### LM48-E02
时间：新旧/撤回来源；冲突：第一方与多份转载；注入：文档含指令；ACL：跨 tenant 禁止文档。每类测 retrieval、最终 context、答案、引用、泄漏和成本，并保留反事实配对。

### LM48-E03
模板列 A/B 同一题集、corpus、K 或预算；Recall/MRR/nDCG、answer、citation、joint；index bytes、build、calls、tokens、p50/p95/p99；逐题配对差与 bootstrap CI；切片、失败树和不能识别的因素。
