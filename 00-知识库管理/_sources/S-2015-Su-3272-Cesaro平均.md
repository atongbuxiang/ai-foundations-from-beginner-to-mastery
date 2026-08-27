---
type: source
status: draft
area: [sources, math/analysis, math/sequences, math/averaging]
source_type: blog
title: "柯西命题：盯着它到显然成立为止！"
author: 苏剑林
year: 2015
url: "https://spaces.ac.cn/archives/3272"
accessed: 2026-08-19
source_tier: C
license: "科学空间署名-非商业用途-保持一致；仅保存独立摘要、必要短公式与链接"
site_category: [数学研究]
scope_role: bridge
temporal_role: historical
related: ["[[数列、极限与完备性的直觉]]", "[[函数极限、连续性与收敛模式]]", "[[S-2025-MIT-18.100B-Sequences-Convergence]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 柯西命题：盯着它到显然成立为止！

> [!abstract] 来源定位
> 文章围绕“若$x_n\to a$，则算术平均也趋于$a$”展开，核心价值是把有限前缀与可控尾部分开：前缀总量固定，除以$n$后消失；尾部每项已小。MATH-07采用这条proof pattern与中文问题意识，不把博客标题中的“柯西命题”误读为Cauchy sequence criterion。

## 元数据与纳入

- 正式引用：苏剑林，2015-04-19，《[柯西命题：盯着它到显然成立为止！](https://spaces.ac.cn/archives/3272)》；
- 主题：若$x_n\to a$，则
  $$
  \frac{x_1+\cdots+x_n}{n}\to a;
  $$
- 本卡只存证明结构与课程判断，不复制长段落；
- “柯西命题”是文章称呼，不等于本章Cauchy数列定义。

## 断言表

| ID | 断言 | 条件 | 当前判断 | MATH-07调用 |
|---|---|---|---|---|
| C1 | 普通收敛推出Cesàro平均收敛到同一极限 | 实数/向量范数收敛 | 正确 | 第14节 |
| C2 | 有限前缀除以$n$趋于0 | 前缀长度固定 | 正确 | prefix-tail split |
| C3 | 尾部平均误差由逐项$\varepsilon$控制 | 收敛尾部 | 正确 | $\varepsilon/2$预算 |
| C4 | 类似拆分可处理多种平均问题 | 需逐题核对权重与归一化 | 作为启发 | AI averaging接口 |
| C5 | 平均收敛可反推原列收敛 | 无 | 错误 | $(-1)^n$反例 |

## 正式证明合同

本库将文章直觉重写为完整量词证明。给定$\varepsilon>0$：

1. 取$N_0$使$k\ge N_0$时$|x_k-a|<\varepsilon/2$；
2. 令固定常数
   $$
   C=\sum_{k=1}^{N_0-1}|x_k-a|;
   $$
3. 再取$n>2C/\varepsilon$；
4. 得
   $$
   \left|\frac1n\sum_{k=1}^nx_k-a\right|
   <\frac Cn+\frac\varepsilon2<\varepsilon.
   $$

这个版本明确了两个不同阶段选择和最终尾部起点的maximum。

## AI迁移边界

参数平均、checkpoint averaging或Polyak–Ruppert方法不能只凭本定理宣布有效。本定理的直接迁移只有：若参数列已在某范数下收敛，则普通算术平均收敛到同一极限。随机优化中的方差、偏差、步长和最优性需要额外理论。

## 已生成与后续调用

- [x] [[数列、极限与完备性的直觉]]：Cesàro证明；
- [x] [[习题 - 数列、极限与完备性的直觉]]：C03；
- [x] [[解答 - 数列、极限与完备性的直觉]]：完整见证；
- [ ] 随机优化节点：Polyak–Ruppert的正式条件。
