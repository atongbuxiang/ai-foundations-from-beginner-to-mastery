---
type: concept
status: draft
area: [math/probability, math/statistics, ai/probabilistic-modeling]
aliases: [条件概率与贝叶斯公式, Bayes Rule, 全概率公式]
prerequisites: ["[[样本空间、事件与概率公理]]"]
related: ["[[随机变量、分布与分位数]]", "[[联合分布、边缘分布与独立性]]", "[[Bayesian 推断与后验预测]]", "[[概率论与数理统计 MOC]]"]
sources: ["MIT-6.041SC-Lecture-2", "MIT-6.436J-Lecture-3", "Harvard-Stat110-Conditioning", "Bertsekas-Tsitsiklis-Introduction-Probability", "Su-9262-Diffusion-Conditional-Probability", "Su-5253-VAE-Posterior"]
exercises: ["[[习题 - 条件概率、全概率与 Bayes 公式]]"]
solutions: ["[[解答 - 条件概率、全概率与 Bayes 公式]]"]
created: 2026-08-18
updated: 2026-08-27
---

# 条件概率、全概率与 Bayes 公式

> [!abstract] 本章主问题
> 条件概率 $P(A\mid B)=P(A\cap B)/P(B)$ 在已知 $B$ 发生后重新归一化原概率空间；全概率公式按互斥原因分解证据，Bayes 公式再把“原因产生证据的概率”反转为“看到证据后原因的概率”。它是概率恒等式，不自动提供先验、似然、因果方向或模型正确性。

## 学习目标

完成本章后，你应能：

1. 从样本空间筛选解释条件概率的分子和分母；
2. 证明固定 $B$ 后 $P(\cdot\mid B)$ 仍是概率测度；
3. 区分 $P(A\mid B)$、$P(B\mid A)$ 与 $P(A\cap B)$；
4. 推导乘法公式和多事件链式法则；
5. 用事件分割推导全概率公式；
6. 从乘法公式推导有限/可数 Bayes 公式；
7. 区分先验、似然、证据和后验；
8. 用频数表、概率树和代数三种方式核对同一答案；
9. 用 odds 与 likelihood ratio 进行顺序更新；
10. 解释 base-rate fallacy 为什么发生；
11. 处理连续变量中的密度 Bayes 公式并说明零概率条件化边界；
12. 识别不可能证据、选择偏差与 Simpson reversal；
13. 区分观测条件化与因果干预；
14. 把 softmax、label shift、VAE 和扩散模型中的条件分布对应到公式；
15. 用 log-domain 与 logsumexp 稳定计算后验。

> [!question] 初学者读完必须能回答
> 1. 条件概率的分子与分母分别承担筛选和归一化中的什么作用？
> 2. 为什么 $P(A\mid B)$ 与 $P(B\mid A)$ 通常不同？
> 3. 全概率公式为什么要求原因互斥且穷尽？
> 4. prior、likelihood、evidence 与 posterior 各是什么对象？
> 5. odds 形式怎样把多次证据更新变成乘法？
> 6. Bayes 恒等式为什么不能自动证明因果解释或模型正确？

先用下图回答一个视觉问题：**条件化、全概率和 Bayes 更新怎样分别对应“筛选—汇总—反转”三种操作？**

![[00-知识库管理/_assets/figures/probability/fig-conditioning-bayes-odds-v2.svg|880]]

> [!figure] 图 10.5.2｜条件化归一、原因分割与 odds 更新
> A 在事件 $B$ 内重新归一；B 把证据 $E$ 按互斥原因 $H_i$ 汇总；C 用低 base-rate 检测示例展示 posterior odds = prior odds × likelihood ratio。来源：独立绘制；生成脚本：[[plot_probability_foundations_v2.py]]；确定性数值示例，无随机种子。

**怎样读图。** A 先将 $B$ 外质量删除，再用 $P(B)$ 缩放；B 沿每个原因到证据的路径计算加权和；C 则先把概率转成 odds，再乘似然比，观察高灵敏度为何仍可能被极低先验率压制。

**适用边界（图没有证明什么）。** Venn 图只适用于正概率事件的直观条件化，不构造零概率事件上的 regular conditional probability。检测例子的数值结论依赖给定先验与似然，也不能把观测条件化解释为干预因果效应。

