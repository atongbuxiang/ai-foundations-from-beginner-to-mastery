---
type: source
status: active
area: [sources, learning-theory, pac-bayes, data-dependent-priors]
source_type: paper
title: "Data-dependent PAC-Bayes priors via differential privacy"
author: [Gintare Karolina Dziugaite, Daniel M. Roy]
year: 2018
url: "https://papers.nips.cc/paper/2018/hash/9a0ee0a9e7a42d2d69b8f86b3a0756b1-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS proceedings; retain citation, independent derivations, and official links"
venue: "Advances in Neural Information Processing Systems 31"
scope_role: primary
temporal_role: modern-extension
related: ["[[PAC-Bayes 先验、后验与数据依赖边界]]", "[[PAC-Bayes Bound 的测度变换主线]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Data-dependent PAC-Bayes priors via differential privacy

> [!abstract] 来源定位
> Dziugaite 与 Roy 研究怎样在 PAC-Bayes 中合法使用依赖训练数据的 prior。核心不是取消 prior independence，而是利用 differential privacy 限制 prior mechanism 对单样本的依赖，并在专门 theorem 中支付附加修正。

## 元数据与纳入

- 论文主页：[NeurIPS](https://papers.nips.cc/paper/2018/hash/9a0ee0a9e7a42d2d69b8f86b3a0756b1-Abstract.html)；
- 官方全文：[PDF](https://proceedings.neurips.cc/paper/8063-data-dependent-pac-bayes-priors-via-differential-privacy.pdf)；
- 正式引用：Dziugaite, G. K. & Roy, D. M. (2018), *NeurIPS 31*；
- 证据角色：differentially private data-dependent priors 与修正项的存在性；
- 本库不把其常数移植到普通 PAC-Bayes-kl theorem。

## 本库调用的断言

1. 用完整样本直接把 prior center 设成训练解，会破坏标准 data-independent-prior theorem 的矩界步骤；
2. differential privacy 可限制 prior mechanism 对一个样本的敏感性；
3. 允许 data-dependent prior 的结论必须引用专门 theorem，并支付 privacy/confidence correction；
4. 这与把独立 split $S_0$ 用于 prior、把 $S_1$ 用于 empirical certificate 的 conditional argument 是两条不同路线；
5. “经验上 prior 很合理”不是合法性证明。

## 后续调用

- [[PAC-Bayes 先验、后验与数据依赖边界]]：合法先验路线分层与泄漏审计。

