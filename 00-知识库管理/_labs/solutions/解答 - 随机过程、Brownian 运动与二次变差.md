---
type: solution
status: draft
area: [math/probability, math/stochastic-processes, math/sde, ai/generative-modeling]
topic: "随机过程、Brownian 运动与二次变差"
exercise: "[[习题 - 随机过程、Brownian 运动与二次变差]]"
related: ["[[随机过程、Brownian 运动与二次变差]]", "[[ODE、动力系统与 SDE MOC]]", "[[练习与测验 MOC]]", "[[实验 - Brownian 增量、路径粗糙性与时间耦合审计]]"]
created: 2026-08-19
updated: 2026-08-19
---

# 解答 - 随机过程、Brownian 运动与二次变差

> [!important] 判断顺序
> 先写过程的共同概率空间与跨时间联合律，再写 filtration；随后区分 marginal、FDD、path law 与 sample path。任何二次变差结论都必须附 partition 和 convergence mode。AI 迁移最后才讨论，不可用“每个时刻分布正确”越级替代过程证据。

## A. 定义、对象与合同

### DYN-BM-A01

对象表：

| 对象 | 数学角色 | 不能替代 |
|---|---|---|
| $(\Omega,\mathcal F,\mathbb P)$ | 共同随机实验 | 单个 seed 字符串 |
| $I,E$ | time index 与 state space | 数组 shape 的口头描述 |
| $X_t$ | 固定 $t$ 的随机变量 | 整条 path law |
| $t\mapsto X_t(\omega)$ | 固定样本的轨迹 | marginal density |
| marginal | $\mathcal L(X_t)$ | multi-time dependence |
| FDD | 任意有限 $(X_{t_1},\ldots,X_{t_n})$ 的 law | 自动连续路径 |
| transition kernel | 从现在到未来的条件 law | 任意 non-Markov 过程的完整历史 law |
| path law | 函数空间上的概率测度 | 单条可视化曲线 |
| filtration | 到时刻 $t$ 可用的信息 | 仅数值时间戳 |
| adapted | $X_t$ 不使用未来信息 | independent increments |
| stopping time | 是否已发生可由当前信息判断 | 依赖未来的最后发生时刻 |
| martingale | 条件均值保持 | constant unconditional mean |

Modification 对每个固定 $t$ almost surely相同，异常集可依赖 $t$；indistinguishability 要求一个概率1事件上所有时刻同时相同。

连续表示 path topology；càdlàg 表示右连续且有左极限；$\alpha$-Hölder 控制

$$
|X_t-X_s|\le C|t-s|^\alpha;
$$

finite variation 控制所有 partitions 上绝对增量总和。

反例取

$$
B_t=W_t,
\qquad
S_t=\sqrt t\,Z,
$$

其中 $Z\sim\mathcal N(0,1)$。固定 $t$ 时都有

$$
B_t,S_t\sim\mathcal N(0,t).
$$

但对 $s<t$，

$$
\operatorname{Cov}(B_s,B_t)=s,
$$

$$
\operatorname{Cov}(S_s,S_t)=\sqrt{st}.
$$

只要 $s<t$，二者通常不同。逐时 histogram只估计 diagonal marginal，无法估计 cross-time covariance，故区分不了。

### DYN-BM-A02

Standard Brownian contract：

1. $W_0=0$ almost surely；
2. 不重叠 increments 相互独立；
3. $W_t-W_s\sim\mathcal N(0,t-s)$；
4. paths almost surely continuous。

Claim ladder 的逻辑：

- $W_t\sim\mathcal N(0,t)$ 只给 marginals；
- stationary Gaussian increments给每个 increment law，但若未给 joint Gaussian/独立性，仍可能跨区间相关；
- independent stationary Gaussian increments加 $W_0=0$ 决定 Brownian FDD；
- zero-mean Gaussian process加
  $$
  K(s,t)=\min(s,t)
  $$
  也决定 Brownian FDD，因为不重叠 increments covariance为0，而 joint Gaussian 下 uncorrelated 等价 independent；
