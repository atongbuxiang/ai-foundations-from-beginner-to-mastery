---
type: concept
status: draft
area: [architecture, transformer, decoder-only, prefix-lm]
aliases: [Transformer 架构家族, Prefix LM, Decoder-only Transformer]
node_id: ARCH-37
prerequisites: ["[[Transformer Encoder 与双向表示]]", "[[Transformer Decoder 与自回归因果结构]]", "[[Encoder–Decoder 与 Cross-Attention]]", "[[Attention Mask、因果性与可见性合同]]"]
related: ["[[Transformer 架构与组合方式 MOC]]", "[[Transformer 形状、参数量与 FLOPs 总账]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]"]
sources: ["[[S-2019-Devlin-BERT]]", "[[S-2018-Radford-GPT]]", "[[S-2020-Raffel-T5]]", "[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2023-Su-9529-DecoderOnly低秩猜想]]"]
exercises: ["[[习题 - Decoder-Only、Prefix 与架构家族比较]]"]
solutions: ["[[解答 - Decoder-Only、Prefix 与架构家族比较]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-transformer-family-contracts-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Decoder-Only、Prefix 与架构家族比较

> [!abstract] 本节主问题
> “Encoder-only、encoder–decoder、decoder-only”不是三个品牌标签，而是三组可检查的计算合同：哪些 token 对可见、Q/K/V 分别来自哪条序列、在哪些位置计算什么目标、输出如何被读取。Prefix LM 又说明“单栈”不必等于“全序列因果”。

## 一、先建立四栏分类法

比较任意 Transformer，先回答四个问题：

1. **Relation**：第 $i$ 个 query 可读取哪些 key positions？
2. **Source**：Q、K、V 来自同一 residual stream，还是 target 读取 source memory？
3. **Objective**：哪些位置参与 loss，预测的是被遮盖 token、下一个 token 还是另一条序列？
4. **Outlet**：使用逐 token 表示、pooling 表示，还是逐步生成分布？

架构接线与预训练目标有关但不等同。同一个双向 encoder 可配 masked-token、对比或监督分类目标；同一个 causal decoder 也可学习文本、代码或多模态序列。

## 二、Encoder-Only：全双向读取，出口可变

对非 padding 的 $T$ 个 token，典型 encoder relation 为

$$
R_{ij}=1,\qquad 1\le i,j\le T.
$$

每层 self-attention 都可让当前位置同时读取左右上下文。出口可以是：

- 每个 token 的 contextual representation，用于标注、检索或 span task；
- 特殊汇聚 token；
- mean/max/attention pooling 后的序列表示。

[[S-2019-Devlin-BERT]] 是代表性实例，但 masked language modeling、`[CLS]` 与 next-sentence objective 不是“encoder-only”的逻辑定义。

## 三、Encoder–Decoder：两条序列、两类读取

Encoder 内部是 source-to-source 双向 relation；decoder 内部是 target causal relation；cross-attention 则是 target-to-source relation：

$$
R^{enc}_{ij}=1,
\qquad
R^{self}_{ij}=\mathbf 1[j\le i],
\qquad
R^{cross}_{ij}=1.
$$

这里三个 $i,j$ 分属不同轴，不能把最后一式错画成 target 三角形。[[S-2020-Raffel-T5]] 代表 text-to-text 接口；接口统一不等于 source/target 接线消失。

## 四、Decoder-Only：把条件与答案序列化

Decoder-only 使用一条 causal residual stream：

$$
p(x_{1:T})=\prod_{t=1}^{T}p(x_t\mid x_{<t}).
$$

若任务有输入 $s$ 与输出 $y$，常把它们序列化为

$$
[\text{BOS},s,\text{SEP},y],
$$

然后只在 $y$ 对应位置计算监督 loss。于是**可见性区域**与**loss 区域**仍是两个对象：prompt token 可作为 keys/values 被读取，却不必作为监督 targets。

这类单栈设计共享参数、接口和 cache 逻辑，但条件与答案争用同一 context window；prompt 被每层反复保存在 causal history 中，也不同于每层显式读取独立 source memory。

## 五、Prefix LM：单栈中的分块可见性

设前 $P$ 个位置为 prefix，后 $S$ 个位置为 generated suffix。一个典型 prefix-LM relation 是

$$
R_{ij}=
\begin{cases}
1,&i\le P,\ j\le P,\\
1,&i>P,\ j\le i,\\
0,&\text{otherwise}.
\end{cases}
$$

也就是说：prefix 内部双向；suffix 可读全部 prefix 和既往 suffix；prefix 不读 suffix；suffix 不读未来 suffix。它可写成分块矩阵

$$
R=
\begin{bmatrix}
\mathbf 1_{P\times P}&0\\
\mathbf 1_{S\times P}&L_S
\end{bmatrix},
$$

其中 $L_S$ 是含对角线的下三角矩阵。训练时是否只在 suffix 上算 loss，必须另外声明。

## 六、拼接式条件化不等于显式 Cross-Attention

把 `[source; target]` 拼进 decoder 与使用 encoder–decoder 都允许 target 读取 source，但它们并非同一计算图：

| 维度 | 拼接/单栈 | Encoder–decoder |
|---|---|---|
| source 表示 | causal 或 prefix relation 下逐层演化 | 先由独立 encoder 双向编码 |
| 参数 | source/target 共享同一 stack | encoder/decoder 可分配不同层数与参数 |
| 读取时机 | source token 作为同层历史 K/V | 每个 decoder layer 读取 encoder 最终 memory |
| cache | 一条自回归 K/V history | target cache + 可复用 source cross K/V |
| 长度预算 | source 与 target 共用 context | 两条长度轴，仍占 memory/compute |

只有在额外参数约束和计算重排下才能谈某种模拟关系，不能从“都能看到 source”推出功能等价。

## 七、系统账与任务账

- **表示型任务**：encoder-only 可一次得到所有 token 的双向表示；decoder-only 最后 token 汇聚会受顺序与长度影响。
- **条件生成**：encoder–decoder 能把 source 编码一次并在每层重读；decoder-only 的统一接口与共享 stack 更简单。
- **在线生成**：两者都可缓存；cache 形状、source 生命周期和并行方式不同。
- **参数预算**：同样总参数下，encoder–decoder 要在两套 stack 间分配；不能按相同层数比较后声称“同规模”。
- **数据与目标**：预训练 token、目标密度、噪声和任务混合常比架构名更强地影响结果。

所以公平比较应固定或报告总参数、训练 FLOPs、训练 token、context 长度、tokenizer、数据、objective、解码规则和 latency target。

## 八、科学空间的低秩猜想：事实与解释分开

[[S-2023-Su-9529-DecoderOnly低秩猜想]] 指出：若 causal softmax attention 的对角权重有限且严格为正，则 attention matrix 是正对角下三角矩阵，因而

$$
\det A=\prod_{i=1}^{T}A_{ii}>0,
\qquad \operatorname{rank}(A)=T.
$$

这是可核验的线性代数事实 `I`。但三点不能随之推出：

1. 满代数秩不等于条件良好，也不等于有效秩高；
2. 单头某层满秩不等于整网表达更强或更易优化；
3. “该性质解释 decoder-only 的总体流行/优越”仍是机制假说 `H`。

架构流行还与 next-token 目标的数据密度、统一任务接口、scaling、parameter allocation 和 serving 工程有关。单一秩事实不能替代受控消融。

## 九、图：把架构还原成 Relation Contract

先看图回答：Prefix LM 的左上块与右下块分别是什么 relation？为何 decoder-only 与 encoder–decoder 即使都能条件生成，也不能说计算图相同？

![[00-知识库管理/_assets/figures/architecture/fig-transformer-family-contracts-v1.svg|900]]

> [!figure] 图 40.5-05　Encoder-only、encoder–decoder、decoder-only 与 prefix-LM 的可见性合同
> 图中按 attention relation、Q/K/V 来源、loss region 与读出方式统一比较。来源：依据 BERT、GPT、T5 与 causal/prefix mask 定义独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_transformer_v1.py]] 生成。

