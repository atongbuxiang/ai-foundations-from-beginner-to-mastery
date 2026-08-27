---
type: source
status: active
area: [sources, learning-theory, adaptive-data-analysis, privacy]
source_type: paper
title: "Generalization in Adaptive Data Analysis and Holdout Reuse"
author: [Cynthia Dwork, Vitaly Feldman, Moritz Hardt, Toniann Pitassi, Omer Reingold, Aaron Roth]
year: 2015
url: "https://arxiv.org/abs/1506.02629"
accessed: 2026-08-20
source_tier: A
license: "Use the author/arXiv copy; notes retain independent summaries, theorem pointers and links"
venue: NeurIPS 2015
scope_role: backbone
temporal_role: classical-foundation
related: ["[[训练集、验证集、测试集与自适应复用]]", "[[互信息与信息论泛化界]]", "[[算法稳定性与替换一个样本]]"]
created: 2026-08-20
updated: 2026-08-20
---

# Generalization in Adaptive Data Analysis and Holdout Reuse

> [!abstract] 来源定位
> 论文把“反复查看同一 holdout 后继续提出新分析”形式化为 adaptive data analysis：输出与 holdout 之间的信息依赖会破坏预先固定查询的普通浓缩结论。论文用 differential privacy、description length 与 approximate max-information 建立可复用 holdout 的严格路线。本章只讲问题、最小反例与方法边界；完整 max-information 理论留到 LT-39。

## 元数据与纳入

- 原论文：[arXiv 1506.02629](https://arxiv.org/abs/1506.02629)；
- NeurIPS proceedings：[paper PDF](https://proceedings.neurips.cc/paper_files/paper/2015/file/bad5f33780c42f2588878a9d07405083-Paper.pdf)；
- 同期 Science 简述：Dwork et al., *The reusable holdout: Preserving validity in adaptive data analysis*, 2015；
- 当前调用者：[[训练集、验证集、测试集与自适应复用]]；
- 后续调用：LT-39 information-theoretic generalization、privacy/generalization 接口。

## 问题合同

给定 holdout

$$
T=(Z_1,\ldots,Z_n)\sim P^n,
$$

分析者按轮提出统计查询 $f_t:\mathcal Z\to[0,1]$。关键是

$$
f_t=\mathcal A_t(a_1,\ldots,a_{t-1},\text{training information}),
$$

其中以往答案 $a_j$ 来自同一 $T$。因此 $f_t$ 不再是抽取 $T$ 前固定的函数，普通 fixed-query concentration 不能逐轮无代价复用。

## 论文主线

| 主线 | 直觉 | 本库调用范围 |
|---|---|---|
| reusable holdout / Thresholdout | 只在 train 与 holdout 分歧显著时以受控方式释放信息 | LT-08 讲思想，不复刻全部常数 |
| differential privacy ⇒ generalization | 单个样本对输出分布影响受控，限制对数据细节的过拟合 | LT-08 预告，LT-33/LT-39 深化 |
| description length | 输出可编码信息有限，则选择空间受到控制 | 连接 Occam、union bound 与 adaptive output |
| approximate max-information | 度量 dataset 与 algorithm output 的最坏型依赖 | LT-39 正式展开 |

## 断言账本

| ID | 断言 | 边界 | 当前判断 |
|---|---|---|---|
| C1 | 对固定查询的 holdout 有 concentration | 查询在看 holdout 前固定 | 经典结论 |
| C2 | 反复自适应查询仍可把每次答案当独立无偏评价 | 查询依先前答案，selection bias 累积 | 否定 |
| C3 | 限制输出信息可恢复统计有效性 | 需指定 privacy/description/max-information 条件 | 论文正式主线 |
| C4 | reusable holdout 意味测试集可被无限、无成本查看 | query 数、阈值、privacy budget 与误差均有限制 | 否定 |
| C5 | differential privacy 只是保密工具，与泛化无关 | 论文证明其稳定输出可迁移浓缩性质 | 否定，但需区分具体定理 |

## 课程补严

- 普通有限候选集、非自适应比较可用 union bound 支付 $\log K$；这与 arbitrary adaptive querying 不同；
- 一个公开 leaderboard 的返回精度、提交次数和反馈信息量都会影响 overfitting；
- 论文的 formal setting 不自动覆盖 temporal shift、benchmark contamination 或训练数据泄漏；这些是另外的分布/采样问题；
- “采用 differential privacy”不自动给有用的 tight generalization bound，仍需核对参数、样本量、loss sensitivity 和 output protocol；
- 若已经反复用坏测试集，最可靠的修复通常是收集新的真正独立 final test，而不是事后把旧测试集重新命名。

## 已生成与后续调用

- [x] [[训练集、验证集、测试集与自适应复用]]：adaptive reuse 的对象与方法边界；
- [ ] [[算法稳定性与替换一个样本]]：单样本敏感度与 generalization；
- [ ] [[互信息与信息论泛化界]]：max-information 与 average mutual information 分型。

