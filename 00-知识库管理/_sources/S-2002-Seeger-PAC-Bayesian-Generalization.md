---
type: source
status: active
area: [sources, learning-theory, pac-bayes]
source_type: paper
title: "PAC-Bayesian Generalisation Error Bounds for Gaussian Process Classification"
author: [Matthias Seeger]
year: 2002
url: "https://www.jmlr.org/papers/v3/seeger02a.html"
accessed: 2026-08-23
source_tier: A
license: "JMLR article; retain citation, independent derivations, and official links"
venue: "Journal of Machine Learning Research 3, 233–269"
scope_role: primary
temporal_role: classical-foundation
related: ["[[PAC-Bayes Bound 的测度变换主线]]", "[[PAC-Bayes 先验、后验与数据依赖边界]]"]
created: 2026-08-23
updated: 2026-08-23
---

# PAC-Bayesian Generalisation Error Bounds for Gaussian Process Classification

> [!abstract] 来源定位
> Seeger 给出适合计算的 PAC-Bayes-kl 形式，并把它用于 Gaussian-process classification。对本库最关键的是：prior 在样本前确定、posterior 可依赖样本、结论同时对所有 posterior 成立，以及 empirical Gibbs risk 与 population Gibbs risk 之间的 Bernoulli-KL 证书。

## 元数据与纳入

- 论文主页：[JMLR](https://www.jmlr.org/papers/v3/seeger02a.html)；
- 官方全文：[PDF](https://www.jmlr.org/papers/volume3/seeger02a/seeger02a.pdf)；
- 正式引用：Seeger, M. (2002), *JMLR* 3, 233–269；
- 证据角色：PAC-Bayes-kl theorem、Gibbs risk、prior/posterior 量词与 convex-duality proof route。

## 本库调用的核心形式

在 i.i.d. binary 0–1 loss 下，令 $P$ 是不依赖实际训练样本的 prior，$Q$ 是任意 posterior。则以至少 $1-\delta$ 的概率，同时对所有 $Q$：

$$
\operatorname{kl}\!\left(\widehat R_S(Q)\middle\|R(Q)\right)
\le
\frac{\operatorname{KL}(Q\|P)+\log((m+1)/\delta)}{m}.
$$

若 $Q\not\ll P$，右侧 KL 取 $+\infty$。本库使用这一较粗但透明的 $m+1$ 二项类型矩常数；其他论文中的 $2\sqrt m$、Catoni 参数式或线性化版本不是同一个 theorem。

## 本库调用的断言

1. posterior 可以在看见 $S$ 后选择，因为成功事件同时覆盖所有 $Q$；
2. prior 不可以用同一 $S$ 后验式调参而不付修正；
3. bound 控制的是 Gibbs classifier 的平均风险，不自动等于 posterior mean、MAP 或 majority vote 的风险；
4. inverse binary KL 通常比 Pinsker 平方根松弛更紧；
5. PAC-Bayes 的优化对象可视作经验风险与相对熵复杂度的共同权衡。

## 后续调用

- [[PAC-Bayes Bound 的测度变换主线]]：完整四步证明；
- [[PAC-Bayes 先验、后验与数据依赖边界]]：Gaussian KL、support、split prior 与模型审计；
- [[容量界、稳定性界与 PAC-Bayes 的比较]]：与 uniform/capacity certificate 的量词比较。

