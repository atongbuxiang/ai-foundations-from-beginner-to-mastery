---
type: concept
status: draft
area: [architecture, efficient-attention, complexity, systems]
aliases: [Attention Cost Ledger, Attention 二次复杂度, Attention IO]
node_id: ARCH-49
prerequisites: ["[[Transformer 形状、参数量与 FLOPs 总账]]", "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[渐近记号、增长率与复杂度]]"]
related: ["[[高效 Attention 与推理接口 MOC]]", "[[FlashAttention、精确计算与 IO Awareness]]", "[[KV Cache、MHA、MQA 与 GQA]]", "[[核特征、线性 Attention 与结合律重排]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2022-Dao-FlashAttention]]", "[[S-2021-Su-8610-线性Transformer反例]]", "[[S-2020-Su-7546-线性Attention]]"]
exercises: ["[[习题 - Attention 的二次复杂度、内存与 IO 瓶颈]]"]
solutions: ["[[解答 - Attention 的二次复杂度、内存与 IO 瓶颈]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-phase-cost-ledger-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Attention 的二次复杂度、内存与 IO 瓶颈

> [!abstract] 核心问题
> “Attention 是 $O(n^2)$”只是一句不完整的缩写。完整问题是：哪个阶段、哪个张量、哪一种成本、在哪种硬件上成为瓶颈？本节建立统一账本，避免把 FLOPs、峰值显存、HBM 流量、KV cache 和 wall-clock 混成一个数字。

## 一、先固定符号与阶段

设：

- batch size 为 $B$；
- 序列长度为 $n$，decode 到当前步时历史长度为 $t$；
- residual width 为 $d$；
- query head 数为 $h_q$，单头维度 $d_h$，通常 $h_qd_h=d$；
- KV head 数为 $h_{kv}$；标准 MHA 中 $h_{kv}=h_q$；
- FFN 中间宽度为 $d_{ff}$；
- Transformer 层数为 $L$；
- 每个 cache 标量占 $s$ bytes。

必须区分三个阶段：

1. **训练**：所有 token 并行前向，还要保存或重算反向所需状态；
2. **Prefill**：一次处理完整 prompt，建立每层 KV cache；
3. **Decode**：每步只有新 query，但反复读取全部历史 K/V。

同一个模型在 prefill 可能 compute-bound，在 decode 却 memory-bandwidth-bound。

## 二、Dense Attention 的算术账本

令 $X\in\mathbb R^{B\times n\times d}$。忽略 bias，Q/K/V/O 四个投影的主要 MAC 数为

$$
3Bnd^2+Bnd^2=4Bnd^2.
$$

对所有 heads，$QK^\top$ 的 MAC 数为

$$
B h_q n^2d_h=B n^2d,
$$

$AV$ 再需要约 $Bn^2d$，所以 pairwise 主项为

$$
2Bn^2d.
$$

FFN 若为两矩阵 $d\to d_{ff}\to d$，主 MAC 数约

$$
2Bndd_{ff}.
$$

于是单层主账本可写成

$$
\underbrace{4Bnd^2}_{QKVO}
+\underbrace{2Bn^2d}_{pairwise}
+\underbrace{2Bndd_{ff}}_{FFN}.
$$

这解释了一个常被忽略的事实：当 $n$ 尚未明显大于 $d$ 或 $d_{ff}$ 时，线性于 $n$ 的投影与 FFN 可能仍占主导。渐近阶不告诉你有限规模 crossover。

### 一个数量级例子

取 $d=4096,d_{ff}=11008,n=2048$，则 pairwise 项与投影/FFN 的比例并没有“$n^2$”三个字看起来那么悬殊。若把 $n$ 增到 64k，pairwise 才迅速支配算术和中间量。正确做法是把实际参数代入，而不是看到二次项就跳过常数和其他维度。

## 三、为什么显存账与 FLOPs 账不同

Naive attention 会物化每层每头的 score 或 probability：

$$
S,A\in\mathbb R^{B\times h_q\times n\times n}.
$$

单个张量需要约 $Bh_qn^2s$ bytes。训练还可能保存 Q/K/V、softmax 统计、dropout mask、residual states 和反向中间量；不同 autograd/kernels 的保存策略不同。

然而，输出只有 $Bnd$。因此 $n^2$ 中间量不是数学输出所必需，而是某种执行计划的产物。这正是 tiling、recomputation 和 online softmax 能改变峰值显存/IO、却不改变 dense pairwise 算术的原因。

## 四、IO 与 Roofline 视角

GPU 上有多层存储：寄存器、shared memory/SRAM、L2、HBM。算术单元只有拿到数据才能工作。粗略 roofline 模型写成

$$
\text{attainable throughput}
\le \min\bigl(
\text{peak FLOP/s},
\text{bandwidth}\times\text{arithmetic intensity}
\bigr).
$$

Arithmetic intensity 是每搬运一个 byte 完成多少算术。Naive attention 若把 $S$、$A$ 写回 HBM、随后再读回，会产生巨大流量；即使总 FLOPs 不变，减少 HBM round trip 也可能显著加速。

所以至少分四张账：

| 账本 | 单位 | 典型问题 |
|---|---|---|
| 算术 | MAC / FLOP | 需要计算多少 pair？ |
| 峰值存储 | byte | 同时驻留哪些张量？ |
| IO | HBM bytes / memory transactions | 数据在存储层级间搬几次？ |
| 并行与调度 | occupancy、warp/block、通信 | 算术能否喂满硬件？ |

## 五、Decode 的真正形状

第 $t$ 步只有一个新 query。它与历史 $t$ 个 keys 做 attention，单层 pairwise MAC 约 $2Btd$，不是 $2Bt^2d$。但为了这一步，系统要读取历史 cache：

$$
\text{KV scalars per layer}
=2B t h_{kv}d_h.
$$

总 cache bytes 为

$$
M_{KV}=2LBTh_{kv}d_hs.
$$

其中 $T$ 是最大缓存长度。Decode 每一步反复读这些历史数据；batch 和 context 增大后，bandwidth 可能比矩阵乘峰值更重要。也因此 MQA/GQA/MLA 的主要优化对象不是 prefill 的 $n^2$ score matrix，而是 decode cache bytes 与读取带宽。

> [!warning] 总生成复杂度
> 逐步生成 $T$ 个 token 时，第 $t$ 步读取 $O(t)$ 历史，累加仍为 $O(T^2)$ pairwise 工作。KV cache 消除了对旧 token 重做整层投影/FFN 的浪费，却没有把所有历史 attention 的总 pair 数变成线性。

## 六、四类“高效 Attention”其实优化不同对象

- **局部/稀疏 Attention**：删除 relation edges，改变模型可见域和算术；
- **低秩/核特征/随机特征**：压缩或近似 pairwise operator，改变模型或引入估计误差；
- **FlashAttention**：保留同一 dense attention 数学函数，用执行计划减少中间存储与 HBM IO；
- **MQA/GQA/MLA**：主要减少增量推理的 KV cache 和 bandwidth，未必减少 query-head 算术。

把这些方法放在一张“谁更线性”的表中而不写优化对象，是错误比较。

## 七、科学空间的有限规模提醒

[[S-2021-Su-8610-线性Transformer反例]] 的重要贡献不是给出一个永恒 crossover 数字，而是提醒我们把 projection、FFN 与 attention 全部代入。文中针对 BERT-like 设置得到的长度阈值属于特定参数与实现下的数量级分析；模型宽度、FFN 比例、kernel、精度和硬件变化都会移动阈值。

[[S-2020-Su-7546-线性Attention]] 则展示了结合律怎样把 $n^2$ pairwise 中间量改成 feature-state 聚合。两篇合起来的正确读法是：先确认代数允许重排，再确认有限规模下实际瓶颈确实在被重排的项。

## 八、正式图：怎样读一张 Attention 成本地图

这张图回答什么问题？为什么 prefill 的 $n^2$、decode 的 cache bandwidth、FlashAttention 的 IO 和 MQA/MLA 的缓存压缩不能互相替代？

![[00-知识库管理/_assets/figures/architecture/fig-attention-phase-cost-ledger-v1.svg|900]]

> [!figure] 图 1｜Attention 的阶段化成本总账。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_efficient_attention_v1.py]] 生成；公式按 dense MHA 的主项绘制，省略 bias、dropout、backward 常数和具体硬件参数。

