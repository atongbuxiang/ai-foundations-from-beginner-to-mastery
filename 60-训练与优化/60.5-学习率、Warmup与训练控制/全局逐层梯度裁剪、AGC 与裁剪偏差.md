---
type: derivation
status: verified
area: [training, optimization, gradient-clipping, stochastic-bias]
node_id: TRN-37
aliases: [梯度裁剪总账, Global Layerwise and Adaptive Gradient Clipping]
prerequisites: ["[[学习率、局部损失变化与相对更新尺度]]", "[[Mini-batch 梯度、平均求和与有效 Batch]]", "[[协方差、相关性与条件期望]]"]
related: ["[[Warmup、早期曲率与优化器状态建立]]", "[[NaN、Inf、梯度爆炸与训练失败决策树]]", "[[范数、平坦性、Sharpness 与参数化不变性]]"]
sources: ["[[S-2013-Pascanu-RNN-Training-Difficulty]]", "[[S-2021-Brock-AGC-NFNet]]", "[[S-2023-Koloskova-Gradient-Clipping-Bias]]", "[[S-2024-Su-10657-梯度裁剪模长]]"]
exercises: ["[[习题 - 全局逐层梯度裁剪、AGC 与裁剪偏差]]"]
solutions: ["[[解答 - 全局逐层梯度裁剪、AGC 与裁剪偏差]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-gradient-clipping-estimator-bias-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 全局逐层梯度裁剪、AGC 与裁剪偏差

> [!abstract] 一句话结论
> 梯度裁剪不是“数值不变的保险丝”，而是把随机梯度估计器通过一个非线性映射。全局、逐组、逐层、逐单元和 AGC 定义了不同方向；裁剪发生在 accumulation、All-Reduce、momentum 或预条件之前/之后，也会产生不同算法。

## 一、Global Norm Clipping 的精确定义

给定拼接后的梯度向量 $g$、阈值 $c>0$：

$$
\operatorname{clip}_c(g)
=\alpha(g)g,
\qquad
\alpha(g)
=\min\left(1,\frac{c}{\lVert g\rVert_2+\epsilon_c}\right).
\tag{1}
$$

若 $\lVert g\rVert\le c$，方向不变；若超过阈值，范数被缩到约 $c$。

对纯 SGD，更新为

$$
\Delta\theta=-\eta\,\operatorname{clip}_c(\widehat g).
\tag{2}
$$

当触发裁剪时，step norm 近似 $\eta c$。因此阈值的含义依赖 LR：只调 $c$ 或只调 $\eta$，都不能独立解释实际最大位移。

> [!warning] “默认 1”没有自然单位
> loss 的 sum/mean、参数单位、batch/token reduction 和 optimizer 预处理都会改变 $\lVert g\rVert$。阈值 1 是配置约定，不是跨任务常数。

## 二、Global、Group、Layer、Unit 不是同一种裁剪

设参数被分成 $K$ 组，梯度为 $g=(g_1,\dots,g_K)$。

### Global clipping

$$
\widetilde g_k
=\alpha_{\mathrm{global}}g_k,
\qquad
\alpha_{\mathrm{global}}
=\min\left(1,\frac{c}{\sqrt{\sum_j\lVert g_j\rVert^2}}\right).
\tag{3}
$$

所有层共用同一缩放，保留拼接梯度的方向；一个异常层会缩小所有层。

### Group/layer clipping

$$
\widetilde g_k
=\min\left(1,\frac{c_k}{\lVert g_k\rVert}\right)g_k.
\tag{4}
$$

各层独立缩放，改变层间相对方向；不再与 global clipping 等价。

### Value clipping

$$
\widetilde g_i=\max(-c,\min(c,g_i)).
\tag{5}
$$

它逐坐标截断，通常改变向量方向，不能称为 norm clipping 的实现细节。

## 三、AGC：把梯度阈值相对到参数单元

[[S-2021-Brock-AGC-NFNet]] 的 Adaptive Gradient Clipping 对参数单元 $W_i$ 比较梯度与参数范数：

$$
\rho_i
=\frac{\lVert G_i\rVert}
{\max(\lVert W_i\rVert,\epsilon_w)}.
\tag{6}
$$

若 $\rho_i>\lambda_{\mathrm{AGC}}$，则

$$
\widetilde G_i
=
\lambda_{\mathrm{AGC}}
\max(\lVert W_i\rVert,\epsilon_w)
\frac{G_i}{\lVert G_i\rVert+\epsilon_g}.
\tag{7}
$$

AGC 的“unit”可能是 dense weight 的输出单元/行、convolution kernel 的输出通道、整个 tensor 或框架自定义维度集合。轴选错会改变算法。bias、norm scale、embedding row 和接近零初始化参数也需要明确 include/exclude 规则。

### AGC 与相对参数更新的关系

对 SGD，触发 AGC 时

$$
\frac{\lVert\Delta W_i\rVert}
{\max(\lVert W_i\rVert,\epsilon_w)}
\approx \eta\lambda_{\mathrm{AGC}}.
\tag{8}
$$

所以 AGC 近似限制相对 step。但对 Adam/Muon，若 AGC 作用在 raw gradient、之后又被非线性预条件，这个结论不再直接成立。

## 四、最重要的统计事实：裁剪会引入偏差

即使随机梯度无偏：

$$
\mathbb E[\widehat g\mid\theta]
=\nabla L(\theta),
\tag{9}
$$

通常也有

$$
\mathbb E[\operatorname{clip}_c(\widehat g)\mid\theta]
\ne \nabla L(\theta).
\tag{10}
$$

因为 clip 是非线性函数。

### 一维反例：方向甚至可以反转

令

$$
\widehat g=
\begin{cases}
10,&\text{概率 }0.1,\\
-1,&\text{概率 }0.9.
\end{cases}
$$

则

$$
\mathbb E[\widehat g]
=1-0.9=0.1>0.
\tag{11}
$$

取 $c=1$，裁剪后

$$
\operatorname{clip}_1(\widehat g)
=
\begin{cases}
1,&0.1,\\
-1,&0.9,
\end{cases}
$$

所以

$$
\mathbb E[\operatorname{clip}_1(\widehat g)]
=0.1-0.9=-0.8<0.
\tag{12}
$$

期望方向反转。[[S-2023-Koloskova-Gradient-Clipping-Bias]] 进一步给出 stochastic clipping 的紧收敛界和失败边界。

> [!note] 这不意味着“永远不要裁剪”
> 有偏估计器仍可能在 heavy-tail、outlier、爆炸梯度或有限数值范围下显著改善训练。关键是承认 bias—robustness trade-off，并测量它。

## 五、先平均再裁剪，不等于先裁剪再平均

对 microbatch 梯度 $g_1,\dots,g_M$：

$$
\operatorname{clip}_c\left(\frac1M\sum_{m=1}^M g_m\right)
\ne
\frac1M\sum_{m=1}^M\operatorname{clip}_c(g_m).
\tag{13}
$$

同样，每样本裁剪后平均、每 microbatch 裁剪后 accumulation、本地 worker 裁剪后 All-Reduce、全局 All-Reduce 后裁剪，都是不同估计器。差分隐私 SGD 通常要求 per-example clipping，这与普通 global norm clipping 的目标、阈值和隐私噪声合同不同。

## 六、Clipping 与 Momentum/Adam 的顺序

设 $C(\cdot)$ 表示裁剪。

### Clip gradient before momentum

$$
m_t=\beta m_{t-1}+(1-\beta)C(\widehat g_t).
\tag{14}
$$

历史中保存的是被裁剪梯度。

### Clip momentum/update after accumulation

$$
m_t=\beta m_{t-1}+(1-\beta)\widehat g_t,
\qquad
\widetilde m_t=C(m_t).
\tag{15}
$$

异常梯度仍进入状态，只在当前输出时被限制。未来 step 可能继续受影响。

### Adam 的三个候选位置

1. clip raw $g_t$，再更新 $m_t,v_t$；
2. 更新 moments，再 clip normalized direction $m/\sqrt v$；
3. 形成含 LR/group scale 的 $\Delta\theta$ 后 clip actual step。

三者对 $v_t$、state history、coordinate geometry 和相对 step 的影响都不同，不能只写“max_grad_norm=1”。

## 七、Clipping 与分布式训练

数据并行下，本地梯度 $g^{(r)}$ 若先裁剪：

$$
\frac1R\sum_r C(g^{(r)})
$$

不等于先全局平均再裁剪：

$$
C\left(\frac1R\sum_r g^{(r)}\right).
$$

还要核对：

- ZeRO/FSDP 分片后 global norm 如何聚合；
- norm 的平方和是否跨 rank 正确 All-Reduce；
- bf16/fp32 accumulation dtype；
- gradient accumulation 的 unscale 时机；
- unused/sparse parameters 是否进入 norm；
- overflow 检查在 clip 前还是后。

## 八、阈值如何选择：从目标量而不是传统数字出发

至少有四种可解释方式：

| 目标 | 阈值设计 |
|---|---|
| 限制 SGD absolute step | 令 $\eta c$ 不超过预注册值 |
| 限制 layer relative step | 用 layer/AGC，控制 $\eta c_\ell/\lVert W_\ell\rVert$ |
| 抗 heavy-tail/outlier | 用梯度范数分位数/稳健统计，报告 bias |
| 只做异常保险丝 | 令正常训练 clip rate 很低，并报警定位根因 |

应记录：

$$
\text{clip rate},\quad
\alpha_t,\quad
\lVert g_t\rVert,\quad
\lVert C(g_t)\rVert,\quad
\cos(g_t,C(g_t)),
\tag{16}
$$

以及按层/参数组分解的触发率。若 80% step 都裁剪，阈值已经定义了主要优化器，而不是偶发护栏。

## 九、图：裁剪位置决定估计器

先看图回答：为什么同一个阈值，在 per-example、microbatch、global、momentum 和 AGC 位置上会得到不同更新？

![[00-知识库管理/_assets/figures/training-optimization/fig-gradient-clipping-estimator-bias-ledger-v1.svg|880]]

> [!figure] 图 TRN-37　梯度裁剪的对象—位置—偏差总账
> 左侧比较先裁剪/先平均，中央比较 global/layer/AGC 与 optimizer-state 顺序，右侧用一维分布展示 clipping 可反转期望方向。来源：依据 [[S-2023-Koloskova-Gradient-Clipping-Bias]]、[[S-2021-Brock-AGC-NFNet]] 与 [[S-2013-Pascanu-RNN-Training-Difficulty]] 原创绘制。

**怎样读图**：先确定随机样本单位，再沿 accumulation/communication/state 路径找到 clip 的确切位置；最后判断它限制的是 gradient norm、relative parameter step 还是 actual update。

**图没有证明什么**：它不证明裁剪必然有害，也不证明 AGC 在 NFNet 之外普遍优于 global clipping。

## 十、科学空间研读框

[[S-2024-Su-10657-梯度裁剪模长]] 追问默认 norm 1 与一阶 loss change 的关系。课程将这条尺度直觉补成完整合同：$\eta c$ 只在特定 SGD/global-clip 顺序下近似限制 step；对 Adam、Muon、accumulation 和分布式归约，必须重新追踪实际更新。

## 十一、初学者自检

1. 为什么 global clip 保留拼接方向，layer clip 却改变层间方向？
2. 写出一个无偏随机梯度经裁剪后方向反转的例子。
3. clip-before-momentum 与 clip-after-momentum 的 state 有何不同？
4. AGC 的 unit axis 为什么属于算法定义？
5. “clip rate 80%”为什么说明裁剪不再只是保险丝？

## 十二、本节出口

你应能把任一 clipping 配置还原为

$$
\text{sample unit}
\to
\text{reduction/communication}
\to
\text{clip object and norm}
\to
\text{optimizer state}
\to
\text{actual step},
$$

并明确估计器偏差与鲁棒收益。

## 练习与独立解答

- [[习题 - 全局逐层梯度裁剪、AGC 与裁剪偏差]]
- [[解答 - 全局逐层梯度裁剪、AGC 与裁剪偏差]]
