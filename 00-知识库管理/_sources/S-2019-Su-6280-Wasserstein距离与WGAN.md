---
type: source
status: draft
area: [sources, ai/generative-models, math/probability, math/optimization]
source_type: blog
title: "从Wasserstein距离、对偶理论到WGAN"
author: 苏剑林
year: 2019
url: "https://spaces.ac.cn/archives/6280"
accessed: 2026-08-18
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要、短公式与链接"
site_category: [数学研究]
series: ""
series_order:
scope_role: bridge
temporal_role: classical-exposition
related: ["[[联合分布、边缘分布与独立性]]", "[[交叉熵与 KL 散度]]", "[[弱对偶、强对偶与 Slater 条件]]", "[[度量空间、拓扑与连续映射]]"]
created: 2026-08-18
updated: 2026-08-19
---

# 从Wasserstein距离、对偶理论到WGAN

> [!abstract] 来源定位
> 文章从运输方案、线性规划和对偶逐步进入 Wasserstein distance 与 WGAN。当前概率分卷只调用最前面的结构：$\gamma$ 是以 $p,q$ 为边缘的联合分布，改变 $\gamma$ 就是在固定边缘下改变配对；对偶与 Lipschitz critic 留给优化和生成模型专章。

## 纳入判定

- 范围角色：`bridge`，服务概率 coupling、optimal transport 与生成模型；
- 年代角色：`classical-exposition`；
- 当前调用者：[[联合分布、边缘分布与独立性]]、[[f-散度、Bregman 散度与概率度量]]、[[度量空间、拓扑与连续映射]]。

## 元数据

- 正式引用：苏剑林，2019-01-20，《从Wasserstein距离、对偶理论到WGAN》；
- 原始页面：[https://spaces.ac.cn/archives/6280](https://spaces.ac.cn/archives/6280)；
- 本地范围：保存 coupling、边缘约束、成本与证据边界，不复制线性规划长推导。

## 结构摘要

```mermaid
flowchart LR
    M["源/目标边缘 p,q"] --> C["coupling γ∈Π(p,q)"]
    C --> P["运输成本"]
    P --> L["线性规划"]
    L --> D["对偶"]
    D --> W["WGAN critic"]
```

## 核心断言与课程判断

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | $\gamma$ 是以 $p,q$ 为边缘的联合分布 | 定义 | 概率测度与可积成本给定 | 已核验 |
| C2 | 运输计划可表为在 $\Pi(p,q)$ 上最小化期望成本 | 定义/方法 | cost measurable；有限性另查 | 已核验 |
| C3 | 离散 OT 是带行列和约束的线性规划 | 推导 | 有限离散支持 | 已核验 |
| C4 | 对偶形式导向 WGAN critic | 方法 | 需 Kantorovich duality 与 Lipschitz 条件 | 留待优化专章 |

## 概率骨架

$$
\int\gamma(x,y)dy=p(x),
\qquad
\int\gamma(x,y)dx=q(y).
$$

独立 coupling $p(x)q(y)$ 只是可行集合中的一个；optimal coupling 通常不独立。由此可见，边缘并不能恢复 joint。

## 限制与保留意见

- $\gamma$ 的 density 写法不覆盖所有一般测度 coupling；
- Kantorovich–Rubinstein duality 的函数空间和 cost 条件不能由直觉运输图替代；
- WGAN 实现中的 gradient penalty 不自动精确实施全局 $1$-Lipschitz；
- 经验 batch OT 与总体 OT 有抽样偏差；匹配不必有语义唯一性；
- 本轮页面直接全文抓取受站点限制，结构、日期与关键公式通过公开索引核对。

## 已生成与后续调用

- [x] [[联合分布、边缘分布与独立性]]：coupling 与固定边缘；
- [x] [[f-散度、Bregman 散度与概率度量]]：$W_1$ primal/dual、support geometry 与 empirical/critic 边界；
- [x] [[度量空间、拓扑与连续映射]]：ground metric、probability topology 与 WGAN 的连续性动机；
- [ ] WGAN 专题：critic game dynamics、Lipschitz enforcement 与训练稳定性。

## 交叉验证

- Villani，*Optimal Transport: Old and New*；
- Kantorovich–Rubinstein duality；
- Arjovsky, Chintala & Bottou，*Wasserstein GAN*。
