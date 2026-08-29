---
type: experiment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/online-learning, learning-theory/boosting, learning-theory/bandits]
assessment_id: ONLINE-CUM-01
gate_id: ONLINE-CUM-01-GATE
seed: exact-enumeration
code: "[[00-知识库管理/_labs/code/online_boosting_cumulative_gate.py]]"
figure: "[[00-知识库管理/_assets/plots/learning-theory/plot-online-boosting-cumulative-gate-v2.svg]]"
related: ["[[阶段测验 - 在线学习、Boosting 与序列预测（20.9）]]", "[[阶段测验解答 - 在线学习、Boosting 与序列预测（20.9）]]", "[[在线学习、Boosting 与序列预测 MOC]]", "[[推导与实验 MOC]]"]
created: 2026-08-29
updated: 2026-08-29
---

# 实验 - 在线学习、Boosting 与序列预测累计复现门

> [!abstract] 实验目的
> 用三个完全有限、无随机依赖的系统检查“在线学得好”到底指什么。A 轨分开 full-information regret、OCO geometry 与 adversary visibility；B 轨分开 sequence mistake certificate 与 empirical boosting potential；C 轨分开 iid risk conversion、stochastic exploration 与 bandit counterfactual estimation。

先看图回答：

1. 为什么 Hedge regret $0.567$ 不是 population excess risk，OGD regret $3.5$ 也不是优化终点证书？
2. 为什么 Perceptron 的 $M\le4$ 和 AdaBoost 的 $\widehat R_{0/1}\le0.8165$ 不能互相替代？
3. 为什么 IPS 无偏估计可以在单次观测上等于 $2.7$，这不表示 loss 超出 $[0,1]$？

![[00-知识库管理/_assets/plots/learning-theory/plot-online-boosting-cumulative-gate-v2.svg|920]]

> [!figure] 实验图｜协议、势能、风险转换与部分反馈分账
> A 轨精确枚举 Hedge 分布、projected OGD 路径和 current-action-aware 线性反例；B 轨同时核对 Perceptron progress/norm 与 AdaBoost $\alpha_t,Z_t,\prod_tZ_t$；C 轨将 random-iterate risk、UCB index、IPS sample/expectation/variance 与 RL 边界排在同一页但不混为一个指标。生成脚本：[[online_boosting_cumulative_gate.py]]；仅用 Python 标准库确定性生成。

**怎样读图。** 每栏先读上方的 target/protocol，再读数值。A 的 regret 与 bound 依赖 full loss vector 和当轮 fresh coin 不可见；B 的两个 certificate 都只针对已给序列/训练集；C 的 risk bridge 需 iid，IPS 需 overlap，UCB 还有自己的 stochastic reward 假设。

**图没有证明什么。** 它没有证明当前 action 可见时仍 no-regret，没有证明 boosting training error 是 test error，没有证明 last iterate 必然继承 average risk，也没有把单步 bandit 无偏性扩张为 RL 长程 safety/value 保证。

## 一、八层可靠复现账本

| 层 | 本实验固定内容 | 失败时不得声称 |
|---|---|---|
| 1 protocol | 轮前决策、轮后 loss/feedback | “这是在线学习保证” |
| 2 filtration | loss 可见过去，不可见当轮 realized action | “对任意 adaptive 环境成立” |
| 3 feedback | A/B 主轨有 full information，C 的 bandit 只观测所选 action | “未选 action loss 已被观测” |
| 4 comparator | A 是 best fixed expert/action；B 是 normalized separator/当轮 weak rule；C 是 fixed risk comparator/target policy | “比每轮 oracle 更好” |
| 5 potential | log-total-weight、Euclidean distance、Perceptron double ledger、boosting product | “更新式本身就是证明” |
| 6 probability | finite pathwise calculation；C 的 risk/IPS 额外声明概率对象 | “一个 sample 等于期望” |
| 7 conversion | iid past-measurability + random iterate/Jensen | “任意 sequence regret 自动是 risk” |
| 8 boundary | overlap、drift、delay、current-action response、state dynamics | “离线/长程部署已安全” |

