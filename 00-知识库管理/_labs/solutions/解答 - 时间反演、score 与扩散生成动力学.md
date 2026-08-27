---
type: solution
status: draft
area: [math/stochastic-processes, math/sde, ai/generative-modeling]
topic: "时间反演、score 与扩散生成动力学"
exercise: "[[习题 - 时间反演、score 与扩散生成动力学]]"
related: ["[[时间反演、score 与扩散生成动力学]]", "[[实验 - 反向时间、score恒等式与扩散采样误差审计]]", "[[练习与测验 MOC]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 时间反演、score 与扩散生成动力学

> [!warning] 使用边界
> 本页用于完成首次独立作答后的核对。只阅读推导不构成掌握证据。每题解答重新声明关键对象和条件，避免离开题目后只剩公式。

## A 组解答

### DYN-REV-A01

#### 1. 使用正常递增的反向时钟

定义

$$
Y_s=X_{T-s},
\qquad 0\le s\le T.
$$

记物理时刻

$$
t=T-s.
$$

题设 diffusion matrix 是

$$
D(t)=g(t)^2I,
$$

不依赖空间。若 $p_t$ 正且足够光滑，并满足反向 diffusion 定理的其余条件，则

$$
dY_s
=\left[
-f(T-s,Y_s)
+g(T-s)^2\nabla_y\log p_{T-s}(Y_s)
\right]ds
+g(T-s)d\bar W_s.
$$

这里 $\bar W_s$ 是相对于反向 filtration 的 Brownian motion。

#### 2. 保留物理时间的 decreasing-$t$ 写法

同一个过程常被写成

$$
dX_t
=\left[
f(t,X_t)-g(t)^2\nabla_x\log p_t(X_t)
\right]dt
+g(t)d\bar W_t,
$$

但必须同时声明积分方向是

$$
t:T\longrightarrow0,
\qquad dt<0.
$$

检查 drift：令 $dt=-ds$，则

$$
[f-g^2s_t]dt
=[-f+g^2s_t]ds,
$$

正好恢复 forward-$s$ 形式。

#### 3. Brownian motion 不是普通可逆轨迹

前向 SDE 的 stochastic integral 要求 integrand 相对于 forward filtration adapted。倒序后的增量会包含从原前向视角看属于“未来”的信息，不能沿用原 adaptedness。

反向 Brownian motion 的定义依赖反向 filtration；它的 increments 在新的时间方向上具有独立、Gaussian、方差等于时间长度等性质。将一个已生成数组倒序可以构造某种路径 coupling，但不能替代 time-reversal theorem 或 filtration 证明。

#### 4. SDE 与 PF ODE 的系数

反向 SDE：

$$
b_{\rm rev}=-f+g^2s_t,
$$

并保留 $g\,d\bar W$。

反向 probability-flow ODE：

$$
b_{\rm PF,rev}=-f+\frac12g^2s_t,
$$

且没有随机项。

系数差来自二阶 diffusion current 是否仍存在，不是记号偏好。

---

### DYN-REV-A02

#### 1. Integrating factor

SDE 为

$$
dX_t=-\frac\beta2X_tdt+\sqrt\beta dW_t.
$$

取

$$
M_t=e^{\beta t/2}.
$$

$M_t$ 是确定性有限变差函数，因此

$$
d[M,X]_t=0.
$$

Itô product rule：

$$
d(M_tX_t)
=M_tdX_t+X_tdM_t.
$$

代入

$$
dM_t=\frac\beta2M_tdt
$$

得

$$
d(M_tX_t)
=M_t\sqrt\beta dW_t.
$$

积分：

$$
M_tX_t
=X_0+\sqrt\beta\int_0^t e^{\beta r/2}dW_r.
$$

故

$$
\boxed{
X_t=e^{-\beta t/2}X_0
+\sqrt\beta\int_0^t e^{-\beta(t-r)/2}dW_r.
}
$$

#### 2. Conditional law

随机积分条件于 $X_0$ 是零均值 Gaussian，方差

$$
\beta\int_0^t e^{-\beta(t-r)}dr
=1-e^{-\beta t}.
$$

因此

$$
\boxed{
X_t\mid X_0=x_0
\sim
\mathcal N(e^{-\beta t/2}x_0,1-e^{-\beta t}).
}
$$

#### 3. Unconditional moments

由 total expectation：

$$
m_t=e^{-\beta t/2}m_0.
$$

由独立随机积分：

$$
v_t=e^{-\beta t}v_0+1-e^{-\beta t}
=1+(v_0-1)e^{-\beta t}.
$$

#### 4. “Variance preserving”的准确含义

若 $m_0=0,v_0=1$，则

$$
m_t=0,
\qquad v_t=1
$$

对所有 $t$ 成立，标准 Gaussian 是 stationary law。

若 $v_0\ne1$，方差并非严格保持原值，而是趋向1。有限 $T$ 时

$$
m_T=e^{-\beta T/2}m_0,
\qquad
v_T=1+(v_0-1)e^{-\beta T},
$$

通常仍不等于 $(0,1)$。只有 $T\to\infty$，或数据一开始就是标准 Gaussian，才精确得到 $\mathcal N(0,1)$。

---

### DYN-REV-A03

#### 1. Noisy marginal 与 score

线性 Gaussian 组合给出

$$
X_t\sim\mathcal N(m_t,v_t),
$$

其中

$$
m_t=\alpha m_0,
\qquad
v_t=\alpha^2v_0+\sigma^2.
$$

因此

$$
\boxed{
s_t(x)=\frac d{dx}\log p_t(x)
=-\frac{x-\alpha m_0}{\alpha^2v_0+\sigma^2}.
}
$$

#### 2. Gaussian conditioning

联合 moments：

$$
\mathbb E[X_0]=m_0,
\qquad
\mathbb E[X_t]=\alpha m_0,
$$

$$
\operatorname{Cov}(X_0,X_t)=\alpha v_0,
\qquad
\operatorname{Var}(X_t)=v_t.
$$

Gaussian conditioning formula：

$$
\boxed{
\mathbb E[X_0\mid X_t=x]
=m_0+\frac{\alpha v_0}{v_t}(x-\alpha m_0).
}
$$

等价写成

$$
\mathbb E[X_0\mid X_t=x]
=\frac{\alpha v_0x+\sigma^2m_0}{v_t}.
$$

#### 3. Tweedie 核对

Tweedie 公式：

$$
\frac{x+\sigma^2s_t(x)}{\alpha}.
$$

代入 score：

$$
\frac1\alpha
\left[
x-\sigma^2\frac{x-\alpha m_0}{v_t}
\right]
$$

$$
=\frac1\alpha
\frac{x(v_t-\sigma^2)+\sigma^2\alpha m_0}{v_t}.
$$

因为

$$
v_t-\sigma^2=\alpha^2v_0,
$$

所以

$$
=\frac{\alpha v_0x+\sigma^2m_0}{v_t},
$$

与 Gaussian conditioning 完全一致。

#### 4. 三个估计对象

- posterior mean：最小化条件平方误差；
- posterior MAP：最大化 $p(x_0\mid x_t)$；
- nearest clean sample：依赖有限训练集和选定距离。

Gaussian posterior 中 mean=mode，但一般多峰 posterior 中不相等；nearest training sample 更是经验数据结构，不是 population posterior 的定义。

## B 组解答

### DYN-REV-B01

#### 1. Reverse density 的守恒律

前向 FPE：

$$
\partial_t p_t=-\nabla\cdot J_t.
$$

定义

$$
q_s(x)=p_{T-s}(x).
$$

链式法则给

$$
\partial_sq_s
=-\partial_tp_t\big|_{t=T-s}
=\nabla\cdot J_{T-s}.
$$

要写成 $s$ 方向的守恒律

$$
\partial_sq_s=-\nabla\cdot J_{\rm rev,s},
$$

必须取

$$
\boxed{J_{\rm rev,s}=-J_{T-s}.}
$$

#### 2. 配平 reverse drift

若 reverse process 保持相同 diffusion matrix $D$，其 current 是

$$
J_{\rm rev}
=b_{\rm rev}p-\frac12\nabla\cdot(Dp).
$$

而

$$
-J=-fp+\frac12\nabla\cdot(Dp).
$$

令二者相等：

$$
b_{\rm rev}p-\frac12\nabla\cdot(Dp)
=-fp+\frac12\nabla\cdot(Dp).
$$

移项并除以 $p>0$：

$$
\boxed{
b_{\rm rev}
=-f+\frac1p\nabla\cdot(Dp).
}
$$

#### 3. 展开乘积

第 $i$ 个分量：

$$
\frac1p\sum_j\partial_j(D_{ij}p)
=\sum_j\partial_jD_{ij}
+\sum_jD_{ij}\partial_j\log p.
$$

因此

$$
\boxed{
b_{\rm rev}
=-f+\nabla\cdot D+D\nabla\log p.
}
$$

#### 4. 一维例子

一维中

$$
D(x)=1+x^2,
\qquad D'(x)=2x.
$$

$f=0$，故

$$
\boxed{
b_{\rm rev}(t,x)
=2x+(1+x^2)\partial_x\log p_t(x).
}
$$

若错误套用 $Dscore$，会漏掉 $2x$。

#### 5. 层级边界

current 配平只得到候选过程的 marginal FPE。要升级为完整 time reversal，还需：

- PDE 解唯一，才能从同一 initial density 推出同一 marginal；
- backward transition kernel 满足 Bayes reversal；
- 反向 filtration 与 Brownian representation 存在；
- coefficients、density、nonexplosion 与 boundary 满足定理条件；
- path-space finite-dimensional distributions 一致。

所以 formal current identity 是必要机制，但不是所有层级的完整证明。

---

### DYN-REV-B02

#### 1. 展开 Fisher divergence

记真实 score

$$
s_p=\nabla\log p.
$$

则

$$
\frac12\mathbb E_p\|s_\theta-s_p\|^2
=\frac12\mathbb E_p\|s_\theta\|^2
-\mathbb E_p[s_\theta^\top s_p]
+\frac12\mathbb E_p\|s_p\|^2.
$$

最后一项与 $\theta$ 无关，记为 $C_p$。

交叉项：

$$
\mathbb E_p[s_\theta^\top s_p]
=\int_\Omega s_\theta(x)^\top\nabla p(x)dx.
$$

#### 2. Boundary term

散度恒等式：

$$
\nabla\cdot(ps_\theta)
=s_\theta^\top\nabla p+p\nabla\cdot s_\theta.
$$

积分并用 divergence theorem：

$$
\int_\Omega s_\theta^\top\nabla p,dx
=\int_{\partial\Omega}p,s_\theta^\top n,dS
-\int_\Omega p\nabla\cdot s_\theta,dx.
$$

若

$$
\int_{\partial\Omega}p,s_\theta^\top n,dS=0,
$$

则

$$
-\mathbb E_p[s_\theta^\top s_p]
=\mathbb E_p[\nabla\cdot s_\theta].
$$

故

$$
\boxed{
\mathcal J_F(\theta)
=\mathbb E_p\left[
\frac12\|s_\theta\|^2+\nabla\cdot s_\theta
\right]+C_p.
}
$$

#### 3. Boundary 不消失的例子

取 $\Omega=[0,1]$，$p(x)=1$，$s_\theta(x)=x$。一维 outward normals 在0和1分别为 $-1,+1$：

$$
\int_{\partial\Omega}psn
=p(1)s(1)-p(0)s(0)=1.
$$

所以不能删掉 boundary term。若想使用无边界形式，必须改用满足 $ps\cdot n=0$ 的向量场、周期边界、适当加权 score matching，或保留边界校正。

#### 4. Empirical distribution 问题

经验分布

$$
\widehat p_n=\frac1n\sum_i\delta_{x_i}
$$

相对于 ambient Lebesgue 测度没有普通 density，$\log\widehat p_n$ 与其梯度也不是普通函数。直接写 $\nabla\log\widehat p_n$ 没有意义。

Gaussian corruption 将点质量卷积成光滑正密度，这是 denoising score matching 可以使用 conditional Gaussian target 的关键原因。

---

### DYN-REV-B03

#### 1. Conditional-to-marginal identity

边缘密度：

$$
p_t(x)=\int q_t(x\mid x_0)p_0(x_0)dx_0.
$$

假设允许将导数移入积分：

$$
\nabla p_t(x)
=\int \nabla_xq_t(x\mid x_0)p_0(x_0)dx_0.
$$

用

$$
\nabla q=q\nabla\log q
$$

得

$$
\nabla p_t(x)
=\int q_t(x\mid x_0)p_0(x_0)
\nabla_x\log q_t(x\mid x_0)dx_0.
$$

除以 $p_t(x)>0$：

$$
\nabla\log p_t(x)
=\int p(x_0\mid x)
\nabla_x\log q_t(x\mid x_0)dx_0.
$$

即

$$
\boxed{
\nabla\log p_t(x)
=\mathbb E[
\nabla_x\log q_t(X_t\mid X_0)
\mid X_t=x].
}
$$

#### 2. 平方损失最优解

令

$$
U=\nabla_{X_t}\log q_t(X_t\mid X_0),
\qquad
m(X_t)=\mathbb E[U\mid X_t].
$$

分解

$$
s(X_t)-U=[s(X_t)-m(X_t)]+[m(X_t)-U].
$$

平方并取期望，交叉项为

$$
\mathbb E[(s-m)^\top(m-U)]
=\mathbb E[(s-m)^\top\mathbb E[m-U\mid X_t]]=0.
$$

所以

$$
\mathbb E\|s-U\|^2
=\mathbb E\|s-m\|^2
+\mathbb E\|m-U\|^2.
$$

第二项与 $s$ 无关，唯一的 $L^2$ minimizer 是

$$
s^\star=m=\nabla\log p_t
$$

（按 almost-everywhere 意义）。

#### 3. Gaussian target

$$
q_t(x_t\mid x_0)
=\mathcal N(\alpha_tx_0,\sigma_t^2I).
$$

因此

$$
\nabla_{x_t}\log q_t
=-\frac{x_t-\alpha_tx_0}{\sigma_t^2}.
$$

用

$$
x_t-\alpha_tx_0=\sigma_t\varepsilon
$$

得

$$
\boxed{U=-\varepsilon/\sigma_t.}
$$

#### 4. Population 最优到实际网络的断点

至少包括：

1. finite sample estimation error；
2. network function class approximation error；
3. optimizer 未到 population/global minimizer；
4. time sampling 与 loss weighting 使某些区域误差很大；
5. finite precision、data preprocessing 或 augmentation mismatch；
6. train/deployment state distribution shift；
7. condition dropout/guidance extrapolation；
8. small-noise cutoff 使 $t<\varepsilon$ 未被训练。

## C 组解答

### DYN-REV-C01

#### 1. Forward law 的归纳

基例 $k=1$：

$$
\bar a_1=a_1,
\qquad
1-\bar a_1=\beta_1,
$$

题设单步核正是结论。

假设

$$
x_{k-1}mid x_0
\sim\mathcal N(\sqrt{\bar a_{k-1}}x_0,
(1-\bar a_{k-1})I).
$$

单步更新：

$$
x_k=\sqrt{a_k}x_{k-1}+\sqrt{\beta_k}z_k.
$$

条件均值：

$$
\mathbb E[x_k\mid x_0]
=\sqrt{a_k\bar a_{k-1}}x_0
=\sqrt{\bar a_k}x_0.
$$

条件方差：

$$
a_k(1-\bar a_{k-1})+\beta_k
=a_k-a_k\bar a_{k-1}+1-a_k
=1-\bar a_k.
$$

所以

$$
\boxed{
q(x_k\mid x_0)
=\mathcal N(\sqrt{\bar a_k}x_0,(1-\bar a_k)I).
}
$$

#### 2. Gaussian posterior

忽略与 $x_{k-1}$ 无关的项，negative log posterior 的两倍为

$$
\frac{\|x_k-\sqrt{a_k}x_{k-1}\|^2}{\beta_k}
+\frac{\|x_{k-1}-\sqrt{\bar a_{k-1}}x_0\|^2}
{1-\bar a_{k-1}}.
$$

二次系数：

$$
\Lambda_k
=\frac{a_k}{\beta_k}
+\frac1{1-\bar a_{k-1}}
=\frac{1-\bar a_k}{\beta_k(1-\bar a_{k-1})}.
$$

所以

$$
\widetilde\beta_k=\Lambda_k^{-1}
=\frac{1-\bar a_{k-1}}{1-\bar a_k}\beta_k.
$$

线性 precision-weighted 项是

$$
\frac{\sqrt{a_k}}{\beta_k}x_k
+\frac{\sqrt{\bar a_{k-1}}}{1-\bar a_{k-1}}x_0.
$$

乘 $\widetilde\beta_k$：

$$
\boxed{
\widetilde\mu_k
=\frac{\sqrt{a_k}(1-\bar a_{k-1})}{1-\bar a_k}x_k
+\frac{\sqrt{\bar a_{k-1}}\beta_k}{1-\bar a_k}x_0.
}
$$

#### 3. Noise parameterization

由 fixed-time noising：

$$
\widehat x_0
=\frac{x_k-\sqrt{1-\bar a_k}\varepsilon_\theta}{\sqrt{\bar a_k}}.
$$

代入 $\widetilde\mu_k$。$x_k$ 的系数化简为

$$
\frac1{\sqrt{a_k}},
$$

$\varepsilon_\theta$ 的系数化简为

$$
-\frac{\beta_k}{\sqrt{a_k}\sqrt{1-\bar a_k}}.
$$

故

$$
\boxed{
\mu_\theta(x_k,k)
=\frac1{\sqrt{a_k}}
\left[
x_k-\frac{\beta_k}{\sqrt{1-\bar a_k}}
\varepsilon_\theta(x_k,k)
\right].
}
$$

#### 4. Fixed-time 与 path

公式

$$
x_k=\sqrt{\bar a_k}x_0+\sqrt{1-\bar a_k}\varepsilon
$$

只给 $X_k\mid X_0$ 的一次条件抽样。完整 Markov path 还要求每一步独立 $z_j$，并由递推共享历史。

若每个 $k$ 都重新抽一个独立 $\varepsilon_k$，虽然每个固定时刻边缘正确，跨时 covariance 与 Markov transition 一般错误。

---

### DYN-REV-C02

#### 1. Score、noise 与 clean-data

conditional target：

$$
s_t^{\rm cond}
=-\frac{x_t-\alpha_tx_0}{\sigma_t^2}
=-\frac\varepsilon{\sigma_t}.
$$

因此模型换算：

$$
\boxed{s_\theta=-\varepsilon_\theta/\sigma_t,}
$$

$$
\boxed{
s_\theta=(\alpha_t\widehat x_{0,\theta}-x_t)/\sigma_t^2,
}
$$

以及

$$
\widehat x_{0,\theta}
=\frac{x_t+\sigma_t^2s_\theta}{\alpha_t},
$$

$$
\varepsilon_\theta=-\sigma_ts_\theta.
$$

#### 2. $v$ 的正交变换

定义

$$
v=\alpha_t\varepsilon-\sigma_tx_0.
$$

结合

$$
x_t=\alpha_tx_0+\sigma_t\varepsilon
$$

有

$$
\begin{bmatrix}x_t\\v\end{bmatrix}
=R_t
\begin{bmatrix}x_0\\\varepsilon\end{bmatrix},
\qquad
R_t=
\begin{bmatrix}
\alpha_t&\sigma_t\\
-\sigma_t&\alpha_t
\end{bmatrix}.
$$

因为 $\alpha_t^2+\sigma_t^2=1$，

$$
R_t^{-1}=R_t^\top.
$$

所以

$$
\boxed{x_0=\alpha_tx_t-\sigma_tv,}
$$

$$
\boxed{\varepsilon=\sigma_tx_t+\alpha_tv.}
$$

#### 3. Loss 权重转换

带权 score MSE：

$$
\lambda(t)\|s_\theta-s_t^{\rm cond}\|^2.
$$

noise parameterization 下：

$$
s_\theta-s_t^{\rm cond}
=-\frac{\varepsilon_\theta-\varepsilon}{\sigma_t},
$$

故

$$
\boxed{
\lambda(t)\|s_\theta-s_t^{\rm cond}\|^2
=\frac{\lambda(t)}{\sigma_t^2}
\|\varepsilon_\theta-\varepsilon\|^2.
}
$$

$x_0$ parameterization 下：

$$
s_\theta-s_t^{\rm cond}
=\frac{\alpha_t}{\sigma_t^2}
(\widehat x_{0,\theta}-x_0),
$$

所以

$$
\boxed{
\lambda(t)\|s_\theta-s_t^{\rm cond}\|^2
=\lambda(t)\frac{\alpha_t^2}{\sigma_t^4}
\|\widehat x_{0,\theta}-x_0\|^2.
}
$$

#### 4. Effective weighting

若 $t\sim\rho(t)$，某时刻对 population risk 的有效密度是

$$
\rho(t)
\times\lambda(t)
\times c_{\rm param}(t),
$$

其中 noise prediction 的

$$
c_{\rm param}=1/\sigma_t^2,
$$

$x_0$ prediction 的

$$
c_{\rm param}=\alpha_t^2/\sigma_t^4.
$$

因此只说“uniformly sample time”不能说明各 SNR 区域被等权训练。

---

### DYN-REV-C03

#### 1. Forward Gaussian law

constant-$\beta$ VP 给

$$
m_t=e^{-\beta t/2}m_0,
$$

$$
v_t=1+(v_0-1)e^{-\beta t}.
$$

故

$$
p_t=\mathcal N(m_t,v_t),
\qquad
s_t(x)=-\frac{x-m_t}{v_t}.
$$

#### 2. Reverse SDE

前向 drift 为

$$
f(t,x)=-\frac\beta2x,
$$

diffusion variance $D=\beta$。forward-$s$ reverse drift：

$$
b_{\rm rev}
=-f+Ds_t
=\frac\beta2x-\beta\frac{x-m_t}{v_t}.
$$

即

$$
\boxed{
b_{\rm rev}
=\beta\left(\frac12-\frac1{v_t}\right)x
+\beta\frac{m_t}{v_t},
\quad t=T-s.
}
$$

#### 3. Reverse PF ODE

$$
b_{\rm PF}
=-f+\frac D2s_t
=\frac\beta2x-\frac\beta2\frac{x-m_t}{v_t}.
$$

所以

$$
\boxed{
b_{\rm PF}
=\frac\beta2\left(1-\frac1{v_t}\right)x
+\frac\beta2\frac{m_t}{v_t}.
}
$$

#### 4. Moment evolution 核对

令 reverse SDE drift 为 $A_tx+c_t$：

$$
A_t=\beta(1/2-1/v_t),
\qquad c_t=\beta m_t/v_t.
$$

反向 SDE moments：

$$
\frac d{ds}\mu_s=A_t\mu_s+c_t,
$$

$$
\frac d{ds}V_s=2A_tV_s+\beta.
$$

若 $\mu_s=m_t,V_s=v_t$，则

$$
A_tm_t+c_t
=\beta(1/2-1/v_t)m_t+\beta m_t/v_t
=\frac\beta2m_t.
$$

另一方面

$$
\frac d{ds}m_{T-s}
=-\frac d{dt}m_t
=\frac\beta2m_t.
$$

方差：

$$
2A_tv_t+\beta
=2\beta(1/2-1/v_t)v_t+\beta
=\beta(v_t-1).
$$

而

$$
\frac d{ds}v_{T-s}
=-\frac d{dt}v_t
=\beta(v_t-1).
$$

完全一致。

PF ODE 中

$$
A_t^{\rm PF}=\frac\beta2(1-1/v_t),
\qquad
c_t^{\rm PF}=\frac\beta2m_t/v_t.
$$

其 mean：

$$
A_t^{\rm PF}m_t+c_t^{\rm PF}=\frac\beta2m_t.
$$

确定性线性 flow 的 variance：

$$
\frac d{ds}V_s=2A_t^{\rm PF}V_s.
$$

代入 $V_s=v_t$：

$$
2A_t^{\rm PF}v_t
=\beta(v_t-1),
$$

也正确。

#### 5. 半系数放进 noisy SDE

若漂移错误地使用 $b_{\rm PF}$，但仍保留 $\sqrt\beta d\bar W$，variance ODE 变成

$$
\frac d{ds}V_s
=2A_t^{\rm PF}V_s+\beta.
$$

在目标 $V_s=v_t$ 上右端为

$$
\beta(v_t-1)+\beta=\beta v_t,
$$

但正确目标导数是 $\beta(v_t-1)$，相差常数 $\beta$。

这是 continuous-model coefficient error；$h\to0$ 只会更精确地求出错误方程，不能恢复目标 law。

## D 组解答

### DYN-REV-D01

#### 1. 两个 joint distribution

Forward variational chain：

$$
q(x_{1:K}\mid x_0)
=\prod_{k=1}^Kq(x_k\mid x_{k-1}).
$$

Generative reverse model：

$$
p_\theta(x_{0:K})
=p(x_K)\prod_{k=1}^Kp_\theta(x_{k-1}\mid x_k).
$$

#### 2. ELBO 分解

从 importance/Jensen：

$$
\log p_\theta(x_0)
=\log\int q(x_{1:K}\mid x_0)
\frac{p_\theta(x_{0:K})}{q(x_{1:K}\mid x_0)}dx_{1:K}
$$

$$
\ge
\mathbb E_q\left[
\log p_\theta(x_{0:K})
-\log q(x_{1:K}\mid x_0)
\right].
$$

使用 forward posterior factorization 重排，可得 NLL upper bound：

$$
-\log p_\theta(x_0)
\le L_T+\sum_{k=2}^KL_{k-1}+L_0,
$$

其中

$$
L_T=\operatorname{KL}(q(x_K\mid x_0)\|p(x_K)),
$$

$$
L_{k-1}
=\mathbb E_q\operatorname{KL}
\left(q(x_{k-1}\mid x_k,x_0)
\|p_\theta(x_{k-1}\mid x_k)\right),
$$

$$
L_0=-\mathbb E_q\log p_\theta(x_0\mid x_1).
$$

#### 3. Gaussian KL 到 noise MSE

若两边 covariance 固定且 isotropic，

$$
\operatorname{KL}
(\mathcal N(\widetilde\mu,\widetilde\beta I)
\|\mathcal N(\mu_\theta,\sigma_k^2I))
$$

中与 $\theta$ 相关的部分为

$$
\frac1{2\sigma_k^2}
\|\widetilde\mu-\mu_\theta\|^2.
$$

$\widetilde\mu$ 与 $\mu_\theta$ 都可写成相同 $x_k$ 项加上 noise target/prediction 项，因此

$$
L_{k-1}
=w_k\mathbb E\|\varepsilon-\varepsilon_\theta(x_k,k)\|^2+C_k.
$$

$w_k$ 由 $\beta_k,\bar a_k$ 和 chosen reverse variance 决定。

#### 4. Simplified loss

$$
\mathcal L_{\rm simple}
=\mathbb E\|\varepsilon-\varepsilon_\theta\|^2
$$

把时刻相关 $w_k$ 改为常数。它共享相同的逐时 population noise regression target，但改变不同噪声时刻的相对权重，因此一般不等于原 ELBO，也不能直接把其数值解释为 NLL bound。

#### 5. 四种 sampler

| sampler | 随机性 | 直接近似对象 | path-law 说明 | 主要数值误差 |
|---|---:|---|---|---|
| DDPM ancestral | 有 | discrete learned reverse Markov kernels | Markov stochastic path | kernel/step schedule |
| reverse-SDE EM | 有 | continuous reverse SDE | diffusion path，非PF path | strong/weak EM error |
| DDIM $\eta=0$ | 无 | deterministic implicit path | 与DDPM共享训练结构但不同 path | skipped grid/model error |
| PF ODE | 无 | continuous probability-flow ODE | exact score时共享 marginals，非path | ODE truncation/tolerance |

只用“都从 noise 生成 data”不能把四者视为同一算法。

---

### DYN-REV-D02

#### 1. Noisy mixture

令 component label $K\in\{-1,+1\}$，先验各为 $1/2$，且

$$
X_0\mid K=k\sim\mathcal N(km,\tau^2).
$$

条件于 $K=k$：

$$
X_t\mid K=k
\sim\mathcal N(\alpha km,V),
$$

其中

$$
V=\alpha^2\tau^2+\sigma^2.
$$

因此

$$
\boxed{
p_t(x)
=\frac12\phi(x;-\alpha m,V)
+\frac12\phi(x;\alpha m,V).
}
$$

#### 2. Mixture score

定义 responsibilities

$$
r_k(x)
=\frac{\phi(x;\alpha km,V)}
{\phi(x;-\alpha m,V)+\phi(x;\alpha m,V)}.
$$

component score：

$$
s_k(x)=-\frac{x-\alpha km}{V}.
$$

mixture derivative 除以 mixture density 得

$$
\boxed{
s_t(x)=\sum_{k\in\{-1,+1\}}r_k(x)s_k(x).
}
$$

也可写为

$$
s_t(x)
=-\frac{x-\alpha m[r_{+}(x)-r_{-}(x)]}{V}.
$$

#### 3. Posterior denoiser

固定 component 后，Gaussian conditioning：

$$
\mathbb E[X_0\mid X_t=x,K=k]
=km+\frac{\alpha\tau^2}{V}(x-\alpha km).
$$

因此

$$
\boxed{
\mathbb E[X_0\mid X_t=x]
=\sum_kr_k(x)
\left[
km+\frac{\alpha\tau^2}{V}(x-\alpha km)
\right].
}
$$

#### 4. Tweedie 核验

条件 score identity 给

$$
s_t(x)
=\mathbb E\left[-\frac{x-\alpha X_0}{\sigma^2}\mid X_t=x\right].
$$

整理：

$$
\boxed{
\mathbb E[X_0\mid X_t=x]
=\frac{x+\sigma^2s_t(x)}{\alpha}.
}
$$

将上一节的 responsibility score 代入，可以逐项化到 Gaussian conditioning 结果。

#### 5. 对称中心的对象分离

在 $x=0$：

$$
r_+(0)=r_-(0)=1/2.
$$

两个 component posterior means 互为相反数，因此总体 posterior mean 为0，score 也为0。

但当 modes 分离充分时，posterior density 仍可能有两个 component peaks；component/MAP 决策可选正或负 mode。posterior mean 位于两者中间，不代表那里有高 clean-data density。

若 sampler 或 denoiser 总输出均值，可能表现为 mode averaging；生成的 stochastic reverse process则还利用噪声选择不同 mode。coverage 不能只由 posterior mean 曲线判断。

---

### DYN-REV-D03

下面给出与配套脚本一致的受控设计。

#### 1. Exact-score solver axis

选择一维 constant-$\beta$ VP，数据

$$
X_0\sim\mathcal N(m_0,v_0).
$$

其 $m_t,v_t,s_t$ 全有闭式。生成从精确 $p_T$ 开始，使用精确 score，分别求 reverse SDE EM 和 PF Euler。

refinement：

$$
N=16,32,64,128,256,512,
\qquad h=T/N.
$$

指标可用 terminal mean/variance 联合误差：

$$
E_h=\sqrt{(\widehat m_0-m_0)^2+(\widehat v_0-v_0)^2}.
$$

为消除 Monte Carlo 噪声，直接使用线性 Euler moment recursion。预期 exact-score error 约按 $O(h)$ 消失。

#### 2. Score-bias axis

固定很细的 $N$，将

$$
\widehat s_t=(1+\epsilon)s_t,
\qquad \epsilon\in\{-0.1,0.1\}
$$

用于 reverse dynamics。继续 refinement；若曲线趋向非零地板，这就是 continuous model bias，而非 step error。

#### 3. Terminal mismatch axis

保持 exact score 与细步长，但把启动 law 从精确

$$
p_T=\mathcal N(m_T,v_T)
$$

替换为

$$
\pi=\mathcal N(0,1).
$$

测 terminal moment error。再改变 $T$ 或 total noise，验证 mismatch 是否随 $p_T\to\pi$ 下降。

#### 4. Coefficient error axis

在 noisy reverse SDE 中错误用

$$
-f+\frac12D\widehat s
$$

而保留 diffusion。做 $h\to0$；误差应稳定在明显非零水平，证明这是错误 continuous generator。

#### 5. 额外指标

除 moments 外可报告：

- Wasserstein-2（Gaussian 时有闭式）；
- KL divergence；
- empirical coverage/quantile error；
- runtime/NFE；
- reverse SDE quadratic variation。

#### 6. 不能外推

一维 Gaussian 结果不能证明：

- 高维多峰数据上的 sampler 排名；
- 任意 learned score 的误差传播界；
- PF ODE 总优于或劣于 reverse SDE；
- 某阶 observed slope 对所有 schedule/solver 成立；
- FID、感知质量或条件一致性结论。

## E 组解答

### DYN-REV-E01

原报告把七层证据压成了一句话。

#### 1. Formal PDE identity

需要检查：

- FPE 符号；
- 一般 $D(x,t)$ 的 $\nabla\cdot D$；
- boundary current；
- score 存在性；
- 导数与积分是否合法。

通过只说明候选密度形式上满足方程。

#### 2. Marginal PDE uniqueness

即使同一 $q_s=p_{T-s}$ 满足候选 FPE，还需该 initial-boundary-value problem 在所选解类中唯一，才能断言 SDE 的 marginals 必为 $q_s$。

还需证明候选 SDE 存在、nonexplosive，且其 law 确实满足该 FPE。

#### 3. Transition reversal

真正 backward kernel 应满足

$$
r_{s+h\mid s}(y\mid x)
=\frac{q_{t\mid t-h}(x\mid y)p_{t-h}(y)}{p_t(x)}.
$$

PDE marginal 一致不唯一决定 transition kernel。需验证 Markov kernel/Bayes 关系。

#### 4. Path-law reversal

需证明所有 finite-dimensional distributions 与倒序原过程一致，并建立反向 filtration 下的 semimartingale/Brownian representation。只比较每时刻 histogram 不够。

#### 5. Learned score

实际 $s_\theta$ 通常不等于 $\nabla\log p_t$。应报告某个加权范数、分区域误差、训练/部署 distribution shift，或可证明的 approximation bound。

用 learned score 得到的是 approximate reverse model，不是 exact time reversal。

#### 6. Finite-step implementation

需报告 solver、grid/tolerance、NFE、stochastic increments、Brownian coupling、final denoising和 refinement。连续模型 theorem 不覆盖有限步输出。

#### 7. 退化、边界与奇异端点

- degenerate $D$：密度可能不光滑，普通反向公式条件失效；
- bounded domain：reflecting/absorbing boundary 会改变 time reversal；
- manifold/empirical data：$p_0$ ambient score 不存在；
- $t\downarrow0$：score 可能发散；
- $p=0$ 区域：$p^{-1}\nabla\cdot(Dp)$ 无定义。

最终可接受的 claim 应分成：formal derivation、exact theorem under assumptions、learned continuous approximation、finite numerical evidence四层。

---

### DYN-REV-E02

#### 1. Conditional score

Bayes：

$$
p_t(x\mid y)=\frac{p_t(y\mid x)p_t(x)}{p_t(y)}.
$$

取 log 并对 $x$ 求梯度：

$$
\boxed{
s_c(x,t)
=s_u(x,t)+\nabla_x\log p_t(y\mid x).
}
$$

#### 2. Classifier guidance density

使用

$$
s_\gamma=s_u+\gamma\nabla\log p_t(y\mid x).
$$

则

$$
s_\gamma
=\nabla_x\left[
\log p_t(x)+\gamma\log p_t(y\mid x)
\right].
$$

对应 fixed-time unnormalized density

$$
\boxed{
\widetilde p_{t,\gamma}(x\mid y)
\propto p_t(x)p_t(y\mid x)^\gamma.
}
$$

$\gamma=1$ 时才恢复原条件 density。

#### 3. CFG density

$$
s_{\rm cfg}
=s_u+w(s_c-s_u)
=(1-w)s_u+ws_c.
$$

若两支都是精确 gradient：

$$
s_{\rm cfg}
=\nabla_x\left[(1-w)\log p_t(x)+w\log p_t(x\mid y)\right].
$$

故

$$
\widetilde p_{t,w}(x\mid y)
\propto p_t(x)^{1-w}p_t(x\mid y)^w.
$$

用 Bayes 还可写成

$$
\boxed{
\widetilde p_{t,w}(x\mid y)
\propto p_t(x)p_t(y\mid x)^w.
}
$$

#### 4. 为什么 $w>1$ 不是更精确

原 conditional score 是 $w=1$。$w>1$ 对 likelihood factor 做 tempering/extrapolation，改变目标 density；它可提高 on-condition concentration，却可能降低 diversity/coverage，并放大两支网络误差。

而且逐时 tempered densities 是否由一个 globally consistent forward/reverse process连接，还需要额外检查，不能只看固定时刻 gradient。

#### 5. 评估协议

至少扫描多个 $w$ 和 seeds，同时报告：

- 条件一致性：独立 classifier、人评或任务指标；
- fidelity：感知质量或 precision；
- coverage/diversity：recall、class coverage、pairwise diversity；
- distribution metric：FID/KID及置信区间；
- solver/NFE 相同的公平比较；
- unconditional/conditional $w=0,1$ 基线；
- classifier-free 两分支误差与 condition dropout 设定。

不应只选择使某个 classifier score 最大的 $w$ 再宣称分布整体更准确。

---

### DYN-REV-E03

下面给出一个完整示例研究卡；其他系统可沿同一字段改写。

#### 1. 研究对象

- 数据：一维 symmetric Gaussian mixture
  $$
  p_0=\tfrac12\mathcal N(-2,0.16)+\tfrac12\mathcal N(2,0.16);
  $$
- state：$x\in\mathbb R$；
- preprocessing：不裁剪、不归一化，直接使用上述单位；
- support：whole space，所有 $t>0$ density 正且光滑。

#### 2. Forward process

constant-$\beta$ VP：

$$
dX_t=-\frac\beta2X_tdt+\sqrt\beta dW_t,
\quad \beta=2,
\quad T=2.
$$

$$
X_t=e^{-t}X_0+\sqrt{1-e^{-2t}}\varepsilon.
$$

mixture noisy density、score 与 posterior denoiser均有闭式。

#### 3. Terminal prior

chosen prior：

$$
\pi=\mathcal N(0,1).
$$

先计算精确 $p_T$ 与 $\pi$ 的 mean/variance、KL numerical quadrature 和 Wasserstein proxy；分别从 $p_T$ 与 $\pi$ 启动，以隔离 terminal mismatch。

#### 4. Parameterization

网络输出 noise $\varepsilon_\theta$；部署转换：

$$
s_\theta=-\varepsilon_\theta/\sigma_t.
$$

单元测试在随机 $(x,t)$ 上比较 noise、score、$x_0$ 三种 conversion 的 algebraic identity。

#### 5. Training

- $t\sim\operatorname{Uniform}[10^{-3},T]$；
- unweighted noise MSE；
- 明确其等价 score weight 为 $\sigma_t^2$；
- small-noise cutoff $10^{-3}$；
- 报告每个 log-SNR bin 的 held-out noise/score error，而非只给总 loss。

#### 6. Reverse dynamics

两条部署：

1. reverse SDE：完整 $g^2s_\theta$；
2. reverse PF ODE：$g^2s_\theta/2$。

统一 time grid，分别扫描 NFE；reverse SDE 使用可嵌套 Brownian increments，PF 使用 Euler/Heun 对照。

#### 7. Conditioning

本基线无 condition/guidance。若扩展到 component label，先做 $w=1$ 的 exact conditional score 基线，再扫描 CFG，避免把 guidance 与基础反演混在一起。

#### 8. 六类误差

| 误差 | 隔离方法 |
|---|---|
| terminal | exact $p_T$ vs $\pi$ 启动 |
| score | analytic score vs learned score |
| solver | analytic score下做步长 refinement |
| MC | 多seed与置信区间；Gaussian moment可用解析递推 |
| parameterization | pointwise conversion unit test |
| evaluation | exact density/Wasserstein/KL 与 finite histogram对照 |

#### 9. Exact baseline

- mixture $p_t$ closed form；
- exact score；
- Tweedie denoiser；
- fine-grid reference sampler；
- 每个时刻的 exact mean、variance、mode weights。

#### 10. Falsification experiments

1. 在 reverse SDE 中故意把 score coefficient 从1改为1/2，检验 refinement 是否收敛到错误 law；
2. 让 network score 在 $t<0.1$ 乘 $1.1$，检验 endpoint-localized error 是否造成 mode/variance偏差；
3. 每个时刻独立抽 fixed-time noise，检验边缘正确但 path metric/QV错误。

#### 11. 禁止外推

不能由该实验声称：

1. reverse SDE 在所有图像模型上优于 PF ODE；
2. Gaussian mixture 的一阶 solver slope 对高维 stiff sampler不变；
3. analytic score下的成功证明 learned neural score已恢复真实数据分布。

## 解答使用后的升级动作

1. 将自己的答案与本页逐条比对；
2. 标记错误属于时钟、对象、条件、代数、数值还是研究外推；
3. 独立复做至少一题 B、一题 C 和一题 E；
4. 运行并改参[[实验 - 反向时间、score恒等式与扩散采样误差审计]]；
5. 48小时后闭卷重做错题，14天后用不同 forward schedule 迁移。

完成以上证据前，DYN-12 仍保持 `draft`。
