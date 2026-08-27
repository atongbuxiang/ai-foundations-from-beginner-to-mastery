---
type: solution
status: draft
area: [learning-theory/generalization-certificates, comparison]
topic: "[[习题 - 容量界、稳定性界与 PAC-Bayes 的比较]]"
prerequisites: ["[[容量界、稳定性界与 PAC-Bayes 的比较]]"]
related: ["[[VC 一致收敛与泛化界]]", "[[深度泛化理论的解释对象与证据等级]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - 容量界、稳定性界与 PAC-Bayes 的比较

> [!warning] 比较原则
> 先对齐 output 与 probability quantifier，再比较 numerical right-hand sides；相同 \(\log K\) 不代表相同 guarantee。

## A. 识别与复述

### LT-CERT-A01

| 路线 | complexity | 量词 | 直接保证 |
|---|---|---|---|
| capacity | class/growth/VC/Rademacher | \(\sup_{h\in\mathcal H}\) | 多为 high-probability uniform gap |
| stability | \(A(S)\) 对 \(S\simeq S'\) 的 loss sensitivity | all neighbors，或 expected variants | algorithm-specific expected/tail gap |
| compression | witnesses/code + decoder | all legal descriptions | realizable/agnostic 特定 high-probability risk |
| PAC-Bayes | \(\operatorname{KL}(Q\|P)\) | simultaneous all \(Q\) | high-probability Gibbs-risk certificate |
| MI | \(I(S;W)\) | average joint channel | 基础式 expected signed gap |

### LT-CERT-A02

- valid：assumptions、quantifiers 与 proof 均成立；
- nonvacuous：比 loss/risk 的 trivial range 更有信息；
- tight：数值接近真实 risk/gap；
- explanatory：随机制 intervention 有正确预测，且不易被无关 parameterization 操纵。

一个 bound 可 valid 但 vacuous；可 nonvacuous 却离真实 risk 很远；可 correlation 好却没有 valid theorem。

### LT-CERT-A03

不同 sample unit 改变 \(m\) 与 independence；不同 loss 改变 scale/sub-Gaussian constant；不同 output 可能是 deterministic、Gibbs 或 transcript；不同 randomness 决定 probability space；不同 \(\delta\) 改变 confidence cost。若不统一，两个数字不控制同一命题，排序无意义。

## B. 手算与数值判断

### LT-CERT-B01

$$
\log|\mathcal H|
=\log1024
=10\log2
\approx\boxed{6.93147\text{ nats}}.
$$

uniform prior 下 point posterior：

$$
\operatorname{KL}(\delta_h\|P)
=\log1024
=6.93147.
$$

10-bit output：

$$
I(S;W)\le10\log2=6.93147.
$$

但分别对应 uniform high-probability class event、PAC-Bayes posterior/Gibbs event、expected signed channel bound；denominator、empirical term 与 constants 也不同。

### LT-CERT-B02

等分：

$$
\delta_j=0.04/4=\boxed{0.01}.
$$

额外 confidence cost：

$$
\log\frac1{0.01}
-\log\frac1{0.04}
=\log4
\approx\boxed{1.38629\text{ nats}}.
$$

### LT-CERT-B03

若

$$
\left|\mathbb E[R(A(S))-\widehat R_S(A(S))]\right|\le0.01
$$

且题中的 \(0.35\) 是可与 expectation 正确对齐的 deterministic/expected empirical risk，则可说

$$
\mathbb ER(A(S))
\le0.35+0.01
=\boxed{0.36}.
$$

不能说 risk 小于 \(0.01\)：\(0.01\) 控制的是 train–population 差，不是 risk 本身。若 \(0.35\) 只是一批 realized sample 的 empirical value，还不能无条件把它代入纯 expectation theorem。

## C. 推导与证明

### LT-CERT-C01

假设相关绝对连续性成立。写

$$
\log\frac{dP_{W\mid S}}{dP}
=
\log\frac{dP_{W\mid S}}{dP_W}
+\log\frac{dP_W}{dP}.
$$

对 \(P_{S,W}\) 取 expectation：

$$
\begin{aligned}
\mathbb E_S\operatorname{KL}(P_{W\mid S}\|P)
&=
\mathbb E_{S,W}\log\frac{dP_{W\mid S}}{dP_W}
+\mathbb E_W\log\frac{dP_W}{dP}\\
&=
I(S;W)+\operatorname{KL}(P_W\|P).
\end{aligned}
$$

所以 \(P=P_W\) 最小化 average posterior-to-reference KL，但 \(P_W\) 依赖未知 data law，未必是可声明 prior。

### LT-CERT-C02

令

$$
E_j=\{R\le B_j(S,\delta_j)\},
\qquad
\mathbb P(E_j^c)\le\delta_j.
$$

union bound：

$$
\mathbb P\left(\bigcap_jE_j\right)
\ge
1-\sum_j\delta_j
\ge1-\delta.
$$

在 \(\cap_jE_j\) 上每个 bound 同时有效，因此

$$
R\le B_j\quad\forall j
\Longrightarrow
R\le\min_jB_j.
$$

这要求所有 \(B_j\) 控制同一 \(R\)/predictor；若 predictors 不同，选择后的 risk statement 也要写成 \(R(h_{\hat j})\) 并确保 joint events 覆盖全部 \(j\)。

### LT-CERT-C03

离散 \(h\) 取 \(Q=\delta_h\)。则

$$
\operatorname{KL}(\delta_h\|P)
=\log\frac1{P(h)}.
$$

代入 PAC-Bayes：

$$
\operatorname{kl}(\widehat R_S(h)\|R(h))
\le
\frac{
\log(1/P(h))+\log((m+1)/\delta)
}{m}.
$$

weighted union bound 给每个 \(h\) failure budget \(\delta P(h)\)，其 confidence term也是

$$
\log\frac1{\delta P(h)}
=\log\frac1\delta+\log\frac1{P(h)}.
$$

两者 description penalty 一致，但 fixed-h concentration 的具体 scalar divergence/constants 可不同。

## D. 边界、反例与纠错

### LT-CERT-D01

常数算法

$$
A(S)=h_0
$$

完全不依赖 \(S\)，所以 uniform stability \(\beta_m=0\)。若 data law 下 \(h_0\) 总是预测错误，

$$
R(h_0)=1.
$$

同时 empirical risk expectation 也是 \(1\)，generalization gap 恰为零。它完美泛化“差的性能”，说明 gap certificate 还需 low empirical risk/approximation guarantee 才成为 learning guarantee。

### LT-CERT-D02

构造：在 probability \(1-\varepsilon\) 的典型 samples 上输出固定 \(w_0\)；在一个概率 \(\varepsilon\) 的 rare event \(E(S)\) 上输出完整编码 \(c(S)\)。当 \(\varepsilon\) 很小时 average MI 可按 \(\varepsilon H(S)\) 量级小，但在跨越 \(E\) 边界的一对 neighboring samples 上 output 从 \(w_0\) 跳到完整 sample code，worst-case sensitivity 巨大。

### LT-CERT-D03

VC theorem 是关于指定 class、i.i.d. data 与 uniform convergence 的逻辑命题。深网 class 的 VC upper bound vacuous 说明：

- class 太大或 scale 太粗；
- sample size 不足以覆盖 worst case；
- actual algorithm/data geometry 未被利用。

它不构成 theorem 的反例。更合理结论是：plain worst-case VC capacity 对当前 deep-learning phenomenon 的 explanatory scope 有限，需要 norm/margin/localization/stability/compression/PAC-Bayes 等附加结构。

## E. AI 迁移

### LT-CERT-E01

- regularized logistic regression：首选 stability（strong convexity）；备选 norm-based Rademacher；
- quantized tree：首选 description-length/Occam 或 compression；备选 finite-class/MI，前提是完整 codebook 固定；
- stochastic neural ensemble：首选 PAC-Bayes；备选 MI/noisy-channel analysis；
- adaptive hyperparameter agent：首选 transcript MI/reusable validation；备选 predeclared finite union/SRM。

每个选择仍需核对 loss、data reuse 与 output。

### LT-CERT-E02

benchmark 至少报告：

1. dataset/distribution；
2. sample unit 与 \(m\)；
3. algorithm/output；
4. loss/range；
5. empirical risk；
6. certificate family；
7. complexity value/units；
8. assumptions；
9. confidence budget \(\delta_j\)；
10. bound type（risk/gap，expectation/tail）；
11. result；
12. trivial baseline/nonvacuity；
13. computation/MC error；
14. parameterization；
15. deployment match；
16. code/data/seed hashes。

规则：训练前固定 certificate list 与 \(\delta_j\)，使 \(\sum_j\delta_j\le\delta\)；若新增 certificate，重新分配预算或使用新的 independent evaluation。

### LT-CERT-E03

五条可证伪问题：

1. capacity：控制 spectral/path norms 与 margins 后，随 width 增长的 empirical Rademacher/margin bound 是否保持或改善？reparameterization 是否破坏趋势？
2. stability：替换一个 document/user 并 coupled retrain，prediction-loss difference 是否随 \(m\) 按理论率下降？训练时长是否放大它？
3. compression：完整 model（architecture、weights、tokenizer）能否以预声明 decoder 和 \(b\) bits 重构，同时保持 empirical loss；bound 是否随 \(b\) 预测 test gap？
4. PAC-Bayes：independent pretrained prior 周围是否存在 noisy posterior，使 empirical Gibbs risk 与 KL 同时给 nonvacuous certificate；center/vote 与 Gibbs gap 多大？
5. MI：在明确 stochastic/quantized release channel 下，能否给 \(I(S;W)\) 的可验证 upper bound；降低 channel information 是否产生预言的 expected-gap 改善而不过度损伤 risk？

每条都包含 mechanism intervention、measurable outcome 与可能证伪的结果，而非只计算静态数字。
