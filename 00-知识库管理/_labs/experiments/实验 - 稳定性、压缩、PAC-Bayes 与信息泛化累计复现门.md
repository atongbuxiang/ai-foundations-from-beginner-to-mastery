---
type: experiment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/stability, learning-theory/compression, learning-theory/pac-bayes, learning-theory/information, reproducible-evidence]
assessment_id: ALG-CUM-01
scope: [LT-33, LT-34, LT-35, LT-36, LT-37, LT-38, LT-39, LT-40]
script: "[[algorithmic_generalization_cumulative_gate.py]]"
assessment: "[[阶段测验 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）]]"
solution: "[[阶段测验解答 - 稳定性、压缩、PAC-Bayes 与信息泛化（20.5）]]"
figure: "[[plot-algorithmic-generalization-cumulative-gate-v2.svg]]"
related: ["[[稳定性、压缩、PAC-Bayes 与信息泛化 MOC]]", "[[学习理论完整课程地图与掌握标准]]", "[[推导与实验 MOC]]"]
created: 2026-08-28
updated: 2026-08-28
---

# 实验 - 稳定性、压缩、PAC-Bayes 与信息泛化累计复现门

> [!abstract] 实验问题
> “不要只看 hypothesis class，要看具体算法或输出描述”怎样成为可核对的证据？本实验用三个完全确定性的有限/解析 fixture 回答：A 穷举 Bernoulli 均值学习器的全部相邻计数，分开 worst-case stability 与真实期望泛化隙，并记录 RERM/SGD 的定理接口；B 精确计算 compression 组合账本和 finite PAC-Bayes-kl，保留 inverse-kl 与 Pinsker 两本账；C 把一个数据摘要经过随机化二元通道，精确计算 mutual information、one-bit 上界与证书选择预算。全程无 Monte Carlo。

![[00-知识库管理/_assets/plots/learning-theory/plot-algorithmic-generalization-cumulative-gate-v2.svg|1200]]

> [!figure] 实验图｜敏感度—描述长度—信息泄漏三种算法依赖视角
> **对象与结论：** A 的红柱是 sample-mean learner 的 exact direct replace-one $\beta$，蓝柱是同一模型在 Bernoulli 分布下的 exact expected gap；RERM/SGD 两柱是另两个抽象算法接口的上界，不是 sample mean 的新估计。B 同时展示 consistent compression risk certificate、PAC-Bayes inverse-kl、Pinsker 松弛与五路线共同预算下的 PAC-Bayes 数值。C 展示学习通道的 exact MI 与 one-bit ceiling，并明确基础信息界只控制 expected signed gap。
>
> **怎样读图：** 先在每一栏内部区分 exact quantity 与 theorem certificate，再读底部对象合同。只有 predictor、loss、sample、算法随机性与 probability event 全部对齐，跨栏比较才有意义。图中并列数值主要训练“不能直接取 minimum”，不是排行榜。
>
> **适用边界（图没有证明什么）：** Bernoulli、两 hypothesis posterior 和二元通道是 finite audit fixtures；RERM/SGD 数值来自其各自条件，不是深网实证；compression 假设 fixed scheme、realizability 与完整一致性；PAC-Bayes 控制 Gibbs risk 且 prior 合法；information 项不是 tail。图不证明现代 Transformer 的界非空洞，也不覆盖 distribution shift、dependent prompts 或未经计数的超参数搜索。

## 一、它验证什么，不验证什么

本实验验证：

1. 对所有相邻 Bernoulli success counts 和 $z\in\{0,1\}$ 的 exact replace-one supremum；
2. 对全部 $K=0,\ldots,m$ 的 Binomial 加权求和，而不是 Monte Carlo 的 expected gap；
3. 标准 RERM $2L^2/(\lambda m)$ 与 convex-smooth SGD $2L^2\sum_t\eta_t/m$ 接口；
4. $\log\binom mk+b\log2+\log(1/\delta)$ 的 compression 组合分账；
5. finite prior/posterior support、Gibbs empirical risk、KL、binary-kl inverse 与 Pinsker；
6. 合法 prior 时间线与 $Q\ll P$ 的输入保护；
7. 二元随机化通道的 exact MI、bit ceiling 和 information radius；
8. 多路线选择时的 $\log J$ / $\delta/J$ 预算；
9. canonical/固定盲参 stdout、SVG/XML、SHA-256 与覆盖保护。

