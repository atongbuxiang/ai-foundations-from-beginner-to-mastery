---
type: solution
status: draft
topic: "[[Residual Flow、可逆 ResNet 与 Logdet 估计]]"
exercise: "[[习题 - Residual Flow、可逆 ResNet 与 Logdet 估计]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Residual Flow、可逆 ResNet 与 Logdet 估计
## A. 识别与复述
### GEN37-A01
若 $\operatorname{Lip}(g)=L<1$，则对每个 $y$，$T_y(x)=y-g(x)$ 是压缩；迭代 $x_{k+1}=T_y(x_k)$ 收敛到唯一 $x^*$，满足 $F(x^*)=y$。
### GEN37-A02
$\log\det(I+J_g)=\sum_{k\ge1}(-1)^{k+1}\operatorname{tr}(J_g^k)/k$。需要矩阵对数分支合法且至少 $\rho(J_g)<1$；$\|J_g\|<1$ 是易用充分条件。
### GEN37-A03
Inverse truncation 使数值反解未到不动点；series truncation 删去高阶项，通常造成 bias；有限 probes 使每个 trace 估计有 sampling variance。三者由不同预算控制。
## B. 手算与建模
### GEN37-B01
$x_1=3,x_2=1.5,x_3=2.25$；精确逆 $x^*=2$。误差依次 $1,0.5,0.25$，按 $L=0.5$ 几何缩小并交替。
### GEN37-B02
精确值 $\log(1.2)+\log(0.6)=\log0.72\approx-0.328504$。第一项 $\operatorname{tr}J=-0.2$；第二项减 $\operatorname{tr}(J^2)/2=-(0.04+0.16)/2=-0.1$，合计 $-0.3$。
### GEN37-B03
$Av=(-1,-1)^\top$，所以 $v^TAv=0$；$\operatorname{tr}A=5$。单 probe 可偏离很大；无偏指对 probe 分布取期望，不是每次相等。
## C. 推导与证明
### GEN37-C01
$\|T_y(x)-T_y(x')\|=\|g(x')-g(x)\|\le L\|x-x'\|$。完备空间上的压缩映射有唯一不动点；不动点方程 $x=y-g(x)$ 等价于 $y=x+g(x)$。
### GEN37-C02
$\|x_k-x^*\|\le\sum_{j=k}^{\infty}\|x_j-x_{j+1}\|$。压缩性给 $\|x_{j+1}-x_j\|\le L^{j-k+1}\|x_k-x_{k-1}\|$；求几何级数得 $L/(1-L)$ 倍。
### GEN37-C03
$v^TAv=\operatorname{tr}(v^TAv)=\operatorname{tr}(Avv^T)$。取期望并用 $E[vv^T]=I$，得 $E[v^TAv]=\operatorname{tr}(AI)=\operatorname{tr}A$。
## D. 边界、反例与纠错
### GEN37-D01
一维 $g(x)=2x$ 的 Lipschitz 常数 2，不满足条件，但 $F(x)=3x$ 显然可逆。故 $L<1$ 是方便的全局充分证书，不是必要条件。
### GEN37-D02
若只保留前 $K$ 项，Hutchinson 期望等于“截断级数”的 trace 和，而非无限级数；被删 tail 仍产生 deterministic truncation bias。除非另用合规随机截断，不能称总 estimator 无偏。
### GEN37-D03
$g(x)=0.999x$，则 $F=1.999x$ 可逆，但 fixed-point error 仅每步乘 0.999；把误差缩小 $10^{-3}$ 约需 $\log(10^{-3})/\log(0.999)\approx6904$ 步。
## E. AI 迁移
### GEN37-E01
证书账：target/estimated Lipschitz；inverse 账：iterations/tolerance/residual；series 账：order/remainder proxy；trace 账：probe type/count/seed/variance。再加 round-trip、condition proxy、NLL 和 wall time。
### GEN37-E02
增加 probes 降低固定 trace 项的 Monte Carlo variance，不能恢复被删高阶项；增加 series order 降低 truncation bias，但每项仍可有 probe variance且计算更贵。应做二维 grid 而非只调一个旋钮。
### GEN37-E03
核对每层 operator norm 的定义、卷积处理、power-iteration 收敛、训练更新后估计是否 stale、激活 Lipschitz、组合 product bound、margin 是否严格小于 1，以及随机 Jacobian norm/逆迭代的经验反证。近似谱归一化不自动是全局精确证书。

