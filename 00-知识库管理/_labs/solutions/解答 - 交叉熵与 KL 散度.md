---
type: solution
status: draft
area: [math/information-theory, ai/losses, ai/generative-models]
topic: "交叉熵与 KL 散度"
exercise: "[[习题 - 交叉熵与 KL 散度]]"
prerequisites: ["[[交叉熵与 KL 散度]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[练习与测验 MOC]]"]
sources: ["Kullback-Leibler-1951-Information-Sufficiency", "MIT-6.441-Information-Theory", "Stanford-EE376A-Information-Theory", "Su-9039-GlobalPointer-KL"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 交叉熵与 KL 散度

> [!warning] 使用边界
> 每次使用 KL 必须先确认 $P,Q$ 是同一空间上的 probability measures，并检查 $P\ll Q$。logit penalty、class-weighted loss 和截断 score 不能只因含有 logarithm 就自动叫 KL。

## A. 识别与复述

### INFO-KL-A01

$$
H(P)=-\sum_xp(x)\log p(x),
$$

$$
H(P,Q)=-\sum_xp(x)\log q(x)=E_P[-\log q(X)],
$$

$$
D(P\|Q)=\sum_xp(x)\log\frac{p(x)}{q(x)}=E_P\log\frac{p(X)}{q(X)}.
$$

因此

$$
D(P\|Q)=-H(P)+H(P,Q),
$$

即

$$
H(P,Q)=H(P)+D(P\|Q).
$$

cross-entropy 与 KL 的 expectation 都在 $P$ 下。若存在 $p(x)>0,q(x)=0$，二者为 $+\infty$；可数 infinite alphabet 还可能因 tail 太重而 entropy/cross-entropy 发散。

### INFO-KL-A02

五句话都不成立：

1. KL 一般不对称；
2. KL 一般不满足 triangle inequality；
3. $\sqrt{D(P\|Q)}$ 甚至仍不对称，当然不总是 metric；
4. symmetric KL 是 $D(P\|Q)+D(Q\|P)$，Jensen–Shannon 则用 mixture $M=(P+Q)/2$：

$$
\operatorname{JS}(P,Q)=\tfrac12D(P\|M)+\tfrac12D(Q\|M);
$$

5. $D(P\|Q)=0$ 表示 $P=Q$ almost everywhere，不只是均值相同。

### INFO-KL-A03

经验 distribution $\widehat P_n$ 下：

$$
\widehat L_n(\theta)
=-\frac1n\sum_i\log q_\theta(x_i)
=H(\widehat P_n,Q_\theta).
$$

最小化它就是最大化 likelihood。population objective 为

$$
H(P,Q_\theta)=H(P)+D(P\|Q_\theta),
$$

所以错设模型的 target 是 forward-KL projection。经验最小到部署表现至少还需审计：

- sampling/generalization error 与 uniform convergence；
- optimization error/local minima；
- approximation/model misspecification；
- hyperparameter/model selection reuse；
- dependent/weighted data 与 likelihood specification；
- train–deployment distribution shift。

## B. 手算与构造

### INFO-KL-B01

$$
H_2(P)=h_2(0.8)\approx0.721928.
$$

$$
\begin{aligned}
H_2(P,Q)
&=-0.8\log_20.6-0.2\log_20.4\\
&\approx0.853958.
\end{aligned}
$$

因此

$$
D_2(P\|Q)=0.853958-0.721928\approx0.132030.
$$

交换方向直接算：

$$
D_2(Q\|P)
=0.6\log_2\frac{0.6}{0.8}
+0.4\log_2\frac{0.4}{0.2}
\approx0.150978.
$$

数值不同，显示方向性。

### INFO-KL-B02

取 $m=2$：

$$
\operatorname{LSE}(z)
=2+\ln(1+e^{-2}+e^{-3}).
$$

denominator factor 为 $1+e^{-2}+e^{-3}\approx1.185122$，故

$$
q\approx(0.843795,0.114195,0.042010).
$$

target 为第一类：

$$
\ell=\operatorname{LSE}(z)-2
=\ln(1.185122)\approx0.169846.
$$

$$
\nabla_z\ell=q-e_1
\approx(-0.156205,0.114195,0.042010).
$$

Hessian：

$$
G=\operatorname{Diag}(q)-qq^\top.
$$

$$
G\mathbf1=q-q(q^\top\mathbf1)=q-q=0,
$$

因为 softmax 对统一平移不变。

### INFO-KL-B03

单变量公式：

$$
D(P\|Q)
=\ln\frac{\sigma_q}{\sigma_p}
+\frac{\sigma_p^2+(\mu_p-\mu_q)^2}{2\sigma_q^2}
-\frac12.
$$

对 $P=N(0,1),Q=N(1,4)$，$\sigma_q=2$：

$$
D(P\|Q)
=\ln2+\frac{1+1}{8}-\frac12
=\ln2-\frac14
\approx0.443147.
$$

反向：

$$
D(Q\|P)
=\ln\frac12+\frac{4+1}{2}-\frac12
=2-\ln2
\approx1.306853.
$$

mean mismatch 是 $(\mu_p-\mu_q)^2/(2\sigma_q^2)$；variance mismatch 由 log standard-deviation ratio、$\sigma_p^2/(2\sigma_q^2)$ 与 $-1/2$ 共同构成。方向交换会改变哪个 variance 出现在 denominator。

## C. 推导与证明

### INFO-KL-C01

对 $p(x)>0$ 且 $q(x)>0$，由

$$
\log t\le t-1
$$

取 $t=q(x)/p(x)$：

$$
-p(x)\log\frac{q(x)}{p(x)}\ge p(x)-q(x).
$$

求和：

$$
D(P\|Q)\ge\sum_x[p(x)-q(x)]=0.
$$

$p(x)=0$ 的项按极限为 $0$；若 $p(x)>0,q(x)=0$，KL 为 $+\infty$，结论仍成立。等号要求所有 $P$-positive 点上 $q/p=1$，再由归一化得 $P=Q$。

由 decomposition：

$$
H(P,Q)=H(P)+D(P\|Q)\ge H(P),
$$

等号同样当且仅当 $P=Q$。

### INFO-KL-C02

density ratio 分解：

$$
\log\frac{p(x,y)}{q(x,y)}
=\log\frac{p(x)}{q(x)}
+\log\frac{p(y\mid x)}{q(y\mid x)}.
$$

对 $P_{XY}$ 取 expectation。第一项只依赖 $x$：

$$
E_{P_{XY}}\log\frac{p(X)}{q(X)}=D(P_X\|Q_X).
$$

第二项先条件化：

$$
E_{X\sim P_X}
\left[
\sum_yp(y\mid X)\log\frac{p(y\mid X)}{q(y\mid X)}
\right]
=E_{P_X}D(P_{Y\mid X}\|Q_{Y\mid X}).
$$

故 chain rule 成立。递归应用到 sequence：

$$
D(P_{1:T}\|Q_{1:T})
=\sum_tE_{X_{<t}\sim P}
D(P_{X_t\mid X_{<t}}\|Q_{X_t\mid X_{<t}}).
$$

outer expectation 必须在 $P$ 下，因为原 joint KL 就是 $P$-expectation；换成 $Q$ 会改变 prefix 权重和 divergence。

### INFO-KL-C03

Gaussian log ratio：

$$
\log\frac{p(x)}{q(x)}
=\frac12\left[
\log\frac{\det\Sigma_q}{\det\Sigma_p}
-(x-\mu_p)^\top\Sigma_p^{-1}(x-\mu_p)
+(x-\mu_q)^\top\Sigma_q^{-1}(x-\mu_q)
\right].
$$

在 $P$ 下，第一 quadratic expectation：

$$
E_P[(X-\mu_p)^\top\Sigma_p^{-1}(X-\mu_p)]
=\operatorname{tr}(\Sigma_p^{-1}\Sigma_p)=d.
$$

令 $\delta=\mu_p-\mu_q$，展开 $X-\mu_q=(X-\mu_p)+\delta$。centered cross term expectation 为零，故

$$
E_P[(X-\mu_q)^\top\Sigma_q^{-1}(X-\mu_q)]
=\operatorname{tr}(\Sigma_q^{-1}\Sigma_p)
+\delta^\top\Sigma_q^{-1}\delta.
$$

代回即得题中公式。

SPD 保证 full-dimensional density、inverse 与 finite logdet 存在。奇异 Gaussian 只在 affine supports 兼容且 covariance 在支撑子空间满足相应绝对连续条件时可能有 finite KL；机械用 pseudoinverse 不足以处理 support。实现中对 $\Sigma_q=LL^\top$：

- 用 triangular solves 算 $\Sigma_q^{-1}\delta$ 与 $L^{-1}\Sigma_pL^{-\top}$ 的 trace；
- 用 $\log\det\Sigma_q=2\sum_i\log L_{ii}$；
- 不形成 explicit inverse 或 raw determinant。

## D. 边界、反例与纠错

### INFO-KL-D01

Bernoulli KL 用 natural log：

$$
D(a\|b)=a\ln\frac ab+(1-a)\ln\frac{1-a}{1-b}.
$$

计算得

$$
D(P\|R)=D(0.1\|0.9)\approx1.757780,
$$

$$
D(P\|Q)=D(0.1\|0.2)\approx0.036690,
$$

$$
D(Q\|R)=D(0.2\|0.9)\approx1.362738.
$$

右侧两项之和为 $1.399428$，小于 $1.757780$：

$$
D(P\|R)>D(P\|Q)+D(Q\|R),
$$

违反 triangle inequality。

### INFO-KL-D02

问题至少包括：

1. 截断后总和一般不为 $1$，不再是 probability distribution；
2. true zero 与 floating-point underflow 被混淆；
3. objective、gradient 和 support penalty 被阈值改变；
4. 若 $p_i>0,q_i=0$，原 KL 是无穷，截断结果却伪装成有限；
5. 阈值依 dtype/类别数可能产生不可比结果。

首选方案是从 logits 用 `log_softmax`/logsumexp 直接得到 normalized log probabilities，不需要 probability clipping。若业务上确要平滑，显式定义

$$
Q_\varepsilon=(1-\varepsilon)Q+\varepsilon U,
$$

其中 $U$ 是指定 base distribution，然后报告优化的是 $D(P\|Q_\varepsilon)$、$\varepsilon$、归一化和 gradient 规则；同时把数学 support failure 与 numerical underflow 分开记录。

### INFO-KL-D03

forward direction：

$$
D(P\|Q_c)\approx0.595108,
$$

而 $Q_m$ 在第三类为零、$P_3=0.49>0$，故

$$
D(P\|Q_m)=+\infty.
$$

forward KL 选择 $Q_c$，因为它覆盖所有 $P$-positive states。

reverse direction：

$$
D(Q_c\|P)\approx1.272966,
$$

$$
D(Q_m\|P)\approx0.679284.
$$

reverse KL 选择 $Q_m$。expectation 在 $Q_m$ 下，第三类 $Q_m=0$ 不直接支付漏掉 $P_3$ 的代价；它集中在一个大 mode。这个例子准确展示了 zero-avoidance/zero-forcing 倾向，但不是说任意 family/optimization 都必然 cover/seek。

## E. AI 迁移

### INFO-KL-E01

固定 teacher distribution $p_T^{(\tau)}$：

$$
H(p_T^{(\tau)},q_S^{(\tau)})
=H(p_T^{(\tau)})
+D(p_T^{(\tau)}\|q_S^{(\tau)}).
$$

第一项对 student 参数为常数，所以 student optimization 等价于 forward KL。

若原 student logits 为 $s$，$q=\operatorname{softmax}(s/\tau)$，则

$$
\frac{\partial H}{\partial s}
=\frac1\tau(q-p).
$$

$\tau$ 增大使 teacher/student distributions 更平坦，并显露非 top-class 的相对 logits；大 $\tau$ 时 $q-p=O(1/\tau)$，未缩放 gradient 因而约为 $O(1/\tau^2)$。乘 $\tau^2$ 后

$$
\nabla_s[\tau^2H]=\tau(q-p)=O(1),
$$

可在大温度极限维持 logit-matching scale。它只是尺度补偿，不保证 teacher 正确/校准，也不消除 hard-label loss、reduction 和 temperature 选择的权衡。

### INFO-KL-E02

先回答每个轴的随机语义。

1. **Categorical**：若恰有一个 mutually exclusive span/type outcome，必须指定归一化集合（例如所有合法 `(type,start,end)` 加 null），沿该集合 softmax；再算 categorical KL。
2. **Factorized Bernoulli**：若每个 span/type 可独立为正，逐坐标 sigmoid 得 $p_i,q_i$，求 Bernoulli KL 之和；这隐含 factorized joint，不能表达 label dependence。
3. **Logit consistency**：直接比较 logits，可用 squared error、symmetric Bregman 或文章明确给出的 surrogate；它不具有 normalized probability KL 的码长/absolute-continuity 解释。

三者的 sample space、normalization、support 和 gradient curvature 不同。所谓“沿所有轴 symmetric categorical KL”若任务不是单一互斥 outcome，就是对象错误。还应审计 invalid spans、mask、temperature、stop-gradient 和 reduction。参见[[S-2022-Su-9039-GlobalPointer下的KL散度]]。

### INFO-KL-E03

审稿意见核心：该结论超出了 objective 能支持的范围。

- class weights 改变了经验 target measure；需说明它对应 training/deployment 哪个 class prior；
- focal factor 依赖当前 $q_y$，通常不是固定 target 下的 ordinary cross-entropy/proper log score；
- loss 的 sum/mean、per-class denominator 与 sampling/oversampling 必须给出；
- 训练 loss 下降只说明该 surrogate 在训练数据下降，不推出部署 $D(P_{deploy}\|Q)$ 下降；
- 应在未参与调参的 held-out deployment-like data 报 unweighted NLL/Brier、accuracy/PR、reliability diagram、ECE 及置信区间；
- class weighting 后若要 probability interpretation，需要 prior correction 或再校准，并独立验证；
- threshold-dependent F1/recall 与 probability calibration 分开报告；
- subgroup、class prior shift、covariate shift 和 label shift 需单独测试；
- 比较 baseline 时保持 data split、temperature/calibration procedure 与 stopping rule 一致。

只有这些证据完成后，才可对部署概率质量作有限声明，不能由 weighted focal training loss 的名字推出 KL/calibration 结论。
