---
type: solution-set
status: draft
area: [math/calculus, math/matrix-calculus, math/matrix-analysis]
aliases: [谱分解导数习题解答, 可微 SVD 习题解答]
prerequisites: ["[[习题 - 特征值、特征向量与 SVD 的导数]]"]
related: ["[[特征值、特征向量与 SVD 的导数]]", "[[练习与测验 MOC]]"]
sources: ["[[S-2025-Su-10878-SVD的导数]]", "Davis-Kahan-1970", "Wedin-1972", "Townsend-2016-SVD-Derivative"]
created: 2026-08-18
updated: 2026-08-18
---

# 解答 - 特征值、特征向量与 SVD 的导数

## A. 基本概念

### A1 解

排序固定且与其余谱分离的简单特征值局部是唯一标量分支；标准化特征向量仍有符号/相位自由度，需选连续规范；重复谱簇内部的基可任意正交旋转，只有与外部谱分离的子空间及投影是基不变对象。$u$ 与 $-u$ 表示同一子空间却相距 $2$，所以应比较 $uu^\top$ 或主角。

### A2 解

微分单位约束：

$$
0=d(u^\top u)=2u^\top du.
$$

若允许随 $t$ 任意翻转符号或乘相位，同一矩阵可对应不连续输出，差商没有唯一极限。实数值规则可在相邻点令 $u(t)^\top u(0)>0$；复数可乘相位使该内积为非负实数。重谱时需整体 Procrustes 对齐或直接比较投影。

### A3 解

$u_1=e_1$、$\lambda_1=2$。由公式

$$
D\lambda_1[E]=E_{11}=0,
\qquad
Du_1[E]=e_2/\delta.
$$

三种 gap 下方向导数范数分别为 $1,10^2,10^6$。谱值一阶不变并不保证方向稳定。

## B. 对称与一般特征问题

### B1 解

微分特征方程：

$$
Eu_i+Adu_i=d\lambda_i u_i+\lambda_i du_i.
$$

对称性给 $u_i^\top A=\lambda_i u_i^\top$，左乘 $u_i^\top$ 后抵消得到 $d\lambda_i=u_i^\top Eu_i$。单位规范给 $u_i^\top du_i=0$。左乘 $u_j^\top$：

$$
u_j^\top Eu_i+\lambda_j u_j^\top du_i
=\lambda_i u_j^\top du_i,
$$

故系数为 $(u_j^\top Eu_i)/(\lambda_i-\lambda_j)$。简单性保证分母非零，正交基展开给最终求和式。

### B2 解

$$
DP_i[E]=Du_i[E]u_i^\top+u_iDu_i[E]^\top.
$$

代入 B1：

$$
DP_i[E]=\sum_{j\ne i}
\frac{u_ju_j^\top Eu_i u_i^\top+u_iu_i^\top Eu_j u_j^\top}
{\lambda_i-\lambda_j}.
$$

$u_i\mapsto-u_i$ 时每项出现两次负号，结果不变。若 $\gamma=\min_{j\ne i}|\lambda_i-\lambda_j|$，可由约化 resolvent 或求和粗略得 $\|DP_i[E]\|_2\le2\|E\|_2/\gamma$；精确常数依赖采用的范数和表示。

### B3 解

微分 $Av=\lambda v$ 并左乘 $w^*$：

$$
w^*Ev+w^*A,dv=d\lambda,w^*v+\lambda w^*dv.
$$

$w^*A=\lambda w^*$ 使后两项抵消，故 $d\lambda=w^*Ev/(w^*v)$。$A_\varepsilon$ 的右/左特征向量随 $1/\varepsilon$ 变得几乎线性相关/近正交，特征向量矩阵条件数发散；因此存在单位范数 $E$ 使 $|D\lambda[E]|$ 按 $1/\varepsilon$ 放大。特征值 gap 为 $1$ 只排除了碰撞，不能控制非正规条件数。

## C. 重谱与 SVD

### C1 解

$$
\lambda_{\max}(tE)=t\lambda_{\max}(E)\quad(t\ge0),
$$

故右方向导数为 $\lambda_{\max}(E)$。取

$$
E_1=\operatorname{diag}(1,0),\quad E_2=\operatorname{diag}(0,1).
$$

各方向导数都为 $1$，但 $E_1+E_2=I$ 的方向导数仍为 $1$，不等于 $2$。Fréchet 导数必须关于 $E$ 线性，所以不存在。

### C2 解

微分 $Av_i=\sigma_i u_i$，左乘 $u_i^\top$；利用 $u_i^\top A=\sigma_i v_i^\top$ 与两个单位约束，得到 $d\sigma_i=u_i^\top Ev_i$。于是

