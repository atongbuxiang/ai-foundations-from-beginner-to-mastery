---
type: experiment
status: draft
material_status: regression-passed
learning_status: not-attempted
area: [learning-theory/qualification, learning-theory/deployment, learning-theory/deep-generalization]
assessment_id: LT-QUAL-02
gate_id: LT-QUAL-02-GATE
seed: exact-finite-pipeline
code: "[[00-知识库管理/_labs/code/learning_theory_qualification_02_gate.py]]"
figure: "[[00-知识库管理/_assets/plots/learning-theory/plot-learning-theory-qualification-02-gate-v2.svg]]"
related: ["[[资格考 - 学习理论 II：从模型选择到深度泛化证据（20.6—20.10）]]", "[[资格考解答 - 学习理论 II：从模型选择到深度泛化证据（20.6—20.10）]]", "[[学习理论完整课程地图与掌握标准]]", "[[推导与实验 MOC]]"]
created: 2026-08-29
updated: 2026-08-29
---

# 实验 - 学习理论资格考 II 跨卷累计复现门

> [!abstract] 这道实验门检查什么
> 同一个二分类 AI 服务依次经历 source 选模、target shift、在线路由、partial-feedback 评价和深网机制解释。本实验不比较“哪个数字最小”，而检查每个箭头是否保留 predictor、sample、feedback 与 statement type。A/B/C 三轨都小到可独立手算，没有 Monte Carlo 或第三方依赖。

先看图，不读后文数值，回答：为什么 source winner 会在 target 上翻转，为什么 Hedge regret 与 target-policy risk 不能比较，为什么同一训练 fit、同一函数和 residual 收敛仍不能单独解释 population generalization？

![[00-知识库管理/_assets/plots/learning-theory/plot-learning-theory-qualification-02-gate-v2.svg|920]]

> [!figure] 实验图｜从离线选模到交互部署，再到深网机制审计
> A 轨把 source/target Brier、density ratio、ESS 与 representation effective rank 放在同一选择账本；B 轨把 full-information Hedge 与 context-action joint-ratio OPE 分开；C 轨把 min-norm/null-space、ReLU rescaling、固定核模态和有限粒子 drift 排成证据阶梯。生成脚本：[[learning_theory_qualification_02_gate.py]]；仅用 Python 标准库确定性生成。

**怎样读图。** 先从 A 的 source/target 成对柱确认 selection target 改变；再读 B 的 sequence comparator 与 off-policy target；最后读 C 的四张机制卡，并逐项问该量是否对 function 不变、是否处于现实 training regime、是否已经连接到 population sample。

**图没有证明什么。** 它没有证明 importance weighting 在零 overlap 下可用、在线 no-regret 自动降低 target population risk、effective rank 单调决定 transfer，也没有把插值、flatness、NTK 或 feature drift 中任何一项升级为统一深度泛化定律。

## 零、执行协议：对象预测先于 stdout

```mermaid
flowchart LR
    P[核验资格考 I 与五卷 retained] --> C[手写十三层合同]
    C --> H[三轨公式与方向预测]
    H --> F[冻结 attempt_id / hash]
    F --> N[评分者公布 scorer nonce]
    N --> B[跨至少两轨 blind 参数]
    B --> X[生成新 stdout / SVG]
    X --> I[注入非法合同]
    I --> S[才可查看 canonical / 详解]
    S --> R[48 h 换 pipeline]
    R --> T[14 d 陌生 claim card]
```

### 0.1 运行前冻结清单

1. 三个模型的 source/target Brier 排名与是否翻转；
2. density ratios、最大 ratio 和 ESS 方向；
3. representation effective rank 与 transfer 不能推出；
4. Hedge 的 best fixed model、regret 符号和最终权重方向；
5. observed IPS 是否高于或低于 true target-policy risk；
6. min-norm/null shift 的 fit、norm 和 test-gap 方向；
7. reciprocal rescaling 对 sharpness/path 的不同影响；
8. kernel slow mode、feature/NTK drift 与 regime 标签；
9. 至少十条跨卷“不能推出”；
10. `attempt_id`、题卷 commit、开始时间与 prediction-sheet SHA-256。

