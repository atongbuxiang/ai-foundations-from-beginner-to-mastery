---
type: concept
status: draft
area: [math/information-theory, math/statistical-learning, ai/losses, ai/generative-models]
aliases: [交叉熵与相对熵, Cross-Entropy and KL Divergence, 相对熵]
prerequisites: ["[[自信息、熵与编码长度]]", "[[联合熵、条件熵与链式法则]]", "[[最大似然估计与 MAP]]", "[[常用连续分布与指数族]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[互信息与依赖性]]", "[[变分推断、ELBO 与证据分解]]", "[[f-散度、Bregman 散度与概率度量]]", "[[多元高斯分布]]"]
sources: ["Kullback-Leibler-1951-Information-Sufficiency", "MIT-6.441-Chapter-1-Information-Measures", "Stanford-EE376A-Lecture-Notes", "Cover-Thomas-Elements-Information-Theory", "Su-8512-Gaussian-Distances", "Su-9039-GlobalPointer-KL"]
created: 2026-08-19
updated: 2026-08-23
---

# 交叉熵与 KL 散度

> [!abstract] 本章主问题
> 若数据真正来自 $P$，却用模型 $Q$ 的概率分配来编码，平均长度是 cross-entropy $H(P,Q)=E_P[-\log q(X)]$；它精确分解为 $H(P)+D_{\rm KL}(P\|Q)$。KL 是因分布失配多付出的平均 log-likelihood ratio，非负且相等仅在分布几乎处处相同，但它不对称、不是 metric，支撑不兼容时可为无穷。固定 target 时最小化经验 cross-entropy 就是最大化 likelihood；一旦加入 label smoothing、class weight、focal factor、temperature 或非概率 logits，目标和解释都必须重新写明。

## 学习目标

完成本节后，你应当能够：

1. 区分 entropy、cross-entropy、KL 和单样本 NLL；
2. 写清 $H(P,Q)$ 的 expectation 在 $P$ 下，而对数中使用 $q$；
3. 推导 $H(P,Q)=H(P)+D_{\rm KL}(P\|Q)$；
4. 用 log inequality 证明 Gibbs inequality 与 equality condition；
5. 判断 KL 何时有限，解释 absolute continuity/support mismatch；
6. 用反例证明 KL 不对称且不满足 triangle inequality；
7. 从 empirical cross-entropy 推导 MLE 与 misspecified KL projection；
8. 从 logits 稳定推导 softmax cross-entropy、gradient 与 Hessian；
9. 推导 Bernoulli、categorical、univariate/multivariate Gaussian KL；
10. 审计蒸馏、VAE、R-Drop/GlobalPointer、label smoothing 与 numerical clipping 中被改变的对象。

> [!question] 初学者读完必须能回答
> 1. self-information、entropy、cross-entropy、单样本 NLL 与 KL 的 expectation 分别在哪个分布下？
> 2. 为什么 $H(P,Q)=H(P)+D_{\rm KL}(P\|Q)$，固定 $P$ 时优化了哪一项？
> 3. Gibbs inequality 如何证明 KL 非负，等号应理解为 pointwise 还是 almost everywhere？
> 4. $P\ll Q$ 与 support coverage 为什么决定 $D_{\rm KL}(P\|Q)$ 是否可能有限？
> 5. KL 为什么不对称、不是 metric，交换方向会改变哪些区域的权重？
> 6. 经验 cross-entropy 与 MLE、总体 KL projection 和泛化误差怎样分层？
> 7. label smoothing、class weight、temperature、clipping 与非概率 logits 会怎样改变原始编码解释？

## 阅读前检查

- [[自信息、熵与编码长度]]：entropy、ideal code length、Kraft；
- [[联合熵、条件熵与链式法则]]：conditional distribution 与 chain rule；
- [[最大似然估计与 MAP]]：likelihood、empirical NLL 与 model misspecification；
- [[多元高斯分布]]：Gaussian density、trace、log-det 与 Cholesky。

## 零、四个对象先摆在同一张表上

设 $P,Q$ 是同一离散 alphabet $\mathcal X$ 上的 distributions，PMF 分别为 $p,q$。

