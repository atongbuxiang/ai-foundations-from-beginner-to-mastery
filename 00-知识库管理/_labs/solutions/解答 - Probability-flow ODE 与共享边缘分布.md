---
type: solution
status: draft
topic: "[[Probability-flow ODE 与共享边缘分布]]"
exercise: "[[习题 - Probability-flow ODE 与共享边缘分布]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Probability-flow ODE 与共享边缘分布
## A. 识别与复述
### GEN51-A01
$$\partial_tp=-\nabla\cdot(fp)+\frac12g^2\Delta p,$$
$$v_{PF}=f-\frac12g^2\nabla\log p,\qquad\dot X=v_{PF}(X,t).$$
公式假定 $g$ 空间无关；一般 $D(x,t)$ 还需 $-(1/2)\nabla\cdot D$。
### GEN51-A02
它指对每个固定 $t$，两过程的 law 都是 $p_t$。不能推出同一 conditional transition、同一 multi-time joint/coupling、同一 sample path 或 quadratic variation，也不推出 finite solver 输出相同。
### GEN51-A03
PF ODE 没有扩散项，score velocity 单独替代 Fokker–Planck 中 $(1/2)g^2\Delta p$，故系数 $1/2$。reverse SDE 仍有 Brownian diffusion；时间反向后 drift 需完整 $g^2s$ 才与该扩散通量共同配平。
## B. 手算与建模
### GEN51-B01
$p_t=N(0,(1+t)I)$，$s=-x/(1+t)$，故 $v=x/[2(1+t)]$。积分 $d\log|X|=dt/[2(1+t)]$，得 $X_t=\sqrt{1+t}X_0$，于是 covariance 为 $(1+t)I$。
### GEN51-B02
SDE：$X_t|X_0=x_0\sim N(x_0,tI)$。ODE：$X_t|X_0=x_0$ 是点质量在 $\sqrt{1+t}x_0$。边缘对随机 $X_0\sim N(0,I)$ 相同，conditional law 完全不同。
### GEN51-B03
$(\nabla\cdot D)_i=\sum_j\partial_jD_{ij}$。给定对角 $D$，第一分量为 $\partial_{x_1}(1+x_1^2)=2x_1$，第二分量为 $\partial_{x_2}2=0$，所以 $\nabla\cdot D=(2x_1,0)^\top$。
## C. 推导与证明
### GEN51-C01
$\Delta p=\nabla\cdot(\nabla p)=\nabla\cdot(p\nabla\log p)$。代入 FP：
$$\partial_tp=-\nabla\cdot(fp)+\frac12g^2\nabla\cdot(ps)=-\nabla\cdot[p(f-g^2s/2)],$$
即 ODE 连续性方程。
### GEN51-C02
非退化 Itô SDE 的 quadratic variation 是 $\int_0^tg(s)^2ds>0$。局部 Lipschitz ODE path 绝对连续、有限变差，quadratic variation 为零。若 path law 相同，这一可测路径泛函的分布也应相同，矛盾。
### GEN51-C03
连续性方程沿 ODE trajectory 给
$$\frac d{dt}\log p_t(X_t)=\partial_t\log p+v\cdot\nabla\log p=-\nabla\cdot v.$$
积分即可用 base log-density 与 divergence integral 换算 data log-density；积分方向决定最后符号。
## D. 边界、反例与纠错
### GEN51-D01
二维标准 Gaussian $p\propto e^{-\|x\|^2/2}$，取旋转场 $w=(-x_2,x_1)$。$\nabla\cdot w=0$，且 $\nabla p=-px$ 与 $w$ 正交，故 $\nabla\cdot(pw)=\nabla p\cdot w+p\nabla\cdot w=0$。所以 $v$ 与 $v+w$ 运输同一 density。
### GEN51-D02
tolerance 只控制 numerical approximation 到 learned ODE。若 prior、score 或 model velocity 已错，精确积分只会更精确地解错的动力学；总误差仍含 terminal mismatch 与 model error。
### GEN51-D03
DDIM 是特定共享边缘的离散 non-Markov family/update；PF ODE 是连续 FP 配平。二者在适当连续极限相关，但有限步公式、parameterization 和截断误差不同，不能把任意 ODE solver 输出都称为 DDIM。
## E. AI 迁移
### GEN51-E01
用 Brownian Gaussian 例子：同一批 $X_0$，一边模拟 SDE 多条 Brownian paths，一边用 exact PF scaling；逐时刻比较 mean/variance/分布距离，同时比较给定初值 conditional variance 与 quadratic variation。预期 marginal 接近、path statistics 明显不同。
### GEN51-E02
记录 base density、积分方向、divergence exact/Hutchinson、probe 数量/分布/seed、ODE solver、rtol/atol、NFE、state dtype、score network 版本、dequantization 和数据尺度；分别报告 trace Monte Carlo error 与 solver refinement error。
### GEN51-E03
用高精度 oracle score/velocity 建 reference trajectory，然后：固定高精 solver 换 learned model，估 model error；固定同一 model 逐级缩 tolerance/步长，估 discretization error。两轴交叉实验，不用粗 solver 输出当 ground truth。