## 二、A 轨：Full-Information Regret、OCO 与 Filtration

### 2.1 Hedge 精确账本

固定 $\eta=\log2$与 loss matrix

$$
\ell_{1:4}=
\begin{pmatrix}
0&1&1\\
1&0&1\\
0&1&0\\
1&1&0
\end{pmatrix}.
$$

脚本不用界去代替 actual mixture loss，而是逐轮精确计算

$$
p_{t,i}=\frac{e^{-\eta L_{t-1,i}}}{\sum_je^{-\eta L_{t-1,j}}},
\qquad
\widehat\ell_t=\langle p_t,\ell_t\rangle.
$$

需同时对上：

- mixture cumulative loss $77/30$；
- best fixed expert loss $2$；
- regret $17/30$；
- final probabilities $(0.4,0.2,0.4)$；
- Hoeffding-potential bound $1.931536$。

### 2.2 Projected OGD 不是同一势能

在 $[-1,1]$ 上用 $x_1=0,\eta=1/2$，梯度 $(1,-2,1,2,-1)$。脚本精确实现

$$
x_{t+1}=\Pi_{[-1,1]}(x_t-\eta g_t),
$$

并分别输出 realized linear loss、best fixed comparator loss、regret 与

$$
\frac{\|x_1-u\|^2}{2\eta}+\frac\eta2\sum_tg_t^2.
$$

这个 bound 来自距离望远镜，不是 Hedge 的 log-partition proof。

### 2.3 Current-Action-Aware 破坏点

对 action 序列 $(1,2,1,2,2,1)$，环境在看到当轮 action 后使它 loss 为 1，另一 action loss 为 0。学习者 loss $6$，best fixed loss $3$，regret $3$。这一轨不是新算法，而是对定理信息边界的反例。

## 三、B 轨：Perceptron 与 AdaBoost

### 3.1 Perceptron 的两条账

数据为

$$
((1,0),+1),\ ((0,1),+1),\ ((-1,-1),-1),
$$

并用 $u=(1,1)/\sqrt2$。脚本必须独立算：

- actual mistakes $M=2$与 final $w=(1,1)$；
- $R=\sqrt2$、$\gamma=1/\sqrt2$；
- progress $\langle w,u\rangle=\sqrt2$；
- norm $\|w\|=\sqrt2$；
- worst-case certificate $(R/\gamma)^2=4$。

证书与 actual mistakes 必须并列；不得把上界 4 谎报成实际错误 4。

### 3.2 AdaBoost 的恒等式与上界

两轮 signed-margin rows 为

$$
s_1=(1,1,1,-1),\qquad s_2=(-1,-1,1,1).
$$

程序逐轮从当前 $D_t$ 重算 $\varepsilon_t$，再算

$$
\alpha_t=\frac12\log\frac{1-\varepsilon_t}{\varepsilon_t},
\qquad
Z_t=2\sqrt{\varepsilon_t(1-\varepsilon_t)}.
$$

要求同时成立：

$$
\frac14\sum_i e^{-\sum_t\alpha_ts_{t,i}}
=\prod_tZ_t=0.8164965809,
$$

以及 training error $0.25\le0.8164965809$。第四个样本最终 margin 仍为负，这正好说明 product bound 可很松。

## 四、C 轨：Risk Bridge、UCB 与 IPS

### 4.1 Random Iterate Risk

设四个 past-measurable predictor 的 population risks 为 $(0.2,0.4,0.1,0.3)$，comparator risk $0.1$。在 iid next-example 条件下，random-iterate risk 为 $0.25$，online regret $0.6$，两者的桥是

$$
0.25-0.1=0.15=0.6/4.
$$

