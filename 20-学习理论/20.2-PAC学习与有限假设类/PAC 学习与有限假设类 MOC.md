---
type: moc
status: active
area: [learning-theory/pac]
prerequisites: ["[[学习问题、决策与风险 MOC]]", "[[浓缩不等式]]"]
related: ["[[学习理论完整课程地图与掌握标准]]", "[[VC 维与一致收敛 MOC]]", "[[阶段测验 - PAC 学习与有限假设类（20.2）]]", "[[实验 - PAC 学习与有限假设类累计复现门]]"]
created: 2026-08-20
updated: 2026-08-28
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

## 卷级累计证据门

- 题卷：[[阶段测验 - PAC 学习与有限假设类（20.2）|PAC-CUM-01]]，20 分钟口试加 210 分钟闭卷；
- 独立详解：[[阶段测验解答 - PAC 学习与有限假设类（20.2）]]，在原稿、nonce 与运行前预测冻结后才可打开；
- 三轨实验：[[实验 - PAC 学习与有限假设类累计复现门]]，并排检查可实现 survival/Union/exp 证书、不可知 lexicographic ERM 与共同事件、Occam/Kraft 上界和 Bernoulli 两点检验下界；
- 确定性总图：[[plot-pac-finite-class-cumulative-gate-v2.svg]]，由[[pac_finite_class_cumulative_gate.py]]生成；
- 独立回归：[[pac_finite_class_cumulative_contract_audit.py]]复核 8/8 scope、14/14 题解与 100 分、解析锚点、canonical/固定盲参双跑、SVG/XML/hash、Kraft 与覆盖保护、六处状态面；
- 延迟门：48 小时换机制重建与 14 天陌生 adaptive-evaluation 迁移。

> [!success] 材料门已建立，学习状态未改变
> PAC-CUM-01 的题卷、详解、实验、脚本与总图为 `regression-passed`；个人仍是 `0/8 经真实验收 / not-attempted`，八篇正文继续保持 `draft`。不能把 canonical 图或审计通过写成个人掌握。

下一卷：[[VC 维与一致收敛 MOC]]。20.3 将把有限类的 $\log|\mathcal H|$ 替换为样本上的 labeling growth、shattering 与 capacity control。
