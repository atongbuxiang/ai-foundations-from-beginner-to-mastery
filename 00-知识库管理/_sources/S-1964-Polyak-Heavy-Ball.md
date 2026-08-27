---
type: source
status: verified
area: [sources, optimization, momentum]
source_type: paper
title: "Some Methods of Speeding Up the Convergence of Iteration Methods"
author: [Boris T. Polyak]
year: 1964
url: "https://m.mathnet.ru/php/archive.phtml?jrnid=zvmmf&option_lang=eng&paperid=7713&wshow=paper"
accessed: 2026-08-26
source_tier: A
venue: "USSR Computational Mathematics and Mathematical Physics 4(5):1–17"
scope_role: primary
related: ["[[Momentum、EMA、偏差修正与框架约定]]", "[[二次模型的学习率—动量稳定域与阻尼]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Polyak 1964：Heavy-ball 方法

> [!abstract] 来源定位
> Heavy-ball/momentum 的经典原始来源。第六章只调用多步迭代、二次问题上的加速参数与“目标值不必逐步单调”这些结论；深网随机训练的有效性不由该论文证明。

## 课程调用

1. 二步递推 $x_{t+1}=x_t-\eta\nabla f(x_t)+\mu(x_t-x_{t-1})$；
2. 对称正定二次型上的特征根分析；
3. $mI\preceq H\preceq LI$ 时的经典最优常参数；
4. 惯性可能产生振荡，loss 的单步单调下降不是算法合同。

## 不得扩大解释

- 经典参数依赖固定二次谱端点，不能直接当作深网默认超参数；
- deterministic quadratic rate 不等于 stochastic non-convex rate；
- “heavy ball”物理类比不能替代离散 Jury 稳定条件。

