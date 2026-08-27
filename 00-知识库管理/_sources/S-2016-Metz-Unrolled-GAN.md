---
type: source
status: verified
area: [sources, generative-models, gan, mode-collapse]
source_type: paper
title: "Unrolled Generative Adversarial Networks"
author: "Luke Metz; Ben Poole; David Pfau; Jascha Sohl-Dickstein"
year: 2016
url: "https://arxiv.org/abs/1611.02163"
venue: "ICLR 2017"
accessed: 2026-08-25
source_tier: A
license: "论文页面；本库仅保存独立摘要、必要公式与链接"
scope_role: mode-collapse-intervention
temporal_role: foundational
related: ["[[Mode Collapse、模式覆盖与生成器熵]]", "[[Minimax 动力学、旋转、阻尼与局部收敛]]"]
created: 2026-08-25
updated: 2026-08-25
---

# Metz et al.：Unrolled GAN

> [!abstract] 来源定位
> 方法令 generator gradient 穿过若干步未来 discriminator optimization，以近似对手响应，并在特定 toy/实验设置改善 collapse。课程采用其“当前 critic 不等于 best response”机制；不把有限 unrolling 解释成精确 bilevel gradient 或普适覆盖保证。

## 边界

- unroll depth 0 回到当前对手；有限 depth 是 truncated response；
- 额外计算与内存必须纳入公平预算；
- mode coverage 改善是设置相关经验事实；
- generator 预见对手响应改变 game dynamics，不等于更准确估计某个固定 divergence。

