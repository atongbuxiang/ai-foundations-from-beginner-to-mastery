---
type: solution
status: draft
area: [math/numerical-linear-algebra]
topic: "[[幂法、反幂法与 Rayleigh 商迭代]]"
exercise: "[[习题 - 幂法、反幂法与 Rayleigh 商迭代]]"
prerequisites: ["[[特征分解]]", "[[二次型与正定矩阵]]", "[[稳定求解线性方程组]]"]
related: ["[[实验 - 谱间隙、移位与 Rayleigh 商迭代收敛]]", "[[Hessenberg 化与 QR 特征值算法]]"]
sources: ["[[S-2023-Demmel-幂法反幂与QR迭代]]"]
created: 2026-08-15
updated: 2026-08-15
---

# 解答 - 幂法、反幂法与 Rayleigh 商迭代

> [!warning] 使用边界
> 先独立作答。特别注意：对角/对称矩阵上的简洁收敛率不能无条件搬到一般非正规矩阵。

## A. 识别与复述

### NLA-EIG-A01

| 方法 | 目标 | 每步核心运算 | 可复用项 | 主要条件 |
|---|---|---|---|---|
| 幂法 | 最大模特征值方向 | $y=Ax$ | 矩阵/算子本身 | 主模唯一，初始目标投影非零 |
| 固定移位反幂 | 离 $\sigma$ 最近的方向 | 解 $(A-\sigma I)y=x$ | 固定移位的 LU/$LDL^T$ 因子 | 最近者唯一，求解可靠 |
| RQI | 局部最近特征对 | 解 $(A-\rho_kI)y=x$ | 通常不能复用完整因子 | 对称/Hermitian、单特征值、局部初值和精确求解才有三次阶 |

三者都应归一化，并用特征残差验收。

### NLA-EIG-A02

- 最大模特征值：幂法；
- 最大代数特征值：对称情形可用 Lanczos/Rayleigh 极值方法，或给 $A$ 加已知移位使排序与模排序一致；
- 离 $\sigma$ 最近：shift-and-invert/反幂法；
- 最大奇异值：交替计算 $u\propto Wv$、$v\propto W^Tu$，等价于不显式形成 $W^TW$ 的幂迭代。

例如 $\operatorname{diag}(-10,2)$ 的最大模是 $-10$，最大代数是 $2$，二者不可混用。

### NLA-EIG-A03

- Rayleigh 商变化量：估计值是否还在移动，但可能因聚簇或舍入过早停滞；
- 特征残差：当前对是否满足 $Ax\approx\rho x$，是最基本停止指标；
- 方向角：若真向量已知，直接衡量方向误差；实际计算通常未知；
- 谱间隙：把残差转化为方向误差界，并决定收敛速度。

因此至少用尺度化特征残差停止；若要宣称单向量准确，还需 gap/sep。

## B. 手算与构造

### NLA-EIG-B01

第一步：

$$
y_1=\frac1{\sqrt2}(5,2)^T,
\qquad
x_1=\frac1{\sqrt{29}}(5,2)^T.
$$

$$
\rho_1=x_1^TAx_1
=\frac{5\cdot25+2\cdot4}{29}
=\frac{133}{29}.
$$

第二步方向：

$$
y_2\propto(25,4)^T,
\qquad
x_2=\frac1{\sqrt{641}}(25,4)^T.
$$

$$
\rho_2
=\frac{5\cdot625+2\cdot16}{641}
=\frac{3157}{641}.
$$

第二/第一分量比依次为

$$
1,
\quad\frac25,
\quad\left(\frac25\right)^2.
$$

### NLA-EIG-B02

由 $r^k\le10^{-6}$：

$$
k\ge\frac{\log10^{-6}}{\log r}.
$$

- $r=0.2$：$k\ge8.58$，至少 $9$ 步；
- $r=0.8$：$k\ge61.91$，至少 $62$ 步；
- $r=0.98$：$k\ge683.84$，至少 $684$ 步。

谱比只从 $0.8$ 变到 $0.98$，迭代数却增加一个数量级。

### NLA-EIG-B03

未归一化方向依次为

$$
A^kx_0\propto((-4)^k,1)^T.
$$

所以主方向第一分量符号按

$$
-,+,-,+,\ldots
$$

