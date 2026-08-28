---
type: solution
status: draft
area: [learning-theory/posterior-predictive, ensembles, approximate-bayes]
topic: "[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"
exercise: "[[习题 - Bayesian Posterior Predictive、Ensemble 与近似边界]]"
prerequisites: ["[[Bayesian Posterior Predictive、Ensemble 与近似边界]]"]
related: ["[[Conformal Prediction 与有限样本 Coverage]]"]
created: 2026-08-23
updated: 2026-08-28
---

# 解答 - Bayesian Posterior Predictive、Ensemble 与近似边界

> [!warning] 解题原则
> 先问目标积分相对于哪个 posterior，再问实际成员怎样产生。更多成员只直接减少既定成员分布下的 Monte Carlo 误差。

## A. 识别与复述

### LT-BPP-A01

parameter posterior 是 $p(\theta\mid D)$；由可测映射 $\theta\mapsto f_\theta$ push forward 得 function distribution；再结合 $p(y_*\mid x_*,\theta)$ 得
$$
p(y_*\mid x_*,D)=\int p(y_*\mid x_*,\theta)p(\theta\mid D)d\theta.
$$
algorithmic ensemble 是 $\widehat\theta_m=\mathcal A(D,\xi_m)$ 诱导的经验函数 mixture，权重来自算法/随机种子，通常不是 Bayes posterior。参数对称可使 parameter distribution 很宽而 function distribution 很窄。

### LT-BPP-A02

exact/high-quality MCMC 目标是明确定义 posterior，但深网计算难；VI 在受限 $q_\phi$ 中优化 divergence，有 family/mode bias；MC dropout 依赖特定 dropout variational contract；SWAG 用 SGD 轨迹拟合局部低秩+对角 Gaussian；deep ensemble 用独立训练 runs，理论身份是 algorithmic mixture；bootstrap ensemble 重采样独立数据单位，混合 sampling variability 与训练算法。六者不能共用“posterior samples”标签。

### LT-BPP-A03

parameter mean plug-in 是 $p(y\mid x,E\Theta)$；probability mixture 是 $E[p(y\mid x,\Theta)]$，非线性下不交换。logit averaging 又是 $\operatorname{softmax}(E[z])$，而 probability averaging 是 $E[\operatorname{softmax}(z)]$。softmax 非线性且 logits 有尺度/平移自由度，因此三者一般不同。

## B. 手算与局部推导

### LT-BPP-B01

$$
\bar\mu=(0+2+4)/3=2.
$$
within：
$$
(1+1+4)/3=2.
$$
between：
$$
[(0-2)^2+(2-2)^2+(4-2)^2]/3=8/3.
$$
total：
$$
2+8/3=14/3.
$$
等价地，$M^{-1}\sum(\sigma_m^2+\mu_m^2)-\bar\mu^2=(1+0+1+4+4+16)/3-4=14/3$。

### LT-BPP-B02

第一成员
$$
p_1(Y=1)=\frac9{9+1}=0.9;
$$
第二成员
$$
p_2(Y=1)=\frac1{1+4}=0.2.
$$
概率 mixture 为 $0.55$。平均 logits 为 $(\tfrac12\log9,\tfrac12\log4)=(\log3,\log2)$，softmax 后
$$
p_{\rm logit\ avg}(Y=1)=\frac3{3+2}=0.6.
$$
两者不同；只有前者是等权 categorical mixture。

### LT-BPP-B03

iid 时 standard error：
$$
\sqrt{0.04/4}=0.1,\qquad
\sqrt{0.04/16}=0.05.
$$
相关时
$$
\operatorname{Var}(\bar G)
=0.04\left(0.2+\frac{0.8}{16}\right)
=0.01,
$$
SE 回到 0.1。有效成员数
$$
M_{\rm eff}\approx\frac{16}{1+15(0.2)}=4.
$$
16 个相关成员只提供约 4 个独立成员的信息。

## C. 证明与反例

### LT-BPP-C01

$-\log u$ 在 $u>0$ 上凸，故
$$
-\log\left(\frac1M\sum_mp_m(y)\right)
\le\frac1M\sum_m-\log p_m(y).
$$
这是与成员平均比较；右侧可能远大于最佳成员的 $-\log\max_mp_m(y)$，所以 mixture 可比最佳成员差。也不推出 accuracy/calibration/shift 排名，因为这些 functional 不由同一逐点 Jensen 不等式控制。

