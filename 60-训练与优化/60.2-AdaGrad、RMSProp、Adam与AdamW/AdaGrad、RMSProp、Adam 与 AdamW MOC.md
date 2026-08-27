---
type: moc
status: active
area: [training, optimization, adaptive-methods]
prerequisites: ["[[SGD、Momentum 与随机优化噪声 MOC]]", "[[自适应优化方法]]", "[[数值稳定性]]"]
related: ["[[训练与优化 MOC]]", "[[训练与优化完整课程地图与掌握标准]]", "[[科学空间 - 第六章训练与优化专题来源地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# AdaGrad、RMSProp、Adam 与 AdamW MOC

> [!abstract] 分卷目标
> 从 diagonal variable metric 重建自适应优化器，既理解为何它们在稀疏/异尺度问题上有吸引力，也能指出 epsilon、bias correction、decay coupling 和反例如何改变有限步算法。

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| TRN-09 | [[AdaGrad、累计平方梯度与稀疏几何]] | 解释 cumulative preconditioner | 静态验收通过；个人掌握另计 |
| TRN-10 | [[RMSProp、滑动二阶矩与非平稳尺度]] | 解释 forgetting time scale | 静态验收通过；个人掌握另计 |
| TRN-11 | [[Adam 的一阶二阶矩、偏差修正与逐坐标步长]] | 手算完整 Adam state | 静态验收通过；个人掌握另计 |
| TRN-12 | [[Adam 的 Epsilon、数值稳定与实现分歧]] | 审计 epsilon placement | 静态验收通过；个人掌握另计 |
| TRN-13 | [[Adam 收敛反例、AMSGrad 与条件化保证]] | 重建经典反例 | 静态验收通过；个人掌握另计 |
| TRN-14 | [[Adam 的尺度不变性、Sign 近似与 Update RMS]] | 审计 scale-free/RMS 解释 | 静态验收通过；个人掌握另计 |
| TRN-15 | [[L2 正则、Coupled Decay 与 AdamW]] | 区分 regularizer 与 decay | 静态验收通过；个人掌握另计 |
| TRN-16 | [[Lion、Adafactor 与自适应优化器证据地图]] | 比较状态内存、质量和成本 | 静态验收通过；个人掌握另计 |

统一记录 $(m_t,v_t,t)$ 的初始化、更新顺序、bias correction、epsilon 位置、weight decay 位置和 step skip 语义；不允许只写“Adam 公式”而忽略 framework variant。

科学空间主线：[[S-2024-Su-10588-Hessian近似与自适应学习率]]、[Adam epsilon](https://spaces.ac.cn/archives/10563)、[Update RMS](https://spaces.ac.cn/archives/11267)、[AdamW Weight RMS](https://spaces.ac.cn/archives/11307)。这些文章的 mean-field/curvature 解释不替代 Adam/AMSGrad/AdamW 原论文。

卷终必须能用手算和脚本回答：何时 $m_t/\sqrt{v_t}$ 近似 sign；为何 L2 与 decoupled decay 在 diagonal preconditioner 下不同；同一个 epsilon 在 FP32 与 BF16 中的数值角色是什么。

## 练习、实验与验收

- 每个节点均有独立的 15 题 A—E 分层习题与逐题解答，共 120 题；
- [[实验 - 自适应优化器状态、尺度与反例数值审计]]：9 条轨道、13 项断言与三张确定性实验图；
- [[60.2 分卷累计测验与复现门]]：闭卷理论、脚本复现、假设干预和真实 optimizer 审计；
- [[60.2 静态完成与质量审计]]：文件、链接、图像、题号、来源与数值证据的静态完成报告。

> [!warning] 掌握状态
> 本卷材料已静态验收，不代表学习者已完成独立作答、延迟重做、脚本干预与真实模型审计。