- FDD contract 不自动给所选 realization 的连续性；需 continuity theorem/continuous modification；
- nowhere differentiability、Hölder threshold和quadratic variation是更强 almost-sure path theorems；
- martingale/Markov 还必须相对于指定 filtration；
- strong Markov把 deterministic time 的 restart 提升到 stopping time，需 usual conditions等正式定理。

Levels相关：

$$
\operatorname{Cov}(W_s,W_t)=s
$$

是因为 $W_t$ 含有过去 $W_s$。不重叠 increments

$$
W_t-W_s,\qquad W_v-W_u,\quad t\le u
$$

没有共享 Gaussian increment，故独立。

Usual augmentation补入零集并使 filtration right-continuous，保证 stopping-time 与 optional/strong-Markov结论采用标准版本。它不改变常规 fixed-time FDD，却会影响信息结构的技术完备性。

### DYN-BM-A03

一份合格 card 可写为：

~~~text
STATE / TIME
  X_t in R^d, t in [0,T], physical time unit

MARGINAL
  q_t(x_t | x_0), alpha_t, sigma_t, endpoint laws

PROCESS
  transition q_{s,t}, Markov/non-Markov
  forward filtration and adapted coefficients
  path space C or D, continuity claim

LOCAL NOISE
  E[dX | F_t] = b dt
  Cov(dX | F_t) = a dt
  factor g with gg^T=a
  cross-component and cross-device policy

DISCRETE
  dX = b_k dt + g_k sqrt(dt) Z_k
  grid, PRNG, key splitting, dtype
  fine/coarse Brownian coupling

TRAIN / SAMPLE
  marginal noising samples used in loss
  learned score/field object
  reverse SDE or probability-flow ODE
  solver, NFE, tolerance

AUDIT
  marginal moments, transition covariance
  disjoint-increment covariance, cross variation
  pathwise/weak/endpoint metrics
~~~

每个 noise level 的 Gaussian histogram只能支持

$$
\mathcal L(X_t)\approx q_t.
$$

它没有验证

$$
\mathcal L(X_s,X_t),
\qquad
\mathcal L(X_t\mid X_s),
$$

也没有验证 adaptedness、increment independence、reverse dynamics或numerical rollout。因此不能推出过程正确。

## B. 联合 Gaussian、条件分布与随机游走

### DYN-BM-B01

对 $0<s<t<u$，

$$
\begin{pmatrix}W_s\\W_t\\W_u\end{pmatrix}
\sim\mathcal N\left(
0,
\begin{bmatrix}
s&s&s\\
s&t&t\\
s&t&u
\end{bmatrix}
\right).
$$

不重叠 increments 的 covariance：

$$
\begin{aligned}
&\operatorname{Cov}(W_t-W_s,W_u-W_t)\\
&=\operatorname{Cov}(W_t,W_u)
-\operatorname{Var}(W_t)
-\operatorname{Cov}(W_s,W_u)
+\operatorname{Cov}(W_s,W_t)\\
&=t-t-s+s=0.
\end{aligned}
$$

它们 joint Gaussian，故 covariance为0进一步推出独立。

Gaussian conditioning：

$$
\boxed{
W_t\mid W_u=b
\sim
\mathcal N\left(\frac tu b,\frac{t(u-t)}u\right).
}
$$

令 $D=W_t-W_s$。有

$$
\operatorname{Var}(D)=t-s,
\qquad
\operatorname{Cov}(D,W_u)=t-s.
$$

所以

$$
\boxed{
D\mid W_u=b
\sim
\mathcal N\left(
\frac{t-s}{u}b,
(t-s)-\frac{(t-s)^2}{u}
\right).
}
$$

Martingale：

$$
W_u=W_t+(W_u-W_t),
$$

未来增量独立于 $\mathcal F_t$ 且均值0，因此

$$
\mathbb E[W_u\mid\mathcal F_t]=W_t.
$$

又

$$
W_u^2
=W_t^2+2W_t\Delta W+(\Delta W)^2.
$$

条件期望后

$$
\mathbb E[W_u^2-u\mid\mathcal F_t]
=W_t^2+(u-t)-u
=W_t^2-t.
$$

数值取 $s=1/4,t=1/2,u=1,b=2$：

