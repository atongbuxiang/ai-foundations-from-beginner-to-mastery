---
type: moc
status: active
area: [training, optimization, matrix-optimization, muon]
prerequisites: ["[[矩阵范数]]", "[[极分解]]", "[[矩阵符号函数]]", "[[Riemann 几何、测地线与流形优化]]"]
related: ["[[训练与优化 MOC]]", "[[训练与优化完整课程地图与掌握标准]]", "[[科学空间 - 第六章训练与优化专题来源地图]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 矩阵优化、谱最速下降与 Muon MOC

> [!abstract] 分卷目标
> 从“最速下降依赖 norm”开始，推到 spectral/nuclear duality 和 matrix sign，再把数学方向变成含 momentum、shape scaling、Newton–Schulz、parameter groups 和 distributed cost 的 Muon 程序。

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| TRN-25 | [[最速下降、范数选择与对偶范数]] | 从单位球推导方向 | 静态验收通过；个人掌握另计 |
| TRN-26 | [[矩阵梯度、谱核范数对偶与 Matrix Sign]] | 证明 polar direction | 静态验收通过；个人掌握另计 |
| TRN-27 | [[Muon 的动量、正交化与参数分组合同]] | 实现完整 optimizer step | 静态验收通过；个人掌握另计 |
| TRN-28 | [[Newton–Schulz Matrix Sign 的收敛与有限精度]] | 做 singular-value residual audit | 静态验收通过；个人掌握另计 |
| TRN-29 | [[Muon 形状缩放、Update RMS 与版本差异]] | 互译三类当前 scaling | 静态验收通过；个人掌握另计 |
| TRN-30 | [[Muon、Shampoo、SOAP 与隐式曲率关系]] | 严格限定相似与不等价 | 静态验收通过；个人掌握另计 |
| TRN-31 | [[Stiefel、谱球面、旋转 Muon 与约束更新]] | 区分 tangent/retraction/exact update | 静态验收通过；个人掌握另计 |
| TRN-32 | [[Muon 的扩展证据、系统成本与迁移边界]] | 审计规模证据和切换风险 | 静态验收通过；个人掌握另计 |

科学空间在本卷是主力第二入口：Muon 赏析/续集/指南、msign Newton–Schulz、流式幂迭代、MuP 之上、流形最速下降与 2026 解析结果。所有博客公式仍必须回到 norm duality、polar decomposition、matrix function 和公开训练证据。

## 推荐学习路径

1. TRN-25—26：从一般 norm duality 推到 spectral/nuclear duality，先得到 exact mathematical target；
2. TRN-27—29：把 target 落成带版本的 Muon state machine，并审计 finite-step NS 与 shape scaling；
3. TRN-30：用对象生成路径区分 Muon、Shampoo、SOAP 与 K-FAC，禁止“矩阵形式相似即二阶等价”；
4. TRN-31：进入真正的 Stiefel constraint，区分 tangent、retraction 与固定谱轨道；
5. TRN-32：最后判断公开证据是否足以支持系统迁移。

## 验收与复现入口

- 数值实验：[[实验 - Muon 矩阵几何、数值迭代与迁移边界审计]]；
- 闭卷与复现门：[[60.4 分卷累计测验与复现门]]；
- 静态交付审计：[[60.4 静态完成与质量审计]]。

> [!warning] 当前验收边界
> 本卷 8 个核心节点、120 道练习、120 份独立详解、11 个正式图文单元、数值实验和分卷测验已通过静态验收。`verified` 只说明材料、链接与复现证据齐备；学习者仍须闭卷作答、从空目录复现并接受延迟复测，才能记录为个人掌握。