| 对象 | 定义 | expectation / realization | 核心问题 |
|---|---|---|---|
| self-information under $Q$ | $-\log q(x)$ | 单个 $x$ | 模型 $Q$ 对这个结果有多惊讶？ |
| entropy | $H(P)=E_P[-\log p(X)]$ | $X\sim P$ | 用真实分布自身编码的平均理想长度？ |
| cross-entropy | $H(P,Q)=E_P[-\log q(X)]$ | $X\sim P$ | 数据来自 $P$，却用 $Q$ 编码的平均长度？ |
| KL divergence | $D_{\rm KL}(P\|Q)=E_P[\log(p/q)]$ | $X\sim P$ | 相对使用 $P$，使用 $Q$ 多付出多少？ |

最容易写错的是 expectation 的方向：外部权重来自 $P$，log 中被评价的是 $Q$。

先用下图回答一个视觉问题：**真实分布的加权、模型码长、KL 失配项和 KL 方向为什么必须同时标清？**

![[00-知识库管理/_assets/figures/information-theory/fig-cross-entropy-kl-v2.svg|880]]

> [!figure] 图 10.6.3｜Cross-entropy 权重、KL 分解与方向性
> A 用成对柱形区分产生数据的 $P$ 与提供码长的 $Q$；B 将 $H(P,Q)$ 拆为真实 entropy 与模型失配 KL；C 用双峰 $P$ 和单峰 $Q$ 示意 $D_{\rm KL}(P\|Q)$ 与 $D_{\rm KL}(Q\|P)$ 的加权区域不同。来源：独立绘制；生成脚本：[[plot_information_foundations_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 对每个类别用 $p_i$ 加权 $-\log q_i$；B 在固定 $P$ 时把 $H(P)$ 看成不可由 $Q$ 优化的常数；C 先读 KL 第一个参数决定 expectation，再检查第二个参数是否在第一参数的 support 上给出正概率。

**适用边界（图没有证明什么）。** 柱形与曲线只示意离散权重和常见优化倾向，不构成所有模型族中的 mode-covering/mode-seeking 定理；KL 可以无穷且不满足对称与三角不等式；经验 NLL 下降不自动证明总体 KL、校准、OOD 表现或生成样本质量同步改善。

## 一、交叉熵：用错误模型给真实数据编码

定义离散 cross-entropy：

$$
\boxed{
H_b(P,Q)
=-\sum_xp(x)\log_bq(x)
=E_{X\sim P}[-\log_bq(X)].
}
$$

若存在 $x$ 使 $p(x)>0$ 但 $q(x)=0$，则

$$
H(P,Q)=+\infty.
$$

模型 $Q$ 没为真实可能结果分配任何码字/概率，这是 support failure，而不是用很小 epsilon 就能从理论上忽略的问题。

### 1.1 手算例子

真实硬币 $P=\operatorname{Bernoulli}(0.8)$，模型使用 $Q=\operatorname{Bernoulli}(0.6)$。以 bits 计：

$$
H_2(P,Q)
=-0.8\log_20.6-0.2\log_20.4
\approx0.854.
$$

真实 entropy 是

$$
H_2(P)=h_2(0.8)\approx0.722.
$$

差值约 $0.132$ bits/sample，正是 $D_{\rm KL}^{(2)}(P\|Q)$。

## 二、KL divergence 与基本分解

定义

$$
\boxed{
D_{\rm KL}(P\|Q)
=\sum_xp(x)\log\frac{p(x)}{q(x)}
=E_P\left[\log\frac{p(X)}{q(X)}\right].
}
$$

约定：

$$
0\log\frac0q=0,
\qquad
p\log\frac p0=+\infty\quad(p>0).
$$

直接展开：

$$
\begin{aligned}
D_{\rm KL}(P\|Q)
&=\sum_xp(x)\log p(x)-\sum_xp(x)\log q(x)\\
&=-H(P)+H(P,Q).
\end{aligned}
$$

所以

$$
\boxed{H(P,Q)=H(P)+D_{\rm KL}(P\|Q).}
$$

当 target $P$ 固定时，$H(P)$ 与模型参数无关，故最小化 cross-entropy 等价于最小化 $D_{\rm KL}(P\|Q)$。若 target 本身也随参数变化，这个“常数项可丢”不再成立。

### 2.1 continuous/general measure 版本

若 $P$ 对 $Q$ 绝对连续，写 $P\ll Q$，Radon–Nikodym derivative 为 $dP/dQ$，则

$$
D_{\rm KL}(P\|Q)
=\int\log\left(\frac{dP}{dQ}\right)dP.
$$

若 $P\not\ll Q$，定义 KL 为 $+\infty$。有 density 时才简写为

$$
\int p(x)\log\frac{p(x)}{q(x)}dx.
$$

这个版本说明 KL 比“两个数组代公式”更根本：先要有同一可测空间上的 probability measures。

## 三、Gibbs inequality：为什么 KL 非负

我们用基本不等式

$$
\log t\le t-1,
\qquad t>0,
$$

且等号当且仅当 $t=1$。

假设先有 $p(x)>0\Rightarrow q(x)>0$。对每个 $p(x)>0$，令 $t=q(x)/p(x)$：

$$
-\log\frac{q(x)}{p(x)}
\ge1-\frac{q(x)}{p(x)}.
$$

乘 $p(x)$ 并求和：

$$
\begin{aligned}
D_{\rm KL}(P\|Q)
&=-\sum_xp(x)\log\frac{q(x)}{p(x)}\\
&\ge\sum_x[p(x)-q(x)]\\
&=1-1=0.
\end{aligned}
$$

因此

$$
\boxed{D_{\rm KL}(P\|Q)\ge0.}
$$

等号要求对所有 $p(x)>0$ 有 $q(x)/p(x)=1$。再结合归一化，得到 $P=Q$（更一般地 $P$-almost surely）。若 support mismatch，KL 已是 $+\infty$，仍满足非负性。

### 3.1 直接推论

$$
H(P,Q)\ge H(P),
$$

等号当且仅当 $P=Q$。真实分布自身给出的 ideal code，在平均意义上不能被错误分布系统性击败。

> [!note] 不是说每个样本都更长
> 某个具体 $x$ 可能有 $q(x)>p(x)$，于是 $-\log q(x)<-\log p(x)$；KL 非负只保证按 $P$ 平均后，其他结果的代价抵消并超过这部分收益。

## 四、为什么 KL 不是距离

### 4.1 不对称

一般

$$
D_{\rm KL}(P\|Q)\ne D_{\rm KL}(Q\|P).
$$

例如 Bernoulli parameters $p=0.1,q=0.5$（nats）：

$$
D(0.1\|0.5)\approx0.368,
\qquad
D(0.5\|0.1)\approx0.511.
$$

方向决定“谁产生样本、谁被拿来解释”。交换方向会改变 rare event 的权重和 zero-support penalty。

### 4.2 不满足 triangle inequality

取 Bernoulli distributions $P,Q,R$ 的 success probabilities 为 $0.1,0.2,0.9$。数值上

$$
D(P\|R)\approx1.758,
$$

而

$$
D(P\|Q)+D(Q\|R)
\approx0.037+1.363=1.400.
$$

所以

$$
D(P\|R)>D(P\|Q)+D(Q\|R).
$$

### 4.3 可为无穷且方向不同

若 $P=(1/2,1/2)$，$Q=(1,0)$，则

$$
D(P\|Q)=+\infty,
$$

因为 $P$ 的第二个结果在 $Q$ 下不可能；但

$$
D(Q\|P)=\log2<\infty.
$$

因此正式名称应是 divergence/relative entropy，而不是 metric distance。

## 五、KL 的 chain rule

设 $P_{XY},Q_{XY}$ 是同一 joint space 上的 distributions，并有相应 marginals/conditionals。利用

$$
\frac{p(x,y)}{q(x,y)}
=\frac{p(x)}{q(x)}
\frac{p(y\mid x)}{q(y\mid x)},
$$

取 $P$-expectation：

$$
\boxed{
D(P_{XY}\|Q_{XY})
=D(P_X\|Q_X)
+E_{X\sim P_X}D(P_{Y\mid X}\|Q_{Y\mid X}).
}
$$

这说明 joint mismatch 由 marginal mismatch 与平均 conditional mismatch 精确组成。对 autoregressive sequence：

$$
D(P_{1:T}\|Q_{1:T})
=\sum_{t=1}^T
E_{X_{<t}\sim P}
D(P_{X_t\mid X_{<t}}\|Q_{X_t\mid X_{<t}}).
$$

注意 prefix 期望在真实 $P$ 下；这正是 teacher-forced population objective 的方向。

## 六、经验 cross-entropy、MLE 与 KL projection

数据 $x_1,\ldots,x_n\overset{iid}\sim P$，模型族 $\{q_\theta\}$。经验 NLL 为

$$
\widehat L_n(\theta)
=-\frac1n\sum_{i=1}^n\log q_\theta(x_i).
$$

它既是 negative average log-likelihood，也是 empirical distribution $\widehat P_n$ 对 $Q_\theta$ 的 cross-entropy：

$$
\widehat L_n(\theta)=H(\widehat P_n,Q_\theta).
$$

因此

$$
\arg\min_\theta\widehat L_n(\theta)
=\arg\max_\theta\sum_i\log q_\theta(x_i),
$$

即 MLE。

### 6.1 population target

在 LLN 条件下，固定 $\theta$ 有

$$
\widehat L_n(\theta)
\to E_P[-\log q_\theta(X)]
=H(P,Q_\theta).
$$

若 $H(P)$ 不依赖 $\theta$，population minimizer 满足

$$
\theta^*
\in\arg\min_\theta D(P\|Q_\theta).
$$

若 $P$ 不在模型族内，MLE 不是找“真实参数”，而是找 forward-KL 意义下的 pseudo-true projection。

### 6.2 经验最小不等于 population 最小

还需要 uniform convergence/complexity control、优化误差和数据协议。训练 cross-entropy 很低可能来自 overfitting、泄漏、重复样本或不正确 reduction，不能单靠 KL identity 宣称泛化。

## 七、categorical cross-entropy 从 logits 稳定推导

模型输出 logits $z\in\mathbb R^K$，softmax probability 为

$$
q_k=\frac{e^{z_k}}{\sum_je^{z_j}}.
$$

若 target distribution 是 $r\in\Delta^{K-1}$，单样本 cross-entropy：

$$
\ell(z;r)
=-\sum_kr_k\log q_k.
$$

代入 $\log q_k=z_k-\operatorname{LSE}(z)$：

$$
\boxed{
\ell(z;r)
=\operatorname{LSE}(z)-r^\top z,
\quad
\operatorname{LSE}(z)=\log\sum_je^{z_j},
}
$$

其中使用了 $\sum_kr_k=1$。

### 7.1 one-hot 特例

若真实类别为 $y$，$r=e_y$：

$$
\ell(z;y)
=-\log q_y
=\operatorname{LSE}(z)-z_y.
$$

### 7.2 gradient

因为

$$
\frac{\partial\operatorname{LSE}}{\partial z_k}=q_k,
$$

所以

$$
\boxed{\nabla_z\ell=q-r.}
$$

这不是“误差碰巧等于概率差”，而是 log-partition gradient 与 target sufficient statistic 的差。

### 7.3 Hessian

$$
\boxed{
\nabla_z^2\ell
=\operatorname{Diag}(q)-qq^\top\succeq0.
}
$$

对任意 $v$，

$$
v^\top[\operatorname{Diag}(q)-qq^\top]v
=\operatorname{Var}_{K\sim q}(v_K)\ge0.
$$

且矩阵对全一向量有零方向，因为给所有 logits 加同一常数不改变 softmax。

### 7.4 稳定 logsumexp

直接算 $e^{z_k}$ 可能 overflow。令 $m=\max_kz_k$：

$$
\operatorname{LSE}(z)
=m+\log\sum_ke^{z_k-m}.
$$

这是完全相同的数学量，却避免最大 exponent 超过 $1$。实现应使用 fused `log_softmax`/cross-entropy，而不是先 softmax 再取 log。

## 八、binary cross-entropy 与 logits

Bernoulli target $y\in\{0,1\}$，预测 $q=\sigma(a)$。BCE 为

$$
\ell(a;y)
=-y\log\sigma(a)-(1-y)\log[1-\sigma(a)].
$$

稳定形式是

$$
\boxed{
\ell(a;y)=\operatorname{softplus}(a)-ya,
}
$$

等价地

$$
\max(a,0)-ya+\log(1+e^{-|a|}).
$$

gradient 和 curvature：

$$
\frac{\partial\ell}{\partial a}=\sigma(a)-y,
\qquad
\frac{\partial^2\ell}{\partial a^2}=\sigma(a)[1-\sigma(a)].
$$

多标签任务通常对多个 Bernoulli coordinates 求和，但这隐含/近似了 factorized conditional likelihood；它不是一个 $K$ 类 categorical distribution。

## 九、常用分布的 KL

### 9.1 Bernoulli KL

$$
D_{\rm KL}(\operatorname{Ber}(p)\|\operatorname{Ber}(q))
=p\log\frac pq+(1-p)\log\frac{1-p}{1-q}.
$$

若 $p\in(0,1)$ 而 $q\in\{0,1\}$，KL 为无穷。

### 9.2 Categorical KL

$$
D(P\|Q)=\sum_{k=1}^Kp_k(\log p_k-\log q_k).
$$

用 log-probabilities 计算，避免先构造极小 $q_k$ 再除法。

### 9.3 单变量 Gaussian KL

设

$$
P=N(\mu_p,\sigma_p^2),
\qquad
Q=N(\mu_q,\sigma_q^2).
$$

log density ratio 为

$$
\log\frac{p(x)}{q(x)}
=\log\frac{\sigma_q}{\sigma_p}
-\frac{(x-\mu_p)^2}{2\sigma_p^2}
+\frac{(x-\mu_q)^2}{2\sigma_q^2}.
$$

在 $X\sim P$ 下：

$$
E_P[(X-\mu_p)^2]=\sigma_p^2,
$$

且

$$
E_P[(X-\mu_q)^2]
=\sigma_p^2+(\mu_p-\mu_q)^2.
$$

代入得到

$$
\boxed{
D(P\|Q)
=\log\frac{\sigma_q}{\sigma_p}
+\frac{\sigma_p^2+(\mu_p-\mu_q)^2}{2\sigma_q^2}
-\frac12.
}
$$

方向交换时分母 variance 与 log ratio 都改变，显式展示了不对称性。

### 9.4 多元 Gaussian KL

设 $P=N(\mu_p,\Sigma_p)$、$Q=N(\mu_q,\Sigma_q)$，两 covariance 都是 $d\times d$ SPD。由 Gaussian log density：

$$
\log\frac{p(x)}{q(x)}
=\frac12\left[
\log\frac{\det\Sigma_q}{\det\Sigma_p}
-(x-\mu_p)^\top\Sigma_p^{-1}(x-\mu_p)
+(x-\mu_q)^\top\Sigma_q^{-1}(x-\mu_q)
\right].
$$

对 $P$ 取 expectation。第一 quadratic term 的 expectation 为

$$
E_P[(X-\mu_p)^\top\Sigma_p^{-1}(X-\mu_p)]
=\operatorname{tr}(\Sigma_p^{-1}\Sigma_p)=d.
$$

令 $\delta=\mu_p-\mu_q$，则

$$
X-\mu_q=(X-\mu_p)+\delta.
$$

交叉项 expectation 为零，故

$$
E_P[(X-\mu_q)^\top\Sigma_q^{-1}(X-\mu_q)]
=\operatorname{tr}(\Sigma_q^{-1}\Sigma_p)
+\delta^\top\Sigma_q^{-1}\delta.
$$

最终

$$
\boxed{
D(P\|Q)=\frac12\left[
\operatorname{tr}(\Sigma_q^{-1}\Sigma_p)
+(\mu_q-\mu_p)^\top\Sigma_q^{-1}(\mu_q-\mu_p)
-d+\log\frac{\det\Sigma_q}{\det\Sigma_p}
\right].
}
$$

数值实现必须用 Cholesky solve 与 logdet，不显式形成 inverse 或 raw determinant。奇异 Gaussian 的支撑若不兼容，KL 可能为无穷；不能把 SPD 公式机械塞入 pseudoinverse 就宣称完成延拓。参见[[S-2021-Su-8512-多元正态分布的KL巴氏与W距离]]。

## 十、forward KL 与 reverse KL：方向效应必须带模型族解释

常见两类 projection：

$$
\min_{Q\in\mathcal Q}D(P\|Q)
\quad\text{与}\quad
\min_{Q\in\mathcal Q}D(Q\|P).
$$

### 10.1 forward KL 的 zero-avoidance

在 $D(P\|Q)$ 中，只要 $P$ 有质量而 $Q=0$，代价就是无穷。因此受限 $Q$ 往往需要覆盖 $P$ 的所有重要区域。MLE/cross-entropy 通常对应这个方向。

### 10.2 reverse KL 的 zero-forcing

在 $D(Q\|P)$ 中，expectation 只看 $Q$ 放质量的地方；若某些 $P$ mode 被 $Q$ 完全忽略但 $Q$ 从不访问，未必直接支付代价。受限 unimodal variational family 可能选择一个 mode，因此常被称为 mode-seeking。

> [!warning] “covering/seeking”不是无条件定理
> 行为依赖 target 的尾部、support、family $\mathcal Q$、parameterization 和局部优化。若两个方向都能取到 $P$，最优都为 $P$；不能把口号当成任意训练过程的预测。

## 十一、AI 目标中哪些改动仍是 cross-entropy

### 11.1 Label smoothing

one-hot $e_y$ 改为

$$
r=(1-\varepsilon)e_y+\varepsilon u,
$$

其中 $u$ 常为 uniform。损失仍是 $H(r,q)$，gradient 为 $q-r$，但 target 已变。它不再是原始 hard-label empirical likelihood；其 calibration/accuracy 效果依数据噪声和模型而定。

### 11.2 Soft targets 与 distillation

teacher distribution $p_T(\cdot\mid x)$、student $q_S$，固定 teacher 时：

$$
H(p_T,q_S)
=H(p_T)+D(p_T\|q_S).
$$

最小化 cross-entropy 等价于 forward KL。若使用 temperature $\tau$，probabilities 和 gradient scale 都改变；实践中常乘 $\tau^2$ 补偿 logit gradient 尺度，必须写入 objective。

### 11.3 Class weights

损失

$$
-w_y\log q_y
$$

改变了 classes/samples 的测度和目标风险。经适当归一化可解释为 reweighted data distribution 的 cross-entropy，但通常不再直接对应原数据分布下的 NLL，预测概率也可能需要 prior correction/calibration。

### 11.4 Focal loss

$$
-(1-q_y)^\gamma\log q_y
$$

让权重依赖当前模型输出。它一般不是固定 target distribution 与 $q$ 的普通 cross-entropy，也不是原始 likelihood；proper-scoring 与 calibration 性质需单独分析。

## 十二、VAE、蒸馏与一致性正则中的 KL

### 12.1 VAE

典型 regularizer

$$
D_{\rm KL}(q_\phi(z\mid x)\|p(z))
$$

是 approximate posterior 到 prior 的 reverse-direction KL（相对于 target posterior 的 VI 结构还会在 ELBO 中展开）。方向、per-sample/batch reduction 和 latent dimension 都影响数值。

### 12.2 Symmetric KL

$$
D(P\|Q)+D(Q\|P)
$$

是对称的，但仍不自动满足 triangle inequality，也不等于 Jensen–Shannon divergence。名称应写清。

### 12.3 非概率输出不能直接套 categorical KL

GlobalPointer、多标签 logits 或任意 score matrix 若整体不归一化为一个 probability distribution，就不能直接把数组代入

$$
\sum_ip_i\log(p_i/q_i).
$$

可选方案包括：

- 明确每个 coordinate 是 Bernoulli probability，求 factorized Bernoulli KL；
- 指定归一化轴，构造 categorical distribution；
- 使用 logits 上的 Bregman/consistency surrogate，并按真实公式命名。

[[S-2022-Su-9039-GlobalPointer下的KL散度]]的价值正是指出这个对象层错误，而不是授权把任何对称 logit penalty 都简称 KL。

## 十三、numerical stability 与 clipping 的含义

### 13.1 计算 log-probability，不先算极小 probability

使用 `log_softmax`、`logsumexp` 和 `BCEWithLogits` 型公式，避免 $q$ underflow 到零后产生虚假的 infinite loss/NaN。

### 13.2 clipping 改变 objective

把 $q$ 替换为

$$
\widetilde q=\max(q,\varepsilon)
$$

再取 log，若不重新归一化，就不再是 probability distribution；即使重新归一化，也是在优化平滑后的 $\widetilde Q$，不是原 $Q$。clipping 可作数值保护，但必须报告阈值与梯度行为，不能把被截断的有限值解释为原 KL 有限。

### 13.3 sum、mean 与有效样本数

框架的 `mean` 可能除 batch size、non-ignored elements 或带权重的 normalization。梯度尺度、regularization 相对强度和跨实验 loss 都受影响。公式必须写 denominator，而不是只写 API 默认值。

## 十四、cross-entropy、accuracy 与 calibration

cross-entropy 是对概率赋值敏感的 proper scoring rule：在 population、模型容量无限且优化精确时，期望 log loss 由真实 conditional distribution 最小化。现实中仍需区分：

- accuracy 只看 argmax；cross-entropy 还惩罚错误置信度；
- 更低 NLL 不保证每个 subgroup 都更准；
- finite data、regularization 和 misspecification 影响概率校准；
- distribution shift 下训练分布的 properness 不保证部署分布校准；
- label smoothing/focal/class weight 改变最优 probability target。

所以报告分类模型时，至少同时给 discrimination、NLL/Brier、calibration 和 shift/subgroup 检查。

## 十五、常见错误与纠正

| 错误说法 | 问题 | 纠正 |
|---|---|---|
| “cross-entropy 就是 KL” | 差一个 $H(P)$ | 固定 $P$ 时优化器相同，数值与概念不同 |
| “KL 是概率分布间的距离” | 不对称、无三角不等式 | 称 divergence，并写方向 |
| “KL 永远有限” | support mismatch 可为无穷 | 检查 $P\ll Q$ |
| “softmax CE 要先算 softmax” | 可能 overflow/underflow | 直接用 logits + logsumexp |
| “加 epsilon 只是实现细节” | clipping 改了 probability/objective | 报阈值、归一化与梯度 |
| “forward KL 一定 cover，reverse 一定 seek” | 忽略模型族与优化 | 只作受限 projection 的倾向解释 |
| “多标签 logits 之间可直接算 categorical KL” | 对象未归一化/语义不互斥 | 指定 Bernoulli/categorical/surrogate |
| “低训练 CE 证明真实分布被学到” | 经验误差、模型错设、overfit | 需要 held-out/generalization/diagnostics |

## 十六、推导与实现审计清单

1. $P$ 和 $Q$ 分别是谁？expectation 在谁下取？
2. 两者是否是同一空间上的 normalized probability measures？
3. 是否满足 $P\ll Q$；zero probability 是数学事实还是 underflow？
4. 对数底、单位与 reduction denominator 是什么？
5. entropy、cross-entropy、KL 和 NLL 是否被分别命名？
6. target 是否 fixed；label smoothing/teacher/weights 是否改变了 $P$？
7. logits 是否通过稳定 logsumexp 计算？
8. categorical 与 multi-label Bernoulli 语义是否正确？
9. Gaussian covariance 是否 SPD；实现是否使用 solve/logdet？
10. forward/reverse 方向是否与 sampling、projection、support 解释一致？
11. clipping、temperature、stop-gradient 和 mask 是否写入 objective？
12. empirical loss 是否被误当成 population divergence 或泛化证书？

## 十七、你现在应能独立重建的主链

$$
H(P,Q)=E_P[-\log q(X)]
=H(P)+D(P\|Q)
$$

$$
\log t\le t-1
\Longrightarrow
D(P\|Q)\ge0
\Longrightarrow
H(P,Q)\ge H(P).
$$

对模型训练：

$$
-\frac1n\sum_i\log q_\theta(x_i)
=H(\widehat P_n,Q_\theta)
\xrightarrow[]{\rm LLN}
H(P,Q_\theta),
$$

所以在固定 target 和合适统计条件下，MLE 是 $D(P\|Q_\theta)$ projection。下一章将取特殊 joint/product distributions 的 KL，得到 mutual information 并正式量化依赖。

## 习题与解答

- [[习题 - 交叉熵与 KL 散度]]：15 道 A–E 分层训练；
- [[解答 - 交叉熵与 KL 散度]]：完整证明、Gaussian 推导和 AI objective 审计。

## 参考来源

- Solomon Kullback & Richard A. Leibler, [On Information and Sufficiency](https://doi.org/10.1214/aoms/1177729694), 1951；
- MIT 6.441, [Information Theory lecture notes](https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/pages/lecture-notes/)，Chapter 1；
- Stanford EE376A, [Lecture Notes](https://web.stanford.edu/class/ee376a/files/lecture_notes.pdf)；
- Cover & Thomas, *Elements of Information Theory*；
- [[S-2021-Su-8512-多元正态分布的KL巴氏与W距离]]；
- [[S-2022-Su-9039-GlobalPointer下的KL散度]]。
