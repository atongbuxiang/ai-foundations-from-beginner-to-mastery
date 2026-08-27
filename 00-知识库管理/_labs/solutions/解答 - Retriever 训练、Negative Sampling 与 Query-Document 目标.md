---
type: solution
status: verified
area: [language-models, dense-retrieval]
topic: "[[Retriever 训练、Negative Sampling 与 Query-Document 目标]]"
exercise: "[[习题 - Retriever 训练、Negative Sampling 与 Query-Document 目标]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Retriever 训练、Negative Sampling 与 Query-Document 目标

## A. 识别与复述

### LM45-A01
可取“含答案字符串”“人工判断与问题相关”“文本蕴含完整答案 claim”。三者不等价：字符串可偶然出现，相关不一定支持，蕴含要求更强。点击或同页又引入展示偏差与粒度问题。

### LM45-A02
随机负例从全库抽样，常太易；BM25 hard negative 有词面相似而标注为非相关，提供 lexical 混淆；model-mined 是当前 dense 模型高分项，贴近决策边界但最容易含 false negatives。

### LM45-A03
负样本由较旧 checkpoint $\eta_{t-\Delta}$ 编出的文档 ANN index 挖掘，而梯度更新当前 $\eta_t$。$\Delta$ 越大，训练所见的“困难”分布越不匹配当前模型。

## B. 手算与构造

### LM45-B01
$Z=e^2+e+1\approx11.107$，正例概率 $e^2/Z\approx0.6652$；损失 $-\log0.6652\approx0.4076$。

### LM45-B02
概率约 $(0.6652,0.2447,0.0900)$。$\tau=1$ 时梯度为 $(p_+-1,p_1,p_2)\approx(-0.3348,0.2447,0.0900)$。梯度和约 0，表示相对移动 logits。

### LM45-B03
同一 batch 含问题“Who wrote Hamlet?”与“Name the author of Hamlet”，两者正例都是不同 chunk 但都正确支持 Shakespeare。把另一题正例当 negative 会错误地下推替代证据。

## C. 推导与证明

### LM45-C01
令 $p_j=e^{s_j/\tau}/Z$，$\mathcal L=-s_+/\tau+\log Z$。因此
$$\partial\mathcal L/\partial s_j=-\mathbf1\{j=+\}/\tau+p_j/\tau.$$
即 $(p_j-\mathbf1\{j=+\})/\tau$。

### LM45-C02
导数显式含 $1/\tau$，且 softmax 在小 $\tau$ 下更集中于最高 logits，困难项获得更大相对梯度。若最高负例其实是漏标正例，错误排斥也被同样放大。

### LM45-C03
$$\mathcal L=-\log\frac{\sum_{d\in P}e^{s_d/\tau}}
{\sum_{d\in P\cup N}e^{s_d/\tau}}.$$
它保护集合 $P$ 内已知正例；未知替代证据若仍在 $N$，照样被惩罚，因此依赖标注覆盖。

## D. 边界、反例与纠错

### LM45-D01
极难项可能是 false negative、时间/权限错位或标注粒度错误。持续强推这类样本会破坏语义邻域；还可能只适配 miner 偏差。质量取决于难度与标签可信度的共同控制。

### LM45-D02
训练候选、query 语言、文档域、索引近似、chunk、时点与正例定义都可能与部署不同；损失只测训练 softmax。部署指标还受 corpus 与 ANN，所以需独立 Recall@K 切片。

### LM45-D03
无法复现每步看到什么负例，也无法判断 false-negative 比例与陈旧程度。应补 random/BM25/model-mined 比例、pool/depth、index checkpoint、刷新周期/lag、过滤规则和人工审计。

## E. AI 迁移

### LM45-E01
按模型分数分位与来源分层抽样；人工标为真负例、替代证据、只相关不支持、时间/ACL 错、粒度错。给置信区间并检查高分尾部，反馈多正例和过滤策略。

### LM45-E02
Query 切片含省略/指代、多轮、关键词、错别字、语言；doc 切片含 OCR 质量、表格、页眉、长段、领域与时间。交叉报告 Recall@K，另测解析/chunk coverage。

### LM45-E03
分别列 $\mathcal L_r,\mathcal L_g,\mathcal L_a$、权重与每项验证指标；报告 evidence recall、answer、citation、联合成功和成本。权重只用验证集选择，并给 Pareto 而非只给总损失。
