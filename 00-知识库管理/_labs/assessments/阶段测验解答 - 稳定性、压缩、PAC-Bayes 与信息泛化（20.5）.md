---
type: assessment-solution
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/stability, learning-theory/compression, learning-theory/pac-bayes, learning-theory/information]
assessment_id: ALG-CUM-01
scope: [LT-33, LT-34, LT-35, LT-36, LT-37, LT-38, LT-39, LT-40]
assessment: "[[阶段测验 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）]]"
experiment: "[[实验 - 稳定性、压缩、PAC-Bayes 与信息泛化累计复现门]]"
related: ["[[稳定性、压缩、PAC-Bayes 与信息泛化 MOC]]", "[[学习理论完整课程地图与掌握标准]]"]
created: 2026-08-28
updated: 2026-08-28
---

# 阶段测验解答 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）

> [!danger] 答案隔离
> 只有在口试、210 分钟闭卷、数值预测与原稿 hash 全部封存后，才可打开本页或 canonical stdout。本页是评分参考和复盘材料，不得充当首次作答。

## 一、口试评分参考

### 1. 四个复杂度对象

- stability：具体学习算法在一对只差一个样本的数据集上的输出损失敏感度；
- compression：重建最终 hypothesis 所需的样本索引与 side message 的描述数；
- PAC-Bayes：数据依赖 posterior $Q$ 偏离预先合法固定的 prior $P$ 的 $\mathrm{KL}(Q\|P)$；
- information：学习通道 $P_{W\mid S}$ 让输出 $W$ 携带的样本信息 $I(S;W)$。

满分回答还会补一句：四者控制的 predictor、概率类型和适用假设不同，不能只比较 complexity term 的数值。

### 2. ghost replacement 主句

对每个 $i$ 引入独立副本 $Z_i'$，利用

