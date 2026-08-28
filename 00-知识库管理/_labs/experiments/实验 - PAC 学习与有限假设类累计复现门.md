---
type: experiment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/pac, learning-theory/finite-classes, reproducible-evidence]
assessment_id: PAC-CUM-01
scope: [LT-09, LT-10, LT-11, LT-12, LT-13, LT-14, LT-15, LT-16]
script: "[[pac_finite_class_cumulative_gate.py]]"
assessment: "[[阶段测验 - PAC 学习与有限假设类（20.2）]]"
solution: "[[阶段测验解答 - PAC 学习与有限假设类（20.2）]]"
figure: "[[plot-pac-finite-class-cumulative-gate-v2.svg]]"
related: ["[[PAC 学习与有限假设类 MOC]]", "[[学习理论完整课程地图与掌握标准]]", "[[推导与实验 MOC]]"]
created: 2026-08-28
updated: 2026-08-28
---

# 实验 - PAC 学习与有限假设类累计复现门

> [!abstract] 实验问题
> 有限类 PAC 的上界到底控制什么随机事件？Union Bound 与精确概率差多少？为什么不可知 ERM 选中者的训练风险系统性偏低，却仍能被 simultaneous event 覆盖？编码长度怎样分配失败预算，而统计下界又怎样从两个难分辨世界产生？本实验用三个完全可枚举的有限模型，把“定理上界、有限模型精确量、算法选择量与下界证书”并排放在一张图里。

![[00-知识库管理/_assets/plots/learning-theory/plot-pac-finite-class-cumulative-gate-v2.svg|1200]]

> [!figure] 实验图｜可实现排除、不可知选择与编码—检验边界
> **对象与结论：** A 并排显示单个坏假设生存、独立坐标模型的 exact any-bad failure、Union Bound 与 exponential relaxation；B 用 exact Binomial sums 计算 lexicographic ERM 的训练/总体风险，同时给 simultaneous Hoeffding radius；C 把 Kraft-weighted Occam 半径与 Bernoulli 两点世界的 exact TV、最优检验错误和 Pinsker 下界分层。生成脚本：[[pac_finite_class_cumulative_gate.py]]；无 Monte Carlo，canonical 与盲参均做字节确定性回归。
>
> **怎样读图：** 先在 A 核对“精确概率 $\le$ Union $\le$ exponential certificate”；再在 B 分开 expected selection gap 与 high-probability $2\alpha$；最后在 C 分开“存在算法的上界预算”和“任意算法面对难世界的下界”。柱长、点位和证书数字属于不同统计对象，不能直接互减。
>
> **适用边界（图没有证明什么）：** exact any-bad 与 exact uniform-event probability 使用脚本特设的跨 hypothesis 独立坐标；一般 finite-class PAC theorem 不需要该独立性，只保留 Union Bound。图不证明现实深网是有限类、插值等于 realizability、压缩推出因果真实性，也不把 Bernoulli toy 下界自动推广到任意 AI 部署问题。

## 一、它验证什么，不验证什么

本实验验证：

1. 可实现制度下，固定坏假设的生存概率、任意坏假设生存的精确并集概率、Union Bound 与指数松弛的顺序；
2. 不可知制度下，finite-class simultaneous radius、共同事件的精确失败概率，以及 lexicographic ERM 的 exact expected selection gap；
3. prefix-free lengths 的 Kraft budget 怎样变成逐假设置信半径；
4. Bernoulli 两点世界的 exact total variation、最优检验错误和 Pinsker-certified lower bound；
5. canonical 与盲参数 SVG/stdout 的字节确定性和覆盖保护。

它不验证：

- 现实神经网络类满足有限类假设；
- 训练 observations 或 token 独立同分布；
- empirical interpolation 等于 realizability；
- Hoeffding 对无界 log loss 仍可直接使用；
- Occam 证书推出因果真实性；
- 一个 finite toy lower bound 自动成为所有 AI 系统的 minimax 下界；
- 仿真曲线替代[[阶段测验 - PAC 学习与有限假设类（20.2）|闭卷证明]]。

## 二、执行顺序、答案隔离与 scorer nonce

严格按顺序执行：

