---
type: solution
status: verified
area: [language-models, evaluation, calibration]
topic: "[[Proper Scoring、Calibration、ECE 与 Selective Generation]]"
exercise: "[[习题 - Proper Scoring、Calibration、ECE 与 Selective Generation]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Proper Scoring、Calibration、ECE 与 Selective Generation

## A. 识别与复述

### LM60-A01
对事件 $Y\in\{0,1\}$ 和预测概率 $P$，总体校准要求
$$
\Pr(Y=1\mid P=p)=p
$$
（严格说是几乎处处或按可测集合定义）。事件可能是“整答正确”或“claim 有支持”，总体可能是某语言/时间用户；换事件或分布，校准命题也随之改变。

### LM60-A02
Brier 是概率与 outcome 的平方误差；log loss 是 outcome 的负对数概率，二者都是 proper scoring rules。ECE 是依分箱的平均置信—准确差，通常不是 proper loss；accuracy 只看离散决策是否正确。它们回答不同问题。

### LM60-A03
Coverage 是系统选择作答的样本比例；selective risk 是在已作答子集上的错误率或损失：
$$R(\tau)=\mathbb E[\ell\mid s(X)\ge\tau].$$
让阈值变化得到 risk–coverage curve；好的置信排序应在相同 coverage 下有更低 risk。

## B. 手算与构造

### LM60-B01
三个平方损失为 $(.8-1)^2=.04$、$(.7-0)^2=.49$、$(.2-0)^2=.04$。平均为 $(.04+.49+.04)/3=.19$。

### LM60-B02
$$
\mathrm{ECE}=\frac{40}{100}|.20-.25|+\frac{60}{100}|.65-.80|
=.4(.05)+.6(.15)=.11.
$$
结果依这两个 bin 的边界；换分箱可能变化。

### LM60-B03
Coverage $.4$ 保留前 2 个，无错误，risk $0$；coverage $.6$ 保留前 3 个，risk $1/3$；coverage $1$ 保留全部，risk $2/5=.4$。

## C. 推导与证明

### LM60-C01
若真实成功率为 $q$，预测 $p$ 的期望 Brier loss 为
$$
q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q).
$$
第二项与 $p$ 无关，第一项非负且只在 $p=q$ 为零，因此 $p=q$ 唯一最优，Brier 对 binary 概率严格 proper。

### LM60-C02
温度缩放把 logits 变为 $z_j/T$，$T>0$ 是共同正比例，所以 $\arg\max_j z_j$ 不变。Softmax 概率却改变，因而正确类的 $-\log p_y$、置信度 bin 和 calibration 可变。它校准概率但不改变 top-1 标签（忽略 tie 与数值边界）。

### LM60-C03
ECE 只保留每个 bin 的样本量、平均置信和平均准确。Bin 内可以一种模型在低端欠置信、高端过置信，另一种处处接近同一偏差，只要 bin 均值相同就得到同 ECE。故不同可靠性函数会映射到同摘要，且边界/样本量会改变值。

## D. 边界、反例与纠错

### LM60-D01
两个系统对同样 50% 正确的样本作相同 hard labels，所以 accuracy 相同。系统 A 对正确/错误分别给 $.6/.4$，系统 B 给 $.99/.99$；B 对错误极度确信，Brier 与 log loss（尤其 log loss）显著更差。

### LM60-D02
ECE 可能因粗分箱、总体平均或样本不足而小；它不衡量代价、OOD、coverage、rare slice、因果后果或恶意攻击。高风险决策还需 proper loss、置信上界、risk–coverage、组别校准、外部分布验证和人工/拒答治理。

### LM60-D03
Token probability 是局部 next-token 事件的概率；整段 factual correctness 是关于多个语义 claims 与外部世界的复合事件。长度、表述变体与 tokenization 都会改变平均值。除非用明确标签对映射做独立校准，否则两者不是同一概率。

## E. AI 迁移

### LM60-E01
表一每 answer 一行，$Y_{\rm ans}$ 表示完整答案满足 rubric，$p_{\rm ans}$ 来自预注册置信模型；表二每 atomic claim 一行，$Y_{\rm sup}$ 表示被证据支持，$p_{\rm sup}$ 对应 claim。两表分别按语言/领域/长度画 reliability、proper loss 和 cluster CI，不能混分母。

### LM60-E02
在 validation 保存 frozen logits 与 labels，只优化一个正温度以最小化 NLL；不得使用 test labels、test prompt 选择结果或上线结果反复调温。锁定 checkpoint、template、class mapping 和 population；最后在独立 test 一次评估。

### LM60-E03
在 validation 扫置信阈值，找满足 risk 上置信界不超过目标（而非只看点估计）的最大 coverage；阈值冻结后在 test 报 coverage、risk、cluster interval、各 slice、拒答原因与代价。若 test 上界越线，决策门失败。
