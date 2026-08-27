---
type: theorem
status: draft
area: [learning-theory/calibration, proper-scoring-rules, reliability]
aliases: [Probability Calibration, Reliability Diagram, Proper Loss]
node_id: LT-61
prerequisites: ["[[条件概率、全概率与 Bayes 公式]]", "[[协方差、相关性与条件期望]]", "[[逻辑回归、复合损失与概率分类]]", "[[训练集、验证集、测试集与自适应复用]]"]
related: ["[[Aleatoric、Epistemic 与模型不确定性]]", "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]", "[[Conformal Prediction 与有限样本 Coverage]]", "[[Covariate、Label 与 Concept Shift]]"]
sources: ["[[S-2007-Gneiting-Raftery-Proper-Scoring]]", "[[S-2017-Guo-Calibration]]", "[[S-2019-Kumar-Verified-Calibration]]", "[[S-2022-Roelofs-Calibration-Bias]]", "[[S-2010-Reid-Williamson-Composite-Binary-Losses]]"]
exercises: ["[[习题 - 概率校准、Proper Scoring Rule 与可靠性图]]"]
solutions: ["[[解答 - 概率校准、Proper Scoring Rule 与可靠性图]]"]
figure: "[[00-知识库管理/_assets/figures/learning-theory/fig-calibration-proper-score-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# 概率校准、Proper Scoring Rule 与可靠性图

> [!abstract] 本章主问题
> 分类正确回答“选哪个标签”，概率预测回答“每个结果有多可能”。校准要求具有相同预测概率的事件在长期频率上相符；proper scoring rule 则让诚实报告真实条件分布成为总体风险最优。可靠性图和 ECE 只是有限样本估计工具，不是定义本身。

## 一、学习目标

完成本章后，应能：

1. 写出 binary、classwise、top-label 与 strong multiclass calibration；
2. 区分 accuracy、calibration、sharpness、NLL/Brier 与 decision utility；
3. 推导 log loss 与 Brier loss 的 strict propriety；
4. 推导 Brier 的 reliability–resolution–uncertainty 分解；
5. 解释 reliability diagram 的分箱偏差—方差；
6. 说明 ECE 为什么依赖 binning、norm、confidence 定义和样本量；
7. 推导 temperature scaling，并说明它能和不能改变什么；
8. 设计无数据泄漏的 calibration train–fit–evaluate 协议；
9. 识别 distribution shift 下“旧校准”失效的原因；
10. 把概率质量转换为成本敏感的 AI 决策。

## 二、先区分三种输出

对 $K$ 分类模型，令

$$
Q(X)=(Q_1(X),\ldots,Q_K(X))\in\Delta^{K-1}.
$$

由它可导出：

$$
\widehat Y(X)=\arg\max_k Q_k(X),
\qquad
C(X)=\max_k Q_k(X).
$$

- $\widehat Y$ 是离散决策；
- $C$ 是 top-label confidence；
- $Q$ 是完整预测分布。

只保存 $\widehat Y$ 会丢掉风险排序与成本阈值信息；只保存 $C$ 又会丢掉非 top classes 的概率结构。

## 三、Binary Calibration 的总体定义

令 $Y\in\{0,1\}$，模型输出 $P=P(X)\in[0,1]$。完美校准定义为

$$
\boxed{
E[Y\mid P]=P
\quad\text{a.s.}
}
$$

等价地，对所有有正概率的预测值 $p$，

$$
\Pr(Y=1\mid P=p)=p.
$$

连续 $P$ 下单点事件通常概率为零，因此严格写法是条件期望等式；经验分箱只是近似观察它。

### 3.1 一个校准但不锋利的预测器

若总体正类比例 $\pi=0.8$，对所有样本都输出 $P=0.8$，则

$$
E[Y\mid P=0.8]=0.8,
$$

所以它校准；但它不能区分任何两个样本，resolution 很低。

### 3.2 一个准确但失校准的预测器

若模型在某测试集 top-1 accuracy 为 $1$，却对每个样本只给正确类 $0.51$，则

$$
\Pr(\widehat Y=Y\mid C=0.51)=1\ne0.51.
$$

accuracy 完美并不意味着 confidence 正确。

## 四、多分类有不止一种“校准”

令 $Q\in\Delta^{K-1}$。

### 4.1 Strong/Distribution Calibration

$$
\boxed{
\Pr(Y=k\mid Q)=Q_k,\qquad k=1,\ldots,K.
}
$$

