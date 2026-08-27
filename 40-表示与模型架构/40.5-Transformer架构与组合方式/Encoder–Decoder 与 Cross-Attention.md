---
type: concept
status: draft
area: [architecture, transformer, encoder-decoder, cross-attention]
aliases: [Seq2Seq Transformer, Encoder-Decoder Transformer, Source-Target Attention]
node_id: ARCH-36
prerequisites: ["[[Transformer Encoder 与双向表示]]", "[[Transformer Decoder 与自回归因果结构]]", "[[Self-Attention、Cross-Attention 与张量形状]]"]
related: ["[[Transformer 架构与组合方式 MOC]]", "[[Decoder-Only、Prefix 与架构家族比较]]", "[[Transformer 形状、参数量与 FLOPs 总账]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2015-Bahdanau-Attention]]", "[[S-2020-Raffel-T5]]"]
exercises: ["[[习题 - Encoder–Decoder 与 Cross-Attention]]"]
solutions: ["[[解答 - Encoder–Decoder 与 Cross-Attention]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-transformer-encoder-decoder-flow-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Encoder–Decoder 与 Cross-Attention

> [!abstract] 本节主问题
> Encoder–decoder Transformer 显式维护两条序列轴：source 先由双向 encoder 变成 memory，target decoder 在因果 self-attention 后以 target states 作 queries、source memory 作 keys/values。Source padding、target causal 与 target loss 是三个不同合同。

## 一、整体函数分解

给 source $s_{1:T_s}$ 与 target $y_{1:T_t}$：

$$
H_e=\operatorname{Encoder}(s)\in\mathbb R^{B\times T_s\times d},
$$

$$
p(y\mid s)=\prod_{t=1}^{T_t}p(y_t\mid y_{<t},H_e).
$$

Encoder memory 在 target 生成过程中固定；decoder state 随 target prefix 增长。

## 二、Decoder Layer 的三种子层

典型 decoder layer 按顺序包含：

1. causal target self-attention；
2. encoder–decoder cross-attention；
3. position-wise FFN。

以 Pre-LN 简写：

$$
U=Y+\operatorname{SelfAttn}(N_1(Y);M_{causal}),
$$

$$
V=U+\operatorname{CrossAttn}(N_2(U),H_e,H_e;M_{src}),
$$

$$
Y^+=V+\operatorname{FFN}(N_3(V)).
$$

每个子层通常有自己的 norm/residual；不能把 self/cross 两次 attention 合为一张权重。

## 三、Cross-Attention Shape

对每层/每头：

$$
Q=YW_Q\in\mathbb R^{B\times T_t\times d_k},
$$

$$
K=H_eW_K\in\mathbb R^{B\times T_s\times d_k},\quad
V=H_eW_V\in\mathbb R^{B\times T_s\times d_v}.
$$

Score/weight 为 $(B,h,T_t,T_s)$，输出回到 target 轴 $(B,T_t,d)$。Source 长度被加权求和，不能误把 output 写成 $T_s$ 行。

## 四、三套 Mask

| Mask | 作用对象 | 语义 |
|---|---|---|
| source padding | cross-attention K/V columns | 不读 source padding |
| target causal | decoder self-attention pairs | 不读 target future |
| target padding/loss | decoder rows/targets | 忽略无效 target 输出 |

Cross-attention 通常不对 source 施加 target-style 三角 mask；所有 target positions 都可读完整 source。若 source 本身是 streaming/causal memory，则是另一架构，必须另定义 relation。

## 五、训练与推理复用

训练时 source encoder 一次前向，target teacher forcing 全部 rows 并行。生成时：

- encoder memory 只算一次；
- 每个 decoder layer 的 cross-attention K/V 可由 $H_e$ 预投影并缓存；
- target self-attention K/V 随步骤增长；
- 每步产生一个 target query row。

因此 source cache 生命周期贯穿整条 target 生成，而 target cache逐步追加。Beam search 复制/重排 target cache，但可共享或索引同一 source memory。

## 六、为何显式分开 Source 与 Target

优点：

- source 可双向编码；
- target 保持严格 causal；
- memory 可多层重复读取；
- source/target tokenizer、模态与长度可不同；
- cross-attention heatmap 有明确两轴。

代价：两套 stacks、每 decoder layer 额外 Q/K/V/O 投影和 $T_tT_s$ pairwise work；serving 也需维护 source memory。

## 七、T5 的统一 Text-to-Text

[[S-2020-Raffel-T5]] 将分类、问答、翻译等任务都编码成输入文本到输出文本。架构上它是 encoder–decoder；接口统一使任务共享生成 head。

但“都写成文本”不消除：评价指标差异、输出长度、标签空间、解码错误、任务数据量与 loss weighting。T5 还采用具体 relative position、pre-norm 风格与 span corruption，不能将这些选择误作所有 encoder–decoder 的定义。

## 八、从 Bahdanau 到 Transformer Cross-Attention

[[S-2015-Bahdanau-Attention]] 已让每个 decoder step 动态读取 encoder states；Transformer 将 recurrence query 换成一列 target states，并用 multi-head scaled dot product 统一并行训练。历史联系是“target query 读取 source memory”，不是 score 形式完全相同。

## 九、常见任务与失败

- 翻译/摘要：source coverage、重复与长度偏置；
- 语音识别：frame memory 长、alignment 与 latency；
- 图文生成：跨模态 tokenization/scale；
- retrieval-conditioned generation：source provenance/leakage；
- structured prediction：target serialization 影响误差传播。

Cross-attention 可见 source 不保证忠实使用；还需 source ablation、counterfactual replacement 与引用验证。

## 十、图：Source–Target 双轴

先看图回答：decoder cross-attention 的 Q 来自哪里？为什么 source memory 可缓存一次，而 target self K/V 必须随生成增长？

![[00-知识库管理/_assets/figures/architecture/fig-transformer-encoder-decoder-flow-v1.svg|900]]

> [!figure] 图 40.5-04　Encoder–decoder 的 source memory、target decoder 与两条长度轴
> 左栏编码 source，中栏逐层展示 target self/cross/FFN，右栏登记 $T_s,T_t$。来源：依据原始 Transformer 与 T5 独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_transformer_v1.py]] 生成。

**怎样读图**：沿蓝线看 H_e 同时成为每层 cross K/V；沿 target 竖线看每层输出仍是 $T_t$ 行。再分别标注 source padding、target causal 和 target loss mask。

**图没有证明什么**：它没有证明 encoder–decoder 对所有任务优于 decoder-only，也没有证明 cross weights 是 source attribution。

## 十一、常见错误与掌握标准

常见错误：将 source/target 拼成同一 mask 却仍称标准 encoder–decoder；cross Q/K 轴颠倒；给 cross-attention 错加 target causal triangle；漏 decoder 第三个 norm/residual；每步重算 encoder；把 text-to-text 接口统一当任务等价。

> [!summary]
> Encoder–decoder 用双向 source memory 条件化 causal target；decoder 每层有 self/cross/FFN；score 为 $T_t\times T_s$；三套 mask 和两类 cache 必须分离。

能重建三子层与 shapes（A/B）、推导参数/计算及缓存复用（C）、构造 mask/来源错位反例（D），并为翻译或多模态系统写 source–target evidence card（E）。

## 十二、练习与独立详解

- [[习题 - Encoder–Decoder 与 Cross-Attention]]
- [[解答 - Encoder–Decoder 与 Cross-Attention]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2015-Bahdanau-Attention]]
- [[S-2020-Raffel-T5]]
