---
type: concept
status: verified
area: [generative-models, evaluation, likelihood, fid, kid, precision-recall, human-evaluation]
node_id: GEN-71
prerequisites: ["[[最大似然、交叉熵与前向 KL]]", "[[协方差、相关性与条件期望]]", "[[f-散度、Bregman 散度与概率度量]]"]
related: ["[[生成模型实验协议、FD Loss 与前沿证据地图]]", "[[条件生成、Bayes 分解与 Classifier Guidance]]"]
sources: ["[[S-2017-Heusel-FID]]", "[[S-2018-Binkowski-KID]]", "[[S-2018-Sajjadi-Precision-Recall]]", "[[S-2019-Kynkaanniemi-Improved-Precision-Recall]]", "[[S-2022-Parmar-CleanFID]]", "[[S-2026-Su-11738-FD-Loss]]"]
exercises: ["[[习题 - Likelihood、FID、KID、Precision–Recall 与人类评估]]"]
solutions: ["[[解答 - Likelihood、FID、KID、Precision–Recall 与人类评估]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-generative-evaluation-metric-matrix-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Likelihood、FID、KID、Precision–Recall 与人类评估

> [!abstract] 一句话结论
> 生成模型没有一个足够的单一分数。Likelihood 测模型给数据的概率；FID/KID 比较指定表示空间中的分布统计；precision/recall 分开 fidelity 与 coverage；人评测任务相关感知和偏好。它们都依赖 estimator、样本量和协议，必须以“指标矩阵 + 成本 + 不确定性”联合报告。

## 一、先定义要评价的五个问题

1. **fidelity**：单个样本是否像目标域的有效样本？
2. **coverage/diversity**：目标分布的模式是否被覆盖？
3. **conditionality**：样本是否遵循 prompt、label、measurement？
4. **novelty/memorization**：是否只是复制训练样本？
5. **efficiency**：在多少 NFE、时间、内存与能耗下得到？

任何指标最多覆盖其中一部分。

## 二、Likelihood：最直接但不等于感知质量

对 test data $x_i\sim p_{data}$，平均 NLL

$$
\widehat{\mathrm{NLL}}
=-\frac1n\sum_{i=1}^n\log p_\theta(x_i).
$$

图像常报告 bits per dimension

$$
\mathrm{BPD}=\frac{\mathrm{NLL}}{D\log2}.
$$

必须说明：离散像素 likelihood、dequantized continuous density、ELBO/importance bound 还是 probability-flow ODE 数值 likelihood。不同对象不能直接比。

高 likelihood 不保证样本感知更好，原因包括：density 对低层统计/背景复杂度敏感；model support 与 perceptual equivalence 不一致；近似 bound 和 solver error 还会影响数值。

## 三、FID：在固定特征中的 Gaussian $W_2^2$

取 encoder $\phi(x)\in\mathbb R^d$。真实/生成特征的均值协方差为 $(\mu_r,\Sigma_r)$、$(\mu_g,\Sigma_g)$。FID 定义

$$
\boxed{
\mathrm{FID}
=\|\mu_r-\mu_g\|^2
+\operatorname{tr}\left(
\Sigma_r+\Sigma_g
-2(\Sigma_r^{1/2}\Sigma_g\Sigma_r^{1/2})^{1/2}
\right).
}
$$

它是两个 fitted Gaussian 在特征空间的 squared Wasserstein-2 distance。三重近似：

1. 原始数据先投影到 encoder 表示；
2. 表示分布只保留一二阶矩并拟合 Gaussian；
3. 均值/协方差由有限样本估计。

### 3.1 为什么用对称夹心

$\Sigma_r^{1/2}\Sigma_g\Sigma_r^{1/2}$ 是对称半正定，主平方根可稳定由特征分解得到。直接计算 $(\Sigma_r\Sigma_g)^{1/2}$ 会遇到非对称矩阵与数值复数；即使 trace 在理想条件下相等，程序也优先用对称形式。

### 3.2 有限样本偏差

plug-in FID 对样本 moments 做非线性变换，通常有有限样本偏差；不同模型的偏差还可能不同。应固定相同 sample count，重复抽样或 bootstrap 报区间，不能把小数点后微小差异当确定排名。

### 3.3 预处理也是指标定义

[[S-2022-Parmar-CleanFID]] 展示 resize/antialias/quantization 的差异可显著改变 FID。必须记录 encoder 权重、resize kernel、颜色范围、数据 split、reference stats hash 与实现版本。

## 四、KID：固定核下的 MMD

令真实特征 $a_1,\ldots,a_m$，生成特征 $b_1,\ldots,b_n$，kernel $k$。unbiased U-statistic estimator：

$$
\widehat{\mathrm{MMD}}_u^2
=\frac1{m(m-1)}\sum_{i\ne j}k(a_i,a_j)
+\frac1{n(n-1)}\sum_{i\ne j}k(b_i,b_j)
-\frac2{mn}\sum_{i,j}k(a_i,b_j).
$$

KID 通常在 Inception features 上使用 polynomial kernel。[[S-2018-Binkowski-KID]] 的重要优点是 estimator 对固定 distributions/kernel 无偏；但：

- 单次估计仍有 variance，甚至可为负；
- kernel/encoder 决定检测哪些差异；
- 同样不直接测语义遵循、memorization 或人类偏好。

## 五、Precision–Recall：方法名必须写全

生成评价中的 precision/recall 不是分类混淆矩阵。直觉：

- precision：生成样本有多少落在真实分布的高支持/流形附近；
- recall：真实分布有多少被生成分布覆盖。

[[S-2018-Sajjadi-Precision-Recall]] 定义分布 PR curve；[[S-2019-Kynkaanniemi-Improved-Precision-Recall]] 在特征空间用 kNN 半径构造 empirical manifolds。二者 estimator 不同。

kNN 版本示意：对真实特征 $a_i$，令 $r_i$ 为其第 $k$ 近邻距离。若生成点 $b$ 落入某个球 $B(a_i,r_i)$，计为被真实 manifold 接受。反向交换集合估计 recall。

参数 $k$、encoder、样本数和 outliers 都会改变结果；报告时写 `Improved P/R, k=3, encoder=..., n=...`。

## 六、条件一致性不是整体质量

文本—图像相似度、分类准确率或 measurement residual 测的是条件的一部分。高 CLIP 相似度可能由关键词/构图偏好驱动，低 residual 可能过拟合观测噪声。

条件模型至少联合：

- unconditional fidelity/coverage；
- prompt/label/task adherence；
- 组合、计数、空间关系等分项；
- 对等 prompts 的人口统计/风格偏差；
- negative/ambiguous prompt 的失败率。

## 七、人类评估怎样避免“看几张图”

### 7.1 明确 estimand

是 realism、prompt adherence、pairwise preference、artifact rate 还是任务可用性？不要用一个“总体更好”问题混合全部维度。

### 7.2 随机化与盲化

- 隐藏模型名与文件顺序；
- 同 prompt/seed 做 paired comparison；
- 左右位置随机；
- prompts 从预先固定 test set 抽样；
- 不由作者手挑样例。

### 7.3 统计单位

同一评审者判断多张图会相关；同一 prompt 的多个 seed 也相关。置信区间应按 prompt/participant 分层 bootstrap 或用混合效应/Bradley–Terry 类模型，而非把每次点击当 iid。

### 7.4 质量控制与伦理

报告人数、资格、补偿、地理/语言范围、attention checks、剔除规则、分歧与不确定性。涉及敏感内容时还要说明暴露风险与审核机制。

## 八、memorization 与 train/test leakage

低 FID 可能来自复制训练集。至少做：

- generated-to-train 与 generated-to-test nearest neighbors；
- pixel 与多个 representation 的距离；
- exact/near-duplicate hash；
- prompt-specific copy inspection；
- selection metric 的 reference set 是否与 test 重叠。

nearest neighbor 看起来不同也不能证明隐私安全；它只是初筛。

## 九、推荐的最小评价面板

| 类别 | 至少一项 | 报告方式 |
|---|---|---|
| density | NLL/BPD/ELBO（若合法） | estimator 与数值误差 |
| distribution | CleanFID + KID | 样本数、重复、CI、encoder |
| fidelity/coverage | Improved P/R 或 density/coverage | 方法名、$k$、特征 |
| conditionality | task metric + 盲化人评 | 分项与 failure rate |
| novelty | NN/copy audit | train/test 对照 |
| cost | NFE、latency、memory | hardware、batch、precision |

## 十、图：每个指标看见什么

先回答：同一个 mode dropping 模型可能让哪些指标变好/变坏？FID 和 KID 为什么都受 encoder 控制？人评怎样补而不是“取代数学”？

![[00-知识库管理/_assets/figures/generative-models/fig-generative-evaluation-metric-matrix-v1.svg|900]]

> [!figure] 图 50.9-07　生成模型评价的指标—失效矩阵
> 图用 fidelity、coverage、conditionality、novelty、cost 五列对照 likelihood、FID/KID、P/R 与人评。来源：据 FID、KID、两类 P/R、CleanFID 原论文与本节协议独立绘制。

**怎样读图**：先选研究问题，再选至少两个互补指标；沿每一行读 encoder、sample size 和 human protocol 的依赖。

**图没有证明什么**：图不证明人评无偏，不证明 KID 无偏就低方差，也不证明低 FID 等同于更真实、更公平或不记忆训练集。

## 十一、学习出口

- 能写出 FID 对称夹心公式与 KID U-statistic；
- 能解释 finite-sample bias 与 encoder bias 的区别；
- 能指出两类 P/R estimator 不同；
- 能设计盲化配对人评和最小指标面板；
- [[习题 - Likelihood、FID、KID、Precision–Recall 与人类评估]]
- [[解答 - Likelihood、FID、KID、Precision–Recall 与人类评估]]