**怎样读图**：先看 A，把投影、pairwise、score storage 与 FFN 分开；再看 B，注意 decode 每步只有一个 query，却必须访问历史 cache；最后看 C，把改变模型边、改变 kernel、改变执行计划和改变 cache 参数化分成四种优化靶点。

**图没有证明什么**：图没有给出任何固定硬件上的速度排序，也没有证明 $O(n)$ 方法在短序列更快；它更没有把少 FLOPs、少显存、低延迟和高吞吐视为同一指标。所有 crossover 都必须用真实 shape、dtype、batch、kernel 与硬件测量。

## 九、一个可复用的成本审计模板

面对任何“高效 Attention”论文，依次填写：

1. 数学输出是否与 dense softmax attention 相同？
2. 训练、prefill、decode 分别改变了哪些张量？
3. 省下的是 pairwise MAC、activation bytes、HBM IO 还是 cache bytes？
4. 新增了什么投影、state、索引、随机特征或通信？
5. 复杂度中的固定量 $k,r,w,h_{kv}$ 是否真的不随 $n$ 增长？
6. wall-clock 在什么硬件、batch、length、dtype、kernel version 下测得？
7. 质量比较是否对齐参数、训练 tokens、上下文和调参预算？

## 十、证据边界

- 上述 shape、MAC 和 cache scalar 公式：`I`；
- 两级内存模型中的 IO 上界/下界：带模型假设的 `T`；
- 某 GPU、某 kernel 的速度和显存：`E`；
- “某方法未来更适合长上下文”的机制解释：`H`；
- 能接收更长输入不等于能使用更远证据，参见 [[位置分辨率、混叠与长度外推评测]]。

## 十一、学习出口

完成本节后，应能在不查资料时从 $(B,n,d,h_q,h_{kv},d_h,d_{ff},L,s)$ 推出训练/prefill 主 MAC、naive score memory 和 decode KV cache；并能解释为什么 FlashAttention、Linear Attention 与 MQA 回答的是三道不同的效率问题。

