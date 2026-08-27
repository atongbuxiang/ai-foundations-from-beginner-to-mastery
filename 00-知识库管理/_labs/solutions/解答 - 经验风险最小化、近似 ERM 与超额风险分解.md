---
type: solution
status: draft
area: [learning-theory/foundations, machine-learning, optimization]
topic: "[[经验风险最小化、近似 ERM 与超额风险分解]]"
exercise: "[[习题 - 经验风险最小化、近似 ERM 与超额风险分解]]"
prerequisites: ["[[损失、总体风险与经验风险]]", "[[优化问题、可行域与局部最优]]"]
related: ["[[泛化间隙与浓缩不等式接口]]", "[[正则化、交叉验证与模型选择]]"]
sources: ["[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - 经验风险最小化、近似 ERM 与超额风险分解

> [!warning] 使用边界
> 分解是对象账本；真正得到小数值还需容量、稳定性、优化与 evaluation 条件。不要把 decomposition identity 本身当作 rate theorem。

## A. 识别与复述

### LT-ERM-A01

$$
R^*=\inf_{h\in\mathcal F}R_P(h),
\qquad
R_{\mathcal H}^*=\inf_{h\in\mathcal H}R_P(h).
$$

$h_{\mathcal H}^*$ 是类内 population minimizer，依未知 $P$、不依当前样本。$\widehat h_S$ 是 exact empirical minimizer，依 $S$；$\widetilde h_{S,U}$ 是实际算法输出，依 $S$ 与算法随机性。$R^*,R_{\mathcal H}^*$ 是最优值，后三者是 predictors。

### LT-ERM-A02

exact ERM 满足

$$
R_S(\widehat h_S)=\inf_{h\in\mathcal H}R_S(h).
$$

$\rho$-approximate ERM 满足

$$
R_S(\widetilde h)\le\inf_{h\in\mathcal H}R_S(h)+\rho.
$$

parameter distance 依坐标和非可辨识表示；目标可能平坦/病态，近参数可有大 objective gap，远参数也可表示同一函数。只有强凸性、smoothness、error bound 等额外结构能连接距离与 gap。

### LT-ERM-A03

- approximation：$R_{\mathcal H}^*-R^*\ge0$；
- class excess：$R_P(\widetilde h)-R_{\mathcal H}^*\ge0$，前提 $\widetilde h\in\mathcal H$；
- signed generalization gap：$R_P(h)-R_S(h)$，可正可负；
- empirical optimization gap：$R_S(\widetilde h)-\inf_hR_S(h)\ge0$。

train–test difference 是另一个随机估计量，不应直接改名为 approximation 或 optimization error。

## B. 手算与构造

### LT-ERM-B01

$$
\mathcal E_{app}=0.13-0.08=0.05,
$$

$$
\mathcal E_{\mathcal H}=0.19-0.13=0.06,
$$

$$
\mathcal E_{total}=0.19-0.08=0.11.
$$

验证 $0.05+0.06=0.11$。

### LT-ERM-B02

已知

$$
g_S(\widetilde h)=0.04,
\qquad
g_S(h_{\mathcal H}^*)=-0.01.
$$

signed-gap bound：

$$
R_P(\widetilde h)-R_{\mathcal H}^*
\le0.04-(-0.01)+0.02=0.07.
$$

若只知道 uniform absolute gap $0.05$：

$$
R_P(\widetilde h)-R_{\mathcal H}^*
\le2(0.05)+0.02=0.12.
$$

粗界更大，因为它丢掉两个具体 signed gaps 的方向信息。

### LT-ERM-B03

$$
\mathcal E_{total}=\frac23-0=\frac23,
$$

$$
\mathcal E_{app}=\frac13-0=\frac13,
$$

$$
\mathcal E_{\mathcal H}=\frac23-\frac13=\frac13.
$$

经验风险为 0，所以 realized generalization gap 是

$$
R_P(\widetilde h)-R_S(\widetilde h)=\frac23.
$$

gap 比 class excess 大，因为训练风险还低于类内 population optimum 的数值；二者不是同一分解项。

## C. 推导与证明

### LT-ERM-C01

令 $g_S(h)=R_P(h)-R_S(h)$：

$$
\begin{aligned}
R_P(\widetilde h)-R_P(h_{\mathcal H}^*)
&=[R_P(\widetilde h)-R_S(\widetilde h)]\\
&+[R_S(\widetilde h)-R_S(\widehat h_S)]\\
&+[R_S(\widehat h_S)-R_S(h_{\mathcal H}^*)]\\
&+[R_S(h_{\mathcal H}^*)-R_P(h_{\mathcal H}^*)].
\end{aligned}
$$

第一项为 $g_S(\widetilde h)$；第二项不超过 $\rho$；第三项因 $\widehat h_S$ 是 ERM 而不超过 0；第四项为 $-g_S(h_{\mathcal H}^*)$。故

$$
R_P(\widetilde h)-R_{\mathcal H}^*
\le g_S(\widetilde h)-g_S(h_{\mathcal H}^*)+\rho.
$$

若类内 infimum 不取到，可用风险距 infimum 任意近的 comparator，再令其近似误差趋零。

### LT-ERM-C02

有

$$
g_S(\widetilde h)
\le\sup_{h\in\mathcal H}|g_S(h)|,
$$

以及

$$
-g_S(h_{\mathcal H}^*)
\le\sup_{h\in\mathcal H}|g_S(h)|.
$$

代入 `C01` 得 class excess 不超过 $2\sup|g_S|+\rho$。再用精确恒等式

$$
R_P(\widetilde h)-R^*
=(R_{\mathcal H}^*-R^*)
+(R_P(\widetilde h)-R_{\mathcal H}^*)
$$

即得结论。前一项是 nonnegative approximation gap，后一项由 uniform generalization 与 approximate optimization 控制。

### LT-ERM-C03

至少需要：

1. approximation：$R_{\mathcal H_{k(m)}}^*-R^*\to0$；
2. learning/algorithm：

$$
2\sup_{h\in\mathcal H_{k(m)}}|R_P(h)-R_S(h)|+\rho_m
\xrightarrow{P}0
$$

或用其他方法控制 class excess。

若 $k(m)$ 增长太快，class complexity 相对 $m$ 不降，uniform gap 可能保持常数甚至失控；optimizer 也可能无法在预算内逼近更大类的经验最优。只保证 union of classes 稠密不足以保证可学习。

## D. 边界、反例与纠错

### LT-ERM-D01

设同一样本上两函数的风险表为

| 函数 | $R_S$ | $R_P$ |
|---|---:|---:|
| $h_{mem}$ | 0 | 0.50 |
| $h_{simple}$ | 0.10 | 0.12 |

exact ERM 选 $h_{mem}$。$h_{simple}$ 是 $\rho=0.10$ approximate ERM，经验 optimization gap 为正，但 population risk 低 $0.38$。这可由含一个可记忆噪声模式的训练样本实现。early stopping/regularization 可能故意返回后者。

### LT-ERM-D02

更大类只保证类内 infimum不升，可能降低 approximation。它也可能扩大选择空间、增加 sample-dependent fluctuation；参数更多会改变 optimizer landscape 和计算成本；若新增数据只是重复/偏移，effective sample 不增长；若 target loss/population 写错，容量无法修复 mismatch。total excess 需把所有账户相加，不能只看其中一个单调项。

### LT-ERM-D03

L2 改成

$$
\min_\theta R_S(h_\theta)+\lambda\|\theta\|^2
$$

后，objective 已不同；它在多个 ERM 间选择小 norm 代表，某些条件下等价于 norm-constrained effective class。正齐次网络中 $(W_1,W_2)\mapsto(cW_1,c^{-1}W_2)$ 保持函数而改变 layerwise L2，因此 penalty 还选择同一 function fiber 上的 scale balance。不能只说“更容易优化的原 ERM”。

## E. AI 迁移

### LT-ERM-E01

建议报告：架构/scaling 与强 baseline 比较 approximation proxy；跨独立 split、seed 的风险方差和 memorization probe 诊断 selection；训练 objective、gradient/residual、multi-start 诊断 optimization；locked group-aware test 的 CI 诊断 evaluation；corruption/temporal/site cohorts 诊断 shift。零 train error 只说明 empirical fit 账户，不关闭其他账户。

### LT-ERM-E02

- 增参数：主要降低 representation/approximation，可能增 selection/compute；
- 增独立数据：主要降低 sampling/estimation，也可能改变 distribution composition；
- 增 steps：降低 empirical optimization gap，过久可能增强 memorization 或改变 implicit bias；
- 改 tokenizer：改变 observation representation 与 class，可能降低信息损失，也可能破坏兼容性、数据统计和 optimization。

每项都需用 target risk 验证，而非从操作名称推定总误差方向。

### LT-ERM-E03

已观测事实：在指定 split、seed、architecture 下，VAT 配置 validation loss 更低。机制假设：局部 worst-direction consistency 降低 input sensitivity 或注入任务正确不变性。尚需：多 split/seed uncertainty、相同调参预算、独立 final test、扰动是否 label-preserving、shift robustness、complexity/stability proxy 与定理条件。单一 validation 改善不能证明 distribution-free complexity 已减少。

