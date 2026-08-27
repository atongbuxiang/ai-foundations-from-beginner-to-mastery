---
type: solution
status: verified
area: [training, optimization, curvature]
topic: "[[GGN、经验 Fisher 与曲率近似陷阱]]"
exercise: "[[习题 - GGN、经验 Fisher 与曲率近似陷阱]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - GGN、经验 Fisher 与曲率近似陷阱

> [!warning] 使用边界
> 一个反例只负责删除一条无条件等号。它不证明某个 proxy 永远无用，也不替代在指定任务上的实证比较。

## A. 识别与复述

### TRN21-A01
对象近似问 $C$ 是否代表目标 Hessian/Fisher/GGN，例如 GGN 删除模型二阶项；统计估计问有限 batch/EMA 是否逼近已定义的总体对象，例如 observed labels 不逼近 model-label law；数值求解问 $(C+\lambda I)^{-1}g$ 是否算准，例如低精度 root 或早停 CG。三层误差可同时存在，不能用末端 loss 下降反向证明每层都正确。

### TRN21-A02
$\operatorname{mean}(g_ig_i^T)$ 是非中心 per-sample 二阶矩；$\bar g\bar g^T$ 先把样本抵消再做 rank-1 outer product；centered covariance 是 $\operatorname{mean}[(g_i-\bar g)(g_i-\bar g)^T]$，删除 mean signal。恒有二阶矩 = covariance + mean outer product。

### TRN21-A03
$F=G$ 常需匹配负对数似然、指数族及 natural-output coordinate；population $H=F$ 还需模型正确指定、在合适总体点/最优点并满足信息恒等式；$F_{emp}\approx F$ 还需 observed-label law 接近当前 model-label law、per-sample reduction 正确且样本足够。大样本只处理最后一层的抽样误差。

## B. 手算与构造

### TRN21-B01
$G=4\theta^2$、$R=2(\theta^2-1)$、$H=6\theta^2-2$。在 $0$：$(G,R,H)=(0,-2,-2)$；在 $1/2$：$(1,-3/2,-1/2)$；在 $1$：$(4,0,4)$。$H<0$ 当 $|\theta|<1/\sqrt3$，而 GGN 始终非负。

### TRN21-B02
三点都满足 $H=F=1$。EF 为 $(\theta-y)^2$，所以在 $\theta=2,1,0$ 分别为 $0,1,4$。它可在 sample optimum 塌缩，也可随 residual 任意变大，而 true Fisher 的模型方差保持 1。

### TRN21-B03
$$\frac12\sum_i g_ig_i^T=\begin{bmatrix}1&0\\0&1\end{bmatrix}.$$
$\bar g=(1,0)$，故 $\bar g\bar g^T=\operatorname{diag}(1,0)$；centered covariance 为 $\operatorname{diag}(0,1)$。Per-sample second moment rank 2，后两者各 rank 1，且分解之和恢复前者。

## C. 推导与证明

### TRN21-C01
$L'=rr'$，再求导得 $H=(r')^2+rr''$；GGN 是 $G=(r')^2$。$r''=0$（模型对参数局部线性）或 $r=0$（interpolation point）都是 $H=G$ 的充分条件；它们非必要，因为 $rr''$ 也可能在多样本期望中相互抵消。

### TRN21-C02
写 $g=(g-\mu)+\mu$、$\mu=\mathbb E g$，展开 outer product 并取期望，两个交叉项因 $\mathbb E(g-\mu)=0$ 消失，得到 $\mathbb E[gg^T]=\operatorname{Cov}(g)+\mu\mu^T$。因此该统计既包含随机波动，也包含确定性 descent signal，不能默认全是 curvature 或全是 noise。

### TRN21-C03
可用 $q(v)=v^TCv/(v^THv)$、$e_F=\|C-H\|_F/\|H\|_F$ 与 $\cos((C+\lambda I)^{-1}g,(H+\lambda I)^{-1}g)$。$q$ 依赖所选方向，Frobenius norm 可能忽视小但关键 eigenmode，step cosine 又依赖 $g$ 与 damping 且不检查长度；还需 model ratio、rank、谱与数值 residual 联合审计。

## D. 边界、反例与纠错

### TRN21-D01
取 $H=I_2$、$C=\operatorname{diag}(1,0)$。$C$ PSD 且 rank 1，但对 $v=e_2$，$v^TCv/(v^THv)=0$，第二方向完全被删掉。若梯度主要落在该方向，damping 将主导 update。

### TRN21-D02
Law of large numbers 让 estimator 收敛到它实际抽样的总体对象。若标签来自 $q$ 而目标需要 $p_\theta$，若先 mean 后 outer product，或若预先删掉 cross-layer blocks，样本增多只会更稳定地估计错误/简化对象，结构 bias 不会消失。

### TRN21-D03
过参数化模型可在训练样本上令 per-sample residual 与 gradient 近零，于是 EF 变小；Gaussian mean 例中该点 $H=F=1$。因此 EF 下降可能仅表示 observed residual interpolation，不表示 objective curvature、模型分布敏感性或 flatness 同步下降。

## E. AI 迁移

### TRN21-E01
Suite 至少含：非线性 least-squares toy，断言 $H=G+R$ 且有 $G=0,H<0$ 点；Gaussian/Bernoulli toy，断言 model-label Fisher 与 observed-label EF 可不同；正负 per-sample gradient toy，断言 `mean_outer != outer_mean` 且 rank 不同。三类失败分别命名，避免一个总误差掩盖原因。

### TRN21-E02
固定随机状态，对随机 $v$ 比较 $v^TCv$ 与通过 HVP 得到的 $v^THv$；用 iterative solves 比较 damped step cosine/norm，并记录两边 residual。最后用同 batch/seed 计算 predicted/actual reduction ratio；随机方向分布、damping、样本数和置信区间必须写入报告。

### TRN21-E03
依次检查 per-example loss 和 label source、gradient 是否在 reduction 前获得、centered 与否、batch/EMA 轴、block/diagonal/Kronecker 结构、damping、inverse/root 算法、clipping/momentum/decay 顺序，最后核对 step norm、direction cosine、model ratio、state bytes 与时间。变量名只是一条检索线索。

## 无提示重做

- [ ] 48 小时后手算三个最小反例。
- [ ] 一周后为任一 curvature proxy 写出不少于四项的联合证书。
