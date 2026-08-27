---
type: theorem
status: draft
area: [learning-theory/contrastive-learning, infonce, density-ratio, mutual-information]
aliases: [InfoNCE Theory, Contrastive Density Ratio, Contrastive Mutual Information Bound]
node_id: LT-55
prerequisites: ["[[交叉熵与 KL 散度]]", "[[互信息与依赖性]]", "[[逻辑回归、复合损失与概率分类]]", "[[度量学习、相似性与检索风险]]"]
related: ["[[正负样本、Batch 依赖与梯度估计]]", "[[数据增强、不变性、等变性与任务充分性]]", "[[表示坍缩、非坍缩与可辨识边界]]"]
sources: ["[[S-2018-Oord-Li-Vinyals-CPC]]", "[[S-2019-Poole-Variational-MI-Bounds]]", "[[S-2020-McAllester-Stratos-MI-Limitations]]", "[[S-2020-Wang-Isola-Alignment-Uniformity]]", "[[S-2010-Gutmann-Hyvarinen-NCE]]", "[[S-2018-Su-6024-深度学习的互信息]]"]
exercises: ["[[习题 - 对比学习、InfoNCE 与密度比]]"]
solutions: ["[[解答 - 对比学习、InfoNCE 与密度比]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-infonce-density-ratio-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 对比学习、InfoNCE 与密度比

> [!abstract] 本章主问题
> InfoNCE首先定义一个candidate-index classification experiment：给anchor $X$，一个candidate $Y_I$ 来自conditional $p(y\mid x)$，其余来自marginal $p(y)$；模型要猜哪个index是positive。
>
> Bayes-optimal score满足
>
> $$
> \boxed{
> s^\star(x,y)
> =
> \log\frac{p(y\mid x)}{p(y)}+c(x)
> }
> $$
>
> 即pointwise density ratio到anchor-dependent additive term。相应population loss给mutual information lower bound
>
> $$
> I(X;Y)
> \ge
> \log K-\mathcal L_{\rm InfoNCE}.
> $$
>
> 但必须分清：candidate classification risk、density-ratio identification、population MI lower bound、finite-batch estimate与downstream representation utility是五个不同claims。

> [!question] 初学者读完必须能回答
> 1. NCE与InfoNCE为什么不是同一个estimand？
> 2. candidate-index posterior怎样推出density ratio？
> 3. InfoNCE loss为什么是cross-entropy？
> 4. $\log K-\mathcal L$ 在什么层次是MI lower bound？
> 5. 为什么bound ceiling为 $\log K$？
> 6. 最大化MI为什么不自动得到disentangled或task-sufficient representation？

## 一、学习目标

1. 写出positive joint/conditional与negative marginal sampling law；
2. 从Bayes rule推导candidate-index posterior；
3. 推导optimal critic的density-ratio形式；
4. 定义population与finite-batch InfoNCE；
5. 解释MI lower bound与 $\log K$ ceiling；
6. 分解critic、optimization、Monte Carlo与generalization gaps；
7. 区分NCE、InfoNCE、negative sampling与contrastive divergence；
8. 解释MI对invertible transformations不变的边界；
9. 连接alignment/uniformity几何；
10. 审计temperature、normalization与negative law。

## 二、先声明 Positive-Pair Law

设两种views为random variables

$$
(X,Y)\sim p_{XY}.
$$

它们可能是：

- 同一image的两种augmentations；
- context与future latent；
- image与caption；
- query与clicked document；
- 同一entity的两次measurement。

marginals为 $p_X,p_Y$。mutual information：

$$
I(X;Y)
=
E_{p_{XY}}
\left[
\log\frac{p_{XY}(X,Y)}{p_X(X)p_Y(Y)}
\right]
=
E\left[\log\frac{p(Y\mid X)}{p_Y(Y)}\right].
$$

> [!warning] Positive 不是自然常量
> positive-pair construction决定joint law。改变augmentation、temporal window、caption pairing或entity rule，就改变了要估计的density ratio与要学习的invariance。

## 三、Candidate-Index Experiment

固定候选数 $K\ge2$：

1. 抽index $I\sim\operatorname{Unif}\{1,\ldots,K\}$；
2. 抽anchor $X\sim p_X$；
3. positive candidate $Y_I\sim p(y\mid X)$；
4. 对 $j\ne I$，independently抽 $Y_j\sim p_Y$。

观察

$$
(X,Y_1,\ldots,Y_K)
$$

并预测 $I$。

## 四、Bayes Posterior 推导

给定 $I=i$，candidate joint density proportional to

$$
p_X(x)p(y_i\mid x)\prod_{j\ne i}p_Y(y_j).
$$

把共同项

$$
p_X(x)\prod_{j=1}^Kp_Y(y_j)
$$

提出，剩下

$$
r(x,y_i)
=
\frac{p(y_i\mid x)}{p_Y(y_i)}.
$$

由Bayes rule与uniform prior：

$$
\boxed{
P(I=i\mid x,y_{1:K})
=
\frac{r(x,y_i)}{\sum_{j=1}^Kr(x,y_j)}.
}
$$

所以任意score满足

$$
e^{s^\star(x,y)}
\propto
r(x,y),
$$

即

$$
s^\star(x,y)
=
\log r(x,y)+c(x).
$$

additive $c(x)$在softmax中消失，因此score本身不唯一。

## 五、InfoNCE 是 Cross-Entropy

model score $s_\theta(x,y)$ 定义candidate probability

$$
q_\theta(i\mid x,y_{1:K})
=
\frac{\exp s_\theta(x,y_i)}
{\sum_{j=1}^K\exp s_\theta(x,y_j)}.
$$

population InfoNCE loss：

$$
\boxed{
\mathcal L_{\rm NCE}(\theta)
=
E[-\log q_\theta(I\mid X,Y_{1:K})].
}
$$

它是proper multiclass log loss。population unrestricted optimum为conditional entropy：

$$
\inf_\theta\mathcal L_{\rm NCE}
=
H(I\mid X,Y_{1:K})
$$

当critic family能表示Bayes posterior时取到。

## 六、常见 NT-Xent 形式

若representations normalized，score常取

$$
s(z,z')
=
\frac{z^Tz'}{\tau},
$$

其中temperature $\tau>0$。对anchor $i$ 与positive $j$：

$$
\ell_{i,j}
=
-\log
\frac{\exp(z_i^Tz_j/\tau)}
{\sum_{k\in\mathcal A(i)}\exp(z_i^Tz_k/\tau)}.
$$

$\mathcal A(i)$ 的exact membership是method definition：是否含same-view、positive、cross-device items、memory bank与mask都会改变loss。

## 七、Mutual Information Lower Bound

在上述ideal candidate experiment与合适support下，对任意critic可得

$$
\boxed{
I(X;Y)
\ge
\log K-\mathcal L_{\rm NCE}(\theta).
}
$$

### 7.1 证明架构

第一步，cross-entropy不小于Bayes conditional entropy：

$$
\mathcal L_{\rm NCE}(\theta)
\ge
H(I\mid X,Y_{1:K}).
$$

因此

$$
\log K-\mathcal L_{\rm NCE}(\theta)
\le
I(I;X,Y_{1:K}).
$$

第二步，用candidate construction、KL chain rule/log-sum inequality可证明

$$
I(I;X,Y_{1:K})
\le
I(X;Y).
$$

组合得到bound。

> [!important] Bound 不是等式
> 等号需要critic充分、candidate information捕获全部pair dependence等强条件。实际neural critic、finite $K$ 与finite data都会留下gap。

## 八、为什么有 $\log K$ Ceiling

因为cross-entropy非负：

$$
\log K-\mathcal L_{\rm NCE}
\le
\log K.
$$

即使true MI远大于 $\log K$，InfoNCE lower bound也会saturate。若希望证出 $b$ nats，至少需要

$$
K\ge e^b.
$$

这体现exponential candidate burden。

McAllester–Stratos更进一步说明：distribution-free high-confidence MI lower bound从 $N$ samples得到时一般受order $\log N$ 限制。这是measurement barrier，不只是某个network训练不好。

## 九、五层 Gap Ledger

令true MI为 $I$，population unrestricted InfoNCE bound为 $B_K^\star$，critic-class optimum为 $B_{K,\mathcal S}$，trained critic bound为 $B(\widehat\theta)$，finite estimate为 $\widehat B$。典型顺序：

$$
I
\ge
B_K^\star
\ge
B_{K,\mathcal S}
\ge
B(\widehat\theta).
$$

另有

$$
\widehat B-B(\widehat\theta)
$$

的sampling/generalization error。分别是：

1. finite-candidate/bound gap；
2. critic approximation gap；
3. optimization gap；
4. finite-batch/statistical error；
5. adaptive selection reuse。

只报告 $\log K-\widehat L$ 无法区分这些项。

## 十、NCE 与 InfoNCE 不可混同

| 方法 | classification experiment | estimand | normalization role |
|---|---|---|---|
| original NCE | data vs known noise，binary | unnormalized density parameter | partition constant可作为parameter估计 |
| InfoNCE | one joint candidate vs marginal candidates | contrastive risk / MI lower bound | softmax overcandidate set |
| negative sampling | 常为简化binary objectives | 依具体算法 | 未必给normalized likelihood |
| contrastive divergence | short Markov chains比较data/model statistics | energy-model learning approximation | 近似likelihood gradient |

名称相似不是理论等价。

## 十一、若 Negatives 来自别的 Distribution

若negative law是 $q_Y$ 而非 $p_Y$，Bayes ratio变成

$$
\frac{p(y\mid x)}{q_Y(y)}.
$$

这通常不再直接等于MI density ratio。hard-negative sampling、class-balanced sampling与memory bank都会改变effective $q$；需要importance correction或重新解释estimand。

## 十二、一个二元例子

令 $X=Y\in\{0,1\}$ uniform，所以

$$
I(X;Y)=\log2.
$$

取 $K=2$。在perfect ratio critic极限，若negative偶然等于positive value，candidate index仍可能ambiguous；若不同则容易识别。lower bound不应被想成“每个batch都等于true MI”。

同时ceiling正好是 $\log2$；只有population expectation、ideal critic与极限条件共同决定是否接近。

## 十三、MI 大不等于表示好

### 13.1 Invertible Transformation Invariance

若 $f,g$ invertible，则在regular条件下

$$
I(f(X);g(Y))=I(X;Y).
$$

所以MI不能区分一个整齐factorized coordinate system与任意复杂invertible entanglement。

### 13.2 Identity Memorization

表示可通过保留instance identity、sensor artifact或augmentation seed获得高view dependence，却不支持目标label或shift。

### 13.3 Task Sufficiency

下游需要的是对target task足够的信息与可由允许head读出的geometry，不是无差别保留所有shared information。

## 十四、Alignment 与 Uniformity 视角

在unit hypersphere与特定asymptotic setup中，contrastive learning可分成：

- alignment：positive views靠近；
- uniformity：marginal representations在sphere上铺开。

alignment alone允许constant collapse；uniformity提供spread pressure。但这两个geometry指标仍不证明：

- augmentation保label；
- representation对目标task充分；
- finite batch没有false negatives；
- OOD与subgroups可靠。

## 十五、图：从候选分类到密度比与 MI Bound

先看图回答：为什么一个更低的InfoNCE loss可以是更好的training signal，却仍不能作为准确MI测量？

![[00-知识库管理/_assets/figures/learning-theory/fig-infonce-density-ratio-v2.svg|900]]

> [!figure] 图 20.7-03　NCE/InfoNCE分界、ratio识别与下界缺口
> 左栏先区分unnormalized-model NCE与candidate-index InfoNCE；中栏从positive conditional和marginal negatives推出softmax与density ratio；右栏列出log-K ceiling、critic/optimization/sampling gaps及task sufficiency边界。来源：依据 Gutmann–Hyvärinen、CPC、Poole et al.、McAllester–Stratos与Wang–Isola独立绘制；确定性 SVG，由 [[plot_representation_contrastive_v2.py]] 生成。

**怎样读图**：ratio结论属于population Bayes classifier；MI结论是lower bound；finite training只是对loss的随机优化。三层不能用同一个等号连接。

**图没有证明什么**：它没有证明in-batch negatives iid from marginal、critic达到Bayes optimum或learned representation对任意downstream task有效。

## 十六、AI 接口

### 16.1 Vision Two-View Learning

augmentation law定义joint；crop、color、texture等是否nuisance由task决定。projection head可吸收pretext-specific geometry。

### 16.2 Language Context Prediction

nearby text共享topic、author与document identity。contrastive signal可能学到semantic content，也可能学到source shortcut。

### 16.3 Multimodal Contrast

image–text pairs的positive law受caption quality与dataset filtering影响；marginal negatives可能是语义相关的false negatives。

### 16.4 Retrieval/Reranking

若production negative distribution偏向hard near-neighbors，而training从global marginal抽样，density-ratio target与deployment ranking不同。

## 十七、常见错误

1. 把InfoNCE叫作无偏MI estimator；
2. 忽略 $\log K$ ceiling；
3. 把finite batch loss直接代入population theorem；
4. 不声明positive/negative law；
5. 把NCE、InfoNCE、negative sampling与contrastive divergence混名；
6. 用低loss证明disentanglement；
7. 用高MI证明task sufficiency；
8. hard-sample后仍引用marginal-negative ratio；
9. 忽略critic overfit与adaptive selection；
10. 把alignment/uniformity当semantic guarantee。

## 十八、最小记忆

1. **InfoNCE是candidate-index cross-entropy。**
2. **Bayes score识别的是 $\log p(y\mid x)/p(y)+c(x)$。**
3. **$I\ge\log K-L$ 是population lower bound，不是finite-batch MI等式。**
4. **bound不能超过 $\log K$。**
5. **改变negative law就改变density ratio与estimand。**
6. **MI大、geometry好与downstream sufficient是不同claims。**

## 十九、掌握标准

- [ ] 能写candidate-index experiment；
- [ ] 能推导Bayes posterior和ratio score；
- [ ] 能写population InfoNCE loss；
- [ ] 能解释MI bound证明架构和ceiling；
- [ ] 能区分NCE/InfoNCE；
- [ ] 能列出五层gap；
- [ ] 能解释MI invariant反例；
- [ ] 能审计negative law、temperature与downstream claim。

## 二十、练习与独立详解

- 练习：[[习题 - 对比学习、InfoNCE 与密度比]]
- 独立详解：[[解答 - 对比学习、InfoNCE 与密度比]]

## 参考来源

- [[S-2018-Oord-Li-Vinyals-CPC]]
- [[S-2019-Poole-Variational-MI-Bounds]]
- [[S-2020-McAllester-Stratos-MI-Limitations]]
- [[S-2020-Wang-Isola-Alignment-Uniformity]]
- [[S-2010-Gutmann-Hyvarinen-NCE]]
- [[S-2018-Su-6024-深度学习的互信息]]
