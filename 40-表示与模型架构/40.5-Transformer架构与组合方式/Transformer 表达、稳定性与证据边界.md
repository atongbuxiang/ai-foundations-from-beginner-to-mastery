---
type: concept
status: draft
area: [architecture, transformer, expressivity, stability, evidence]
aliases: [Transformer 理论边界, Transformer 稳定性, Transformer Expressivity]
node_id: ARCH-40
prerequisites: ["[[Transformer Block、残差、归一化与 FFN]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]", "[[残差缩放、Lipschitz 界与深度稳定性]]"]
related: ["[[Transformer 架构与组合方式 MOC]]", "[[Decoder-Only、Prefix 与架构家族比较]]", "[[Transformer 形状、参数量与 FLOPs 总账]]"]
sources: ["[[S-2020-Yun-Transformer-Universal-Approximation]]", "[[S-2021-Dong-Pure-Attention-RankCollapse]]", "[[S-2020-Xiong-Transformer-LayerNorm]]", "[[S-2022-Wang-DeepNet]]", "[[S-2021-Su-8978-千层Transformer困难]]", "[[S-2022-Su-8994-Why-Residual]]", "[[S-2022-Su-9009-PreNorm-PostNorm]]", "[[S-2026-Chen-Attention-Residuals]]", "[[S-2026-Su-11664-Attention-Residuals]]"]
exercises: ["[[习题 - Transformer 表达、稳定性与证据边界]]"]
solutions: ["[[解答 - Transformer 表达、稳定性与证据边界]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-transformer-stability-evidence-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Transformer 表达、稳定性与证据边界

> [!abstract] 本节主问题
> Transformer “能表示什么”“是否训练稳定”“在某任务是否有效”是三个不同问题。表达定理要保留函数空间、紧集、position 与精度假设；稳定性要看 Jacobian、初始化、residual scale 与优化协议；实验结果只支持被测模型、数据、预算和指标。

## 一、表达能力来自四种结构的组合

标准 block 的功能可拆成：

1. attention：跨 token 的内容依赖混合；
2. FFN：逐 token 的非线性通道变换；
3. residual：把多层增量组合并提供恒等路径；
4. position/structure：打破或利用 token 置换对称。

只有 attention 而没有非线性 FFN，不等于完整 Transformer；只有 FFN 而没有 token mixing，各位置不能交换信息；没有 position 时，模型对 token 排列保留置换等变结构，不能一般地区分顺序。

## 二、通用逼近定理到底说了什么

[[S-2020-Yun-Transformer-Universal-Approximation]] 在指定设置下证明 Transformer 能逼近某类连续的序列到序列函数；加入位置编码后可处理不要求 permutation equivariance 的函数类。典型结论形式是：对紧定义域上的目标函数 $f$ 与任意 $\varepsilon>0$，存在某个 Transformer $g_\theta$ 使适当距离满足

$$
d(f,g_\theta)<\varepsilon.
$$

必须保留：输入域、连续性/可测性、距离范数、位置编码、深度/宽度与构造假设。这是**存在性** `T`，不意味着 SGD 能找到该参数，不给样本复杂度，也不保证有限预算的推理效率。

## 三、表达存在不等于可学习

一个模型类即使包含目标函数，训练仍可能受：

- 病态 Jacobian 与梯度尺度；
- 数据不足或目标不识别；
- 优化落入不同表示；
- 有限精度与长序列成本；
- 分布偏移与错误评价指标。

所以从 universal approximation 直接跳到“模型理解任何任务”属于量词偷换：`存在参数` 被误换成 `给定算法、数据和资源能找到且泛化`。

## 四、Pure Attention 的秩坍塌边界

[[S-2021-Dong-Pure-Attention-RankCollapse]] 分析没有 skip connection 与 MLP 的 pure self-attention，在特定假设下 token representations 可能随深度快速趋向 rank-one/一致状态。它揭示了反复 averaging-like mixing 的潜在退化机制。

但不能把结论直接复制到有 residual、FFN、normalization、position、multi-head 与训练参数更新的完整 Transformer。正确用法是：

1. 写出论文所分析的层映射；
2. 对照目标模型是否满足假设；
3. 实测 centered token matrix 的奇异值、有效秩与任务指标；
4. 把“不满足假设”列为外推边界。

## 五、Pre/Post-Norm 的精确 Jacobian

抽象一层分支 $F$ 与 normalization $N$：

$$
y_{pre}=x+F(N(x)),
\qquad
J_{pre}=I+J_FJ_N,
$$

$$
y_{post}=N(x+F(x)),
\qquad
J_{post}=J_N(I+J_F).
$$

这是链式法则 `I`。它说明 Pre-Norm 的恒等项没有经过 $J_N$，但不单独证明任意深度、任意参数下梯度都有界。[[S-2020-Xiong-Transformer-LayerNorm]] 的初始化梯度结论属于带 mean-field/宽度/随机初始化条件的 `T`。

## 六、Residual Scale：状态与参数两条通道

对

$$
x_{l+1}=x_l+\varepsilon_lF_l(x_l;\theta_l),
$$

有

$$
\frac{\partial x_{l+1}}{\partial x_l}=I+\varepsilon_lJ_{F_l},
\qquad
\frac{\partial x_{l+1}}{\partial\theta_l}
=\varepsilon_l\frac{\partial F_l}{\partial\theta_l}.
$$

[[S-2022-Su-8994-Why-Residual]] 强调 residual coefficient 同时改变状态传播与参数更新。若只要求最坏情形增量绝对和受控，常会看到 $1/L$ 尺度；若近似独立零均值增量按方差累计，则会看到 $1/\sqrt L$ 尺度。两者的随机性与相关性假设不同，不能混写成唯一法则。

## 七、Pre-Norm 的精确展开与“深度稀释”假说

Pre-Norm residual stack 可精确展开为

$$
x_L=x_0+\sum_{l=0}^{L-1}F_l(N(x_l)).
$$

展开是 `I`。[[S-2022-Su-9009-PreNorm-PostNorm]] 进一步讨论：如果 residual stream 尺度增长，而新分支增量相对越来越小，相邻深层可能只产生微弱区别，出现“等效较浅而较宽”的深度稀释。这是有条件机制 `H/E`，需要逐层增量、representation similarity、ablation 与最终指标共同支持。

因此“Pre-Norm 更易训练”与“同预算最终效果更好”不是同一命题。

## 八、DeepNorm 与千层证据

[[S-2022-Wang-DeepNet]] 以深度相关 residual scaling 和初始化控制模型更新，给出相应理论分析与深层实验。[[S-2021-Su-8978-千层Transformer困难]] 从增量/更新爆炸角度给出中文推导接口。

证据要拆开：

- update bound：在论文假设内为 `T`；
- 千层模型被成功训练：在特定数据、架构和优化协议下为 `E`；
- 任意任务都应加到千层：不成立；
- 具体 $\alpha,\beta$ 系数：依 encoder/decoder 配置，不能跨架构照抄。

## 九、2026 Attention Residuals：前沿而非默认

[[S-2026-Chen-Attention-Residuals]] 让当前层沿**深度轴**对先前表示做内容依赖加权；Block AttnRes 用块级表示缓解历史激活和 pipeline communication。[[S-2026-Su-11664-Attention-Residuals]] 记录这一设计从 residual scaling 到 depth routing 的思路演化。

它提供新的实验与机制假说，但当前应标为版本化 `E/H`：

- 结果依论文版本、模型规模、数据与训练协议；
- depth attention 增加历史表示/摘要的 memory 与通信合同；
- depth weights 不自动是因果解释；
- 不能据此把标准 residual 宣告“过时”。

## 十、经验成功的正确表述

BERT、GPT、T5、ViT 等工作表明不同 Transformer 家族在相应数据和任务协议下取得强结果，属于 `E`。要支持新的系统声明，至少建立 evidence card：

| 字段 | 必须记录 |
|---|---|
| Claim | 训练稳定、最终 loss、迁移、鲁棒、效率中的哪一个 |
| Model | 接线、norm、position、FFN、参数量、context |
| Data/objective | 数据来源、token 数、污染、目标与 loss region |
| Optimization | 初始化、学习率、warm-up、optimizer、precision |
| Comparator | 同参数/同 FLOPs/同数据/同 latency 哪种公平性 |
| Metrics | 均值、方差、失败率、显存、吞吐、下游指标 |
| Boundary | 未覆盖的规模、模态、分布与硬件 |

单个最佳分数不能同时证明机制、泛化和系统效率。

## 十一、失败诊断的五层顺序

1. **接线**：mask、Q/K/V 来源、residual 与 norm 是否正确；
2. **数值**：softmax、dtype、溢出、padding、cache position；
3. **优化**：梯度/更新范数、warm-up、初始化、loss scale；
4. **表示**：token rank、层间增量、attention entropy、FFN activation；
5. **任务证据**：数据泄漏、baseline、公平预算、分布偏移。

先排 implementation contract，再谈宏大理论，避免把一个 off-by-one causal mask 错误解释成“模型表达不足”。

## 十二、证据等级 I/T/E/H/O

- `I`（Identity）：由定义/代数精确推出，如 Pre-Norm 展开；
- `T`（Theorem）：保留明确假设与量词的定理；
- `E`（Experiment）：特定协议下可复现结果；
- `H`（Hypothesis）：机制解释或外推猜想；
- `O`（Observation）：教学/调试观察，尚未形成受控证据。

一条陈述可包含多个层级，但必须逐句标记。例如“Pre-Norm 有恒等 Jacobian 项 `I`，所以任意深度都稳定 `未推出`”。

## 十三、图：从表达定理到系统证据

先看图回答：为什么 universal approximation 与训练稳定之间没有直接箭头？Pre-Norm 展开、DeepNorm 千层实验和 Attention Residuals 应分别放在哪个证据层？

![[00-知识库管理/_assets/figures/architecture/fig-transformer-stability-evidence-v1.svg|900]]

> [!figure] 图 40.5-08　Transformer 表达、优化稳定与经验结果的证据边界
> 图将结构机制、精确恒等式、条件定理、受控实验与前沿假说分层。来源：依据 Yun、Dong、Xiong、DeepNet 及 Science Space 相关文章独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_transformer_v1.py]] 生成。

