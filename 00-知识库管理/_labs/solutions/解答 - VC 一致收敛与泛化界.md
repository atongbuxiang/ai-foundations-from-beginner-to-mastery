---
type: solution
status: draft
area: [learning-theory/vc, probability/uniform-convergence]
topic: "[[VC 一致收敛与泛化界]]"
exercise: "[[习题 - VC 一致收敛与泛化界]]"
prerequisites: ["[[Sauer-Shelah 引理]]", "[[不可知 PAC、ERM 与双侧一致收敛]]", "[[浓缩不等式]]"]
related: ["[[二分类统计学习基本定理]]", "[[Ghost Sample、对称化与经验过程入口]]", "[[Rademacher 复杂度与经验复杂度]]"]
sources: ["[[S-1971-Vapnik-Chervonenkis-Uniform-Convergence]]", "[[S-2014-Shalev-Shwartz-Ben-David-Understanding-Machine-Learning]]", "[[S-1963-Hoeffding-Bounded-Random-Variables]]"]
created: 2026-08-20
updated: 2026-08-20
---

# 解答 - VC 一致收敛与泛化界

> [!warning] 使用边界
> 本解答固定正文的一个常数版本。换用别的对称化或浓缩可以改变常数，但必须整体重证；不能只把指数改紧而保留未经验证的其他步骤。

## A. 识别与复述

### LT-VCUC-A01

对 fixed binary class $\mathcal H$、0–1 loss、$S\sim P^m$ iid，若 $m\varepsilon^2\ge2$，

$$
P\left(
\sup_{h\in\mathcal H}|R_P(h)-R_S(h)|>\varepsilon
\right)
\le4\tau_{\mathcal H}(2m)e^{-m\varepsilon^2/8}.
$$

第一个 2 来自：每个坏训练样本至少有一半 ghost samples 使双样本差坏，所以反向除以 $1/2$。第二个 2 来自 fixed pattern 的 two-sided Hoeffding tail。指数 $1/8$ 来自 range length 2 和 threshold $\varepsilon/2$。

### LT-VCUC-A02

$S'$ 必须与 $S$ 独立且同为 $P^m$。它用 $P_m'$ 近似未知 $P$，把 $|P-P_m|$ 的坏事件转成 $|P_m'-P_m|$ 的坏事件，随后才能条件于有限 pooled sample。它只存在于证明的扩展概率空间，算法训练/部署不需要真实获得第二份数据。

### LT-VCUC-A03

pointwise：对每个事先固定 $h$，$R_S(h)\to R_P(h)$；它不能直接代入 data-dependent ERM output。uniform：同一事件上对所有 $h$ 同时小 gap，需要 class complexity（growth/VC）和对称化。uniform event 再结合 ERM empirical optimality，经过 output 和 comparator 两次 deviation，得到 excess $\le2\gamma$。所以链为

$$
\text{pointwise concentration}
+\text{capacity/symmetrization}
\Rightarrow\text{uniform convergence}
+\text{ERM optimality}
\Rightarrow\text{excess guarantee}.
$$

## B. 手算与数值判断

### LT-VCUC-B01

因 $2em/d=10000e$：

$$
d\log\frac{2em}{d}
=2\log(10000e)
\approx20.4207.
$$

加 $\log80\approx4.3820$ 得 $24.8027$。因此

$$
\gamma_m
\approx\sqrt{\frac8{10000}\cdot24.8027}
=\sqrt{0.0198422}
\approx0.1409.
$$

exact ERM class excess 至多 $2\gamma_m\approx0.2817$。这是 distribution-free sufficient bound，不是实际 gap 预测。

### LT-VCUC-B02

$$
\gamma
\le
\sqrt{\frac8{2000}\left(\log500+\log80\right)}.
$$

$\log500\approx6.2146$，总和 $10.5966$，故

$$
\gamma\approx\sqrt{0.004\cdot10.5966}
=\sqrt{0.0423864}
\approx0.2059.
$$

直接 growth 信息避免了再用可能更松的 VC/Sauer 粗化。

### LT-VCUC-B03

$\varepsilon^2/8=0.04/8=0.005$。

当 $m=500$：

$$
400e^{-2.5}\approx400(0.082085)\approx32.83.
$$

概率当然不超过 1，所以真正可写 $\min\{1,32.83\}=1$，没有非平凡信息。

当 $m=5000$：

$$
400e^{-25}\approx400(1.3888\times10^{-11})
\approx5.56\times10^{-9}.
$$

此时界非常小。上界大于 1 不表示失败概率大于 1或 theorem 错，只表示这次粗估计不能改进概率公理的 trivial bound。

## C. 推导与证明

### LT-VCUC-C01

设

$$
A=\{S:\sup_f|Pf-P_mf|>\varepsilon\}.
$$

对每个 $S\in A$ 选 witness $f_S$ 使 gap $>\varepsilon$。固定 $S$ 后，$f_S$ 不依赖 $S'$，且