## 进入正文前：Bayes 更新是同一联合概率的两种分解

> [!info] 课程位置
> [[样本空间、事件与概率公理]]已经给隐藏来源和两次抛掷赋予联合质量；本章只是在观察证据后重新归一，并把生成方向 $P(E\mid Z)$ 反转成诊断方向 $P(Z\mid E)$。下一章会把观察结果编码为随机变量及其分布。

> [!tip] 建议两遍阅读
> - **第一遍：** 用联合表、概率树和 odds 三种方法重算一次正面与两次正面后的来源后验。
> - **第二遍：** 再读连续条件密度、零概率条件、选择偏差、Simpson reversal、因果边界和数值稳定实现。

> [!question] 本章的推导问题链
> 1. 已知事件发生后，哪些原子被删除，剩余质量怎样重新缩放到 $1$？
> 2. 全概率公式怎样把一个证据按互斥来源拆开？
> 3. Bayes 公式为什么没有“倒转条件”这么简单，而必须包含先验和证据归一化？
> 4. 顺序观察多条条件独立证据时，odds 为什么可以逐次乘 likelihood ratio？

### 第一次正面怎样更新隐藏来源

沿用

$$
P(Z=F)=\frac23,
\qquad
P(Z=B)=\frac13,
$$

以及

$$
P(X_i=1\mid Z=F)=\frac12,
\qquad
P(X_i=1\mid Z=B)=\frac34.
$$

令证据

$$
E_1=\{X_1=1\}.
$$

按来源分割做全概率：

$$
\begin{aligned}
P(E_1)
&=P(E_1\mid Z=F)P(Z=F)
+P(E_1\mid Z=B)P(Z=B)\\
&=\frac12\cdot\frac23
+\frac34\cdot\frac13\\
&=\frac7{12}.
\end{aligned}
$$

Bayes 更新为

$$
\boxed{
P(Z=B\mid E_1)
=\frac{(3/4)(1/3)}{7/12}
=\frac37.}
$$

观察正面后，偏置硬币的概率从 $1/3$ 上升到 $3/7$，但没有变成 $3/4$；后者是似然 $P(E_1\mid Z=B)$，不是后验。

odds 形式把同一计算压缩为

$$
\underbrace{\frac{P(B)}{P(F)}}_{1/2}
\times
\underbrace{\frac{P(E_1\mid B)}{P(E_1\mid F)}}_{3/2}
=
\underbrace{\frac{P(B\mid E_1)}{P(F\mid E_1)}}_{3/4}.
$$

若第二次也观察到正面，并使用“给定 $Z$ 后两次抛掷独立”的模型假设，则再乘一次 $3/2$：

$$
\frac{P(B\mid X_1=X_2=1)}
{P(F\mid X_1=X_2=1)}
=\frac12\left(\frac32\right)^2
=\frac98.
$$

所以

$$
\boxed{
P(B\mid X_1=X_2=1)=\frac9{17}.}
$$

也可直接由八原子表核对：

$$
P(B,1,1)=\frac3{16},
\qquad
P(X_1=X_2=1)=\frac{17}{48},
$$

从而 $(3/16)/(17/48)=9/17$。

> [!note] 符号账本
> | 符号 | 类型 | 含义 |
> |---|---:|---|
> | $Z$ | 离散随机变量 | 未观察的硬币来源 |
> | $E_1$ | 事件 | 第一次观察到正面 |
> | $P(B)$ | 概率 | 偏置来源的先验 |
> | $P(E_1\mid B)$ | 条件概率 | 偏置来源产生证据的似然 |
> | $P(E_1)$ | 概率 | 对所有来源加权后的证据概率 |
> | $P(B\mid E_1)$ | 条件概率 | 观察证据后的后验 |
> | likelihood ratio | 正数 | 两个来源对同一证据的相对支持 |

