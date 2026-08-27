---
type: solution
status: draft
topic: "[[习题 - Experts、Weighted Majority 与 Multiplicative Weights]]"
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Experts、Weighted Majority 与 Multiplicative Weights

## A

### LT-MW-A01
给 prior $\pi_i>0$，令 $w_{1,i}=\pi_i$、$p_{t,i}=w_{t,i}/W_t$。根据 $p_t$ 混合或采样，承受 mixture loss $\widehat\ell_t=\langle p_t,\ell_t\rangle$，再更新
$$w_{t+1,i}=w_{t,i}e^{-\eta\ell_{t,i}}.$$
full-information 版本需要观察整个 $\ell_t$。

### LT-MW-A02
经典 deterministic Weighted Majority 对错误专家乘固定折扣并作加权多数表决；randomized WM 按权重采样专家；Hedge 允许一般 $[0,1]$ loss 并用指数更新。它们共享 multiplicative potential，但 prediction 与损失模型不同。

### LT-MW-A03
对任一专家 $i$，下界是
$$W_{T+1}\ge w_{T+1,i}=\pi_i e^{-\eta L_{T,i}}.$$
上界由 Hoeffding lemma 给
$$\log(W_{t+1}/W_t)\le-\eta\langle p_t,\ell_t\rangle+\eta^2/8.$$
取对数、对 $t$ 求和并夹住同一 potential，得到 regret。

## B

### LT-MW-B01
$e^{-\eta}=1/2$、$e^{-\eta/2}=1/\sqrt2$，新 weights 为
$$\left(1,\frac12,\frac1{\sqrt2}\right).$$
归一化常数 $Z=3/2+1/\sqrt2\approx2.2071$，probabilities 约为 $(0.4531,0.2265,0.3204)$。

### LT-MW-B02
令 $f(\eta)=\log N/\eta+\eta T/8$。由 $f'(\eta)=0$ 得
$$\eta^*=\sqrt{\frac{8\log N}{T}},\qquad f(\eta^*)=\sqrt{\frac{T\log N}{2}}.$$
若 theorem 还限制 $\eta$ 范围，则要截断到允许区间。

### LT-MW-B03
三个 complexity terms 分别是
$$\frac{\log2}{\eta},\quad\frac{\log3}{\eta},\quad\frac{\log6}{\eta}.$$
prior 越大，惩罚越小；但 prior 必须在看当前评价序列前合法确定。

## C

### LT-MW-C01
令 $L_{T,i}=\sum_t\ell_{t,i}$。由更新，$w_{T+1,i}=\pi_i e^{-\eta L_{T,i}}$，所以
$$\log W_{T+1}\ge\log\pi_i-\eta L_{T,i}.$$
另一方面，条件于 $I\sim p_t$ 且 $\ell_{t,I}\in[0,1]$，Hoeffding lemma 给
$$
\log\frac{W_{t+1}}{W_t}
=\log E_{I\sim p_t}e^{-\eta\ell_{t,I}}
\le-\eta\langle p_t,\ell_t\rangle+\frac{\eta^2}{8}.
$$
从 $1$ 到 $T$ 求和，若 $\sum_i\pi_i=1$ 则 $W_1=1$，合并上下界并除以 $\eta$：
$$
\sum_t\langle p_t,\ell_t\rangle-L_{T,i}
\le\frac{\log(1/\pi_i)}{\eta}+\frac{\eta T}{8}.
$$
uniform prior 即得到 $\log N/\eta+\eta T/8$。

### LT-MW-C02
写 $z=(\ell-a)/(b-a)\in[0,1]$。在 $z$ 上的 regret bound 乘回 $(b-a)$；共同平移 $a$ 在 learner 与 comparator 累计损失中抵消。因此最优量级变为 $(b-a)\sqrt{T\log N}$，update 可等价使用 learning rate $\eta/(b-a)$ 作用于原 loss。

### LT-MW-C03
environment 看见 sampled $I_t$ 后令 $\ell_{t,I_t}=1$、其余为 $0$。learner realized loss 为 $T$；全部专家 losses 总和为 $T$，故 best expert loss 至多 $T/N$，regret 至少 $T(1-1/N)$。标准 Hedge theorem 排除了看当前 sample 再定 loss 的 adversary。

## D

### LT-MW-D01
按 epochs $1,2,4,8,\ldots$ 重启，每段长度 $H_k=2^k$，在段内用 $\eta_k=\sqrt{8\log N/H_k}$。每段 regret $O(\sqrt{H_k\log N})$，而几何级数 $\sum_{k\le K}\sqrt{2^k}=O(\sqrt T)$，总 regret 仍为 $O(\sqrt{T\log N})$，代价只是常数。

### LT-MW-D02
若 $\pi$ 用了同一评价 loss sequence 或 target labels，专家已通过数据被选择，$\log(1/\pi_i)$ 不再是 theorem 中预先固定的 complexity。可用独立数据确定 prior，或把 prior-selection 信息纳入条件化/数据依赖先验的额外代价。

### LT-MW-D03
未选专家的 $\ell_{t,i}$ 不可见，因而无法执行每个坐标的 $w_{t+1,i}=w_{t,i}e^{-\eta\ell_{t,i}}$。bandit 版本必须保持探索并用 inverse-propensity estimator；这会引入方差与通常更差的 $\sqrt{TN}$ 依赖。

## E

### LT-MW-E01
可将 loss 归一到 $[0,1]$：质量错误、tail latency、调用成本按部署效用加权。timeout 作为可观测高损失；永久失效专家可冻结并重新归一，临时失效则在当轮 action set 中屏蔽。若只观察被调用模型，必须用 bandit routing，不能冒充 full-information Hedge。

### LT-MW-E02
entropy-FTRL 解
$$p_t=\arg\min_{p\in\Delta_N}\left\langle p,L_{t-1}\right\rangle+\frac1\eta\sum_i p_i\log\frac{p_i}{\pi_i}.$$
加入 simplex multiplier $\lambda$，一阶条件给
$$L_{t-1,i}+\eta^{-1}(\log(p_i/\pi_i)+1)+\lambda=0,$$
故 $p_{t,i}\propto\pi_i e^{-\eta L_{t-1,i}}$，即 exponential weights。

### LT-MW-E03
claim card 要固定：$N$ 与 prior、loss range、horizon 是否已知、$\eta$ 或 doubling 方法、full/bandit feedback、adversary 是否 non-anticipating、mixture 还是 sampled loss、static expert comparator，以及 expectation/high-probability 量词。
