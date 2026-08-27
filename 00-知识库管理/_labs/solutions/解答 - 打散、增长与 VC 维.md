---
type: solution
status: draft
area: [learning-theory/vc, combinatorics/capacity]
topic: "[[打散、增长与 VC 维]]"
exercise: "[[习题 - 打散、增长与 VC 维]]"
prerequisites: ["[[集合、元素与集合运算]]", "[[数学归纳、递归与组合计数]]"]
related: ["[[增长函数与经验二分模式]]", "[[二分类统计学习基本定理]]"]
sources: ["[[S-1971-Vapnik-Chervonenkis-Uniform-Convergence]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - 打散、增长与 VC 维

> [!warning] 使用方式
> VC 题的上下界量词相反：下界只需构造一个可打散点集；上界必须排除任意更大点集。若解答没有明确这两个量词，即使结论数值正确也不算完整证明。

## A. 识别与复述

### LT-VC-A01

$$
h|_C=(h(x_1),\ldots,h(x_m))\in\{0,1\}^m,
$$

$$
\mathcal H|_C=\{h|_C:h\in\mathcal H\}.
$$

$C$ 被打散是 $\mathcal H|_C=\{0,1\}^m$。完整量词为

$$
\forall\boldsymbol y\in\{0,1\}^m,
\ \exists h_{\boldsymbol y}\in\mathcal H,
\ \forall i\in[m],
\ h_{\boldsymbol y}(x_i)=y_i.
$$

$$
\operatorname{VCdim}(\mathcal H)
=\sup\{|C|:C\text{ finite and shattered by }\mathcal H\},
$$

若可打散任意大有限集合则为 $\infty$。

### LT-VC-A02

不等价。拟合给定训练标签只陈述

$$
\exists h\ \forall i:h(x_i)=y_i
$$

对一个固定 $\boldsymbol y$ 成立。打散要求对全部 $2^m$ 个 $\boldsymbol y$ 都分别存在实现者。前者是后者的一个必要片段，但远非充分。例如 thresholds 可拟合三点上的 $001$，却不能实现 $101$，所以三点未被打散。

### LT-VC-A03

若 $C$ 被 $\mathcal H_1$ 打散，每个 labeling 都由某个 $h\in\mathcal H_1$ 实现；因 $\mathcal H_1\subseteq\mathcal H_2$，同一 $h$ 也在 $\mathcal H_2$，所以 $C$ 也被 $\mathcal H_2$ 打散。对可打散规模取 supremum 即得不等式。

不能反推 inclusion。两个互不包含的 classes 可有相同 VC 维；例如实轴左阈值与右阈值类都为 1，但彼此不包含。

## B. 手算与构造

### LT-VC-B01

按 $(-2,1,4)$ 坐标顺序：

| pattern | 一个可行 $t$ |
|---|---:|
| $(0,0,0)$ | $t=5$ |
| $(0,0,1)$ | $t=3$ |
| $(0,1,1)$ | $t=0$ |
| $(1,1,1)$ | $t=-3$ |

没有其他 pattern，因为 $x_i<x_j$ 且 $h_t(x_i)=1$ 会推出 $t\le x_i<x_j$，从而 $h_t(x_j)=1$。即 1 的集合只能是后缀。

### LT-VC-B02

可实现：

$$
000,\ 100,\ 010,\ 001,\ 110,\ 011,\ 111.
$$

分别对应空样本 block、三个单点、两个相邻双点和全部三点。唯一缺少 $101$：任何包含 0 和 5 的区间也包含二者之间的 2。因此三点不被打散。

### LT-VC-B03

因为 $2^9=512\le1000<1024=2^{10}$，

$$
\operatorname{VCdim}(\mathcal H)
\le\lfloor\log_21000\rfloor=9.
$$

VC 维 3 只说明至少需要 $2^3=8$ 个 distinct restrictions 在某个三点集上，不说明 class 总大小恰为 8。它可以有 8、1000 或不可数多个 functions，同时仍只有 VC 维 3。

## C. 推导与证明

### LT-VC-C01

任取 $B\subseteq C$ 及任意 $y_B:B\to\{0,1\}$。在 $C\setminus B$ 上任意赋值，例如全部设为 0，得到补全 $\widetilde y:C\to\{0,1\}$。因 $C$ 被打散，存在 $h\in\mathcal H$ 满足 $h|_C=\widetilde y$。限制回 $B$ 得 $h|_B=y_B$。$y_B$ 任意，所以 $B$ 被打散。

### LT-VC-C02

下界：取 $x_1<x_2$。$00$ 可用避开两点的开区间；$10,01$ 用各点附近足够小的开区间；$11$ 用 $(x_1-\eta,x_2+\eta)$。所以两点被打散。

上界：任取 $x_1<x_2<x_3$，$101$ 不可实现，因为开区间是凸的：含 $x_1,x_3$ 就含中间 $x_2$。故 VC 维为 2。开/闭端点只影响恰落在边界的点；对有限互异样本可微调端点而保留所需包含关系，所以不改变最大可打散规模。

### LT-VC-C03

取 $d+1$ 个 affinely independent points。其增广向量

$$
\widetilde x_i=(x_i^\top,1)^\top\in\mathbb R^{d+1}
$$

线性无关；这正是 affine independence 的等价定义。因此以 $\widetilde x_i^\top$ 为行的方阵 $\widetilde X$ 可逆。

给 labels $y_i$，置 $s_i=2y_i-1\in\{-1,1\}$，解

$$
\widetilde X\widetilde w=\boldsymbol s,
\qquad\widetilde w=(\boldsymbol w^\top,b)^\top.
$$

则 $\boldsymbol w^\top x_i+b=s_i$，阈值化后恰得 $y_i$。任意 labeling 都可实现，因此该点集被打散，VC 维至少 $d+1$。

## D. 边界、反例与纠错

### LT-VC-D01

上界推理量词错了。某个三点集失败只说明这三个共线点没被打散；VC 下界只需存在另一个成功配置。在 $\mathbb R^2$ 取三个不共线点，它们 affinely independent，可由上一题构造任意 affine scores $\pm1$，所以被打散。证明 VC 小于 3 必须证明任意三点集都失败，这是假的。

### LT-VC-D02

令 $\mathcal X=\mathbb N$，$\theta=0.b_1b_2\cdots$ 采用标准二进制展开，定义 $h_\theta(i)=b_i$。任取有限 indices 和 labels，可选择 $\theta$ 的对应 bits 实现，所以 VC 维无穷。

它依赖一个实数携带无限精度、函数对参数高度不规则。线性模型的参数—VC 联系额外使用 affine/algebraic structure；它从未声称对任意实参数化都成立。

### LT-VC-D03

VC 维是对输入点集和 labeling 取 worst-case 的 class-level capacity；test error 是特定算法 $A$ 在特定数据分布 $P$、样本量 $m$、损失和训练结果上的随机/经验表现。大 VC 只允许更多 worst-case patterns，不强迫算法选坏函数，也不说明真实数据落在最坏配置。margin、norm、regularization、noise、distribution 和 evaluation protocol 都会影响 test error。

## E. AI 迁移

### LT-VC-E01

$$
\mathcal H
=\{x\mapsto\mathbf1[\boldsymbol w^\top\phi(x)+b\ge0]:
\boldsymbol w\in\mathbb R^{128},b\in\mathbb R\}.
$$

它是 $\mathbb R^{128}$ 中 affine halfspaces 拉回输入空间，VC 维至多 129；若 $\phi(\mathcal X)$ 含 129 个 affinely independent points，则达到 129。实际样本模式更低的情形包括：features 全落在 $r<128$ 的 affine 子空间；大量 features 重复/共线；或者 representation support 只覆盖狭窄区域。若 encoder 也 fine-tune，class 必须扩大，不能继续用冻结 probe 的 129。

### LT-VC-E02

至少审计：

1. hypothesis 是参数还是参数诱导的函数，是否存在表示冗余；
2. 激活函数、depth、计算图、weight sharing、bias 与输出 threshold；
3. 参数是无限精度实数、有限精度还是受范数/稀疏约束；
4. 声明是 VC upper bound、lower bound 还是精确值；
5. 是否引用适用于该架构的定理及其附加条件；
6. 代入样本量后泛化 bound 是否非平凡；
7. 是否把 worst-case class capacity 错当成训练算法或真实分布解释。

### LT-VC-E03

100% 只证明存在一个 prompt 实现真实 50-label vector；打散要求同一 50 个 inputs 上的全部 $2^{50}$ labeling 都分别可实现。部署泛化还要求这些问题是合法独立样本、prompt 选择没有把测试集自适应过拟合，并控制未来分布风险。

应补充两类不同证据：组合容量证据，例如明确 prompt class 并分析/下界它的 restrictions；统计泛化证据，例如预注册 class 后使用独立 holdout，或在新的 iid deployment-like sample 上评估并给置信区间。两者不能互相替代。
