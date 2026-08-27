---
type: source
status: verified
area: [sources, scientific-spaces, neural-networks, language-modeling, weight-tying]
source_type: blog
title: "语言模型输出端共享Embedding的重新探索"
author: 苏剑林
year: 2023
url: "https://spaces.ac.cn/archives/9698"
accessed: 2026-08-26
source_tier: C
license: "科学空间博客；本库仅保存独立摘要、短公式与链接"
site_category: [数学研究, 信息时代]
scope_role: application-entry
temporal_role: modern-exposition
related: ["[[输入—输出权重共享与 Weight Tying]]", "[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[Embedding 初始化、缩放、分解与量化接口]]"]
created: 2026-08-24
updated: 2026-08-26
---

# 苏剑林：输出端共享 Embedding 的重新探索

> [!abstract] 来源定位
> 文章重访语言模型 output projection 与 input embedding 共享，分析直接以内积加 Softmax 建模时的损失/尺度困难并讨论改进方向。本库采用它作为中文问题入口，重点审计 row norm、hidden norm、logit scale、初始化与输出概率族；一般梯度和可辨识结论由独立推导承担。

## 问题主线

共享后 logits 形如

$$
z_j=e_j^\mathsf Th+b_j.
$$

于是 input row norm、hidden norm 与夹角共同控制输出尺度。直接复用一个为输入角色设计的初始化，并不自动保证 output logits 处于合适区间；projection、normalization、scale 或不同初始化合同可能改变这一点。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| SU9698-C1 | shared row 同时是输入向量与输出 prototype | 结构 | 直接 tying | 精确 |
| SU9698-C2 | 初始化尺度会影响初始 Softmax loss | 机制 | 还依赖 hidden 与相关性 | 有条件成立 |
| SU9698-C3 | tying 必然造成过大损失 | 普遍外推 | projection/norm/scale/训练可改变 | 不成立 |
| SU9698-C4 | 一种修正可普遍优于 untied | 经验外推 | 需跨模型公平消融 | 不成立 |
