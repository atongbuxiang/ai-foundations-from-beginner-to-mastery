---
type: solution
status: draft
area: [architecture, state-space-models, hippo, s4]
topic: "[[HiPPO、S4 与结构化长记忆]]"
exercise: "[[习题 - HiPPO、S4 与结构化长记忆]]"
sources: ["[[S-2020-Gu-HiPPO]]", "[[S-2022-Gu-S4]]", "[[S-2024-Su-10162-S4高效计算]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - HiPPO、S4 与结构化长记忆

## A. 识别与复述

### ARCH-HIPPO-A01
选定 $L^2(\mu_t)$ 与 orthonormal $g_n^{(t)}$，令 $c_n(t)=\langle u,g_n^{(t)}\rangle$，用 $\hat u_t=\sum_{n<N}c_ng_n^{(t)}$ 重构。在线算法随新输入更新有限 $c(t)$，目标是该子空间/测度下的 projection error。

### ARCH-HIPPO-A02
最优相对指定 $\mu_t$、norm、basis span 和阶数 $N$；不能推出任意 downstream loss 最优，也不能推出离散、学习后修改仍精确保持连续 projection，亦不能推出无限历史逐点无损。

### ARCH-HIPPO-A03
HiPPO 投影导出 $A,B$ → 选择离散化得 $\bar A,\bar B$ → 利用 NPLR/DPLR 基变换 → 在频点计算 resolvent/Cauchy-like kernel → inverse FFT 得时域 kernel 并做 convolution；流式可用 recurrence。

## B. 手算与建模

### ARCH-HIPPO-B01
概率测度为 $dx/2$。$c_0=E[2+x]=2$；$c_1=E[(2+x)\sqrt3x]=\sqrt3E[x^2]=\sqrt3/3=1/\sqrt3$。重构 $2+(1/\sqrt3)(\sqrt3x)=2+x$，因原函数就在 span 中而精确。

### ARCH-HIPPO-B02
$K_n=C\bar A^n\bar B=2(0.8)^n$，前四项 $(2,1.6,1.28,1.024)$。$K(z)=2/(1-0.8z)$，解析收敛域 $|z|<1.25$。

### ARCH-HIPPO-B03
$M^{-1}=\operatorname{diag}(1/2,1/3)$，分母 $1+v^TM^{-1}u=1+5/6=11/6$。逆为 $M^{-1}-M^{-1}uv^TM^{-1}/(11/6)=\begin{bmatrix}4/11&-1/11\\-1/11&3/11\end{bmatrix}$；直接求 $\begin{bmatrix}3&1\\1&4\end{bmatrix}^{-1}$ 可核验。

## C. 推导与证明

### ARCH-HIPPO-C01
令 $P_Vu$ 为正交 projection，对任意 $v\in V$，$u-P_Vu\perp P_Vu-v$。故 $\|u-v\|^2=\|u-P_Vu\|^2+\|P_Vu-v\|^2\ge\|u-P_Vu\|^2$，唯一最佳由第二项为零取得。

### ARCH-HIPPO-C02
Leibniz rule 对变上限积分产生上端 $u(t)g_n^{(t)}(t)$；integrand 中 $g_n^{(t)}$ 和 density/coordinate warp 的 $t$ 依赖又产生积分项。特定 basis closure 让这些积分项可写成 coefficients 的线性组合。

### ARCH-HIPPO-C03
令 $M=zI-\Lambda$，则 $zI-A=M+PQ^*$。Woodbury 给 inverse 为 $M^{-1}-M^{-1}P(I+Q^*M^{-1}P)^{-1}Q^*M^{-1}$。$M^{-1}$ 对角逐元素，核心额外 inverse 只有 low-rank 尺寸；与 $B,C$ 配对形成 Cauchy-like sums。

## D. 边界、反例与纠错

### ARCH-HIPPO-D01
在 $[0,1]$ 对 $u(x)=x$ 用常数子空间。均匀概率测度 projection 常数为 $E[x]=1/2$；density $2x$ 的概率测度下为 $\int_0^1x(2x)dx=2/3$。同一 basis span 因 measure 改变而系数改变。

### ARCH-HIPPO-D02
Projection theorem只最小化历史函数在指定 weighted $L^2$ 与有限 subspace 中的 reconstruction error。S4 还经历离散、参数学习、非线性 block 和任务 readout；任意 task loss、data 与 optimizer 不在该定理中。

### ARCH-HIPPO-D03
完整 block 在 linear SSM 前后含 activation、gate、normalization、projection、residual，多层复合。只要任一非线性激活存在，整体 input-output map 通常不线性。

## E. AI 迁移

### ARCH-HIPPO-E01
Continuum：basis truncation 与 measure mismatch；discretization：hold assumption、step、method error；kernel：DPLR/resolvent/FFT 与有限精度误差；task：readout approximation、optimization、generalization。分别给 reference 与 metric，不能只报最终 accuracy。

### ARCH-HIPPO-E02
数学：recurrence 与 generated convolution 小矩阵 float64 对齐；数值：扫长度、poles、dtype、gradient；硬件：官方 optimized 与 fallback、warm-up、batch/length throughput和memory；任务：固定参数/compute 对 baseline、多个 seed、长程与反例任务。

### ARCH-HIPPO-E03
第一篇主要 I/T bridge 到 projection/ODE，第二篇 T bridge 到 discretization/stability，第三篇 T/H bridge 到 DPLR/Cauchy，第四篇 I/O extension 到 rational transfer function。正式 theorem/algorithm 归属引用原论文；博客用于中文推导和研究拓展，不单独承担普遍 empirical claim。

