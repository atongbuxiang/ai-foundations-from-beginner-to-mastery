---
type: source
status: verified
area: [sources, numerical-linear-algebra, matrix-functions, muon]
source_type: blog
title: "msign的Newton–Schulz迭代（上）"
author: 苏剑林
year: 2025
url: "https://spaces.ac.cn/archives/10922"
accessed: 2026-08-26
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要与链接"
site_category: [信息时代]
scope_role: numerical-method-bridge
temporal_role: active-research
related: ["[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Newton–Schulz Matrix Sign 的收敛与有限精度]]"]
created: 2026-08-26
updated: 2026-08-26
---

# msign 的 Newton–Schulz 迭代（上）

> [!abstract] 来源定位
> 文章从奇异值函数视角讨论矩阵 msign 与 Newton–Schulz 型迭代，适合作为“矩阵多项式如何逐个变换奇异值”的中文入口。本库用 Higham 的矩阵函数与极分解结果补足收敛域和稳定性条件。

## 核心断言账本

| ID | 断言 | 类型 | 采用边界 |
|---|---|---|---|
| C1 | 对 $X=U\Sigma V^T$ 施加奇多项式，奇异值按相应标量多项式演化 | 精确代数 | 需满足维度匹配并避免把 singular value map 当 eigenvalue map |
| C2 | 经典 Newton–Schulz 可局部把正奇异值推向 1 | 数值算法 | 依赖初始缩放/收敛区间；零奇异值保持为零 |
| C3 | Muon 常用的三项五次多项式可用有限步近似 polar direction | 工程方法 | 系数目标是有限步效果，不是逐步单调精确收敛证明 |
| C4 | 正交残差、polar residual 与方向误差是不同诊断量 | 审计原则 | 只报告 iteration count 不足以判断质量 |

## 限制

有限精度下必须同时观察溢出、下溢、rank、condition number 和低精度 GEMM。理论上的固定点性质不自动保证 BF16 实现稳定；参见 [[S-2012-Nakatsukasa-Higham-Polar-Stability]]。

