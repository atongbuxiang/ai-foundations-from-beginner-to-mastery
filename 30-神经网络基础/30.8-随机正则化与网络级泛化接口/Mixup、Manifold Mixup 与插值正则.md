---
type: derivation
status: draft
area: [neural-networks/regularization, mixup, manifold-mixup, vicinal-risk, interpolation]
aliases: [Mixup, Manifold Mixup, Vicinal Interpolation]
node_id: NN-62
prerequisites: ["[[凸集、凸组合与分离超平面]]", "[[损失、总体风险与经验风险]]", "[[数据增强、不变性、等变性与任务充分性]]", "[[Label Smoothing、置信度与目标偏置]]"]
related: ["[[Embedding 几何、相似度与各向异性]]", "[[表示学习的任务、表示与下游风险]]", "[[Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]", "[[网络级正则化的交互、消融与证据地图]]"]
sources: ["[[S-2018-Zhang-Mixup]]", "[[S-2019-Verma-Manifold-Mixup]]"]
exercises: ["[[习题 - Mixup、Manifold Mixup 与插值正则]]"]
solutions: ["[[解答 - Mixup、Manifold Mixup 与插值正则]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-mixup-vicinal-geometry-v2.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Mixup、Manifold Mixup 与插值正则

> [!abstract] 本章主问题
> Mixup 不只是“把两张图平均”。它先定义 pairing 和 $\lambda$ 的随机机制，再用同一个 $\lambda$ 对输入与监督 target 做凸组合，从 empirical distribution 改到一族 vicinal distributions。Manifold Mixup 把插值位置移到随机 hidden layer。两者都对样本间行为施加线性/平滑归纳偏置，但 input chord、hidden chord 与真实语义路径并不自动相同；Beta 参数、增强顺序、mask、normalization、distributed pairing 与评估协议都是方法合同的一部分。

## 一、学习目标

读完本节，你应能：

1. 写出 Mixup 的概率空间、pairing 与 target 合同；
2. 推导 $\operatorname{Beta}(\alpha,\alpha)$ 的均值、方差与平均混合强度；
3. 把 Mixup 写成 vicinal risk；
4. 证明 soft-target cross-entropy 对 label mixing 精确线性；
5. 完成二维输入与三分类 target 手算；
6. 推导 hidden Mixup 的 backward split；
7. 区分 input chord、learned representation chord 与真实 data manifold；
8. 分析 Mixup 与 Label Smoothing 的可交换部分；
9. 审计 pairing、augmentation order、padding、BatchNorm 与 distributed RNG；
10. 设计自然协议、matched-strength 与 semantic-validity 三轨验收。

## 二、标准 Mixup 合同

训练样本为 $(x_i,y_i)$ 与 $(x_j,y_j)$，其中 target 可是 one-hot 或 simplex probability vector。采

$$
\lambda\sim\operatorname{Beta}(\alpha,\alpha),
\qquad \alpha>0.
$$

定义

$$
\boxed{
\widetilde x=\lambda x_i+(1-\lambda)x_j,
\qquad
\widetilde y=\lambda y_i+(1-\lambda)y_j.
}
$$

关键不变量是：

1. 输入与 target 使用同一个 $\lambda$；
2. $\lambda\in(0,1)$，所以二者都在相应凸包内；
3. pairing distribution 明确：同 batch permutation、全局池或 class-conditional；
4. model 在 $\widetilde x$ 上求值，而不是把两个原样本 prediction 事后平均。

## 三、Beta 参数控制什么

对对称 Beta distribution，

$$
\mathbb E[\lambda]=\frac12.
$$

一般 Beta$(a,b)$ 的方差是

$$
\frac{ab}{(a+b)^2(a+b+1)}.
$$

令 $a=b=\alpha$，得到

$$
\boxed{
\operatorname{Var}(\lambda)
=\frac{1}{4(2\alpha+1)}.
}
$$

另一个直接衡量 chord interior 强度的量是

$$
\lambda(1-\lambda).
$$

利用

$$
\mathbb E[\lambda^2]
=\frac{\alpha+1}{2(2\alpha+1)},
$$

可得

$$
\boxed{
\mathbb E[\lambda(1-\lambda)]
=\frac{\alpha}{2(2\alpha+1)}.
}
$$

### 3.1 三个 regime

- $\alpha\ll1$：密度集中在 0 和 1，样本多接近某个 endpoint；
- $\alpha=1$：$\lambda$ uniform；
- $\alpha\gg1$：集中在 $1/2$，强制大量 midpoint-like 样本。

平均 $\lambda$ 永远是 $1/2$，所以不能用 $\mathbb E\lambda$ 区分强度；应看 variance、$\lambda(1-\lambda)$、实际距离和 target entropy。

### 3.2 `max(lambda,1-lambda)` 改变了 Distribution

有些实现把

$$
\lambda' = \max(\lambda,1-\lambda)
$$

以便第一个样本权重不小于 $1/2$。若同时交换配对顺序与 target，unordered mixed point 可以等价；若只改 $\lambda$ 不交换来源，或有 source-specific augmentation/mask，则合同改变。必须记录。

## 四、从 ERM 到 Vicinal Risk

经验分布是

$$
\widehat P_n=\frac1n\sum_{i=1}^n\delta_{(x_i,y_i)}.
$$

ERM 最小化

$$
\widehat R(\theta)
=\frac1n\sum_i\ell(f_\theta(x_i),y_i).
$$

Mixup 定义一个由 pair $(i,j)$ 与 $\lambda$ 诱导的 vicinal distribution $Q_{\rm mix}$，优化

$$
\boxed{
R_{\rm mix}(\theta)
=\mathbb E_{i,j,\lambda}
\left[
\ell\big(f_\theta(\lambda x_i+(1-\lambda)x_j),
\lambda y_i+(1-\lambda)y_j\big)
\right].
}
$$

它不是原 empirical risk 的 unbiased estimator；它有意改变训练分布和监督目标。

## 五、Cross-Entropy 对 Mixed Label 的精确线性

固定 mixed input 上的 prediction $p=f_\theta(\widetilde x)$。Cross-entropy 对 target 线性：

$$
\begin{aligned}
H(\widetilde y,p)
&=-\sum_k\big(\lambda y_{i,k}+(1-\lambda)y_{j,k}\big)\log p_k\\
&=\lambda H(y_i,p)+(1-\lambda)H(y_j,p).
\end{aligned}
$$

注意右侧两个 losses 都在 **同一个 mixed prediction $p(\widetilde x)$** 上计算。它不等于

$$
\lambda H(y_i,p(x_i))+(1-\lambda)H(y_j,p(x_j)).
$$

### 5.1 它约束 Probabilities，不直接约束 Logits 线性

在无限容量、对每个 mixed point 可独立拟合时，最优 prediction 倾向 $p(\widetilde x)=\widetilde y$。但这不等于

$$
z(\widetilde x)=\lambda z(x_i)+(1-\lambda)z(x_j),
$$

也不自动给 hidden features 的 affine equality。

## 六、完整手算：二维输入、三分类 Target

取

$$
x_1=(2,0),\qquad x_2=(0,4),\qquad \lambda=0.25.
$$

则

$$
\widetilde x=0.25(2,0)+0.75(0,4)=(0.5,3).
$$

令 $y_1=e_1=(1,0,0)$、$y_2=e_3=(0,0,1)$，则

$$
\widetilde y=(0.25,0,0.75).
$$

若模型在 $\widetilde x$ 上输出

$$
p=(0.2,0.1,0.7),
$$

则

$$
\begin{aligned}
H(\widetilde y,p)
&=-0.25\log0.2-0.75\log0.7\\
&\approx0.66987.
\end{aligned}
$$

同样也可写成

$$
0.25H(e_1,p)+0.75H(e_3,p).
$$

## 七、几何：Chord 是归纳偏置，不是事实

Mixed point 到 endpoint 的位移是

$$
\widetilde x-x_i=(1-\lambda)(x_j-x_i),
$$

所以

$$
\|\widetilde x-x_i\|=(1-\lambda)\|x_j-x_i\|
$$

对任意绝对齐次 norm 成立。Mixup 在数据点之间的 chord 上采样并规定 target 沿 chord 线性变化。

### 7.1 Manifold Intrusion

某条 chord interior 可能：

- 接近第三类真实样本，却被分配两类混合 target；
- 离开自然图像/语音/离散序列支持；
- 跨越物理不可行区域；
- 破坏对象拓扑、长度或 padding 语义。

因此“vicinal sample 可计算”不等于“语义有效”。

### 7.2 为什么有时仍有用

即使 mixed point 不是真实样本，它仍可作为函数空间约束：限制训练点之间出现极端高置信度边界。是否改善真实 risk 是经验问题，不由 chord 几何单独保证。

## 八、Manifold Mixup 的算子合同

把网络拆成 prefix 与 suffix：

$$
h_k=g_{\theta,\le k}(x),
\qquad
f_\theta(x)=s_{\theta,>k}(h_k).
$$

对一对样本，计算

$$
h_i=g_{\le k}(x_i),\qquad h_j=g_{\le k}(x_j),
$$

再构造

$$
\widetilde h=\lambda h_i+(1-\lambda)h_j,
\qquad
\widetilde y=\lambda y_i+(1-\lambda)y_j,
$$

并优化

$$
\ell(s_{>k}(\widetilde h),\widetilde y).
$$

Layer $k$ 可以固定或随机采样；这会改变被约束的 representation family。

## 九、Hidden Mix 的反向传播

设 suffix 对 mixed hidden state 的 cotangent 为

$$
g=\frac{\partial L}{\partial\widetilde h}.
$$

由线性 mixing，

$$
\boxed{
\frac{\partial L}{\partial h_i}=\lambda g,
\qquad
\frac{\partial L}{\partial h_j}=(1-\lambda)g.
}
$$

若 prefix parameters 共享，则

$$
\nabla_{\theta_{\le k}}L
=\lambda J_{g_i,\theta}^\mathsf Tg
+(1-\lambda)J_{g_j,\theta}^\mathsf Tg.
$$

所以 Manifold Mixup 不只改变 suffix 的训练点，也把同一 suffix gradient 以两条权重路径送回 prefix。

## 十、“Manifold”一词的边界

Hidden representation $h_k(x)$ 是 learned coordinate。两点的欧氏 chord

$$
\lambda h_k(x_i)+(1-\lambda)h_k(x_j)
$$

未必：

- 位于 $h_k(\mathcal X)$ 的 image 上；
- 是某个语义 geodesic；
- 对 reparameterization invariant；
- 保持 object identity 或 causal factors。

原论文在特定理想条件下分析 representation flattening，并给出经验结果；不能把命名当作真实流形定理。

## 十一、Mixup 与 Label Smoothing 的精确可交换部分

定义统一 prior $u$ 的 smoothing map

$$
S_\epsilon(y)=(1-\epsilon)y+\epsilon u.
$$

则

$$
\begin{aligned}
S_\epsilon(\lambda y_i+(1-\lambda)y_j)
&=(1-\epsilon)\{\lambda y_i+(1-\lambda)y_j\}+\epsilon u\\
&=\lambda S_\epsilon(y_i)+(1-\lambda)S_\epsilon(y_j).
\end{aligned}
$$

所以在 **同一固定 prior、同一 $\epsilon$** 下，target smoothing 与 target mixing 代数可交换。

但完整训练方法不因此可交换：

- Mixup 还改变输入/hidden state；
- class-dependent prior 可能随 source label 改变；
- augmentation、normalization 与 pairing order 会不同；
- 两者叠加提高 target entropy，可能过度 regularize。

## 十二、不同任务的 Label Geometry

### 12.1 Multiclass Classification

Simplex convex combination天然合法，但语义是否线性仍需验证。

### 12.2 Regression

数值 target 可直接插值，但若输入—输出关系非线性或有 discontinuity，线性 target 是额外假设。

### 12.3 Multi-Label

每个 component 可混成 $[0,1]$ target，但 BCE 与互斥 softmax 不同；class co-occurrence 可能不闭合于凸组合。

### 12.4 Segmentation / Detection

需要说明 spatial alignment、box assignment、mask mixing 和 area-based $\lambda$。单个 scalar $\lambda$ 未必等于实际可见对象比例。

### 12.5 Tokens / Graphs / Sets

离散结构通常不能在 raw index 上线性插值；应在 embedding、probability、span 或 structure-aware operator 中定义，同时处理 length/padding/edge validity。

## 十三、Pairing 与 Augmentation Order

至少区分：

1. raw samples 先独立 augmentation，再 Mixup；
2. 先 Mixup，再对 mixed object augmentation；
3. 同一个 augmentation 参数作用于两端；
4. class-aware 或 nearest-neighbor pairing；
5. 允许 self-pair 还是 derangement。

这些会改变 $Q_{\rm mix}$，不是无关紧要的 data-loader 细节。

## 十四、Normalization、Mask 与系统边界

### BatchNorm

若在 input Mixup 后进入 BatchNorm，batch statistics 来自 mixed distribution。Manifold Mixup 若发生在某个 BN 前后，所约束对象和 running state 都不同。

### LayerNorm

没有 running state，但 hidden mixing 前后做 LayerNorm 一般不交换：

$$
\operatorname{LN}(\lambda h_i+(1-\lambda)h_j)
\ne
\lambda\operatorname{LN}(h_i)+(1-\lambda)\operatorname{LN}(h_j).
$$

### Padding / Attention Mask

两个不同长度序列 mixing 时，必须定义 valid positions、padding embedding、attention edges 与 loss mask；不能只混 hidden tensor 而沿用任一来源 mask。

### Distributed Pairing

Local-rank permutation 只在每个 replica 内配对；global pairing 需通信或可复现 index exchange。两者的 class/distance distribution 不同。记录 seed、permutation、$\lambda$ shape 和是否跨 replicas。

### Cost

Input Mixup 通常增加少量 elementwise cost；Manifold Mixup 可能需要同时保留两路 prefix activations、改变 compilation graph 或增加通信。必须测 peak memory 和 throughput，不能只引用“几行代码”。

## 十五、公平实验的三条轨道

### Natural Protocol

每种方法用推荐 pairing、$\alpha$、layer distribution 和 tuning，回答最佳可达表现。

### Matched Strength

匹配平均 $\lambda(1-\lambda)$、mixed distance 或 target entropy，回答类似扰动预算下的差异。

### Semantic Validity

按同类/异类、near/far pair、modality-valid constraint 分层，测 mixed point 的第三类 intrusion、human/teacher consistency 或任务可行性。

所有轨道固定或匹配：architecture、optimizer、training steps、augmentation budget、data order、seed、parameter count 与 tuning compute。报告 accuracy/NLL/Brier、calibration、noise/shift robustness、train loss、time、memory 和 classwise effect。

## 十六、常见误区

1. **“$\mathbb E\lambda=1/2$ 所以所有 $\alpha$ 强度相同”**：variance 与 interior mass 不同；
2. **“输入和 label 可用不同 $\lambda$”**：这改变监督语义；
3. **“Mixed target CE 等于两个原样本 loss”**：prediction 必须是在同一 $\widetilde x$ 上；
4. **“Manifold Mixup 一定在 data manifold 上”**：hidden chord 仍可能离开 representation image；
5. **“Mixup 证明模型全局线性”**：只在采样 chords 与 objective 下施加偏置；
6. **“与 Label Smoothing 可交换，所以整套训练可交换”**：只证明 target affine map 的代数；
7. **“随机 pairing 是实现细节”**：它定义 vicinal distribution；
8. **“无额外参数就是零成本”**：memory、routing 与 distributed pairing 仍有成本。

## 十七、图：Chord、Beta 与三份实现合同

先看图回答：$\lambda=0.25$ 为什么把 $(2,0)$ 与 $(0,4)$ 混成 $(0.5,3)$？为什么不同 $\alpha$ 虽有相同 $\mathbb E\lambda$，却给出不同 interior strength？为什么 hidden mix 的名称不能替代语义证明？

![[00-知识库管理/_assets/figures/neural-networks/fig-mixup-vicinal-geometry-v2.svg|880]]

> [!figure] 图注与来源
> **对象与结论**：左栏给同一 $\lambda$ 的 input/target toy；中栏画出 $\mathbb E[\lambda(1-\lambda)]$ 随 $\alpha$ 增大而趋近 $1/4$；右栏分开 input、hidden、normalization 与 distributed pairing 合同。
>
> **来源**：Mixup 定义与原始经验参考[[S-2018-Zhang-Mixup]]；hidden interpolation 与原范围 representation 结果参考[[S-2019-Verma-Manifold-Mixup]]。自绘 SVG 由[[plot_regularization_interfaces_v2.py]]确定性生成。
>
> **怎样读图**：先沿左栏 chord 检查坐标和 target，再用中栏区别 endpoint-heavy 与 midpoint-heavy sampling，最后逐项核对右栏的随机/系统变量。
>
> **图没有证明什么**：图不证明 chord interior 是自然样本、hidden chord 是真实 geodesic、Mixup 必然改善 robustness/calibration，也不证明三种实现具有相同计算成本。

## 十八、最小验收

1. 写出 Mixup 的完整概率合同；
2. 推导 symmetric Beta 的 mean、variance 与 $\mathbb E[\lambda(1-\lambda)]$；
3. 把目标写成 vicinal risk；
4. 证明 mixed-target CE 的线性分解；
5. 复算二维三分类 toy；
6. 推导 hidden mix 的 backward split；
7. 构造 manifold intrusion 反例；
8. 证明与 fixed-prior Label Smoothing 的 target-level 可交换式；
9. 审计 augmentation、pairing、normalization、padding 与 distributed RNG；
10. 设计 natural/matched-strength/semantic-validity 三轨实验。