1. 完成 20 分钟口试和 210 分钟闭卷；
2. 冻结 `attempt_id`、原稿、起止时间和 SHA-256；
3. 在未看本页 canonical 数值的条件下，写完三轨解析校准；
4. 评分者公布 `scorer nonce`，随机指定主轨和至少一个跨轨盲参；
5. 对指定参数先写数值区间、单调性、界的方向和可能的松弛来源；
6. 使用非 canonical `--output` 运行；
7. 保存 command、stdout、SVG、SHA-256 与运行前预测；
8. 才可对照 canonical 与独立详解；
9. 48 小时换机制，14 天迁移到陌生 AI 选择问题。

推荐轨道映射：取 nonce 的 SHA-256 首字节模 3，余数 0/1/2 对应 A/B/C。下一字节决定盲参模板，参数数值由评分者另存，不提前写入学习者笔记。

> [!warning] 防止循环认证
> 本仓库中的 canonical hash 是材料回归 fixture。学习者复述已知 stdout，或先运行再填写“预测”，只能记 practice。个人证据必须来自新的输出路径、新的参数和运行前冻结的解析预期。

## 三、进入实验前的解析校准门

不得运行代码，先完成以下内容。

### 3.1 Track A 校准

设 $M$ 个坏假设风险都为 $r$，每个坏假设对应独立错误坐标，样本量为 $m$：

1. 手推单个坏假设生存概率 $s=(1-r)^m$；
2. 手推精确失败概率 $1-(1-s)^M$；
3. 写出 $\min\{1,Ms\}$ 和 $\min\{1,Me^{-mr}\}$；
4. 预测增大 $m$、增大 $r$、增大 $M$ 分别怎样改变四个量；
5. 解释独立坐标被删掉后，为什么仍保留 Union Bound，却失去精确乘积式。

### 3.2 Track B 校准

对 risks $q_1,\ldots,q_K$ 和 sample size $m$：

1. 写出 $N_j\sim\operatorname{Binomial}(m,q_j)$；
2. 手推 simultaneous radius

   $$
   \alpha=\sqrt{\frac{\log(2K/\delta)}{2m}};
   $$

3. 说明 exact uniform failure 为什么可由各 $N_j$ 落在区间内的概率乘积得到——这依赖脚本的 loss-coordinate 独立构造；
4. 对 lexicographic ERM，手推

   $$
   \Pr(\widehat j=j,N_j=c)
   =\Pr(N_j=c)
   \prod_{i<j}\Pr(N_i>c)
   \prod_{i>j}\Pr(N_i\ge c);
   $$

5. 预测 risks 间距缩小、$K$ 增大、$m$ 增大时 selection gap 与 class excess 的变化方向。

### 3.3 Track C 校准

1. 检查给定 code lengths 的 Kraft sum；
2. 手推

   $$
   \alpha_j=\sqrt{\frac{\log(2/\delta)+L_j\log2}{2m}};
   $$

3. 写出等先验二元检验的 $P_e^*=(1-\mathrm{TV})/2$；
4. 手推 Bernoulli$(1/2-\gamma)$ 到 Bernoulli$(1/2+\gamma)$ 的 KL；
5. 预测 $\gamma\downarrow0$ 或 testing sample size 减小时，exact testing error 和 Pinsker lower bound 怎样变。

只有三轨均完成解析校准，实验才可记入 evidence gate。

## 四、三轨统一对象合同

| 字段 | Track A | Track B | Track C |
|---|---|---|---|
| observation | target label + $M$ 个错误坐标 | $K$ 个 hypothesis-loss 坐标 | code index；或单个 Bernoulli bit |
| sampling | coordinates/samples 独立 | coordinates/samples 独立 | prefix-free budget；Bernoulli product law |
| learner/decision | 从版本空间任取一致者 | lexicographic exact ERM | weighted certificate；Bayes-optimal binary test |
| comparator | 零风险 target | $\min_jq_j$ 的类内 oracle | 每个 code hypothesis；正确 world |
| exact quantity | any-bad survival probability | ERM expected population/train risk | Kraft sum、TV、optimal testing error |
| theorem quantity | union/exponential failure certificate | Hoeffding radius 与 $2\alpha$ bridge | weighted radius、Pinsker lower bound |
| 关键边界 | exact product 需跨 $h$ 独立 | exact sums 需跨 $j$ 独立，定理不需 | language 预先固定；lower bound problem class 固定 |

