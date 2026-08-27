---
type: solution
status: draft
area: [learning-theory/k-means, clustering, unsupervised-learning]
topic: "[[习题 - K-Means、聚类风险与不可辨识性]]"
prerequisites: ["[[K-Means、聚类风险与不可辨识性]]"]
related: ["[[潜变量模型、混合模型与 EM]]", "[[PCA 的统计估计与主子空间风险]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - K-Means、聚类风险与不可辨识性

> [!warning] 解题原则
> K-Means objective定义的是unordered codebook和nearest-center distortion；Lloyd只是一个local search。任何“恢复cluster”结论必须说明 metric、representation、(K)、population uniqueness（modulo permutation）、global optimization gap和评价target。

## A. 识别与复述

### LT-KMEANS-A01

对 (C=\{c_1,\ldots,c_K\}\subset\mathbb R^d)，population risk为

$$
R(C)=E\left[\min_{k\le K}\|X-c_k\|^2\right],
$$

empirical distortion可写mean或sum：

$$
\widehat R_n(C)=\frac1n\sum_{i=1}^n\min_k\|X_i-c_k\|^2.
$$

unordered centers是codebook；给定tie rule后，Voronoi cell为

$$
V_k(C)=\{x:\|x-c_k\|\le\|x-c_j\|,\ \forall j\}.
$$

global empirical minimizer是 (\arg\min_C\widehat R_n(C)) 中的元素；Lloyd输出是从特定initialization经 alternating assignments/means得到的fixed point，可能只是local optimum或degenerate stationary configuration。算法输出不应被定义成全局ERM。

### LT-KMEANS-A02

- label permutation：重排center indices不改变codebook/risk，是representation symmetry；
- empty cluster：当前assignment没有point给某center，其mean update未定义，需要明确reinitialization/drop policy；
- duplicate centers：两个centers重合，assignment依赖ties，effective number of cells可能少于 (K)；
- multiple global optima：除permutation外，数据/分布symmetry可产生几何不同但同risk的codebooks。

前两项可发生于算法iterate；后两项可能反映population/objective本身不唯一。报告时要区分。

### LT-KMEANS-A03

internal metric只用features与assignments，如 distortion、silhouette；external metric把clusters与独立labels/known structure比较，如 adjusted Rand index；downstream utility检验cluster/code是否改善retrieval、compression、routing或prediction。

silhouette高只表示所选representation与metric下 points相对本cluster更近、相对其他cluster更远。它不证明：(K) 对应自然类别、cluster有causal/semantic意义、labels稳定于shift、或partition对实际task有用。一个人为加入巨大scale的无意义feature也可制造分离良好的clusters。

## B. 手算与数值判断

### LT-KMEANS-B01

初始centers为 (c_1=0,c_2=9)。nearest assignment：

$$
A_1=\{0,2\},
\qquad
A_2=\{9,11\}.
$$

更新前sum distortion：

$$
(0-0)^2+(2-0)^2+(9-9)^2+(11-9)^2=8.
$$

mean update：

$$
c_1'=1,
\qquad c_2'=10.
$$

assignment不变，更新后：

$$
(0-1)^2+(2-1)^2+(9-10)^2+(11-10)^2
=\boxed4.
$$

这也是global optimum (C^\star=\{1,10\})（modulo permutation），mean empirical distortion为 (4/4=1)。可枚举一维有序数据的contiguous two-way splits验证：在 0|2,9,11 处后三点SSE为 (134/3)；在 0,2,9|11 处同理很大，middle split最优。

### LT-KMEANS-B02

令 (\bar x_A=|A|^{-1}\sum_{x\in A}x)。对任意 (c)，ANOVA identity：

$$
\sum_{x\in A}\|x-c\|^2
=
\sum_{x\in A}\|x-\bar x_A\|^2
+|A|\|c-\bar x_A\|^2.
$$

cross term因 (\sum(x-\bar x_A)=0) 消失，故unique minimizer为 (c=\bar x_A)（nonempty cluster）。

对 (A=\{2,9,11\})：

$$
\bar x_A=22/3.
$$

SSE为

$$
\left(-\frac{16}3\right)^2
+\left(\frac53\right)^2
+\left(\frac{11}3\right)^2
=\frac{402}{9}
=\boxed{\frac{134}3\approx44.67}.
$$

### LT-KMEANS-B03

若机械按列出的index比较：

$$
\|(10.5,0)-(0,0)\|^2
+\|(0.5,0)-(10,0)\|^2
=110.25+90.25
=\boxed{200.5}.
$$

允许permutation匹配，交换估计center编号：

$$
\|(0.5,0)-(0,0)\|^2
+\|(10.5,0)-(10,0)\|^2
=0.25+0.25
=\boxed{0.5}.
$$

naive error主要测量了label convention，而不是codebook estimation。

## C. 推导与证明

### LT-KMEANS-C01

设当前centers为 (C^{(t)})。assignment step对每个 (x_i) 选择最近center：

$$
z_i^{(t+1)}\in\arg\min_k\|x_i-c_k^{(t)}\|^2.
$$

逐点最小化使固定centers下总distortion不增加。

update step对每个nonempty assignment set (A_k) 选择

$$
c_k^{(t+1)}=\frac1{|A_k|}\sum_{i\in A_k}x_i.
$$

由mean的least-squares最优性，它在固定assignments下最小化该cluster SSE，所以总distortion再次不增加。因此

$$
\widehat R(C^{(t+1)})\le\widehat R(C^{(t)}).
$$

但 alternating minimization只分别对一个block优化；joint objective nonconvex，不同initialization可能到达不同fixed points。单调序列只保证不向上，并不保证到达所有codebooks中的global minimum；ties与empty-cluster policy还需单独处理。

### LT-KMEANS-C02

对任意 permutation (\pi)：

$$
\min_k\|x-c_{\pi(k)}\|^2
=\min_j\|x-c_j\|^2,
$$

故 (R(\pi C)=R(C))。一个 permutation-invariant loss是

$$
d^2(C,C^\star)
=
\min_{\pi\in S_K}
\sum_{k=1}^K\|c_k-c_{\pi(k)}^\star\|^2.
$$

若population minimizer set为

$$
\mathcal C^\star=\arg\min_CR(C),
$$

且不只含一个permutation orbit，consistency应写成

$$
\operatorname{dist}(\widehat C_n,\mathcal C^\star)
\xrightarrow{p}0,
$$

而非武断选择某个 (C^\star)。也可陈述risk consistency：

$$
R(\widehat C_n)\to\inf_CR(C).
$$

### LT-KMEANS-C03

对限制在compact set中的candidate codebooks，证明架构是：

1. **uniform convergence**：
   $$
   \sup_C|\widehat R_n(C)-R(C)|\xrightarrow{p}0;
   $$
2. **separation/identification**：离 population minimizer set至少 (\varepsilon) 的codebooks有正risk gap；
3. **argmin transfer**：global empirical minimizer $\widehat C_n$ 的 population risk 接近最优，由 separation 推出到 minimizer set 的 distance 趋零。

还需 moments/existence、center boundedness与measurability等条件。

Lloyd输出 (\widetilde C_n) 未必满足

$$
\widehat R_n(\widetilde C_n)
\le\inf_C\widehat R_n(C)+o_p(1).
$$

uniform convergence只能把统计误差转移给近似global empirical minimizer；它不会自动消掉optimization error。要继承结论，必须证明多重restart/algorithm使 empirical optimality gap也趋零，或直接把algorithmic target纳入声明。

## D. 边界、反例与纠错

### LT-KMEANS-D01

几何上，若有三个well-separated groups而 (K=2)，两个initial centers若都落在同一大group，第一次assignment可能让其中一个center服务该group的一部分，另一个center被远处两groups共同拉到中间；后续partition可稳定在较差basin。更极端时empty cluster handling会固定坏配置。

k-means++按 squared distance选择新seeds，减少多个seeds挤在同一区域的概率，并对初始 expected distortion给出相对global optimum的 (O(\log K)) approximation保证。它不保证：

- 每次得到global optimum；
- Lloyd更新后恢复population truth；
- 所选 (K)/metric/representation有语义；
- shift下稳定；
- 对outliers robust。

### LT-KMEANS-D02

取四点近似矩形：

$$
(0,0),(0,1),(10,0),(10,1).
$$

(K=2) 时raw Euclidean metric倾向按 (x) 左右分组。若把 (y) 乘100，vertical distance变为100，最优partition会倾向按 (y) 上下分组。coordinate units定义了objective geometry。

standardization把每feature按sample scale归一，只是另一种metric choice。若某feature noise很小、某feature的绝对unit具有任务意义，或data有outliers，z-score未必合适；并且scaler必须在training fold拟合。

### LT-KMEANS-D03

cluster id不等于latent truth，因为：

1. K-Means只优化chosen representation中的squared Euclidean distortion；
2. representation可能丢失或人为放大semantic factors；
3. 不同 (K) 给出不同粒度；
4. label permutation使编号本身无意义；
5. non-spherical、unequal-density groups未必由Voronoi cells描述；
6. 同一objects可按topic、style、language或user utility形成不同合法partitions；
7. local initialization与outliers会改变结果。

语义必须由independent annotations、interventions或downstream task验证，不能由低distortion自我认证。

## E. AI 迁移

### LT-KMEANS-E01

vector-quantization protocol：

- 用training embeddings拟合codebook，validation选择 (K)、metric、normalization与restart count；
- 记录train/held-out quantization distortion及分位数；
- 报告每个code的usage、entropy、dead/near-duplicate codes；
- 多seeds做permutation-matched codebook/assignment stability；
- 评价reconstruction或decoder质量、retrieval/latency等真实utility；
- 防止test embeddings参与normalization/codebook；
- 对domain/time shift监控nearest-code distance、usage drift和downstream degradation；
- 展示outliers与少数groups是否被系统性高distortion覆盖。

### LT-KMEANS-E02

把development data外层分成train/outer-validation或grouped folds。在inner training中：

1. 训练representation；
2. 比较K-Means initializations/restarts/(K)；
3. 用inner validation的routing load、task loss与stability选一次；
4. 固定选择规则后，在outer training重新拟合codebook/router；
5. outer split只评价task utility、expert load、calibration与failure groups。

若看outer结果后继续改initialization，outer已变成development signal，需全新test。hard routing还应报告ties、dead experts和capacity overflow。

### LT-KMEANS-E03

最小report字段：

1. observation/group/time unit与sampling frame；
2. representation生成方式及其training data；
3. distance metric、normalization与feature weights；
4. (K) 的候选集与选择target；
5. initialization、restarts、seed与empty-cluster policy；
6. best/median/worst empirical distortion和近似optimization gap；
7. permutation-matched center/assignment stability；
8. internal指标及其限制；
9. independent external labels（若有）与匹配协议；
10. downstream held-out utility；
11. group/domain/time shift；
12. cluster命名、stereotyping与自动决策的伦理风险。
