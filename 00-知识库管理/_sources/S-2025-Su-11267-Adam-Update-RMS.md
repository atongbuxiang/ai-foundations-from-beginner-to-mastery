---
type: source
status: verified
area: [sources, optimization, adam, mean-field]
source_type: blog
title: "为什么Adam的Update RMS是0.2？"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/11267"
accessed: 2026-08-26
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
scope_role: chinese-derivation-entry
temporal_role: research-exposition
related: ["[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]", "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 苏剑林：Adam Update RMS

> [!abstract] 来源定位
> 文章从模拟与平均场近似解释特定大模型配方中 Adam direction RMS 常在 0.2—0.3，并得到低 SNR 稳态近似。课程采用其推导和可复现实验，不把 0.2 写成 Adam 的定义或跨任务常数。

## 推导骨架

在 $t\to\infty$、epsilon 可忽略、坐标 gradient 近似 i.i.d.，令 $\mathbb E[g]=\mu$、$\operatorname{Var}(g)=\sigma^2$。对

$$u_t=m_t/\sqrt{v_t}$$

采用 $\mathbb E[m_t^2/v_t]\approx\mathbb E[m_t^2]/\mathbb E[v_t]$，得到

$$
\operatorname{RMS}(u_t)^2
\approx
\frac{\|\mu\|^2/\|\sigma\|^2+(1-\beta_1)/(1+\beta_1)}
{\|\mu\|^2/\|\sigma\|^2+1}.
$$

低 SNR 且 $\beta_1=0.9$ 时约为 $\sqrt{0.1/1.9}=0.2294$。

## 边界

- ratio of expectations 不是 expectation of ratio 的恒等式；
- $\beta_2$ 近似消失依赖稳态与 denominator concentration，较小 $\beta_2$ 时误差会增大；
- 非零均值、时间相关、重尾、epsilon、bias correction 与参数分组都会改变结果；
- observed Update RMS 反推 SNR 是诊断性估计，不是可辨识性定理。
