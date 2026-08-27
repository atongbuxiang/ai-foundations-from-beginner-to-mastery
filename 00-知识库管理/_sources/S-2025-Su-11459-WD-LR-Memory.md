---
type: source
status: verified
area: [sources, optimization, weight-decay, schedule]
source_type: blog
title: "滑动平均视角下的权重衰减和学习率"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/11459"
accessed: 2026-08-26
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: research-hypothesis-entry
temporal_role: research-exposition
related: ["[[L2 正则、Coupled Decay 与 AdamW]]", "[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]", "[[权重衰减、尺度不变性与 Weight RMS 动力学]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 苏剑林：Weight Decay、Learning Rate 与滑动记忆

> [!abstract] 来源定位
> 文章从 $\theta_t=(1-\eta_t\lambda_t)\theta_{t-1}-\eta_tu_t$ 的精确乘法衰减出发，把训练轨迹解释为历史 update 的带权组合，并提出记忆时标与联合 schedule 的研究假说。课程采用权重核推导，不把“记住数据”写成信息容量定理。

## 课程采用

常数 LR/decay 下，距当前 $s$ 步的乘法权重近似

$$
(1-\eta\lambda)^s\approx e^{-\eta\lambda s},
$$

所以工程时标为 $O(1/(\eta\lambda))$。动态版本由累计量

$$
\kappa_t=\sum_{i=1}^t\eta_i\lambda_i
$$

控制初始化和历史 update 的权重。文章进一步在“每 batch 增量信息同等重要”、平均场与动量已衰减等假设下反推候选 LR/WD schedule。

## 证据分层

| 主张 | 等级 |
|---|---|
| 参数递推可展开为历史 update 的乘积权重 | exact identity |
| $1/(\eta\lambda)$ 是乘法衰减 e-folding 时标 | 近似 identity，需 $\eta\lambda$ 小 |
| 该时标等于模型的数据记忆能力 | 解释性假说 |
| 每个 batch 应拥有相等最终权重 | 设计原则/可证伪假说 |
| 由此得到的 schedule 普遍最优 | 不成立，需任务与实验验证 |

课程在 60.5 才系统讨论 schedule；60.2 只用它解释 AdamW 的状态与尺度边界。
