---
type: solution
status: draft
topic: "[[从离散扩散到 VP、VE 与 sub-VP SDE]]"
exercise: "[[习题 - 从离散扩散到 VP、VE 与 sub-VP SDE]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 从离散扩散到 VP、VE 与 sub-VP SDE
## A. 识别与复述
### GEN49-A01
令 $m(t)=\exp(\int_0^ta(s)ds)$，则
$$X_t\mid X_0=x_0\sim N\left(m(t)x_0,m(t)^2\int_0^t\frac{g(s)^2}{m(s)^2}ds\ I\right).$$
drift coefficient $a$ 决定 signal mean 的缩放；$a$ 与 $g$ 共同决定 conditional variance，因为已有噪声也会被后续 drift 放大或衰减。等价检查是 $m'=am$、$V'=2aV+g^2$。
### GEN49-A02
记 $B(t)=\int_0^t\beta(s)ds$。VP：$a=-\beta/2,g^2=\beta,V=1-e^{-B}$。VE：$a=0,g^2=\Sigma'(t),V=\Sigma(t)$。sub-VP：$a=-\beta/2,g^2=\beta(1-e^{-2B}),V=(1-e^{-B})^2$。
### GEN49-A03
$1/h$ 个独立步的方差要累积成 $O(1)$，故每步 variance 必须是 $O(h)$，标准差是 $O(\sqrt h)$。若随机项是 $O(h)$，每步 variance $O(h^2)$，总 variance $O(h)\to0$；极限只剩确定性 ODE。
## B. 手算与建模
### GEN49-B01
$B=\beta t=1$，两者均值系数 $m=e^{-1/2}\approx0.60653$。VP 方差 $1-e^{-1}\approx0.63212$；sub-VP 方差 $(1-e^{-1})^2\approx0.39958$。后者较小，差约 $0.23254$，但 signal decay 完全相同。
### GEN49-B02
$\sigma^2(t)=e^{2t}$，所以 $g(t)^2=d\sigma^2/dt=2e^{2t}$。$t=\log2$ 时 $e^{2t}=4$，$\Sigma(t)=4-1=3$。若忽略减去 $\sigma(0)^2$，就悄悄把初始数据改成 variance 1 的平滑分布。
### GEN49-B03
$m=e^{-t}$。方差
$$V=e^{-2t}\int_0^t4e^{2s}ds=2(1-e^{-2t}).$$
故 $X_t\mid X_0=x_0\sim N(e^{-t}x_0,2(1-e^{-2t})I)$。代入 $V'=-2V+4$ 可复核。
## C. 推导与证明
### GEN49-C01
令 $Y_t=X_t/m(t)$。因为 $m'=am$ 且 $m$ 确定，Itô 乘积法则使 drift 抵消：$dY_t=g(t)m(t)^{-1}dW_t$。积分得 $X_t=m(t)X_0+m(t)\int_0^tg/m\,dW$。随机积分均值为零，Itô isometry 给 covariance $m(t)^2\int_0^tg^2/m^2ds\ I$。
### GEN49-C02
$\sqrt{1-\beta(t)h}=1-\beta(t)h/2+o(h)$，一步增量为 $-\beta Xh/2+\sqrt\beta\sqrt h\epsilon+o(h)$，由局部条件矩识别 VP SDE。又
$$\log\bar\alpha_k=\sum_j\log(1-\beta(t_j)h)=-\sum_j\beta(t_j)h+O(h),$$
Riemann 和收敛到 $-B(t)$，故 $\bar\alpha\to e^{-B}$。
### GEN49-C03
候选 $V=(1-e^{-B})^2$ 的导数是 $2\beta e^{-B}(1-e^{-B})$。方差 ODE 右侧
$$-\beta(1-e^{-B})^2+\beta(1-e^{-2B})=2\beta e^{-B}(1-e^{-B}),$$
且 $V(0)=0$，因此候选解成立。
## D. 边界、反例与纠错
### GEN49-D01
应写 $X_{n+1}=X_n+f h+g\sqrt{|h|}\epsilon$。写成 $gh\epsilon$ 会把累计 variance 压到零；写成 $g\epsilon$ 又会使步数越多累计 variance 越大。反向网格的 drift 用带符号 $h$，噪声标准差用 $\sqrt{|h|}$。
### GEN49-D02
反例：常数 $\beta=2,t=0.5$ 时 VP variance 是 $0.632$，sub-VP 是 $0.400$；VE 若 $g^2=2$ 则 variance 是 $1$。时间只是 parameter，noise level 由 $m,V$ 或 log-SNR 决定。
### GEN49-D03
有限 $B$ 时 $m=e^{-B/2}>0$，terminal 仍含缩放数据；conditional variance 也小于极限值。若数据非 Gaussian，缩放数据与 Gaussian 的卷积一般也非严格 Gaussian。只有相应极限和正则条件下才收敛，有限终点需报告 prior mismatch。
## E. AI 迁移
### GEN49-E01
至少检查：时间网格单调；$\beta\ge0$；$g^2\ge0$；$B(0)=0$；$m(0)=1$；$V(0)=0$；数值差分满足 $m'\approx am$；满足 $V'\approx2aV+g^2$；VP/sub-VP 同 $m$；sub-VP $V\le V_{VP}$；VE $m=1$；所有 sqrt 输入非负且 finite。
### GEN49-E02
固定 $x_0,t$ 大量采闭式样本，比较样本 mean/variance 与解析值。再用多个步长 Euler–Maruyama 模拟完整路径，比较终点的 mean/variance error；在相同样本量与 seed policy 下画误差随 $h$ 缩小的趋势。闭式验 marginal，Euler 部分验离散弱误差，二者不要混成逐路径 equality。
### GEN49-E03
记录离散 $T$、时间归一化、$\beta_k$ 是 variance 还是 rate、从 $k$ 到 $t$ 的映射、端点 inclusion、插值方式、连续 $\beta(t)$ 公式、积分 $B(t)$ 算法、dtype、cumprod/log-sum 实现、目标 terminal SNR 以及离散/连续边缘最大偏差。
