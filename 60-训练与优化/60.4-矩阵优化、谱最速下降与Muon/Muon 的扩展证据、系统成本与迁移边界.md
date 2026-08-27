---
type: evidence-map
status: verified
area: [training, optimization, muon, systems, reproducibility]
node_id: TRN-32
aliases: [Muon Scale Evidence, Muon Migration Protocol]
prerequisites: ["[[Muon 的动量、正交化与参数分组合同]]", "[[Muon 形状缩放、Update RMS 与版本差异]]", "[[训练系统的对象、状态与一步更新合同]]"]
related: ["[[单因素、全因子消融与交互效应]]", "[[训练实验协议、事故记录与因果证据地图]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]", "[[训练与优化完整课程地图与掌握标准]]"]
sources: ["[[S-2024-Jordan-Muon]]", "[[S-2025-Liu-Muon-Scalable-LLM]]", "[[S-2026-PyTorch-Muon]]", "[[S-2025-Su-11416-Muon优化器指南]]", "[[S-2026-Su-11772-Muon-max-scaling]]", "[[S-2026-Su-11777-Muon双旋转]]"]
exercises: ["[[习题 - Muon 的扩展证据、系统成本与迁移边界]]"]
solutions: ["[[解答 - Muon 的扩展证据、系统成本与迁移边界]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-muon-evidence-system-migration-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Muon 的扩展证据、系统成本与迁移边界

> [!abstract] 一句话结论
> Muon 已从小模型原型走到公开的大规模语言模型训练和主流框架接口，但“能规模化”不等于“对任意模型都更优”。可靠决策必须把算法证据、同预算 quality、wall-clock、通信、显存、调参成本和失败运行放在同一张账上。

## 一、先用证据阶梯替代“已经被证明”

### L0：数学身份

- spectral norm 与 nuclear norm 对偶；
- exact polar factor 为 canonical steepest direction；
- partial isometry 的 Frobenius/RMS identity。

这些是可证明的线性代数/凸分析结论，但不包含神经网络训练优势。

### L1：算法定义与小规模原型

[[S-2024-Jordan-Muon]] 给出 Muon 名称、参考实现、参数分组建议以及 NanoGPT/CIFAR/早期 1.5B 实验。这能证明“明确算法在这些设置中可运行并产生所报告曲线”，但外推范围受任务、实现、调参和基线约束。

### L2：大规模单组织主证据

[[S-2025-Liu-Muon-Scalable-LLM]] 报告 3B/16B MoE、最高 5.7T tokens 的 Moonlight 训练，并在论文协议内报告约 2 倍 compute efficiency。应保留：

- 模型族与 MoE 架构；
- 数据、token budget 和 scaling-law fit；
- baseline 的训练配方与超参数搜索；
- weight decay、shape adjustment 和 distributed implementation；
- 开源代码/checkpoint 所能复核的范围。

“约 2 倍”只能在论文的 compute-optimal 比较口径中引用，不能直接改写为 wall-clock 减半或所有 dense LLM 上两倍。

### L3：框架产品化

[[S-2026-PyTorch-Muon]] 表明 Muon 已进入主流 optimizer API，并给出当前 transition/defaults。框架收录提升可用性和实现审计能力，却不是跨任务 superiority 的独立实验。

### L4：跨组织、跨模型、长期复现

真正强的通用结论还需多个独立团队在 dense/MoE、vision/language/multimodal、不同 width/depth、不同硬件与同调参预算下复现，并公开失败结果。2026 年近期博客变体应仍放在 frontier 层。

## 二、“compute efficiency”至少有四个分母

设验证 loss/quality 达到同一门槛，常见成本口径包括：

1. **tokens**：需要多少训练 token；
2. **model FLOPs**：理论前后向计算；
3. **optimizer-inclusive FLOPs**：再加 NS、communication 与状态更新；
4. **wall-clock / energy / dollar**：真实 kernel、network、failure/restart 的系统成本。

一个 optimizer 可能在 tokens-to-quality 更好，却因额外 GEMM 或通信使 wall-clock 优势变小；也可能 NS GEMM 在加速器上效率高，额外理论 FLOPs 对实际 step time 影响有限。必须实测，不能从 FLOP 公式直接猜 wall-clock。

## 三、Muon 系统成本从哪里来

### 3.1 每步矩阵乘

每个 Newton–Schulz step 包含若干 Gram/GEMM。总成本取决于 $A\times B$ shape 和选择 $X^TX$ 还是 $XX^T$。对许多小矩阵，kernel launch 和 batching 可能主导；对超大矩阵，算力和通信成为主导。

### 3.2 persistent state 与 workspace

- momentum buffer：通常每个 Muon parameter 一个同 shape state；
- master weights / gradients：由混合精度和 optimizer framework 决定；
- NS workspace：Gram matrix、temporary products、可能的 fused buffers；
- fallback AdamW groups：另有 first/second moments。

报告 peak memory 时必须包含 Muon 与 fallback optimizer 的联合峰值，而不是只数 Muon buffer。

### 3.3 distributed layout

可能方案：

- replicated parameter：先 all-reduce gradient，再本地一致地做 NS；
- tensor-parallel shard：对 shard 做局部 NS，结果一般不等于 global polar；
- gather–orthogonalize–scatter：更接近 global object，但增加通信和 peak；
- distributed matrix multiplication：保持 global geometry，系统复杂度更高。

还要记录 collective tail latency、overlap 程度和 straggler。平均 step time 不能隐藏 P95/P99。

## 四、公平比较协议

### 4.1 先固定目标，再分配同等搜索预算

预先注册：

- target validation loss / downstream score；
- total tokens 或 total wall-clock；
- model/data/seed；
- learning-rate、decay、warmup 与 scaling 搜索空间；
- 每种 optimizer 相同的 trial 数或总搜索 compute。

若只精调 Muon 而沿用未调的 AdamW baseline，或反之，就不能归因于 optimizer。

### 4.2 至少三种横轴

同一 run 画：

$$
\text{quality vs tokens},\quad
\text{quality vs model FLOPs},\quad
\text{quality vs wall-clock}.
$$

并附：

- tokens/s、step time median/P95；
- peak allocated/reserved memory；
- optimizer kernel time 与 communication time；
- NaN、divergence、restart、OOM 和人工干预；
- 最优 run 之外的 trial distribution。

### 4.3 消融必须拆组合包

Muon 配方常同时改变：

- momentum convention；
- polar/NS；
- shape scaling；
- weight decay；
- parameter groups；
- LR schedule。

至少做逐项 ablation 或 factorial subset，才能知道收益来自哪里。只比较完整 Muon package 与旧 AdamW package，得到的是“配方差异”，不是单一 polar mechanism 的因果估计。

## 五、从 AdamW 迁移到 Muon 的风险

### 5.1 状态不兼容

AdamW 有 first/second moments $(m_t,v_t)$；Muon 至少有 matrix momentum $B_t$。不存在无假设的 lossless state map：

$$
(m_t,v_t)\not\longleftrightarrow B_t.
$$

中途切换可选：

- **reset**：Muon buffer 从零开始；会产生新的 warmup transient；
- **heuristic map**：用 Adam first moment 初始化，但需处理 EMA convention、scale 和 parameter group；
- **overlap phase**：短期混合两类 update；这又定义了新算法。

任何选择都要标记 switch step 并单独画 transition window。

### 5.2 learning rate 不能照抄

AdamW update 受 $v_t^{-1/2}$ 影响；Muon direction 的 scale 由 polar 与 shape adjustment 决定。同一个数字 learning rate 没有相同物理意义。迁移应从 layerwise

$$
\operatorname{RMS}(\Delta W),\quad
\frac{\operatorname{RMS}(\Delta W)}{\operatorname{RMS}(W)},\quad
\lVert\Delta W\rVert_2
\tag{1}
$$

对齐，而非只复制配置字段。

### 5.3 decay 与 parameter groups

embedding、head、bias/norm 仍可能用 AdamW。若 weight tying 使 embedding 与 output head 共用 tensor，就不能同时加入两个 optimizer；必须选择唯一 owner。decay 也要核对 base LR/adjusted LR 和 exclusion rules。

### 5.4 checkpoint 与回滚

上线前保存：

- 完整旧 optimizer state；
- parameter-group manifest 与 tensor names；
- 新旧配置、代码 commit、RNG state；
- 可在一个 evaluation interval 内回滚的 checkpoint；
- NaN/OOM/quality regression 的停止门。

## 六、建议的三阶段迁移实验

### 阶段 A：离线 replay

从已有 gradient/activation trace 或小模型 checkpoint 比较：

- direction cosine；
- update RMS/spectral norm；
- NS residual；
- per-layer state bytes 和 kernel cost。

不声称最终 quality，只排除显然的 scale/shape 错误。

### 阶段 B：缩小版 controlled run

固定 data order 与 seeds，执行 AdamW、Muon 和关键 ablations；观察至少一个完整 LR schedule，并包括 3—5 个 seeds 或等效不确定性分析。

### 阶段 C：shadow-scale 与正式扩展

先用少量节点/短 token horizon 测量 distributed tail，再按预注册 gate 扩展。gate 示例：

| Gate | 通过条件示例 |
|---|---|
| 数值 | 无 NaN/Inf；NS residual 在层级阈值内 |
| 质量 | 同 tokens 不劣于 baseline 的容忍区间 |
| 系统 | step P95、peak memory、network bytes 在预算内 |
| 稳健 | seed/trial 分布无明显长尾失败 |
| 运维 | checkpoint save/load 与回滚演练通过 |

阈值由项目风险决定，不能把示例数字写成通用标准。

## 七、图：证据阶梯、系统账本与迁移门

先看图回答：一个“更快”的 Muon 结果处在哪个证据层、使用什么成本分母，又必须通过哪些迁移门才能扩展？

![[00-知识库管理/_assets/figures/training-optimization/fig-muon-evidence-system-migration-v1.svg|900]]

> [!figure] 图 TRN-32　Muon 证据层级、系统成本与迁移协议
> 左栏从数学身份、原型、大规模主证据到跨组织复现分级；中栏展开 tokens/FLOPs/wall-clock/state/communication；右栏给出 AdamW→Muon 的 replay、controlled run、shadow-scale 和 rollback 门。来源：依据 [[S-2024-Jordan-Muon]]、[[S-2025-Liu-Muon-Scalable-LLM]]、[[S-2026-PyTorch-Muon]] 独立绘制。

**怎样读图**：任何性能声明先落到左栏证据等级，再沿中栏补齐分母，最后才决定能否通过右栏迁移门。

**图没有证明什么**：图不替代具体模型的 benchmark，也不把框架支持当作通用效果证明。

## 八、本节出口

你应能对 Muon 结果给出不越界的证据表述，设计同调参预算的多横轴 benchmark，估算 NS/state/communication 成本，并写出支持回滚的 AdamW→Muon 迁移合同。

## 练习与独立解答

- [[习题 - Muon 的扩展证据、系统成本与迁移边界]]
- [[解答 - Muon 的扩展证据、系统成本与迁移边界]]
