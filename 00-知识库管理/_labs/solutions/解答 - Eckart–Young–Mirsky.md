---
type: solution
status: draft
area: [labs, math/matrix-analysis, ai/foundations]
topic: "[[定理 - Eckart–Young–Mirsky]]"
exercise: "[[习题 - Eckart–Young–Mirsky]]"
related: ["[[有效秩]]", "[[随机化低秩近似与随机 SVD]]", "[[练习与测验 MOC]]"]
sources: ["Eckart-Young-1936", "Mirsky-1960"]
created: 2026-08-18
updated: 2026-08-18
---
# 解答 - Eckart–Young–Mirsky

## A
### MA-EYM-A01
在 $\operatorname{rank}B\le k$ 上，$A_k=\sum_{i\le k}\sigma_iu_iv_i^*$ 最优；谱最优值 $\sigma_{k+1}$，Frobenius 最优值 $(\sum_{i>k}\sigma_i^2)^{1/2}$。
### MA-EYM-A02
酉不变范数只依赖奇异值。Frobenius 下若 $\sigma_k>\sigma_{k+1}$，最佳矩阵唯一；截断点重数导致子空间旋转。谱范数非严格凸，即使有 gap 也可能多解：$A=\operatorname{diag}(3,2),k=1$，$B=\operatorname{diag}(b,0)$ 且 $1\le b\le5$ 都有误差 2。
### MA-EYM-A03
核范数是酉不变范数，可用 Mirsky 推广；元素加权、缺失观测和任务损失一般不酉不变，不能直接套用。

## B
### MA-EYM-B01
$k=1:A_1=\operatorname{diag}(5,0,0)$，谱误差 3，F 误差 $\sqrt{10}$。$k=2:A_2=\operatorname{diag}(5,3,0)$，两种误差均为 1。
### MA-EYM-B02
$uu^T$ 对任意单位 $u$ 都是最优秩一近似；例如 $e_1e_1^T$ 与 $e_2e_2^T$ 不同，但对 $I_3$ 的谱误差均 1、F 误差 $\sqrt2$。
### MA-EYM-B03
可取 $L=U_k\Sigma_k,R=V_k^*$，或 $L=U_k\Sigma_k^{1/2},R=\Sigma_k^{1/2}V_k^*$。任意可逆 $C$ 给 $(LC)(C^{-1}R)=LR$。

## C
### MA-EYM-C01
令 $S=\operatorname{span}(v_1,\ldots,v_{k+1})$。因 $\dim S=k+1$、$\dim\mathcal N(B)\ge n-k$，交集含单位 $x$。于是 $Bx=0$ 且 $\|Ax\|^2=\sum_{i\le k+1}\sigma_i^2|c_i|^2\ge\sigma_{k+1}^2$，故 $\|A-B\|_2\ge\sigma_{k+1}$。
### MA-EYM-C02
令 $P=P_{\mathcal R(B)}$。Frobenius 正交分解给 $\|A-B\|_F^2\ge\|(I-P)A\|_F^2=\|A\|_F^2-\operatorname{tr}(PAA^*)$。写 $AA^*=\sum\sigma_i^2u_iu_i^*$，权重 $\alpha_i=\|Pu_i\|^2\in[0,1]$ 且和不超过 $k$，故 trace 至多前 $k$ 项平方和，得到尾和下界。
### MA-EYM-C03
秩 $s\le k$ 的 $B$ 取紧致 SVD $U_s\Sigma_sV_s^*$，补零列即可写成 $m\times k$ 与 $k\times n$ 乘积。反之 $\operatorname{rank}(LR)\le k$。乘积可行集相同，但因可逆 gauge，因子不唯一。

## D
### MA-EYM-D01
取 $A=\operatorname{diag}(2,1),k=1$，标准截断为 $B_0=\operatorname{diag}(2,0)$。令元素平方权重 $w_{11}=0.01,w_{22}=100$，则 $B_0$ 加权误差 100，而 $B_1=\operatorname{diag}(0,1)$ 的误差仅 $0.01\cdot4=0.04$，故截断 SVD 不再最优。
### NLA-EYM-D02
最优误差值由连续奇异值决定而稳定；选定 $k$ 维子空间因小 gap 可大幅旋转；有限精度算法还会受停止、重正交和随机误差影响，应验收子空间与残差。
### NLA-EYM-D03
比较 $\|A-\tilde A_k\|$ 与理论尾界：超出 $\|A-A_k\|$ 的部分是算法附加误差。报告 $k$、oversampling、power 次数、seed、dtype、停止准则及谱/F 尾误差。

## E
### AI-EYM-E01
$\|(W-W_k)x\|\le\sigma_{k+1}\|x\|$；$\|(W-W_k)X\|_F\le\sigma_{k+1}\|X\|_F$。端到端还经后续 Jacobian、激活、归一化与数据分布传播。
### AI-EYM-E02
样本按行 $X:N\times d$ 时，$V_k:d\times k$ 给特征方向，$XV_kV_k^T$ 是最佳线性 rank-$k$ 重构；样本按列则由左奇异向量承担方向。必须先中心化。
### AI-EYM-E03
训练后截断优化预训练矩阵的酉不变范数；LoRA 直接在因子参数化中按任务损失学习；结构化低秩还限制稀疏、卷积或采样形式，可行集不同，EYM 不再直接保证。
