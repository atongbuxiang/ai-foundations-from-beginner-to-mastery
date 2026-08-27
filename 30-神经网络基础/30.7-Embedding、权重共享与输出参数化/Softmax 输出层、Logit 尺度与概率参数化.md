---
type: derivation
status: draft
area: [neural-networks/embedding-output, softmax, logits, categorical-parameterization]
aliases: [Softmax Output Head, Logit Scale and Categorical Probability]
node_id: NN-52
prerequisites: ["[[Softmax–Cross-Entropy 的稳定融合反向]]", "[[交叉熵与 KL 散度]]", "[[线性泛函与对偶空间]]", "[[函数、映射、关系与等价类]]"]
related: ["[[输入—输出权重共享与 Weight Tying]]", "[[Softmax Bottleneck 与低秩限制]]", "[[Sampled、Hierarchical 与 Adaptive Softmax]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[Label Smoothing、置信度与目标偏置]]"]
sources: ["[[S-2022-Su-9070-logsumexp不等式]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]", "[[S-2023-Su-9698-Output-Embedding]]"]
exercises: ["[[习题 - Softmax 输出层、Logit 尺度与概率参数化]]"]
solutions: ["[[解答 - Softmax 输出层、Logit 尺度与概率参数化]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-softmax-output-parameterization-v2.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Softmax 输出层、Logit 尺度与概率参数化

> [!abstract] 本章主问题
> 线性输出层先产生未归一化 logits，Softmax 再把 logit 的平移等价类映到 categorical simplex 内部。概率只由两两 logit differences 决定；正温度/尺度不改 argmax，却改变 entropy、NLL、梯度、曲率和校准。有限 logits 无法精确表示 $p_i=0$ 的边界分布，而大词表 full Softmax 仍需形成并归一化全部 $V$ 个类别。

## 一、学习目标

读完本节，你应能：

1. 写出 hidden–logit–probability 的完整 shape 合同；
2. 证明 Softmax 的 normalization、正性和平移不变性；
3. 从 log-odds 证明概率只依赖 logit differences；
4. 构造 simplex interior 到 logit gauge 的逆映射；
5. 推导 temperature 对概率、梯度、Hessian 与 entropy 的影响；
6. 解释 bias、weight tying、mask 与 logit scale 的角色；
7. 区分高 confidence、概率校准与正确决策；
8. 审计 stable logsumexp 与 full-vocabulary 成本。

## 二、从 hidden state 到 logits

设 hidden state

$$
h\in\mathbb R^{d_h},
$$

类别/词表大小为 $V$。输出层参数

$$
W\in\mathbb R^{V\times d_h},
\qquad
b\in\mathbb R^V
$$

产生

$$
\boxed{z=Wh+b\in\mathbb R^V}.
$$

第 $i$ 个 logit

$$
z_i=w_i^\mathsf Th+b_i
$$

是一个实数 score，不是概率，也不要求非负或和为 1。对 batch/sequence hidden

$$
H\in\mathbb R^{B\times T\times d_h},
$$

输出 logits shape 是

$$
Z\in\mathbb R^{B\times T\times V}.
$$

最后一维 $V$ 才是 categorical normalization axis。

## 三、Softmax 定义

对 $z\in\mathbb R^V$，

$$
\boxed{
p_i=\operatorname{softmax}(z)_i
=\frac{e^{z_i}}{\sum_{j=1}^Ve^{z_j}}
}.
$$

因为指数为正，

$$
p_i>0,
$$

且

$$
\sum_i p_i=1.
$$

因此

$$
p\in\Delta_{V-1}^{\circ}
=\{p\in\mathbb R^V:p_i>0,\sum_i p_i=1\},
$$

即概率单纯形的内部。

## 四、平移不变性与 Gauge

对任意 $c\in\mathbb R$，

$$
\frac{e^{z_i+c}}{\sum_je^{z_j+c}}
=\frac{e^ce^{z_i}}{e^c\sum_je^{z_j}}
=p_i.
$$

故

$$
\boxed{
\operatorname{softmax}(z+c\mathbf1)
=\operatorname{softmax}(z)
}.
$$

logits 不是唯一参数；真正可辨识对象是商空间

$$
\mathbb R^V/\operatorname{span}\{\mathbf1\}.
$$

可选择 gauge：

- $max_i z_i=0$，适合数值计算；
- $\sum_i z_i=0$，适合对称分析；
- 固定一个 reference logit 为 0，适合统计模型。

不同 gauge 表示同一概率。

## 五、Log-Odds 就是 Logit Difference

对任意 $i,j$：

$$
\frac{p_i}{p_j}
=\frac{e^{z_i}}{e^{z_j}}
=e^{z_i-z_j}.
$$

所以

$$
\boxed{
\log\frac{p_i}{p_j}=z_i-z_j
}.
$$

这说明：

- ranking 只由 logit differences 决定；
- common bias/shift 不可辨识；
- margin $z_y-\max_{j\ne y}z_j$ 直接是相对 log-odds 的最小证据差；
- 单个绝对 logit 没有脱离 gauge 的概率意义。

## 六、Softmax 对 simplex interior 是满的

给任意严格正概率

$$
p_i>0,
\qquad
\sum_i p_i=1,
$$

取

$$
z_i=\log p_i.
$$

则

$$
\operatorname{softmax}(z)_i
=\frac{p_i}{\sum_jp_j}=p_i.
$$

所以自由 logits 可表示任意 interior categorical distribution。加任意 $c$ 仍表示同一个 $p$。若固定 sum-zero gauge，唯一代表为

$$
\boxed{
z_i=\log p_i-\frac{1}{V}\sum_j\log p_j
}.
$$

这不意味着深网输出层能在所有 contexts 自由选择任意 $z$；$z=Wh+b$ 与 hidden family 会施加跨 context 的结构约束，后续[[Softmax Bottleneck 与低秩限制]]专门分析这一点。

## 七、边界概率需要无限 Logit Gap

有限 logits 给 $p_i>0$。若希望

$$
p_i=0,
$$

则必须让

$$
z_i-\max_jz_j\to-\infty.
$$

同理，one-hot probability 只能作为差值趋于无穷时的极限。分类数据线性可分时，cross-entropy 可通过 logit norm 持续增长逼近 0，而没有有限最优 logit；0–1 error 已为零不代表 NLL 已为零。

mask 在实数数学中常把 invalid class logit 设为 $-\infty$，这相当于改变支持集；用有限大负数近似时必须结合 dtype 和稳定实现审计泄漏。

## 八、Temperature 与 Logit Scale

定义

$$
\boxed{
p_i^{(\tau)}
=\frac{e^{z_i/\tau}}
{\sum_je^{z_j/\tau}},
\qquad
\tau>0
}.
$$

等价于把 logits 乘 scale

$$
s=\frac1\tau.
$$

- $\tau<1$：差值放大，分布更尖；
- $\tau>1$：差值缩小，分布更平；
- 任意 $\tau>0$ 保持无并列时 argmax；
- 概率、NLL、entropy、梯度与 calibration 都会改变。

## 九、Temperature 对 Entropy 的单调性

记

$$
Z(\tau)=\sum_i e^{z_i/\tau},
\qquad
\mu_\tau=\mathbb E_{p^{(\tau)}}[z].
$$

entropy 为

$$
H(\tau)
=-\sum_i p_i^{(\tau)}\log p_i^{(\tau)}
=\log Z(\tau)-\frac{\mu_\tau}{\tau}.
$$

令 $\beta=1/\tau$，指数族恒等式给

$$
\frac{d\mu}{d\beta}=\operatorname{Var}_{p^{(\tau)}}(z).
$$

因此

$$
\boxed{
\frac{dH}{d\tau}
=\frac{\operatorname{Var}_{p^{(\tau)}}(z)}{\tau^3}
\ge0
}.
$$

只要 logits 不全相等，entropy 随温度严格增加。$\tau\to\infty$ 时趋于 uniform；$\tau\to0^+$ 时集中到最大 logit 的并列集合。

## 十、Gradient 与 Hessian 的尺度

对 normalized target $y$，temperature-softmax cross-entropy

$$
\ell_\tau(z,y)
=-\sum_i y_i\log p_i^{(\tau)}
$$

满足

$$
\boxed{
\nabla_z\ell_\tau
=\frac{p^{(\tau)}-y}{\tau}
}.
$$

Hessian 为

$$
\boxed{
\nabla_z^2\ell_\tau
=\frac1{\tau^2}
\left[\operatorname{Diag}(p)-pp^\mathsf T\right]
}.
$$

所以温度不仅改变 target distribution 的“软硬”，还显式改变 gradient 和 curvature scale。蒸馏中额外乘 $\tau^2$ 是另一个 objective 约定，必须写明。

## 十一、一个三类手算

取

$$
z=(2,1,0).
$$

$\tau=1$ 时，减去最大值后指数为

$$
(1,e^{-1},e^{-2}),
$$

所以

$$
p\approx(0.66524,0.24473,0.09003).
$$

对第一类与第三类，

$$
\log\frac{p_1}{p_3}=2=z_1-z_3.
$$

加 100：

$$
(102,101,100)
$$

概率完全不变。取 $\tau=2$，

$$
p^{(2)}=\operatorname{softmax}(1,0.5,0)
\approx(0.50648,0.30720,0.18632),
$$

分布更平，但第一类仍是 argmax。

## 十二、Output Bias 的角色

若 $h=0$，

$$
p=\operatorname{softmax}(b).
$$

给定严格正 baseline prior $\pi$，取

$$
b_i=\log\pi_i+c
$$

即可使初始输出为 $\pi$。因此 bias 可表达类别基线频率，而 rows $w_i$ 表达 feature-dependent differences。

但训练后 $b$ 不必等于数据 log-frequency；regularization、sampling、label smoothing、class weights 和 hidden mean 都会改变它。把 bias 初始化为 log prior 也改变初始 loss/gradient，需作为实验因素登记。

## 十三、与 Weight Tying 的接口

共享输出矩阵时

$$
z_i=e_i^\mathsf Th+b_i.
$$

若对 $e_i,h$ 做 unit normalization 并加入 scale $s$：

$$
z_i=s\cos\theta_i+b_i.
$$

这把 output head 变成 cosine classifier。$s$ 决定最大可实现 logit gap 和梯度尺度；固定/学习 $s$、是否有 bias、norm 的 $\varepsilon$ 都会改变概率族。不能把 cosine visualization 与 raw tied Softmax 当成同一模型。

## 十四、Stable Softmax 与 LogSumExp

直接算 $e^{z_i}$ 可能 overflow。取

$$
m=\max_i z_i,
$$

利用 shift invariance：

$$
p_i
=\frac{e^{z_i-m}}{\sum_je^{z_j-m}}.
$$

log-probability 应写为

$$
\log p_i
=z_i-m-log\sum_je^{z_j-m}.
$$

训练使用 fused logits-domain cross-entropy，避免先形成 underflow 到 0 的概率再取 log。完整反向与 reduction 细节见[[Softmax–Cross-Entropy 的稳定融合反向]]。

## 十五、Confidence 不等于 Calibration

最大 Softmax 概率

$$
\max_i p_i(x)
$$

是模型内部 confidence score。它不自动等于

$$
\Pr(Y=\widehat Y\mid \max p=s).
$$

把 logits 正尺度放大可以让 confidence 接近 1，却不改变 argmax accuracy。temperature scaling 可在 validation protocol 下改善 calibration，但不能凭同一 validation set 的反复选择宣称无偏；distribution shift 下也需重验。详见[[概率校准、Proper Scoring Rule 与可靠性图]]。

## 十六、Full-Vocabulary 成本

对每个 hidden state，dense output projection 计算

$$
Wh
$$

需要约 $O(Vd_h)$ 乘加，并形成 $V$ 个 logits；Softmax normalization 本身还需 $O(V)$ reduction/exp。对 $BT$ 个位置，朴素账本为

$$
O(BTVd_h)
$$

以及 $O(BTV)$ logit/probability 临时量级。

在大词表系统中，matrix multiplication、memory bandwidth、vocabulary sharding、cross-device max/sum reduction 与 loss fusion 共同决定成本。sampled/hierarchical/adaptive 方法改变计算与有偏性，留到[[Sampled、Hierarchical 与 Adaptive Softmax]]。

## 十七、概率参数化的边界

Softmax 只说明给定 $z$ 如何得到 categorical law，不说明：

- logits 是否能表达所有 context-to-distribution mappings；
- 模型概率是否 calibrated；
- OOD 输入上 confidence 是否可靠；
- argmax 是否符合成本敏感决策；
- sampled approximation 是否仍优化同一 likelihood；
- mask/特殊 token 是否定义了正确支持集。

输出层是概率合同的一部分，不是整个统计模型的证明。

## 十八、图：Logit 差、温度与单纯形

先看图回答：为什么加 common shift 不改变概率？为什么温度不改 argmax 却改变 entropy 和 gradient？有限 logits 为什么只能落在 simplex interior？

![[00-知识库管理/_assets/figures/neural-networks/fig-softmax-output-parameterization-v2.svg|900]]

> [!figure] 图 30.7-04　Softmax 输出参数化的 gauge、temperature 与系统边界
> 左栏从 $h$ 经 affine head 到 categorical law，并突出 log-odds 等于 logit difference；中栏展示 shift gauge 与温度的 entropy/gradient 效应；右栏并列 stable logsumexp、概率边界和 full-vocabulary 成本。来源：依据 Goodfellow et al.、D2L、苏剑林的 logsumexp/输出 Embedding 讨论与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_embedding_output_foundations_v2.py]] 确定性生成。

