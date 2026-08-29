---
type: moc
status: active
area: [neural-networks]
aliases: [第三章总入口, 神经网络基础总入口]
prerequisites: ["[[数学基础完整课程地图与掌握标准]]", "[[学习理论完整课程地图与掌握标准]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[表示与模型架构 MOC]]", "[[训练与优化 MOC]]"]
created: 2026-08-14
updated: 2026-08-24
---

# 神经网络基础 MOC

> [!abstract] 核心问题
> 深层网络怎样把仿射映射、非线性、参数共享和随机训练部件组合成可表达、可微分、可训练且数值稳定的函数？第三章不只罗列模块 API，而是逐个回答前向对象、反向梯度、尺度传播、计算代价、参数对称性和失效边界。

固定的 64 节范围、ID、先修、掌握标准和验收规划见[[神经网络基础完整课程地图与掌握标准]]。

## 八卷入口

| 卷 | 入口 | 节点 | 一句话出口 |
|---|---|---:|---|
| 30.1 | [[前馈网络、感知机与表达能力 MOC]] | 8 | 从仿射神经元走到 MLP、万能逼近与深度表达 |
| 30.2 | [[计算图、反向传播与自动微分 MOC]] | 8 | 从局部导数重建高效反向传播 |
| 30.3 | [[激活函数、门控与非线性 MOC]] | 8 | 用梯度、尺度、平滑性和门控比较非线性 |
| 30.4 | [[初始化与信号传播 MOC]] | 8 | 控制前向方差、反向梯度和相关传播 |
| 30.5 | [[归一化、尺度与统计量 MOC]] | 8 | 区分 normalization 的轴、统计量和训练—推理语义 |
| 30.6 | [[残差连接、深度与稳定性 MOC]] | 8 | 用 Jacobian、动力系统和缩放理解深度可训练性 |
| 30.7 | [[Embedding、权重共享与输出参数化 MOC]] | 8 | 理解离散查表、共享矩阵与大词表输出层 |
| 30.8 | [[随机正则化与网络级泛化接口 MOC]] | 8 | 审计 dropout、随机深度、平滑和插值正则 |

## 总主线

```mermaid
flowchart LR
    F["仿射层与非线性"] --> G["计算图"]
    G --> B["反向传播 / AD"]
    B --> I["初始化与信号传播"]
    I --> N["归一化"]
    N --> R["残差与深度稳定"]
    R --> E["Embedding / 输出层"]
    E --> Q["随机正则化"]
    Q --> F
```

## 每个部件的六问

1. 前向映射的定义域、值域与张量形状是什么？
2. 反向 VJP/梯度怎样推导，分支和广播在哪里累加？
3. 均值、方差、范数、相关性和 Jacobian spectrum 怎样随深度变化？
4. 时间、显存、通信和数值稳定性代价是什么？
5. 它具有哪些重缩放、置换或平移不变性？
6. 删除假设、切换 train/eval、改变 batch/precision 后怎样失败？

## 当前状态

```text
locked scope: 64 / 64
formal nodes: 64 / 64
exercise sets: 64 / 64
solutions: 64 / 64
current-standard teaching migration: 64 / 64
teaching migration pending: 0 / 64
material-regression-passed volumes: 8 / 8
NN-CUM-01 material: regression-passed
state: draft nodes / 30.1--30.8 material regression-passed / cumulative material regression-passed / not-attempted learner
next: execute personal oral, closed-book, nonce-blind, 48 h and 14 d evidence; do not infer mastery from material
```

NN-01—64 已形成 64/64 静态骨架与 960 道节点题。[[neural_network_foundations_teaching_contract_audit.py]]确认 NN-01—64 达到 **64/64 现行教学迁移**，待迁移为 **0/64**；30.1—30.8 静态材料门达到 **8/8 `regression-passed`**。个人仍为 `not-attempted`。

累计出口[[阶段测验 - 神经网络基础（第三章）]]、[[阶段测验解答 - 神经网络基础（第三章）]]与[[实验 - 神经网络基础累计复现门]]已由[[neural_network_foundations_cumulative_contract_audit.py]]按现行合同回归为 `regression-passed`：64 节范围、14/14 题解与 100 分、20 分钟口试、答案隔离、scorer nonce、三轨盲参数、canonical/固定盲参双跑、非法输入保护、48 小时换机制和 14 天陌生迁移均有静态与计算证书。个人仍为 `not-attempted`，材料建设不等于个人八卷或累计门已经通过。

## NN-CUM-01：八卷累计证据出口

| 阶段 | 直接证据 | 材料状态 | 个人状态 |
|---|---|---|---|
| 口试 | 十二层对象账本、VJP/尺度主链、陌生 block 审计 | regression-passed | not-attempted |
| 闭卷 | 240 分钟、A—E 五区、14 题、100 分 | regression-passed | not-attempted |
| 计算门 | nonce 指定轨、运行前预测、新 stdout/SVG/hash | regression-passed | not-attempted |
| 延迟门 | 48 h 换机制、14 d 陌生 AI 模型迁移 | regression-passed | not-attempted |

Canonical 图 hash 为 `aac6c5167ac56ff94b1f7b374d4fdc22deda5cb336b5fb6bdc94059dfdc8bb0e`；固定盲参 hash 为 `a36bc4dfb6dda830b0b4e5bd82f0962c2224f1e0e6b9f18dbc3ae6b5260d8c4f`。两者只认证工具，不可填入个人证据字段。
