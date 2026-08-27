---
type: exercise
status: verified
area: [language-models, evidence, gpt, bert, t5]
topic: "[[GPT、BERT、T5 的目标—模型族—能力证据地图]]"
solution: "[[解答 - GPT、BERT、T5 的目标—模型族—能力证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - GPT、BERT、T5 的目标—模型族—能力证据地图

## A. 识别与复述

### LM16-A01
分别写 GPT、BERT、T5 代表性配置的概率目标、架构与可见性。

### LM16-A02
解释 `I/T/A/E/H/O` 六类证据标签。

### LM16-A03
为什么 text-to-text 是接口统一而非任务决策问题统一？

## B. 手算与构造

### LM16-B01
将“BERT 双向，所以理解一定优于 GPT”拆成至少四个待控制变量。

### LM16-B02
给“causal mask 禁止未来可见”“T5 在数据集 X 更好”“双向性导致提升”分别标证据类型。

### LM16-B03
构造一张三模型公平比较的最小实验表，至少含预算、tokenizer、迁移与服务指标。

## C. 推导与证明

### LM16-C01
说明为何观察到的性能差异不能从多变量函数中唯一识别 objective 因果效应。

### LM16-C02
从三类概率对象推导各自原生 score 为什么不能直接等同。

### LM16-C03
说明参数量相同为何不推出训练/推理 FLOPs 相同。

## D. 边界、反例与纠错

### LM16-D01
给出“decoder-only 只能生成、不能分类”的反例接口。

### LM16-D02
反驳“encoder-only 不能参与生成系统”。

### LM16-D03
指出把 2018/2019/2020 论文结果直接外推到现代大模型的三个时间性问题。

## E. AI 迁移

### LM16-E01
为一篇模型博客填写最小 claim-evidence audit。

### LM16-E02
设计只替换 objective、尽量固定其他轴的反事实实验。

### LM16-E03
对“模型 A 全面优于模型 B”写一份必须补交的证据清单。

独立完成后查看[[解答 - GPT、BERT、T5 的目标—模型族—能力证据地图]]。