> [!analysis] Bayes 公式的公式七问
> | 问题 | 回答 |
> |---|---|
> | 核心公式是什么？ | $P(H_i\mid E)=P(E\mid H_i)P(H_i)/\sum_jP(E\mid H_j)P(H_j)$。 |
> | 分母从哪里来？ | 全概率公式对互斥且穷尽的原因求和，使更新后的所有后验重新归一为 $1$。 |
> | 四个角色是什么？ | $P(H_i)$ 是先验，$P(E\mid H_i)$ 是似然，$P(E)$ 是证据，$P(H_i\mid E)$ 是后验。 |
> | 为什么不能倒转条件？ | $P(E\mid H)$ 与 $P(H\mid E)$ 的分母不同；后者还必须包含 base rate。 |
> | odds 形式何时可连乘？ | 当多条证据在给定假设后条件独立时，联合 likelihood ratio 才分解为各次比值的乘积。 |
> | 怎样验收？ | 用联合表、概率树和代数/odds 至少两路核对，并检查后验归一化和先验敏感性。 |
> | AI 中怎样调用？ | 分类先验偏移、Naive Bayes、VAE 后验、扩散条件反转和序列证据更新都依赖相同分解。 |

> [!success] 第一遍停靠线
> 若你能从全概率得到 $P(X_1=1)=7/12$，再分别用分数公式和 odds 得到 $P(B\mid X_1=1)=3/7$，并在两次正面后得到 $9/17$，就已掌握本章主干。还应能逐项说出 prior、likelihood、evidence 与 posterior。

## 零、阅读前检查

需要掌握：

- 概率空间 $(\Omega,\mathcal F,P)$；
- 交集、并集和事件分割；
- 概率公理与可列可加性；
- 基本分数、比值和对数。

本章先以 $P(B)>0$ 的事件条件化为主。给定连续随机变量精确取值的严格条件分布需要联合密度或 regular conditional probability；我们会说明公式边界，但完整测度论放到条件期望节点。

## 一、先看一个具体问题：高准确率检测为何后验仍不高

某疾病患病率为 $1\%$：

$$
P(D)=0.01.
$$

检测灵敏度 $99\%$：

$$
P(+\mid D)=0.99.
$$

特异度 $95\%$，所以假阳性率为

$$
P(+\mid D^c)=0.05.
$$

问题是：观察到阳性后，$P(D\mid +)$ 是多少？绝不能把 $P(+\mid D)=0.99$ 直接倒过来。

### 1.1 用 10,000 人频数表

按模型期望频数：

| | 阳性 | 阴性 | 合计 |
|---|---:|---:|---:|
| 患病 | $99$ | $1$ | $100$ |
| 未患病 | $495$ | $9405$ | $9900$ |
| 合计 | $594$ | $9406$ | $10000$ |

阳性人群中患病比例为

$$
P(D\mid +)=\frac{99}{594}=\frac16\approx16.7\%.
$$

检测本身很灵敏，但低先验患病率使假阳性数量仍然很大。这就是 base rate 不能被忽略的最小例子。

## 二、条件概率的定义

> [!definition] 条件概率
> 对事件 $A,B\in\mathcal F$ 且 $P(B)>0$，定义
> $$
> P(A\mid B)=\frac{P(A\cap B)}{P(B)}.
> $$

### 2.1 逐项理解

- $B$ 是已知发生的信息；
- $A\cap B$ 是新宇宙 $B$ 内同时满足 $A$ 的部分；
- 除以 $P(B)$ 把整个新宇宙重新归一为 1。

因此

$$
P(B\mid B)=1,
\qquad
P(B^c\mid B)=0.
$$

### 2.2 条件概率不是集合大小比的普遍定义

在有限等可能模型中，

$$
P(A\mid B)=\frac{|A\cap B|}{|B|}.
$$

这是因为每个基本结果质量相同；非均匀或连续模型必须用概率测度/密度，而不是数元素。

## 三、固定条件后得到新的概率测度

固定 $B$ 且 $P(B)>0$，定义

$$
Q(A)=P(A\mid B).
$$

验证三条公理：

1. 非负性：$P(A\cap B)\ge0$，所以 $Q(A)\ge0$；
2. 归一化：

   $$
   Q(\Omega)=\frac{P(\Omega\cap B)}{P(B)}=1;
   $$

3. 若 $A_i$ 两两不交，则 $A_i\cap B$ 也两两不交，故

   $$
   Q\left(\bigcup_iA_i\right)
   =\frac{P(\bigcup_i(A_i\cap B))}{P(B)}
   =\sum_iQ(A_i).
   $$

