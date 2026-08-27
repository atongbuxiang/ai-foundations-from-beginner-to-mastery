---
type: concept
status: draft
area: [learning-theory/foundations, no-free-lunch, inductive-bias]
aliases: [No Free Lunch, NFL Theorem, Inductive Bias]
node_id: LT-15
prerequisites: ["[[PAC 学习定义与样本复杂度]]", "[[可实现情形的一致 ERM 保证]]", "[[命题、量词与逻辑等价]]", "[[集合、元素与集合运算]]"]
related: ["[[样本复杂度下界与 Minimax 视角]]", "[[打散、增长与 VC 维]]", "[[结构风险最小化与非一致可学习性]]", "[[深度泛化证据地图与开放问题]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1996-Wolpert-Lack-of-A-Priori-Distinctions]]", "[[S-1984-Valiant-Theory-of-the-Learnable]]"]
exercises: ["[[习题 - No-Free-Lunch 与归纳偏置]]"]
solutions: ["[[解答 - No-Free-Lunch 与归纳偏置]]"]
created: 2026-08-20
updated: 2026-08-23
---

# No-Free-Lunch 与归纳偏置

> [!abstract] 本章主问题
> 对二分类中任意学习算法 $A$ 和任意 $m<|\mathcal X|/2$，总能构造一个甚至完全 realizable 的分布 $P$，使 $A$ 在 $m$ 个 iid 样本后仍以至少 $1/7$ 的概率承受至少 $1/8$ 的总体错误。No-Free-Lunch 不是说“学习无用”或“所有算法在现实任务上一样”，而是说：若允许任意 target labeling，就没有一个算法能无条件外推；架构、函数类、表示、平滑性、数据增强、先验和优化偏好必须排除某些世界、偏爱另一些世界。

> [!question] 初学者读完必须能回答
> 1. 为什么 $m$ 个样本在 $2m$ 个候选点中至少留下 $m$ 个未见点？
> 2. 怎样构造两个在训练集上不可区分、在未见点标签相反的世界？
> 3. 为什么该构造仍可 realizable，却让任意算法承担常数错误？
> 4. No-Free-Lunch 的完整量词与“所有算法在现实任务上一样”有何不同？
> 5. 假设类、表示、架构、优化和数据协议各自怎样注入归纳偏置？

先用下图回答一个视觉问题：**如果训练集没有观察到一半输入点，任意 learner 凭什么决定这些点的标签，又必须在哪些世界中出错？**

![[00-知识库管理/_assets/figures/learning-theory/fig-no-free-lunch-inductive-bias-v2.svg|880]]