### 0.2 Scorer Nonce

- nonce 首字节模 3 指定 A/B/C 主轨；
- 第二字节指定另外两轨各一个干预，保证 blind 至少跨两卷；
- 第三字节指定一个非法合同：support、probability row、context/action、rank、rescaling、kernel 或 canonical overwrite；
- 参数公布后不得因 winner 不翻转、IPS 不好看或 regime 标签不合预期而重抽；
- 本页 fixed blind 只做材料回归，不得当作个人 blind evidence。

## 一、共同服务与十三层最小合同

四个 context $x\in\{0,1,2,3\}$ 有 deterministic binary label。三个 encoder-classifier 输出 probability score $s_j(x)$。离线 source law 为 $q$，计划部署 target law 为 $p$；上线后 router 选择一个模型 action，只观察 chosen model 对应的 outcome/loss。

| 接口 | predictor/sample | 主要输出 | 禁止偷换 |
|---|---|---|---|
| A source selection | 三个 deterministic scores，$X\sim q$ | source Brier winner | target winner |
| A shift | 同三个 scores，$X\sim p$ | target Brier / weighted identity | source accuracy |
| A representation | encoder covariance spectrum | effective-rank proxy | target task risk |
| B online | Hedge mixture，给定 context sequence/full loss | external regret | iid population risk |
| B OPE | stochastic target router $\pi$，logs 来自 $q,\mu$ | expected target policy risk | realized IPS/safety |
| C selection | 欠定线性 predictor | min-norm/null-space | unique test behavior |
| C invariance | 同一 ReLU function 的多个坐标 | sharpness/path stress | function ordering |
| C regime | fixed kernel 与 finite particles | residual/drift diagnostic | population theorem |

## 二、A 轨：Model、Representation 与 Shift

### 2.1 Source/Target Brier

程序从共同 label、source/target probability vector 和 model-score matrix 直接计算

$$
R_q(j)=\sum_xq_x(s_j(x)-y_x)^2,
\qquad
R_p(j)=\sum_xp_x(s_j(x)-y_x)^2.
$$

它同时输出两个 winner；不预设必须翻转。若 blind 参数令 winner 相同，这也是合法结果，不能为制造故事而换 seed。

### 2.2 Density Ratio 与 ESS

在所有 source mass 为正时，输出 $w_x=p_x/q_x$ 与

$$
\operatorname{ESS}_{\rm fraction}
=\frac{(\mathbb E_q[w])^2}{\mathbb E_q[w^2]}
=\frac1{\sum_xp_x^2/q_x}.
$$

这是 population second-moment diagnostic，不是某个 finite sample 的置信半径。程序要求 source probability 严格正，避免把不可识别 support 缺口藏成除零。

### 2.3 Calibration 与 Representation Proxy

在每个 context 对应独立 score bin 的 fixture 中，报告

$$
\sum_xp_x|s_j(x)-y_x|.
$$

它是特定分箱合同下的 calibration gap，不是任意 ECE 实现。Representation spectrum 使用 $\operatorname{tr}\Sigma/\lambda_{\max}$；正 eigenvalue guard 让 near-collapse 仍可量化，但该 proxy 不承担 transfer theorem。

## 三、B 轨：Online Routing 与 Off-Policy Evaluation

### 3.1 Hedge 使用全信息

给定 context sequence 后，三模型 Brier loss vector 全部可见。程序以

$$
p_{t,j}\propto e^{-\eta L_{t-1,j}}
$$

逐轮重算 mixture loss、best fixed loss、regret 与 final probabilities。它不模拟只观察 chosen action 的 bandit update；full-information 标签是合同的一部分。

### 3.2 Context 与 Action 的联合换测度

Logs 假定

$$
X\sim q,\qquad A|X\sim\mu(\cdot|X).
$$

目标是

$$
V_p(\pi)=\sum_{x,a}p_x\pi(a|x)\ell_a(x).
$$

单条记录 estimator 为

