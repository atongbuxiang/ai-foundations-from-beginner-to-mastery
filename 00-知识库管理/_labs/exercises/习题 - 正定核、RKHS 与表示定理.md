---
type: exercise
status: draft
area: [math/functional-analysis, math/kernel-methods, math/probability-metrics, ai/kernel-learning]
topic: "正定核、RKHS 与表示定理"
prerequisites: ["[[正定核、RKHS 与表示定理]]"]
related: ["[[练习与测验 MOC]]", "[[解答 - 正定核、RKHS 与表示定理]]", "[[实验 - Gram 正定性、KRR 表示与随机特征近似审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 正定核、RKHS 与表示定理

> [!abstract] 作答合同
> 共 15 题，A–E 每层 3 题。先闭卷保留原稿，再查正文。每次使用“核”“RKHS”“Mercer”“characteristic”时都要写清 domain、measure/function class 与所需条件；只做一组 Gram 数值检验不能替代普遍证明。建议 A/B 70 分钟、C/D 150 分钟、E 120 分钟。

## A. 对象、定义与条件识别

### GEO-RKHS-A01 六种性质的量词审计

分别精确定义或说明以下性质的对象、量词与 ambient class：

1. PSD kernel；
2. strictly positive-definite kernel；
3. conditionally positive-definite kernel（采用 $\sum_i c_i=0$ 的版本）；
4. RKHS；
5. characteristic kernel；
6. universal kernel（采用 compact Hausdorff $\mathcal X$ 上对 $C(\mathcal X)$ 的 sup-norm density）。

最后说明哪几组性质不能直接互推，以及“某一训练集的 Gram matrix positive definite”究竟证明了什么。

### GEO-RKHS-A02 三层对象与形状

对 $x_1,\ldots,x_n\in\mathcal X$，填完下表并解释对象所在空间：

| 对象 | 定义 | 所在空间/形状 | 依赖 sample 还是 population |
|---|---|---|---|
| canonical feature $k_x$ |  |  |  |
| Gram matrix $K$ |  |  |  |
| integral operator $T_k$ |  |  |  |
| mean embedding $\mu_P$ |  |  |  |
| empirical covariance $\widehat C$ |  |  |  |
| RFF matrix $Z$ |  |  |  |

指出哪些对象只需 set + PSD kernel，哪些还需 measure、integrability、topology 或 random-feature construction。

### GEO-RKHS-A03 Mercer、表示定理与 GP 的条件表

为下列三个结论分别写出最小课程版条件、结论、不包含的保证及一个删条件风险：

1. Classical Mercer expansion；
2. Generalized representer theorem；
3. Gaussian-process regression posterior formula。

特别回答：Mercer theorem 是否由一个 finite Gram eigendecomposition证明？表示定理是否保证 minimizer 存在且唯一？任意 symmetric $k$ 是否都能作为 GP covariance？

## B. 手算与最小例子

### GEO-RKHS-B01 Polynomial kernel 的显式 feature map

在 $\mathbb R^2$ 上令

$$
k(x,z)=(1+x^\top z)^2.
$$

1. 展开并给出一个最小自然维数的显式 $\phi(x)$，使 $k(x,z)=\phi(x)^\top\phi(z)$；
2. 对 $x_1=(1,0)$、$x_2=(0,1)$、$x_3=(1,1)$ 计算 Gram matrix；
3. 证明该 Gram matrix PSD，并判断是否 positive definite；
4. 计算 $d_k(x_1,x_2)$；
5. 若把平方改成 $p=1/2$，解释为什么不能沿用同一普遍合法性证明。

### GEO-RKHS-B02 Brownian kernel 与一个具体 RKHS

在 $[0,1]$ 上令 $k(s,t)=\min(s,t)$。

1. 用 indicator features证明 $k$ PSD；
2. 对 $0<t_1<t_2\le1$ 计算 $2\times2$ Gram determinant；
3. 计算 $\|k_t\|_{\mathcal H_k}$ 与 $d_k(s,t)$；
4. 说明为什么对应 RKHS 可与 absolutely continuous、$f(0)=0$、$f'\in L^2$ 的函数空间联系，并写出候选 inner product；
5. 用该 inner product验证 reproducing property。

### GEO-RKHS-B03 KRR 与 GP 同均值账本

给

$$
K=\begin{bmatrix}1&r\\r&1\end{bmatrix},
\quad |r|<1,
\quad y=\begin{bmatrix}1\\-1\end{bmatrix}.
$$

1. 对 objective $n^{-1}\|K\alpha-y\|^2+\lambda\alpha^\top K\alpha$ 求 $\alpha$；
2. 求 fitted vector $\hat y=K\alpha$；
3. 写出测试 covariance vector $k_*=(a,b)^\top$ 时的预测；
4. 对 noise variance $\sigma^2=2\lambda$ 写 GP posterior mean，并验证相同；
5. 写 posterior latent variance，指出 KRR 公式中没有的部分。

## C. 证明与推导

### GEO-RKHS-C01 Moore–Aronszajn 构造全证明

从任意 PSD kernel $k$ 出发：

1. 在 formal finite sums $\sum_i a_i k_{x_i}$ 上定义 sesquilinear form；
2. 证明其 positive semidefinite，并说明如何 quotient zero-norm directions；
3. 证明 $\langle f,k_x\rangle=f(x)$ 在 quotient 后良定义；
4. 完成该 pre-Hilbert space，并证明 completion 中 evaluation仍 bounded；
5. 证明 reproducing kernel 的唯一性；
6. 说明一个非最小 feature space如何与 canonical RKHS 的 closed feature span建立等距对应。

### GEO-RKHS-C02 广义表示定理与线性观测推广

设 $\ell_1,\ldots,\ell_m$ 是 $\mathcal H$ 上 bounded linear functionals，Riesz representers为 $r_i$。考虑

$$
\min_{f\in\mathcal H}
L(\ell_1(f),\ldots,\ell_m(f))
+\Omega(\|f\|_{\mathcal H}).
$$

1. 当 $\Omega$ strictly increasing 时证明每个 minimizer 属于 $\operatorname{span}\{r_i\}$；
2. 当 $\Omega$ 仅 nondecreasing 时说明能保证什么；
3. 令 $\ell_i(f)=f(x_i)$ 恢复经典形式；
4. 若 loss 同时依赖 $f'(x_i)$ 且 derivative evaluation bounded，写出表示基应怎样改变；
5. 给一个非单调 regularizer使结论失败的例子或构造思路。

### GEO-RKHS-C03 KRR 的 primal、dual、谱收缩与稳定性

对 $J(f)=n^{-1}\sum_i(f(x_i)-y_i)^2+\lambda\|f\|^2$：

1. 从表示定理推导 coefficient objective；
2. 不假设 $K$ invertible，证明 $\alpha=(K+n\lambda I)^{-1}y$ 给出唯一函数 minimizer；
3. 对 $K=U\operatorname{diag}(\kappa_j)U^\top$ 推导 smoother eigenvalues；
4. 求 $\operatorname{tr}S_\lambda$ 并解释 effective degrees of freedom；
5. 给出 label perturbation $\delta y$ 对训练预测和 coefficient 的 norm bound；
6. 解释为何显式 inverse、jitter 与 statistical $\lambda$ 必须分开处理。

## D. 反例、条件删除与数值陷阱

### GEO-RKHS-D01 十二个错误命题

逐项判定并给证明或反例：

1. Symmetric 且 $k(x,x)\ge0$ 就是 PSD kernel；
2. PSD kernel 的每个值都非负；
3. 任意 finite dataset 上 Gram PSD 推出给定公式在全 domain PSD；
4. Strictly PD 自动推出 characteristic；
5. Characteristic 自动意味着在任意 function space universal；
6. 每个 Hilbert space of functions 都是 RKHS；
7. Moore–Aronszajn theorem 需要 compact domain；
8. 每个 PSD kernel 都有无条件 uniform Mercer expansion；
9. Representer theorem 保证 minimizer存在且唯一；
10. GP sample paths 典型地属于 covariance RKHS；
11. RFF feature dimension翻倍使每个 seed 的 approximation error严格下降；
12. Fixed finite-width NTK PSD 说明训练期间 kernel保持不变。

### GEO-RKHS-D02 非法相似度与 PSD 修复审计

在 points $x=(0,1,2)$ 上比较：

$$
k_1(x,z)=-|x-z|^2,
\qquad
k_2(x,z)=\exp(-|x-z|^2/(2\ell^2)).
$$

1. 写出 $k_1$ Gram matrix并证明 indefinite；
2. 证明 centered matrix $-\tfrac12HD^2H$ PSD，并解释它对应什么 Euclidean geometry；
3. 说明“加一个足够大 diagonal”只能修复当前 finite matrix，不能自动给出 out-of-sample kernel formula；
4. 证明 $k_2$ 在 $\mathbb R$ 上 PSD 的一种路线，并明确调用的 theorem；
5. 讨论 finite-precision 下最小 eigenvalue略为负时的诊断顺序。

### GEO-RKHS-D03 Bandwidth、centering 与泄漏

设计一个 kernel workflow 失败审计，至少覆盖：

1. RBF $\ell\to0$ 与 $\ell\to\infty$ 时 Gram matrix的极限、rank与 KRR 行为；
2. Kernel PCA/HSIC 为什么要 center，训练/测试 centering 如何保持一致；
3. 用全部数据调 bandwidth 后再报告同一测试集性能为何 leakage；
4. Jitter、regularization、early stopping分别在哪一层；
5. 只报告 Gram condition number不能推出什么统计结论。

## E. AI 与研究迁移

### GEO-RKHS-E01 MMD/HSIC 两样本与独立性合同

给 iid samples $x_1,\ldots,x_m\sim P$、$y_1,\ldots,y_n\sim Q$ 及 paired samples $(u_i,v_i)_{i=1}^N$：

1. 推导 population MMD 平方 kernel expansion；
2. 写 biased 与 unbiased empirical MMD estimator，并解释 diagonal项；
3. 写 biased HSIC estimator及 centering matrix；
4. 说明 MMD $=0\Rightarrow P=Q$、HSIC $=0\Rightarrow U\perp V$ 各需什么 kernel richness；
5. 设计 permutation calibration，并说明 time dependence 下为什么不能任意置换；
6. 给完整报告字段：kernel/bandwidth、estimator、sample assumptions、null calibration、effect scale等。

### GEO-RKHS-E02 Exact kernel、Nyström 与 RFF 方案评审

现有 $n=200{,}000$、$d=128$ 的 regression 数据，候选是 RBF KRR。你不能存 dense Gram matrix。

1. 比较 exact iterative matvec、Nyström $m$ landmarks 与 RFF $D$ features 的 time/memory代理；
2. 为 Nyström 写 landmark、rank/regularization与 conditioning audit；
3. 为 RFF 写 spectral sampling、seed、feature normalization与 approximation audit；
4. 设计 held-out kernel-approximation 与 downstream-risk 双重验收；
5. 说明为何只让 $\|K-\tilde K\|_F$ 最小不保证最小 test risk；
6. 给出 resource budget改变时的选择规则。

### GEO-RKHS-E03 Linear Attention 与 NTK 声明边界

对 attention approximation $a(q,k)\approx\phi(q)^\top\varphi(k)$ 和 network NTK

$$
\Theta_t(x,z)=\langle\nabla_\theta f_{\theta_t}(x),\nabla_\theta f_{\theta_t}(z)\rangle,
$$

完成一份研究审计：

1. $\phi=\varphi$ 与 $\phi\ne\varphi$ 时 PSD/symmetry结论分别是什么；
2. 把 affinity approximation error传播到 normalized attention时需要控制什么 denominator；
3. Causal mask如何影响矩阵结合律实现；
4. 证明每个固定 $t$ 的 scalar-output empirical NTK Gram PSD；
5. 说明“训练等价 kernel regression”还需哪些 width/scaling/kernel-drift条件；
6. 设计记录 $\|\Theta_t-\Theta_0\|/\|\Theta_0\|$、function linearization error与task error的三层实验。

## 作答记录

| 题号 | 日期 | 状态 | 用时 | 主要错误 | 回链/重做日期 |
|---|---|---|---:|---|---|
| GEO-RKHS-A01—E03 |  | not-attempted |  |  |  |

状态只使用：`independent / hinted / copied / blocked / careless / not-attempted`。完整答案见[[解答 - 正定核、RKHS 与表示定理]]。