交替，而第二分量相对大小按 $4^{-k}$ 衰减。可用

$$
\sin\angle(x_k,e_1)
$$

或

$$
\min(\|x_k-e_1\|,\|x_k+e_1\|)
$$

作为相位不变误差。

### NLA-EIG-B04

$$
y_1=(A-1.9I)^{-1}x_0
=\frac1{\sqrt3}
\begin{bmatrix}
1/3.1\\10\\-1/0.9
\end{bmatrix}.
$$

相对于目标第二分量 $10$，其余两分量绝对比例为

$$
\frac{1/3.1}{10}\approx0.03226,
\qquad
\frac{1/0.9}{10}\approx0.11111.
$$

一次求解已经把 $e_2$ 变成明显主方向。

### NLA-EIG-B05

$$
\rho
=\sin^2\theta+3\cos^2\theta
=3-2\sin^2\theta.
$$

因此

$$
1-\rho=-2\cos^2\theta,
\qquad
3-\rho=2\sin^2\theta.
$$

反幂步骤给出

$$
y=
\begin{bmatrix}
\sin\theta/(1-\rho)\\
\cos\theta/(3-\rho)
\end{bmatrix}
=
\frac12
\begin{bmatrix}
-\sin\theta/\cos^2\theta\\
\cos\theta/\sin^2\theta
\end{bmatrix}.
$$

新角度相对 $e_2$ 的正切绝对值是

$$
|\tan\theta_+|
=\left|\frac{y_1}{y_2}\right|
=\left|\frac{\sin^3\theta}{\cos^3\theta}\right|
=|\tan\theta|^3.
$$

这在二维对称例子中给出精确三次关系。

### NLA-EIG-B06

向量已归一化，因为 $0.99+0.01=1$。Rayleigh 商为

$$
\rho=2(0.99)+5(0.01)=2.03.
$$

残差为

$$
r=
\begin{bmatrix}
0\\
(2-2.03)\sqrt{0.99}\\
(5-2.03)0.1
\end{bmatrix}.
$$

所以

$$
\|r\|_2
=\sqrt{0.03^2\cdot0.99+2.97^2\cdot0.01}
\approx0.2985.
$$

最近特征值是 $2$，距离

$$
|2.03-2|=0.03\le0.2985.
$$

## C. 推导与证明

### NLA-EIG-C01

$$
\begin{aligned}
A^kx_0
&=\sum_i\alpha_i\lambda_i^kq_i\\
&=\lambda_1^k\alpha_1
\left[q_1+
\sum_{i\ge2}\frac{\alpha_i}{\alpha_1}
\left(\frac{\lambda_i}{\lambda_1}\right)^kq_i
\right].
\end{aligned}
$$

归一化只去掉共同标量。括号内非主分量的范数至多为

$$
\left(
\sum_{i\ge2}\left|\frac{\alpha_i}{\alpha_1}\right|^2
\left|\frac{\lambda_i}{\lambda_1}\right|^{2k}
\right)^{1/2}
\le
C\left|\frac{\lambda_2}{\lambda_1}\right|^k.
$$

方向正弦由非主分量与总范数之比控制，因此得到所需阶。$\alpha_1\ne0$ 和严格谱比正是证明中不能删除的两处。

### NLA-EIG-C02

因 $w\perp q_1$ 且 $A$ 对称，$q_1^TAw=\lambda_1q_1^Tw=0$。于是

$$
\rho(x)
=\lambda_1\cos^2\theta+(w^TAw)\sin^2\theta.
$$

所以

$$
\lambda_1-\rho(x)
=\left(\lambda_1-w^TAw\right)\sin^2\theta.
$$

Rayleigh 极值界给出

$$
\lambda_n\le w^TAw\le\lambda_1,
$$

故

$$
0\le\lambda_1-\rho(x)
\le(\lambda_1-\lambda_n)\sin^2\theta.
$$

### NLA-EIG-C03

写 $x=\sum_i\alpha_iq_i$、$\sum_i|\alpha_i|^2=1$。则

$$
r=\sum_i(\lambda_i-\rho)\alpha_iq_i,
$$

从而

$$
\|r\|^2
=\sum_i|\lambda_i-\rho|^2|\alpha_i|^2
\ge
\min_i|\lambda_i-\rho|^2
\sum_i|\alpha_i|^2.
$$