三个有限模型被刻意设计为可枚举。精确模型使用的跨 hypothesis 坐标独立性不是一般 PAC 定理假设；它只为了提供一个可审计的 exact comparator。

## 五、轨道 A：可实现版本空间的生存证书

### 5.1 模型

target $h^*$ 总是输出正确标签。对 $j=1,\ldots,M$，观察包含 $E_j\sim\operatorname{Bernoulli}(r)$；$h_j$ 在 $E_j=1$ 时出错。全部 $E_j$ 及全部样本位置相互独立。

固定 $h_j$ 在 $m$ 个样本上与 target 一致，当且仅当 $m$ 个对应坐标全为 0：

$$
s=\Pr(h_j\in V(S))=(1-r)^m.
$$

### 5.2 四个不得混称的量

$$
\begin{aligned}
p_{\rm exact}&=1-[1-(1-r)^m]^M,\\
p_{\rm union}&=\min\{1,M(1-r)^m\},\\
p_{\rm exp}&=\min\{1,Me^{-mr}\},\\
m_{\rm suff}&=\left\lceil\frac{\log(M/\delta)}r\right\rceil.
\end{aligned}
$$

$p_{\rm exact}$ 是这个独立坐标世界的真实失败概率；$p_{\rm union}$ 是不使用跨假设独立性的证书；$p_{\rm exp}$ 又把 $(1-r)^m$ 松弛为 $e^{-mr}$。图中它们接近不等于概念相同。

### 5.3 正确读图

先从单假设 survival 读起，再看 exact any-bad，最后比较两层上界。若 $m_{\rm suff}$ 明显大于 exact minimal $m$，这是 distribution-free proof 的保守性，不是程序误差。

### 5.4 盲参干预

至少做两项：

- 固定 $M,r$，使 $m$ 增加 25%；
- 固定 $m,r$，将 $M$ 加倍；
- 固定 $M,m$，增大 $r$；
- 48 小时门把等风险 $r$ 改成 $r_j$，自行重写脚本或手推乘积。

必须记录哪些变化影响精确模型，哪些只影响 theorem certificate。

## 六、轨道 B：不可知 ERM、双侧共同事件与选择偏差

### 6.1 模型

每个 observation 含 $K$ 个独立 loss coordinates，$L_j\sim\operatorname{Bernoulli}(q_j)$。因此

$$
N_j=mR_S(h_j)\sim\operatorname{Binomial}(m,q_j)
$$

且不同 $j$ 的 counts 独立。算法取经验 count 最小者；平票选最小 index。

这不是说现实候选模型的错误必然独立。它让 finite sum 可精确枚举，而 Hoeffding + Union Bound 本身不使用跨 $j$ 独立性。

### 6.2 exact lexicographic selection

若 $h_j$ 以 count $c$ 胜出，则所有更早 hypothesis 必须严格大于 $c$，所有更晚 hypothesis 至少为 $c$。因此

$$
w_{j,c}=\Pr(N_j=c)
\prod_{i<j}\Pr(N_i>c)
\prod_{i>j}\Pr(N_i\ge c).
$$

脚本检查 $\sum_{j,c}w_{j,c}=1$，并计算

$$
\mathbb E R_P(\widehat h)=\sum_{j,c}w_{j,c}q_j,
\qquad
\mathbb E R_S(\widehat h)=\sum_{j,c}w_{j,c}\frac cm.
$$

二者之差是这个算法/模型下的 expected selection gap。它不是高概率 uniform radius，也不等于 $2\alpha$。

### 6.3 exact common-event probability

脚本还计算

$$
1-\prod_{j=1}^K
\Pr\left(\left|\frac{N_j}m-q_j\right|\le\alpha\right).
$$

乘积仍依赖跨 $j$ loss-coordinate 独立构造。一般 theorem 只声称失败概率至多 $\delta$，不会给此精确值。

### 6.4 盲参干预

- 让前两个 risks 从相差 0.04 缩到 0.01；
- 固定 risk grid，加倍 $m$；
- 在保持最小 risk 不变时增加较差 hypotheses；
- 改变 risk 顺序，检查 lexicographic tie rule 的对象是否改变。

