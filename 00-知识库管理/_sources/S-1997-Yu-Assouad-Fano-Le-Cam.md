---
type: source
status: active
area: [sources, statistics, minimax, information-theory]
source_type: paper
title: "Assouad, Fano, and Le Cam"
author: Bin Yu
year: 1997
url: "https://doi.org/10.1007/978-1-4612-1880-7_29"
accessed: 2026-08-20
source_tier: A
license: "Publisher-copyrighted chapter; retain citation, independent derivations and DOI link only"
venue: Festschrift for Lucien Le Cam, pp. 423–435
scope_role: lower-bound-backbone
temporal_role: classical-foundation
related: ["[[样本复杂度下界与 Minimax 视角]]", "[[互信息与信息论泛化界]]", "[[不可知 PAC、ERM 与双侧一致收敛]]"]
created: 2026-08-20
updated: 2026-08-20
---

# Assouad, Fano, and Le Cam

> [!abstract] 来源定位
> Yu 1997 系统比较 Le Cam、Assouad 与 Fano 三类 minimax lower-bound 方法及其联系。本库用它建立“把估计困难归约为检验困难”的统一视角；具体学习类的常数仍由明确 construction 与标准学习理论定理承担，不能只写方法名就宣称得到 sharp lower bound。

## 元数据与纳入

- DOI：[10.1007/978-1-4612-1880-7_29](https://doi.org/10.1007/978-1-4612-1880-7_29)；
- 正式引用：Yu, B. (1997), *Assouad, Fano, and Le Cam*, in *Festschrift for Lucien Le Cam*, 423–435；
- 三种骨架：two-point testing、many-way packing、hypercube/coordinate reduction；
- 当前调用者：[[样本复杂度下界与 Minimax 视角]]。

## 方法路由

| 方法 | construction | 典型出口 |
|---|---|---|
| Le Cam | 两个彼此接近、参数分离的分布 | 基础 rate、confidence dependence |
| Fano | 多个分离 hypotheses，互信息不足以识别 index | $\log M$、dimension/packing dependence |
| Assouad | hypercube 邻接分布，逐坐标 testing | 可加 loss、维数线性 dependence |

## 断言审计

| 断言 | 判断 |
|---|---|
| lower bound 对所有 estimator/learner 取 infimum | 采用 |
| 一个算法失败可证明 minimax 不可能性 | 否定 |
| KL 小且 parameter separation 大可产生 estimation lower bound | 采用，需明确 testing lemma 与 constants |
| expected lower bound 自动等于 high-probability PAC lower bound | 否定 |
| Fano 中候选数越多总会使 bound 更强 | 否定；pairwise/average KL 也必须受控 |

## 已生成与后续调用

- [x] [[样本复杂度下界与 Minimax 视角]]：Le Cam/Fano 证明模板与 finite-class rate 审计；
- [ ] [[互信息与信息论泛化界]]：information quantity 在 upper/lower bounds 中的不同方向；
- [ ] [[二分类统计学习基本定理]]：VC-rich constructions 的正式 lower bound。
