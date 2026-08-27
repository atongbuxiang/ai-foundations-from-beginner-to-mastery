---
type: moc
status: active
area: [training, optimization, curvature]
prerequisites: ["[[Hessian、二阶微分与曲率]]", "[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[共轭梯度法]]", "[[镜像下降、Bregman 几何与自然梯度]]"]
related: ["[[训练与优化 MOC]]", "[[训练与优化完整课程地图与掌握标准]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 曲率、自然梯度与矩阵预条件 MOC

> [!abstract] 分卷目标
> 把“二阶优化”拆成 derivative object、expectation measure、隐式线性代数、结构近似、数值证书和系统证据六层。完成后应能区分 Hessian/GGN/Fisher/EF，从 KL 推出自然梯度，用 HVP+CG 建立可验收二阶步，并准确限定 K-FAC、Shampoo、SOAP 的近似与性能结论。

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| TRN-17 | [[Hessian、GGN、Fisher 与经验 Fisher 对象总账]] | 区分四种矩阵 | 静态验收通过；个人掌握另计 |
| TRN-18 | [[Newton、Damping、Trust Region 与 Levenberg–Marquardt]] | 控制不定/病态二阶步 | 静态验收通过；个人掌握另计 |
| TRN-19 | [[Hessian-vector Product、共轭梯度与隐式二阶步]] | HVP+CG residual audit | 静态验收通过；个人掌握另计 |
| TRN-20 | [[自然梯度、KL 局部几何与坐标不变性]] | 从 KL constraint 推导方向 | 静态验收通过；个人掌握另计 |
| TRN-21 | [[GGN、经验 Fisher 与曲率近似陷阱]] | 构造不等价反例 | 静态验收通过；个人掌握另计 |
| TRN-22 | [[K-FAC、Kronecker 分块与阻尼合同]] | 推导 layer block approximation | 静态验收通过；个人掌握另计 |
| TRN-23 | [[Shampoo、逆矩阵根与 Kronecker 预条件]] | 计算多轴 inverse root | 静态验收通过；个人掌握另计 |
| TRN-24 | [[SOAP、二阶混合优化器与成本证据地图]] | 比较 hybrid method 总成本 | 静态验收通过；个人掌握另计 |

## 学习主线

$$
\text{derivative object / measure}
\to \text{local quadratic or KL model}
\to \text{matrix-free solve}
\to \text{Kronecker/tensor approximation}
\to \text{root/basis state}
\to \text{system and evidence}.
$$

本卷的每个方法都必须报告：矩阵对象与测度、PSD/rank、damping、求逆/根 residual、更新频率、状态内存、通信、失败出口，以及 performance evidence 是否 compute-matched。

## 练习、实验与验收

- 每个节点均有独立 15 题 A—E 分层习题与逐题解答，共 120 题；
- 数值实验：[[实验 - 曲率对象、隐式二阶步与矩阵预条件数值审计]]；
- 卷终验收：[[60.3 分卷累计测验与复现门]]；
- 完成审计：[[60.3 静态完成与质量审计]]。

## 来源与证据

正式骨架来自 Nocedal–Wright、Steihaug、Pearlmutter、Amari/Martens、Kunstner、K-FAC、Shampoo、Guo–Higham 与 SOAP 原始来源；当前 HVP 实现语义由 PyTorch 官方文档承担。[[S-2024-Su-10588-Hessian近似与自适应学习率]]作为中文问题入口，不能替代 Fisher/GGN/Hessian 的正式等价条件。

## 下一卷出口

下一卷 [[矩阵优化、谱最速下降与 Muon MOC]]从 norm/dual norm 与 polar/msign 推出矩阵最速方向。矩阵函数外形相似不构成 K-FAC、Shampoo、SOAP 与 Muon 的曲率等价证明。
