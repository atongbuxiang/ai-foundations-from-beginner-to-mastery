---
type: exercise
status: verified
area: [language-models, privacy, memorization]
topic: "[[Memorization、Exposure、Canary 与训练数据抽取]]"
solution: "[[解答 - Memorization、Exposure、Canary 与训练数据抽取]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Memorization、Exposure、Canary 与训练数据抽取

## A. 识别与复述

### LM65-A01
区分 inclusion、memorization、verbatim reproduction、extractability 与 privacy harm。

### LM65-A02
定义 canary，并列出一个合格 canary 实验必须固定的四项内容。

### LM65-A03
定义 rank 与 exposure，并解释 exposure 的 bit 单位。

## B. 手算与构造

### LM65-B01
候选空间大小为 $2^{24}$，canary 排名为 $2^9$，计算 exposure；再解释该结果把枚举规模缩小了多少倍。

### LM65-B02
八个候选损失为 $(2.1,1.4,3.0,1.9,2.6,1.2,2.8,2.0)$，canary 是第三个候选。无并列时求 rank；若候选空间正好是这八个，求 exposure。

### LM65-B03
设计一个只使用合成六位数字、含 inserted/control 两组的 canary 表，列出最少字段。

## C. 推导与证明

### LM65-C01
从“rank 倍增意味着多搜索一 bit”解释 exposure 为何取对数差。

### LM65-C02
若每次独立查询成功抽取某合成 canary 的概率为 $p$，推导 $B$ 次内至少一次成功概率；指出独立假设的局限。

### LM65-C03
说明为什么逐字复现公开事实不能推出该字符串在训练集中，并给出两个替代来源。

## D. 边界、反例与纠错

### LM65-D01
反驳“没有从 1000 次采样中抽取到任何记录，所以模型没有记忆”。

### LM65-D02
实验者先枚举一百万候选，看到结果后把候选空间改成最好的一千个。说明 exposure 为何失效。

### LM65-D03
构造“高 exposure 但低实际伤害”和“低 exposure 但高风险”的各一个场景。

## E. AI 迁移

### LM65-E01
为一个内部模型写最小隐私红队合同，包含访问、预算、匹配、核验与停止规则。

### LM65-E02
设计比较 dedup 前后训练的 canary 实验，指出主要混杂与独立单位。

### LM65-E03
某输出疑似训练数据。写出从首次告警到结论的证据链，不接触或扩散真实敏感内容。

独立完成后查看[[解答 - Memorization、Exposure、Canary 与训练数据抽取]]。