它条件在完整向量 $Q$ 上，是最强也最难估计的常见版本。

### 4.2 Classwise Calibration

$$
\Pr(Y=k\mid Q_k=p)=p
$$

对每类分别检查，但忽略其余坐标。

### 4.3 Top-Label Calibration

$$
\Pr(Y=\widehat Y\mid C=p)=p.
$$

它只检查“最大概率是否等于正确频率”。strong calibration 蕴含 classwise 与 top-label calibration，但反向一般不成立：压缩条件变量会隐藏系统误差。

## 五、Calibration 不是确定预测的全部质量

一个概率预测至少有四个轴：

| 轴 | 问题 | 典型量 |
|---|---|---|
| discrimination | 正例是否排在负例前？ | ROC-AUC、ranking |
| accuracy | argmax 是否正确？ | 0–1 risk |
| calibration | 概率与条件频率是否一致？ | reliability functional |
| sharpness/resolution | 预测是否随输入有效变化？ | resolution、entropy |
| utility | 在具体成本下是否做对决策？ | expected cost/value |

校准的常数 base-rate 预测器可能缺乏分辨率；高 AUC 模型也可能系统过度自信。

## 六、Proper Scoring Rule

把 score 写成要最小化的 loss $L(q,y)$。若真实分布为 $p$，则

$$
\mathcal L_p(q)=E_{Y\sim p}[L(q,Y)].
$$

若对所有 $p,q$，

$$
\mathcal L_p(p)\le \mathcal L_p(q),
$$

则 $L$ proper；若等号只在 $q=p$ 成立，则 strictly proper。它的意义是：在总体期望下，诚实报告 $p$ 没有损失上的激励劣势。

> [!warning] Proper 不等于有限样本一定恢复
> strict propriety 是 population risk 的识别性质。有限数据、受限模型类、正则化、优化失败和 shift 都会使训练输出偏离真实条件分布。

## 七、Log Loss 的严格适当性

多分类 log loss：

$$
L_{\log}(q,y)=-\log q_y.
$$

若真实分布为 $p$，

$$
\mathcal L_p(q)
=-\sum_{k=1}^K p_k\log q_k.
$$

加减 $-\sum_kp_k\log p_k$：

$$
\mathcal L_p(q)
=H(p)+D_{\mathrm{KL}}(p\Vert q).
$$

因此

$$
\boxed{
\mathcal L_p(q)-\mathcal L_p(p)
=D_{\mathrm{KL}}(p\Vert q)\ge0.
}
$$

只要按支持集处理零概率，等号仅在 $q=p$。log loss 对把真实事件赋极小概率施加强惩罚。

## 八、Brier Loss 的严格适当性

多分类 Brier loss：

$$
L_{\rm Br}(q,y)
=\sum_{k=1}^K(q_k-\mathbf 1\{y=k\})^2.
$$

对 $Y\sim p$ 取期望：

$$
\begin{aligned}
\mathcal L_p(q)
&=\sum_k E[(q_k-\mathbf1\{Y=k\})^2]\\
&=\sum_k(q_k^2-2q_kp_k+p_k)\\
&=\|q-p\|_2^2+\sum_k(p_k-p_k^2).
\end{aligned}
$$

后一项与 $q$ 无关，故

$$
\boxed{
\mathcal L_p(q)-\mathcal L_p(p)=\|q-p\|_2^2.
}
$$

Brier 是有界二次损失；与 log loss 对小概率错误的敏感性不同。两个 proper losses 对有限模型的排序可能不同。

## 九、Proper Loss 与 Calibration 的关系边界

若函数类足够丰富且能最小化严格 proper population risk，则最优预测是

$$
q^*(x)=\Pr(Y=\cdot\mid X=x),
$$

它当然 strong calibrated。现实中最常见的断裂点是：

1. 模型类不含真实条件分布；
2. 训练目标含正则化、label smoothing 或 sampling correction；
3. optimization 没到总体最优；
4. 验证与部署分布不同；
5. 概率经 quantization、top-$k$ truncation 或 prompt 变换；
6. 只评 top-label calibration，遗漏完整分布错误。

所以“用交叉熵训练过”不是校准证书。

## 十、Brier 分解

回到 binary 情形。定义

$$
\eta(P)=E[Y\mid P],
\qquad
\pi=E[Y].
$$

在平方损失中插入 $\eta(P)$，利用条件期望正交性：

