---
type: source
status: active
area: [sources, learning-theory, algorithmic-stability, optimization]
source_type: paper
title: "Train faster, generalize better: Stability of stochastic gradient descent"
author: [Moritz Hardt, Benjamin Recht, Yoram Singer]
year: 2016
url: "https://proceedings.mlr.press/v48/hardt16.html"
accessed: 2026-08-23
source_tier: A
license: "PMLR article; retain citation, independent derivations, and official article/PDF links"
venue: "Proceedings of ICML 2016, PMLR 48, 1225–1234"
scope_role: primary
temporal_role: classical-foundation
related: ["[[随机梯度算法的稳定性接口]]", "[[算法稳定性与替换一个样本]]", "[[随机梯度与小批量估计]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Train Faster, Generalize Better

> [!abstract] 来源定位
> Hardt、Recht 与 Singer 用同一随机索引耦合两个相邻数据集上的 SGD 轨迹，把 update map 的 nonexpansiveness/expansiveness 与“抽到那条不同样本”的 $1/m$ 概率合并成 stability bound。本库用它承担训练时间、步长、光滑性与泛化之间的算法依赖接口。

## 元数据与纳入

- 论文主页：[PMLR](https://proceedings.mlr.press/v48/hardt16.html)；
- 官方全文：[PDF](https://proceedings.mlr.press/v48/hardt16.pdf)；
- 正式引用：Hardt, M., Recht, B. & Singer, Y. (2016), ICML, PMLR 48, 1225–1234；
- 证据角色：randomized uniform stability、coupled trajectories、convex/nonconvex smooth SGD 与 iteration-dependent bounds；
- 版权边界：课程使用独立 recurrence、机制图和边界审计，不复制论文图示。

## 本库调用的断言

1. 对相邻数据集使用同一初始化、同一抽样索引和同一内部随机性，可把 algorithm sensitivity 化成 trajectory distance；
2. $L$-Lipschitz loss 把 parameter distance 转成 test-loss difference；
3. convex、smooth 且 $\eta_t\le 2/\gamma$ 时，单步 gradient map nonexpansive；
4. 以 replacement sampling 运行 $T$ 步时，经典 convex bound 为
   $$
   \epsilon_{\mathrm{stab}}
   \le \frac{2L^2}{m}\sum_{t=1}^T\eta_t;
   $$
5. nonconvex smooth 情形的同轨迹误差可被扩张因子放大，所以 training horizon 与 step schedule 进入证书；
6. 实际深网是否满足全局 Lipschitz/smoothness、batch coupling 与 adaptive-update 条件，必须另行核对。

> [!warning] 不外推的结论
> “SGD 通常泛化好”不是无条件 theorem。数据采样协议、loss regularity、step-size schedule、随机性量词和停止时刻都属于定理合同；mini-batch、BatchNorm、data augmentation 与 Adam 不能只改算法名称后沿用同一证明。

## 后续调用

- [[随机梯度算法的稳定性接口]]：完整 coupling recurrence；
- [[容量界、稳定性界与 PAC-Bayes 的比较]]：algorithm-dependent certificate；
- 后续 optimization/generalization 章节：early stopping 与 implicit regularization 的分账。
