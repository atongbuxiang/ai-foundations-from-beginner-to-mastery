---
type: solution
status: draft
topic: "[[连续性方程、概率路径与 Flow Matching]]"
exercise: "[[习题 - 连续性方程、概率路径与 Flow Matching]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 连续性方程、概率路径与 Flow Matching
## A. 识别与复述
### GEN53-A01
probability path $p_t$ 是各时间分布截面；sample trajectory $X_t(\omega)$ 是某个随机样本的时间曲线；velocity field $v_t(x)$ 是 ODE 到位置 $x$ 时使用的瞬时方向。相同 $p_t$ 可由不同 coupling/trajectory/velocity 实现。
### GEN53-A02
强形式是 $\partial_tp_t+\nabla\cdot(p_tv_t)=0$。弱形式是对每个光滑紧支撑 $\varphi$，
$$\frac d{dt}\int\varphi p_tdx=\int\nabla\varphi\cdot v_tp_tdx.$$
它通过分部积分与强形式相连，并显式编码边界通量。
### GEN53-A03
它排除训练 loss 内对 learned ODE trajectory 的数值模拟：可直接采 $X_t,U_t$。它没有排除生成时 ODE solver、likelihood divergence integration，也不保证 conditional path/OT target 本身计算便宜。
## B. 手算与建模
### GEN53-B01
$U_t=\partial_t[(1-t)X_0+tX_1]=X_1-X_0$，对固定端点对与 $t$ 无关。
### GEN53-B02
$X_t\sim N(0,(1-t)+t)=N(0,1)$，密度不变，可取 $v=0$。但
$$U=-\frac{X_0}{2\sqrt{1-t}}+\frac\epsilon{2\sqrt t}$$
通常非零。给定 $X_t=x$，$E[X_0|X_t]=\sqrt{1-t}x$、$E[\epsilon|X_t]=\sqrt t x$，两项平均后恰好抵消。
### GEN53-B03
取 $\varphi(x)=x$，弱式给 $m'(t)=E[v(X_t)]=cm(t)$，所以 $m(t)=m_0e^{ct}$。这与逐样本解 $X_t=e^{ct}X_0$ 一致。
## C. 推导与证明
### GEN53-C01
沿 ODE 有 $d\varphi(X_t)/dt=\nabla\varphi\cdot v$。取期望并写成 density integral，再分部积分：$d\int\varphi p/dt=-\int\varphi\nabla\cdot(pv)dx$。对所有 $\varphi$ 成立即得到弱连续性方程。
### GEN53-C02
$X_t=\phi_t(Z),U_t=\partial_t\phi_t(Z)$。对 $\varphi$：
$$\frac d{dt}E\varphi(X_t)=E[\nabla\varphi(X_t)\cdot U_t]=E[\nabla\varphi(X_t)\cdot E(U_t|X_t)],$$
所以 $v=E(U|X)$ 满足同一弱式并运输该 marginal path。
### GEN53-C03
令 $v(X)=E[U|X]$，展开 $\|U-v_\theta\|^2$ 并以 $v$ 插入。交叉项因 $E[U-v|X]=0$ 消失，得到 $L_{CFM}=L_{FM}+E\|U-v\|^2$。后项依赖 path/coupling，但不依赖模型参数。
## D. 边界、反例与纠错
### GEN53-D01
若 $w$ 满足 $\nabla\cdot(pw)=0$，则 $v+w$ 与 $v$ 给出同一连续性方程。二维旋转 current 就是例子；因此 density path 只约束通量散度。
### GEN53-D02
网络只输入 $(x,t)$，在交叉处输出多条 straight target 的条件平均；生成轨迹随后不断读取这个平均场，可能弯曲。条件直线属于带 latent 的 teacher construction，不是 marginal ODE path identity。
### GEN53-D03
训练可直接采监督对，但生成必须把 reference sample 运输到 data endpoint，仍需积分 learned velocity。除非另学有限步 map/consistency object，simulation-free training 不会自动给 closed-form endpoint map。
## E. AI 迁移
### GEN53-E01
采 $t:[B]$、端点/latent $Z$；构造 $X_t:[B,d]$ 与 $U_t:[B,d]$；网络输入 $X_t,t$，输出同形 velocity；loss 对 feature 维求平方再按 batch/time weighting。记录 endpoint direction、coupling、time sampler、random seed、是否额外噪声及 target stop-gradient。
### GEN53-E02
选一组 $\varphi_k$（坐标、平方、Fourier/RBF）。用邻近时间样本估 $[E\varphi(X_{t+h})-E\varphi(X_t)]/h$，与 $E[\nabla\varphi(X_t)\cdot v_\theta(X_t,t)]$ 比较；报告 Monte Carlo CI、finite-difference bias 与按时间 residual。
### GEN53-E03
记录 $\|U_t\|$、分位数、gradient norm 和 Lipschitz/Jacobian proxy 随 $t$ 的曲线；做端点截断 $[\delta,1-\delta]$、time reparameterization 和 weighting 消融；同时报告 endpoint mismatch，避免只靠截断隐藏奇异而改变任务。
