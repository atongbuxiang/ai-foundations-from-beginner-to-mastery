---
type: solution
status: verified
area: [training, optimization, curvature]
topic: "[[Newton、Damping、Trust Region 与 Levenberg–Marquardt]]"
exercise: "[[习题 - Newton、Damping、Trust Region 与 Levenberg–Marquardt]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Newton、Damping、Trust Region 与 Levenberg–Marquardt

> [!warning] 使用边界
> 二阶方程只给 candidate。是否接受该步，还要看正定性、约束、真实下降和数值求解证书。

## A. 识别与复述

### TRN18-A01
Newton 解 $Bp=-g$，即无约束二次模型的驻点；damped step 解 $(B+\lambda I)p=-g$，修改局部曲率以抑制敏感 eigenmode；trust region 直接解 $\min_{\|p\|\le\Delta}m(p)$，把可信范围写成约束。只有在相应正定与最优性条件下，前两者才是模型极小点。

### TRN18-A02
Curvature damping 只改变用于求 step 的局部矩阵；$L_2$ penalty 改变目标、梯度和 Hessian；AdamW decay 在 optimizer transition 中直接缩放参数并与自适应梯度步解耦。三者可出现 $\lambda$，但作用对象、持久状态和 fixed point 不同。

### TRN18-A03
$\operatorname{ared}=L(\theta)-L(\theta+p)$，$\operatorname{pred}=m(0)-m(p)$，$\rho=\operatorname{ared}/\operatorname{pred}$。只有 pred 为正且超过数值阈值时，比值才表示“实际下降占预测下降多少”；否则分母符号或消减误差会让比值无意义。

## B. 手算与构造

### TRN18-B01
Newton step 为 $p_N=(-2,1/3)^\top$。$B+3I=\operatorname{diag}(4,12)$，所以 $p_\lambda=(-1/2,1/4)^\top$。相对 Newton，两个 eigenmode 分别乘 $1/(1+3)=1/4$ 与 $9/(9+3)=3/4$；低曲率方向收缩得更多。

### TRN18-B02
$m'(p)=-2-p$、$m''(p)=-1<0$，无约束驻点 $p=-2$ 是最大点且在区间外。端点比较得 $m(1)=-2.5<m(-1)=1.5$，故全局解 $p^*=1$，predicted reduction 为 $m(0)-m(1)=2.5$。

### TRN18-B03
第一步 ared $=0.6$，pred $=0.5$，所以 $\rho=1.2$：实际下降略优于模型，通常接受并可能扩大半径。第二步 ared $=-0.1$，所以 $\rho=-0.2$：loss 上升，通常拒绝并缩小半径或增大阻尼。

## C. 推导与证明

### TRN18-C01
当 $B\succ0$，
$$m(p)=\tfrac12(p+B^{-1}g)^\top B(p+B^{-1}g)-\tfrac12g^\top B^{-1}g.$$
第一项非负且仅在 $p=-B^{-1}g$ 为零，故唯一极小。若 $B$ 不正定，第一项不再是范数，沿负曲率方向可下降，完成平方不再给下界。

### TRN18-C02
令 $\tilde p=Q^\top p,\tilde g=Q^\top g$，则 $(\mu_i+\lambda)\tilde p_i=-\tilde g_i$，所以 $\tilde p_i=-\tilde g_i/(\mu_i+\lambda)$。对称 $B$ 下，$B+\lambda I\succ0$ 当且仅当 $\lambda>-\mu_{\min}$；若只需半正定则为 $\lambda\ge-\mu_{\min}$。

### TRN18-C03
全局解满足
$$ (B+\lambda I)p=-g,\quad B+\lambda I\succeq0,\quad \lambda\ge0,\quad \|p\|\le\Delta,\quad \lambda(\|p\|-\Delta)=0.$$
若无约束 Newton 解位于球内，$\lambda=0$；否则约束活跃、$\|p\|=\Delta$，$\lambda$ 同时充当半径的 dual variable 与 curvature shift。

## D. 边界、反例与纠错

### TRN18-D01
取 $B=\operatorname{diag}(1,-1)$、$g=(1,1)$。Newton 方程给 $p=(-1,1)$，但 $m$ 沿第二坐标含 $-p_2^2/2$，无下界；驻点是 saddle。线性代数上的唯一解只证明 stationarity，不证明 minimum 或真实 loss 下降。

### TRN18-D02
大 damping 能改善线性系统正定性，却会把 $p$ 缩成近似 $-g/\lambda$，导致模型下降和实际进展过小；求解/刷新曲率仍有成本。训练速度是每步进展、失败重试、吞吐和调参共同结果，不随稳定性单调增加。

### TRN18-D03
若 $g\approx0$ 且 $p$ 极小，pred 可能接近机器精度；若不定模型给出的候选让 $m(p)\ge m(0)$，pred 非正。此时比值可爆炸或反号。实现应要求 `pred > atol + rtol*scale`，否则标记 `invalid_model_decrease`，拒绝/回退并重新求步。

## E. AI 迁移

### TRN18-E01
记录 `old/new_loss`、`ared/pred/rho`、`radius`、`lambda`、`step_norm`、`gTp`、`pTBp`、线性 residual、negative-curvature flag、boundary hit、accept/reject、重试数、HVP 数和 wall-clock。还需注明 loss batch 与 reduction，否则 ared 不可比较。

### TRN18-E02
冻结同一 batch、dropout mask、数据增强 seed、model buffers 与 precision policy，在旧参数和候选参数上成对评估；或用足够大的独立评估 batch 并报告 paired uncertainty。不能让两次 loss 使用无关随机 realization 后再把差值全归于 step。

### TRN18-E03
给两类方法相同训练 token/样本、总加速器时、搜索次数与预注册参数空间；统一初始化、数据顺序、checkpoint/early-stop 规则，并把 OOM、NaN 与失败 trial 计入。报告 time-to-quality、最终质量、峰值/平均内存、通信与能耗；LM 一步含多次 HVP/solve，故 iteration 不是等额成本。

## 无提示重做

- [ ] 48 小时后从 KKT 条件统一 Newton 与边界步。
- [ ] 一周后根据一串 $\rho$ 值手工更新 accept/reject 与半径策略。
