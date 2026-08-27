---
type: source
status: draft
area: [sources, math/randomized-linear-algebra, math/low-rank]
source_type: survey-paper
title: "Randomized Numerical Linear Algebra: Foundations and Algorithms"
author: "Per-Gunnar Martinsson and Joel A. Tropp"
year: 2020
url: "https://authors.library.caltech.edu/records/5gj83-t3t47"
accessed: 2026-08-15
source_tier: A
license: "Acta Numerica 作者公开版本；知识库保存独立摘要、概率边界与链接"
scope_role: modern-randomized-nla-synthesis
temporal_role: established-research-survey
aliases: [MT-2020-RandNLA]
related: ["[[随机化低秩近似与随机 SVD]]", "[[SVD 算法与谱范数估计]]", "[[有效秩]]"]
created: 2026-08-15
updated: 2026-08-15
---

# Martinsson–Tropp：随机数值线性代数的现代框架

> [!abstract] 来源定位
> 该综述把随机嵌入、范围寻找、低秩分解、误差估计、单遍算法和核矩阵近似放入统一概率框架。它补充 HMT 2011 的现代视角，尤其强调随机算法的失败概率、数据访问和自适应认证。

## 核心映射

| ID | 方法或原则 | 纳入位置 |
|---|---|---|
| MT20-1 | 随机测试矩阵以高概率探测主值域 | 基本 range finder |
| MT20-2 | oversampling、power/subspace iteration 控制失败率和慢谱衰减 | 参数章节 |
| MT20-3 | 先随机压缩，再确定性分解小问题 | randomized SVD |
| MT20-4 | passes、通信和内存可能比 flop 更关键 | 成本模型 |
| MT20-5 | 独立随机探针可做后验残差估计与自适应增秩 | 认证章节 |
| MT20-6 | structured sketch、Nyström、CUR 各有不同结构假设 | 扩展边界 |

## 证据边界

- 高概率不等于必然，任何单次结果都应记录 seed 和失败诊断；
- 对抗性输入、慢衰减谱和有限精度会改变经验质量；
- power iteration 增强谱隙但增加 passes，且必须重正交化；
- 随机低秩近似不能替代任务所需的精确秩、最小奇异值或小尾部高相对精度计算。

## 生成节点

- [x] [[随机化低秩近似与随机 SVD]]
