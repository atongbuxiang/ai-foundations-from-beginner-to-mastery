---
type: source
status: draft
area: [sources, architecture/ssm, approximation]
source_type: paper
title: "HiPPO: Recurrent Memory with Optimal Polynomial Projections"
author: "Albert Gu, Tri Dao, Stefano Ermon, Atri Rudra, Christopher Ré"
year: 2020
url: "https://proceedings.neurips.cc/paper_files/paper/2020/hash/102f0bb6efb3a6128a3c750dd16729be-Abstract.html"
accessed: 2026-08-24
source_tier: A
scope_role: primary
related: ["[[HiPPO、S4 与结构化长记忆]]", "[[Banach 空间、Hilbert 空间与正交投影]]"]
created: 2026-08-24
updated: 2026-08-24
---

# HiPPO: Recurrent Memory with Optimal Polynomial Projections

> [!abstract] 来源定位
> HiPPO 把在线历史压缩形式化为指定测度下的多项式投影，并导出可递推更新的系数动力学。课程用它连接 Hilbert 投影、线性 ODE 与有限状态记忆。

## 证明边界

- “optimal” 指选定函数空间、基、阶数与随时间测度下的投影误差最小；
- 改变测度就改变“哪些历史更重要”，不能把一个 optimality 口号外推到所有任务损失；
- 连续投影保证、离散实现误差、可训练参数化与下游效果必须分账。

## 调用

- [[HiPPO、S4 与结构化长记忆]]
- [[S-2024-Su-10114-HiPPO正交函数投影]]

