---
type: source
status: verified
area: [sources, causal-inference, statistics, experimentation]
source_type: textbook
title: "Causal Inference: What If"
author: "Miguel A. Hernán and James M. Robins"
year: 2025
url: "https://miguelhernan.org/whatifbook"
accessed: 2026-08-26
source_tier: A
scope_role: formal-causal-framework
related: ["[[数据优化器调度交互、混杂与归因边界]]", "[[单因素、全因子消融与交互效应]]", "[[训练实验协议、事故记录与因果证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Hernán–Robins：Causal Inference — What If

> [!abstract] 来源定位
> 免费权威教材从 potential outcomes、exchangeability、randomized experiments、confounding 与 selection bias 建立因果推断主线。本卷用它规范训练干预的 estimand 与识别条件。

## 本卷调用

- 对配置 $A$ 定义 $Y(a)$，目标先写成 ATE、paired conditional effect 或 policy value；
- 随机化使 treatment 与潜在结果在设计上可交换，blocking/paired randomization 可提高精度；
- 观测比较必须说明 consistency、positivity、exchangeability 与 measurement；
- mediator、collider、post-treatment selection 不可因“可记录”就随意控制。

## 边界

训练实验中的 experimental unit 可能是 seed、data draw、pretrained checkpoint 或完整 pipeline；若单位定义错，形式正确的公式仍会回答错误问题。
