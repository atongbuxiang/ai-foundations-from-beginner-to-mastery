---
type: moc
status: active
area: [learning-theory/algorithm-dependent]
prerequisites: ["[[PAC 学习与有限假设类 MOC]]", "[[交叉熵与 KL 散度]]", "[[互信息与依赖性]]"]
related: ["[[学习理论完整课程地图与掌握标准]]", "[[数据依赖复杂度、间隔与快率 MOC]]"]
created: 2026-08-20
updated: 2026-08-23
---

# 稳定性、压缩、PAC-Bayes 与信息泛化 MOC

> [!abstract] 本卷任务
> 把泛化对象从整个 hypothesis class 转向具体 algorithm、compressed description、randomized posterior 与 sample information；比较这些界的量词、可计算性和深网适用边界。

| ID | 节点 | 关键出口 | 状态 |
|---|---|---|---|
| LT-33 | [[算法稳定性与替换一个样本]] | replace-one sensitivity | draft + A–E 闭环 |
| LT-34 | [[正则化 ERM 的稳定性]] | curvature → stability | draft + A–E 闭环 |
| LT-35 | [[随机梯度算法的稳定性接口]] | steps/smoothness/time tradeoff | draft + A–E 闭环 |
| LT-36 | [[样本压缩方案与泛化]] | compression-size bound | draft + A–E 闭环 |
| LT-37 | [[PAC-Bayes Bound 的测度变换主线]] | empirical risk + KL | draft + A–E 闭环 |
| LT-38 | [[PAC-Bayes 先验、后验与数据依赖边界]] | legal prior/posterior contract | draft + A–E 闭环 |
| LT-39 | [[互信息与信息论泛化界]] | sample-output information | draft + A–E 闭环 |
| LT-40 | [[容量界、稳定性界与 PAC-Bayes 的比较]] | bound-selection audit | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 习题与独立详解，0/8 经真实作答验收**。20.5 已完成 draft 闭环：从 stability、sample compression 延伸到 PAC-Bayes 与 information-theoretic generalization，并以五类证书比较收束。下一批进入 20.6 的 LT-41—44：偏差—方差、正则化与交叉验证、线性回归、逻辑回归。