> [!figure] 图 20.2.7｜No-Free-Lunch 与归纳偏置
> A 将 $2m$ 点分为训练中已见与可能未见部分；B 构造在已见标签上完全一致、在未见标签上相反的两个世界，学习器因观测分布相同而不能同时正确；C 列出函数类、表示、架构、优化和数据协议中的归纳偏置。来源：独立绘制；理论接口参考 textbook No-Free-Lunch construction 与 Wolpert 的先验对称性讨论；生成脚本：[[plot_pac_finite_class_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** A 先做计数：重复抽样只会让未见点更多；B 固定训练记录后比较两个兼容 target，算法输出分布相同，但未见点上的正确动作相反；对随机 labeling 取平均，再用 averaging argument 选出一个固定坏 target。C 则把现实学习成功解释为偏置与真实结构的匹配。

**适用边界（图没有证明什么）。** 图没有证明所有算法在给定现实分布上表现相同，也没有否定学习、迁移或深度模型；它只说明允许任意 labeling 且不给结构假设时不存在统一外推保证。具体常数还依赖 theorem 版本与 expectation-to-probability 转换；归纳偏置也可能错配目标分布。

## 一、学习目标

1. 写出教材版 No-Free-Lunch theorem 的完整量词与常数；
2. 从 $2m$ 个点和全部 labelings 完整重建 adversarial construction；
3. 证明平均 expected risk 至少 $1/4$；
4. 把 expectation lower bound 转成 $1/7$—$1/8$ high-probability statement；
5. 解释为什么构造仍满足 realizability；
6. 推出无限域上“所有二分类函数类”不可 PAC 学习；
7. 区分教材 adversarial-distribution NFL 与 Wolpert target-average NFL；
8. 用量词解释 NFL 与 pointwise consistency 为什么不矛盾；
9. 识别 AI 系统中的归纳偏置来自哪里；
10. 纠正“所有模型一样”“深度学习违反 NFL”等常见口号。

## 二、定理陈述

考虑输入空间 $\mathcal X$、标签 $\mathcal Y=\{0,1\}$ 与 0–1 loss。令

$$
A:(\mathcal X\times\mathcal Y)^m\to\{0,1\}^{\mathcal X}
$$

为任意学习算法；它甚至可输出任意函数，不要求 proper。

若

$$
m<\frac{|\mathcal X|}{2},
$$

则存在一个 $P$ over $\mathcal X\times\{0,1\}$，使：

1. 存在 $f:\mathcal X\to\{0,1\}$ 且
   $$
   R_P(f)=0;
   $$
2. 对 $S\sim P^m$，
   $$
   \boxed{
   \Pr\left(R_P(A(S))\ge\frac18\right)
   \ge\frac17.
   }
   $$

若 $A$ 有内部随机种子 $U$，可把概率写成 $\Pr_{S,U}$；同一 averaging argument 仍适用。

> [!important] 量词顺序
> $$
> \forall A,\forall m<|\mathcal X|/2,
> \exists P,\exists f:
> \Pr_S(\text{failure})\ge1/7.
> $$
> adversarial distribution 可以依赖算法和样本预算。定理没有说存在一个固定 $P$ 让所有算法都同样失败。

## 三、第一步：选出 $2m$ 个点

因为 $|\mathcal X|>2m$，可选

$$
C=\{x_1,\ldots,x_{2m}\}\subset\mathcal X.
$$

只在这个有限子集上构造困难问题。考虑 $C$ 上所有二进制 labelings：

$$
\mathcal F_C
=\{f:C\to\{0,1\}\}.
$$

其大小为

$$
|\mathcal F_C|=2^{2m}.
$$

对每个 $f\in\mathcal F_C$，定义分布 $P_f$：

$$
P_f(X=x,Y=f(x))=\frac1{2m}
\qquad(x\in C).
$$

也就是说，输入在 $C$ 上均匀，标签由 $f$ 确定。

显然

$$
R_{P_f}(f)=0.
$$

所以每个候选困难分布都是 noiseless、realizable 的。困难不来自标签噪声，而来自未观察点上没有任何可利用结构。

## 四、第二步：至少一半点未见

训练集有 $m$ 个 examples，即使输入从不重复，也至多覆盖 $m$ 个 distinct points。因为 $C$ 有 $2m$ 个点，所以对每个 input sequence：

$$
|C\setminus\{X_1,\ldots,X_m\}|
\ge m.
$$

记未见集合为

$$
U(S_X)=C\setminus\{X_1,\ldots,X_m\}.
$$

重复抽样只会让未见点更多，不会帮助 learner。

## 五、第三步：未见标签上的平均错误是 $1/2$

先固定训练输入序列 $S_X$、已见标签以及算法随机性。对任一未见点 $x\in U(S_X)$：

- 算法的预测 $A(S)(x)$ 只依赖已见信息；
- 若从所有 $f\in\mathcal F_C$ 均匀选择 target，则 $f(x)$ 是独立公平 bit；
- 因而无论算法预测 0 还是 1，平均错误概率都是 $1/2$。

形式上：

$$
\mathbb E_{f\sim\operatorname{Unif}(\mathcal F_C)}
\mathbf1\{A(S_f)(x)\ne f(x)\}
=\frac12.
$$

每个未见点在 $P_f$ 下质量为 $1/(2m)$，未见点至少 $m$ 个，因此对 targets 与 samples 联合平均：

$$
\begin{aligned}
\mathbb E_f\mathbb E_{S\sim P_f^m}
R_{P_f}(A(S))
&\ge
m\cdot\frac1{2m}\cdot\frac12\\
&=\frac14.
\end{aligned}
$$

这就是 proof 的 information bottleneck：样本没有携带未见 labels 的任何信息。

## 六、第四步：从平均 target 找到一个坏 target

若所有 $f$ 都满足

$$
\mathbb E_{S\sim P_f^m}R_{P_f}(A(S))<\frac14,
$$

那么对 $f$ 的平均也会小于 $1/4$，与上一步矛盾。因此至少存在一个 $\bar f$：

$$
\boxed{
\mathbb E_{S\sim P_{\bar f}^m}
R_{P_{\bar f}}(A(S))
\ge\frac14.
}
$$

令困难分布 $P=P_{\bar f}$。它由 deterministic target $\bar f$ 产生，所以仍 realizable。

## 七、第五步：把期望转换成常数概率

令

$$
Z=R_P(A(S))\in[0,1],
$$

并记

$$
q=\Pr(Z\ge1/8).
$$

在事件 $Z<1/8$ 上，$Z\le1/8$；在其余事件上，粗略用 $Z\le1$。所以

$$
\mathbb EZ
\le\frac18(1-q)+1\cdot q
=\frac18+\frac78q.
$$

又知 $\mathbb EZ\ge1/4$，故

$$
\frac14
\le\frac18+\frac78q.
$$

整理：

$$
\frac18\le\frac78q
\quad\Longrightarrow\quad
\boxed{q\ge\frac17.}
$$

因此

$$
\Pr(R_P(A(S))\ge1/8)
\ge1/7.
$$

> [!note] 这不是 Markov 不等式
> Markov 从 expectation upper bound 推 tail upper bound；这里使用 boundedness，把 expectation lower bound 转为 tail lower bound。

## 八、推论：所有函数组成的类不可 PAC 学习

设 $\mathcal X$ 是无限集合，令

$$
\mathcal H=\{0,1\}^{\mathcal X},
$$

即所有二分类函数。

假设它 PAC learnable。选择

$$
\varepsilon<1/8,
\qquad
\delta<1/7.
$$

PAC 定义应给某个有限

$$
m=m_{\mathcal H}(\varepsilon,\delta).
$$

因为 $\mathcal X$ 无限，可选 $2m$ 个点并应用 NFL。于是存在 realizable $P$，使 failure probability 至少 $1/7>\delta$ 且 risk 至少 $1/8>\varepsilon$，与 PAC 合同矛盾。

所以

$$
\boxed{
\{0,1\}^{\mathcal X}
\text{ 在无限域上不可 PAC 学习。}
}
$$

## 九、这一定理为什么叫“没有免费午餐”

若 hypothesis class 包含任意 labeling，algorithm 必须允许每个未见点标签任意变化。任何外推规则都隐含一个偏好：

- nearest neighbor 偏好局部相似；
- linear classifier 偏好线性边界；
- convolution 偏好局部和平移共享；
- Transformer architecture 偏好 tokenized sequence、attention 和 parameter sharing；
- data augmentation 偏好某些变换保持标签；
- weight decay/norm/margin 偏好特定解；
- pretraining 偏好与预训练分布共享的表示。

这些偏好排除了大量 arbitrary labelings。若真实任务与偏好匹配，学习就可能成功；若不匹配，则产生 misspecification 或 harmful invariance。

## 十、归纳偏置的形式

### 10.1 restriction bias

只允许 $h\in\mathcal H$，直接排除其他函数。有限 class、VC dimension 与 norm constraints 属于此类。

### 10.2 preference bias

class 很大，但算法偏爱其中某些成员：regularization、implicit bias、early stopping、minimum norm、MDL prior。

### 10.3 representation bias

tokenizer、features、architecture 和 pretrained representation 决定哪些规律容易表达或优化。

### 10.4 data/augmentation bias

sampling、augmentation、negative construction 与 curriculum 声明了哪些变换、邻域或因果结构重要。

### 10.5 evaluation bias

loss、benchmark 和 judge 定义“成功”是什么。它可能推动系统优化 proxy 而非部署价值。

> [!important] bias 不是贬义词
> 没有偏置就无法从有限 observations 外推。关键问题不是“有没有 bias”，而是 bias 是否透明、是否与 target environment 对齐、在 shift 下怎样失败。

## 十一、Wolpert NFL 与教材 theorem 的区别

Wolpert 1996 研究 off-training-set error，并在对 target functions 或 priors 作对称平均时比较算法，得到缺乏 a priori algorithm distinction 的结果。

本节教材 theorem 则：

- 先固定任意算法与样本量；
- 再构造一个 realizable distribution；
- 给出具体的 $1/7$ failure probability 与 $1/8$ risk；
- 用于证明 unrestricted class 不可 PAC 学习。

两者共享“无任务偏好则无统一优势”的精神，但随机对象、平均方式和常数不同。不能把所有称 NFL 的定理当成完全同一命题。

## 十二、NFL 与 consistency 不矛盾

某个 memorization algorithm 可能对每个固定离散分布 $P$ 最终 pointwise consistent：随着 $m\to\infty$，高质量点陆续被看见。

NFL 的量词是

$$
\forall m,\exists P_m:\text{在这个样本预算下失败}.
$$

pointwise consistency 可能是

$$
\forall P,\exists m_P:\text{超过分布依赖阈值后成功}.
$$

交换 $\forall P$ 与 $\exists m$ 会改变命题。PAC 要一个只依 $(\varepsilon,\delta,\mathcal H)$、不依具体 $P$ 的统一 threshold；pointwise consistency 可让 threshold 依 $P$。

## 十三、NFL 与 Minimax

NFL proof 已有 minimax 味道：

$$
\inf_A\sup_{P\in\mathcal P}
\Pr_P(R_P(A(S))\ge1/8)
\ge1/7
$$

对于包含全部 labelings 的问题族成立。证明先对 targets 平均，再推出存在一个 worst-case target，这与 Yao/minimax reasoning 相似。

LT-16 会把这种逻辑抽象为：

- upper bound：构造一个算法；
- lower bound：任取算法，构造难分布；
- testing reduction：若学习成功，就能区分本来很难区分的 distributions。

## 十四、AI 领域中的正确解释

### 14.1 “大模型违反 NFL”

不对。大模型使用了强烈归纳偏置：互联网语料分布、tokenization、architecture、pretraining objective、optimization 和人类反馈。它们在自然任务上有效，恰恰说明任务不是均匀任意 labeling。

### 14.2 “所有架构平均一样，所以不用比较”

NFL 的平均通常覆盖极其宽、对称的 target family。现实研究关心一个高度非均匀的 task distribution；在这个 distribution 上架构可以显著不同。

### 14.3 “更多数据最终解决一切”

有限域上若最终观察所有点，memorization 可行；巨大/连续域、distribution shift、partial observability 与 action feedback 下，样本永远有限且外推结构仍必需。

### 14.4 benchmark 优势是 task-conditional evidence

某算法在固定 benchmarks 上更好，证明它与这些 task/protocol 更匹配；不能无条件推出对所有未来任务更好。需要明确 target family 和 transfer assumptions。

## 十五、归纳偏置的 trade-off

限制 class 产生两面：

$$
R_P(h_S)-R^*
=\underbrace{R_{\mathcal H}^*-R^*}_{\text{bias / approximation}}
+\underbrace{R_P(h_S)-R_{\mathcal H}^*}_{\text{selection / estimation}}.
$$

更小 $\mathcal H$：

- 可能更容易从有限样本选择，降低 estimation error；
- 也可能排除 truth，增加 approximation error。

NFL 不是要求 class 越小越好，而是要求显式管理 bias–complexity trade-off。

## 十六、如何“打破”NFL 的对称性

不是推翻 theorem，而是增加真实结构：

1. 限制 VC dimension、norm、margin 或 smoothness；
2. 假设 target 属于某个 generative/causal family；
3. 使用 informative prior 或 pretrained representation；
4. 允许 active queries 获取最有信息的 labels；
5. 假设 cluster/manifold/invariance structure；
6. 明确 distribution family 而非全部 $P$；
7. 用 task ensemble/meta-distribution 定义平均性能。

每一种“免费午餐”都由新假设付费。

## 十七、常见误解

> [!failure] “NFL 证明所有算法表现完全相同”
> 只在指定的对称平均/问题族和 performance definition 下；特定任务分布上可明显不同。

> [!failure] “NFL 证明学习不可能”
> 它证明无结构的 universal learning 不可能；有合适归纳偏置时 PAC learning 完全可能。

> [!failure] “realizable 就一定容易”
> 本 theorem 的困难分布完全 realizable，但 class 太宽、未见 labels 无结构。

> [!failure] “只要训练误差为零就能外推”
> 全部 labelings class 中有海量零训练误差 extensions，它们在未见点任意冲突。

> [!failure] “某个 bias 在一个 benchmark 有效，所以是普遍先验”
> 这是 task-conditional evidence；跨域有效性还需新的 family/shift 证据。

## 十八、证明模板

1. 任取算法 $A$ 与样本量 $m$；
2. 选 $2m$ 个输入点；
3. 枚举这组点的全部 $2^{2m}$ labelings；
4. 每个 labeling 定义 uniform realizable distribution；
5. 固定 sample inputs，数出至少 $m$ 个未见点；
6. 对 targets 平均，未见点错误为 $1/2$；
7. 得联合平均 risk 至少 $1/4$；
8. 由平均推出存在一个坏 target；
9. 用 $Z\in[0,1]$ 把期望 lower bound 转成 tail lower bound；
10. 回到量词，说明 adversary 能依 $A,m$ 选择 $P$。

## 十九、本节边界与来源说明

- $1/7$—$1/8$ theorem 与证明采用标准教材 Theorem 5.1；
- Wolpert 1996 用于区分 target/prior average 下的 NFL；
- 不把 optimization NFL、supervised OTS NFL 和本节 PAC impossibility theorem 混成同一公式；
- 科学空间没有承担该 theorem 的正式来源角色。

## 二十、掌握检查

- [ ] 我能写对 NFL 的全部量词；
- [ ] 我能重建 $2m$ 点与全部 labelings 的构造；
- [ ] 我能证明 average expected risk $\ge1/4$；
- [ ] 我能推导 $1/7$—$1/8$ tail 常数；
- [ ] 我能说明困难分布仍 realizable；
- [ ] 我能推出 unrestricted class 不可 PAC 学习；
- [ ] 我能区分教材 theorem 与 Wolpert NFL；
- [ ] 我能为具体 AI 系统列出 restriction/preference/representation/data/evaluation biases。

## 二十一、进一步连接

- [[样本复杂度下界与 Minimax 视角]]：把 adversarial construction 系统化为 testing lower bound；
- [[打散、增长与 VC 维]]：一个 class 能否在有限点上实现任意 labeling，正是 NFL construction 能否嵌入的关键；
- [[结构风险最小化与非一致可学习性]]：允许 hypothesis-dependent 样本阈值时，量词怎样改变；
- [[深度泛化证据地图与开放问题]]：现代模型的归纳偏置应由什么证据确认。