它不验证：

- 几次随机 replacement 的平均值等于 uniform stability；
- RERM/SGD certificate 是 Bernoulli mean exact gap；
- 参数量少就构成 sample compression；
- $P_S=Q_S$ 可用于标准 PAC-Bayes；
- Gibbs posterior 的 bound 自动属于 MAP 或 posterior mean 网络；
- one-bit ceiling 等于实际 MI；
- $|\mathbb E\,\mathrm{gen}|$ 自动控制 $\mathbb E|\mathrm{gen}|$ 或单次 tail；
- 把五条未对齐的数值事后取最小是合法 model selection。

## 二、执行顺序、答案隔离与 scorer nonce

1. 完成 20 分钟口试和 210 分钟闭卷；
2. 冻结 attempt_id、原稿、时间和 SHA-256；
3. 未看图与 stdout 时完成三轨解析校准；
4. 评分者公布 scorer nonce，指定主轨、跨轨盲参和非法合同；
5. 学习者先写 exact/bound 类型、数值区间与单调性预测；
6. 使用新 --output 执行非 canonical 参数；
7. 保存 command、stdout、SVG、hash、运行前预测与差异解释；
8. 才可打开 canonical 输出和封存详解；
9. 48 小时换机制，14 天迁移到陌生算法依赖泛化问题。

nonce 建议映射：SHA-256 首字节模 3 对应 A/B/C；第二字节模 5 对应 sample、regularization、description、prior、information；第三字节从“非法概率 / $k\ge m$ / support violation / 覆盖 canonical / posterior 不归一”中选一项。公开固定盲参只用于审计脚本，不得充当学习者个人盲参。

> [!warning] 防止循环认证
> 先运行再补写“我知道 inverse-kl 比 Pinsker 紧”，或照图报告 $\beta=0.0975$，只能记 practice。个人 evidence 必须保留运行前的相邻计数式、Binomial moment、compression index 数、KL 手算、inverse-kl bracket 与 MI entropy 预测。

## 三、进入实验前的解析校准门

### 3.1 Track A：replace-one、RERM 与 SGD

对 $A(S)=\bar Z$、$\ell(w,z)=(w-z)^2$：

1. 用成功数 $K$ 代替枚举 $2^m$ 个样本；
2. 写出 $K=k$ 与 $K'=k+1$ 时 $z=0,1$ 的两个 loss differences；
3. 先预测最大值出现于哪个端点，再算 exact $\beta_m$；
4. 写出 $R(K/m)$ 与 $\widehat R_S(K/m)$，用 $\mathbb EK$ 和 $\mathbb EK^2$ 求 expected gap；
5. 另外对抽象凸 Lipschitz RERM/SGD 接口计算两个 certificate，明确它们不是同一模型的精确量。

任一答案把 $\beta$ 与 expected gap 写成同一个对象，不得进入 blind run。

### 3.2 Track B：compression 与 PAC-Bayes

1. 写出 subset、side message、decoder 的 fixed scheme；
2. 从 $|\mathcal Q|\binom mk(1-\varepsilon)^{m-k}$ 解出 risk；
3. 逐项计算 $\widehat R(Q)$ 与 $\mathrm{KL}(Q\|P)$；
4. 检查 $Q\ll P$，并写出 prior 在 certificate data 前固定的时间线；
5. 计算 $c=[\mathrm{KL}+\log((m+1)/\delta)]/m$；
6. 先给 inverse-kl root bracket，再用数值二分；
7. 比较 Pinsker，但不得把差异解释为换了 predictor；
8. 若同时筛选五条 high-probability 路线，先把 $\delta$ 预算改成共同事件。

### 3.3 Track C：information 与选择预算

令 $X=f(S)\sim\mathrm{Bernoulli}(1/2)$ 是训练样本的一个确定性摘要，学习输出 $W$ 只通过 $X$ 产生：

