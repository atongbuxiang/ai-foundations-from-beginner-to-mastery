---
type: experiment
status: draft
area: [math/numerical-analysis, math/numerical-linear-algebra, ai-systems]
question: "binary16 分解、binary32 更新与更高精度残差如何决定 classical IR 的地板，GMRES-IR 能将失效边界推到哪里？"
hypothesis: "当低精度因子仍可用时，高精度残差降低地板，GMRES 预条件校正扩展收敛区间；因子已奇异时两者都失败。"
code: "[[plot_mixed_precision_refinement.py]]"
figure: "[[00-知识库管理/_assets/plots/iterative-refinement/plot-mixed-precision-refinement-v2.svg]]"
data: "n=8 DCT 正交基、指定条件数的 SPD 矩阵和确定性真解"
seed: null
sources: ["[[S-2018-Carson-Higham-三精度迭代改进]]", "[[S-2022-Higham-Mary-混合精度数值线性代数]]"]
related: ["[[迭代改进、混合精度与残差校正]]", "[[实验 - 选主元、后向误差与迭代改进]]"]
created: 2026-08-15
updated: 2026-08-23
---

# 实验 - 三精度迭代改进与 GMRES-IR 边界

> [!question] 本实验的判别问题
> factor、residual、update 三种精度分别控制哪一段误差链，GMRES-IR 又能把低精度因子的可用区间推进到哪里？

## 设计与算术

- 矩阵：$A=Q\operatorname{diag}(\lambda)Q^T$，$Q$ 为 DCT 正交基，$n=8$；
- factor/correction solve：每个基本操作显式舍入到 binary16 的部分选主元 LU；
- update：binary32；residual：binary16/32/64 对照；
- GMRES-IR：每个外层校正用 5 步右预条件 GMRES。

- 代码：[plot_mixed_precision_refinement.py](</Users/tong/Nodes/basic/00-知识库管理/_labs/code/plot_mixed_precision_refinement.py>)；
- 图形：[[00-知识库管理/_assets/plots/iterative-refinement/plot-mixed-precision-refinement-v2.svg]]；
- 图形 SHA-256：`e5c0da4135e7d26928bb738351073c219749a335fa00ad5d6904191902c47cf9`；
- Python：系统 `python3`，仅标准库。

## 结果

先用图回答：**在同一个低精度 LU 上，条件数、残差精度和内层 Krylov 校正怎样分别改变收敛速度、误差地板与最终失败边界？**

![[00-知识库管理/_assets/plots/iterative-refinement/plot-mixed-precision-refinement-v2.svg|880]]

> [!figure] 实验图｜三精度迭代改进的三道边界
> A 固定 binary16 LU，比较 $\kappa_2=10^2,10^3,10^4$ 的 classical IR；B 固定 $\kappa_2=10^2$，只改变 residual 精度；C 比较一次低精度校正与 5 步右预条件 GMRES-IR。生成脚本：[[plot_mixed_precision_refinement.py]]；确定性 DCT-SPD 家族，并对 moderate-condition 修复、残差精度分离和 $10^5$ 失败点设断言。

**怎样读图。** A 先看误差是否随外迭代收缩，再比较不同 $\kappa$ 的地板；B 的三线分离只归因于 residual 精度；C 观察 GMRES-IR 绿线在 $3\times10^4$ 前保持参考地板、到 $10^5$ 与 classical IR 一同失败。

**适用边界（图没有证明什么）。** 这是 $n=8$ 的 DCT-SPD 机制实验，未覆盖非正规性、pivot growth、GPU 实际算术与大规模通信成本；图不把观察到的非单调 sweep 当作一般收敛定理。

### Classical IR，10 步后

| $\kappa_2(A)$ | 初始前向误差 | 最终前向误差 |
|---:|---:|---:|
| $10^2$ | $6.495\times10^{-3}$ | $7.487\times10^{-7}$ |
| $10^3$ | $1.117\times10^{-1}$ | $3.371\times10^{-5}$ |
| $10^4$ | $1.423$ | $4.763\times10^{-2}$ |

在 $\kappa=10^2$ 固定同一 binary16 LU 时，binary16/32/64 残差的最终误差分别为 $8.470\times10^{-3}$、$1.113\times10^{-6}$、$7.487\times10^{-7}$。这支持“残差精度决定可信信号地板”。

### 条件数 sweep

GMRES-IR 在 $\kappa=10$ 至 $3\times10^4$ 的该构造上到达 $2.112\times10^{-8}$ 的 binary32 参考地板；classical IR 随条件数总体恶化，但 $10^4$ 到 $3\times10^4$ 间不单调，说明条件数不是唯一预测量。在 $10^5$ 时，binary16 因子被检测为奇异，两种方法均失败。

## 结论边界

- $n=8$ 的 DCT-SPD 家族是机制实验，不是 Carson–Higham 理论阈值的全面复现；
- GMRES 固定 5 步且小维数，因而本实验的平台过于理想；
- sweep 非单调来自低精度因子的具体舍入/选主元路径，这恰好是“$\kappa$ 不足以单独预言实现”的证据；
- 生产基准还需加入尺度失衡、pivot growth、非正规性、大维数成本和 GPU 实际算术。

## 复现

```bash
python3 "00-知识库管理/_labs/code/plot_mixed_precision_refinement.py"
```
