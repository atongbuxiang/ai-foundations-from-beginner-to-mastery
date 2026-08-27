---
type: solution
status: verified
area: [language-models, information-retrieval]
topic: "[[BM25、Dense Retrieval、Hybrid 与 Score Fusion]]"
exercise: "[[习题 - BM25、Dense Retrieval、Hybrid 与 Score Fusion]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - BM25、Dense Retrieval、Hybrid 与 Score Fusion

## A. 识别与复述

### LM43-A01
IDF 提高罕见、具判别力词项的权重；词频饱和避免重复词线性放大；长度校正避免长文只因机会更多而得高分。三者仍依赖 analyzer 与具体公式变体。

### LM43-A02
分数只在最终用 $f_q(q)^\top f_d(d)$ 交互；$f_d(d)$ 不依赖当前 query，所以可离线编码入索引。Cross-encoder 在每层联合处理 $(q,d)$，不能同样复用完整文档计算。

### LM43-A03
RRF 把不同量纲分数转为名次后相加，避免 raw-score 尺度假设；它丢失分数间隔和候选截断外信息，并仍有 $k_0$、列表深度与 tie 协议。

## B. 手算与构造

### LM43-B01
因 $|d|/\operatorname{avgdl}=1$，分母为 $3+1.5(1)=4.5$；分子 $3(2.5)=7.5$。词频因子 $7.5/4.5=5/3$，乘 IDF 2 得 $10/3\approx3.333$。

### LM43-B02
$q^\top d_1=2$，$q^\top d_2=4$，故 $d_2$ 在前。若改用 cosine，必须先按范数再算，不能沿用本结论。

### LM43-B03
A：$1/61+1/70\approx0.03068$；B：$2/63\approx0.03175$，所以 B 在前。

## C. 推导与证明

### LM43-C01
词频部分为 $f(k_1+1)/(f+C)$，其中 $C$ 与 $f$ 无关。分子分母同除 $f$，极限为 $(k_1+1)/(1+C/f)\to k_1+1$。

### LM43-C02
后续 fusion/rerank 的输入只含 $U=B_K\cup D_K$。若 $G\cap U=\varnothing$，任何只重排/删减 $U$ 的函数输出仍不含 gold；故最终 coverage 不超过 union coverage。

### LM43-C03
BM25 可为非负且范围随查询/语料变化，cosine 常在 $[-1,1]$。权重 $\alpha$ 同时吸收单位、尺度和模型偏好；索引或查询变化就会改变实际贡献。需校准、rank fusion 或学习式融合。

## D. 边界、反例与纠错

### LM43-D01
查询“错误码 ZXQ-7319”。BM25 对罕见精确 token 有高 IDF；dense tokenizer/训练可能把编号平滑成通用“错误码”语义，返回别的编号。

### LM43-D02
Query“怎样让模型不凭空编事实”，文档写“reduce hallucination through evidence grounding”，几乎无词面重叠但语义相近；dense 可能命中，严格 lexical 可能漏失。

### LM43-D03
在测试集枚举 $\alpha$ 再报最大分数会利用测试标签，结果含选择乐观偏差。应在训练/验证选定 analyzer、深度与 fusion，冻结后对独立测试只运行一次，并报告候选搜索空间。

## E. AI 迁移

### LM43-E01
同一 corpus/chunk/gold 下保存两路完整排名；分别算指标；union oracle 只问 gold 是否在并集；RRF 用冻结 $k_0$/depth 排序。这样将互补覆盖与融合排序收益分开。

### LM43-E02
Analyzer 分开测试中文切词、英文小写、型号/符号保留；embedding 测中英改写、代码、实体。切片含纯中、纯英、混合、罕见编号、同义改写和否定，逐路报告而非只看平均。

### LM43-E03
记录每路 scorer/analyzer/encoder、raw score、rank、top depth、missing rank、tie-break、RRF $k_0$、union/dedup、filter、最终 rank。分数变换和参数选择数据也入 manifest。