> [!important] 关键认识
> 条件概率不是一种“较弱的概率”；固定条件后，它本身就是合法概率测度。因此补集、容斥、union bound 等所有概率规则仍可在条件世界中使用。

## 四、乘法公式：从条件回到联合

由定义直接整理：

$$
\boxed{P(A\cap B)=P(B)P(A\mid B).}
$$

对称地，若 $P(A)>0$，

$$
P(A\cap B)=P(A)P(B\mid A).
$$

于是

$$
P(A)P(B\mid A)=P(B)P(A\mid B).
$$

### 4.1 多事件链式法则

若相关条件事件概率为正，则

$$
\boxed{
P(A_1\cap\cdots\cap A_n)
=P(A_1)
\prod_{k=2}^nP(A_k\mid A_1\cap\cdots\cap A_{k-1}).
}
$$

它只是一再应用乘法公式，不要求独立。

### 4.2 语言模型中的链式法则

对 token 序列 $x_{1:T}$，

$$
p(x_{1:T})
=p(x_1)\prod_{t=2}^Tp(x_t\mid x_{<t}).
$$

自回归模型选择用网络参数化这些条件分布。链式分解本身总成立；“只依赖有限上下文”才是额外结构假设。

## 五、事件分割与全概率公式

> [!definition] 事件分割
> $H_1,H_2,\ldots$ 构成 $\Omega$ 的可数分割，如果它们两两不交且
> $$
> \bigcup_iH_i=\Omega.
> $$

任意事件 $E$ 可分成互斥部分：

$$
E=E\cap\Omega
=E\cap\left(\bigcup_iH_i\right)
=\bigcup_i(E\cap H_i).
$$

由可列可加性与乘法公式：

$$
\boxed{
P(E)=\sum_iP(E\cap H_i)
=\sum_iP(E\mid H_i)P(H_i).
}
$$

这就是全概率公式。

### 5.1 它在做什么

当直接计算 $P(E)$ 困难时，按互斥原因 $H_i$ 分层：

1. 原因 $H_i$ 出现的概率；
2. 该原因下产生证据 $E$ 的概率；
3. 对所有原因加权求和。

在检测例中，$D,D^c$ 构成分割：

$$
P(+)=P(+\mid D)P(D)+P(+\mid D^c)P(D^c).
$$

## 六、Bayes 公式：把生成方向反转

从乘法公式，若 $P(E)>0$，

$$
P(H_i\mid E)
=\frac{P(E\cap H_i)}{P(E)}
=\frac{P(E\mid H_i)P(H_i)}{P(E)}.
$$

再用全概率展开分母：

$$
\boxed{
P(H_i\mid E)
=\frac{P(E\mid H_i)P(H_i)}
{\sum_jP(E\mid H_j)P(H_j)}.
}
$$

### 6.1 四个角色

| 名称 | 符号 | 固定什么、变化什么 |
|---|---|---|
| 先验 prior | $P(H_i)$ | 看证据前对假设的概率 |
| 似然 likelihood | $P(E\mid H_i)$ | 固定证据 $E$，把它视为假设 $H_i$ 的函数 |
| 证据 evidence | $P(E)$ | 对所有假设加权后的归一化常数 |
| 后验 posterior | $P(H_i\mid E)$ | 看到证据后对假设的概率 |

“posterior proportional to likelihood × prior”写作

$$
P(H_i\mid E)\propto P(E\mid H_i)P(H_i),
$$

但比例式隐藏了归一化分母。比较假设时可暂时省略；需要合法后验概率或跨模型比较时不能忘记。

### 6.2 检测例的代数核对

$$
P(D\mid +)
=\frac{0.99\times0.01}
{0.99\times0.01+0.05\times0.99}
=\frac{0.0099}{0.0594}
=\frac16.
$$

频数表和代数得到同一答案；概率树则把每条路径的联合概率写成边概率乘积。

## 七、odds 与 likelihood ratio

对二元假设 $H$ 与 $H^c$，定义 odds：

$$
O(H)=\frac{P(H)}{P(H^c)}.
$$

Bayes 公式两边取比：

$$
\frac{P(H\mid E)}{P(H^c\mid E)}
=\frac{P(E\mid H)}{P(E\mid H^c)}
\frac{P(H)}{P(H^c)}.
$$

即

