---
type: comparison
status: draft
area: [learning-theory/ensembles, bagging, random-forests, boosting]
aliases: [Ensemble Learning Theory, Bagging Random Forest Boosting, Tree Ensembles]
node_id: LT-48
prerequisites: ["[[决策树、分裂准则与剪枝]]", "[[偏差—方差—噪声分解]]", "[[一阶最优性条件与梯度下降]]", "[[统计模型、估计量与偏差方差]]", "[[随机变量的收敛与大数定律]]"]
related: ["[[在线学习、Boosting 与序列预测 MOC]]", "[[分类间隔、Margin Bound 与 SVM 接口]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
sources: ["[[S-1996-Breiman-Bagging-Predictors]]", "[[S-2001-Breiman-Random-Forests]]", "[[S-1997-Freund-Schapire-AdaBoost]]", "[[S-2001-Friedman-Gradient-Boosting]]", "[[S-2009-Hastie-Tibshirani-Friedman-ESL]]"]
exercises: ["[[习题 - Bagging、Random Forest 与 Boosting]]"]
solutions: ["[[解答 - Bagging、Random Forest 与 Boosting]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-ensemble-bagging-forest-boosting-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Bagging、Random Forest 与 Boosting

> [!abstract] 本章主问题
> “多训练几个模型再组合”掩盖了三种本质不同的 procedure：
>
> - **Bagging**：从同一 empirical distribution抽 bootstrap samples，平行训练 base algorithm，再平均/投票；
> - **Random Forest**：在 bootstrap之外，每个 node只看随机 feature subset，以牺牲部分 individual-tree strength换取更低 correlation；
> - **Boosting**：顺序构造 additive model，每轮针对当前 weighted mistakes或 negative functional gradient拟合新 learner。
>
> 增加 bagging/forest成员主要消除 conditional Monte Carlo error，不消除有限 dataset uncertainty；OOB predictions不是可无限复用的独立 test set；AdaBoost的指数更新与一般 gradient boosting的 pseudo-residual虽有关联，却不是同一算法。`bagging reduces variance`、`boosting reduces bias`只能作为常见机制直觉，不能当普遍定理。

> [!question] 初学者读完必须能回答
> 1. ideal bagged predictor对哪一个 randomness取 expectation？
> 2. bootstrap sample为什么平均只含约 \(63.2\%\) 不同 observations？
> 3. random forest增加树数到底收敛到什么？
> 4. feature subsampling为什么可能降低 correlation，也可能损害 tree strength？
> 5. AdaBoost 的 \(\alpha_m\) 与 weight update怎样从 exponential objective推出？
> 6. gradient boosting为什么是受 base-learner class限制的 function-space descent？

## 一、学习目标

1. formalize ideal/finite bagging与两层随机性；
2. 推导 exchangeable ensemble variance与 correlation floor；
3. 计算 bootstrap unique/OOB proportions；
4. 明确 OOB estimand与 adaptive reuse边界；
5. 定义 random forest的 row/feature randomization与 infinite-forest limit；
6. 推导 AdaBoost coefficient、weight update与 exponential training bound；
7. 推导 general gradient boosting pseudo-residual；
8. 解释 shrinkage、depth、subsampling与 early stopping；
9. 比较 bagging、RF、AdaBoost、gradient boosting的目标与错误机制；
10. 审计 probability calibration、feature importance、shift与 AI deployment。

## 二、统一 Ensemble 记号

base learning algorithm：

$$
A:S\mapsto f_S.
$$

ensemble members：

$$
f_1,\ldots,f_B.
$$

regression average：

$$
\overline f_B(x)
=
\frac1B\sum_{b=1}^B f_b(x).
$$

classification vote：

$$
\widehat h_B(x)
=
\operatorname{mode}
\{h_b(x)\}_{b=1}^B.
$$

probability average、logit average、majority vote与score sum不是相同 aggregation；对应 loss与 calibration不同。

## 三、Bagging 的概率对象

给定 observed sample

$$
S=(Z_1,\ldots,Z_n),
$$

bootstrap sample \(S^*\) 是从 empirical distribution

$$
\widehat P_n
=
\frac1n\sum_{i=1}^n\delta_{Z_i}
$$

有放回抽 \(n\) 次。

ideal bagged predictor：

$$
\boxed{
f_{\rm bag,S}(x)
=
E_*[A(S^*)(x)\mid S].}
$$

这里 expectation只对 conditional bootstrap randomness取，不对真实训练 dataset重新抽样。

finite Monte Carlo bagging：

$$
\boxed{
\widehat f_{B,S}(x)
=
\frac1B\sum_{b=1}^B
A(S_b^*)(x).}
$$

若 conditional on \(S\)，bootstrap draws独立：

$$
E_*[\widehat f_{B,S}(x)\mid S]
=f_{\rm bag,S}(x),
$$

$$
\operatorname{Var}_*
(\widehat f_{B,S}(x)\mid S)
=
\frac1B
\operatorname{Var}_*(A(S^*)(x)\mid S).
$$

增加 \(B\) 消除的是对 ideal conditional bootstrap expectation的 Monte Carlo approximation error。

## 四、两层 Variance 不要混写

完整 repeated-training randomness：

$$
\operatorname{Var}_{S,*}(\widehat f_{B,S}(x)).
$$

law of total variance：

$$
\boxed{
\operatorname{Var}_{S,*}(\widehat f_B)
=
\operatorname{Var}_S
[E_*(\widehat f_B\mid S)]
+
E_S
[\operatorname{Var}_*(\widehat f_B\mid S)].}
$$

第二项随 \(B\) 增长可下降；第一项是 ideal bagged procedure跨 datasets的 variance，不因同一 dataset再多生成 trees必然消失。

## 五、相关成员的 Ensemble Variance

在 repeated-data视角，固定 \(x\)，若 exchangeable members各有 variance \(v\)，pairwise correlation \(\rho\)：

$$
\operatorname{Cov}(f_b,f_{b'})
=\rho v
\quad(b\ne b').
$$

则

$$
\begin{aligned}
\operatorname{Var}(\overline f_B)
&=\frac1{B^2}
\left[
Bv+B(B-1)\rho v
\right]\\
&=
\boxed{
v\left[
\rho+
\frac{1-\rho}{B}
\right].}
\end{aligned}
$$

当 \(B\to\infty\)：

$$
\operatorname{Var}(\overline f_B)
\to\rho v.
$$

所以低 correlation与低 individual variance同样重要。该公式要求 equal variance/correlation的简化结构；classification vote无相同平方代数。

## 六、图解：三种集成机制

先回答：**为什么左/中栏可以平行训练，而右栏的第 \(m\) 个 learner必须等待前 \(m-1\) 轮？**

![[00-知识库管理/_assets/figures/learning-theory/fig-ensemble-bagging-forest-boosting-v2.svg|900]]

> [!figure] 图 20.6.8｜Bagging bootstrap平均、Random Forest去相关与 Boosting顺序下降
> 左栏把 observed sample变成多个 bootstrap replicates并平行 aggregate；中栏在 row resampling外加入 node-level feature randomization，区分 infinite-forest limit与 OOB role；右栏从当前 additive function计算 negative loss gradient，拟合新 learner再 shrinkage更新。来源：依据 Breiman bagging/random forests、Freund–Schapire与 Friedman独立绘制；确定性 SVG，由 [[plot_classical_models_ensemble_v2.py]] 生成。

**怎样读图。** bagging/forest成员条件于 data可独立并行生成；boosting的 pseudo-residual或 weights依当前 ensemble，所以顺序不可交换。三者都要用独立 protocol选择 member count、depth、feature subsampling与 stopping。

**图没有证明什么。** 它没有证明 bagging只降 variance、RF总优于 single tree、OOB可无限调参、Boosting只降 bias、training loss单调下降必然改善 test risk，或 forest vote proportion与 boosting sigmoid自动 calibrated。

## 七、Bootstrap 的 63.2% / 36.8% 现象

固定 observation \(i\)，一次 bootstrap draw不选到它的概率：

$$
1-\frac1n.
$$

连续 \(n\) 次都不选到：

$$
\boxed{
P_*(i\notin S^*)
=
\left(1-\frac1n\right)^n
\longrightarrow e^{-1}
\approx0.3679.}
$$

所以被至少选一次的概率：

$$
1-\left(1-\frac1n\right)^n
\to1-e^{-1}
\approx0.6321.
$$

注意 bootstrap sample仍有 \(n\) 个 draws，只是 unique observations约 \(0.632n\)；重复 multiplicities改变 training weights。

## 八、为什么 Bagging 帮助 Unstable Procedure

若小 sample perturbation使 \(A(S)\) 大幅变化，bootstrap distribution覆盖这些变化；平均可平滑 decision boundary或 split threshold。

trees、subset selection等常不稳定。对已经非常稳定、近线性的 estimator，bagging收益可能小；甚至在特定 bias结构下变差。

bagging不是“bootstrap自动增加有效数据”。所有 members仍来自同一 \(n\) observations，不能创造新 independent information。

## 九、Out-of-Bag Prediction

对 observation \(i\)，定义不包含它的 trees集合：

$$
\mathcal B_i
=
\{b:i\notin S_b^*\}.
$$

OOB regression prediction：

$$
\widehat f_i^{\rm OOB}
=
\frac1{|\mathcal B_i|}
\sum_{b\in\mathcal B_i}
f_b(x_i).
$$

OOB error：

$$
\widehat R_{\rm OOB}
=
\frac1n\sum_i
\ell(\widehat f_i^{\rm OOB},y_i).
$$

每个 prediction由未训练该 observation的 trees给出，因此避免直接 resubstitution。但：

- 每个 \(i\) 使用不同 subensemble；
- OOB predictions共享 trees/data，彼此相关；
- base trees训练在 bootstrap weighted sample，而不是 full empirical sample；
- groups/time dependence会泄漏相关 observations；
- 反复用 OOB选择 features/hyperparameters产生 adaptive overfitting；
- OOB score不是最终 untouched test的无限替代品。

## 十、Random Forest 定义

令 \(\Theta_b\) 包含：

- bootstrap row indices；
- 每个 node的 random feature subset；
- tie-breaking或其他 randomness。

tree：

$$
T_b(x)=T(x;S,\Theta_b).
$$

forest regression：

$$
\widehat f_B^{\rm RF}(x)
=
\frac1B\sum_{b=1}^B T(x;S,\Theta_b).
$$

classification通常投票或平均 class probabilities。

## 十一、Infinite-Forest Limit

conditional on \(S\)，若 \(\Theta_b\) i.i.d. 且 tree prediction integrable，law of large numbers给

$$
\boxed{
\widehat f_B^{\rm RF}(x)
\longrightarrow
E_\Theta[T(x;S,\Theta)\mid S]
\quad\text{a.s.}}
$$

当 \(B\to\infty\)，forest不会因树太多而产生新的 Monte Carlo overfitting；它趋于固定 data-dependent limit。但：

- limit仍可能有 approximation bias；
- dataset sampling error仍在；
- hyperparameters可能过拟合 validation/OOB；
- computation/latency增加；
- finite precision与 nondeterminism需审计。

## 十二、Feature Subsampling 的 Strength–Correlation Trade-off

如果每个 split都让所有 features竞争，强 predictor可能在多数 trees的 root出现，使 trees高度相关。只给随机 subset候选可：

- 强迫 alternative features参与；
- 改变 high-level partitions；
- 降低 pairwise error correlation；
- 提高 ensemble diversity。

但 \(m_{\rm try}\) 太小会经常排除真正 informative features，削弱 individual trees。最佳 \(m_{\rm try}\) 依 signal sparsity、feature correlation、interactions与 sample size。

“随机特征降低 variance”不是单向定理；它同时改变 base learner bias、strength与 correlation。

## 十三、Random Forest 不是 Bagged Pruned Trees 的同义词

典型 RF trees：

- bootstrap rows；
- node-level random feature candidates；
- often deep/unpruned；
- minimum leaf/feature count作为 regularization。

bagging可应用任何 base algorithm，也可 bag pruned trees。extremely randomized trees可能不用 bootstrap并随机 thresholds。名称相近不代表 procedure相同。

## 十四、Random-Forest Probability

两种常见 class probability：

1. vote fraction：预测某类的 trees比例；
2. average leaf proportion：各 tree leaf中的 class frequency再平均。

二者不同。class weights、balanced bootstrap与 minimum leaf size会改变 target。forest probabilities可 discrimination好但 over/under-confident；需 independent proper-score与 calibration评价。

## 十五、AdaBoost 对象

binary labels：

$$
y_i\in\{-1,+1\},
$$

weak learners：

$$
h_m(x)\in\{-1,+1\}.
$$

additive score：

$$
F_M(x)
=
\sum_{m=1}^M\alpha_mh_m(x).
$$

classifier：

$$
H_M(x)=\operatorname{sign}(F_M(x)).
$$

initialize：

$$
D_1(i)=\frac1n.
$$

## 十六、AdaBoost Weighted Error

第 \(m\) 轮，weak learner最小化 weighted misclassification：

$$
\varepsilon_m
=
\sum_{i=1}^n
D_m(i)
\mathbf1\{h_m(x_i)\ne y_i\}.
$$

假设

$$
0<\varepsilon_m<\frac12.
$$

选择 coefficient：

$$
\boxed{
\alpha_m
=
\frac12
\log\frac{1-\varepsilon_m}{\varepsilon_m}.}
$$

error越小，coefficient越大；若 \(\varepsilon_m=1/2\)，\(\alpha_m=0\)。若 error大于 \(1/2\)，可在 binary symmetric class中翻转 learner；实际 weak-learning合同需明确。

## 十七、AdaBoost Weight Update

$$
\boxed{
D_{m+1}(i)
=
\frac{
D_m(i)
\exp[-\alpha_my_ih_m(x_i)]
}{Z_m},}
$$

其中

$$
Z_m
=
\sum_iD_m(i)
\exp[-\alpha_my_ih_m(x_i)].
$$

- 正确分类：\(y_ih_m=+1\)，weight乘 \(e^{-\alpha_m}\)；
- 错误分类：\(y_ih_m=-1\)，weight乘 \(e^{+\alpha_m}\)。

normalization使 \(D_{m+1}\) 是 distribution。

## 十八、AdaBoost Coefficient 推导

固定当前 \(D_m\) 与 \(h_m\)，选择 \(\alpha\) 最小化 normalization/exponential stage objective：

$$
Z(\alpha)
=
(1-\varepsilon_m)e^{-\alpha}
+\varepsilon_me^{\alpha}.
$$

derivative：

$$
Z'(\alpha)
=
-(1-\varepsilon_m)e^{-\alpha}
+\varepsilon_me^{\alpha}.
$$

令零：

$$
e^{2\alpha}
=
\frac{1-\varepsilon_m}{\varepsilon_m},
$$

所以得到 \(\alpha_m\)。second derivative正，确为 minimizer。

最小值：

$$
Z_m
=
2\sqrt{\varepsilon_m(1-\varepsilon_m)}
<1
$$

若 \(\varepsilon_m<1/2\)。

## 十九、Exponential Loss 与 Training Error Bound

AdaBoost empirical exponential loss：

$$
\widehat L_{\exp}(F)
=
\frac1n\sum_i
e^{-y_iF(x_i)}.
$$

0–1 training error满足：

$$
\mathbf1\{y_iF(x_i)\le0\}
\le
e^{-y_iF(x_i)}.
$$

因此

$$
\boxed{
\widehat R_{01}(H_M)
\le
\widehat L_{\exp}(F_M).}
$$

通过 weight recursion可得

$$
\widehat L_{\exp}(F_M)
=
\prod_{m=1}^M Z_m.
$$

若每轮 \(\varepsilon_m\le1/2-\gamma\)，training error指数下降。该结论需要 weak-learning condition，且只直接控制 training error/exponential surrogate；population risk还需 margin/capacity/stability等桥。

## 二十、Margin View of Boosting

ensemble normalized/unnormalized margin：

$$
y_iF_M(x_i)
$$

或除以 \(\sum_m|\alpha_m|\)。即使 training error已为零，继续 boosting可增加许多 points的 margin，这解释部分 test improvement。但 noisy/outlier points可能持续获得巨大 weight；margin distribution、base class complexity与 stopping共同决定行为。

## 二十一、Gradient Boosting 的一般目标

additive function：

$$
F_M(x)
=
F_0(x)
+\sum_{m=1}^M
\nu\rho_m h_m(x),
$$

其中 \(0<\nu\le1\) 是 shrinkage。

empirical risk：

$$
\widehat R(F)
=
\frac1n\sum_{i=1}^n
\ell(y_i,F(x_i)).
$$

在当前 \(F_{m-1}\) 上，sample values的 negative gradient：

$$
\boxed{
r_{im}
=
-\left.
\frac{\partial\ell(y_i,F)}{\partial F}
\right|_{F=F_{m-1}(x_i)}.}
$$

选择 base learner拟合 pseudo-responses：

$$
h_m
\approx
\arg\min_{h\in\mathcal H_0}
\sum_i(r_{im}-h(x_i))^2.
$$

再 line search：

$$
\rho_m
\in
\arg\min_\rho
\sum_i
\ell(y_i,F_{m-1}(x_i)+\rho h_m(x_i)).
$$

更新：

$$
\boxed{
F_m=F_{m-1}+\nu\rho_mh_m.}
$$

这是受 base-learner class限制的 functional gradient approximation，不是能沿任意 function direction精确下降。

## 二十二、两个 Pseudo-Residual 例子

### 22.1 Squared Loss

取

$$
\ell(y,F)=\frac12(y-F)^2.
$$

则

$$
r_i=y_i-F(x_i),
$$

即 ordinary residual。新 tree拟合当前 residual。

### 22.2 Binary Logistic Loss

用 \(y\in\{0,1\}\)，logit \(F\)：

$$
\ell(y,F)
=
\log(1+e^F)-yF.
$$

$$
\frac{\partial\ell}{\partial F}
=
\sigma(F)-y.
$$

所以

$$
\boxed{
r_i=y_i-\sigma(F(x_i)).}
$$

即 observed label减当前 predicted probability。finite-depth tree只能近似这些 sample gradients的 structure。

## 二十三、Tree Boosting 的 Leaf Update

若第 \(m\) 棵 tree产生 regions \(R_{jm}\)：

$$
h_m(x)
=
\sum_{j=1}^{J_m}
c_{jm}\mathbf1\{x\in R_{jm}\}.
$$

可对每个 leaf选择

$$
c_{jm}
\in
\arg\min_c
\sum_{x_i\in R_{jm}}
\ell(y_i,F_{m-1}(x_i)+c).
$$

squared loss下是 residual mean；logistic/deviance下可能用 Newton approximation或专门 line search。

## 二十四、Second-Order Tree Boosting 接口

对增量 \(q(x_i)\)，Taylor approximation：

$$
\ell_i(F+q)
\approx
\ell_i(F)
+g_iq(x_i)
+\frac12h_iq(x_i)^2,
$$

其中

$$
g_i=\frac{\partial\ell_i}{\partial F},
\qquad
h_i=\frac{\partial^2\ell_i}{\partial F^2}.
$$

若 leaf \(R\) 的 constant weight是 \(w\)，加 \(L_2\) penalty \(\lambda w^2/2\)：

$$
G_R=\sum_{i\in R}g_i,
\qquad
H_R=\sum_{i\in R}h_i,
$$

optimal weight：

$$
\boxed{
w_R^\star
=
-\frac{G_R}{H_R+\lambda}.}
$$

split gain原型：

$$
\frac12
\left[
\frac{G_L^2}{H_L+\lambda}
+\frac{G_R^2}{H_R+\lambda}
-\frac{G_P^2}{H_P+\lambda}
\right]
-\gamma,
$$

其中 \(\gamma\) 是新增 leaf/split complexity cost。不同 libraries的 scaling、Hessian clipping、missing direction与 regularization convention不同。

## 二十五、Boosting 的 Regularization

有效 complexity由多个 knobs共同决定：

- rounds \(M\)；
- learning rate \(\nu\)；
- base tree depth/leaves；
- minimum leaf/Hessian；
- row subsampling；
- column subsampling；
- leaf-weight penalties；
- split gain penalty；
- early stopping；
- loss robustness。

小 \(\nu\) 常需更多 rounds；比较固定 rounds而不匹配 path length不公平。early stopping使用 validation feedback，是 model selection，不是无成本 optimizer detail。

## 二十六、Stochastic Gradient Boosting

每轮只用 row subsample拟合 pseudo-residual，可：

- 降低 computation；
- 注入 randomness；
- 减少 base learners correlation；
- 改变 optimization noise与 regularization。

但 time/group data不能普通 row subsample；rare classes可能在子样本中缺失。随机性与 sampling unit必须声明。

## 二十七、Bagging、RF 与 Boosting 对照

| 维度 | Bagging | Random Forest | Boosting |
|---|---|---|---|
| members | 条件于 data平行 | 条件于 data平行 | 顺序依赖 |
| perturbation | bootstrap rows | bootstrap + node feature subsets | residual/weight trajectory |
| aggregation | average/vote | average/vote | weighted additive score |
| base learner | 任意，unstable时更有益 | randomized trees | weak/shallow learners常见 |
| 主要直觉 | smoothing instability | strength–correlation balance | function-space loss descent |
| member count极限 | bootstrap expectation | random-tree expectation | optimization/regularization path继续变化 |
| internal evaluation | 可 OOB | 常用 OOB | validation/early stopping |
| probability | 不自动 calibrated | vote/leaf average不自动 calibrated | logistic loss有概率接口但仍需校准审计 |

## 二十八、Bias–Variance 口号的边界

常见说法：

- bagging/RF降低 variance；
- boosting降低 bias。

这有机制直觉，但非 universal theorem：

- averaging可改变 bias，bootstrap training-size/weighting也改变 target；
- random feature restriction可增加或减少 approximation bias；
- deep forests可同时改变 bias与 variance；
- boosting继续 rounds可降低 training bias同时放大 noise sensitivity；
- classification 0–1 loss没有简单平方分解。

应实际估计 repeated-data/seed variability、calibration与 regime-specific risk，而非只贴标签。

## 二十九、Noise、Outliers 与 Robust Loss

AdaBoost exponential loss对 large negative margin增长很快，mislabeled/outlier points可占据 weights。对策可能包括：

- shrinkage/early stopping；
- robust boosting losses；
- weight clipping；
- subsampling；
- label audit；
- minimum leaf。

这些改变 objective与 theory，不能只称“训练技巧”。

gradient boosting可用 Huber/quantile/logistic等 loss；robustness由 chosen loss与 data contamination model决定，不由“boosting”一词保证。

## 三十、Feature Importance 与解释

forest/boosted-tree impurity gain继承单树 candidate-count与correlation bias。permutation importance继承 off-support与substitute问题。boosting late trees可能在 residual细节上重复使用 feature，累计 gain不等于 causal effect。

解释应至少报告：

- importance definition；
- evaluation distribution；
- conditional/interventional background；
- correlated features；
- seeds/bootstrap variability；
- hyperparameter selection；
- subgroup/time stability。

## 三十一、Probability 与 Calibration

### 31.1 Forest

vote fraction不是由 proper scoring theorem推出的 \(P(Y=k\mid X=x)\)。leaf probability受 adaptive partitions、class weights与 small leaves影响。

### 31.2 Logistic Gradient Boosting

population unrestricted log-loss minimizer是 true logit，但 finite additive-tree class、regularization、early stopping与 shift引入 approximation/estimation error。sigmoid output仍需 independent calibration check。

### 31.3 Calibration Procedure

temperature/Platt/isotonic等 calibrator必须在未用于 ensemble fitting与 hyperparameter selection的数据上 fit，或放进 nested pipeline。calibration后 threshold再由 deployment cost选择。

## 三十二、Evaluation Protocol

1. 定义 sample unit/group/time；
2. 在 training fold内做 preprocessing；
3. bagging/RF选择 \(B\)、depth、leaf、mtry等；
4. boosting选择 loss、depth、\(\nu\)、subsampling、rounds；
5. OOB只承担预声明内部角色；
6. nested outer folds评价完整 selection procedure；
7. final untouched test只在冻结后使用；
8. 报告 seeds、mean/variance、latency与 memory；
9. probability任务报告 proper score/calibration；
10. shift/rare groups单独评价。

## 三十三、现代 AI 接口

### 33.1 Tabular Foundation Features

对 pretrained embeddings + metadata，tree ensembles可捕获 thresholds/interactions。但若 embeddings用 test/domain labels选择，固定-tree evaluation失效。high-dimensional dense embeddings的 distance/rotation geometry与 tree axis alignment也可能不匹配。

### 33.2 Reward / Preference Modeling

gradient-boosted trees可拟合 handcrafted/embedding features上的 preferences。pair sampling、annotator groups与 prompt shift定义 target；高 AUC不保证 reward calibrated或 policy optimization安全。

### 33.3 Cascades 与 Routing

forest uncertainty或 boosted score可触发 human review/model escalation。阈值必须结合 cost与 capacity；ensemble disagreement不是无条件 epistemic uncertainty。

### 33.4 Distillation 与 Rule Extraction

用 boosted/forest surrogate拟合 neural model可提高 tabular deployment效率，但 fidelity只在 sampled distribution上成立；必须测试 boundary/shift与rare cases。

### 33.5 Stacking 不是 Bagging

stacking用 meta-learner学习成员组合权重；训练 meta-features必须 out-of-fold，否则 severe leakage。simple averaging、Bayesian model averaging与 stacking的概率对象不同。

## 三十四、常见误区

> [!warning] 误区 1：bootstrap产生了更多独立数据
> 它只重加权同一 observations，不增加原始信息量。

> [!warning] 误区 2：树越多越不会过拟合任何东西
> tree count消除 Monte Carlo error；data/hyperparameter/OOB adaptive error仍在。

> [!warning] 误区 3：OOB 是可无限查看的 test set
> repeated adaptive reuse会选择性过拟合 OOB feedback。

> [!warning] 误区 4：random forest只是 bagging trees
> node-level feature randomization改变 strength、correlation与 partition distribution。

> [!warning] 误区 5：Boosting每轮拟合原始 labels
> 它拟合 weighted mistakes、pseudo-residual或 second-order objective，依当前 ensemble。

> [!warning] 误区 6：Boosting训练 loss下降，所以 test loss必降
> rounds是 regularization path；noise、capacity与 selection决定 generalization。

## 三十五、验收清单

1. base algorithm \(A\) 是什么？
2. randomness来自 data、bootstrap、features还是 solver？
3. aggregation是 mean、vote、probability还是 logit sum？
4. \(B\) 足以使 Monte Carlo error相对 data error小吗？
5. OOB estimand与复用规则是什么？
6. RF是否 bootstrap？mtry在哪一层抽？
7. single-tree strength与 pairwise correlation怎样？
8. AdaBoost weak error是否低于 \(1/2\)？
9. gradient boosting loss与 pseudo-residual是什么？
10. learning rate、rounds、depth如何 joint select？
11. early stopping data是否独立？
12. class weights/oversampling改变什么 probability target？
13. feature importance如何处理 correlation与 candidate bias？
14. group/time/shift结构是否进入 resampling？
15. probability、decision threshold与 calibration是否分开？

## 三十六、小结

集成学习的完整逻辑链：

1. bagging是 conditional bootstrap expectation的 Monte Carlo approximation；
2. 增加成员只直接降低 conditional Monte Carlo variance；
3. exchangeable members的 variance floor由 correlation决定；
4. bootstrap每次约保留 \(63.2\%\) unique observations，约 \(36.8\%\) OOB；
5. OOB避免 direct resubstitution，却不是无限可复用 test；
6. RF用 node-level feature randomization平衡 strength与 correlation；
7. infinite forest仍是 data-dependent predictor；
8. AdaBoost通过 weighted errors得到 \(\alpha_m\) 与 exponential weight update；
9. exponential loss upper-bound training 0–1 error；
10. gradient boosting拟合 negative functional gradient的 base-class approximation；
11. squared/logistic losses分别产生 residual与 label-minus-probability pseudo-residual；
12. shrinkage、depth、subsampling、penalties与 early stopping共同定义 estimator；
13. bagging降 variance、boosting降 bias不是 universal decomposition；
14. probabilities、importance与 uncertainty仍需独立评价；
15. AI deployment还需 group/time、shift、cost与 adaptive-selection审计。

真正掌握 ensembles，是能说清每个 member为何不同、能否并行、组合在哪个 scale、增加成员收敛到什么，以及 evaluation data被用了多少次。

## 来源与延伸

- [[S-1996-Breiman-Bagging-Predictors]]：bootstrap aggregation与 instability；
- [[S-2001-Breiman-Random-Forests]]：randomized trees、feature subsampling、strength/correlation与 forest limit；
- [[S-1997-Freund-Schapire-AdaBoost]]：decision-theoretic weight update与 weak-to-strong boosting；
- [[S-2001-Friedman-Gradient-Boosting]]：function-space gradient、pseudo-residual与 tree boosting；
- [[S-2009-Hastie-Tibshirani-Friedman-ESL]]：ensemble比较、loss与model assessment；
- [[决策树、分裂准则与剪枝]]：single-tree partition、pruning与 instability；
- [[在线学习、Boosting 与序列预测 MOC]]：multiplicative weights、regret与 boosting的后续统一。
