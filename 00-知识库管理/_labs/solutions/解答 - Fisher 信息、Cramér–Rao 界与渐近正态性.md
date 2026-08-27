---
type: solution
status: draft
area: [math/statistics, ai/information-geometry]
topic: "Fisher 信息、Cramér–Rao 界与渐近正态性"
exercise: "[[习题 - Fisher 信息、Cramér–Rao 界与渐近正态性]]"
prerequisites: ["[[Fisher 信息、Cramér–Rao 界与渐近正态性]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
sources: ["MIT-18.655-Lecture-13-Information-Inequality", "MIT-18.655-Lecture-17-Asymptotic-Normality", "van-der-Vaart-Asymptotic-Statistics", "Martens-2020-New-Insights-Natural-Gradient"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Fisher 信息、Cramér–Rao 界与渐近正态性

> [!warning] 使用边界
> 每个信息恒等式和渐近结论都带正则条件。若支持移动、真值在边界、信息奇异、模型错设或维数随样本增长，不能只替换一个矩阵就继续使用经典答案。

## A. 识别与复述

### PROB-FI-A01

单样本 score：

$$
s_\theta(X)=\nabla_\theta\log p_\theta(X).
$$

样本 score：

$$
s_n(\theta)=\sum_{i=1}^ns_\theta(X_i)
$$

仅在 iid/product likelihood 时是这种简单和。

expected/model Fisher：

$$
I(\theta)
=E_{X\sim p_\theta}[s_\theta(X)s_\theta(X)^\top].
$$

它是总体期望，保证 PSD。observed information：

$$
J_n(\theta)=-\nabla^2\ell_n(\theta),
$$

依赖已观测数据，不保证处处 PSD。empirical Fisher：

$$
\widehat F_{\rm emp}
=\frac1n\sum_i s_\theta(x_i)s_\theta(x_i)^\top,
$$

依赖已观测样本，保证 PSD，但标签通常没有按当前模型再取期望。

GGN 对复合 loss 写成

$$
G=J_f^\top H_{\ell,f}J_f;
$$

若 output loss convex 则 PSD，它忽略网络映射的某些二阶项。

在固定支持、可交换微分/期望、模型正确时，

$$
I(\theta)
=-E_\theta[\nabla^2\log p_\theta(X)].
$$

observed information 的样本平均可由 LLN 趋近 expected Fisher。对 canonical exponential-family conditional likelihood，model Fisher 常与 GGN 对齐。empirical Fisher 还需数据来自模型、采样层次匹配且样本量足够才可能靠近 model Fisher；四者不能无条件互换。

### PROB-FI-A02

标量参数、$E_\theta T=\theta$：

$$
\operatorname{Var}_\theta(T)\ge\frac1{I_n(\theta)}.
$$

若 $E_\theta T=g(\theta)$：

$$
\operatorname{Var}_\theta(T)
\ge\frac{[g'(\theta)]^2}{I_n(\theta)}.
$$

若 $m(\theta)=E_\theta T$，有偏的一般版本：

$$
\operatorname{Var}_\theta(T)
\ge\frac{[m'(\theta)]^2}{I_n(\theta)}
=\frac{[1+b'(\theta)]^2}{I_n(\theta)}
$$

其中 $b=m-\theta$。MSE 还要加 $b^2$。

向量参数、无偏估计 $g(\theta)$：

$$
\operatorname{Cov}(T)
\succeq G I_n^{-1}G^\top,
\qquad
G=\partial g/\partial\theta^\top.
$$

它不是任意 MSE 地板，因为经典版本限制无偏/regular estimator，且只在正则模型中成立；有偏 shrinkage 可用 bias 换 variance，Bayes/minimax risk 是另一比较类，边界模型可有不同速率，pointwise super-efficiency 也需用邻域风险解释。

### PROB-FI-A03

至少需要：

1. 真分布位于模型内，或明确 pseudo-true target；
2. $\theta_0$ 是参数空间内点；
3. 模型局部 identifiable；
4. 支持在 $\theta_0$ 邻域固定；
5. log-density 足够光滑；
6. 可交换导数与积分/期望；
7. score 有有限二阶矩，Hessian 有可积 envelope；
8. $I(\theta_0)$ 有限且 nonsingular；
9. MLE 存在、所选局部分支一致；
10. Hessian 有 local uniform LLN；
11. score 满足 CLT；
12. 参数维数固定或有适配高维的替代理论。

作用分别是：fixed support 排除 Uniform 式移动边界项；interior truth 排除 one-sided/tangent-cone limit；identifiability 排除多个参数同一分布；nonsingular information 保证局部二次型和逆存在；fixed dimension 让 classical matrix LLN/CLT 与 remainder 控制不随维数崩溃。

## B. 手算与构造

### PROB-FI-B01

单样本 log-likelihood：

$$
\ell(p;X)=X\log p+(1-X)\log(1-p).
$$

score：

$$
s_p(X)
=\frac Xp-\frac{1-X}{1-p}
=\frac{X-p}{p(1-p)}.
$$

故

$$
I_1(p)
=E[s_p^2]
=\frac{\operatorname{Var}(X)}{p^2(1-p)^2}
=\frac1{p(1-p)}.
$$

iid additivity 给

$$
I_n(p)=\frac n{p(1-p)}.
$$

无偏估计 $p$ 的 CRLB：

$$
\operatorname{Var}(T)\ge\frac{p(1-p)}n.
$$

$\bar X$ 无偏且 variance 正好为 $p(1-p)/n$，所以有限样本达界。

令

$$
\eta=\log\frac p{1-p},\qquad \frac{dp}{d\eta}=p(1-p).
$$

参数变换律：

$$
I_1(\eta)
=I_1(p)\left(\frac{dp}{d\eta}\right)^2
=p(1-p).
$$

直接求导也得 $s_\eta=X-p$，其 variance 是 $p(1-p)$。边界 $p=0,1$ 不属于有限 $\eta$，故上述 regular 计算只针对 $0<p<1$。

### PROB-FI-B02

单样本 score：

$$
s_\mu(X)=\frac{X-\mu}{\sigma^2}.
$$

所以

$$
I_1(\mu)=\frac1{\sigma^2},
\qquad
I_n(\mu)=\frac n{\sigma^2}.
$$

估计 $\mu$ 的无偏 CRLB 是 $\sigma^2/n$，由 $\bar X$ 达到。

对 $g(\mu)=e^\mu$，因

$$
\bar X\sim N(\mu,\sigma^2/n),
$$

可取

$$
T=\exp\left(\bar X-\frac{\sigma^2}{2n}\right).
$$

Gaussian MGF 给 $E[T]=e^\mu$。其二阶矩：

$$
E[T^2]
=e^{2\mu+\sigma^2/n},
$$

所以

$$
\operatorname{Var}(T)
=e^{2\mu}(e^{\sigma^2/n}-1).
$$

$g$ 版本 CRLB 为

$$
\frac{[g'(\mu)]^2}{I_n(\mu)}
=e^{2\mu}\frac{\sigma^2}{n}.
$$

由于 $e^a-1>a$ 对 $a>0$，$T$ 在有限样本不达界；但

$$
e^{\sigma^2/n}-1
=\frac{\sigma^2}{n}+O(n^{-2}),
$$

所以它一阶渐近达到该界。

### PROB-FI-B03

单样本 log-density：

$$
\ell(\mu,v)
=-\frac12\log(2\pi v)-\frac{(X-\mu)^2}{2v}.
$$

scores：

$$
s_\mu=\frac{X-\mu}{v},
$$

$$
s_v=-\frac1{2v}+\frac{(X-\mu)^2}{2v^2}.
$$

利用 Gaussian 中心奇矩为零和

$$
E[(X-\mu)^2]=v,\qquad
\operatorname{Var}((X-\mu)^2)=2v^2,
$$

得到

$$
I(\mu,v)
=\begin{pmatrix}
1/v&0\\
0&1/(2v^2)
\end{pmatrix}.
$$

令 $\rho=\log v$，Jacobian

$$
\frac{\partial(\mu,v)}{\partial(\mu,\rho)}
=\begin{pmatrix}1&0\\0&v\end{pmatrix}.
$$

因此

$$
I(\mu,\rho)
=\begin{pmatrix}
1/v&0\\
0&1/2
\end{pmatrix}.
$$

直接求导：

$$
s_\rho=v s_v
=-\frac12+\frac{(X-\mu)^2}{2v},
$$

其 variance 为 $1/2$，且与 $s_\mu$ 的乘积含三阶中心矩，期望为零。

交叉信息为零表示 $\mu$ 与 variance 坐标在该点的 Fisher metric 中正交，也让一阶 asymptotic covariance 为零；它不自动证明任意估计器在有限样本独立，也不适用于 $v=0$ 的边界。

## C. 推导与证明

### PROB-FI-C01

共同支持且允许求导移入积分时：

$$
\begin{aligned}
E_\theta[s_\theta(X)]
&=\int \nabla_\theta\log p_\theta(x)\,p_\theta(x)dx\\
&=\int\nabla_\theta p_\theta(x)dx\\
&=\nabla_\theta\int p_\theta(x)dx=0.
\end{aligned}
$$

对第 $j$ 个 score mean 再对 $\theta_k$ 求导。注意期望本身的 measure 也依赖 $\theta$：

$$
0
=\partial_kE_\theta[s_j]
=E_\theta[\partial_k s_j]+E_\theta[s_js_k].
$$

逐分量集合得

$$
E[ss^\top]
=-E[\nabla^2\log p_\theta(X)].
$$

对 iid 样本，$S_n=\sum_i s_i$：

$$
\begin{aligned}
I_n
&=E[S_nS_n^\top]\\
&=\sum_iE[s_is_i^\top]
+\sum_{i\ne j}E[s_i]E[s_j]^\top\\
&=nI_1.
\end{aligned}
$$

若仍能把依赖 joint score 分成 $S_n=\sum_i s_i$，一般是

$$
\operatorname{Var}(S_n)
=\sum_i\operatorname{Var}(s_i)
+\sum_{i\ne j}\operatorname{Cov}(s_i,s_j).
$$

cross-covariance 不再消失。更一般的依赖 likelihood 甚至不能写成 marginal score 的简单和，而要从 joint/conditional factorization 重新定义 score。

### PROB-FI-C02

令 joint score $S=\partial_\theta\log p_\theta^{(n)}(X)$，且 $E_\theta T=g(\theta)$。交换导数和积分：

$$
\begin{aligned}
E[TS]
&=\int T(x)\partial_\theta p_\theta^{(n)}(x)dx\\
&=\partial_\theta E_\theta[T]
=g'(\theta).
\end{aligned}
$$

因 $E[S]=0$，

$$
\operatorname{Cov}(T,S)=g'(\theta).
$$

Cauchy–Schwarz：

$$
[g'(\theta)]^2
\le\operatorname{Var}(T)\operatorname{Var}(S)
=\operatorname{Var}(T)I_n(\theta).
$$

故

$$
\operatorname{Var}(T)
\ge\frac{[g'(\theta)]^2}{I_n(\theta)}.
$$

等号当且仅当中心化变量线性相关：

$$
T-g(\theta)=a(\theta)S
$$

几乎处处成立。

若 $\theta=(\psi,\lambda)$ 且 $\lambda$ 是 nuisance，block Fisher：

$$
I=\begin{pmatrix}
I_{\psi\psi}&I_{\psi\lambda}\\
I_{\lambda\psi}&I_{\lambda\lambda}
\end{pmatrix}.
$$

block inverse 的左上块是

$$
(I^{-1})_{\psi\psi}
=\left(
I_{\psi\psi}
-I_{\psi\lambda}I_{\lambda\lambda}^{-1}I_{\lambda\psi}
\right)^{-1}.
$$

所以目标参数的有效信息为 Schur complement

$$
I_{\psi\cdot\lambda}
=I_{\psi\psi}
-I_{\psi\lambda}I_{\lambda\lambda}^{-1}I_{\lambda\psi},
$$

下界用 $I_{\psi\cdot\lambda}^{-1}$。未知 nuisance 会扣掉与其 score 可线性解释的那部分目标 score 信息。

### PROB-FI-C03

令平均 score

$$
\Psi_n(\theta)=\frac1n\sum_i s_\theta(X_i),
$$

且 $\Psi_n(\widehat\theta_n)=0$。在 $\theta_0$ 与 $\widehat\theta_n$ 之间 Taylor：

$$
0=\Psi_n(\theta_0)
+\dot\Psi_n(\widetilde\theta_n)
(\widehat\theta_n-\theta_0).
$$

因此

$$
\sqrt n(\widehat\theta_n-\theta_0)
=-\dot\Psi_n(\widetilde\theta_n)^{-1}
\sqrt n\,\Psi_n(\theta_0).
$$

证明链：

1. **一致性**：先由 identifiable population likelihood、uniform LLN 与 argmax theorem 得 $\widehat\theta_n\to_p\theta_0$；这保证中间点 $\widetilde\theta_n$ 也进入真值邻域；
2. **score mean zero/variance**：固定支持、交换条件给 $E_{\theta_0}s_{\theta_0}=0$、variance $I(\theta_0)$；
3. **multivariate CLT**：finite second moment 与 iid/Lindeberg 条件给

$$
\sqrt n\Psi_n(\theta_0)
\Rightarrow N(0,I(\theta_0));
$$

4. **uniform LLN for Hessian**：局部 smoothness 和 integrable envelope 给

$$
\sup_{\theta\in N(\theta_0)}
\|\dot\Psi_n(\theta)-E\dot\Psi(\theta)\|\to_p0;
$$

5. **information identity/continuity**：

$$
\dot\Psi_n(\widetilde\theta_n)\to_p-I(\theta_0);
$$

6. **matrix inverse continuity**：$I(\theta_0)$ nonsingular，故

$$
-\dot\Psi_n(\widetilde\theta_n)^{-1}
\to_p I(\theta_0)^{-1};
$$

7. **Slutsky**：

$$
\sqrt n(\widehat\theta_n-\theta_0)
\Rightarrow
N(0,I^{-1}II^{-1})
=N(0,I^{-1}).
$$

如果只有某个 stationary root 而无 consistency，它可能收敛到另一 mode；若 Hessian convergence 只是 pointwise，也不能自动控制随机中间点；若 $I$ singular，matrix inverse continuity 这一步直接失败。

## D. 边界、反例与纠错

### PROB-FI-D01

likelihood

$$
L(\theta;x)=\theta^{-n}\mathbf1\{\theta\ge X_{(n)}\},
$$

故 $\widehat\theta=X_{(n)}$。对 $t\ge0$ 且 $n>t$：

$$
\begin{aligned}
P\left(
n\frac{\theta-X_{(n)}}{\theta}>t
\right)
&=P\left(
X_{(n)}<\theta(1-t/n)
\right)\\
&=(1-t/n)^n\to e^{-t}.
\end{aligned}
$$

所以

$$
n\frac{\theta-X_{(n)}}{\theta}
\Rightarrow\operatorname{Exp}(1).
$$

误差尺度为 $1/n$，极限是单边 Exponential，不是 $1/\sqrt n$ Gaussian。原因是 support $(0,\theta)$ 随参数移动，normalization 求导出现边界贡献；MLE 又位于随机边界，而非由 interior score root 决定。只在 $0<x<\theta$ 写 $s=-1/\theta$ 会得到 $E[s]\ne0$，正是在提醒 regular score identity 不能使用，不能把 $E[s^2]=1/\theta^2$ 硬称为 classical Fisher 后继续套 CRLB。

### PROB-FI-D02

$X_i\sim N(\theta,\sigma^2)$，无偏 estimator $\bar X$ 达到 CRLB $\sigma^2/n$。考虑

$$
T_c=c\bar X.
$$

其 MSE：

$$
R_c(\theta)
=c^2\frac{\sigma^2}{n}+(1-c)^2\theta^2.
$$

在 $\theta=0$，取任何 $|c|<1$ 都有

$$
R_c(0)=c^2\sigma^2/n<\sigma^2/n;
$$

极端 $c=0$ 的 MSE 为零。没有违反 CRLB，因为 $T_c$ 对一般 $\theta$ 有 bias $(c-1)\theta$；无偏下界不是所有有偏 estimator 的 MSE 下界。

Hodges estimator 可写成：若 $|\bar X|\le n^{-1/4}$ 就输出 0，否则输出 $\bar X$。在 $\theta=0$，它以高概率精确输出 0，收敛比 $n^{-1/2}$ 更快；但在 local sequence $\theta_n$ 接近 threshold 的邻域，shrink-to-zero 造成放大的偏差和糟糕风险。regular local asymptotic efficiency 比较 $1/\sqrt n$ 邻域中的稳定 estimator，而不是只看一个固定点。因此单点超效率用邻域不稳定作为代价。

### PROB-FI-D03

至少两种结构零方向：

1. hidden-unit permutation 的多个离散等价 modes；
2. ReLU 相邻层正向缩放/反向缩放，形成连续 flat direction；
3. overparameterization 中 Jacobian rank 小于参数维数；
4. softmax logits 整体平移不改变 probabilities。

pseudoinverse 会丢弃低于数值容差的 eigen-directions；结果依赖 parameter coordinates、threshold、matrix approximation 和所选 generalized inverse。damping 使用

$$
(F+\lambda I)^{-1},
$$

在零方向赋予 $1/\lambda$ 的人工尺度，方向强烈依赖 $\lambda$ 与参数单位。若把它解释为 uncertainty，还隐含了某种 ridge/prior/metric choice，而非数据自己提供的信息。

这些零方向来自函数映射的结构对称或 rank 上限，同一分布对所有样本量都不区分它们；增加数据可以抬高已辨识方向的信息，却不能消灭真正 gauge symmetry。应改为 identifiable functionals、quotient geometry 或预测不确定性，而非给每个冗余权重硬造置信区间。

## E. AI 迁移

### PROB-FI-E01

固定输入 $x$，令 $Y$ 是 one-hot categorical vector，$P(Y=e_k)=p_k$。对 logits，

$$
\nabla_z\log p(Y\mid z)=Y-p.
$$

因此 model Fisher：

$$
\begin{aligned}
F_z
&=E[(Y-p)(Y-p)^\top]\\
&=\operatorname{Cov}(Y)\\
&=\operatorname{Diag}(p)-pp^\top.
\end{aligned}
$$

因为 $\operatorname{Diag}(p)\mathbf1=p$ 且 $pp^\top\mathbf1=p(\mathbf1^\top p)=p$，

$$
F_z\mathbf1=0.
$$

所有 logits 加同一常数不改 softmax，故该零方向有明确 symmetry 含义。

若 $J_z=\partial z/\partial\theta^\top$，

$$
F_\theta=J_z^\top F_zJ_z.
$$

model Fisher 对 $Y\sim p_\theta(\cdot\mid x)$ 取全部类别期望；用真实标签 $y_{\rm obs}$ 只产生

$$
(e_{y_{\rm obs}}-p)(e_{y_{\rm obs}}-p)^\top.
$$

对经验数据平均得到 empirical Fisher。若真实 conditional $Q(Y\mid X)$ 与模型不同，标签期望是 $Q$ 而非 $p_\theta$，结果一般不等于 model Fisher/GGN。

### PROB-FI-E02

审稿意见应指出：mini-batch empirical Fisher inverse diagonal 目前只能被描述为某种局部 preconditioner diagnostic，尚不能称 parameter confidence interval。至少需回答：

1. estimator 的重复抽样对象和 estimand 是什么？
2. conditional likelihood 是否正确 specified？
3. 为什么用 observed labels 的 outer product 等于 model Fisher？
4. 参数是否 identifiable，网络有哪些 permutation/scale/gauge symmetry？
5. 数据是 iid、user-clustered 还是 sequence dependent？
6. checkpoint 是 finite MLE、penalized optimum 还是 early-stopped SGD iterate？
7. mean/sum loss 与 Fisher scaling 是否正确？
8. mini-batch estimator 的 Monte Carlo variance 和 batch sensitivity 多大？
9. 使用 diagonal 后忽略的 parameter correlation 有多大？
10. inverse 如何处理零/负/微小 eigenvalue，damping 和 threshold 是什么？
11. 模型错设为何不用 $H^{-1}JH^{-1}$ sandwich？
12. regularization/weight decay 的 curvature 是否计入？
13. parameter coordinate 改变后 interval 如何变？
14. 真正关心的是 weight、logit、probability 还是 deployment risk，是否做 Delta propagation？
15. interval coverage 是否通过独立 simulation/bootstrap 验证？

在这些问题解决前，图上的“±2 standard errors”没有可验证的 95% repeated-sampling coverage 含义。

### PROB-FI-E03

pseudo-true parameter 满足 population estimating equation

$$
E_Q[s_{\theta^*}(X)]=0.
$$

样本 root 满足 $n^{-1}\sum_i s_{\widehat\theta}(X_i)=0$。Taylor：

$$
0
=\frac1n\sum_i s_{\theta^*}(X_i)
+\left[
\frac1n\sum_i\nabla s_{\widetilde\theta}(X_i)
\right](\widehat\theta-\theta^*).
$$

定义

$$
H=-E_Q[\nabla s_{\theta^*}(X)],
\qquad
J=E_Q[s_{\theta^*}(X)s_{\theta^*}(X)^\top].
$$

LLN、CLT 和 Slutsky 给

$$
\sqrt n(\widehat\theta-\theta^*)
\Rightarrow
N(0,H^{-1}JH^{-\top}).
$$

simulation 可选真实 $Q$ 为重尾或异方差 regression，而拟合 homoskedastic Gaussian linear model：

1. 固定 $n$ 与真 pseudo-target；
2. 重复生成 $R$ 份独立数据并拟合；
3. 每次构造 naive inverse-Hessian interval 与 sandwich interval；
4. 记录目标 coefficient/预测 functional 的 coverage、平均宽度和失败率；
5. 多个 $n$ 检查 asymptotic trend，$R$ 足够大并给 coverage 的 Monte Carlo standard error；
6. 同时画 standardized error，确认 failure 是 variance formula 还是 nonnormal finite-sample。

若记录按 user/sequence clustered，先把同一 cluster 的 score 求和

$$
S_g=\sum_{i\in g}s_i,
$$

再估

$$
\widehat J_{\rm cluster}
=\frac1G\sum_{g=1}^G S_gS_g^\top
$$

并配合与 $H$ 一致的归一化。token-level outer products 会漏掉 cluster 内所有 cross-covariance。有效渐近单位是独立 clusters 数 $G$，不是 token 总数。

## 结论复盘

- Fisher 是模型与参数点的局部对象，不是数据集的绝对属性；
- CRLB 的证明核心是 score covariance 与 Cauchy–Schwarz；
- MLE 正态性依赖 consistency、CLT、uniform LLN 和 nonsingular curvature；
- misspecification 用 sandwich，dependency 用 cluster/long-run score covariance；
- 深度网络中的 inverse curvature 只有在对象、近似与 regularity 对齐后才可解释为 uncertainty。
