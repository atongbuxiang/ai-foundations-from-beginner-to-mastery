---
type: concept
status: draft
area: [learning-theory/pac, machine-learning/erm, probability/concentration]
aliases: [Agnostic PAC, Finite-Class Agnostic ERM, Noisy ERM Guarantee]
node_id: LT-13
prerequisites: ["[[有限假设类、Union Bound 与一致收敛]]", "[[可实现情形的一致 ERM 保证]]", "[[PAC 学习定义与样本复杂度]]", "[[经验风险最小化、近似 ERM 与超额风险分解]]"]
related: ["[[Occam 界、编码长度与先验权重]]", "[[样本复杂度下界与 Minimax 视角]]", "[[VC 一致收敛与泛化界]]", "[[收缩引理与 Lipschitz 损失复合]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1963-Hoeffding-Bounded-Random-Variables]]", "[[S-2020-Su-7466-泛化性乱弹]]"]
exercises: ["[[习题 - 不可知 PAC、ERM 与双侧一致收敛]]"]
solutions: ["[[解答 - 不可知 PAC、ERM 与双侧一致收敛]]"]
created: 2026-08-20
updated: 2026-08-23
---

# 不可知 PAC、ERM 与双侧一致收敛

> [!abstract] 本章主问题
> 对任意有限假设类 $|\mathcal H|=M$、iid 样本和 $[0,1]$ 有界损失，即使不存在零风险假设，exact ERM 仍以至少 $1-\delta$ 的概率满足
> $$
> R_P(\widehat h_S)-R_{\mathcal H}^*
> \le2\sqrt{\frac{\log(2M/\delta)}{2m}}.
> $$
> 因而 $m\ge2\log(2M/\delta)/\varepsilon^2$ 足以获得 class excess 至多 $\varepsilon$。与 realizable 的 $1/\varepsilon$ 不同，这里必须区分两个非零且可能非常接近的风险，均值估计噪声使 $1/\varepsilon^2$ 成为一般不可知问题的典型尺度。

> [!question] 初学者读完必须能回答
> 1. 为什么不可知情形不能继续使用零错生存事件？
> 2. Uniform event 为什么要同时覆盖 $\widehat h_S$ 与 $h_{\mathcal H}^*$？
> 3. $R_P(\widehat h_S)\le R_P(h_{\mathcal H}^*)+2\alpha$ 的三步桥怎样逐行推出？
> 4. Approximate ERM 的容差 $\rho$ 加在桥的哪一步？
> 5. $1/\varepsilon^2$、class excess 与 approximation error 应怎样分别解释？

先用下图回答一个视觉问题：**在没有零风险假设时，ERM 怎样通过两次经验—总体转换与一次经验比较获得 class excess 保证？**

![[00-知识库管理/_assets/figures/learning-theory/fig-agnostic-erm-two-gap-bridge-v2.svg|880]]

> [!figure] 图 20.2.5｜不可知有限类 ERM 的双侧比较桥
> A 构造同时覆盖 ERM 输出与类内总体 oracle 的 uniform event；B 逐行展示总体输出、经验输出、经验 comparator、总体 comparator 四个量之间的三步不等式；C 给出 $2\alpha$ excess 与 $1/\varepsilon^2$ 样本尺度，并标出 approximate ERM 与 unbounded loss 的接口。来源：独立绘制；理论接口参考 finite-class agnostic ERM theorem；生成脚本：[[plot_pac_finite_class_v2.py]]；确定性证明地图，无随机种子。

**怎样读图。** A 先把共同事件固定下来；B 第一箭头为输出预测器花费一个 $alpha$，中间箭头使用 ERM 定义，最后箭头让总体 oracle 再花一个 $alpha$。把四行首尾相减便得到 class excess；若只做到 $\rho$-approximate ERM，则中间不等式额外支付 $\rho$。

**适用边界（图没有证明什么）。** 图给的是有限、预先固定类和 $[0,1]$ 有界 loss 下的充分上界，不证明常数或 rate 对所有结构都最优。它不含 approximation、deployment shift 或计算误差之外的算法偏差；无界 surrogate、依赖样本、数据依赖类、nonattained infimum 和非 ERM learner 都需另行处理。

