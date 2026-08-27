---
type: concept
status: draft
area: [learning-theory/vc, combinatorics/capacity]
aliases: [Shattering, VC Dimension, Vapnik-Chervonenkis Dimension]
node_id: LT-17
prerequisites: ["[[有限假设类、Union Bound 与一致收敛]]", "[[No-Free-Lunch 与归纳偏置]]", "[[集合、元素与集合运算]]", "[[数学归纳、递归与组合计数]]"]
related: ["[[增长函数与经验二分模式]]", "[[Sauer-Shelah 引理]]", "[[VC 一致收敛与泛化界]]", "[[二分类统计学习基本定理]]"]
sources: ["[[S-1971-Vapnik-Chervonenkis-Uniform-Convergence]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
exercises: ["[[习题 - 打散、增长与 VC 维]]"]
solutions: ["[[解答 - 打散、增长与 VC 维]]"]
created: 2026-08-20
updated: 2026-08-23
---

# 打散、增长与 VC 维

> [!abstract] 本章主问题
> 一个 binary hypothesis class 的 VC 维，不数它有多少参数，也不问它能否拟合某一组标签；它问的是：**是否存在同一组 $d$ 个输入点，使这个类能实现这组点上的全部 $2^d$ 种二分标签。** 能做到就称这组点被打散（shattered）。VC 维是可被打散点集规模的上确界；当它有限时就是最大值，当它无穷时表示任意大的有限点集都有某个配置可被打散。

> [!question] 初学者读完必须能回答
> 1. Shattering 的“存在点集、对所有 labeling、存在 hypothesis”量词怎样排列？
> 2. 为什么“拟合过一组标签”远弱于“打散同一组点”？
> 3. Thresholds、intervals、affine halfspaces 与 axis-aligned rectangles 的 VC 维上下界分别怎样证明？
> 4. 有限类为何满足 $\operatorname{VCdim}(\mathcal H)\le\log_2|\mathcal H|$？
> 5. VC 维为什么不等于参数个数，也不能单独预测某个模型的测试误差？

## 一、学习目标

1. 区分输入点、标签向量、hypothesis、class 与 restriction；
2. 用量词准确写出 shattering 和 VC dimension；
3. 证明 thresholds 的 VC 维为 1、区间的 VC 维为 2；
4. 理解 affine halfspaces 的 $d+1$ 与 axis-aligned rectangles 的 $2d$；
5. 证明有限类满足 $\operatorname{VCdim}(\mathcal H)\le\log_2|\mathcal H|$；
6. 识别“拟合一次”“参数多”“训练误差为零”与“打散”的区别；
7. 解释 VC 维为什么是 worst-case、representation-independent 的容量；
8. 把它映射到线性 probe、决策区域和神经分类器的函数类，而不把理论能力误写成实际泛化结论。

## 二、先看一个具体问题

设输入空间是实数轴，分类器是右侧阈值：

$$
\mathcal H_{\mathrm{thr}}
=\{h_t:t\in\mathbb R\},
\qquad
h_t(x)=\mathbf 1\{x\ge t\}.
$$

固定一个点 $C=\{x_1\}$。它有两种可能标签：

- 要标签 0，选 $t>x_1$；
- 要标签 1，选 $t\le x_1$。

所以一个点能被打散。

再固定两个不同点 $x_1<x_2$。四种标签中：

| $(h(x_1),h(x_2))$ | 能否实现 | 一种选择 |
|---|---:|---|
| $(0,0)$ | 能 | $t>x_2$ |
| $(0,1)$ | 能 | $x_1<t\le x_2$ |
| $(1,1)$ | 能 | $t\le x_1$ |
| $(1,0)$ | **不能** | 阈值右侧为 1，不会先 1 后 0 |

只缺一种 labeling，也不算打散。因此 thresholds 能打散 1 点，不能打散任意 2 点，VC 维为 1。把 thresholds 与 intervals 并排比较，可以看清两类最小阻碍的共同形式：**类别的结构迫使标签向量满足某种顺序约束。**

先看图回答：**单调性与连通性分别排除了哪一种 labeling，为什么“只缺一个模式”就足以否定打散？**

![[00-知识库管理/_assets/figures/learning-theory/fig-vc-shattering-minimal-examples-v2.svg|880]]

> [!figure] 图 1　两个“只缺一种 labeling”的最小阻碍
> 右阈值在 $x_1<x_2$ 上只能产生 $00,01,11$，缺失 $10$；闭区间在 $x_1<x_2<x_3$ 上无法产生 $101$，因为包含两端点必然包含中点。来源：依据本节定义与 *Understanding Machine Learning* 第 6 章的标准例子独立绘制；确定性 SVG 示意，无随机种子。

**怎样读图。** 左栏的限制来自单调性：沿有序样本向右，标签至多从 0 切换到 1 一次；右栏的限制来自连通性：标签 1 必须构成一个连续块。两种结构都把全部二分标记中的某些向量永久排除。

**适用边界（图没有证明什么）。** 图只完成两个**上界阻碍**：任意两点都缺失 $10$，任意三点都缺失 $101$。要断言 VC 维分别等于 1 和 2，还必须另行给出一个点、两个点确实可被打散的**下界构造**；图也不覆盖无序输入或非区间型函数类。

> [!intuition] “自由 bit”视角
> 被打散的每个点像一个可以独立开关的 bit。$d$ 个点若被打散，class 在同一输入集合上就能独立设置 $d$ 个 bit，共实现 $2^d$ 种行为。VC 维测量的是这种最坏情形独立自由度，而不是参数文件大小。

## 三、对象、限制与迹

固定：

- 输入空间 $\mathcal X$；
- binary label space $\mathcal Y=\{0,1\}$；
- hypothesis class $\mathcal H\subseteq\{0,1\}^{\mathcal X}$，即每个 $h$ 是从 $\mathcal X$ 到 $\{0,1\}$ 的函数；
- 有限、互异的点集 $C=\{x_1,\ldots,x_m\}\subseteq\mathcal X$。

把 $h$ 只看在 $C$ 上，得到标签向量

$$
h|_C
=\bigl(h(x_1),\ldots,h(x_m)\bigr)
\in\{0,1\}^m.
$$

整个 class 在 $C$ 上的限制（restriction，也叫 trace）为

$$
\mathcal H|_C
=\{h|_C:h\in\mathcal H\}
\subseteq\{0,1\}^m.
$$

不同 $h$ 若在 $C$ 上给出同一标签向量，在 $\mathcal H|_C$ 中只数一次。因为本节关心的是样本能区分多少**函数行为**，不是有多少参数表示。

也可把每个 $h$ 写成正类集合

$$
A_h=\{x\in\mathcal X:h(x)=1\}.
$$

于是 $h|_C$ 与交集 $A_h\cap C$ 一一对应。函数类语言和集合族语言只是 0–1 编码不同：

$$
\mathcal H|_C
\longleftrightarrow
\{A_h\cap C:h\in\mathcal H\}.
$$

这正是 [[Sauer-Shelah 引理]] 能从极值集合论进入学习理论的接口。

## 四、打散的正式定义与量词

> [!definition] 打散（shattering）
> 若
> $$
> \mathcal H|_C=\{0,1\}^{m},
> $$
> 即 $|\mathcal H|_C|=2^m$，则称 $\mathcal H$ 打散 $C$。

把等式展开为量词：

$$
\boxed{
\forall\boldsymbol y=(y_1,\ldots,y_m)\in\{0,1\}^{m},
\ \exists h_{\boldsymbol y}\in\mathcal H,
\ \forall i\in[m],\ h_{\boldsymbol y}(x_i)=y_i.
}
$$

读法是：对每一种标签向量，都允许选择一个可能不同的 hypothesis，使它在**同一个**点集上匹配该标签。

三个容易写错的地方：

1. $C$ 在检验全部 labeling 时不能更换；
2. 不要求同一个 $h$ 同时实现互相冲突的 labeling；每个 labeling 可选不同 $h$；
3. 必须实现全部 $2^m$ 种，不是“很多种”或“训练时碰到的那一种”。

### 4.1 否定怎样写

$C$ 未被打散等价于

$$
\exists\boldsymbol y\in\{0,1\}^m,
\ \forall h\in\mathcal H,
\ \exists i\in[m]:h(x_i)\ne y_i.
$$

要证明一个特定 $C$ 没被打散，只需构造一个 class 无法实现的 labeling。要证明**没有任何** $m$ 点集被打散，则必须对任意 $C$ 找到这样的 labeling。

## 五、VC 维

> [!definition] Vapnik–Chervonenkis dimension
> $$
> \operatorname{VCdim}(\mathcal H)
> =\sup\{|C|:C\subseteq\mathcal X\text{ finite and }\mathcal H\text{ shatters }C\}.
> $$
> 若可打散任意大的有限点集，定义 $\operatorname{VCdim}(\mathcal H)=\infty$。若连一个点也不能打散，VC 维为 0。

当上确界为有限整数 $d$ 时，它实际是最大值：存在一个 $d$ 点集被打散，但没有 $d+1$ 点集被打散。

### 5.1 downward closure

若 $C$ 被打散，则任意 $B\subseteq C$ 也被打散。证明如下：给 $B$ 上任意 labeling，把它任意补全到 $C$ 上；因为 $C$ 被打散，存在 $h$ 实现补全，限制回 $B$ 即实现原 labeling。

所以可打散规模不会出现“能打散 5 点却不能打散 3 点”的断层。

### 5.2 class inclusion monotonicity

若 $\mathcal H_1\subseteq\mathcal H_2$，则

$$
\operatorname{VCdim}(\mathcal H_1)
\le
\operatorname{VCdim}(\mathcal H_2).
$$

因为 $\mathcal H_1$ 能实现的每个 labeling，$\mathcal H_2$ 也能实现。扩大 class 不会降低组合容量。

## 六、标准例子与完整证明

计算 VC 维时，不能只展示一个成功例子，也不能只展示一个失败例子。设目标答案为 $d$，完整证明固定为两步：

1. **下界构造** $\operatorname{VCdim}(\mathcal H)\ge d$：找出一个具体的 $d$ 点集，并证明它的全部 $2^d$ 种 labeling 都能实现；
2. **上界阻碍** $\operatorname{VCdim}(\mathcal H)\le d$：任取一个 $d+1$ 点集，根据其结构构造至少一个不可实现的 labeling。

量词分别是“存在一个好配置”和“任意更大配置都有坏标签”。后面四个标准例子都按这个模板核对。

### 6.1 实轴 thresholds：VC 维为 1

下界已在开头证明：任意一个点可被打散。

上界：任取 $x_1<x_2$，labeling $(1,0)$ 无法由 $h_t(x)=\mathbf1\{x\ge t\}$ 实现。因为 $h_t(x_1)=1$ 意味着 $t\le x_1<x_2$，从而 $h_t(x_2)=1$，矛盾。因此没有两点集被打散：

$$
\boxed{\operatorname{VCdim}(\mathcal H_{\mathrm{thr}})=1.}
$$

### 6.2 实轴闭区间：VC 维为 2

令

$$
\mathcal H_{\mathrm{int}}
=\{h_{a,b}(x)=\mathbf1\{a\le x\le b\}:a\le b\}.
$$

**下界。** 取 $x_1<x_2$：

- $(0,0)$：选一个避开两点的小区间；
- $(1,0)$：在 $x_1$ 附近取小区间；
- $(0,1)$：在 $x_2$ 附近取小区间；
- $(1,1)$：取 $[x_1,x_2]$。

所以两点被打散。

**上界。** 任取 $x_1<x_2<x_3$。labeling $(1,0,1)$ 不可实现：任何同时包含 $x_1,x_3$ 的区间也包含中间点 $x_2$。故

$$
\boxed{\operatorname{VCdim}(\mathcal H_{\mathrm{int}})=2.}
$$

### 6.3 $\mathbb R^d$ 中 affine halfspaces：VC 维为 $d+1$

类为

$$
\mathcal H_{\mathrm{half}}
=\left\{
x\mapsto\mathbf1\{\boldsymbol w^\top x+b\ge0\}:
\boldsymbol w\in\mathbb R^d,b\in\mathbb R
\right\}.
$$

**下界。** 取 $d+1$ 个 affinely independent points $x_1,\ldots,x_{d+1}$。增广向量

$$
\widetilde x_i=(x_i^\top,1)^\top\in\mathbb R^{d+1}
$$

线性无关。给任意 labels，令 $s_i=2y_i-1\in\{-1,1\}$。方程组

$$
\widetilde X\widetilde w=\boldsymbol s
$$

有唯一解，其中第 $i$ 行是 $\widetilde x_i^\top$，$\widetilde w=(\boldsymbol w,b)$。于是 affine score 在各点恰为 $s_i$，正确实现 labeling。

**上界路线。** 任意 $d+2$ 个点由 Radon 定理可分成两个非空集合，其凸包相交。把一边标 1、另一边标 0。若一个 affine halfspace 实现该 labeling，则相交点作为两边的凸组合必须同时满足 score $\ge0$ 与 score $<0$，矛盾。因此不能打散 $d+2$ 点。

$$
\boxed{\operatorname{VCdim}(\mathcal H_{\mathrm{half}})=d+1.}
$$

这里 bias $b$ 对应多出的一个 affine 自由度；homogeneous halfspaces $\mathbf1\{\boldsymbol w^\top x\ge0\}$ 在合适约定下 VC 维为 $d$。

### 6.4 轴对齐长方体：VC 维为 $2d$

令 hypothesis 的正类为

$$
\prod_{j=1}^d[a_j,b_j]\subseteq\mathbb R^d.
$$

**下界构造。** $2d$ 个点 $\{\pm e_1,\ldots,\pm e_d\}$ 可被打散。给任意想保留的子集，逐坐标选择区间端点：若保留 $e_j$ 就让第 $j$ 维上界达到 1，否则把上界置于 1 以下；对 $-e_j$ 同理控制下界。其他坐标为 0，可同时保留所选点。

**上界。** 任取 $2d+1$ 个点。对每个坐标只需选出一个最小值见证和一个最大值见证，全部极值见证至多 $2d$ 个，因此至少有一点 $x_0$ 不是所选见证。把所有极值见证标 1、$x_0$ 标 0。任何包含全部见证的轴对齐长方体都包含它们的 bounding box，也包含坐标逐维夹在极值之间的 $x_0$，矛盾。

故

$$
\boxed{\operatorname{VCdim}(\mathcal H_{\mathrm{rect}})=2d.}
$$

四个几何论证看起来不同，但都能放入同一张“下界见证—上界阻碍”矩阵：哪一部分只需要存在性，哪一部分必须覆盖任意配置？

![[00-知识库管理/_assets/figures/learning-theory/fig-vc-geometric-lower-upper-v2.svg|880]]

> [!figure] 图 2　二维几何类的 VC 上下界证明矩阵
> 左列是 affine halfspaces：三个仿射无关点给下界，四点的 Radon 分割给上界；右列是 axis-aligned rectangles：$\{\pm e_1,\pm e_2\}$ 给下界，五点中的非极值点给上界。来源：依据本节证明独立绘制；未临摹教材或博客版式；确定性 SVG 示意，无随机种子。

**怎样读图。** 先横向区分类别，再纵向检查证明方向。上排只需展示一个精心选择的配置；下排必须从任意更大配置中抽取阻碍结构。蓝色表示下界见证，红色表示上界中故意构造的冲突标签。

**适用边界（图没有证明什么）。** 图只是 $d=2$ 的几何切片。它不能替代一般维度中的线性方程可解性、Radon 定理或“至多 $2d$ 个坐标极值见证”的证明；这些量词与维度依赖仍以上文推导为准，也不能直接推广到非仿射边界或旋转矩形。

## 七、有限类与 VC 维

若 $|\mathcal H|=M<\infty$，一个 $m$ 点集被打散需要至少 $2^m$ 个不同 restrictions。每个 $h$ 最多贡献一个 restriction，所以

$$
2^m\le M.
$$

取以 2 为底的对数：

$$
m\le\log_2M.
$$

因此

$$
\boxed{
\operatorname{VCdim}(\mathcal H)
\le\lfloor\log_2|\mathcal H|\rfloor.
}
$$

反方向不成立。例如在实轴上取至少两个彼此不同、并能在某个输入点上给出不同标签的 thresholds，VC 维仍只有 1；即使 $M$ 很大，它们在任意有序样本上的 labeling 仍高度嵌套，不提供 $\log_2M$ 个独立 bit。若类中只有一个函数，VC 维则为 0。

## 八、参数个数为什么不是定义

对规则良好的线性、低次多项式或分段线性族，参数个数常与 VC 维相关。但“$p$ 个实参数所以 VC 维就是 $p$”没有一般定理。

构造一个极端反例。令 $\mathcal X=\mathbb N$，每个 $\theta\in[0,1)$ 采用不以无限个 1 结尾的标准二进制展开

$$
\theta=0.b_1b_2b_3\cdots,
$$

定义

$$
h_\theta(i)=b_i.
$$

这个类只有一个实参数 $\theta$，但任取有限 indices $i_1,\ldots,i_m$ 和任意 labels，只需把相应二进制位设成这些 labels，就能找到 $\theta$ 实现。因此它能打散任意有限集合，VC 维为无穷。

> [!warning] 这里暴露的是 representation 陷阱
> 一个无限精度实数能编码无限 bits。实际神经网络 VC 结果需要依赖激活的代数/分段结构、计算图和精度模型，不能只看参数向量的维数，也不能用这个病理构造否定所有参数相关上界。

## 九、VC 维能说什么，不能说什么

### 9.1 它能说

- class 在最坏有限点集上的二分表达力；
- 是否可能存在 distribution-free binary uniform-convergence/PAC 结果的关键组合坐标；
- 通过 [[Sauer-Shelah 引理]] 控制任意 $m$ 点上的最大模式数；
- 为模型类之间的容量比较提供 representation-independent 基线。

### 9.2 它不能单独说

- 训练算法实际会输出哪个 $h$；
- 数据分布是否会遇到可打散的 worst-case geometry；
- margin、norm、stability、augmentation 或 optimization bias；
- bound 的常数是否在现代深网规模上非平凡；
- test set 被自适应复用后是否仍合法。

VC 维是 class-level worst-case quantity。算法与数据依赖的细化要进入 [[Rademacher 复杂度与经验复杂度]]、[[分类间隔、Margin Bound 与 SVM 接口]] 和 [[算法稳定性与替换一个样本]]。

## 十、AI 中的对象映射

### 10.1 线性 probe

固定 representation $\phi:\mathcal X\to\mathbb R^d$，训练 affine binary probe

$$
h_{\boldsymbol w,b}(x)
=\mathbf1\{\boldsymbol w^\top\phi(x)+b\ge0\}.
$$

- 数学对象：$\phi(x)\in\mathbb R^d$ 是 feature；$(\boldsymbol w,b)$ 是 probe 参数；
- 调用位置：对冻结表征做下游分类；
- class：所有 feature-space affine halfspaces；
- 容量：若 $\phi(\mathcal X)$ 含足够一般位置的点，VC 维至多且通常达到 $d+1$；
- 失败边界：若表示落在低维子空间或高度退化，实际 trace 可能远小于 $d+1$；若同时 fine-tune $\phi$，class 已不是固定 probe 类。

### 10.2 决策树与规则系统

树的 leaf 数、depth、feature tests 共同限制可实现 label patterns。VC 思路要求先定义完整函数类：允许哪些 split、树是否固定结构、阈值是否连续、是否剪枝。只报告“一棵训练树有 200 个节点”不是 class 定义。

### 10.3 神经网络

网络参数 $\theta\in\mathbb R^p$ 诱导函数

$$
h_\theta(x)=\mathbf1\{f_\theta(x)\ge0\}.
$$

VC 维讨论的是 $\{h_\theta:\theta\in\Theta\}$ 的函数行为，不是参数集合本身。激活函数、深度、计算单元、weight sharing 和输出 threshold 都会改变 class。有限 VC 可给最坏情形可学习性，但对过参数化网络的实际泛化通常过粗，后续需要 norm、margin、compression、stability 或 data-dependent structure。

## 十一、常见误区与反例

> [!warning] 误区 1：训练误差为零，所以训练集被打散
> 零训练误差只实现真实标签这一种 labeling。打散要求在相同输入上，class 对全部 $2^m$ 种人为 labeling 都各有一个 hypothesis。

> [!warning] 误区 2：某个 $d$ 点集没被打散，所以 VC 维小于 $d$
> VC 维取“存在某个点集”的最坏情况。一个坏几何配置失败不能排除另一个配置成功。证明上界必须覆盖任意 $d$ 点集。

> [!warning] 误区 3：VC 维 $d$ 意味着恰好只有 $2^d$ 个函数
> VC 维限制有限样本模式，不限制函数总数。threshold class 不可数无限，但 VC 维只有 1。

> [!warning] 误区 4：VC 维大必然 test error 大
> 大容量表示 worst-case overfitting 机会更大，不是给某次训练的 error 下界。分布、算法偏置、margin 和样本量仍会改变实际结果。

## 十二、前沿地位与研究边界

- **经典定理**：shattering、VC 维、有限类对数上界及标准几何类结果；
- **已建立方法**：VC 维通过增长函数控制 distribution-free binary learning；
- **实践边界**：深网的参数规模可使 worst-case VC bound 数值上松，但这不使 theorem 错误；它说明所选 complexity 没有利用训练算法、数据几何与实际解；
- **开放接口**：什么 complexity 能同时对 feature learning、optimization trajectory、scale 与 data geometry 敏感，仍是深度泛化研究的核心问题。

## 十三、本节回顾

学完后应能不看正文回答：

1. $\mathcal H|_C$ 中究竟数什么？
2. shattering 的 $\forall\boldsymbol y\exists h$ 为什么不能交换？
3. thresholds 和 intervals 的缺失 labeling 分别是什么？
4. 为什么 finite $|\mathcal H|$ 给出 $\log_2|\mathcal H|$ 上界但不保证取等？
5. 参数个数与 VC 维为什么只能在附加结构下关联？
6. VC 维怎样进入下一节的增长函数，而又为什么尚未直接得到泛化概率？

## 十四、来源与后继

- 原始历史与事件族视角：[[S-1971-Vapnik-Chervonenkis-Uniform-Convergence]]；
- 现代教材校准：[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]] 第 6 章；
- 下一步：[[增长函数与经验二分模式]]把“最大可完全打散规模”升级为每个样本量 $m$ 的精细模式计数；
- 训练闭环：[[习题 - 打散、增长与 VC 维]]与[[解答 - 打散、增长与 VC 维]]。
