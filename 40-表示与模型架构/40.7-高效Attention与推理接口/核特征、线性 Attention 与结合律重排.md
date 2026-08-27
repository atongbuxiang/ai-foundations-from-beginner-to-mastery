---
type: concept
status: draft
area: [architecture, efficient-attention, kernel, linear-attention]
aliases: [Kernelized Attention, Linear Attention, Associative Attention]
node_id: ARCH-52
prerequisites: ["[[正定核、RKHS 与表示定理]]", "[[Attention 的几何、核与概率视角]]", "[[状态空间的递推—卷积对偶与并行扫描]]"]
related: ["[[高效 Attention 与推理接口 MOC]]", "[[Performer、随机特征与近似误差]]", "[[选择性状态空间、Mamba 与证据边界]]", "[[局部、分块与稀疏 Attention]]"]
sources: ["[[S-2020-Katharopoulos-Linear-Transformer]]", "[[S-2020-Su-7546-线性Attention]]", "[[S-2021-Su-8338-Performer到线性Attention]]", "[[S-2021-Su-8601-无限维线性Attention与核特征]]", "[[S-2021-Su-8610-线性Transformer反例]]", "[[S-2025-Su-11033-线性注意力简史]]", "[[S-2025-Su-11320-线性Attention短卷积]]"]
exercises: ["[[习题 - 核特征、线性 Attention 与结合律重排]]"]
solutions: ["[[解答 - 核特征、线性 Attention 与结合律重排]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-kernel-linear-attention-state-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# 核特征、线性 Attention 与结合律重排

> [!abstract] 核心问题
> 线性 Attention 的关键不是“删掉 softmax”五个字，而是相似度能否写成有限维特征内积。只有这时，分子和分母才可用矩阵结合律先聚合 K/V；causal 版本进一步成为固定维 recurrent state。

## 一、从一般归一化 Attention 开始

写成

$$
o_i=\frac{\sum_{j\in\mathcal N(i)}\kappa(q_i,k_j)v_j}
{\sum_{j\in\mathcal N(i)}\kappa(q_i,k_j)}.
$$

Softmax attention 对应

$$
\kappa(q,k)=\exp(q^\top k/\sqrt{d_h}).
$$

若存在 feature map $\phi:\mathbb R^{d_h}\to\mathbb R^r$，使

$$
\kappa(q,k)=\phi(q)^\top\phi(k),
$$

就称相似度可有限维分解。若 $\phi$ 分量非负，分母较容易保持正值，但仍要检查全零/下溢。

## 二、结合律推导

Full bidirectional attention 中，所有 query 使用同一组 keys。定义

$$
S=\sum_{j=1}^n\phi(k_j)v_j^\top\in\mathbb R^{r\times d_v},
\qquad
z=\sum_{j=1}^n\phi(k_j)\in\mathbb R^r.
$$

则

$$
o_i=\frac{\phi(q_i)^\top S}{\phi(q_i)^\top z}.
$$

矩阵形式相当于不先形成

$$
\Phi(Q)\Phi(K)^\top\in\mathbb R^{n\times n},
$$

而先算

$$
\Phi(K)^\top V\in\mathbb R^{r\times d_v}.
$$

主工作约 $O(nrd_v)$，状态约 $O(rd_v+r)$。只有 $r\ll n$ 时才可能优于 dense pairwise。

## 三、什么是恒等重排，什么是模型变化

若目标 kernel 本来就等于 $\phi(q)^\top\phi(k)$，结合律只是计算顺序变化，是 `I`。但常见 $\phi(x)=\operatorname{ELU}(x)+1$ 定义的是一个新 kernel，它并不等于 softmax exponential dot-product；此时线性 Attention 是新架构，不是 exact softmax implementation。

Performer 则使用随机 $\phi$ 近似 softmax kernel，属于第三种情况：目标函数相同，但有限 features 引入随机误差。三者必须分开：

| 类型 | 数学对象 | 误差 |
|---|---|---|
| 有限核精确重排 | 同一 kernel | 仅浮点/实现 |
| 选择新 feature map | 新 attention kernel | 架构偏差 |
| 随机特征近似 softmax | 目标为 softmax kernel | 随机近似与比值误差 |

## 四、Causal Attention 变成状态更新

对 causal $j\le t$：

$$
S_t=S_{t-1}+\phi(k_t)v_t^\top,
\qquad
z_t=z_{t-1}+\phi(k_t),
$$

$$
o_t=\frac{\phi(q_t)^\top S_t}{\phi(q_t)^\top z_t}.
$$

这就是一个输入依赖写入、query 依赖读取的 recurrent state。推理时无需保存全部历史 K/V，状态大小与 $t$ 无关。

但训练时若逐 token Python loop，会失去 Transformer 并行优势。实际需要 parallel scan、chunkwise recurrence 或专用 kernel；有些更新含衰减/门控后不再是简单可交换前缀和，需要更一般的 associative scan。

## 五、分母是语义，不是装饰

若删掉分母，输出尺度随可见 token 数增长。保留分母则需保证

$$
d_i=\phi(q_i)^\top z>0.
$$

当 $d_i$ 很小时，数值误差会被放大。常见实现加 $\varepsilon$，但这改变精确函数；必须记录 epsilon、dtype、归约和 mask。

此外，任意 mask $M_{ij}$ 会给

$$
\sum_jM_{ij}\phi(q_i)^\top\phi(k_j)v_j.
$$

若每个 query 的可见集合不同，不能总用一个全局 $S$。Causal mask 可用 prefix state；固定 local window 可用 rolling add/subtract；任意结构 mask 通常破坏简单线性化。

## 六、固定维状态的容量边界

$S_t\in\mathbb R^{r\times d_v}$ 把任意长历史压成固定维状态。不同历史可能映射到同一 $(S_t,z_t)$，之后任何 query 都无法区分它们。这是一种明确的信息瓶颈。

因此线性长度复杂度不是免费午餐：

- 增大 $r$ 提高容量但增加 $O(rd_v)$ 成本；
- 加衰减/门控改变记忆分配；
- 加 short convolution 补局部顺序；
- 混合少量 full/sparse attention 恢复精确检索通路。

这也连接 [[选择性状态空间、Mamba 与证据边界]]：两者都把历史写入状态，但状态更新、读取和归一化不同。

## 七、科学空间的推导主线

[[S-2020-Su-7546-线性Attention]] 从一般非负相似度和结合律切入，是理解分子/分母与 $Q(K^TV)$ 重排的良好入口。[[S-2021-Su-8338-Performer到线性Attention]] 进一步讨论 feature activation、稀疏性与 rank，但其中“最佳激活”等表述应理解为设计直觉/实验线索，而非跨任务定理。

[[S-2021-Su-8601-无限维线性Attention与核特征]] 把 softmax kernel 看作无限维 feature expansion，适合作为有限/无限 feature map 的数学桥。[[S-2025-Su-11033-线性注意力简史]] 展示方法从模仿 softmax 到发展独立 recurrent updates 的谱系；历史优先权仍逐篇回查原论文。

[[S-2025-Su-11320-线性Attention短卷积]] 提出 short conv 补充局部顺序/高分辨率关系的机制解释。它是有价值的 `H`，但“为什么需要”不能写成所有线性 attention 的必要定理，仍需 kernel-size/移除卷积/混合层消融。

## 八、正式图：结合律究竟改变了什么

这张图回答什么问题？为什么 full attention 的右结合、分母归一化与 causal recurrent state 是同一条代数链？

![[00-知识库管理/_assets/figures/architecture/fig-kernel-linear-attention-state-v1.svg|900]]

> [!figure] 图 1｜Kernel linear attention 的左结合、右结合与 causal state。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_efficient_attention_v1.py]] 生成；符号使用一般 feature dimension $r$，不绑定 ELU、exp 或特定论文实现。

