---
type: experiment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/qualification, learning-theory/generalization, curriculum/capstone]
assessment_id: LT-QUAL-01
gate_id: LT-QUAL-01-GATE
seed: exact-enumeration
code: "[[00-知识库管理/_labs/code/learning_theory_qualification_01_gate.py]]"
figure: "[[00-知识库管理/_assets/plots/learning-theory/plot-learning-theory-qualification-01-gate-v2.svg]]"
related: ["[[资格考 - 学习理论 I：从风险到算法依赖泛化（20.1—20.5）]]", "[[资格考解答 - 学习理论 I：从风险到算法依赖泛化（20.1—20.5）]]", "[[学习理论完整课程地图与掌握标准]]", "[[推导与实验 MOC]]"]
created: 2026-08-28
updated: 2026-08-28
---

# 实验 - 学习理论资格考 I 跨卷累计复现门

> [!abstract] 这道实验门检查什么
> 这不是把五张旧图放在一起，也不是用数值替代理论。它让风险、finite/VC 容量、stability、compression、PAC-Bayes 与 information 共用一个 finite threshold learning problem，再强制把 predictor、sample 和 statement type 分账。通过标准不是“跑出了漂亮曲线”，而是能在看 stdout 前解析预测、在看数值后解释为什么某些 bound 仍不能比较。

先读图，不看后文数字，回答：为什么黄色 compression 数值虽然最小，却不能自动成为紫色 Gibbs posterior 的风险证书？为什么红色 stability 等于 1，却不否定蓝绿色 expected gap 很小？

![[00-知识库管理/_assets/plots/learning-theory/plot-learning-theory-qualification-01-gate-v2.svg|920]]

> [!figure] 实验图｜一个模型、五条证明路线、三本互不混账的账簿
> A 轨枚举全部训练样本和全部替换，核对 exact learner、ghost identity、worst-case stability 与 output channel；B 轨在较大的 balanced certificate sample 上计算 finite-class、compression 与 PAC-Bayes 证书；C 轨不再画一个“谁最小谁最好”的排行榜，而是先列 predictor 与 statement type。图由 [[learning_theory_qualification_01_gate.py]] 确定性生成，无 Monte Carlo、无第三方依赖。

**怎样读图。** 先横向读底部 proof spine，确认每条路线从同一个 observation/loss 起步；再纵向读三轨。A 的 `gap = ghost` 是恒等式校准，`beta=1` 是 worst-case 反例；B 的五根条形并不都控制同一 predictor；C 明示 expected gap 与 high-probability risk 不在同一坐标轴。

**图没有证明什么。** 它不证明所有阈值 ERM、所有 stability theorem 或所有深度网络都表现如此；不证明较小的实验数值就是较好的 universal theorem；也不把仓库材料回归变成学习者个人通过。

## 零、执行协议：推导必须先于 stdout

```mermaid
flowchart LR
    P[核验五卷 retained] --> W[手写三轨对象合同]
    W --> H[解析预测与数值区间]
    H --> F[冻结 attempt_id / hash]
    F --> N[评分者公布 scorer nonce]
    N --> B[跨至少两轨盲参数]
    B --> X[新 output 执行]
    X --> E[保存 stdout / SVG / SHA-256]
    E --> I[非法合同注入]
    I --> S[才可看 canonical 与详解]
    S --> R[48 h 换机制复测]
```

### 0.1 运行前必须冻结的内容

在任何命令前，提交一页 prediction sheet：

1. 写出 observation、label、loss、Bayes rule、class 与 learner；
2. 推出 lexicographic ERM 的输出 law，不得从脚本抄；
3. 预测 expected empirical risk、population risk、ghost replacement 与 stability 的方向和范围；
4. 写出 finite radius、compression code length、posterior KL 和 inverse-kl equation；
5. 给五条 route 各写 predictor 与 statement type；
6. 预测至少一个“数值更小但不能比较”的结果；
7. 记录 `attempt_id`、开始时间、题卷 hash 和预测页 hash。

若先看 canonical stdout 或图中数值，A/B 数值轨只能记演示，不能记盲测。

### 0.2 scorer nonce 与防挑题

评分者在两场闭卷原稿冻结后生成 nonce：

- SHA-256 首字节模 3 指定 A/B/C 主轨；
- 第二字节指定至少跨两个轨道的一组未见参数；
- 第三字节指定一个非法合同：枚举预算超限、certificate size 不整除、prior mass 错、support violation 或覆盖 canonical；
- 参数给出后不得因结果“不好看”重抽；
- canonical 与本页固定 blind fixture 只用于材料回归，不能当个人 blind evidence。