$$
\Sigma=
\begin{bmatrix}
0.25&0.25&0.25\\
0.25&0.5&0.5\\
0.25&0.5&1
\end{bmatrix}.
$$

$$
W_{1/2}\mid W_1=2
\sim\mathcal N(1,0.25).
$$

$$
W_{1/2}-W_{1/4}\mid W_1=2
\sim\mathcal N(0.5,0.1875).
$$

Bridge conditional mean是 $2t$，但在 $t=1/2$ conditional variance仍为0.25，因此不是确定性直线。

### DYN-BM-B02

对

$$
X_t=aW_{bt},
$$

increment variance为

$$
\operatorname{Var}(X_t-X_s)
=a^2b(t-s).
$$

所以

$$
\boxed{a^2b=1}
$$

时 $X$ 是标准 Brownian；$a$ 可正可负，负号由反射对称处理。

$$
Y_t=W_{t+c}-W_c
$$

具有从0开始的stationary independent Gaussian increments和连续路径，故是 Brownian，并且整个未来增量过程与 $\mathcal F_c$ 独立。

$$
R_t=W_T-W_{T-t}
$$

在 $[0,T]$ 上有 Brownian law。可是对 $t<T$，$R_t$ 使用 $W_T$，一般不对原 forward filtration $\mathcal F_t$ adapted。若要作反向过程，必须定义reverse filtration。

对

$$
Z_t=LW_t+\mu t,
$$

$$
Z_t-Z_s
\sim\mathcal N\left(
\mu(t-s),(t-s)LL^\top
\right).
$$

若 $Q$ 正交，则

$$
(LQ)(LQ)^\top=LL^\top,
$$

所以 $LQW$ 与 $LW$ 的 process law相同。但若 $W$ 还与别的变量共享 coupling，旋转 noise coordinates 会改变joint coupling，不能由单独 law 等价推出整个程序等价。

量纲：若 $t$ 有时间单位，$W_t$ 有 $\sqrt{\text{time}}$ 单位；$\mu$ 是 state/time，$L$ 是 state/$\sqrt{\text{time}}$。纯 time-rescaling中的 $b$ 是将模型时间映到 Brownian clock 的比例，$a$ 补偿其平方根。

### DYN-BM-B03

$$
\mathbb E[X_t^{(n)}]=0,
$$

$$
\operatorname{Var}(X_t^{(n)})
=n^{-2\gamma}\lfloor nt\rfloor
\sim t\,n^{1-2\gamma}.
$$

因此：

- $\gamma>1/2$：方差趋0，退化；
- $\gamma<1/2$：方差发散；
- 只有
  $$
  \boxed{\gamma=1/2}
  $$
  给非退化极限。

固定 $t$ 时 CLT 给

$$
X_t^{(n)}\Rightarrow\mathcal N(0,t).
$$

对 $s<t$，

$$
\operatorname{Cov}(X_s^{(n)},X_t^{(n)})
=\frac{\lfloor ns\rfloor}{n}
\to s=\min(s,t).
$$

借 Cramér–Wold 可把这一思路扩展为 FDD convergence，但仍需 tightness 才能得到 path-space convergence。

阶梯插值自然位于 càdlàg space $D([0,T])$；分段线性插值位于 $C([0,T])$。Donsker theorem陈述这些缩放随机游走的 path laws 在相应 topology下 weakly converge 到 Brownian law。

不过界的说法是：

> 均值0、方差1且满足相应条件的 i.i.d. 随机游走，在 diffusive space–time scaling 和指定插值/函数空间拓扑下，其 path law weakly converges 到 Brownian motion。

它不是说任意有限网格随机游走路径等于某条 Brownian path。

## C. 二次变差、有限变差与信息流推导

### DYN-BM-C01

记

$$
\Delta_iW\sim\mathcal N(0,\Delta_it).
$$

于是

$$
\mathbb E[(\Delta_iW)^2]=\Delta_it,
$$

所以

$$
\mathbb E[Q_\Pi]=\sum_i\Delta_it=T.
$$

Gaussian fourth moment给

$$
\operatorname{Var}((\Delta_iW)^2)
=2(\Delta_it)^2.
$$

平方增量独立，因此

