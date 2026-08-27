---
type: source
status: verified
area: [sources, optimization, adam]
source_type: paper
title: "Adam: A Method for Stochastic Optimization"
author: "Diederik P. Kingma; Jimmy Ba"
year: 2015
url: "https://arxiv.org/abs/1412.6980"
venue: "ICLR 2015"
accessed: 2026-08-26
source_tier: A
license: "arXiv/ICLR 论文；本库仅保存独立摘要、必要公式与链接"
scope_role: foundational
temporal_role: historical-foundational
related: ["[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]", "[[Adam 的 Epsilon、数值稳定与实现分歧]]", "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Kingma、Ba：Adam

> [!abstract] 来源定位
> Adam 的原始算法来源：用梯度的一阶、二阶原始矩 EMA 形成逐坐标方向，并对零初始化作 bias correction。原论文关于收敛的早期论证不能绕过后来的反例与修订文献。

## 算法对象

$$
\begin{aligned}
m_t&=\beta_1m_{t-1}+(1-\beta_1)g_t,\\
v_t&=\beta_2v_{t-1}+(1-\beta_2)g_t^2,\\
\widehat m_t&=m_t/(1-\beta_1^t),\qquad
\widehat v_t=v_t/(1-\beta_2^t).
\end{aligned}
$$

课程逐项区分：step 从 1 还是 0 计；$\epsilon$ 对应 Algorithm 1 还是文中 $\hat\epsilon$ 形式；weight decay 是否进入 gradient；最大化、稀疏梯度与 step skip 的实现合同。

## 断言审计

| 断言 | 课程判断 |
|---|---|
| 对角 gradient rescaling 下具有尺度不变性 | 在 $\epsilon=0$、状态同步缩放等条件下成立 |
| Adam 是二阶法 | 不成立；$v_t$ 不是 Hessian，至多在强假设下作尺度 proxy |
| 原始 regret 结论足以保证所有 Adam 轨迹 | 不采用；与 [[S-2018-Reddi-Adam-AMSGrad]] 联读 |
