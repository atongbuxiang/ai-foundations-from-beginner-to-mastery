---
type: solution
status: draft
area: [learning-theory/vc, learning-theory/multiclass]
topic: "[[多分类的 Natarajan 维与 Graph 维]]"
exercise: "[[习题 - 多分类的 Natarajan 维与 Graph 维]]"
prerequisites: ["[[多分类的 Natarajan 维与 Graph 维]]"]
related: ["[[实值函数类、伪维与阈值化]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - 多分类的 Natarajan 维与 Graph 维

> [!warning] 使用边界
> 所有维数题都要给出见证与不可能性两部分。只展示很多标签或很多参数，不构成 shattering 证明。

## A. 识别与复述

### LT-MC-A01

点集 $C$ 被 Natarajan-shatter 当且仅当

$$
\exists f_0,f_1:C\to\mathcal Y,
\quad f_0(x)\ne f_1(x)\ \forall x,
$$

$$
\forall T\subseteq C,\ \exists h_T\in\mathcal H:
\quad
h_T(x)=f_1(x)\ (x\in T),
\quad
h_T(x)=f_0(x)\ (x\notin T).
$$

$C,f_0,f_1$ 在 $T$ 之前固定；$h_T$ 可依赖 $T$。见证标签可随点变化，却不能随 desired pattern 改写。

### LT-MC-A02

Graph shattering 要求存在固定 $f:C\to\mathcal Y$，使每个 $T$ 都有 $h_T$ 满足

$$
h_T(x)=f(x)\quad(x\in T),
$$

$$
h_T(x)\ne f(x)\quad(x\notin T).
$$

补集上只规定“不等”，所以替代标签可依赖 $T,h_T,x$；Natarajan 则预先固定 $f_0(x)$ 作为补标签。前者约束更弱，因此更容易打散。

### LT-MC-A03

- class PAC learnable：存在某 learner 满足统一 PAC 合同；
- 存在 good ERM：至少一种经验最优 tie-breaking 满足合同；
- 指定 ERM learnable：给定的 output range/tie-breaking rule 满足合同；
- 任意 ERM learnable：所有返回经验最优函数的规则都满足合同。

一般 multiclass setting 中四者强度依次增加，不能自动互换。

## B. 手算与数值判断

### LT-MC-B01

输入域只有两个点，所以任何维数至多 2。全函数类可对 $a,b$ 独立赋任意标签。取

$$
f_0(a)=f_0(b)=0,
\qquad
f_1(a)=f_1(b)=1.
$$

四个子集对应标签向量

$$
(0,0),(1,0),(0,1),(1,1),
$$

均在 $\mathcal H$ 中，因此两个点被 Natarajan-shatter，$d_N=2$。由 $d_N\le d_G\le|\mathcal X|=2$，$d_G=2$。

### LT-MC-B02

一个点可选两个不同常数标签，因此 $d_N,d_G\ge1$。两个不同点上所有 restrictions 都形如 $(y,y)$，不能实现 $(y_1,y_0)$ 这样的混合 pattern，所以二者都小于 2：

$$
d_N=d_G=1.
$$

$\log_2 1000$ 只反映 hypothesis 个数的 finite-class selection price，不是能独立打散多少输入点。

### LT-MC-B03

$$
d_N\log_2K
=20\log_2100
\approx20(6.644)
\approx132.9.
$$

所以量级坐标约 133。关系写的是

$$
d_G\le C d_N\log K
$$

一类 universal-constant 上界，并依赖对数底与 theorem convention；不能断言 $d_G=132.9$，维数本来也必须是整数。

## C. 推导与证明

### LT-MC-C01

若 $C$ 有 Natarajan 见证 $f_0,f_1$，令 Graph reference $f=f_1$。对任意 $T$，Natarajan 给出的 $h_T$ 满足：

$$
x\in T\Rightarrow h_T(x)=f_1(x)=f(x),
$$

$$
x\notin T\Rightarrow h_T(x)=f_0(x)\ne f_1(x)=f(x).
$$

所以同一 $C$ 被 graph-shatter。对所有可 Natarajan-shatter 的 $C$ 取 supremum，得 $d_N\le d_G$。

### LT-MC-C02

当 $\mathcal Y=\{0,1\}$：

- Natarajan 每点两个不同标签只能是 0/1，可能交换次序；自由二选一等价于实现全部 binary labelings；
- Graph 中 $h(x)\ne f(x)$ 唯一等价于 $h(x)=1-f(x)$，所以 match/mismatch pattern 也等价于任意 binary labeling。

因此一个点集被任一三种定义打散当且仅当被另外两种打散，最大基数相同：

$$
d_N=d_G=\operatorname{VCdim}.
$$

### LT-MC-C03

令

$$
G_h=\{(x,y):h(x)=y\}.
$$

若 $C=\{x_i\}$ 被 reference $f$ graph-shatter，取扩展点 $\widetilde C=\{(x_i,f(x_i))\}$。对每个 $T$，

$$
(x_i,f(x_i))\in G_{h_T}
\iff h_T(x_i)=f(x_i)
\iff x_i\in T,
$$

所以 $\widetilde C$ 被 $\{G_h\}$ VC-shatter。

反之，若扩展点集 $\{(x_i,y_i)\}$ 被 $\{G_h\}$ VC-shatter，它不可能含相同 $x$ 的两个不同标签：包含这两点的 subset 要求单个 $h(x)$ 同时等于两标签。因此输入坐标不同。令 $f(x_i)=y_i$，membership/nonmembership 正好给出 equality/inequality，故 $\{x_i\}$ 被 graph-shatter。

error set $E_h=G_h^c$。对任何有限点集，取补把每个 realized bit vector 逐位翻转；能实现全部 patterns 的性质不变，所以 VC 维不变。

## D. 边界、反例与纠错

### LT-MC-D01

取 $C=\{a,b\}$、$\mathcal Y=\{0,1,2\}$，只含三个常数函数：

$$
\mathcal H|_C=\{(0,0),(1,1),(2,2)\}.
$$

在每个单点上都能看到三个标签，当然“各能取两个标签”。但任意两个预先见证标签若要 Natarajan-shatter 两点，都必须实现一个在 $a,b$ 选择不同分支的 mixed pattern；常数类做不到。因此逐点 richness 不等于联合 combinatorial freedom。

### LT-MC-D02

至少有四个断点：

1. $d_N$ 控制 argmax prediction patterns，不直接控制 real-valued logits；
2. generic ERM 0–1 uniform convergence 自然使用 $d_G$，从 $d_N$ 到 $d_G$ 还需 finite-$K$ 关系；
3. cross-entropy 可因正确类概率趋零而无界，Hoeffding/0–1 tail 不适用；
4. surrogate excess 到 0–1 excess 需要 calibration bridge；
5. end-to-end score class 还需 norm/Rademacher/covering 等容量控制。

### LT-MC-D03

若 $K=\infty$，$\log K$ 无意义或发散，有限标签组合抽取论证不能直接使用。可替代的结构包括：

- 限制每个输入可达的 label set / learner output range；
- 标签 embedding 与 Lipschitz score/margin 结构；
- hierarchical/factorized output；
- description length 或 label-frequency assumptions。

必须用对应 theorem 重新建立容量，而不是形式上把 $K$ 换成“有效标签数”。

## E. AI 迁移

### LT-MC-E01

- label space：$\mathcal Y$ 为 50,000 tokens；
- score class：$f_\theta(x)\in\mathbb R^{50000}$；
- argmax class：$h_\theta(x)=\arg\max_y f_{\theta,y}(x)$；
- loss class：$(x,y)\mapsto-\log\operatorname{softmax}(f_\theta(x))_y$。

Natarajan/Graph 维直接描述第三项的 multiclass 0–1 pattern。第二项需实值/vector-valued complexity；第四项还需 loss composition、range/tail；token sequence dependence另需采样合同。

### LT-MC-E02

保持训练数据和 empirical error 完全相同，构造多种 tie-breaking：例如优先常见类、最小 label id、层级邻近类或随机标签。对稀有/未见输入 strata 分别测 per-class risk、macro risk 与 calibration，并在独立样本上比较。

tie-breaking 属于 learner/output rule，不是 nominal class 本身；class 决定可选函数集合，learner 决定在经验并列时输出哪个函数。

### LT-MC-E03

层级/序列任务合同至少写：

- $X$、结构化 $Y$ 与可行动作；
- sample unit 和 dependence；
- exact-match、token、tree-distance 或 cost-sensitive loss；
- score/factorization class 与 inference algorithm；
- comparator 与 approximation error；
- evaluation distribution 与 label-set shift。

flat 0–1 theorem把整个结构只视为一个 label，可能令 $K$ 指数大、忽略局部 loss 和共享结构，也不反映 inference hardness。