$$
\operatorname{Var}(Q_\Pi)
=2\sum_i(\Delta_it)^2
\le2T|\Pi|.
$$

故

$$
\mathbb E[(Q_\Pi-T)^2]\to0,
$$

即 $Q_\Pi\to T$ in $L^2$。

Uniform $n$-partition下：

$$
\operatorname{Var}(Q_n)
=n\cdot2(T/n)^2
=\frac{2T^2}{n},
$$

$$
\boxed{
\operatorname{RMSE}(Q_n)
=T\sqrt{2/n}.
}
$$

Dyadic $n=2^m$ 时：

$$
\mathbb P(|Q_{2^m}-T|>\varepsilon)
\le
\frac{2T^2}{\varepsilon^2\,2^m}.
$$

关于 $m$ 求和有限，Borel–Cantelli给

$$
Q_{2^m}\to T
\quad a.s.
$$

若 partition依赖路径，increments的区间端点成为随机，独立性和

$$
\Delta_iW\sim\mathcal N(0,\Delta_it)
$$

不能不加 stopping-time/optional-sampling条件直接使用。

单步

$$
(\Delta_iW)^2
=\Delta_it\,Z_i^2
$$

不是 $\Delta_it$；只是 $Z_i^2$ 的均值为1，许多独立项累计后其波动消失。

Uniform grid上

$$
\mathbb E|\Delta_iW|
=\sqrt{\frac{2T}{\pi n}}.
$$

因此

$$
\boxed{
\mathbb E\sum_{i=1}^n|\Delta_iW|
=\sqrt{\frac{2nT}{\pi}},
}
$$

按 $\sqrt n$ 增长。

### DYN-BM-C02

若连续 $x$ 的 total variation有限，

$$
\sum_i(\Delta_ix)^2
\le
\max_i|\Delta_ix|
\sum_i|\Delta_ix|.
$$

后一和不超过 $\operatorname{TV}(x)$；一致连续性使前一最大值随mesh趋0。因此平方和趋0。

Brownian dyadic quadratic variation almost surely趋于 $T>0$，与有限变差所需的0冲突，故

$$
\operatorname{TV}_{[0,T]}(W)=\infty
\quad a.s.
$$

这只排除整段有限变差；它没有单独分析每一点差商，故不等于完整 nowhere-differentiability proof。

令 $W,B$ 独立 Brownian：

$$
C_\Pi=\sum_i\Delta_iW\,\Delta_iB.
$$

每项均值0，不同项独立，且

$$
\operatorname{Var}(\Delta_iW\,\Delta_iB)
=(\Delta_it)^2.
$$

所以

$$
\mathbb E[C_\Pi^2]
=\sum_i(\Delta_it)^2
\le T|\Pi|\to0.
$$

即 $[W,B]_T=0$ in $L^2$。

相关二维 Brownian可写

$$
W_t^{(2)}
=\rho W_t^{(1)}
+\sqrt{1-\rho^2}B_t,
$$

于是

$$
[W^{(1)},W^{(2)}]_t
=\rho[W^{(1)}]_t
+\sqrt{1-\rho^2}[W^{(1)},B]_t
=\rho t.
$$

若 $X=LW$，

$$
\boxed{
[X]_t=tLL^\top.
}
$$

Quadratic variation固定一列细分并取极限；$2$-variation对所有partitions平方和取supremum。Brownian前者为 $t$，后者 almost surely无限。

若两个声称独立的components复用同一 increments，则 realized cross variation趋近 $t$ 而非0；若部分相关，则趋近相应 $\rho t$。

### DYN-BM-C03

$W_t$ 是

$$
\mathcal F_t^W=\sigma(W_r:r\le t)
$$

的生成变量之一，故 adapted。

对 $s<t$，

$$
W_t=W_s+(W_t-W_s),
$$

未来增量独立于 $\mathcal F_s$ 且均值0，所以

$$
\mathbb E[W_t\mid\mathcal F_s]=W_s.
$$

类似地，

$$
\begin{aligned}
\mathbb E[W_t^2-t\mid\mathcal F_s]
&=W_s^2+\mathbb E[(W_t-W_s)^2] -t\\
&=W_s^2+(t-s)-t\\
&=W_s^2-s.
\end{aligned}
$$

