---
type: solution
status: draft
area: [neural-networks/regularization, dropout, bernoulli-noise, train-eval]
topic: "[[Dropout 的随机掩码、期望与 Inverted Scaling]]"
exercise: "[[习题 - Dropout 的随机掩码、期望与 Inverted Scaling]]"
sources: ["[[S-2014-Srivastava-Dropout]]", "[[S-2026-PyTorch-Dropout-Stochastic-Depth]]", "[[S-2021-Su-8770-Dropout-MLM-MAE]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Dropout 的随机掩码、期望与 Inverted Scaling

## A

### NN-DRO-A01
$p\in[0,1)$ 是删除概率，$q=1-p>0$ 是保留概率，$M_i\sim\operatorname{Bernoulli}(q)$。Inverted Dropout 的合同是
$$
Y_i=\begin{cases}M_iX_i/q,&\text{train},\\X_i,&\text{eval}.\end{cases}
$$
“均值保持”首先是固定输入后的 mask 条件期望：$\mathbb E_M[Y_i\mid X=x]=x_i$。它不自动声称一般深层非线性网络的最终输出满足 $\mathbb E_M[f(Y)]=f(x)$，也不声称单次 eval 输出是所有随机函数的精确平均。

### NN-DRO-A02
对 $X\in\mathbb R^{B\times T\times D}$，常见合同可写为：element mask $(B,T,D)$；channel/feature mask $(B,1,D)$；token mask $(B,T,1)$；sample mask $(B,1,1)$；path mask 通常作用在 residual branch 输出，shape 为 $(B,1,1)$ 或全 batch 共享的 $(1,1,1)$。尺寸为 1 的轴通过 broadcast 共享同一 Bernoulli 变量。名称不是充分合同；必须同时记录 shape、broadcast axes、是否跨层/时间复用。

### NN-DRO-A03
历史合同可在训练时用 $MX$、测试时用 $qX$；inverted 合同在训练时用 $MX/q$、测试时用 $X$。前者的 train mean 为 $qx$，后者为 $x$。若随后只有确定仿射映射，历史合同的 test scaling 与随机 train 输出的一阶矩相配，而 inverted 合同把这一步预先移到训练阶段。两者的参数化和数值轨迹不同，不能混着载入 checkpoint。

## B

### NN-DRO-B01
采样输出为
$$
y=\frac mq\odot x=2(1,0,1)\odot(2,-1,3)=(4,0,6).
$$
由于 $p/q=1$，
$$
\mathbb E[Y\mid x]=(2,-1,3),\qquad
\operatorname{Var}(Y_i\mid x)=(4,1,9).
$$
二阶矩为 $\mathbb E[Y_i^2\mid x]=x_i^2/q=(8,2,18)$，所以
$$
\mathbb E\|Y\|_2^2=8+2+18=28,
$$
而 $\|x\|_2^2=14$。均值保持并不保持能量。

### NN-DRO-B02
Dropout 的局部 Jacobian 是 $\operatorname{diag}(m/q)$，故
$$
\bar x=\frac mq\odot g=(2,0,8).
$$
若 $x=Wa$，记 $h=(m/q)\odot g$，则
$$
\nabla_WL=ha^\mathsf T,\qquad \nabla_aL=W^\mathsf Th.
$$
同一次 forward/backward 必须复用同一 mask；backward 重采样会得到另一个计算图的导数。

### NN-DRO-B03
$Y$ 以各 $1/2$ 的概率取 $0$ 和 $2$。因此
$$
\mathbb E[f(Y)]=\tfrac12\operatorname{ReLU}(-1)+\tfrac12\operatorname{ReLU}(1)=\tfrac12,
$$
但 $\mathbb EY=1$，所以 $f(\mathbb EY)=\operatorname{ReLU}(0)=0$。它否定“一阶矩在任意非线性后仍可交换”的普遍命题；它没有否定被 mask 张量本身的条件均值保持，也没有否定仿射 $f$ 下的等式。

## C

### NN-DRO-C01
Bernoulli 变量满足 $\mathbb EM=q$、$\mathbb EM^2=q$、$\operatorname{Var}(M)=qp$。固定 $x_i$ 后，
$$
\mathbb E[Y_i\mid x_i]=\frac{x_i}{q}\mathbb EM=x_i,
$$
$$
\mathbb E[Y_i^2\mid x_i]=\frac{x_i^2}{q^2}\mathbb EM^2=\frac{x_i^2}{q},
$$
从而
$$
\operatorname{Var}(Y_i\mid x_i)=\frac{x_i^2}{q}-x_i^2=\frac pqx_i^2.
$$
当 $q\to0^+$ 且 $x_i\ne0$ 时，二阶矩与方差都按 $1/q$ 量级发散；罕见保留样本的幅度为 $x_i/q$。

### NN-DRO-C02
期望与确定线性算子可交换：
$$
\mathbb E[AY+b\mid x]=A\mathbb E[Y\mid x]+b=Ax+b.
$$
一般非线性没有这个交换律；Jensen 不等式甚至表明凸函数通常只有 $f(\mathbb EY)\le\mathbb E f(Y)$。B03 已给出严格反例。深网还会让后层 mask 的输入依赖前层 mask，因此不能只对每层局部均值反复代换。

### NN-DRO-C03
若坐标 $i,j$ 共用同一个 $M$，则
$$
Y_i=\frac Mqx_i,\qquad Y_j=\frac Mqx_j,
$$
$$
\operatorname{Cov}(Y_i,Y_j\mid x)
=\frac{x_ix_j}{q^2}\operatorname{Var}(M)
=\frac pqx_ix_j.
$$
若 $M_i,M_j$ 独立且 $i\ne j$，该 covariance 为 0。两种设计每个坐标仍有相同均值和方差，却有不同联合分布；后续混合层、loss 与梯度会感知这个差异。

## D

### NN-DRO-D01
该命题只对 Dropout 紧接确定仿射映射、且讨论相应一阶矩时精确成立。一般非线性、多个随机层和 mask-dependent evaluation points 会破坏逐层交换。较弱且准确的表述是：“inverted scaling 精确保持被 mask 张量的条件均值；identity eval 是常用的 deterministic approximation，其预测质量需实验验收。”若要估计随机网络的 predictive mean，应明确采样合同并做 MC averaging。

### NN-DRO-D02
`Dropout → BatchNorm` 会把随机零值与 $1/q$ spikes 纳入 batch/running statistics；eval 时 Dropout 消失而 BatchNorm 使用训练累计状态，可能产生额外 train/eval shift。`BatchNorm → Dropout` 不污染该层已计算的 BN statistics，但随机输出仍改变下游层输入。`LayerNorm → Dropout` 没有 running statistics，却仍改变每样本后续二阶矩；若顺序反过来，LayerNorm 会重新标准化并耦合 mask coordinates。必须记录顺序和 axes，不能只写“都用了 normalization”。

### NN-DRO-D03
Checkpoint 重算若不恢复同一 RNG state，backward 会对另一张随机图求导。Gradient accumulation 中若意外复用 mask，会使 microbatches 相关；data parallel 中不当同步或不当重复 seeds 会改变 replica covariance。至少测试：(1) 固定 seed 的 forward bitwise/容差复现；(2) checkpoint on/off 的 loss 与梯度一致；(3) 不同 replicas/microbatches 的 mask 独立性符合合同；还应记录 generator、seed/counter、mask shape、train/eval state。

## E

### NN-DRO-E01
先做 shape/broadcast tests，检查输出 shape、dtype/device 和 mask 共享轴；用大样本固定 $x$ 验证 sample mean $\approx x$、variance $\approx(p/q)x^2$；在小张量上与显式 mask 公式比较 forward/VJP，并做 finite differences（避开会改变 mask 的调用）；eval 必须恒等且不消耗约定外 RNG；同 seed 同输出、不同 seed 的统计独立性要符合合同。再覆盖 $p=0$、接近 1、zero input、mixed precision 和 noncontiguous tensor。

### NN-DRO-E02
固定 architecture、总训练步、optimizer/schedule、数据顺序、augmentation、参数预算和 paired seeds；三组只改变 mask shape，并按同一 nominal $q$ 起步，另做 matched output-variance sensitivity。报告 train loss、held-out NLL/accuracy、activation moments、gradient/update ratios、wall time/memory。若 channel mask 更优，只能说该架构与协议下的 structured noise 更合适，不能据此证明所有表示都应共享 feature mask。

### NN-DRO-E03
逐层审计：(1) 对被 mask tensor，条件均值、方差和 VJP 可由 Bernoulli 代数精确证明；(2) 对其后的仿射层，一阶矩仍精确；(3) 对含非线性与多 mask 的最终 predictive mean，需枚举或 MC，并报告 sampling error；(4) “无需集成仍有更好泛化”是 held-out empirical claim；(5) “等价 Bayesian model averaging”还需 prior、variational family、likelihood 和目标的形式对应。每条结论都要写对象、条件和证据等级。