**怎样读图**：A 展示先物化 $n\times n$ 相似矩阵的 dense 路径；B 先聚合 $S=\Phi(K)^TV$ 和 denominator state $z$，再逐 query 读取；C 把全局和替换为前缀递推，得到 causal fixed-size state。三栏共享同一 feature-factorization 前提。

**图没有证明什么**：图没有证明所选 $\phi$ 等于 softmax kernel，也没有证明固定维 state 保留所有历史信息；$O(nrd_v)$ 的算术式还不包含 feature computation、scan、normalization、kernel launch 和硬件常数，因此也不能直接推出 wall-clock 胜出。

## 九、数值稳定清单

- feature 值是否非负、有界，exp 是否溢出；
- $z$ 与 $S$ 的累加 dtype；
- 长序列和的舍入误差与 rescaling；
- denominator 最小值及 epsilon；
- causal scan/chunk 的 reduction order；
- dropout 应作用在哪里，能否保持 associative update；
- mixed precision 下 full/recurrent 两种实现是否近似等价。

## 十、公平比较

线性与 softmax attention 比较时，至少对齐 model parameters、head/feature dimension、训练 tokens、local conv、position、优化器和 kernel maturity。分别报告短/长序列、训练/prefill/decode、质量、state/cache bytes、latency、throughput 与 numerical failures。

## 十一、证据边界

- Feature factorization 后的结合律与 state recurrence：`I`；
- 某 kernel 的正定/feature representation：带条件的 `T`；
- 有限 $r$ 的模型质量和速度：`E`；
- “short conv 补局部性”“高维更易集中”：`H/E`；
- fixed-size state 能否完成某类 associative recall，需要任务特定理论/实验。

## 十二、学习出口

应能从一般 $\kappa$ 推导 $(S,z)$，写出 full 与 causal 两种算法、成本和分母条件；并能判断一个所谓 linear attention 是 exact kernel reordering、新 kernel，还是 softmax 的随机近似。
