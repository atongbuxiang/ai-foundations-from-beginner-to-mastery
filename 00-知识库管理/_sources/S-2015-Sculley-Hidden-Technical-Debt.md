---
type: source
status: verified
area: [sources, ml-systems, causality, technical-debt]
source_type: paper
title: "Hidden Technical Debt in Machine Learning Systems"
author: "Sculley et al."
year: 2015
url: "https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html"
accessed: 2026-08-26
source_tier: A
scope_role: systems-evidence
related: ["[[数据优化器调度交互、混杂与归因边界]]", "[[训练实验协议、事故记录与因果证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Sculley 等：机器学习系统中的隐性技术债

> [!abstract] 来源定位
> 论文整理了 entanglement、hidden feedback loop、undeclared consumers、data dependency 与 configuration debt，提醒模型实验不是孤立函数调用。

## 本卷调用

- 将数据、特征、代码、配置、服务消费者和反馈回路放入因果图；
- 把 pipeline 版本、缓存、预处理和外部服务列为潜在 treatment bundle；
- 事故记录同时追踪局部训练症状与上下游系统变化。

## 边界

技术债分类是系统风险框架，不自动识别某次训练差异的因果效应；仍需随机化、阻断或可辩护的观测假设。
