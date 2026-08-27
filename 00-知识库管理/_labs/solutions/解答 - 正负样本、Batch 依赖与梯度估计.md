---
type: solution
status: draft
area: [learning-theory/contrastive-learning, batch-dependence, gradients]
topic: "[[习题 - 正负样本、Batch 依赖与梯度估计]]"
prerequisites: ["[[正负样本、Batch 依赖与梯度估计]]"]
related: ["[[数据增强、不变性、等变性与任务充分性]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - 正负样本、Batch 依赖与梯度估计

> [!warning] 解题原则
> sampler、mask、temperature、queue、all-gather与stop-gradient共同定义算法。先定population target，再问batch estimator的bias、dependence与variance。

## A. 识别与复述

### LT-BAT-A01

先抽$U_{1:B}$，每个生成two views $X_{2b-1},X_{2b}$，positive map$j(i)$。对eligible set$\mathcal A(i)$，
$$ \ell_i=-\log\frac{\exp(s(z_i,z_{j(i)})/\tau)}{\sum_{k\in\mathcal A(i)}\exp(s(z_i,z_k)/\tau)},\qquad \widehat L=(2B)^{-1}\sum_i\ell_i. $$
必须说明self/same-group mask与是否双向。

### LT-BAT-A02

false negative在task semantics上其实positive；dependent negative与anchor共享user/sequence/site而不满足声明的iid marginal；stale negative由旧encoder/queue产生。三者分别是target contamination、sampling dependence与moving-representation mismatch。

### LT-BAT-A03

改变B会改变candidate数K、log-sum-exp law、InfoNCE ceiling、hard/false-negative exposure、gradient direction、BN statistics与communication。故它常改变objective或population surrogate，而非只降低固定risk estimator variance。

## B. 手算与数值判断

### LT-BAT-B01

$Z=e^2+e+1=11.107$，$p\approx(0.66524,0.24473,0.09003)$，loss$\approx0.40761$。gradient
$$ \nabla_u\ell=p-e_1\approx(-0.33476,0.24473,0.09003). $$

### LT-BAT-B02

$$ P(\text{at least one collision})=1-(1-0.1)^{63}=1-0.9^{63}\approx0.99869. $$
balanced classes不意味着large batches没有false negatives。

### LT-BAT-B03

single-negative average collision：
$$ 0.8^2+0.2^2=0.68. $$
class-1 anchor在7 negatives中至少一次collision：
$$ 1-(1-0.8)^7=1-0.2^7=0.9999872. $$
frequent classes承受更高collision。

## C. 推导与证明

### LT-BAT-C01

$\ell=-u_++\log\sum_re^{u_r}$，故$\partial\ell/\partial u_k=p_k-1\{k=+\}$。若$u_k=z_i^Tz_k/\tau$，
$$ \nabla_{z_i}\ell=\frac1\tau\left(\sum_kp_kz_k-z_+\right), $$
即拉向positive、推离softmax-weighted candidate average；还要叠加anchor作为别人candidate的cross terms。

### LT-BAT-C02

$z=v/r,r=\|v\|$。微分
$$ dz=\frac1r\left(I-zz^T\right)dv, $$
所以Jacobian $J=(I-zz^T)/\|v\|$。因 $z^TJ=0$，backprop gradient在unit sphere tangent space；norm还控制scale。

### LT-BAT-C03

若目标negative expectation在$p_Y$、samples来自$q_\beta(y\mid x)$，weight为
$$ w(x,y)=\frac{p_Y(y)}{q_\beta(y\mid x)}. $$
但$q\propto p_Ye^{\beta s}$的normalizer依赖x且常未知；self-normalized weights有finite-sample bias，hard proposal还可能给heavy weights与high variance。log-sum nonlinear使逐项correction也需重新推导。

## D. 边界、反例与纠错

### LT-BAT-D01

更多negatives提高candidate diversity与log-K ceiling，也增加false-negative/duplicate概率、hard outliers、communication和staleness；dependent candidates不提供等量information。下游最优B取决于sampler、class prior、temperature与task，非单调定理。

### LT-BAT-D02

bank key为$h_{\theta_{t-\Delta}}(x)$，anchor为$h_{\theta_t}(x)$；它们不是同一current representation law。queue age与parameter drift造成moving-target bias/covariate mismatch。momentum encoder减缓而不消除，并改变stop-gradient graph。

### LT-BAT-D03

同user records在batch中互作negatives会把user-specific positives推开或让shortcut主导；跨train/test又泄漏identity/style，夸大generalization。应先按user/time分split与unit sampling，再在unit内augment，必要时mask same-group negatives。

## E. AI 迁移

### LT-BAT-E01

记录global source sampler与replica sharding；two-view seeds；local/global B；all-gather是否backprop；global positive indices与masks；similarity/temperature；sum/mean和LR scaling；SyncBN；drop-last/uneven batch；deterministic duplicate policy；outer evaluation版本。

### LT-BAT-E02

先按document/author/time/translation cluster分组；source units跨groups抽。same-document、parallel translations和near-duplicates进入positive或mask池而非默认negative；hard mining限定跨合法groups。记录被mask比例、estimated collision与downstream semantic/retrieval risk。

### LT-BAT-E03

factorial/分阶段扫描B、$\tau$、hardness、debias prior、queue size/age；每格固定compute或同时报告compute。诊断loss、gradient norm、effective softmax entropy、false-negative audit、queue age与duplicate rate；inner选择，outer冻结后评价linear probe/retrieval、groups与shift，多seed置信区间。
