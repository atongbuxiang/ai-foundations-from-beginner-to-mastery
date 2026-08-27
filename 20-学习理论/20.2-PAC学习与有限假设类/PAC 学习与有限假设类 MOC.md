---
type: moc
status: active
area: [learning-theory/pac]
prerequisites: ["[[学习问题、决策与风险 MOC]]", "[[浓缩不等式]]"]
related: ["[[学习理论完整课程地图与掌握标准]]", "[[VC 维与一致收敛 MOC]]"]
created: 2026-08-20
updated: 2026-08-23
---

# PAC 学习与有限假设类 MOC

> [!abstract] 本卷任务
> 从一个固定 hypothesis 的 concentration 出发，经 union bound 走到 finite-class ERM guarantee；完整展开 probability 对 sample/algorithm 的量词和 realizable/agnostic 的不同 sample complexity。

| ID | 节点 | 关键出口 | 状态 |
|---|---|---|---|
| LT-09 | [[泛化间隙与浓缩不等式接口]] | fixed-hypothesis generalization | draft + A–E 闭环 |
| LT-10 | [[PAC 学习定义与样本复杂度]] | $\epsilon,\delta,m$ 量词合同 | draft + A–E 闭环 |
| LT-11 | [[有限假设类、Union Bound 与一致收敛]] | $\log|\mathcal H|$ complexity | draft + A–E 闭环 |
| LT-12 | [[可实现情形的一致 ERM 保证]] | consistent learner guarantee | draft + A–E 闭环 |
| LT-13 | [[不可知 PAC、ERM 与双侧一致收敛]] | excess-risk guarantee | draft + A–E 闭环 |
| LT-14 | [[Occam 界、编码长度与先验权重]] | countable weighted classes | draft + A–E 闭环 |
| LT-15 | [[No-Free-Lunch 与归纳偏置]] | 无结构不可普遍学习 | draft + A–E 闭环 |
| LT-16 | [[样本复杂度下界与 Minimax 视角]] | upper/lower bound 分离 | draft + A–E 闭环 |

当前为 **8/8 正文，8/8 独立 v2 图文单元，0/8 经真实验收**。LT-09—16 已完成正文、每章独立的教材式证明地图、读图方法、适用边界、初学者自检问题，以及每节点 15 道 A—E 习题与独立详解；图示由 [[plot_pac_finite_class_v2.py]] 确定性生成，并通过 SVG 结构、XML、1200 px 渲染与人工视觉检查。`draft` 只表示课程材料成稿，尚不能替代学习者的闭卷作答与延迟复测证据。