$$
S\longrightarrow X\longrightarrow W,\qquad
\Pr(W=X)=q.
$$

由于 $X$ 是 $S$ 的函数且 $W\perp S\mid X$，

$$
I(S;W)=I(X;W).
$$

进入脚本前：

1. 手算 $H(W)=\log2$ 和 $H(W\mid X)=H_b(q)$；
2. 比较 exact $I$ 与 one-bit ceiling $\log2$；
3. 用 0—1 loss 版本计算 $\sqrt{I/(2m)}$；
4. 说明 $q\to1/2$ 和 $q\to1$ 时 MI 的方向；
5. 区分 finite-output upper bound、actual MI、expected gap 三个层次。

## 四、三轨统一对象合同

| 合同 | Track A | Track B | Track C |
|---|---|---|---|
| 固定对象 | mean learner；另列 RERM/SGD theorem interfaces | fixed compression scheme；fixed prior $P$ | binary summary/channel law |
| 随机对象 | $S\sim\mathrm{Bernoulli}(p)^m$；算法接口 seed | i.i.d. certificate sample；$h\sim Q$ | $S,X,W$ joint law |
| 复杂度对象 | adjacent loss sensitivity | subset/message count；KL$(Q\|P)$ | $I(S;W)$ |
| 精确量 | exact $\beta$、exact expected gap | empirical Gibbs、finite KL | exact channel MI |
| 上界量 | RERM/SGD stability certificates | compression/PAC-Bayes risk certificates | expected generalization radius |
| 概率语义 | expected；另有 bounded-loss tail | high probability | expected signed gap |
| predictor | mean/RERM/SGD 各自分开 | reconstructed $h$；Gibbs $Q$ 分开 | randomized output $W$ |
| 关键边界 | convex/nonconvex 与 optimization 分账 | fixed scheme/prior、support、realizable | channel law、sub-Gaussian、非 tail |

## 五、轨道 A：replace-one、RERM 与 SGD

### 5.1 exact direct replace-one

一次 replacement 改变成功数 $k\to k+1$：

$$
w=\frac{k}{m},\qquad w'=\frac{k+1}{m}.
$$

对 $z=0$，

