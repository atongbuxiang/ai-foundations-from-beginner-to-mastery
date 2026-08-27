---
type: source
status: active
area: [sources, implicit-regularization, matrix-factorization, parameterization]
source_type: paper
title: "Implicit Regularization in Matrix Factorization"
author: [Suriya Gunasekar, Blake E. Woodworth, Srinadh Bhojanapalli, Behnam Neyshabur, Nathan Srebro]
year: 2017
url: "https://papers.nips.cc/paper_files/paper/2017/hash/58191d2a914c6dae66371c9dcdc91b41-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "Open NeurIPS article; retain citation and stated limitations"
venue: "NeurIPS 2017"
scope_role: primary
temporal_role: modern-theory
related: ["[[隐式偏置、最大间隔与优化选择]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Implicit Regularization in Matrix Factorization
> [!abstract] 来源定位
> 研究欠定 matrix sensing/factorization 中 GD dynamics 的低核范数倾向。本库把它作为“参数化改变隐式偏置”的案例；commutativity、gradient-flow、small-init 等限制不省略。
## 本库调用
1. underdetermined factorization；
2. small initialization；
3. nuclear-norm hypothesis/evidence；
4. parameterization dependence；
5. limited theorem regime。
