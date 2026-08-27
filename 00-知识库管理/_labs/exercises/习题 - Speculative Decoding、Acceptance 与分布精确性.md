---
type: exercise
status: verified
area: [language-models, decoding, inference-acceleration]
topic: "[[Speculative Decoding、Acceptance 与分布精确性]]"
solution: "[[解答 - Speculative Decoding、Acceptance 与分布精确性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Speculative Decoding、Acceptance 与分布精确性

## A. 识别与复述

### LM55-A01
说明 draft proposal、target verification、acceptance 与 residual recovery 的角色。

### LM55-A02
解释 distribution exact、fixed-seed identical 与 wall-clock faster 的区别。

### LM55-A03
写平均接受率与 total variation 的关系。

## B. 手算与构造

### LM55-B01
给 $p=(.5,.3,.2)$、$q=(.35,.45,.2)$，计算各 token 接受概率、平均接受率、拒绝率和 residual。

### LM55-B02
假设每位置独立同接受率 $\alpha=.8$、draft 长度 $\gamma=4$，计算期望接受 token 数。

### LM55-B03
普通 target 单 token 成本 10 ms；draft 4 tokens 为 8 ms，target 验证为 13 ms，其他成本 1 ms，平均每轮提交 3 tokens。估算相对速度。

## C. 推导与证明

### LM55-C01
证明单步接受—残差输出分布等于 $p$。

### LM55-C02
证明 $\sum_x\min(p_x,q_x)=1-\operatorname{TV}(p,q)$。

### LM55-C03
解释多 token 验证为何必须在首次拒绝后丢弃后续 draft。

## D. 边界、反例与纠错

### LM55-D01
处理 $q(x)=0,p(x)>0$ 的 support 边界。

### LM55-D02
反驳“accept rate 80% 就等于加速 1.8 倍”。

### LM55-D03
解释 exact sampler 为何仍可与 baseline 在同 seed 下输出不同字节。

## E. AI 迁移

### LM55-E01
设计小词表 exactness 实验。

### LM55-E02
为 speculative server 写最小 trace。

### LM55-E03
设计 draft size 与 $\gamma$ 的联合选择实验。

独立完成后查看[[解答 - Speculative Decoding、Acceptance 与分布精确性]]。
