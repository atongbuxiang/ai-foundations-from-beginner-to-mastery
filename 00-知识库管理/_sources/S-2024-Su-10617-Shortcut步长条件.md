---
type: source
status: verified
area: [sources, generative-models, flow-matching, shortcut]
source_type: blog
title: "生成扩散模型漫谈（二十七）：将步长作为条件输入"
author: 苏剑林
year: 2024
url: "https://spaces.ac.cn/archives/10617"
accessed: 2026-08-25
source_tier: C
scope_role: supporting
related: ["[[扩散蒸馏、一致性模型与 Shortcut]]", "[[平均速度、MeanFlow 与有限步生成]]"]
created: 2026-08-25
updated: 2026-08-25
---
# 科学空间：将步长作为条件输入

> [!abstract] 来源定位
> 文章从 Euler 大步失配出发，推导 Shortcut model 的 step-conditioned velocity $v_\theta(x,t,h)$，并用“一次 $2h$ 与两次 $h$ 的位移相同”构造自洽损失。课程用它区分 instantaneous field 与 finite-step map。

核心组合约束是

$$
2h\,v_\theta(x,t,2h)
\approx h\,v_\theta(x,t,h)
+h\,v_\theta(x+h v_\theta(x,t,h),t+h,h).
$$

页面发布日期：2024-12-15。约束在训练采样点成立不等于全域 semigroup、可逆流或任意未见步长泛化；这些必须通过 composition residual 与 step extrapolation 实验检查。
