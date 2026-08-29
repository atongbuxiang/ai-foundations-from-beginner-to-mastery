---
type: moc
status: active
area: [neural-networks/embedding-output]
prerequisites: ["[[前馈网络、感知机与表达能力 MOC]]", "[[交叉熵与 KL 散度]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[随机正则化与网络级泛化接口 MOC]]"]
created: 2026-08-23
updated: 2026-08-29
---
# Embedding、权重共享与输出参数化 MOC
| ID | 节点 | 出口 | 状态 |
|---|---|---|---|
| NN-49 | [[Embedding Lookup、稀疏梯度与参数规模]] | lookup algebra | draft + A–E 闭环 |
| NN-50 | [[Embedding 几何、相似度与各向异性]] | representation geometry | draft + A–E 闭环 |
| NN-51 | [[输入—输出权重共享与 Weight Tying]] | shared matrix | draft + A–E 闭环 |
| NN-52 | [[Softmax 输出层、Logit 尺度与概率参数化]] | categorical head | draft + A–E 闭环 |
| NN-53 | [[Softmax Bottleneck 与低秩限制]] | rank restriction | draft + A–E 闭环 |
| NN-54 | [[Sampled、Hierarchical 与 Adaptive Softmax]] | large-vocab cost | draft + A–E 闭环 |
| NN-55 | [[Padding、Mask、特殊符号与词表边界]] | discrete contract | draft + A–E 闭环 |
| NN-56 | [[Embedding 初始化、缩放、分解与量化接口]] | scale/compression | draft + A–E 闭环 |

## 当前迁移与学习状态

- [[neural_network_foundations_teaching_contract_audit.py]]已复核 NN-49—56 的两遍路线、问题链、对象账本、$\mathcal E_\square$ 四词二维参数表、lookup/scatter-add、几何谱、共享参数、Softmax 温度、rank bottleneck、采样偏差、mask 事务与压缩误差；
- 当前为 **8/8 现行教学迁移、8/8 正文、8/8 A—E 题解、8/8 正式图，30.7 材料门 `regression-passed`**；
- 全章为 **56/64 已迁移、8/64 pending、分卷材料门 7/8**，个人仍为 **0/8 / `not-attempted`**；下一批 NN-57—60。

NN-49—56 共 120 题与逐题独立详解已经形成全卷静态闭环：前半从 lookup/scatter-add 推进到表示几何、共享 Parameter 双路径 VJP 和 Softmax 概率参数化；后半进一步处理跨 context 的 centered log-ratio rank、采样/树/adaptive 大词表合同、padding/mask/词表事务，以及初始化—分解—量化的函数类与系统账。`draft` 只表示材料完备，学习者仍需闭卷、重做与迁移验收。