$$
\boxed{
O(H\mid E)=\operatorname{LR}(E)\,O(H),
}
$$

其中

$$
\operatorname{LR}(E)=\frac{P(E\mid H)}{P(E\mid H^c)}
$$

是 likelihood ratio。

### 7.1 对数域

取对数得到加法更新：

$$
\log O(H\mid E)
=\log O(H)+\log\operatorname{LR}(E).
$$

这既便于解释证据贡献，也避免极小概率直接相乘下溢。

### 7.2 多条证据顺序更新

一般情况：

$$
P(H\mid E_1,E_2)
\propto P(E_2\mid H,E_1)P(H\mid E_1).
$$

只有在给定 $H$（以及竞争假设）后证据条件独立时，likelihood ratio 才能简单相乘。把相关证据重复当独立，会产生过度自信。

## 八、三种解题表示必须互相核对

### 8.1 频数表

适合低维离散问题，最能暴露 base rate。可以任选方便总人数，只要所有格子按同一比例缩放。

### 8.2 概率树

沿边相乘得到一条路径的联合概率；对互斥路径相加得到边缘概率。树的第一层选择体现分解方向。

### 8.3 代数公式

适合一般化和证明，但最容易把条件方向写反。每次写公式前先用自然语言读：

> “在什么已经知道的条件下，问什么事件？”

## 九、经典例题：Monty Hall 的信息机制

三扇门后仅一辆车。你先选门 1；主持人知道车的位置，并且总会在其余两门中打开一扇羊门。主持人打开门 3 后是否应换到门 2？

关键不是“还剩两门”，而是主持人的条件机制。

令 $C_i$ 表示车在门 $i$，$M_3$ 表示主持人打开门 3。若车在门 1，主持人在门 2/3 中等概率开；若车在门 2，他必须开门 3；若车在门 3，他不可能开门 3。因此

$$
P(M_3\mid C_1)=\frac12,
\quad
P(M_3\mid C_2)=1,
\quad
P(M_3\mid C_3)=0.
$$

先验均为 $1/3$，所以

$$
P(C_2\mid M_3)
=\frac{1\cdot(1/3)}{(1/2)(1/3)+1(1/3)+0(1/3)}
=\frac23.
$$

如果主持人不知情、可能误开车门，或选择规则不同，likelihood 会改变，答案也会改变。信息的价值来自产生信息的机制。

## 十、连续情形的 Bayes 公式

### 10.1 为什么不能直接写 $P(X=x)$

连续随机变量通常满足 $P(X=x)=0$。因此

$$
P(A\mid X=x)=\frac{P(A\cap\{X=x\})}{P(X=x)}
$$

是 $0/0$，不能用事件条件公式直接定义。

### 10.2 联合密度下的条件密度

若 $(X,Y)$ 有联合密度 $p_{X,Y}(x,y)$，且边缘密度

$$
p_Y(y)=\int p_{X,Y}(x,y)\,dx>0,
$$

则定义（几乎处处）

$$
\boxed{
p_{X\mid Y}(x\mid y)=\frac{p_{X,Y}(x,y)}{p_Y(y)}.
}
$$

若联合密度分解为

$$
p_{X,Y}(x,y)=p_{Y\mid X}(y\mid x)p_X(x),
$$

便得到密度版 Bayes：

$$
\boxed{
p_{X\mid Y}(x\mid y)
=\frac{p_{Y\mid X}(y\mid x)p_X(x)}
{\int p_{Y\mid X}(y\mid u)p_X(u)\,du}.
}
$$

密度只在选定基准测度下定义，且可在零测集上修改；后验分布才是坐标无关的主要对象。

### 10.3 零概率条件的严格边界

一般空间中，给定随机变量的信息需要 regular conditional distribution 或条件期望。它们通常只在“几乎处处”意义下唯一。不能从单个零概率切片的任意密度版本推出逐点物理结论。

## 十一、Bayes 公式不等于 Bayesian 推断的全部

Bayes 公式是恒等式；Bayesian 推断还要选择：

- 参数/潜变量空间；
- 先验分布；
- 数据似然；
- 模型比较或预测目标；
- 后验计算近似；
- 决策损失。

