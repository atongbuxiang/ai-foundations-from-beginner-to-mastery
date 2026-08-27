---
type: solution
status: verified
area: [training, optimization, numerical-linear-algebra, muon]
topic: "[[Newton–Schulz Matrix Sign 的收敛与有限精度]]"
exercise: "[[习题 - Newton–Schulz Matrix Sign 的收敛与有限精度]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Newton–Schulz Matrix Sign 的收敛与有限精度

> [!warning] 使用边界
> exact-arithmetic scalar map 是诊断工具，不是低精度大矩阵的完整误差模型。实际结论必须回到 reference residual 与 runtime guards。

## A. 识别与复述

### TRN28-A01
exact polar target 是 $Q=U_rV_r^T$；经典 NS 是具有局部二次收敛性质的迭代规则；Jordan 五次式是为固定少步训练近似设计的另一多项式；kernel output 是在指定 scaling、shape、steps、dtype、GEMM 与硬件下得到的数值矩阵。前两层是数学对象/算法，后两层分别是有限迭代与有限精度实现。

### TRN28-A02
$XX^TX=U\Sigma^3V^T$，更高奇次幂同理，因此 exact arithmetic 下左右 singular vectors 保持、每个 $\sigma_i$ 进入同一 scalar polynomial。浮点 GEMM 可扰动 basis，误差受 condition、singular-value gaps、rounding、accumulation 与 multiplication order 影响；只能把 scalar map 当作无舍入 reference。

### TRN28-A03
- orthogonality：检查 $Q^TQ$ 或 $QQ^T$ 接近 identity/support projector，漏掉 sign/alignment；
- polar residual：检查 $G\approx Q(Q^TG)$ 且 $Q^TG$ 近 PSD，能抓方向错，但受 rank/reference 定义影响；
- direction cosine：检查与 exact polar 的角度，可能漏掉 scale；
- dual gap：检查线性 oracle objective，能连接优化目标，但必须同时规范 spectral feasibility。

## B. 手算与构造

### TRN28-B01
$$
s_1=\frac12(0.5)(3-0.25)=0.6875.
$$
$$
e_0=0.75,\qquad e_1=1-0.6875^2=0.52734375.
$$
再算
$$
s_2=\frac12(0.6875)(3-0.6875^2)
\approx0.8687744141,
$$
故 $e_2\approx0.24523$。递推给
$$
\frac14e_1^2(3+e_1)\approx0.24523,
$$
与直接平方一致。误差已明显加速收缩，但尚非“数值上精确为 1”。

### TRN28-B02
任何奇多项式 $p(s)=a_1s+a_3s^3+\cdots$ 都满足 $p(0)=0$。故从 singular values $(\alpha,0)$ 出发，第二个值所有步都为零。canonical output 是 rank-1 partial isometry $Q=\operatorname{diag}(1,0)$；正交 target 是
$$
Q^TQ=\operatorname{diag}(1,0),
$$
而非 $I_2$。

### TRN28-B03
$\widehat Q=-I$ 仍满足 $\widehat Q^T\widehat Q=I$，所以 orthogonality residual 为 0。但
$$
\cos_F(-I,I)=-1,
\qquad
\langle G,-I\rangle_F=-5
$$
（若 $+I$ 是 maximizing polar direction）。它完全反向。正交性只约束列/行关系，不约束与 $G$ 的 alignment。

## C. 推导与证明

### TRN28-C01
令 $X=U\Sigma V^T$。则
$$
XX^TX
=U\Sigma V^TV\Sigma U^TU\Sigma V^T
=U\Sigma^3V^T,
$$
五次项为 $U\Sigma^5V^T$，故
$$
X_+=U(a\Sigma+b\Sigma^3+c\Sigma^5)V^T.
$$
每个 $s$ 因而变成 $as+bs^3+cs^5$。tall $m\ge n$ 常形成 $X^TX$ 后右乘；wide $m<n$ 可形成 $XX^T$ 后左乘，以使用较小 Gram，但必须保持代数次序与 shape。