## 一、学习目标

1. 写出 finite-class agnostic ERM theorem 的完整条件与常数；
2. 从 uniform convergence 逐行推出 $2\alpha$ excess bridge；
3. 反解 $2\log(2M/\delta)/\varepsilon^2$ 样本复杂度；
4. 推导 $\rho$-approximate ERM 的 $2\alpha+\rho$ 保证；
5. 用 pairwise loss difference 给出另一条 exact ERM 证明；
6. 解释 realizable $1/\varepsilon$ 与 agnostic $1/\varepsilon^2$ 的机制差异；
7. 区分 uniform estimation theorem 与 ERM-specific theorem；
8. 处理 randomized tie-breaking 与类内 infimum；
9. 识别无界 surrogate、数据依赖 class 与 distribution shift 的断点；
10. 把定理用于有限 checkpoint/prompt/rule 选择而不夸大其范围。

## 二、问题设置

固定：

- 数据空间 $\mathcal Z$ 与未知分布 $P$；
- 有限假设类 $\mathcal H=\{h_1,\ldots,h_M\}$；
- 损失 $\ell:\mathcal H\times\mathcal Z\to[0,1]$；
- iid 样本 $S=(Z_1,\ldots,Z_m)\sim P^m$。

总体风险与经验风险：

$$
R_P(h)=\mathbb E_{Z\sim P}\ell(h,Z),
\qquad
R_S(h)=\frac1m\sum_{i=1}^m\ell(h,Z_i).
$$

因为 $\mathcal H$ 有限，类内最优必能取到：

$$
h_{\mathcal H}^*
\in\arg\min_{h\in\mathcal H}R_P(h),
\qquad
R_{\mathcal H}^*=R_P(h_{\mathcal H}^*).
$$

exact ERM 为

$$
\widehat h_S
\in\arg\min_{h\in\mathcal H}R_S(h).
$$

本节**不假设** $R_{\mathcal H}^*=0$。标签可有噪声、特征可不足、class 可 misspecified；目标只是与类内最佳预测器竞争。

## 三、为什么 LT-12 的证明不能继续用

LT-12 的关键事件是

$$
R_S(h)=0.
$$

realizability 保证真实 $h^*$ 的训练错误为零，所以 ERM 输出必在版本空间中。若 $R_{\mathcal H}^*>0$：

1. 最优假设也会在训练集上出错；
2. 版本空间可能为空；
3. ERM 要比较多个非零 empirical risks；
4. 一个较差假设不必“连续 $m$ 次零错”，只需因 sampling noise 暂时看起来不差。

因此概率机制从

$$
(1-p)^m\le e^{-mp}
$$

变为一般均值差的 concentration：

$$
e^{-cm\varepsilon^2}.
$$

## 四、uniform event

LT-11 已证明：令

$$
\alpha_m(M,\delta)
=\sqrt{\frac{\log(2M/\delta)}{2m}},
$$

则以至少 $1-\delta$ 的概率发生

$$
G=\left\{
\forall h\in\mathcal H:
|R_S(h)-R_P(h)|\le\alpha_m
\right\}.
$$

在 $G$ 上，两个方向同时成立：

$$
R_P(h)\le R_S(h)+\alpha_m,
$$

$$
R_S(h)\le R_P(h)+\alpha_m.
$$

第一条用于 learner output，第二条用于 population comparator。

## 五、exact ERM theorem 的逐行证明

在共同事件 $G$ 上：

$$
\begin{aligned}
R_P(\widehat h_S)
&\le R_S(\widehat h_S)+\alpha_m
&&\text{uniform deviation at }\widehat h_S\\
&\le R_S(h_{\mathcal H}^*)+\alpha_m
&&\text{ERM optimality}\\
&\le R_P(h_{\mathcal H}^*)+2\alpha_m
&&\text{uniform deviation at }h_{\mathcal H}^*.
\end{aligned}
$$

所以

$$
\boxed{
R_P(\widehat h_S)-R_{\mathcal H}^*
\le2\alpha_m
=2\sqrt{\frac{\log(2M/\delta)}{2m}}.
}
$$

