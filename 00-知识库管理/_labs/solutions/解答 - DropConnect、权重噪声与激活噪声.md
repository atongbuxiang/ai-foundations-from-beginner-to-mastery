---
type: solution
status: draft
area: [neural-networks/regularization, dropconnect, weight-noise, activation-noise, stochastic-estimators]
topic: "[[DropConnect、权重噪声与激活噪声]]"
exercise: "[[习题 - DropConnect、权重噪声与激活噪声]]"
sources: ["[[S-2013-Wan-DropConnect]]", "[[S-1995-Bishop-Training-with-Noise]]", "[[S-2015-Kingma-Variational-Dropout]]", "[[S-2013-Wager-Dropout-Adaptive-Regularization]]", "[[S-2026-PyTorch-Dropout-Stochastic-Depth]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - DropConnect、权重噪声与激活噪声

## A

### NN-NOI-A01
以 $z=Wx+b$ 为基准，可写成：activation Dropout
$$z=W(D_mx)+b,\quad D_m=\operatorname{diag}(m/q);$$
DropConnect
$$z=(W\odot M/q)x+b;$$
additive weight noise
$$z=(W+E)x+b;$$
additive activation noise
$$z=W(x+\varepsilon)+b;$$
multiplicative Gaussian activation noise
$$z=W\{x\odot(1+\alpha\xi)\}+b.$$
最后一种通常取 $\mathbb E\xi=0$、$\operatorname{Var}(\xi)=1$。公式相似不表示随机对象或 covariance 相同。

### NN-NOI-A02
Activation mask 可与 $x$ 同 shape，或沿 channel/token/sample axes broadcast；DropConnect mask 可与 $W$ 同 shape，或按 row/filter/block 共享；weight noise 同理。Per-example noise 使不同样本的 noise 条件独立，per-batch shared noise 会让所有样本通过同一随机函数，产生跨样本 covariance；recurrent/time-shared noise 在时间上相关，而每步重采样会注入 temporal white-like noise。任何推导都应把这些 axes 写进概率空间。

### NN-NOI-A03
Forward noise 先改变被求导的随机函数；gradient masking 直接改 backward estimator；optimizer noise 在得到 gradient 后改变 update。Dropout/DropConnect 的某些参数梯度因 forward mask 为零而为零，但同样的 zero gradient 也可能来自 ReLU、显式 stop-gradient、稀疏 loss 或人为 gradient mask。必须核对 forward 输出及其对同一随机变量的导数，而不是只看梯度零值。

## B

### NN-NOI-B01
无噪声输出为
$$Wx=(4,-1)^\mathsf T.$$
两种 inverted noise 都保持该条件均值。Activation Dropout 的 covariance 为
$$
\frac pqW\operatorname{diag}(x_1^2,x_2^2)W^\mathsf T
=\begin{bmatrix}8&-2\\-2&5\end{bmatrix}.
$$
独立 connection masks 下，不同 output rows 使用独立随机变量，所以
$$
\operatorname{Cov}(z^{\rm dc}\mid x)
=\begin{bmatrix}8&0\\0&5\end{bmatrix}.
$$
边际均值和方差相同，但 activation mask 被两个 outputs 共享，造成 $-2$ 的 cross covariance。

### NN-NOI-B02
Activation mask 给 $D_m=\operatorname{diag}(2,0)$。先算 $W^\mathsf Tg=(5,4)^\mathsf T$，故
$$
\nabla_xL=D_mW^\mathsf Tg=(10,0)^\mathsf T,
$$
$$
\nabla_WL=g(D_mx)^\mathsf T
=\begin{bmatrix}3\\-2\end{bmatrix}(4,0)
=\begin{bmatrix}12&0\\-8&0\end{bmatrix}.
$$
DropConnect mask 全 1 时 effective weight 为 $2W$，所以
$$
\nabla_xL=2W^\mathsf Tg=(10,8)^\mathsf T,
$$
$$
\nabla_WL=(M/q)\odot(gx^\mathsf T)
=2\begin{bmatrix}6&3\\-4&-2\end{bmatrix}
=\begin{bmatrix}12&6\\-8&-4\end{bmatrix}.
$$

### NN-NOI-B03
第 $i$ 个输出噪声为 $\sum_jE_{ij}x_j$。若 entries 独立同方差，
$$
\operatorname{Var}(z_i\mid x)=\sigma_W^2\sum_jx_j^2=\sigma_W^2\|x\|_2^2,
$$
不同 rows 的 covariance 为 0；共享/相关 weight noise 时需保留完整 covariance。对 activation noise，随机项为 $W\varepsilon$，故
$$
\operatorname{Cov}(z\mid x)=W\Sigma_\varepsilon W^\mathsf T.
$$
若 $\Sigma_\varepsilon=\sigma^2I$，则为 $\sigma^2WW^\mathsf T$。

## C

### NN-NOI-C01
Activation Dropout 有
$$z_i=\sum_jW_{ij}x_jM_j/q+b_i.$$
独立 features 给
$$
\operatorname{Cov}(z_i,z_k\mid x)=\frac pq\sum_jW_{ij}W_{kj}x_j^2.
$$
DropConnect 则为 $z_i=\sum_jW_{ij}x_jM_{ij}/q+b_i$。若所有 $M_{ij}$ 独立，$i\ne k$ 时任意 $M_{ij}$ 与 $M_{kr}$ 独立，cross covariance 为 0。若 mask 按 column/filter 共享或 weight noise 相关，这个零结论不再成立。

### NN-NOI-C02
令扰动对象为 $u$，$\mathbb E\varepsilon=0$、covariance 为 $\Sigma$。Taylor 展开并取期望得
$$
\mathbb E L(u+\varepsilon)\approx L(u)+\frac12\operatorname{tr}(H_uL\,\Sigma).
$$
若 $u$ 是 input/activation，Hessian 是 loss 对表示的曲率；若扰动先经线性映射，在平方损失等条件下可重写成 input–output Jacobian penalty；若 $u$ 是 preactivation，则测其局部曲率；若 $u=W$，则是 parameter-space Hessian contraction。坐标、covariance 与 loss 变了，所得 penalty 就变了，不能统一叫同一个 weight decay。

### NN-NOI-C03
在 Gaussian variational layer 中，随机 weights 诱导每个样本 preactivation 的 Gaussian marginal，其 mean/variance 可先计算，再直接采 local preactivation noise。这可减少 minibatch 样本共享同一 weight draw 造成的 gradient correlation，从而降低 estimator variance。它保持所推导的一维或逐样本 marginals，但若为每个样本独立采 local noise，会改变由同一 global weight sample 产生的跨样本联合依赖；非 Gaussian、非线性或结构化 posterior 时还需额外条件。

## D

### NN-NOI-D01
B01 已给反例：两者的两个 marginal variances 都是 $(8,5)$，但 cross-output covariance 分别为 $-2$ 与 0，所以后续非线性或 joint loss 看到不同分布。它们还会在参数梯度稀疏位置、mask storage/communication、跨样本共享方式、parameter-space vs activation-space curvature，以及可能的 kernel 实现成本上不同。匹配对角线不是匹配 covariance，更不是匹配训练轨迹。

### NN-NOI-D02
生成和读取 dense mask 本身有 RNG 与 memory traffic；dense GEMM 在看到大量数值零时通常仍执行相同 multiply–accumulate。若先构造 masked dense weight，再调用 dense kernel，既没有跳过计算还可能增加带宽。真正加速需要结构化稀疏、可预测 block pattern 或 branch short-circuit，以及支持该 pattern 的 kernel；过细的随机 sparsity 会造成 divergence、索引开销和低 utilization。必须用 profiler/算子 trace，而不能用 zero ratio 推算 FLOP。

### NN-NOI-D03
考虑 minibatch 中两个样本。一次 global Gaussian weight draw 与为每个样本独立采 local preactivation noise，可以匹配每个样本的 preactivation marginal mean/variance；前者让两个样本的输出通过同一 $\Delta W$ 相关，后者消除这部分 covariance。因此 batch loss gradient 的 covariance、有效样本数与 update noise 不同。Forward-only test 若只检查每样本 histogram 会通过，却遗漏 cross-sample covariance 和 VJP/parameter-gradient distribution。

## E

### NN-NOI-E01
在固定 $W,x$ 上调各噪声参数，使每个 output 的 conditional mean 和 diagonal variance 尽量匹配；用足够多 samples 与置信区间验收。随后必须额外比较完整 output covariance、higher quantiles/tails、cross-example covariance、loss distribution、input VJP 和 parameter-gradient covariance。若联合统计不同，实验只能称 matched marginal moments，而不能称等价 noise model。

### NN-NOI-E02
Matched-quality 轨道调每种方法到相近 validation metric，再比较 wall time、memory、calibration、robustness 与训练稳定性，回答“达到同等质量代价如何”。Natural protocol 轨道则按各方法推荐的 noise rate、optimizer 和实现分别优化，回答“现实使用的最佳可达表现如何”。前者牺牲各方法自由发挥，后者混入 tuning/compute 差异；两者并列报告比强行一个排行榜更诚实。

### NN-NOI-E03
Exact 层：特定线性模型、平方损失与指定零均值 noise 下，expected noisy risk 可精确分解为 clean risk 加二次项。Approximate 层：一般 smooth network 的小噪声展开给 $\tfrac12\operatorname{tr}(H\Sigma)$，其 Jacobian/Tikhonov 形式还依赖 loss 与坐标。False generalization：把 input-noise 结果推广到任意 weight/activation/gradient noise，再声称都等价 isotropic $\lambda\|W\|^2$。扰动位置、covariance、非线性与高阶项都可使结论不同。
