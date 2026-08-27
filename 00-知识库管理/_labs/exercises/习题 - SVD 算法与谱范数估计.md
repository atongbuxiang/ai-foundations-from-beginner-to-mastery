---
type: exercise
status: draft
area: [math/numerical-linear-algebra, math/low-rank-methods]
topic: "[[SVD 算法与谱范数估计]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[奇异值分解]]", "[[Householder 与 Givens 变换]]", "[[Lanczos 方法]]"]
related: ["[[解答 - SVD 算法与谱范数估计]]", "[[实验 - SVD 双对角化、谱范数与随机子空间]]", "[[低秩近似]]"]
solution: "[[解答 - SVD 算法与谱范数估计]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - SVD 算法与谱范数估计

> [!abstract] 训练目标
> 把 SVD 定理落实为可计算算法：双对角化、结构化求解、部分 SVD、谱范数幂迭代、随机值域、双侧残差和 AI 中的可微/时变边界。

## A. 识别与复述

### NLA-SVA-A01

区分完整 SVD、经济 SVD、截断 SVD、谱范数估计与 randomized range finder 的输入输出和主要成本。

### NLA-SVA-A02

描述稠密 SVD 的“两阶段算法”，并解释左右正交变换为何保持奇异值。

### NLA-SVA-A03

解释 `GEBRD`、`BDSQR`、`GESVD` 与 `GESDD` 各处于算法栈哪一层；为什么不能只凭函数名断言某驱动在所有机器上最快？

## B. 手算与构造

### NLA-SVA-B01

对

$$
A=\begin{bmatrix}3&0\\4&1\\0&2\end{bmatrix}
$$

复现正文双对角化，验证 $P_1A$，并写出最终 $B$。

### NLA-SVA-B02

对 `B01` 的 $A$ 与 $B$，计算 Frobenius 范数平方并验证相等；再写出 $B^TB$。

### NLA-SVA-B03

若候选 $\widehat\sigma=5$、$\|Av-5u\|=3\times10^{-4}$、$\|A^Tu-5v\|=4\times10^{-4}$、$\|A\|_2\approx5$，计算合并残差与尺度化指标。

### NLA-SVA-B04

谱比 $r=\sigma_2/\sigma_1$ 分别为 $0.2,0.8,0.98$。估计把方向误差常数 $1$ 降到 $10^{-6}$ 所需完整交替幂步，使用 $r^{2t}\le10^{-6}$。

### NLA-SVA-B05

目标秩 $k=20$、过采样 $p=8$、幂步 $q=2$。写出随机 SVD 所需的 $A/A^T$ 块乘顺序、块宽和数据 pass 数（不计最后小矩阵 SVD）。

### NLA-SVA-B06

给定奇异值 $10,3,0.9,0.1$。分别写出 $q=0,1,2$ 的随机幂方案中相对第一方向的权重比例，并解释有限精度风险。

## C. 推导与证明

### NLA-SVA-C01

证明左右正交变换 $B=P^TAR$ 保持奇异值，并保持 Frobenius 范数。

### NLA-SVA-C02

从 $Av_i=\sigma_i u_i$、$A^Tu_i=\sigma_i v_i$ 推导增广矩阵的成对特征值 $\pm\sigma_i$。

### NLA-SVA-C03

推导交替谱范数幂迭代等价于对 $A^TA$ 做幂法，并得到方向收敛因子 $(\sigma_2/\sigma_1)^{2t}$。

### NLA-SVA-C04

证明 randomized power scheme

$$
Y=(AA^T)^qA\Omega
$$

把第 $i$ 个左奇异方向的权重乘到 $\sigma_i^{2q+1}$。

### NLA-SVA-C05

证明任意正交 $Q$ 下，$QB$ 对 $A$ 的最佳 Frobenius 近似（列空间限制在 $\mathcal R(Q)$）取 $B=Q^TA$，误差为 $\|(I-QQ^T)A\|_F$。

### NLA-SVA-C06

说明为何显式正规方程使二范数条件数平方；若 $\kappa_2(A)=10^8$，在双精度单位舍入约 $10^{-16}$ 下，解释可分辨小方向的风险。

## D. 边界、反例与纠错

### NLA-SVA-D01

纠正“先形成 $A^TA$ 再调用对称特征值算法，总比 SVD 简单”的说法。至少讨论条件数、填充、舍入和左向量恢复。

### NLA-SVA-D02

构造 $\sigma_1=\sigma_2$ 的例子，说明最大奇异向量为何不唯一、单向量幂迭代为何不能稳定选定一列，但谱范数仍唯一。

### NLA-SVA-D03

纠正“随机 SVD 的 $q$ 越大越好”。讨论数据 pass、正交化、舍入吞噬和噪声放大。

### NLA-SVA-D04

解释为什么只报告 $\|A-U_k\Sigma_kV_k^T\|_F$ 不能完整验收一个部分 SVD。还应报告哪些量？

### NLA-SVA-D05

纠正“所有小于 $10^{-6}$ 的奇异值都视为零”。给出尺度、维数、噪声和任务相关的数值秩规则。

## E. AI 迁移

### NLA-SVA-E01

为神经网络层 $W$ 的谱归一化设计 warm-start 一步幂迭代。说明状态、更新、估计偏差、偶发校准和失败报警。

### NLA-SVA-E02

只有 JVP/VJP 时，设计估计 Jacobian 最大三个奇异值的块 Golub–Kahan/子空间方法，并写出双侧残差。

### NLA-SVA-E03

用随机 SVD 压缩权重矩阵。设计离线验收，区分矩阵范数误差、层输出误差和端到端任务误差。

### NLA-SVA-E04

比较用截断 SVD 初始化 LoRA 与直接训练随机低秩因子。SVD 的最优性承诺在哪个范数、对哪个静态对象成立？哪些训练结论不能推出？

### NLA-SVA-E05

一个损失依赖前 $k$ 个奇异向量。解释谱隙、符号/相位、重根、截断排序和固定步算法求导的风险，并提出更稳定的子空间损失。

## 分级提示

- `B02`：$\|A\|_F^2=30$；
- `B03`：合并残差为 $5\times10^{-4}$；
- `B05`：初始 $A\Omega$ 一次，此后每个 $q$ 增加一次 $A^T$ 与一次 $A$；
- `C05`：把 $A=QQ^TA+(I-QQ^T)A$ 正交分解；
- `D02`：可取 $A=I_2$；
- `E05`：用 $U_kU_k^T$ 或重构算子代替逐列比较。

## 解答入口

完成独立尝试后再打开：[[解答 - SVD 算法与谱范数估计]]。
