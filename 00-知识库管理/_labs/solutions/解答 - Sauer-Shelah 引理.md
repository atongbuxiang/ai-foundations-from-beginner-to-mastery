---
type: solution
status: draft
area: [learning-theory/vc, combinatorics/extremal-set-theory]
topic: "[[Sauer-Shelah 引理]]"
exercise: "[[习题 - Sauer-Shelah 引理]]"
prerequisites: ["[[增长函数与经验二分模式]]", "[[数学归纳、递归与组合计数]]", "[[基本不等式与界的构造]]"]
related: ["[[VC 一致收敛与泛化界]]", "[[二分类统计学习基本定理]]"]
sources: ["[[S-1972-Sauer-Density-Families-Sets]]", "[[S-1972-Shelah-Combinatorial-Problem]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - Sauer-Shelah 引理

> [!warning] 使用方式
> 这组题的掌握证据是能闭卷重建“投影 + 双实现 + 降一维 + Pascal”四步。只背 $\sum_{i=0}^d{m\choose i}$ 不能诊断你是否理解结论为何成立。

## A. 识别与复述

### LT-SAUER-A01

若 $\operatorname{VCdim}(\mathcal H)\le d<\infty$，则

$$
\tau_{\mathcal H}(m)
\le\sum_{i=0}^{d}{m\choose i},
$$

约定 $i>m$ 时 ${m\choose i}=0$，故 $d\ge m$ 时右侧为 $2^m$。只有在 $m\ge d\ge1$ 时，才进一步使用

$$
\sum_{i=0}^{d}{m\choose i}
\le\left(\frac{em}{d}\right)^d.
$$

### LT-SAUER-A02

$$
\mathcal F_0
=\{B\subseteq[m-1]:B\in\mathcal F\text{ or }B\cup\{m\}\in\mathcal F\},
$$

$$
\mathcal F_1
=\{B\subseteq[m-1]:B\in\mathcal F\text{ and }B\cup\{m\}\in\mathcal F\}.
$$

只出现最后标签 1 意味着 $B\cup\{m\}\in\mathcal F$ 但 $B\notin\mathcal F$；它属于投影族 $\mathcal F_0$，不属于要求两种延伸同时出现的 $\mathcal F_1$。

### LT-SAUER-A03

“至多 $d$ 次多项式量级”是 uniform upper asymptotic：固定 $d$ 时 $\tau(m)=O(m^d)$。“恰为 $m^d$”声称具体函数值/主项，通常不对，例如 thresholds 是 $m+1$。“达到 Sauer 上界”是更精确的 equality

$$
\tau(m)=\sum_{i=0}^{d}{m\choose i}
$$

在相关 $m$ 上成立；其主项约为 $m^d/d!$，也不是恰好 $m^d$。

## B. 手算与构造

### LT-SAUER-B01

binomial sum：

$$
1+6+15+20=42.
$$

trivial bound：$2^6=64$。解析粗界：

$$
\left(\frac{6e}{3}\right)^3=(2e)^3=8e^3\approx160.68.
$$

三者中精确 Sauer sum 42 最小，trivial 64 次之，解析粗界此处甚至比 trivial bound 大。解析形式的价值是 log 后简洁，不保证小样本数值最紧。

### LT-SAUER-B02

对 $d=1$，递推得到 Pascal 第二斜列：

$$
T_1(1)\le T_1(0)+T_0(0)=2,
$$

继而上界为 3、4、5，所以

$$
T_1(4)\le5={4\choose0}+{4\choose1}.
$$

对 $d=2$：$T_2(1)\le2$，$T_2(2)\le4$，

$$
T_2(3)\le T_2(2)+T_1(2)=4+3=7,
$$

$$
T_2(4)\le T_2(3)+T_1(3)=7+4=11.
$$

也即 $1+4+6=11$。

### LT-SAUER-B03

函数数等于至多二元子集数：

$$
{5\choose0}+{5\choose1}+{5\choose2}
=1+5+10=16.
$$

任意两个点可被打散，因为其任意 positive subset 大小至多 2；三个点不能被打散，因为全 1 labeling 需要 positive set 大小 3。因此 VC 维为 2。模式数 16 恰等于 $d=2,m=5$ 的 Sauer 上界。

## C. 推导与证明

### LT-SAUER-C01

对每个 $B\in\mathcal F_0$，fiber

$$
\{A\in\mathcal F:A\cap[m-1]=B\}
$$

大小为 1 或 2；恰在 $B\in\mathcal F_1$ 时大小为 2。因此

$$
|\mathcal F|
=|\mathcal F_0\setminus\mathcal F_1|+2|\mathcal F_1|
=|\mathcal F_0|+|\mathcal F_1|.
$$

若 $\mathcal F_1$ 打散 $d$ 元集合 $S$，则对 $S\cup\{m\}$ 的任意 subset $U$：若 $m\notin U$，选 $B\in\mathcal F_1$ 实现 $U$ 并用 $B\in\mathcal F$；若 $m\in U$，选 $B$ 实现 $U\setminus\{m\}$ 并用 $B\cup\{m\}\in\mathcal F$。这使 $\mathcal F$ 打散 $d+1$ 点，矛盾，所以 $\operatorname{VCdim}(\mathcal F_1)\le d-1$。

### LT-SAUER-C02

定义 $T_d(m)$ 为 $[m]$ 上 VC 维至多 $d$ 的最大集合族大小。边界：$T_d(0)=1$；$T_0(m)=1$，因为两个不同集合会在某坐标上同时产生 0、1，从而打散单点。

由 C01 及 $\operatorname{VCdim}(\mathcal F_0)\le d$、$\operatorname{VCdim}(\mathcal F_1)\le d-1$：

$$
T_d(m)\le T_d(m-1)+T_{d-1}(m-1).
$$

归纳假设代入：

$$
\begin{aligned}
T_d(m)
&\le\sum_{i=0}^{d}{m-1\choose i}
+\sum_{i=0}^{d-1}{m-1\choose i}\\
&={m-1\choose0}
+\sum_{i=1}^{d}
\left[{m-1\choose i}+{m-1\choose i-1}\right]\\
&=\sum_{i=0}^{d}{m\choose i},
\end{aligned}
$$

最后用 Pascal 恒等式。边界与递推覆盖全部非负 $m,d$。

### LT-SAUER-C03

令 $a=d/m\in(0,1]$。对 $i\le d$ 有 $a^i\ge a^d$，故

$$
a^d\sum_{i=0}^{d}{m\choose i}
\le\sum_{i=0}^{d}{m\choose i}a^i
\le(1+a)^m.
$$

因此

$$
\sum_{i=0}^{d}{m\choose i}
\le\left(\frac md\right)^d
\left(1+\frac dm\right)^m.
$$

由 $\log(1+u)\le u$，

$$
\left(1+\frac dm\right)^m
\le e^d,
$$

合并得 $(em/d)^d$。

## D. 边界、反例与纠错

### LT-SAUER-D01

$\mathcal F_1$ 不收集“最后 bit 为 1”的所有 patterns；它收集删掉最后 bit 后**0、1 两种延伸都存在**的旧 pattern。正因每个旧 pattern 已获得最后 bit 的自由度，若它还能打散 $d$ 个旧坐标，就会使原族打散 $d+1$ 点。因此 VC 至多 $d-1$。

### LT-SAUER-D02

$m=5,d=2$ 时

$$
(5e/2)^2\approx46.2>32=2^5.
$$

不反驳定理：上界可以比另一个合法上界更松。Sauer 的精确 sum 是 16；实际使用取

$$
\tau(m)\le\min\left\{2^m,\sum_{i=0}^d{m\choose i},(em/d)^d\right\}.
$$

解析形式主要方便渐近和取 log。

### LT-SAUER-D03

仍缺：数据分布 $P$ 与 iid sample contract；总体风险 $R_P$ 和经验风险 $R_S$；把未知 expectation 换成两个 samples 的 symmetrization；条件 concentration；置信参数 $\delta$；以及说明 patterns 数为何可用于同一个随机事件的 Union Bound。Sauer 只做组合计数，不包含概率。

## E. AI 迁移

### LT-SAUER-E01

在 $m$ 个 IDs 上可选任意至多 $d$ 个标异常，patterns 数为

$$
\sum_{i=0}^{d}{m\choose i}.
$$

VC 维恰为 $d$，所以达到 Sauer 界。它本质上是记住 exception IDs；对从未见过的新 ID 没有特征规律，可能全部预测正常。组合可学习性只是在 iid、固定分布和足够样本下相对这个 class 的风险保证，不把 ID memorization 变成 semantic anomaly detection。

### LT-SAUER-E02

$d=10^6>m=10^5$，条件 $m\ge d$ 不成立，不能用 $(em/d)^d$ 推导。对 pooled $2m=2\cdot10^5$ 仍有 $d>2m$；binomial convention 给

$$
\sum_{i=0}^{d}{2m\choose i}=2^{2m},
$$

即只恢复 trivial maximal growth。它暗示仅凭这个 VC upper bound，当前样本规模无法得到非平凡 worst-case uniform convergence；不等于实际网络一定不泛化。

### LT-SAUER-E03

函数/参数总数描述全 domain 上的全局候选，可能无限且含表示冗余；pooled pattern 数描述当前 $2m$ inputs 可区分的行为，是 sample-dependent；Sauer 用 VC 维对所有 pooled samples 给 distribution-free 上界。

观测 pattern 小可用于诊断实际数据 geometry、压缩 conditional union，或启发 data-dependent complexity。但它与所观测样本耦合，也不约束样本外 behavior；要形成 theorem 仍需对称化、独立验证或专门的数据依赖界。
