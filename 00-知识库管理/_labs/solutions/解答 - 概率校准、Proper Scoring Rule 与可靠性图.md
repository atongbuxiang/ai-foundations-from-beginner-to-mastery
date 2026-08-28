---
type: solution
status: draft
area: [learning-theory/calibration, proper-scoring-rules, reliability]
topic: "[[概率校准、Proper Scoring Rule 与可靠性图]]"
exercise: "[[习题 - 概率校准、Proper Scoring Rule 与可靠性图]]"
prerequisites: ["[[概率校准、Proper Scoring Rule 与可靠性图]]"]
related: ["[[Aleatoric、Epistemic 与模型不确定性]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - 概率校准、Proper Scoring Rule 与可靠性图

> [!warning] 解题原则
> 先写 population conditional-frequency object，再写 finite-sample estimator。任何 ECE、温度或成本阈值都要声明数据角色、概率事件和部署分布。

## A. 识别与复述

### LT-CAL-A01

binary：
$$
E[Y\mid P]=P.
$$
strong multiclass：
$$
\Pr(Y=k\mid Q)=Q_k,\quad\forall k.
$$
classwise：
$$
\Pr(Y=k\mid Q_k=p)=p.
$$
top-label：令 $\widehat Y=\arg\max_kQ_k,C=\max_kQ_k$，
$$
\Pr(Y=\widehat Y\mid C=p)=p.
$$
strong 通过迭代条件期望蕴含 classwise；对 $(\widehat Y,C)$ 再条件化也蕴含 top-label。压缩到一个坐标或最大坐标会丢信息，所以逆命题一般不成立。

### LT-CAL-A02

discrimination 问排序，典型 ROC-AUC；accuracy 问 argmax，典型 0–1 risk；calibration 问概率与条件频率，典型 reliability functional；sharpness/resolution 问预测是否随输入有效分开，可看 Brier resolution/entropy distribution；utility 问给定成本的行动价值，看 expected cost/net benefit。一个模型可高 AUC、同样 accuracy，却因 logit scale 不同而 calibration/utility 不同。

### LT-CAL-A03

loss $L$ proper 若对真实 $p$ 有 $E_pL(p,Y)\le E_pL(q,Y)$，strictly proper 若等号只在 $q=p$。这是无限数据的总体风险识别性质。有限样本 ERM 还受函数类错设、estimation、regularization、optimization、label smoothing、validation selection 和 source–target shift 影响，所以训练目标 proper 不是结果校准证书。

## B. 手算与局部推导

### LT-CAL-B01

expected binary log loss：
$$
\mathcal L_p(q)=-p\log q-(1-p)\log(1-q).
$$
当 $p=q=0.8$：
$$
\mathcal L(0.8)\approx0.5004.
$$
当 $q=0.6$：
$$
\mathcal L(0.6)
=-0.8\log0.6-0.2\log0.4
\approx0.5919.
$$
regret 约 $0.0915=D_{\rm KL}(\operatorname{Ber}(0.8)\Vert\operatorname{Ber}(0.6))$。

以 scalar binary Brier $(Y-q)^2$ 计，
$$
\mathcal B_p(q)=p(1-p)+(q-p)^2.
$$
故 $\mathcal B(0.8)=0.16$，$\mathcal B(0.6)=0.20$，regret 为 $0.04$。若使用两坐标 multiclass Brier，二者都乘 2；报告必须声明 convention。

### LT-CAL-B02

$$
\widehat{\rm ECE}
=\tfrac12|0.1-0.2|
+\tfrac12|0.9-0.8|
=0.1.
$$
合并后平均 confidence 为 $0.5$，accuracy 也为 $0.5$，ECE 变为 0。两个方向相反的 bin error 被抵消，说明粗分箱可隐藏局部失校准；ECE 不是与 binning 无关的模型常数。

### LT-CAL-B03

预测正类成本 $(1-q)2$，预测负类成本 $8q$。选正类当
$$
2(1-q)<8q
\Longleftrightarrow q>0.2.
$$
所以 $q=0.15$ 选负类，$q=0.25$ 选正类。阈值来自成本而非固定 0.5；若概率失校准，成本比较也随之错误。

## C. 证明与反例

### LT-CAL-C01

log loss：
$$
\mathcal L_p(q)-\mathcal L_p(p)
=-\sum_kp_k\log q_k+\sum_kp_k\log p_k
=D_{\rm KL}(p\Vert q)\ge0.
$$
若支持条件满足，等号只在 $p=q$。

Brier：
$$
\begin{aligned}
\mathcal B_p(q)
&=\sum_kE(q_k-\mathbf1\{Y=k\})^2\\
&=\sum_k(q_k^2-2q_kp_k+p_k)\\
&=\|q-p\|_2^2+\sum_k(p_k-p_k^2).
\end{aligned}
$$
后项是 $\mathcal B_p(p)$，故 regret 为平方距离，只有 $q=p$ 时为 0。

### LT-CAL-C02

令两种输入等概率。A 上预测
$$
Q^A=(0.6,0.4,0),
$$
真实条件标签分布
$$
P^A=(0.6,0,0.4).
$$
B 上预测
$$
Q^B=(0.6,0,0.4),
$$
真实条件标签分布
$$
P^B=(0.6,0.4,0).
$$
两组 top label 都是 1、confidence 都为 0.6，正确频率也均为 0.6，因此 top-label calibrated。A 中 $Q_2=0.4$ 时类 2 频率为 0 而非 0.4；B 中 $Q_2=0$ 时类 2 频率为 0.4，故 classwise 失败。显然 $P^A\ne Q^A,P^B\ne Q^B$，strong 也失败。

### LT-CAL-C03

令 $\eta(P)=E[Y\mid P]$、$\pi=E[Y]$。因为 $Y-\eta(P)$ 与任意 $P$ 的函数正交，
$$
E(Y-P)^2
=E(Y-\eta)^2+E(\eta-P)^2.
$$
再由总方差，
$$
E(Y-\eta)^2
=\operatorname{Var}(Y)-\operatorname{Var}(\eta)
=\pi(1-\pi)-E(\eta-\pi)^2.
$$
合并即
$$
\operatorname{BS}
=E(P-\eta)^2-E(\eta-\pi)^2+\pi(1-\pi).
$$
常数 $P=\pi$ 时 $\eta(P)=\pi$，reliability error 为 0、resolution 为 0、Brier 等于 base uncertainty $\pi(1-\pi)$。

## D. 审计与诊断

### LT-CAL-D01

至少补充：校准定义（top/classwise/strong proxy）、confidence/event、binning（equal-width/mass）、bin 数、norm、空 bin、sample size/bin counts、independent unit、置信区间、同一数据是否拟合 calibrator、模型/checkpoint selection、class/subgroup aggregation、quantization/ties、deployment distribution。缺任意关键项，“1.7%”都不可复算，也不可与别的 ECE 公平比较。

### LT-CAL-D02

污染来自在 test noise 上最大化 $20\times5\times4$ 个配置的表现。正确流：
$$
D_{\rm train}
\to\text{fit models}
\to D_{\rm cal}\text{ fit each calibrator}
\to D_{\rm select}\text{ choose checkpoint/method}
\to D_{\rm test}^{\rm locked}\text{ evaluate once}.
$$
binning 若只是预注册的 estimator 可直接在 locked test 评；若也要选择，就属于 selection space，不能用同一 test 决定。最终报告多重选择规则及 paired uncertainty。

### LT-CAL-D03

按 time/site/device/group 记录 confidence、outcome 与 delay；画 rolling NLL/Brier、bin counts、classwise/group reliability 和 cost curve，并设 minimum effective sample size。source 的 $E_s[Y\mid Q]=Q$ 不推出 $E_t[Y\mid Q]=Q$；prevalence 改变还会使 PPV 和阈值 utility 改变。重校准只能用新 calibration window，且 concept drift 时单纯 intercept/temperature 可能不足。

## E. 研究与迁移

### LT-CAL-E01

event 先定义为“经盲评器/可执行测试判为整题正确”，不是下一个 token。confidence 可来自专门 correctness head、verbalized probability 或多次 procedure 的预注册映射；unit 是独立问题/source，template variants 按 cluster 处理。报告 answer-level log/Brier、reliability、risk–coverage 与错误回答成本；train/calibration/test 按题源和时间隔离。token probability 只描述 decoder 下局部序列概率，受长度、分词、候选集与表达多样性影响，不等于事实正确率。

### LT-CAL-E02

先锁定 source/time/group splits；train 拟合模型，calibration 拟合 temperature/isotonic，selection 选方法，outer test 只评一次。报告 NLL、scalar/multiclass Brier、top/classwise/group reliability（含 bin counts/CI）、risk–coverage、cost threshold curves、accuracy/AUC。对 paired bootstrap 使用 patient/user unit；另做 prevalence、temporal、site shifts。最强 claim 绑定目标人群、时间窗、成本和 calibrator。

### LT-CAL-E03

claim card 至少含 event、概率向量/置信度定义、模型与 calibrator、数据角色、proper scores、calibration estimator、sharpness、groups、shift、cost 和 uncertainty。允许：“在锁定的 target-like test 与预注册 estimator 下，模型 Brier/NLL 和指定 calibration error 为多少。”拒绝：“ECE 低所以概率真实”“交叉熵训练所以处处校准”“source 校准保证任意部署”“top-label 校准说明完整分布正确”。