$$
|\ell(w',0)-\ell(w,0)|=\frac{2k+1}{m^2};
$$

对 $z=1$，

$$
|\ell(w',1)-\ell(w,1)|=\frac{2(m-k)-1}{m^2}.
$$

所以

$$
\beta_m=\frac{2m-1}{m^2}.
$$

canonical $m=20$ 给 $0.097500$。脚本不是随机抽 replacement，而是枚举全部 $k=0,\ldots,m-1$ 和两个测试点。

### 5.2 exact expected gap

对 $K\sim\mathrm{Binomial}(m,p)$，$W=K/m$：

$$
R(W)-\widehat R_S(W)=p-(2p+1)W+2W^2.
$$

由 $\mathbb EW=p$ 和 $\operatorname{Var}(W)=p(1-p)/m$，

$$
\mathbb E\,\mathrm{gen}=\frac{2p(1-p)}m.
$$

canonical $p=1/2,m=20$ 给 $0.025000$。它小于 worst-case $\beta$ 不表示 stability theorem 错；二者的 supremum/expectation 量词不同。

### 5.3 RERM/SGD 接口

canonical $L=1,\lambda=2,m=20$：

$$
\beta_{\mathrm{RERM}}\le\frac{2L^2}{\lambda m}=0.050000.
$$

步长和 $\sum_t\eta_t=0.5$：

$$
\epsilon_{\mathrm{SGD}}\le
\frac{2L^2}{m}\sum_t\eta_t=0.050000.
$$

这两个数只审计公式接口。RERM 需要 convex Lipschitz loss、$\lambda$-strongly convex objective 与 exact minimization；SGD 数值对应 convex-smooth synchronous coupling。非凸时可能出现后续 expansion products，不能照搬。

## 六、轨道 B：compression 与 PAC-Bayes

### 6.1 compression

canonical $m=200,k=5,b=3,\delta=0.05$：

$$
\varepsilon_{\mathrm{comp}}
=\frac{\log\binom{200}{5}+3\log2+\log20}{195}
=0.137071.
$$

$k$ 接近 $m$ 会同时恶化 numerator 和 denominator；增加 side bits 每一 bit 支付 $\log2/(m-k)$。raw bound 必须保留，即使超过 1 后可另报 clipped risk。

### 6.2 finite PAC-Bayes-kl

canonical

$$
P=(0.7,0.3),\quad
Q=(0.9,0.1),\quad
\widehat R=(0.02,0.25).
$$

因此

$$
\widehat R(Q)=0.043000,\qquad
\mathrm{KL}(Q\|P)=0.116322.
$$

PAC-Bayes-kl budget：

$$
c=\frac{\mathrm{KL}(Q\|P)+\log(201/0.05)}{200}
=0.042077.
$$

脚本在 $[0.043,1)$ 上求

$$
\operatorname{kl}(0.043\|r)=c
$$

的最大 $r$，得到 $0.127958$。Pinsker 外包络给 $0.188046$。若同时从五条预注册 high-probability certificate 中选择，简单 union ledger 用 $\delta/5=0.01$，PAC-Bayes inverse-kl 变为 $0.138265$。

> [!warning] 共同事件的适用范围
> information 轨的基础式是 expected statement，并不能只靠把 $\delta$ 除以 5 变成 high-probability certificate。图中 $\delta/5$ 的演示只针对可以各自建立 tail event 的候选路线；跨类型选择仍须先换成同类结论。

## 七、轨道 C：information 与证书选择

### 7.1 exact binary channel MI

对均匀 $X$ 与对称通道，输出 $W$ 也均匀：

$$
I(X;W)=\log2-H_b(q).
$$

canonical $q=0.8$ 给

$$
I=0.192745\ \text{nats}.
$$

one-bit ceiling 只是

$$
I\le H(W)\le\log2=0.693147.
$$

它比 actual MI 松，不得把 ceiling 当测量结果。

### 7.2 expected generalization radius

0—1 loss 的一个标准 expected bound 是

$$
|\mathbb E[R(W)-\widehat R_S(W)]|
\le\sqrt{\frac{I(S;W)}{2m}}.
$$

若学习通道只通过 $X=f(S)$ 生成 $W$，则 $I(S;W)=I(X;W)$。canonical $m=200$ 时 exact 与 bit-ceiling radii 是

$$
0.021951,\qquad0.041628.
$$

这些是 expected signed-gap radii，不是 $R(W)$ 的 upper bound。empirical risk 尚未加进来，也没有 $\delta$。

## 八、评分者随机指定、跨轨盲参与防挑题协议

固定审计 blind fixture：

~~~text
--stability-size 16
--bernoulli-p 0.3
--lipschitz 1.2
--regularization 3
--step-sizes 0.1,0.08,0.04
--certificate-size 160
--compression-k 4
--message-bits 5
--delta 0.08
--prior 0.6,0.4
--posterior 0.75,0.25
--empirical-risks 0.04,0.3
--information-size 160
--channel-accuracy 0.7
--route-count 4
~~~

预期 stdout：

~~~text
TRACK A m=16 exact_beta=0.121094 expected_gap=0.026250 rerm_beta=0.060000 sgd_beta=0.039600 step_sum=0.220000
TRACK B m=160 compression=0.147925 empirical_gibbs=0.105000 posterior_kl=0.049857 kl_budget=0.047856 inverse_kl=0.223594 pinsker=0.259687 joint_inverse_kl=0.235887
TRACK C m=160 accuracy=0.700000 exact_mi=0.082283 bit_budget=0.693147 exact_radius=0.016035 bit_radius=0.046541 routes=4 joint_delta=0.020000
~~~

该 fixture 用于独立审计，不得作为个人 nonce。个人 blind run 至少改变两个轨道的参数；评分者应要求先写：

- $\beta_m$ 对 $m$ 的方向；
- RERM 对 $\lambda$、SGD 对 $\sum\eta_t$ 的方向；
- compression 对 $k,b,m,\delta$ 的方向；
- PAC-Bayes 对 posterior/prior 距离和 $\widehat R(Q)$ 的方向；
- MI 对 $q$ 从 $1/2$ 远离的方向。

## 九、盲参数干预怎样才算独立

有效盲参：

1. 由 nonce 在预测封存后确定；
2. 改变至少两个轨道；
3. 不能从 canonical 图直接读出；
4. 包含一个量词/支持/概率合同检查；
5. 使用全新 output path。

无效盲参：

- 只改 SVG 文件名；
- 把 $m=20$ 改成 $21$，但其余全部照 canonical；
- 运行后才写方向预测；
- 用固定审计 fixture 冒充个人随机轨；
- 非 canonical 参数写入 canonical SVG；
- 只比较数值大小，不写 statement type。

## 十、独立审计固定 fixture

canonical artifact：

~~~text
SHA256 ef8b95b87a1595550669fc4a1db3d623f8f4d6ad5c7ee7463eae5e06498fd6a6
~~~

固定 blind artifact：

~~~text
SHA256 e6a4bd8767c33414445f9b7920e5ddf5cbd11f5577ff5a00ac80b44f22df7736
~~~

[[algorithmic_generalization_cumulative_contract_audit.py]]不得调用 gate 内部函数作为 oracle。它要独立重算：

1. 相邻 count 的 squared-loss differences；
2. Binomial expected gap；
3. RERM/SGD formulas；
4. $\log\binom mk$ compression；
5. finite KL、Gibbs risk、binary-kl bisection；
6. binary-channel joint table 与 MI；
7. canonical/盲参 stdout、SVG/XML/hash；
8. 非法 $k\ge m$、非法 probability、support violation 与 canonical overwrite rejection；
9. LT-33—40、题卷/详解、五处状态面。

## 十一、运行命令

canonical：

~~~bash
python3 00-知识库管理/_labs/code/algorithmic_generalization_cumulative_gate.py
~~~

个人 blind run 示例只展示命令形状；参数必须由 nonce 重新给出：

~~~bash
python3 00-知识库管理/_labs/code/algorithmic_generalization_cumulative_gate.py \
  --stability-size <m_a> \
  --bernoulli-p <p> \
  --certificate-size <m_b> \
  --compression-k <k> \
  --prior <p_1,p_2> \
  --posterior <q_1,q_2> \
  --information-size <m_c> \
  --channel-accuracy <q> \
  --output <new-path.svg>
~~~

脚本保护：

- 非 canonical 参数没有 --output 时拒绝；
- 非 canonical 参数指向 canonical SVG 时拒绝；
- $k\ge m$、概率越界、质量不归一或 $Q\not\ll P$ 时拒绝；
- canonical 参数允许写到临时路径，便于审计字节确定性。

## 十二、证据状态机

~~~mermaid
flowchart LR
    A[not-attempted] -->|口试与闭卷原稿封存| B[attempted]
    B -->|对象/计算/证明/边界/迁移五门通过| C[written-pass]
    C -->|nonce 跨轨盲参 + 非法合同拒绝| D[blind-pass]
    D -->|48h 换机制| E[retained]
    E -->|14d 陌生 AI 迁移| F[volume-pass]
    A -.材料回归不改变个人状态.-> A
~~~

材料状态与学习状态始终分开：

- 题卷、详解、gate、SVG 和 audit 通过：**material regression-passed**；
- 没有学习者原稿：**learner not-attempted**；
- canonical stdout 复述：最多 **practice**；
- 只有 D、E、F 的真实证据才允许升级个人状态。

## 十三、48 小时与 14 天出口

48 小时至少换一个机制，而非只换数字：

- output noise：同时审计 shared-seed stability 与 $I(S;W)$；
- Gaussian PAC-Bayes：检查 continuous KL 与 point mass support；
- side-message compression：把新增 decoder family 写进 description budget。

14 天迁移需对陌生问题完成：

1. predictor/loss/sample/randomness；
2. complexity object；
3. theorem assumptions；
4. exact vs bound；
5. expected vs tail；
6. selection budget；
7. 一个失败反例；
8. legal/nonvacuous/tight/explanatory 四级结论。