## 一、共同模型与十二层最小合同

### 1.1 生成机制

$$
\mathcal X=\{0,1,\ldots,d-1\},\qquad
X\sim\operatorname{Unif}(\mathcal X),
$$

$$
Y=h_{t_*}(X)=\mathbf 1\{X\ge t_*\},qquad
\mathcal H=\{h_t:t=0,\ldots,d\}.
$$

loss 是 0—1 loss。Bayes rule 与 class optimum 都是 $h_{t_*}$，两者 risk 都为 0。算法 $A$ 在 empirical minimizers 中选阈值 index 最小者。这个 tie-break 使 $S\mapsto T=A(S)$ 成为 deterministic channel。

### 1.2 为什么是同一个模型，却不是同一个数值问题

| 轨 | sample | predictor | 随机性 | 输出陈述 |
|---|---|---|---|---|
| A | $m=6$ i.i.d. all-sample enumeration | lexicographic deterministic ERM | training sample | exact expectation / worst case |
| B finite | $m_c=200$ balanced certificate | Gibbs $t\sim Q$ | posterior draw + certificate event | high-probability risk |
| B compression | 同一规模的 realizable sample | fixed decoder 重构的 ERM | sample/event | high-probability risk |
| B PAC-Bayes | $m_c=200$ balanced certificate | Gibbs $t\sim Q$ | posterior draw + certificate event | high-probability risk |
| C information | A 轨的 deterministic output channel | small-$m$ ERM | training sample | expected signed gap radius |

balanced certificate sample 被选作可手算 calibration：每个 domain point 出现相同次数，因此每个 threshold 的 empirical risk 恰等于 true risk。它不是声称真实 benchmark 会如此平衡，也不是从 i.i.d. tail theorem 中抽出的典型样本。

### 1.3 restriction 与 VC 接口

在一个有序样本上，threshold labelings 只有“一串 0 后接一串 1”。因此 VC dimension 为 1；在完整 $d$ 点 domain 上 restriction 数为 $d+1$。脚本报告 `vc=1` 和 `growth=d+1`，用于检查容量对象没有误写成参数数量。

## 二、A 轨：全部样本、全部替换、一个 output channel

### 2.1 不运行代码的解析推导

令 $M_-$ 是样本中最大的负类点。lexicographic consistent ERM 为

$$
T=
\begin{cases}
0,&\text{没有负类点},\\
M_-+1,&\text{否则}.
\end{cases}
$$

canonical $d=5,t_*=3,m=6$ 时：

$$
\begin{aligned}
P(T=0)&=(2/5)^6,\\
P(T=1)&=(3/5)^6-(2/5)^6,\\
P(T=2)&=(4/5)^6-(3/5)^6,\\
P(T=3)&=1-(4/5)^6.
\end{aligned}
$$

必须在运行前算出四个概率和其和为 1。对任意输出 $t$，

$$
R(h_t)=\frac{|t-t_*|}{d}.
$$

由于输出总 consistent，$\widehat R_S(T)=0$；因此 expected gap 就是由 output law 加权的 population risk。

### 2.2 exact enumeration 做了什么

脚本枚举 $d^m$ 个 point sequences。对每个 sample：

1. 计算全部 $d+1$ 个 threshold 的 empirical errors；
2. 按 `(error, threshold)` 选 lexicographic ERM；
3. 累计 output law、empirical risk 与 population risk；
4. 对每个 index 和每个 replacement point 构造相邻样本；
5. 累计 ghost replacement term；
6. 对所有 test point 搜索最大 loss difference，得到 direct stability。

这是 finite exhaustive verification，不是 Monte Carlo approximation。它能证明脚本定义的有限 fixture 输出，但一般 ghost identity 仍由 exchangeability 解析证明。

### 2.3 ghost 与 stability 为什么共享 replacement 却给出不同印象

ghost identity 是

