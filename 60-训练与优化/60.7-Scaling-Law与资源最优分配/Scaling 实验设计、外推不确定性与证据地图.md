---
type: research-map
status: verified
area: [training, scaling-laws, experimentation, uncertainty, evidence]
node_id: TRN-56
aliases: [Scaling Law Experimental Protocol, Held-out Scale Audit]
prerequisites: ["[[经验 Scaling Law、幂律拟合与不可约项]]", "[[训练集、验证集、测试集与自适应复用]]", "[[假设检验、置信区间与多重比较]]"]
related: ["[[随机种子、配对比较、置信区间与序贯决策]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2022-Alabdulmohsin-Revisiting-Neural-Scaling-Laws]]", "[[S-2025-Choshen-Hitchhikers-Scaling-Law]]", "[[S-2024-Besiroglu-Chinchilla-Replication]]", "[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]]", "[[S-2025-Ye-Data-Mixing-Laws]]", "[[S-2022-Caballero-Broken-Neural-Scaling-Laws]]", "[[S-2023-Schaeffer-Emergent-Mirage]]", "[[S-2026-Su-11833-解构ScalingLaw]]"]
exercises: ["[[习题 - Scaling 实验设计、外推不确定性与证据地图]]"]
solutions: ["[[解答 - Scaling 实验设计、外推不确定性与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-scaling-experiment-heldout-protocol-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Scaling 实验设计、外推不确定性与证据地图

> [!abstract] 一句话结论
> Scaling 实验的最小单位不是一个点，而是“尺度 cell × seed × checkpoint × 完整训练合同”。可靠外推需要按尺度分离 calibration、function-selection 与 held-out target，分解评测噪声、训练随机性、参数估计和函数族不确定性，并把失败与调参 compute 保留在原分母。

## 一、先把 Claim 写成可失败句子

模糊：

> 模型遵循 Scaling Law。

可检验：

> 对固定 tokenizer、数据 mixture、dense pre-LN Transformer family、AdamW/时钟和 validation loss，在 $N\in[N_1,N_6]$ 的 calibration/validation cells 上拟合候选函数；在未参与函数选择的 $N_7,N_8$ 上，plus-offset model 的 90% prediction interval 覆盖 seed mean，relative error 不超过 $\tau$。

后者明确：

- scale axis/path；
- family；
- training controller；
- metric；
- calibration 与 target；
- function selection；
- interval 与阈值。

## 二、实验单元与数据表

每行至少包含：

| 类别 | 字段 |
|---|---|
| scale | total/non-embedding/active $N$，unique/seen $D$，context/vocab/depth/width |
| run | seed、code/data commit、optimizer、schedule、batch、precision |
| checkpoint | successful step、tokens、model/executed FLOPs、wall time |
| outcome | train/validation loss、domain metrics、failure state |
| system | devices、MFU/HFU、throughput、memory、energy |
| selection | last/best/EMA、early stop、HP search lineage |

checkpoint 不是独立 seed。把同一 run 的 100 个 checkpoints 当作 100 个独立样本会严重低估不确定性。

## 三、Scale Split 不等于随机行 Split

Scaling 的目标是外推到更大尺度，因此 split 应按 scale block：

1. **calibration scales**：估计每个候选函数参数；
2. **validation scales**：选择函数族、offset/regularization；
3. **held-out target scales**：锁定后只评估一次。

若把同一 scale 的不同 seeds 随机分到 train/test，模型只是在插值该尺度，不能证明跨尺度外推。

[[S-2022-Alabdulmohsin-Revisiting-Neural-Scaling-Laws]] 强调 extrapolation loss；[[S-2025-Choshen-Hitchhikers-Scaling-Law]] 显示 intermediate checkpoints 可提高信息利用，但这些 checkpoints 仍需按 run/scale block 处理。

## 四、最小 Grid 设计

若目标是联合 $N,D$ surface：

- 至少多个 $N$；
- 每个 $N$ 至少多个 $D$；
- 多条近似 IsoFLOP slices；
- 每个关键 cell 多 seeds；
- 最大尺度留出。

只有一条 $D\propto N^q$ 路径无法分别识别参数项和数据项。只有每 compute 一个模型也无法观察 IsoFLOP valley。

资源有限时优先：

1. 保留关键横向/纵向切片；
2. 牺牲过密的中间点；
3. 用 intermediate checkpoints 增加 time-axis 信息；
4. 不删除 held-out target；
5. 对 near-optimal valley 加密。

## 五、四层不确定性

### 1. Evaluation noise

固定 checkpoint，在有限 validation tokens 上的均值误差。可用文档/block bootstrap，避免把强相关 tokens 当 iid。

### 2. Training randomness

seed、data order、dropout、distributed nondeterminism 引起。需要真正独立 runs。

### 3. Parameter uncertainty

在固定函数族下，$E,A,\alpha$ 等估计误差与相关性。

### 4. Structural uncertainty

plus-offset、finite-correction、broken law、joint surface 等函数族之间的差。

总 prediction interval 不能只用回归参数的 standard error；外推时 structural uncertainty 常占主导。

## 六、Block Bootstrap 的对象

推荐层级：

1. 以 scale cell 为外层；
2. cell 内 resample seeds；
3. seed 内若需要，再对 evaluation documents 做 block bootstrap；
4. 每次完整重拟合函数并重新求 optimum；
5. 得到 target loss、$N_*,D_*$ 与 breakpoint 的分布。

不要：

- 独立 resample 同一训练曲线的相邻 checkpoints；
- 只 resample regression residual 而忽略 seed heteroskedasticity；
- 在 bootstrap 中偷偷重新选择最有利窗口却不计 selection。

## 七、函数族与 Model Selection

候选可含：

$$
\begin{aligned}
M_1&:L=Ax^{-\alpha},\\
M_2&:L=E+Ax^{-\alpha},\\
M_3&:L=E+Ax^{-\alpha}(1+Bx^{-\delta}),\\
M_4&:\text{smoothly broken power law}.
\end{aligned}
\tag{1}
$$

选择标准按优先级：

1. held-out scale loss；
2. prediction interval calibration；
3. residual pattern；
4. complexity penalty；
5. parameter stability/sensitivity。

in-sample $R^2$ 只能作最低层诊断。

## 八、超参数与训练充分度

每个 scale 的 optimizer 若不公平，会把 optimization gap 写入 scaling exponent。

两种合法协议：

### Locked recipe

用前卷 μTransfer 或预注册规则映射超参数，适合测 family+recipe 的整体 scaling。

### Per-scale tuned

每个 scale 给对称 search space、algorithm、seeds 与 compute，适合估计各规模可达 frontier。

两者回答不同问题，不能把 per-scale tuned target 与 locked proxy 小模型混在一条曲线。

[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]] 是 optimization protocol 改变 scaling 结论的直接案例。

