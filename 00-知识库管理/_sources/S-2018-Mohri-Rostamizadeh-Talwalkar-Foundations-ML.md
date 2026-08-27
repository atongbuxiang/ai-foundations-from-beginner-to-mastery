---
type: source
status: active
area: [sources, learning-theory, machine-learning]
source_type: book
title: "Foundations of Machine Learning, Second Edition"
author: [Mehryar Mohri, Afshin Rostamizadeh, Ameet Talwalkar]
year: 2018
url: "https://cs.nyu.edu/~mohri/mlbook/"
accessed: 2026-08-23
source_tier: A
license: "Copyrighted textbook; retain independent summaries, formulas, theorem pointers, and official links only"
scope_role: backbone
temporal_role: classical-foundation
related: ["[[学习理论 MOC]]", "[[二分类统计学习基本定理]]", "[[多分类的 Natarajan 维与 Graph 维]]", "[[实值函数类、伪维与阈值化]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Foundations of Machine Learning

> [!abstract] 来源定位
> Mohri、Rostamizadeh 与 Talwalkar 的教材系统连接 PAC、VC/Rademacher、回归、多分类、核、Boosting、在线学习与稳定性。本库主要用它交叉校准复杂度定义、风险界的量词、实值函数推广和经典算法接口；证明均按本库对象合同独立重写。

## 元数据与纳入

- 正式引用：Mohri, M., Rostamizadeh, A. & Talwalkar, A. (2018), *Foundations of Machine Learning*, 2nd ed., MIT Press；
- 作者课程与官方开放版本入口：[book site](https://cs.nyu.edu/~mohri/mlbook/)；
- 出版信息：[MIT Press](https://mitpress.mit.edu/9780262039406/foundations-of-machine-learning/)；
- 证据角色：graduate-level textbook backbone，不替代原始论文的历史优先权；
- 版权边界：不复制书中插图、整段文字或习题答案，只保留独立推导、短公式和定位。

## 本库调用的主线

1. VC/Rademacher/covering 等 complexity measure 控制的是不同函数、损失与尺度对象；
2. binary、multiclass、ranking 与 regression 不能只通过替换标签集合复用同一容量定义；
3. generalization bound 必须声明 empirical/population、expectation/high probability、固定/数据依赖类；
4. SVM、kernel、Boosting 和 online learning 的算法推导应与 statistical guarantee 分账；
5. 伪维、fat-shattering 与 Lipschitz contraction 是从二分类进入实值风险的不同桥梁。

> [!warning] 使用边界
> 教材中的通用上界是可靠的定理骨架，但不自动解释现代深网的实际数值泛化。把一个 bound 用于具体模型前，仍需核对其范数、范围、尾部、margin、数据依赖与可计算性。

## 后续调用

- [[二分类统计学习基本定理]]：容量—uniform convergence—ERM—PAC 等价关系；
- [[结构风险最小化与非一致可学习性]]：可数分层、惩罚与 oracle comparison；
- [[多分类的 Natarajan 维与 Graph 维]]：多标签组合容量；
- [[实值函数类、伪维与阈值化]]：subgraph class 与 bounded real-valued uniform convergence；
- 20.4—20.9 的 Rademacher、margin、kernel、Boosting 与 online 主线。
