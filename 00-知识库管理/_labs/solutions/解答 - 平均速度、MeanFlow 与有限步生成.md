---
type: solution
status: draft
topic: "[[平均速度、MeanFlow 与有限步生成]]"
exercise: "[[习题 - 平均速度、MeanFlow 与有限步生成]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 平均速度、MeanFlow 与有限步生成
## A. 识别与复述
### GEN70-A01
$v(z_t,t)$ 是局部切线；$u(z_t,r,t)$ 是给定区间沿实际轨迹的位移率；$F_{t\to r}$ 是把状态直接映到另一时间的 map。相同单位不等于相同对象。
### GEN70-A02
沿满足 $\dot z_s=v(z_s,s)$ 且经过当前 $z_t$ 的实际 trajectory；integrand 是 $v(z_s,s)$。
### GEN70-A03
固定 $r$，$D_tu=\partial_tu+J_zu\,v(z_t,t)$。JVP 的状态切向量是 $v$，上端时间切向量是 1，下端 $r$ 切向量是 0。
## B. 手算与建模
### GEN70-B01
$u=(t-r)^{-1}\int_r^t2ds=2$；$z_r=z_t-2(t-r)$。
### GEN70-B02
$z_t=e^t$。$u=(e-1)/(1-0)=e-1\approx1.71828$；端点速度平均 $(1+e)/2\approx1.85914$，不相等。
### GEN70-B03
$\partial_tu=1,J_zu=2$，故 $D_tu=1+2(z-t)$。
## C. 推导与证明
### GEN70-C01
ODE 积分给 $z_t-z_r=\int_r^tvds=(t-r)u$，移项即 $z_r=z_t-(t-r)u$。
### GEN70-C02
对 $(t-r)u(z_t,r,t)=\int_r^tv(z_s,s)ds$ 求全导数：左为 $u+(t-r)D_tu$，右为 $v(z_t,t)$；移项得到结论。
### GEN70-C03
$u$ 是连续函数 $s\mapsto v(z_s,s)$ 在缩小区间上的积分平均。由连续性，对任意 $\epsilon$，足够小区间内 integrand 与 $v(z_t,t)$ 差小于 $\epsilon$，故平均差也小于 $\epsilon$。
## D. 边界、反例与纠错
### GEN70-D01
$\dot z=z$ 的 $[0,1]$ 例子已给反例：真实平均 $e-1$，端点平均 $(1+e)/2$。后者只是 trapezoid approximation。
### GEN70-D02
不同曲线可共享同一对端点与相同总位移，弦/endpoint residual 都为零，但中间速度、曲率和 density evolution 不同。
### GEN70-D03
continuous likelihood 需要随时间定义的可微 invertible flow、divergence 积分与适定性。有限 map/average predictor 可能不满足 semigroup、可逆性或对应唯一连续 field。
## E. AI 迁移
### GEN70-E01
在 affine/exponential oracle flow 上算 analytic $u$；检查 identity、$r\to t$ boundary、endpoint、两段 composition；再加入 unseen intervals 与 off-trajectory perturbations。
### GEN70-E02
核对输入排列 $(z,r,t)$；JVP tangent 是否 $(v,0,1)$；$v$ 是否与 interpolation 方向一致；target 哪些项 stop-gradient；有限差分沿联合方向验证 $D_tu$。
### GEN70-E03
endpoint 到 rate 要除 $t-r$，短区间会放大 endpoint error；instantaneous velocity 做大步有 discretization error；average velocity直接匹配位移但 target 含 interval/JVP。应扫区间长度比较 target norm、梯度方差和终点误差。
