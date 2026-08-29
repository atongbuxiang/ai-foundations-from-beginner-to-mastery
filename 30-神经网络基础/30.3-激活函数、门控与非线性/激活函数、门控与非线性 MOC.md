---
type: moc
status: active
area: [neural-networks/activations]
prerequisites: ["[[计算图、反向传播与自动微分 MOC]]"]
related: ["[[神经网络基础完整课程地图与掌握标准]]", "[[初始化与信号传播 MOC]]"]
created: 2026-08-23
updated: 2026-08-29
---
# 激活函数、门控与非线性 MOC
| ID | 节点 | 出口 | 状态 |
|---|---|---|---|
| NN-17 | [[激活函数的角色、选择准则与函数性质]] | choice contract | draft + A–E 闭环 |
| NN-18 | [[Sigmoid、Tanh 与饱和梯度]] | saturation | draft + A–E 闭环 |
| NN-19 | [[ReLU、Leaky ReLU 与次梯度约定]] | piecewise linearity | draft + A–E 闭环 |
| NN-20 | [[ELU、SELU 与自归一化接口]] | self-normalizing claim | draft + A–E 闭环 |
| NN-21 | [[Softplus、GELU、SiLU 与平滑门控]] | smooth activations | draft + A–E 闭环 |
| NN-22 | [[GLU、GeGLU、SwiGLU 与乘性门]] | multiplicative gates | draft + A–E 闭环 |
| NN-23 | [[Maxout、分段线性区域与条件计算]] | max-affine regions | draft + A–E 闭环 |
| NN-24 | [[激活函数的数值稳定、尺度与经验选择]] | fair comparison | draft + A–E 闭环 |

## 当前迁移与学习状态

- [[neural_network_foundations_teaching_contract_audit.py]]已复核 NN-17—24 的两遍路线、问题链、对象账本、$s_\triangle$ 共享探针与公式七问；
- 前半卷闭合 sigmoid/tanh 饱和、ReLU/Leaky kink 与 ELU 负支；后半卷独立复算 Softplus/GELU/SiLU、GLU/SwiGLU 两路 VJP 与 Maxout winner，并将局部事实升级为五道证据门；
- 当前为 **8/8 现行教学迁移、8/8 正文、8/8 A—E 题解、8/8 正式图，30.3 材料门 `regression-passed`**；
- 全章为 **52/64 已迁移、12/64 pending、分卷材料门 6/8**，30.7 前半卷 `in-progress`，个人仍为 **0/8 / `not-attempted`**；下一批 NN-53—56。
