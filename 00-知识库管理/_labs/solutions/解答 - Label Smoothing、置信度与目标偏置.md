---
type: solution
status: draft
area: [neural-networks/regularization, label-smoothing, cross-entropy, calibration]
topic: "[[Label Smoothing、置信度与目标偏置]]"
exercise: "[[习题 - Label Smoothing、置信度与目标偏置]]"
sources: ["[[S-2016-Szegedy-Label-Smoothing]]", "[[S-2019-Muller-Label-Smoothing]]", "[[S-2026-PyTorch-CrossEntropy-Label-Smoothing]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Label Smoothing、置信度与目标偏置

## A

### NN-LSM-A01
Inclusive uniform convention 是
$$
t=(1-\epsilon)e_y+\epsilon(1/K)\mathbf1,
$$
所以 $t_y=1-\epsilon+\epsilon/K$、$t_k=\epsilon/K$。Exclude-true convention 是 $t_y=1-\epsilon_{\rm ex}$、$t_k=\epsilon_{\rm ex}/(K-1)$。令错误类质量相等得
$$
\epsilon/K=\epsilon_{\rm ex}/(K-1),
\qquad
\epsilon=\frac{K}{K-1}\epsilon_{\rm ex}.
$$
换算还要检查参数仍在合法区间；不能只比较名义 $\epsilon$。

### NN-LSM-A02
Confidence 是单次 prediction 的 maximum probability/entropy；calibration 是 prediction 与 outcome 的群体对应关系；epistemic uncertainty 讨论知识/模型状态不确定性。Label Smoothing 直接改变监督 target 与 loss gradient，通常间接压缩 confidence。它是否改善 calibration 需 held-out outcome 验收，也不从 target smoothing 自动得到 epistemic 分解。

### NN-LSM-A03
交叉熵对 target 线性：$H(t,p)=(1-\epsilon)H(e_y,p)+\epsilon H(u,p)$。又有
$$H(u,p)=H(u)+\operatorname{KL}(u\|p).$$
Uniform $u$ 时 $H(u)=\log K$ 是常数，故附加可优化项是 reverse-direction $\operatorname{KL}(u\|p)$。而 $\operatorname{KL}(p\|u)=\log K-H(p)$ 才直接对应 entropy penalty；KL 不对称，所以两者梯度与 boundary behavior 不同。

## B

### NN-LSM-B01
True component 为
$$1-0.2+0.2/5=0.84,$$
其余四项各 $0.04$，target 为 $(0.04,0.04,0.84,0.04,0.04)$。Entropy：
$$
H(t)=-0.84\log0.84-4(0.04\log0.04)\approx0.66148.
$$
最优 true-vs-wrong margin 是
$$
\log(0.84/0.04)=\log21\approx3.04452.
$$

### NN-LSM-B02
$t=(14/15,1/30,1/30)$。因此
$$
L=-\frac{14}{15}\log0.8-\frac1{15}\log0.1\approx0.36177.
$$
Logit gradient：
$$p-t=(-0.13333,0.06667,0.06667).$$
Hard target gradient 是 $p-e_1=(-0.2,0.1,0.1)$。Smoothing 不是把整个 gradient 统一乘 $2/3$ 的一般操作；此对称 toy 恰有相同比例，但一般 $p,K,u$ 下 component offsets 不同。

### NN-LSM-B03
$$
r=0.8(0.7,0.2,0.1)+0.2(1/3,1/3,1/3)
=(0.62667,0.22667,0.14667).
$$
Argmax 仍是 class 1，因为 uniform affine shrink 保持所有 pairwise signs。形式反变换
$$
(r-0.2u)/0.8=(0.7,0.2,0.1)=\eta.
$$
有限模型输出若不在合法 affine image 中，反变换可能越出 simplex，并把误差放大 $1/(1-\epsilon)$。

## C

### NN-LSM-C01
代入 $t=(1-\epsilon)e_y+\epsilon u$：
$$
-\sum_kt_k\log p_k
=-(1-\epsilon)\log p_y-\epsilon\sum_ku_k\log p_k.
$$
即 $(1-\epsilon)H(e_y,p)+\epsilon H(u,p)$。由 KL 定义
$$
\operatorname{KL}(u\|p)=\sum_ku_k\log u_k-\sum_ku_k\log p_k
=-H(u)+H(u,p),
$$
故 $H(u,p)=H(u)+\operatorname{KL}(u\|p)$。Uniform 时 $H(u)=\log K$。

### NN-LSM-C02
$\partial L/\partial p_k=-t_k/p_k$，softmax Jacobian为 $\partial p_k/\partial z_j=p_k(\mathbf1_{k=j}-p_j)$。链式求和：
$$
\frac{\partial L}{\partial z_j}
=-t_j(1-p_j)+p_j\sum_{k\ne j}t_k
=p_j-t_j,
$$
其中 $\sum_kt_k=1$。可完全拟合时 $p=t$；uniform target 给
$$z_y-z_k=\log(p_y/p_k)=\log\frac{K-(K-1)\epsilon}{\epsilon}.$$

### NN-LSM-C03
Uniform $u$ 下
$$r_i-r_j=(1-\epsilon)(\eta_i-\eta_j).$$
$\epsilon<1$ 时乘数为正，ranking 保持。反例取二分类 $\eta=(0.51,0.49)$、$\epsilon=0.5$、nonuniform $u=(0,1)$：
$$r=0.5\eta+0.5u=(0.255,0.745),$$
argmax 从 class 1 翻到 class 2。Nonuniform prior 是任务假设，不是无害常数。

## D

### NN-LSM-D01
Maximum probability 降低只是 confidence 变化。Calibration 要比较预测与真实频率，smoothing 甚至使理想 population optimum 从 $\eta$ 变为 $(1-\epsilon)\eta+\epsilon u$；经验改善来自抵消有限模型过度置信，需 NLL/Brier/reliability 验证。Epistemic uncertainty 还需模型/知识状态语义；人为加入 $\epsilon$ 不识别 uncertainty source。正确表述是“可能改变并常降低 confidence，校准与 uncertainty 另测”。

### NN-LSM-D02
Inclusive convention 等价于：以 $1-\epsilon$ 保留 label，以 $\epsilon$ 从所有 $K$ 类 uniform 重抽，故最终仍可能是 true class。Exclude-true 则以 $\epsilon_{\rm ex}$ 强制翻到 $K-1$ 个错误类之一。若真实 corruption transition 与这两者不同，训练 bias 未匹配；即使匹配，finite model/optimization 与 clean-risk tradeoff 仍需实验。因此只能在声明的 transition、noise rate 与 evaluation clean/noisy distribution 下说抗噪。

### NN-LSM-D03
验收小 logits：手算 hard/smoothed target、per-class weighted loss 与 $p-t$ gradient；分别测试 class-index API 和 probability-target API；检查 ignored positions 的 numerator/denominator、all-ignored batch；确认 class weight 是按每个 target component 还是 hard class；对 sampled/adaptive vocabulary 核对 uniform prior term是否 exact full-vocabulary；覆盖 reduction `none/sum/mean`、低精度和非法 probability target。配置名一致不足以证明公式一致。

## E

### NN-LSM-E01
以等额 tuning 比较 $\epsilon=0$ 和多个 target-equivalent smoothing levels；将 inclusive/exclusive 换算后复验，比较 uniform、empirical-prior、class-dependent prior。固定 architecture、optimizer/schedule、augmentation、steps、early stopping、paired seeds 和 validation budget。报告 accuracy、NLL、Brier、可靠性/ECE estimator、margin/target entropy、classwise/rare-class risk，以及预声明 noise/shift。结论限于所测 target contract 与分布。

### NN-LSM-E02
第一段训练多组 teacher（hard/smoothed），匹配 compute/tuning，测 teacher accuracy/NLL/calibration 与 logits/representation information；第二段固定同一 teacher，扫描 distillation temperature/weight 与 student seeds；第三段用相同 student baseline 比较 teacher variants，并控制 teacher accuracy或做分层。若 smoothed teacher transfer 变差，要区分 teacher 本身质量、dark-class information 压缩和 student optimization，而非只看最终 student score。

### NN-LSM-E03
窄命题例：(1) 在已知 exclude-true symmetric transition rate $\rho$ 下，某 $\epsilon$ 降低 clean test risk——预先指定 $K,\rho$、clean estimand；(2) 在 instance-independent uniform corruption 下，smoothing 降低 noisy-label memorization 但不过度增加 clean bias——测 train noisy fit、clean risk；(3) 在 class-dependent corruption 下，transition-aware prior 优于 uniform prior——固定 transition estimation protocol。三条都只支持相应 corruption、模型和 tuning 范围，不推出任意真实标注错误下的普适鲁棒性。
