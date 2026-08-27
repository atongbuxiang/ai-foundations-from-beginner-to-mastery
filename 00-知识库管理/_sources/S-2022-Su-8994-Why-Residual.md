---
type: source
status: draft
area: [sources, scientific-spaces, neural-networks/residual-stability]
source_type: blog
title: "为什么需要残差？一个来自 DeepNet 的视角"
author: 苏剑林
year: 2022
url: "https://spaces.ac.cn/archives/8994"
venue: "科学空间"
accessed: 2026-08-23
source_tier: C
license: "科学空间；本库仅保存独立摘要、必要短公式与链接"
scope_role: bridge
temporal_role: modern-exposition
related: ["[[残差学习、恒等捷径与退化问题]]", "[[残差块 Jacobian 与梯度直通]]", "[[残差缩放、Lipschitz 界与深度稳定性]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 表达、稳定性与证据边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 苏剑林：为什么需要残差

> [!abstract] 来源定位
> 文章从 DeepNet 的尺度分析出发，把 residual scale 与前向传播、反向传播、参数梯度和“增量爆炸”联系起来。本库把它作为中文推导入口，并把确定性 Lipschitz 最坏情况、随机二阶矩量级、训练更新和任务性能分开验收。

## 核心入口

文章考察

$$
y=x+\varepsilon f(x;\theta),
$$

由此得到

$$
\frac{\partial y}{\partial x}
=I+\varepsilon\frac{\partial f}{\partial x},
\qquad
\frac{\partial y}{\partial\theta}
=\varepsilon\frac{\partial f}{\partial\theta}.
$$

这清楚展示 residual scale 可同时进入 state Jacobian 与参数梯度。文章随后用 $(1+\varepsilon)^N$ 讨论最坏同向增长，并指出 $\varepsilon=1/N$ 与 $1/\sqrt N$ 在不同尺度目标下不能混为一谈。

## 断言分层

| ID | 断言 | 类型 | 课程处理 |
|---|---|---|---|
| SU-RES-C1 | scale $\varepsilon$ 线性缩放 branch parameter gradient | 代数 | 精确 |
| SU-RES-C2 | 小 branch 使单块接近 identity | 局部分析 | 需指定 Jacobian/norm |
| SU-RES-C3 | $\varepsilon=1/\sqrt N$ 足以给任意深度的 uniform worst-case bound | 强外推 | 一般不成立；最坏同向积仍可按 $e^{c\sqrt N}$ 增长 |
| SU-RES-C4 | residual 解释了所有深网优化优势 | 机制解释 | 需原论文、结构消融与其他机制共同支持 |

## 课程补严

- 用 $\prod_ell(1+\varepsilon_ell L_ell)\le e^{\sum\varepsilon_ell L_ell}$ 给出确定性上界；
- 用 one-sided Lipschitz/dissipativity 区分“分支小”与“整个 update 收缩”；
- 把 $1/N$ 的 worst-case 累积、$1/\sqrt N$ 的随机方差尺度和参数更新尺度分账；
- 不把 Transformer 初始化处的量级分析直接外推到所有 CNN/MLP 和训练全过程。
