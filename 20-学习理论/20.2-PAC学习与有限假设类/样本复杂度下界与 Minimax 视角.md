---
type: concept
status: draft
area: [learning-theory/lower-bounds, statistics/minimax, information-theory]
aliases: [Sample Complexity Lower Bounds, Minimax Risk, Le Cam and Fano]
node_id: LT-16
prerequisites: ["[[No-Free-Lunch 与归纳偏置]]", "[[不可知 PAC、ERM 与双侧一致收敛]]", "[[交叉熵与 KL 散度]]", "[[假设检验、置信区间与多重比较]]"]
related: ["[[二分类统计学习基本定理]]", "[[互信息与信息论泛化界]]", "[[局部 Rademacher 复杂度与快收敛率]]", "[[Bandit Feedback 与强化学习接口]]"]
sources: ["[[S-1997-Yu-Assouad-Fano-Le-Cam]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1984-Valiant-Theory-of-the-Learnable]]"]
exercises: ["[[习题 - 样本复杂度下界与 Minimax 视角]]"]
solutions: ["[[解答 - 样本复杂度下界与 Minimax 视角]]"]
created: 2026-08-20
updated: 2026-08-23
---

# 样本复杂度下界与 Minimax 视角

> [!abstract] 本章主问题
> 上界通过构造一个算法证明“可以做到”；下界必须对任意算法证明“都做不到”。Minimax 方法把后者写成 $\inf_A\sup_{P\in\mathcal P}$，再构造参数相隔足够远、但 $m$ 个样本分布仍难区分的 $P_0,P_1$ 或 packing。Le Cam 用两点得到基础精度/置信依赖，Fano 用多点产生 $\log M$ 或维数依赖，Assouad 用 hypercube 累加坐标困难。它们解释 finite-class agnostic 的 $1/\varepsilon^2$ 在一般噪声下不是 Hoeffding 的偶然松弛。

> [!question] 初学者读完必须能回答
> 1. 一个算法的坏例子与 minimax lower bound 的量词有何根本不同？
> 2. Le Cam 为什么同时要求 $P_0^m,P_1^m$ 接近而最优决策分离？
> 3. Testing error 怎样转换成 estimation 或 excess-risk 下界？
> 4. Fano 与 Assouad 分别怎样把二点困难推广到多世界或多坐标？
> 5. Expected、high-probability 与 sample-complexity 下界为何必须分开陈述？

先用下图回答一个视觉问题：**怎样构造“统计上难分辨、决策上必须分开”的世界，使任意学习算法都承担不可避免的风险？**

![[00-知识库管理/_assets/figures/learning-theory/fig-minimax-lower-bound-information-v2.svg|880]]