对连续 adapted $W$，

$$
\{\tau_a\le t\}
=\left\{\sup_{0\le r\le t}W_r\ge a\right\}
$$

在适当方向/起点下是 $\mathcal F_t$-measurable，故首次到达是 stopping time。

“$T$ 前最后一次过0”要知道 $t$ 之后直到 $T$ 是否还会过0，通常不是 forward stopping time。

均值恒定但非martingale：令 $Z$ 是均值0、非退化随机变量，并令全部时刻 filtration都已知 $Z$，

$$
X_t=tZ.
$$

虽然 $\mathbb E[X_t]=0$ 对所有 $t$，

$$
\mathbb E[X_t\mid\mathcal F_s]
=tZ\ne sZ=X_s.
$$

Independent increments约束不同时间段的随机创新；Markov约束给定当前后未来条件law；martingale只约束给定当前信息后的未来条件均值。三者不能互换。

若时刻 $t$ 的网络读取未来噪声 key，则输出不再对 forward filtration adapted，因果/stochastic-integral合同被破坏。

## D. 复现、失败注入与数值判断

### DYN-BM-D01

标准复现结果见[[实验 - Brownian 增量、路径粗糙性与时间耦合审计]]。应按以下账本解释：

1. $\widehat{\operatorname{Var}}(W_t)$ 的误差是有限 path count 的 Monte Carlo error；
2. covariance kernel同样受样本误差，但理论离散 Brownian grid本身在网格点是 exact FDD；
3. disjoint increment covariance应接近0，其标准误差约随 $M^{-1/2}$；
4. realized $Q_n$ 对单路径随机，ensemble mean应接近1；
5. $Q_n$ 的 RMSE相对1按 $n^{-1/2}$；
6. total variation mean按 $n^{1/2}$；
7. 非均匀 deterministic partitions仍有 $L^2$ convergence，误差由最大mesh控制；
8. 若不同 $n$ 使用independent paths，跨resolution单路径difference不是纯partition error。

对 $T=1$，理论基准是

$$
\mathbb E[Q_n]=1,
\qquad
\operatorname{RMSE}(Q_n)=\sqrt{2/n},
$$

$$
\mathbb E[\operatorname{TV}_n]
=\sqrt{2n/\pi}.
$$

换 seed 后单项会变化，但 normalized slope、均值置信范围与理论缩放应稳定。增加 path count主要减 Monte Carlo error；增加 $n$ 改变 partition approximation与单路径 variation。

### DYN-BM-D02

三者 fixed-time都满足

$$
B_t,S_t,I_t\sim\mathcal N(0,t).
$$

Brownian：

$$
\mathbb E[(B_{t_0+h}-B_{t_0})^2]=h.
$$

Shared noise：

$$
\begin{aligned}
\mathbb E[(S_{t_0+h}-S_{t_0})^2]
&=(\sqrt{t_0+h}-\sqrt{t_0})^2\\
&=\frac{h^2}{(\sqrt{t_0+h}+\sqrt{t_0})^2}\\
&\sim\frac{h^2}{4t_0}.
\end{aligned}
$$

Independent-time：

$$
\mathbb E[(I_{t_0+h}-I_{t_0})^2]
=(t_0+h)+t_0
=2t_0+h.
$$

因此 log-log orders分别是1、2、0。

$B$ 与 $S$ mean-square continuous；$I$ 在 $t_0>0$ 处不是，因为 increment second moment不趋0。若存在continuous modification，则必然stochastically continuous，进而mean-square结论在此Gaussian二阶有界情形下冲突；所以没有continuous Gaussian modification。

只有 $B$ 具有 Brownian independent increments。$S_t=\sqrt tZ$ 在任意 $[\varepsilon,T]$ 上是同一 $Z$ 乘 $C^1$ 函数，故finite variation且quadratic variation为0。

迁移：

- 每时刻重采 $\varepsilon_t$：fixed-time corruption对，但时间上不连续；
- 所有时刻共享 $\varepsilon$：fixed-time corruption也对，但创新维数只有一个，路径过度相关且quadratic variation错误；
- 正确forward diffusion需要一致transition或Brownian increment coupling。

