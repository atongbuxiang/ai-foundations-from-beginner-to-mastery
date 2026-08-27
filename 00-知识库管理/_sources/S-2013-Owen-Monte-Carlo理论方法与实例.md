---
type: source
status: draft
area: [sources, math/probability, math/statistics, numerical-computation]
source_type: book
title: "Monte Carlo theory, methods and examples"
author: "Art B. Owen"
year: 2013
url: "https://artowen.su.domains/mc/"
accessed: 2026-08-19
source_tier: A
license: "Author-hosted online book; repository stores metadata, independent summaries and short formulas only"
scope_role: bridge
temporal_role: foundational
related: ["[[Monte Carlo、重要性采样与方差缩减]]", "[[浓缩不等式]]", "[[MCMC 与随机模拟诊断]]"]
created: 2026-08-19
updated: 2026-08-19
---

# Monte Carlo theory, methods and examples

> [!abstract] 来源定位
> Owen 的在线专著系统覆盖 simple Monte Carlo、误差估计、随机数、方差缩减、importance sampling、MCMC 与 QMC。当前课程以第 2、8、9 章作为 Monte Carlo 主证据链，并用第 15—17 章限定 QMC/RQMC 的边界。

## 元数据与纳入

- 正式引用：Art B. Owen (2013), *Monte Carlo theory, methods and examples*；
- 官方入口：[https://artowen.su.domains/mc/](https://artowen.su.domains/mc/)；
- 官方目录明确列出 Simple Monte Carlo、Variance Reduction、Importance Sampling、MCMC、QMC/RQMC；
- 当前调用者：[[Monte Carlo、重要性采样与方差缩减]]、[[浓缩不等式]]。

## 本轮使用章节

| 章节 | 课程用途 |
|---|---|
| Ch. 2 Simple Monte Carlo | accuracy、error estimation、safe SE、failure、Chebyshev/Hoeffding intervals |
| Ch. 8 Variance reduction | antithetics、stratification、CRN、conditioning、control variates |
| Ch. 9 Importance sampling | ordinary/SNIS、diagnostics、mixture/multiple IS |
| Ch. 11 MCMC | 相关样本误差、burn-in、诊断的后续入口 |
| Ch. 15–17 | QMC、lattice、randomized QMC 的边界 |

## 核心断言与课程判断

| ID | 断言 | 条件/边界 | 当前采用 |
|---|---|---|---|
| C1 | iid sample mean 在有限方差下有 $n^{-1/2}$ SE | iid、二阶矩有限 | 作为 simple MC 基线 |
| C2 | 方差缩减应同时考虑 variance 与计算成本 | 同一目标、合法 estimator | 采用 efficiency 审计 |
| C3 | IS proposal 质量由目标 integrand 与 weight moments 决定 | support 与矩条件 | 采用并补 measure 语言 |
| C4 | SNIS、diagnostics 与普通 IS 必须区分 | random denominator | 采用并补 Delta 推导 |
| C5 | QMC 误差理论不是 iid MCSE | variation/discrepancy 或 randomization | 仅作高级接口 |

## 课程补充边界

- “ESS”需要标明是 weight ESS 还是 autocorrelation ESS；
- logsumexp 只处理浮点稳定，不证明 proposal 合格；
- 自适应 proposal、estimated control coefficient 和 MCMC 各自改变误差估计；
- 书中方法的实现仍需记录 seed、PRNG streams、dtype 与并行采样契约。

## 已生成与后续调用

- [x] [[Monte Carlo、重要性采样与方差缩减]]：完整方法主线；
- [x] [[浓缩不等式]]：MC 的 Chebyshev/Hoeffding 有限样本接口；
- [ ] [[MCMC 与随机模拟诊断]]：相关样本、链诊断与 MCSE；
- [ ] 数值积分专题：QMC/RQMC、effective dimension 与 randomized error estimate。

