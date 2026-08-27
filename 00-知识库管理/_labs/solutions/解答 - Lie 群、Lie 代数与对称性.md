---
type: solution
status: draft
area: [math/lie-theory, math/group-theory, ai/equivariant-learning]
topic: "Lie 群、Lie 代数与对称性"
exercise: "[[习题 - Lie 群、Lie 代数与对称性]]"
prerequisites: ["[[Lie 群、Lie 代数与对称性]]"]
related: ["[[练习与测验 MOC]]", "[[实验 - Lie 指数、BCH 与群平均等变审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - Lie 群、Lie 代数与对称性

> [!abstract] 使用方式
> 本文是独立详解，不用“见正文”替代证明。先闭卷完成[[习题 - Lie 群、Lie 代数与对称性]]并保留原稿，再比对对象类型、条件、符号 convention 与 claim level。能读懂以下答案不等于能独立重建。

## A01 解答：十类对象与六个纠错

| 对象 | domain → codomain | 所需结构 | 边界/AI 对应 |
|---|---|---|---|
| multiplication $m$ | $G\times G\to G$ | group | associative；变换 composition |
| inversion $i$ | $G\to G$ | group | $i(gh)=h^{-1}g^{-1}$ |
| $L_g$ | $G\to G,h\mapsto gh$ | group；Lie 时 smooth | inverse 为 $L_{g^{-1}}$ |
| $\mathfrak g$ | vector space $T_eG$ | Lie group | 只看 identity component |
| bracket | $\mathfrak g^2\to\mathfrak g$ | invariant-field commutator | matrix 中为 $XY-YX$ |
| $\exp_G$ | $\mathfrak g\to G$ | one-parameter flow | local diffeo at $0$，非必 global bijection |
| action | $G\times X\to X$ | group + compatible $X$ | 指定 transforms 如何作用 data |
| orbit/stabilizer | $x\mapsto Gx$ / $G_x\subseteq G$ | action | semantic equivalence需另假设 |
| representation | $G\to GL(V)$ | linear action | feature transformation type |
| $d\rho$ | $\mathfrak g\to\mathfrak{gl}(V)$ | smooth representation | 不编码 disconnected components |
| equivariant $F$ | $X\to Y$ | input/output actions | $F\rho_X=\rho_YF$ |
| Haar average | function/map → invariant/equivariant part | locally compact；归一化需 compact | exact symmetrization |
| parameter orbit | $G_\theta\cdot\theta$ | parameter action保持 function | non-identifiability/zero modes |

纠错：

1. 错。Finite/discrete group 是零维 Lie group时 algebra 为 $0$；arbitrary abstract group甚至未给 smooth structure。
2. 错。SO(2) 中 $\exp((\theta+2\pi k)J)=\exp(\theta J)$；一般还可能不 surjective。
3. 错。Invariant 是 output action trivial 的 equivariant 特例。
4. 错。Generator identity只覆盖 identity component；$O(n)$ 的 reflection 要另验。
5. 错。Augmentation改变 empirical/risk objective，不把 function class硬限制为 intertwiners。
6. 错。$\mathbb R$ 与 $S^1$ 有同一一维 abelian algebra但 global topology 不同。

## A02 解答：六组概念

Abstract group 只要 algebraic law；topological group 还要求 multiplication/inverse continuous；Lie group 要 smooth finite-dimensional manifold 且两 map smooth；matrix Lie group 是 $GL(n)$ 的 closed subgroup这一可计算实现。

Subgroup 只需群公理；normal subgroup还满足 conjugation invariant以构造 quotient group；Lie subgroup还需 compatible immersed/embedded manifold structure。Closed subgroup theorem使 closed subgroup 自动 embedded。

Action 性质：free 要每个 stabilizer trivial；effective 只要所有 stabilizers 的交 trivial；transitive 表示单一 orbit；proper 控制 quotient/stabilizer 的全局良性。$SO(3)$ 作用 $S^2$：任意两单位向量可旋转相连，故 transitive；固定全部向量的 rotation 只有 $I$，故 effective；但固定 north pole 的所有绕 $z$ 轴 rotations 形成 $SO(2)$，故不 free。

Coordinate change 是同一对象的被动重表达；global symmetry 用同一 $g$ 主动作用全部 points；gauge transformation允许 $g(x)$ 随位置变。Input/output symmetry规定 predictor关系；parameter symmetry保持同一 represented function。Exact equivariance是全量词 theorem；numerical approximate 是 sampled residual；empirical robustness是 performance statement。

## A03 解答：五个 symmetry contracts

1. **Rotated-image classification**：$X$ 是 sampled images，候选 $G=SO(2)$ 或 discrete $C_4$，action含空间 resampling，label用 trivial rep。若 crop/background/orientation本身含类别信息，则 full invariance错；grid interpolation使 continuous rotation只 approximate。
2. **3D energy/force**：points受 $E(3)$ 或 $SE(3)$ action。Energy scalar invariant；forces按 $f_i\mapsto Rf_i$ equivariant且 translation invariant。Chiral任务不能随意加入 reflection；neighbor cutoff和periodic boundary需审计。
3. **Set classification**：$G=S_n$ 作用 index rows，output trivial；sum/mean pooling invariant。若 multiplicity/size重要，mean可能抹去 cardinality。
4. **Causal LM**：token indices有 total/causal order，arbitrary permutation不是 symmetry。无 position attention虽对同步 permutation equivariant，但 causal mask/encoding明确破缺 $S_n$；这是正确 inductive bias。
5. **ReLU rescaling**：action在 parameters，$(W_1,W_2)\mapsto(cW_1,c^{-1}W_2)$，represented function不变；它造成 non-identifiability，不要求 input/output随 $c$ 变。

## B01 解答：SO(2)

取 $Q(0)=I,\dot Q(0)=A$。对 $Q^\top Q=I$ 求导：

$$A^\top+A=0.$$

二维 skew matrix 必为 $A=\theta J$。因 $J^{2k}=(-1)^kI$、$J^{2k+1}=(-1)^kJ$，

$$e^{\theta J}=I\sum_k\frac{(-1)^k\theta^{2k}}{(2k)!}
+J\sum_k\frac{(-1)^k\theta^{2k+1}}{(2k+1)!}
=I\cos\theta+J\sin\theta.$$

同一生成元 commute，故指数加法律成立；直接由三角公式也得 $R(a)R(b)=R(a+b)$，inverse 为 $R(-\theta)$。

$$d\exp_0(aJ)=\left.\frac d{dt}\right|_0e^{taJ}=aJ,$$

所以是 identity under $T_0\mathfrak g\cong\mathfrak g$。Kernel 为 $\{2\pi kJ:k\in\mathbb Z\}$，故非 injective。

Local log 可取 angle $\theta=\operatorname{atan2}(R_{21},R_{11})\in(-\pi,\pi)$。在 $-I=R(\pi)$ 处 $\pi$ 与 $-\pi$ 接缝，不能有覆盖整圆的连续单值角度。Standard bi-invariant metric 下，$t\mapsto R(t\theta)$ 是从 $I$ 出发的 Riemannian geodesic，故两 exp 在 $I$ 一致；这依赖 metric。

## B02 解答：SO(3)、hat 与 BCH 首项

按分量计算：

$$\widehat\omega v=
(\omega_2v_3-\omega_3v_2,
\omega_3v_1-\omega_1v_3,
\omega_1v_2-\omega_2v_1)^\top
=\omega\times v.$$

对任意 $v$，用 vector triple product：

$$[\widehat\omega,\widehat\nu]v
=\omega\times(\nu\times v)-\nu\times(\omega\times v)
=(\omega\times\nu)\times v,$$

故 commutator 为 $\widehat{\omega\times\nu}$。

单位 $u$ 时

$$\widehat u^2v=u\times(u\times v)=u(u^\top v)-v,$$

所以 $\widehat u^2=uu^\top-I$，再乘 $\widehat u$ 得 $\widehat u^3=-\widehat u$。指数级数把奇偶幂归并为

$$e^{\theta\widehat u}
=I+\sin\theta\widehat u+(1-\cos\theta)\widehat u^2.$$

对 $X=a\widehat e_1,Y=a\widehat e_2$，

$$[X,Y]=a^2\widehat{e_1\times e_2}=a^2\widehat e_3.$$

二阶展开给

$$e^Xe^Y-e^{X+Y}=\tfrac12[X,Y]+O(a^3).$$

$\theta=0$ 时 axis不识别但 rotation平滑；$\pi$ 时 $u$ 与 $-u$ 的表示在 branch边界粘合，log敏感；$2\pi$ 回到 identity说明 global noninjectivity。数值上小角用 sinc series，$\pi$ 附近避免只从 skew part除以 $\sin\theta$。

## B03 解答：SE(2)

Matrix product 给

$$
(R_1,t_1)(R_2,t_2)
=(R_1R_2,R_1t_2+t_1),
$$

$$
(R,t)^{-1}=(R^\top,-R^\top t).
$$

Translation $N=\{(I,t)\}$ 满足

$$
(R,a)(I,t)(R,a)^{-1}=(I,Rt)\in N,
$$

故 normal。反之

$$
(I,a)(R,0)(I,-a)=(R,a-Ra),
$$

一般带非零 translation，不在 embedded rotation subgroup，故后者不 normal。

单位元曲线求导得

$$
\mathfrak{se}(2)=
\left\{
\begin{bmatrix}\omega J&v\\0&0\end{bmatrix}
:\omega\in\mathbb R,v\in\mathbb R^2
\right\}.
$$

令 $\xi=(\omega,v),\eta=(\alpha,w)$，block multiplication 得

$$[\xi,\eta]=(0,\omega Jw-\alpha Jv).$$

Cross term $Rt$ 说明 composition中 rotation作用 translation，所以是 $SO(2)\ltimes\mathbb R^2$ 而非 componentwise direct product。对 point action $Rx+t$，generator是

$$\xi_X(x)=\omega Jx+v.$$

Origin stabilizer是所有 $(R,0)\cong SO(2)$。任意固定 $x\ne0$ 的 rigid motions满足 $t=x-Rx$，仍同构于 $SO(2)$；若只让 rotation subgroup作用，则非零点 stabilizer通常只有 identity。

## C01 解答：从 translation 到 Ad/ad

$L_{g^{-1}}L_g=L_e=id$，且 multiplication smooth，所以 $L_g$ 是 diffeomorphism；right translation同理。

给 $\xi\in T_eG$ 定义 $X_\xi(g)=(dL_g)_e\xi$。Chain rule与 $L_hL_g=L_{hg}$ 给 left invariance。若 $X$ left invariant，则 $X(g)=(dL_g)_eX(e)$，故唯一。

Diffeomorphism pushforward保持 vector-field bracket：

$$\phi_*[X,Y]=[\phi_*X,\phi_*Y].$$

取 $\phi=L_g$，left-invariant $X,Y$ 的 bracket仍 left invariant。因此在 $e$ 取值定义 $[\xi,\eta]$，bilinearity、antisymmetry、Jacobi继承自 vector-field bracket。

Matrix group中 left-invariant field为 $X_A(g)=gA$。对 coordinate functions直接求导，

$$[X_A,X_B](g)=g(AB-BA),$$

故在 $e=I$ 得 commutator。

$C_{gh}=C_g\circ C_h$，chain rule at $e$ 给

$$\operatorname{Ad}_{gh}=\operatorname{Ad}_g\operatorname{Ad}_h.$$

Matrix case $\operatorname{Ad}_{e^{tX}}Y=e^{tX}Ye^{-tX}$，在 $0$ 求导：

$$\operatorname{ad}_X(Y)=XY-YX=[X,Y].$$

## C02 解答：generator criterion

Global relation为

$$F(\exp(t\xi)\cdot x)=\exp(t\xi)\cdot F(x).$$

在 $t=0$ 求导，左侧 chain rule给 $dF_x(\xi_X(x))$，右侧按 generator定义给 $\xi_Y(F(x))$。每个 basis generator $\xi_a$ 给一条 first-order differential constraint；对 linear actions $\xi_X(x)=A_\xi x$、$\xi_Y(y)=B_\xi y$：

$$J_F(x)A_\xi x=B_\xi F(x).$$

反向令

$$H(t)=F(\exp(t\xi)\cdot x),\qquad
K(t)=\exp(t\xi)\cdot F(x).$$

Generator identity使二者满足相同由 $Y$ 上 generator给出的 ODE且初值相同；在 local uniqueness与domain存在条件下 $H=K$。Connected group中若每个元素可写为有限个 exponentials的乘积，逐段得到 identity-component equivariance。

所需条件包括 actions/F smooth、generator identity全域成立、ODE existence/uniqueness、orbit不离开domain。$O(1)=\{\pm1\}$ 的 algebra为 $0$，任何 $F$ 都满足空条件，但 $F(x)=x+1$ 不满足 even invariance或 odd equivariance。数值 audit应同时：对 algebra basis比较 Jacobian-vector generator residual；对每个 disconnected component选 representative（如 reflection）比较 finite residual。

## C03 解答：Reynolds projector

记 $P=\mathcal P(L)$。对 $h\in G$：

$$
P\rho_X(h)
=\frac1{|G|}\sum_g\rho_Y(g^{-1})L\rho_X(gh).
$$

令 $k=gh$，则 $g^{-1}=hk^{-1}$，故

$$P\rho_X(h)=\rho_Y(h)
\frac1{|G|}\sum_k\rho_Y(k^{-1})L\rho_X(k)
=\rho_Y(h)P.$$

所以 $P$ equivariant。若 $L$ 已 equivariant，则每项

$$\rho_Y(g^{-1})L\rho_X(g)=L,$$

故 $\mathcal P(L)=L$。第一次投影后已 equivariant，因此 $\mathcal P^2=\mathcal P$。

对 Frobenius inner product，orthogonal representations满足 $\rho^{-1}=\rho^\top$。利用 trace循环性和变量 $g\leftrightarrow g^{-1}$：

$$\langle\mathcal P(A),B\rangle_F
=\langle A,\mathcal P(B)\rangle_F.$$

Self-adjoint idempotent正是 orthogonal projector，其 image是 fixed points，即 intertwiners。

对 cyclic shift $S$，intertwiner满足 $LS=SL$。因 $e_j=S^je_0$，

$$Le_j=LS^je_0=S^jLe_0,$$

故 columns是 cyclic shifts，$L$ circulant；反向 circulant matrix显然 commute。只取部分 group elements的 sample set通常不在 left multiplication下封闭，变量替换无法把和变回自身，所以不 exact。Compact group把和换 normalized Haar integral；noncompact group没有 normalized finite Haar probability，full uniform average不可定义为有限均值。

## D01 解答：七个全局反例

1. $\mathbb R$（simply connected、noncompact）与 $S^1$（compact）都有 algebra $\mathbb R$、零 bracket，但 groups不同构。
2. $\exp:\mathbb R J\to SO(2)$ 以 $2\pi J$ 为周期。
3. 在 $SL(2,\mathbb R)$ 中，matrix exponential若有两个 distinct negative real eigenvalues会与 real logarithm的必要谱条件冲突；例如 $\operatorname{diag}(-2,-1/2)\in SL(2,\mathbb R)$ 不是真实 $2\times2$ matrix exponential。它仍在 connected $SL(2,\mathbb R)$ 中，说明 connected不保证单个 exponential surjective。（群元素可由多个 exponentials生成是另一命题。）
4. $X=a\widehat e_1,Y=a\widehat e_2$ 有 $[X,Y]=a^2\widehat e_3\ne0$，二阶展开即否定等式。
5. $SO(3)$ 作用 $S^2$ transitive，但 point stabilizer $SO(2)$ 非平凡。
6. “Faithful”常修饰 homomorphism/representation的 kernel trivial；“effective”常修饰 action且全局 kernel trivial。二者数学条件对应，但“free”要求每点 stabilizer trivial，不能替代。
7. $O(1)$ algebra为零；$F(x)=x+1$ 自动通过所有 infinitesimal checks，却既非 even invariant也不满足 $F(-x)=-F(x)$。

缺失条件依次是 global topology、injectivity domain、surjectivity theorem、commutativity、trivial stabilizer、术语对象、connected-component coverage。

## D02 解答：grid equivariance

Circular case按指标：

$$
(K*T_kx)[u]=\sum_vK[v]x[u-v-k]
=(T_k(K*x))[u].
$$

Zero-padding最小例：长度3，kernel $[1,1,1]$，$x=(1,0,0)$。向右shift并补零后 $T x=(0,1,0)$。Same-padding outputs分别为 $(1,1,0)$ 与 $(1,1,1)$，而 shift前者为 $(0,1,1)$，不等。

Stride-2若定义为先 equivariant convolution再采偶数格，只对偶数 shifts自然对应 output integer shift；奇数 shift改变 sampling phase。Arbitrary rotation不把 square lattice映回自身，需 interpolation；插值 kernel、boundary与aliasing造成 residual。因此 continuous $SO(2)$ theorem不能直接宣称 sampled operator exact。

Report应分 interior/boundary，列每个 transform angle/shift的 relative residual，给 mean、high quantile与max，并扫描 resolution/interpolation/precision。只报平均会隐藏少数 angles、corners或large-amplitude inputs上的灾难性误差。

## D03 解答：三种 enforcement

Exact architecture把 function class限制在 equivariant maps；推理通常无需多次变换，但 layer/kernel/feature-type设计复杂。Full group average $\bar F(x)=\int\rho_Y(g)^{-1}F(\rho_X(g)x)d\mu(g)$ 把任意 predictor symmetrize，对 compact group exact但计算昂贵；Monte Carlo only approximate，noncompact group无 uniform probability。Augmentation只对 sampled risk施压，最灵活但不提供 pointwise guarantee。

错误 invariance例：$x\in\{-1,1\}$、group sign flip、label $y=x$。任何 invariant predictor满足 $F(1)=F(-1)=c$，squared risk均匀分布下

$$\tfrac12[(c-1)^2+(c+1)^2]=c^2+1\ge1,$$

而 unrestricted $F(x)=x$ risk为0。

Labels invariant但 augmentation不 exact例：$y=x^2$，训练只采有限 $x$ 和有限 transformations；高容量 model可在这些 points拟合同时在未采点违反 $F(-x)=F(x)$。即使随机 augmentation，finite optimization/sample只给经验约束。

## E01 解答：attention 的 permutation law

令 $X\in\mathbb R^{n\times d}$，$W_Q\in\mathbb R^{d\times d_k}$、$W_K$ 同形、$W_V\in\mathbb R^{d\times d_v}$。对 permutation matrix $P$：

$$Q'=PXW_Q=PQ,\quad K'=PK,\quad V'=PV.$$

Score

$$A'=Q'K'^\top/\sqrt{d_k}=PA P^\top.$$

Row-softmax分量为

$$[\sigma(A)]_{ij}=\frac{e^{A_{ij}}}{\sum_\ell e^{A_{i\ell}}}.$$

$PAP^\top$ 同时重排行列，denominator也按同一 row内重排，故

$$\sigma(PAP^\top)=P\sigma(A)P^\top.$$

于是

$$\operatorname{Attn}(PX)
=P\sigma(A)P^\top PV
=P\operatorname{Attn}(X).$$

Multi-head若各头相同按 token维作用并在 channel维concat仍保持；shared pointwise MLP、residual与per-token LayerNorm也 commute。若 normalization跨 token且使用非 symmetric position-dependent权重则未必。

Full output是 equivariant；固定 query且只同步重排 key-value pairs时该 query output invariant；symmetric pooling后classification invariant。Causal mask不在任意 conjugation下保持，选择order；absolute encoding绑定indices；relative bias可对joint translations相容；RoPE用position-difference representation，但都破除 arbitrary $S_n$ symmetry。

## E02 解答：RoPE

因 $J$ 与自身 commute，

$$R(m+n)=e^{(m+n)\theta J}=e^{m\theta J}e^{n\theta J}=R(m)R(n).$$

$J^\top=-J$，所以 $R(m)^\top=R(-m)$，进而

$$R(m)^\top R(n)=R(n-m).$$

多频率时

$$R(m)=\operatorname{diag}(R_{\theta_1}(m),\ldots,R_{\theta_r}(m)),$$

每个 block满足 representation law，direct sum亦满足。

二维位置可取 commuting block generators $A,B$，定义

$$R(x,y)=e^{xA+yB}=e^{xA}e^{yB},\qquad[A,B]=0.$$

若不 commute，$e^{xA+yB}\ne e^{xA}e^{yB}$，BCH给额外 $\tfrac12xy[A,B]+\cdots$；坐标平移 representation law也可能失败。

Periodicity会让不同长距离positions产生相同/近似phase；频率离散和浮点 argument reduction会积累误差。Algebraic实验可逐点验证 $\|R(m)^TR(n)-R(n-m)\|$；downstream实验另比较attention logits/output，在相同 relative offsets但不同 absolute positions、不同长度/precision下测误差与performance。前者成立不推出后者泛化。

## E03 解答示例：chiral molecule 的 SE(3) 设计

选择 $SE(3)$ 而非 $E(3)$：translation/rotation是 nuisance，但 enantiomers可能有不同目标，不能强制 reflection同一。Atoms输入含 position vectors与element scalars；intermediate features按 $SO(3)$ irreducible scalar/vector/tensor types变换；energy output scalar invariant，forces为 polar vectors且可由 $-\nabla_xE$ 得到 equivariance与energy conservation接口。

Linear layers必须是 intertwiners；tensor products按 Clebsch–Gordan规则组合，scalar-gated nonlinearity要保持 type，invariant readout聚合 atom scalars。Local frame若被显式选取要审计 gauge dependence；更安全是直接以 relative vectors/irreps组织。

三层证据：

1. 符号证明每个 layer、cutoff、aggregation与readout commute；
2. 数值对 random rotations/translations和单独 reflections报告 per-layer/end-to-end residual、precision与neighbor-list变化；
3. 数据集上比较 accuracy/force error、rotation augmentation baseline、错误 $E(3)$ model与non-equivariant baseline，多 seeds给 uncertainty。

Neighbor graph cutoff在距离基础上可 rigid-invariant，但阈值附近浮点/skin update会改变edges；periodic cell、minimum image convention与batch centering要列入。错误 symmetry baseline预计在区分 enantiomers时出现 irreducible bias。

Parameter hidden-channel permutations/rescalings会产生函数相同的 parameter orbits、Hessian/Fisher zero/near-zero modes，影响 optimization和Laplace uncertainty；它们作用在 parameter space，不是 molecule的 $SE(3)$ action，故不能作为 data equivariance proof。

## 最终核对表

完成后应能独立重建：

- $\mathfrak{so}(n)$ 的 tangent constraint与 SO(2)/SO(3) exponential；
- BCH 二阶 commutator correction；
- orbit–stabilizer与 $S^2\cong SO(3)/SO(2)$；
- Reynolds operator 的 equivariant、idempotent、orthogonal-projector证明；
- circular convolution converse与 boundary反例；
- attention permutation equivariance和 RoPE relative law；
- Lie algebra只检查 identity component；
- exact、numerical与empirical三层 symmetry claim。

> [!important] 状态不自动升级
> 解答文档存在只表示验收工具已 `composed`。没有首次闭卷原稿、错误分类、48 小时重做、14 天迁移与实验改参，本节点仍是 `draft / not-attempted`。
