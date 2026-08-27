---
type: solution
status: verified
area: [language-models, rag, data-contracts]
topic: "[[Chunk、Metadata、Embedding 与 Index 合同]]"
exercise: "[[习题 - Chunk、Metadata、Embedding 与 Index 合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Chunk、Metadata、Embedding 与 Index 合同

## A. 识别与复述

### LM42-A01
原文先被解析、规范化、切分与编码；真正参与排序的是派生 chunk/向量。若不识别这个单位，就无法解释边界损伤、重复、截断、权限或把命中向量定位回来源。

### LM42-A02
最少应有 chunk-id、doc-id、原文 span、规范文本、metadata/ACL、有效时间/版本。实践还应有 parent、parser/chunker 版本与内容 hash。

### LM42-A03
Pre-filter 在近邻搜索前限制可见集合；post-filter 先取候选再删除不合条件项。后者可能导致返回不足 $K$ 或候选泄漏到中间日志；前者会改变可搜索子图/分片及性能。

## B. 手算与构造

### LM42-B01
步长 $L-O=192$。$m=1+\lceil(1000-256)/192\rceil=1+\lceil3.875\rceil=5$。

### LM42-B02
单位向量满足 $\|q-v\|^2=2-2(0.8)=0.4$；欧氏距离为 $\sqrt{0.4}\approx0.632$。题目问平方距离，因此答案是 $0.4$。

### LM42-B03
检索 child C17-04，映射到 parent P17（完整小节），引用再映射到 P17 内原文字符 $[842,931)$ 或页/段。日志同时保存 C17-04、P17 与 span，使检索粒度、阅读粒度、引用粒度彼此独立。

## C. 推导与证明

### LM42-C01
$$\|q-v\|^2=\|q\|^2+\|v\|^2-2q^\top v.$$
仅当两范数都为 1 时化为 $2-2q^\top v$，此时最大内积等价于最小欧氏距离。未归一化时范数项随文档改变。

### LM42-C02
Overlap 产生高度重叠单元；同一 gold 被多个 chunk 覆盖是重复覆盖，不是多份独立来源。它还增加重复候选并挤占 context，所以 evidence diversity 不会按 chunk 数等比增长。

### LM42-C03
若切分后的集合中不存在完整覆盖 gold 的 chunk，则任何只对该固定集合排序的 retriever 都无法返回一个不存在的成功单元。其成功事件是空集，概率上界为 0；需改变 chunk/parent/span 定义。

## D. 边界、反例与纠错

### LM42-D01
令 $q=(1,0)$，$d_1=(100,1)$，$d_2=(1,0)$。dot 分别 100 与 1，排 $d_1$ 前；cosine 约 $0.99995$ 与 1，排 $d_2$ 前。仅单位归一化时排序等价。

### LM42-D02
旧向量不属于新 encoder 表示空间；query 用新 encoder、documents 用旧 encoder 时相似度失去训练语义。必须版本阻断、全量或确定性增量重建，并以 index manifest 绑定 encoder hash。

### LM42-D03
ANN replica 或 cache 仍可能返回已删除内容，造成权限、隐私与时效错误。删除完成条件必须覆盖所有派生存储与查询路径，而非只看 source-of-record 一行。

## E. AI 迁移

### LM42-E01
保存 file hash/许可/ACL→parser/OCR 版本→页块与字符 span→chunker 参数与 chunk IDs→parent→encoder/tokenizer/prefix/truncation→vector dtype→index/shard/replica。每级存输入 hash 和父 ID。

### LM42-E02
构造答案分别落在窗口内部、正好边界、跨两句、表格跨页的 gold spans；对多个 $L,O$ 检查是否有 chunk/parent 完整覆盖，并把 span 文本逐字回溯到原文。

### LM42-E03
为每个 tenant 建允许/禁止文档；跨 valid-time 查询；比较 pre/post filter 的候选数与返回。验证禁止 ID 不出现在结果、日志或 cache，并在权限变更后立即回归。