**怎样读图**：沿每条箭头询问“多了什么假设”。从接线到 Jacobian 可精确推导；从 Jacobian 到深层训练要加初始化/相关性/优化条件；从训练到泛化和部署还要加数据与系统证据。箭头越往右，不能省略的条件越多。

**图没有证明什么**：它不裁决某种 norm/residual 永远最佳，也不证明通用逼近模型必然可学习、可泛化或高效；AttnRes 仍是随论文版本更新的前沿证据。

## 十四、常见错误与掌握标准

常见错误：从存在性定理推出 SGD 成功；把 pure-attention 定理直接套到完整模型；由一层 Jacobian 推任意深度稳定；混淆 $1/L$ 与 $1/\sqrt L$ 假设；将千层可训练写成千层必优；把新前沿实验写成普遍定理；用 attention/depth weights 直接作因果解释。

> [!summary]
> Transformer 的表达由 token mixing、channel nonlinearity、residual composition 与 position 共同提供；表达存在、优化稳定、有限样本泛化和系统效率没有逻辑等价。每个结论都应落在 I/T/E/H/O，并保留其假设、协议和失败边界。

能复述定理量词（A/B）、推导 Jacobian 与 residual 尺度假设（C）、构造错误外推反例（D），并为一个架构稳定性声明写完整 evidence card 与复现实验（E）。

## 十五、练习与独立详解

- [[习题 - Transformer 表达、稳定性与证据边界]]
- [[解答 - Transformer 表达、稳定性与证据边界]]

## 参考来源

- [[S-2020-Yun-Transformer-Universal-Approximation]]
- [[S-2021-Dong-Pure-Attention-RankCollapse]]
- [[S-2020-Xiong-Transformer-LayerNorm]]
- [[S-2022-Wang-DeepNet]]
- [[S-2021-Su-8978-千层Transformer困难]]
- [[S-2022-Su-8994-Why-Residual]]
- [[S-2022-Su-9009-PreNorm-PostNorm]]
- [[S-2026-Chen-Attention-Residuals]]
- [[S-2026-Su-11664-Attention-Residuals]]
