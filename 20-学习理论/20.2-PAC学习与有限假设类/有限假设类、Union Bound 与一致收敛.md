---
type: concept
status: draft
area: [learning-theory/pac, probability/union-bound, machine-learning/generalization]
aliases: [Finite Hypothesis Classes, Uniform Convergence, Simultaneous Concentration]
node_id: LT-11
prerequisites: ["[[泛化间隙与浓缩不等式接口]]", "[[PAC 学习定义与样本复杂度]]", "[[浓缩不等式]]", "[[经验风险最小化、近似 ERM 与超额风险分解]]"]
related: ["[[可实现情形的一致 ERM 保证]]", "[[不可知 PAC、ERM 与双侧一致收敛]]", "[[打散、增长与 VC 维]]", "[[Occam 界、编码长度与先验权重]]"]
sources: ["[[S-1963-Hoeffding-Bounded-Random-Variables]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-2020-Su-7466-泛化性乱弹]]"]
exercises: ["[[习题 - 有限假设类、Union Bound 与一致收敛]]"]
solutions: ["[[解答 - 有限假设类、Union Bound 与一致收敛]]"]
created: 2026-08-20
updated: 2026-08-23
---

# 有限假设类、Union Bound 与一致收敛

> [!abstract] 本章主问题
> 若 $\mathcal H$ 含 $M$ 个预先固定的假设、损失在 $[0,1]$ 且样本 iid，那么对每个 $h$ 的 Hoeffding 坏事件做 Union Bound，可得
> $$
> \Pr\!\left(\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|>\varepsilon\right)
> \le2M e^{-2m\varepsilon^2}.
> $$
> 因而 class complexity 只以 $\log M$ 进入置信半径。这个 simultaneous event 允许我们安全地控制看过数据后选出的 ERM；它是最简单的一致收敛定理，也是 VC、Rademacher 与描述长度思想的原型。

> [!question] 初学者读完必须能回答
> 1. Supremum 偏差事件为什么等价于各 $B_h$ 的并集？
> 2. Union Bound 为什么不要求 $B_h$ 相互独立？
> 3. $M$ 为什么以 $\log M$ 而不是 $M$ 进入置信半径？
> 4. 共同好事件怎样合法覆盖数据依赖的 ERM 输出 $h_S$？
> 5. 候选集由评价数据生成或 $M=\infty$ 时，简单证明在哪里断开？

先用下图回答一个视觉问题：**怎样把 $M$ 个 pointwise 浓缩证书合成一个可以安全覆盖数据依赖选择的共同事件？**

![[00-知识库管理/_assets/figures/learning-theory/fig-finite-class-union-uniform-convergence-v2.svg|880]]

