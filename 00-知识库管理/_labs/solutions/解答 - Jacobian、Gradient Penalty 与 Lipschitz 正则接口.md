---
type: solution
status: draft
area: [neural-networks/regularization, jacobian, gradient-penalty, lipschitz]
topic: "[[Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]"
exercise: "[[习题 - Jacobian、Gradient Penalty 与 Lipschitz 正则接口]]"
sources: ["[[S-1992-Drucker-LeCun-Double-Backprop]]", "[[S-2017-Gulrajani-WGAN-GP]]", "[[S-2018-Miyato-Spectral-Normalization]]", "[[S-2018-Su-6051-Lipschitz约束]]", "[[S-2020-Su-7466-泛化性乱弹]]", "[[S-2021-Su-8796-输入参数梯度惩罚]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Jacobian、Gradient Penalty 与 Lipschitz 正则接口

## A

### NN-JGP-A01
对 $f:(\Omega,\|\cdot\|_X)\to(\mathcal Y,\|\cdot\|_Y)$，合同是所有 $x,x'\in\Omega$ 满足 $\|f(x)-f(x')\|_Y\le L\|x-x'\|_X$。Scalar output derivative action是 $df_x[v]=\nabla f(x)^Tv$；由 dual-norm 定义
$$\sup_{\|v\|_X\le1}|\nabla f^Tv|=\|\nabla f\|_{X,*}.$$
所以 input $\ell_p$ 对应 dual $\ell_q$，$1/p+1/q=1$。

### NN-JGP-A02
Loss gradient 含 loss 与 model 的链；model Jacobian直接测 logits/prob/features 对 input；operator penalty看 worst direction；WGAN-GP 对 scalar critic 和特定插值点把 norm 拉向 1；parameter gradient依赖参数化；spectral weight control约束每层 operator。它们的 output、coordinates、norm、sample domain 与 optimization cost都不同。

### NN-JGP-A03
Local 是某点/邻域；empirical 是有限样本平均；expected 是某 sampling distribution 的积分；global 是 domain 中任意点对或 Jacobian supremum；certified 还要求 sound computable upper bound 和数值容差。量词从“抽到的点通常小”到“所有点都不超过”不能靠措辞升级。

## B

### NN-JGP-B01
Singular values 为 $(3,1)$，所以 $\|J\|_2=3$、$\|J\|_F=\sqrt{10}$。$Je_1=(3,0)$、norm 3；$Je_2=(0,1)$、norm 1。只 probe $e_2$ 会报告 gain 1，却漏掉 worst direction $e_1$；单方向小不是 operator bound。

### NN-JGP-B02
串行 product bound：
$$2\cdot0.8\cdot1.5=2.4.$$
Residual block $F(x)=x+0.2G(x)$ 有
$$\operatorname{Lip}(F)\le1+0.2(0.8)=1.16.$$
二者都是 upper bounds；方向 cancellation、activation masks 和实际 trajectory 可使真实 constant 更小。

### NN-JGP-B03
$J^T=\begin{bmatrix}1&0\\2&-1\end{bmatrix}$。四个 probes 的 $J^Tv$ 与平方 norm：

- $(1,1)\mapsto(1,1)$：2；
- $(1,-1)\mapsto(1,3)$：10；
- $(-1,1)\mapsto(-1,-3)$：10；
- $(-1,-1)\mapsto(-1,-1)$：2。

平均为 $(2+10+10+2)/4=6$。而 $\|J\|_F^2=1^2+2^2+0^2+(-1)^2=6$，验证无偏性；单次 sample variance 仍很大。

## C

