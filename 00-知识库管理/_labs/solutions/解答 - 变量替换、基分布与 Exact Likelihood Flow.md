---
type: solution
status: draft
topic: "[[变量替换、基分布与 Exact Likelihood Flow]]"
exercise: "[[习题 - 变量替换、基分布与 Exact Likelihood Flow]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 变量替换、基分布与 Exact Likelihood Flow
## A. 识别与复述
### GEN33-A01
$\log p_X(x)=\log p_Z(f(x))+\log|\det J_f(x)|$；在 $x=g(z)$ 处，$\log p_X(g(z))=\log p_Z(z)-\log|\det J_g(z)|$。二者由 $J_f=J_g^{-1}$ 等价。
### GEN33-A02
它承诺给定连续模型和预处理时，模型 log-density 不靠 ELBO/MCMC 即可按声明公式评价。不承诺离散 pmf 精确、浮点 inverse/logdet 无误差、有限样本学到真分布、OOD/语义质量优或部署后处理保持同一密度。
### GEN33-A03
普通微分同胚的 Jacobian 是方阵且有非零 determinant；不同维空间间不存在这种局部可逆方阵合同。降维会把体积压到零测集，升维则不能由普通 inverse 唯一恢复。
## B. 手算与建模
### GEN33-B01
$f(x)=(x+2)/3$，故 $p_X(x)=\phi((x+2)/3)/3$。$x=1$ 时 $z=1$，$\log p_X(1)=-\frac12-\frac12\log(2\pi)-\log3$。
### GEN33-B02
$x=(2,-3)^\top+b$。$\det A=6$，生成 logdet 为 $\log6$，编码 Jacobian $A^{-1}$ 的 logdet 为 $-\log6$。
### GEN33-B03
编码总 logdet $0.4-0.2+1.1=1.3$，故 $\log p_X=-3.5+1.3=-2.2$。
## C. 推导与证明
### GEN33-C01
小邻域内 $dx\approx|\det J_g(z)|dz$；同一概率质量满足 $p_Z(z)dz=p_X(g(z))dx$。相除得 $p_X(g(z))=p_Z(z)/|\det J_g(z)|$，再用 inverse 得编码式。绝对值处理 orientation reversal。
### GEN33-C02
若 $u_k=h_k(u_{k-1})$，链式法则给 $J_f=J_{h_K}(u_{K-1})\cdots J_{h_1}(u_0)$。取 determinant 的乘积、绝对值和 log，得到 $\sum_k\log|\det J_{h_k}(u_{k-1})|$；不能都在原始 $x$ 处评价。
### GEN33-C03
任取 $x$，唯一 $z=f(x)$ 存在。$p_Z(z)>0$，diffeomorphism 又给 $|\det J_f(x)|>0$，二者乘积严格为正。
## D. 边界、反例与纠错
### GEN33-D01
生成映射放大体积 $dx=|\det J_g|dz$，同一质量除以更大体积，所以 $p_X=p_Z/|\det J_g|$。只有编码式才乘 inverse Jacobian determinant。
### GEN33-D02
取 $A=\operatorname{diag}(10^{10},10^{-10})$，determinant 为 1 且数学可逆，但条件数 $10^{20}$；小舍入误差沿小奇异值方向反求时被放大，det=1 不能作为稳定证书。
### GEN33-D03
Density 有单位且依赖坐标缩放；离散质量应为 bin integral $P(x)=\int_{bin(x)}p_c(y)dy$。单点 density 既非该积分，也可能大于 1。
## E. AI 迁移
### GEN33-E01
输入 $x:[B,d]$；编码输出 $z:[B,d]$、各层 logdet $[B]$，base logprob 对 feature 求和后为 $[B]$，最终 `log_px=log_pz+sum_logdet:[B]`；loss 再按 batch reduction。保留每层状态以在正确评价点算 logdet。
### GEN33-E02
一维 $x=az+b$ 与解析 Gaussian 对照；小维显式/autodiff Jacobian 对照 analytic logdet；双向 identity 检查 $\log|\det J_f|+\log|\det J_g|=0$ 且 round-trip 成立。三者分别抓符号、层公式和 inverse 错误。
### GEN33-E03
分开模型 density 可计算性、训练估计、预处理/dequantization、测试 likelihood、质量/覆盖、OOD、参数与计算预算、采样 latency、后处理分布和 evaluator。需 compute-matched baselines 与多 seed，不能由 `exact` 推出经验最优。

