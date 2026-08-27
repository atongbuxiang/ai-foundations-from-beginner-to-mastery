---
type: exercise
status: draft
area: [math/information-theory, ai/losses, ai/generative-models]
topic: "交叉熵与 KL 散度"
difficulty: [A, B, C, D, E]
prerequisites: ["[[交叉熵与 KL 散度]]"]
related: ["[[信息论与统计学习接口 MOC]]", "[[练习与测验 MOC]]"]
solution: "[[解答 - 交叉熵与 KL 散度]]"
created: 2026-08-19
updated: 2026-08-19
---

# 习题 - 交叉熵与 KL 散度

> [!abstract] 训练目标
> 从平均错误码长重建 KL decomposition 与 Gibbs inequality；能处理方向、支撑、Gaussian 公式、logits 稳定计算、模型错设和现代 AI surrogate 的对象边界。

## A. 识别与复述

### INFO-KL-A01

分别定义 $H(P)$、$H(P,Q)$ 与 $D(P\|Q)$，说明 expectation 在哪个 distribution 下取，并证明三者的代数关系。何时某一项为 $+\infty$？

### INFO-KL-A02

逐项判断并纠正：“KL 对称”“KL 满足三角不等式”“KL 的平方根总是 metric”“symmetric KL 就是 Jensen–Shannon divergence”“$D(P\|Q)=0$ 只说明均值相同”。

### INFO-KL-A03

解释经验 NLL、empirical cross-entropy、MLE、population cross-entropy 与 misspecified KL projection 的关系。列出从经验最小到泛化至少还缺的四类条件/误差。

## B. 手算与构造

### INFO-KL-B01

$P=\operatorname{Ber}(0.8)$，$Q=\operatorname{Ber}(0.6)$。以 bits 计算 $H(P)$、$H(P,Q)$、$D_2(P\|Q)$ 和 $D_2(Q\|P)$，核对 decomposition 与不对称性。

### INFO-KL-B02

三分类 logits 为 $z=(2,0,-1)$，target 为第一类。用稳定 logsumexp 计算 probability、loss 和 $\nabla_z\ell$（保留三位小数）；写出 Hessian 形式并验证全一向量是零方向。

### INFO-KL-B03

$P=N(0,1)$，$Q=N(1,4)$。计算 $D(P\|Q)$ 与 $D(Q\|P)$（nats）。分别指出 mean mismatch 与 variance mismatch 在公式中的位置。

## C. 推导与证明

### INFO-KL-C01

从 $\log t\le t-1$ 证明 Gibbs inequality，处理 zero-probability cases，并给出 equality condition。再推出 cross-entropy lower bound。

### INFO-KL-C02

证明 joint KL chain rule：

$$
D(P_{XY}\|Q_{XY})
=D(P_X\|Q_X)+E_{P_X}D(P_{Y\mid X}\|Q_{Y\mid X}).
$$

扩展到 autoregressive sequence，并说明 prefix expectation 为什么在 $P$ 下而不是 $Q$ 下。

### INFO-KL-C03

从多元 Gaussian log density 出发推导

$$
D(N_p\|N_q)=\frac12\left[
\operatorname{tr}(\Sigma_q^{-1}\Sigma_p)
+(\mu_q-\mu_p)^\top\Sigma_q^{-1}(\mu_q-\mu_p)
-d+\log\frac{\det\Sigma_q}{\det\Sigma_p}
\right].
$$

解释 SPD 条件、奇异 support 边界和 Cholesky 实现方式。

## D. 边界、反例与纠错

### INFO-KL-D01

取 Bernoulli success probabilities $p=0.1,q=0.2,r=0.9$。计算 $D(P\|R)$、$D(P\|Q)$、$D(Q\|R)$，给出违反 triangle inequality 的数值证据。

### INFO-KL-D02

模型实现先把每个 probability 截断为 $\max(q_i,10^{-4})$，不重新归一化，再计算“KL”。指出至少三处数学/实现问题；给出一个既保留稳定性又诚实报告 objective 的方案。

### INFO-KL-D03

目标为

$$
P=(0.49,0.02,0.49),
$$

候选为

$$
Q_c=(0.25,0.50,0.25),\qquad Q_m=(0.98,0.02,0).
$$

比较 forward KL $D(P\|Q)$ 与 reverse KL $D(Q\|P)$ 的候选选择，解释 support penalty 与 mode-seeking 口号在这个有限例子中的准确含义。

## E. AI 迁移

### INFO-KL-E01

蒸馏使用 temperature $\tau$：teacher/student logits 分别除以 $\tau$ 后计算 $H(p_T^{(\tau)},q_S^{(\tau)})$。证明固定 teacher 时它等价于 forward KL 加常数；分析 $\tau$ 增大时分布与 logit gradient 尺度，并解释实践中乘 $\tau^2$ 的动机与边界。

### INFO-KL-E02

某模型输出形状 `[batch, entity_type, start, end]` 的未归一化 logits。作者沿所有轴直接计算“symmetric categorical KL”。写一份对象审计：至少给出 categorical、factorized Bernoulli 与 logit consistency 三种可选建模方式，并说明它们为何不是同一个目标。

### INFO-KL-E03

一个不平衡分类器使用 class-weighted focal loss，并把训练 loss 下降解释为“部署分布 KL 下降且概率更校准”。写一份审稿意见，至少审计 target measure、proper scoring、class prior、reduction、held-out NLL、calibration、threshold 与 distribution shift。

## 分级提示

- `B02`：先取 $m=2$，计算 $m+\log(1+e^{-2}+e^{-3})$；
- `C02`：把 density ratio 分为 marginal ratio 与 conditional ratio；
- `D01`：全部使用 natural log，并保留至少三位小数；
- `D03`：$D(P\|Q_m)=+\infty$，而 reverse direction 不对 $P$ 的未覆盖第三类直接取 expectation；
- `E01`：softmax 对 logits 的 Jacobian 带 $1/\tau$。

## 解答入口

完成独立尝试后再打开：[[解答 - 交叉熵与 KL 散度]]。
