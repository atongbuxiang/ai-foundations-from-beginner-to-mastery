---
type: solution
status: draft
area: [neural-networks/differentiation, jvp, vjp]
topic: "[[局部微分、Jacobian、JVP 与 VJP]]"
exercise: "[[习题 - 局部微分、Jacobian、JVP 与 VJP]]"
sources: ["[[S-2018-Baydin-AD-Survey]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 局部微分、Jacobian、JVP 与 VJP
## A
### NN-JVP-A01
若 $f:\mathbb R^n\to\mathbb R^m$，Fréchet derivative $Df(x)$ 是从输入扰动空间到输出扰动空间的线性算子；$J_f(x):[m,n]$ 是选定坐标后的矩阵表示。JVP 输入 $v:[n]$、输出 $Jv:[m]$；VJP 输入 $u:[m]$、输出 $J^Tu:[n]$。网络实现中常只调用后两种作用，不形成 $J$。
### NN-JVP-A02
$u$ 定义输出扰动上的线性测量 $u^T\delta y$。由 $\delta y=J\delta x$，它在输入侧变为 $(J^Tu)^T\delta x$，故 $J^Tu$ 是 dual/cotangent pullback。这个操作对矩形或奇异 $J$ 仍有定义；求逆则要求方阵且可逆，并回答完全不同的问题。
### NN-JVP-A03
per-example Jacobian 保留每个样本输出对输入/参数的索引；batch-aggregated gradient 是经 sum/mean loss 的 VJP，已把样本轴约掉；full Jacobian 则保留所有输出坐标与输入坐标。一个 parameter `.grad` 通常只是第二种。
## B
### NN-JVP-B01
$$J=\begin{bmatrix}3&2\\\cos2&0\end{bmatrix}.$$
因此 $Jv=(3-2,\cos2)^T=(1,\cos2)^T$；$J^Tu=(12+5\cos2,8)^T$。JVP 与二维输出同形，VJP 与二维输入同形。
### NN-JVP-B02
直接对每个输出取方向导数：$D(x_1^2+x_2)[v]=2x_1v_1+v_2=4-1=3$；$D(e^{x_1-x_2})[v]=e^{-1}(v_1-v_2)=3/e$；$D(x_1x_2)[v]=x_2v_1+x_1v_2=4-1=3$。故 $Jv=(3,3/e,3)^T$。
### NN-JVP-B03
broadcast 的 JVP 是 $\dot Y_{btd}=\dot X_{btd}+\dot c_d$；其 VJP 是 $\bar X_{btd}{+}=\bar Y_{btd}$、$\bar c_d{+}=\sum_{b,t}\bar Y_{btd}$。reduction 的 JVP 是 $\dot s_d=\sum_{b,t}\dot Y_{btd}$；其 VJP 是 $\bar Y_{btd}{+}=\bar s_d$。广播与求和互为 transpose actions。
## C
### NN-JVP-C01
$Jv$ 是输出扰动，与 $u$ 配对得 $u^T(Jv)$。矩阵乘法结合性和转置给出 $u^TJv=(J^Tu)^Tv$。dot test 用独立实现的 JVP/VJP 检查两者是否近似互为伴随，能很敏感地捕捉 transpose、axis 和 accumulation 错误；有限次随机方向仍不是全域证明。
### NN-JVP-C02
$Dh(x)=Dg(f(x))\circ Df(x)$。对 tangent $v$，先得 $v_f=Df(x)[v]$，再得 $Dg(f(x))[v_f]$，因而正序。对 output cotangent $u$，先经 $Dg(f(x))^*$ 拉回到 $f$ 的输出空间，再经 $Df(x)^*$ 拉回输入；$(J_gJ_f)^T=J_f^TJ_g^T$ 强制逆序。
### NN-JVP-C03
forward mode 一次推进一个输入 seed，构造 full Jacobian 约需 $n$ 次 basis seeds；reverse mode 一次拉回一个输出 seed，约需 $m$ 次。所以 $n\ll m$ 或只需少数输入方向时选 forward，$m\ll n$ 或 scalar loss 时选 reverse。实际还要计 cache、vectorization 和硬件常数。
## D
### NN-JVP-D01
令 $f(x,y)=x^3/(x^2+y^2)$ 当 $(x,y)\ne(0,0)$，且 $f(0,0)=0$。两个坐标轴上都有原点偏导：沿 $x$ 轴 $f(h,0)=h$，故 $\partial_xf=1$；沿 $y$ 轴恒为 0，故 $\partial_yf=0$。若 Fréchet derivative 存在应为 $A(h,k)=h$。沿 $(t,t)$，$f(t,t)=t/2$，而 $A(t,t)=t$，余项为 $-t/2$，除以 $\sqrt2|t|$ 不趋 0，故不可微。
### NN-JVP-D02
ReLU 在 0 的左右导数不同，max tie 有多个 active branches，discrete predicate 跳变时局部线性近似可能不存在。AD 系统仍需为 primitive 指定一条 backward rule，所以返回的可是选定 subgradient、任一 tie convention 或 executed-branch derivative，而非 classical derivative 存在性证明。
### NN-JVP-D03
有限差分只在某个 point、direction、step size 和 dtype 下比较一个标量投影；bug 可落在未测子空间，截断与 roundoff 也可偶然抵消。需要多个随机方向、step sweep、dot test、small explicit Jacobian 和 boundary cases 共同建立证据。
## E
### NN-JVP-E01
对 $L:\mathbb R^n\to\mathbb R$且 $n$ 极大，reverse/VJP 从 seed $1$ 一次给出所有参数梯度；forward mode 需对每个参数方向推一次。若只需某个低维参数方向的 loss directional derivative，JVP 反而合适。
### NN-JVP-E02
对 $J^TJ$ 做 power iteration：从随机 $v$ 开始，先用 JVP 得 $w=Jv$，再用 VJP 得 $v'=J^Tw$，归一化后重复。Rayleigh quotient $\|Jv\|^2/\|v\|^2$ 估计 $\sigma_{max}^2$。它只需 operator actions，不物化 $J$，但要报告迭代收敛与谱隙敏感性。
### NN-JVP-E03
先检查 primal/tangent/cotangent 的 dtype、device 和 shape；随机 $u,v$ 做伴随 dot test；用中心差分验 JVP 并 sweep $h$；小维问题对显式 Jacobian；专门测 broadcast/reduction/empty axes；在 kink/tie 两侧分开检查，并把选定 convention 写入 API 合同。
