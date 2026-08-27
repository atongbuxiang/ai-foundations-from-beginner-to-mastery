---
type: derivation
status: verified
area: [training, scaling-laws, compute-optimal, constrained-optimization]
node_id: TRN-51
aliases: [Chinchilla Scaling, Compute-optimal Allocation]
prerequisites: ["[[Kaplan 参数数据律、联合拟合与有限区间]]", "[[Lagrange 乘子与 KKT 条件]]", "[[一元导数与中值定理]]"]
related: ["[[IsoFLOP、训练算力口径与系统校正]]", "[[过训练、推理成本与多目标最优规模]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
sources: ["[[S-2022-Hoffmann-计算最优训练]]", "[[S-2024-Besiroglu-Chinchilla-Replication]]", "[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]]", "[[S-2020-Kaplan-语言模型尺度定律]]"]
exercises: ["[[习题 - Chinchilla、Compute-optimal 参数与数据分配]]"]
solutions: ["[[解答 - Chinchilla、Compute-optimal 参数与数据分配]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-chinchilla-compute-optimal-tangency-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Chinchilla、Compute-optimal 参数与数据分配

> [!abstract] 一句话结论
> Chinchilla 的核心不是“每参数固定若干 tokens”，而是固定训练 compute 下在模型项和数据项之间平衡边际收益。对 $L=E+AN^{-\alpha}+BD^{-\beta}$、$C=\kappa ND$，最优指数由 $\alpha,\beta$ 推导；任何固定比例都只是特定函数、常数、尺度与系统约束下的局部结果。

## 一、问题是约束优化

考虑教学基线

$$
L(N,D)=E+A N^{-\alpha}+B D^{-\beta},
\tag{1}
$$

以及 dense Transformer 的粗略训练 compute

$$
C=\kappa ND.
\tag{2}
$$

$\kappa$ 汇总每参数每 token 的 forward/backward 常数；它不是永远等于同一数字，下一节点会拆解。

目标是在固定 $C$ 下解

$$
\min_{N,D>0}L(N,D)
\quad\text{s.t.}\quad
\kappa ND=C.
\tag{3}
$$

地板 $E$ 不影响最优 $N,D$，但影响 loss 外推。

## 二、代入法完整推导

由约束

$$
D=\frac{C}{\kappa N}.
\tag{4}
$$

代回 reducible loss：

$$
R(N)
=A N^{-\alpha}
+B\left(\frac{\kappa N}{C}\right)^\beta.
\tag{5}
$$

求导：

$$
\frac{dR}{dN}
=-\alpha A N^{-\alpha-1}
+\beta B\left(\frac{\kappa}{C}\right)^\beta N^{\beta-1}.
\tag{6}
$$

令其为 0：

$$
\alpha A N^{-\alpha}
=\beta B D^{-\beta}.
\tag{7}
$$

这就是最重要的边际平衡式：最优点处，参数受限项与数据受限项按 exponent 加权后的收益相等。

继续整理：

$$
N^{\alpha+\beta}
=\frac{\alpha A}{\beta B}
\left(\frac{C}{\kappa}\right)^\beta,
\tag{8}
$$

所以

$$
N_*(C)
=\left(\frac{\alpha A}{\beta B}\right)^{1/(\alpha+\beta)}
\left(\frac{C}{\kappa}\right)^{\beta/(\alpha+\beta)}.
\tag{9}
$$

再由式 (4)：

$$
D_*(C)
=\left(\frac{\beta B}{\alpha A}\right)^{1/(\alpha+\beta)}
\left(\frac{C}{\kappa}\right)^{\alpha/(\alpha+\beta)}.
\tag{10}
$$

于是 compute exponents 是

$$
a=\frac{\beta}{\alpha+\beta},
\qquad
b=\frac{\alpha}{\alpha+\beta},
\qquad
a+b=1.
\tag{11}
$$

只有 $\alpha=\beta$ 时才有 $a=b=1/2$。

## 三、最优 Loss 的 Compute 指数

由式 (7)，两项在 optimum 上同阶。代入式 (9)：

$$
L_*(C)-E
=\Theta\!\left(
C^{-\alpha\beta/(\alpha+\beta)}
\right).
\tag{12}
$$

定义

$$
\gamma_C=\frac{\alpha\beta}{\alpha+\beta}.
\tag{13}
$$

它小于 $\alpha,\beta$；因为 compute 必须同时购买参数和数据，整体改善比只消除一个瓶颈更慢。

## 四、数值例子

若

$$
\alpha=0.34,\qquad\beta=0.28,
\tag{14}
$$

则

$$
a=\frac{0.28}{0.62}\approx0.452,
\qquad
b=\frac{0.34}{0.62}\approx0.548.
\tag{15}
$$

compute 增加 $100$ 倍时：

$$
\frac{N_*(100C)}{N_*(C)}
\approx100^{0.452}\approx8.0,
\tag{16}
$$

$$
\frac{D_*(100C)}{D_*(C)}
\approx100^{0.548}\approx12.5.
\tag{17}
$$

这说明“近似等比例”不等于精确 $10$ 倍/$10$ 倍；常数与指数不确定性都会影响规划。

## 五、为什么不是背诵 Tokens-per-Parameter

由式 (9)—(10)，

$$
\frac{D_*}{N_*}
\propto
C^{(\alpha-\beta)/(\alpha+\beta)}.
\tag{18}
$$

只有 $\alpha=\beta$ 时比例才与 compute 无关。即使 exponent 接近，常数

$$
\left(\frac{\beta B}{\alpha A}\right)^{2/(\alpha+\beta)}
\tag{19}
$$

也依赖数据、loss、模型族与口径。

因此“约 20 tokens/parameter”应理解为 Chinchilla 研究设置附近的经验摘要，不是自然常数。数据重复、质量、inference demand、context length、MoE active parameters 和 optimizer 都可能改变它。

## 六、IsoFLOP 怎样给出最优点

[[S-2022-Hoffmann-计算最优训练]] 使用多种估计路线。最直观的一类是：

1. 选定多个 compute budgets $C_k$；
2. 每个 $C_k$ 下训练多个 $N$，令 $D=C_k/(\kappa N)$；
3. 得到同 compute 的 U-shaped loss–$N$ profile；
4. 找每条 profile 的 minimum $N_*(C_k)$；
5. 拟合 $N_*(C)$、$D_*(C)$ 与 $L_*(C)$。

U 形来自两个极端：

- $N$ 太小：capacity-limited；
- $N$ 太大：在固定 compute 下 $D$ 太少，data-limited/undertrained。

IsoFLOP 比只看一条共同增长路径更能识别 optimum valley。

## 七、三种估计路线为何可能不一致

可以估计：

1. 每个 IsoFLOP profile 的离散 minimum；
2. minimum frontier 的 power law；
3. 所有 runs 的参数化 loss surface，再解析求 optimum。

三者使用的信息、平滑假设和噪声不同。[[S-2024-Besiroglu-Chinchilla-Replication]] 指出第三种程序的公开重建、拟合质量和置信区间需要谨慎复核。

课程要求报告：

- 每条 IsoFLOP curve 的原始点与 seeds；
- minimum 是否落在网格内部；
- 离散 grid uncertainty；
- surface fit 的 residual/held-out error；
- 三种路线的结果差；
- 参数统计和 compute 公式。

## 八、整数、内存与可行域

连续解 $(N_*,D_*)$ 只是起点。真实模型有：

- depth/head/width 的整数与整除约束；
- accelerator memory 与并行策略；
- 最小/最大 global batch；
- unique data 上限；
- context length 和 vocab compute；
- checkpoint、wall-time 与交付期限。

因此实际问题是

$$
\min_{(N,D,a)\in\mathcal F}
L(N,D,a),
\tag{20}
$$

其中 $a$ 是架构/系统配置，$\mathcal F$ 是离散可行域。做法通常是先用连续律定位区域，再在邻近可行模型上做 IsoFLOP 验证。

## 九、不确定性如何传播到最优规模

取式 (9) 的对数：

$$
\log N_*
=\frac{\log(\alpha A)-\log(\beta B)}{\alpha+\beta}
+\frac{\beta}{\alpha+\beta}
(\log C-\log\kappa).
\tag{21}
$$

$\alpha,\beta,A,B$ 的小误差会随 $\log C$ 放大。target compute 离 calibration window 越远，参数相关性与函数族不确定性越重要。

不能只给 $a=0.5\pm0.01$；还要给：

- $N_*,D_*$ 的 prediction interval；
- alternate fit families；
- held-out IsoFLOP minima；
- target loss 对邻近 allocation 的平坦度。

若 valley 很平，精确 optimum 不可识别，但宽 near-optimal region 仍有决策价值。

## 十、图：IsoFLOP 切线就是边际收益平衡

先看图回答：沿同一条 $ND=C/\kappa$ 曲线从“小模型多数据”走向“大模型少数据”，为什么 loss 先降后升？切点处式 (7) 表达了什么？

![[00-知识库管理/_assets/figures/training-optimization/fig-chinchilla-compute-optimal-tangency-v1.svg|900]]

> [!figure] 图 TRN-51-01　Compute constraint、loss contours 与 Chinchilla optimum
> 来源：课程原创教材图；左栏在 log $N$–log $D$ 平面画 IsoFLOP 线与 loss contours；中栏给 U-shaped IsoFLOP profile；右栏列出 $N_*,D_*,L_*$ 的 exponent 与适用门。概念依据：[[S-2022-Hoffmann-计算最优训练]]。

**怎样读图**：先固定 compute line，再找与最低 loss contour 相切的位置；不要跨不同 compute 线直接比较横坐标 minimum。

**图没有证明什么**：图中切线不提供真实 Chinchilla 系数，也不证明 additive loss surface 在新架构成立；它展示约束优化 identity。

## 十一、教授视角的验收

真正掌握本节意味着你能：

1. 从式 (1)—(2) 独立推导式 (9)—(13)；
2. 解释为什么 $a+b=1$ 依赖 $C\propto ND$；
3. 看到固定 tokens/parameter 时先问 exponent、constant 与 objective；
4. 把连续 optimum 转成带内存、数据和离散架构约束的候选区间；
5. 对原论文的三种估计方法分别报告证据和不确定性。
