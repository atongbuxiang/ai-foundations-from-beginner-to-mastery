---
type: solution
status: draft
area: [learning-theory/conformal-prediction, coverage, exchangeability]
topic: "[[Conformal Prediction 与有限样本 Coverage]]"
exercise: "[[习题 - Conformal Prediction 与有限样本 Coverage]]"
prerequisites: ["[[Conformal Prediction 与有限样本 Coverage]]"]
related: ["[[Covariate、Label 与 Concept Shift]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - Conformal Prediction 与有限样本 Coverage

> [!warning] 解题原则
> 每道题先画 proper-train/calibration/future 三角色，再检查 score 是否固定、联合 scores 是否 exchangeable、coverage 到底对什么随机性取概率。

## A. 识别与复述

### LT-CFM-A01

score $s_{D_{\rm tr}}(x,y)$ 越大越不符合；calibration scores $S_i=s(X_i,Y_i)$，索引 $k=\lceil(m+1)(1-\alpha)\rceil$，threshold 为第 $k$ order statistic（$k=m+1$ 时 $+\infty$）；集合 $\mathcal C(x)=\{y:s(x,y)\le\widehat q\}$；coverage event 是 $Y_{m+1}\in\mathcal C(X_{m+1})$。exchangeable rank 控制 validity；score/model quality 主要控制集合长度、大小和条件误差分布。

### LT-CFM-A02

marginal：
$$
\Pr\{Y_*\in C(X_*)\}\ge1-\alpha.
$$
pointwise conditional：
$$
\Pr\{Y_*\in C(x)\mid X_*=x\}\ge1-\alpha,\ \forall x.
$$
group：
$$
\Pr\{Y_*\in C(X_*)\mid G=g\}\ge1-\alpha,\ \forall g;
$$
class-conditional 把条件换成 $Y_*=k$。对 $T$ 个 future points 的 simultaneous：
$$
\Pr\{\forall t\le T,\ Y_t\in C_t\}\ge1-\alpha.
$$
它远强于每点 marginal coverage。

### LT-CFM-A03

i.i.d. 蕴含 exchangeable；exchangeable 不要求无条件独立，例如 de Finetti mixture 中给 latent variable 后 iid。错误包括按 visit 而非 patient split、同一原图的增强 views 跨 split、时间趋势数据随机打乱、session/household 记录当独立、policy 根据旧预测选择新数据。关键是 score sequence 的联合置换不变，而不是口头写“样本很多”。

## B. 手算与局部推导

### LT-CFM-B01

$$
k=\lceil(9+1)(0.8)\rceil=8,
$$
第 8 个 score 为 $\widehat q=1.0$。absolute-residual interval：
$$
[3.2-1.0,3.2+1.0]=[2.2,4.2].
$$
重复的 0.2 ties 用 $\le$ 纳入不会使该阈值下 coverage 变小。

### LT-CFM-B02

$$
k=\lceil5(0.9)\rceil=5=m+1,
$$
但 calibration 只有 4 个 scores，所以按保守 convention $\widehat q=+\infty$，集合为全空间。有限 $m$ 的 nonrandomized coverage levels 以 $1/(m+1)$ 为网格；要保证 90% 而 $m=4$ 时只能退化地全覆盖，说明 calibration size 决定可实现分辨率。

### LT-CFM-B03

最终区间：
$$
[4-0.8,7+0.8]=[3.2,7.8].
$$
score $s(y)=\max(4-y,y-7)$，故
$$
s(3.5)=0.5,\qquad
s(5)=\max(-1,-2)=-1,\qquad
s(8.2)=1.2.
$$
CQR score 可为负；若实现强行截断为 0，就改变 score 和可能的 efficiency，必须明确。

## C. 证明与反例

### LT-CFM-C01

给定 proper training data，固定 score 后，$m$ 个 calibration scores 与 future score exchangeable。无 ties 时 future rank $R$ 在 $\{1,\ldots,m+1\}$ 均匀。若 $R\le k$，future score 不超过第 $k$ calibration threshold；若 $R>k$ 则超过。因此
$$
\Pr(Y_*\in C(X_*))
=\Pr(S_*\le\widehat q)
=\Pr(R\le k)
=\frac{k}{m+1}\ge1-\alpha.
$$
当 $k=m+1$ 集合全空间。ties 时用 $\le$ 把边界 ties 全纳入，相当于让某些高 rank 也覆盖，不会降低概率；随机 tie-breaking 可获得更精确 level。

### LT-CFM-C02

令大群组质量 0.9，coverage 为 $17/18\approx0.9444$；小群组质量 0.1，coverage 为 0.5。总体
$$
0.9(17/18)+0.1(0.5)=0.85+0.05=0.90.
$$
所以 marginal 90% 完全允许小群组只有 50%。定理没有对 $G$ 条件化；若要 group coverage，需预先分组校准或使用相应方法，并承担更大方差/集合。

### LT-CFM-C03

每个 score 单独固定时 rank argument成立；看同一 calibration labels 后挑最短且刚好覆盖的 score，使 score-selection function依赖这些 ranks，future score不再与“被挑选后的 calibration scores”对称。修复流：
$$
D_{\rm train}\to\text{fit base scores},\quad
D_{\rm tune}\to\text{choose score/hyperparameters},\quad
D_{\rm cal}^{\rm untouched}\to\widehat q,\quad
D_{\rm test}\to\text{audit}.
$$
或使用有显式 adaptive validity 理论的方法，不能继续引用基础 split theorem。

## D. 审计与诊断

### LT-CFM-D01

按 patient ID 互斥分 train/calibration/test；同一患者全部 visits 留在一侧。score 可聚合到 visit 或 patient event，但 coverage unit 必须明确；bootstrap/CI 也按 patient cluster。预注册 hospital/age/disease groups，报告 overall/group coverage、interval length quantiles、empty/full rate、visit count sensitivity 与 temporal/site shift。若目标是未来患者整段轨迹，需要 simultaneous event，不能用 visit marginal 代替。

### LT-CFM-D02

该方法 valid 但几乎无信息，接近全集 baseline。应报告 coverage–mean/median/quantile set size、coverage at fixed size、size-stratified error、empty/full-set rates、class/group set size、latency和 utility。与 simple conformal、APS、base top-$k$ 及全集比较；模型选择只能用 tuning data。coverage 是硬约束时，再在其下优化 efficiency。

### LT-CFM-D03

source calibration scores 与 target future score不再 exchangeable，故“future rank uniform”这一步断裂。covariate shift只变 $P(X)$ 且条件机制可能稳定，可在可估 density ratio 等假设下做 weighted variants；label shift变 priors；concept shift变 $P(Y\mid X)$，旧 score calibration通常无救；temporal dependence同时破坏置换对称。必须重新校准或使用有明确 shift/online 假设的扩展，“distribution-free”从不表示“任意关系-free”。

## E. 研究与迁移

### LT-CFM-E01

simple score $1-\widehat p_y$ 产生 probability-threshold set；APS 按概率排序，用累计质量到 true label 的 score，预测时纳入到 conformal threshold。按独立 source units 划分，预注册 calibration $m$ 与 $\alpha$；对概率 ties用稳定 label order或随机ized uniform并保存 seed。报告 marginal/classwise coverage、mean/quantile size、empty/full rate、per-class sample size和 repeated-split uncertainty；APS 常更 adaptive，但不保证每类 conditional validity。

### LT-CFM-E02

one-step 事件是 $Y_{t+1}\in C_t$，即使每步 95%，整条 $T$ 步全部覆盖概率也不是 95%，在独立近似下甚至约 $0.95^T$。trajectory tube 要对 $\max_t s_t$ 或 joint structured score conformalize，并定义 sequence/block exchangeability；时间依赖需 rolling/block/online 方法及 drift assumptions。控制安全还需 robust invariant set、emergency policy 和 cost，prediction coverage 不是 safety proof。

### LT-CFM-E03

card 写 exchangeable unit、proper train/tune/calibration/test sizes、score、基础模型、$k=\lceil(m+1)(1-\alpha)\rceil$ 和 ties convention、集合 inversion、marginal/group/simultaneous量词、coverage CI、length/size、empty/full rate、reuse history、shift/dependence。允许：“在声明的 exchangeable target population 上，此 split-conformal procedure 有有限样本 marginal coverage至少 $1-\alpha$。”拒绝 conditional、任意 shift、causal safety和高效率的自动外推。
