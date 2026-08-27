---
type: moc
status: active
area: [training, scaling-laws, compute-allocation]
prerequisites: ["[[渐近记号、增长率与复杂度]]", "[[统计模型、估计量与偏差方差]]", "[[正则化、交叉验证与模型选择]]"]
related: ["[[训练与优化 MOC]]", "[[训练与优化完整课程地图与掌握标准]]", "[[科学空间 - 第六章训练与优化专题来源地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Scaling Law 与资源最优分配 MOC

> [!abstract] 分卷目标
> 把“画 log-log 直线”升级为带 offset、finite range、held-out scales 和成本口径的统计建模，并从约束优化推导 compute-optimal allocation，而不是背诵 Chinchilla 比例。

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| TRN-49 | [[经验 Scaling Law、幂律拟合与不可约项]] | 拟合并诊断 power law | 静态验收通过；个人掌握另计 |
| TRN-50 | [[Kaplan 参数数据律、联合拟合与有限区间]] | 区分 marginal/joint fits | 静态验收通过；个人掌握另计 |
| TRN-51 | [[Chinchilla、Compute-optimal 参数与数据分配]] | 推导 $N(C),D(C)$ | 静态验收通过；个人掌握另计 |
| TRN-52 | [[IsoFLOP、训练算力口径与系统校正]] | 建立 compute ledger | 静态验收通过；个人掌握另计 |
| TRN-53 | [[数据质量、重复、混合与有效 Token]] | 审计 token equivalence | 静态验收通过；个人掌握另计 |
| TRN-54 | [[过训练、推理成本与多目标最优规模]] | 比较 training/deployment optimum | 静态验收通过；个人掌握另计 |
| TRN-55 | [[Broken Scaling、涌现表象与优化架构数据分解]] | 区分 kink 竞争解释 | 静态验收通过；个人掌握另计 |
| TRN-56 | [[Scaling 实验设计、外推不确定性与证据地图]] | 做 held-out scale audit | 静态验收通过；个人掌握另计 |

一级来源以 Kaplan、Hoffmann/Chinchilla 及后续数据/推理成本研究为主；科学空间的量子化假说和 2026 三重奏提供解释框架，不承担普遍幂律定理。

## 卷级实验与验收

- [[实验 - Scaling Law、资源分配与外推证据审计]]：10 条定义/反例轨道、34 项机器断言和 3 张实验图；
- [[60.7 分卷累计测验与复现门]]：闭卷推导、开卷复现和真实小模型 scaling pilot；
- [[60.7 静态完成与质量审计]]：题号、来源、链接、图像、公式、实验与状态的最终审计。

## 题库入口

| 节点 | 习题 | 独立解答 |
|---|---|---|
| TRN-49 | [[习题 - 经验 Scaling Law、幂律拟合与不可约项]] | [[解答 - 经验 Scaling Law、幂律拟合与不可约项]] |
| TRN-50 | [[习题 - Kaplan 参数数据律、联合拟合与有限区间]] | [[解答 - Kaplan 参数数据律、联合拟合与有限区间]] |
| TRN-51 | [[习题 - Chinchilla、Compute-optimal 参数与数据分配]] | [[解答 - Chinchilla、Compute-optimal 参数与数据分配]] |
| TRN-52 | [[习题 - IsoFLOP、训练算力口径与系统校正]] | [[解答 - IsoFLOP、训练算力口径与系统校正]] |
| TRN-53 | [[习题 - 数据质量、重复、混合与有效 Token]] | [[解答 - 数据质量、重复、混合与有效 Token]] |
| TRN-54 | [[习题 - 过训练、推理成本与多目标最优规模]] | [[解答 - 过训练、推理成本与多目标最优规模]] |
| TRN-55 | [[习题 - Broken Scaling、涌现表象与优化架构数据分解]] | [[解答 - Broken Scaling、涌现表象与优化架构数据分解]] |
| TRN-56 | [[习题 - Scaling 实验设计、外推不确定性与证据地图]] | [[解答 - Scaling 实验设计、外推不确定性与证据地图]] |

> [!success] 当前状态
> 八个核心节点、八张机制图、120 道题与逐题解答、十轨道卷级实验、三张实验图和累计测验均已通过静态质量审计。本状态只表示教材 artifact 完整，学习者仍需完成习题、闭卷推导与真实小模型复现。