$$
(S,Z_i')\overset d=(S^{(i)},Z_i)
$$

得到

$$
\mathbb E\,\mathrm{gen}(A,S)
=\frac1m\sum_{i=1}^m
\mathbb E\!\left[
\ell(A(S^{(i)}),Z_i)-\ell(A(S),Z_i)
\right].
$$

$S^{(i)}$ 与 $S$ 相邻，所以每项绝对值至多 $\beta_m$。

### 3. RERM 位移

把 $F_S$ 在 $w_S$ 最小、$F_{S'}$ 在 $w_{S'}$ 最小所给的两个 strong-convexity lower bound 相加。共同的 $m-1$ 项消失，剩余两项用 $L$-Lipschitz 控制，得到

$$
\lambda\|w_S-w_{S'}\|^2
\le \frac{2L}{m}\|w_S-w_{S'}\|.
$$

若位移非零，两边约去一次范数。这里不需要 smoothness；需要凸 loss 使加正则后的目标具有所声明的强凸性，并需要 exact minimizer。

### 4. PAC-Bayes 时间线

$P$ 在 certificate sample 之前固定；$Q=Q_S$ 可在看见数据后选择，因为最终高概率事件同时覆盖所有 $Q\ll P$。$\widehat R_S(Q)$ 与 $R(Q)$ 都是先抽 $h\sim Q$ 再计算损失的 Gibbs risk。MAP、posterior mean 和 majority vote 是不同预测规则，除非另加转移不等式，否则定理不直接控制它们。

### 5. 一分钟证书选择审计

依次核对：

1. 是否控制同一 predictor 与同一 loss；
2. 是否使用同一训练/证书样本和同一分布假设；
3. 是 expected、high-probability 还是 conditional statement；
4. 算法/后验/压缩器是否以定理允许的方式依赖数据；
5. 多路线选择是否预注册，或是否为共同事件支付 union/selection cost。

任何一项不一致，都不能把数值直接放在同一个 minimum 中。

## 二、闭卷详解

### 第 1 题解答：八层算法依赖泛化证明账本（5 分）

| 路线 | 随机/固定对象 | complexity 对象 | 概率与结论 | 直接控制 | 主要工具 | 不能推出 |
|---|---|---|---|---|---|---|
| stability | 随机 $S$；固定算法合同；随机算法还含 seed | 相邻 $S\simeq S'$ 的 loss sensitivity $\beta_m$ | 基础结论是 expected signed gap；有界 loss 下另有 tail | $A(S)$ 的 loss | ghost replacement、shared-seed coupling、bounded differences | 小 optimization error、任意 shift 或自动 tight tail |
| compression | 随机 i.i.d. $S$；固定 compressor/message/decoder | $\log\binom mk+\log|\mathcal Q|$ | realizable/consistent 条件下 high probability | reconstructed deterministic $h$ | 固定描述后留出样本独立性、union bound | 事后发明 decoder；不一致/noisy case 的同一结论 |
| PAC-Bayes | 随机 $S$；固定 prior $P$；数据依赖 $Q$ | $\mathrm{KL}(Q\|P)$ | 对所有 $Q$ 同时的 high-probability event | Gibbs predictor 的风险 | exponential moment、change of measure、Markov | MAP/mean network 风险；非法 data prior |
| information | 联合分布 $P_{SW}=P_SP_{W\mid S}$ | $I(S;W)$ | 常见基础式是 expected signed gap | 随机输出 $W$ | KL variational/change-of-measure、sub-Gaussian mgf | $E|\mathrm{gen}|$、高概率 tail、连续确定性输出必有有限 MI |

给分：每条路线对象与复杂度各 0.5 分，共 4 分；能清楚分开 expected/high-probability 与“不能推出”得 1 分。

### 第 2 题解答：replace-one 定义与 ghost replacement（5 分）

#### 2.1 定义

若 $S\simeq S'$ 表示两个大小为 $m$ 的样本只差一个坐标，则 direct replace-one uniform stability 是

$$
\sup_{S\simeq S'}\sup_{z\in\mathcal Z}
\left|\ell(A(S),z)-\ell(A(S'),z)\right|
\le\beta_m.
$$

它是 loss-level 的 uniform statement，不只是参数距离，也不是对随机测试点取平均。

#### 2.2 ghost replacement

从定义展开：

$$
\begin{aligned}
\mathbb E\,\mathrm{gen}(A,S)
&=\frac1m\sum_{i=1}^m
\mathbb E_{S,Z_i'}\!
\left[\ell(A(S),Z_i')-\ell(A(S),Z_i)\right].
\end{aligned}
$$

由于 $Z_i$ 与 $Z_i'$ 独立同分布，交换它们不改变联合分布。交换后，算法看到的样本从 $S$ 变成 $S^{(i)}$，而测试点从 $Z_i'$ 变成 $Z_i$：

$$
\mathbb E_{S,Z_i'}\ell(A(S),Z_i')
=\mathbb E_{S,Z_i'}\ell(A(S^{(i)}),Z_i).
$$

所以

$$
\mathbb E\,\mathrm{gen}(A,S)
=\frac1m\sum_i
\mathbb E\!\left[
\ell(A(S^{(i)}),Z_i)-\ell(A(S),Z_i)
\right].
$$

#### 2.3 随机算法

令 $A(S;U)$ 的随机 seed 为 $U$。shared-randomness coupling 在比较 $S$ 与 $S'$ 时使用同一个 $U$，从而把差异归因于替换样本，而不是两次无关的算法噪声。可以要求 pathwise stability

$$
\sup_u\sup_{S\simeq S'}\sup_z
|\ell(A(S;u),z)-\ell(A(S';u),z)|\le\beta_m,
$$

或在明确的耦合下控制对 $U$ 的期望；两者强度不同，不能省略随机性量词。

### 第 3 题解答：五条证书的接口表（5 分）

| 路线 | 输入 | complexity | 结论 | 允许的数据依赖 | 常见作弊 |
|---|---|---|---|---|---|
| capacity | fixed class $\mathcal H/\mathcal F$ | VC/Rademacher/cover/norm | 常为 uniform high probability | 可在共同事件中选 $h\in\mathcal H$；class 必须按定理固定/支付 | 用同一数据训练 representation 后把 realized class 当预先固定 |
| stability | algorithm $A$、loss、adjacency | $\beta_m$ | expected；有界损失可做 tail | 输出当然依赖数据，但算法敏感度需统一控制 | 只测几个随机 replacement 就称 uniform stability |
| compression | fixed encoder/message/decoder | $k,b$ 或描述数 | realizable consistent high probability | subset 可自适应选，因已枚举；scheme 本身不能事后发明 | 忽略 side message/decoder 搜索 |
| PAC-Bayes | fixed prior $P$、posterior $Q$ | KL$(Q\|P)$ | simultaneous high probability | $Q$ 可依赖证书数据；标准 $P$ 不可 | 令 $P_S=Q_S$；把 Gibbs bound 报给 MAP |
| information | channel $P_{W\mid S}$、sub-Gaussian loss | $I(S;W)$ | 基础式为 expected signed gap | 允许一般随机算法，依赖被 MI 支付 | 把有限 bit 上限当实际 MI；把 expected 当 tail |

每条完整接口 1 分。

### 第 4 题解答：PAC-Bayes 时间线与 predictor 身份（5 分）

标准 theorem 的事件为：对 certificate sample $S\sim D^m$，以至少 $1-\delta$ 的概率，**同时对所有 $Q\ll P$** 成立某个不等式。这里 $P$ 在抽取该 $S$ 之前已固定。因此 posterior 能依赖 $S$，不意味着 prior 也能未经代价依赖同一 $S$。

令 $P_S=Q_S$ 的错误发生在 Markov/exponential-moment 事件的构造之前：原证明先对固定 $P$ 求 $\mathbb E_{h\sim P}$，再对 $S$ 取期望。若 $P=P_S$，两个随机对象已经耦合，原 moment calculation 不再适用。

三种合法路线：

1. independent pretraining prior：用与 certificate sample 独立的公开数据/预训练过程产生 $P$；
2. sample split：用 $S_0$ 学 $P_{S_0}$，只在独立 $S_1$ 上构造 certificate，分母使用 $|S_1|$；
3. weighted family：预注册 $\{P_j\}$ 和 $\pi_j$，对第 $j$ 个 prior 支付 $\log(1/\pi_j)$，再在共同事件中选。

Gibbs risk 是

$$
R(Q)=\mathbb E_{h\sim Q}\mathbb E_Z\ell(h,Z).
$$

MAP 只选 $\arg\max_hQ(h)$；posterior mean 在参数空间平均；majority vote 在预测空间聚合。非线性模型中这些操作一般都不等于 Gibbs 随机化。

评分：违法量词 2 分，三种修复 2 分，predictor 区分 1 分。

### 第 5 题解答：Bernoulli 均值学习器的精确定标（7 分）

#### 5.1 精确稳定性

令样本中有 $K=k$ 个 1。一次 $0\to1$ 替换使

$$
w=\frac{k}{m},\qquad w'=\frac{k+1}{m}.
$$

测试点 $z=0$ 时

$$
|(w')^2-w^2|=\frac{2k+1}{m^2};
$$

测试点 $z=1$ 时

$$
|(1-w)^2-(1-w')^2|
=\frac{2(m-k)-1}{m^2}.
$$

对 $k=0,\ldots,m-1$ 取最大值，两者都给

$$
\beta_m=\frac{2m-1}{m^2}.
$$

$m=20$ 时

$$
\boxed{\beta_{20}=\frac{39}{400}=0.097500}.
$$

#### 5.2 精期期望泛化隙

记 $W=K/m$。population risk 和 empirical risk 分别为

$$
R(W)=p(1-W)^2+(1-p)W^2=p-2pW+W^2,
$$

$$
\widehat R_S(W)=W(1-W)=W-W^2.
$$

因此

$$
R(W)-\widehat R_S(W)=p-(2p+1)W+2W^2.
$$

利用

$$
\mathbb EW=p,\qquad
\mathbb EW^2=p^2+\frac{p(1-p)}m,
$$

得到

$$
\mathbb E\,\mathrm{gen}
=\frac{2p(1-p)}m.
$$

$p=1/2,m=20$ 时

$$
\boxed{\mathbb E\,\mathrm{gen}=0.025000}.
$$

#### 5.3 为什么不相等

$\beta_m$ 是对所有相邻数据集和所有测试点取 worst case；期望隙按真实 Binomial 权重平均，并允许正负/大小结构相互平均。稳定性是安全证书，不是这一个分布下 gap 的精确等式。

评分：相邻计数推导 3 分，期望求和 3 分，语义解释 1 分。

### 第 6 题解答：RERM 与 SGD 证书（7 分）

RERM 标准界为

$$
\beta_m^{\mathrm{RERM}}\le\frac{2L^2}{\lambda m}.
$$

代入 $L=1,\lambda=2,m=20$：

$$
\boxed{\beta_m^{\mathrm{RERM}}\le0.050000}.
$$

凸、光滑情形的 synchronous-coupling SGD 接口为

$$
\epsilon_{\mathrm{stab}}
\le\frac{2L^2}{m}\sum_{t=1}^T\eta_t.
$$

预注册步长之和为 $0.5$，所以

$$
\boxed{\epsilon_{\mathrm{stab}}\le0.050000}.
$$

机制判断：

- 在这个凸证书中延长训练且继续加入正步长会增大 $\sum_t\eta_t$；
- 增大 $\lambda$ 使 RERM stability 按 $1/\lambda$ 改善，但可能增加 optimization/statistical bias；
- 非凸光滑的朴素展开会出现
  $$
  \frac{2L^2}{m}\sum_t\eta_t\prod_{s>t}(1+\gamma\eta_s),
  $$
  旧扰动可能被后续迭代放大；
- stability 只比较相邻数据集上的输出敏感度。一个稳定但几乎不优化目标的算法仍可有很大 training/excess risk，所以 optimization error 必须另列。

评分：两个数各 2 分，三项机制 2 分，optimization 分账 1 分。

### 第 7 题解答：样本压缩的组合账本（7 分）

side message 有 $|\mathcal Q|=2^b$ 种。由

$$
2^b\binom mk(1-\varepsilon)^{m-k}\le\delta
$$

和 $1-\varepsilon\le e^{-\varepsilon}$，得到

$$
R(h_S)
\le
\frac{\log\binom mk+b\log2+\log(1/\delta)}{m-k}.
$$

代入 $m=200,k=5,b=3,\delta=0.05$：

$$
\boxed{R(h_S)\le0.137071}.
$$

subset 的确是看数据后选择的，但证明对所有 $\binom mk$ 个 subset 做 union，因此选择已经被枚举。相反，如果学习者看完数据后才设计新的 decoder 或扩大 message family，union index 中没有这些选择；必须预先固定、显式计数，或使用另一份独立数据。

评分：概率式/指数化 3 分，数值 2 分，选择边界 2 分。

### 第 8 题解答：PAC-Bayes-kl 与信息通道（7 分）

#### 8.1 PAC-Bayes 数值

经验 Gibbs risk：

$$
\widehat R(Q)=0.9(0.02)+0.1(0.25)=0.043000.
$$

KL 使用自然对数：

$$
\begin{aligned}
\mathrm{KL}(Q\|P)
&=0.9\log\frac{0.9}{0.7}
+0.1\log\frac{0.1}{0.3}\\
&=\boxed{0.116322}.
\end{aligned}
$$

binary-kl budget：

$$
c=\frac{0.1163217566+\log(201/0.05)}{200}
=\boxed{0.042077}.
$$

在 $r\in[0.043,1)$ 上二分求满足

$$
\operatorname{kl}(0.043\|r)=c
$$

的右端点，得

$$
\boxed{r_{\mathrm{invkl}}=0.127958}.
$$

Pinsker corollary 给

$$
0.043+\sqrt{\frac c2}
=\boxed{0.188046}.
$$

inverse-kl 更紧，因为它没有先把非对称的 Bernoulli KL 子水平集替换成对称平方根外包络。

#### 8.2 信息通道数值

对称二元通道的输出仍为均匀分布，所以

$$
I(X;W)=H(W)-H(W\mid X)=\log2-H_b(0.8).
$$

数值为

$$
\boxed{I(X;W)=0.192745\ \text{nats}}.
$$

对 0—1 loss，若把这个通道作为相关学习通道 fixture，

$$
\sqrt{\frac{I}{2m}}
=\boxed{0.021951}.
$$

PAC-Bayes 数值是概率至少 $1-\delta$ 的 Gibbs-risk 上界，包含 empirical risk；互信息式在这里是 expected signed generalization radius，不是 population risk upper bound，也没有同样的 $\delta$ 语义。因此不能把 $0.021951$ 与 $0.127958$ 直接取最小。

评分：PAC 计算 4 分，MI 计算 2 分，语义分账 1 分。

### 第 9 题解答：稳定性到期望泛化（8 分）

写

$$
R(A(S))=\mathbb E_{Z'}\ell(A(S),Z'),\qquad
\widehat R_S(A(S))=\frac1m\sum_i\ell(A(S),Z_i).
$$

为每个 $i$ 引入 $Z_i'\sim D$，独立于 $S$：

$$
\mathbb E\,R(A(S))
=\frac1m\sum_i
\mathbb E_{S,Z_i'}\ell(A(S),Z_i').
$$

关键换元不是说“$A(S)$ 与 $Z_i$ 独立”；那是错的。正确事实是完整随机向量

$$
(Z_1,\ldots,Z_i,\ldots,Z_m,Z_i')
$$

在交换 $Z_i$ 与 $Z_i'$ 后分布不变。交换后，算法输入成为

$$
S^{(i)}=(Z_1,\ldots,Z_i',\ldots,Z_m),
$$

测试坐标成为原来的 $Z_i$。于是

$$
\mathbb E_{S,Z_i'}\ell(A(S),Z_i')
=\mathbb E_{S,Z_i'}\ell(A(S^{(i)}),Z_i).
$$

相减得到

$$
\mathbb E\,\mathrm{gen}
=\frac1m\sum_i\mathbb E
\left[\ell(A(S^{(i)}),Z_i)-\ell(A(S),Z_i)\right].
$$

对每一个实现，$S^{(i)}\simeq S$ 且测试点就是 $Z_i$。因此 uniform stability 给

$$
\left|\ell(A(S^{(i)}),Z_i)-\ell(A(S),Z_i)\right|\le\beta_m.
$$

最后用三角不等式与期望单调性：

$$
\left|\mathbb E\,\mathrm{gen}\right|
\le\frac1m\sum_i\mathbb E\,\beta_m
=\beta_m.
$$

评分：risk 展开 1 分，联合分布换元 3 分，identity 2 分，stability closure 2 分。

### 第 10 题解答：strong convexity 到 RERM 稳定性（8 分）

令 $S$ 的特殊样本为 $z$，$S'$ 对应为 $z'$，共同部分记作 $C$。因为 $F_S$ 是 $\lambda$-strongly convex 且 $w_S$ 是 exact minimizer，

$$
F_S(w_{S'})\ge F_S(w_S)+\frac\lambda2\|w_{S'}-w_S\|^2.
$$

同理，

$$
F_{S'}(w_S)\ge F_{S'}(w_{S'})+\frac\lambda2\|w_{S'}-w_S\|^2.
$$

相加并移项：

$$
\lambda\|\Delta\|^2
\le
\big[F_S(w_{S'})-F_S(w_S)\big]
+\big[F_{S'}(w_S)-F_{S'}(w_{S'})\big],
$$

其中 $\Delta=w_{S'}-w_S$。展开两个 objective 后：

- $C$ 中的 $m-1$ 个经验损失项成对消掉；
- 正则项也成对消掉；
- 只剩

$$
\lambda\|\Delta\|^2
\le\frac1m\left[
\ell(w_{S'},z)-\ell(w_S,z)
+\ell(w_S,z')-\ell(w_{S'},z')
\right].
$$

由 $L$-Lipschitz，

$$
\lambda\|\Delta\|^2\le\frac{2L}{m}\|\Delta\|.
$$

若 $\Delta=0$ 结论平凡；否则约去 $\|\Delta\|$：

$$
\|w_S-w_{S'}\|\le\frac{2L}{\lambda m}.
$$

再对任意测试点 $u$ 使用 loss 的 Lipschitz 性：

$$
|\ell(w_S,u)-\ell(w_{S'},u)|
\le L\|w_S-w_{S'}\|
\le\boxed{\frac{2L^2}{\lambda m}}.
$$

条件定位：

- exact minimizer 用来让一阶最优条件/强凸 lower bound 在最小点成立；
- convex loss 加二次正则保证整体 strong convexity；
- strong convexity 产生平方位移；
- Lipschitz 把目标差变成线性位移，再把参数位移转回测试 loss；
- smoothness 没有在此证明中使用。

评分：两 lower bounds 2 分，消项 2 分，位移 2 分，loss stability 1 分，条件定位 1 分。

### 第 11 题解答：压缩界的留出样本证明（8 分）

先固定一个索引集合 $I\subset[m]$，$|I|=k$，以及一个 side message $q\in\mathcal Q$。decoder 只看 $S_I,q$，输出

$$
h_{I,q}=\rho(S_I,q).
$$

条件于 $S_I$ 后，其余 $m-k$ 个样本仍是从 $D$ 独立抽取，并且没有参与 $h_{I,q}$ 的构造。若 $R(h_{I,q})>\varepsilon$，单个留出样本不犯错的概率小于 $1-\varepsilon$，所以所有留出样本都不犯错的概率至多

$$
(1-\varepsilon)^{m-k}.
$$

如果 reconstruction 与完整样本一致，那么它特别在这些留出样本上全部零误差。因此，对固定 $(I,q)$，

$$
\Pr\big(R(h_{I,q})>\varepsilon
\ \text{且}\ h_{I,q}\text{ 与 }S\text{ 一致}\big)
\le(1-\varepsilon)^{m-k}.
$$

可能的索引总数是

$$
|\mathcal Q|\binom mk.
$$

对全部 $(I,q)$ 做 union：

$$
\Pr\!\left(\exists\text{ consistent }h_{I,q}:R(h_{I,q})>\varepsilon\right)
\le|\mathcal Q|\binom mk(1-\varepsilon)^{m-k}.
$$

注意“先固定 $(I,q)$ 再用独立性”是证明的核心。不能先把数据依赖的最终 $I(S)$ 固定后，假装它与留出样本独立；合法性来自随后对所有候选 $(I,q)$ 的 union。

评分：固定描述与条件独立 3 分，一致性事件 2 分，union 2 分，量词警告 1 分。

### 第 12 题解答：PAC-Bayes-kl 的测度变换主链（8 分）

对固定 hypothesis $h$，记

$$
\widehat r_h=\widehat R_S(h),\qquad r_h=R(h).
$$

0—1 loss 下 $m\widehat r_h$ 是 Binomial$(m,r_h)$。一个标准离散 moment 计算给出

$$
\mathbb E_{S\sim D^m}
\exp\!\left(m\,\operatorname{kl}(\widehat r_h\|r_h)\right)
\le m+1.
$$

先对固定 prior $P$ 积分，再用 Tonelli：

$$
\mathbb E_S\mathbb E_{h\sim P}
\exp\!\left(m\,\operatorname{kl}(\widehat r_h\|r_h)\right)
\le m+1.
$$

Markov 不等式说明：以至少 $1-\delta$ 的概率，

$$
\mathbb E_{h\sim P}
\exp\!\left(m\,\operatorname{kl}(\widehat r_h\|r_h)\right)
\le\frac{m+1}{\delta}.
$$

现在固定在这个事件内。对任意 $Q\ll P$，在 change-of-measure lemma 中取

$$
f(h)=m\,\operatorname{kl}(\widehat r_h\|r_h),
$$

得到

$$
\mathbb E_Q m\,\operatorname{kl}(\widehat r_h\|r_h)
\le\mathrm{KL}(Q\|P)+\log\frac{m+1}{\delta}.
$$

Bernoulli KL 对两个参数联合凸，所以 Jensen 给

$$
\operatorname{kl}\!\left(
\mathbb E_Q\widehat r_h\ \middle\|\ \mathbb E_Qr_h
\right)
\le
\mathbb E_Q\operatorname{kl}(\widehat r_h\|r_h).
$$

识别

$$
\mathbb E_Q\widehat r_h=\widehat R_S(Q),\qquad
\mathbb E_Qr_h=R(Q),
$$

便得到

$$
\operatorname{kl}(\widehat R_S(Q)\|R(Q))
\le
\frac{\mathrm{KL}(Q\|P)+\log((m+1)/\delta)}m.
$$

“所有 data-dependent $Q$”合法的原因是：Markov 构造出的同一个事件只依赖 $S$ 和固定 $P$，进入事件后 change-of-measure 对任意 $Q\ll P$ 都成立。不是先为每个 $Q$ 各自抽一个事件。

若 $Q\not\ll P$，存在 $P$ 质量为零但 $Q$ 质量为正的集合，Radon–Nikodym derivative 不存在于所需形式，$\mathrm{KL}(Q\|P)=\infty$；change-of-measure 不给有限证书。

inverse-kl 直接保留 Bernoulli KL 的非对称几何；Pinsker 先用

$$
\operatorname{kl}(a\|b)\ge2(a-b)^2
$$

把它松弛成平方根半径，因此通常更松。

评分：fixed-$h$ moment 2 分，Markov 1 分，change of measure 2 分，joint convexity 1 分，simultaneous/support/inverse-kl 边界 2 分。

### 第 13 题解答：五条声明审计（10 分）

#### 1. “$\beta_m=O(1/m)$ 就一定有高概率收敛”

**条件不足。** 对有界损失 $0\le\ell\le M$ 的经典界，

$$
R(A(S))
\le\widehat R_S(A(S))+\beta_m
+(2m\beta_m+M)\sqrt{\frac{\log(1/\delta)}{2m}}.
$$

此时 $\beta_m=O(1/m)$ 确实使右侧 gap 为 $O(m^{-1/2})$。但没有有界性/尾部条件、i.i.d. 和正确 stability 定义，不能只凭 $\beta_m$ 推出 high-probability tail。

#### 2. “subset 自适应所以压缩界无效”

**错误。** 标准证明恰好枚举全部 $\binom mk$ 个 subset，自适应选择已经被 union 支付。需要额外支付的是未被预先固定/计数的 message、decoder 或 scheme family。

#### 3. “posterior 可依赖数据，所以 prior 也可”

**错误。** posterior 的数据依赖由 simultaneous event 允许；标准 prior 在 certificate sample 前固定。修复方式是 independent prior、sample split、weighted family 或一条带明确 correction 的 data-dependent-prior theorem。

#### 4. “有限浮点输出，所以 MI 有限且小”

**前半在完全离散实现模型下可成立，后半错误。** 若输出 alphabet 真是有限的，则

$$
I(S;W)\le H(W)\le\log|\mathcal W|,
$$

但现代参数向量的 alphabet 可大到该上界完全空洞。若理论把参数视为连续实数，deterministic $W=f(S)$ 还可能使 $I(S;W)=\infty$。有限存储不等于信息少。

#### 5. “五类界可事后直接取 minimum”

**错误。** 必须先对齐 predictor、loss、sample、随机性和结论类型；若它们确实是同一目标的多个 high-probability certificate，还要预注册选择或建立 joint event，例如给五条路线各分配 $\delta/5$。expected information bound 与 high-probability risk bound 尤其不能直接比较。

每小题 2 分：判断 0.5、修复 1、理由/反例 0.5。

### 第 14 题解答：为微调大模型建立多路线泛化合同（10 分）

下面是一份合格 protocol 的骨架。

#### 14.1 对象与数据

- 明确目标分布 $D$、i.i.d./exchangeability 是否可信，以及 public pretraining corpus 与 private certificate sample 是否独立；
- 冻结 private sample 的 train/certificate split；若同一数据搜索 rank/checkpoint，必须把搜索包含进学习算法 $A$；
- 定义 bounded/clipped loss $\ell\in[0,M]$，或逐 $w$ 验证统一 sub-Gaussian 参数，不能用“经验上波动小”代替；
- 定义算法输出是随机 LoRA 参数 $W$、Gibbs sample、ensemble 还是 deterministic deployed model。

#### 14.2 stability 路线

把随机 seed、minibatch order 和 dropout 纳入 $A(S;U)$，对相邻 $S,S'$ 使用 shared $U$。凸光滑 SGD 定理需要凸 loss、smoothness、Lipschitz、合法步长和固定迭代协议；真实 Transformer/LoRA 通常非凸，因此不能直接把该 theorem 作为正式证书。可以降级为：

- 一个局部/线性化模型中的条件性 theorem；
- empirical replace-one sensitivity audit；
- 或明确引用覆盖非凸 regime 的专门 theorem 并核对其 expansion factors。

三者都不能被写成无条件的深网 uniform-stability 结论。

#### 14.3 PAC-Bayes 路线

用公开、独立预训练权重中心构造 prior，例如

$$
P=\mathcal N(\mu_{\mathrm{pre}},\sigma_P^2I).
$$

在 private data 上学习 posterior $Q_S$ 是合法的。rank、temperature、prior variance 和 checkpoint 若要搜索：

- 预注册 finite family $\{P_j\}$ 与 weights $\pi_j$，为选择支付 $\log(1/\pi_j)$；
- 或 split 数据，用一部分选择，另一部分认证；
- 或一次性建立覆盖全部候选的共同事件。

报告对象必须是 Gibbs/随机化 predictor。若部署 posterior mean 或 MAP，另给转移界或单独评估。

#### 14.4 information 路线

完整学习通道是

$$
P_{W\mid S}
$$

而不是只写“模型有多少参数”。随机初始化、minibatch、量化、噪声、checkpoint selection 都属于通道。有限 $b$ bit transcript 只给粗上界 $I(S;W)\le b\log2$；噪声注入可能通过 data processing 降低信息，但必须计算/上界实际 joint law。基础结论

$$
|\mathbb E\,\mathrm{gen}|
\le\sqrt{\frac{2\sigma^2 I(S;W)}m}
$$

是 expected signed gap，不是单次训练的 tail certificate。

#### 14.5 compression 路线

若声称 LoRA 被少量“代表样本”决定，必须在训练前固定：

- compressor $\kappa$ 输出哪些样本索引和 side message；
- decoder $\rho$ 怎样只从这些对象重建 predictor；
- reconstruction 在完整样本上满足何种一致性/近似条件；
- rank、量化码本、optimizer state 是否属于 message。

仅仅“LoRA 参数少”不是 sample compression scheme。

#### 14.6 选择与证据等级

先为每条路线建立对象相同的 ledger，再决定能否比较。若五条 high-probability 证书都针对同一 deployed predictor，可用预注册优先级，或各自 $\delta/5$ 建 joint event。最后分四层报告：

1. legal：全部定理条件、量词和选择预算正确；
2. nonvacuous：数值优于损失平凡上界；
3. tight：与可观测 gap 或已知 lower bound 的差距小；
4. explanatory：干预相应机制时证书与现象共同变化，而不是只做事后相关。

评分：对象/数据 2 分，stability 2 分，PAC-Bayes 2 分，information 1.5 分，compression 1 分，选择与证据分层 1.5 分。

## 三、实验复现与延迟门参考

### canonical 解析锚点

运行[[algorithmic_generalization_cumulative_gate.py]]应得到：

| 轨道 | 锚点 |
|---|---:|
| A exact replace-one $\beta$ | $0.097500$ |
| A expected gap | $0.025000$ |
| A RERM / SGD certificates | $0.050000/0.050000$ |
| B compression | $0.137071$ |
| B empirical Gibbs / KL | $0.043000/0.116322$ |
| B inverse-kl / Pinsker | $0.127958/0.188046$ |
| B five-route joint inverse-kl | $0.138265$ |
| C exact MI / one-bit ceiling | $0.192745/0.693147$ nats |
| C exact / bit radii | $0.021951/0.041628$ |

这些数只能用于封存后的材料核对。学习者 blind run 必须改变至少两个跨轨参数，且不得覆盖 canonical SVG。

### nonce 评分

1. 主轨解析预测正确且 stdout 一致：4 分；
2. 跨轨参数的方向预测正确：2 分；
3. 能解释 exact/certificate 和 expected/high-probability 的差异：2 分；
4. 非法参数被明确拒绝：1 分；
5. command、SVG、hash 与原始预测齐全：1 分。

### 48 小时与 14 天

- 48 小时复测若只替换数字、不替换机制，最多记 practice；
- 14 天迁移必须出现新的随机对象、新的失败模式和至少一个无法验证的假设；
- 只要仍把 Gibbs 当 MAP、把 expected 当 tail 或把 data-dependent prior 当标准 prior，卷级状态不得升级。

## 四、状态边界

本详解、题卷、三轨脚本与独立审计证明的是“验收材料可用”，不是“学习者已经掌握”。个人状态只有在口试、闭卷、nonce 盲参、非法合同拒绝、48 小时与 14 天证据全部归档后，才能由评分者从 **not-attempted** 改为相应学习状态。
