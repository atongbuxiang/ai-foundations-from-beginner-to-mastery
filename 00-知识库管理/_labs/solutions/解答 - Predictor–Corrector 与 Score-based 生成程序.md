---
type: solution
status: draft
topic: "[[Predictor–Corrector 与 Score-based 生成程序]]"
exercise: "[[习题 - Predictor–Corrector 与 Score-based 生成程序]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Predictor–Corrector 与 Score-based 生成程序
## A. 识别与复述
### GEN31-A01
Predictor 近似 reverse-time SDE/ODE 在相邻时刻间的 transition/marginal evolution；corrector 冻结时间，用以当前 $p_t$ 为目标的 MCMC 作局部 relaxation。
### GEN31-A02
固定 $t$ 的 corrector 只保持/逼近 $p_t$，不会自动改变 noise schedule 或执行从 $t=T$ 到 0 的 transport。需要 predictor 或显式切换目标的 annealing 路径。
### GEN31-A03
Score approximation：$s_\theta-s_t$；solver：时间离散/随机数值误差；mixing：finite corrector 与 ULA bias；deployment：NFE、最后 denoise、clipping、temperature 和实现精度。
## B. 手算与建模
### GEN31-B01
Predictor 50 次，corrector $50\times2=100$ 次，总 NFE 150。若 corrector 每步需额外网络评估或最后 denoise 调用网络，应继续加上。
### GEN31-B02
$r=\sqrt{\alpha/2}\|s\|/\|z\|$，故 $\alpha=2r^2\|z\|^2/\|s\|^2=2(.01)(100)/25=0.08$。
### GEN31-B03
$x^+=2+0.1(-2)+\sqrt{0.2}(0.5)=1.8+0.223606\approx2.023606$。随机项可使能量暂时上升。
## C. 推导与证明
### GEN31-C01
平方 $r^2=\epsilon\|s\|^2/(2\|z\|^2)$，所以 $\epsilon=2r^2\|z\|^2/\|s\|^2$。若 $\|s\|$ 很小需 clipping，否则步长爆大。
### GEN31-C02
用 $dX=s_t(X)d\tau+\sqrt2dW$，目标 energy 为 $E_t=-\log p_t$，drift $-\nabla E_t=s_t$。Fokker–Planck current 在 $p_t$ 处为 $p_ts_t-\nabla p_t=0$。
### GEN31-C03
Exact predictor 若输出 $X\sim p_{t_{i-1}}$，再施加 invariant kernel $K$，则 law 为 $pK=p$。实践 predictor law 有偏、score 不精确、ULA kernel 的 invariant law 也有步长偏差且只跑有限步，故等式的前提逐层失效。
## D. 边界、反例与纠错
### GEN31-D01
Corrector 只读取当前 $x,t,s_\theta$ 与随机噪声，不知道 exact solution 或 local truncation error。它可将分布向 learned $p_t$ relaxation，但不是逐轨迹误差估计器。
### GEN31-D02
更多 steps 增加 NFE；ULA 还可能积累 discretization bias，过大步长会失稳，过多噪声可能破坏细节。固定 wall time 下会挤占 predictor resolution，需要受控比较。
### GEN31-D03
每个时间步可有多次 corrector score calls，高阶 predictor 也可每步多评估。只报网格长度会低估 PC 成本，必须用总 score evaluations 与 wall time。
## E. AI 迁移
### GEN31-E01
固定相同模型、initial noise、总 NFE 和最后处理：predictor-only 用更细网格；corrector-only 用 annealed levels；PC 分配相同预算。报告 FID/precision/recall、toy marginal error、runtime 与 seeds，并扫描预算分配。
### GEN31-E02
记录 SDE/schedule、time grid、predictor 名称/阶数、corrector kernel、每层 steps、步长/SNR/clipping、score parameterization、随机种子、NFE、wall time、dtype、最后 denoise、batch 与指标协议。
### GEN31-E03
MALA 用 MH ratio 校正 fixed-time ULA invariant bias，理论目标更精确；但需 proposal 两端密度/energy 或可算 log target，score-only model 未必提供 normalized-free energy difference，且拒绝导致分支和额外评估。高维接受率与 wall-time 可能抵消收益。