### LT-BPP-C02

令 $f_\theta(x)=\theta^2x$，posterior 对 $\theta=\pm1$ 等权。则
$$
E[f_\Theta(x)]=x,
\qquad
f_{E\Theta}(x)=f_0(x)=0.
$$
更极端地令 modes 在 $\pm10$，两者函数都为 $100x$，posterior mean parameter 仍为 0 并给零函数。参数 mean 位于低 posterior density 的对称中心；parameter averaging 还忽略神经网络 permutation/scale symmetry。

### LT-BPP-C03

对目标 $I_p=E_p g$、近似 $I_q=E_qg$ 和 MC estimate：
$$
\widehat I_M-I^*
=
(\widehat I_M-I_q)
+(I_q-I_p)
+(I_p-I^*).
$$
在 iid finite-variance 下第一项均值 0、方差 $\operatorname{Var}_q(g)/M$；第二、三项不含 $M$。所以 $M\to\infty$ 只令 $\widehat I_M\to I_q$，若 $q\ne p$ 或模型错设，bias 保留。

## D. 审计与诊断

### LT-BPP-D01

需说明训练时 dropout 是否按相应 objective 使用、placement/rate、weight decay 与 prior/likelihood precision 的对应、test masks 的独立性和跨 token/time sharing、哪些层随机、BatchNorm 冻结/重估、10 samples 的 MC SE、calibration data 与 shift test。临时对 deterministic pretrained model 打开 dropout 没有自动继承 variational posterior 解释；10 也不是由理论统一规定的充分样本数。

### LT-BPP-D02

同时给 per-member 与 total FLOPs/tokens/steps、wall time、memory、trainable parameters、search budget、data/augmentation、calibration 和 serving latency。比较 single strongest member、same-total-compute single/wider model、$M$-member mixture；报告 NLL/Brier/accuracy/calibration/risk–coverage、within/between spread、pairwise prediction correlation、$M$-curve 和 MC SE。SWAG/MC dropout 还披露 samples 与 BN；不能让 ensemble 获得 $M$ 倍训练预算后只称“方法更好”。

### LT-BPP-D03

按预注册 severity 生成或收集 shifts，并保留真实 provenance；每点用同一 locked examples/splits 画 accuracy、NLL、Brier、ECE 配置、risk–coverage/abstention utility，附 paired uncertainty。区分 corruption、new site、prevalence、concept/time shift；报告 confidence histogram 与 subgroup。clean NLL 只支持 source claim，不能证明 shift robustness。

## E. 研究与迁移

### LT-BPP-E01

weight ensemble 是多个参数函数的概率 mixture，只有成员来自定义 posterior 才可称 posterior predictive approximation；prompt ensemble 是接口/measurement variation；decoder sampling 是单一 conditional generator 的 output randomness；self-consistency 是对生成 paths/answers 的 aggregation。后三者可作为 algorithmic mixtures，但不能直接叫 weight posterior epistemic uncertainty。所有方法要声明 weights、semantic clustering、temperature 与 answer event。

### LT-BPP-E02

observation noise 进 likelihood；parameter posterior 在给定 PDE/solver 模型内；discretization 由 mesh/time-step refinement 或 numerical-error model；surrogate error 比较 neural surrogate 与高精度 solver；model-form error 比较 PDE 与真实系统。weight ensemble可能表达部分 parameter/function/optimization variation，不能自动表达共同的 discretization bias 或错误 PDE。需要 multi-fidelity、residual/conservation tests、实验数据和 model averaging。

### LT-BPP-E03

card 包含 prior/likelihood 或明确声明“非 Bayesian”，成员算法、数据/seed、probability-space组合、member weights、correlation/$M_{\rm eff}$、MC SE、approximation family、BN、calibration、proper scores、shift curves、strongest-member和compute。允许：“在给定 algorithmic ensemble 与数据上，概率 mixture 的 NLL/coverage 为……”。拒绝：“成员是真 posterior”“spread 是完整 epistemic”“更多 members 修复错设”“clean 优势保证 OOD”。
