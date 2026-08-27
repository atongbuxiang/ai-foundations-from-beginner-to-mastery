---
type: source
status: verified
area: [sources, optimization, lion, optimizer-search]
source_type: paper
title: "Symbolic Discovery of Optimization Algorithms"
author: "Xiangning Chen et al."
year: 2023
url: "https://arxiv.org/abs/2302.06675"
venue: "NeurIPS 2023"
accessed: 2026-08-26
source_tier: A
license: "arXiv/会议论文；本库仅保存独立摘要、必要公式与链接"
scope_role: modern-comparison
temporal_role: modern-primary
related: ["[[Lion、Adafactor 与自适应优化器证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Chen 等：Lion

> [!abstract] 来源定位
> 论文把优化器发现表述为程序搜索，并得到 Lion：只保留一阶动量状态，用动量组合的 sign 作为更新方向。课程调用算法、状态成本与报告实验，不把代理任务搜索自动视为普遍最优性证明。

## 算法与证据边界

Lion 典型形式先用 $\beta_1m_{t-1}+(1-\beta_1)g_t$ 形成 sign direction，再以 $\beta_2$ 更新长期 momentum；只有一个与参数同形的一阶状态。每坐标方向幅值相同不等于每层 update RMS、函数空间位移或 wall-time 成本相同。

论文覆盖多类视觉、语言与多模态实验，是较强经验依据；但公平比较仍需记录 LR/decay 搜索空间、训练预算、batch、schedule、参数组和失败运行。
