---
type: solution
status: draft
area: [neural-networks/regularization, dropout, variance, bayesian-boundary, uncertainty]
topic: "[[Dropout 的方差、共适应解释与 Bayesian 边界]]"
exercise: "[[习题 - Dropout 的方差、共适应解释与 Bayesian 边界]]"
sources: ["[[S-2014-Srivastava-Dropout]]", "[[S-2013-Wager-Dropout-Adaptive-Regularization]]", "[[S-2016-Gal-Ghahramani-MC-Dropout]]", "[[S-2015-Kingma-Variational-Dropout]]", "[[S-2021-Su-8770-Dropout-MLM-MAE]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Dropout 的方差、共适应解释与 Bayesian 边界

## A

### NN-DBY-A01
精确代数例：“固定 $x$ 时 $\operatorname{Var}(MX/q\mid x)=px^2/q$”，由概率模型直接证明。局部近似例：“小噪声 expected loss 增量约为 $\tfrac12\operatorname{tr}(H\Sigma)$”，需噪声小与高阶余项受控。机制假说例：“随机删除 features 抑制脆弱共适应”，需中介变量和排他性实验。经验结果例：“某数据集上 Dropout 降低 test NLL”，需预注册协议、多 seeds 和统计不确定性。四层不能因措辞相似而相互升级。

### NN-DBY-A02
“减少共适应”谈表示或 features 之间的依赖机制，但需先定义 co-adaptation 指标；“隐式集成”把随机 masks 看作共享参数的子网络族，deterministic eval 只是某种近似；“近似 Bayesian inference”则要求指定 prior、variational family、likelihood、KL/regularization scaling 与预测采样。一个方法能同时接受这些视角，不表示任一视角的条件自动满足，也不表示某个 held-out gain 识别了哪种机制。

### NN-DBY-A03
MC error 是有限 $T$ 对既定 sampling distribution 的积分误差，通常随有效独立样本数增大而下降。Variational bias 来自近似 posterior family/optimization；misspecification 来自模型或 likelihood 不含真实数据过程；calibration error 还受 shift、finite data、选择和指标估计影响。单纯增加 $T$ 只直接减少第一类，不能修复后三类。

## B

### NN-DBY-B01
独立性给出
$$
\mathbb E[Y]=\frac{\mathbb EM\,\mathbb EX}{q}=\mu,
$$
$$
\mathbb E[Y^2]=\frac{\mathbb EM^2\,\mathbb EX^2}{q^2}
=\frac{\sigma^2+\mu^2}{q}.
$$
因此
$$
\operatorname{Var}(Y)=\frac{\sigma^2+p\mu^2}{q}.
$$
代入 $\mu=2,\sigma^2=3,q=0.8,p=0.2$，得 $\mathbb EY=2$、$\operatorname{Var}(Y)=(3+0.8)/0.8=4.75$。注意随机输入本身的方差也被 $1/q$ 放大。

### NN-DBY-B02
均值为 $\mathbb E[u\mid x]=a^\mathsf Tx=1-2=-1$。独立 element masks 下
$$
\operatorname{Var}(u\mid x)=\frac pq\sum_i a_i^2x_i^2=1(1+4)=5,
$$
$$
\operatorname{Cov}(u,v\mid x)=\frac pq\sum_i a_ic_ix_i^2
=1\{1\cdot2\cdot1+(-1)\cdot3\cdot4\}=-10.
$$
负 covariance 来自两个 scores 对第二个被共同 mask feature 的权重方向相反。

### NN-DBY-B03
均值为 $\bar y=6/5=1.2$。平方偏差之和为
$$
0.04+0.04+0.16+0+0.16=0.40,
$$
所以以 $1/T$ 为分母的 variance 为 $0.08$，predictive standard deviation 为 $\sqrt{0.08}\approx0.2828$。若把这五项近似当独立同分布样本，mean 的 MC standard error estimate 为
$$
\sqrt{0.08/5}\approx0.1265.
$$
前者描述 sampled predictor 分布的 spread，后者描述其均值估计因有限 $T$ 的不确定性。

## C

### NN-DBY-C01
固定 $(x,t)$，令 $\widetilde x_i=M_ix_i/q$ 且 masks 独立。Score $S=w^\mathsf T\widetilde x$ 的均值为 $w^\mathsf Tx$，方差为 $(p/q)\sum_iw_i^2x_i^2$。用 bias–variance identity：
$$
\mathbb E_M[(t-S)^2\mid x,t]
=(t-w^\mathsf Tx)^2+\frac pq\sum_iw_i^2x_i^2.
$$
对数据分布或样本平均后，附加项是
$$
\frac pq\sum_iw_i^2\,\mathbb E[X_i^2]
$$
或其 empirical version，是 feature-scale-dependent diagonal quadratic penalty。精确性依赖线性 score、平方损失和指定独立 mask 合同；不能原样外推到任意深网。

### NN-DBY-C02
在 $u$ 附近展开
$$
L(u+\varepsilon)=L(u)+\nabla L(u)^\mathsf T\varepsilon+
\frac12\varepsilon^\mathsf TH(u)\varepsilon+R_3.
$$
若 $\mathbb E\varepsilon=0$、$\operatorname{Cov}(\varepsilon)=\Sigma$，则线性项消失，并用 $\mathbb E[\varepsilon^\mathsf TH\varepsilon]=\operatorname{tr}(H\Sigma)$ 得
$$
\mathbb E L(u+\varepsilon)\approx L(u)+\frac12\operatorname{tr}(H(u)\Sigma).
$$
若 $L$ 对 $u$ 是恰好二次函数且 Hessian 常数，三阶及以上余项为零，这个式子成为精确等式。

### NN-DBY-C03
令 $\bar p(y\mid x)=T^{-1}\sum_tp_t(y\mid x)$，则
$$
H[\bar p]= -\sum_y\bar p_y\log\bar p_y,
$$
$$
\overline H=T^{-1}\sum_t\left(-\sum_yp_{t,y}\log p_{t,y}\right),
\qquad I_T=H[\bar p]-\overline H.
$$
在 samples 可解释为指定近似 posterior 下的参数/函数样本时，$I_T$ 是相应 predictive mutual information 的 MC estimator。否则它仍严格是 sampled predictors 的 disagreement statistic，但“真实 epistemic uncertainty”这一命名没有自动成立。

## D

### NN-DBY-D01
当 $T\to\infty$，只会收敛到当前 mask-induced approximate predictive distribution 的精确积分。不会自动消失的误差包括：variational family 不能表示真实 posterior；训练目标或 weight-decay/KL scaling 不对应所声称的 Bayesian model；likelihood/prior/model misspecification；优化未找到变分最优；distribution shift 与 calibration bias。因而“MC 收敛”与“Bayesian approximation 正确”是两个命题。

### NN-DBY-D02
全模型 `train()` 会让 BatchNorm 使用当前 batch statistics 并更新 running state，还可能启用 augmentation-like stochastic modules，改变的不再只是 Dropout。协议应先 `model.eval()` 固定所有 evaluation behavior，再只把 Dropout modules 切到 sampling mode，冻结参数和 BN buffers；用相同输入做 $T$ 次 no-grad forward，检查 BN running means/variances 不变，并验证 $T=1$ deterministic baseline 与 Dropout sampling 分开报告。

### NN-DBY-D03
例如实验只报告 Dropout 组 train accuracy 从 90% 到 93%，这既可能来自更长训练、学习率耦合、数据顺序或尺度改变，也不能定义 co-adaptation。可加入机制测量：feature/gradient covariance、feature ablation sensitivity、conditional mutual information、single-feature reliance；替代解释至少包括优化噪声改善和有效 learning-rate/activation-scale 改变。还应匹配训练预算与超参搜索后再看 held-out risk。

## E

### NN-DBY-E01
固定数据 split、architecture、optimizer、训练 steps、augmentation、early-stopping rule、parameter count 和 paired seeds；对 no Dropout 与多个 $q$ 分别做等额超参搜索。Optimization 账记录 train loss/gradient/update ratio/time-to-target；regularization 账记录 train–validation gap、NLL/accuracy/Brier；compute 账记录 wall time、memory、吞吐。若某 $q$ 只因训练更慢而欠拟合，不能把 gap 变小直接解释为泛化机制改善。

### NN-DBY-E02
三组使用相同 backbone/data split 与可比训练/推理预算；deterministic、$K$ 独立 deep ensemble、单模型 $T$ 次 MC Dropout 分开计 training FLOP、inference FLOP 和 storage。报告 accuracy、NLL、Brier、ECE/可靠性图，并在预先声明的 corruptions/OOD 或 selective-risk–coverage 上测试；用 paired bootstrap/seed interval。结果只支持所测分布和预算下的预测性质，不能由单个 AUROC 宣称 posterior 正确。

### NN-DBY-E03
可证伪版本包括：(1) “在明确 prior/likelihood/variational family 和 objective scaling 下，本训练目标等于或近似某 ELBO”——需形式推导；(2) “$T$ 增大时 MC mean 的数值误差按预期下降”——需 convergence/SE test；(3) “在指定 test distribution 上，MC Dropout 的 NLL/Brier/ECE 优于 deterministic baseline”——需 held-out 多 seed 实验；(4) “在指定 shift 下 disagreement 与 error/risk 单调关联”——需 selective/OOD evaluation。没有任何一条单独推出“所有 uncertainty 已校准”。
