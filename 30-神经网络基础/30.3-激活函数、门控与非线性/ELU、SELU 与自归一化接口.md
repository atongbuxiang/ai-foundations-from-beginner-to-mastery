---
type: derivation
status: draft
area: [neural-networks/activations, elu, selu, self-normalization]
aliases: [Exponential Linear Unit, Scaled ELU, Self-Normalizing Networks]
node_id: NN-20
prerequisites: ["[[ReLU、Leaky ReLU 与次梯度约定]]", "[[期望、方差与矩]]", "[[数列、极限与完备性的直觉|压缩映射与 Banach 不动点定理]]"]
related: ["[[方差传播与宽层均值场近似]]", "[[BatchNorm 前向统计与训练—推理差异]]", "[[Dropout 的随机掩码、期望与 Inverted Scaling]]"]
sources: ["[[S-2016-Clevert-ELU]]", "[[S-2017-Klambauer-SNN]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
exercises: ["[[习题 - ELU、SELU 与自归一化接口]]"]
solutions: ["[[解答 - ELU、SELU 与自归一化接口]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-elu-selu-self-normalizing-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---
# ELU、SELU 与自归一化接口

> [!abstract] 本章主问题
> ELU 用负侧指数饱和换取负输出与连续过渡；SELU 再选择特定 $\alpha,\lambda$，使理想化前馈均值—方差映射在 $(0,1)$ 附近具有吸引固定点。自归一化是带独立性、初始化、架构和 dropout 合同的定理，不是“换一个激活就自动标准化任何深网”。

## 一、ELU 的定义

给 $\alpha>0$，

$$
\operatorname{ELU}_\alpha(x)=
\begin{cases}
x,&x>0,\\
\alpha(e^x-1),&x\le0.
\end{cases}
$$

值域是 $(-\alpha,\infty)$。正侧保持 identity；负侧趋于 $-\alpha$，允许负均值贡献并压缩极端负输入。

导数为

$$
\operatorname{ELU}_\alpha'(x)=
\begin{cases}
1,&x>0,\\
\alpha e^x,&x<0.
\end{cases}
$$

在 0 连续；只有 $\alpha=1$ 时左右一阶导都为 1，因此才是 $C^1$。即使 $\alpha=1$，左右二阶导分别为 1 和 0，所以不是 $C^2$。

## 二、ELU 与 ReLU/Leaky 的结构差异

| 性质 | ReLU | Leaky ReLU | ELU |
|---|---|---|---|
| 正侧 | $x$ | $x$ | $x$ |
| 负侧 | 0 | $ax$ | $\alpha(e^x-1)$ |
| 负极限 | 0 | $-\infty$ | $-\alpha$ |
| 负侧导数 | 0 | $a$ | $\alpha e^x$ |
| 正齐次 | 是 | 是 | 否 |
| 负输出 | 否 | 是 | 是 |

ELU 不会像 ReLU 那样在所有负值处 exact zero，但在极负区间导数仍趋 0；它缓解的机制不等于消除饱和。

## 三、数值实现

负侧应使用 `expm1(x)` 计算 $e^x-1$，避免 $x$ 接近 0 时 cancellation。对很负的 $x$，underflow 到 0 会使输出精确成为 $-\alpha$、导数为 0；需要按 dtype 审计发生阈值。

若 backward 缓存 output $y$，负侧导数可写为

$$
\phi'(x)=y+\alpha.
$$

这减少一次指数计算，但要求保存/重算语义一致。

## 四、SELU 的定义与常数

SELU 是 scaled ELU：

$$
\operatorname{SELU}(x)=\lambda
\begin{cases}
x,&x>0,\\
\alpha(e^x-1),&x\le0,
\end{cases}
$$

经典常数近似为

$$
\alpha\approx1.6732632423543772,
\qquad
\lambda\approx1.0507009873554805.
$$

因为 $\alpha\ne1$，SELU 在 0 处左右导数分别为 $\lambda\alpha$ 与 $\lambda$，classical derivative 不存在；框架仍需选 convention。

## 五、自归一化研究的是 moment map

设一层 preactivation 为

$$
Z_j=\sum_{i=1}^nW_{ji}X_i+b_j.
$$

在独立、宽层、适当权重均值/方差和近 Gaussian 近似下，用输入均值 $\mu$、方差 $\nu$ 描述下一层：

$$
(\mu',\nu')=F(\mu,\nu).
$$

SELU 常数被选择为使

$$
F(0,1)=(0,1),
$$

并在论文给定区域内让该固定点具有吸引性。对象是 population/mean-field moment map，不是每个 mini-batch 的 sample mean 恰好为 0、sample variance 恰好为 1。

## 六、标准正态下一阶矩推导

令 $Z\sim\mathcal N(0,1)$，$\varphi,\Phi$ 分别为标准正态密度与分布函数。利用

$$
E[Z\mathbf1_{Z>0}]=\frac1{\sqrt{2\pi}},
$$

以及配方公式

$$
E[e^{tZ}\mathbf1_{Z\le0}]=e^{t^2/2}\Phi(-t),
$$

得到

$$
E[\operatorname{SELU}(Z)]
=\lambda\left[
\frac1{\sqrt{2\pi}}
+\alpha\left(e^{1/2}\Phi(-1)-\frac12\right)
\right].
$$

令括号为 0 即确定 $\alpha$ 的固定点条件之一。

## 七、标准正态下二阶矩推导

因为 $E[Z^2\mathbf1_{Z>0}]=1/2$，

$$
E[\operatorname{SELU}(Z)^2]
=\lambda^2\left[
\frac12+
\alpha^2E[(e^Z-1)^2\mathbf1_{Z\le0}]
\right].
$$

展开平方：

$$
E[(e^Z-1)^2\mathbf1_{Z\le0}]
=e^2\Phi(-2)-2e^{1/2}\Phi(-1)+\frac12.
$$

在均值已为 0 时，令该二阶矩等于 1 可确定 $\lambda$。这展示常数来自 moment equations，而不是经验凑数。

## 八、局部 contraction 不等于全局万能稳定

若 $J_F(0,1)$ 的谱半径小于 1，则在适当邻域内 moment perturbation 会收缩。Banach fixed-point 还需要：

1. 明确完备的状态域；
2. $F$ 把该域映回自身；
3. 在该域有统一 contraction constant；
4. 初始 moments 落入适用域。

只检查固定点 $F(0,1)=(0,1)$ 不足以证明吸引；只看局部 Jacobian 也不自动得到全局 contraction。

## 九、架构与初始化合同

经典 self-normalizing 结论依赖一组联合选择：

- feedforward-style 层与足够 fan-in；
- 权重近零均值、variance 约 $1/n$；
- bias 通常为 0；
- 输入预处理接近零均值、单位方差；
- units/weights 的相关性可被 mean-field 近似控制；
- 配套 alpha dropout，而非普通 dropout。

卷积共享、residual addition、attention、normalization、强相关特征、有限宽和训练后权重依赖都会改变 moment map。

## 十、Alpha Dropout 的精确校准

令 SELU 负饱和值

$$
c=-\lambda\alpha.
$$

若 $X$ 的均值 0、方差 1，保留 mask $D\sim\operatorname{Bernoulli}(q)$，先构造

$$
\widetilde X=DX+(1-D)c.
$$

则

$$
E[\widetilde X]=(1-q)c,
$$

$$
\operatorname{Var}(\widetilde X)=q+q(1-q)c^2.
$$

再令 $Y=a\widetilde X+b$，取

$$
a=\bigl(q+q(1-q)c^2\bigr)^{-1/2},
\qquad
b=-a(1-q)c,
$$

即可在理想假设下恢复均值 0、方差 1。普通 inverted dropout 把 dropped units 设 0，不能保持同一 SELU fixed-point 结构。

## 十一、梯度侧仍需独立分析

forward moments 稳定不等于 Jacobian singular values 全接近 1。SELU derivative 是

$$
\phi'(x)=
\begin{cases}
\lambda,&x>0,\\
\lambda\alpha e^x,&x<0,
\end{cases}
$$

其分布与权重共同决定 backward second moment 和 dynamical isometry。自归一化主要是均值—方差机制，不能替代谱分析。

## 十二、ELU 与 SELU 的使用边界

- ELU 的 $\alpha$ 可独立选择，通常不声称 fixed-point self-normalization；
- SELU 必须连同 constants、LeCun-normal-like initialization 和 alpha dropout 一起使用；
- 已有 BatchNorm/LayerNorm、residual 或 Transformer block 时，原 SELU theorem 的 map 已改变；
- output layer 仍由任务支持集决定，不因 hidden SELU 而固定；
- 低精度下负饱和和 exponential kernel 需测吞吐与 underflow。

## 十三、实验验收

至少比较：

1. layerwise mean、variance、second moment；
2. derivative mean/second moment 与 gradient norm；
3. width/depth、fan-in 和 input preprocessing 扫描；
4. zero/biased initialization 扰动；
5. no dropout、ordinary dropout、alpha dropout；
6. plain FNN 与 residual/normalization 架构；
7. FP64/32/BF16/16 finite rate 与 wall-clock；
8. fixed-point 附近 perturbation 是否经验收缩。

## 十四、图：固定点不是魔法按钮

先看图回答：SELU 的 $(0,1)$ 固定点为什么必须和初始化、架构及 alpha dropout 一起陈述？

![[00-知识库管理/_assets/figures/neural-networks/fig-elu-selu-self-normalizing-v2.svg|900]]

> [!figure] 图 30.3-04　ELU/SELU：负饱和、moment fixed point 与适用合同
> 左栏比较 ReLU/leaky/ELU 的负侧机制；中栏把 $(\mu,\nu)$ moment map 画为指向 $(0,1)$ 的局部流；右栏列出 initialization、independence、plain feedforward 与 alpha-dropout 条件及越界架构。来源：依据 Clevert 等 2016 与 Klambauer 等 2017 独立绘制；由 [[00-知识库管理/_labs/code/plot_activation_foundations_v2.py]] 确定性生成。

**怎样读图**：先读局部函数，再读 moment map 的对象与邻域，最后逐项核对当前网络是否满足右栏合同。

**图没有证明什么**：图没有证明任意有限宽、卷积、残差或注意力网络逐 batch 自动达到零均值单位方差，也没有证明 Jacobian spectrum 已实现 dynamical isometry。

## 十五、常见错误

1. 把 SELU 叫作“自动 BatchNorm”；
2. 只验证 fixed point，不验证 contraction 与 invariant domain；
3. 使用普通 dropout 却声称保持自归一化；
4. 忘记实际 SELU 在 0 处不可微；
5. 把 forward moment 稳定当作完整梯度谱稳定；
6. 在 residual/normalization 架构中机械套用 plain FNN 结论；
7. 忽略 `expm1` 与低精度负饱和。

## 十六、回顾与练习

> [!summary]
> ELU 提供负输出与负侧指数饱和；SELU 的特殊常数让理想化 moment map 在 $(0,1)$ 附近自归一化。结论必须携带初始化、独立近似、架构和 alpha-dropout 条件，且不能替代 backward spectrum 分析。

- [[习题 - ELU、SELU 与自归一化接口]]
- [[解答 - ELU、SELU 与自归一化接口]]
