---
type: source
status: draft
area: [sources, ai/cnn, receptive-field]
source_type: paper
title: "Understanding the Effective Receptive Field in Deep Convolutional Neural Networks"
author: [Wenjie Luo, Yujia Li, Raquel Urtasun, Richard Zemel]
year: 2016
url: "https://proceedings.neurips.cc/paper_files/paper/2016/hash/c8067ad1937f728f51288b3eb986afaa-Abstract.html"
accessed: 2026-08-24
source_tier: A
scope_role: core
temporal_role: original-analysis
related: ["[[堆叠卷积、感受野与有效感受野]]"]
created: 2026-08-24
updated: 2026-08-24
---

# Luo et al.：Effective Receptive Field

> [!abstract] 来源定位
> 论文区分 theoretical receptive field 与输入位置对输出影响强弱定义的 effective receptive field，并在特定线性化/随机权重分析下得到中心更强、近 Gaussian 的路径贡献结构，再以网络实验研究训练、subsampling、skip、dropout 与非线性的影响。

## 核心断言审计

| 断言 | 条件 | 课程处理 |
|---|---|---|
| 堆叠局部层的 theoretical RF 可递推精确计算 | 图结构、kernel/stride/dilation 已知 | `I`，独立推导 |
| 多路径贡献在简化条件下趋近 Gaussian-like | 权重/路径与渐近假设 | `T/H`，不写成任意训练网定理 |
| effective RF 往往小于 theoretical RF | 文中模型/定义/实验 | `E`，保留测量定义 |
| 增大 theoretical RF 自动解决长程信息利用 | 不成立 | 构造梯度/路径权重反例 |

## 课程补严

- theoretical RF 是“可能影响”的 support；effective RF 是依输入、参数、非线性、输出标量与测量阈值的 sensitivity；
- gradient map 不是因果解释或任务充分性的完整证明；
- padding/boundary 会使不同位置的 RF 不同。