该不等式以至少 $1-\delta$ 的概率成立。

> [!important] data-dependent output 在这里合法
> 我们没有对 $\widehat h_S$ 直接套 fixed-$h$ Hoeffding。先通过 Union Bound 建立对全部 $h$ 同时成立的 $G$，随后才在 $G$ 内代入 ERM output。

## 六、样本复杂度反解

希望 class excess 不超过 $\varepsilon$，要求

$$
2\sqrt{\frac{\log(2M/\delta)}{2m}}
\le\varepsilon.
$$

两边除以 2 并平方：

$$
\frac{\log(2M/\delta)}{2m}
\le\frac{\varepsilon^2}{4}.
$$

整理：

$$
\boxed{
m\ge
\frac{2\log(2M/\delta)}{\varepsilon^2}.
}
$$

因此 finite class agnostic ERM 的一个显式充分上界是

$$
\boxed{
m_{\mathcal H}^{\rm ag}(\varepsilon,\delta)
\le
\left\lceil
\frac{2\log(2|\mathcal H|/\delta)}{\varepsilon^2}
\right\rceil.
}
$$

大 $O$ 形式：

$$
O\!\left(
\frac{\log M+\log(1/\delta)}{\varepsilon^2}
\right).
$$

## 七、$\rho$-approximate ERM

若实际输出 $\widetilde h_S$ 满足

$$
R_S(\widetilde h_S)
\le\inf_{h\in\mathcal H}R_S(h)+\rho,
$$

则同样在 $G$ 上：

$$
\begin{aligned}
R_P(\widetilde h_S)
&\le R_S(\widetilde h_S)+\alpha_m\\
&\le R_S(h_{\mathcal H}^*)+\rho+\alpha_m\\
&\le R_P(h_{\mathcal H}^*)+2\alpha_m+\rho.
\end{aligned}
$$

故

$$
\boxed{
R_P(\widetilde h_S)-R_{\mathcal H}^*
\le2\sqrt{\frac{\log(2M/\delta)}{2m}}+\rho.
}
$$

若目标总 excess 为 $\varepsilon$ 且 $0\le\rho<\varepsilon$，充分条件为

$$
2\alpha_m\le\varepsilon-\rho,
$$

即

$$
\boxed{
m\ge
\frac{2\log(2M/\delta)}{(\varepsilon-\rho)^2}.
}
$$

> [!warning] optimization tolerance 必须与统计目标同尺度
> 固定一个不随 $m$ 下降的 $\rho$，会形成 excess-risk floor。样本再多也无法由此 theorem 保证低于 $\rho$。

## 八、另一条证明：直接比较 loss differences

uniform convergence 控制整个 class 的绝对 gap，是强而通用的事件。若只想证明 exact ERM 好，可以直接比较每个坏假设与 $h_{\mathcal H}^*$。

对固定 $h$ 定义

$$
W_i
=\ell(h,Z_i)-\ell(h_{\mathcal H}^*,Z_i).
$$

因为两个 loss 均在 $[0,1]$：

$$
W_i\in[-1,1].
$$

其期望是 risk gap：

$$
\mathbb EW_i
=R_P(h)-R_P(h_{\mathcal H}^*)
=:\Delta_h.
$$

若 $h$ 是 $\varepsilon$-坏假设，即 $\Delta_h>\varepsilon$，但 empirical risk 不高于 oracle：

$$
R_S(h)\le R_S(h_{\mathcal H}^*),
$$

则

$$
\frac1m\sum_iW_i\le0,
$$

也就是 sample mean 从正期望 $\Delta_h$ 向下偏移至少 $\Delta_h$。Hoeffding 对区间宽度 2 给出

$$
\Pr\left(R_S(h)\le R_S(h_{\mathcal H}^*)\right)
\le e^{-m\Delta_h^2/2}
\le e^{-m\varepsilon^2/2}.
$$

若 ERM 输出是坏假设，就必有某个坏 $h$ empirical risk 不高于 oracle。因此

$$
\Pr\left(
R_P(\widehat h_S)>R_{\mathcal H}^*+\varepsilon
\right)
\le M e^{-m\varepsilon^2/2}.
$$