$$
\begin{aligned}
E[(Y-P)^2]
&=E[(Y-\eta(P))^2]+E[(\eta(P)-P)^2].
\end{aligned}
$$

又有

$$
E[(Y-\eta(P))^2]
=\pi(1-\pi)-E[(\eta(P)-\pi)^2].
$$

因此

$$
\boxed{
\operatorname{BS}
=
\underbrace{E[(P-\eta(P))^2]}_{\text{reliability error}}
-
\underbrace{E[(\eta(P)-\pi)^2]}_{\text{resolution}}
+
\underbrace{\pi(1-\pi)}_{\text{uncertainty}}.
}
$$

校准降低第一项；有信息的个体化预测提高 resolution，从而降低总 Brier risk。常数 base-rate predictor 第一项为零，但 resolution 也为零。

## 十一、可靠性图到底估计什么

把 $[0,1]$ 分为 bins $B_1,\ldots,B_M$。第 $m$ 个 bin：

$$
\widehat{\operatorname{conf}}_m
=\frac{1}{n_m}\sum_{i:P_i\in B_m}P_i,
\qquad
\widehat{\operatorname{freq}}_m
=\frac{1}{n_m}\sum_{i:P_i\in B_m}Y_i.
$$

可靠性图画点

$$
(\widehat{\operatorname{conf}}_m,\widehat{\operatorname{freq}}_m),
$$

并与对角线比较。还应同时显示 $n_m$ 或直方图；一个只有 3 个样本的 bin 不能与 3000 个样本的 bin 等量解读。

## 十二、ECE 是估计器，不是定义

常见 top-label ECE：

$$
\widehat{\operatorname{ECE}}
=\sum_{m=1}^M\frac{n_m}{n}
\left|
\widehat{\operatorname{acc}}_m-
\widehat{\operatorname{conf}}_m
\right|.
$$

它依赖：

- equal-width 还是 equal-mass bins；
- $M$；
- top-label、classwise 还是完整向量；
- $L_1$、$L_2$ 或 maximum norm；
- 空 bin 处理；
- 同一数据是否用于校准和评估；
- 样本独立单位与重复预测；
- finite-sample absolute-value bias。

少 bins 会把同一 bin 内正负失校准平均掉；多 bins 降低离散化偏差但增加频率估计方差。不同 ECE 配置的数字不能直接比较。

## 十三、Temperature Scaling

给定 logits $z(x)\in\mathbb R^K$，以 $T>0$ 定义

$$
q_k^{(T)}(x)
=
\frac{\exp(z_k(x)/T)}
{\sum_j\exp(z_j(x)/T)}.
$$

在独立 calibration/validation set 上最小化 NLL：

$$
\widehat T
=
\arg\min_{T>0}
\sum_{i\in\mathcal C}
-\log q_{y_i}^{(T)}(x_i).
$$

当 $T>1$ 时分布变平，$T<1$ 时变尖。正温度保持 logit 大小次序，因此不改变无并列时的 argmax 与 top-1 accuracy；它会改变 NLL、Brier、confidence 和成本阈值。

### 13.1 它不能做什么

单一 $T$ 不能：

- 改善错误 class ranking；
- 修复 class-dependent 或 input-dependent miscalibration；
- 保证 subgroup calibration；
- 保证分布偏移后仍校准；
- 抵消 calibration set 的选择污染。

## 十四、校准协议的数据合同

推荐四角色：

1. train：拟合原模型；
2. calibration/validation：拟合 $T$、isotonic 或其他 calibrator；
3. selection validation：若比较多个 calibrators，选择规则使用独立层；
4. locked test：最终只评一次。

若在 test ECE 上挑 bin 数、温度、模型、checkpoint 或 subgroup，再汇报同一 test，结果已经 optimistic。

## 十五、从概率到成本敏感决策

二分类中，假阳性成本 $c_{\rm FP}$，假阴性成本 $c_{\rm FN}$。若 $q=\Pr(Y=1\mid X=x)$：

$$
\operatorname{cost}(a=1)=(1-q)c_{\rm FP},
\qquad
\operatorname{cost}(a=0)=qc_{\rm FN}.
$$

故选择正类当且仅当

$$
\boxed{
q>\frac{c_{\rm FP}}{c_{\rm FP}+c_{\rm FN}}.
}
$$

这说明概率误差只有与 decision threshold、资源和伤害函数结合，才能解释实际影响。固定 0.5 并非普遍正确。

## 十六、Distribution Shift 下为什么会失效

