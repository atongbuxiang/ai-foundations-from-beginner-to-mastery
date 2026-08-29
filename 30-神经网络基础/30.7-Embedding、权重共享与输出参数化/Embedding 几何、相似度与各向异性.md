---
type: concept
status: draft
area: [neural-networks/embedding-output, representation-geometry, similarity, anisotropy]
aliases: [Embedding Geometry and Anisotropy, Cosine and Dot Product]
node_id: NN-50
prerequisites: ["[[Embedding Lookup、稀疏梯度与参数规模]]", "[[内积空间]]", "[[协方差、相关性与条件期望]]", "[[度量学习、相似性与检索风险]]"]
related: ["[[输入—输出权重共享与 Weight Tying]]", "[[表示坍缩、非坍缩与可辨识边界]]", "[[PCA 的统计估计与主子空间风险]]", "[[Embedding 初始化、缩放、分解与量化接口]]"]
sources: ["[[S-2013-Mikolov-Distributed-Representations]]", "[[S-2019-Ethayarajh-Contextual-Anisotropy]]", "[[S-2017-Su-4669-词向量与互信息]]", "[[S-2020-Su-7695-词向量维度与最小熵]]"]
exercises: ["[[习题 - Embedding 几何、相似度与各向异性]]"]
solutions: ["[[解答 - Embedding 几何、相似度与各向异性]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-embedding-geometry-anisotropy-v2.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# Embedding 几何、相似度与各向异性

> [!abstract] 本章主问题
> Embedding 的“相似”不是坐标表自动附带的语义，而是向量对象、预处理、metric 与任务共同定义的测量。内积混合 norm 与 angle，cosine 去掉正尺度但不对平移不变，欧氏距离对共同平移不变却保留尺度。所谓 anisotropy 也不是一个唯一数字：共同均值、pairwise cosine、centered covariance spectrum、有效秩、局部簇与下游风险必须分开。

## 课程位置与两遍学习路线

- **承接什么：** NN-49 已把每个 token row 定义成 $E$ 中可被精确索引和更新的参数对象；
- **本页解决什么：** 说明“row 是向量”之后仍须选择 inner product、cosine、distance、centering 与谱诊断，几何数字才有可解释含义；
- **后续为何需要：** weight tying 会让同一 row 成为 output prototype，Softmax 则直接使用内积作为 logit，因此几何预处理会改变概率模型而不只是可视化。

**第一遍只比较三种测量。** 对同一对 rows 算 dot、cosine 与 distance，并逐项检查 rotation、scale、translation 不变性。

**第二遍再诊断整个空间。** 明确采样分布后计算 mean、centered covariance、spectrum 与 effective rank，再用 retrieval/classification/generation 风险验证干预是否有益。

### 问题链

1. token row、contextual state 与 output prototype 是不是同一个随机对象？
2. dot、cosine 与 Euclidean distance 分别保留或删除了什么信息？
3. 为什么减去共同均值可能大幅改变 cosine，却仍不保证 isotropy？
4. covariance rank、participation ratio 与平均 pairwise cosine 会不会给出不同诊断？
5. 移除 top PCs 后几何指标变好，为何下游任务仍可能变差？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal E_\square$ 中算出 $e_1^{\mathsf T}e_2=-1$、$\cos(e_1,e_2)=-1/\sqrt5$、$\|e_1-e_2\|^2=8$，并解释三个数字为何回答不同问题，就已掌握本页主干。

## 符号与对象账本

| 对象 | 定义 | 是否依赖采样/预处理 | 主要风险 |
|---|---|---|---|
| $e_i$ | input/output table row | 依参数时刻 | norm 与频率混杂 |
| $h(c,t,\ell)$ | contextual state | 强依 context/layer/mode | 把 token type 与 token occurrence 混写 |
| $a^{\mathsf T}b$ | inner product | 不中心化、保留 norm | 大 norm 主导排序 |
| $\cos(a,b)$ | 归一化 inner product | 不平移不变 | 共同均值制造窄锥 |
| $C$ | centered covariance | 依样本权重与中心 | 小样本必然秩亏 |
| $r_{\mathrm{PR}}$ | 谱 participation ratio | 依 covariance 定义 | 单标量隐藏局部结构 |

### 贯穿算例 $\mathcal E_\square$：从一对 rows 到整表谱

沿用 NN-49 的

$$
E=
\begin{bmatrix}
1&0\\0&1\\2&-1\\-1&3
\end{bmatrix}.
$$

对 token 1 与 2，

$$
e_1=(0,1),\qquad e_2=(2,-1),
$$

所以

$$
e_1^{\mathsf T}e_2=-1,
\qquad
\cos(e_1,e_2)=-\frac1{\sqrt5},
\qquad
\|e_1-e_2\|_2^2=8.
$$

均匀看待四个 rows 时，均值为

$$
\mu=\left(\frac12,\frac34\right),
$$

population centered covariance 是

$$
C=\frac14\sum_{i=0}^3(e_i-\mu)(e_i-\mu)^{\mathsf T}
=
\begin{bmatrix}
5/4&-13/8\\
-13/8&35/16
\end{bmatrix}.
$$

它的 trace、determinant 与 eigenvalues 为

$$
\operatorname{tr}C=\frac{55}{16},
\qquad
\det C=\frac3{32},
$$

$$
\lambda_{\pm}=\frac{55\pm\sqrt{2929}}{32}
\approx(3.410007,0.027493).
$$

因此

$$
\boxed{
r_{\mathrm{PR}}
=\frac{(\operatorname{tr}C)^2}{\operatorname{tr}(C^2)}
=\frac{3025}{2977}
\approx1.016124
}.
$$

$C$ 虽然满秩，variation 却几乎集中在一个方向。这个结论来自整表谱，不能由某一对 token 的 cosine 单独推出。

## 核心公式七问：任务绑定的几何诊断

$$
\boxed{
\text{geometry report}
=(\text{object},\text{sampling},\text{preprocess},\text{metric},\text{spectrum},\text{task risk})
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 防止把一个漂亮的 cosine/PCA 图误当成表示质量 |
| 对象 | token rows、contextual states 或 output prototypes 必须三选一并注明 |
| 来路 | 相似性是向量、采样、预处理和 metric 共同定义的测量 |
| 步骤 | 固定对象与分布→算局部 metric→中心化谱→实施干预→测任务风险 |
| 读法 | 几何指标描述坐标分布，task risk 才回答应用是否改善 |
| 检查 | rotation/scale/shift intervention、频率分桶、bootstrap 与下游消融 |
| 去路 | ANN 检索、cosine classifier、weight tying、representation collapse |

### AI / 系统对应

向量检索系统必须把训练 metric、索引 metric 和线上 reranking metric 对齐；否则离线 cosine 结论无法解释 inner-product ANN 的召回。中心化、whitening 或 top-PC removal 还会改变增量索引、量化范围和 output logits，必须同时记录质量、延迟与重建成本。

## 一、学习目标

读完本节，你应能：

1. 区分 token-table row、contextual representation 与输出 prototype；
2. 推导 dot、cosine 与 Euclidean distance 的关系；
3. 给出三种 metric 对 rotation、scale 与 translation 的不变性；
4. 计算均值、centered covariance、谱集中度与有效秩；
5. 用手算例子解释共同均值为何制造高 cosine；
6. 说明 centering、top-PC removal、normalization 与 whitening 的风险；
7. 把几何诊断绑定到 retrieval/classification/generation 的任务目标；
8. 识别参数重表示下“坐标语义”的不可辨识边界。

## 二、先固定“哪个 Embedding”

同一个系统中至少有三类向量：

1. **input token row**：参数表 $E_{i:}$；
2. **contextual state**：给定句子、位置和层的 $h_{b,t}^{(\ell)}$；
3. **output prototype**：输出矩阵第 $i$ 行 $w_i^\mathsf T$。

它们可能维度相同，甚至因 weight tying 共用参数，但随机对象不同。token row 对一个 ID 固定；contextual state 随上下文、层与 model mode 改变；output row 的角色是定义类别 logit。

任何“embedding space 很各向异性”的报告必须注明：测的是哪一类向量、哪个 layer、哪些 token/contexts、是否按频率加权。

## 三、内积、cosine 与欧氏距离

对非零向量 $a,b\in\mathbb R^d$：

$$
\operatorname{dot}(a,b)=a^\mathsf Tb,
$$

$$
\operatorname{cos}(a,b)
=\frac{a^\mathsf Tb}{\|a\|_2\|b\|_2},
$$

$$
d_2(a,b)=\|a-b\|_2.
$$

令夹角为 $\theta$，则

$$
a^\mathsf Tb=\|a\|\|b\|\cos\theta.
$$

所以 dot 同时受长度与方向影响。距离满足

$$
\boxed{
\|a-b\|^2
=\|a\|^2+\|b\|^2-2a^\mathsf Tb
}.
$$

只有当所有向量都单位归一化时，

$$
\|a-b\|^2=2-2\cos(a,b),
$$

cosine 排序才与 Euclidean distance 排序等价。

## 四、手算：三种测量给出不同信息

令

$$
a=(3,4),
\qquad
b=(4,3).
$$

两者 norm 都是 5，

$$
a^\mathsf Tb=24,
$$

$$
\cos(a,b)=\frac{24}{25}=0.96,
$$

$$
\|a-b\|=\sqrt{(-1)^2+1^2}=\sqrt2.
$$

若把 $b$ 换为 $10b$，cosine 仍为 0.96，但 dot 变为 240，距离变为

$$
\|a-10b\|
=\sqrt{37^2+26^2}
=\sqrt{2045}
\approx45.22.
$$

所以一个 ANN index 按 inner product、cosine 或 L2 建库，会回答不同 nearest-neighbor 问题。

## 五、不变性表

对 orthogonal $Q$、正尺度 $s>0$、共同平移 $c$：

| 变换 | dot | cosine | distance |
|---|---|---|---|
| $a\mapsto Qa,b\mapsto Qb$ | 不变 | 不变 | 不变 |
| $a\mapsto sa,b\mapsto sb$ | 乘 $s^2$ | 不变 | 乘 $s$ |
| $a\mapsto a+c,b\mapsto b+c$ | 一般改变 | 一般改变 | 不变 |
| 一般可逆 $A$ | 一般改变 | 一般改变 | 一般改变 |

若只缩放 query 或 document 一侧，inner-product 排序也可能改变。声明“cosine 去掉了尺度”只对每个非零向量的正缩放成立；零向量 cosine 未定义，负尺度还会翻转方向。

## 六、norm 本身可能承载信号

将所有向量单位化会丢弃 row norm。norm 可能与：

- token frequency；
- uncertainty/置信度；
- output logit scale；
- 训练次数和 regularization；
- modality-specific quality

相关。相关不等于语义：高频导致大/小 norm 的方向取决于目标和 optimizer。应先检验 norm 与频率、label、损失、校准和检索相关性，再决定是否归一化。

## 七、共同均值与高 cosine

设四个二维向量

$$
e_1=(10,1),\quad
e_2=(10,-1),\quad
e_3=(10,2),\quad
e_4=(10,-2).
$$

共同均值

$$
\mu=\frac14\sum_{i=1}^4e_i=(10,0).
$$

例如

$$
\cos(e_1,e_2)
=\frac{99}{101}
\approx0.9802,
$$

$$
\cos(e_3,e_4)
=\frac{96}{104}
\approx0.9231.
$$

即使 centered residuals 分别指向相反方向，未中心化 cosine 仍很高，因为所有向量共享大的第一坐标。

## 八、Centering 不保证 isotropy

中心化

$$
\widetilde e_i=e_i-\mu
$$

后，四个向量变为

$$
(0,1),(0,-1),(0,2),(0,-2).
$$

population covariance 为

$$
C=\frac14\sum_i\widetilde e_i\widetilde e_i^\mathsf T
=
\begin{bmatrix}
0&0\\
0&2.5
\end{bmatrix}.
$$

均值消失了，但 covariance rank 只有 1，所有 centered variation 仍落在一条直线上。故：

$$
\text{mean removal}
\not\Rightarrow
\text{isotropy}.
$$

## 九、谱诊断与有效秩

令 centered covariance 特征值为

$$
\lambda_1\ge\cdots\ge\lambda_d\ge0.
$$

常见诊断包括：

$$
\frac{\lambda_1}{\operatorname{tr}C},
\qquad
\kappa_{\mathrm{support}}=\frac{\lambda_{\max}}{\lambda_{\min,+}},
$$

participation ratio

$$
r_{\mathrm{PR}}
=\frac{(\operatorname{tr}C)^2}{\operatorname{tr}(C^2)},
$$

以及 entropy effective rank。令

$$
\pi_i=\frac{\lambda_i}{\sum_j\lambda_j},
$$

则

$$
\boxed{
r_{\mathrm{eff}}
=\exp\left(-\sum_{i:\pi_i>0}\pi_i\log\pi_i\right)
}.
$$

完全等谱时 $r_{\mathrm{eff}}=d$；rank-one 时为 1。样本量小于 $d$ 时 sample covariance 必然秩亏，不能把这种代数限制误说成模型坍缩。

## 十、Anisotropy 没有唯一标量定义

至少可检查：

1. $\|\mu\|$ 相对 RMS radius；
2. 随机 pairwise cosine distribution；
3. centered covariance spectrum/effective rank；
4. 不同方向的 partition/投影统计；
5. local cluster 内与 cluster 间的谱；
6. 频率加权与均匀 token 加权的差异；
7. 下游 metric 下的检索/分类风险。

两个空间可能 mean cosine 相同，却有完全不同的 spectrum；也可能 global anisotropic、每个 local cluster 近 isotropic。报告应给多指标，而不是用“isotropy score”隐藏定义。

## 十一、Contextual Embedding 的证据边界

Ethayarajh 2019 在 ELMo、BERT、GPT-2 与论文协议中观察到 contextual representations 的 anisotropy，并研究同词跨上下文 self-similarity。该证据说明：

- 直接用 raw cosine 比较 contextual states 需要方向基线；
- layer、context sampling 与 token frequency 会改变几何；
- static token row 不能代表同一词在所有上下文中的状态。

它不证明所有现代模型各层都以同一方式 anisotropic，也不证明“越 isotropic 越好”。后者必须指定任务和干预实验。

## 十二、重参数化与坐标不可辨识

设 embedding 输出列向量 $x$，后接线性层 $Wx$。对任意可逆矩阵 $A$，定义

$$
x'=Ax,
\qquad
W'=WA^{-1}.
$$

则

$$
W'x'=WA^{-1}Ax=Wx.
$$

网络函数不变，但一般 $A$ 会改变 dot、cosine、distance 和 covariance spectrum。因此仅由任务函数无法唯一识别 embedding 的坐标几何；需要正交约束、normalization、weight tying、regularization 或固定读出才减少 gauge freedom。

这也是为什么“第 137 维表示语法”通常不是参数化不变的结论。

## 十三、后处理不是免费改进

### 13.1 Centering

用

$$
e_i' = e_i-\widehat\mu
$$

可去共同均值，但 $\widehat\mu$ 必须只在训练/索引库上拟合；测试集共同估计会泄漏。

### 13.2 Top-PC removal

删除前 $k$ 个主方向可能减少 frequency/common components，也可能删掉任务信号。$k$ 是要验证的超参数。

### 13.3 Whitening

$$
e_i'=C_\varepsilon^{-1/2}(e_i-\mu)
$$

可拉平训练 covariance，但小 eigenvalues 会放大噪声；必须有 regularization/pseudoinverse，并在分布偏移下重验。

### 13.4 Unit normalization

将 cosine retrieval 化为 sphere geometry，却丢弃 norm 信息并改变 tied output logits。后处理若只应用 query 或 index 一侧，也会改变模型合同。

## 十四、与任务接口

| 任务 | 几何对象 | 额外审计 |
|---|---|---|
| cosine retrieval | 单位方向 | 零 norm、hubness、ANN index metric |
| MIPS | dot + norm | norm-frequency bias、最大内积索引 |
| L2 retrieval | affine distance | centering、scale、whitening |
| linear probe | 可分子空间 | probe capacity、regularization |
| tied language head | $e_i^\mathsf Th+b_i$ | row/hidden norm、bias、temperature |

“语义质量”必须通过目标任务和评价协议落地；analogy、word similarity、retrieval recall 与生成 perplexity不是同一个出口。

## 十五、图：相似度、均值锥与诊断

先看图回答：为什么 $b\mapsto10b$ 不改变 cosine 却改变 dot 和 distance？共同均值怎样抬高 cosine？哪一种变换可同时保持三种测量？

![[00-知识库管理/_assets/figures/neural-networks/fig-embedding-geometry-anisotropy-v2.svg|900]]

> [!figure] 图 30.7-02　Embedding metric、共同均值与各向异性诊断族
> 左栏手算 dot/cosine/distance；中栏把共同均值画成窄锥，并要求 centering 后继续看 covariance spectrum；右栏列出 rotation、scale、shift 与一般可逆变换的不变性。来源：依据 Mikolov et al. 2013、Ethayarajh 2019 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_embedding_output_foundations_v2.py]] 确定性生成。

**怎样读图**：先确定 metric 是否保留 norm，再看向量是否有共同均值，最后用 centered spectrum、有效秩、局部簇和任务结果交叉验证。

**图没有证明什么**：窄锥示意不证明真实模型只有二维结构，也不证明 centering、去主成分或 whitening 必然改善下游任务。

## 十六、最小验收

1. 推导 dot/cos/distance 关系；
2. 复算 $(3,4),(4,3)$ 与尺度变化；
3. 填写三类变换不变性表；
4. 复算共同均值例子的 cosine、covariance 与 rank；
5. 定义 participation/effective rank；
6. 区分 token row、contextual state 与 output prototype；
7. 构造可逆重参数化使函数不变但 cosine 改变；
8. 为 centering/PC removal/whitening 设计无泄漏评估。

> [!summary]
> Embedding 几何不是一张 cosine heatmap。可靠分析从向量对象与 metric 开始，分离 norm、angle、mean 和 centered spectrum，再检查坐标重参数化与下游任务。Anisotropy 是诊断问题族，而不是一个天然等于“表示差”的标签。

- [[Embedding、权重共享与输出参数化 MOC]]
- [[习题 - Embedding 几何、相似度与各向异性]]
- [[解答 - Embedding 几何、相似度与各向异性]]
