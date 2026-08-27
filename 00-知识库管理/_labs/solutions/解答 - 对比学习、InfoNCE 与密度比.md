---
type: solution
status: draft
area: [learning-theory/contrastive-learning, infonce, mutual-information]
topic: "[[习题 - 对比学习、InfoNCE 与密度比]]"
prerequisites: ["[[对比学习、InfoNCE 与密度比]]"]
related: ["[[正负样本、Batch 依赖与梯度估计]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - 对比学习、InfoNCE 与密度比

> [!warning] 解题原则
> 先写candidate experiment。population classification、density ratio、MI lower bound、finite estimate与downstream utility各需单独证据。

## A. 识别与复述

### LT-NCE-A01

$I\sim Unif[K]$，$X\sim p_X$，$Y_I\sim p(y\mid X)$，其余$Y_j\sim p_Y$ iid。critic probability $q(i)=e^{s(x,y_i)}/\sum_je^{s(x,y_j)}$，population loss $L=E[-\log q(I)]$。support、conditional independence和negative law属于定义。

### LT-NCE-A02

original NCE是data-vs-known-noise binary classification，用于估计unnormalized model与partition parameter；InfoNCE是one-joint-among-marginals的multiclass risk/MI lower bound；negative sampling常是简化binary surrogate；contrastive divergence用short Markov chains近似energy-model likelihood gradient。

### LT-NCE-A03

五层依次是：candidate-index prediction risk；Bayes score对density ratio的identification；$\log K-L$的population MI lower bound；trained critic在finite reused samples上的estimate；表示在声明downstream task的risk。前一层不自动证明后一层。

## B. 手算与数值判断

### LT-NCE-B01

$Z=e^2+e+1\approx11.107$，positive probability $p_1\approx0.66524$，loss $-\log p_1\approx0.40761$。因此
$$ \log3-L\approx1.09861-0.40761=0.69100\text{ nats}. $$

### LT-NCE-B02

ceiling为 $\log256=8\log2\approx5.54518$ nats，即8 bits。要lower bound达到20 nats，必要条件 $\log K\ge20$，故 $K\ge e^{20}\approx4.85\times10^8$；这还不保证critic/gaps允许达到。

### LT-NCE-B03

$X=Y$ uniform binary时 $H(Y)=\log2$、$H(Y\mid X)=0$，故 $I=\log2$。$K=2$ ceiling也为$\log2$；但marginal negative以1/2概率等于positive value，使candidate index ambiguous，finite candidate task并非每次完美。

## C. 推导与证明

### LT-NCE-C01

给$I=i$的density为 $p_X(x)p(y_i\mid x)\prod_{j\ne i}p_Y(y_j)$。提出共同项 $p_X(x)\prod_jp_Y(y_j)$，只余 $r_i=p(y_i\mid x)/p_Y(y_i)$。uniform prior下
$$ P(I=i\mid x,y_{1:K})=\frac{r_i}{\sum_jr_j}. $$
所以softmax Bayes score为 $\log r(x,y)+c(x)$。

### LT-NCE-C02

cross-entropy decomposition给 $L=H(I\mid W)+E[KL(P(I\mid W)\|q(I\mid W))]\ge H(I\mid W)$，$W=(X,Y_{1:K})$。因$H(I)=\log K$，
$$ \log K-L\le I(I;W). $$
再用candidate construction的KL chain rule或log-sum inequality证明 $I(I;W)\le I(X;Y)$，才得到InfoNCE bound；第二步依赖positive conditional与iid marginal negatives。

### LT-NCE-C03

对bijective measurable $f,g$，sigma-algebras $\sigma(f(X))=\sigma(X)$、$\sigma(g(Y))=\sigma(Y)$；或用KL在bijection pushforward下不变，得 $I(f(X);g(Y))=I(X;Y)$。任意invertible entangling map保持MI，所以MI不能偏好axis-aligned factors。

## D. 边界、反例与纠错

### LT-NCE-D01

它不是无偏MI estimator，因为：finite-$K$ lower-bound gap；critic approximation gap；optimization gap；finite-sample/within-batch dependence；trained-and-evaluated critic overfit；adaptive selection；ceiling $\log K$。loss的unbiasedness即使成立，也只是对chosen contrastive risk。

### LT-NCE-D02

negative来自$q(y\mid x)$时Bayes ratio proportional to $p(y\mid x)/q(y\mid x)$，而非$p(y\mid x)/p_Y(y)$。hard proposal常依赖x与current model，所以original MI proof的marginal-negative step失效；可importance-correct或重新声明estimand。

### LT-NCE-D03

每个sample含独立task label $Y$、unique ID $I$；two views保留watermark ID但task content被破坏。encoder只编码$I$即可完美匹配positive、排除other instances，得到低contrastive loss/高view MI，却对$Y$为chance。

## E. AI 迁移

### LT-NCE-E01

image–text positive是curated pair joint；negatives说明in-batch/global/filtered law；记录encoders、projection、normalization、temperature、K与all-gather。inner validation选择；outer按source/time/near-duplicate split评价bidirectional Recall/mAP、caption quality groups与downstream tasks。

### LT-NCE-E02

构造correlated Gaussian with analytic $I=-\frac12\log(1-\rho^2)$。扫描$\rho$、K、N和critic family；独立train/eval critic；重复seeds估bias/variance；比较true MI、population-near Monte Carlo bound、held-out bound与training estimate，展示log-K saturation。

### LT-NCE-E03

报告变量/units、positive/negative laws、support、K与nats/bits；critic family和optimization；train/eval split与confidence method；log-K ceiling；所有searched configs；bound而非equality措辞；distribution assumptions；下游task、head、groups与shift证据。
