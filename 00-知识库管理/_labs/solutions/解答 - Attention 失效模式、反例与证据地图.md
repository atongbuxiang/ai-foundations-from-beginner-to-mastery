---
type: solution
status: draft
area: [architecture, attention, evidence]
topic: "[[Attention 失效模式、反例与证据地图]]"
exercise: "[[习题 - Attention 失效模式、反例与证据地图]]"
sources: ["[[S-2019-Jain-Wallace-Attention-Explanation]]", "[[S-2019-Michel-Head-Pruning]]", "[[S-2020-Yun-Transformer-Universal-Approximation]]", "[[S-2021-Dong-Pure-Attention-RankCollapse]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Attention 失效模式、反例与证据地图

## A. 识别与复述

### ARCH-EVID-A01
`I` 可复算恒等，如 rank$(QK^T)\le d_k$；`T` 带假设定理，如 pure-attention rank collapse；`E` 版本化实验，如某 checkpoint head pruning；`H` 机制猜想，如 causal full rank 解释 decoder-only；`O` 未验证外推，如同方法在更大模型/更长上下文仍有效。

### ARCH-EVID-A02
症状：一行权重的熵较基线低。可能机制：logit scale/norm 增大、正确稀疏选择、shortcut 饱和或 mask 候选变少。不能推出准确率提高、解释忠实、rank 健康或长度泛化；需控制可见数并做 temperature/norm/候选干预。

### ARCH-EVID-A03
内部读取描述问该层 A 如何混合 V；局部敏感性问小扰动输入/权重的微分影响；反事实忠实性问替换/删除是否改变预测；人类语义解释问模式是否可理解/合理。它们的目标和验证标准不同，不能由同一热图同时证明。

## B. 手算与建模

### ARCH-EVID-B01
令 $v_1=v_2=v$，权重 $a=(1,0),b=(0,1)$，均输出 v。权重图完全不同但本层输出相同，说明权重不具备唯一功能归因；若后续只看输出，也无法区分两种解释。

### ARCH-EVID-B02
可说：在这组未说明不确定性的测量中，normalized 版本各测试长度 loss 更低，且随长度退化较缓；这是 `E`。不可说因 key normalization 单一机制导致、统计显著、任意模型有效或 4096 以上仍有效；还缺 seed、数据、baseline 调参、logit诊断与规模实验。

### ARCH-EVID-B03
单个 head 的边际作用小，但 heads 之间存在替代/交互；单头效应不可相加。联合剪 80% 暴露冗余容量耗尽或关键组合被移除。结论应来自整个 pruning curve，而非一次 zeroing。

## C. 推导与证明

### ARCH-EVID-C01
令远端 value 全被投影为 0，或对目标 token 的权重为 0/随 T 稀释到 $1/T$；尽管 query 到它有一条直接边，输出不含可恢复信号。Path length 是图结构事实，不给 channel capacity、weight 或 value injectivity。

### ARCH-EVID-C02
Rank-collapse 研究无 skip/MLP 的 pure attention 深堆叠，在规定条件下得 residual component 收缩。通用逼近研究含完整 Transformer 组件/位置条件、允许构造深宽，对紧致域连续函数给存在参数。模型类和量词不同：某受限递推会退化，不妨碍更丰富类存在通用逼近器。

### ARCH-EVID-C03
设 quadratic kernel 时间 $t_q(T)=aT^2$，linear 方法 $t_l(T)=bTr+cT$，其中 b/c 可因 feature/kernel 较大。只有 $T>(br+c)/a$ 左右才可能交叉；缓存、tile 和 fixed overhead 还会改变式子。因此渐近阶不裁决有限 T。

## D. 边界、反例与纠错

### ARCH-EVID-D01
论文在特定 NLP 模型中否定“权重自动等于忠实解释”的普遍假设；它未测试所有架构、层、头和解释目标。Attention 可视化仍可描述内部读取、发现 bug、提出假说；只是因果/反事实结论需额外干预。

### ARCH-EVID-D02
训练时过参数化可帮助优化、提供替代路径或让任务分配后再压缩；训练后一个 checkpoint 的局部剪枝不说明较小架构从头训练可达同解。还存在联合剪枝非线性、任务/OOD差异和系统 kernel 约束。

### ARCH-EVID-D03
小模型结果依参数规模、GAU 架构、数据、position、训练长 512 和测试协议；scale-up 会改变 norm、优化、数据与 kernel。最多形成可复现的 `E` 和待验证的 `H/O`，不能用归纳一例给全称保证。

## E. AI 迁移

### ARCH-EVID-E01
Card 应含：精确方法/版本；same-quality 定义；模型/参数与训练 FLOP；QKV/mask/position；数据/split/length；feature/head width；dtype/hardware/kernel；峰值 memory、prefill/decode/backward latency；多 seed quality；crossover curve。否证：在对齐质量/预算后扫描 T/batch，若任何宣称范围无速度收益或近似误差导致质量差即限制 claim，而不是挑最佳点。

### ARCH-EVID-E02
固定输入与 V/后续网络，寻找/优化另一组 A' 与 A 差大但输出近似，检查预测稳定；再交换/删除高权重位置，并与等量随机/梯度基线比较。另做 value-controlled synthetic task 知道真因果 token。报告层/头/样本分布；若改变 A 同时改变 V，不能归因权重本身。

### ARCH-EVID-E03
症状：长度增大 loss 上升。测量：q/k norm、logit std/max、entropy/effective support、position phase、mask/cache、spectra、latency。干预：temperature/key norm、position方案、训练长度 curriculum、window/cache kernel 对照，一次改变一项。Shape/mask恒等为 `I`，已有定理保条件为 `T`，扫描结果为 `E`，机制解释为 `H`，更大规模为 `O`；最终只写实验支持的范围。
