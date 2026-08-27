---
type: solution
status: verified
area: [language-models, pretraining-data, deduplication]
topic: "[[精确去重、MinHash、LSH 与近重复检测]]"
exercise: "[[习题 - 精确去重、MinHash、LSH 与近重复检测]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 精确去重、MinHash、LSH 与近重复检测

## A. 识别与复述

### LM19-A01
Byte exact 要 raw bytes 相等；canonical exact 在显式 normalization 后相等；substring 找重复片段而非全文；near duplicate 用 Jaccard/edit/semantic 等阈值判断相近。对象越宽松越需处理假阳与代表策略。

### LM19-A02
$J=|A∩B|/|A∪B|$ 对称，问整体集合重合；$C(A\subset B)=|A∩B|/|A|$ 非对称，问 A 有多少被 B 包含。短文复制进长文时 containment 高而 Jaccard 低。

### LM19-A03
MinHash 用定长签名估计 Jaccard；LSH 用 band buckets 避免全对比较、只产 candidates；exact verification 在原对象上算真实指标；clustering 把验证 pair 组成删除单位；代表策略决定留谁。

## B. 手算与构造

### LM19-B01
交集 `{b,c}` 大小 2，并集 `{a,b,c,d,e}` 大小 5，$J=2/5=0.4$。$C(A\subseteq B)=2/4=0.5$；$C(B\subseteq A)=2/3$。

### LM19-B02
$P=1-(1-.8^4)^{10}=1-(.5904)^{10}\approx1-.00515=0.99485$。这只是理想独立下成为 candidate 的概率，不是“重复概率”。

### LM19-B03
阈值 $\tau=.5$，取 $A=\{1,2\},B=\{1,2,3\},C=\{2,3\}$。$J(A,B)=J(B,C)=2/3$，$J(A,C)=1/3$。Connected components 把三者放一起，尽管端点未达阈值。

## C. 推导与证明

### LM19-C01
对 $U=A∪B$ 的均匀随机排列，最小元素均匀落在 $U$ 每个元素。两集合最小元素相同当且仅当全局最小在 $A∩B$；概率 $|A∩B|/|U|=J$。

### LM19-C02
令 $I_k=1\{h_k(A)=h_k(B)\}\sim Bernoulli(J)$，$\hat J=K^{-1}\sum I_k$。线性期望给 $E\hat J=J$；理想独立给 $Var(\hat J)=K^{-2}KJ(1-J)=J(1-J)/K$。

### LM19-C03
一 band $r$ 行全匹配概率 $s^r$，不匹配 $1-s^r$；$b$ bands 全不匹配 $(1-s^r)^b$，补事件得 $1-(1-s^r)^b$。增大 b 增 recall/candidates；增大 r 降 recall/candidates，具体 frontier 依 corpus。

## D. 边界、反例与纠错

### LM19-D01
A 有 10 shingles且全部在 B，B 有 1000：containment $C(A\subset B)=1$，Jaccard $10/1000=.01$。只用 Jaccard 会漏完整抄入的短文。

### LM19-D02
Candidate event是随机签名/分 band 的检索；对任意 $s<1$ 未碰撞概率 $(1-s^r)^b>0$。未召回只说明该索引 realization 没命中，不是 exact similarity 小于阈值证明。

### LM19-D03
留最早偏向旧 crawl/首发站，留最长偏向聚合页，留最高质量继承 classifier 偏差，留许可清晰改变来源/域。应报告 cluster-level slice 前后和 removed→kept 映射。

## E. AI 迁移

### LM19-E01
选小宇宙 $U$ 枚举所有 $|U|!$ permutations；每 pair 集合计算 exact Jaccard和 MinHash equality count/阶乘；断言相等。再固定伪随机 hash 做近似，区分定理 oracle 与实现误差。

### LM19-E02
构造人工标注 exact/near/nonduplicate pairs，按长度/语言/来源切片；扫 shingle k、K、b/r、verify threshold；报告 pair recall、false delete、candidate pairs/N、CPU/IO；代表策略另测分布漂移。

### LM19-E03
缺 normalization、shingle unit/k、set/multiset、hash family/seed/width、signature K、bands b×r、candidate/verify threshold、similarity metric、cluster/representative。`0.8` 可能指 Jaccard verify，不是 LSH 硬阈值。

## 无提示重做

- [ ] 证明 MinHash 概率恒等式。
- [ ] 由 b、r、s 手算 candidate probability。

