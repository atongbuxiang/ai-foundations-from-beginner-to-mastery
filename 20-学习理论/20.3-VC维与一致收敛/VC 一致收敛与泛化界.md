---
type: theorem
status: draft
area: [learning-theory/vc, probability/uniform-convergence]
aliases: [VC Inequality, VC Uniform Convergence Bound, Ghost-Sample VC Bound]
node_id: LT-20
prerequisites: ["[[Sauer-Shelah 引理]]", "[[增长函数与经验二分模式]]", "[[不可知 PAC、ERM 与双侧一致收敛]]", "[[浓缩不等式]]"]
related: ["[[二分类统计学习基本定理]]", "[[Ghost Sample、对称化与经验过程入口]]", "[[Rademacher 复杂度与经验复杂度]]", "[[收缩引理与 Lipschitz 损失复合]]"]
sources: ["[[S-1971-Vapnik-Chervonenkis-Uniform-Convergence]]", "[[S-1972-Sauer-Density-Families-Sets]]", "[[S-1972-Shelah-Combinatorial-Problem]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1963-Hoeffding-Bounded-Random-Variables]]"]
exercises: ["[[习题 - VC 一致收敛与泛化界]]"]
solutions: ["[[解答 - VC 一致收敛与泛化界]]"]
created: 2026-08-20
updated: 2026-08-23
---

# VC 一致收敛与泛化界

> [!abstract] 本章主问题
> 对 binary class $\mathcal H$、0–1 loss 和 iid 样本，增长函数给出经典 VC inequality：当 $m\varepsilon^2\ge2$ 时，
> $$
> \Pr\left(
> \sup_{h\in\mathcal H}|R_P(h)-R_S(h)|>\varepsilon
> \right)
> \le
> 4\tau_{\mathcal H}(2m)e^{-m\varepsilon^2/8}.
> $$
> 若 $\operatorname{VCdim}(\mathcal H)=d<\infty$，Sauer–Shelah 把它变成约
> $$
> \sqrt{\frac{d\log(m/d)+\log(1/\delta)}{m}}
> $$
> 的 uniform gap。证明分三步：ghost sample 把未知总体期望换成两个经验均值；随机交换把它变成条件独立符号和；最后只对 pooled $2m$ 点上的至多 $\tau(2m)$ 个 patterns 做 Union Bound。

> [!question] 初学者读完必须能回答
> 1. Ghost sample 为什么把未知总体期望变成两个经验均值，条件 $m\varepsilon^2\ge2$ 从哪里来？
> 2. Pairwise random swap 留下了什么随机性，为什么 pooled sample 上只需数 $\tau_{\mathcal H}(2m)$ 个 patterns？
> 3. 最终界中的前因子 $4$、指数 $1/8$ 与 $\tau_{\mathcal H}(2m)$ 分别在哪一步产生？
> 4. Sauer–Shelah 怎样把增长函数改写为含 $d$ 的显式半径？
> 5. 经典 VC worst-case 半径、教材 U 形示意和实际深网泛化为什么不能混为一谈？

## 一、学习目标

1. 写清概率对样本 $S$ 取、supremum 对 class 取的顺序；
2. 从 binary prediction class 构造 0–1 error-function class；
3. 完整证明 ghost-sample symmetrization lemma 及其 $m\varepsilon^2\ge2$ 条件；
4. 解释 pairwise exchangeability 与 Rademacher swap signs；
5. 条件于 pooled sample，用 Hoeffding 和 $\tau_{\mathcal H}(2m)$ 合法做 Union Bound；
6. 追踪常数 $2\times2=4$ 与指数 $1/8$；
7. 代入 Sauer–Shelah 得到 high-probability radius；
8. 从 uniform gap 推出 exact/approximate ERM excess-risk bound；
9. 区分经典显式 VC bound、最优阶 sample complexity 与数据依赖界；
10. 识别 iid、0–1 bounded loss、固定 class、measurability 和 distribution shift 的边界。

## 二、问题设置

固定：

- 输入标签空间 $\mathcal Z=\mathcal X\times\{0,1\}$；
- 未知分布 $P$ on $\mathcal Z$；
- binary hypotheses $\mathcal H\subseteq\{0,1\}^{\mathcal X}$；
- iid 样本
  $$
  S=(Z_1,\ldots,Z_m)\sim P^m,
  \qquad Z_i=(X_i,Y_i);
  $$
