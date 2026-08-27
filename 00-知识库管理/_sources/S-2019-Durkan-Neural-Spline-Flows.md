---
type: source
status: verified
area: [sources, generative-models, normalizing-flows, splines]
source_type: paper
title: "Neural Spline Flows"
author: "Conor Durkan; Artur Bekasov; Iain Murray; George Papamakarios"
year: 2019
url: "https://arxiv.org/abs/1906.04032"
venue: "NeurIPS 2019"
accessed: 2026-08-25
source_tier: A
scope_role: foundational
temporal_role: foundational
related: ["[[Neural Spline Flow 与单调可逆变换]]"]
created: 2026-08-25
updated: 2026-08-25
---
# Durkan et al.：Neural Spline Flows

> [!abstract] 来源定位
> Rational-quadratic spline 用正的 bin widths/heights 与 knot derivatives 保证单调，并保留解析 inverse 与 derivative。课程用它展示 coupling/autoregressive skeleton 不变时，elementwise transform 如何提升表达力。

Softmax/softplus 只保证参数正，不自动保证数值条件良好；最小 bin、tail transform、边界匹配、root selection 与 log-derivative clipping 都属于实现合同。

