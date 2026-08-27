---
type: solution
status: draft
topic: "[[数据、噪声、速度与 Score 参数化]]"
exercise: "[[习题 - 数据、噪声、速度与 Score 参数化]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 数据、噪声、速度与 Score 参数化
## A. 识别与复述
### GEN43-A01
$x_t=ax_0+\sigma\epsilon,v=a\epsilon-\sigma x_0$；inverse $x_0=ax_t-\sigma v,\epsilon=\sigma x_t+av$，要求 VP convention $a^2+\sigma^2=1$。
### GEN43-A02
Noise MSE Bayes optimum $\epsilon^*(x_t,t)=E[\epsilon|x_t]$；marginal score $s^*(x_t,t)=-\epsilon^*/\sigma_t$。
### GEN43-A03
代数等价：同一 sample 的变量线性可换；Bayes 等价：unrestricted squared-loss conditional means 可换；训练等价还要求函数类、权重、optimizer、clipping/conditioning 等匹配，通常不自动成立。
## B. 手算与建模
### GEN43-B01
$x_t=0.8(2)+0.6(-1)=1$；$v=0.8(-1)-0.6(2)=-2$。反算 $x_0=0.8(1)-0.6(-2)=2$，$\epsilon=0.6(1)+0.8(-2)=-1$。
### GEN43-B02
$\sigma\approx0.953939$；$\hat x_0=(1-0.953939(0.2))/0.3\approx2.69737$。小 $a$ 放大 prediction error。
### GEN43-B03
$s^*=-(-0.3)/0.5=0.6$。
## C. 推导与证明
### GEN43-C01
$R=\begin{pmatrix}a&\sigma\\-\sigma&a\end{pmatrix}$，$R^TR=(a^2+\sigma^2)I=I$。故 inverse $R^T$，且 $\|x_t\|^2+\|v\|^2=\|x_0\|^2+\|\epsilon\|^2$。
### GEN43-C02
由 $x_0=(x_t-\sigma\epsilon)/a$，固定 $x_t$ 时 $\delta x_0=-(\sigma/a)\delta\epsilon$；故 $\|\delta\epsilon\|^2=(a^2/\sigma^2)\|\delta x_0\|^2=SNR\|\delta x_0\|^2$。
### GEN43-C03
$\nabla_{x_t}\log q(x_t|x_0)=-(x_t-ax_0)/\sigma^2=-\epsilon/\sigma$。Fisher identity/对 posterior 取期望给 $\nabla\log q_t(x_t)=E[\nablalog q(x_t|x_0)|x_t]=-E[\epsilon|x_t]/\sigma$。
## D. 边界、反例与纠错
### GEN43-D01
$\hat x_0=(x_t-\sigma\hat\epsilon)/a$ 的误差为 $-(\sigma/a)\delta\epsilon$；$a\to0$ 时增益无界，float error 与 model error 被放大。
### GEN43-D02
给同一 $x_t$ 可能有多个 $(x_0,\epsilon)$ posterior pairs；每个 $-\epsilon/\sigma$ 不同。Marginal score 是这些 conditional targets 的 posterior mean。
### GEN43-D03
Clipping 是非线性多对一映射；clip 后 $x_0$ 再换回 epsilon 不会恢复原网络输出，且等价 loss/mean 公式被改变。它是 sampler/model constraint，需单独报告。
## E. AI 迁移
### GEN43-E01
随机生成 $x_0,\epsilon,a,\sigma$，构造 $x_t,v$；四条 inverse round-trip；用 float64/32 和端点 sweep；比较各预测经统一转换得到的 $\hat x_0,\hat\epsilon$；验证 score 符号。
### GEN43-E02
统一 architecture/parameters、schedule、timestep proposal、显式 loss 在共同对象（如 x0 error）的权重、optimizer、clipping、EMA 和 sampling solver；同时报告 native loss 与换算后的 x0/noise/score error、质量和 NFE。
### GEN43-E03
按 log-SNR 分箱报告样本数、native MSE、统一 x0 MSE、epsilon MSE、score MSE、gradient norm、预测范数、clipping rate 和 sampler error；全局平均会掩盖端点失衡。