$$
\mathbb E\operatorname{gen}(A,S)
=\frac1m\sum_i\mathbb E[
\ell(A(S^{i\leftarrow Z_i'}),Z_i)-\ell(A(S),Z_i)].
$$

它对 replacement effect 取数据分布下的平均。direct uniform stability 则对相邻样本和 test point 取 supremum。canonical 中，一个极少见相邻对即可令 supremum 等于 1；但其分布平均仍只有约 0.063。两者回答的是不同问题。

### 2.4 output entropy 与 mutual information

因为 $T=A(S)$ deterministic，

$$
I(S;T)=H(T)=-\sum_tP(T=t)\log P(T=t).
$$

对 $[0,1]$ loss，Hoeffding lemma 给 $\sigma=1/2$，所以 basic information radius 是

$$
\sqrt{\frac{I(S;T)}{2m}}.
$$

它控制 expected gap 的绝对值，不是给当前一次输出 $T=t$ 的 conditional risk 区间。运行前应预测：entropy 有限、radius 大于 exact gap、radius 小于 trivial range 1。

### 2.5 A 轨通过标准

- 手推 output law 与六位数 exact gap；
- 口头证明 ghost identity，不引用 enumeration 当证明；
- 给出 stability=1 的相邻样本 witness；
- 解释 finite MI 与 worst-case instability 可同时成立；
- 能修改 tie-break 后重新判断所有四个量，而不是只改图标题。

## 三、B 轨：大样本证书账

### 3.1 balanced certificate 与 posterior

canonical 使用 $m_c=200$，每个 $x$ 出现 40 次；$\delta=0.05$；

$$
P=(1/6,\ldots,1/6),
$$

$$
Q=(0.02,0.03,0.10,0.70,0.10,0.05).
$$

六个 thresholds 的 empirical/true risks 是

$$
(0.6,0.4,0.2,0,0.2,0.4),
$$

故 Gibbs empirical/true risk 都是 0.084。相等来自构造的 balanced sample，不是 generalization theorem 的结论。

### 3.2 finite-class route

two-sided Hoeffding + union 给共同半径

$$
r_{\rm finite}=\sqrt{\frac{\log(2(d+1)/\delta)}{2m_c}}.
$$

在共同事件内，可对 data-dependent $Q$ 加权，得到

$$
R(Q)\le\widehat R(Q)+r_{\rm finite}.
$$

这里的 predictor 是 Gibbs $Q$。若改成 posterior-mean weights，在离散 threshold family 中甚至未必还是一个合法 hypothesis。

### 3.3 compression route

脚本采用一个 sample point 加 `compression-bits` side bits 的固定 exact compression certificate：

$$
R(\widehat h_{\rm comp})
\le\frac{\log\binom{m_c}{1}+b\log2+\log(1/\delta)}{m_c-1}.
$$

这个数服务于 reconstructed consistent ERM，不服务于 Gibbs $Q$。实验通过者必须先写 predictor 名字，再写数值。

### 3.4 PAC-Bayes-kl route

$$
\mathrm{KL}(Q\|P)=\sum_tQ_t\log\frac{Q_t}{P_t},
$$

$$
c=\frac{\mathrm{KL}(Q\|P)+\log((m_c+1)/\delta)}{m_c},
$$

$$
R(Q)\le\operatorname{kl}^{-1}_+(\widehat R(Q),c).
$$

脚本用 deterministic bisection 求最大的 $r\in[\widehat R,1]$ 使 $\operatorname{kl}(\widehat R\|r)\le c$。需要手检 bracket：endpoint 应不小于 empirical risk；把 endpoint 代回 Bernoulli KL 应接近 budget；增加 KL 或减小 $\delta$ 应令 endpoint 不降。

### 3.5 route selection budget

若从 $J$ 条预注册 high-probability certificate 中事后选最小者，等权 union 把 PAC-Bayes 的 $\delta$ 改成 $\delta/J$：

$$
c_J=\frac{\mathrm{KL}(Q\|P)+\log((m_c+1)J/\delta)}{m_c}.
$$

canonical 取 $J=5$。实验必须同时报告未校正 endpoint 与共同预算 endpoint，不能把前者拿来支撑“我们比较五个后仍有总体 95% 置信”。

### 3.6 B 轨通过标准

- 手算 Gibbs empirical risk 和 posterior KL；
- 写清 finite event 为什么能转移到任意 $Q$；
- 说明 compression endpoint 控制另一个 predictor；
- 独立实现或手工 bracket 一次 inverse-kl；
- 干预 $m_c,\delta,Q,P,b,J$ 中至少两个，并预测单调方向；
- 构造一个合法但 vacuous 的 posterior/certificate。

## 四、C 轨：先路由，再比较

### 4.1 五路线最小字段

| route | 必填对象 | 默认 statement | 最常见非法跨越 |
|---|---|---|---|
| finite/VC/Rademacher | fixed class/restriction/loss class | uniform high probability | 对 same-data 新设计 class 不付成本 |
| stability | 完整算法、adjacency、seed coupling | expected gap | 从平均替换实验跳到 worst-case theorem |
| compression | encoder/decoder/message/consistency | deterministic risk tail | 参数少等同 sample compression |
| PAC-Bayes | independent prior、posterior、Gibbs | high-probability Gibbs risk | 直接认证 posterior mean/MAP |
| information | joint $P_{SW}$、product $P_SP_W$ | expected gap | 把 proxy entropy 当 MI，或升级成 tail |

### 4.2 一个合法 minimum 的判定顺序

对候选 bounds $B_1,\ldots,B_J$，按下列顺序过滤：

1. theorem hypotheses 是否成立；
2. predictor 是否就是部署 predictor；
3. risk/loss/distribution 是否相同；
4. statement type 是否都能支撑目标声明；
5. sample 与 conditioning 是否一致；
6. 是否支付 route/model/checkpoint selection；
7. 只在剩余合法且共同事件成立的数中比较 tightness。

“先看谁最小，再补解释”会系统性选择最乐观的错误坐标。

### 4.3 C 轨的 AI 迁移

对 fine-tuned language model，把 threshold index 换成 checkpoint/weights 并不会自动保留 threshold theorem。必须重新声明：prompt-response sampling unit；sequence/token loss；base checkpoint 与 LoRA class；完整 optimizer/seed/early-stop algorithm；PAC-Bayes 的 Gibbs sampling；最终 deterministic deployment；public-data contamination；certificate/test 的时间线。C 轨通过要求是能写出一个会失败的研究合同，而不是只说“用 PAC-Bayes 解释大模型”。

## 五、canonical 运行与复核

在仓库根目录执行：

```bash
python3 00-知识库管理/_labs/code/learning_theory_qualification_01_gate.py
```

canonical stdout 的三行核心部分应为：

```text
TRACK A d=5 target=3 enum_m=6 hypotheses=6 vc=1 growth=6 bayes=0.000000 class=0.000000 expected_emp=0.000000 expected_pop=0.062579 ghost=0.062579 stability=1.000000
TRACK B cert_m=200 gibbs_emp=0.084000 gibbs_true=0.084000 finite=0.201054 compression=0.045162 kl=0.748346 pac=0.191657 joint_pac=0.202908
TRACK C output_entropy=0.711929 info_radius=0.243572 output=0:0.004096,1:0.042560,2:0.215488,3:0.737856,4:0.000000,5:0.000000 routes=5 joint_delta=0.010000
```

canonical SVG：

```text
00-知识库管理/_assets/plots/learning-theory/plot-learning-theory-qualification-01-gate-v2.svg
SHA-256 e61df86632115cab0f592b07661abd9fdafa1c81f45fff9570ea51fb7274b7f6
```

### 5.1 四个独立 sanity checks

1. output probabilities 和为 1；
2. `expected_emp=0` 且 `expected_pop=ghost` 到 $10^{-12}$；
3. $0.084<0.191657<0.201054$，但不能据此把 PAC-Bayes 宣称为普遍更紧；
4. joint-budget PAC endpoint 不小于 uncorrected endpoint。

### 5.2 canonical 图只算材料锚点

得到相同 hash 说明当前 Python 与 SVG 字节一致。它不说明学习者没有看答案、不说明推导由本人完成、不说明能迁移到新 learner。因此个人证据目录必须保存 scorer 给出的新参数和独立 output。

## 六、固定回归 blind fixture

下面 fixture 供独立材料审计脚本使用，学习者不得把它当个人 blind。它同时改变 A、B、C 三轨：

```bash
python3 00-知识库管理/_labs/code/learning_theory_qualification_01_gate.py \
  --domain-size 6 \
  --target-threshold 4 \
  --enumeration-size 5 \
  --certificate-size 240 \
  --delta 0.08 \
  --prior '0.1,0.1,0.1,0.15,0.2,0.15,0.2' \
  --posterior '0.02,0.03,0.05,0.1,0.65,0.1,0.05' \
  --compression-bits 2 \
  --route-count 4 \
  --output /tmp/lt-qual-blind.svg
```

回归锚点：

```text
TRACK A d=6 target=4 enum_m=5 hypotheses=7 vc=1 growth=7 bayes=0.000000 class=0.000000 expected_emp=0.000000 expected_pop=0.094822 ghost=0.094822 stability=1.000000
TRACK B cert_m=240 gibbs_emp=0.095000 gibbs_true=0.095000 finite=0.198730 compression=0.039300 kl=0.512753 pac=0.191608 joint_pac=0.200615
TRACK C output_entropy=1.012295 info_radius=0.318166 output=0:0.004115,1:0.027135,2:0.100437,3:0.270190,4:0.598122,5:0.000000,6:0.000000 routes=4 joint_delta=0.020000
SHA-256 45aa1b16b5a0f8e7ce1c5125e97414e0fc871b72af16a07c6e7bf8f9f73ab218
```

固定 fixture 的用途是让审计实现不依赖 canonical 参数，防止脚本把默认常数硬编码后“自证通过”。

## 七、非法合同注入

每次正式 blind 至少测试 scorer 指定的一项，预期为非零 exit 且不得产生/覆盖 artifact：

| 注入 | 示例 | 应拒绝原因 |
|---|---|---|
| 枚举预算超限 | `--domain-size 7 --enumeration-size 7` | $7^7>500000$，避免伪装成已做 exhaustive check |
| certificate 不整除 | `--domain-size 6 --certificate-size 241` | balanced design 无法让每点等频 |
| prior mass 错 | prior 总和不为 1 | 不是概率分布 |
| support violation | 某 $P_t=0,Q_t>0$ | $Q\not\ll P$，KL/theorem 非法 |
| 非默认覆盖 canonical | blind 参数配 canonical `--output` | 防止污染材料锚点 |
| 非默认无 output | 改参数但不传 `--output` | 防止悄悄覆盖 canonical |

失败 stderr 本身是资格证据的一部分：它证明学习者理解边界不仅是“算出一个数”，还包括拒绝一个无定义或不可审计的实验。

## 八、个人 blind artifact 规范

建议目录：

```text
artifacts/<attempt_id>/
  protocol.md
  prediction.md
  command.txt
  stdout.txt
  stderr-invalid.txt
  lt-qual-blind.svg
  sha256.txt
  interpretation.md
  oral-record.md
```

`protocol.md` 至少记录：日期、Python 版本、git commit、scorer nonce、参数、主轨、非法合同、查看答案时间。`interpretation.md` 必须回答：

1. 哪些预测方向正确、哪些错误；
2. exact identity、theorem consequence 与 finite output 分别是什么；
3. 哪两个数看似可比但实际不控制同一对象；
4. 哪个证书 legal 但 vacuous，或 tight 但 explanatory 弱；
5. 若换到真实 AI 模型，哪三个 hypotheses 最先失效。

## 九、48 小时和 14 天复测

### 9.1 48 小时：换机制，不只换参数

评分者在以下三项抽一项：

- 改成 largest-consistent 或 randomized-consistent learner；
- 加独立 label noise，使 consistency/compression 前提失效；
- 将 finite posterior 换成 Gaussian parameter posterior，并审计 support、KL 与 posterior-mean deployment。

学习者须先写“哪些证明仍成立、哪些常数改变、哪些对象不再定义”，再改代码或另写最小实验。只重复本页命令不能记 retained。

### 9.2 14 天：陌生论文证书路由

选择一篇此前未读的学习理论或深度泛化论文，只取一个主 theorem 和一个实验 claim：填写十二层账本、重建 proof interface、指出一个 failure witness、判断 bound 是否可计算、审计模型/route selection，并把博客只作为线索回链到论文/教材原文。

## 十、通过与证据边界

本实验的材料状态在独立审计、blind fixture、失败注入、SVG XML 与视觉检查全通过后可记 `material_status: regression-passed`。个人状态仍从 `not-attempted` 开始。正式通过 `LT-QUAL-01-GATE` 需要：

- [ ] 五卷 retained 前置证据；
- [ ] 运行前 prediction sheet 与 hash；
- [ ] scorer nonce 指定的跨轨 blind；
- [ ] command/stdout/SVG/hash 完整；
- [ ] 指定非法合同被拒绝；
- [ ] 能口头解释 exact gap、ghost、stability、KL/MI 与 predictor identity；
- [ ] 48 小时换机制通过；
- [ ] 14 天陌生论文路由通过。

自动脚本只能核验材料的一致性和有限 fixture，不能替代闭卷推导、口试、迁移与延迟保持。
