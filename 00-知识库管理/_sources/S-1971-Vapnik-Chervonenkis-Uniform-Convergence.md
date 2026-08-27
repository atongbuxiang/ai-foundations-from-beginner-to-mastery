---
type: source
status: active
area: [sources, learning-theory, probability]
source_type: paper
title: "On the Uniform Convergence of Relative Frequencies of Events to Their Probabilities"
author: [Vladimir N. Vapnik, Alexey Ya. Chervonenkis]
year: 1971
url: "https://doi.org/10.1137/1116025"
accessed: 2026-08-20
source_tier: A
license: "Copyrighted journal article; retain bibliographic data, independent derivations, and DOI only"
scope_role: primary
temporal_role: classical-foundation
related: ["[[打散、增长与 VC 维]]", "[[增长函数与经验二分模式]]", "[[VC 一致收敛与泛化界]]", "[[二分类统计学习基本定理]]"]
created: 2026-08-20
updated: 2026-08-20
---

# Vapnik–Chervonenkis：事件相对频率的一致收敛

> [!abstract] 来源定位
> 这是 VC 理论的奠基论文：研究一族事件的经验频率何时能对全部事件同时逼近真实概率，并以组合增长性质刻画其关键条件。本库用现代 binary hypothesis / error-set 记号重建定义和证明，不把原论文的符号、常数与现代教材版本混写。

## 元数据

- V. N. Vapnik and A. Ya. Chervonenkis, “On the Uniform Convergence of Relative Frequencies of Events to Their Probabilities,” *Theory of Probability and Its Applications*, 16(2), 264–280, 1971；
- DOI：[10.1137/1116025](https://doi.org/10.1137/1116025)；
- 原始问题：对事件族 $\mathcal A$，研究 $\sup_{A\in\mathcal A}|P_m(A)-P(A)|$；
- 课程映射：事件 $A_h=\{(x,y):h(x)\ne y\}$ 对应分类器 $h$ 的 0–1 损失函数。

## 本库调用的断言

1. 无限类不能直接把 finite-class Union Bound 中的 $|\mathcal H|$ 原样代入；
2. 应改数一个有限样本上能出现多少不同事件迹或二分模式；
3. 组合增长受控可推出 distribution-free uniform convergence；
4. 现代“VC 维”是该增长性质的紧凑参数化。

> [!warning] 常数纪律
> [[VC 一致收敛与泛化界]]的 $4\tau_{\mathcal H}(2m)e^{-m\varepsilon^2/8}$ 是本库选定的现代 ghost-sample/Hoeffding 证明版本，不宣称逐字等于 1971 原文的定理常数。

## 后续调用

- [[打散、增长与 VC 维]]：打散和 VC 维；
- [[增长函数与经验二分模式]]：有限样本上的有效类大小；
- [[VC 一致收敛与泛化界]]：双样本概率界；
- [[二分类统计学习基本定理]]：有限 VC 与二分类可学习性的等价范围。
