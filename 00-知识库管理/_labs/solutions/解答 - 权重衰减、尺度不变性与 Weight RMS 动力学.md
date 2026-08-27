---
type: solution
status: verified
area: [training, optimization, adamw, weight-rms, scale-invariance]
topic: "[[权重衰减、尺度不变性与 Weight RMS 动力学]]"
exercise: "[[习题 - 权重衰减、尺度不变性与 Weight RMS 动力学]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 权重衰减、尺度不变性与 Weight RMS 动力学

> [!warning] 使用边界
> 稳态平方根律需要平稳、弱相关和 optimizer-direction 二阶矩近似固定；动态训练必须回到精确记忆递推。

## A. 识别与复述

### TRN38-A01
coupled L2 把 $\lambda\theta$ 加进梯度，再让 optimizer 预条件；decoupled decay 直接执行 $(1-\eta\lambda)\theta$，不经过梯度预条件。普通 SGD 且同一 LR 时两者都产生 $-\eta\lambda\theta$，可等价；Adam 对 $g+\lambda\theta$ 做逐坐标 moments/除以 $\sqrt v$，不等于统一径向收缩。

### TRN38-A02
$a_t^2q_t$ 是旧权重能量经 decay 后的保留；$\eta_t^2r_t$ 是 optimizer 方向注入的新能量；$-2a_t\eta_tc_t$ 是权重与方向的对齐交叉项。$c_t>0$ 时更新更倾向减小半径，$c_t<0$ 时可能增大；忽略它需要数据或几何理由。

### TRN38-A03
尺度不变意味着 $f(cw)=f(w)$（$c>0$），功能只依赖方向。此时 raw gradient norm 随半径约为 $1/\|w\|$；SGD step norm 为 $\eta/\|w\|$，再除半径得 angular LR $\eta/\|w\|^2$。若 optimizer 把方向归一到常数 norm，step norm 约 $\eta$，angular LR 为 $\eta/\|w\|$。

## B. 手算与构造

### TRN38-B01
$$
\theta_1=0.9(2)-0.1(1)=1.7,
$$
$$
\theta_2=0.9(1.7)-0.1(-1)=1.63,
$$
$$
\theta_3=0.9(1.63)-0.1(2)=1.267.
$$
历史核给
$$
0.9^3(2)-0.1[0.9^2(1)+0.9(-1)+2]
=1.458-0.191=1.267.
$$

### TRN38-B02
$a=1-eta\lambda=0.999$，在 $c=0$ 时
$$
q_\star=\frac{\eta^2r}{1-a^2}
=\frac{0.0004}{0.001999}
\approx0.20010005.
$$
小步近似为 $\eta r/(2\lambda)=0.2$，相对误差约 $5\times10^{-4}$。RMS 是 $\sqrt q\approx0.44733$，而不是 $q$ 本身。

### TRN38-B03
历史 shrinkage 为
$$
(1-0.1\cdot0.2)^3(1-0.01\cdot0.2)^2
=0.98^3\,0.998^2\approx0.937431.
$$
五步全用末段配置则 $0.998^5\approx0.990040$。当前配置相同不抹去前三步更强衰减的记忆。

## C. 推导与证明

### TRN38-C01
反复代入得
$$
\theta_t=\left(\prod_{j=0}^{t-1}a_j\right)\theta_0
-\sum_{k=0}^{t-1}\eta_k
\left(\prod_{j=k+1}^{t-1}a_j\right)u_k.
$$
空积按 1。每个历史方向的权重由之后所有 decay factor 决定，所以时变 LR/WD 共同定义非平稳记忆核。

### TRN38-C02
平方一步更新并取期望：
$$
q_{t+1}=a^2q_t+\eta^2r_t-2a\eta c_t.
$$
若 $a,r$ 常数、$c=0$ 且 $|a|<1$，
$$
q_\star=\frac{\eta^2r}{1-(1-\eta\lambda)^2}
=\frac{\eta r}{2\lambda-eta\lambda^2}.
$$
当 $\eta\lambda\ll1$，$q_\star\approx\eta r/(2\lambda)$，故 RMS $\propto\sqrt{\eta/\lambda}$，比例常数还含 $r/2$。

### TRN38-C03
令 $\phi(c)=f(cw)$，尺度不变使 $\phi'(1)=0$，链式法则给 $w^T\nabla f(w)=0$，梯度是切向的。又由齐次关系可得 $\|g(cw)\|\propto1/c$。SGD 的切向 step 为 $\eta\|g\|\propto\eta/\|w\|$，除半径得角度 $\propto\eta/\|w\|^2$；单位方向更新的 step 约 $\eta$，角度 $\propto\eta/\|w\|$。

## D. 边界、反例与纠错

### TRN38-D01
失效条件包括：$r_t$ 随半径/LR 改变；$c_t\ne0$；schedule 尚未混合到稳态；参数并非尺度不变；decay factor 太大；optimizer direction 非平稳。数值反例：若 $u_t=-\theta_t$，则 $c_t=-q_t$，递推实际为 $\theta_{t+1}=(a+eta)\theta_t$，可膨胀，完全不服从弱相关稳态式。

### TRN38-D02
题 B03 已给出相同末段 $\eta/\lambda$、不同历史导致当前半径不同。即使历史一致，若 run A 的 $c_t=0$、run B 的方向长期与权重正相关，交叉项会额外收缩 B。瞬时 ratio 不是充分状态。

### TRN38-D03
尺度不变网络中沿径向改变权重可改变 RMS 却不改变函数；反过来相同 RMS 的两个方向可实现不同函数。即使参数完全相同，SGD、Adam、Muon 的 $u_t$ 与 Jacobian 投影不同，下一 feature step 也不同。应联合观察角更新和 probe function change。

## E. AI 迁移

### TRN38-E01
matrix 按逻辑矩阵/层记录 RMS、radial/tangential update、decay product；embedding 还可按 token-frequency 分位；norm scale 与 bias 维度和功能不同，应单独且通常明确 no-decay。共享参数只由一个 owner 计数；不能把大量 matrix 元素的全局 RMS 与小型 norm/bias 混成一个平均。

### TRN38-E02
先在稳定段达到近似平台，再单独阶跃 LR 或 WD，保持其他配置和数据配对。记录 $q,r,c$、predicted one-step $q_{t+1}$、effective decay product、angular/feature step；用精确递推预测过渡曲线。只有残差小、最终平台随 $\eta/\lambda$ 的平方根移动且多阶段一致，才接受近似；否则报告动态/相关项。

### TRN38-E03
动态调 WD 只能改变未来 $a_t$，旧方向仍通过积核存在；瞬时 $\sqrt{\eta/\lambda}$ 还假设 $r,c$ 不变。审计需先验证 exact $q$ recursion，再测 lag 和相关项，最后检查 angular/feature metrics；结论应写成“在给定组和稳态范围近似保持 RMS”，不能升级为保持函数训练速度。

## 无提示重做

- [ ] 48 小时后从一步更新推导 $q_t$ 三项账。
- [ ] 一周后解释 SGD 与 normalized direction 的角 LR 指数差异。