**怎样读图**：先读每张小矩阵的 query 行与 key 列，再沿数据流确认 source/target 是同一 stack 还是独立 memory；最后单独圈出算 loss 的 positions。三次检查得到 relation、architecture 和 objective 三份合同。

**图没有证明什么**：图不证明某一家族在所有任务上占优，也不证明 causal attention 的满秩性质是 decoder-only 成功的唯一原因。

## 十、常见错误与掌握标准

常见错误：把 BERT objective 当 encoder 定义；把单栈等同全 causal；将 attention mask 与 loss mask 合一；把 prompt 当不会产生计算成本；把拼接式条件化称为“就是 cross-attention”；只比层数不比总参数；由因果矩阵满秩推出模型普遍优越。

> [!summary]
> 架构家族应由 relation、Q/K/V 来源、objective 与 outlet 联合定义。Prefix LM 证明单栈可有分块 relation；拼接与 cross-attention 有不同的参数、层间读取和 cache 合同；低秩观点中，三角满秩是事实，架构优势是待检验解释。

能重画四类 mask（A/B）、推导 prefix block 与 cache 差异（C）、构造“可见性相同但计算图不同”的反例（D），并完成固定预算的架构比较表（E）。

## 十一、练习与独立详解

- [[习题 - Decoder-Only、Prefix 与架构家族比较]]
- [[解答 - Decoder-Only、Prefix 与架构家族比较]]

## 参考来源

- [[S-2019-Devlin-BERT]]
- [[S-2018-Radford-GPT]]
- [[S-2020-Raffel-T5]]
- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2023-Su-9529-DecoderOnly低秩猜想]]
