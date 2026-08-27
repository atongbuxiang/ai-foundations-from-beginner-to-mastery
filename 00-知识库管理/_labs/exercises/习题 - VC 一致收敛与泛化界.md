---
type: exercise
status: draft
area: [learning-theory/vc, probability/uniform-convergence]
topic: "[[VC 一致收敛与泛化界]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[Sauer-Shelah 引理]]", "[[不可知 PAC、ERM 与双侧一致收敛]]", "[[浓缩不等式]]"]
related: ["[[解答 - VC 一致收敛与泛化界]]", "[[二分类统计学习基本定理]]", "[[Ghost Sample、对称化与经验过程入口]]"]
solution: "[[解答 - VC 一致收敛与泛化界]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - VC 一致收敛与泛化界

> [!abstract] 训练目标
> 能独立重建 ghost sample—random swap—pattern count—Hoeffding 证明，追踪常数并把 uniform gap 正确转成 ERM excess，同时判断 bound 的假设与数值有效性。

## A. 识别与复述

### LT-VCUC-A01

陈述本笔记采用的 VC inequality，包括数据、loss、class、$m\varepsilon^2$ 条件和 failure probability。常数 4 的两个因子 2 分别来自哪里？

### LT-VCUC-A02

ghost sample $S'$ 与训练样本 $S$ 必须满足什么关系？它在证明中做什么，算法在部署时是否需要它？

### LT-VCUC-A03

解释 pointwise convergence、uniform convergence 和 ERM excess guarantee 三者的蕴含链，并指出每一步多用了什么。

## B. 手算与数值判断

### LT-VCUC-B01

取 $d=2,m=10000,\delta=0.05$，用

$$
\gamma_m=
\sqrt{\frac8m\left[d\log\frac{2em}{d}+\log\frac4\delta\right]}
$$

计算 uniform gap 上界和 exact ERM excess 上界。

### LT-VCUC-B02

若已知 $\tau_{\mathcal H}(2m)\le500$、$m=2000$、$\delta=0.05$，不经过 VC 维粗化，计算 growth-function radius。

### LT-VCUC-B03

固定 $\varepsilon=0.2$、$\tau_{\mathcal H}(2m)\le100$。分别在 $m=500$ 和 $m=5000$ 时计算

$$
4\tau_{\mathcal H}(2m)e^{-m\varepsilon^2/8},
$$

并解释 failure upper bound 大于 1 时应怎样读。

## C. 推导与证明

### LT-VCUC-C01

用 variance bound $\operatorname{Var}(f(Z))\le1/4$ 和 Chebyshev 完整证明双样本对称化：当 $m\varepsilon^2\ge2$ 时，

$$
P\left(\sup_f|P-P_m|>\varepsilon\right)
\le2P\left(\sup_f|P_m-P_m'|>\varepsilon/2\right).
$$

### LT-VCUC-C02

条件于 pooled sample，证明对固定 error pattern

$$
P_\sigma\left(\left|m^{-1}\sum_i\sigma_i a_i\right|>\varepsilon/2\right)
\le2e^{-m\varepsilon^2/8},
$$

并说明为什么 Union Bound 的项数不超过 $\tau_{\mathcal H}(2m)$。

### LT-VCUC-C03

设 $\widetilde h_S$ 是 $\rho$-approximate ERM，uniform event 上 $\sup_h|R_P(h)-R_S(h)|\le\gamma$。完整推导

$$
R_P(\widetilde h_S)-\inf_{h\in\mathcal H}R_P(h)
\le2\gamma+\rho,
$$

包括 infimum 不取到时的处理。

## D. 边界、反例与纠错

### LT-VCUC-D01

纠正：“只需对原训练样本上的 $\tau(m)$ 个 patterns 做 Union Bound，所以 theorem 中的 $2m$ 是多余的。”

### LT-VCUC-D02

纠正：“ghost sample 是额外验证集；没有第二份真实数据就不能使用 VC theorem。”

### LT-VCUC-D03

构造或描述 train law $P$ 与 deployment law $Q\ne P$，使 VC uniform convergence 对 $R_P$ 完全成立但 $R_Q$ 很差。指出 theorem 的哪条假设/目标没有覆盖 shift。

## E. AI 迁移

### LT-VCUC-E01

冻结 encoder，训练 VC 维至多 129 的 binary linear head。给定 $m=50000,\delta=0.01$，写出可直接代入的 uniform radius 公式；说明若 encoder 也用这批 labels fine-tune，为什么该公式的 class 定义失效。

### LT-VCUC-E02

团队在同一 2000 题 benchmark 上自适应生成 10 万个 prompts，最后挑最佳者。说明 finite/VC uniform proof 要怎样重新定义 class 才可能覆盖流程，并给出更稳妥的 evaluation 设计。

### LT-VCUC-E03

某深网 VC bound 代入后得到 uniform gap 7.3，而实际 gap 是 0.02。分别判断 theorem 是否错误、bound 是否有预测力、下一步应研究哪些更细结构。

## 分级提示

- `B01`：$\log(10000e)\approx10.2103$，$\log80\approx4.3820$；
- `B03`：先注意概率上界最终可与 1 取最小；
- `C01`：对每个坏 $S$ 选择一个 witness $f_S$；
- `C02`：$a_i\in\{-1,0,1\}$，Hoeffding range length 至多 2；
- `C03`：用一个 $\eta$-optimal comparator，最后令 $\eta\downarrow0$；
- `D03`：可让 $Q$ 的质量集中在 $P$ 几乎不见、模型系统性出错的区域。

## 解答入口

完成独立尝试后再打开：[[解答 - VC 一致收敛与泛化界]]。
