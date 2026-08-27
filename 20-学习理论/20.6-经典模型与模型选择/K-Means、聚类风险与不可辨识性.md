---
type: theorem
status: draft
area: [learning-theory/k-means, clustering, quantization, nonidentifiability]
aliases: [K-Means Statistical Theory, Clustering Risk, Vector Quantization]
node_id: LT-50
prerequisites: ["[[损失、总体风险与经验风险]]", "[[统计模型、估计量与偏差方差]]", "[[PCA 的统计估计与主子空间风险]]", "[[随机变量的收敛与大数定律]]"]
related: ["[[潜变量模型、混合模型与 EM]]", "[[No-Free-Lunch 与归纳偏置]]", "[[表示学习的任务、表示与下游风险]]", "[[度量学习、相似性与检索风险]]"]
sources: ["[[S-1981-Pollard-KMeans-Consistency]]", "[[S-2007-Arthur-Vassilvitskii-KMeansPP]]", "[[S-2002-Kleinberg-Clustering-Impossibility]]", "[[S-2009-Hastie-Tibshirani-Friedman-ESL]]"]
exercises: ["[[习题 - K-Means、聚类风险与不可辨识性]]"]
solutions: ["[[解答 - K-Means、聚类风险与不可辨识性]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-kmeans-risk-nonidentifiability-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# K-Means、聚类风险与不可辨识性

> [!abstract] 本章主问题
> K-Means不是“自动发现数据中的真实类别”，而是一个明确的 Euclidean quantization problem：
>
> $$
> \min_{c_1,\ldots,c_K}
> E\min_{1\le k\le K}\|X-c_k\|^2.
> $$
>
> 这一定义带来五个必须分开的层：
>
> 1. **objective**：nearest-center squared-distance risk；
> 2. **algorithm**：Lloyd assignment/mean updates，只做局部交替下降；
> 3. **statistics**：empirical global minimizer何时逼近 population minimizer；
> 4. **identifiability**：center set只定义到 permutation，population optimum还可能不唯一；
> 5. **semantics**：low distortion不自动等于 ground-truth classes、causal types或 useful routing。
>
> representation、metric、scaling、\(K\)、initialization与evaluation共同定义答案。

> [!question] 初学者读完必须能回答
> 1. 为什么固定 assignments时 center一定是 sample mean？
> 2. Lloyd每轮为什么不增加 empirical objective？
> 3. 为什么这不证明找到 global optimum？
> 4. center labels为何不可辨识，怎样定义 permutation-invariant loss？
> 5. Pollard式 consistency为什么不等于 semantic label recovery？
> 6. internal、external与downstream clustering metrics分别回答什么？

## 一、学习目标

1. 把 K-Means写成 unordered center-set risk；
2. 推导 Voronoi assignment与 cluster mean update；
3. 证明 Lloyd objective monotonicity；
4. 区分 local fixed point、global empirical optimum与population optimum；
5. 解释 label permutation、duplicate/empty centers与 nonunique optima；
6. 陈述 K-Means consistency所需的核心条件；
7. 理解 k-means++ seeding guarantee的对象；
8. 比较 distortion、silhouette、ARI/NMI与downstream utility；
9. 审计 feature scale、outliers、\(K\) selection与 representation leakage；
10. 将 K-Means连接到 vector quantization、codebook与AI routing。

## 二、Population Quantization Object

令

$$
X\in\mathbb R^d,
\qquad
E\|X\|^2<\infty.
$$

一个 \(K\)-center codebook是 unordered set

$$
C=\{c_1,\ldots,c_K\}
\subset\mathbb R^d.
$$

到 center set 的距离：

$$
d(x,C)
=
\min_{c\in C}\|x-c\|_2.
$$

population K-Means risk：

$$
\boxed{
R(C)
=
E[d(X,C)^2]
=
E\min_{1\le k\le K}\|X-c_k\|^2.
}
$$

population optimal value：

$$
R_K^*
=
\inf_{|C|\le K}R(C).
$$

最优 center set集合：

$$
\mathcal C_K^*
=
\arg\min_{|C|\le K}R(C).
$$

这里允许 \(|C|\le K\) 可自然处理 duplicate centers；若要求恰好 \(K\) 个 distinct centers，需要额外 existence/separation条件。

> [!important] 参数顺序没有统计意义
> \((c_1,c_2)\) 与 \((c_2,c_1)\) 定义同一 center set与同一 predictor。parameter tuple不是 identifiable object，至少要 quotient by permutations。

## 三、Empirical Risk

样本 \(S=(X_1,\ldots,X_n)\)。empirical distortion：

$$
\widehat R_n(C)
=
\frac1n\sum_{i=1}^n
\min_{1\le k\le K}\|X_i-c_k\|^2.
$$

global empirical minimizer：

$$
\widehat C_n^{\mathrm{ERM}}
\in
\arg\min_C\widehat R_n(C).
$$

实际 Lloyd output记为

$$
\widetilde C_n
=
A(S,U,\text{init},\text{ties},\text{stopping}),
$$

其中 \(U\) 表示 random seed。通常

$$
\widehat R_n(\widetilde C_n)
\ge
\widehat R_n(\widehat C_n^{\mathrm{ERM}}).
$$

所以任何 global-ERM consistency theorem若要应用到 Lloyd，必须另控制 optimization gap：

$$
\rho_n
=
\widehat R_n(\widetilde C_n)
-
\inf_C\widehat R_n(C).
$$

## 四、Voronoi Assignment

给定 distinct centers，定义 cell：

$$
V_k(C)
=
\left\{
x:
\|x-c_k\|^2
\le
\|x-c_j\|^2,\ \forall j
\right\}.
$$

两个 centers的 boundary满足

$$
\|x-c_k\|^2=\|x-c_j\|^2.
$$

展开并消去 \(\|x\|^2\)：

$$
2(c_j-c_k)^Tx
=
\|c_j\|^2-\|c_k\|^2.
$$

因此 Euclidean K-Means cells由 hyperplanes分隔，是 convex polyhedra。若使用 cosine、Mahalanobis、manifold或 learned distance，cell geometry会改变。

ties必须有 deterministic或random rule；ties具有正概率时，assignment itself可能不唯一。

## 五、固定 Assignment 时 Center 为什么是 Mean

给定 nonempty cluster index set \(I_k\)，考虑

$$
Q_k(c)
=
\sum_{i\in I_k}\|X_i-c\|^2.
$$

展开：

$$
\nabla_cQ_k(c)
=
2|I_k|c
-
2\sum_{i\in I_k}X_i.
$$

令 gradient为零：

$$
\boxed{
c_k
=
\frac1{|I_k|}
\sum_{i\in I_k}X_i.
}
$$

Hessian为

$$
2|I_k|I_d\succ0,
$$

所以 mean是唯一 minimizer。

ANOVA identity：

$$
\sum_{i\in I_k}\|X_i-c\|^2
=
\sum_{i\in I_k}\|X_i-\bar X_k\|^2
+
|I_k|\|c-\bar X_k\|^2.
$$

这同时给出证明而不依微分。

## 六、Lloyd Algorithm

给 initial centers \(C^{(0)}\)，重复：

### Assignment Step

$$
z_i^{(t)}
\in
\arg\min_{1\le k\le K}
\|X_i-c_k^{(t)}\|^2.
$$

### Update Step

$$
c_k^{(t+1)}
=
\frac{
\sum_i\mathbf 1\{z_i^{(t)}=k\}X_i
}{
\sum_i\mathbf 1\{z_i^{(t)}=k\}
}.
$$

empty cluster时 denominator为零，必须声明 reinitialization/drop/split rule。

### 为什么 Objective 不增

定义 joint objective：

$$
J(z,C)
=
\frac1n\sum_i\|X_i-c_{z_i}\|^2.
$$

assignment step对 fixed \(C^{(t)}\) 最小化 \(z\)：

$$
J(z^{(t)},C^{(t)})
\le
J(z^{(t-1)},C^{(t)}).
$$

update step对 fixed \(z^{(t)}\) 最小化 \(C\)：

$$
J(z^{(t)},C^{(t+1)})
\le
J(z^{(t)},C^{(t)}).
$$

合并：

$$
\boxed{
\widehat R_n(C^{(t+1)})
\le
\widehat R_n(C^{(t)}).
}
$$

但 \(J(z,C)\) joint nonconvex；coordinatewise minimum不必是 global minimum。ties、empty-cluster处理与 finite precision还会影响 exact monotonicity/termination。

## 七、图：Objective、Algorithm 与 Semantics

先看图回答：如果两次运行得到相同 distortion但 center编号相反，它们是两个不同模型吗？

![[00-知识库管理/_assets/figures/learning-theory/fig-kmeans-risk-nonidentifiability-v2.svg|900]]

> [!figure] 图 20.6-10　K-Means 的量化目标、Lloyd 局部下降与三类评价
> 左栏把 center set与Voronoi partition连接到 population distortion；中栏显示 assignment与mean updates交替不增 empirical objective，但终点仅是 local fixed point；右栏区分 internal geometry、external labels与downstream utility，并强调 \(K\)、metric和representation都是inductive bias。来源：依据 Pollard、Arthur–Vassilvitskii、Kleinberg与ESL独立绘制；确定性 SVG，由 [[plot_classical_models_unsupervised_v2.py]] 生成。

**怎样读图**：左栏的 cluster编号没有含义；中栏每个 arrow只证明固定另一 block时的改进；右栏三种 metrics可以给出不同排序，因为它们评价不同对象。

**图没有证明什么**：图没有证明任意 dataset含“天然 \(K\) 类”，没有证明 Lloyd会找到global optimum，也没有证明 geometric clusters与human categories或causal populations一致。

## 八、一个一维手算

数据：

$$
x=(0,2,9,11),
\qquad
K=2.
$$

考虑 partition

$$
\{0,2\},
\qquad
\{9,11\}.
$$

centers：

$$
c_1=1,
\qquad
c_2=10.
$$

sum distortion：

$$
(0-1)^2+(2-1)^2+(9-10)^2+(11-10)^2
=
4.
$$

mean empirical risk为

$$
\widehat R_n=4/4=1.
$$

另一 partition

$$
\{0\},
\qquad
\{2,9,11\}
$$

给

$$
c_1=0,
\qquad
c_2=\frac{22}{3}.
$$

sum distortion：

$$
\left(2-\frac{22}{3}\right)^2
+
\left(9-\frac{22}{3}\right)^2
+
\left(11-\frac{22}{3}\right)^2
=
\frac{134}{3}
\approx44.67.
$$

所以前者更好。但这个比较只对 observed points与squared distance成立；它没有外部类别证据。

## 九、Initialization 与 k-means++

Lloyd output高度依 initial centers。k-means++：

1. 从 data points均匀选第一个 center；
2. 对每点定义到当前 centers的 squared distance
   $$
   D(x)^2;
   $$
3. 按 \(D(x)^2\) 比例抽下一个 center；
4. 重复到 \(K\) 个，再运行 Lloyd。

其经典 guarantee针对随机 seeding后的 expected empirical potential：

$$
E[\Phi(C_{\mathrm{seed}})]
\le
O(\log K)\Phi^*.
$$

精确经典常数是 \(8(\log K+2)\) 类型，依 theorem convention。随后 Lloyd只会继续降低 \(\Phi\)。

但不要越界：

- approximation比较 empirical K-Means objective；
- 不是 population risk guarantee；
- 不是 semantic label recovery；
- 不是 stability或calibration theorem；
- 多次 restart后选最低 training distortion又形成 adaptive search，应在外层评估。

## 十、不可辨识性的四种来源

### 10.1 Label Permutation

任意 permutation \(\pi\)：

$$
(c_1,\ldots,c_K)
\mapsto
(c_{\pi(1)},\ldots,c_{\pi(K)})
$$

不改变 distribution-free K-Means predictor。比较 center tuples前应做 optimal matching：

$$
d_{\mathrm{match}}(C,\widetilde C)
=
\min_{\pi\in S_K}
\left(
\sum_{k=1}^K
\|c_k-\widetilde c_{\pi(k)}\|^2
\right)^{1/2}.
$$

### 10.2 Duplicate / Empty Centers

若 \(K\) 大于 effective number of groups，多个 centers可重合或某些 centers没有 Voronoi mass。此时 parameter tuple维数并不等于有效复杂度。

### 10.3 Symmetric Population Optima

例如 isotropic circle distribution与 \(K=2\)，任意穿过中心的对称 axis可产生旋转等价 optima。没有唯一 target center set。

### 10.4 Representation Symmetry

对所有数据与centers施加同一 orthogonal transform不改变 Euclidean distortion。若 representation本身只定义到 rotation，单坐标 center interpretation不稳定。

## 十一、Population Consistency 到底说什么

Pollard式结论的结构是：

- \(X_i\) i.i.d.；
- finite second moment；
- population optimal center sets满足适当存在、唯一/分离条件；
- 研究 global empirical minimizers；

则经验最优 center set可 almost surely趋向 population optimum（常按 unordered-set metric）。

每个条件都重要：

1. **global minimizer**：普通单次 Lloyd不满足；
2. **unique optimum**：对称/重复结构下可能失败；
3. **finite moment**：squared loss对heavy tails敏感；
4. **fixed distribution**：shift下 target本身改变；
5. **fixed \(K,d\)**：随 \(n\) adaptive增长需新分析。

而且 center-set consistency不推出：

$$
P(\widehat z(X)=Z_{\mathrm{true}})\to1.
$$

后者需要一个包含真实 latent labels的 generative model、separation与identification assumptions。

## 十二、为什么“真实聚类”不是默认对象

无监督 data只给 \(P_X\)，没有 canonical label variable。不同结构可产生不同合理聚类：

- elongated group可按density mode、Euclidean variance或semantic class切；
- hierarchical data在不同scale有不同 partitions；
- continuous manifold未必存在离散 classes；
- rare subgroup可能被 distortion objective忽略；
- feature transform会改变 nearest-center geometry。

Kleinberg式 impossibility theorem表明一组直觉 clustering axioms不能同时满足。其意义不是“聚类不可能”，而是必须声明 inductive bias与trade-off。

## 十三、三类 Evaluation

### 13.1 Internal

- within-cluster distortion；
- silhouette；
- between/within separation；
- stability under resampling。

它们只看 geometry，可能偏好 compact/spherical/equal-density groups。

### 13.2 External

有 reference labels时：

- adjusted Rand index；
- normalized mutual information；
- matching accuracy。

这些评价 label agreement；labels本身可能粗糙、多义或与K-Means geometry不兼容。

### 13.3 Downstream Utility

- retrieval precision；
- routing reward/latency；
- codebook reconstruction；
- anomaly detection utility；
- human interpretability。

deployment metric往往比“是否像类别”更重要。

> [!warning] 不同 Metrics 不能用一个“聚类质量”概括
> 低 distortion、high ARI与high downstream utility可能互相冲突。报告必须先写 estimand。

## 十四、\(K\) 的选择

随着 \(K\) 增大：

$$
R_{K+1}^*
\le
R_K^*.
$$

training distortion单调下降，所以不能直接取最小值选择 \(K\)。

常见路线：

- elbow：主观，需预声明 rule；
- silhouette：隐含 compact separation偏好；
- gap statistic：依 reference null；
- stability：不稳定可能来自 nonidentifiability，也可能来自真实连续结构；
- mixture likelihood/BIC：改变为 generative model；
- held-out quantization：评价新数据 reconstruction；
- downstream validation：选择task-specific \(K\)。

从多个 \(K\)、metrics、representations和seeds中挑最好会产生多重 selection optimism，需要 nested/untouched test。

## 十五、Feature Scaling、Metric 与 Outliers

K-Means目标不是 coordinate-free：

$$
\|Dx-Dc\|^2
=
(x-c)^TD^2(x-c).
$$

所以 standardization等价于选择 diagonal Mahalanobis metric。

outlier \(x_o\) 的 squared contribution：

$$
\min_k\|x_o-c_k\|^2
$$

可随距离平方增长，拉动 center。robust alternatives包括 trimmed K-Means、K-medians、medoids、Huberized loss，但它们改变 target。

cosine spherical K-Means通常先 normalize points/centers并优化方向相似度；不能把其输出解释成 ordinary Euclidean K-Means theorem。

## 十六、Computation

每次 dense Lloyd iteration约需：

$$
O(nKd)
$$

distance work与 \(O(Kd)\) centers storage（不含 data）。

工程路线：

- mini-batch K-Means；
- triangle-inequality pruning；
- approximate nearest-center search；
- distributed sufficient statistics；
- streaming center updates；
- quantized distance kernels。

这些改变 approximation、randomness与possibly estimator。报告 iteration count不够，还要给 objective gap proxy、seed variability、empty clusters与wall-clock/communication。

## 十七、AI 接口

### 17.1 Vector Quantization

encoder输出 \(h(x)\)，codebook \(C\)，quantized vector：

$$
q(h)
=
\arg\min_{c_k\in C}\|h-c_k\|^2.
$$

若 encoder与codebook joint training，representation会适配 assignments；fixed-data K-Means consistency不再直接适用。还要处理 straight-through gradient、commitment loss、dead codes与usage entropy。

### 17.2 Embedding Clustering

cluster LLM/document embeddings前要冻结：

- checkpoint/pooling；
- normalization；
- corpus sampling；
- deduplication；
- metric；
- \(K\) selection；
- seed/restart budget。

同一 document的chunks跨 split会导致 stability/external evaluation泄漏。

### 17.3 Expert Routing

K-Means可生成 router prototypes，但 nearest center不等于 best expert。需要 held-out route reward、load balance、capacity、fallback与shift tests。高频 cluster可能垄断capacity；rare safety requests可能被压到错误center。

### 17.4 Pseudo-Labels

用 clusters作为 labels训练 classifier会把 K-Means geometry bias固化。classification accuracy对 pseudo-labels只证明复现cluster assignment，不证明真实 semantics。

## 十八、一个完整 Protocol

1. 按 user/document/time group切 outer train/test；
2. 只在 train拟合 representation normalization/PCA；
3. inner folds选择 metric、\(K\)、seeding、restart与stopping；
4. 对同一 candidate报告多个 seeds的 distortion与center matching stability；
5. 若有 labels，仅用于明确的external validation，不反向偷偷调无监督 pipeline；
6. final test同时报告 held-out distortion、external metric、downstream utility与 subgroup；
7. deployment监控 center occupancy、distance distribution、empty/dead codes与 drift；
8. 保存 codebook version与matching rule。

## 十九、常见错误

### 错误 1：Lloyd Converged，所以全局最优

它只说明 assignment/mean updates达到 local fixed point或stopping tolerance。

### 错误 2：Distortion 低，所以找到了真实类别

distortion只评价 declared metric下的 quantization。

### 错误 3：Cluster 1跨运行仍应是同一类

labels可 permutation；需 matching。

### 错误 4：k-means++ 保证语义正确

它保证的是 empirical potential approximation。

### 错误 5：无监督 preprocessing不用放进 CV

validation features影响 representation/centers同样会泄漏。

## 二十、审计清单

1. input representation与sampling unit是什么？
2. metric、normalization与feature weights是什么？
3. \(K\) 怎样选择？
4. center set是否按 permutation-invariant metric比较？
5. 算法是global ERM approximation还是单次 Lloyd？
6. initialization/restarts/ties/empty clusters如何处理？
7. population optimum是否唯一？
8. internal、external、downstream评价分别是什么？
9. outliers、rare groups与shift如何处理？
10. pipeline是否完全嵌套在split内？

## 二十一、本章掌握标准

### A. 识别

能区分 center set、Voronoi partition、assignment labels、global ERM与Lloyd output。

### B. 计算

能手算一轮 assignment/mean update、distortion与permutation matching。

### C. 推导

能证明 cluster mean最优与Lloyd monotonicity，并陈述 consistency的对象条件。

### D. 边界

能构造 local optimum、symmetric nonunique optimum、scale dependence与semantic mismatch。

### E. AI 迁移

能为embedding clustering/vector quantization/router设计nested、grouped、shift-aware评估。

对应训练：[[习题 - K-Means、聚类风险与不可辨识性]]  
独立详解：[[解答 - K-Means、聚类风险与不可辨识性]]

## 二十二、最小记忆

1. K-Means优化 nearest-center squared-distance risk；
2. fixed assignment的最优 center是mean；
3. Lloyd交替不增 training distortion；
4. 不增不等于global optimum；
5. center labels只定义到permutation；
6. unique population optimum是强条件；
7. global empirical consistency不自动适用于single Lloyd run；
8. k-means++保证的是objective initialization；
9. internal/external/downstream metrics不能混称；
10. representation、metric、\(K\)、seed与split共同定义聚类结果。
