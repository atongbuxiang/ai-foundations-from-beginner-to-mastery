---
type: solution
status: draft
area: [learning-theory/masked-prediction, teacher-student, self-supervision]
topic: "[[习题 - 遮蔽预测、Teacher–Student 与自监督目标]]"
prerequisites: ["[[遮蔽预测、Teacher–Student 与自监督目标]]"]
related: ["[[Linear Probe、Fine-Tuning 与迁移评估]]"]
created: 2026-08-23
updated: 2026-08-23
---

# 解答 - 遮蔽预测、Teacher–Student 与自监督目标

> [!warning] 解题原则
> 每道题先画 target lineage：clean data/quantizer/teacher 中谁生成 target，student 看见什么，哪些边 stop-gradient。再讨论 loss 的 population optimum 与下游意义。

## A. 识别与复述

### LT-TGT-A01

$X\sim P_X$，$M\sim Q(\cdot\mid X)$，$\widetilde X=C(X,M,\xi)$，$T=\mathcal T(X,M,\omega)$，student $q_\theta(\cdot\mid\widetilde X,M)$：

$$
R_{\rm pre}(\theta)
=
E\ell(q_\theta(\widetilde X,M),T).
$$

若 $T$ 来自 teacher、quantizer assignment 或另一 branch，需说明其参数是否 detach；EMA/center更新本身通常不经当前 loss 反传。若 target 是 clean token/pixel，则 clean target path也不反传到数据，但 decoder/encoder的可微路径要明确。

### LT-TGT-A02

raw token用 vocabulary CE，鼓励 conditional symbolic prediction，风险是 tokenizer/mask mismatch；pixel用 MSE/likelihood，鼓励 appearance reconstruction，风险是局部纹理和conditional mean；latent用 feature distance，继承 teacher geometry/bias；discrete code用 CE，风险是 codebook collapse；cluster assignment用 CE/OT，可能产生 balance artifact；teacher distribution用 CE/KL，平滑历史但可 self-confirm。target“抽象程度”不是单调语义保证。

### LT-TGT-A03

Mean Teacher有真实 labeled loss，并用 student weights EMA 生成 teacher prediction，对 unlabeled perturbations做 consistency。BYOL 无显式 labels，以 online predictor 匹配 EMA target latent，使用 stop-gradient。DINO 用 EMA teacher 的 prototype distribution，teacher sharpening/temperature和centering控制 entropy/prototype占用，常配 multi-crop。三者都需写 EMA，但 target space、监督项与 collapse control 不同。

## B. 手算与局部推导

### LT-TGT-B01

给 visible context $V$，真实 conditional $p(t\mid V)$：

$$
\begin{aligned}
E[-\log q(T\mid V)\mid V]
&=-\sum_t p(t\mid V)\log q(t\mid V)\\
&=H(p(\cdot\mid V))+D_{\rm KL}(p(\cdot\mid V)\|q(\cdot\mid V)).
\end{aligned}
$$

KL 非负，故 unrestricted optimum 为 $q=p$。model class 受限时最小额外 gap 是

$$
\inf_{q\in\mathcal Q}E_VD_{\rm KL}(p_{T\mid V}\|q_{T\mid V}),
$$

另有有限样本、优化与 target估计误差，不能全称作“表示不好”。

### LT-TGT-B02

设 $m(V)=E[T\mid V]$。恒等式

$$
E[(T-a)^2\mid V]
=
\operatorname{Var}(T\mid V)+(m(V)-a)^2
$$

给出 $a^*=m(V)$。题中 $m=0$，$\operatorname{Var}=1$，最优预测0、最小风险1。真实 target 只取 $-1,+1$，预测0从不出现；这就是多峰 conditional 被平方损失压成均值的“模糊”现象。

### LT-TGT-B03

$$
\xi_1=0.9\times0+0.1\times1=0.1,
$$

$$
\xi_2=0.9\times0.1+0.1\times2=0.29,
$$

$$
\xi_3=0.9\times0.29+0.1\times4=0.661.
$$

展开：

$$
\xi_3=0.1\theta_3+0.09\theta_2+0.081\theta_1+0.9^3\xi_0
=0.4+0.18+0.081.
$$

权重随历史指数衰减，余下质量在初始化项；有限步权重和小于1。

## C. 证明与反例

### LT-TGT-C01

only-masked risk 可写

$$
E_XE_{M\sim Q(\cdot\mid X)}
\sum_{i\in M}-\log q(X_i\mid \widetilde X,M).
$$

