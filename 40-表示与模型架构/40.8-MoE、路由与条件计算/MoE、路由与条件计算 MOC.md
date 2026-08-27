---
type: moc
status: active
area: [architecture, moe, conditional-compute]
related: ["[[表示与模型架构完整课程地图与掌握标准]]", "[[科学空间 - 第四章专题来源地图]]"]
created: 2026-08-24
updated: 2026-08-24
---

# MoE、路由与条件计算 MOC

> [!abstract] 本卷主线
> MoE 用输入相关的稀疏路由，把总参数容量与每 token 激活专家计算解耦；随之引入离散选择、容量溢出、负载控制与跨设备通信。本卷从模型函数一路追到系统执行，并用 I/T/E/H/O 区分恒等式、有限条件理论、实验、解释和开放问题。

## 建议学习顺序

1. 用 ARCH-57 建立 total/active/resident parameters 与 MAC/bytes/latency 的分账；
2. 用 ARCH-58—59 写完整路由合同，再把 Top-k assignment 变成 capacity-aware dispatch；
3. 用 ARCH-60—61 比较辅助损失、反馈 bias 与容量约束 assignment；
4. 用 ARCH-62—63 分离专家设计轴和 Expert Parallel 系统代价；
5. 用 ARCH-64 收束门控归一化、Hash 对照、证据等级和开放问题。

| ID | 节点 | 学习出口 | 状态 |
|---|---|---|---|
| ARCH-57 | [[条件计算、专家混合与稀疏激活]] | capacity/compute separation | 正文、图、A–E 题解完成 |
| ARCH-58 | [[Router、Gate、Top-k 与稀疏组合]] | routing contract | 正文、图、A–E 题解完成 |
| ARCH-59 | [[Expert Capacity、Dispatch 与 Token Dropping]] | dispatch audit | 正文、图、A–E 题解完成 |
| ARCH-60 | [[MoE 负载均衡辅助损失与偏置]] | objective separation | 正文、图、A–E 题解完成 |
| ARCH-61 | [[Loss-Free 路由、偏置更新与分配视角]] | feedback balancing | 正文、图、A–E 题解完成 |
| ARCH-62 | [[细粒度专家、共享专家与动态激活]] | expert granularity | 正文、图、A–E 题解完成 |
| ARCH-63 | [[Expert Parallel、All-to-All 与通信成本]] | system cost ledger | 正文、图、A–E 题解完成 |
| ARCH-64 | [[MoE 门控归一化、证据地图与开放问题]] | evidence/open-problem audit | 正文、图、A–E 题解完成 |

## 科学空间拓展线

- 10699 从专家输出几何理解 Router，但“预测输出范数”保留为可检验 `H/E`；
- 10735、10757、11619、11626 把辅助损失、bias feedback、assignment/quantile 和动态激活连成一条优化—控制线；
- 10815、10945 讨论动态专家数、共享与细粒度专家，机制解释不替代 matched-budget 消融；
- 11750、11760、11782、11848 分别提供固定路由、序列均衡、门控归一化和近期整体系的开放问题入口。

## 卷内验收

- 题库：8 组 × 15 题，共 120 题；每个 A—E 层级 24 题，解答 ID 一一对应；
- 确定性复现：[[00-知识库管理/_labs/code/architecture_moe_audit.py]]，覆盖容量/MAC、路由、dispatch、辅助梯度、反馈/assignment、专家轴、All-to-All 和门控边界；
- 图像：8 张原创矢量教学图，每张均含视觉问题、来源、读图说明和不可推出项；
- 状态边界：静态材料与 toy audit 完成，不等于真实学习通过，也不等于某 MoE 合同在未知任务/集群上最优。