图中另显示 $\sqrt{\log(1/\delta)/(2T)}$的示意半径，它只是受控差值的浓缩尺度，不代替完整 high-probability online-to-batch theorem 中对 comparator 和 martingale 的分账。

### 4.2 UCB 与 IPS 不是同一模型

UCB 使用 stochastic reward means/counts，两个 index 为 $(1.183198,1.324766)$，选第 2 臂。IPS 另用三臂 loss fixture：

$$
p=(0.5,0.3,0.2),\quad
\pi=(0.2,0.2,0.6),\quad
\ell=(0.2,0.6,0.9).
$$

当 $A=3$ 时，vector IPS 为 $(0,0,4.5)$，target-policy sample 为 $2.7$，但其 expectation 为 true target risk $0.7$。脚本还直接计算

$$
\sum_i\frac{\pi_i^2\ell_i^2}{p_i}-R_\pi^2=1.0192
$$

与 maximum ratio $3$，使“无偏但高方差”成为数字事实。

## 五、Canonical 复现

```bash
python3 00-知识库管理/_labs/code/online_boosting_cumulative_gate.py
```

标准输出：

```text
TRACK A T=4 eta=0.693147 hedge_loss=2.566667 best=2.000000 regret=0.566667 bound=1.931536 final_probs=0.400000,0.200000,0.400000 ogd_T=5 ogd_eta=0.500000 ogd_loss=2.500000 comparator=-1.000000 ogd_regret=3.500000 ogd_bound=3.750000 adaptive_T=6 adaptive_regret=3.000000
TRACK B mistakes=2 final_w=1.000000,1.000000 R=1.414214 gamma=0.707107 mistake_bound=4.000000 progress=1.414214 norm=1.414214 boost_errors=0.250000,0.333333 alphas=0.549306,0.346574 Z=0.866025,0.942809 product=0.816497 training_error=0.250000 min_margin=-0.202733
TRACK C T=4 random_risk=0.250000 comparator=0.100000 online_regret=0.600000 excess=0.150000 radius=0.611937 ucb=1.183198,1.324766 ucb_choice=2 ips=0.000000,0.000000,4.500000 target_risk=0.700000 observed_estimate=2.700000 ips_variance=1.019200 max_ratio=3.000000
```

Canonical SVG SHA-256：

```text
2c61d35ce6dc1acedec1e6e62dea4ca62797ece325edc4787ca06eb055c45181
```

## 六、固定跨轨 Blind 干预

在运行前先封存以下方向判断：

- Hedge 的最终权重是否集中到累计 loss 最低专家，actual regret 与 bound 各如何变；
- 放大 Perceptron input radius 但保持最小 margin 后，certificate 怎样变；
- weak edge 变小时 $Z_t$ 是远离还是接近 1；
- logging/target 仍有 overlap 但 target 更集中于稀少 action 时，IPS variance 怎样变。

```bash
python3 00-知识库管理/_labs/code/online_boosting_cumulative_gate.py \
  --hedge-losses '0,1,0;1,0,1;1,1,0;0,0,1;1,0,0' \
  --hedge-eta 1.0986122886681098 \
  --ogd-gradients '2,-1,-1,2,-2,1' --ogd-eta 0.25 \
  --adaptive-actions '1,1,2,2,1' \
  --perceptron-examples '2,0,1;0,1,1;-1,-2,-1' --separator '1,1' \
  --boost-margins '1,1,1,-1,-1;-1,-1,1,1,1' \
  --online-risks '0.15,0.35,0.25,0.05,0.2' --comparator-risk 0.05 --delta 0.1 \
  --ucb-counts '12,18' --ucb-means '0.55,0.48' \
  --logging-probabilities '0.4,0.4,0.2' \
  --target-probabilities '0.1,0.3,0.6' \
  --bandit-losses '0.3,0.5,0.8' --chosen-action 2 \
  --output /tmp/online-cum-blind.svg
```

