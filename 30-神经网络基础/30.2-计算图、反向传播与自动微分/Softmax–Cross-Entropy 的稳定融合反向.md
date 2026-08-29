---
type: derivation
status: draft
area: [neural-networks/losses, softmax, cross-entropy, numerical-stability]
aliases: [Fused Softmax Cross Entropy, Stable Log-Softmax Backward]
node_id: NN-14
prerequisites: ["[[激活、分支、广播与梯度累加]]", "[[交叉熵与 KL 散度]]", "[[数值稳定性|对数和指数的数值稳定计算]]"]
related: ["[[逻辑回归、复合损失与概率分类]]", "[[Label Smoothing、置信度与目标偏置|标签平滑与决策边界]]", "[[Forward_Reverse AD、Tape 与复杂度|Forward/Reverse AD、Tape 与复杂度]]", "[[Taylor 展开与余项]]", "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]"]
sources: ["[[S-2022-Su-9070-logsumexp不等式]]", "[[S-2026-Su-11814-LSE-Softmax-Taylor]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]"]
exercises: ["[[习题 - Softmax–Cross-Entropy 的稳定融合反向]]"]
solutions: ["[[解答 - Softmax–Cross-Entropy 的稳定融合反向]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-softmax-cross-entropy-fused-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# Softmax–Cross-Entropy 的稳定融合反向

> [!abstract] 本章主问题
> 对 logits $z$ 和归一化 target $y$，softmax cross-entropy 可重写为 $\operatorname{LSE}(z)-y^Tz$，因而梯度是 $p-y$。这个简洁结果同时依赖归一化、损失定义与 reduction scale。实现上应从 shifted log-sum-exp 直接计算 log-probability 与融合 backward，避免先形成极端概率再取对数。

## 课程位置与两遍学习路线

- **承接什么：** NN-13 已产生二维 logits $Q$，但 logits 既不是概率，也还没有定义训练目标；
- **本页解决什么：** 用 shifted log-sum-exp 把 logits、normalized target、cross-entropy、mean reduction 与 $P-Y$ 反向写成一个稳定合同；
- **后续为何需要：** NN-15 将比较对该 scalar loss 求导的 forward/reverse 成本，NN-16 用差分和 HVP 独立检查一阶、二阶作用。

**第一遍只记住稳定三步。** 每行减最大值、用 log-sum-exp 计算 NLL、直接用 $P-Y$ 回传；同时明确 sum 还是 mean。

**第二遍再推导边界。** 从 LSE differential 与 softmax Jacobian 两条路线交叉验证，并检查 soft target 归一化、temperature、mask、label smoothing、shift zero-direction 和有限精度。

### 问题链

1. 为什么 logits 不能直接解释为概率？
2. 减去每行最大值为什么是恒等变换，不是数值近似？
3. $P-Y$ 的简洁形式依赖 target 的哪个归一化条件？
4. mean reduction 为什么会把整个 batch gradient 再除以有效样本数？
5. 为什么稳定 fused operator 比“先 softmax、再 log、再链式相乘”更可靠？

> [!check] 第一遍停靠线
> 若你能从 $Q$ 算出 mean loss 约 $0.0255315$，并写出每行和为零的 $\bar Q=(P-Y)/2$，就可以进入 AD mode；Hessian、temperature 与非标准 target 留到第二遍。

## 符号与对象账本

| 对象 | shape | 在 AI 分类头中的身份 | 不能偷换成 |
|---|---|---|---|
| $Q$ | $2\times2$ | raw logits | 已归一化 probability |
| $Y_c$ | $2\times2$ | one-hot target distributions | model prediction |
| $P=\operatorname{softmax}(Q)$ | $2\times2$ | categorical probabilities | 独立 Bernoulli outputs |
| $\ell_1,\ell_2$ | scalar per sample | NLL contributions | 已经 mean 的 batch loss |
| $L_{\rm ce}$ | scalar | mean training objective | calibration/deployment risk 的全部 |

### 贯穿算例：同一 logits 的稳定前向与融合反向

沿用 $X_\diamond$ 路径在 NN-13 得到

$$
Q=\begin{bmatrix}8&2\\1&4\end{bmatrix},\qquad
Y_c=\begin{bmatrix}1&0\\0&1\end{bmatrix}.
$$

逐行减最大值后，logit gaps 分别为 $6$ 与 $3$。因此

$$
P\approx\begin{bmatrix}0.997527&0.002473\\0.047426&0.952574\end{bmatrix},qquad
L_{\rm ce}=\frac{-\log P_{11}-\log P_{22}}2\approx0.0255315.
$$

mean reduction 的融合反向为

$$
\bar Q=\frac{P-Y_c}{2}
\approx\begin{bmatrix}-0.001236&0.001236\\0.023713&-0.023713\end{bmatrix}.
$$

每行梯度和为零，对应 softmax 对 $Q+\alpha\mathbf1$ 的 shift invariance。下一页将用方向 $V=E_{11}$ 同时做 JVP 与 VJP。

## 核心公式七问：$\ell(q,y)=\operatorname{LSE}(q)-y^Tq,\;\nabla_q\ell=p-y$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 在不形成 softmax Jacobian 和 $-y/p$ 中间大数时得到稳定 loss 与 logit gradient |
| 对象 | $q$ 是 logits，$y$ 是和为 1 的 target distribution，$p=\nabla\operatorname{LSE}(q)$ |
| 来路 | 展开 $-\sum_i y_i\log p_i$ 并使用 $\sum_i y_i=1$ |
| 步骤 | shifted LSE 算值；反向直接计算 $p-y$；batch mean 最后除有效样本数 |
| 读法 | 提高真类 logit、压低其余 logits，但共同平移方向没有梯度 |
| 检查 | 梯度分量和为零；非归一化 target 时应为 $(\sum y_i)p-y$ |
| 去路 | language-model token loss、label smoothing、distillation temperature、fused kernels 与 curvature |

## 一、对象合同

对 $K$ 类单样本，给 logits

$$
z=(z_1,…,z_K)\in\mathbb R^K,
$$

softmax probability 为

$$
p_i=\frac{e^{z_i}}{\sum_{j=1}^Ke^{z_j}},
\qquad \sum_i p_i=1.
$$

对 target distribution $y_i\ge0$、$\sum_i y_i=1$，cross-entropy 是

$$
\ell(z,y)=-\sum_{i=1}^K y_i\log p_i.
$$

one-hot label $c$ 是 $y_c=1$、其余为 0，此时 $\ell=-\log p_c$。

## 二、Shift Invariance 与 Stable Softmax

对任意标量 $a$，

$$
\operatorname{softmax}(z+a\mathbf1)=\operatorname{softmax}(z).
$$

取 $m=\max_i z_i$，

$$
p_i=\frac{e^{z_i-m}}{\sum_j e^{z_j-m}}.
$$

现在所有指数输入不大于 0，至少一项等于 1，避免 $e^{1000}$ 溢出。减最大值是代数恒等变换，不是近似。

## 三、损失重写为 LogSumExp

因

$$
\log p_i=z_i-\log\sum_j e^{z_j},
$$

且 $\sum_i y_i=1$，

$$
\ell(z,y)
=\log\sum_j e^{z_j}-\sum_i y_i z_i
=\operatorname{LSE}(z)-y^Tz.
$$

稳定值计算是

$$
\ell
=m+\log\sum_j e^{z_j-m}-y^Tz.
$$

对 one-hot target，最后一项就是 $-z_c$。

## 四、直接微分：一行得到 $p-y$

LogSumExp 的 differential 是

$$
d\operatorname{LSE}(z)
=\sum_i p_i\,dz_i
=p^Tdz.
$$

因此

$$
d\ell=(p-y)^Tdz,
$$

即

$$
\boxed{\nabla_z\ell=p-y.}
$$

这个推导不需物化 softmax Jacobian，也避免了 $-y_i/p_i$ 在极小 $p_i$ 处的中间大数。

## 五、用 Softmax Jacobian 交叉验证

softmax 的分量导数为

$$
\frac{\partial p_i}{\partial z_j}
=p_i(\delta_{ij}-p_j),
$$

所以

$$
J_p=\operatorname{diag}(p)-pp^T.
$$

对 $\ell=-\sum_i y_i\log p_i$，$\partial\ell/\partial p_i=-y_i/p_i$。因 $J_p$ 对称，

$$
J_p^T\left(-\frac{y}{p}\right)
=-y+p\sum_i y_i
=p-y.
$$

这个交叉推导明确显示 $\sum_i y_i=1$ 的作用。

## 六、非归一化 Soft Target 的一般式

若 $\alpha=\sum_i y_i$ 不一定为 1，但损失仍定义为 $-\sum_i y_i\log p_i$，则

$$
\ell=\alpha\operatorname{LSE}(z)-y^Tz,
\qquad
\nabla_z\ell=\alpha p-y.
$$

所以“梯度永远是 $p-y$”是错的；它隐含 normalized target 合同。class weights、sample weights、mask 和非标准 reduction 也会改变 scale。

## 七、一个极端 Logit 手算

取

$$
z=(1000,999,998),\qquad c=2.
$$

减去 $m=1000$ 得 $(0,-1,-2)$，所以

$$
p\approx(0.66524,0.24473,0.09003).
$$

对第二类 one-hot target，

$$
\ell=-\log p_2\approx1.40761,
$$

$$
\nabla_z\ell
\approx(0.66524,-0.75527,0.09003).
$$

梯度各分量之和为 0，因为沿 $\mathbf1$ 同时平移所有 logits 不改变损失。

## 八、为什么要 Fused Forward/Backward

天真实现可先算 `p = softmax(z)`，再算 `-log(p[c])`。在有限精度中，小概率可 underflow 为 0，然后 `log(0)=-inf`，而真实 NLL 仍是有限大数。

稳定 fused operator：

1. 用 shifted logsumexp 直接得 log-probability/loss；
2. backward 重用稳定 softmax 或保存的 normalization statistics；
3. 直接输出 $p-y$，不形成 $-y/p$ 与 Jacobian product；
4. 把 mask、label smoothing、class weight 和 reduction 放在同一明确合同中。

## 九、Batch 与 Reduction

对 logits $Z:[B,K]$、targets $Y:[B,K]$，逐样本梯度是 $P-Y$。若

$$
L_{sum}=\sum_{b=1}^B\ell_b,
$$

则 $\bar Z=P-Y$；若

$$
L_{mean}=\frac1B\sum_{b=1}^B\ell_b,
$$

则

$$
\bar Z=\frac{P-Y}{B}.
$$

有 padding/mask 时，mean 的分母通常是有效 token 数，不是固定 $BT$。distributed training 必须对齐 global valid count 和 all-reduce 默认 scale。

## 十、Label Smoothing

一种定义是

$$
y^{(\varepsilon)}=(1-\varepsilon)e_c+\varepsilon u,
$$

其中 $u$ 是某个归一化参考分布（可包含或不包含真类，必须声明）。梯度仍为

$$
p-y^{(\varepsilon)}.
$$

不同库对 $u$ 的定义可不同，所以只报一个 smoothing coefficient 不足以重现损失。

## 十一、Temperature

若

$$
p_i^{(\tau)}
=\frac{e^{z_i/\tau}}{\sum_j e^{z_j/\tau}},
$$

且损失是 $-\sum_i y_i\log p_i^{(\tau)}$，则

$$
\nabla_z\ell=\frac{p^{(\tau)}-y}{\tau}.
$$

若 distillation 另外乘 $\tau^2$，总梯度 scale 又改变。temperature 越小，分布越尖，但局部曲率与数值敏感性也变大。

## 十二、Hessian、Convexity 与平移零方向

对 normalized fixed target，

$$
\nabla_z^2\ell
=\operatorname{diag}(p)-pp^T\succeq0.
$$

它是 categorical one-hot vector 的 covariance matrix，并满足

$$
\left(\operatorname{diag}(p)-pp^T\right)\mathbf1=0.
$$

因此损失对 logits 凸，但在完整 logit space 上因 shift invariance 不严格凸。logits 由深网络非线性生成时，对 logits 的凸性不能外推为对 parameters 凸。

## 十三、与 Binary Cross-Entropy 的区别

softmax 把 $K$ 类强制为互斥且概率和为 1。multi-label 任务通常对每类用独立 sigmoid binary cross-entropy，梯度形式也可写成 $\sigma(z)-y$，但没有类间 normalization 耦合。不能因为公式相像就互换任务合同。

## 十四、图：稳定前向与融合反向是同一个合同

先看图回答：为什么“减去最大 logit”不改变 probability，而“先 softmax 后 log”却可能改变浮点结果？

![[00-知识库管理/_assets/figures/neural-networks/fig-softmax-cross-entropy-fused-v2.svg|900]]

> [!figure] 图 30.2-06　Shifted logsumexp、$p-y$ 与 reduction/curvature 账本
> 左栏对照 naive exponentiation 与 max-shift；中栏从 $\operatorname{LSE}(z)-y^Tz$ 直达 $p-y$；右栏分开 target normalization、temperature、mask/reduction 与 Hessian 零方向。来源：依据科学空间 logsumexp 文章、Goodfellow–Bengio–Courville 和 D2L 独立绘制；由 [[00-知识库管理/_labs/code/plot_backprop_advanced_v2.py]] 确定性生成。

**怎样读图**：先把数学恒等重写与浮点实现分开，再逐项核对 target sum、temperature 和 reduction 对 gradient scale 的影响。

**图没有证明什么**：图没有证明 cross-entropy 会产生良好校准、深网络参数优化为凸，或任意 fused kernel 在低精度下都数值安全。

## 十五、验证清单

> [!connection] Taylor 近似与 Attention 的边界
> [[S-2026-Su-11814-LSE-Softmax-Taylor]] 可帮助理解 LSE/Softmax 的局部级数，但 fused cross-entropy 的稳定恒等式并不要求截断近似。若用低阶多项式替代 softmax，必须额外检查概率和、非负性、shift invariance、梯度/Hessian 误差与极端 logits；进入 [[Scaled Dot-Product Attention 与 Softmax 数值语义]] 后还要检查 mask 与 normalized output，不能把局部展开直接当作全域线性 Attention。

1. logits 平移 $z\mapsto z+a\mathbf1$ 后 loss/probability 应不变；
2. normalized target 下梯度分量和应近 0；
3. 用极端 logits 比较 naive 与 stable forward；
4. 对非极端 FP64 小例做 finite difference；
5. 单独验证 one-hot、soft target、label smoothing、class/sample weights；
6. 用不同有效 token 数验证 mean denominator；
7. 对 temperature 检查 $1/\tau$ 因子；
8. 在 FP16/BF16/FP32 下报告 finite loss、gradient 和误差，不只看不报错。

## 十六、回顾与练习

> [!summary]
> normalized cross-entropy 的核心重写是 $\ell=\operatorname{LSE}(z)-y^Tz$，因此 $\nabla_z\ell=p-y$。正确实现还必须同时处理 max-shift、target normalization、temperature、mask 和 reduction scale。

- [[习题 - Softmax–Cross-Entropy 的稳定融合反向]]
- [[解答 - Softmax–Cross-Entropy 的稳定融合反向]]