同一个 Bayes 恒等式也被频率主义计算、分类器纠偏、通信检测和生成模型使用。是否称为 Bayesian 方法，取决于哪些未知对象被赋予概率分布以及怎样进行推断。

## 十二、条件概率不等于因果

### 12.1 观测条件化

$$
P(Y\mid X=x)
$$

描述在观察到 $X=x$ 的子群中 $Y$ 的分布。

### 12.2 干预问题

$$
P(Y\mid do(X=x))
$$

描述主动把 $X$ 设置为 $x$ 后 $Y$ 的分布。混杂、选择机制和反向因果会使二者不同。

例如观察到“使用某治疗的人病情更重”，可能因为重症更容易接受治疗，不能由 $P(Y\mid X)$ 直接判断治疗有害。

### 12.3 Simpson reversal

总体关联方向可能在按混杂变量分层后反转。全概率公式告诉我们总体是各层条件概率的加权平均；不同组权重改变即可造成反转。识别因果还需要图结构或实验设计，不是再套一次 Bayes 公式。

## 十三、数值稳定地计算后验

对离散假设 $H_i$，设

$$
s_i=\log P(E\mid H_i)+\log P(H_i).
$$

后验为 softmax：

$$
P(H_i\mid E)=\frac{e^{s_i}}{\sum_je^{s_j}}.
$$

用

$$
m=\max_js_j
$$

改写：

$$
P(H_i\mid E)=\frac{e^{s_i-m}}{\sum_je^{s_j-m}}.
$$

减去共同常数不改变比值，却避免溢出/下溢。

### 13.1 必须同时审计

- $P(H_i)=0$ 会使该假设无法被有限 likelihood 挽救；
- 所有 $s_i=-\infty$ 表示证据在模型支持之外，不能静默输出均匀后验；
- 极端 log-likelihood 可能来自尺度错误或重复计数相关证据；
- 近似归一化会改变后验质量，需报告误差。

## 十四、AI 中的具体调用

### 14.1 分类器的条件分布

对 batch $X\in\mathbb R^{B\times d}$、$K$ 类标签，模型输出

$$
p_\theta(y=k\mid x_i),
\qquad
P\in[0,1]^{B\times K}.
$$

softmax 保证每行归一化，但不保证等于真实 $P(Y\mid X)$，更不保证部署分布下校准。模型训练、采样机制和 loss 共同决定它能近似什么。

### 14.2 先验偏移与类别重加权

若假设类条件分布近似不变：

$$
p_{\text{test}}(x\mid y)\approx p_{\text{train}}(x\mid y),
$$

但类别先验改变，则

$$
p_{\text{test}}(y\mid x)
\propto p_{\text{train}}(y\mid x)
\frac{p_{\text{test}}(y)}{p_{\text{train}}(y)}.
$$

这不是无条件纠偏公式；类条件不变、支持重叠和先验估计可靠都是必要审计项。

### 14.3 Naive Bayes

若特征 $X_1,\ldots,X_d$ 在给定类别 $Y$ 后条件独立，则

$$
p(y\mid x_{1:d})
\propto p(y)\prod_{j=1}^dp(x_j\mid y).
$$

“naive”正是条件独立假设。现实特征相关时，重复证据会使概率过度尖锐；分类边界仍可能有用，但后验校准需要另验。

### 14.4 VAE 的 prior、likelihood 与 posterior

生成方向通常写作

$$
p_\theta(z)p_\theta(x\mid z),
$$

真实后验为

$$
p_\theta(z\mid x)
=\frac{p_\theta(x\mid z)p_\theta(z)}{p_\theta(x)}.
$$

难点是证据

$$
p_\theta(x)=\int p_\theta(x\mid z)p_\theta(z)\,dz
$$

通常难算，才引入近似后验 $q_\phi(z\mid x)$。必须区分模型后验 $p_\theta$ 与推断网络 $q_\phi$。

### 14.5 扩散模型中的条件反转

前向加噪给出 $p(x_t\mid x_0)$，反向推断涉及 $p(x_0\mid x_t)$ 或中间条件分布。Bayes 恒等式连接二者，但实际算法还需要边缘 $p(x_t)$、score 或近似网络。科学空间的扩散推导可以作为条件概率恒等式的应用入口，但模型结构与近似误差必须另行审计。

## 十五、常见错误速查

