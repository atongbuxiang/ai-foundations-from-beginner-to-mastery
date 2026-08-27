---
type: solution
status: draft
area: [generative-models, autoregressive, sequence-learning]
topic: "[[Teacher Forcing、暴露偏差与生成时分布漂移]]"
exercise: "[[习题 - Teacher Forcing、暴露偏差与生成时分布漂移]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - Teacher Forcing、暴露偏差与生成时分布漂移

## A. 识别与复述

### GEN05-A01
$$
R_{TF}=\sum_t\mathbb E_{H_t\sim P_*^{<t}}
\mathbb E_{X_t\sim P_*(\cdot|H_t)}[-\log p_\theta(X_t|H_t)].
$$

自由生成的 prefix 则 $H_t\sim Q_{\theta,\phi}^{<t}$，其中 $Q=\prod_sq_{\theta,\phi}(x_s|x_{<s})$。差异不在 loss 公式表面，而在 prefix 的积分测度；数据支持外的 $P_*(\cdot|h)$ 还可能没有可监督版本。

### GEN05-A02
Chain rule 使 TF loss 之和恰等于 joint NLL。若模型包含真实分布、数据无限且达到总体全局最优，forward KL 在 $P_\theta=P_*$ 取零，届时 rollout prefix 也相同。Exposure bias 描述有限/错设模型自由生成时的输入分布错配，不是否定这项统计一致性结论。

### GEN05-A03
Label leakage 是 shift/mask 错误使模型直接看到 target；prefix shift 是训练 $P_*^{<t}$ 与部署 $Q^{<t}$ 不同；sequence objective mismatch 是 token NLL 与 BLEU、reward、人偏好等目标不同。三者的修复分别是程序校正、稳健/rollout 训练或解码、以及重新定义/估计序列目标。

## B. 手算与建模

### GEN05-B01
模型复制第一位，故 $Q(00)=0.4,Q(11)=0.6$，其他为 0。与真实各半的 TV 为

$$
\tfrac12(|0.5-0.4|+|0.5-0.6|)=0.1.
$$

真实前缀 0/1 下第二步都复制正确，所以 TF 第二步错误率为 0。joint 偏差完全来自第一步，说明 rollout 差异不必由后续 conditional error 产生。

### GEN05-B02
逐步最大耦合下每步首次分叉概率至多 0.02，union bound 给

$$
\operatorname{TV}(P_{1:20},Q_{1:20})\le20(0.02)=0.4.
$$

一般还应截断为 $\min(1,T\varepsilon)$；这是粗上界，不等于实际 TV。

### GEN05-B03
若独立模型前缀也均匀，则训练 pair 四种 $(\hat x_1,x_2)$ 各概率 $1/4$，即 $Q(\hat x_1)P_*(x_2)$。所以

$$
P(x_2=1\mid\hat x_1=0)=P(x_2=1\mid\hat x_1=1)=1/2.
$$

最优 conditional 忽略前缀，尽管真实关系是 $x_2=x_1$。

## C. 推导与证明

### GEN05-C01
由 chain rule，

$$
-\log p_\theta(x_{1:T})
=-\log\prod_t p_\theta(x_t|x_{<t})
=-\sum_t\log p_\theta(x_t|x_{<t}).
$$

再对 $P_*$ 取期望即 TF population risk；并行实现不改变此恒等式。

### GEN05-C02
在尚未分叉且共享前缀 $h$ 时，对两个条件分布作最大耦合，使下一 token 不同概率等于其 TV，至多 $\varepsilon$。若前 $t-1$ 步均相同，第 $t$ 步首次不同概率至多 $\varepsilon$；任一步分叉的概率由 union bound 至多 $T\varepsilon$。Coupling characterization 给 joint TV 不超过该分叉概率。

### GEN05-C03
若以概率 $1-\alpha$ 用真实 $x_1$，以概率 $\alpha$ 用独立模型样本 $\hat x_1$，训练 pair 分布为

$$
M_\alpha(h,x_2)=(1-\alpha)P_*(h,x_2)+\alpha Q_\theta(h)P_*(x_2).
$$

$M_\alpha=P_*$ 当 $\alpha=0$，或替换项本身等于真实 joint，即 $Q_\theta(h)P_*(x_2)=P_*(h,x_2)$；后者要求真实两步独立且 $Q_\theta=P_*^{1}$（忽略零质量退化情形）。

## D. 边界、反例与纠错

### GEN05-D01
令真实目标从第二步起永远是 0，模型无论读到何前缀也以概率 1 输出 0。第一步即使错误，下一步进入同一状态，误差不继续传播。更一般地，contractive hidden dynamics 可衰减扰动；所以增长率需稳定性假设。

### GEN05-D02
数据仅含大量正常序列，模型在所有真实前缀下一步正确率 0.9999；但一旦误生成特殊 token `LOOP`，其 conditional 为 $p(LOOP|\cdots LOOP)=1$ 且 EOS=0。TF 几乎从不评价该前缀，平均 loss 很低；自由生成以小概率进入后便永不恢复。

### GEN05-D03
Estimand：混合前缀把目标从真实 joint cross-entropy 改为混合分布风险；pairing：模型前缀和原样本未来 target 可能不存在真实依赖；gradient：离散采样通常 stop-gradient，参数既决定输入分布又未计完整 score-function/path derivative。因此“输入像推理”只说明表面 covariate 相似，不能保证正确估计。

## E. AI 迁移

### GEN05-E01
构建三组相同长度前缀：held-out 真实前缀；随机替换一个语义/语法受控 token；同 checkpoint 原样 rollout 前缀。对每组测 next-token NLL、entropy、calibration、恢复到合法状态的步数和最终任务指标；按扰动位置/频率分层，并保证 target 定义合理（人工续写或 simulator ground truth）。

### GEN05-E02
TF：目标 joint NLL，低方差可并行，但只见数据前缀。Scheduled sampling：混合风险，离散输入 estimator 有偏/stop-gradient，经验可能改善恢复。Sequence RL：目标 $E_Q[-r(X)]$，直接评价 rollout reward，但 policy gradient 高方差且 reward 易错设。公平比较需相同 compute、decoder 和多 seed，同时报 NLL、reward、coverage 与稳定性。

### GEN05-E03
依次：关闭截断用原样 sampling 看循环概率；扫 temperature/top-$p$ 并记录 EOS 是否被 mask；在循环前缀读取 raw logits 与 EOS hazard；同 token 序列比较 full forward 与 cache decode 排除 cache/position bug；在训练域与新 prompt 域分组；最后用 prefix injection 看模型能否恢复。每次只改一项并复用 seed。