令右端不超过 $\delta$：

$$
m\ge\frac{2\log(M/\delta)}{\varepsilon^2}.
$$

它比双侧 uniform route 少一个不重要的因子 2 inside log，但只服务于 ERM comparison，不提供所有 $h$ 的误差条。

## 九、两条证明回答不同问题

| 路线 | 共同事件 | 可控制对象 | 优点 | 局限 |
|---|---|---|---|---|
| 双侧 uniform | 所有 $h$ 的 risk estimates 都准 | 任意 data-dependent choice、approximate ERM | 模块化、可复用 | 可能比任务需要更强 |
| pairwise ERM | 坏 $h$ 不会 empirical beat oracle | exact ERM output | 常数略紧、机制直接 | comparator/ERM-specific |

理论工作中不要只问哪个式子更短，要问后续算法真正需要哪种 event。

## 十、为什么一般是 $1/\varepsilon^2$

考虑两个假设，真实 risks 分别为

$$
r
\quad\text{与}\quad
r+\varepsilon.
$$

经验 risk 的标准波动量级为 $1/\sqrt m$。要可靠分辨间隔 $\varepsilon$，需要

$$
\frac1{\sqrt m}\ll\varepsilon,
$$

即

$$
m\gg\frac1{\varepsilon^2}.
$$

LT-12 的 $1/\varepsilon$ 利用了零 empirical error 这一端点事件；噪声使我们回到一般均值比较。LT-16 将用 two-point testing 说明 $1/\varepsilon^2$ 不只是 Hoeffding proof artifact。

## 十一、一个数值例子

设

$$
M=10^4,
\qquad
\varepsilon=0.05,
\qquad
\delta=0.05.
$$

uniform route 要求

$$
m\ge
\frac{2\log(2\cdot10^4/0.05)}{0.05^2}
=\frac{2\log400000}{0.0025}
\approx10319.4.
$$

所以取 $m=10320$ 是一个充分值。它可能很保守，因为：

- Hoeffding 忽略 variance；
- Union Bound 忽略候选相关性；
- theorem 做 distribution-free worst-case；
- 所有候选被统一按同等复杂度处理。

“保守”不等于“错误”；它表示 theorem 用很少的分布结构换取统一有效性。

## 十二、randomized learner 与 tie-breaking

若多个 hypotheses empirical risk 相同，算法可用随机种子 $U$ tie-break。uniform event $G$ 对所有 $h$ 同时成立，所以在 $G$ 上每个 ERM minimizer 都满足同一 $2\alpha_m$ 保证。于是

$$
\Pr_{S,U}(\text{failure})
\le\Pr_S(G^c)
\le\delta.
$$

这里算法随机性没有额外代价，因为 $G$ 已覆盖所有可能输出。若算法可能输出非 ERM 元素，则必须用 approximate gap 或直接分析算法。

## 十三、与 surrogate loss 的接口

对 bounded surrogate $\ell_{\rm sur}\in[0,1]$，theorem 控制的是 surrogate class excess：

$$
R_P^{\rm sur}(h_S)
-\inf_{h\in\mathcal H}R_P^{\rm sur}(h).
$$

要推出 0–1 excess，还需要 calibration/reduction 函数，例如

$$
\psi\left(
R_{01}(h)-R_{01}^*
\right)
\le
R_{\rm sur}(h)-R_{\rm sur}^*.
$$

若 log loss 无界，则 $[0,1]$ Hoeffding 条件也不成立；需要 clipping、tail assumptions 或其他 empirical-process 工具。

## 十四、AI 模型选择中的正确读法

### 14.1 固定 checkpoint 库

若 $M$ 个模型在 validation sample 抽取前冻结，可用本 theorem 说明 validation ERM 所选模型接近库中 population-best model。comparator 是库内最佳，不是所有可能神经网络或 Bayes predictor。

### 14.2 prompt 搜索

预先固定 prompt library 可视为有限 $\mathcal H$。根据同一 validation feedback 继续生成 prompts 时，class 已 data-dependent，不能只数最终 prompts；需 sample splitting 或 adaptive-analysis 记账。

