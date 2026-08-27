---
type: solution
status: draft
topic: "[[Rectified Flow、ReFlow 与轨迹直化]]"
exercise: "[[习题 - Rectified Flow、ReFlow 与轨迹直化]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Rectified Flow、ReFlow 与轨迹直化
## A. 识别与复述
### GEN55-A01
$X_t=(1-t)X_0+tX_1$，target $U=X_1-X_0$，population field $v^*(x,t)=E[X_1-X_0|X_t=x,t]$。本卷从 data $t=0$ 到 reference $t=1$，生成反向积分。
### GEN55-A02
沿 ODE 的 material acceleration 是 $a_{mat}=\partial_tv+J_xv\,v=d^2Z_t/dt^2$。若沿轨迹恒为零，velocity 不变，轨迹为仿射直线；小但非零表示近似直化。
### GEN55-A03
采 reference；用当前模型高精积分得到 paired generated endpoint；保存新 endpoint coupling；在这些 pairs 的直线 interpolation 上回归 displacement；训练新模型并重新测曲率、NFE error 与质量。下一轮可重复。
## B. 手算与建模
### GEN55-B01
积分 $d\log Z=t dt$ 得 $Z_t=Z_0e^{t^2/2}$，所以 exact reverse $Z_0=e^{-1/2}Z_1$。从 $t=1$ 用一步 $h=-1$ 的 Euler：$\widehat Z_0=Z_1+(1\cdot Z_1)(-1)=0$，除零点外错误很大。
### GEN55-B02
路径长 $L=7$，chord 长 $5$，ratio $R=7/5=1.4$。说明路径比端点直线长 40%；它量几何绕行，不直接等于 Euler error。
### GEN55-B03
exact reverse $Z_0=Z_1-\int_0^1(a+bt)dt=Z_1-a-b/2$。一步 Euler 用 $v(1)=a+b$，得 $\widehat Z_0=Z_1-a-b$。因此 exact minus Euler 为 $b/2$，Euler error magnitude $|b|/2$。
## C. 推导与证明
### GEN55-C01
对固定 $(X_t,t)$，平方风险 $E[\|v-U\|^2|X_t,t]$ 对 $v$ 的 minimizer 是 conditional mean $E[U|X_t,t]$，可通过配方或对 $v$ 求导证明。这里 $U=X_1-X_0$。
### GEN55-C02
$\dot Z=v(Z,t)$。再次求导：$\ddot Z=\partial_tv(Z,t)+J_xv(Z,t)\dot Z=\partial_tv+J_xv\,v$。它包含显式 time variation 与位置变化两部分。
### GEN55-C03
exact reverse $Z_0=Z_1-\int_0^1v(Z_t,t)dt$；一步 Euler $\widehat Z_0=Z_1-v(Z_1,1)$。相减：
$$Z_0-\widehat Z_0=\int_0^1[v(Z_1,1)-v(Z_t,t)]dt.$$
沿轨迹 velocity 近常量时误差才小。
## D. 边界、反例与纠错
### GEN55-D01
teacher velocity 带端点 latent；learned field 是在同一 $(x,t)$ 的条件平均。交叉/邻近线段的方向会平均，生成 trajectory 按这个场重新演化，material acceleration 不必为零。
### GEN55-D02
non-increase 只说明新 coupling 的某类 convex cost 不超过旧 coupling，并未说明达到所有 couplings 中的最小值。还存在 theorem 条件、population field、有限网络和 solver gap；一次改进不等于全局 optimum。
### GEN55-D03
$Z_0$ 来自当前模型和有限 solver，包含 model bias、prior mismatch 和 numerical error；其分布可能已偏离真实数据。ReFlow 是 self-training coupling，不是重新获得无噪声 ground truth。
## E. AI 迁移
### GEN55-E01
冻结 teacher checkpoint；采 reference 与 seed；用声明的高精 solver 生成 $Z_0$；保存 $(Z_0,Z_1)$、teacher/solver 元数据；训练时采 $t$ 构造线性 $Z_t$ 与 target $Z_1-Z_0$；新模型不得反向传播进 teacher pairing；最后独立验证并版本化 round。
### GEN55-E02
几何：path-length ratio/曲率；动力学：$\|\partial_tv+J_vv\|$ 或沿轨迹 velocity variation；数值：1/2/4/8-step 对高精 reference endpoint error。再配端点 convex cost 与 sample-quality/coverage，不能只给二维轨迹图。
### GEN55-E03
固定架构、训练 token/steps、数据与评估样本；分别报告 pairing generation 的额外 NFE/wall time，以及 inference equal-NFE 与 equal-error cost。每轮多 seed；同时测 teacher bias、质量/覆盖、曲率、endpoint error，防止只选择改善的指标。
