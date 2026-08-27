---
type: solution
status: draft
area: [learning-theory/pac, machine-learning/erm]
topic: "[[不可知 PAC、ERM 与双侧一致收敛]]"
exercise: "[[习题 - 不可知 PAC、ERM 与双侧一致收敛]]"
prerequisites: ["[[有限假设类、Union Bound 与一致收敛]]", "[[可实现情形的一致 ERM 保证]]"]
related: ["[[样本复杂度下界与 Minimax 视角]]", "[[VC 一致收敛与泛化界]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1963-Hoeffding-Bounded-Random-Variables]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - 不可知 PAC、ERM 与双侧一致收敛

> [!warning] 使用边界
> 以下常数要求候选类预先固定、样本 iid、loss 落在 $[0,1]$。agnostic 只删除 realizability，不删除其余统计协议。

## A. 识别与复述

### LT-AGN-A01

若 $|\mathcal H|=M<\infty$、$S\sim P^m$ iid、$\ell\in[0,1]$，则任意 exact ERM $\widehat h_S$ 以至少 $1-\delta$ 概率满足

$$
R_P(\widehat h_S)-R_{\mathcal H}^*
\le2\sqrt{\frac{\log(2M/\delta)}{2m}}.
$$

因此

$$
m\ge\frac{2\log(2M/\delta)}{\varepsilon^2}
$$

足以使 class excess $\le\varepsilon$。不要求 $R_{\mathcal H}^*=0$。

### LT-AGN-A02

realizable 时 oracle 与 ERM 都可零训练错误，坏 hypothesis 必须连续避开错误区域，概率为 $(1-p)^m$。agnostic 时 oracle 自身有非零错误，版本空间可能为空；坏 hypothesis 只需 sampling noise 使其 empirical risk 暂时低于 oracle。区分相差 $\varepsilon$ 的两个均值需要 standard error $1/\sqrt m$ 小于 $\varepsilon$，故 $m$ 为 $1/\varepsilon^2$ 量级。

### LT-AGN-A03

uniform proof 建立

$$
\forall h:\ |R_S(h)-R_P(h)|\le\alpha,
$$

覆盖任意 data-dependent choice 和 approximate ERM，但付两个 deviations。pairwise proof只控制坏 $h$ empirical beat 固定 oracle 的事件，专用于 exact ERM，给 $Me^{-m\varepsilon^2/2}$，常数略紧，却不提供全部 hypotheses 的 risk intervals。

## B. 手算与构造

### LT-AGN-B01

$$
\begin{aligned}
m&\ge
\frac{2\log(2\cdot200/0.05)}{0.1^2}\\
&=200\log8000\\
&\approx1797.439.
\end{aligned}
$$

取 $m=1798$。

### LT-AGN-B02

统计项允许

$$
2\alpha\le0.08-0.02=0.06.
$$

所以

$$
\begin{aligned}
m&\ge
\frac{2\log(2\cdot500/0.01)}{0.06^2}\\
&=\frac{2\log100000}{0.0036}\\
&\approx6396.070.
\end{aligned}
$$

取 $m=6397$。

### LT-AGN-B03

$$
\Pr(R_S(h)\le R_S(h^*))
\le e^{-m\Delta^2/2}
=e^{-2000(0.06)^2/2}
=e^{-3.6}
\approx0.02732.
$$

这是单个固定坏 hypothesis 的 bound；对多个候选还需 Union Bound。

## C. 推导与证明

### LT-AGN-C01

在 simultaneous event 上：

$$
\begin{aligned}
R_P(\widehat h_S)
&\le R_S(\widehat h_S)+\alpha\\
&\le R_S(h_{\mathcal H}^*)+\alpha\\
&\le R_P(h_{\mathcal H}^*)+2\alpha.
\end{aligned}
$$

第一处 deviation 用于 data-dependent ERM output；第二处用于固定 population oracle。中间不等式来自 empirical optimality。减去 $R_{\mathcal H}^*$ 即得 excess $\le2\alpha$。

### LT-AGN-C02

$\rho$-approximate ERM 给

$$
R_S(\widetilde h)
\le R_S(h_{\mathcal H}^*)+\rho.
$$

因此同一链得到

$$
R_P(\widetilde h)-R_{\mathcal H}^*
\le2\alpha+\rho.
$$

要使其 $\le\varepsilon$，需 $\rho<\varepsilon$ 且

$$
m\ge
\frac{2\log(2M/\delta)}{(\varepsilon-\rho)^2}.
$$

若 $\rho\ge\varepsilon$，即使 $\alpha\to0$，右端也至少为 $\rho$；此 theorem 无法证明目标精度。

### LT-AGN-C03

令 $\Delta_h=R_P(h)-R_P(h^*)>0$。因为 $W_i\in[-1,1]$，Hoeffding lower tail 为

$$
\Pr\left(
\frac1m\sum_iW_i-\Delta_h\le-\Delta_h
\right)
\le
\exp\left(-\frac{2m\Delta_h^2}{(1-(-1))^2}\right)
=e^{-m\Delta_h^2/2}.
$$

事件 $R_S(h)\le R_S(h^*)$ 正是 $m^{-1}\sum_iW_i\le0$。若 ERM class excess $>\varepsilon$，至少一个 $\Delta_h>\varepsilon$ 的 hypothesis empirical beat/equal oracle，所以

$$
\Pr(\text{bad ERM})
\le\sum_{h:\Delta_h>\varepsilon}e^{-m\Delta_h^2/2}
\le Me^{-m\varepsilon^2/2}.
$$

## D. 边界、反例与纠错

### LT-AGN-D01

令 $X=x_0$ 恒定、$Y\sim\operatorname{Bernoulli}(0.2)$，class 是两个常数分类器。样本一旦同时出现 0 和 1，就没有零训练错误 hypothesis，版本空间为空；但 class 有限、0–1 loss bounded、samples iid，所以 agnostic ERM theorem 完全适用，并与 risk $0.2$ 的最佳常数分类器竞争。

### LT-AGN-D02

cross-entropy $-\log p_Y$ 无界，不能直接套 $[0,1]$ Hoeffding。即便 clipping/概率下界使 surrogate bounded，theorem 先控制 surrogate class excess；要推出 0–1 excess，还需 classification calibration/reduction inequality。两个缺口分别是 concentration 条件和 target-risk 转换。

### LT-AGN-D03

30 个 prompts 都依赖 validation feedback，故候选生成过程编码了 validation；观察到的 $M=30$ 不是 sample-independent class size。修复一：用独立 development set 生成 prompts，冻结后在新 validation 上选择。修复二：预先固定 rounds/family 并对完整 adaptive transcript 使用 reusable holdout/DP-style analysis；最终再保留一次独立 test。

## E. AI 迁移

### LT-AGN-E01

冻结 100 个 checkpoints、preprocessing、decoding 和 bounded per-user loss；以独立 user/session 为 sampling unit。validation ERM 与库内 population-best checkpoint 比较，使用 $M=100$ 的 simultaneous event。预先选 $\varepsilon,\delta$ 和样本量；选定后冻结模型，只在从未参与选择的 independent test 上做最终 pointwise evaluation。comparator 不是所有神经网络或 Bayes predictor。

### LT-AGN-E02

可把一次随机 judge outcome 并入 $Z=(\text{response},\text{judge seed/outcome})$，前提是每个 sampling unit 独立。对同一 response 重复调用 judge 主要降低该 response conditional-score estimation noise；这些 calls 共享内容和潜在 judge state，不能自动当作新的独立 deployment responses。有效 $m$ 通常按独立 response/user 数；重复 judge calls 应在每个 unit 内先聚合，并另行分析 conditional variance。

### LT-AGN-E03

- 增加独立 examples：按 $1/\sqrt m$ 直接缩小统计半径；
- 减少 $M$：只通过 $\sqrt{\log M}$ 改善，且可能增加 approximation error；
- variance-sensitive bound：低方差时改善常数/rate 局部项，但仍需 simultaneous selection 处理；
- 降低 $\rho$：降低 optimization floor，不会改变 sampling noise。

四者作用于不同账目，不能互相完全替代。
