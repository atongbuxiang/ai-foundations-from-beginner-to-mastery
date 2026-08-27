---
type: moc
status: active
area: [training, optimization, training-control]
prerequisites: ["[[SGD、Momentum 与随机优化噪声 MOC]]", "[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"]
related: ["[[训练与优化 MOC]]", "[[训练与优化完整课程地图与掌握标准]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 学习率、Warmup 与训练控制 MOC

> [!abstract] 分卷目标
> 学习率不是脱离更新方向的绝对速度。本卷把 LR、warmup、schedule、clipping、decay 与 averaging 放在同一控制系统里，要求报告端点、时域、参数组和交互。

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| TRN-33 | [[学习率、局部损失变化与相对更新尺度]] | 对齐 optimizer-specific step scale | 静态验收通过；个人掌握另计 |
| TRN-34 | [[Warmup、早期曲率与优化器状态建立]] | 区分多种机制假说 | 静态验收通过；个人掌握另计 |
| TRN-35 | [[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]] | 手算 schedule 端点与面积 | 静态验收通过；个人掌握另计 |
| TRN-36 | [[训练时域、Restart、Schedule-Free 与末端学习率]] | 审计 horizon change | 静态验收通过；个人掌握另计 |
| TRN-37 | [[全局逐层梯度裁剪、AGC 与裁剪偏差]] | 写出 clipping estimator | 静态验收通过；个人掌握另计 |
| TRN-38 | [[权重衰减、尺度不变性与 Weight RMS 动力学]] | 联立 LR/decay/RMS | 静态验收通过；个人掌握另计 |
| TRN-39 | [[参数 EMA、SWA 与 Checkpoint Averaging]] | 区分三种平均对象 | 静态验收通过；个人掌握另计 |
| TRN-40 | [[训练控制器的联合实验、消融与证据地图]] | 设计 factorial comparison | 静态验收通过；个人掌握另计 |

本卷不允许用“某 schedule 通常更好”作结；必须声明总步数、warmup fraction、peak/final LR、optimizer、batch、decay、selection rule 和 compute budget。

## 分卷实验与验收

- [[实验 - 训练控制器、调度时域与证据账审计]]：10 条确定性轨道、27 项机器断言与 3 个完整实验图文单元；
- [[60.5 分卷累计测验与复现门]]：理论 60 分、开卷复现 40 分；
- [[60.5 静态完成与质量审计]]：静态交付、链接、图像、来源和确定性复跑总账。

> [!success] 当前状态
> 60.5 已静态验收通过；`verified` 只表示材料和复现工具通过审计，个人掌握仍需独立完成题库、累计测验与真实框架迁移。
