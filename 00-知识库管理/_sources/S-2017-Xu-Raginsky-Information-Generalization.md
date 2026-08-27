---
type: source
status: active
area: [sources, learning-theory, information-theoretic-generalization]
source_type: paper
title: "Information-Theoretic Analysis of Generalization Capability of Learning Algorithms"
author: [Aolin Xu, Maxim Raginsky]
year: 2017
url: "https://papers.nips.cc/paper_files/paper/2017/hash/ad71c82b22f4f65b9398f76d8be4c615-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS proceedings; retain citation, independent derivations, and official links"
venue: "Advances in Neural Information Processing Systems 30"
scope_role: primary
temporal_role: modern-foundation
related: ["[[互信息与信息论泛化界]]", "[[容量界、稳定性界与 PAC-Bayes 的比较]]", "[[训练集、验证集、测试集与自适应复用]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Information-Theoretic Analysis of Generalization Capability of Learning Algorithms

> [!abstract] 来源定位
> Xu 与 Raginsky 把 randomized learning algorithm 看作从 sample $S$ 到 output $W$ 的 channel，并用 $I(S;W)$ 控制期望泛化间隙。它提供一种 algorithm-、distribution-dependent 复杂度，但基础 theorem 控制的是 expected signed gap，而不是自动给出 high-probability certificate。

## 元数据与纳入

- 论文主页：[NeurIPS](https://papers.nips.cc/paper_files/paper/2017/hash/ad71c82b22f4f65b9398f76d8be4c615-Abstract.html)；
- 官方全文：[PDF](https://papers.nips.cc/paper/2017/file/ad71c82b22f4f65b9398f76d8be4c615-Paper.pdf)；
- 正式引用：Xu, A. & Raginsky, M. (2017), *NeurIPS 30*；
- 证据角色：KL transport lemma、sample–output mutual information theorem、data processing 与 composition interfaces。

## 本库调用的核心形式

若对每个 $w$，$\ell(w,Z)$ 在 $Z\sim P_Z$ 下是 $\sigma$-sub-Gaussian，$S=(Z_1,\ldots,Z_m)$ i.i.d.，且 $W\sim P_{W\mid S}$，则

$$
\left|\mathbb E\left[R(W)-\widehat R_S(W)\right]\right|
\le
\sqrt{\frac{2\sigma^2}{m}I(S;W)}.
$$

若 $\ell\in[a,b]$，Hoeffding lemma 允许取 $\sigma=(b-a)/2$。

## 本库调用的断言

1. $P_{W\mid S}$ 是 algorithmic channel；训练随机种子应包含在 conditional law 中；
2. mutual information 衡量 joint law 相对 product law 的平均依赖；
3. finite/countable output 满足 $I(S;W)\le H(W)\le\log|\mathcal W|$；
4. post-processing 不增加 mutual information；
5. deterministic continuous-valued output 常导致 $I(S;W)=+\infty$，使基础界无效；
6. expected signed gap、expected absolute gap 与 high-probability gap 是不同保证。

## 后续调用

- [[互信息与信息论泛化界]]：逐样本 transport 推导和 bit-budget corollary；
- [[容量界、稳定性界与 PAC-Bayes 的比较]]：信息证书的优点、缺口和可比边界。