最后一项为 $1$，开平方即得结论。

### NLA-EIG-C04

变换矩阵

$$
B=(A-\sigma I)^{-1}
$$

与 $A$ 共享特征向量，而特征值变为

$$
\mu_i=\frac1{\lambda_i-\sigma}.
$$

若 $\lambda_j$ 离移位最近，则 $|\mu_j|$ 最大；第二近 $\lambda_\ell$ 对应第二大模。幂法谱比为

$$
\left|\frac{\mu_\ell}{\mu_j}\right|
=\left|
\frac{1/(\lambda_\ell-\sigma)}{1/(\lambda_j-\sigma)}
\right|
=\left|\frac{\lambda_j-\sigma}{\lambda_\ell-\sigma}\right|.
$$

### NLA-EIG-C05

证明骨架：

1. $A$ 实对称/复 Hermitian，目标 $\lambda$ 是单特征值；
2. $x_k$ 已足够接近对应 $q$，角误差为 $e_k$；
3. Rayleigh 商驻点性质给出
   $$|\rho_k-\lambda|=O(e_k^2);$$
4. 其余特征值与 $\lambda$ 的 separation 有正下界；
5. 反幂一步把非目标/目标分量比乘以
   $$O(|\rho_k-\lambda|/\operatorname{sep});$$
6. 原非目标比例为 $O(e_k)$，故
   $$e_{k+1}=O(e_k)O(e_k^2)=O(e_k^3).$$

还需线性系统求解足够准确；多重特征值、非正规矩阵或局部区域外都不能直接使用此结论。

### NLA-EIG-C06

由 QR

$$
AZ_k=Z_{k+1}R_{k+1}
$$

且 $R_{k+1}$ 可逆，得

$$
\mathcal R(AZ_k)=\mathcal R(Z_{k+1}R_{k+1})=\mathcal R(Z_{k+1}).
$$

另一方面

$$
\mathcal R(AZ_k)=A\mathcal R(Z_k)=A\mathcal S_k.
$$

所以 $\mathcal S_{k+1}=A\mathcal S_k$。QR 只把同一列空间换成正交基；若不正交化，多列反复乘 $A$ 后都会数值靠近第一主方向，失去较弱方向的信息。

## D. 边界、反例与纠错

### NLA-EIG-D01

取

$$
A=\operatorname{diag}(1,-1),
\qquad x_0=(1,1)^T/\sqrt2.
$$

则

$$
A^{2k}x_0=x_0,
\qquad
A^{2k+1}x_0=(1,-1)^T/\sqrt2.
$$

方向在两个向量间振荡，不趋向唯一特征向量。原因是两个特征值模都为 $1$，没有严格主模。

### NLA-EIG-D02

取 $A=\operatorname{diag}(5,2)$，主向量 $q_1=e_1$，初始 $x_0=e_2$。则

$$
A^kx_0=2^ke_2.
$$

归一化后永远是 $e_2$。矩阵在特征基中不会混合坐标，所以缺失的 $e_1$ 分量不可能凭空产生。

### NLA-EIG-D03

写

$$
J=\lambda I+N,
\qquad
N=\begin{bmatrix}0&1\\0&0\end{bmatrix},
\quad N^2=0.
$$

二项式展开只有前两项：

$$
J^k
=\lambda^kI+k\lambda^{k-1}N
=\begin{bmatrix}
\lambda^k&k\lambda^{k-1}\\0&\lambda^k
\end{bmatrix}.
$$

即使 $|\lambda|<1$，$k\lambda^{k-1}$ 也可能先增长后衰减。只看 $\lambda^k$ 会漏掉非正规/缺陷结构的多项式暂态。

### NLA-EIG-D04

正确做法是分解一次

$$
P(A-\sigma I)=LU
$$

并每步解三角系统。显式逆：

- 计算全部逆元素，而每步只需逆作用于一个向量；
- 往往产生更多舍入误差和内存访问；
- 稀疏逆通常变稠密；
- 难以报告每次线性求解残差；
- 隐藏主元、条件估计与失败状态。

固定移位时因子可复用；变化移位时考虑更新、预条件迭代或重新分解。

### NLA-EIG-D05

取聚簇矩阵

$$
A=\operatorname{diag}(1,1+10^{-8})
$$

