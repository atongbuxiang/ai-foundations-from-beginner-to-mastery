---
type: source
status: active
area: [sources, neural-networks/normalization, rmsnorm]
source_type: paper
title: "Root Mean Square Layer Normalization"
author: "Biao Zhang; Rico Sennrich"
year: 2019
url: "https://proceedings.neurips.cc/paper/2019/hash/1e8a19426224ca89e83cef47f1e7f53b-Abstract.html"
arxiv: "1910.07467"
venue: "NeurIPS 2019"
accessed: 2026-08-23
source_tier: A
license: "NeurIPS author paper；本库仅保存独立摘要、短公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[RMSNorm、均值移除与缩放不变性]]", "[[LayerNorm 的逐样本几何与反向传播]]", "[[小批量、混合精度、分布式与因果归一化边界]]"]
created: 2026-08-23
updated: 2026-08-29
---

# Zhang–Sennrich：RMSNorm

> [!abstract] 来源定位
> 论文提出只用 root mean square、删除 mean centering 的 LayerNorm 变体。它是 RMSNorm 的定义与原始经验来源；本库另外独立推导 Jacobian、VJP、谱、不变性及 epsilon 边界，不把原论文的特定运行时间和任务结果外推为现代硬件上的普遍收益。

## 核心对象

对一组 $D$ 维输入，论文核心算子是

$$
r=\sqrt{\frac1D\sum_{j=1}^D x_j^2+\varepsilon},
\qquad
y_i=\gamma_i\frac{x_i}{r}.
$$

它与 LayerNorm 的结构差别不是“少算一个常数”，而是删除 centering projection：RMSNorm 保留共同平移方向的信息，只对径向尺度进行归一。

## 断言表

| ID | 断言 | 类型 | 条件/证据 | 本库判断 |
|---|---|---|---|---|
| RMS-C1 | RMSNorm 不执行 re-centering | 定义 | 原论文公式 | 已建立 |
| RMS-C2 | 正尺度重缩放在 $\varepsilon=0$ 时被抵消 | 数学性质 | 非零输入、正尺度 | 独立核验 |
| RMS-C3 | pRMSNorm 可用坐标子集估计 RMS | 方法 | subset 规则与采样条件需声明 | 有条件成立 |
| RMS-C4 | 删除均值计算可降低某些实现开销 | 系统/经验 | kernel、shape、memory traffic 与硬件相关 | 不作普遍保证 |
| RMS-C5 | 原论文任务上与 LayerNorm 表现可比 | 经验 | 论文模型、数据和训练设置 | 不跨设置外推 |

## 本库补出的理论

令 $\widehat x=x/r$，则无 affine Jacobian 为

$$
J=\frac1r\left(I-\frac1D\widehat x\widehat x^{\mathsf T}\right).
$$

与 LayerNorm 相比，它没有 $I-\boldsymbol1\boldsymbol1^{\mathsf T}/D$ 的 centering projection。$\varepsilon=0$ 时只有径向零方向；LayerNorm 还多删除共同平移方向。

## 证据边界

- “不需要 re-centering”是论文假说加特定实验支持，不是对所有架构的定理；
- RMSNorm 不保证输出均值为零；
- pRMSNorm 的 subset 估计引入统计误差，不能只按计算量评价；
- 当前库不复述论文的百分比加速为现代 GPU 结论；
- 实现默认 epsilon、是否含 bias 和 accumulation dtype 必须另查框架版本。
