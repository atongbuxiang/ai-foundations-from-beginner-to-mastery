---
type: solution
status: draft
area: [math/statistics, ai/bayesian-inference]
topic: "Bayesian 推断与后验预测"
exercise: "[[习题 - Bayesian 推断与后验预测]]"
prerequisites: ["[[Bayesian 推断与后验预测]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
sources: ["MIT-18.655-Lecture-3-5-11-18", "Gelman-et-al-Bayesian-Data-Analysis", "Stan-Users-Guide-Posterior-Prediction"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Bayesian 推断与后验预测

> [!warning] 使用边界
> 所有 posterior 声明都条件于 prior、likelihood、数据处理与推断实现。计算正确不等于模型正确。

## A. 识别与复述

### PROB-BAYES-A01

完整 joint model：

$$
p(\theta,y)=p(\theta)p(y\mid\theta).
$$

- prior $p(\theta)$ 在 parameter space 上积分为 1；
- likelihood $L(\theta;y)=p(y\mid\theta)$ 固定 $y$ 后一般不在参数上积分为 1；
- evidence

$$
p(y)=\int p(y\mid\theta)p(\theta)d\theta
$$

是在 data space 上的 prior predictive density；
- posterior

$$
p(\theta\mid y)=p(y\mid\theta)p(\theta)/p(y)
$$

在 parameter space 上归一化；
- posterior predictive

$$
p(\widetilde y\mid y)
=\int p(\widetilde y\mid\theta)p(\theta\mid y)d\theta
$$

在 future-data space 上归一化。

likelihood 只比较参数对已观测数据的相对支持；没有 prior 与 evidence normalization，所以不是参数分布。

### PROB-BAYES-A02

posterior risk

$$
\rho(a\mid y)=E[L(\Theta,a)\mid y].
$$

squared loss 展开为 posterior variance 加 $(a-E[\Theta\mid y])^2$，故 mean 最优。absolute loss 的左右导数由 $P(\Theta<a\mid y)$ 与 $P(\Theta>a\mid y)$ 决定，任一 median 使两侧概率不超过 $1/2$。离散 0–1 loss 下 risk 是 $1-P(\Theta=a\mid y)$，故 mode 最优。

连续参数中 $P(\Theta=a\mid y)=0$，pointwise 0–1 loss 对所有 action risk 都为 1；MAP 要用小邻域 loss/density mode 才得到。MAP 还依参数坐标，且丢掉 width、skewness 与 multi-modality，因此没有“最 Bayesian”的通用地位。

### PROB-BAYES-A03

| 对象 | 条件/重复方式 | 用途 |
|---|---|---|
| credible interval | 给定数据后的 posterior | parameter conditional uncertainty |
| confidence interval | 固定参数、重复采数据 | procedure coverage |
| prior predictive check | 从 prior 与 likelihood 生成 | 拟合前检查尺度/支持 |
| posterior predictive check | posterior 后生成 replicated data | 定向模型批评 |
| held-out evaluation | 未参与拟合/选择的新数据 | predictive comparison |
| SBC | prior 抽真参数、likelihood 造数据、反复运行推断 | 验证算法在已声明模型下是否校准 |

SBC 不证明现实模型正确；PPC 不给独立 test performance；credible mass 不自动给 fixed-parameter coverage。

## B. 手算与构造

### PROB-BAYES-B01

posterior：

$$
p\mid y\sim\operatorname{Beta}(2+7,3+3)
=\operatorname{Beta}(9,6).
$$

mean 与 mode：

$$
E[p\mid y]=\frac9{15}=0.6,
$$

$$
\operatorname{mode}(p\mid y)
=\frac{9-1}{9+6-2}
=\frac8{13}\approx0.6154.
$$

variance：

$$
\operatorname{Var}(p\mid y)
=\frac{9\cdot6}{15^2\cdot16}
=0.015.
$$

未来一次成功：

$$
P(\widetilde Y=1\mid y)=E[p\mid y]=0.6.
$$

未来三次恰两次成功：

$$
\begin{aligned}
P(\widetilde S=2\mid y)
&=\binom32\frac{B(11,7)}{B(9,6)}\\
&=3\frac{(9)_2(6)_1}{(15)_3}\\
&=\frac{1620}{4080}
\approx0.3971.
\end{aligned}
$$

### PROB-BAYES-B02

prior precision $1/9$，data precision $n/4=1$：

$$
\tau_n^2=\frac1{1/9+1}=\frac9{10}=0.9.
$$

$$
\mu_n
=0.9\left(\frac0{9}+\frac{4\cdot3}{4}\right)
=2.7.
$$

posterior：

$$
\mu\mid y\sim N(2.7,0.9).
$$

95% equal-tail interval：

$$
2.7\pm1.96\sqrt{0.9}
\approx2.7\pm1.859
=[0.841,4.559].
$$

未来观测：

$$
\widetilde Y\mid y\sim N(2.7,4+0.9)
=N(2.7,4.9).
$$

predictive variance 比 posterior parameter variance 大，因为还包含 observation noise 4。

### PROB-BAYES-B03

posterior：

$$
\pi\mid y\sim\operatorname{Dirichlet}(5,3,1),
$$

$$
E[\pi\mid y]=(5/9,3/9,1/9).
$$

对 $k_1+k_2+k_3=2$：

$$
P(k\mid y)
=\frac{2!}{\prod_jk_j!}
\frac{\Gamma(9)}{\Gamma(11)}
\prod_{j=1}^3\frac{\Gamma(\alpha_j+k_j)}{\Gamma(\alpha_j)},
\quad\alpha=(5,3,1).
$$

六种 counts 的概率：

$$
\begin{array}{c|cccccc}
k&(2,0,0)&(0,2,0)&(0,0,2)&(1,1,0)&(1,0,1)&(0,1,1)\\
\hline
P&1/3&2/15&1/45&1/3&1/9&1/15
\end{array}
$$

unseen class 的 posterior parameter 是 1 而非 0，所以 predictive probability 为 $1/9$。正概率来自 prior，不是数据凭空证明该类必出现。

## C. 推导与证明

### PROB-BAYES-C01

令 $m=E[\Theta\mid y]$：

$$
E[(\Theta-a)^2\mid y]
=\operatorname{Var}(\Theta\mid y)+(m-a)^2,
$$

故 $a=m$ 最小。

absolute risk

$$
r(a)=\int|\theta-a|p(\theta\mid y)d\theta.
$$

连续情形：

$$
r'(a)=P(\Theta<a\mid y)-P(\Theta>a\mid y)
=2F(a)-1.
$$

零点是 median；有 atom 时 subgradient 包含 0 的条件等价于左右 posterior mass 都不超过 $1/2$。

连续 pointwise 0–1 loss 的退化与 A02 相同；MAP 是 density/小球极限下的 action，且受坐标变换影响。

### PROB-BAYES-C02

令

$$
m(\Theta)=E[\widetilde Y\mid\Theta,y].
$$

插入减去 $m(\Theta)$ 与 $E[m(\Theta)\mid y]$，或直接用 total variance：

$$
\begin{aligned}
\operatorname{Var}(\widetilde Y\mid y)
&=E[(\widetilde Y-E[\widetilde Y\mid y])^2\mid y]\\
&=E[\operatorname{Var}(\widetilde Y\mid\Theta,y)\mid y]\\
&\quad+\operatorname{Var}(m(\Theta)\mid y).
\end{aligned}
$$

plug-in 把 $\Theta$ 固定为 $\widehat\theta$，删掉第二项。非线性例：

$$
E[e^\Theta\mid y]
=e^{m+s^2/2}>e^m
$$

当 $\Theta\mid y\sim N(m,s^2)$ 且 $s^2>0$。所以 plug-in 连 predictive mean 也可能偏离 posterior integration。

### PROB-BAYES-C03

conditional independence：

$$
p(y_{1:n}\mid\theta)=\prod_i p(y_i\mid\theta).
$$

batch posterior：

$$
p(\theta\mid y_{1:n})
\propto p(\theta)\prod_{i=1}^np(y_i\mid\theta).
$$

序贯一步：

$$
p(\theta\mid y_{1:k})
\propto p(y_k\mid\theta)p(\theta\mid y_{1:k-1}),
$$

递归展开得到同一 product；归一化常数不同但最终 distribution 相同。

若 $\theta^{(s)}\sim p(\theta\mid y)$：

$$
\widehat p(\widetilde y\mid y)
=\frac1S\sum_s p(\widetilde y\mid\theta^{(s)}).
$$

令 $\ell_s=\log p(\widetilde y\mid\theta^{(s)})$、$m=\max_s\ell_s$：

$$
\log\widehat p
=m+\log\sum_s e^{\ell_s-m}-\log S.
$$

这是 stable log-average-exp。

## D. 边界、反例与纠错

### PROB-BAYES-D01

若 $\theta>0$ 上写 $p_\Theta(\theta)\propto1$，令 $\phi=\log\theta$，则

$$
p_\Phi(\phi)
\propto p_\Theta(e^\phi)\left|\frac{d\theta}{d\phi}\right|
\propto e^\phi,
$$

并不 flat。反之在 $\phi$ 上 flat 对应 $p_\Theta(\theta)\propto1/\theta$。所以“无信息”不能由坐标上的常数密度定义。

improper prior 的未定常数 $c$ 可能在单模型 posterior normalization 中抵消，使 posterior proper；但 evidence

$$
p(y)=c\int p(y\mid\theta)\widetilde p(\theta)d\theta
$$

保留 $c$，Bayes factor 随任意常数改变，因而未定义。

### PROB-BAYES-D02

真数据 $Y_i\sim t_3(0,1)$，却拟合 $N(\mu,1)$ 且给 regular prior。posterior 对 $\mu$ 随 $n$ 以约 $1/\sqrt n$ 集中，可非常窄；但 Gaussian predictive 严重低估 tail probability，极端风险不可靠。

至少检查：

1. prior predictive 与 prior scale sensitivity；
2. posterior predictive tail/max/outlier discrepancy；
3. held-out log score 与 tail coverage；
4. robust Student-$t$ likelihood 替代；
5. contamination/leave-one-out sensitivity；
6. deployment-shift stress test。

窄只表示指定错误模型内参数被精确确定。

### PROB-BAYES-D03

VAE：

$$
p_\theta(x,z)=p(z)p_\theta(x\mid z),
$$

true local posterior 是 $p_\theta(z\mid x)$；encoder $q_\phi(z\mid x)$ 是 amortized approximation。标准训练把 $\theta,\phi$ 当优化参数，得到点 estimates。

full Bayesian weights 还需

$$
p(\theta,\phi\mid D)
\propto p(D\mid\theta,\phi)p(\theta,\phi),
$$

并对其积分/采样。标准 VAE 的 latent uncertainty 不等于 weight posterior uncertainty。

## E. AI 迁移

### PROB-BAYES-E01

最低审计：

- prior 在 weight coordinates 的尺度、layer mask 与 induced function smoothness；
- permutation/ReLU-scale symmetry；
- categorical likelihood、label noise 与 sampling shift；
- exact target 与 Laplace/VI/MCMC/dropout 的 approximation；
- posterior predictive 是否对 weight draws 积分；
- in-distribution calibration、proper score 与 subgroup coverage；
- OOD/adversarial stress；
- ESS/MCSE 或 optimization variability；
- PPC/SBC 与 held-out evaluation；
- prior/model sensitivity。

deep ensemble 是多个 optimization basins 的经验 mixture，不自动按 posterior mass 加权；MC dropout 只有在特定 variational model/目标下有近似解释，普通 dropout passes 不是任意 BNN 的 exact draws。

### PROB-BAYES-E02

对客户 $j=1,\ldots,50$：

$$
S_j\mid p_j\sim\operatorname{Binomial}(n_j,p_j),
$$

$$
\operatorname{logit}p_j\mid\mu,\tau
\sim N(\mu,\tau^2),
$$

并给 $\mu$ weakly informative prior、$\tau$ proper positive prior。posterior predictive 可针对各客户未来 conversions、new customer 的 $p_{\rm new}$ 与总体 weighted rate。

no pooling 各客户独立，small $n_j$ 极不稳定；complete pooling 强制同 $p$；partial pooling 让 small groups 更向 population shrink。检查 group size 与 activity weighting、极端 groups、new-vs-existing customer predictive、hyperprior sensitivity、PPC 的 group mean/variance/max 和 leave-one-group-out。

### PROB-BAYES-E03

以 hierarchical negative-binomial count model 为例：

1. prior predictive：检查 counts、zero rate、max、group variance 是否现实；不能证明 data fit；
2. SBC：prior 造参数/数据并检查 posterior ranks；发现代码/近似推断 calibration，不能证明现实 prior/likelihood；
3. PPC：比较 zero、tail、dispersion、time/group residual；发现模型结构缺口，不能给独立预测分数；
4. held-out：按部署单位/时间切分，报告 log score、coverage、decision loss；能比较预测，但只覆盖该 test distribution，不能证明未来不 shift。

四阶段分别覆盖 specification、computation、model criticism、external prediction，不能省并为一个“Bayesian accuracy”数字。
