---
type: source
status: active
area: [sources, learning-theory, svm, margin-methods]
source_type: paper
title: "Support-Vector Networks"
author: [Corinna Cortes, Vladimir Vapnik]
year: 1995
url: "https://doi.org/10.1007/BF00994018"
accessed: 2026-08-23
source_tier: A
license: "Machine Learning journal article; retain citation and independent derivations"
venue: "Machine Learning 20, 273–297"
scope_role: primary
temporal_role: classical-foundation
related: ["[[支持向量机、最大间隔与核方法]]", "[[分类间隔、Margin Bound 与 SVM 接口]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Support-Vector Networks

> [!abstract] 来源定位
> Cortes 与 Vapnik 给出 soft-margin support-vector network 的经典形式，把高维 feature-space linear separator、margin control、slack variables 与 kernel evaluation 连接起来。它是本库 SVM primal/dual、support vector 与 kernelized decision rule 的原始来源。

## 元数据与纳入

- 正式 DOI：[Springer](https://doi.org/10.1007/BF00994018)；
- 正式引用：Cortes, C. & Vapnik, V. (1995), *Machine Learning* 20, 273–297；
- 证据角色：soft margin、support vectors、feature-space decision surface 与 kernel computation；
- 边界：现代 convex duality/KKT 表述由优化教材校准，margin generalization 与 probability calibration 分别由专门理论承担。

## 本库调用的断言

1. nonseparable data 可通过 slack variables 与 penalty 参数定义 soft-margin problem；
2. dual solution 只依赖 pairwise feature inner products，可用 PSD kernel 替换；
3. nonzero dual coefficients 对应 support vectors，决策函数由其有限展开给出；
4. margin maximization、empirical hinge optimization 与 generalization guarantee 是连接但不同的层。
