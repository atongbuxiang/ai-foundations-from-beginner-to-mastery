---
type: solution
status: draft
area: [neural-networks/initialization, correlation-propagation, edge-of-chaos]
topic: "[[相关传播、Edge of Chaos 与临界初始化]]"
exercise: "[[习题 - 相关传播、Edge of Chaos 与临界初始化]]"
sources: ["[[S-2016-Poole-Transient-Chaos]]", "[[S-2017-Schoenholz-Deep-Information-Propagation]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 相关传播、Edge of Chaos 与临界初始化

## A

### NN-EOC-A01
$q_\ell(x)=\mathbb E[z_i(x)^2]$ 追踪一个输入的长度/二阶尺度；$q_{12}^{(\ell)}=\mathbb E[z_i(x)z_i(x')]$ 追踪两个输入在共享随机网络中的未归一化相似度；$c_\ell=q_{12}/\sqrt{q_{11}q_{22}}$ 去掉 marginal scale，追踪相对方向。$q$ 稳定不能排除所有输入 correlation 都趋于 1，也不能排除小差异被放大。

### NN-EOC-A02
在 $q_{11}=q_{22}=q_*$ 时，令 $(U,V)$ 为 covariance matrix $q_*\begin{bmatrix}1&c\\c&1\end{bmatrix}$ 的 Gaussian pair，则
$$\mathcal C(c)=\frac{\sigma_w^2\mathbb E[\phi(U)\phi(V)]+\sigma_b^2}{q_*}.$$
同一网络对两个输入复用同一个 bias $b$，交叉乘积含 $\mathbb E[b^2]=\sigma_b^2$；若为两条路径错误地抽独立 bias，研究的就不再是同一个函数。

### NN-EOC-A03
局部斜率
$$\chi_1=\mathcal C'(1)=\sigma_w^2\mathbb E[\phi'(\sqrt{q_*}Z)^2]$$
（在所需正则条件下）。$\chi_1<1$ 为 ordered，邻近输入差异收缩；$=1$ 为 critical/edge，一阶中性；$>1$ 为 chaotic，$c=1$ 对小差异局部不稳定。

## B

### NN-EOC-B01
由 $Z_1,Z_2$ 独立、零均值、单位 variance，
$$\mathbb E[U^2]=q,$$
$$\mathbb E[V^2]=q(c^2+1-c^2)=q,$$
$$\mathbb E[UV]=q\mathbb E[Z_1(cZ_1+\sqrt{1-c^2}Z_2)]=qc.$$
所以 correlation 正好为 $c$；$|c|\le1$ 保证根号与 covariance matrix 都合法。

### NN-EOC-B02
线性 activation 时 $\mathbb E[UV]=c$，故
$$\mathcal C(c)=0.8c+0.2.$$
固定点解 $c=0.8c+0.2$ 为 $c_*=1$，$\chi_1=0.8$。correlation depth
$$\xi_c=-\frac1{\log0.8}\approx4.481.$$
因此 $1-c_L\approx e^{-L/4.481}(1-c_0)$；这个近似是 $c\approx1$ 的局部描述。

### NN-EOC-B03
ReLU map 为
$$\mathcal C(c)=\pi^{-1}[\sqrt{1-c^2}+(\pi-\arccos c)c].$$
所以
$$\mathcal C(0)=\frac1\pi\approx0.31831,$$
$$\mathcal C(1/2)=\frac{\sqrt3/2+\pi/3}{\pi}\approx0.608998.$$
又 $\mathcal C'(c)=1-\arccos(c)/\pi$，故 $\mathcal C'(1)=1$。数值计算 $c\to1$ 时应避免直接用差分穿过 domain 边界。

## C

### NN-EOC-C01
一层有
$$z_j(x)=\sum_iW_{ji}h_i(x)+b_j,
\qquad z_j(x')=\sum_kW_{jk}h_k(x')+b_j.$$
相乘取期望。在权重零均值、不同坐标不相关、与上一层 signals 独立的初始化合同下，$i\ne k$ 项消失：
$$\mathbb E[z_j(x)z_j(x')]
=\sum_i\mathbb E[W_{ji}^2]\mathbb E[h_i(x)h_i(x')]+\mathbb E[b_j^2].$$
若单权重 variance 为 $\sigma_w^2/n$ 且坐标同分布，得到
$$q_{12}'=\sigma_w^2\mathbb E[\phi(U)\phi(V)]+\sigma_b^2.$$

### NN-EOC-C02
在 $c=1$ 时 Gaussian pair 满足 $U=V=\sqrt{q_*}Z$（几乎处处）。因此
$$\mathcal C(1)=\frac{\sigma_w^2\mathbb E[\phi(\sqrt{q_*}Z)^2]+\sigma_b^2}{q_*}=1,$$
最后一步正是单输入 fixed-point equation。若 marginal moments 尚未到同一 $q_*$，不能直接使用这个 normalized one-dimensional map。

### NN-EOC-C03
递推给出
$$\varepsilon_L\approx\chi_1^L\varepsilon_0=exp(L\log\chi_1)\varepsilon_0.$$
与 $\exp(-L/\xi_c)$ 比较即得 $\xi_c=-1/\log\chi_1$。当 $\chi_1\uparrow1$，$\log\chi_1\uparrow0$，线性 depth scale 发散；恰在 $\chi_1=1$ 时一阶项不能决定 $\varepsilon$ 的变化，必须展开 $\mathcal C(1-\varepsilon)$ 的下一非零项，收敛可能转为 polynomial。

## D

### NN-EOC-D01
第一个校准网络取 linear $\phi(z)=z$、$q_*=1$、$\sigma_w^2=0.8,\sigma_b^2=0.2$，于是 $q'=1$ 且 $\chi_1=0.8$。第二个取 $\phi(z)=z^3$、$\sigma_b=0$、$q_*=1$、$\sigma_w^2=1/\mathbb E[Z^6]=1/15$；仍有 $q'=1$，但
$$\chi_1=\frac1{15}\mathbb E[(3Z^2)^2]=\frac9{15}\mathbb E[Z^4]=\frac{27}{15}=1.8.$$
两者的单输入 second moment 证据相同，相关性局部制度相反。

### NN-EOC-D02
$\chi_1=1$ 只给 $\mathcal C$ 在 $c=1$ 的导数。不同 nonlinear maps 可有相同端点导数却在 $c<1$ 时明显偏离对角线；即使接近 1，高阶项也会累计。有限 width、bias、residual/normalization 与训练后权重相关还会改变 map。因此“任意输入、任意深度保持原 correlation”远强于已有条件。

### NN-EOC-D03
ReLU + He、zero bias 给 $\chi_1=1$，控制的是 correlation map 在 $c=1$ 的局部斜率。Dynamical isometry 要求输入—输出 Jacobian 的全部 relevant singular values 接近 1；ReLU derivative diagonal 含大量 0，能产生 rank loss 和宽谱。平均相关临界不控制最坏方向，所以推论无效。

## E

### NN-EOC-E01
先用高样本数二维 Gaussian Monte Carlo 或 quadrature 得到 reference $\mathcal C(c)$，用重复采样估 integration standard error。再对 width $n\in\{64,256,1024,4096\}$、固定 depth 与多个 independent initializations 测 empirical map；每个 seed 内用足够 input pairs，seed 间统计 ensemble variation。对每个 width 报 bias、RMSE 与 confidence interval，不能把同一网络内 pair variation 当 seed uncertainty。

### NN-EOC-E02
两输入 $x,x'$ 经过 block 后
$$\operatorname{Cov}(x+F(x),x'+F(x'))
=\operatorname{Cov}(x,x')+\operatorname{Cov}(F(x),F(x'))$$
$$+\operatorname{Cov}(x,F(x'))+\operatorname{Cov}(F(x),x').$$
最后两项是 skip–branch cross covariance，通常不能凭“branch 随机”就删除；它们依赖参数共享、normalization、branch input 与训练状态。marginal variances 也有对应 cross terms，归一化 correlation 还需重新除以两侧 scale。

### NN-EOC-E03
对每组初始化记录：(i) 多输入 correlation trajectory；(ii) 随机 $v$ 的 $\|Jv\|/\|v\|$ 与随机 cotangent 的 $\|J^Tu\|/\|u\|$；(iii) power/Lanczos 的 $s_{\max}$、可行时的 $s_{\min}$ 或 lower proxy。固定 width/depth/data/seed set。结论分层：correlation 只支持 pairwise mean-field geometry；random-direction gain 支持平均方向；extremes 才接近 condition/dynamical-isometry claim，仍限初始化与测量子空间。
