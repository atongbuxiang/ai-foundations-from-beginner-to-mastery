---
type: exercise
status: verified
area: [language-models, pretraining-data, curriculum]
topic: "[[Curriculum、持续预训练与域适配数据路径]]"
solution: "[[解答 - Curriculum、持续预训练与域适配数据路径]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Curriculum、持续预训练与域适配数据路径

## A. 识别与复述

### LM23-A01
为什么静态 mixture 不能描述 curriculum 的完整训练对象？

### LM23-A02
区分 continued pretraining、DAPT、TAPT 与 supervised fine-tuning。

### LM23-A03
区分参数漂移与功能遗忘。

## B. 手算与构造

### LM23-B01
给一维 $g_A(\theta)=\theta-1,g_B(\theta)=2(\theta+1)$、$\eta=0.1,\theta_0=0$，算 AB 与 BA 两步结果。

### LM23-B02
新/旧 loss 从 `(2.0,1.0)` 到 `(1.2,1.4)`，算 $\Delta_{new},\Delta_{old}$ 并解释。

### LM23-B03
unique tokens 2B、draws 40B，算平均 exposure；说明不足以给分位数。

## C. 推导与证明

### LM23-C01
展开两次梯度更新，说明 $U_BU_A\ne U_AU_B$ 的一般原因。

### LM23-C02
写 time-varying mixture SGD 与最终 path dependence。

### LM23-C03
说明只在新域选择 checkpoint 如何产生旧域指标 survivor bias。

## D. 边界、反例与纠错

### LM23-D01
反驳“easy-to-hard 总比 shuffle 好”。

### LM23-D02
反驳“加入 replay 后旧域更好，所以方法更高效”，若总 compute 未固定。

### LM23-D03
构造参数距离小但关键功能退化的例子。

## E. AI 迁移

### LM23-E01
设计 DAPT/TAPT 的 checkpoint-lineage manifest。

### LM23-E02
设计新/旧/安全/时间五切片持续预训练实验。

### LM23-E03
审计只报告最佳 curriculum、未报告 tried paths 的论文。

独立完成后查看[[解答 - Curriculum、持续预训练与域适配数据路径]]。

