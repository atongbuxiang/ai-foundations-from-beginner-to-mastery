---
type: concept
status: verified
area: [training, model-selection, benchmarking, compute-budget]
course_id: TRN-71
prerequisites: ["[[正则化、交叉验证与模型选择]]", "[[随机种子、配对比较、置信区间与序贯决策]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
related: ["[[训练实验协议、事故记录与因果证据地图]]", "[[训练与优化完整课程地图与掌握标准]]"]
sources: ["[[S-2010-Arlot-Celisse-Cross-Validation]]", "[[S-2019-Dodge-Show-Your-Work]]", "[[S-2020-Dodge-Finetuning-Variance]]", "[[S-2021-Bouthillier-Benchmark-Variance]]", "[[S-2020-MLPerf-Training-Benchmark]]", "[[S-2026-MLCommons-Training-Rules]]", "[[S-2021-Pineau-ML-Reproducibility]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Checkpoint 选择、验证泄漏与 Compute-matched 比较

> [!abstract] 本节目标
> 理解“最佳 checkpoint”是一次统计选择而不是免费读数；能隔离训练、调参与最终评估数据，分别匹配 token/FLOPs、tuning budget、wall-clock 和 time-to-quality，并把失败与未达标运行纳入公平比较。

## 一、一个 run 会产生很多候选模型

训练 trajectory 产生 checkpoints

$$
\theta_{t_1},\theta_{t_2},\dots,\theta_{t_K}.
$$

若用 validation 选择

$$
\hat k=\arg\min_{1\le k\le K}\widehat R_{val}(\theta_{t_k}),
\tag{1}
$$

真正被评估的对象不是某个固定 checkpoint，而是完整 procedure：训练轨迹 + evaluation cadence + selection rule。改变 $K$、评估频率、smoothing、patience 或 tie-break 都改变算法。

## 二、为什么 best validation score 会乐观

写成

$$
\widehat R_k=R_k+\varepsilon_k,
\tag{2}
$$

即观测 validation risk 是真实风险加噪声。即便所有 $R_k=R$，选择最小者也有

$$
\mathbb E\left[\min_k\widehat R_k\right]
=R+\mathbb E[\min_k\varepsilon_k]<R
\tag{3}
$$

（非退化对称噪声时）。检查越多 checkpoints/configs，越可能挑到一次幸运低估。checkpoint 高度相关会减小但不会消除 selection optimism。

所以必须区分：

- `best validation`：用于选择，天然偏乐观；
- `test at selected checkpoint`：在 test 未参与选择时评估完整 procedure；
- `oracle best test`：事后用 test 选 checkpoint，只能作诊断上界，不能作泛化结果。

## 三、Early stopping 是算法，不是纯省算力技巧

典型规则：每隔 $e$ steps 评估，若连续 $p$ 次未改善超过 $\epsilon$ 则停止，并恢复 best checkpoint。完整合同为

$$
\mathcal S=(e,p,\epsilon,\text{smoothing},\text{metric},
\text{direction},\text{warmup},\text{max horizon},\text{restore rule}).
\tag{4}
$$

[[S-2020-Dodge-Finetuning-Variance]] 显示 initialization/data order 与 early stopping 共同影响 fine-tuning 结果。不同方法若用不同 evaluation cadence 或 patience，既改变 compute，也改变 selection pressure。

## 四、四种验证泄漏

### 4.1 直接 test 泄漏

看 test 分数选 checkpoint、HP、seed、paper figure 或是否继续研究。哪怕不反向传播，信息已反馈进 procedure。

### 4.2 Validation 自适应复用

研究者经过数百次配置比较反复查看同一 validation，逐步对其过拟合。最终模型对“开发过程”而言并非独立。

### 4.3 Preprocessing/normalization 泄漏

用全数据拟合 tokenizer、normalizer、feature selector、dedup threshold 或 imputation，再切 split；信息在训练前已进入 pipeline。

### 4.4 时间/组结构泄漏

相同用户、文档近重复、未来时间或同一来源跨 split，使 validation 不再模拟目标泛化。随机行切分可能形式独立、语义不独立。

解决方案是把 split 作为 pipeline 的第一等合同：group/time/dedup policy、fit scope、hash 与访问日志全部记录。

## 五、嵌套选择：开发与最终评估分开

推荐三层：

1. **train**：拟合参数和 optimizer state；
2. **development/validation**：选择 HP、checkpoint、recipe；
3. **locked test**：procedure 冻结后一次或受控次数评估。

数据小需 cross-validation 时，outer folds 估计 selection procedure，inner folds 选择 HP。[[S-2010-Arlot-Celisse-Cross-Validation]] 强调 CV 用于 risk estimation 与 model selection 是不同目标；training fraction 也会改变被估计 procedure。

若大量人类研究迭代已使用 test，诚实做法是承认其已变成 development set，并引入新 locked evaluation，而不是继续称其“测试集”。

## 六、公平比较至少有四本预算账

### 6.1 数据与更新预算

- unique/raw/effective tokens；
- optimizer steps、global batch、sequence length/padding；
- epochs/repetition、augmentation/curriculum；
- checkpoint/evaluation 频率。

### 6.2 算术与系统预算

- model/executed FLOPs、precision、recompute；
- hardware count/type/topology；
- wall-clock、energy、memory 与失败重试；
- throughput 与 utilization。

### 6.3 调参与开发预算

- number of trials、search space/algorithm；
- early terminated/failed runs；
- researcher/manual interventions；
- reused prior knowledge 与 transfer cost。

[[S-2019-Dodge-Show-Your-Work]] 的核心提醒是：最终一个 score 无法显示获得它所花的随机搜索和 compute。

### 6.4 推理/部署预算

- latency、memory、tokens/s、energy；
- context/output length、batch/concurrency；
- target quality 与 serving distribution。

训练更贵但推理更省，或反之，都需按研究目标定义总成本。

## 七、“Compute-matched”有多种含义

| 匹配方式 | 固定什么 | 回答的问题 |
|---|---|---|
| token-matched | 有效训练 token | 相同数据曝光下谁更好？ |
| step-matched | optimizer updates | 相同更新次数下谁更好？ |
| FLOP-matched | 估算/执行 FLOPs | 相同算术预算下谁更好？ |
| hardware-time matched | 设备×时间 | 当前平台预算下谁更好？ |
| dollar/energy matched | 成本/能耗 | 资源约束下谁更值？ |
| target-quality | 达到固定质量 | 谁更快达到有用结果？ |
| total-R&D matched | training+tuning+failures | 完整 procedure 谁更高效？ |

这些口径不会自动给出同一排名。论文应声明 primary budget，并给其他关键账作为敏感性分析。

## 八、Time-to-quality 比 throughput 更接近端到端结果

定义目标质量 $q^*$，evaluation times 为 $\tau_j$：

$$
T_{q^*}=\inf\{\tau_j:Q(\theta_{\tau_j})\ge q^*\}.
\tag{5}
$$

[[S-2020-MLPerf-Training-Benchmark]] 与当前 [[S-2026-MLCommons-Training-Rules]] 采用固定目标质量与多次运行的思想，因为更高 throughput 可能伴随更差 convergence。协议还需定义：

- 计时起点和数据触达边界；
- evaluation cadence 与插值是否允许；
- target 的统计波动/持续性；
- 未达到 target 的 run 如何处理；
- 多次 run 的 aggregation。

本库可借鉴这一结构，但未按官方规则执行的实验不能称 MLPerf 合规。

## 九、失败、删失与 survivor bias

若 A 10 次运行有 4 次失败，剩余 6 次平均质量高于 B 的 10 次成功，不能只比较成功均值。至少联合报告：

$$
\hat p_{fail}=\frac{\#\text{failed}}{\#\text{launched}},
\tag{6}
$$

以及 intention-to-run outcome。Time-to-quality 中未达标是右删失；可用成功率随预算、survival curve 或 restricted mean time。把失败 run 删除会条件化一个 treatment 与 run difficulty 共同影响的 collider。

## 十、一个公平比较例子

方法 A：吞吐 120k tok/s，30B token 达到 loss 2.50；方法 B：100k tok/s，20B token 达到同阈值。忽略评估成本：

$$
T_A=30\text{B}/120\text{k}=250{,}000\text{s},
$$

$$
T_B=20\text{B}/100\text{k}=200{,}000\text{s}.
\tag{7}
$$

A throughput 高 20%，却晚 25% 到达目标。若 A 调了 40 trials、B 调 10 trials，总研发成本差距更大；若 B 有更高失败率，结论又可能逆转。公平比较必须把学习动力学和系统速度相乘，而不是只选一边。

## 十一、冻结协议的检查表

在最终比较前锁定：

- claim、primary outcome、quality threshold 与 margin；
- model/data/tokenizer 与 split hash；
- optimizer/schedule/precision/distribution recipe；
- train/tuning/eval/deployment 四本预算；
- checkpoint cadence、selection/early-stop/tie-break；
- seeds、pairing、failure/censoring、stopping；
- test access policy；
- statistical estimator、interval 和 multiplicity family。

只有冻结后产生的 runs 才进入 confirmatory result；之前的探索用于形成假设，不应与确认数据静默合并。

## 十二、图解：选择回路与泄漏防火墙

带着一个问题读图：**为什么“每 100 step 取最优并报告”比固定 checkpoint 多出一层统计选择？**

![[00-知识库管理/_assets/figures/training-optimization/fig-checkpoint-selection-firewall-v1.svg|880]]

> [!figure] 图 TRN-71-01　训练轨迹、validation 选择与 locked test 防火墙
> 来源：自绘机制图；CV 目标边界依据 [[S-2010-Arlot-Celisse-Cross-Validation]]，time-to-quality 协议依据 [[S-2020-MLPerf-Training-Benchmark]]。

**怎样读图**：左侧一条 trajectory 产生多个候选，validation 只输出一个 selected checkpoint；中间冻结完整 procedure，右侧 locked test 评估 procedure，并与 token/FLOP/time/tuning 四本账连接。

**图没有证明什么**：独立 test 只保护当前一次冻结选择；若结果反复反馈到下一轮开发，它也会逐渐成为 validation。

## 十三、核心结论

“最佳 checkpoint”属于 selection procedure，不是无偏观测。公平比较要同时固定选择规则、失败处理和预算口径；token、FLOP、hardware-time、time-to-quality 与 total R&D 各回答不同问题。任何使用 test 或 validation 的信息反馈，都必须计入算法与证据边界。
