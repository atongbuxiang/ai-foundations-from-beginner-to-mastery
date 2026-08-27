---
type: solution
status: verified
area: [language-models, in-context-learning, demonstrations]
topic: "[[Zero-shot、Few-shot ICL、示例顺序与标签映射]]"
exercise: "[[习题 - Zero-shot、Few-shot ICL、示例顺序与标签映射]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Zero-shot、Few-shot ICL、示例顺序与标签映射

## A. 识别与复述

### LM34-A01
Zero-shot 无任务 demonstrations，one-shot 有一个，few-shot 有多个；ICL 指部署权重不更新而预测随上下文样例改变。Instruction 是否存在需另记，不能把 zero-shot 自动等同“无说明”。

### LM34-A02
六类为任务语义、输入分布、label space、序列格式、局部标签/位置 prior 和与 query 的检索相似性。它们同时变化，所以 few-shot 总增益不等于正确映射贡献。

### LM34-A03
Checkpoint $\theta$ 在 ICL 调用中固定；但 hidden activations、attention weights 和 KV cache 都由 prompt 决定并变化。前者是外部参数更新，后者是一次前向计算的条件状态。

## B. 手算与构造

### LM34-B01
均值 $(0.8+0.7+0.5+0.4)/4=0.6$；排序后中位数 $(0.5+0.7)/2=0.6$；范围 $0.8-0.4=0.4$；最好值 0.8。只报 0.8 会隐去排列不稳定和四次选择。

### LM34-B02
$4!=24$，$8!=40320$。四例常可完整枚举；八例若每次模型调用昂贵，通常预注册随机排列或结构化子集，并报告采样误差。

### LM34-B03
基准 demos 将正面→positive、负面→negative；置换版统一改为正面→B、负面→A，并把 scorer 期望同步。若 query 预测也按置换变化，说明模型至少能覆盖一部分固有 label semantics。

## C. 推导与证明

### LM34-C01
$E_i=1\{\hat y_i(\sigma P)=\sigma(\hat y_i(P))\}$，均值给置换等变成功率。它测临时 label mapping 是否随上下文置换，而非单独证明模型理解任务语义。

### LM34-C02
该观察的量词只覆盖被测模型、任务、模板和随机化方式；格式、label space 或输入分布仍可贡献。换自然词/无语义 label、类别数、instruction 或模型规模，正确映射的边际作用可改变。

### LM34-C03
预先随机部署的 estimand 是 $E_\pi[A_\pi]$；用测试分数选择后报告的是 $\max_\pi A_\pi$。后者使用了测试标签提供的监督，且因噪声乐观；应在验证集选、独立测试集估计固定 selector。

## D. 边界、反例与纠错

### LM34-D01
模型原本不知道必须只输出 A/B。给两个输入与任意 A/B 输出示例后，parser success 从低变高，但随机交换标签不改变总体准确率；提升来自输出格式/label space，不是 input-label 关系。

### LM34-D02
Causal LM 中早期位置不能看后期位置，query 对不同相对位置、recency 与 position encoding 有不同表示。相同集合的不同连接顺序是不同 token 序列，模型没有 permutation invariance 保证。

### LM34-D03
无法确定选择器、数据泄漏与相似度定义。需补 encoder checkpoint/tokenizer、embedding normalization、index corpus/version、distance、tie rule、label usage、query-time filters、seed 和候选 IDs。

## E. AI 迁移

### LM34-E01
做真配对、随机 label、系统置换 label、无 label/format-only 四条件；固定 inputs、顺序、token budget 与 scorer。对每题报告预测和 label-equivariance，并测试 model/template 交互。

### LM34-E02
固定 $K$ 时添加/删除无关 filler 改总长度，测纯长度影响；固定 token budget 时改变示例压缩和 $K$，测数量效应。两套都扫描位置与 truncation，避免把 $K$ 和 $T$ 混合。

### LM34-E03
训练 split 只用于 selector/encoder 学习；验证 split 选 $K$、距离和排序；测试 split 只运行冻结 selector 一次。缓存每个 query 的候选、得分、最终 demos 和顺序，禁止依据测试正确性重选。
