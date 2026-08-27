---
type: derivation
status: draft
area: [neural-networks/regularization, label-smoothing, cross-entropy, calibration, target-bias]
aliases: [Label Smoothing, Soft Target Bias]
node_id: NN-61
prerequisites: ["[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[交叉熵与 KL 散度]]", "[[损失、总体风险与经验风险]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
related: ["[[Mixup、Manifold Mixup 与插值正则]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]", "[[Covariate、Label 与 Concept Shift]]"]
sources: ["[[S-2016-Szegedy-Label-Smoothing]]", "[[S-2019-Muller-Label-Smoothing]]", "[[S-2026-PyTorch-CrossEntropy-Label-Smoothing]]"]
exercises: ["[[习题 - Label Smoothing、置信度与目标偏置]]"]
solutions: ["[[解答 - Label Smoothing、置信度与目标偏置]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-label-smoothing-target-bias-v2.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Label Smoothing、置信度与目标偏置

> [!abstract] 本章主问题
> Label Smoothing 不是“让模型谦虚一点”的口号，而是直接替换监督 target。对 uniform smoothing，soft target 为 $t_\epsilon=(1-\epsilon)e_y+\epsilon u$；交叉熵精确分解为 hard-label fit 与 prior cross-entropy。它让 logit optimum 从无限 margin 变为有限 margin，同时把 population optimum 从真实条件分布 $\eta(x)$ 推向 $(1-\epsilon)\eta(x)+\epsilon u$。经验上它可能抵消过度置信，但“置信度下降”“概率校准”“抗标签噪声”“不确定性更可靠”是四个不同命题。

## 一、学习目标

读完本节，你应能：

1. 区分含 true class 与排除 true class 的两种 smoothing convention；
2. 把 smoothed cross-entropy 精确分解为两项；
3. 推导 logits gradient $p-t_\epsilon$；
4. 计算 uniform smoothing 下的有限最优 logit margin；
5. 推导 population target bias；
6. 区分 Label Smoothing、confidence penalty 与 temperature scaling；
7. 解释它与 symmetric label noise 的条件性联系；
8. 区分低置信度、校准、aleatoric/epistemic uncertainty；
9. 审计 class weights、ignore mask、reduction 与大词表实现；
10. 设计 accuracy—NLL—calibration—distillation 的公平验收。

## 二、先锁定 Target Contract

有 $K$ 个互斥类别，真实 class index 为 $y$，one-hot vector 为

$$
e_y\in\Delta^{K-1},
$$

其中 $\Delta^{K-1}$ 是 probability simplex。选一个 label prior

$$
u\in\Delta^{K-1},
$$

以及 smoothing strength $\epsilon\in[0,1]$。本节默认的 **inclusive convention** 是

$$
\boxed{t_\epsilon=(1-\epsilon)e_y+\epsilon u.}
$$

若 $u_k=1/K$，则

$$
t_{\epsilon,y}=1-\epsilon+\frac{\epsilon}{K},
\qquad
t_{\epsilon,k}=\frac{\epsilon}{K}\quad(k\ne y).
$$

> [!warning] $\epsilon$ 的名字相同，公式未必相同
> 另一常见 convention 直接规定 true class 为 $1-\epsilon_{\rm ex}$、每个错误类为 $\epsilon_{\rm ex}/(K-1)$。它与 inclusive-uniform convention 的参数换算是
> $$
> \epsilon=\frac{K}{K-1}\epsilon_{\rm ex}.
> $$
> 比较论文或库时必须先换成同一 target vector，不能只比较参数名。若还要求 inclusive 形式中的 $\epsilon\in[0,1]$，则该参数化只能覆盖 $\epsilon_{\rm ex}\le (K-1)/K$；更大的 exclude-true smoothing 虽仍给出合法 target，却不能写成上述合法区间内的 inclusive convex mixture。

## 三、Smoothed Cross-Entropy 的精确分解

模型 logits 为 $z\in\mathbb R^K$，预测概率

$$
p_k=\frac{e^{z_k}}{\sum_j e^{z_j}}.
$$

对 probability target $t$，cross-entropy 是

$$
H(t,p)=-\sum_{k=1}^K t_k\log p_k.
$$

由于它对第一个参数 $t$ 线性，

$$
\begin{aligned}
H(t_\epsilon,p)
&=H((1-\epsilon)e_y+\epsilon u,p)\\
&=(1-\epsilon)H(e_y,p)+\epsilon H(u,p)\\
&=-(1-\epsilon)\log p_y-\epsilon\sum_ku_k\log p_k.
\end{aligned}
$$

若 $u$ 是 uniform distribution，

$$
H(u,p)=H(u)+\operatorname{KL}(u\|p)
=\log K+\operatorname{KL}(u\|p).
$$

因此忽略与参数无关的 $\epsilon\log K$ 后，Label Smoothing 添加的是

$$
\epsilon\operatorname{KL}(u\|p),
$$

不是 $\operatorname{KL}(p\|u)$，也不是直接最大化 predictive entropy $H(p)$。

### 3.1 为什么 KL 方向重要

- $\operatorname{KL}(u\|p)$ 在任何 $p_k\to0$ 且 $u_k>0$ 时发散，阻止某类概率被压到严格 0；
- $\operatorname{KL}(p\|u)=\log K-H(p)$ 是 confidence/entropy penalty 的一种写法，权重由当前 $p$ 决定；
- 二者在 uniform 附近有局部联系，但全局梯度、边界行为和最优点不同。

## 四、Logit Gradient：Target 直接进入误差信号

Softmax cross-entropy 的标准结果是

$$
\boxed{\frac{\partial H(t,p)}{\partial z_j}=p_j-t_j.}
$$

于是 Label Smoothing 给

$$
\nabla_zL=p-t_\epsilon.
$$

对 true class：

$$
\frac{\partial L}{\partial z_y}
=p_y-\left(1-\epsilon+\epsilon u_y\right).
$$

对错误类：

$$
\frac{\partial L}{\partial z_k}=p_k-\epsilon u_k.
$$

Hard target 会在 $p_y<1$ 时持续推动 $z_y-z_k$ 增大；smoothed target 在 $p=t_\epsilon$ 时所有 logit gradients 同时为 0。

## 五、为什么最优 Logit Margin 变成有限值

若模型能在该样本上精确拟合 target，则 $p^*=t_\epsilon$。对 uniform prior，任意错误类 $k$ 与 true class 的最优 logit difference 是

$$
z_y-z_k
=\log\frac{p_y^*}{p_k^*}
=\log\frac{1-\epsilon+\epsilon/K}{\epsilon/K}
=\boxed{\log\frac{K-(K-1)\epsilon}{\epsilon}}.
$$

只要 $0<\epsilon<1$，margin 有限；当 $\epsilon\to0^+$ 时它才发散。

## 六、完整手算：$K=3,\epsilon=0.1$

令 $y=1$、$u=(1/3,1/3,1/3)$。则

$$
t_\epsilon
=0.9(1,0,0)+0.1(1/3,1/3,1/3)
=\left(\frac{14}{15},\frac1{30},\frac1{30}\right).
$$

即

$$
t_\epsilon\approx(0.93333,0.03333,0.03333).
$$

最优 true-vs-wrong margin 为

$$
\log\frac{14/15}{1/30}=\log28\approx3.33220.
$$

若当前 $p=(0.8,0.1,0.1)$，则

$$
\nabla_zL
=p-t_\epsilon
\approx(-0.13333,0.06667,0.06667),
$$

而 hard target 的 gradient 是 $(-0.2,0.1,0.1)$。Smoothed target 减弱继续拉大 margin 的驱动力，但没有让梯度整体乘一个常数：各 class 的 offset 被直接改变。

Cross-entropy 为

$$
L=-\frac{14}{15}\log0.8-\frac1{30}\log0.1-\frac1{30}\log0.1
\approx0.36177.
$$

## 七、Population Optimum：它确实引入 Target Bias

令真实 conditional class distribution 为

$$
\eta(x)=\big(P(Y=1\mid X=x),\ldots,P(Y=K\mid X=x)\big).
$$

对 $Y\mid X=x$ 取期望，平均 smoothed target 是

$$
\begin{aligned}
r_\epsilon(x)
&=\mathbb E[t_\epsilon(Y)\mid X=x]\\
&=(1-\epsilon)\eta(x)+\epsilon u.
\end{aligned}
$$

Cross-entropy 对目标分布是 strictly proper，因此在无限函数类和精确优化下，population optimum 是

$$
\boxed{p^*(x)=r_\epsilon(x),}
$$

不是原始 $\eta(x)$。

### 7.1 Uniform Smoothing 保持 Argmax，但收缩概率差

若 $u$ uniform 且 $\epsilon<1$，

$$
r_{\epsilon,i}-r_{\epsilon,j}
=(1-\epsilon)(\eta_i-\eta_j),
$$

所以 class ranking 与 Bayes argmax 保持，但 probability gaps 收缩。非 uniform prior 则可能改变 ranking。

### 7.2 能否反变换

若 $u,\epsilon$ 已知，形式上

$$
\eta(x)=\frac{r_\epsilon(x)-\epsilon u}{1-\epsilon}.
$$

但有限样本模型的 $p$ 未必恰在该 affine image 内，反变换可能出现负值或大于 1，且会放大 estimation error。它不是免费“去平滑”。

## 八、与 Symmetric Label Noise 的条件性联系

Inclusive uniform smoothing 等价于这样的 target randomization 的条件期望：

- 以概率 $1-\epsilon$ 保留真实 one-hot；
- 以概率 $\epsilon$ 从 $K$ 个类均匀重新抽一个 label，包括可能抽回 true class。

Exclude-true convention 则对应以概率 $\epsilon_{\rm ex}$ 强制翻到某个错误类。两种 transition matrix 不同。

> [!warning] “像 label noise”不等于“自动抗 label noise”
> 若真实 annotation noise 是 class-dependent、instance-dependent 或 asymmetric，uniform transition 未必匹配；过度 smoothing 还会增加 bias。抗噪必须在声明的 corruption model 下验证。

## 九、置信度、校准与不确定性不要混账

### 9.1 Confidence

Maximum softmax probability 或 entropy 是一次 prediction 的数值性质。Label Smoothing 往往压缩 logit gap，因此可降低 confidence。

### 9.2 Calibration

Calibration 要求在预测 confidence 为 $c$ 的样本群体中，实际正确率约为 $c$。它是 prediction—outcome 的 joint property，必须用 held-out reliability、NLL、Brier 和有偏差控制的 estimator 检查。

在理想 population 分析中，Label Smoothing 的 optimum 是 $r_\epsilon\ne\eta$，所以它对原始 label probability 有结构性偏置；经验上它仍可能改善 calibration，因为有限深网的 hard-label solution 常过度置信。二者不矛盾：一个是目标偏置，另一个是现实误差的净结果。

### 9.3 Uncertainty

低 confidence 不自动区分 aleatoric uncertainty、epistemic uncertainty、distribution shift 或人为 target smoothing。$\epsilon$ 是训练超参数，不是 posterior uncertainty。

## 十、与 Knowledge Distillation 的边界

Teacher logits 的非 top-class relative structure 可携带 instance similarity。Label Smoothing 鼓励错误类 targets 接近同一 prior，可能压缩这些差异；Müller et al. 在其设置下观察到 smoothed teacher 的 distillation 变差。

但结论不能升级为“teacher 永远不能 smoothing”：

- teacher/student capacity、temperature、task 与 representation 都会改变结果；
- hard teacher accuracy、teacher calibration 与 student transfer 是不同指标；
- 应做 teacher-only、student-only 和 teacher→student 三段实验。

## 十一、非 Uniform 与结构化 Smoothing

一般 prior $u$ 可取：

- empirical class prior；
- class-dependent confusion distribution；
- taxonomy/semantic similarity；
- teacher distribution。

这时 target 仍为 $(1-\epsilon)e_y+\epsilon u_y$，但 $u$ 可能依赖真实 class 或 input。必须说明：

1. $u$ 是固定 prior、transition row 还是 learned teacher；
2. 它是否由 validation/test 信息估计；
3. 是否改变 Bayes argmax；
4. 是否与 class weighting 重复补偿 imbalance。

## 十二、实现合同

### 12.1 Index Target 与 Probability Target

Framework 可直接接受 class index 加 `label_smoothing`，也可接受完整 probability target。二者必须用小 logits 对齐 loss 和 gradient；当前 PyTorch 文档说明 probability target 的合法性由调用者负责。

### 12.2 Class Weight

Class weight 可能按 target component 加权，也可能只按 hard index 取权；不同实现下“先 smooth 后 weight”与“先 weight 后 smooth”不一定相同。不要仅凭参数名推断。

### 12.3 Ignore / Padding

Sequence task 中 padding positions 应在 target 构造、loss numerator 和 denominator 三处一致排除。不能把 smoothing mass 分给词表外 padding class，也不能让 all-ignored batch 产生除零。

### 12.4 Large Vocabulary

Uniform term需要全类别 $\sum_k\log p_k/K$。若使用 sampled/adaptive output，必须说明是在 exact full distribution 还是 proxy objective 上 smoothing；不能假设只改 target index 就免费实现完整 uniform CE。

### 12.5 Precision

不要显式先算 softmax 再取 log；继续使用稳定 log-softmax/fused cross-entropy。很小 $\epsilon/K$ 在低精度下也需检查 representability 和 reduction accumulation。

## 十三、公平验收协议

至少比较：

1. $\epsilon=0$ baseline；
2. 多个 $\epsilon$；
3. inclusive/exclusive convention 对齐到相同 target；
4. uniform 与 task-specific prior；
5. 必要时 temperature scaling post-hoc baseline。

固定或匹配：architecture、optimizer、LR schedule、weight decay、augmentation、训练步数、early stopping、seed/data order 和 tuning budget。

同时报告：

- train/test CE、accuracy 与 margin；
- NLL、Brier、reliability/ECE estimator；
- clean、label-noise 与预声明 shift；
- teacher/student distillation；
- classwise 指标和 rare-class effect。

## 十四、常见误区

1. **“$\epsilon=0.1$ 就表示 true class 是 0.9”**：inclusive uniform 下是 $0.9+0.1/K$；
2. **“它等价最大化 entropy”**：默认分解是 $\operatorname{KL}(u\|p)$，不是 $\operatorname{KL}(p\|u)$；
3. **“低 confidence 就是校准”**：校准需要 outcome-conditioned evaluation；
4. **“不改变 argmax，所以没有 bias”**：概率目标仍被 affine 收缩；
5. **“是 symmetric noise，所以自动抗真实噪声”**：真实 transition 可能不同；
6. **“统一 $\epsilon$ 可跨数据集复制”**：$K$、label quality、model capacity 与其他正则共同决定强度；
7. **“概率小一点就是 epistemic uncertainty”**：训练 target bias 不识别知识不确定性。

## 十五、图：Target、Margin 与证据边界

先看图回答：$K=3,\epsilon=0.1$ 时为什么 true target 是 $0.9333$ 而不是 $0.9$？为什么最优 margin 是 $\log28$？为什么 confidence 下降不能直接推出 calibration 或 uncertainty 改善？

![[00-知识库管理/_assets/figures/neural-networks/fig-label-smoothing-target-bias-v2.svg|880]]

> [!figure] 图注与来源
> **对象与结论**：左栏显示 inclusive uniform target；中栏连接 loss 分解与有限 logit margin；右栏把 target bias、calibration、label noise 与 distillation 分账。数值由本节公式直接计算。
>
> **来源**：方法合同参考[[S-2016-Szegedy-Label-Smoothing]]；表示、校准和蒸馏边界参考[[S-2019-Muller-Label-Smoothing]]；当前接口参考[[S-2026-PyTorch-CrossEntropy-Label-Smoothing]]。自绘 SVG 由[[plot_regularization_interfaces_v2.py]]确定性生成。
>
> **怎样读图**：先验证左栏 target sum 为 1，再由概率比读出中栏 margin，最后把右栏每个经验命题还原到独立指标。
>
> **图没有证明什么**：图不证明 smoothing 必然改善 accuracy、calibration、noise robustness 或 distillation，也不把低 confidence 解释为 Bayesian uncertainty。

## 十六、最小验收

1. 写出并换算两种 smoothing convention；
2. 推导 smoothed CE 的凸组合与 KL 方向；
3. 推导 $\nabla_zL=p-t_\epsilon$；
4. 完整复算 $K=3,\epsilon=0.1$ toy；
5. 推导有限 optimal margin；
6. 推导 population optimum $(1-\epsilon)\eta+\epsilon u$；
7. 解释 uniform 情形 argmax 保持与 probability bias 并存；
8. 区分 confidence、calibration 与 uncertainty；
9. 审计 class weight、ignore/reduction 与 full-vocabulary cost；
10. 设计含 distillation 和 shift 的公平实验。