> [!figure] 图 20.2.3｜有限类、Union Bound 与一致收敛
> A 为每个固定 $h$ 定义偏差坏事件；B 将“存在坏 $h$”改写为事件并集并应用 Boole inequality；C 反解 simultaneous radius，显示候选函数数目只以 $\log M$ 进入，同时强调 candidate set 必须独立固定。来源：独立绘制；理论接口参考 Hoeffding inequality、Boole inequality 与 finite-class uniform convergence；生成脚本：[[plot_pac_finite_class_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** 先把 supremum 写成存在量词，再把存在量词翻译为并集；逐个代入 fixed-$h$ 尾界后相加，最后令总失败概率不超过 $\delta$ 并反解 $\varepsilon$。共同好事件一旦成立便同时覆盖所有 $h$，因此也覆盖随后由样本选出的 $h_S$。

**适用边界（图没有证明什么）。** 图没有声称 Union Bound 紧，也没有把参数配置数自动等同于不同函数数。若候选类用同一数据自适应构造、损失无界、样本不独立或类无限，需条件化、sample splitting、covering/VC/Rademacher 等新工具；$\log M$ 只是选择复杂度，不负责 approximation 或 optimization error。

## 一、学习目标

1. 从 fixed-$h$ Hoeffding 推导 finite-class simultaneous bound；
2. 正确操作 $\sup_h$、$\exists h$ 与 Union Bound；
3. 反解 uniform convergence 的置信半径与样本复杂度；
4. 解释为什么 class size 以 $\log M$ 而不是 $M$ 进入样本量；
5. 说明 simultaneous event 如何覆盖 data-dependent $h_S$；
6. 用一致收敛推导 approximate ERM 的 class excess risk；
7. 区分 pointwise convergence 与 uniform convergence；
8. 识别“参数配置数量”和“不同函数数量”的差别；
9. 判断 data-dependent candidate set 何时破坏简单证明；
10. 理解有限类证明向 VC、Rademacher、Occam bound 的推广方向。

## 二、问题设置

设

$$
\mathcal H=\{h_1,\ldots,h_M\},
\qquad |\mathcal H|=M<\infty.
$$

样本

$$
S=(Z_1,\ldots,Z_m)\sim P^m,
$$

损失满足

$$
0\le\ell(h,z)\le1.
$$

对每个固定 $h$，LT-09 已给出

$$
\Pr_S\left(|R_S(h)-R_P(h)|>\varepsilon\right)
\le2e^{-2m\varepsilon^2}.
$$

现在的目标不是单独问某个 $h$，而是构造一个**共同的好事件**：在这同一份样本上，所有 $h$ 的经验风险都接近各自总体风险。

## 三、从 supremum 到事件并集

定义每个假设的坏事件

$$
B_h
=\left\{S:
|R_S(h)-R_P(h)|>\varepsilon
\right\}.
$$

至少一个假设偏差过大的事件是

$$
\bigcup_{h\in\mathcal H}B_h.
$$

它与 supremum 事件完全等价：

$$
\left\{
\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|>\varepsilon
\right\}
=\bigcup_{h\in\mathcal H}B_h.
$$

所以“控制 supremum”可以翻译成“控制有限多个坏事件的并集”。

## 四、Union Bound 完整推导

Boole 不等式给出

$$
\Pr\left(\bigcup_{h\in\mathcal H}B_h\right)
\le\sum_{h\in\mathcal H}\Pr(B_h).
$$

对每个 $h$ 代入 Hoeffding：

$$
\begin{aligned}
\Pr\left(
\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|>\varepsilon
\right)
&\le\sum_{h\in\mathcal H}2e^{-2m\varepsilon^2}\\
&=2M e^{-2m\varepsilon^2}.
\end{aligned}
$$

因此

$$
\boxed{
\Pr\left(
\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|>\varepsilon
\right)
\le2|\mathcal H|e^{-2m\varepsilon^2}.
}
$$

等价的好事件形式是

$$
\boxed{
\Pr\left(
\forall h\in\mathcal H:
|R_S(h)-R_P(h)|\le\varepsilon
\right)
\ge1-2M e^{-2m\varepsilon^2}.
}
$$

> [!important] 不需要事件独立
> $B_{h_1},\ldots,B_{h_M}$ 都由同一个 $S$ 生成，通常强烈相关。Union Bound 仍然成立，因为
> $$
> \mathbf1\{\cup_hB_h\}\le\sum_h\mathbf1\{B_h\}
> $$
> 是逐点成立的；对两边取期望即可。

## 五、反解统一置信半径

令失败上界等于 $\delta$：

$$
2M e^{-2m\varepsilon^2}=\delta.
$$

则

$$
2m\varepsilon^2
=\log\frac{2M}{\delta},
$$

所以以至少 $1-\delta$ 的概率：

$$
\boxed{
\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|
\le
\sqrt{\frac{\log(2M/\delta)}{2m}}.
}
$$

展开对数：

$$
\log\frac{2M}{\delta}
=\log M+\log\frac2\delta.
$$

因此统一半径的尺度是

$$
O\!\left(
\sqrt{\frac{\log M+\log(1/\delta)}{m}}
\right).
$$

### 5.1 uniform convergence sample complexity

要保证 uniform deviation 不超过 $\varepsilon$，充分条件是

$$
\boxed{
m\ge
\frac{\log(2M/\delta)}{2\varepsilon^2}.
}
$$

若样本量必须为整数，可取

$$
m_{\mathcal H}^{\rm UC}(\varepsilon,\delta)
\le
\left\lceil
\frac{\log(2M/\delta)}{2\varepsilon^2}
\right\rceil.
$$

这里是一个充分上界，未宣称对所有有限类都达到最优常数。

## 六、为什么复杂度是 $\log M$

Union Bound 先产生乘法因子 $M$：

$$
M e^{-cm\varepsilon^2}.
$$

要让它小于 $\delta$，取对数后得到

$$
cm\varepsilon^2
\ge \log M+\log(1/\delta).
$$

所以 $M$ 在 tail probability 中是乘法，在 sample size 中变成 $\log M$。

### 6.1 描述长度直觉

从 $M$ 个候选中指出一个，需要约

$$
\log_2 M
$$

bits。有限类 bound 因而暗示：选择自由度可以用“描述候选所需的信息量”衡量。后续 Occam bound 会给不同假设不同 code length，PAC-Bayes 则把复杂度换成 posterior 相对 prior 的 KL。

### 6.2 对数底数

概率论推导默认自然对数。若用 $\log_2$，只差常数 $\ln2$：

$$
\ln M=(\ln2)\log_2M.
$$

严谨写常数时不要静默换底；讨论大 $O$ 时通常无关紧要。

## 七、simultaneous event 如何覆盖 $h_S$

设算法输出 $h_S\in\mathcal H$。在好事件

$$
G=\left\{
\forall h\in\mathcal H:
|R_S(h)-R_P(h)|\le\varepsilon
\right\}
$$

上，结论对**每个** $h$ 都成立，因此特别对由 $S$ 选择的 $h_S$ 成立：

$$
|R_S(h_S)-R_P(h_S)|\le\varepsilon.
$$

关键不是把 $h_S$ 当成固定，而是先建立覆盖整个 class 的共同事件，然后在这个事件内部代入任何 data-dependent choice。

> [!note] 两种逻辑路线
> 错误路线：固定 $h$ 的定理 $\to$ 直接把 $h$ 换成 $h_S$。
>
> 正确路线：固定每个 $h$ $\to$ Union Bound 得 all-$h$ event $\to$ 在共同事件内代入 $h_S$。

## 八、一致收敛的定义

称 $\mathcal H$ 关于 loss $\ell$ 具有 uniform convergence property，若存在函数 $m_{\mathcal H}^{\rm UC}(\varepsilon,\delta)$，使对所有允许 $P$，当 $m$ 不小于该阈值时：

$$
\Pr_{S\sim P^m}\left(
\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|\le\varepsilon
\right)
\ge1-\delta.
$$

有限类与有界 loss 的推导已经证明了这一性质。

### 8.1 pointwise vs uniform

pointwise convergence 说，对每个固定 $h$：

$$
R_S(h)\to R_P(h).
$$

uniform convergence 说：

$$
\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|\to0.
$$

在无限类中，可能每个固定函数都收敛，但 supremum 不收敛，因为“最坏的函数”随样本变化。这正对应学习算法的数据依赖选择。

## 九、从一致收敛到 approximate ERM

令 $\widetilde h_S$ 是 $\rho$-approximate ERM：

$$
R_S(\widetilde h_S)
\le\inf_{h\in\mathcal H}R_S(h)+\rho.
$$

设 class optimum $h_{\mathcal H}^*$ 存在。在 uniform event

$$
\sup_{h\in\mathcal H}|R_S(h)-R_P(h)|\le\alpha
$$

上：

$$
\begin{aligned}
R_P(\widetilde h_S)
&\le R_S(\widetilde h_S)+\alpha\\
&\le R_S(h_{\mathcal H}^*)+\rho+\alpha\\
&\le R_P(h_{\mathcal H}^*)+2\alpha+\rho.
\end{aligned}
$$

因此

$$
\boxed{
R_P(\widetilde h_S)-R_{\mathcal H}^*
\le2\alpha+\rho.
}
$$

代入有限类半径：

$$
R_P(\widetilde h_S)-R_{\mathcal H}^*
\le
2\sqrt{\frac{\log(2M/\delta)}{2m}}+\rho
$$

以至少 $1-\delta$ 的概率成立。

### 9.1 为什么是 $2\alpha$

一次 deviation 用在输出 $\widetilde h_S$ 上，把 population risk 换成 empirical risk；另一次用在 oracle $h_{\mathcal H}^*$ 上，把 empirical comparator 换回 population comparator。因此有两个 gap。

### 9.2 目标 excess 为 $\varepsilon$

若 exact ERM 即 $\rho=0$，要让 excess 不超过 $\varepsilon$，足以要求 uniform radius

$$
\alpha\le\varepsilon/2.
$$

于是

$$
m\ge
\frac{2\log(2M/\delta)}{\varepsilon^2}.
$$

这就是有限类 agnostic ERM 的基本缩放；LT-13 将把 theorem、常数与 approximate ERM 情形单独闭环。

## 十、$M$ 到底在数什么

$M$ 应数假设空间中的不同预测函数，而不是代码仓库中的模型文件数，更不是参数向量的数量。

### 10.1 重复参数化

神经网络可因 hidden-unit permutation、ReLU rescaling 等原因，让许多参数向量表示同一个函数。直接数参数配置既可能是无穷，也会大量重复。

### 10.2 只在支持集上不同才有风险差异

若两个函数只在 $P_X$ 概率零的区域不同，它们有相同总体 risk。某些更精细分析会按分布下的等价类计数，但 distribution-free theorem 不能预先利用未知 $P$ 的零测集。

### 10.3 离散化连续参数

若参数被 $b$ bit 量化、共有 $p$ 个独立编码位，粗略有

$$
M\le2^p,
\qquad \log M\le p\log2.
$$

这能产生一个正确但往往很松的 bound；是否有意义取决于量化后函数与 loss 的近似误差。

## 十一、候选集必须怎样“固定”

简单证明假设 $\mathcal H$ 在抽样前固定。若先看 $S$ 再构造候选集 $\mathcal H_S$，不能仅以观察到的 $|\mathcal H_S|$ 代入公式，因为候选生成过程已编码样本信息。

可安全的常见情形包括：

1. 候选集只依赖与评价样本独立的数据；
2. 对一个预先固定的更大母类做 uniform bound；
3. 条件于独立随机机制后，候选仍与评价样本独立；
4. 用 sample splitting、PAC-Bayes、information 或 adaptive analysis 记账。

> [!example] 模型选择
> 用训练集生成 100 个 checkpoint，再用独立验证集选择一个。条件于训练过程，这 100 个候选对验证集固定，可在验证集上做 $M=100$ 的 simultaneous bound。若验证得分反过来持续驱动新 checkpoint 生成，就不再是简单的一次固定候选比较。

## 十二、Union Bound 的松与不可替代

Union Bound 可能松，因为它把高度重叠的坏事件直接相加。但它有三个优势：

- 无需事件独立；
- 证明透明、常数明确；
- 常能抓住正确的 $\log M$ 尺度。

若不同假设的预测高度相似，实际“有效复杂度”远小于 $\log M$。覆盖数、VC growth function、Rademacher complexity 和 Gaussian complexity 会利用函数之间的几何/相关结构。

## 十三、有限类到无限类的三条桥

### 13.1 数据上的不同标记数

即使 $\mathcal H$ 无限，在 $m$ 个点上可能只能产生有限种 label patterns。增长函数与 VC 维用这一点替代全局 $|\mathcal H|$。

### 13.2 用 $\varepsilon$-net 离散化

若无限类可由有限覆盖近似，先对 cover 做 Union Bound，再控制近似误差。这引出 covering number 与 metric entropy。

### 13.3 data-dependent complexity

Rademacher complexity 直接测量类在观察样本上拟合随机符号的能力，避免仅按最坏情形全局计数。

## 十四、一个数值例子

设 $M=10^6$、$m=10^4$、$\delta=0.05$。统一半径为

$$
\sqrt{\frac{\log(2\cdot10^6/0.05)}{2\cdot10^4}}
\approx0.030.
$$

尽管有一百万个候选，复杂度只通过 $\log(10^6)\approx13.8$ 进入；但这依赖候选在评价样本抽取前固定，且损失在 $[0,1]$。

若要用 exact ERM 得到 class excess 不超过约 $0.06$，上述 $2\alpha$ bridge 正好给出相应量级。

## 十五、AI 应用解释

### 15.1 超参数网格

预先固定 $M$ 组超参数、各训练一个模型，然后在独立 validation set 上选择最优者，可把最终选择看成 $M$ 个固定损失函数之一，并对 validation selection 做 simultaneous correction。

### 15.2 多 benchmark 与多指标

若同时搜索许多模型、任务和指标，“尝试总数”不只是模型数。每个被用于选择/宣传的统计查询都可能贡献 multiplicity；必须先定义 family of claims。

### 15.3 深度网络

对实数参数网络直接使用 $|\mathcal H|$ 通常无意义。即便量化使 class 有限，所得 bit-count bound 往往过松。科学空间对深度泛化的讨论可作为机制层提醒；正式 theorem 仍要转向 margin、norm、compression、PAC-Bayes 或 algorithmic stability 等结构。

## 十六、常见误解

> [!failure] “Union Bound 要求各模型错误独立”
> 错。它对任意事件成立。

> [!failure] “对每个 $h$ 有 $95\%$ 置信度，所以同时对全部 $h$ 也有 $95\%$”
> 错。若不校正，至少一个失败的概率可能随候选数显著增加。

> [!failure] “类有 $p$ 个实参数，所以 $M=p$”
> 错。连续参数通常产生无限函数；参数个数不是 cardinality。

> [!failure] “最终只选了一个模型，所以 $M=1$”
> 错。若这个模型是从 $M$ 个候选中根据同一评价数据选出的，选择自由度来自整个候选集合。

> [!failure] “uniform convergence 是所有泛化的必要解释”
> 错。它是强而通用的充分路线；稳定性、压缩等可在某些场景绕开全类 uniform convergence。

## 十七、证明模板

1. 写出预先固定的 finite class 与 $M$；
2. 对每个 $h$ 定义坏事件 $B_h$；
3. 用 fixed-$h$ inequality 控制 $\Pr(B_h)$；
4. 把 supremum event 改写为 $\cup_hB_h$；
5. 使用 Union Bound，不添加虚假的 independence 假设；
6. 令总失败概率小于 $\delta$ 并反解；
7. 只有建立 simultaneous event 后，才代入 $h_S$；
8. 若要控制 ERM excess，记得出现两个 deviation terms。

## 十八、本节边界与来源说明

- fixed-$h$ tail 以 Hoeffding 原始结果为概率论基础；
- finite-class uniform convergence 与 ERM bridge 以标准学习理论教材为准；
- 科学空间文章只承担深度模型机制与经典容量解释边界的延伸阅读，不作为本定理来源。

## 十九、掌握检查

- [ ] 我能从事件并集完整推导 $2Me^{-2m\varepsilon^2}$；
- [ ] 我能解释为何事件无需独立；
- [ ] 我能反解统一置信半径；
- [ ] 我能解释 $\log M$ 的描述长度直觉；
- [ ] 我能在共同事件内合法代入 $h_S$；
- [ ] 我能推导 approximate ERM 的 $2\alpha+\rho$；
- [ ] 我能识别 data-dependent candidate set 的问题；
- [ ] 我知道有限类方法如何通向 VC、covering 与 Rademacher。

## 二十、进一步连接

- [[可实现情形的一致 ERM 保证]]：不用双侧 uniform estimation，而用“坏函数零错生存”得到快一个 $\varepsilon$ 次方的 rate；
- [[不可知 PAC、ERM 与双侧一致收敛]]：把本节 $2\alpha$ bridge 变成完整 agnostic theorem；
- [[打散、增长与 VC 维]]：无限二分类如何把 $\log M$ 替换成 data-label complexity；
- [[Occam 界、编码长度与先验权重]]：给不同假设分配不同失败预算，推广到可数 class。
