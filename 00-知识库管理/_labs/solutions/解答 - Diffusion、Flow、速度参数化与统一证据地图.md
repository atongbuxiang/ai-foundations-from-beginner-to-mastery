---
type: solution
status: draft
topic: "[[Diffusion、Flow、速度参数化与统一证据地图]]"
exercise: "[[习题 - Diffusion、Flow、速度参数化与统一证据地图]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Diffusion、Flow、速度参数化与统一证据地图
## A. 识别与复述
### GEN56-A01
端点分布；中间 probability path；endpoint/trajectory coupling；conditional target；marginal score/velocity；parameterized network 与 training estimator；numerical sampler 与 evaluation protocol。
### GEN56-A02
同边缘只比较每个固定时间的 law；同路径律比较完整 multi-time process；同 population minimizer 比较理想期望目标；同 finite sampler 还要求模型、solver、NFE、随机数与实现输出一致。前一层通常不能推出后一层。
### GEN56-A03
$X_t=\alpha X_0+\sigma\epsilon$：$s=-\epsilon/\sigma=(\alpha X_0-X_t)/\sigma^2$；$X_0=(X_t-\sigma\epsilon)/\alpha$；instantaneous velocity $u=\dot\alpha X_0+\dot\sigma\epsilon$。各式需 $\alpha,\sigma$ 非退化。
## B. 手算与建模
### GEN56-B01
$d\alpha/d\phi=-\sin\phi=-\sigma$、$d\sigma/d\phi=\cos\phi=\alpha$，故
$$\frac{dX}{d\phi}=-\sigma X_0+\alpha\epsilon=\alpha\epsilon-\sigma X_0.$$
这依赖角度参数，不是任意 $t$ 的恒等式。
### GEN56-B02
$u=-X_0+2t\epsilon$，而 $v^{diff}=(1-t)\epsilon-t^2X_0$。取 $t=1/2,X_0=1,\epsilon=0$，前者 $-1$，后者 $-1/4$，不相等。
### GEN56-B03
drift $v+\varepsilon s=-x+0.3(-2x)=-1.6x$；diffusion amplitude $\sqrt{2\varepsilon}=\sqrt{0.6}$。SDE 为 $dX=-1.6Xdt+\sqrt{0.6}dW$，在给定 $p_t,s_t,v_t$ 一致且适定时共享密度方程。
## C. 推导与证明
### GEN56-C01
Fokker–Planck 右侧
$$-\nabla\cdot[p(v+\varepsilon s)]+\varepsilon\Delta p=-\nabla\cdot(pv)-\varepsilon\nabla\cdot(ps)+\varepsilon\Delta p.$$
因 $ps=\nabla p$，后两项抵消，剩 $-\nabla\cdot(pv)$，与 ODE 连续性方程相同。
### GEN56-C02
Score-SDE 的 PF velocity $v=f-g^2s/2$，移项得 $f=v+g^2s/2$。对应上一题的一族取 $\varepsilon=g^2/2$，diffusion $\sqrt{2\varepsilon}=g$。
### GEN56-C03
若 $y=A(t)z$，prediction error $y_\theta-y=A(z_\theta-z)$，未加权 MSE 为 $(z_\theta-z)^\top A^\top A(z_\theta-z)$。除 $A^\top A$ 是与时间/方向无关的 scalar multiple of identity，否则 metric/weight 改变，有限容量与优化折中也变。
## D. 边界、反例与纠错
### GEN56-D01
Brownian SDE 与其 PF ODE 可有同一 $N(0,1+t)$ 边缘；前者 conditional law 有新增噪声、quadratic variation 正，后者是初值确定放缩、quadratic variation 零，因此 coupling/path law 不同。
### GEN56-D02
可逆换算只保证理想输出空间一一对应。loss metric、time weighting、gradient scale、optimizer、clipping、finite precision 与 estimator variance可不同；sampling coefficient 写错也会破坏对应。
### GEN56-D03
统一框架描述可构造关系和密度方程，不包含特定网络逼近、训练预算、solver stability、数据 inductive bias 与指标协议。benchmark 优劣属于受控 empirical evidence，不能从统一 identity 演绎。
## E. AI 迁移
### GEN56-E01
六字段：比较的具体对象；时间/生成方向；所需假设；等价类型（identity/theorem/constant/minimizer/limit/empirical）；未覆盖误差；直接证据与可复现协议。任一为空就避免“本质等价”。
### GEN56-E02
随机生成合法 $\alpha,\sigma,X_0,\epsilon$，构造 $X_t$；逐对 round-trip 检查 data↔noise↔score，避开小分母并对边界单测；对角度 schedule 检查 $v^{diff}=dX/d\phi$，对一般 schedule 确认只等于 $\dot\alpha X_0+\dot\sigma\epsilon$；覆盖 batch/broadcast/dtype/tolerance。
### GEN56-E03
表中逐 claim 标：可代数复算的 identity；带假设原 theorem；exact score/infinite-capacity 的 continuous idealization；solver order/stability 的 numerical statement；固定协议与误差条的 experiment；机制解释/待证问题的 hypothesis。每格附来源、对象、假设、反例与当前复现状态。
