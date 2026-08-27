---
type: theorem
status: draft
area: [learning-theory/vc, combinatorics/extremal-set-theory]
aliases: [Sauer Lemma, Sauer-Shelah-Perles Lemma, VC Growth Lemma]
node_id: LT-19
prerequisites: ["[[增长函数与经验二分模式]]", "[[打散、增长与 VC 维]]", "[[数学归纳、递归与组合计数]]", "[[基本不等式与界的构造]]"]
related: ["[[VC 一致收敛与泛化界]]", "[[二分类统计学习基本定理]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]"]
sources: ["[[S-1972-Sauer-Density-Families-Sets]]", "[[S-1972-Shelah-Combinatorial-Problem]]", "[[S-1971-Vapnik-Chervonenkis-Uniform-Convergence]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
exercises: ["[[习题 - Sauer-Shelah 引理]]"]
solutions: ["[[解答 - Sauer-Shelah 引理]]"]
created: 2026-08-20
updated: 2026-08-23
---

# Sauer-Shelah 引理

> [!abstract] 本章主问题
> 若 binary class 的 VC 维为有限 $d$，则它在任意 $m$ 个点上最多产生
> $$
> \sum_{i=0}^{d}{m\choose i}
> $$
> 种 labeling；当 $m\ge d\ge1$ 时进一步不超过 $(em/d)^d$。因此一旦 class 不能打散 $d+1$ 点，最坏模式数便不能继续按 $2^m$ 指数增长，而至多按 $m^d$ 多项式增长。证明核心是把最后一个点的标签分成“只出现一边”和“0、1 都出现”，后一部分会消耗一个 VC 维度。

> [!question] 初学者读完必须能回答
> 1. 删除最后一个坐标后，$\mathcal F_0$ 与双延拓族 $\mathcal F_1$ 分别记录什么？
> 2. 为什么有 $|\mathcal F|=|\mathcal F_0|+|\mathcal F_1|$？
> 3. 为什么双延拓会把 VC 维上界从 $d$ 降到 $d-1$？
> 4. Pascal 恒等式怎样闭合双参数归纳？
> 5. 精确二项式和、$(em/d)^d$ 与 $2^m$ 三种上界应怎样选择，历史三角图又能提供什么证据？

## 一、学习目标

1. 用集合族语言重写 binary restrictions；
2. 构造投影族 $\mathcal F_0$ 与双实现族 $\mathcal F_1$；
3. 证明精确计数恒等式 $|\mathcal F|=|\mathcal F_0|+|\mathcal F_1|$；
4. 证明 $\operatorname{VCdim}(\mathcal F_1)\le d-1$ 的关键“加回最后一点”论证；
5. 用双参数归纳与 Pascal 恒等式推出 binomial sum；
6. 推导 $\sum_{i=0}^d{m\choose i}\le(em/d)^d$；
7. 构造达到上界的集合族，理解 sharpness；
8. 处理 $d=0$、$m<d$、$d=\infty$ 等边界；
9. 解释组合引理为何尚不足以独立证明泛化；
10. 把 $\log\tau(2m)$ 转成后续的 $d\log(em/d)$ complexity term。

## 二、为什么“在 $d+1$ 处少一个 pattern”会约束所有更大规模

仅从 VC 维定义，我们知道

$$
\tau_{\mathcal H}(d)=2^d,
\qquad
\tau_{\mathcal H}(d+1)<2^{d+1}.
$$

这看起来只是在某个规模上少了至少一种 labeling。为什么到了 $m=1000$ 时，pattern 数不能重新接近 $2^{1000}$？

关键是 patterns 之间并非任意独立。若在新增点 $x_m$ 上，一个旧 pattern 能同时延伸为标签 0 和标签 1，那么这批“有两种延伸”的旧 patterns 本身不能再拥有完整的 $d$ 维自由度；否则它们加上 $x_m$ 就打散 $d+1$ 点。每增加一个真正自由的新 bit，就必须消耗一个可打散维度。

这产生与 Pascal 三角形完全相同的递推。

## 三、定理的正式表述

> [!theorem] Sauer–Shelah–Perles lemma
> 设 $\mathcal H\subseteq\{0,1\}^{\mathcal X}$ 且
> $$
> \operatorname{VCdim}(\mathcal H)\le d<\infty.
> $$
> 则对任意整数 $m\ge0$，
> $$
> \boxed{
> \tau_{\mathcal H}(m)
> \le
> \sum_{i=0}^{d}{m\choose i},
> }
> $$
> 其中约定 $i>m$ 时 ${m\choose i}=0$。特别地，若 $m\ge d\ge1$，则
> $$
> \boxed{
> \tau_{\mathcal H}(m)
> \le
> \left(\frac{em}{d}\right)^d.
> }
> $$

当 $d\ge m$，binomial sum 为 $2^m$，定理只恢复 universal bound；真正的压缩发生在 $m>d$。

## 四、把函数限制写成集合族

固定任意 $m$ 点集

$$
C=\{x_1,\ldots,x_m\}.
$$

把每个 restriction 的正标签坐标写成

$$
A_h=\{i\in[m]:h(x_i)=1\}\subseteq[m].
$$

得到集合族

$$
\mathcal F
=\{A_h:h\in\mathcal H\}
\subseteq2^{[m]}.
$$

这里 $2^{[m]}$ 是 $[m]=\{1,\ldots,m\}$ 的幂集。因为 distinct label vectors 与 distinct positive-coordinate subsets 一一对应，

$$
|\mathcal F|=|\mathcal H|_C|.
$$

$\mathcal H$ 在 $C$ 的某个坐标子集上打散，当且仅当 $\mathcal F$ 在对应 indices 上实现全部 traces。因此

$$
\operatorname{VCdim}(\mathcal F)
\le\operatorname{VCdim}(\mathcal H)
\le d.
$$

现在问题纯化为：VC 维至多 $d$ 的 $[m]$ 子集族最多有多大？

## 五、删除最后一点：两个派生族

把最后坐标记为 $m$。对每个 $B\subseteq[m-1]$，它在 $\mathcal F$ 中可能有三种 fiber 情况：

1. 只有 $B$ 出现，即最后 bit 只能为 0；
2. 只有 $B\cup\{m\}$ 出现，即最后 bit 只能为 1；
3. 两者都出现，即最后 bit 可自由取 0 或 1。

定义投影族

$$
\mathcal F_0
=\left\{
B\subseteq[m-1]:
B\in\mathcal F\ \text{或}\ B\cup\{m\}\in\mathcal F
\right\},
$$

以及双实现族

$$
\mathcal F_1
=\left\{
B\subseteq[m-1]:
B\in\mathcal F\ \text{且}\ B\cup\{m\}\in\mathcal F
\right\}.
$$

$\mathcal F_0$ 记录删掉第 $m$ 坐标后出现的所有 patterns；$\mathcal F_1$ 记录哪些旧 patterns 在第 $m$ 坐标上有两种延伸。先用一个小族回答：**删除最后坐标后，原来的 6 个模式为什么精确分成 $4+2$？**

![[00-知识库管理/_assets/figures/learning-theory/fig-sauer-fiber-decomposition-v2.svg|880]]

> [!figure] 图 1　把纤维分解变成可逐项核对的计数
> 对示例族 $\mathcal F=\{000,001,100,101,010,110\}$，删除第三位得到四个不同前缀；其中只有 $00,10$ 同时具有 0、1 两种延伸。因此 $|\mathcal F_0|=4$、$|\mathcal F_1|=2$，且 $|\mathcal F|=4+2$。来源：为本节证明专门构造并独立绘制；确定性 SVG 计数示意，无随机种子。

**怎样读图。** 中栏先把相同前缀合并，所以每个前缀至少为原族贡献一次；右栏再挑出具有两条纤维的前缀，它们各自多贡献一次。这个“先计一次、双延拓再补一次”的规则，正是下一行恒等式的组合含义。

**适用边界（图没有证明什么）。** 图只核对一个六模式示例的精确恒等式，不证明 $\operatorname{VCdim}(\mathcal F_1)\le d-1$，也不证明对所有集合族的极值递推；一般证明仍需处理任意 $m,d$、空族与边界值。

### 5.1 精确计数恒等式

每个 $B\in\mathcal F_0\setminus\mathcal F_1$ 对原族贡献一个集合；每个 $B\in\mathcal F_1$ 贡献两个集合。因此

$$
\begin{aligned}
|\mathcal F|
&=|\mathcal F_0\setminus\mathcal F_1|
+2|\mathcal F_1|\\
&=|\mathcal F_0|-|\mathcal F_1|+2|\mathcal F_1|\\
&=\boxed{|\mathcal F_0|+|\mathcal F_1|}.
\end{aligned}
$$

第二行只用了 $\mathcal F_1\subseteq\mathcal F_0$。

## 六、两个 VC 维上界

### 6.1 $\operatorname{VCdim}(\mathcal F_0)\le d$

假设 $\mathcal F_0$ 打散 $S\subseteq[m-1]$。对每个 $U\subseteq S$，存在 $B\in\mathcal F_0$ 满足 $B\cap S=U$。由 $\mathcal F_0$ 定义，$B$ 或 $B\cup\{m\}$ 中至少一个属于 $\mathcal F$；无论选哪个，它与 $S$ 的交仍为 $U$。所以 $\mathcal F$ 也打散 $S$。

因此 $\mathcal F_0$ 不可能打散超过 $d$ 个点：

$$
\operatorname{VCdim}(\mathcal F_0)\le d.
$$

### 6.2 $\operatorname{VCdim}(\mathcal F_1)\le d-1$

这是证明的发动机。反设 $\mathcal F_1$ 打散某个 $d$ 元集合 $S\subseteq[m-1]$。要证明 $\mathcal F$ 会打散 $S\cup\{m\}$。

任取 $U\subseteq S\cup\{m\}$：

- 若 $m\notin U$，因为 $\mathcal F_1$ 打散 $S$，存在 $B\in\mathcal F_1$ 满足 $B\cap S=U$；而 $B\in\mathcal F$；
- 若 $m\in U$，取 $B\in\mathcal F_1$ 使 $B\cap S=U\setminus\{m\}$；由双实现定义，$B\cup\{m\}\in\mathcal F$。

两种情况都能实现，所以 $\mathcal F$ 打散 $d+1$ 个坐标，与 $\operatorname{VCdim}(\mathcal F)\le d$ 矛盾。故

$$
\boxed{
\operatorname{VCdim}(\mathcal F_1)\le d-1.
}
$$

> [!intuition] 为什么降一维
> $\mathcal F_1$ 中的每个 pattern 都已经预留了第 $m$ 点的一个自由 bit。若它还能在另外 $d$ 点上自由设置 $d$ 个 bits，总自由度就是 $d+1$，这正被 VC 维上界禁止。

## 七、极值递推

定义

$$
T_d(m)
=\max\left\{
|\mathcal F|:
\mathcal F\subseteq2^{[m]},
\operatorname{VCdim}(\mathcal F)\le d
\right\}.
$$

由前两节：

$$
\begin{aligned}
|\mathcal F|
&=|\mathcal F_0|+|\mathcal F_1|\\
&\le T_d(m-1)+T_{d-1}(m-1).
\end{aligned}
$$

对最大族取最大，得到

$$
\boxed{
T_d(m)
\le T_d(m-1)+T_{d-1}(m-1).
}
$$

边界条件：

$$
T_d(0)=1,
\qquad
T_0(m)=1.
$$

第二条值得证明：若一个集合族含两个不同集合，它们至少在某坐标上不同，于是该单点上 0、1 都出现，VC 维至少 1。所以 VC 维 0 的族至多含一个集合。

## 八、由 Pascal 恒等式闭合归纳

我们对 $(m,d)$ 做归纳，假设更小参数处已有

$$
T_d(m-1)\le\sum_{i=0}^{d}{m-1\choose i},
$$

$$
T_{d-1}(m-1)\le\sum_{i=0}^{d-1}{m-1\choose i}.
$$

代入递推：

$$
\begin{aligned}
T_d(m)
&\le
\sum_{i=0}^{d}{m-1\choose i}
+\sum_{i=0}^{d-1}{m-1\choose i}\\
&={m-1\choose0}
+\sum_{i=1}^{d}
\left[
{m-1\choose i}+{m-1\choose i-1}
\right]\\
&={m\choose0}
+\sum_{i=1}^{d}{m\choose i}\\
&=\boxed{\sum_{i=0}^{d}{m\choose i}}.
\end{aligned}
$$

第三行使用 Pascal 恒等式

$$
{m-1\choose i}+{m-1\choose i-1}={m\choose i}.
$$

因为 $C$ 任意且 $|\mathcal H|_C|=|\mathcal F|\le T_d(m)$，再对 $C$ 取最大就得到

$$
\tau_{\mathcal H}(m)
\le\sum_{i=0}^{d}{m\choose i}.
$$

组合部分证明完成。现在只把归纳真正闭合的两个接口并排放在一起：**纤维分解怎样产生递推，递推又怎样被 Pascal 恒等式吸收？** 解析松弛属于下一节，不再挤入同一张图。

![[00-知识库管理/_assets/figures/learning-theory/fig-sauer-recursion-pascal-v2.svg|880]]

> [!figure] 图 2　极值递推如何在 Pascal 恒等式处闭合
> 投影族保留维数上界 $d$，双重延拓族把维数上界降为 $d-1$，于是得到 $T_d(m)\le T_d(m-1)+T_{d-1}(m-1)$；两个归纳上界再由 Pascal 恒等式合并为下一行二项式和。图内为跨 SVG 渲染器稳定显示，把同一极值函数写作 $T(m,d)=T_d(m)$。来源：依据本节证明独立绘制；确定性证明地图，无随机种子。

**怎样读图。** 左栏负责“为什么出现两个子问题”，右栏负责“为什么两个二项式和能重新合成一个”。图是证明的依赖地图，不替代上文对 $\operatorname{VCdim}(\mathcal F_0)$ 与 $\operatorname{VCdim}(\mathcal F_1)$ 的量词论证。

**适用边界（图没有证明什么）。** 图没有独立证明两个派生族的 VC 维上界，也没有展示双参数归纳的全部基例；Pascal 恒等式只负责代数闭合，不能替代“为何双延拓消耗一个可打散维度”的组合论证。

### 8.1 同一个递推的历史图像

先用历史原图回答一个跨时代问题：**现代极值集合论递推中的 Pascal 恒等式，在传统筹算三角图里对应哪条局部生成规则？**

![[00-知识库管理/_assets/images/wikimedia-commons/yanghui-triangle-1303-public-domain.png|420]]

> [!figure] 图 3｜《四元玉鉴》贾宪—杨辉三角图（历史原图）
> 这幅 1303 年刊刻图以筹算数字排列二项系数；相邻两项相加生成下一层内部条目，对应现代 Pascal 恒等式。原作：朱世杰《四元玉鉴》所刊历史图，Wikimedia Commons 当前 475×753 PNG；许可：Public Domain Mark 1.0；本地文件未裁切、校色或改字。原件、许可、已知误刻与 SHA-256 见 [[外部图像资产登记]]。

**怎样读图。** 不要先把它当装饰史料：选择一个内部条目，沿上方相邻两格回溯，核对“左父项 + 右父项 = 当前项”的局部递推；再把现代二项式恒等式与图 2 的归纳闭合对齐。

**适用边界（图没有证明什么）。** 历史三角图只显示二项系数递推，不解释为何 Sauer–Shelah 的派生族恰好产生 $(m-1,d)$ 与 $(m-1,d-1)$ 两个子问题，也不是无误数据表；倒数第二行一项 34 应为 35，现代公式与证明不以该误刻为依据。

把图中的筹算数字换成现代阿拉伯数字后，整幅图遵循的构造规则（除下文指出的一处误刻外）是：内部条目由上一行相邻两项相加得到，

$$
{m-1\choose i}+{m-1\choose i-1}={m\choose i}.
$$

这正是上面归纳闭合时使用的 Pascal 恒等式。历史图的教学价值不是给 Sauer–Shelah 提供另一份证明，而是让人看见：**集合族的极值递推最终落在一个古老的二项系数结构上**。现代证明解释“为什么两个子问题分别是 $(m-1,d)$ 与 $(m-1,d-1)$”；三角图只负责把这两个边界值如何合并显示出来。

> [!warning] 古图也需要校勘
> Wikimedia 文件页指出倒数第二行左起第四项写作 34，正确值应为 35。它是一件历史文献图像，不应被当作无误的数值数据表；本节的公式与证明以现代定义为准。

## 九、从 binomial sum 到 $(em/d)^d$

设 $m\ge d\ge1$，令

$$
a=\frac dm\in(0,1].
$$

对 $0\le i\le d$，因为 $a\le1$，指数越大值越小，所以

$$
a^i\ge a^d.
$$

逐项乘以非负的 ${m\choose i}$ 并求和：

$$
a^d\sum_{i=0}^{d}{m\choose i}
\le
\sum_{i=0}^{d}{m\choose i}a^i.
$$

把右侧扩到完整 binomial sum：

$$
\sum_{i=0}^{d}{m\choose i}a^i
\le
\sum_{i=0}^{m}{m\choose i}a^i
=(1+a)^m.
$$

故

$$
\sum_{i=0}^{d}{m\choose i}
\le a^{-d}(1+a)^m
=\left(\frac md\right)^d
\left(1+\frac dm\right)^m.
$$

使用 $\log(1+u)\le u$：

$$
\left(1+\frac dm\right)^m
\le e^d.
$$

最终

$$
\boxed{
\sum_{i=0}^{d}{m\choose i}
\le\left(\frac{em}{d}\right)^d.
}
$$

取自然对数得到后续真正使用的 complexity 形式：

$$
\boxed{
\log\tau_{\mathcal H}(m)
\le d\log\frac{em}{d}.
}
$$

## 十、手算：$d=2,m=5$

Sauer–Shelah 给

$$
\tau_{\mathcal H}(5)
\le{5\choose0}+{5\choose1}+{5\choose2}
=1+5+10=16.
$$

最大可能 $2^5=32$，所以 VC 维 2 已把模式数至少砍半。粗解析界为

$$
\left(\frac{5e}{2}\right)^2\approx46.2,
$$

反而大于 trivial bound 32；这提醒我们 $(em/d)^d$ 是便于代数处理的松上界，小样本时应优先用

$$
\min\left\{2^m,\sum_{i=0}^{d}{m\choose i},(em/d)^d\right\}.
$$

区间分类器在 5 个有序点上恰有

$$
1+\frac{5\cdot6}{2}=16
$$

个 patterns，正好达到 binomial-sum 上界。把三个上界画在一起，可以区分“组合上精确”“代数上方便”和“永远成立但没有利用维数”这三种角色。

先看图回答：**精确二项式和、解析松弛与平凡上界在小样本区怎样换位，数值计算时为什么应先取三者最小值？**

![[00-知识库管理/_assets/plots/learning-theory/plot-sauer-bounds-v2.svg|880]]

> [!figure] 图 4　三种上界各自适用的尺度
> 固定 $d=2$，比较 $2^m$、精确 Sauer sum 与解析松弛 $(em/d)^d$。在 $m=5$，精确和为 16，而解析式约为 46.2，甚至松于平凡上界 32。**生成：**`00-知识库管理/_labs/code/plot-vc-visual-pilot.mjs`。

> 由精确二项式和与闭式公式确定性生成，无随机种子。

**怎样读图。** 绿色曲线保留离散组合信息，琥珀曲线牺牲常数以换取便于代数求解的闭式，红线则是所有二分标记的上限。数值计算应取三者的最小值；只有在关注 $m$、$d$ 的渐近依赖时，才优先使用解析式。

**适用边界（图没有证明什么）。** 图固定 $d=2$ 且以对数纵轴比较三种上界，不证明解析松弛在其他 $m,d$ 下何时最紧，也不表示存在某个函数类同时达到所有三条曲线。曲线是上界尺度，不是随机抽样得到的经验 pattern 数。

## 十一、上界是锐的

在无限 domain $\mathcal X$ 上考虑

$$
\mathcal H_{\le d}
=\{\mathbf1_A:A\subseteq\mathcal X,\ |A|\le d\}.
$$

它能打散任意 $d$ 点集：任意正标签子集大小不超过 $d$，可直接取为 $A$。但不能打散 $d+1$ 点，因为全 1 labeling 需要 $|A|\ge d+1$。所以 VC 维恰为 $d$。

在任意 $m$ 点集 $C$ 上，restriction 正类可以是 $C$ 的任意至多 $d$ 元子集，因此

$$
\Pi_{\mathcal H_{\le d}}(C)
=\sum_{i=0}^{d}{m\choose i}.
$$

所以仅知道 $m,d$ 时，binomial-sum 上界无法统一改进。这类达到上界的族称为 maximum class；不是每个 VC 维 $d$ 的类都达到它。

## 十二、边界情形

### 12.1 $d=0$

上界为

$$
{m\choose0}=1.
$$

这与“类中任意两函数都不能在任何点上不同”一致。

### 12.2 $m\le d$

约定 ${m\choose i}=0$ for $i>m$，则

$$
\sum_{i=0}^{d}{m\choose i}
=\sum_{i=0}^{m}{m\choose i}=2^m.
$$

此时 theorem 没有压缩，因为一个 VC 维至少 $m$ 的类确实可能打散 $m$ 点。

### 12.3 $d=\infty$

不存在固定次数的 polynomial envelope；对每个 $m$ 都有 $\tau(m)=2^m$。不能把 $(em/d)^d$ 形式用于 $d=\infty$。

### 12.4 有限 domain

只对 $m\le|\mathcal X|$ 定义 distinct-point growth。超过 domain 大小的“新点”不存在；这不是更强统计结论，只是问题规模已经耗尽。

## 十三、它怎样进入泛化，又缺少什么

有限类一致收敛的原型为

$$
\Pr\left(
\sup_{h\in\mathcal H}|R_P(h)-R_S(h)|>\varepsilon
\right)
\le2|\mathcal H|e^{-2m\varepsilon^2}.
$$

Sauer–Shelah 提供一个候选替代：

$$
|\mathcal H|\quad\rightsquigarrow\quad
\tau_{\mathcal H}(2m)
\le\left(\frac{2em}{d}\right)^d.
$$

但不能直接替换并宣布完成。$\tau(2m)$ 数的是随机 pooled sample 上的 restrictions；还要证明未知总体风险的偏差事件可由两个经验样本之间的偏差事件控制，并在条件于 pooled sample 后合法做 Union Bound。这个概率桥梁是 [[VC 一致收敛与泛化界]] 的 ghost sample 与随机交换证明。

> [!warning] 组合容量不是概率定理
> Sauer–Shelah 不包含分布、iid、风险、置信度或浓缩。它只提供“最多需要同时控制多少 patterns”。概率保证还需 sampling contract 和 concentration。

## 十四、AI 视角

### 14.1 polynomial pattern growth 的含义

若一个 binary model family 的 VC 维为 $d$，则对 pooled $2m$ 个 inputs，它最多留下

$$
O(m^d)
$$

种 prediction patterns，而不是 $2^{2m}$。取 log 后 complexity 是

$$
O(d\log m),
$$

这正好能与 concentration exponent $m\varepsilon^2$ 竞争。

### 14.2 为什么仍可能数值松

现代网络的 worst-case $d$ 可随参数和计算单元很大。即使理论上从指数模式压为 $m^d$，$d\log m$ 仍可能超过样本量，使 bound 大于 1。此时应把结论理解为可学习性的结构基线，而不是 test error 的精确预测。

### 14.3 与 sparse rules 的直接对应

$\mathcal H_{\le d}$ 的 tight example 可解释为“至多记住/例外化 $d$ 个输入”的规则类。它在 $m$ 个 items 上能选择任意至多 $d$ 个例外，pattern 数正是 binomial sum。这展示了 combinatorial capacity 怎样对应记忆槽位，但不能据此断言一般神经网络等价于 sparse exception list。

## 十五、常见错误

> [!warning] 把 $\sum_{i=0}^d{m\choose i}$ 写成 ${m\choose d}$
> 后者只数恰好 $d$ 个正点，漏掉大小 $0,1,\ldots,d-1$ 的 traces。两者同阶不代表定理相同。

> [!warning] 在 $m<d$ 时套 $(em/d)^d$
> 推导选择 $a=d/m\le1$，明确要求 $m\ge d$。小于 $d$ 时直接用 $2^m$。

> [!warning] 以为 polynomial degree 就等于实际增长次数
> theorem 给统一上界。thresholds 恰为一次，intervals 恰为二次，但很多 VC 维 $d$ 的类增长远低于上界。

> [!warning] 以为递推中的 $\mathcal F_1$ 是“标签为 1 的集合”
> $\mathcal F_1$ 是同一旧 pattern 在最后坐标上 0、1 **都能实现**的 fiber；只出现标签 1 的 pattern 属于 $\mathcal F_0$，不属于 $\mathcal F_1$。

## 十六、历史与证据地位

该组合结论由 Sauer、Shelah 与 Perles 在不同语境中独立获得，Vapnik–Chervonenkis 也在统计学习/事件频率问题中使用同源性质：

- [[S-1972-Sauer-Density-Families-Sets]]：极值集合论；
- [[S-1972-Shelah-Combinatorial-Problem]]：模型论稳定性；
- [[S-1971-Vapnik-Chervonenkis-Uniform-Convergence]]：事件族的一致收敛；
- [[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]：现代学习理论表述。

本节点的 fiber decomposition、递推和解析上界均已独立逐步展开；历史来源不替代证明。

## 十七、本节回顾

1. 为什么删除最后一点后不能只写 $|\mathcal F|\le2|\mathcal F_0|$？
2. $\mathcal F_1$ 为什么比 $\mathcal F_0$ 少一个 VC 维？
3. Pascal 恒等式在哪一行闭合归纳？
4. $(em/d)^d$ 的推导为何要求 $m\ge d\ge1$？
5. 哪个 class 达到 binomial-sum 上界？
6. 为什么本引理本身还没有给出任何 $1-\delta$ 泛化保证？

## 十八、训练与后继

- A–E 训练：[[习题 - Sauer-Shelah 引理]]；
- 独立解答：[[解答 - Sauer-Shelah 引理]]；
- 概率闭环：[[VC 一致收敛与泛化界]]；
- 可学习性等价：[[二分类统计学习基本定理]]。
