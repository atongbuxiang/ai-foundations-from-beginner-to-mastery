---
type: solution
status: draft
topic: "[[Mean-Field、Feature Learning 与训练 Regime]]"
exercise: "[[习题 - Mean-Field、Feature Learning 与训练 Regime]]"
created: 2026-08-23
updated: 2026-08-28
---
# 解答 - Mean-Field、Feature Learning 与训练 Regime
## A
### LT-MF-A01
$\rho_m=m^{-1}\sum_{j=1}^m\delta_{\vartheta_j}$。若 $\phi(x;\vartheta)=a\sigma(w^Tx)$，则 $f_m(x)=m^{-1}\sum_j\phi(x;\vartheta_j)=\int\phi(x;\vartheta)\rho_m(d\vartheta)$。
### LT-MF-A02
若 $v_t(\vartheta)=-\nabla_\vartheta\Psi(\vartheta;\rho_t)$，质量守恒给 $\partial_t\rho_t+\nabla\cdot(\rho_tv_t)=0$，即 $\partial_t\rho_t=\nabla\cdot(\rho_t\nabla\Psi)$。
### LT-MF-A03
积分 $f_\rho=\int\phi d\rho$ 对 measure 是线性的；但速度势 $\Psi$ 包含 residual $f_\rho-y$，所以速度场依赖当前全体 $\rho$。于是 transport equation 的系数也依赖解本身，是非线性 dynamics。
## B
### LT-MF-B01
$\rho_3=(\delta_{\vartheta_1}+\delta_{\vartheta_2}+\delta_{\vartheta_3})/3$，且 $\int g(\vartheta)d\rho_3=[g(\vartheta_1)+g(\vartheta_2)+g(\vartheta_3)]/3$。
### LT-MF-B02
令 $T_t(\vartheta)=\vartheta+tv$，则 $\rho_t=(T_t)_\#\rho_0$；即对集合 $A$，$\rho_t(A)=\rho_0(A-tv)$。
### LT-MF-B03
$1/m=0.01$，$1/\sqrt m=0.1$。这只是输出归一化的一部分；还不能不看初始化、learning rate 和 time scaling 就判定 regime。
## C
### LT-MF-C01
对光滑测试函数 $g$，粒子平均满足 $d[m^{-1}\sum_jg(\vartheta_j)]/dt=m^{-1}\sum_j\nabla g(\vartheta_j)\cdot v(\vartheta_j)$。极限为 $d\int g,d\rho_t/dt=\int\nabla g\cdot v_t,d\rho_t$；分部积分得 $\partial_t\rho+\nabla\cdot(\rho v)=0$ 的弱形式。
### LT-MF-C02
$1/m$ 前因子使单粒子对输出/gradient 的贡献随 $m$ 缩小；若学习率和时间不补偿，极限可能冻结，若补偿过强则发散或进入不同动力学。非平凡 mean-field ODE/PDE 由这三者共同定义。
### LT-MF-C03
证明有限时间内 empirical measure $\rho_{m,t}$ 集中于 deterministic $\rho_t$，并使固定有限个粒子的 joint law 接近独立 copies。这样 PDE 预测可带 finite-$m$ 误差转回真实网络；长时间、非光滑与深层依赖需另证。
## D
### LT-MF-D01
raw movement 不具参数化不变性，也可能是无用漂移或噪声拟合。需要联合 kernel/feature covariance drift、linear probe、transfer、受控干预及 held-out risk，才能支持“有用 feature learning”。
### LT-MF-D02
对象不匹配：两层、特定 scaling/activation/init/population 或 noisy dynamics 的 theorem 不覆盖多层 attention、normalization、finite batch、自适应优化。还需 finite-width bridge、architecture-specific dynamics 与 risk theorem。
### LT-MF-D03
固定有限时间的 finite-width approximation error 可随时间累积；PDE 可能在 $t\to\infty$ 接近的 measure 也未由 finite-$m$ 网络 uniform-in-time 跟踪。相反有限网络先长时间训练可经历 kernel change/particle correlations，导致不同极限。
## E
### LT-MF-E01
跨 width 与 parameterization 锁定有效 step/time，测 kernel drift、线性化误差、activation covariance/CKA、tangent-subspace residual、particle-distribution统计与 transfer probes；加入 analytical NTK、mean-field simulation 和 finite model，对训练早中晚分段并报告 seed uncertainty。
### LT-MF-E02
在 source task 预训练后冻结表示，用低样本 target linear probe；对照随机初始化 feature、NTK predictor、同 training loss 但不同 feature movement 的 scaling，并做 label/augmentation干预。若只 source fit 改善而 transfer 不改善，不能称任务有用的 feature learning。
### LT-MF-E03
claim card：网络/前因子/init/learning-rate/time scaling；经验测度与势函数；PDE解的存在/唯一/收敛对象；$m\to\infty,t\to\infty,n\to\infty$ 顺序；propagation-of-chaos误差和时间窗；population/empirical risk；两层到深层外推等级；可证伪 observable。
