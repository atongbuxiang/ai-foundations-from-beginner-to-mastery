---
type: moc
status: active
area: [training, optimization, parameterization, mup]
prerequisites: ["[[方差传播与宽层均值场近似]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[矩阵范数]]"]
related: ["[[训练与优化 MOC]]", "[[训练与优化完整课程地图与掌握标准]]", "[[科学空间 - 第六章训练与优化专题来源地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 参数化、μP 与尺度迁移 MOC

> [!abstract] 分卷目标
> 参数化决定“宽度变化时什么保持 $\Theta(1)$”。本卷比较 standard/NTK/mean-field/μP，并把 μTransfer 从规则表提升为可手推、可做 base-shape oracle 的尺度合同。

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| TRN-41 | [[模型尺度、稳定性指标与 Width-Depth 对象合同]] | 声明 scale axis | 静态验收通过；个人掌握另计 |
| TRN-42 | [[Standard、NTK 与 Mean-field 参数化]] | 比较 limiting regime | 静态验收通过；个人掌握另计 |
| TRN-43 | [[μP 的 Maximal Update 与宽度尺度推导]] | 推导 width exponents | 静态验收通过；个人掌握另计 |
| TRN-44 | [[Tensor Programs、坐标检查与无限宽极限]] | 连接 coordinate law | 静态验收通过；个人掌握另计 |
| TRN-45 | [[μTransfer、Base Shape 与超参数零样本迁移]] | 建立 transfer protocol | 静态验收通过；个人掌握另计 |
| TRN-46 | [[Embedding、Readout、Attention 与特殊参数组缩放]] | 处理 non-hidden parameters | 静态验收通过；个人掌握另计 |
| TRN-47 | [[谱条件、高阶 μP 与参数更新稳定性]] | 比较 RMS 与 operator control | 静态验收通过；个人掌握另计 |
| TRN-48 | [[Scale-up 协议、μP 证据与失效边界]] | 验收跨规模迁移 | 静态验收通过；个人掌握另计 |

科学空间的初探 μP、高阶 μP 与“MuP 之上”系列贯穿本卷；原创 maximal-update/tensor-program 结论必须回查 Tensor Programs，博客中的谱条件和各向同性视角以可证伪假说进入实验。

## 卷级实验与验收

- [[实验 - μP 坐标、谱条件与尺度迁移审计]]：10 条定义/反例轨道、29 项机器断言和 3 张实验图；
- [[60.6 分卷累计测验与复现门]]：闭卷推导、开卷复现和真实小模型 scale-up 协议；
- [[60.6 静态完成与质量审计]]：题号、来源、链接、图像、公式、实验与状态的最终审计。

> [!success] 当前状态
> 八个核心节点、八张机制图、120 道题与逐题解答、十轨道卷级实验、三张实验图和累计测验均已通过静态质量审计。本状态只表示教材 artifact 完整，学习者仍需完成习题、闭卷推导与真实小模型复现。
