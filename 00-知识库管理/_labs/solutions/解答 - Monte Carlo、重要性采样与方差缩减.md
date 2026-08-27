---
type: solution
status: draft
area: [math/probability, math/statistics, ai/probabilistic-computation]
topic: "Monte Carlo、重要性采样与方差缩减"
exercise: "[[习题 - Monte Carlo、重要性采样与方差缩减]]"
prerequisites: ["[[Monte Carlo、重要性采样与方差缩减]]"]
related: ["[[概率论与数理统计 MOC]]", "[[练习与测验 MOC]]"]
sources: ["Owen-2013-Monte-Carlo-Theory-Methods-Examples", "Glynn-1994-Efficiency-Improvement-Techniques"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Monte Carlo、重要性采样与方差缩减

> [!warning] 使用边界
> 数值上能算出一个平均值不等于估计器有合法的误差理论。每个答案都分别检查目标、采样分布、支持、矩、偏差和相关结构。

## A. 识别与复述

### PROB-MC-A01

令 $Y_i=f(X_i)$、$X_i\overset{iid}{\sim}p$、$\mu=E_p f$，

$$
\hat\mu_n=\frac1n\sum_iY_i.
$$

- 若 $E|Y|<\infty$，则 $E\hat\mu_n=\mu$；
- 若 $\operatorname{Var}(Y)=\sigma^2<\infty$，则 $\operatorname{Var}(\hat\mu_n)=\sigma^2/n$；
- 若 $E|Y|<\infty$，SLLN 给 $\hat\mu_n\to\mu$ a.s.；
- 若 $0<\sigma^2<\infty$，CLT 给 $\sqrt n(\hat\mu_n-\mu)\Rightarrow N(0,\sigma^2)$。

无偏不限制方差；可存在无偏但无限方差的估计器。$n$ 大也必须相对于稀有事件概率、尾部和相关时间尺度来理解。当前一次运行还可能遭遇 seed sensitivity、实现错误、离散化偏差或模型错误，所以至少要报告 MCSE/重复运行和失败诊断。

### PROB-MC-A02

普通 IS 在能计算归一化 $p/q$ 时使用：

$$
\hat\mu_{IS}=\frac1n\sum_i\frac{p(X_i)}{q(X_i)}f(X_i),
\qquad X_i\sim q.
$$

在可积、支持覆盖下有限样本无偏；若 $E_q[w^2f^2]<\infty$，方差为 $\operatorname{Var}_q(wf)/n$ 并有普通 CLT。

SNIS 在 target 只知比例 $\tilde p=Zp$ 时使用：

$$
\hat\mu_{SNIS}
=\frac{\sum_ir_if_i}{\sum_ir_i},
\qquad r_i=\frac{\tilde p(X_i)}{q(X_i)}.
$$

它一般有限样本有偏，但在分子、分母 LLN 条件和 $E_qr=Z>0$ 下相合。其渐近方差为

$$
\tau^2=
\frac{\operatorname{Var}_q(r(f-\mu))}{(E_qr)^2}.
$$

支持要求：在 $|f|p$ 有正质量的任何集合上，$q$ 不能为零；否则漏掉部分积分。更强的 CLT/方差要求还需对应二阶矩有限。

### PROB-MC-A03

- 权重 ESS $1/\sum\tilde w_i^2$ 描述同一批 IS 权重集中度；
- MCMC ESS $n/\tau_{int}$ 描述相关序列均值因 autocorrelation 损失的信息量；
- 独立重复数是实验设计中的独立随机 streams/runs 数。

三者来源不同。高权重 ESS 不能证明链混合；高 MCMC ESS 不能修复 wrong target；多次重复也不能把有偏 estimator 自动变无偏。

最低报告：目标、estimator、$n$ 与独立重复、采样分布/链、MCSE、权重 ESS 与 max weight、log-weight 分位数、seed/PRNG、dtype/logsumexp、计算成本、running diagnostics 和失败案例。

## B. 手算与构造

### PROB-MC-B01

$X\sim U(0,1)$：

$$
\mu=E[X^2]=\frac13,
\qquad
E[X^4]=\frac15.
$$

所以

$$
\operatorname{Var}(X^2)
=\frac15-\frac19
=\frac4{45}.
$$

估计器精确均值、方差：

$$
E\hat\mu_n=\frac13,
\qquad
\operatorname{Var}(\hat\mu_n)=\frac4{45n}.
$$

$n=10^4$ 的理论 MCSE：

$$
\sqrt{\frac4{45\times10^4}}
=\frac2{\sqrt{450000}}
\approx\boxed{0.002981}.
$$

若样本标准差 $s=0.300$：

$$
\widehat{MCSE}=\frac{0.300}{100}=\boxed{0.00300}.
$$

### PROB-MC-B02

密度为

$$
p(x)=\frac1{\sqrt{2\pi}}e^{-x^2/2},
\qquad
q(x)=\frac1{\sqrt{4\pi}}e^{-x^2/4}.
$$

因此

$$
w(x)=\frac{p(x)}{q(x)}
=\sqrt2e^{-x^2/4}.
$$

$q$ 在整条实线上为正，支持覆盖成立，且

$$
E_q[wX^2]=\int x^2p(x)dx=1,
$$

所以 IS 无偏。

二阶矩：

$$
E_q[(wX^2)^2]
=\int x^4\frac{p(x)^2}{q(x)}dx.
$$

计算

$$
\frac{p(x)^2}{q(x)}
=\frac1{\sqrt\pi}e^{-3x^2/4},
$$

故积分有限，且

$$
E_q[(wX^2)^2]
=\frac8{3\sqrt3}.
$$

单样本贡献方差为

$$
\frac8{3\sqrt3}-1<\infty.
$$

较宽 proposal 在本题尾部覆盖良好。

### PROB-MC-B03

$$
\sum_i\tilde w_i^2
=0.5^2+0.2^2+3(0.1^2)
=0.32.
$$

所以

$$
\boxed{ESS_w=1/0.32=3.125},
\qquad
\boxed{\max_i\tilde w_i=0.50}.
$$

SNIS 估计：

$$
\hat\mu
=0.5(0)+0.2(0)+0.1(10)+0.1(10)+0.1(10)
=\boxed{3}.
$$

若 $f$ 的大值恰落在小权重样本上，贡献结构不同于大值落在最大权重样本上；ESS 完全没有读取 $f_i$。所以同一组权重对不同函数可产生完全不同的方差和偏差表现。

## C. 推导与证明

### PROB-MC-C01

在 $fp$ 对 $q$ 绝对连续时：

$$
\mu=\int fp
=\int f\frac pq q
=E_q[wf].
$$

因此样本平均无偏。若二阶矩存在：

$$
\operatorname{Var}(\hat\mu_{IS})
=\frac1n\left[
\int\frac{f^2p^2}{q}-\mu^2
\right].
$$

要最小化第一项。Cauchy–Schwarz：

$$
\left(\int|f|p\right)^2
=\left(\int\frac{|f|p}{\sqrt q}\sqrt q\right)^2
\le\left(\int\frac{f^2p^2}{q}\right)\left(\int q\right).
$$

因 $\int q=1$，下界在

$$
\frac{|f|p}{\sqrt q}=c\sqrt q
$$

时取等，即

$$
q^*(x)=\frac{|f(x)|p(x)}{\int|f|p}.
$$

若 $f\ge0$，分母就是未知 $\mu$，并且从 $q^*=fp/\mu$ 直接采样通常与原积分同样困难。它给出 proposal 应集中的理想形状，而非可直接调用的免费解。

### PROB-MC-C02

令

$$
A_n=\frac1n\sum_ir_if_i,
\qquad
B_n=\frac1n\sum_ir_i,
\qquad
\hat\mu=A_n/B_n.
$$

记 $a=E_q[rf]=Z\mu$、$b=E_qr=Z$。在二维二阶矩有限时，多元 CLT：

$$
\sqrt n\left(
\begin{bmatrix}A_n\\B_n\end{bmatrix}
-\begin{bmatrix}a\\b\end{bmatrix}
\right)
\Rightarrow N(0,\Sigma).
$$

对 $g(a,b)=a/b$，

$$
\nabla g(a,b)=
\begin{bmatrix}1/b\\-a/b^2\end{bmatrix}
=\frac1Z\begin{bmatrix}1\\-\mu\end{bmatrix}.
$$

作用在单样本向量 $(rf,r)$ 上的中心化线性组合是

$$
\frac1Z[(rf-a)-\mu(r-b)]
=\frac{r(f-\mu)}Z,
$$

其均值为零。因此 Delta 方法给

$$
\sqrt n(\hat\mu-\mu)
\Rightarrow N\left(0,
\frac{\operatorname{Var}_q(r(f-\mu))}{Z^2}
\right).
$$

又因 $Z=E_qr$，即题中结论。

有限样本时 $A_n/B_n$ 是随机比值，通常

$$
E[A_n/B_n]\ne EA_n/EB_n,
$$

故一般有偏；LLN 只保证比值最终趋于 $a/b=\mu$。

### PROB-MC-C03

设 $Eh=\eta$，

$$
Y_\beta=f-\beta(h-\eta).
$$

$EY_\beta=Ef=\mu$。方差

$$
V(\beta)=V_f+\beta^2V_h-2\beta C_{fh}.
$$

求导：

$$
V'(\beta)=2\beta V_h-2C_{fh}=0,
$$

所以

$$
\boxed{\beta^*=C_{fh}/V_h}.
$$

代回：

$$
V(\beta^*)
=V_f-\frac{C_{fh}^2}{V_h}
=V_f(1-\rho_{fh}^2).
$$

若 $\hat\beta$ 用同一批数据估计，它与样本均值项相关；有限样本下 estimator 不再简单等于“固定 $\beta$ 的无偏平均”，naive variance formula 也忽略拟合不确定性。

sample splitting：用独立 pilot 样本估 $\hat\beta$，冻结它；在 evaluation 样本上计算 $f_i-\hat\beta(h_i-\eta)$。条件于 pilot，$\hat\beta$ 是常数，evaluation estimator 无偏，可用 evaluation sample variance 估计条件 MCSE。可交叉拟合以减少数据浪费，但需合并 fold covariance。

## D. 边界、反例与纠错

### PROB-MC-D01

取空间 $\{0,1\}$：

$$
p(0)=p(1)=1/2,
\qquad
q(0)=1,q(1)=0,
\qquad
f(x)=\mathbf1_{\{x=1\}}.
$$

真目标

$$
\mu=E_pf=1/2.
$$

但从 $q$ 采样永远得到 0，在已采区域 $w(0)=p(0)/q(0)=1/2$，所有贡献 $w(0)f(0)=0$。估计恒为 0，稳定地错。

若做 SNIS，所有已观察 raw weights 还完全相等，权重 ESS $=n$，看起来“非常健康”。这证明 support audit 不能由样本内权重诊断代替。

### PROB-MC-D02

取 target $p=N(0,1)$、proposal $q=N(0,1/2)$，估计归一化积分 $\int p(x)dx=1$，即 $f=1$。

$$
w(x)=\frac{p(x)}{q(x)}
=\frac1{\sqrt2}e^{x^2/2}.
$$

一阶矩：

$$
E_qw=\int p=1,
$$

故样本平均权重无偏。但

$$
E_q[w^2]
=\int\frac{p(x)^2}{q(x)}dx.
$$

本题

$$
\frac{p(x)^2}{q(x)}=\frac1{2\sqrt\pi},
$$

在整条实线上为正常数，积分发散。因此方差无限。

常规 $s/\sqrt n$ 会高度不稳定且没有有限总体方差作为目标；经典有限方差 CLT 不适用。多 seed 和权重图可能暴露偶发巨权重，却无法从有限观察证明远尾二阶矩有限；需要解析尾比较、换更重尾 proposal 或采用有理论依据的截断/鲁棒方法并承认偏差。

### PROB-MC-D03

- **数值层**：logsumexp 避免计算 $e^{\ell_i}$ 时上下溢；
- **统计层**：若一个 $\ell_i$ 比其余大数百，稳定计算只会准确返回权重约 1，ESS 仍约 1；
- **支持层**：若 $q=0$ 而 $|f|p>0$，未采区域根本没有 log-weight 可算；
- **高维层**：似然比常是每维 log-ratio 之和，其方差/均值差随维度累积，典型集合错配可使权重退化指数恶化。

因此稳定 softmax 是必要实现技术，不是 IS 可行性的证明。

## E. AI 迁移

### PROB-MC-E01

取 $z_k\overset{iid}{\sim}q_\phi(z\mid x)$，定义

$$
w_k=\frac{p_\theta(x,z_k)}{q_\phi(z_k\mid x)},
\qquad
\hat p_K(x)=\frac1K\sum_kw_k.
$$

在 support 与可积条件下：

$$
E_q\hat p_K(x)
=\int q(z\mid x)\frac{p(x,z)}{q(z\mid x)}dz
=p(x).
$$

因为 $\log$ 凹：

$$
E\log\hat p_K(x)
\le\log E\hat p_K(x)
=\log p(x).
$$

所以 density estimator 无偏不代表 log-density estimator 无偏。

至少报告：

1. `log p(x,z)-log q(z|x)` 的分位数/范围；
2. normalized weight ESS 与 max weight；
3. $K$ 增长下 estimate/bound 曲线；
4. 多独立 seed 的分散；
5. posterior mode/support coverage；
6. logsumexp、dtype 和 NaN/inf；
7. encoder/decoder gradient norms 与权重 concentration；
8. 每个 data point 的诊断分布，而不只全局平均。

### PROB-MC-E02

单步 value 目标 $V=E_{S,A\sim\pi}[R]$。行为数据来自 $q$：

$$
\hat V_{IS}=\frac1n\sum_i
\frac{\pi(A_i\mid S_i)}{q(A_i\mid S_i)}R_i.
$$

SNIS：

$$
\hat V_{SNIS}
=\frac{\sum_iw_iR_i}{\sum_iw_i},
\qquad w_i=\frac{\pi(A_i\mid S_i)}{q(A_i\mid S_i)}.
$$

条件：若 $\pi(a\mid s)>0$，必须有 $q(a\mid s)>0$（positivity）。bounded reward 只控制 $R$，不能控制无界 ratio；还需权重相关矩。clipping $w^c=\min(w,c)$ 降方差但产生

$$
E[(w-w^c)R]
$$

型偏差，必须报告阈值 sensitivity。

长 horizon trajectory ratio

$$
W=\prod_{t=1}^T\frac{\pi(A_t\mid S_t)}{q(A_t\mid S_t)}
$$

的 log 是 $T$ 项和，方差与极值可快速增长。应考虑 per-decision IS、doubly robust、模型辅助及 horizon-wise diagnostics，但不能隐瞒各自假设/偏差。

### PROB-MC-E03

让一组随机场景/初始噪声 $U_i$ 同时驱动 A、B：

$$
D_i=Q_A(U_i)-Q_B(U_i),
\qquad
\hat\Delta=\frac1n\sum_iD_i.
$$

则

$$
\operatorname{Var}(D)
=V_A+V_B-2\operatorname{Cov}(Q_A,Q_B).
$$

正 covariance 降低 paired difference 方差。

实验设计：预注册 scenario distribution；每个独立 run 使用独立 master seed，并通过可记录的 substream 同步喂给 A/B；报告 $\hat\Delta$、$s_D/\sqrt n$、独立 run 数、paired scatter、A/B 单独方差、wall-clock/GPU-hours、失败率与 timeout 处理；保存原始 paired results 和软件版本。

若相同噪声使两算法输出负相关，则 covariance $<0$，差值方差反而大于独立随机数方案。应先用 pilot 估 covariance，并保留配对与非配对 sensitivity。
