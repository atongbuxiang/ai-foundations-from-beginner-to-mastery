---
type: concept
status: draft
area: [learning-theory/vc, learning-theory/multiclass]
aliases: [Natarajan Dimension, Graph Dimension, 多分类 VC 维]
node_id: LT-23
prerequisites: ["[[二分类统计学习基本定理]]", "[[打散、增长与 VC 维]]", "[[不可知 PAC、ERM 与双侧一致收敛]]"]
related: ["[[实值函数类、伪维与阈值化]]", "[[逻辑回归、复合损失与概率分类]]", "[[收缩引理与 Lipschitz 损失复合]]", "[[Online-to-Batch Conversion]]"]
sources: ["[[S-1989-Natarajan-On-Learning-Sets-Functions]]", "[[S-2015-Daniely-Multiclass-Learnability-ERM]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]"]
exercises: ["[[习题 - 多分类的 Natarajan 维与 Graph 维]]"]
solutions: ["[[解答 - 多分类的 Natarajan 维与 Graph 维]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-multiclass-natarajan-graph-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 多分类的 Natarajan 维与 Graph 维

> [!abstract] 本章主问题
> 对多分类函数类 $\mathcal H\subseteq\mathcal Y^{\mathcal X}$，普通 binary VC 维不再直接适用。Natarajan 维要求每个输入点预先指定两个不同标签，并由 $\mathcal H$ 实现全部逐点二选一模式；Graph 维先固定一幅 reference labeling，再要求任意子集上与 reference 相等、补集上不等。总有
> $$
> d_N(\mathcal H)\le d_G(\mathcal H),
> $$
> 二分类时二者都退化为 VC 维。有限标签集下，$d_N$ 刻画 PAC learnability，$d_G$ 自然控制 0–1 error graph 和 generic ERM；一般多分类中不同 ERM tie-breaking 甚至可能有不同 sample complexity。

> [!question] 初学者读完必须能回答
> 1. Natarajan shattering 中为什么每个点需要两个**预先固定且不同**的标签？
> 2. Graph shattering 的“相等/不等”与 Natarajan 的“两标签选择”有何强弱关系？
> 3. 为什么 $d_N\le d_G$，二分类时为什么相等？
> 4. Graph 维如何等价为预测图集合的 VC 维，并进入 ERM uniform convergence？
> 5. 为什么 label count、softmax 参数数和 Natarajan 维不是同一个对象？

## 一、学习目标

1. 严格定义 Natarajan 与 Graph shattering；
2. 用最小例子手工检验一个点集是否被打散；
3. 证明 $d_N\le d_G$ 和 binary collapse；
4. 把 Graph 维写成扩展域 $\mathcal X\times\mathcal Y$ 上的普通 VC 维；
5. 陈述有限标签集上的 learnability 与 ERM 边界；
6. 区分 0–1 task loss、multiclass surrogate 与 calibration；
7. 审计 large-vocabulary、structured output 与开放标签任务中的维数声明；
8. 说明“类别更多”何时影响 sample complexity，何时只是输出编码变化。

## 二、问题设置

固定：

- 输入空间 $\mathcal X$；
- 标签空间 $\mathcal Y$，本节主要假设有限，$|\mathcal Y|=K\ge2$；
- multiclass hypothesis class
  $$
  \mathcal H\subseteq\mathcal Y^{\mathcal X};
  $$
- 0–1 loss
  $$
  \ell(h,(x,y))=\mathbf1\{h(x)\ne y\}.
  $$

对有限点集 $C=\{x_1,\ldots,x_m\}$，restriction 集为

$$
\mathcal H|_C
=
\{(h(x_1),\ldots,h(x_m)):h\in\mathcal H\}
\subseteq\mathcal Y^m.
$$

最多可出现 $K^m$ 个标签向量；但直接数 $K^m$ 过于粗糙，因为真实 class 往往只实现其中极少一部分。

## 三、为什么 binary shattering 不能直接照搬

二分类时，每一点只有 0/1 两个标签，“实现任意标签”与“对每点做任意二选一”是同一件事。

多分类时至少有三种不同问题：

1. 每个点能否从某两个指定标签中自由选择？
2. 每个点能否选择任意 $K$ 个标签之一？
3. 相对某个 reference label，能否自由决定匹配还是不匹配？

若要求实现全部 $K^m$ 种标签，容量定义会过强；若只要求每点至少出现两个标签，却允许这两个标签随 desired pattern 改变，又会过弱且难以进行一致组合计数。Natarajan 与 Graph 定义分别固定了不同见证。

## 四、Natarajan Shattering

> [!definition] Natarajan 打散
> 点集 $C=\{x_1,\ldots,x_m\}$ 被 $\mathcal H$ Natarajan-shatter，若存在两幅见证标记
> $$
> f_0,f_1:C\to\mathcal Y,
> \qquad
> f_0(x_i)\ne f_1(x_i)\quad\forall i,
> $$
> 使对每个子集 $T\subseteq C$，都存在 $h_T\in\mathcal H$ 满足
> $$
> h_T(x)=
> \begin{cases}
> f_1(x),&x\in T,\\
> f_0(x),&x\notin T.
> \end{cases}
> $$

等价地，对每个 bit vector $b\in\{0,1\}^m$，类中都存在 $h_b$ 使

$$
h_b(x_i)=f_{b_i}(x_i).
$$

> [!definition] Natarajan 维
> $$
> d_N(\mathcal H)
> =\sup\{|C|:C\text{ 被 }\mathcal H\text{ Natarajan-shatter}\}.
> $$

### 4.1 三个细节

1. $f_0,f_1$ 在看到 desired subset $T$ **之前**固定；
2. 两个标签可随点 $x_i$ 改变，例如点 1 用 cat/dog，点 2 用 red/blue；
3. 必须实现全部 $2^m$ 个组合，仅逐点各能出现两个标签还不够。

## 五、Graph Shattering

> [!definition] Graph 打散
> 点集 $C$ 被 $\mathcal H$ graph-shatter，若存在一幅 reference labeling
> $$
> f:C\to\mathcal Y,
> $$
> 使对每个 $T\subseteq C$，都存在 $h_T\in\mathcal H$ 满足
> $$
> x\in T\Rightarrow h_T(x)=f(x),
> $$
> $$
> x\notin T\Rightarrow h_T(x)\ne f(x).
> $$

> [!definition] Graph 维
> $$
> d_G(\mathcal H)
> =\sup\{|C|:C\text{ 被 }\mathcal H\text{ graph-shatter}\}.
> $$

与 Natarajan 不同，补集上的“替代标签”不需要预先固定，也不要求同一 $x$ 在不同 pattern 中使用相同替代标签。因此 Graph shattering 较容易发生，容量不小于 Natarajan 维。

## 六、先用图分清两类见证

在证明关系前先回答：**左栏的两标签在何时固定，中栏的非 reference 标签又可依赖哪些对象？**

![[00-知识库管理/_assets/figures/learning-theory/fig-multiclass-natarajan-graph-v2.svg|900]]

> [!figure] 图 20.3.7｜Natarajan 二标签见证、Graph reference 见证与学习接口
> 左栏展示逐点固定的两标签选择；中栏展示相对 reference labeling 的匹配/偏离；右栏汇总 binary collapse、有限标签关系与 ERM 边界。来源：依据 Natarajan 1989 与现代 multiclass learning 理论独立绘制；确定性 SVG，由 [[plot_vc_extensions_v2.py]] 生成。

**怎样读图。** Natarajan 见证给 Graph 见证提供了一个固定“偏离标签”，所以左栏的自由度自动满足中栏；反方向不成立，因为 Graph 的偏离标签可以随 $T,h,x$ 改变。

**适用边界（图没有证明什么）。** 图没有给出所有常数、无限标签空间的完整刻画、surrogate calibration 或 structured prediction 的计算复杂度；右栏 $O(d_N\log K)$ 只在有限标签条件下表达量级关系。

## 七、证明 $d_N\le d_G$

假设 $C$ 被 Natarajan-shatter，见证为 $f_0,f_1$。令 Graph reference 为

$$
f=f_1.
$$

对任意 $T\subseteq C$，Natarajan 性质给出 $h_T$：

$$
x\in T\Rightarrow h_T(x)=f_1(x)=f(x),
$$

$$
x\notin T\Rightarrow h_T(x)=f_0(x)\ne f_1(x)=f(x).
$$

因此 $C$ 也被 graph-shatter，故

$$
\boxed{d_N(\mathcal H)\le d_G(\mathcal H).}
$$

证明只用了“两个见证标签逐点不同”。

## 八、二分类时为何都等于 VC 维

若 $\mathcal Y=\{0,1\}$：

- Natarajan 见证在每点只能是 $(0,1)$ 或 $(1,0)$，实现全部二选一模式等价于实现全部 binary labelings；
- Graph reference 的补标签是唯一的：$h(x)\ne f(x)$ 就强制 $h(x)=1-f(x)$。

所以

$$
d_N(\mathcal H)=d_G(\mathcal H)=\operatorname{VCdim}(\mathcal H).
$$

这解释了为什么 binary fundamental theorem 只需要一个维数，而 multiclass 要区分至少两个。

## 九、Graph 维就是预测图集合的 VC 维

为每个 $h\in\mathcal H$ 定义其 graph set

$$
G_h=\{(x,y)\in\mathcal X\times\mathcal Y:h(x)=y\}.
$$

令

$$
\mathcal G_{\mathcal H}=\{G_h:h\in\mathcal H\}.
$$

若 $C=\{x_1,\ldots,x_m\}$ 被 reference $f$ graph-shatter，就考察扩展域中的点

$$
\widetilde C=\{(x_i,f(x_i)):i=1,\ldots,m\}.
$$

对任意 $T$，

$$
(x_i,f(x_i))\in G_{h_T}
\iff h_T(x_i)=f(x_i)
\iff x_i\in T.
$$

所以 $\widetilde C$ 被 set class $\mathcal G_{\mathcal H}$ 普通 VC-shatter。反向也可从任一被 $\mathcal G_{\mathcal H}$ 打散且输入坐标不重复的扩展点集读出 reference labels。于是

$$
d_G(\mathcal H)=\operatorname{VCdim}(\mathcal G_{\mathcal H}).
$$

0–1 error set 是 graph set 的补：

$$
E_h=\{(x,y):h(x)\ne y\}=G_h^c.
$$

取补不改变 VC 维。因此 binary VC uniform-convergence machinery 可在扩展 observation domain 上用 $d_G$ 控制 multiclass 0–1 loss class。

> [!important] 为什么 generic ERM 自然看到 $d_G$
> ERM 比较的是训练 observation $(x_i,y_i)$ 上“预测是否等于真实标签”的 binary error pattern。Graph class 恰好编码这种 equality pattern，故 uniform convergence 直接依赖 $d_G$。

## 十、有限标签集中的维数关系

对 $K=|\mathcal Y|<\infty$，有量级关系

$$
d_N(\mathcal H)
\le d_G(\mathcal H)
\le O\bigl(d_N(\mathcal H)\log K\bigr).
$$

不同教材可给出不同 universal constant 与对数底；本节只使用量级，不宣称一个未追踪的精确常数。

直觉上，Graph 见证允许偏离 reference 时在至多 $K-1$ 个标签间变化；组合抽取论证可从足够大的 graph-shattered 集中找出一个子集，使替代标签稳定为逐点两标签见证，损失一个 $\log K$ 因子。

### 10.1 标签数不是容量本身

若 $\mathcal H$ 只有 $K$ 个常数分类器

$$
h_y(x)\equiv y,
\qquad y\in\mathcal Y,
$$

只要 $K\ge2$，就有

$$
d_N=d_G=1,
$$

无论 $K$ 多大。一个点可在两个常数标签间选择；两个不同点无法独立混合标签。

### 10.2 全函数类

若 $|\mathcal X|=n$ 且

$$
\mathcal H=\mathcal Y^{\mathcal X},
$$

则每个输入点都可独立选择任意标签，故

$$
d_N=d_G=n.
$$

即使 $K$ 从 2 增到 100，维数仍由输入域大小 $n$ 截断；标签数影响 pattern 数和常数，却不把可打散点数提升到 $n$ 以上。

## 十一、多分类基本学习结论

在有限标签集与常规可测性条件下，定性上：

$$
\boxed{
d_N(\mathcal H)<\infty
\quad\Longleftrightarrow\quad
\mathcal H\text{ is multiclass PAC learnable}.
}
$$

必要性可把 Natarajan-shattered 点集限制在每点两个标签上，复用 binary 未见点下界。充分性可通过 $d_G$ 的 uniform convergence 与有限标签关系得到。

但 quantitative statement 要更谨慎：

- lower bound 通常由 $d_N$ 构造；
- generic ERM uniform bound 自然含 $d_G$；
- 用 $d_G=O(d_N\log K)$ 可把上界写回 $d_N$ 和标签数；
- 更精细 learner、对称类或 output restriction 可改善 label dependence；
- 当 $K$ 无限或随样本增长时，必须重新声明条件。

## 十二、为什么“一个 ERM”与“任意 ERM”会分离

binary 0–1 classification 中，只要 ERM 输出某个经验最优函数，普通 VC 分析通常同时覆盖所有 tie-breaking。

多分类中，经验上相同的最小误差可以对应许多未见区域行为。[[S-2015-Daniely-Multiclass-Learnability-ERM]]表明一般 multiclass class 上：

1. 不同 ERM rule 可能有不同 sample complexity；
2. 某些 class 存在可学习的 ERM，同时也存在失败的 ERM；
3. output range 与 tie-breaking 本身成为 learner complexity 的一部分；
4. 对 label permutation 对称的类可得到更整齐的结论。

因此必须区分：

$$
\text{class is learnable},
$$

$$
\text{there exists a good ERM},
$$

$$
\text{this specified ERM rule is good},
$$

$$
\text{every ERM rule is good}.
$$

这四句话不再自动等价。

## 十三、从 0–1 类到 Surrogate Loss

实际 softmax 模型常优化 cross-entropy，而任务评价使用 0–1 accuracy。此时至少有三层：

1. score function class $f:\mathcal X\to\mathbb R^K$；
2. prediction rule $h_f(x)=\arg\max_y f_y(x)$；
3. surrogate loss $\ell_{\rm CE}(f(x),y)$。

$d_N$ 或 $d_G$ 控制 prediction functions 的 0–1 组合容量，不自动控制无界 logits 上的 cross-entropy loss values。要从 surrogate excess risk 推出 classification excess risk，还需要 calibration/consistency theorem；要控制 surrogate generalization，常使用 Rademacher complexity、norm bound、Lipschitz contraction 与 logit range。

> [!warning] 不能直接替换
> 把 binary VC theorem 中的 $d$ 换成 $d_N$，再把 0–1 loss 换成 cross-entropy，并不是合法证明。标签容量、score complexity、loss composition 与 calibration 是不同桥梁。

## 十四、Large Vocabulary 与 Structured Output

### 14.1 Large vocabulary

语言模型 token 预测的 $K$ 可达数万。$\log K$ 看似温和，但 class 的 score functions、共享 embedding、sequence context 和 autoregressive factorization远超单步 multiclass 0–1 模型。

### 14.2 Structured labels

若 $\mathcal Y$ 是序列、树、排列或集合，标签空间可能指数大甚至可数无限。此时：

- 不能只代入 $K=|\mathcal Y|$；
- 结构化 loss 可能不是 0–1 exact match；
- inference oracle 的计算复杂度成为瓶颈；
- 可使用 factorization、margin-rescaling、structured Rademacher 或 task-specific dimensions。

### 14.3 Open-set / new labels

若部署时出现训练标签集合外的新类，目标问题已不是固定 $\mathcal Y$ 上的 closed-set PAC classification。需要拒识、novelty detection、hierarchy 或 semantic representation 假设。

## 十五、AI 中的对象映射

| 实际对象 | 理论对象 | 容易错置之处 |
|---|---|---|
| softmax argmax | $h:\mathcal X\to\mathcal Y$ | 把 logit 函数类与 argmax class 混为一谈 |
| label vocabulary | $\mathcal Y$ | 只报 $K$，不报可实现标签模式 |
| tie-breaking | learner/output rule | 当作无关实现细节 |
| cross-entropy | surrogate loss | 用 0–1 Graph 维直接控制无界 loss |
| hierarchical labels | structured output | 当成普通 flat $K$-class 问题 |
| prompt-generated labels | data-dependent label/action set | 忽略标签空间随样本改变 |

## 十六、常见错误

> [!warning] “每个点都能预测至少两个标签，所以点集被 Natarajan 打散”
> 错。必须存在预先固定的两标签见证，并联合实现全部 $2^m$ 组合。

> [!warning] “Graph 偏离 reference 时必须使用同一个替代标签”
> 错。Graph 定义只要求不等，替代标签可随 hypothesis 和点变化；正因如此 $d_G$ 可大于 $d_N$。

> [!warning] “类别数为 $K$，所以容量是 $\log K$”
> 错。$K$ 只是一项坐标；class restrictions、input geometry 和 parameter sharing 决定可实现模式。

> [!warning] “有限 $d_N$ 证明任意 ERM 都有最佳率”
> 错。一般多分类中 tie-breaking 与 output range 会影响 ERM sample complexity。

> [!warning] “多分类定理直接解释 language modeling perplexity”
> 错。per-token log loss、sequence dependence、autoregressive factorization 与 vocabulary shift 都超出这里的 iid multiclass 0–1 合同。

## 十七、本节回顾

1. 写出 Natarajan shattering 的两个见证函数和全部量词。
2. 写出 Graph shattering 的 reference labeling 与相等/不等条件。
3. 用哪一个见证可立即证明 $d_N\le d_G$？
4. Graph 维怎样变成 $\mathcal X\times\mathcal Y$ 上 set class 的 VC 维？
5. 为什么常数分类器族在任意 $K\ge2$ 时维数仍为 1？
6. finite label 下 $d_G$ 与 $d_N$ 的量级关系是什么？
7. class learnability 与指定 ERM learnability 为什么要分开？
8. cross-entropy generalization 还缺哪两座桥？

## 十八、来源与后继

- 历史来源：[[S-1989-Natarajan-On-Learning-Sets-Functions]]；
- 现代 ERM 边界：[[S-2015-Daniely-Multiclass-Learnability-ERM]]；
- 教材校准：[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]与[[S-2018-Mohri-Rostamizadeh-Talwalkar-Foundations-ML]]；
- 下一步：[[实值函数类、伪维与阈值化]]把“多个标签”进一步推广到连续实值输出；
- 训练闭环：[[习题 - 多分类的 Natarajan 维与 Graph 维]]与[[解答 - 多分类的 Natarajan 维与 Graph 维]]。
