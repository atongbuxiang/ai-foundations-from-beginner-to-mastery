---
type: source
status: verified
area: [sources, ai/transformer, math/probability, numerical-stability]
source_type: blog
title: "浅谈Transformer的初始化、参数化与标准化"
author: 苏剑林
year: 2021
url: "https://spaces.ac.cn/archives/8620"
accessed: 2026-08-18
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要、短公式与链接"
site_category: [数学研究, 信息时代]
series: ""
series_order:
scope_role: core
temporal_role: classical-exposition
related: ["[[期望、方差与矩]]", "[[协方差、相关性与条件期望]]", "[[内积空间]]", "[[方差传播与宽层均值场近似]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 形状、参数量与 FLOPs 总账]]", "[[Transformer 表达、稳定性与证据边界]]"]
created: 2026-08-18
updated: 2026-08-26
---

# 浅谈Transformer的初始化、参数化与标准化

> [!abstract] 来源定位
> 文章以 Transformer 训练失败为入口，连接权重初始化、$QK^\top/\sqrt d$、残差路径与 normalization。当前概率章调用均值/方差传播及其假设；不同架构的参数化建议需在模型、实验与后续文献中分别核验。

## 元数据与纳入

- 正式引用：苏剑林，2021-08-17，《浅谈Transformer的初始化、参数化与标准化》；
- 原始页面：[https://spaces.ac.cn/archives/8620](https://spaces.ac.cn/archives/8620)；
- 范围角色：`core`（Transformer 理论），概率分卷中作 `bridge`；
- 当前调用者：[[期望、方差与矩]]。

## 核心断言与课程判断

| ID | 断言 | 类型 | 条件/边界 | 当前判断 |
|---|---|---|---|---|
| C1 | 初始化需控制前向/反向尺度 | 方法原则 | 架构、激活、残差和 normalization 固定 | 已建立 |
| C2 | iid 零均值单位方差坐标下 $\operatorname{Var}(q\cdot k)=d$ | 推导 | 独立、零交叉 covariance、有限二阶矩 | 已核验 |
| C3 | 除以 $\sqrt d$ 可把初始 score 二阶尺度归一 | 推导 | 同 C2；不是训练全过程精确分布 | 有条件成立 |
| C4 | normalization/参数化选择影响训练稳定性 | 方法/经验 | 依赖模型和实验设置 | 需分架构核验 |

## 本章保留的概率骨架

$$
q\cdot k=\sum_{i=1}^dq_ik_i,
$$

在文中典型初始化假设下

$$
\mathbb E[q\cdot k]=0,
\qquad
\operatorname{Var}(q\cdot k)=d.
$$

因此 $1/\sqrt d$ 是二阶尺度控制。T5 等实现可通过不同初始化/参数化调整等效尺度，说明公式必须与整个合同一起读。

## 限制与保留意见

- 坐标 iid/独立主要是初始化近似，训练后通常不成立；
- variance 稳定不等于 spectral norm、tail 或 gradient 稳定；
- RMS、variance、LayerNorm statistics 不可混用；
- 单次训练故障是问题入口，不构成普遍实证；
- 页面全文抓取受限，元数据和核心结构由公开索引交叉核对。

## 已生成与后续调用

- [x] [[期望、方差与矩]]：Attention 二阶尺度；
- [x] [[Transformer Block、残差、归一化与 FFN]]与[[Transformer 表达、稳定性与证据边界]]；
- [ ] MuP、residual scaling、Pre-LN/Post-LN 的对照实验。

## 交叉验证

- Vaswani et al.，*Attention Is All You Need*；
- Glorot & Bengio；He et al. 初始化论文；
- Tensor Programs / MuP 与后续 Transformer scaling 文献。
