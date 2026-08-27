---
type: source
status: verified
area: [sources, ai/optimization, math/curvature]
source_type: blog
title: "从 Hessian 近似看自适应学习率优化器"
author: 苏剑林
year: 2024
url: "https://spaces.ac.cn/archives/10588"
accessed: 2026-08-19
source_tier: C
license: "科学空间页面声明 CC BY-NC-SA；本库仅保存独立摘要、必要短公式与链接"
site_category: [数学研究]
scope_role: supporting
temporal_role: research-exposition
related: ["[[自适应优化方法]]", "[[Hessian、二阶微分与曲率]]", "[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[非凸优化、鞍点与深度网络损失地形]]", "[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[GGN、经验 Fisher 与曲率近似陷阱]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 从 Hessian 近似看自适应学习率优化器

> [!abstract] 来源定位
> 文章提出一个有价值的解释视角：在最优点附近线性化 gradient，并对参数偏移作近似 isotropic 的长期平均时，gradient outer-product 的期望可与 Hessian square 联系，从而帮助理解 RMSProp/Adam 的平方梯度 EMA 为什么可能携带 curvature scale。课程采用这条“条件性联系”，但不把它表述为 Adam 等于 Newton。

## 元数据与纳入

- 正式引用：苏剑林，2024-11-29，《从 Hessian 近似看自适应学习率优化器》；
- 原始页面：[https://spaces.ac.cn/archives/10588](https://spaces.ac.cn/archives/10588)；
- 当前调用者：[[Hessian、二阶微分与曲率]]、[[自适应优化方法]]、[[Newton 法、Gauss-Newton 与拟 Newton 法]]、[[非凸优化、鞍点与深度网络损失地形]]；
- 只纳入 gradient-square、time averaging、diagonal Hessian scale 与 adaptive optimizer 有关内容。

## 推导骨架

在 $\theta^*$ 附近：

$$
g_\theta\approx H_*(\theta-\theta^*).
$$

若进一步假设

$$
\mathbb E[(\theta-\theta^*)(\theta-\theta^*)^T]
\approx\sigma^2I,
$$

则

$$
\mathbb E[g_\theta g_\theta^T]
\approx\sigma^2H_*H_*^T.
$$

在 $H_*$ symmetric PSD、坐标与 eigenbasis 近似对齐并只取 diagonal 时，$\sqrt{\mathbb E[g_i^2]}$ 才可解释为 curvature scale proxy。

## 核心断言与课程判断

| ID | 断言 | 类型 | 必须保留的条件 | 判断 |
|---|---|---|---|---|
| C1 | gradient-square 长期平均含 curvature 信息 | local heuristic | 线性化、近最优、稳定 Hessian、轨迹分布 | 有条件采用 |
| C2 | square root 与 Hessian scale 联系 | 矩阵关系 | isotropy、PSD、matrix/diagonal distinction | 有条件采用 |
| C3 | Adam 可视作近似二阶法 | 解释性类比 | 不能恢复 off-diagonal/eigenvectors/sign | 不作算法等价 |
| C4 | $\beta_2$ 应比 $\beta_1$ 长期 | 设计直觉 | 非平稳性、任务与稳定性依赖 | 作为实验假设 |

## 与经典二阶近似的区分

- Hessian：objective 的二阶导；
- GGN：模型 Jacobian 与 loss output curvature；
- empirical Fisher：样本 score outer products；
- Adam $v_t$：沿训练轨迹、带抽样噪声与 forgetting 的 coordinate raw second moments。

它们在特定条件下有关，不能仅因都出现 outer product 或平方就互换。

## 限制与最小验证

1. 在 known quadratic 上改变 Hessian eigenbasis 与坐标轴夹角；
2. 改变 noise covariance 和 trajectory anisotropy；
3. 比较 $\sqrt{\operatorname{EMA}(g^2)}$、$\operatorname{diag}(H)$ 和 $\operatorname{diag}(H^2)^{1/2}$；
4. 扫描 $\beta_2$ 与 nonstationarity；
5. 报 off-diagonal energy 与 approximation error；
6. 不用训练成功反推 Hessian approximation 正确。

## 已生成与后续调用

- [x] [[Hessian、二阶微分与曲率]]：Hessian/outer-product 关系的假设审计；
- [x] [[自适应优化方法]]：Adam 近似二阶解释与严格边界；
- [x] [[Newton 法、Gauss-Newton 与拟 Newton 法]]：与 exact Hessian、GGN/Fisher、Gauss–Newton 和 secant curvature 对照，并明确不作算法等价。
- [x] [[非凸优化、鞍点与深度网络损失地形]]：作为 curvature diagnostic/自适应尺度的中文问题入口；negative curvature、SOSP 与 escape theorem 由正式原论文补严。