$$
dF=\sum_i\phi'(\sigma_i)u_i^\top dA v_i
=\left\langle U\operatorname{Diag}(\phi'(\sigma_i))V^\top,dA\right\rangle_F,
$$

所以梯度即盒中矩阵；在重值/零值处还需 $F$ 的对称组合本身可微。

### C3 解

反对称性给 $(\Omega_U)_{ji}=-\alpha$、$(\Omega_V)_{ji}=-\beta$。取 $(i,j)$ 与 $(j,i)$ 元素：

$$
\begin{bmatrix}\sigma_j&-\sigma_i\\-\sigma_i&\sigma_j\end{bmatrix}
\begin{bmatrix}\alpha\\\beta\end{bmatrix}
=\begin{bmatrix}P_{ij}\\P_{ji}\end{bmatrix}.
$$

行列式为 $\sigma_j^2-\sigma_i^2$，故

$$
\alpha=\frac{\sigma_jP_{ij}+\sigma_iP_{ji}}{\sigma_j^2-\sigma_i^2},
\quad
\beta=\frac{\sigma_iP_{ij}+\sigma_jP_{ji}}{\sigma_j^2-\sigma_i^2}.
$$

相等奇异值时，分解允许同值子空间内联合旋转，$U,V$ 的逐列导数不是唯一函数；这不是单纯浮点除零，而是可识别对象改变。

## D. 实现与 AI 审计

### D1 解

构造 $C(\delta)=Q\operatorname{diag}(\lambda_1,\ldots,\lambda_r,\lambda_r-\delta,\ldots)Q^\top$，由 $X$ 或直接由 $C$ 求前 $r$ 维基 $U_r$ 和 $P=U_rU_r^\top$。随机对称方向 $E$，比较 $[P(C+hE)-P(C-hE)]/(2h)$ 与候选 JVP；内部随机旋转 $U_rR$ 后 $P$ 和损失应不变。扫描 $\delta,h$。诊断至少包括 eig residual、正交误差、投影差/主角、方向差分相对误差和 $\|DP[E]\|$ 对 $1/\delta$ 的缩放。

### D2 解

设 $s=\sigma_1(W)$，$ds=u_1^\top Ev_1$：

$$
\boxed{
D\widehat W[E]=\frac{E}{s}-\frac{W}{s^2}(u_1^\top Ev_1).
}
$$

有限幂迭代产生的是近似 $s_K,u_K,v_K$，展开反传会对迭代程序求导；stop-gradient 则有意删除某些状态路径；碰撞时 $s$ 虽仍 Lipschitz，却通常只有次梯度，简单公式失去唯一性。

### D3 解

$\|C^{-1/2}\|_2=\lambda_{\min}^{-1/2}$；标量函数 $x^{-1/2}$ 的导数尺度为 $\frac12x^{-3/2}$，所以前向与反向分别强烈放大小谱方向。hard clipping 把谱函数改成分段函数，在阈值处非光滑且阈值下梯度常被截断；$C+\varepsilon I$ 是平滑但改变全部特征值的 ridge/jitter 模型；截断子空间删除小谱方向并改变输出秩/空间，边界仍需 gap。三者不是同一个“稳定技巧”。

## E. 证明与边界

### E1 解

选基把空间分成 $\mathcal U\oplus\mathcal U^\perp$。在 $\mathcal U$ 内，$A$ 的主块为 $\lambda I_k$；一阶退化扰动理论要求先在该块内对角化 $U_0^\top EU_0$，其特征值 $\mu_j$ 给 $\lambda+t\mu_j+o(t)$。若换基 $U_0\mapsto U_0R$，压缩矩阵变为 $R^\top(U_0^\top EU_0)R$，特征值不变，所以分裂结果基不变。

### E2 解

若 $U_0$ 张成最大特征子空间：

$$
\partial\lambda_{\max}(A)
=\{U_0HU_0^\top:H\succeq0,\operatorname{tr}H=1\}.
$$

若 $U_1,V_1$ 对应重数 $k$ 的最大奇异值：

$$
\partial\|A\|_2
=\{U_1HV_1^\top:H\succeq0,\operatorname{tr}H=1\}.
$$

若 $A=U_r\Sigma_rV_r^\top$：

$$
\partial\|A\|_*
=\{U_rV_r^\top+W:U_r^\top W=0,WV_r=0,\|W\|_2\le1\}.
$$

次微分含多个元素时不存在唯一线性一阶近似；框架选一个元素只给算法约定，不使集合变成单点。

### E3 解

声明错误。即使训练样本没有精确重值，每列仍有符号/相位自由度；接近碰撞时导数按 gap 反比放大；排序可交换；有限精度可把近重值视为重值并返回任意基；分布外样本可能跨越碰撞集合。MLP 通常不对 $U_r\mapsto U_rR$ 不变，所以输出依赖分解算法规范。替代方案包括输入 $P=U_rU_r^\top$、重构 $U_r\Sigma_rU_r^\top$、谱值的对称函数，或使用明确设计的 Grassmann/子空间不变网络。

> [!success] 验收提示
> 若能在公式前主动声明 simple/gap/gauge，并在重值时把逐列向量替换成投影、子空间或次梯度，才算跨过“会对 SVD 公式求微分”到“理解可微谱层”的门槛。