每个 token/context 的权重正比于其被选入 $M$ 的概率，故换 $Q$ 就换 estimand。例：稀有 token 出现率1%，但规则见到稀有 token 必遮蔽，常见 token 仅以0.01概率遮蔽；被监督位置中稀有 token 权重被放大约100倍。模型优化的是 selection-reweighted conditional loss，不是自然 token频率下均匀目标。需记录/必要时 importance weighting。

### LT-TGT-C02

令所有图像 patches 满足

$$
X_i=\mu+\epsilon_i,
\qquad E\epsilon_i=0,
\qquad \operatorname{Var}(\epsilon_i)=\sigma^2\ll1.
$$

令 encoder 恒定，decoder仅输出每个位置的训练均值 $\mu$。每 patch MSE 为 $\sigma^2$，可非常小，但 representation 不含 sample-specific或semantic信息。这说明低 reconstruction loss可能来自低 target variance/强位置先验；decoder capacity、unconditional baseline与downstream评估必须进入审计。

### LT-TGT-C03

二分类真实 $Y=1$，但 teacher 对所有未标样本输出 class0，student也输出class0。则 consistency divergence为0，却100%错误。可打破的独立信号包括真实 labeled loss、另一模态/另一view中的互补证据、可信 rule/constraint、confidence+calibration filter、diverse independent teachers、正确 augmentation invariance以及对错误cluster的人工审计。单纯增加 imitation权重只会强化错误。

## D. 审计与诊断

### LT-TGT-D01

登记：选中比例（经典 BERT 为15%）、选中位置中80% `[MASK]`、10% random token、10% unchanged；是否动态重采样；loss只在选中位置、按 token数还是sequence mean；WordPiece/vocab/version与special tokens；random replacement是否可能等于原token；pretrain clean/masked与downstream clean mismatch；document/user/time去重与split；MLM loss、pseudo-likelihood、linear/fine-tune任务分别报告。80/10/10是该方法recipe，不应写成MLM定理。

### LT-TGT-D02

25% mask：visible compute高，局部copy/texture shortcut强，conditional ambiguity低；75%：compute显著下降、任务较难，通常是MAE经典平衡点；95%：visible信息很少，ambiguity和optimization难度高，可能主要学dataset prior。公平ablation固定encoder、decoder、steps或明确对齐总FLOPs，分别报告pretext MSE、throughput、linear/fine-tune risk和mask-shift；同时做decoder容量交叉，避免把更高mask带来的compute节省误归因于表示。

### LT-TGT-D03

同一prototype collapse可能由：teacher温度太低产生早期one-hot自强化；太高则uniform targets；centering更新过慢/错误导致prototype偏置；EMA过高使坏teacher滞留，过低则teacher追student；multi-crop pairing或mask错误只看同一crop；local而非global batch center造成worker偏置；更新顺序（先/后teacher与center）不一致。诊断需同时画prototype occupancy、teacher/student entropy、center、logit spectrum、EMA lag、各crop loss与跨worker统计。

## E. 研究与迁移

### LT-TGT-E01

以患者/设备/序列为 source unit；对历史窗口内随机 contiguous spans或变量块mask，禁止target时刻后的值、由未来计算的normalization与全序列插值进入visible input。target可用条件Gaussian/quantile/categorical likelihood而非只MSE；missingness若informative，mask indicator与自然缺失机制分开。下游按时间滚动forecast，outer未来窗口锁定；报告mask pattern transfer、horizon、calibration与sensor-failure shift。

### LT-TGT-E02

三路共享同一encoder、visible tokens、mask law、pretraining data、optimizer、encoder FLOPs/steps。token/pixel/teacher-latent各用最小必要decoder，并通过参数/FLOPs匹配或做decoder-capacity factorial design；teacher计算成本另计。评估同一label budgets下linear、MLP、fine-tune、reconstruction/conditional likelihood与shift。允许比较target geometry在该预算下的效果，不能宣称某target普遍最语义。

### LT-TGT-E03

事故报告字段：时间线与影响；clean/mask/target lineage；发现的不可用信息路径；teacher/center/EMA/temperature历史；collapse面板；pretext与downstream曲线分歧；受污染splits/checkpoints；selection次数；最小复现；停止训练与隔离资产；修复、重新split/训练/outer test证据；未解决边界与回滚点。恢复条件必须由锁定测试与独立审计通过，而非原test继续调参。