| 错误 | 为什么错 | 修正 |
|---|---|---|
| $P(A\mid B)=P(B\mid A)$ | 条件改变分母与新宇宙 | 写联合概率并分别除以 $P(A),P(B)$ |
| 忽略 base rate | likelihood 不能单独决定 posterior | 用全概率算 evidence |
| 把 likelihood 当后验 | 关于参数未归一化且缺 prior | 乘 prior 并归一化 |
| 对 $P(B)=0$ 套事件公式 | 分母为零 | 使用密度/regular conditional framework |
| 相关证据 likelihood 相乘 | 重复计算信息 | 建模联合 likelihood 或条件链 |
| 条件关联解释为因果 | 选择和混杂未控制 | 区分 observe 与 intervene |
| softmax 输出即真实概率 | 只有形式归一化 | 校准并验证分布偏移 |

## 十六、验证协议

### 16.1 归一化检查

对每个证据 $E$，验证

$$
\sum_iP(H_i\mid E)=1.
$$

### 16.2 联合概率双路检查

验证

$$
P(H_i)P(E\mid H_i)
=P(E)P(H_i\mid E).
$$

### 16.3 表格—树—公式交叉

小问题必须能用频数表、概率树和 Bayes 公式得到同一结果。若不一致，通常是条件方向、分割遗漏或归一化错误。

### 16.4 敏感性扫描

扫描 prior、假阳性率或 likelihood ratio，观察后验如何变化。单点后验值不能替代对先验与模型错误的敏感性报告。

## 十七、研究边界

### 经典定理

- 条件概率、乘法公式、全概率与 Bayes 公式；
- 条件概率仍构成概率测度；
- 联合密度下的条件密度公式。

### 已建立方法

- likelihood ratio 检测；
- Bayesian 更新、Naive Bayes、先验偏移校正；
- 潜变量模型与扩散中的条件分布反转。

### 不能自动推出

- 模型先验客观正确；
- 条件概率有因果意义；
- 近似后验等于真实后验；
- 多条证据可条件独立相乘；
- 分布偏移下训练后验仍校准。

## 十八、掌握检查清单

- [ ] 我能用“限制到 $B$ 并重新归一化”解释条件概率。
- [ ] 我能证明 $P(\cdot\mid B)$ 是概率测度。
- [ ] 我能逐步推出乘法、链式、全概率和 Bayes 公式。
- [ ] 我能区分 prior、likelihood、evidence 与 posterior。
- [ ] 我能用频数表解释 base-rate fallacy。
- [ ] 我能使用 odds 和 log-likelihood ratio。
- [ ] 我不会在零概率事件上直接套分式定义。
- [ ] 我能区分条件概率与因果干预。
- [ ] 我能指出 VAE/扩散中的生成方向与推断方向。
- [ ] 我会用 logsumexp 稳定归一化并检查模型外证据。

## 十九、训练入口

- 分层习题：[[习题 - 条件概率、全概率与 Bayes 公式]]；
- 独立解答：[[解答 - 条件概率、全概率与 Bayes 公式]]。

## 来源与延伸

1. MIT 6.041SC, [Resource Index: Conditioning and Bayes’ Rule](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/pages/resource-index/)：本科条件化、树图与经典问题路线。
2. MIT 6.436J, [Lecture Notes](https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/pages/lecture-notes/)：条件概率、独立性与严格概率空间接口。
3. Harvard [Stat 110](https://stat110.hsites.harvard.edu/youtube)：Bayes、全概率、Monty Hall 与 Simpson paradox 的问题训练。
4. 苏剑林，[生成扩散模型漫谈（十）：统一扩散模型（理论篇）](https://spaces.ac.cn/archives/9262)：条件分布恒等式在扩散建模中的应用入口。
5. 苏剑林，[变分自编码器（一）：原来是这么一回事](https://spaces.ac.cn/archives/5253)：先验、生成条件分布与近似后验的 AI 问题入口；符号角色需按具体模型重新核对。

> [!success] 本章出口
> 看到任何“给定 $B$ 的 $A$”时，你应先检查条件事件、生成机制和分母，再决定用表格、树、odds 还是密度公式。下一章将把 $\omega$ 映射为数值 $X(\omega)$，并研究由此产生的分布、CDF 和分位数。