**怎样读图**：先把 logits 与 probability 分开，再固定 gauge 比较差值；随后检查 scale/temperature，最后把数值归一化和词表并行成本加入合同。

**图没有证明什么**：图不证明 Softmax confidence 已校准，也不证明线性 head 能对所有 contexts 表达任意 categorical distribution。

## 十九、最小验收

1. 写出 $[B,T,d_h]\to[B,T,V]$；
2. 证明正性、归一化和平移不变性；
3. 推导 log-odds 与 sum-zero inverse；
4. 解释 simplex boundary；
5. 推导 $dH/d\tau$、gradient 与 Hessian；
6. 复算 $z=(2,1,0)$ 在两个温度下的概率；
7. 分析 bias prior 与 tied cosine head；
8. 给出 stable/logit/large-vocab/calibration 四层审计。

> [!summary]
> Softmax 把 logit differences 参数化为严格正 categorical probabilities；common shift 是冗余 gauge，temperature 是会改变 entropy、梯度和校准的真实尺度。理解输出层必须同时掌握概率几何、数值实现、weight/bias 参数化与大词表系统成本。

- [[Embedding、权重共享与输出参数化 MOC]]
- [[习题 - Softmax 输出层、Logit 尺度与概率参数化]]
- [[解答 - Softmax 输出层、Logit 尺度与概率参数化]]
