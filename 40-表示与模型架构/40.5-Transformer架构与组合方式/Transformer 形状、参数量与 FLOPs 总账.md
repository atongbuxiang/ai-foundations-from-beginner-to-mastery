---
type: concept
status: draft
area: [architecture, transformer, shapes, parameters, compute]
aliases: [Transformer Cost Ledger, Transformer 参数量, Transformer FLOPs]
node_id: ARCH-39
prerequisites: ["[[Multi-Head Attention、投影子空间与参数量]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[Encoder–Decoder 与 Cross-Attention]]"]
related: ["[[Transformer 架构与组合方式 MOC]]", "[[Vision Transformer、Patch Token 与二维结构]]", "[[Transformer Decoder 与自回归因果结构]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
exercises: ["[[习题 - Transformer 形状、参数量与 FLOPs 总账]]"]
solutions: ["[[解答 - Transformer 形状、参数量与 FLOPs 总账]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-transformer-cost-ledger-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Transformer 形状、参数量与 FLOPs 总账

> [!abstract] 本节主问题
> “Attention 是 $O(T^2)$”只写出 pairwise 项，不能替代真实成本账。一个合格总账必须先声明 batch、长度、宽度、头数、FFN 宽度与层数，再分别计算参数、乘加工作、激活/缓存内存和训练/推理阶段；真实延迟还受 kernel、带宽与硬件利用率影响。

## 一、统一符号与计量单位

本节使用：

$$
B: \text{batch},\quad T: \text{sequence length},\quad d: \text{model width},
$$

$$
h: \text{heads},\quad d_h=d/h,\quad d_{ff}: \text{FFN width},\quad L: \text{layers},\quad V: \text{vocabulary size}.
$$

默认标准 dense MHA 中 $h d_h=d$，忽略 bias 与 norm 的低阶项。这里把一次乘加记为一个 **MAC**；若平台把乘法和加法分别算一次 floating-point operation，则常近似 $1\text{ MAC}=2\text{ FLOPs}$。报告时必须写明口径。

## 二、标准 Multi-Head Attention 参数量

四个主投影

$$
W_Q,W_K,W_V,W_O\in\mathbb R^{d\times d}
$$

给出

$$
P_{MHA}=4d^2
$$

个权重。头数 $h$ 改变 reshape 与每头宽度，并不在固定总宽 $d$ 下把参数量乘 $h$。若使用 grouped/multi-query attention，则 K/V 投影 shape 改变，必须另算。

## 三、FFN 与门控 FFN 参数量

普通两矩阵 FFN：

$$
d\to d_{ff}\to d,
\qquad P_{FFN}=2dd_{ff}.
$$

若使用三矩阵门控 FFN（如常见 SwiGLU 形式）：

$$
P_{gated}=3dd_{ff}.
$$

若要在参数预算上与普通 FFN 接近，门控分支的 $d_{ff}$ 通常不能机械沿用；应由目标参数量反解。

## 四、每层与整网参数总账

标准 encoder 或 decoder-only block 有一组 self-MHA 和一组 FFN：

$$
P_{block}\approx 4d^2+2dd_{ff}.
$$

标准 encoder–decoder 的 encoder layer 同上；decoder layer 多一组 cross-attention：

$$
P_{dec-layer}\approx 8d^2+2dd_{ff}.
$$

因此

$$
P_{enc-dec}\approx L_e(4d^2+2dd_{ff})+L_d(8d^2+2dd_{ff})+P_{embed/head/norm}.
$$

词嵌入约 $Vd$；输出 softmax head 若不与输入 embedding tying，再加约 $Vd$。Position embedding、norm scale/bias 和所有 linear biases 要在精确实现账中补回。

## 五、Self-Attention 前向 MACs

对 $X\in\mathbb R^{B\times T\times d}$：

1. Q/K/V/O 投影合计约
   $$4BTd^2;$$
2. $QK^\top$ 与 $AV$ 两次 pairwise contraction 合计
   $$2BhT^2d_h=2BT^2d;$$
3. 普通 FFN 两次矩阵乘合计
   $$2BTdd_{ff}.$$

一个标准 block 的主要 forward MACs 为

$$
C_{block}\approx4BTd^2+2BT^2d+2BTdd_{ff}.
$$

Softmax、norm、activation、bias、dropout 和 data movement 没有写入；它们在小矩阵或 memory-bound regime 可能并不可以忽略。

## 六、二次项何时主导

Attention pair 项与四投影项比较：

$$
2BT^2d \gtrsim 4BTd^2
\iff T\gtrsim2d.
$$

与普通 FFN 比较：

$$
2BT^2d\gtrsim2BTdd_{ff}
\iff T\gtrsim d_{ff}.
$$

所以在 $T\ll d$ 且 $d_{ff}\approx4d$ 时，linear projections/FFN 可能比 pairwise attention 占更多算术工作。`$O(T^2)$` 说的是长度渐近，不等于所有实际配置里它已经主导 wall-clock。

## 七、Cross-Attention 的双长度账

设 target 长 $T_t$、source 长 $T_s$。每层 cross-attention 的主要 MACs 约为

$$
BT_t d^2+2BT_s d^2+BT_t d^2+2BT_tT_s d,
$$

依次对应 Q、K/V、O 与 QK/AV。生成时 source K/V 可预投影一次并跨 steps 复用；因此逐 token decode 不应每步重算 $2BT_s d^2$。

但每个新 target query 仍要与 $T_s$ 个 source keys 做 pairwise work；source memory 也要常驻或被重新读取。

## 八、训练、Prefill 与 Decode 是三张不同账

### 训练

所有 $T$ 行并行；需保存反向传播所需激活。总训练 FLOPs 不能只取 forward 的固定倍数而不说明 checkpointing、optimizer 与 embedding head。

### Prefill

给定长 prompt，一次计算所有 prompt tokens；像一个 causal full-sequence forward，但只 materialize 合法下三角 relation。

### Decode

有 K/V cache 时，每层每步只产生一个 query，却读取长度 $t$ 的缓存。投影与 FFN 对新 token 约为 $O(d^2)$，attention pair 约为 $O(td)$；累计生成 $S$ tokens 仍含随长度增长的总读取。

没有 cache 则每一步重算整个 prefix，计算图与复杂度完全不同。

## 九、激活、Attention Matrix 与 KV Cache

若朴素实现 materialize attention scores/weights，单层规模约

$$
O(BhT^2).
$$

Flash-style exact attention 可通过分块重计算避免保存完整 $T\times T$ 矩阵，但不改变 dense all-pairs 的数学 relation，也不自动把算术量变成线性。

Decoder-only K/V cache 在 $L$ 层、batch $B$、缓存长 $T$、每层总 K/V 宽度 $d_{kv}$ 下约含

$$
2LBTd_{kv}
$$

个标量；字节数还要乘 dtype bytes，并计入 allocator、beam expansion 与量化元数据。

## 十、从数学账到硬件账

相同 FLOPs 可能有不同延迟，因为：

- 小 batch decode 常受 memory bandwidth 与 kernel launch 限制；
- tensor shape 是否对齐硬件 tile 会改变利用率；
- fused kernels 减少中间写回；
- sequence padding 浪费 work；
- communication、optimizer state 与 activation checkpointing 改变训练吞吐。

因此成本报告至少应给参数量、training/prefill/decode MAC/FLOP 口径、峰值显存、tokens/s、batch/length 分布与硬件软件版本。

## 十一、参数化尺度不等于成本尺度

[[S-2021-Su-8620-Transformer初始化参数化与标准化]] 讨论宽度、初始化与标准化怎样影响信号/梯度尺度。矩阵从 $d$ 扩到更大不仅增加 $d^2$ 参数和计算，也会改变合适的初始化、学习率与 residual scale。

“同样训练稳定”不等于“同样算力高效”；“同参数”也不等于“同训练 FLOPs”或“同推理延迟”。这几张账必须分开。

## 十二、图：一张完整成本账

先看图回答：在固定 $d$ 下增加 head 数为何不把标准 MHA 参数量乘 $h$？长序列 decode 中，哪个量随着 cache length 线性增长？

![[00-知识库管理/_assets/figures/architecture/fig-transformer-cost-ledger-v1.svg|900]]

> [!figure] 图 40.5-07　Transformer 参数、计算、激活与阶段成本总账
> 图按 shape、每层参数、训练/prefill/decode 和证据边界拆开。来源：依据标准 dense Transformer 张量收缩独立推导；由 [[00-知识库管理/_labs/code/plot_architecture_transformer_v1.py]] 生成。

**怎样读图**：每一项都先找到参与相乘的三维/四维 shape，再消掉被 contraction 的维度；随后标注它是参数、MAC、临时激活还是持久 cache。最后再选择训练、prefill 或 decode 阶段，不能把四类数相加成一个“复杂度”。

**图没有证明什么**：公式不预测特定硬件的 wall-clock，也不证明某个理论上少 FLOPs 的实现一定更快、更省能耗或更易训练。

## 十三、常见错误与掌握标准

常见错误：把 head 数重复乘入参数量；漏掉 O projection；门控 FFN 仍算两矩阵；MAC 与 FLOP 口径混用；只报 $T^2$ 不报 $d^2$；训练、prefill、decode 混成一张账；把 Flash 的显存改进说成 relation/算术都线性；用参数量替代 latency。

> [!summary]
> 标准 block 约有 $4d^2+2dd_{ff}$ 参数、forward 约有 $4BTd^2+2BT^2d+2BTdd_{ff}$ MACs。Encoder–decoder decoder layer 多一组 cross-attention；训练、prefill、decode、激活与 K/V cache 必须分别核算；wall-clock 还需硬件测量。

能逐项核对 shapes 与参数（A/B）、推导阶段复杂度和交叉点（C）、发现错误成本声明（D），并为真实模型写可复现成本卡（E）。

## 十四、练习与独立详解

- [[习题 - Transformer 形状、参数量与 FLOPs 总账]]
- [[解答 - Transformer 形状、参数量与 FLOPs 总账]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2021-Su-8620-Transformer初始化参数化与标准化]]
