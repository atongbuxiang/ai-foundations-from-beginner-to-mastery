---
type: source
status: verified
area: [sources, neural-tangent-kernel, infinite-width]
source_type: paper
title: "Neural Tangent Kernel: Convergence and Generalization in Neural Networks"
author: [Arthur Jacot, Franck Gabriel, Clement Hongler]
year: 2018
url: "https://papers.nips.cc/paper_files/paper/2018/hash/5a4be1fa34e62bb8a6ec6b91d2462f5a-Abstract.html"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS proceedings; retain citation"
venue: "Advances in Neural Information Processing Systems 31"
scope_role: primary
temporal_role: modern-theory
related: ["[[NTK、Lazy Training 与 Kernel Regime]]", "[[正定核、RKHS 与表示定理]]", "[[Standard、NTK 与 Mean-field 参数化]]"]
created: 2026-08-23
updated: 2026-08-26
---
# Neural Tangent Kernel
> [!abstract] 来源定位
> 引入参数梯度 Gram 形式的 NTK，并研究全连接网络无限宽极限中 kernel 的确定性与训练期稳定性。本库调用 NTK 定义、function-space gradient dynamics 与 eigenmode 解释；finite-width、parameterization 和 statistical assumptions 单独审计。
## 本库调用
1. $K_\theta(x,x')$ 定义；
2. 无限宽 deterministic kernel；
3. least-squares kernel dynamics；
4. eigenmode convergence；
5. optimization 与 generalization 分层。
