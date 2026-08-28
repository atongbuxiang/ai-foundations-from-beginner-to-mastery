---
type: solution
status: draft
area: [learning-theory/uncertainty, aleatoric, epistemic]
topic: "[[Aleatoric、Epistemic 与模型不确定性]]"
exercise: "[[习题 - Aleatoric、Epistemic 与模型不确定性]]"
prerequisites: ["[[Aleatoric、Epistemic 与模型不确定性]]"]
related: ["[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - Aleatoric、Epistemic 与模型不确定性

> [!warning] 解题原则
> 方差和 entropy 分解都是对一个已声明层级模型的恒等式。不要把代数项无条件升级为数据中唯一可辨识的“真实不确定性类型”。

## A. 识别与复述

### LT-UNC-A01

五项是：随机预测对象、条件信息、谁的知识状态、uncertainty functional、支持的行动。例如补全为：“给定当前相机帧 $X$ 和训练数据 $D$，该 ensemble 对行人是否进入 2 秒碰撞区的 Bernoulli predictive entropy 为 0.61；系统用它决定是否减速。”还要说明 ensemble 如何生成。原句没有 event、conditioning、measure 和 decision，无法验证。

### LT-UNC-A02

observation noise：传感器误差，可重复测量/换设备；label ambiguity：标注定义冲突，可重定义事件/多标注；parameter/function uncertainty：数据不足，可采集覆盖相关方向的数据；model-form：真实机制不在模型族，可扩充/比较结构；approximation：$q$ 或优化不充分，可改推断和计算；shift：部署联合分布改变，可监控、重校准、适应。各层的缓解动作不同，所以不应合并成一个 heatmap。

### LT-UNC-A03

“不可约”是相对于 $\sigma(X)$-field：增加传感器 $Z$、重复测量或澄清标签后，$\operatorname{Var}(Y\mid X,Z)$ 可下降。OOD 描述 $x$ 与参考分布的关系，epistemic 描述 agent 的知识；模型可在简单 OOD 上一致且正确，也可在训练支持内的数据稀疏边界上分歧。二者没有定义上的等价。

## B. 手算与局部推导

### LT-UNC-B01

mean：
$$
\bar\mu=(0+1+2)/3=1.
$$
within：
$$
(1+4+1)/3=2.
$$
between：
$$
[(0-1)^2+(1-1)^2+(2-1)^2]/3=2/3.
$$
total：
$$
2+2/3=8/3.
$$
不能只对成员均值算方差，否则漏掉 observation component。

### LT-UNC-B02

$$
\ell'(s)=-\tfrac12e^{-s}r^2+\tfrac12,
\qquad
\ell''(s)=\tfrac12e^{-s}r^2.
$$
当 $r\ne0$，二阶导为正，驻点满足 $e^s=r^2$，所以 $s^*=\log r^2$。当 $r=0$，$\ell(s)=s/2$，令 $s\to-\infty$ 可使 loss 无下界，显示 exact interpolation 下 variance-collapse 退化；实际需噪声下限、正则化或合适 likelihood。

### LT-UNC-B03

mixture probability 为 0.5，所以
$$
H(\bar p)=\log2\approx0.6931.
$$
每个成员 entropy 相同：
$$
h(0.9)=-0.9\log0.9-0.1\log0.1\approx0.3251.
$$
平均仍为 0.3251，故
$$
I(Y;\Theta)=0.6931-0.3251\approx0.3681.
$$
高 predictive entropy 此处主要来自成员分歧；若两成员都给 0.5，MI 为 0 而 expected entropy 为 $\log2$。

## C. 证明与反例

### LT-UNC-C01

令 $\mu_\Theta=E[Y\mid x,\Theta]$，$m=E[Y\mid x,D]$。有
$$
Y-m=(Y-\mu_\Theta)+(\mu_\Theta-m).
$$
平方取 $E[\cdot\mid x,D]$。交叉项
$$
E[(Y-\mu_\Theta)(\mu_\Theta-m)\mid x,D]
=E[(\mu_\Theta-m)E(Y-\mu_\Theta\mid x,\Theta,D)\mid x,D]=0.
$$
余下两项分别是 $E[\operatorname{Var}(Y\mid x,\Theta)]$ 和 $\operatorname{Var}(\mu_\Theta\mid x,D)$，结论成立。

### LT-UNC-C02

令 $Z\sim\operatorname{Ber}(1/2)$，$Y=Z$，但 $X$ 是常数。则
$$
\operatorname{Var}(Y\mid X)=1/4.
$$
加入可观测传感器 $Z$ 后，
$$
\operatorname{Var}(Y\mid X,Z)=0.
$$
在只看 $X$ 的任务中 1/4 是剩余随机性；在看 $(X,Z)$ 时完全可约。若 $Z$ 本身有测量噪声，方差会介于两者之间。

### LT-UNC-C03

OOD 低分歧：所有成员只在训练域学到同一饱和 ReLU/logit，对远离支持集的输入都输出 class 1 概率 0.999；输入 OOD，但 variance 近零且可能错。ID 高分歧：训练分布包含一个极少数、标签边界附近的合法 subgroup，不同初始化对其 decision boundary 不同；它是 ID 却分歧大。ensemble variance 同时受 architecture、optimization、regularization 与 mode coverage 影响，不能由定义识别 OOD。

## D. 审计与诊断

### LT-UNC-D01

先画 signed residual $Y-\mu(X)$ 与 $\sigma(X)$、features 的关系；检查标准化 residual $(Y-\mu)/\sigma$ 是否零均值、单位尺度及尾部是否匹配；比较 mean-only richer model 与 heteroscedastic model；做 PIT/quantile coverage 和 NLL/Brier/CRPS；对该区域收集重复测量或更强 features；做 counterfactual 保持噪声条件只改变可预测 factor。若均值升级后 $\sigma$ 大幅下降，旧 variance 很可能吸收 bias；高 coverage 但区间过宽也不是成功。

### LT-UNC-D02

需说明成员是 exact posterior、VI、dropout、SWAG 还是 independent runs；prior、likelihood、posterior family、training objective、weighting、成员相关性、samples、parameter symmetry、BatchNorm、calibration 和 shift。没有这些，entropy 分解仍可作为某个 empirical mixture 的代数分账，但 “aleatoric/epistemic” 的 Bayesian 语义未成立。

### LT-UNC-D03

比较 predictive entropy、expected entropy、MI/disagreement 和重复标注者 entropy；对被查询样本测新增标签后的 held-out risk reduction，而非只看当下 entropy。加入 group-coverage constraint、density/support 与 cost；batch acquisition 对相似样本做 diversity/conditional gain。高 expected entropy 但低 disagreement 的点可能只是不可约歧义，反复标注价值有限。

## E. 研究与迁移

### LT-UNC-E01

矩阵示例：遮挡→条件多模态→多传感器/轨迹分布；传感器噪声→likelihood/重复测量；罕见天气→support gap→定向数据；模型错设→替代 architecture/physics constraints；推断近似→更丰富 $q$/ensembles；反馈 shift→在线监控和 policy-aware evaluation。每格报告 NLL/coverage/width、detection 与行动成本；pixel variance 不能替代 collision-event risk。

### LT-UNC-E02

对象分层：token entropy 用 decoder log probabilities；answer disagreement 用预注册 semantic clustering；事实未知用可核验 QA 和 time cutoff；题目歧义用多标注/多解释；evaluator uncertainty 用评审者模型与 agreement。metrics 分别为 token NLL、answer distribution entropy、correctness calibration/risk–coverage、inter-annotator entropy、evaluator reliability。改变 temperature/prompt/source/time 做干预，不能把 self-consistency 直接叫 knowledge。

### LT-UNC-E03

claim card 写随机对象、条件信息、模型/likelihood、成员生成、functional、data split、proper score、calibration/coverage、sharpness、shift、groups 与 decision。允许：“在声明的 Gaussian-mixture ensemble 下，between-member variance 与 held-out error detection/coverage 的关系为……”。禁止：“这是模型的真实不确定性”“aleatoric 永远不可约”“高 entropy 就是 OOD”“MI 是唯一 epistemic 真值”。