运行前必须预测 expected population、expected train、selection gap、class excess 与 uniform failure 的方向；若方向不确定，明确写“非单调，需由 competing mechanisms 决定”，并说明机制。

## 七、轨道 C：Occam 失败预算与 Le Cam 难分辨性

### 7.1 编码半边

给定正整数 lengths $L_j$，脚本先拒绝 Kraft sum 超过 1 的输入。合法时使用 $\pi_j=2^{-L_j}$，把总失败预算切为 $\delta\pi_j$，得到各自半径。

正确解释是：在预先固定语言中，短 description 占更大的失败预算份额，因而 penalty 小。不能解释为“短模型更接近自然真理”。

### 7.2 下界半边

两世界为

$$
P_-=\operatorname{Bernoulli}(1/2-\gamma),
\qquad
P_+=\operatorname{Bernoulli}(1/2+\gamma).
$$

count 是充分统计量。脚本逐项求 Binomial pmf 的 $L^1$ 距离，得到 exact TV 和

$$
P_e^*=\frac{1-\operatorname{TV}(P_-^m,P_+^m)}2.
$$

同时使用

$$
D_{KL}(P_-\|P_+)=2\gamma\log\frac{1/2+\gamma}{1/2-\gamma}
$$

及 Pinsker 生成一个可能更松的检验错误下界。若 Pinsker lower 变为 0，只说明这个 inequality 在该参数上无信息，不说明真实检验错误为 0。

### 7.3 上界与下界为什么能放同一轨

编码半边问：给定结构后，能否为某个算法构造高概率证书？测试半边问：给定问题族后，是否所有算法都必须承担某种错误？它们方向相反；放在一轨是为了训练“可行证书”和“不可避免代价”同时记账，而不是声称二者已经 rate-matched。

### 7.4 盲参干预

- 保持 Kraft 合法，拉长一个 code 并预测其 radius；
- 增加 occam sample size，预测所有 radii 的 $m^{-1/2}$ 缩放；
- 减半 $\gamma$ 或 testing size，预测 exact testing error；
- 构造 Kraft 违规输入，确认脚本拒绝而不是静默归一化。

## 八、评分者随机指定、跨轨盲参与防挑题协议

主轨必须完成：完整手推、两个数值锚点、两组盲参、SVG 读图和边界说明。跨轨至少完成一组盲参和一个解析锚点。

建议评分 20 分：

| 项目 | 分值 |
|---|---:|
| 主轨对象与独立性合同 | 3 |
| 主轨解析式和手算锚点 | 5 |
| 运行前方向/区间预测 | 3 |
| 跨轨盲参与手算 | 3 |
| stdout/SVG/hash 可复现 | 2 |
| bound 与 exact quantity 分离 | 2 |
| theorem 不覆盖项 | 2 |

14/20 通过；对象合同、解析式、bound/exact 分离任一为 0 则不通过。

## 九、命令行协议

### 9.1 canonical 材料回归

```bash
python3 00-知识库管理/_labs/code/pac_finite_class_cumulative_gate.py
```

canonical 参数：

```text
bad_count=31, bad_risk=0.18, realizable_size=28
risk_grid=0.18,0.22,0.29,0.36, agnostic_size=40
code_lengths=1,2,4,4,5, occam_size=80
testing_size=40, gamma=0.04, delta=0.05
```

canonical SHA-256：

```text
7dda45017be1cf60331afeebc506c727be597c4d40b8ea4bebbcee7d0099ab80
```

### 9.2 非 canonical 盲参

```bash
python3 00-知识库管理/_labs/code/pac_finite_class_cumulative_gate.py \
  --bad-count 17 --bad-risk 0.23 --realizable-size 19 \
  --risk-grid 0.15,0.21,0.28,0.41 --agnostic-size 31 \
  --code-lengths 2,2,3,3 --occam-size 70 \
  --testing-size 33 --gamma 0.055 --delta 0.08 \
  --output /tmp/pac-cum-blind.svg
```

固定审计 fixture 的 SHA-256 为：

```text
f5bdaabff75caafbd2ebfefe3505fc5ec003caa6fd9331236dd9d81c9c0b9536
```

学习者个人证据不得复用这组公开 fixture；评分者必须给新参数。

### 9.3 覆盖保护

只要参数偏离 canonical 且未提供 `--output`，脚本必须失败并报告：