### TRN28-C02
由 $s_+=\tfrac12s(3-s^2)$：
$$
1-s_+^2
=1-\frac14s^2(3-s^2)^2.
$$
令 $e=1-s^2$，则 $s^2=1-e$、$3-s^2=2+e$，展开得
$$
1-\frac14(1-e)(2+e)^2
=\frac14e^2(3+e).
$$
若 $0<s_0<\sqrt2$，则 $-1<e_0<1$ 且 $s_1>0$；$e_1\in[0,1)$。之后 $e_k\ge0$ 且
$$
e_{k+1}/e_k=\tfrac14e_k(3+e_k)<1,
$$
故单调趋于某 fixed point，只能为 0，因而 $s_k\to1$。

### TRN28-C03
奇异值满足
$$
\lVert G\rVert_2=\sigma_1
\le\sqrt{\sum_i\sigma_i^2}
=\lVert G\rVert_F,
$$
故归一化后 spectral norm 不超过 1。若 rank $r$ 且所有非零 singular values 都为 $\sigma$，则 $\lVert G\rVert_F=\sqrt r\,\sigma$，所以 $X_0$ 的每个非零 singular value 都是 $1/\sqrt r$。rank 越大，初值离 1 越远。

## D. 边界、反例与纠错

### TRN28-D01
取 full-rank $\operatorname{diag}(1,\varepsilon)$，$\varepsilon>0$ 极小。任何在零附近斜率有限的固定多项式经过 $K$ 步后，小值约只放大有限因子；选择足够小 $\varepsilon$，五步后仍远离 1。若直接取 rank-deficient $\varepsilon=0$，它永远为 0，输出也不可能 full orthogonal。

### TRN28-D02
有限步 power iteration 的 Rayleigh/singular estimate 通常从下方逼近主 singular value，除非有额外 residual upper bound。若 $\widehat\sigma<\sigma_1$，用 $G/\widehat\sigma$ 会使最大初始 singular value $\sigma_1/\widehat\sigma>1$，甚至越出 polynomial 的安全区间，引起 overshoot/divergence。certificate 必须含可证明上界或 safety factor。

### TRN28-D03
至少控制：input dtype、GEMM multiply dtype、accumulation dtype、matrix shape/layout、spectrum/condition/rank、initial scaling/epsilon、steps/coefficients、kernel fusion/reassociation、hardware math mode、overflow/underflow/flush-to-zero、determinism 和 reference precision。FP32 通过只覆盖其中一条 arithmetic path。

## E. AI 迁移

### TRN28-E01
生成已知 SVD 的矩阵：flat、log-spaced、clustered、exact zero rank、多个 shapes；condition 从 $1$ 扫到 dtype 可解析极限。用 FP64 SVD polar 为 reference。每步记录 singular values、orthogonality/support residual、polar PSD residual、direction cosine、dual gap、NaN/Inf。passes 应按 spectrum regime 分层，不能用一个平均值掩盖小 singular failure。

### TRN28-E02
使用预注册的统一 grid：同一组 $s_0$（含 log-uniform、小值、近 1、边界外探针）和同一 matrix suite，对两组 coefficients 都跑 0—8 steps。报告 worst/median/quantiles、首次 residual rebound 和 cost；不能删掉某组不利区间，也不能只比较各自最优 step 而不计额外 GEMM。

### TRN28-E03
验收清单：

- 与 FP64 reference 的四类 residual；
- tall/wide/rank-deficient/zero matrix；
- BF16/FP16/FP32 输入与 accumulation；
- NaN/Inf、underflow、residual rebound guard；
- deterministic mode 或误差分布；
- noncontiguous/layout/shard correctness；
- peak temporary memory、kernel time、throughput；
- 失败时安全 fallback/skip 及日志；
- versioned coefficients、steps 和 compiler flags。

## 无提示重做

- [ ] 48 小时后推导 scalar map 与经典误差递推。
- [ ] 一周后设计一个会让“5 steps 足够”失败的 spectrum suite。
