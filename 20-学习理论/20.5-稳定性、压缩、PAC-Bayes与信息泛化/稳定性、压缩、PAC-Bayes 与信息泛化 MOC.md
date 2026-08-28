---
type: moc
status: active
area: [learning-theory/algorithm-dependent]
prerequisites: ["[[PAC 学习与有限假设类 MOC]]", "[[交叉熵与 KL 散度]]", "[[互信息与依赖性]]"]
assessment: "[[阶段测验 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）]]"
solution: "[[阶段测验解答 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）]]"
experiment: "[[实验 - 稳定性、压缩、PAC-Bayes 与信息泛化累计复现门]]"
related: ["[[学习理论完整课程地图与掌握标准]]", "[[数据依赖复杂度、间隔与快率 MOC]]", "[[推导与实验 MOC]]"]
created: 2026-08-20
updated: 2026-08-28
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

当前为 **8/8 正文、8/8 习题与独立详解，0/8 经真实作答验收**。20.5 已完成 draft 闭环：从 stability、sample compression 延伸到 PAC-Bayes 与 information-theoretic generalization，并以五类证书比较收束。

## 卷级材料门：ALG-CUM-01

本卷现已建立[[阶段测验 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）|ALG-CUM-01]]、[[阶段测验解答 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）|独立封存详解]]与[[实验 - 稳定性、压缩、PAC-Bayes 与信息泛化累计复现门|三轨累计复现门]]。三轨分别核对 replace-one/mean/RERM/SGD、compression/PAC-Bayes-kl、binary-channel MI/证书选择；题卷以 20 分钟口试、210 分钟闭卷、scorer nonce、跨轨盲参、48 小时与 14 天迁移防止照图复述。[[algorithmic_generalization_cumulative_contract_audit.py]]独立重算数值锚点并检查 canonical/盲参双跑、SVG/XML/hash、support 与覆盖保护。

因此本卷的**验收材料**为 `regression-passed`，但学习者仍为 `not-attempted`，不得把 8/8 材料闭环写成个人通过。全章卷级材料门现为 **5/10**；下一步先建立 20.1—20.5 的 LT-QUAL-01 跨卷资格考，再推进 20.6。
