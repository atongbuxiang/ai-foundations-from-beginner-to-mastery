---
type: source
status: verified
area: [sources, in-context-learning, meta-optimization]
source_type: paper
title: "Transformers Learn In-Context by Gradient Descent"
author: "Johannes von Oswald et al."
year: 2023
url: "https://proceedings.mlr.press/v202/von-oswald23a.html"
accessed: 2026-08-26
source_tier: P1
license: "PMLR; independent summary"
scope_role: constructive-mechanism
related: ["[[ICL 的 Bayesian、线性回归与元优化解释]]", "[[Induction Head、机制回路与因果干预边界]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 线性 Attention 与上下文梯度下降构造

> [!abstract] 来源定位
> 论文给出线性 self-attention 层与线性回归一步梯度更新的数据变换对应，并在受控回归训练中比较学得权重与构造。课程采用一阶更新手算、层—迭代类比和曲率修正入口。

等价依赖特定表示、损失、构造与模型族；它不能单独证明聊天模型在自然语言 prompt 上维护显式参数向量或总在执行梯度下降。