$$
\widehat V
=\frac{p_X\pi(A|X)}{q_X\mu(A|X)}\ell_A(X).
$$

程序输出 true risk、给定日志的 observed mean、全 context-action support 上最大 ratio，以及 realized weights 的 Kish ESS。Observed mean 不是 oracle truth；canonical 中它明显低于 true risk，正用于反驳“无偏意味着单次准确”。

## 四、C 轨：Deep Mechanism Evidence Ladder

### 4.1 同 Fit 多解

程序对 $2\times3$ 满行秩 design 独立计算 $X^\top(XX^\top)^{-1}y$，用 row cross product 得 null direction，再比较 min-norm 与平移解的训练残差、参数 norm 和 null test gap。

### 4.2 同 Function 多坐标

在 $L(a,b)=\frac12(ab-1)^2$ 上比较 $(1,1)$ 与 $(c,c^{-1})$。Function product/path quantity 固定为 1，raw Hessian sharpness 变为 $c^2+c^{-2}$。

### 4.3 Fixed Kernel 与 Moving Particles

固定核

$$
K=\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}
$$

通过 eigenmodes 精确计算 $e^{-Kt}r_0$。有限粒子则对 $f=m^{-1}\sum_ja_jw_j$ 做一步 Euler gradient flow，输出 feature second moment 与 empirical tangent scalar 的相对 drift。`feature-moving` 只是在本 fixture 中最大 drift 达到 0.1，不是理论 phase transition。

## 五、Canonical 复现

```bash
python3 00-知识库管理/_labs/code/learning_theory_qualification_02_gate.py
```

```text
TRACK A source_brier=0.069250,0.091250,0.141250 target_brier=0.127000,0.057500,0.121250 target_cal_gap=0.340000,0.200000,0.265000 weights=0.250000,0.666667,1.500000,4.000000 ess_fraction=0.452830 source_winner=0 target_winner=1 effective_rank=1.275000,1.750000,1.020000
TRACK B T=8 hedge_loss=0.857972 best=0.542500 regret=0.315472 final_probs=0.297629,0.421512,0.280858 target_policy_risk=0.073375 observed_ips=0.033313 max_joint_ratio=6.400000 observed_ess=2.631218 observed_ratios=0.035714,6.400000,0.111111,3.000000,1.333333,0.875000
TRACK C min_norm=0.333333,0.333333,0.666667 min_length=0.816497 shifted_length=2.160247 train_residual=0.000000 null_test_gap=2.000000 sharpness=2.000000->16.062500 path=1.000000 kernel_eigenvalues=1.600000,0.400000 residual_final_norm=0.213056 feature_drift=0.325000 ntk_drift=0.084987 regime=feature-moving
```

Canonical SVG SHA-256：

```text
7bfd9f947a3416dd9fbf7fb889d525128723e5702fcba343e65beba258d71563
```

## 六、固定跨卷 Blind

运行前先预测：target 更集中于 context 3 后 winner、最大 density ratio 与 ESS 怎样变；$\eta$ 下降后 Hedge mixture 怎样变；target routing 更集中到 $M_1$ 后 true risk 怎样变；null shift 减小而 $c$ 增大时哪些量同向、哪些反向；pure slow kernel mode 与更小 particle step 怎样影响 residual/drift。

```bash
python3 00-知识库管理/_labs/code/learning_theory_qualification_02_gate.py \
  --source-probabilities '0.5,0.2,0.2,0.1' \
  --target-probabilities '0.1,0.1,0.3,0.5' --labels '0,0,1,1' \
  --model-probabilities '0.05,0.25,0.75,0.5;0.3,0.4,0.9,0.95;0.1,0.55,0.65,0.9' \
  --representation-spectra '5,1,0.2;2,1,0.25;3,0.1,0.02' \
  --online-contexts '0,1,3,3,2,1,3,0,2' --hedge-eta 0.6 \
  --logging-policy '0.75,0.15,0.1;0.55,0.3,0.15;0.35,0.45,0.2;0.15,0.55,0.3' \
  --target-policy '0.1,0.75,0.15;0.1,0.75,0.15;0.1,0.8,0.1;0.05,0.85,0.1' \
  --logged-contexts '0,3,1,2,3,0,2' --logged-actions '0,1,2,1,2,1,0' \
  --design '2,0,1;0,1,1' --responses '1,2' --null-shift 1.5 --rescale 8 \
  --kernel-rho 0.3 --kernel-time 2 --initial-residual '1,-1' \
  --particle-a '0.8,-1.2' --particle-w '0.4,-0.3' \
  --particle-step 0.1 --particle-target 0.8 \
  --output /tmp/lt-qual-02-blind.svg
```