```text
noncanonical parameters require --output; refusing to overwrite canonical SVG
```

即使显式把 `--output` 指向 canonical 总图，非 canonical 参数也会被拒绝。这项合同防止个人实验覆盖教材总图。

## 十、独立审计固定 fixture

[[pac_finite_class_cumulative_contract_audit.py]]独立检查：

1. LT-09—16 的 8/8 node scope 与 MOC mapping；
2. 14/14 题解、100 分与答案隔离；
3. 三轨公式锚点、selection mass 和 Kraft 合法性；
4. canonical 双跑字节一致、stdout markers、SVG XML/viewBox/text density 和固定 hash；
5. 公开 blind fixture 双跑一致和固定 hash；
6. 非 canonical 无 output 时拒绝覆盖；
7. 六处状态面同时写明 `PAC-CUM-01`、`regression-passed`、`not-attempted`、卷级材料 2/10 与个人 0/10。

独立 audit 不 import gate 脚本中的核心函数；关键解析锚点在审计端重新计算，避免同一 bug 自证正确。

## 十一、盲参数干预怎样才算独立

合格盲参同时满足：

- 评分者在预测前不向学习者透露 stdout/hash；
- 参数不是 canonical 或公开 fixture；
- 学习者先冻结预测文本和时间戳；
- 输出写到新路径；
- 至少改变两个机制参数，而非只改文件名；
- 至少跨两轨；
- 记录 prediction error，并解释是算术错、事件错、量词错还是机制直觉错。

若学习者能直接从同一仓库 git history 找到预期输出，该参数不再算盲参。

## 十二、常见失败模式

1. 把 exact independent-coordinate probability 当成 distribution-free theorem；
2. 看到 Union Bound 比 exact 松，就断言 Union Bound “错误”；
3. 把 $\mathbb E[R_P(\widehat h)-R_S(\widehat h)]$ 当作 high-probability radius；
4. 用 $2\alpha$ 解释每次实际 excess 必须恰等于 $2\alpha$；
5. 忘记 lexicographic tie-breaking，导致 selection mass 不为 1；
6. Kraft sum 合法，却漏算 decoder 和 meta-language；
7. 把 Pinsker lower bound 与 exact Bayes testing error 混写；
8. 只展示两个分布接近，未证明最优决策分离；
9. 用 canonical 图替代个人盲参输出；
10. 先看结果再补单调性预测。

## 十三、证据状态机

```text
not-attempted
  -> attempted          口试/闭卷有冻结原稿，但未过全部硬门
  -> passed             口试 + 闭卷 + nonce 主轨 + 跨轨盲参通过
  -> retained           passed + 48 h 换机制 + 14 d 陌生迁移通过
  -> verified-node      retained 后另有逐节点独立证据
```

材料状态独立：

```text
draft material
  -> regression-passed  题卷、详解、脚本、图和独立审计均通过
```

材料 `regression-passed` 不会推动个人状态。个人失败也不会把材料回归状态改坏。

## 十四、48 小时换机制与 14 天迁移

48 小时门从三种机制中随机抽一项：异质 $r_j$、$\rho$-approximate ERM、分层 prefix code 或 Gaussian two-point testing。提交修改后的对象合同、解析式、至少一个反例和新输出。

14 天门必须选择一个陌生 adaptive AI evaluation 问题，提交：

1. target law 与 sampling/feedback 图；
2. fixed vs data-dependent candidate boundary；
3. 一个合法 upper-bound route；
4. 一个 two-world lower-bound construction；
5. theorem 不覆盖的 shift/computation/loss 边界；
6. 可证伪实验和失败判据。

只重复 prompt-selection 题面或替换模型名称，不算迁移。

## 十五、结论边界

本门把 20.2 的三条主线接成同一证据链：

$$
\text{bad-h survival}
\longrightarrow
\text{simultaneous concentration}
\longrightarrow
\text{ERM comparison}
\longrightarrow
\text{weighted complexity}
\longleftrightarrow
\text{indistinguishability lower bound}.
$$

它能证明学习者是否会运行有限类 PAC 的基础论证；不能证明其已掌握下一卷无限类容量、现实深网的泛化机制或分布偏移。下一卷入口是[[VC 维与一致收敛 MOC]]。
