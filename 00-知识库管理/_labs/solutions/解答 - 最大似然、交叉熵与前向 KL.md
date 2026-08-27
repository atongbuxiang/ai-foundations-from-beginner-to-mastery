---
type: solution
status: draft
area: [generative-models, likelihood]
topic: "[[最大似然、交叉熵与前向 KL]]"
exercise: "[[习题 - 最大似然、交叉熵与前向 KL]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - 最大似然、交叉熵与前向 KL

## A. 识别与复述

### GEN03-A01
$L_n=\prod_i p_\theta(x_i)$，$\ell_n=\sum_i\log p_\theta(x_i)$，$\widehat R_n=-n^{-1}\ell_n$，$R=\mathbb E_{P_*}[-\log p_\theta(X)]$。前三者随抽到的数据集变化；给定 $P_*$ 和模型族后，population risk 是确定函数。训练随机性还会使最终 $\hat\theta$ 随 seed 变化。

### GEN03-A02
准确说法是：在 $P_*\ll P_\theta$、共享参考测度、相关 log density 可积且 $P_*$ 固定时，population NLL 与 $D_{KL}(P_*\Vert P_\theta)$ 相差 $H(P_*)$，故 argmin 相同。它不是有限样本 loss 数值相等，也不消除模型错设与优化误差。

### GEN03-A03
Approximation：模型族最近分布仍离 $P_*$ 多远；estimation：经验目标逼近总体目标的误差；optimization：算法离所选目标最优值多远；protocol：mask、去量化、缩放等是否定义了预期 estimand；sampling：实际 $Q_{\theta,\phi}$ 离 $P_\theta$ 多远。

## B. 手算与建模

### GEN03-B01
$n=15$，Bernoulli MLE $\hat q=10/15=2/3$。平均 NLL 为

$$
-\frac{10}{15}\log\frac23-\frac5{15}\log\frac13\approx0.6365.
$$

若全为 1，无约束 MLE 在边界 $\hat q=1$；对未见的 0 给零概率，显示有限样本过拟合/support 风险。先验/MAP 或平滑会改变估计器。

### GEN03-B02
$$
H(P_*,Q)=-\tfrac12\log\tfrac12-\tfrac13\log\tfrac14-\tfrac16\log\tfrac14\approx1.03972.
$$

$$
D_{KL}(P_*\Vert Q)=\tfrac13\log\tfrac43+\tfrac16\log\tfrac23\approx0.02832.
$$

故 $H(P_*)\approx1.01140$，且 $1.01140+0.02832=1.03972$。

### GEN03-B03
训练权重下 $0.8(0.1)+0.2(1)=0.28$ nat；部署权重下 $0.3(0.1)+0.7(1)=0.73$ nat。conditional 模型没变，条件 mixture 改变了平均指标。

## C. 推导与证明

### GEN03-C01
从

$$
D_{KL}(P_*\Vert P_\theta)=\int p_*\log\frac{p_*}{p_\theta}d\mu
$$

拆开对数得 $\int p_*\log p_*d\mu-\int p_*\log p_\theta d\mu=-H(P_*)+H(P_*,P_\theta)$，移项即结论。若某处 $p_*>0,p_\theta=0$，两边按扩展实数为无穷，需保留 support 条件。

### GEN03-C02
对任意 categorical $q$，

$$
H(p_*,q)-H(p_*)=D_{KL}(p_*\Vert q)\ge0.
$$

Gibbs 不等式给非负性；在 $p_*$ 支持上等号当且仅当 $q=p_*$。若 $p_*(i)=0$，该坐标不直接贡献 cross-entropy，但归一化要求把质量放在那里会减少支持内质量，除非总零质量仍为零；全分布最优仍是 $q=p_*$。

### GEN03-C03
对每个 $c$ 应用前一恒等式，再对 $P_*(c)$ 积分：

$$
\mathbb E_{c,x}[-\log p_\theta(x|c)]
=H_{P_*}(X|C)+\mathbb E_{c\sim P_*}D_{KL}(P_*(X|c)\Vert P_\theta(X|c)).
$$

需要条件 density 相对相容参考测度且期望存在。

## D. 边界、反例与纠错

### GEN03-D01
连续模型 $Q$ 对任何 singleton 质量为 0，经验分布 $\widehat P_n$ 却对训练点给正质量，所以 $\widehat P_n\not\ll Q$，测度 KL $D_{KL}(\widehat P_n\Vert Q)=\infty$。训练中计算的 $-n^{-1}\sum\log q(x_i)$ 是 density log score，不是无条件有限的经验测度 KL；可通过加噪/离散 bins 改变对象。

### GEN03-D02
例如 NLL 改善集中在空格、背景像素或频繁 token，而关键事实 token 仍失校准；部署又用低温 top-$p$ 删除稀有正确项，使 $Q$ 覆盖下降。要验证应分 token/group NLL、关闭 decoder 改动、测 calibration/coverage，而不是只看样本。

### GEN03-D03
“Mode-covering”是 objective 对零密度漏失的性质。有限样本可能未见稀有 mode；模型 support/容量可能无法覆盖；optimizer 可能停在坏点；dequantization/regularization 改变目标；部署截断也可删 mode。因此 MLE 目标不提供实际训练系统绝不漏模式的保证。

## E. AI 迁移

### GEN03-E01
Token-average 让长序列权重大；sequence-average 先对每条平均则每序列等权。Prompt/assistant loss mask 改条件监督区域；padding 若未 mask 会引入虚假易 token；不同 log base 改报告单位；packed segments 的 attention/loss isolation 决定条件对象；label smoothing 又不再是原 one-hot MLE。

### GEN03-E02
按 token 频率分桶、序列长度分桶、领域/语言/条件组分别累加总 NLL 与有效 token 数；报告 delta 的加权贡献，而非只报组均值。再做 calibration、rare event recall 和 free-running probes，检查平均改善是否由大频率组独占。

### GEN03-E03
相同数据预处理下报 held-out NLL/BPD；用独立特征与人评报质量；用 precision–recall/覆盖测试报模式覆盖；相同 sample budget、seed 和 decoder。低 NLL不能推出人评更好，precision 高不能推出 recall 高，recall 高不能推出样本细节好；三者连同成本才形成受控证据。