### DYN-BM-D03

Nonuniform grid sampler：

$$
\Delta W_k
=\sqrt{t_{k+1}-t_k}\,Z_k,
\qquad
Z_k\overset{iid}\sim\mathcal N(0,I).
$$

Fine-to-coarse：若细 increments为 $\delta W_j$，粗区间 increment必须是所覆盖细increments的和。因为独立Gaussian方差相加，粗increment law自动正确，并且表示同一 path coupling。

Brownian bridge refinement：已知 $W_a,W_b$，在 $a<m<b$，

$$
W_m\mid W_a,W_b
\sim
\mathcal N\left(
\frac{b-m}{b-a}W_a+\frac{m-a}{b-a}W_b,
\frac{(m-a)(b-m)}{b-a}
\right).
$$

对多device使用可分割/counter-based keys，并把 path id、time interval、component id纳入key，防止重复。Common random numbers用于paired comparison时，应让两个算法读取同一 underlying Brownian tree。

Barrier crossing不能只看线性插值；端点同侧时bridge仍可能越界，需要bridge crossing probability或更细自适应处理。

错误实现：

~~~python
coarse = simulate(dt=1/64, seed=1)
fine   = simulate(dt=1/128, seed=2)
error  = norm(coarse[-1] - fine[-1])
~~~

即使两个方法都精确模拟Brownian endpoint，error仍是两条独立 $N(0,T)$ 的差，方差为 $2T$，不会随step缩小。

修复：先生成fine increments

$$
\delta W_0,\ldots,\delta W_{127},
$$

再令

$$
\Delta W_k^{coarse}
=\delta W_{2k}+\delta W_{2k+1}.
$$

指标分层：

- pathwise/strong：同一噪声coupling下轨迹差；
- weak：$\mathbb E[\phi(X_T)]$ 差；
- endpoint distribution：样本law距离；
- event functional：hitting/barrier需bridge-aware estimator。

## E. 研究迁移与声明审计

### DYN-BM-E01

错误在于不可数并集。已知每个固定 $t$ 有

$$
\mathbb P(A_t)=0
$$

只允许对可数个 $t$ 推出

$$
\mathbb P\left(\bigcup_tA_t\right)=0.
$$

$[0,T]$ 不可数，不能直接求和。

固定时刻差商

$$
D_h=\frac{W_{t+h}-W_t}{h}
\sim\mathcal N(0,1/h).
$$

若 $D_h$ almost surely收敛到有限随机变量，则必然依概率收敛，因而这一family必须tight；但

$$
\mathbb P(|D_h|\le M)
=\mathbb P(|Z|\le M\sqrt h)\to0
$$

对每个固定 $M$ 成立，不可能tight。

即使证明所有有理时刻不可微，也可能存在无理时刻可微；可微性不是由稠密集上的差商值直接排除。

正式 nowhere-differentiability proof需要把“某个时刻存在有限斜率”包含进可数个网格事件：按导数大小、邻域尺度与有理网格分层，然后证明这些事件概率可求和，再用Borel–Cantelli排除。也可调用更强 modulus/law-of-iterated-logarithm theorem。

非零 quadratic variation严格推出路径不是有限变差，并排除 $C^1$/绝对连续整段表示；不单独推出每点不可微。

Kolmogorov continuity theorem用increment moments推出连续 modification及低于阈值的Hölder regularity；它本身不证明not-$1/2$ Hölder或nowhere differentiability。

合格claim：

> Standard Brownian motion admits a continuous modification; on every compact interval its paths are almost surely $\alpha$-Hölder for every $\alpha<1/2$, have quadratic variation $[W]_t=t$ along deterministic refining partitions in the stated convergence mode, have infinite total variation, and are almost surely nowhere differentiable by the cited path-regularity theorem.

每个子句都对应不同证据。

### DYN-BM-E02

Centered Gaussian process任意有限向量都是multivariate Gaussian；其law由covariance matrix完全决定。因此 kernel

$$
K(s,t)=\mathbb E[X_sX_t]
$$

决定所有FDD。

若

$$
K(s,t)=\min(s,t),
$$

则 $X_0=0$，且

