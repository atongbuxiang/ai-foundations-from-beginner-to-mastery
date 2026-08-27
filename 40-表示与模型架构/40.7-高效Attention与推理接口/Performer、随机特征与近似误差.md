---
type: concept
status: draft
area: [architecture, efficient-attention, performer, random-features]
aliases: [Performer, FAVOR+, Positive Random Features]
node_id: ARCH-53
prerequisites: ["[[核特征、线性 Attention 与结合律重排]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[正定核、RKHS 与表示定理]]"]
related: ["[[高效 Attention 与推理接口 MOC]]", "[[随机化低秩近似与随机 SVD]]", "[[Attention 的几何、核与概率视角]]"]
sources: ["[[S-2021-Choromanski-Performer]]", "[[S-2020-Su-7921-Performer随机投影]]", "[[S-2021-Su-8338-Performer到线性Attention]]", "[[S-2021-Su-8601-无限维线性Attention与核特征]]"]
exercises: ["[[习题 - Performer、随机特征与近似误差]]"]
solutions: ["[[解答 - Performer、随机特征与近似误差]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-performer-random-feature-error-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Performer、随机特征与近似误差

> [!abstract] 核心问题
> Performer 不是简单把 softmax 换成 ELU kernel，而是用正随机特征近似 exponential dot-product kernel，再利用 linear-attention 结合律。需要分清：kernel estimator 是否无偏、归一化 attention 是否无偏、有限 feature 误差怎样被 denominator 放大，以及实际 crossover 在哪里。

## 一、Softmax Attention 的未归一化核

忽略 $1/\sqrt{d_h}$，先看

$$
K(q,k)=e^{q^\top k}.
$$

若要应用 ARCH-52 的结合律，需要把它近似为

$$
K(q,k)\approx \phi(q)^\top\phi(k),
$$

其中 $\phi(x)\in\mathbb R^m$，$m$ 是随机 feature 数。

## 二、正随机特征恒等式的逐步推导

令 $\omega\sim\mathcal N(0,I)$，定义

$$
\psi_\omega(x)=
\exp\left(\omega^\top x-\frac{\|x\|^2}{2}\right).
$$

由高斯矩母函数

$$
\mathbb E[e^{\omega^\top a}]=e^{\|a\|^2/2},
$$

取 $a=q+k$：

$$
\begin{aligned}
\mathbb E[\psi_\omega(q)\psi_\omega(k)]
&=\exp\left(-\frac{\|q\|^2+\|k\|^2}{2}\right)
\mathbb E[e^{\omega^\top(q+k)}]\\
&=\exp\left(-\frac{\|q\|^2+\|k\|^2}{2}
+\frac{\|q+k\|^2}{2}\right)\\
&=e^{q^\top k}.
\end{aligned}
$$

取 $m$ 个样本 $\omega_r$，定义

$$
\phi(x)=\frac1{\sqrt m}
[\psi_{\omega_1}(x),\ldots,\psi_{\omega_m}(x)]^\top,
$$

则 $\widehat K(q,k)=\phi(q)^\top\phi(k)$ 是 kernel 的 Monte Carlo estimator。分量严格为正，适合归一化 attention。

## 三、无偏 Kernel 不等于无偏 Attention

对 query $i$，真实输出

$$
o_i=\frac{N_i}{D_i},\quad
N_i=\sum_jK_{ij}v_j,\quad D_i=\sum_jK_{ij}.
$$

随机近似为

$$
\hat o_i=\frac{\hat N_i}{\hat D_i}.
$$

即使 $\mathbb E[\hat K_{ij}]=K_{ij}$，通常仍有

$$
\mathbb E\left[\frac{\hat N_i}{\hat D_i}\right]
\ne \frac{\mathbb E[\hat N_i]}{\mathbb E[\hat D_i]}.
$$

因为期望不能穿过随机比值。这是理解 Performer 证据边界的关键。

对一阶扰动 $\delta N,\delta D$，

$$
\frac{N+\delta N}{D+\delta D}-\frac ND
\approx \frac{\delta N}{D}-\frac{N\delta D}{D^2}.
$$

当 $D$ 小或相对误差大，ratio error 会显著放大。

## 四、随机方差为什么可能很大

$\psi_\omega(x)$ 是 log-normal 型正变量；当 $\|x\|$ 大，少数随机方向可产生巨大值。虽然均值正确，有限样本方差和数值范围可能很差。

Performer 的 FAVOR+ 使用结构化/正交随机特征等技术降低方差与计算，并给出相应理论。正确表述是“在论文的 feature construction、norm 控制和概率条件下有误差/收敛保证”，而不是“任意高斯随机矩阵都稳定”。

固定 random seed 只保证复现同一个 estimator，不会让近似误差消失。每步重采样则会把模型函数变成带额外随机性的对象，通常不是推理合同。

## 五、Feature 数 $m$ 的三方权衡

增加 $m$ 通常：

- 降低随机估计误差；
- 增加 feature projection、state $m\times d_v$、MAC 与存储；
- 推迟相对于 optimized dense attention 的 crossover。

主计算约为 $O(nmd_v)$，所以“线性于 $n$”不等于不依赖 $m$。若为了精度让 $m$ 随 $n$ 或 norm 增长，必须把增长写入复杂度。

## 六、缩放因子怎样进入

Softmax kernel 实际为

$$
e^{q^\top k/\sqrt{d_h}}.
$$

可令 $\tilde q=q/d_h^{1/4}$、$\tilde k=k/d_h^{1/4}$，使 $\tilde q^\top\tilde k=q^\top k/\sqrt{d_h}$，再应用特征恒等式。若只缩一侧或重复缩放，会改变目标 kernel。

位置变换也需核查：RoPE 保范数但改变 dot product；若先/后 feature map 次序不同，不能假设可交换。

## 七、Causal Performer 与状态

一旦得到 $\phi(Q),\phi(K)$，causal 算法沿用 ARCH-52：

$$
S_t=S_{t-1}+\phi(k_t)v_t^\top,
\quad z_t=z_{t-1}+\phi(k_t),
$$

$$
\hat o_t=\frac{\phi(q_t)^\top S_t}{\phi(q_t)^\top z_t}.
$$

这不存完整 KV cache，但 state 的随机近似、累加误差与 denominator 稳定性会随长度共同作用。并行训练仍需 scan/chunk kernel。

## 八、科学空间的推导与批评如何使用

[[S-2020-Su-7921-Performer随机投影]] 详细重写高斯恒等式，并讨论正交特征与实际速度边界，是中文理解入口。文章对当时实现价值的怀疑应视为特定时间/硬件的工程判断；后续 kernel 进步可以改变速度，但不会改变“先算有限规模 crossover”的方法论。

[[S-2021-Su-8338-Performer到线性Attention]] 从随机特征反推可学习 feature activation，带来有启发性的模型设计路线；但把随机投影吸收到可训练层后，模型类已改变，不再自动继承原 FAVOR+ estimator 的无偏/方差保证。

[[S-2021-Su-8601-无限维线性Attention与核特征]] 提供“softmax 是无限维线性 attention”的展开直觉。无限维表示说明存在 feature expansion，不说明有限 $m$ 的效率或最优 feature selection。

## 九、正式图：误差究竟有几层

这张图回答什么问题？为什么 kernel estimator 的无偏性、归一化比值误差和最终 output error 不能合并成一句“近似准确”？

![[00-知识库管理/_assets/figures/architecture/fig-performer-random-feature-error-v1.svg|900]]

> [!figure] 图 1｜Performer 的高斯恒等式、误差传播链与 feature 预算。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_efficient_attention_v1.py]] 生成；随机点仅表示 feature draws，不是实测误差样本。

