---
type: source
status: active
area: [sources, learning-theory, multiclass]
source_type: paper
title: "Multiclass Learnability and the ERM Principle"
author: [Amit Daniely, Sivan Sabato, Shai Ben-David, Shai Shalev-Shwartz]
year: 2015
url: "https://jmlr.org/papers/v16/daniely15a.html"
accessed: 2026-08-23
source_tier: A
license: "JMLR article; retain citation, independent explanation, and official article/PDF links"
venue: "Journal of Machine Learning Research 16(72), 2377–2404"
scope_role: primary-modern-clarification
temporal_role: modern-classical-interface
related: ["[[多分类的 Natarajan 维与 Graph 维]]", "[[二分类统计学习基本定理]]", "[[Online-to-Batch Conversion]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Multiclass Learnability and the ERM Principle

> [!abstract] 来源定位
> 该论文说明 binary setting 中“任意 ERM 都一样好”的直觉不能无条件搬到 multiclass：某些多分类类上，不同 ERM 的 tie-breaking 会产生不同 sample complexity，甚至有的 ERM 可学习而另一些失败。它迫使课程把“类可学习”与“这个 ERM 规则可学习”分开。

## 元数据与核心结论

- 论文主页：[JMLR article](https://jmlr.org/papers/v16/daniely15a.html)；
- 官方全文：[PDF](https://jmlr.org/papers/volume16/daniely15a/daniely15a.pdf)；
- 正式引用：Daniely, A., Sabato, S., Ben-David, S. & Shalev-Shwartz, S. (2015), JMLR 16(72), 2377–2404；
- 课程角色：校准 Natarajan/Graph 维、ERM sample complexity 与 label symmetry 的边界。

## 本库调用的断言

1. 多分类 hypothesis class 的 PAC learnability 与某个具体 ERM rule 的表现是不同命题；
2. Graph dimension 常自然进入 generic ERM 的一致收敛分析，Natarajan dimension 更接近 learnability 的必要容量；
3. finite label set 时二者可通过含 $log|\mathcal Y|$ 的关系连接，但不能删除标签空间条件；
4. 对称类可得到更整齐的 tight characterization，一般类仍须审计 tie-breaking 与 output range。

> [!warning] 不作过度推广
> 论文不意味着“ERM 在多分类中普遍无效”，也不意味着所有现实 softmax 训练都由 0–1 ERM 定理覆盖。surrogate optimization、calibration 与 neural parameterization 是另外的证明层。
