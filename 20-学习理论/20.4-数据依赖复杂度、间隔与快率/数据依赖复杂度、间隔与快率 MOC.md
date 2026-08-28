---
type: moc
status: active
area: [learning-theory/empirical-process]
prerequisites: ["[[VC 维与一致收敛 MOC]]", "[[期望、方差与矩]]", "[[浓缩不等式]]"]
related: ["[[学习理论完整课程地图与掌握标准]]", "[[阶段测验 - 数据依赖复杂度、间隔与快率（20.4）]]", "[[实验 - 数据依赖复杂度、间隔与快率累计复现门]]", "[[稳定性、压缩、PAC-Bayes 与信息泛化 MOC]]"]
created: 2026-08-20
updated: 2026-08-28
---

# 数据依赖复杂度、间隔与快率 MOC

> [!abstract] 本卷任务
> 从 ghost sample 与 symmetrization 建立 empirical-process 主线；用 Rademacher complexity、norm、margin、covering 和 localization 得到比全局 worst-case 容量更贴近数据的界。

| ID | 节点 | 关键出口 | 状态 |
|---|---|---|---|
| LT-25 | [[Ghost Sample、对称化与经验过程入口]] | expectation difference reduction | draft + A–E 闭环 |
| LT-26 | [[Rademacher 复杂度与经验复杂度]] | data-dependent capacity | draft + A–E 闭环 |
| LT-27 | [[收缩引理与 Lipschitz 损失复合]] | complexity through loss | draft + A–E 闭环 |
| LT-28 | [[范数约束线性类的复杂度]] | norm/data-radius bound | draft + A–E 闭环 |
| LT-29 | [[分类间隔、Margin Bound 与 SVM 接口]] | empirical margin distribution | draft + A–E 闭环 |
| LT-30 | [[覆盖数、Metric Entropy 与 Chaining 入口]] | multiscale complexity | draft + A–E 闭环 |
| LT-31 | [[局部 Rademacher 复杂度与快收敛率]] | localized fixed point | draft + A–E 闭环 |
| LT-32 | [[Fat-Shattering、回归与 Lipschitz 风险]] | scale-sensitive real-valued capacity | draft + A–E 闭环 |

当前为 **8/8 正文、8/8 A—E 习题与独立详解、0/8 经真实验收**。LT-25—32 共配置 8 张独立 paper-ink v2 图，全部通过 SVG 结构、XML、1200×600 实际渲染与逐图视觉检查；两套生成器连续复跑哈希 8/8 稳定。本卷已形成 ghost sample → symmetrization → Rademacher → contraction → norm/margin → entropy/chaining → local fixed point → fat-scale regression 的闭环。下一施工批次进入 20.5 的 LT-33—40；`draft` 不替代闭卷证明、延迟复测与迁移证据。

## 卷级累计证据门

- 题卷：[[阶段测验 - 数据依赖复杂度、间隔与快率（20.4）|RAD-CUM-01]]；
- 独立详解：[[阶段测验解答 - 数据依赖复杂度、间隔与快率（20.4）]]；
- 三轨复现：[[实验 - 数据依赖复杂度、间隔与快率累计复现门]]；
- 独立审计：[[rademacher_margin_local_cumulative_contract_audit.py]]。

材料门以 exact signs/双范数—margin 共同选择—cover/local/fat 三轨把八节点压成一条证据链，并含 20 分钟口试、210 分钟 100 分闭卷、`attempt_id + scorer nonce`、跨轨盲参、48 小时换机制与 14 天陌生迁移。当前仅是 `regression-passed` 材料；个人仍为 `not-attempted`，八篇正文仍为 `draft`。全章已建立 **4/10** 卷级材料门，个人通过 **0/10**；下一施工点为 20.5 的 LT-33—40。
