---
type: theorem
status: draft
area: [learning-theory/covariate-shift, importance-weighting, density-ratio]
aliases: [Importance-Weighted ERM, Density Ratio Estimation, Sample Selection Correction]
node_id: LT-66
prerequisites: ["[[Covariate、Label 与 Concept Shift]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[经验风险最小化、近似 ERM 与超额风险分解]]"]
related: ["[[Domain Adaptation 与 Domain Generalization Bound]]", "[[训练集、验证集、测试集与自适应复用]]"]
sources: ["[[S-2000-Shimodaira-Covariate-Shift]]", "[[S-2007-Huang-KMM]]", "[[S-2010-Cortes-Importance-Weighting]]", "[[S-2009-Quinonero-Dataset-Shift]]"]
exercises: ["[[习题 - 重要性加权与 Covariate Shift 校正]]"]
solutions: ["[[解答 - 重要性加权与 Covariate Shift 校正]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-importance-weighting-overlap-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 重要性加权与 Covariate Shift 校正

> [!abstract] 本章主问题
> 在 $P_s(Y\mid X)=P_t(Y\mid X)$ 与 target support 被 source 覆盖时，target risk 可精确写成 source weighted risk。这个等式解决期望对象转换，却不保证有限样本稳定：ratio 估计、大权重、clipping、self-normalization 与 model selection 都有独立误差。

## 一、学习目标

完成本章后，应能：

1. 推导 covariate-shift change-of-measure identity；
2. 解释 conditional stability 与 absolute continuity；
3. 区分 true、estimated、clipped 与 self-normalized weights；
4. 推导 weighted estimator 的方差和 effective sample size；
5. 定量说明 clipping bias–variance；
6. 从 domain classifier 概率恢复 density ratio；
7. 解释 KMM 等 direct ratio/moment matching 的边界；
8. 设计 cross-fitting 与 weighted validation；
9. 判断 concept/label shift 下何时不可用；
10. 写 importance-weighting claim card。

## 二、Target Risk Identity

目标风险：

$$
R_t(f)=E_t[\ell(f(X),Y)].
$$

在 covariate shift 下

$$
p_t(y\mid x)=p_s(y\mid x),
$$

且 $P_t^X\ll P_s^X$。定义

$$
w(x)=\frac{p_t(x)}{p_s(x)}.
$$

则

$$
\boxed{
\begin{aligned}
R_t(f)
&=\int \ell(f(x),y)p_t(y\mid x)p_t(x)\,dxdy\\
&=\int \ell(f(x),y)w(x)p_s(y\mid x)p_s(x)\,dxdy\\
&=E_s[w(X)\ell(f(X),Y)].
\end{aligned}
}
$$

这不是近似；近似来自有限数据、ratio estimation 和假设失效。

## 三、Importance-Weighted ERM

若有 source labeled sample：

$$
\widehat R_w(f)
=\frac1n\sum_{i=1}^n
\widehat w(X_i)\ell(f(X_i),Y_i).
$$

用 true $w$ 且 $f$ 固定时，

$$
E_s[\widehat R_w(f)]=R_t(f).
$$

但对同一数据最小化 $\widehat R_w$ 还包含 weighted empirical-process 与 selection error；“risk estimator 无偏”不等于 learned model 无偏或低风险。

## 四、Overlap 与 Positivity

必要条件：

$$
p_t(x)>0\Rightarrow p_s(x)>0.
$$

强 overlap 常写为

$$
w(x)\le W_{\max}.
$$

若 target mass 位于 source 空洞，任何有限 weight 都无法创造缺失 labels。应收集 target labels、限制 target domain，或引入可验证结构外推。

## 五、Variance 与 Weight Tail

对固定 $f$，令 $Z=w(X)\ell(f(X),Y)$。iid source 下：

$$
\operatorname{Var}(\widehat R_w)
=\frac{\operatorname{Var}_s(Z)}{n}.
$$

即使 loss 有界，$w$ 的二阶矩很大也会导致高方差。常用诊断：

$$
\boxed{
n_{\rm eff}
=
\frac{(\sum_iw_i)^2}{\sum_iw_i^2}.
}
$$

均匀 weights 时 $n_{\rm eff}=n$；一个 weight 主导时接近 1。

## 六、Self-Normalization

归一化 estimator：

$$
\widehat R_{\rm SN}
=
\frac{\sum_iw_i\ell_i}{\sum_iw_i}.
$$

它对全局 weight scale 不敏感，常降低波动，但一般有限样本有偏，因为

$$
E\!\left[\frac{A}{B}\right]
\ne
\frac{EA}{EB}.
$$

其一致性需要 law of large numbers、有限矩和正确 weights；不能在报告中与无偏 Horvitz–Thompson 型 estimator 混称。

## 七、Clipping 的定量偏差

令

$$
w_c(x)=\min\{w(x),c\}.
$$

对 $0\le\ell\le L$：

$$
0\le
R_t(f)-E_s[w_c(X)\ell]
=E_s[(w-c)_+\ell]
\le L E_s[(w-c)_+].
$$

clipping 降低方差与单点支配，却引入对 weight tail 区域的系统低估。应画 $c$ 的 sensitivity curve，而不是隐藏 clip。

## 八、用 Domain Classifier 估 Ratio

混合 source/target inputs，令 $D=1$ 表示 target。若采样先验

$$
\Pr(D=1)=\rho,
$$

且

$$
r(x)=\Pr(D=1\mid X=x),
$$

由 Bayes：

$$
\boxed{
\frac{p_t(x)}{p_s(x)}
=
\frac{1-\rho}{\rho}
\frac{r(x)}{1-r(x)}.
}
$$

balanced domain sample 时 $\rho=1/2$，ratio 为 odds $r/(1-r)$。domain classifier 必须概率校准；接近 1 的 $r$ 产生巨大 weights。

## 九、Direct Ratio 与 KMM

不必分别估计两个高维 densities。KMM 选择 $\beta_i$ 使加权 source feature mean 接近 target：

$$
\left\|
\frac1n\sum_i\beta_i\phi(X_i)
-
\frac1m\sum_j\phi(X_j^t)
\right\|_{\mathcal H}^2
$$

尽量小，并约束 weights。它匹配所选 RKHS moments；有限 kernel、有限样本或 regularization 下，不等于完整 density ratio 精确恢复。

## 十、Weight Estimation Error

写

$$
\widehat w=w+\Delta.
$$

则 risk error 含

$$
E_s[\Delta(X)\ell(f(X),Y)].
$$

若同一 source labels 同时训练 ratio、模型并选超参，依赖会复杂化。可用 source/target inputs 的独立 folds 或 cross-fitting：每个样本的 weight 由未使用该样本训练的 ratio model 产生。

## 十一、Weighted Model Selection

训练加权但在 unweighted source validation 上选超参，会重新优化 source objective。应在独立 source validation 上估

$$
\widehat R_{t,\rm val}
=
\frac1{n_v}\sum_i
\widehat w(X_i^v)\ell_i^v,
$$

或使用有 labels 的 target-like validation。最终仍需 locked target test；ratio/kernel/clip threshold 本身也属于 selection space。

## 十二、何时不能用

- concept shift：$P_t(Y\mid X)\ne P_s(Y\mid X)$；
- support failure；
- label shift 若仅用 $p_t(x)/p_s(x)$，可能可形式转换但高维 ratio 非目标结构，class-prior weights更合适；
- feedback/policy shift 未记录行动；
- hidden confounding 使 observed $X$ 不足以满足 conditional stability。

## 十三、图：无偏公式与有限样本稳定性分账

先看图回答：为什么两个方法都精确估计 $E_s[w]=1$，target-risk estimator 的方差仍可差几个数量级？

![[00-知识库管理/_assets/figures/learning-theory/fig-importance-weighting-overlap-v2.svg|900]]

> [!figure] 图 20.8-06　Importance weighting 的 overlap、ratio 与有效样本量
> 左栏推导 target-risk identity；中栏展示 domain odds/KMM、weight tail、clipping 与 $n_{\rm eff}$；右栏给出 cross-fit、weighted validation 与不可用条件。来源：依据 Shimodaira、Huang et al.、Cortes–Mansour–Mohri 独立绘制；由 [[plot_distribution_shift_v2.py]] 确定性生成。

**怎样读图**：先过 conditional stability 与 overlap 两道门，再检查 weight estimator 和 tail，最后才把 weighted risk 用于选择。

**图没有证明什么**：图没有证明 estimated weights 正确，也没有证明 importance weighting 可修复 concept shift 或 support 空洞。

## 十四、AI 接口

- 数据筛选/主动学习：sampling propensity 必须记录；
- 医疗：target hospital support 与 patient unit；
- 推荐：曝光 propensity、off-policy overlap 与反馈；
- LLM：语料重采样 weights 不修复时间后的事实机制变化。

## 十五、常见错误

1. 只写 ratio 不写 conditional stability；
2. 忽略 target support；
3. 把无偏当低方差；
4. 不报 $n_{\rm eff}$ 和 maximum weight；
5. clipping 不报告阈值和偏差；
6. domain classifier 未校准；
7. 用 source validation 选 weighted model；
8. concept shift 仍套 covariate correction。

## 十六、最小记忆

> [!summary]
> - covariate shift 下 target risk = source importance-weighted risk；
> - overlap 是可识别硬条件；
> - weight second moment 控制有限样本稳定性；
> - self-normalization 与 clipping 以偏差换方差；
> - ratio estimation、模型训练和选择需要数据隔离；
> - weighting 不能创造 source support 外的 labels。

## 十七、掌握标准

### A. 定义
能写 ratio、overlap、weighted risk 与 $n_{\rm eff}$。
### B. 推导
能推导 change-of-measure、domain odds 与 clipping bias bound。
### C. 反例
能构造无偏但高方差、support failure 与 concept-shift 失败。
### D. 实验
能画 weight distribution、ESS、clip sensitivity 与 target risk curve。
### E. 迁移
能设计 cross-fitted ratio、weighted validation 与 target locked test。

## 十八、练习与独立详解

- [[习题 - 重要性加权与 Covariate Shift 校正]]
- [[解答 - 重要性加权与 Covariate Shift 校正]]

## 参考来源

- [[S-2000-Shimodaira-Covariate-Shift]]
- [[S-2007-Huang-KMM]]
- [[S-2010-Cortes-Importance-Weighting]]
- [[S-2009-Quinonero-Dataset-Shift]]
