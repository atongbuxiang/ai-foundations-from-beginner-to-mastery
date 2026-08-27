---
type: solution
status: draft
area: [learning-theory/lower-bounds, statistics/minimax]
topic: "[[样本复杂度下界与 Minimax 视角]]"
exercise: "[[习题 - 样本复杂度下界与 Minimax 视角]]"
prerequisites: ["[[No-Free-Lunch 与归纳偏置]]", "[[交叉熵与 KL 散度]]", "[[假设检验、置信区间与多重比较]]"]
related: ["[[二分类统计学习基本定理]]", "[[互信息与信息论泛化界]]"]
sources: ["[[S-1997-Yu-Assouad-Fano-Le-Cam]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - 样本复杂度下界与 Minimax 视角

> [!warning] 使用边界
> lower bound 必须与 upper bound 使用同一个 problem family、sampling protocol、loss 和 probability mode。否则“匹配”只是表面公式相似。

## A. 识别与复述

### LT-MIN-A01

expected minimax risk：

$$
\inf_A\sup_{P\in\mathcal P}\mathbb E_{P^m}L(A(S),P).
$$

high-probability minimax quantile：先对每个 $A,P$ 求使 tail $\le\delta$ 的最小半径，再取 $\inf_A\sup_P$。PAC sample complexity 是最小 $m$，使存在 $A$ 对所有 $P$ 都有

$$
\Pr(L(A(S),P)>\varepsilon)\le\delta.
$$

第一者平均 loss，后两者控制 tail；quantile 固定 $m$ 求半径，sample complexity 固定半径求 $m$。

### LT-MIN-A02

Le Cam 用两个 distributions，把 estimation 归约为 binary testing；Fano 用许多 pairwise-separated distributions/packing，把识别 index 所需的 $\log N$ information 写入 lower bound；Assouad 用 hypercube 邻接 worlds，逐坐标做 binary tests 并累加 Hamming/coordinate loss。

### LT-MIN-A03

一个算法失败只说明算法选择不好。minimax 必须任取 $A$ 或任取 estimator/test，并构造它无法区分的 worlds。需检查：worlds 在允许 family 内、最优 decisions 有 separation、sample distributions 的 KL/TV 足够小、learner success 可解码 world、testing theorem 对所有 decoders 成立，以及 expected/high-probability 口径一致。

## B. 手算与构造

### LT-MIN-B01

single-sample KL：

$$
\begin{aligned}
\mathrm{KL}(P_0\|P_1)
&=0.45\log\frac{0.45}{0.55}
+0.55\log\frac{0.55}{0.45}\\
&=0.1\log\frac{0.55}{0.45}\\
&\approx0.0200671.
\end{aligned}
$$

product KL 为 $20\times0.0200671\approx0.40134$。Pinsker：

$$
\operatorname{TV}(P_0^{20},P_1^{20})
\le\sqrt{0.40134/2}
\approx0.44796.
$$

参数 separation $0.1=2s$，$s=0.05$。Le Cam expected absolute-error lower bound：

$$
\frac{s}{2}(1-\mathrm{TV})
\ge0.025(1-0.44796)
\approx0.01380.
$$

这是由 Pinsker 得到的保守数值 lower bound。

### LT-MIN-B02

$$
m\ge
\frac{\log(1/(4\cdot0.05))}{16(0.05)^2}
=\frac{\log5}{0.04}
\approx40.236.
$$

整数尺度至少为 41。它是所用保守 two-point inequality 给出的必要条件，不是 sharp 最小常数。

### LT-MIN-B03

Fano：

$$
\Pr(\widehat V\ne V)
\ge1-0.25-\frac{\log2}{\log64}.
$$

因为 $64=2^6$，比值为 $1/6$，所以

$$
\Pr(\text{error})
\ge\frac34-\frac16
=\frac7{12}
\approx0.5833.
$$

## C. 推导与证明

### LT-MIN-C01

给 estimator $\widehat\theta$，定义 test 选择离它更近的 $\theta_j$。若真值为 $\theta_j$ 且 test 选错，假设 $d(\widehat\theta,\theta_j)<s$，则由 separation $d(\theta_0,\theta_1)\ge2s$ 和 triangle inequality，$\widehat\theta$ 不可能更靠近另一参数；矛盾。因此 test error 蕴含 $d(\widehat\theta,\theta_j)\ge s$。

故

$$
\frac12\sum_j\mathbb E_jd(\widehat\theta,\theta_j)
\ge s\frac12\sum_jP_j(\text{error}).
$$

任意 binary test 的最小平均错误是 $(1-\mathrm{TV}(P_0^m,P_1^m))/2$。最大 risk 不小于平均 risk，所以

$$
\sup_j\mathbb E_jd
\ge\frac{s}{2}(1-\mathrm{TV}).
$$

去掉 loss factor，同样有

$$
\sup_jP_j(d\ge s)
\ge\frac{1-\mathrm{TV}}2.
$$

最后对所有 estimators 取 infimum。

### LT-MIN-C02

若 $V$ 在 $N$ 个 indices 上均匀：

$$
P(\widehat V\ne V)
\ge1-\frac{I(V;S)+\log2}{\log N}.
$$

若 average KL to reference $Q^m$ 至多 $\alpha\log N$，则 $I(V;S)\le\alpha\log N$。若 parameters pairwise $2s$ separated，事件 $d(\widehat\theta,\theta_V)<s$ 允许 nearest-neighbor 正确 decode；所以

$$
\sup_vP_v(d(\widehat\theta,\theta_v)\ge s)
\ge1-\alpha-\frac{\log2}{\log N}.
$$

$\log N$ 来自识别 $N$ 个等可能 indices 所需的信息量；product KL 必须与它比较。

### LT-MIN-C03

取两个 deterministic targets $f_0,f_1$，只在 rare point $x_r$ 上标签相反，且 $P_X(x_r)=2\varepsilon$。两者都 realizable。事件

$$
E=\{x_r\text{ 未被观察}\}
$$

概率为 $(1-2\varepsilon)^m$。条件于 $E$，两个 worlds 的 observed data distribution 相同；对两个 targets 均匀平均，任意 randomized learner 在 $x_r$ 至少有 $1/2$ 错误概率。故至少一个 world 的 excess-$>\varepsilon$ failure probability 至少

$$
\frac12(1-2\varepsilon)^m.
$$

若要它对两个 worlds 都 $\le\delta$，必须

$$
\frac12(1-2\varepsilon)^m\le\delta,
$$

即

$$
m\ge
\frac{\log(1/(2\delta))}{-\log(1-2\varepsilon)}
=\Omega\left(\frac{\log(1/\delta)}{\varepsilon}\right).
$$

## D. 边界、反例与纠错

### LT-MIN-D01

SGD failure 可能由 optimization、hyperparameters 或 poor bias 导致，另一个 learner 可成功。要升级为 lower bound，应构造至少两个满足同一 assumptions 的 distributions，使任何高质量 output 能 decode world；再证明所有 tests 因 product KL/TV overlap 都有非零错误。这样量词从“这个 SGD”提升到“所有 algorithms”。

### LT-MIN-D02

同一 expectation 可有不同 tails。例如 $Z_1\equiv q$，$Z_2\sim\operatorname{Bernoulli}(q)$ 都有均值 $q$；对 threshold $2q<1$，$P(Z_1>2q)=0$，而 $P(Z_2>2q)=q$。所以 expected lower/upper information 不决定任意 confidence level 的 quantile。boundedness 可做粗转换，sharp $\delta$ dependence 需专门 tail/testing argument。

### LT-MIN-D03

$M$ 只数 cardinality，不保证 functions 形成大的 statistical packing。例：$M$ 个有序 thresholds 的 VC dimension 仅为 1；其 label patterns 高度嵌套，难度远小于任意 $M$ 个 independent bits。也可能许多 functions 在相关 distributions 的 support 上等价。$\log M$ lower bound 需要 shattering/packing 与 controlled KL construction，不能由文件数自动推出。

## E. AI 迁移

### LT-MIN-E01

构造安全世界 $P_0$ 无事故，危险世界 $P_1$ 每次独立 exposure 以概率 $p$ 出事故；未见事故的 likelihood 在危险世界为 $(1-p)^m\approx e^{-mp}$。若 $m\ll1/p$，两世界都经常产生“零事故”日志，任何 certifier 难以区分。要把危险世界误判安全的概率压到 $\delta$，需 $m\gtrsim\log(1/\delta)/p$，前提 exposures 真正独立且覆盖 deployment distribution。

### LT-MIN-E02

差值 $0.01$ 与 per-example constant-scale noise 比较，基本 requirement 为

$$
m=\Theta(1/0.01^2)=\Theta(10^4)
$$

再乘 confidence log 和 variance constants。paired evaluation 在同一 examples 上比较两个 models，分析 per-example score difference；若两模型 errors 强正相关，difference variance 可远小于两个独立 estimates 之和，从而改善常数，但 worst-case $1/\Delta^2$ 结构仍在。

### LT-MIN-E03

- minimax：安全/保证导向，保护允许 family 中最坏分布；
- Bayes-average：有可信 task prior 时优化平均性能；
- local minimax：研究当前模型/分布附近小扰动的不可辨识性；
- instance-dependent：难度依具体 margin、gap、frequency 或 variance，适合 adaptive sampling 和具体部署预算。

选择视角等于选择量词；应与风险容忍度和 prior evidence 匹配。