### NN-JGP-C01
凸性保证 $\gamma(t)=x+t(x'-x)\in\Omega$。由链式法则与积分
$$f(x')-f(x)=\int_0^1J_f(\gamma(t))(x'-x)dt.$$
Triangle inequality 和 operator norm 给
$$\|f(x')-f(x)\|\le\sup_{z\in\Omega}\|J_f(z)\|\|x'-x\|.$$
非凸 domain 中 chord 可能离开 $\Omega$，此处的 supremum 没覆盖路径；需扩 domain 或用 domain内路径/geodesic length。

### NN-JGP-C02
若 $E[vv^T]=I$，
$$
E\|J^Tv\|^2=E[v^TJJ^Tv]=\operatorname{tr}(JJ^TE[vv^T])=\|J\|_F^2.
$$
Rademacher/Gaussian probes 都可。有限 probes 的 variance 取决于 spectrum/off-diagonal structure；共享 probe 还引入 batch correlation。Estimator针对 singular values平方和，不是最大 singular value，不能把 trace estimate 当 operator certificate。

### NN-JGP-C03
$$\ell(x+\delta)=\ell(x)+\nabla_x\ell^T\delta+R_2.$$
在 $\|\delta\|\le\rho$ 上，dual-norm identity 给线性项最大值 $\rho\|\nabla_x\ell\|_*$，得到题中近似。若 $\rho$ 大、Hessian/curvature 大、跨越 ReLU kinks、attack 未求到 worst direction、gradient masking 或 loss不光滑，高阶/优化误差不可忽略；它不是 certified robust risk 等式。

## D

### NN-JGP-D01
Frobenius 是某点的 operator upper proxy，training average 不控制未采点的 supremum；target数值“小”也未指定 1-Lipschitz；finite optimization 只软惩罚而非硬约束。Adversarial robustness还依赖 threat norm/radius、loss margin和attack/certificate。因此只能声称“在所测 points 上某 Jacobian statistic 较小”，需另做 domain certificate 与 robust-risk evaluation。

### NN-JGP-D02
Two-sided $(\|g\|-1)^2$ 同时惩罚小于和大于1，适合 WGAN-GP 对 critic gradient norm接近1的特定动机；zero-centered $\|g\|^2$ 直接鼓励局部平坦；one-sided $\max(0,\|g\|-c)^2$ 只惩罚超过上限，允许更小 gradient。分类 loss、logit或critic的理想 gradient不同，必须根据任务定义 target而非照搬。

### NN-JGP-D03
先确认 dense/conv operator layout 与输入 norm；记录 power-iteration次数、warm start、gap/residual与 stop-gradient；把 activation和residual sum的 bounds接上，而非只报单层 norm；train-mode BN是 batch-coupled随机 operator，eval buffers不同；AMP下 norm estimation/normalization用何 dtype、underflow/overflow；再用 exact small matrices、SVD reference、export/eval一致性与 profiler 验收。

## E

### NN-JGP-E01
Local层：clean/augmented/mixed/held-out points 上测 loss/logit/prob Jacobian的mean/quantile和probe SE。Certificate层：声明 $\ell_p$ norm、radius/domain、sound method、bound/tolerance与认证率。Robust-risk层：强attack convergence、clean/robust accuracy/NLL、shift severity、gradient-masking checks。固定model/optimizer/steps/tuning seeds，报告double-backward FLOP、memory、wall time；三个层次分别下结论。

### NN-JGP-E02
在光滑小网络用中心差分检 input gradient、再差分参数验证 penalty gradient；显式 Jacobian与JVP/VJP/Hutchinson对齐；固定 RNG 比较checkpoint on/off；在 ReLU kink 两侧分别测并标 nondifferentiability；FP64 reference 对照 AMP；BN分别以 train/eval测试跨样本 coupling与buffer不变；覆盖 custom/in-place ops和多probe reduction。

### NN-JGP-E03
四组明确 output：scalar loss、logits vector、probability vector、parameters；为每组选择norm/probe数，使测得wall time或FLOP接近，等额调 penalty coefficient。报告对应 local statistic、clean/robust/shift risk、calibration、gradient/update和compute。差异只支持 matched-compute协议下该对象的作用，不能把最优一组称作普遍Lipschitz控制或唯一机制。
