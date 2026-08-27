---
type: solution
status: verified
area: [training, scaling-laws, compute-optimal]
topic: "[[Chinchilla、Compute-optimal 参数与数据分配]]"
exercise: "[[习题 - Chinchilla、Compute-optimal 参数与数据分配]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Chinchilla、Compute-optimal 参数与数据分配

> [!warning] 使用边界
> 以下是连续代理模型的条件最优。实际选择还要经过拟合不确定性、离散配置、数据可得性和系统约束。

## A. 识别与复述

### TRN51-A01
固定训练算力最优是在 $C$ 的等成本曲线上分配 $N,D$；固定 token 最优是在给定 $D$ 下选容量与训练协议；部署最优还加入未来请求量、延迟、内存和推理成本。约束与目标一变，最优点就可能改变，所以不能把训练期 allocation 直接称为全生命周期最优。

### TRN51-A02
最优点满足
$$
\alpha AN^{-\alpha}=\beta BD^{-\beta}.
$$
左、右是沿算力约束把一小部分资源从数据移给参数时两类 excess loss 的加权边际贡献。最优处继续增大某一侧造成的收益，恰好抵消另一侧缩小造成的损失。

### TRN51-A03
IsoFLOP 曲线固定一个计算预算，系统扫描多个 $N$–$D$ 分配并观察 loss 谷底。两个点只能做成对比较，无法判断谷底位置、曲率、近优宽度或是否漏过最优；多预算的多点曲线还能估计最优路径如何随 $C$ 移动。

## B. 手算与构造

### TRN51-B01
约束为 $ND=10^4$，对称性或一阶条件给 $N=D$，故
$$
N^*=D^*=100,\qquad L^*-E=100^{-1/2}+100^{-1/2}=0.2.
$$

### TRN51-B02
$$
\frac{\beta}{\alpha+\beta}=\frac{0.28}{0.62}\approx0.4516,\qquad
\frac{\alpha}{\alpha+\beta}\approx0.5484.
$$
所以 $N^*\propto C^{0.4516}$、$D^*\propto C^{0.5484}$，且
$$
\frac{D^*}{N^*}\propto C^{(0.34-0.28)/0.62}\approx C^{0.0968}.
$$
该模型甚至预测 token/parameter 比随预算缓慢变化，而非常数。

### TRN51-B03
三者 excess loss 分别为
$$
0.1+0.1=0.2,\quad 0.2+0.05=0.25,quad0.05+0.2=0.25.
$$
偏离最优四倍的参数/数据比例只使 excess loss 增加 25%，说明谷底可较平；离散网格报告唯一 argmin 会夸大定位精度。

## C. 推导与证明

### TRN51-C01
代入 $D=C/(\kappa N)$：
$$
R(N)=AN^{-\alpha}+B(\kappa N/C)^\beta.
$$
令导数为零：
$$
-\alpha AN^{-\alpha-1}+\beta B(\kappa/C)^\beta N^{\beta-1}=0,
$$
从而
$$
N^{\alpha+\beta}=\frac{\alpha A}{\beta B}\left(\frac C\kappa\right)^\beta,\quad
N^*=\left(\frac{\alpha A}{\beta B}\right)^{1/(\alpha+\beta)}
\left(\frac C\kappa\right)^{\beta/(\alpha+\beta)}.
$$
再由 $D^*=C/(\kappa N^*)$ 得 $D^*\propto C^{\alpha/(\alpha+\beta)}$。

### TRN51-C02
将 $N^*\propto C^{\beta/(\alpha+\beta)}$ 代入参数项，得
$$
AN^{*-\alpha}\propto C^{-\alpha\beta/(\alpha+\beta)}.
$$
数据项同理，因为 $D^*\propto C^{\alpha/(\alpha+\beta)}$。两项指数相同，和仍为同阶，故结论成立。

### TRN51-C03
一阶条件给
$$
\alpha AN^{-\alpha}=\beta BD^{-\beta}
\quad\Rightarrow\quad
\frac{AN^{-\alpha}}{BD^{-\beta}}=\frac\beta\alpha.
$$
平衡的是乘上弹性后的边际量，不是两项数值本身；仅 $\alpha=\beta$ 时两项相等。

## D. 边界、反例与纠错

### TRN51-D01
“20”是特定 family、数据、参数口径、训练 FLOPs 近似、尺度区间和拟合选择下的经验规则，不是定理。数据质量/重复、tokenizer、优化成熟度、架构与稀疏性、参数计数、推理目标、可用数据上限以及后续复现实验都可改变系数或指数，因而改变最优比率。

### TRN51-D02
连续解可能要求不存在的模型宽度/层数或 token 数；数据可能不足或重复过多；硬件 tensor shape、并行拓扑和内存约束只允许特定配置；最优附近某些模型还可能训练不稳定。应在可行离散集合中比较近优点，而不是四舍五入后宣称实现了理论最优。

### TRN51-D03
平谷意味着采样噪声和拟合微扰就能让 argmin 在多个配置间跳动。应报告 $\epsilon$-optimal set（例如 loss 在最佳点误差带/1% 内）、曲率、bootstrap 中的最优分布，以及工程约束下选择理由。

## E. AI 迁移

### TRN51-E01
取三预算 $C_0,4C_0,16C_0$；每个预算围绕先验最优 ratio 以 $N$ 的 $\{1/4,1/2,1,2,4\}$ 倍布点，并令 $D=C/(\kappa N)$。每格共享训练实现与预注册 scale-aware 超参规则，再设统一搜索预算；保存失败和实际 FLOPs。否则某点的坏 loss 可能只是学习率或 batch 不合适。

### TRN51-E02
对每个 block-bootstrap 参数样本 $(A,B,\alpha,\beta,\kappa)$ 重新计算连续 $N^*,D^*$，再映射到可行网格并计算 $\epsilon$-optimal 集。汇总分位区间、配置入选频率、loss regret 与相关性；不能只把各参数边际区间独立代入，因为它们通常高度相关。

### TRN51-E03
示例：
> 代理曲面在预算 $C$ 下给出连续最优 $(N^*,D^*)$ 及 bootstrap 区间；预注册离散网格的观测最佳为配置 B，但 A/B/C 均落入 1% 近优集。考虑数据上限与并行效率后选择 C。该选择是约束下工程决策，不把单次网格最小值解释为普遍 tokens/parameter 定律。

## 无提示重做

- [ ] 不查笔记重推 $N^*(C),D^*(C)$。
- [ ] 为一个平坦 IsoFLOP 谷底画近优集合。