```text
TRACK A source_brier=0.051250,0.079250,0.091000 target_brier=0.150250,0.029250,0.073000 target_cal_gap=0.355000,0.125000,0.220000 weights=0.200000,0.500000,1.500000,5.000000 ess_fraction=0.331126 source_winner=0 target_winner=1 effective_rank=1.240000,1.625000,1.040000
TRACK B T=9 hedge_loss=0.817734 best=0.527500 regret=0.290234 final_probs=0.294396,0.392064,0.313540 target_policy_risk=0.039850 observed_ips=0.047251 max_joint_ratio=7.727273 observed_ess=2.765490 observed_ratios=0.026667,7.727273,0.500000,2.666667,1.666667,1.000000,0.428571
TRACK C min_norm=0.000000,1.000000,1.000000 min_length=1.414214 shifted_length=2.061553 train_residual=0.000000 null_test_gap=1.500000 sharpness=2.000000->64.015625 path=1.000000 kernel_eigenvalues=1.300000,0.700000 residual_final_norm=0.348741 feature_drift=0.129521 ntk_drift=0.027379 regime=feature-moving
```

Blind SVG SHA-256：

```text
1df68fb356beefc67fbd9bf54dbb50e77160ddbd080e8acf7c9b424e1e77d876
```

## 七、输入与覆盖保护

以下合同必须非零退出：

1. source/target 非概率向量、长度不等或 source 含零；
2. labels 非 binary，model score 超出 $[0,1]$；
3. model/context 形状不一致，少于两个模型；
4. spectrum 行数不匹配、少于两个 eigenvalues 或非正；
5. online/logged context 或 action 越界，日志长度不等；
6. Hedge learning rate 非正；
7. logging/target policy 形状错误、行不归一或 logging 含零；
8. design 不是 $2\times3$、responses 非二向量或 design 不满行秩；
9. rescale 非正、kernel $\rho\notin(-1,1)$、time 为负或 residual 为零；
10. particle 列表不等长/少于两个或 step 非正；
11. 非 canonical 参数不提供 `--output`；
12. 非 canonical 运行覆盖 canonical SVG。

这些 guards 保护的是 identification、support、geometry 与 evidence isolation。

## 八、学习证据状态机

```text
not-attempted
  -> prerequisites-retained
  -> oral-completed
  -> session-I-sealed
  -> session-II-sealed
  -> prediction-sheet-sealed
  -> nonce-revealed
  -> blind-compute-passed
  -> corrected
  -> 48h-retest-passed
  -> 14d-transfer-passed
  -> retained
```

材料状态为 `regression-passed`，个人仍为 `not-attempted`。没有 `LT-QUAL-01 + 五卷 retained` 时，连 `prerequisites-retained` 都不能记录。

## 九、48 小时与 14 天迁移

48 小时后必须更换至少两个接口：

- source/target 改成 conditional shift 或 support gap；
- Brier 改成 log loss/成本敏感 decision；
- fixed representations 改成 same-data learned representation selection；
- full information 改成 bandit/delayed feedback；
- static target policy 改成 action-induced state dynamics；
- min-norm 改成 preconditioned geometry；
- fixed NTK 改成多步 finite-particle drift。

14 天后对一篇陌生论文、博客或真实系统报告写完整 claim card：原始命题、十三层合同、证明覆盖、实验 intervention、invariance/regime、反事实 target、最小反例、部署门与三条不能推出。
