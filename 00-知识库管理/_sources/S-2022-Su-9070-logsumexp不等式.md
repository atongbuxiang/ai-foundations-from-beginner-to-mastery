---
type: source
status: draft
area: [sources, math/convex-analysis, ai/loss-functions]
source_type: blog
title: "logsumexp 运算的几个不等式"
author: 苏剑林
year: 2022
url: "https://spaces.ac.cn/archives/9070"
accessed: 2026-08-19
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
site_category: [数学研究]
scope_role: supporting
temporal_role: classical-exposition
related: ["[[基本不等式与界的构造]]", "[[凸函数、Jensen 不等式与上图集]]", "[[Taylor 展开与余项]]", "[[交叉熵与 KL 散度]]"]
created: 2026-08-19
updated: 2026-08-19
---

# logsumexp 运算的几个不等式

> [!abstract] 来源定位
> 文章集中整理 logsumexp 的 max approximation bound、temperature scaling、convexity 与 Jensen 接口，是 softmax/cross-entropy 进入凸分析的清晰中文入口。课程采用其问题结构和基本不等式；Hessian PSD、strict-convexity null direction、composition rules、数值稳定与 parameter-space 非凸边界由正式教材和本课程补严。

## 元数据与纳入

- 正式引用：苏剑林，2022-05-10，《logsumexp 运算的几个不等式》；
- 原始页面：[https://spaces.ac.cn/archives/9070](https://spaces.ac.cn/archives/9070)；
- 当前调用者：[[基本不等式与界的构造]]、[[凸函数、Jensen 不等式与上图集]]；
- 本卡只纳入与 AI/优化相关的数学内容，不复制原文长段落。

## 核心对象

$$
\operatorname{LSE}(x)
=\log\sum_{i=1}^ne^{x_i}.
$$

令 $m=\max_i x_i$，则

$$
m\le\operatorname{LSE}(x)\le m+\log n.
$$

temperature 形式

$$
L_\tau(x)
=\tau\log\sum_i e^{x_i/\tau}
$$

满足

$$
0\le L_\tau(x)-\max_i x_i\le\tau\log n.
$$

## 核心断言与课程判断

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | LSE 与 max 相差至多 $\log n$ | 精确不等式 | finite $n$、统一 log base | 采用 |
| C2 | temperature 降低使 smooth max 更接近 max | 极限/近似 | gradient/Hessian 与浮点代价同时变化 | 采用并补边界 |
| C3 | LSE convex | 定理 | 对 logits $x$；不等于对生成 logits 的深网参数 convex | 采用并补严 |
| C4 | Jensen 可用于 LSE | 定理应用 | 随机向量可积、LSE expectation 定义 | 采用 |
| C5 | Hölder 可直接证明 convexity | 证明路径 | 需明确指数与权重条件 | 作为替代证明 |

## 课程补严

gradient 是 softmax：

$$
\nabla\operatorname{LSE}(x)=p.
$$

Hessian 是 categorical covariance：

$$
\nabla^2\operatorname{LSE}(x)
=\operatorname{diag}(p)-pp^T\succeq0.
$$

但

$$
(\operatorname{diag}p-pp^T)\mathbf1=0,
$$

所以 LSE 在完整 logits space 上不 strictly convex。cross-entropy

$$
\ell(z,y)=\operatorname{LSE}(z)-z_y
$$

对 logits convex；只有 logits 对参数 affine 时，才沿 affine-precomposition 保持 parameter convexity。

数值实现必须使用

$$
\operatorname{LSE}(x)
=m+\log\sum_i e^{x_i-m}
$$

避免 overflow。数学 convexity 不等于 naive floating-point 稳定。

## 限制与保留意见

- $\tau\to0$ 时 approximation error 降低，但 Hessian scale 含 $1/\tau$，优化和精度可能更困难；
- finite $\tau$ 的 smooth max 不等于 exact max；
- Jensen 只给相应 convex quantity 的平均不等式，不自动给 accuracy/calibration 改善；
- logit convexity 不能外推到 deep parameter space；
- `logsumexp` 的 log base 改变单位与 scale，代码/公式必须统一。

## 已生成与后续调用

- [x] [[基本不等式与界的构造]]：max双边界、temperature、$\ell_\infty$ Lipschitz与stable shift；
- [x] [[Taylor 展开与余项]]：方向均值/方差与有限温度近似；
- [x] [[凸函数、Jensen 不等式与上图集]]：max bound、gradient/Hessian、Jensen 与严格凸性边界；
- [x] [[光滑性、强凸性与条件数]]：softmax Hessian spectral bound；
- [x] [[一阶最优性条件与梯度下降]]：temperature 对 smoothness 与步长的影响。

## 交叉验证

- Boyd–Vandenberghe Chapter 3：logsumexp example、convexity calculus 与 composition；
- Stanford EE364A convex-functions lecture：epigraph、Jensen、一阶/二阶判据；
- [[交叉熵与 KL 散度]]：stable softmax NLL、target 与 parameter variable 的区分。