$$
\operatorname{Var}(P_m'f_S)
\le\frac1{4m}.
$$

Chebyshev：

$$
P_{S'}(|P_m'f_S-Pf_S|>\varepsilon/2)
\le\frac{1/(4m)}{\varepsilon^2/4}
=\frac1{m\varepsilon^2}
\le\frac12.
$$

故至少一半 $S'$ 满足 ghost gap $\le\varepsilon/2$。在其上，triangle inequality 给

$$
|P_mf_S-P_m'f_S|
\ge|P_mf_S-Pf_S|-|P_m'f_S-Pf_S|
>\varepsilon/2.
$$

所以

$$
P_{S'}(\text{two-sample bad}\mid S)\ge1/2
$$

对每个 $S\in A$ 成立。积分得

$$
P_{S,S'}(\text{two-sample bad})
\ge\frac12P_S(A),
$$

整理即结论。

### LT-VCUC-C02

固定 pooled data 和一个 pattern，$a_i=f(Z_i)-f(Z_i')\in[-1,1]$。$X_i=\sigma_i a_i$ 独立、均值 0、范围长度 $2|a_i|\le2$。Hoeffding 对 $t=\varepsilon/2$：

$$
\begin{aligned}
P_\sigma\left(\left|m^{-1}\sum_iX_i\right|>t\right)
&\le2\exp\left(-\frac{2m^2t^2}{\sum_i(2|a_i|)^2}\right)\\
&\le2\exp(-mt^2/2)\\
&=2e^{-m\varepsilon^2/8}.
\end{aligned}
$$

在固定 pooled labels 下，error vector 是 prediction vector XOR label vector，故 distinct error patterns 不超过 $\tau_{\mathcal H}(2m)$。相同 error pattern 给相同所有 $a_i$，只需 union 一次。因此 conditional union bound 乘 $\tau(2m)$。

### LT-VCUC-C03

若 infimum 取到 $h^*$，

$$
\begin{aligned}
R_P(\widetilde h_S)
&\le R_S(\widetilde h_S)+\gamma\\
&\le R_S(h^*)+\rho+\gamma\\
&\le R_P(h^*)+2\gamma+\rho.
\end{aligned}
$$

若不取到，对任意 $\eta>0$ 选 $h_\eta$ 满足

$$
R_P(h_\eta)\le\inf_hR_P(h)+\eta.
$$

同样推得

$$
R_P(\widetilde h_S)
\le\inf_hR_P(h)+\eta+2\gamma+\rho.
$$

因对任意 $\eta>0$ 成立，令 $\eta\downarrow0$ 即得 $2\gamma+\rho$。

## D. 边界、反例与纠错

### LT-VCUC-D01

原样本 patterns 只决定 $P_mf$，不决定 $Pf$；两个函数可在 $S$ 上相同、在 sample 外不同。ghost sample 把 $Pf$ 替成 $P_m'f$，双样本差同时依赖 $S,S'$，所以必须按 pooled 至多 $2m$ inputs 去重。$\tau(2m)$ 正是使 conditional event 完全由 restrictions 决定的规模。

### LT-VCUC-D02

ghost sample 是分析者在证明空间中引入的独立副本，用于 upper-bound 原样本坏事件。定理最后的概率只对 $S$ 陈述，learner 从未访问 $S'$。真实验证集有 evaluation/selection 作用，若被算法使用反而要进入数据合同；两者概念不同。

### LT-VCUC-D03

令 $\mathcal X=\{a,b\}$，$P_X(a)=1$，$Q_X(b)=1$。class/learner 输出 $h(a)$ 正确但 $h(b)$ 错。对任意 $P$ 样本，$R_S(h)=R_P(h)=0$，uniform convergence 可完美成立；部署 $R_Q(h)=1$。

VC theorem 对每个固定 law 控制 train sample 与**同一 law** population risk。它没有声称从 $P$ sample 控制另一个 $Q$，所以不是组合或浓缩步骤出错，而是目标风险发生了 distribution shift。

## E. AI 迁移

### LT-VCUC-E01

可代入

$$
\gamma
\le
\sqrt{
\frac8{50000}
\left[
129\log\frac{2e\cdot50000}{129}
+\log400
\right]
}.
$$

这把 $d=129$ 视为事先固定 representation 上所有 affine heads 的 VC 上界。若 encoder 也根据同一 labels fine-tune，输出函数类包含 encoder 参数导致的 representation 变化，不再是固定 $\phi$ 的 affine-halfspace 拉回；必须分析完整 fine-tuning class或用算法依赖工具。

### LT-VCUC-E02

若 10 万 prompts 事先固定，finite-class uniform bound 可把它们全纳入 $\mathcal H$；若生成器根据 benchmark feedback 继续创造 prompts，class 应定义为在允许交互 transcript、随机种子和预算下所有可能最终 prompts/functions，而不是只数最后看到的 10 万个文件。这个整体 class 可能大得多。

更稳妥：把 benchmark 用于开发，冻结 generator 与候选选择规则后，在未被访问、与部署匹配的新 iid holdout 上做一次确认；若要长期反复查询，使用分批 fresh data、预注册 stopping rule 或专门 adaptive evaluation 机制。

### LT-VCUC-E03

theorem 没错：0–1 gap 最大为 1，所以 7.3 只说明上界比 trivial bound 还松。它对该规模没有数值预测力，不能解释 0.02，也不能推出模型不泛化。

下一步可研究实际 weight/path/spectral norms、classification margin、sample-dependent Rademacher complexity、compression、algorithmic stability、optimization trajectory、data geometry/effective dimension 与 distribution-specific assumptions。每个候选都要说明控制对象和是否能在真实数值上非平凡。
