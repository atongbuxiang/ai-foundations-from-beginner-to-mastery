---
type: theorem
status: draft
area: [learning-theory/domain-adaptation, domain-generalization, discrepancy]
aliases: [H-Delta-H Bound, Domain Adversarial Learning, Domain Generalization]
node_id: LT-67
prerequisites: ["[[Covariate、Label 与 Concept Shift]]", "[[二分类统计学习基本定理]]", "[[打散、增长与 VC 维]]", "[[表示学习的任务、表示与下游风险]]"]
related: ["[[重要性加权与 Covariate Shift 校正]]", "[[OOD、鲁棒性与因果不变性的边界]]"]
sources: ["[[S-2010-BenDavid-Domain-Adaptation]]", "[[S-2016-Ganin-DANN]]", "[[S-2019-Zhao-Invariant-DA]]", "[[S-2021-Gulrajani-Domain-Generalization]]", "[[S-2021-Koh-WILDS]]"]
exercises: ["[[习题 - Domain Adaptation 与 Domain Generalization Bound]]"]
solutions: ["[[解答 - Domain Adaptation 与 Domain Generalization Bound]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-domain-adaptation-bound-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Domain Adaptation 与 Domain Generalization Bound

> [!abstract] 本章主问题
> 经典 adaptation bound 把 target error 分为 source error、hypothesis-relative domain discrepancy 与“两个域是否共享好预测器”的 $\lambda$。只做 domain confusion 主要控制中间项；若 $\lambda$ 大或表示删掉标签信息，域越不可分也可能越糟。

## 一、学习目标

完成本章后，应能：

1. 区分 domain adaptation 与 domain generalization；
2. 定义 $\mathcal H\Delta\mathcal H$ divergence；
3. 逐步证明经典 target-risk bound；
4. 解释 $\lambda$ 的 task-compatibility 含义；
5. 从 domain-classifier error 解释 proxy distance；
6. 写 DANN 的 min–max objective；
7. 构造 domain-invariant 但 label-useless representation；
8. 区分 input、marginal、conditional 与 label alignment；
9. 审计 DG model selection 泄漏；
10. 设计 multi-domain、shift 与 compute 公平评估。

## 二、DA 与 DG 的数据合同

- unsupervised domain adaptation：source labeled + target unlabeled，目标是 target labeled risk；
- semi-supervised DA：另有少量 target labels；
- domain generalization：训练时只有多个 source environments，目标域不可见；
- test-time adaptation：部署时允许更新，需声明 batches、labels/feedback 与安全边界。

把 target validation 用于选模型后，实验不再是纯 DG。

## 三、$\mathcal H\Delta\mathcal H$ Divergence

对二分类 hypothesis class $\mathcal H$，对 input marginals $P_s^X,P_t^X$：

$$
\boxed{
d_{\mathcal H\Delta\mathcal H}(P_s^X,P_t^X)
=
2\sup_{h,h'\in\mathcal H}
\left|
\Pr_s(h(X)\ne h'(X))
-
\Pr_t(h(X)\ne h'(X))
\right|.
}
$$

它只测 $\mathcal H$ 能表达的 disagreement events，不是分布的绝对几何距离。换表示 $\Phi$ 或换 class，数值就变。

## 四、Joint Ideal Error

定义

$$
\boxed{
\lambda_{\mathcal H}
=
\min_{h\in\mathcal H}
\left(R_s(h)+R_t(h)\right).
}
$$

若存在一个 hypothesis 同时适合两域，$\lambda$ 小；label rules 冲突、表示丢信息或 class 太弱时 $\lambda$ 大。它依赖 target labels，通常不能由 unsupervised DA data 直接估计。

## 五、经典 Bound

对任意 $h\in\mathcal H$：

$$
\boxed{
R_t(h)
\le
R_s(h)
+
\frac12d_{\mathcal H\Delta\mathcal H}(P_s^X,P_t^X)
+
\lambda_{\mathcal H}.
}
$$

### 5.1 证明

令

$$
h^*=\arg\min_{g\in\mathcal H}[R_s(g)+R_t(g)].
$$

用 0–1 loss 的逐点 triangle：

$$
R_t(h)\le R_t(h^*)+\Pr_t(h\ne h^*).
$$

由 divergence 定义：

$$
\Pr_t(h\ne h^*)
\le
\Pr_s(h\ne h^*)+\frac12d_{\mathcal H\Delta\mathcal H}.
$$

又有

$$
\Pr_s(h\ne h^*)\le R_s(h)+R_s(h^*).
$$

合并得到结论。经验版还要用 source labeled sample 与 source/target unlabeled samples 估计各项，并加入 VC/Rademacher complexity。

## 六、为什么不能删掉 $\lambda$

设两个域 $X$ 分布完全相同，故 divergence 为 0；source label 为 $Y=X$，target label 为 $Y=1-X$。任意同一 classifier 至少在一个域错，$\lambda$ 大。只看 domain discrepancy 会错误预测可迁移。

这也是 “marginal alignment” 不足的最短反例。

## 七、Domain Classifier Proxy

给 source/target domain labels，若 equal priors 且 discriminator family 对应 $\mathcal H\Delta\mathcal H$，最佳 domain classification error 为 $\epsilon$，常用 proxy：

$$
\widehat d_A=2(1-2\epsilon).
$$

- $\epsilon=1/2$：域不可分，proxy 0；
- $\epsilon=0$：完全可分，proxy 2。

finite sample、capacity、optimization 与 calibration 都影响 $\epsilon$；低 proxy 不说明 $\lambda$ 小。

## 八、DANN Objective

feature extractor $\Phi_\theta$、source label head $g_\omega$、domain head $d_\psi$：

$$
\min_{\theta,\omega}\max_{\psi}
\left[
\widehat R_{\rm label}(\theta,\omega)
-
\gamma\widehat R_{\rm domain}(\theta,\psi)
\right].
$$

gradient reversal 让 $\theta$ 增大 domain-head loss，同时 label head 降 source error。$\gamma$、domain balance、head capacity 与 optimization path 定义实际 tradeoff。

## 九、Invariant 但无用的表示

常数表示

$$
\Phi(X)\equiv0
$$

使 source/target feature distributions 完全相同，却删除所有 label information。更隐蔽地，若 label prevalence 不同，强 marginal alignment 可把不同 classes 错误配对，增加 target risk。

因此至少同时监控 source label sufficiency、class-conditional structure 与 target pseudo-label sensitivity。

## 十、Conditional Alignment 的循环

想匹配

$$
P_s(\Phi(X)\mid Y)
\approx
P_t(\Phi(X)\mid Y)
$$

需要 target labels；用 pseudo-labels 又依赖当前模型正确。应报告 confidence threshold、class balance、error amplification 与 oracle-label upper bound，不能把 pseudo conditional alignment 当真条件分布。

## 十一、Domain Generalization 的额外困难

DG 没有当前 target inputs，无法直接估计 source–target discrepancy。它必须假设：

- target 来自某个 environment family；
- invariant mechanism/feature 存在；
- source environments 足够多样；
- selection rule 能由 source data选择可迁移模型。

有限环境上不变，不推出所有未见干预不变。

## 十二、Model Selection 与 Benchmark Hygiene

必须区分：

1. source IID validation；
2. leave-one-source-domain-out validation；
3. target-domain oracle validation；
4. test-domain repeated tuning。

第 3/4 类可用于 upper bound 或 adaptation setting，但不能标为 target-blind DG。统一 augmentation、architecture、pretraining、search budget 与 seeds 后再比较算法。

## 十三、图：Bound 的三账户

先看图回答：若 domain classifier 已降到 chance，target accuracy 仍差，bound 中最可能被忽略的是哪一项？

![[00-知识库管理/_assets/figures/learning-theory/fig-domain-adaptation-bound-v2.svg|900]]

> [!figure] 图 20.8-07　Source risk、domain discrepancy 与 joint ideal error
> 左栏给出 bound 的 disagreement 证明；中栏连接 domain classifier/DANN 与表示对齐；右栏展示 $\lambda$、常数表示、DG selection 与 target-blind 边界。来源：依据 Ben-David et al.、Ganin et al.、Zhao et al. 与 Gulrajani–Lopez-Paz 独立绘制；由 [[plot_distribution_shift_v2.py]] 确定性生成。

**怎样读图**：DANN 主要作用于 discrepancy proxy；source label loss 防止明显 collapse；$\lambda$ 与 unseen environment assumptions 仍需额外证据。

**图没有证明什么**：图没有证明低 domain-classifier accuracy 导致低 target risk，也没有证明 finite-source invariance 是 causal invariance。

## 十四、常见错误与 AI 接口

- 把 DA 与 DG 混称；
- 省略 $\lambda$；
- 常数表示当成功 alignment；
- 用 target test 调 DG；
- 不报 ERM 与 pretrained baseline；
- 多模态/LLM 中把 topic/domain classifier confusion 当语义保持；
- 医疗中忽略 hospital-specific label policy；
- 只报平均域，不报 worst domain。

## 十五、最小记忆

> [!summary]
> - target risk bound 有 source risk、discrepancy、$\lambda$ 三项；
> - discrepancy 相对于 hypothesis/representation；
> - domain confusion 不控制 shared labeling compatibility；
> - DANN 是具体 min–max algorithm，不是 bound 自动最小化器；
> - DG 没有 target inputs，依赖更强 environment assumptions；
> - model selection protocol 决定 claim 是否真 target-blind。

## 十六、掌握标准

### A. 定义
能定义 DA/DG、$\mathcal H\Delta\mathcal H$ 与 $\lambda$。
### B. 推导
能逐步证明三项 bound 与 domain-proxy relation。
### C. 反例
能构造 divergence 0 但 target error 高、常数 invariance。
### D. 实验
能设计 ERM/DANN/DG 的 target-blind selection 与 worst-domain 报告。
### E. 迁移
能说明 foundation model 的域对齐证据不能自动支持因果或通用迁移。

## 十七、练习与独立详解

- [[习题 - Domain Adaptation 与 Domain Generalization Bound]]
- [[解答 - Domain Adaptation 与 Domain Generalization Bound]]

## 参考来源

- [[S-2010-BenDavid-Domain-Adaptation]]
- [[S-2016-Ganin-DANN]]
- [[S-2019-Zhao-Invariant-DA]]
- [[S-2021-Gulrajani-Domain-Generalization]]
- [[S-2021-Koh-WILDS]]