**怎样读图**：A 从正随机特征的 Gaussian moment identity 开始；B 依次检查 kernel、ratio 和 output 三层误差，特别注意 denominator；C 把 $m$ 同时放入随机误差、feature state/MAC 和随机性合同，而不是只把它当“越大越好”的精度旋钮。

**图没有证明什么**：图没有证明正交特征在所有分布都最优，也没有给出固定 $m$ 下的任务质量；更没有证明 feature 数增加会单调改善训练后的模型，因为优化、数值范围和容量也会变化。

## 十、最小审计实验

对固定 Q/K/V 小矩阵：

1. fp64 计算 exact softmax output；
2. 对多 seed、$m\in\{16,32,64,128,256\}$ 计算 kernel、denominator、output error；
3. 分别报告 bias、variance、RMSE 和最差 query；
4. 扫描 Q/K norm 与 attention sharpness；
5. 比较 iid 与论文规定的 orthogonal features；
6. 再测 kernel time、state bytes 与 end-to-end crossover。

只报告平均 kernel MSE 会隐藏 denominator 小和关键 query 失败。

## 十一、证据边界

- Gaussian moment identity：`I`；
- FAVOR+ 收敛/方差：带 feature construction 和概率条件的 `T`；
- 特定 $m$/任务/硬件质量与速度：`E`；
- 可学习 exp activation 比随机特征“更强”：模型类直觉 `H`，需公平实验；
- 近似 softmax kernel 不等于解释 attention 或保证长度外推。

## 十二、学习出口

应能从高斯矩母函数完整推导正随机特征，解释 ratio bias，设计多 seed 误差审计，并在复杂度中显式保留 $m$ 与 state 维度。