$$
\operatorname{Var}(X_t-X_s)
=t+s-2s=t-s.
$$

对不重叠increments可算covariance为0；joint Gaussian使其独立，因此得到Brownian FDD。连续版本仍需regularity。

$$
K(s,t)=st
$$

对应

$$
X_t=tZ,
\qquad Z\sim\mathcal N(0,1).
$$

其 marginal为 $\mathcal N(0,t^2)$，increments全部由同一 $Z$ 驱动，完全相关。若要与 $\mathcal N(0,t)$ marginal对齐，应使用 kernel $\sqrt{st}$，对应 $X_t=\sqrt tZ$。

$$
K(s,t)=e^{-|t-s|}
$$

是stationary Gaussian covariance，$K(0,0)=1$，所以过程不从0开始；它对应stationary Ornstein–Uhlenbeck型law，而非Brownian。

合法 covariance kernel必须对任意 $n,t_i,c_i$ 满足

$$
\sum_{i,j}c_ic_jK(t_i,t_j)\ge0.
$$

只拟合 diagonal $K(t,t)$ 只控制逐时variance，遗漏 cross-time correlation、increment law、Markov性与path regularity。

经验测试：

1. 选网格 $t_1,\ldots,t_n$；
2. 多路径估计
   $$
   \widehat K_{ij}
   =M^{-1}\sum_mX_{t_i}^{(m)}X_{t_j}^{(m)};
   $$
3. 分别与 $\min(t_i,t_j)$、$\sqrt{t_it_j}$ 和 diagonal independent-time kernel比较；
4. 报告Frobenius/maximum error、eigenvalues和increment covariance；
5. 用independent holdout paths给不确定性。

### DYN-BM-E03

Claim–evidence matrix：

| 原声明部分 | 当前证据实际支持 | 缺失证据 |
|---|---|---|
| 正确Gaussian corruption | fixed-time marginals | multi-time transitions/coupling |
| 学到正确score | 训练loss较低 | population score error、coverage、tail |
| 正确forward SDE | 某些 $q_t$ 正确 | local drift/diffusion、generator、path law |
| 正确reverse SDE | 使用某公式 | time reversal条件、score error、filtration |
| Brownian noise | Gaussian draws | $\sqrt{dt}$、independence、cross variation |
| 高精度solver | tolerance较紧 | same-objective convergence、field error |
| 正确过程 | endpoint metric好 | path functional、transition、weak tests |
| ODE/SDE等价 | marginals看似接近 | Fokker–Planck与probability-flow theorem条件 |

必须分账：

$$
\text{total error}
=\text{model/specification}
+\text{score approximation}
+\text{finite sample/optimization}
+\text{time discretization}
+\text{Monte Carlo/precision}.
$$

Probability-flow ODE与reverse SDE可在正式条件下共享marginals，但path laws、quadratic variation和随机性不同；不能用ODE solver精度证明SDE path正确。

DYN-10负责Itô integral/SDE解与Euler–Maruyama；DYN-11负责Fokker–Planck/probability-flow；DYN-12负责reverse time与score。当前章只能验收Brownian/process contract。

不过界改写：

> 在所测试的时间网格和数据分布上，模型的fixed-time Gaussian corruption marginals与目标矩匹配；在明确的PRNG与 $\sqrt{\Delta t}$ 规则下，离散forward increments通过了covariance审计。是否收敛到所声明的连续forward/reverse SDE，以及learned score和finite-step sampler的误差，仍需独立的transition、Itô、Fokker–Planck、time-reversal与grid-refinement证据。

## 复查索引

| 核心能力 | 主问题 |
|---|---|
| 对象分层 | A01、A03 |
| Brownian定义/信息流 | A02、C03 |
| Gaussian手算 | B01、B02 |
| 随机游走极限 | B03 |
| quadratic/cross variation | C01、C02 |
| 复现实验 | D01、D02、D03 |
| 定理量词审计 | E01 |
| covariance kernel | E02 |
| 扩散研究声明 | E03 |

> [!check] 状态
> 本解答只用于作答后核对。题卷和详解存在不代表学习者已掌握；需要保留首次答案、实验日志、失败注入与间隔复测证据。