模型在 source distribution $P_s$ 上校准：

$$
E_s[Y\mid Q]=Q,
$$

并不推出 target distribution $P_t$ 上

$$
E_t[Y\mid Q]=Q.
$$

label prevalence、class-conditional score distribution、input–label mechanism 或采样选择改变，都可能破坏条件频率。部署后要按时间、站点、设备、群体与 shift severity 重做 calibration monitoring。

## 十七、图：从真实条件概率到可审计决策

先看图回答：为什么“沿对角线的可靠性图”仍不足以证明模型是一个好的概率预测器？

![[00-知识库管理/_assets/figures/learning-theory/fig-calibration-proper-score-v2.svg|900]]

> [!figure] 图 20.8-01　Calibration、proper scoring 与 decision contract
> 左栏区分完整概率、top-label confidence 与校准层级；中栏展示 log/Brier regret 及 reliability–resolution 分账；右栏给出分箱估计、temperature scaling、locked test 与成本阈值。来源：依据 Gneiting–Raftery、Guo et al.、Kumar et al. 与 Roelofs et al. 独立绘制；确定性 SVG，由 [[plot_calibration_uncertainty_v2.py]] 生成。

**怎样读图**：先在左栏选择校准定义，再用中栏的 proper risk 同时约束校准和 sharpness，最后在右栏把有限样本估计、后处理和实际决策分开验收。

**图没有证明什么**：图没有证明 ECE 是唯一或无偏的 calibration metric，也没有证明 temperature scaling 在 shift 后有效；它只给出对象、估计与决策的分层合同。

## 十八、AI 接口

### 18.1 大语言模型

token-level NLL、sequence-level correctness、verbalized confidence 与“回答是否正确”是不同随机对象。先定义 event，再谈 calibration；长度归一化、sampling temperature 和 abstention 会改变接口。

### 18.2 医疗与风控

base rate 随医院、时间和人群变化。即使 ranking 稳定，原概率也可能需要重校准；同时报告 subgroup reliability 与成本曲线。

### 18.3 检索与生成

retrieval score 未必是概率；若经 softmax 归一化，其候选集合改变会改变数值。生成模型的 token probability 也不自动等于事实正确概率。

### 18.4 Selective Prediction

以 confidence 决定 abstain 时，应评 risk–coverage curve，而不是假设高 confidence 必然低风险；calibration 是其中一项证据。

## 十九、常见错误

1. 把 accuracy 当 calibration；
2. 把一个 ECE 数字当 population definition；
3. 不声明 top-label、classwise 或 strong calibration；
4. 只画 bin 点，不画 bin count 与区间；
5. 在 test 上拟合 temperature；
6. 用更多 bins 必然“更准确”；
7. 只报 calibration，不报 sharpness/NLL/Brier；
8. 认为交叉熵训练自动保证有限样本校准；
9. 忽略 label smoothing、采样和 quantization；
10. 从 source 校准外推到 target shift。

## 二十、最小记忆

> [!summary]
> - 校准是条件频率等式，不是图或 ECE；
> - strong、classwise 与 top-label calibration 强弱不同；
> - strictly proper loss 让真实条件分布成为总体唯一最优；
> - calibration 与 resolution 必须同时考虑；
> - 后处理只在独立 calibration data 上拟合；
> - 可靠概率最终要经过成本和 shift 审计。

## 二十一、掌握标准

### A. 定义

能写 binary 与三种 multiclass calibration，并说明蕴含关系。

### B. 推导

能推导 log/Brier regret 和 Brier 三项分解。

### C. 反例

能构造“校准但无分辨率”“准确但失校准”及 top-label 校准但非 strong 校准的例子。

### D. 实验

能实现带 bin count/uncertainty 的 reliability diagram，比较 ECE 配置并用 locked test 评 temperature scaling。

### E. 迁移

能把模型概率转成成本阈值，监控群体/时间 shift，并拒绝超出证据的校准声明。

## 二十二、练习与独立详解

- [[习题 - 概率校准、Proper Scoring Rule 与可靠性图]]
- [[解答 - 概率校准、Proper Scoring Rule 与可靠性图]]

## 参考来源

- [[S-2007-Gneiting-Raftery-Proper-Scoring]]
- [[S-2017-Guo-Calibration]]
- [[S-2019-Kumar-Verified-Calibration]]
- [[S-2022-Roelofs-Calibration-Bias]]
- [[S-2010-Reid-Williamson-Composite-Binary-Losses]]