- 0–1 loss
  $$
  f_h(z)=\mathbf1\{h(x)\ne y\}\in\{0,1\}.
  $$

记 error-function class

$$
\mathcal F
=\{f_h:h\in\mathcal H\}
\subseteq\{0,1\}^{\mathcal Z}.
$$

总体风险与经验风险为

$$
R_P(h)=Pf_h
=\mathbb E_{Z\sim P}f_h(Z),
$$

$$
R_S(h)=P_mf_h
=\frac1m\sum_{i=1}^mf_h(Z_i).
$$

目标随机变量是

$$
\Gamma(S)
=\sup_{h\in\mathcal H}
|Pf_h-P_mf_h|.
$$

注意顺序：先抽一个共同样本 $S$，再在这个样本上找偏差最大的 $h$。这正允许最坏 $h$ 依赖 $S$，因此 fixed-$h$ Hoeffding 不够。

## 三、为什么增长函数在 $2m$ 而不是 $m$ 上出现

固定训练输入后，$\tau_{\mathcal H}(m)$ 只知道 hypotheses 在训练点上怎样预测；总体风险还依赖所有未见输入。两个在训练点上相同的 $h$，可在样本外完全不同。

引入独立 ghost sample

$$
S'=(Z'_1,\ldots,Z'_m)\sim P^m,
\qquad S'\perp S,
$$

及

$$
P'_mf=\frac1m\sum_{i=1}^mf(Z_i').
$$

若 $P_mf$ 远离 $Pf$，而独立 $P'_mf$ 正常靠近 $Pf$，则 $P_mf$ 与 $P'_mf$ 必相距很远。这样未知的 $Pf$ 被两个可对称处理的 empirical means 替代。

代价是必须同时观察 $S,S'$ 上的 behavior，所以计数规模是 pooled $2m$ points：

$$
\tau_{\mathcal H}(2m).
$$

## 四、第一步：ghost-sample 对称化

> [!lemma] 双样本对称化
> 对 $\mathcal F\subseteq[0,1]^{\mathcal Z}$，若 $m\varepsilon^2\ge2$，则
> $$
> \boxed{
> \Pr_S\left(
> \sup_{f\in\mathcal F}|Pf-P_mf|>\varepsilon
> \right)
> \le
> 2\Pr_{S,S'}\left(
> \sup_{f\in\mathcal F}|P_mf-P'_mf|>\frac\varepsilon2
> \right).
> }

### 4.1 固定一个坏样本

设 $S$ 落入左侧坏事件。为避免 supremum 不取到的技术干扰，可选一个近似最大者 $f_S$，使

$$
|Pf_S-P_mf_S|>\varepsilon.
$$

现在把 $S$ 固定，只对独立 $S'$ 取概率。

### 4.2 ghost mean 以至少一半概率靠近总体均值

