---
type: source
status: verified
area: [sources, ai/scaling-laws, extrapolation]
source_type: paper
title: "Revisiting Neural Scaling Laws in Language and Vision"
author: "Ibrahim M. Alabdulmohsin, Behnam Neyshabur, Xiaohua Zhai"
year: 2022
url: "https://proceedings.neurips.cc/paper_files/paper/2022/hash/8c22e5e918198702765ecff4b20d0a90-Abstract-Conference.html"
accessed: 2026-08-26
source_tier: A
license: "NeurIPS paper; independent summary only"
scope_role: core-method
temporal_role: active-research
related: ["[[经验 Scaling Law、幂律拟合与不可约项]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Revisiting Neural Scaling Laws in Language and Vision

> [!abstract] 来源定位
> 论文把 scaling-law 估计从“训练窗口内拟合最好”转向“held-out 尺度外推误差更小”，并给出从 learning curves 可靠估计参数的经验方法。课程用它支持 extrapolation loss、函数族选择与 held-out scale，而不是某一组固定指数。

## 可调用证据

- 插值残差小不等于外推可靠；
- 不同函数族可在观测窗口内几乎重合、在窗口外显著分离；
- fitting protocol 应以未参与拟合的较大尺度评估；
- 论文跨语言、视觉与多种架构比较估计方法，说明“选函数”本身属于实验设计。

## 边界

- 论文给的是经验估计 recipe，不是保证真实曲线属于某个函数族的定理；
- held-out scales 仍可能离真正 target 太近，不能消除 regime change；
- 跨任务结果不能替代当前模型族、指标和训练协议中的重新验证。