> [!figure] 图 20.2.8｜样本复杂度下界与 Minimax 信息瓶颈
> A 对照上界与下界的量词次序；B 展示 Le Cam 两点法中 product distributions 的接近性与 optimal actions 的分离；C 将方法扩展为 Fano 的多世界 packing 与 Assouad 的 hypercube 坐标累加。来源：独立绘制；理论接口参考 Le Cam、Fano、Assouad 与 minimax decision theory；生成脚本：[[plot_pac_finite_class_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** A 先确认结论是“对任意算法存在难分布”，而不是只让某个算法失败；B 选择 perturbation，使 $m$ 份样本的 TV/KL 仍小，但两世界的正确动作距离足够大，然后把决策误差归约为检验误差；C 按所需复杂度因子选择二点、多点或多坐标构造。

**适用边界（图没有证明什么）。** 图是 lower-bound 工作流，不自动给出某个具体问题的数值下界；必须另行声明 problem family、loss、metric、randomization、概率模式与参数范围。KL 小只是难分辨的充分接口之一，expected lower bound 也不能无条件升级为同常数的高概率结论；minimax 困难不排除带额外结构或 favorable distribution 的更快率。

## 一、学习目标

1. 区分 algorithm-specific failure 与 minimax impossibility；
2. 定义 expected minimax risk、high-probability minimax quantile 与 sample complexity；
3. 推导 Le Cam two-point reduction 的 metric-risk 形式；
4. 使用 total variation、KL product rule 与 Pinsker；
5. 用 Bernoulli two-point construction 得到 $1/\sqrt m$ estimation rate；
6. 用 testing tail 解释 $\log(1/\delta)/\varepsilon^2$；
7. 陈述并解释 Fano many-way lower bound；
8. 说明 Assouad 如何把 hypercube 坐标困难相加；
9. 比较 realizable 与 agnostic finite-class 上下界尺度；
10. 识别 lower bound 的 problem family、loss 与 probability mode 边界。

## 二、先分清三种结论

### 2.1 一个算法的坏例子

存在 $P$ 使某个算法 $A_0$ 失败：

$$
\exists P:\ R_P(A_0(S))\text{ large}.
$$

这只否定 $A_0$，别的算法可能成功。

### 2.2 minimax lower bound

$$
\boxed{
\inf_A\sup_{P\in\mathcal P}
\mathbb E_{S\sim P^m}
L(A(S),P)
\ge r_m.
}
$$

先允许我们选择最佳算法，再让最坏分布行动；若结果仍大，说明 problem family 本身困难。

### 2.3 sample complexity lower bound

定义

$$
m^*(\varepsilon,\delta)
=\inf\left\{
m:\exists A,
\sup_{P\in\mathcal P}
\Pr_{P^m}(L(A(S),P)>\varepsilon)
\le\delta
\right\}.
$$

证明

$$
m^*(\varepsilon,\delta)\ge g(\varepsilon,\delta)
$$

意味着少于该样本量时，每个算法都至少在一个 $P$ 上违反 PAC event。

## 三、expected risk 与 high-probability risk

expected minimax risk：

$$
\mathfrak R_m^*
=\inf_A\sup_{P\in\mathcal P}
\mathbb E L(A(S),P).
$$

minimax $(1-\delta)$ quantile 可定义为

$$
q_m^*(\delta)
=\inf_A\sup_{P\in\mathcal P}
\inf\{r:\Pr(L(A(S),P)>r)\le\delta\}.
$$

二者不能不加条件地互换：

- expectation lower bound 可由 boundedness 给某些常数概率 lower bound；
- 精确 $\log(1/\delta)$ dependence 通常需要 testing affinity/tail 工具；
- PAC sample complexity 本质上是 high-probability quantity。

## 四、lower bound 的核心反证逻辑

选择若干 distributions $P_v$，它们满足：

1. **decision separation**：不同 $v$ 的最优参数/预测器相距至少 $2s$；
2. **statistical closeness**：$P_v^m$ 仍然难区分；
3. **reduction**：若 learner 的 loss 小于 $s$，就能从输出解码 $v$；
4. **testing lower bound**：任何 decoder 都有不可忽略错误率；
5. 因此 learner 必有不可忽略 loss。

最困难的设计往往不是套某个 inequality，而是同时让 separation 大、KL/TV 小。

## 五、Le Cam two-point method

考虑两个参数 $\theta_0,\theta_1$ 及 distributions $P_0,P_1$。设 metric $d$ 满足

$$
d(\theta_0,\theta_1)\ge2s.
$$

任意 estimator $\widehat\theta=A(S)$ 都可诱导 test：输出离 $\widehat\theta$ 更近的 index。

若真世界是 $j$，但 test 选错，则 triangle inequality 保证

$$
d(\widehat\theta,\theta_j)\ge s.
$$

所以

$$
\mathbb E_jd(\widehat\theta,\theta_j)
\ge s\Pr_j(\text{test error}).
$$

等先验 binary testing 的最小平均错误率为

$$
\frac{1-\operatorname{TV}(P_0^m,P_1^m)}{2}.
$$

因此

$$
\boxed{
\inf_{\widehat\theta}
\sup_{j\in\{0,1\}}
\mathbb E_jd(\widehat\theta,\theta_j)
\ge
\frac{s}{2}
\left(1-\operatorname{TV}(P_0^m,P_1^m)\right).
}
$$

若记 separation $\Delta=d(\theta_0,\theta_1)=2s$，右端是

$$
\frac\Delta4(1-\operatorname{TV}).
$$

### 5.1 high-probability 形式

同一 reduction 给

$$
\boxed{
\inf_{\widehat\theta}
\sup_j
\Pr_j\left(d(\widehat\theta,\theta_j)\ge s\right)
\ge
\frac{1-\operatorname{TV}(P_0^m,P_1^m)}{2}.
}
$$

所以只要 product distributions 仍重叠，某个世界下 estimator 以常数概率至少错 $s$。

## 六、如何控制 product-distribution closeness

### 6.1 KL product rule

iid samples 给

$$
\mathrm{KL}(P_0^m\|P_1^m)
=m\,\mathrm{KL}(P_0\|P_1).
$$

每个样本携带的信息线性累积。

### 6.2 Pinsker inequality

$$
\operatorname{TV}(P,Q)
\le\sqrt{\frac12\mathrm{KL}(P\|Q)}.
$$

合并：

$$
\operatorname{TV}(P_0^m,P_1^m)
\le
\sqrt{\frac m2\mathrm{KL}(P_0\|P_1)}.
$$

要维持 constant overlap，通常选择 single-sample KL 为 $O(1/m)$。

## 七、Bernoulli 均值例子：$1/\sqrt m$

令

$$
P_0=\operatorname{Bernoulli}(1/2-a),
\qquad
P_1=\operatorname{Bernoulli}(1/2+a),
$$

其中 $0<a\le1/4$。参数 separation 是

$$
|p_1-p_0|=2a.
$$

可验证

$$
\mathrm{KL}(P_0\|P_1)
=2a\log\frac{1+2a}{1-2a}
\le16a^2.
$$

故

$$
\operatorname{TV}(P_0^m,P_1^m)
\le\sqrt{8ma^2}.
$$

选择

$$
a=\frac1{8\sqrt m},
$$

则 TV 被某个严格小于 1 的常数控制。Le Cam 因而给出

$$
\inf_{\widehat p}\sup_{p\in\{p_0,p_1\}}
\mathbb E|\widehat p-p|
\ge\frac{c}{\sqrt m}
$$

对某个 universal $c>0$。若 loss 是 squared error，则得到

$$
\inf_{\widehat p}\sup_p
\mathbb E(\widehat p-p)^2
\ge\frac{c'}{m}.
$$

这证明均值估计的 $1/\sqrt m$ deviation 尺度不是 Hoeffding 独有。

## 八、置信参数为何产生 $\log(1/\delta)$

Bretagnolle–Huber 型 testing inequality 给出

$$
P_0^m(\phi=1)+P_1^m(\phi=0)
\ge
\frac12e^{-\mathrm{KL}(P_0^m\|P_1^m)}.
$$

仍取 Bernoulli pair $1/2\pm\varepsilon$，且 $\varepsilon\le1/4$。single-sample KL 至多 $16\varepsilon^2$，所以任意 test 的最大错误概率至少

$$
\frac14e^{-16m\varepsilon^2}.
$$

若一个 estimator 想在两个世界都以失败概率至多 $\delta$ 达到 absolute error 小于 $\varepsilon$，它诱导的 test 也必须两边错误至多 $\delta$。必要条件为

$$
\delta
\ge\frac14e^{-16m\varepsilon^2},
$$

即

$$
\boxed{
m
\ge
\frac{\log(1/(4\delta))}{16\varepsilon^2}.
}
$$

常数可用更细 construction 改善，但尺度

$$
\Omega\!\left(
\frac{\log(1/\delta)}{\varepsilon^2}
\right)
$$

已经显现。

## 九、从 Bernoulli testing 到 agnostic classification

令 $\mathcal X$ 只有一个点，$\mathcal H=\{h_+,h_-\}$ 为两个常数分类器。世界 $b\in\{+,-\}$ 中：

$$
\Pr(Y=b)=\frac12+a,
\qquad
\Pr(Y=-b)=\frac12-a.
$$

最佳分类器是 $h_b$，risk 为 $1/2-a$；选错分类器 risk 为 $1/2+a$，class excess 为

$$
2a.
$$

所以任何能以小 excess 选择分类器的 learner，都能识别 Bernoulli bias 的符号。取 $a$ 与目标 $\varepsilon$ 同阶，testing lower bound 给

$$
m=\Omega\!\left(
\frac{\log(1/\delta)}{\varepsilon^2}
\right).
$$

即使 $M=2$，agnostic $1/\varepsilon^2$ 已不可避免。

## 十、Fano：从两个世界到多个世界

设 hidden index

$$
V\sim\operatorname{Unif}\{1,\ldots,N\},
$$

条件于 $V=v$，样本 $S\sim P_v^m$。任意 decoder $\widehat V(S)$ 满足 Fano inequality：

$$
\boxed{
\Pr(\widehat V\ne V)
\ge
1-
\frac{I(V;S)+\log2}{\log N}.
}
$$

若存在 reference $Q$ 使

$$
\frac1N\sum_{v=1}^N
\mathrm{KL}(P_v^m\|Q^m)
\le\alpha\log N,
$$

则 $I(V;S)\le\alpha\log N$，所以

$$
\Pr(\widehat V\ne V)
\ge1-\alpha-\frac{\log2}{\log N}.
$$

若 parameters $\theta_v$ 两两满足

$$
d(\theta_v,\theta_{v'})\ge2s,
$$

任何 $d(\widehat\theta,\theta_V)<s$ 的 estimator 都能 nearest-neighbor decode $V$。故 decoding lower bound 转为 estimation lower bound。

### 10.1 $\log N$ 怎样出现

若 single-sample KL 约为 $c s^2$，product KL 约为 $mc s^2$。要让 mutual information 不足以识别 $N$ 个 indices，需

$$
mc s^2\lesssim\log N.
$$

于是

$$
s\gtrsim\sqrt{\frac{\log N}{m}},
$$

或等价地，为达到 $s\le\varepsilon$ 必须

$$
m\gtrsim\frac{\log N}{\varepsilon^2}.
$$

这就是 finite-class agnostic upper bound 中 $\log M$ 的 lower-bound 原型。

## 十一、Assouad：把坐标困难相加

Fano 使用一个 large packing。Assouad 构造 hypercube：

$$
v\in\{-1,+1\}^d,
$$

并让只差一个 bit 的相邻 distributions 难以区分。若 loss 可按 coordinates 分解，则每个 bit 都对应一个 binary test，累计得到

$$
\text{risk lower bound}
\gtrsim
d\times(\text{single-coordinate separation})
\times(\text{testing affinity}).
$$

它特别适合证明 dimension-linear、Hamming、$L_1/L_2$ 与 nonparametric lower bounds。具体应用必须写出邻接 KL/TV，不能只说“由 Assouad 得”。

## 十二、realizable 下界为何是 $1/\varepsilon$

构造两个 targets，它们只在一个 rare point $x_r$ 上标签不同。令

$$
P_X(x_r)=2\varepsilon.
$$

若 $m$ 个样本都未看到 $x_r$，两个 realizable worlds 产生完全相同的 observations；任意算法至少在一个 world 对 $x_r$ 猜错，population error 为 $2\varepsilon>\varepsilon$。

rare point 未见概率是

$$
(1-2\varepsilon)^m
\approx e^{-2m\varepsilon}.
$$

要把 failure 压到 $\delta$，必须有

$$
m
=\Omega\!\left(
\frac{\log(1/\delta)}{\varepsilon}
\right).
$$

这里是“看见稀有区域”问题，不是“估计微小 bias”问题，所以 exponent 对 $\varepsilon$ 是一次。

## 十三、finite class 上下界怎样对照

对 worst-case 足够丰富的 finite classes：

| setting | upper bound | lower-bound mechanism | worst-case scale |
|---|---|---|---|
| realizable | bad consistent survivor | rare points / shattered packing | $\Theta((\log M+\log(1/\delta))/\varepsilon)$ |
| agnostic | uniform/pairwise concentration | noisy many-way testing | $\Theta((\log M+\log(1/\delta))/\varepsilon^2)$ |

但要加一句关键限定：**cardinality $M$ 本身不能给每个具体 class 同样的 lower bound**。

例如某个包含许多高度冗余、嵌套或只在不可达区域不同的 functions 的 class，可能比最坏 $M$-element class 容易。要得到 $\log M$ lower bound，需要 packing、shattering 或其他 richness construction。

## 十四、教材中的 agnostic lower-bound 坐标

标准学习理论可进一步证明，对 VC dimension 为 $d$ 的某些/一般可学习类，agnostic sample complexity 至少按

$$
\Omega\!\left(
\frac{d+\log(1/\delta)}{\varepsilon^2}
\right)
$$

增长；教材给出相应显式常数 construction。这里先学习 proof architecture，VC-rich class 的正式上下界在下一卷闭环。

## 十五、上界与下界的 gap 怎么读

若上界为 $U$、下界为 $L$：

1. 若同阶，只差 universal constants：rate 基本 sharp；
2. 若差一个 $\log m$：可能是 covering/union proof 松，也可能 construction 不够强；
3. 若对 dimension 的次数不同：通常存在重要理论缺口；
4. 若 upper 是 high probability、lower 是 expectation：不能直接宣布匹配；
5. 若 upper 与 lower 的 problem family/loss 不同：没有可比性。

“已知最好上界”和“信息论最优 rate”必须分栏记录。

## 十六、lower bound 的常见证明错误

### 16.1 只展示某算法失败

必须从“任意 $A$”开始，或用 testing theorem 已对所有 tests 取 infimum。

### 16.2 distributions 太容易区分

参数 separation 大但 KL 也巨大，$m$ 个样本可轻易识别，lower bound 变成零。

### 16.3 parameters 没有 separation

distributions 很接近，但对应最优 decisions 也几乎相同，识别失败不产生大 loss。

### 16.4 product KL 忘记乘 $m$

single-sample closeness 不代表无限样本仍难；iid information 线性积累。

### 16.5 expectation 与 probability 偷换

PAC lower bound 需 high-probability failure。expected risk lower bound 必须明确转换条件与损失。

### 16.6 construction 不在 theorem class 内

若 upper bound 假设 realizable、margin、bounded norm，lower-bound distributions 也必须满足同样条件才可比较。

## 十七、AI 场景中的 Minimax 视角

### 17.1 稀有安全事件

若危险行为概率为 $p\ll1$，未观测危险的概率约 $e^{-mp}$。要验证风险低于 $p$ 量级，本质上需要 $1/p$ 级 exposure；普通 accuracy benchmark 无法免费证明 rare-event safety。

### 17.2 近似相同的模型质量

两个 checkpoint 的真实得分只差 $\varepsilon$，每例评分噪声有常数量级时，可靠选择通常需要 $1/\varepsilon^2$ samples。重复训练 steps 不能替代独立 evaluation information。

### 17.3 大候选库

若候选确实形成许多统计可区分 directions，Fano 解释了 $\log M$ 成本；若模型高度相关，有效 packing number 可能远小于文件数。

### 17.4 distribution assumptions 的价值

minimax worst case 可能悲观。low noise、margin、smoothness、sparsity、causal invariance 或 pretrained prior 会缩小 $\mathcal P$，既可改善算法，也会改变 lower bound。任何快率都应标明它排除了哪些 hard instances。

## 十八、Minimax 不是唯一决策准则

minimax 保护最坏分布，适合安全基线与 assumption audit，但可能对现实 task prior 过度悲观。其他视角包括：

- Bayes risk：对明确 prior 平均；
- local minimax：只在某个 neighborhood 内最坏；
- instance-dependent bounds：难度依具体 gap/noise；
- adaptive minimax：未知 smoothness/sparsity 下接近各子类最优；
- distribution-dependent learning：允许 sample complexity 依 $P$。

它们不是推翻 minimax，而是改变 quantifiers 和 problem family。

## 十九、证明工作流

1. 写清 parameter/problem family $\mathcal P$；
2. 写清 loss 与 expected/high-probability target；
3. 决定 two-point、packing 还是 hypercube；
4. 验证 candidate distributions 全满足 upper-bound assumptions；
5. 计算 decision separation；
6. 计算 single-sample KL/TV/Hellinger；
7. 用 product rule进入 $m$ samples；
8. 构造 learner-output-to-test decoder；
9. 应用 Le Cam/Fano/Assouad；
10. 优化 separation 参数并与 upper bound 同口径比较。

## 二十、本节边界与来源说明

- Le Cam/Fano/Assouad 的统一方法定位来自 Yu 1997；
- finite-class、NFL 与 agnostic lower-bound 坐标由标准学习理论教材校准；
- 本节给出可重建的 two-point constants，但不把所有 class 的 sharp constant 宣称已解决；
- 下一卷用 VC/shattering 正式说明哪些 infinite/finite classes 足够 rich 以实现这些 worst-case lower rates。

## 二十一、掌握检查

- [ ] 我能区分 algorithm failure 与 minimax lower bound；
- [ ] 我能写出 expected risk、quantile 和 PAC sample complexity；
- [ ] 我能推导 Le Cam metric-risk inequality；
- [ ] 我能使用 KL product rule 与 Pinsker；
- [ ] 我能用 Bernoulli pair 得到 $1/\sqrt m$；
- [ ] 我能解释 $\log(1/\delta)/\varepsilon^2$ 的 testing 来源；
- [ ] 我能陈述 Fano 并解释 $\log N$；
- [ ] 我能说明 realizable rare-event 下界为何是 $1/\varepsilon$；
- [ ] 我能判断一个 finite class 是否真的支持 $\log M$ lower bound；
- [ ] 我能按相同 problem family、loss 与 probability mode 比较上下界。

## 二十二、进一步连接

- [[二分类统计学习基本定理]]：VC dimension 怎样同时控制 upper 和 lower sample complexity；
- [[互信息与信息论泛化界]]：information 在 Fano lower bound 与 generalization upper bound 中方向相反；
- [[局部 Rademacher 复杂度与快收敛率]]：缩小 local hard family 后何时获得快率；
- [[Bandit Feedback 与强化学习接口]]：feedback 变少、自适应采样后 testing constructions 如何改变。
