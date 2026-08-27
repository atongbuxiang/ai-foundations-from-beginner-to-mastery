---
type: concept
status: draft
area: [architecture, transformer, decoder, autoregressive]
aliases: [Causal Transformer Decoder, Autoregressive Decoder, Teacher Forcing]
node_id: ARCH-35
prerequisites: ["[[Transformer Block、残差、归一化与 FFN]]", "[[Attention Mask、因果性与可见性合同]]", "[[序列因果性、隐藏状态与递推计算]]"]
related: ["[[Transformer 架构与组合方式 MOC]]", "[[Encoder–Decoder 与 Cross-Attention]]", "[[Decoder-Only、Prefix 与架构家族比较]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2018-Radford-GPT]]"]
exercises: ["[[习题 - Transformer Decoder 与自回归因果结构]]"]
solutions: ["[[解答 - Transformer Decoder 与自回归因果结构]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-transformer-decoder-causal-cache-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Transformer Decoder 与自回归因果结构

> [!abstract] 本节主问题
> 自回归 decoder 用 causal self-attention 表示 $p(x_t\mid x_{<t})$。训练时所有位置的 logits 可以在一个 masked tensor 中并行计算；生成时第 t 个 token 必须等前缀确定后才能产生。Shift、causal diagonal、loss index 与 KV cache 必须写成同一时间合同。

## 一、自回归分解

$$
p(x_{1:T})=\prod_{t=1}^{T}p(x_t\mid x_{<t}).
$$

模型输出 logits $z_t\in\mathbb R^V$，

$$
p_\theta(x_t\mid x_{<t})=\operatorname{softmax}(z_t)_{x_t}.
$$

训练负对数似然通常为

$$
\mathcal L=-\sum_{t\in\mathcal T_{loss}}\log p_\theta(x_t\mid x_{<t}),
$$

再按 token 或 sequence 归约。Padding、prompt-only 区域和 ignore index 改变 $\mathcal T_{loss}$，因此是 estimand 合同。

## 二、右移输入与 Teacher Forcing

若目标序列为

$$
(x_1,x_2,\ldots,x_T,\mathrm{EOS}),
$$

输入常为

$$
(\mathrm{BOS},x_1,\ldots,x_T).
$$

同一 index 的 input 预测 target。Teacher forcing 指训练时输入真实前缀而非模型生成前缀；它让 loss 可并行估计，但会产生 train/inference prefix distribution 差异。

最危险的 bug 是未 shift 却让 inclusive diagonal 可见：位置 t 直接看到要预测的 $x_t$。

## 三、因果 Self-Attention

对输入位置 i，允许 $j\le i$（在上述 shift 约定下）。每层仍能同时构造全部 $T\times T$ score，再 mask 未来项，所以**计算并行**不违反**统计因果分解**。

训练时第 i 行的计算不依赖未来 token values；不同 rows 可由 GPU 同时执行。生成时未知的未来 tokens 尚不存在，因此 token loop 仍是顺序依赖。

## 四、Decoder Layer 的两种语境

- 原始 encoder–decoder Transformer 的 decoder layer：causal self-attention + cross-attention + FFN；
- decoder-only Transformer 的 layer：causal self-attention + FFN，不含 encoder cross-attention。

两者都可称 decoder，必须写明是否有 external memory。ARCH-35 先讨论共同的 causal target stack，[[Encoder–Decoder 与 Cross-Attention]]再加入 source memory。

## 五、训练并行与生成串行

训练：给定完整右移输入，所有 $T$ 行一次前向，pairwise core 为 $O(T^2d)$。

Naive 生成：每增加 token 若重算全部前缀，累计成本浪费严重。增量生成对每层只计算新 query 及新 k/v，并保存历史 K/V：

$$
K_{1:t}=[K_{1:t-1};k_t],\qquad V_{1:t}=[V_{1:t-1};v_t].
$$

新 query 与 $t$ 个 cached keys 计算一个 score row。Cache 改变计算复用与内存，不应改变 exact logits；训练全序列与逐步 cached decoding 在 eval、相同 position/mask 下应数值一致。

## 六、Cache 生命周期与位置

每层每个序列都需缓存 K/V，典型 shape

$$
(B,h_{kv},t,d_h).
$$

需记录：batch reorder、beam duplication、sequence reset、position offset、sliding window、dtype/quantization、GQA/MQA heads。错误复用旧请求 cache 会形成严重跨样本泄漏。

KV cache 的精确内存与 MQA/GQA/MLA 放到高效推理卷；本节只建立语义不变量。

## 七、Prompt、Prefix 与 Loss Mask

在 instruction/chat 训练中，输入可包含 system/user/assistant 多段。所有前缀可见不表示所有 token 都计 loss。常见做法只在 assistant response 区域计 next-token loss。

需明确：

- 哪些 token 可被谁看见；
- 哪些 token 产生 target loss；
- segment boundary 是否 reset position/cache；
- packing 后不同样本是否完全隔离。

可见 mask 与 loss mask 是两张不同的表。

## 八、采样不是 Decoder 架构本身

Greedy、beam、top-k、top-p、temperature 决定怎样从 $p_\theta(\cdot\mid prefix)$ 选 token。它们不改变 decoder 前向分布定义，但改变生成轨迹、计算分支与评价。不能把 decoding heuristic 的失败全归因架构。

## 九、GPT 的历史接口

[[S-2018-Radford-GPT]] 以 causal Transformer decoder 做生成式预训练，再用任务感知输入变换与监督 fine-tuning。它说明 decoder-only backbone 可服务生成以外任务；但现代 LLM 的 normalization、position、tokenizer、数据、规模和 cache kernel 已显著演化，不能把 GPT-1 配置当当前默认。

## 十、最小验证套件

1. shift gold example；
2. future-pulse invariance；
3. full forward vs cached step logits；
4. padding/packing isolation；
5. cache reset and batch reorder；
6. position offset 长序列；
7. loss token count 与 ignore index；
8. eval dropout disabled。

## 十一、图：Shift、Mask 与 Cache

先看图回答：为什么训练可同时算六行，却不能在生成时同时决定六个未知 token？cache 保存的是哪些投影而不是最终 hidden states？

![[00-知识库管理/_assets/figures/architecture/fig-transformer-decoder-causal-cache-v1.svg|900]]

> [!figure] 图 40.5-03　自回归 decoder 的 teacher-forcing shift、causal mask 与 KV cache
> 左栏对齐输入/target，中栏区分训练并行与统计依赖，右栏展示增量步骤。来源：依据 Transformer decoder 与 GPT 接口独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_transformer_v1.py]] 生成。

**怎样读图**：先逐 index 检查左栏不能原位复制，再把中栏每一行看成一个条件分布，最后在右栏确认只新增一个 query row、历史 K/V 不重算。

**图没有证明什么**：它没有证明 cached kernel 无数值差异，也没有证明 teacher forcing 是所有生成误差的唯一原因。

## 十二、常见错误与掌握标准

常见错误：shift 与 diagonal 错一位；把训练并行说成看到未来；把 loss mask 当 attention mask；缓存 hidden states 却称 KV cache；batch/beam reorder 忘记同步 cache；用训练 teacher-forcing loss保证 free-running 质量；把采样算法当 decoder block。

> [!summary]
> Decoder 的核心是 next-token factorization、shifted input、causal relation 与目标区域；训练 rows 可并行，生成 tokens 串行；KV cache 只复用历史 projections，不改变 exact 语义。

能手算 shift/mask/loss（A/B）、证明训练不泄漏与 cached 等价条件（C）、构造 cache/packing 反例（D），并写完整 autoregressive serving contract（E）。

## 十三、练习与独立详解

- [[习题 - Transformer Decoder 与自回归因果结构]]
- [[解答 - Transformer Decoder 与自回归因果结构]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2018-Radford-GPT]]