固定 blind stdout：

```text
TRACK A T=5 eta=1.098612 hedge_loss=2.790476 best=2.000000 regret=0.790476 bound=1.686633 final_probs=0.142857,0.428571,0.428571 ogd_T=6 ogd_eta=0.250000 ogd_loss=1.750000 comparator=-1.000000 ogd_regret=2.750000 ogd_bound=3.875000 adaptive_T=5 adaptive_regret=3.000000
TRACK B mistakes=2 final_w=2.000000,1.000000 R=2.236068 gamma=0.707107 mistake_bound=10.000000 progress=2.121320 norm=2.236068 boost_errors=0.400000,0.333333 alphas=0.202733,0.346574 Z=0.979796,0.942809 product=0.923760 training_error=0.400000 min_margin=-0.143841
TRACK C T=5 random_risk=0.200000 comparator=0.050000 online_regret=0.750000 excess=0.150000 radius=0.479853 ucb=1.302905,1.094745 ucb_choice=1 ips=0.000000,1.250000,0.000000 target_risk=0.660000 observed_estimate=0.375000 ips_variance=0.774900 max_ratio=3.000000
```

Blind SVG SHA-256：

```text
2f54d14536bf71f86c76a57011d33456c91173d5d808b6f97b8eb3d92ff24960
```

## 七、输入与覆盖保护

下列情况必须非零退出：

1. Hedge matrix 不是矩形、专家数小于 2 或 loss 超出 $[0,1]$；
2. Hedge/OGD learning rate 非正或 OGD radius 非正；
3. adaptive action 不在 $\{1,2\}$；
4. Perceptron row 不是 $(x_1,x_2,y)$、$y\notin\{-1,1\}$ 或 separator 为零；
5. separator 不能对所有样本给正 margin；
6. Boosting signed margin 不在 $\{-1,1\}$，或某轮 $\varepsilon_t\notin(0,1/2)$；
7. online risks/comparator/means/losses 超出 $[0,1]$，或 $\delta\notin(0,1)$；
8. UCB counts 非正或与 means 长度不等；
9. logging/target 非概率向量，logging 包含零，或三个 bandit vector 长度不等；
10. chosen action 超出 action set；
11. 任一非 canonical 参数未指定 `--output`；
12. 非 canonical 运行试图覆盖 canonical SVG。

这些 guard 是证据合同的一部分，不是“为了让脚本不报错”的工程附件。

## 八、学习证据状态机

```text
not-attempted
  -> oral-completed
  -> closed-book-sealed
  -> prediction-sheet-sealed
  -> nonce-revealed
  -> blind-compute-passed
  -> corrected
  -> 48h-retest-passed
  -> 14d-transfer-passed
  -> retained
```

任一状态都必须有 `attempt_id`、时间戳、原稿 hash、题卷 commit 和评分记录。材料当前为 `regression-passed`，学习者仍为 `not-attempted`；并且 `REL-CUM-01 retained` 个人前置尚未满足。

## 九、48 小时与 14 天迁移

48 小时后不重放同一组数，而从下列机制换一个：

- Hedge 换 prior/range 或 unknown horizon；
- OGD 换 simplex/entropy mirror geometry；
- Perceptron 换 kernel 或 nonseparable hinge-loss bound；
- AdaBoost 换 weak edge/noise 并必须重新判定证书范围；
- online-to-batch 换 dependence/drift 以识别哪一步失效；
- bandit 换 delayed/censored feedback 或 policy overlap。

14 天后必须对陌生 AI 交互系统交付 protocol diagram、comparator ledger、feedback/filtration 定位、主副指标、失效检查与上线/回滚规则。

> [!important] 证据边界
> canonical 数字、图、脚本双跑和独立审计只能证明这套教学材料可复现。它们不能把学习者状态从 `not-attempted` 提升为 `passed`，也不能把 finite fixture 当成现实部署的通用 safety 证明。
