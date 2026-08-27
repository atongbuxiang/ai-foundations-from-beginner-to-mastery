---
type: research-map
status: verified
area: [training, optimization, mup, scale-up, experimentation]
node_id: TRN-48
aliases: [μP Scale-up Protocol, μP Evidence and Failure Boundaries]
prerequisites: ["[[μTransfer、Base Shape 与超参数零样本迁移]]", "[[谱条件、高阶 μP 与参数更新稳定性]]", "[[训练控制器的联合实验、消融与证据地图]]"]
related: ["[[训练 Telemetry、损失梯度更新与激活总账]]", "[[随机种子、配对比较、置信区间与序贯决策]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2022-Yang-Tensor-Programs-V-MuTransfer]]", "[[S-2026-Microsoft-MuP-Implementation]]", "[[S-2025-EssentialAI-Practical-Muon-MuP]]", "[[S-2026-Zheng-Spectral-MuP-Width-Depth]]", "[[S-2026-Su-11729-MuP之上4]]", "[[S-2024-Su-10001-LoRA差分学习率]]"]
exercises: ["[[习题 - Scale-up 协议、μP 证据与失效边界]]"]
solutions: ["[[解答 - Scale-up 协议、μP 证据与失效边界]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-scale-up-evidence-failure-gates-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Scale-up 协议、μP 证据与失效边界

> [!abstract] 一句话结论
> μP scale-up 成功必须同时满足：shape/parameterization 正确、坐标与功能更新跨尺度稳定、超参数曲线或 transfer regret 可接受、目标规模未触发预注册失败门、总调参/确认预算诚实。单张水平 coord plot、单个 target loss 或一次没有 NaN 的训练都只能支持其中一层。

## 一、先把要证明的 Claim 写窄

模糊 claim：

> μP 可以让超参数跨模型规模迁移。

可检验 claim：

> 对固定 pre-LN Transformer family、tokenizer、数据分布、AdamW 语义和训练 token budget，仅改变 $d_{model}$ 与 $d_{ff}=4d_{model}$、固定 depth/head path；在预注册 LR/init-multiplier 网格与 seeds 下，base-coordinate 最优区间跨宽度重叠，proxy 选择在 target 的 transfer regret 不超过 $\tau$，且 activation/feature/logit 与失败率通过门限。

后者明确了：

- family；
- scale axes/path；
- optimizer/training clock；
- HP set；
- outcome；
- tolerance；
- failure denominator。

## 二、Scale-up 前的冻结清单

在任何 target run 前保存不可变 manifest：

### 模型

block 公式、depth、width ratios、head path、norm、residual multiplier、activation、tying、position/attention scaling、MoE/LoRA 等。

### 参数化

base/delta shapes、每个 parameter 的 infshape、orientation、init multiplier、forward multiplier、optimizer group、实际 LR formula。

### 数据与时钟

tokenizer、dataset snapshot、sampling mixture、sequence packing、batch/token reduction、steps/tokens/FLOPs、schedule endpoints。

### 搜索与选择

HP space、search algorithm、seeds、evaluation cadence、last/best/EMA、early stop、failure handling、primary metric。

### 计算预算

$$
C_{total}=C_{train}+C_{tune}+C_{select}+C_{eval}+C_{confirm}.
\tag{1}
$$

target health check 和 rescue run 属于 $C_{confirm}$，不能从 μTransfer 成本中消失。

## 三、一个 5×5 Scale Grid

每次只改变一个轴很清楚，但不足以发现交互。建议建立最小二维/分阶段网格：

| 轴 | 示例 levels | 要回答的问题 |
|---|---|---|
| width | 128, 256, 512, 1024 | 基本 μP/curve transfer |
| depth | 6, 12, 24 | residual accumulation |
| aspect | $d_{ff}/d=2,4,8$ | non-square shape rule |
| head path | fixed $h$ / fixed $d_h$ | attention scaling |
| optimizer | SGD / AdamW / Muon-hybrid | direction scale 是否重译 |

不必跑完整笛卡尔积。可以：

1. 固定其余轴验证 width；
2. 在两个代表 width 上验证 depth/aspect/head interaction；
3. 只在通过 telemetry gate 的 family 中比较 optimizer；
4. 对关键交互做 full factorial 子集。

任何新增轴都意味着原 claim 的适用域扩大，应获得新证据。

## 四、四类主要结果与一个失败分母

### 1. 参数化正确性

- base/delta/target shape diff；
- parameter group actual init/LR；
- coord-check slope；
- fan orientation 和特殊参数组测试。

### 2. 稳定性/机制

- activation/preactivation RMS；
- gradient、direction、parameter update；
- feature/logit update；
- spectral norm/effective rank；
- attention entropy、norm/residual stats。

### 3. 超参数迁移

- full proxy curves；
- near-optimal set overlap；
- argmin/optimum drift；
- transfer regret；
- rank correlation。

### 4. 训练与资源

- train/validation loss；
- tokens/FLOP、wall time、memory/communication；
- downstream metric 及其选择协议；
- last/best/EMA 分工。

### 5. 失败分母

OOM、NaN、Inf、divergence、timeout、loss spike、checkpoint corruption 和人为中止都保留在原配置分母中。只报告成功 run 会让“不稳定参数化”看似性能更好。

## 五、三种迁移指标

令 $F_n(h)$ 为 width $n$ 的期望 objective。

### 1. Optimum drift

$$
D_{opt}(n,n_0)
=d(h_n^*,h_{n_0}^*).
\tag{2}
$$

它直观，但对平坦、多峰和离散 grid 很不稳。

### 2. Transfer regret

$$
R(n\leftarrow n_0)
=F_n(h_{n_0}^*)-\min_hF_n(h).
\tag{3}
$$

它回答“复制 proxy 选择实际损失多少”，比 argmin distance 更接近决策价值。

### 3. Near-optimal overlap

定义

$$
\mathcal H_n(\tau)
=\{h:F_n(h)\le\min_hF_n(h)+\tau\}.
\tag{4}
$$

比较 $\mathcal H_{n_0}(\tau)$ 与 $\mathcal H_n(\tau)$ 的交集。若谷底很平，最优 grid point 可变化但 near-optimal region 大量重叠，迁移仍很实用。

所有指标都应带 seed uncertainty。若 target 不做 sweep，就不能无偏估计 target minimum；此时应降低措辞为“transferred HP 达到某绝对/基线结果”。

## 六、预注册 Failure Gates

### Gate A：Shape

- missing/mismatched parameter names = fail；
- 未解释的 finite/infinite dimension = fail；
- tied/custom tensor 无 orientation = fail。

### Gate B：Coordinate

- activation/update slope 超阈值；
- 最宽/最窄 ratio 超区间；
- readout/attention 瞬态不符合预期；
- 任一关键层消失或爆炸。

### Gate C：Spectral/Depth

- normalized spectral weight/update 随 width/depth 系统漂移；
- residual stream 或 Jacobian proxy 越界；
- rank collapse/top singular concentration 未解释。

### Gate D：Training Safety

- NaN/Inf/OOM/overflow/clip rate；
- loss spike、logit saturation、attention entropy collapse；
- throughput/communication 超预算。

### Gate E：Transfer

- proxy curves 不对齐；
- near-optimal set 无重叠；
- transferred HP regret/absolute result 未达阈值；
- target rescue 次数超预注册预算。

Gate 触发后的正确动作是暂停、定位层级和更新 claim；不是删除 run 后继续。

## 七、失效模式到诊断的映射

| 观察 | 首要假说 | 区分实验 |
|---|---|---|
| $t=0$ hidden RMS 随 width 漂移 | init/fan orientation | forward-only coord check |
| $t=0$ 正常，step 1 爆炸 | LR/group/optimizer normalization | 记录 raw grad→direction→actual update |
| 只有 readout 爆炸 | output rule/MuReadout 遗漏 | zero-init + readout group audit |
| attention entropy随 width 塌缩 | score scaling/head path | 固定 $h$ vs 固定 $d_h$ |
| width 迁移好，depth 失败 | residual/Jacobian accumulation | fixed width depth ladder |
| RMS 平稳，谱增长 | low-rank aligned update | SVD/power iteration + effective rank |
| proxy optimum 稳，target 失效 | finite jump/data/system change | 中间尺度 telescoping |
| train loss 迁移，val 不迁移 | regularization/data-size effect | WD/dropout 单独搜索 |
| LoRA A/B 一端不动 | zero-init/gradient coupling | factor-wise gradient/update telemetry |
| resume 后突然失稳 | infshape/scheduler state 丢失 | fresh-vs-resume state diff |

## 八、Reverse μTransfer：用小模型复现大模型事故

若 target 出现 instability，可以把 target 的 base-coordinate recipe 映射回较小模型，尝试复现相同 telemetry signature。若小模型也出现同一层的 feature/logit/spectral drift，说明问题更可能来自参数化或 recipe；若只在 target 出现，则考虑：

- width 未进入相同有限范围；
- depth/aspect/head path 改变；
- distributed reduction/precision/system 差异；
- data order/batch/sequence 改变；
- 长时状态和稀有事件。

reverse transfer 是诊断，不是因果证明；复现失败也不排除小模型统计功效不足。

## 九、Telescoping 的预注册形式

当一步从 proxy 到 target 太远，可设

$$
n_0<n_1<\cdots<n_K=n_{target}.
\tag{5}
$$

在第 $k$ 层只允许搜索上一层 near-optimal set 的预定义邻域 $\mathcal N_k$，并记录

$$
C_{tune}^{tel}
=\sum_{k=0}^{K}C_{search,k}.
\tag{6}
$$

优点是及时发现 optimum drift 和 implementation error；缺点是 target information 已逐步进入选择，不能再把全流程称“零 target tuning”。

[[S-2025-EssentialAI-Practical-Muon-MuP]] 提供近期实践入口；具体效率结论限定于其 Muon/模型/数据/系统协议。

## 十、证据等级与允许措辞

| 等级 | 已完成 | 允许措辞 |
|---|---|---|
| E0 | exponent 手推 | “规则在假设下量级自洽” |
| E1 | toy/statistical simulation | “有限样本趋势支持推导” |
| E2 | multi-width coord/spectral check | “实现未见显著尺度漂移” |
| E3 | proxy HP curves | “在 proxy ladder 上 optimum region 稳定” |
| E4 | target confirm + comparator | “在锁定 family/axes/protocol 内迁移成功” |
| E5 | 多架构/数据/轴重复 | “在这些列明设置中具有外部复现” |

不允许从 E2 直接写“μP 提高性能”，也不允许从单个 E4 写“所有大模型可 zero-shot tuning”。

## 十一、一个最小报告模板

```text
Claim domain:
  architecture / scale axes / optimizer / data / clock

Shape contract:
  base / delta / target / infshape diff / special groups

Transfer contract:
  HP space / proxy widths / seeds / selection / target-confirm budget

Telemetry gates:
  coordinate / feature / logit / spectral / depth / failures

Outcomes:
  full curves / near-optimal sets / regret or bounded wording

Budget:
  train + tune + select + eval + confirm + failed runs

Boundary:
  untested axes / implementation version / unresolved failures
```

## 十二、图：从 Shape 到 Claim 的六道门

先看图回答：为什么 target loss 好看仍不能反推 shape oracle 和 μP 实现正确？

![[00-知识库管理/_assets/figures/training-optimization/fig-scale-up-evidence-failure-gates-v1.svg|880]]

> [!figure] 图 TRN-48　Scale-up 的 Shape、Coordinate、Spectral、Transfer、Safety 与 Budget Gates
> 图将 scale-up 分为 family/shape 冻结、机制遥测、proxy 曲线、target 确认和证据措辞；任何失败沿红色回路退回最近可诊断层，而不是删除运行。来源：依据 [[S-2022-Yang-Tensor-Programs-V-MuTransfer]]、[[S-2025-EssentialAI-Practical-Muon-MuP]] 与 [[S-2026-Zheng-Spectral-MuP-Width-Depth]] 原创绘制。

**怎样读图**：从左到右逐门升级 claim；如果 shape 或 coordinate gate 未过，后续好 loss 只能是一次观察，不能验证 μP 机制；若 target 多次调整，预算和方法名称同步更新。

**图没有证明什么**：六道门提高可证伪性，不保证任何 family 必然迁移成功；门限、grid、seeds 和 target budget 都需在具体项目中预注册。

## 十三、初学者自检

1. 一个合格的 μP scale-up claim 至少要限定哪些轴？
2. transfer regret 与 optimum drift 为什么回答不同问题？
3. target 不做 sweep 时，为什么不能宣称 transferred HP “近似最优”？
4. coordinate stable、spectral unstable 表示什么候选机制？
5. target rescue 为什么必须进入 $C_{confirm}$？
6. reverse μTransfer 能诊断什么，不能证明什么？
7. E2 与 E4 的允许措辞有什么差别？

## 十四、本节出口

你应能把一次扩展实验组织为

$$
\text{family/shape}
\to\text{coordinate}
\to\text{spectral/depth}
\to\text{proxy curves}
\to\text{target safety}
\to\text{budgeted claim},
$$

并在任何一层失败时给出可定位、可复现、不过度外推的结论。