### 14.3 noisy judge

只要每个 evaluated example 的 bounded loss 是 iid draw 的一部分，judge stochasticity 可并入 $Z$；但 judge 的系统 bias 会改变目标 $P$ 与 loss，不会因 concentration 自动消失。

### 14.4 多个 seeds

若 seed 在训练前产生不同冻结 predictor，每个 seed-model pair 都是候选，$M$ 应覆盖真实选择 family。若部署时每次重新随机输出，则 hypothesis 应定义为 randomized prediction rule，并相应定义 risk。

## 十五、定理不覆盖什么

1. 无界或重尾 loss；
2. dependent/adaptive samples；
3. train 与 deployment distribution 不同；
4. evaluation sample 参与候选生成；
5. infinite real-parameter class 直接令 $M$ 为参数个数；
6. 从 surrogate excess 自动跳到 task excess；
7. 从 class-relative guarantee 跳到 Bayes optimality；
8. 从统计 sample efficiency 跳到 ERM computational efficiency。

## 十六、常见误解

> [!failure] “agnostic 表示不作任何假设”
> 错。仍假设 class、loss、iid、有界性与同分布评价；只是不要求 class 中存在零风险 predictor。

> [!failure] “训练误差不是零，所以没有泛化理论”
> 错。agnostic theory 比较非零 risks，目标是 class excess。

> [!failure] “$1/\varepsilon^2$ 说明 ERM 一定低效”
> 它是 worst-case sample scaling，不是计算 runtime，也不否认 margin/low-noise/localization 下的快率。

> [!failure] “双侧 uniform convergence 是唯一证明方法”
> 错。pairwise comparison、stability、PAC-Bayes 等可建立不同保证。

> [!failure] “bound 大于 1，所以 theorem 完全无用”
> 数值 certificate 可能 vacuous，但证明仍揭示依赖关系；应继续寻找更贴合结构的 complexity，而非把数学有效性和实用紧致性混为一谈。

## 十七、证明模板

1. 固定 finite $\mathcal H$、bounded loss 与 iid protocol；
2. 定义 $h_{\mathcal H}^*$ 和 exact/approximate ERM；
3. 用 Hoeffding + Union 建立 all-$h$ event；
4. population output $\to$ empirical output；
5. 使用 ERM/approximate ERM inequality；
6. empirical oracle $\to$ population oracle；
7. 得 $2\alpha+\rho$；
8. 令它不超过目标 $\varepsilon$ 并反解；
9. 检查 comparator、loss scale 和 candidate-generation protocol；
10. 若只需 exact ERM，可比较 pairwise loss differences。

## 十八、本节边界与来源说明

- 显式 finite-class agnostic ERM 常数以标准教材 Corollary 4.6 为准；
- concentration 输入来自 Hoeffding；
- 科学空间《泛化性乱弹》只用于讨论深度模型机制和经典 worst-case bound 的解释边界，不承担本 theorem 的形式证明。

## 十九、掌握检查

- [ ] 我能完整推导 $2\alpha$ bridge；
- [ ] 我能反解 $2\log(2M/\delta)/\varepsilon^2$；
- [ ] 我能处理 $\rho$-approximate ERM；
- [ ] 我能重建 pairwise-difference 证明；
- [ ] 我能解释 $1/\varepsilon$ 与 $1/\varepsilon^2$ 的机制差异；
- [ ] 我能区分 uniform theorem 与 ERM-specific theorem；
- [ ] 我能判断 prompt/checkpoint 候选是否预先固定；
- [ ] 我能指出 surrogate、unbounded loss 与 distribution shift 的缺口。

## 二十、进一步连接

- [[Occam 界、编码长度与先验权重]]：不再给所有候选同样 penalty，而按 prior/code 分配失败预算；
- [[样本复杂度下界与 Minimax 视角]]：证明 $1/\varepsilon^2$ 在一般 noisy problem 中不可随意改善；
- [[VC 一致收敛与泛化界]]：用 growth function 处理无限二分类类；
- [[局部 Rademacher 复杂度与快收敛率]]：何种 curvature/noise/localization 条件可超越全局慢率。
