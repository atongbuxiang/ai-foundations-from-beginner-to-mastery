---
type: experiment
status: verified
area: [training, scaling-laws, compute-allocation, reproducibility]
experiment_id: EXP-TRN-607-V1
related: ["[[经验 Scaling Law、幂律拟合与不可约项]]", "[[Kaplan 参数数据律、联合拟合与有限区间]]", "[[Chinchilla、Compute-optimal 参数与数据分配]]", "[[IsoFLOP、训练算力口径与系统校正]]", "[[数据质量、重复、混合与有效 Token]]", "[[过训练、推理成本与多目标最优规模]]", "[[Broken Scaling、涌现表象与优化架构数据分解]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
script: "[[experiment_scaling_law_resource_audit_v1.py]]"
results: "[[00-知识库管理/_labs/experiments/trn60.7-scaling-resource-audit-v1/results.json]]"
created: 2026-08-26
updated: 2026-08-26
---

# 实验 - Scaling Law、资源分配与外推证据审计

> [!abstract] 实验结论
> Python 标准库实验用 10 条互相分账的轨道、34 项机器断言，验收 offset 对局部斜率的影响、有限窗口函数族分叉、$N$–$D$ 联合可辨识性、compute-optimal 边际平衡、model/system/energy 账本、重复 token、mixture 目标依赖、推理 break-even、指标诱导的涌现表象，以及 scale-block held-out 证据。34/34 断言通过；从另一空目录复跑时，1 JSON、10 CSV、3 SVG 共 14/14 个文件逐字节一致。实验支持定义、恒等式、审计指标与反例，不构成真实神经网络的 E3/E4 Scaling Law 证据。

## 一、研究问题与预注册门

| ID | 对象 | 可证伪预期 |
|---|---|---|
| H1 | offset 与局部斜率 | $L=1+4x^{-1/2}$ 的 excess slope 恒为 $-1/2$，raw slope 随 floor 占比增大而趋 0 |
| H2 | 有限窗口外推 | 无 offset 模型可穿过两个 calibration 点，却在远 held-out scale 与真实 offset 曲线显著分叉 |
| H3 | joint identifiability | 路径 $D=\sqrt N$ 使两个贡献都按 $N^{-1/4}$ 变化；crossed grid 才能看到瓶颈交换 |
| H4 | compute-optimal allocation | $\kappa ND=C$ 严格成立；解析 $N^*$ 使加权边际相等并最小化每条 IsoFLOP profile |
| H5 | 系统校正 | model FLOPs 相同不推出 wall time、HFU、energy 或 carbon 相同；$HFU=r\,MFU$ |
| H6 | repeated token | seen tokens 线性增长，几何边际模型的 effective tokens 单调但饱和于 $U/(1-q)$ |
| H7 | mixture | 训练权重留在 simplex；增大 A 比重改善 A、伤害 B；部署目标改变观测最优 mixture |
| H8 | lifecycle objective | A/B 在 $Q=500$ 相交；前后最优翻转；方案 C 同时被 B 的成本与延迟支配 |
| H9 | broken/emergence | 平滑 per-step $p$ 经 $p^{10}$ 放大；零成功概率随能力增长下降；局部 loss exponent 平滑从 $-.3$ 到 $-.7$ |
| H10 | held-out evidence | calibration、validation、held-out 按整尺度有序；失败保留在 24 次计划分母；锁定区间覆盖观测 |

## 二、环境、命令与 artifacts

- 脚本：[[experiment_scaling_law_resource_audit_v1.py]]；
- 环境：Python 3.9.6 标准库，无 NumPy、SciPy、Matplotlib 或网络；
- seed：20260826；本版使用解析式与确定性代理，seed 是卷级复现标识；
- 输出目录：`00-知识库管理/_labs/experiments/trn60.7-scaling-resource-audit-v1/`；
- 正式图目录：`00-知识库管理/_assets/plots/training-optimization/`。

运行：

    python3 "00-知识库管理/_labs/code/experiment_scaling_law_resource_audit_v1.py"

脚本只有在 34 项 checks 全为真时返回退出码 0。另用 `--output-dir` 与 `--plot-dir` 指向两个空目录复跑，并逐文件做二进制比较；JSON、10 CSV 与 3 SVG 共 14/14 一致。

## 三、关键数值摘要

| 轨道 | 关键观测 | 证据层级 |
|---|---:|---|
| offset slope | excess slope 恒为 $-.5$；raw magnitude 从 $.4$ 降到约 $.056$ | exact derivative identity |
| finite window | 无 offset 指数仅 $.02787$；在 $x=10^8$ 绝对外推误差 $.25165$ | deterministic counterexample |
| joint design | diagonal 上两项同为 $N^{-.25}$；crossed grid 为 $3\times3=9$ cells | design-rank construction |
| allocation | $N^*\sim C^{.4516}$，$D^*\sim C^{.5484}$；$N=N^*/4$ 的 relative regret $.0955$ | constrained analytic proxy |
| system ledger | 同为 $1.8\times10^{21}$ model FLOPs，wall time 为 $.556/.658/1.667$ h | declared system scenarios |
| repeat value | 10 epochs：seen 1000B，effective 248.49B，上限 250B | geometric proxy |
| mixture | balanced target 选 $w_A=.2$；A-heavy target 选 $w_A=.8$ | deterministic multi-domain loss |
| lifecycle | A/B 在 $Q=500$、总成本 2000 相交；C 被 B 支配 | exact affine-cost identity |
| emergence | $p$ 从 $.616$ 平滑升至 $.834$，$p^{10}$ 从 $.0079$ 升至 $.1624$ | metric-transform construction |
| held-out | 24 planned、22 success、2 failure；最大绝对误差 $.01411$，8/8 区间覆盖 | synthetic E3 bookkeeping |

## 四、实验图 1：直线内插不等于正确渐近结构

先看图回答：左栏为什么 excess slope 保持 $1/2$ 而 raw slope 逐渐变平？右栏两条曲线在 calibration 点重合，为什么到 $10^8$ 会相差约 $.252$？

![[00-知识库管理/_assets/plots/training-optimization/plot-scaling-offset-extrapolation-audit-v1.svg|900]]

> [!figure] 图 EXP-TRN-607-01　Offset-aware slope 与有限窗口函数族分叉
> 左栏精确计算 $d\log L/d\log x$ 与 $d\log(L-E)/d\log x$；右栏让无 offset 幂律穿过 $x=10^2,10^3$ 两个 calibration 点，再与真实 offset 曲线做远尺度比较。来源：[[experiment_scaling_law_resource_audit_v1.py]] 确定性生成；SVG SHA-256 `747dd9998ea0a06ad501e9747f1c8bdc2216f18c88f6aa4fc1f74320b23c9aea`。

**怎样读图**：左栏纵轴是斜率绝对值，不是 loss；右栏先看两条曲线是否在拟合窗口重合，再看进入 validation/held-out 后是否结构性分离。这里内插完全吻合并未阻止远端误差增长。

**图没有证明什么**：合成曲线没有证明真实训练 loss 的 floor 为 1、指数为 $1/2$，也不证明 offset power law 一定优于所有 broken/saturating 函数；它只给出“短窗口直线不能识别渐近结构”的精确反例。

## 五、实验图 2：资源最优谷与数据价值账不能混写

先看图回答：左栏为什么三个预算的 normalized regret 曲线精确重合，却仍只能支持所设代理模型？右栏为什么第 10 轮仍增加 seen tokens，但边际 effective value 已约为首轮的 1%？

![[00-知识库管理/_assets/plots/training-optimization/plot-scaling-compute-data-allocation-audit-v1.svg|900]]

> [!figure] 图 EXP-TRN-607-02　IsoFLOP 近优谷与 repeated-token 饱和
> 左栏固定 $C$，以 $N/N^*$ 扫描 $N$–$D$ 分配并画 relative regret；幂律齐次性使三个预算的归一化曲线重合。右栏比较 $D_{seen}=rU$ 与 $D_{eff}=U(1-q^r)/(1-q)$。来源：同一标准库脚本；SVG SHA-256 `941151148a2e4cf8a35421bfea970ef5c83808d7446de93e8231c780056761f5`。

**怎样读图**：左栏虚线是解析连续最优而不是某个实测架构；曲线两侧分别是“模型过小、数据过多”和“模型过大、数据过少”。右栏蓝线是可计数日志，赭线是声明 $q=.6$ 后得到的潜在价值代理。

**图没有证明什么**：预算曲线重合来自齐次、加性且 $C=\kappa ND$ 的设定，不保证真实系统同形；effective-token 饱和也不提供真实语料的 $q$，更不能据此宣布一个通用 epoch 上限。

## 六、实验图 3：指标陡升与外推通过是两种证据

先看图回答：左栏没有任何不连续机制，exact match 为什么仍显得陡峭？右栏哪一部分允许选函数、哪一部分只能做一次最终评分，两个失败 run 又为何不能删除？

![[00-知识库管理/_assets/plots/training-optimization/plot-scaling-broken-heldout-evidence-audit-v1.svg|900]]

> [!figure] 图 EXP-TRN-607-03　Metric-induced emergence 与 scale-block held-out protocol
> 左栏把平滑 per-step 概率映射为十步 exact match；右栏用整尺度区分 calibration、validation、held-out，画锁定预测区间、观测点和失败分母。来源：同一标准库脚本；SVG SHA-256 `946748d4d16205765fa1adf592d33dfb379b2bccd84c652a7b062c06579e12eb`。

**怎样读图**：左栏两条线共用 $[0,1]$ 概率轴，红线是非线性 metric 而非独立能力；右栏背景色表达信息进入顺序，蓝线/竖条是锁定预测与区间，绿点是观测，红字保留每个 held-out cell 的一次失败。

**图没有证明什么**：左栏只证明 metric 可以制造陡峭表象，不证明所有涌现都是幻觉；右栏的 E3 是合成验收标签，不是对 Kaplan、Chinchilla 或某真实模型族的外部尺度验证。

## 七、十个结果文件

| 文件 | 内容 |
|---|---|
| `offset_slopes.csv` | raw/excess loss、floor 与解析 local slope |
| `extrapolation_families.csv` | calibration/validation/held-out 上的两类预测与误差 |
| `joint_identifiability.csv` | diagonal path 与 $3\times3$ crossed grid 的参数/数据贡献 |
| `compute_optimal_allocation.csv` | 三预算、五分配点、边际平衡、指数与 regret |
| `compute_system_ledger.csv` | model/executed FLOPs、MFU/HFU、时间、能耗与碳排 |
| `repeated_tokens.csv` | unique/seen/effective token、边际权重与饱和上限 |
| `mixture_transfer.csv` | simplex 权重、逐域 loss 与两类部署目标 |
| `inference_break_even.csv` | 训练/单请求/生命周期成本、延迟与 break-even |
| `broken_emergence.csv` | per-step、exact match、零成功概率与 smooth broken slope |
| `heldout_evidence.csv` | scale split、失败分母、锁定区间、误差与证据等级 |

`results.json` 汇总 34 项 checks、artifact manifest 和四条证据边界。

> [!warning] 复现边界
> 本实验是定义验收、解析代理和反例实验。进入真实训练框架后还需多 seed crossed grid、实际 optimizer gap、tokenizer/数据 lineage、profiler/power telemetry、完整调参成本、scale-level block bootstrap、函数族选择、失败分类和真正未见过的 target scales。

## 八、回链与继续实验

- 曲线与联合面：[[经验 Scaling Law、幂律拟合与不可约项]]、[[Kaplan 参数数据律、联合拟合与有限区间]]；
- 分配与系统：[[Chinchilla、Compute-optimal 参数与数据分配]]、[[IsoFLOP、训练算力口径与系统校正]]；
- 数据与部署：[[数据质量、重复、混合与有效 Token]]、[[过训练、推理成本与多目标最优规模]]；
- kink 与证据：[[Broken Scaling、涌现表象与优化架构数据分解]]、[[Scaling 实验设计、外推不确定性与证据地图]]。

学习者至少完成一次干预：移动 calibration window；把 additive joint surface 改成含交互项；改变 $\alpha,\beta$；让 execution multiplier 随规模变化；改 repetition decay；交换 deployment target；加入 nonlinear inference cost；改变 exact-match 长度；或让 held-out scale 超出锁定区间。运行前写定量预测，运行后分别说明改变的是统计函数族、资源约束、数据价值模型、系统口径、指标映射还是证据等级。
