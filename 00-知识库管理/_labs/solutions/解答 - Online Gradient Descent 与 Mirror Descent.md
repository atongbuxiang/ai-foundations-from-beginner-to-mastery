---
type: solution
status: draft
topic: "[[Online Gradient Descent 与 Mirror Descent]]"
exercise: "[[习题 - Online Gradient Descent 与 Mirror Descent]]"
created: 2026-08-23
updated: 2026-08-28
---
# 解答 - Online Gradient Descent 与 Mirror Descent

## A

### LT-OMD-A01
$\mathcal W$ 是闭凸集，每轮 $\ell_t$ 在 $\mathcal W$ 上凸；取 $g_t\in\partial\ell_t(w_t)$，OGD 为
$$w_{t+1}=\Pi_{\mathcal W}(w_t-\eta g_t).$$
static regret 是 $\sum_t\ell_t(w_t)-\inf_{u\in\mathcal W}\sum_t\ell_t(u)$。

### LT-OMD-A02
凸性把 loss difference 上界为 $\langle g_t,w_t-u\rangle$；projection nonexpansiveness 产生单步势能差；diameter $D$ 控制首尾势能；$\|g_t\|\le G$ 控制每轮二次项；projection 保证 iterate 留在 theorem 的 domain。

### LT-OMD-A03
对可微严格凸 $\psi$，
$$D_\psi(u,w)=\psi(u)-\psi(w)-\langle\nabla\psi(w),u-w\rangle.$$
若 $D_\psi(u,w)\ge\frac\alpha2\|u-w\|^2$，则 $\psi$ 对该 norm 为 $\alpha$-strongly convex。dual norm 是 $\|g\|_* =\sup_{\|v\|\le1}\langle g,v\rangle$。

## B

### LT-OMD-B01
对任意 $u\in\mathcal W$，projection nonexpansiveness 给
$$
\|w_{t+1}-u\|^2
\le\|w_t-\eta g_t-u\|^2
=\|w_t-u\|^2-2\eta\langle g_t,w_t-u\rangle+\eta^2\|g_t\|^2.
$$
移项即
$$\langle g_t,w_t-u\rangle\le\frac{\|w_t-u\|^2-\|w_{t+1}-u\|^2}{2\eta}+\frac\eta2\|g_t\|^2.$$

### LT-OMD-B02
导数 $-D^2/(2\eta^2)+G^2T/2=0$，故 $\eta^*=D/(G\sqrt T)$；代回得 $DG\sqrt T$。

### LT-OMD-B03
在 simplex 用 $\psi(p)=\sum_i p_i\log p_i$，OMD 的 unconstrained dual step 后归一，得到
$$p_{t+1,i}=\frac{p_{t,i}e^{-\eta g_{t,i}}}{\sum_jp_{t,j}e^{-\eta g_{t,j}}}.$$
这正是指数权重；初始坐标必须为正，否则 multiplicative update 无法复活零坐标。

## C

### LT-OMD-C01
凸性给 $\ell_t(w_t)-\ell_t(u)\le\langle g_t,w_t-u\rangle$。代入 B01 单步式并对 $t$ 求和，势能 telescope：
$$
R_T(u)\le\frac{\|w_1-u\|^2}{2\eta}+\frac\eta2\sum_t\|g_t\|^2
\le\frac{D^2}{2\eta}+\frac{\eta G^2T}{2}.
$$
取 $\eta=D/(G\sqrt T)$ 得 $R_T(u)\le DG\sqrt T$，再对 $u$ 取 infimum。

### LT-OMD-C02
OMD 更新
$$w_{t+1}=\arg\min_{w\in\mathcal W}\{\eta\langle g_t,w\rangle+D_\psi(w,w_t)\}.$$
一阶变分不等式对任意 $u$ 给
$$\langle\eta g_t+\nabla\psi(w_{t+1})-\nabla\psi(w_t),u-w_{t+1}\rangle\ge0.$$
用三点恒等式把后一项写为
$$D_\psi(u,w_t)-D_\psi(u,w_{t+1})-D_\psi(w_{t+1},w_t).$$
再拆 $\langle g_t,w_t-u\rangle$，用 Hölder 与 strong convexity 吸收 $w_t-w_{t+1}$，得到
$$
\eta\langle g_t,w_t-u\rangle
\le D_\psi(u,w_t)-D_\psi(u,w_{t+1})+\frac{\eta^2}{2\alpha}\|g_t\|_*^2.
$$
求和 telescope 即 OMD bound。

### LT-OMD-C03
取 $\ell(w)=-w^2$，在 $w_t=0$ 有 gradient $0$，但对 $u=1$，$\ell(0)-\ell(1)=1$，而 $\langle0,0-1\rangle=0$。所以凸函数所需的 $\ell(w_t)-\ell(u)\le\langle g_t,w_t-u\rangle$ 失败。

## D

### LT-OMD-D01
例如 $\mathcal W=[0,1]$、$w_1=0.9$、$g_1=-1$、$\eta=1$，无 projection 得 $w_2=1.9\notin\mathcal W$。此后 loss/gradient bound 可能未定义，diameter 也不能控制势能，OGD theorem 的可行性链条断裂。

### LT-OMD-D02
simplex 在 $\ell_2$ 下 diameter 至多 $\sqrt2$，但若 gradient 只在 $\ell_\infty$ 有界，转成 $\ell_2$ 常引入 $\sqrt N$。negative entropy 对 $\ell_1$ strong convex，其 Bregman radius 对 uniform start 到 vertex 为 $\log N$，dual norm 是 $\ell_\infty$，由此得到 $\sqrt{T\log N}$ 而非典型 $\sqrt{TN}$ 尺度。

### LT-OMD-D03
若用 $\widetilde g_t=g_t+e_t$，线性化中多出 $\langle e_t,w_t-u\rangle$，可由 $D\|e_t\|_*$ 控制。若 projection/prox 只近似满足最优性，还会出现每轮 variational-inequality residual $\varepsilon_t$。总 regret 加上这些 residual 的累计量；必须给可求和误差预算。

## E

### LT-OMD-E01
portfolio/routing 权重在 simplex，negative entropy 匹配非负与归一约束，update 是乘法形式并自然响应相对尺度。所有可能重新启用的坐标初始应给正质量；为数值稳定可设 floor、在 log-weight 域计算，再说明 floor 引入的 comparator 限制。

### LT-OMD-E02
深网 loss 非凸，convex linearization inequality 通常不成立；parameter domain 常无有界 diameter，gradient 也未必有统一 bound，投影步骤通常缺失。因此 OCO convex regret 不能直接推出训练到全局最优；最多把 optimizer 视为启发式，或另证局部/非凸 stationarity guarantee。

### LT-OMD-E03
claim card 应列：闭凸 domain 与 diameter；loss convexity；chosen norm/dual norm；mirror map 与 strong-convexity 常数；gradient/oracle bound；projection/prox 精度；step schedule 与 horizon；static comparator；adversary 和概率量词。