和两方向混合的 $x$。Rayleigh 商始终落在宽度仅 $10^{-8}$ 的区间中，相邻两步变化可以很快小于浮点/用户阈值；但方向收敛因子约为

$$
\frac1{1+10^{-8}}\approx1-10^{-8},
$$

方向几乎没有收敛。残差约由 gap 与混合系数控制，可能仍高于目标容差。因此应直接检查尺度化 $\|Ax-\rho x\|$，并用 gap 解释方向。

## E. AI 迁移

### NLA-EIG-E01

若

$$
W\in\mathbb R^{d_{out}\times d_{in}},
$$

则

$$
u\in\mathbb R^{d_{out}},
\qquad v\in\mathbb R^{d_{in}}.
$$

一步更新：

$$
u\leftarrow\frac{Wv}{\|Wv\|},
\qquad
v\leftarrow\frac{W^Tu}{\|W^Tu\|},
\qquad
\widehat\sigma=u^TWv.
$$

它承诺的是从上一步状态继续跟踪主奇异方向的一个迭代近似，不是每步精确 $\sigma_1$。当 $\sigma_1\approx\sigma_2$、权重一步变化很大、初始化差或低精度归一化失真时，估计可能滞后。

### NLA-EIG-E02

最大模幂法只返回 $|\lambda|$ 最大的方向，可能是最大正曲率，也可能是最负曲率。可用：

- Lanczos 同时估计谱区间两端；
- 对 $H$ 与 $-H$ 分别做最大代数估计；
- 使用移位/shift-and-invert 定位指定区间；
- 用 Rayleigh 商符号判断方向曲率。

验收需报告 Hessian-vector 残差 $\|Hv-\rho v\|$、迭代历史、seed、gap 估计和 HVP 数值误差。

### NLA-EIG-E03

$$
V_t\in\mathbb R^{n\times p}
$$

的各列若不正交化，会一起塌到第一主方向。Householder QR 通常给较可靠正交性；Cholesky QR 主要由矩阵乘构成、硬件友好，却形成 $Y^TY$ 并承受条件数平方。应检查

$$
\|V_t^TV_t-I\|,
\qquad
\|MV_t-V_t(V_t^TMV_t)\|,
$$

并设置失败检测、再正交化或 Householder 回退。

### NLA-EIG-E04

若 $A=U\Sigma V^T$，则

$$
(AA^T)^qA
=U\Sigma^{2q+1}V^T.
$$

相对谱比从 $\sigma_i/\sigma_1$ 变为

$$
(\sigma_i/\sigma_1)^{2q+1},
$$

主子空间分离加快。每轮正交化防止弱方向在有限精度中消失。$q$ 过大时动态范围过宽，较小奇异方向会下溢或被主方向污染，同时增加矩阵乘成本。

### NLA-EIG-E05

对有限 $K$ 步算法求导，目标函数实际上依赖初值、每步归一化、截断步数和 stop-gradient 位置；它描述“这个近似算法输出怎样变化”。

精确特征向量导数描述收敛极限，并含 $1/(\lambda_i-\lambda_j)$，要求单特征值与非零 gap。二者只有在 $K$ 足够大且微分与极限可交换时才接近。停止梯度会把状态视为常量，得到另一种偏导含义；初始化小投影与小 gap 都会使有限步梯度偏差大。

## 常见错误模式

| 错误 | 为什么错 | 回链 |
|---|---|---|
| 最大模等于最大代数 | 负特征值可有更大绝对值 | [[幂法、反幂法与 Rayleigh 商迭代#六、幂法的四个必要检查]] |
| RQI 总是三次 | 需要对称、单根、局部和准确求解 | [[幂法、反幂法与 Rayleigh 商迭代#十四、对称 RQI 的局部三次收敛]] |
| Rayleigh 商不变就停止 | 聚簇谱会隐藏方向停滞 | [[幂法、反幂法与 Rayleigh 商迭代#八、残差给出的后验信息]] |
| 显式形成逆 | 破坏稳定性、稀疏与验收 | [[幂法、反幂法与 Rayleigh 商迭代#十一、绝不显式形成 (A-σ I)^{-1}]] |

## 无提示重做

- [ ] 48 小时后重做 `B05、C01、C05`；
- [ ] 一周后为一个 HVP 或谱归一化任务写可信迭代报告。