因为 $f_S(Z_i')\in[0,1]$ iid，

$$
\operatorname{Var}(P'_mf_S)
=\frac{\operatorname{Var}(f_S(Z))}{m}
\le\frac1{4m}.
$$

Chebyshev inequality 给

$$
\begin{aligned}
\Pr_{S'}\left(
|P'_mf_S-Pf_S|>\frac\varepsilon2
\right)
&\le
\frac{1/(4m)}{(\varepsilon/2)^2}\\
&=\frac1{m\varepsilon^2}\\
&\le\frac12.
\end{aligned}
$$

最后一行正是使用 $m\varepsilon^2\ge2$。因此至少以概率 $1/2$ 发生

$$
|P'_mf_S-Pf_S|\le\frac\varepsilon2.
$$

### 4.3 triangle inequality 把坏 gap 转移到双样本差

在这个概率至少 $1/2$ 的事件上：

$$
\begin{aligned}
|P_mf_S-P'_mf_S|
&\ge
|P_mf_S-Pf_S|-|P'_mf_S-Pf_S|\\
&>\varepsilon-\frac\varepsilon2\\
&=\frac\varepsilon2.
\end{aligned}
$$

所以每个坏 $S$ 至少有一半 ghost samples 使右侧事件发生。对 $S$ 积分：

$$
\Pr_S(\text{bad})
\le2\Pr_{S,S'}(\text{two-sample bad}).
$$

这就是第一个常数 2 的来源。

> [!info] 技术约定
> 对不可数 class，严格概率论需假设相关 suprema 可测，或使用 outer probability / 可数稠密可分版本。本课程主线采用标准可测性约定；这不是统计思想的附加容量假设，但在正式研究论文中不能完全省略。

## 五、第二步：随机交换与 Rademacher signs

观察 $m$ 个 iid pairs

$$
(Z_1,Z'_1),\ldots,(Z_m,Z'_m).
$$

每一对内部可交换：$(Z_i,Z'_i)$ 与 $(Z'_i,Z_i)$ 同分布。令

$$
\sigma_1,\ldots,\sigma_m
\overset{\mathrm{iid}}\sim\operatorname{Unif}\{-1,+1\},
$$

且与数据独立。$\sigma_i=-1$ 表示交换第 $i$ 对，$+1$ 表示不交换。由 exchangeability，

$$
P_mf-P'_mf
\overset d=
\frac1m\sum_{i=1}^{m}
\sigma_i\bigl(f(Z_i)-f(Z_i')\bigr).
$$

这一步的价值是：条件于 pooled data

$$
\widetilde S=(Z_1,Z'_1,\ldots,Z_m,Z'_m),
$$

所有 $f(Z_i),f(Z_i')$ 都变成固定的 0–1 数；剩余随机性只来自相互独立、均值为 0 的 signs。此时最容易混淆的问题是：**幽灵样本、对内交换和有限模式计数，分别消除了哪一种困难？**

![[00-知识库管理/_assets/figures/learning-theory/fig-vc-ghost-sample-swap-v2.svg|880]]

> [!figure] 图 1　从未知总体量到有限模式事件的三次改写
> 独立副本 $S'$ 把总体风险差改写为两个经验均值之差；随机符号 $\sigma_i$ 只在第 $i$ 对内部交换位置；固定 pooled data 后，无限假设族在这 $2m$ 个观测上至多留下 $\tau_{\mathcal H}(2m)$ 个 restriction。来源：依据本节对称化证明独立绘制；确定性证明地图，无随机种子。

**怎样读图。** 从左到右追踪“剩余随机性”：第一栏仍随机抽取两份样本，第二栏在固定样本对上只随机选择交换方向，第三栏进一步固定合并样本并按 restriction 去重。只有到第三栏，才能对有限个模式逐一使用 Hoeffding 再作 Union Bound。

**适用边界（图没有证明什么）。** 这张图只说明随机对象与条件化顺序，不证明 symmetrization 的因子 2，也不证明 VC 维如何控制 $\tau_{\mathcal H}(2m)$；前者由上一节的事件包含给出，后者依赖 [[Sauer-Shelah 引理]]。非 iid 样本或不可测 supremum 也不在图示合同内。

## 六、第三步：条件 Hoeffding 与模式 Union Bound

固定 pooled sample $\widetilde S$ 和某个 $f$，令

$$
a_i(f)=f(Z_i)-f(Z_i')\in\{-1,0,1\}.
$$

随机变量 $\sigma_i a_i(f)$ 独立、均值 0，且位于 $[-|a_i|,|a_i|]\subseteq[-1,1]$。Hoeffding 给任意 $t>0$：

$$
\begin{aligned}
\Pr_\sigma\left(
\left|\frac1m\sum_{i=1}^m\sigma_i a_i(f)\right|>t
\ \middle|\ \widetilde S
\right)
&\le
2\exp\left(
-\frac{2m^2t^2}{\sum_{i=1}^m(2|a_i|)^2}
\right)\\
&\le2\exp\left(-\frac{mt^2}{2}\right).
\end{aligned}
$$

取 $t=\varepsilon/2$：

$$
\boxed{
\Pr_\sigma\left(
\left|\frac1m\sum_i\sigma_i a_i(f)\right|>\frac\varepsilon2
\ \middle|\ \widetilde S
\right)
\le2e^{-m\varepsilon^2/8}.
}
$$

### 6.1 为什么只需 union 至多 $\tau(2m)$ 次

对固定 labels，error pattern

$$
\bigl(f_h(Z_1),f_h(Z'_1),\ldots,f_h(Z_m),f_h(Z'_m)\bigr)
$$

由 prediction pattern 对固定 label vector 做 XOR 得到，数量不变。即使 pooled inputs 有重复，distinct error patterns 也不超过

$$
\tau_{\mathcal H}(2m).
$$

两个 hypotheses 若 pooled error pattern 相同，则所有 $a_i$ 相同，在 conditional sign experiment 中是同一个事件，只需数一次。于是 Union Bound：

$$
\Pr_\sigma\left(
\sup_{h\in\mathcal H}
\left|\frac1m\sum_i\sigma_i a_i(f_h)\right|
>\frac\varepsilon2
\ \middle|\ \widetilde S
\right)
\le
2\tau_{\mathcal H}(2m)e^{-m\varepsilon^2/8}.
$$

右侧与具体 $\widetilde S$ 无关，再对 pooled data 积分，界保持不变。

## 七、合并得到 VC inequality

对称化给外部因子 2；conditional two-sided Hoeffding 给因子 2 和指数 $1/8$。因此：

> [!theorem] 本笔记选定常数版本的 VC inequality
> 若 $m\varepsilon^2\ge2$，则
> $$
> \boxed{
> \Pr_{S\sim P^m}\left(
> \sup_{h\in\mathcal H}|R_P(h)-R_S(h)|>\varepsilon
> \right)
> \le
> 4\tau_{\mathcal H}(2m)
> \exp\left(-\frac{m\varepsilon^2}{8}\right).
> }

证明链可压缩为：

```mermaid
flowchart LR
    A["sup |P−P_m| > ε"] -->|"ghost sample；×2"| B["sup |P_m−P'_m| > ε/2"]
    B -->|"pairwise exchangeability"| C["sup |m⁻¹Σ σ_i a_i| > ε/2"]
    C -->|"pooled patterns ≤ τ_H(2m)"| D["finite Union Bound"]
    D -->|"conditional Hoeffding"| E["4 τ_H(2m) e^(−mε²/8)"]
```

> [!warning] 不同书中的常数可不同
> 用更强的 symmetrization、不同 threshold splitting、one-sided/two-sided event 或其他 concentration，会出现 8、32 等不同常数。只要条件与证明一致，它们并不矛盾。本节点固定上述版本，不能把另一版本的前因子和本版本的指数任意拼接。

上面的流程图回答“证明依次做了什么”；下面的账本只回答另一个问题：**最终式中的 4、$1/8$ 与 $\tau_{\mathcal H}(2m)$ 分别从哪一步进入？**

![[00-知识库管理/_assets/figures/learning-theory/fig-vc-constant-ledger-v2.svg|880]]

> [!figure] 图 2　常数账本不是证明路线图的重复
> ghost step 的“至少一半”产生第一个因子 2；随机交换不损失系数；two-sided Hoeffding 再产生因子 2，并因阈值 $\varepsilon/2$ 与变量区间给出指数 $1/8$；最后才乘限制模式数 $\tau_{\mathcal H}(2m)$。来源：由本节逐行推导整理并独立绘制；确定性常数账本，无随机种子。

**怎样读图。** 沿“累计形态”一列向下读，每一行必须能由上一行和“本步代价”相乘得到。若改用另一版对称化或 concentration inequality，应从发生变化的那一行重新记账，而不能只替换最终常数。

**适用边界（图没有证明什么）。** 账本只对应本节选定的 two-sided VC inequality 版本；它不证明每一步事件包含，也不声称常数最优。换用 one-sided event、不同 threshold split、Bernstein 型界或更强对称化时，必须从变化处重算，不能拼接不同教材的常数。

## 八、high-probability radius

令右侧不超过 $\delta\in(0,1)$：

$$
4\tau_{\mathcal H}(2m)e^{-m\varepsilon^2/8}
\le\delta.
$$

取 log 并整理：

$$
\frac{m\varepsilon^2}{8}
\ge
\log\tau_{\mathcal H}(2m)+\log\frac4\delta.
$$

所以，以至少 $1-\delta$ 的概率，

$$
\boxed{
\Gamma(S)
\le
\sqrt{
\frac8m
\left[
\log\tau_{\mathcal H}(2m)
+\log\frac4\delta
\right]
}.
}
$$

所选右侧自动满足对称化的 $m\varepsilon^2\ge2$：因为

$$
m\varepsilon^2
=8\left[\log\tau(2m)+\log(4/\delta)\right]
>8\log4>2.
$$

若 radius 大于 1，结论仍真但没有信息，因为 0–1 risks 的 gap 本来就至多 1。

## 九、代入 Sauer–Shelah

若

$$
d=\operatorname{VCdim}(\mathcal H),
\qquad1\le d\le2m,
$$

则

$$
\tau_{\mathcal H}(2m)
\le\left(\frac{2em}{d}\right)^d.
$$

取 log：

$$
\log\tau_{\mathcal H}(2m)
\le d\log\frac{2em}{d}.
$$

得到经典显式 VC uniform bound：

$$
\boxed{
\sup_{h\in\mathcal H}|R_P(h)-R_S(h)|
\le
\sqrt{
\frac8m
\left[
d\log\frac{2em}{d}
+\log\frac4\delta
\right]
}
}
$$

以至少 $1-\delta$ 的概率成立。

若 $d>2m$，直接用 $\tau(2m)\le2^{2m}$；此时 class 对当前样本规模近似拥有全部 labeling，自然不能期待这个 worst-case route 给出小 gap。

### 9.1 教材中的 U 形曲线与 VC 定理各自说了什么

先用教材原图回答一个区分问题：**经典“欠拟合—最优—过拟合”示意中的两条曲线，哪些是定性建模直觉，哪些能由上面的 VC inequality 直接推出？**

![[00-知识库管理/_assets/images/d2l/d2l-capacity-vs-error-white-v2.svg|820]]

> [!figure] 图 3｜模型复杂度、训练损失与泛化损失（教材原图）
> 图沿某条模型族扩张路径画出训练损失下降与泛化损失先降后升的经典定性示意。作者：Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola；来源：*Dive into Deep Learning*，Figure “Influence of model complexity on underfitting and overfitting”；许可：CC BY-SA 4.0。显示 wrapper 只增加白色背景与可访问元数据，原始 SVG 的曲线和文字未改；教材页、源文件、许可、改动声明与 SHA-256 见 [[外部图像资产登记]]。

**怎样读图。** 先分别读 training loss 与 generalization loss，再问横轴“model complexity”由哪条嵌套类路径定义。训练最优值随类扩大不升来自集合包含；泛化曲线的 U 形则是近似误差与估计误差折中的定性图景，虚线 optimum 不是由本节 VC 半径算出的固定坐标。

**适用边界（图没有证明什么）。** 原图不证明真实测试误差必为严格 U 形，不覆盖 double descent，也没有给出 VC 维、样本量或置信参数；它不能替代结构风险最小化的 simultaneous guarantee。不同模型族之间的 complexity 横轴未必可直接比较，数据漂移与优化误差也未在图中分账。

这张图是有用的**定性示意**，但不是上面 VC radius 的函数图像。横轴 “Model Complexity” 表示沿某条模型族扩张路径移动；纵轴混合展示训练损失与泛化损失。常见读法是：

1. class 扩大时，经验风险的最优值不会上升，因为旧 hypotheses 仍在新 class 中，所以 training loss 可以单调下降；
2. class 太小时近似误差主导，表现为 underfitting；
3. class 太大而数据不足时，估计误差可能主导，表现为 overfitting；
4. “optimum” 是近似误差与估计误差折中的概念位置，不是由 VC 定理算出的固定横坐标。

经典 VC 定理给出的更谨慎陈述是：对每个预先固定的 class $\mathcal H_k$，有一个随其容量增加而变大的 uniform penalty。若使用嵌套类

$$
\mathcal H_1\subseteq\mathcal H_2\subseteq\cdots,
$$

便可比较

$$
\widehat R_S(\mathcal H_k)+\operatorname{pen}(d_k,m,\delta_k),
$$

这通向 [[结构风险最小化与非一致可学习性]]。VC bound 支持“训练拟合项下降、复杂度罚项上升”的折中结构，却**不保证真实测试曲线严格呈 U 形**；现代深度网络还可能出现 double descent，因此不能把教材示意图误写成定理结论。

为了判断显式半径的数值工作区，把 $m$ 除以 VC 维 $d$，考察“每个组合自由度分到多少样本”时，结论才从正确但空泛变为非平凡。

先看图回答：**经典显式 VC 半径要到多大的 $m/d$ 才跌破 0–1 风险的平凡边界，不同 $d$ 为什么仍不会完全重合？**

![[00-知识库管理/_assets/plots/learning-theory/plot-vc-radius-regimes-v2.svg|880]]

> [!figure] 图 4　经典显式 VC 半径何时才非平凡
> 固定 $\delta=0.05$，横轴为样本—容量比 $m/d$。水平虚线 $\gamma_m=1$ 是 0–1 风险的信息边界：高于它的结论虽正确，却弱于风险差本来就不超过 1 的事实。**生成：**`00-知识库管理/_labs/code/plot-vc-visual-pilot.mjs`。

> 由本节显式半径公式确定性生成，无随机种子。

**怎样读图。** 先看曲线穿过水平虚线的位置，再沿横轴判断所需的 $m/d$ 数量级；不同 $d$ 的曲线并不完全重合，因为置信项 $\log(4/\delta)/d$ 仍保留维数依赖。该图展示的是经典 worst-case 保证的保守程度，不能解释为实际测试误差随样本量变化的预测曲线。

**适用边界（图没有证明什么）。** 图固定 $\delta=0.05$ 并使用本节这一版保守显式半径；它不表示实际模型需要相同的 $m/d$ 才能泛化，也不比较局部复杂度、margin、stability 或 norm-based bounds。$\gamma_m>1$ 只说明该证书空泛，不说明学习算法必然失败。

## 十、从 uniform gap 到 ERM excess risk

令 exact ERM

$$
\widehat h_S\in\arg\min_{h\in\mathcal H}R_S(h),
$$

并假设类内总体最优 $h^*\in\arg\min_hR_P(h)$ 存在。记 high-probability uniform radius 为 $\gamma_m$。在共同事件

$$
\forall h:\ |R_P(h)-R_S(h)|\le\gamma_m
$$

上：

$$
\begin{aligned}
R_P(\widehat h_S)
&\le R_S(\widehat h_S)+\gamma_m
&&\text{learner output 的 deviation}\\
&\le R_S(h^*)+\gamma_m
&&\text{ERM optimality}\\
&\le R_P(h^*)+2\gamma_m
&&\text{comparator 的 deviation}.
\end{aligned}
$$

因此

$$
\boxed{
R_P(\widehat h_S)-R_{\mathcal H}^*
\le2\gamma_m.
}
$$

若是 $\rho$-approximate ERM：

$$
R_S(\widetilde h_S)
\le\inf_hR_S(h)+\rho,
$$

则

$$
\boxed{
R_P(\widetilde h_S)-R_{\mathcal H}^*
\le2\gamma_m+\rho.
}
$$

若 population infimum 不取到，选任意 $\eta$-optimal comparator，最后令 $\eta\downarrow0$，结论仍成立。

## 十一、样本复杂度怎样读

要让 uniform gap 至多 $\alpha$，一个隐式充分条件是

$$
\boxed{
m
\ge
\frac8{\alpha^2}
\left[
d\log\frac{2em}{d}
+\log\frac4\delta
\right].
}
$$

$m$ 同时出现在左侧和 log 内，这不是循环定义错误；可数值求最小整数，或用粗化消去。它给出尺度

$$
m
=O\left(
\frac{d\log(1/\alpha)+\log(1/\delta)}{\alpha^2}
\right).
$$

对 exact ERM excess 目标 $\varepsilon$，令 $\alpha=\varepsilon/2$：

$$
m
=O\left(
\frac{d\log(1/\varepsilon)+\log(1/\delta)}{\varepsilon^2}
\right)
$$

是这条经典 growth-function proof 的直接结果。

> [!important] 经典显式界不是最优阶终点
> binary agnostic PAC 的最优 sample-complexity 阶可达
> $$
> \Theta\left(\frac{d+\log(1/\delta)}{\varepsilon^2}\right),
> $$
> 不需要额外 $\log(1/\varepsilon)$。去掉经典证明中的 log 需要更细的 covering/Rademacher/经验过程估计，而不能从上面一行代数中凭空删除。[[Rademacher 复杂度与经验复杂度]]与[[覆盖数、Metric Entropy 与 Chaining 入口]]将解释改善发生在哪里。

## 十二、手算：正确但可能很松的界

取

$$
d=10,
\qquad m=5000,
\qquad\delta=0.05.
$$

先算 complexity：

$$
d\log\frac{2em}{d}
=10\log(1000e)
\approx79.08,
$$

$$
\log\frac4\delta=\log80\approx4.38.
$$

所以

$$
\gamma_m
\le
\sqrt{\frac8{5000}(79.08+4.38)}
\approx0.365.
$$

exact ERM excess bound 约为 $0.730$。这个数远可能大于实际 test excess，但 theorem 仍有意义：它对任意数据分布、任意 VC 维 10 的 class、任意 iid sample 给统一置信保证。

这个例子必须学会两种判断同时成立：

1. 数学结论合法；
2. 数值上对当前任务可能不够有用。

不能因为 bound 松就宣称模型没有泛化，也不能因为模型实测泛化好就宣称 worst-case theorem 已精确解释原因。

## 十三、realizable 情形为何可有 $1/\varepsilon$

本节的双侧 uniform convergence 要估计任意非零 Bernoulli risk 到精度 $\varepsilon$，因此 exponent 是 $m\varepsilon^2$。若 realizable 且 learner 输出 consistent hypothesis，则一个真实风险至少 $\varepsilon$ 的坏假设必须在 $m$ 个训练点上全部零错，其生存概率像

$$
(1-\varepsilon)^m\le e^{-m\varepsilon}.
$$

把 growth-function double-sampling 与这个 one-sided survival event 结合，会得到经典

$$
O\left(
\frac{d\log(1/\varepsilon)+\log(1/\delta)}{\varepsilon}
\right)
$$

consistent-learning 上界。完整 realizable/agnostic 等价和上下界比较放在 [[二分类统计学习基本定理]]；此处只强调 $1/\varepsilon$ 与 $1/\varepsilon^2$ 来自不同概率事件，不是把同一公式换个常数。

## 十四、假设边界与证明断点

### 14.1 iid / exchangeability

我们同时使用：

- $S'$ 与 $S$ 独立同分布；
- 每对 $(Z_i,Z_i')$ 可交换；
- signs 条件下各 pair 独立；
- Hoeffding 的独立性。

时间序列、adaptive sampling、同 batch coupling 或 distribution drift 会在这些步骤断裂，需要 mixing、martingale、online 或 stability 工具。

### 14.2 0–1 bounded loss

error pattern 数与 prediction pattern 数由 XOR 等数，且 $a_i\in[-1,1]$。对实值/无界 loss，VC 维本身不够；需要 pseudo-dimension、fat-shattering、tail assumption 或 loss contraction。

### 14.3 class 必须事先固定

若用同一数据选择 representation、architecture 或 prompt generator 后才定义 $\mathcal H_S$，本 theorem 不能条件化后当它事先固定。必须把所有选择纳入一个更大的预先 class、使用独立 validation，或分析 algorithm/data-dependent complexity。

### 14.4 distribution-free 不等于 shift-robust

“对任意 $P$”表示 theorem 对每个固定 train/deployment law 都成立；它仍假设训练和未来样本来自同一个 $P$。若 deployment 变为 $Q\ne P$，这里只控制 $R_P$，不自动控制 $R_Q$。

### 14.5 randomized learner

uniform event 对全部 $h\in\mathcal H$ 同时成立，所以 randomized learner 只要输出仍在 $\mathcal H$，额外随机种子不破坏代入。但若随机性改变 class 或数据收集分布，需要重新定义对象合同。

## 十五、AI 中的对象映射

### 15.1 固定 representation 的 binary head

设冻结 encoder 输出

$$
\Phi(X)\in\mathbb R^{m\times d},
$$

head 为 affine threshold。定理中的：

- $h$：完整的 feature-to-label 函数，不只是 weight vector；
- $\mathcal H$：所有允许 heads；
- $S$：iid labeled downstream examples；
- $R_S$：训练/经验 0–1 risk；
- $R_P$：同分布未来 0–1 risk；
- $d+1$：一般位置下的 VC 维，而非 batch size。

若 encoder 也用 $S$ fine-tune，固定-head class 已不再覆盖完整 pipeline。

### 15.2 checkpoint / prompt selection

若预先固定一族 binary evaluators，VC/finite-class uniform event 可以保护数据依赖的 ERM selection。若 prompts 由 evaluation failures 反复自适应生成，class 不再预先固定；需要把生成协议包含进 class 或使用独立 holdout/adaptive data analysis。

### 15.3 深网容量报告

报告一个 neural VC upper bound 时至少同时给：

1. 网络函数类的精确定义；
2. 激活、深度、参数共享和输出阈值；
3. bound 是 upper/lower 还是 tight order；
4. 代回真实 $m,\delta$ 后 radius 是否小于 1；
5. 是否只证明 worst-case class capacity，还是利用了实际 norms/margins/algorithm。

只写“VC dimension 有限，所以深网会泛化”遗漏了数值非平凡性和实际 inductive bias。

## 十六、常见错误

> [!warning] 对每个 $h$ 分别有 $1-\delta$，所以同时对所有 $h$ 有 $1-\delta$
> 错。无限多个 individual events 的交概率可能很小。增长函数只在对称化后把 pooled restrictions 变成有限事件族。

> [!warning] ghost sample 是算法需要的第二份数据
> 错。它是 proof device，用于控制原 learner 只使用 $S$ 时的概率；部署时不要求真的抽取 $S'$。

> [!warning] $\tau(m)$ 应该乘标签的 $2^m$
> 错。固定 pooled labels 后，prediction-to-error 是 XOR 双射；labels 已包含在随机样本中。

> [!warning] 用 $\tau(m)$ 而不是 $\tau(2m)$
> 双样本差依赖 $S$ 与 $S'$ 的联合 restriction，最多涉及 $2m$ 个输入。

> [!warning] 从经典 bound 直接宣称最优 sample complexity 含 $\log(1/\varepsilon)$
> 它只是此证明路线的上界。判断最优阶需要匹配 upper/lower bounds 与更精细工具。

## 十七、前沿地位与研究边界

- **经典定理**：finite VC $\Rightarrow$ binary 0–1 uniform convergence，及由此得到的 ERM learnability；
- **经典但非最紧证明**：本节点的 explicit growth-function radius；
- **已建立改进**：最优 agnostic rate 去掉额外 log，data-dependent/margin/norm/local complexity 可在结构允许时更细；
- **实践边界**：现代 overparameterized networks 的 worst-case VC bound 往往数值 vacuous；
- **开放问题**：怎样把 feature learning、optimization bias、数据几何和 scale 统一进可计算且预测力强的泛化理论。

## 十八、本节回顾

1. 对称化中为何需要 $m\varepsilon^2\ge2$？
2. 第一个因子 2、第二个因子 2 和指数 $1/8$ 分别来自哪里？
3. 为什么条件于 pooled sample 后才可把 class 当成至多 $\tau(2m)$ 个 patterns？
4. error pattern 数为何不超过 prediction growth？
5. Sauer–Shelah 在证明链中只承担哪一步？
6. uniform gap 为 $\gamma$ 时，ERM excess 为什么是 $2\gamma$？
7. 经典显式界与最优 agnostic rate 为什么可以不同？
8. deployment shift 会破坏哪个风险对象，而不是哪条组合计数？

## 十九、来源与后继

- 原始一致收敛来源：[[S-1971-Vapnik-Chervonenkis-Uniform-Convergence]]；
- 组合输入：[[S-1972-Sauer-Density-Families-Sets]]与[[S-1972-Shelah-Combinatorial-Problem]]；
- 现代教材：[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]] 第 6 章；
- 浓缩输入：[[S-1963-Hoeffding-Bounded-Random-Variables]]；
- 下一步：[[二分类统计学习基本定理]]区分 uniform convergence、ERM learnability、PAC learnability 与 finite VC 的等价条件和 quantitative rates；
- 训练闭环：[[习题 - VC 一致收敛与泛化界]]与[[解答 - VC 一致收敛与泛化界]]。