## 九、Failure Denominator

NaN、OOM、timeout、divergence、loss spike、checkpoint corruption 和人为中止都留在发起 cell 的分母。

如果只对成功 runs 拟合：

- 不稳定大模型被删除；
- 平均 loss 偏好能完成的配置；
- compute 与 wall-time 总账偏低；
- prediction interval 忽略 catastrophic tail。

可用两部分报告：

1. success/failure probability；
2. 条件于成功的 loss curve。

二者都重要，不能只保留第二个。

## 十、外推误差与决策误差

点预测误差：

$$
e_{\rm pred}
=\frac{|\widehat L(x_t)-L(x_t)|}{|L(x_t)-E|+\epsilon}.
\tag{2}
$$

若目标是选 allocation，更重要的是 decision regret：

$$
R_{\rm decision}
=L(x_t,\widehat a_*)-\min_aL(x_t,a).
\tag{3}
$$

曲线预测有小误差不保证最优 allocation 正确；反之，valley 很平时参数预测偏差大、regret 仍小。

因此同时报告：

- loss calibration；
- optimum/near-optimal region；
- decision regret；
- budget overrun。

## 十一、多重比较与事后选窗口

若尝试 20 个窗口、10 个函数族、5 种 metric，只报告最平的一条线，nominal interval 已失效。

可采取：

- 预注册 primary model/window；
- secondary analyses 明确标 exploratory；
- nested validation 选函数；
- held-out target 不参与任何选择；
- 保存所有尝试与 compute；
- 对多个 benchmarks 报 false-discovery/家族级解释。

[[S-2023-Schaeffer-Emergent-Mirage]] 说明 metric choice 本身可制造表面转折；因此 metric 也属于预注册对象。

## 十二、证据等级

| 等级 | 已完成 | 允许措辞 |
|---|---|---|
| E0 | dimensional/optimization derivation | “在假设模型内 exponent 自洽” |
| E1 | synthetic/toy simulation | “程序能回收已知 law/反例” |
| E2 | calibration-window multi-seed fit | “观测窗口内描述良好” |
| E3 | held-out larger scales | “在锁定 family/path 上外推通过” |
| E4 | alternate data/architecture replication | “在列明设置中有外部复现” |
| E5 | decision trial | “使用该 law 的资源决策达到预注册 regret/cost 门” |

没有 E3，不说 target extrapolation；没有 E5，不说资源决策已经被验证有效。

## 十三、图：Scale 必须按时间顺序进入证据

先看图回答：为什么 validation scale 可以参与函数选择，而 held-out target 不可以？四种不确定性在哪一步进入 prediction interval？

![[00-知识库管理/_assets/figures/training-optimization/fig-scaling-experiment-heldout-protocol-v1.svg|900]]

> [!figure] 图 TRN-56-01　Calibration→selection→held-out→decision 的证据流水线
> 来源：课程原创教材图；上栏按 scale block 划分数据，下栏将 evaluation、seed、parameter 与 function-family uncertainty 送入 prediction interval，最后以 decision regret 验收。概念依据：[[S-2022-Alabdulmohsin-Revisiting-Neural-Scaling-Laws]]、[[S-2025-Choshen-Hitchhikers-Scaling-Law]]。

**怎样读图**：沿尺度从左到右，只允许信息单向流动；任何 target 反馈到函数/窗口选择的箭头都构成泄漏。

**图没有证明什么**：流水线不保证选中的函数真实，也不替代足够尺度跨度；它定义可审计外推程序。

## 十四、最终 Report 模板

1. Claim card：family、axes、metric、target、阈值；
2. Scale/parameter/data/compute contract；
3. 全部 cells、seeds、checkpoints、failures；
4. 候选函数与 error model；
5. calibration/validation/held-out split；
6. parameter、structural、prediction uncertainty；
7. IsoFLOP minima 与 near-optimal region；
8. system/energy/tuning/selection budget；
9. sensitivity 与 negative results；
10. 有限作用域结论和下一次可证伪实验。

做到这十项，Scaling Law 才从漂亮图变成研究与工程决策工具。
