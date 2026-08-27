---
type: theorem
status: draft
area: [learning-theory/conformal-prediction, coverage, exchangeability]
aliases: [Split Conformal Prediction, Distribution-Free Prediction Sets, Exchangeable Rank Coverage]
node_id: LT-64
prerequisites: ["[[随机变量、分布与分位数]]", "[[联合分布、边缘分布与独立性]]", "[[训练集、验证集、测试集与自适应复用]]", "[[概率校准、Proper Scoring Rule 与可靠性图]]"]
related: ["[[Aleatoric、Epistemic 与模型不确定性]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[Covariate、Label 与 Concept Shift]]", "[[OOD、鲁棒性与因果不变性的边界]]"]
sources: ["[[S-2018-Lei-Conformal-Regression]]", "[[S-2019-Romano-CQR]]"]
exercises: ["[[习题 - Conformal Prediction 与有限样本 Coverage]]"]
solutions: ["[[解答 - Conformal Prediction 与有限样本 Coverage]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-conformal-rank-coverage-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Conformal Prediction 与有限样本 Coverage

> [!abstract] 本章主问题
> Conformal prediction 不要求基础模型正确，而是利用 calibration scores 与未来 score 的交换秩，构造有限样本 marginal coverage。保证的核心不是“Bayesian uncertainty”或“区间看起来合理”，而是 untouched calibration set、固定 score、正确分位数舍入与 exchangeability。

## 一、学习目标

完成本章后，应能：

1. 区分 point predictor、predictive distribution、prediction interval/set；
2. 写出 split conformal 的训练、校准与预测算法；
3. 推导 $\lceil(m+1)(1-\alpha)\rceil$ 分位数索引；
4. 用 exchangeable rank 证明有限样本 marginal coverage；
5. 正确处理 ties、随机化与 $k=m+1$；
6. 构造 residual conformal regression interval；
7. 推导 conformalized quantile regression score；
8. 构造 classification threshold/APS prediction set；
9. 区分 marginal、conditional、group 与 simultaneous coverage；
10. 识别 calibration reuse、shift、dependence 与 efficiency 边界。

## 二、Prediction Set 的对象

给定训练数据 $D$，算法输出集合值函数

$$
\mathcal C_D:\mathcal X\to2^{\mathcal Y}.
$$

对新样本 $(X_{n+1},Y_{n+1})$，coverage 事件是

$$
Y_{n+1}\in\mathcal C_D(X_{n+1}).
$$

分类时集合包含多个 labels；回归时常是区间，也可以是不连通集合。coverage 只说明真值进入集合的频率，不说明集合短、小、有用或语义安全。

## 三、Split Conformal 的三份数据

把数据分为：

1. proper training set $D_{\rm tr}$；
2. calibration set $D_{\rm cal}=\{(X_i,Y_i)\}_{i=1}^m$；
3. future/test pair $(X_{m+1},Y_{m+1})$。

用 $D_{\rm tr}$ 拟合模型和 nonconformity score：

$$
s_{D_{\rm tr}}(x,y)\in\mathbb R.
$$

score 越大表示候选 $(x,y)$ 越不符合训练所得规律。校准时计算

$$
S_i=s_{D_{\rm tr}}(X_i,Y_i),
\qquad i=1,\ldots,m.
$$

## 四、有限样本分位数

目标 miscoverage $\alpha\in(0,1)$。令

$$
\boxed{
k=\left\lceil(m+1)(1-\alpha)\right\rceil.
}
$$

把 calibration scores 排序：

$$
S_{(1)}\le\cdots\le S_{(m)}.
$$

定义

$$
\widehat q=
\begin{cases}
S_{(k)},&k\le m,\\
+\infty,&k=m+1.
\end{cases}
$$

预测集合：

$$
\boxed{
\mathcal C(x)
=\{y:s_{D_{\rm tr}}(x,y)\le\widehat q\}.
}
$$

常见错误是直接取 calibration empirical $(1-\alpha)$ quantile，忘记 $m+1$ 与 ceiling；这会在小样本下 under-cover。

## 五、为什么是 $m+1$

未来真值 score：

$$
S_{m+1}
=s_{D_{\rm tr}}(X_{m+1},Y_{m+1}).
$$

在给定 $D_{\rm tr}$ 后，若 calibration pairs 与 future pair exchangeable，且 score function 已固定，则

$$
(S_1,\ldots,S_m,S_{m+1})
$$

也 exchangeable。未来 score 是总共 $m+1$ 个位置中的一个，因此其秩要相对于 $m+1$ 计算。

## 六、有限样本 Coverage 定理

> [!theorem] Split Conformal Marginal Coverage
> 若 calibration pairs 与 future pair 在给定 proper training data 后 exchangeable，且 $s_{D_{\rm tr}}$ 不使用 calibration labels 自适应重拟合，则上述集合满足
> $$
> \Pr\{Y_{m+1}\in\mathcal C(X_{m+1})\}
> \ge1-\alpha.
> $$

### 6.1 无 ties 时的证明

无 ties 时，$S_{m+1}$ 在 $m+1$ 个 scores 中的 rank

$$
R_{m+1}\in\{1,\ldots,m+1\}
$$

均匀：

$$
\Pr(R_{m+1}=r)=\frac1{m+1}.
$$

若 $R_{m+1}\le k$，则未来 score 不大于合并样本的第 $k$ 个 score，也等价于不超过 calibration threshold 的保守版本。因此

$$
\Pr(S_{m+1}\le\widehat q)
\ge
\Pr(R_{m+1}\le k)
=\frac{k}{m+1}
\ge1-\alpha.
$$

又因为

$$
S_{m+1}\le\widehat q
\Longleftrightarrow
Y_{m+1}\in\mathcal C(X_{m+1}),
$$

结论成立。

### 6.2 有 ties 时

若 ties 按“$\le$ threshold”保守纳入，coverage 仍至少为目标值，通常略大。若要更接近 exact finite-sample level，可对 ties 加独立随机数做 randomized rank；随机化规则必须预先声明。

## 七、一个手算例子

设 calibration size $m=9$，目标 coverage $1-\alpha=0.8$。则

$$
k=\lceil10\times0.8\rceil=8.
$$

若排序后的 residual scores 为

$$
0.1,0.2,0.2,0.4,0.5,0.7,0.8,1.0,1.6,
$$

则

$$
\widehat q=S_{(8)}=1.0.
$$

不能取第 $\lceil9\times0.8\rceil=8$ 只是巧合；例如 $m=19,\alpha=0.1$ 时正确索引为 $\lceil20\times0.9\rceil=18$，小样本舍入必须由 $m+1$ 公式统一处理。

## 八、Absolute-Residual Conformal Regression

先在 $D_{\rm tr}$ 上拟合 point predictor $\widehat f$。定义

$$
S_i=|Y_i-\widehat f(X_i)|.
$$

则

$$
\boxed{
\mathcal C(x)
=
[\widehat f(x)-\widehat q,\ 
\widehat f(x)+\widehat q].
}
$$

基础模型越准确，calibration residuals 通常越小，区间越窄；但 coverage 的 rank argument 不要求 $\widehat f$ 是真实条件均值。

### 8.1 局限：固定宽度

同一个 $\widehat q$ 加到所有 $x$，难以适应 heteroscedasticity。可设计 normalized score：

$$
S_i=
\frac{|Y_i-\widehat f(X_i)|}
{\widehat\sigma(X_i)+\varepsilon},
$$

预测区间半宽为 $\widehat q(\widehat\sigma(x)+\varepsilon)$。coverage 仍取决于 score 固定和 exchangeability；$\widehat\sigma$ 的质量主要影响 efficiency。

## 九、Conformalized Quantile Regression

在 proper training set 上拟合 lower/upper quantiles：

$$
\widehat q_{\rm lo}(x),
\qquad
\widehat q_{\rm hi}(x).
$$

calibration score：

$$
\boxed{
S_i=
\max\{
\widehat q_{\rm lo}(X_i)-Y_i,\ 
Y_i-\widehat q_{\rm hi}(X_i)
\}.
}
$$

取 conformal threshold $\widehat q$ 后：

$$
\boxed{
\mathcal C_{\rm CQR}(x)
=
[
\widehat q_{\rm lo}(x)-\widehat q,\ 
\widehat q_{\rm hi}(x)+\widehat q
].
}
$$

score 可为负，表示标签落在初始区间内部；有限样本 quantile 甚至可能导致整体收缩。CQR 的 input-adaptive shape 来自 quantile model，finite-sample marginal validity 来自 calibration ranks，两条证据必须分开。

## 十、Classification Conformal Set

若基础分类器输出 $\widehat p_k(x)$，最简单 score：

$$
s(x,y)=1-\widehat p_y(x).
$$

则集合：

$$
\mathcal C(x)
=
\{k:1-\widehat p_k(x)\le\widehat q\}
=
\{k:\widehat p_k(x)\ge1-\widehat q\}.
$$

它可能：

- 只含一个类；
- 含多个类；
- 极端情况下为空或含全部类。

基础概率无需完美校准，但好的 ranking/sharpness 通常使集合更小。

## 十一、Adaptive Prediction Sets 的直觉

对类别按概率降序

$$
\widehat p_{(1)}(x)\ge\cdots\ge\widehat p_{(K)}(x),
$$

定义 true label 所在位置前的累计概率或含 true label 的累计质量作为 score。预测时纳入高概率类别，直到累计 score 达到 conformal threshold。

这允许在容易输入上输出小集合、困难输入上输出大集合。ties、随机化、label ordering 与 regularization 必须进入协议。

## 十二、Marginal Coverage 的量词

split conformal 典型结论：

$$
\boxed{
\Pr_{D_{\rm cal},(X_{m+1},Y_{m+1})}
\left\{
Y_{m+1}\in\mathcal C(X_{m+1})
\right\}
\ge1-\alpha.
}
$$

它不是：

$$
\Pr\{Y_{m+1}\in\mathcal C(x)\mid X_{m+1}=x\}
\ge1-\alpha
\quad\text{对所有 }x.
$$

总体覆盖可以由容易区域 over-cover、困难/少数区域 under-cover 平均得到。对所有分布同时要求非平凡 exact conditional coverage 通常不可得。

## 十三、Group、Classwise 与 Simultaneous Coverage

- group coverage：对预先定义群组 $G=g(X)$ 分别校准；
- class-conditional coverage：对 $Y=k$ 条件化，但每类需足够 calibration data；
- simultaneous coverage：多个未来点或整个轨迹同时进入集合，需控制 joint event；
- average coverage：只控制每点边际频率。

每增加条件层，样本量和集合大小成本都会上升。不能把 marginal 95% 区间称为“95% 的所有未来轨迹都安全”。

## 十四、Exchangeability 不是简单的 i.i.d. 口号

exchangeability 要求联合分布对置换不变。i.i.d. 蕴含 exchangeability，但某些 mixture/exchangeable data 不是条件外独立。

常见破坏：

- 时间趋势与概念漂移；
- 同一患者/用户多条记录跨 split；
- spatial correlation；
- active/adaptive data collection；
- calibration 与 deployment selection mechanism 不同；
- feedback loop 改变 future labels。

应以 patient、session、site、time block 等真实 exchangeable unit 划分，而不是把相关 observations 当独立样本。

## 十五、Calibration Set 不能随意复用

保证要求 score function 和选择规则相对于 calibration pairs 固定。危险做法：

1. 用 calibration labels 反复调基础模型；
2. 试很多 scores，挑 coverage/length 最好者；
3. 根据同一 calibration set 选择 subgroup partition；
4. 看 deployment failures 后回头改 score，却沿用旧保证；
5. 把 test set 并入 calibration 后仍报告独立测试。

若需要 selection，可增加 tuning split、做 nested protocol，或使用有相应理论的 adaptive conformal 方法；不能沿用基础 split-conformal 定理名称掩盖复用。

## 十六、Coverage 与 Efficiency

coverage 可以通过输出

$$
\mathcal C(x)=\mathcal Y
$$

轻易达到，因此必须同时报告：

- regression interval length/quantiles；
- classification set size；
- empty/full-set rate；
- subgroup length/set size；
- conditional error pattern；
- risk–coverage 或 utility；
- compute 与 latency。

基础模型不需要正确来保证 marginal validity，但更好的 score 排序和局部尺度通常提高 efficiency。

## 十七、Distribution Shift 下的断裂

若 calibration 来自 $P_s$，future 来自 $P_t$，合并 scores 一般不 exchangeable。于是原 rank proof 的第一步失效。

covariate shift、label shift、concept shift、selection bias 与 temporal drift 需要不同修正或重新校准。任何 weighted/online conformal 扩展都必须声明额外假设；不能说“distribution-free”就忽略 distribution relation。

## 十八、图：保证来自交换秩

先看图回答：为什么一个极差的 point predictor 仍可获得 conformal marginal coverage，却可能给出毫无实用价值的宽区间？

![[00-知识库管理/_assets/figures/learning-theory/fig-conformal-rank-coverage-v2.svg|900]]

> [!figure] 图 20.8-04　Split conformal 的 rank proof、应用形态与保证边界
> 左栏展示 proper train、calibration scores、future rank 与 finite quantile；中栏比较 residual、normalized、CQR 与 classification set；右栏区分 marginal/conditional/group coverage、exchangeability、reuse、shift 与 efficiency。来源：依据 Lei et al. 与 Romano–Patterson–Candès 独立绘制；确定性 SVG，由 [[plot_calibration_uncertainty_v2.py]] 生成。

**怎样读图**：先沿左栏检查 score 在 calibration 前是否固定，再用 $m+1$ 秩计算 threshold；中栏只改变集合形状，右栏规定最终 claim 的量词和失败条件。

**图没有证明什么**：图没有证明逐点 conditional coverage、分布偏移鲁棒性或集合效率；这些都需要额外结构、数据或假设。

## 十九、AI 接口

### 19.1 LLM 回答集合与拒答

标签空间若是有限候选答案，可对 answer scores conformalize；开放生成的语义等价类、不可枚举输出和 evaluator shift 需要额外定义，不能直接套分类集合。

### 19.2 医疗区间

按患者单位划分，避免同一患者记录跨 calibration/test。除总体 coverage 外必须报告医院、年龄、病种群组 coverage 与 interval length。

### 19.3 视觉检测与分割

多个 boxes/pixels 产生结构化、多重预测。per-box marginal coverage 不等于整张图 simultaneous coverage；matching 与 missing-object score 属于对象定义。

### 19.4 时间序列与控制

rolling/online 数据通常不 exchangeable。单步 marginal intervals 也不等于整条 trajectory safety tube；需使用序列依赖假设和控制层安全约束。

## 二十、常见错误

1. 忘记 $m+1$ 与 ceiling；
2. 用训练 residuals 代替 untouched calibration residuals；
3. 把 marginal 写成 conditional；
4. 把 distribution-free 写成 shift-free；
5. 不声明 exchangeable unit；
6. 只报 coverage，不报宽度/集合大小；
7. 用 calibration data 选 score 后仍套原定理；
8. 把 Bayesian credible interval 与 conformal interval 混称；
9. 忽略 ties、空集合和全集合；
10. 从单点 coverage 外推 simultaneous trajectory safety。

## 二十一、最小记忆

> [!summary]
> - split conformal 的核心是 fixed score + untouched calibration + exchangeable rank；
> - threshold index 是 $\lceil(m+1)(1-\alpha)\rceil$；
> - 保证是有限样本 marginal coverage；
> - 基础模型质量主要影响 efficiency，不是 rank validity；
> - conditional/group/simultaneous coverage 是不同量词；
> - reuse、dependence 与 shift 会破坏原证明。

## 二十二、掌握标准

### A. 定义

能写 score、calibration quantile、prediction set 与 marginal coverage event。

### B. 推导

能从 exchangeable rank 完整证明 split-conformal coverage，并手算小样本索引。

### C. 反例

能构造 marginal coverage 合格但 subgroup under-coverage、shift 后失效及 coverage 高但集合无用的例子。

### D. 实验

能比较 residual、normalized 与 CQR intervals，报告 coverage–length、群组与 shift curves。

### E. 迁移

能在 LLM、医疗、视觉或序列系统中选择真实 exchangeable unit，并限制 claim 到相应量词。

## 二十三、练习与独立详解

- [[习题 - Conformal Prediction 与有限样本 Coverage]]
- [[解答 - Conformal Prediction 与有限样本 Coverage]]

## 参考来源

- [[S-2018-Lei-Conformal-Regression]]
- [[S-2019-Romano-CQR]]
