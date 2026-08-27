---
type: exercise
status: verified
area: [language-models, decoding]
topic: "[[EOS、停止规则、重复惩罚与退化循环]]"
solution: "[[解答 - EOS、停止规则、重复惩罚与退化循环]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - EOS、停止规则、重复惩罚与退化循环

## A. 识别与复述

### LM52-A01
定义 EOS hazard 与 survival probability。

### LM52-A02
列举五类 finish event，并区分模型内生与外部事件。

### LM52-A03
解释重复惩罚为何改变生成分布，而非仅做显示后处理。

## B. 手算与构造

### LM52-B01
给 hazard $(.1,.2,.5)$，计算生成到各步前的 survival 与恰在三步停止的概率。

### LM52-B02
原 logits 中已出现 token 的值为 $2$，未出现 token 为 $1.5$。采用正 logit 除以 repetition penalty $1.25$ 的规则，比较惩罚前后排序。

### LM52-B03
构造三状态确定性退化循环并给转移矩阵。

## C. 推导与证明

### LM52-C01
推导 $Pr(T=t)=S(t)h_t$ 及有限上限下未 EOS 的概率。

### LM52-C02
证明 stop string 若跨 token 边界，单 token 检查会漏检。

### LM52-C03
比较 presence penalty 与 temperature 的顺序；再说明常见按符号乘除的 repetition penalty 为何可能与正温度缩放交换。

## D. 边界、反例与纠错

### LM52-D01
纠正“返回文本没有 EOS 字符，所以模型没有预测 EOS”。

### LM52-D02
审计把 `length`、`stop`、`cancelled` 都记成 `eos` 的 API。

### LM52-D03
反驳“所有重复都是 exposure bias 导致”。

## E. AI 迁移

### LM52-E01
设计 stop/finish 单元测试矩阵。

### LM52-E02
设计重复退化的因子实验。

### LM52-E03
为 streaming API 写安全截断与可观测性合同。

独立完成后查看[[解答 - EOS、停止规则、重复惩罚与退化循环]]。
