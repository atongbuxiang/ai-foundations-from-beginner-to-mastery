---
type: source
status: draft
area: [sources, ai/attention, math/kernel-methods, ai/efficient-transformers]
source_type: blog
title: "Transformer升级之路：5、作为无限维的线性Attention"
author: 苏剑林
year: 2021
url: "https://spaces.ac.cn/archives/8601"
accessed: 2026-08-19
source_tier: C
license: "科学空间站点声明存在版本差异；仅保存独立摘要、短公式与链接"
site_category: [信息时代]
scope_role: bridge
temporal_role: modern-exposition
related: ["[[正定核、RKHS 与表示定理]]", "[[有界算子、紧算子与谱理论基础]]", "[[Attention 的几何、核与概率视角]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]", "[[S-2019-Su-6910-HSIC与RKHS接口]]"]
created: 2026-08-19
updated: 2026-08-19
---

# Transformer升级之路：5、作为无限维的线性Attention

> [!abstract] 来源定位
> 文章把 softmax attention 的指数 dot-product 看作可分解的 kernel，并比较随机正特征、Taylor/多项式截断等有限化路线。课程采用“infinite feature inner product → finite feature approximation → matrix associativity → linear complexity”的问题链；核的 PSD/RKHS 定理、概率误差界和完整 attention normalization 由正式教材及原论文补严。

## 元数据与纳入

- 正式引用：苏剑林，2021-08-06，《Transformer升级之路：5、作为无限维的线性Attention》；
- 页面：[https://spaces.ac.cn/archives/8601](https://spaces.ac.cn/archives/8601)；
- 当前调用者：[[正定核、RKHS 与表示定理]]；
- 同系列前置包括《线性Attention的探索：Attention必须有个Softmax吗？》与 Performer 讨论，本卡不复制整条系列。

## 核心问题

标准 attention 的未归一化权重含

$$
\exp(q^\top k).
$$

如果能构造有限或无限 features $\phi,\varphi$ 使

$$
\phi(q)^\top\varphi(k)\approx\exp(q^\top k),
$$

就能把 $(QK^\top)V$ 类型的 quadratic token interaction改写为 $\phi(Q)(\varphi(K)^\top V)$，利用结合律降低 sequence-length complexity。文章展示了 Taylor tensor features 与 random projection/positive features 的直觉。

## 断言与课程判断

| ID | 断言 | 条件/边界 | 判断 |
|---|---|---|---|
| C1 | Exponential dot-product可看作无限维 feature inner product | 需给收敛展开或合法随机特征构造 | 采用 |
| C2 | 截断 feature map可近似 attention affinity | 误差依赖 norm范围、维数、sampling与tail | 采用并要求误差账本 |
| C3 | Factorization允许通过矩阵结合律避免显式 $n^2$ affinity | 仍依赖 feature dimension、normalizer、mask与implementation | 采用 |
| C4 | 任意 $\phi(q)^\top\varphi(k)$ 都是 PSD kernel | 只有同一 feature map且形成 symmetric Gram时自动 PSD | 不采用 |
| C5 | 逼近 unnormalized exponential kernel即可保证完整 attention输出同误差 | denominator、causal masking与value interaction可放大误差 | 不采用 |
| C6 | 有限 feature维数越大，单次随机 realization误差必单调下降 | Monte Carlo误差可波动，只能给概率/平均趋势 | 不采用 |

## 课程补严

- Positive kernel 需要对任意有限样本的 Gram quadratic form非负；“核函数形式”不能只靠命名；
- $\phi=\varphi$ 时有标准 inner-product kernel，$\phi\ne\varphi$ 时一般只是双 feature pairing；
- Classic RFF 来自 Bochner theorem，直接适用于 continuous shift-invariant PSD kernels；softmax positive random features是相关但不同的构造；
- Taylor truncation的 deterministic error需限制 $q^\top k$ 范围，且 tensor feature dimension会快速增长；
- Attention output error需把 numerator kernel approximation、denominator stability、mask与finite precision分开；
- Linear-time 是相对 sequence length $n$ 的说法，feature dimension与head/value dimensions仍进入成本。

## 已生成与后续调用

- [x] [[正定核、RKHS 与表示定理]]：positive feature factorization、RFF对照和linear-attention声明边界；
- [x] [[Attention 的几何、核与概率视角]]：positive random features、核特征与 denominator error；
- [ ] 后续大模型理论专题：kernel regime 与 feature-learning regime 的比较。

## 交叉验证

- Rahimi & Recht, *Random Features for Large-Scale Kernel Machines*：shift-invariant kernels 的 RFF 原始来源；
- Choromanski et al., *Rethinking Attention with Performers*：softmax attention 的 positive orthogonal random features；
- Aronszajn 与 MIT 9.520：positive kernel/RKHS 的严格定义；
- 原文承担 AI 问题入口，不单独承担上述一般定理或概率误差结论。
