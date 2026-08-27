---
type: concept
status: draft
area: [architecture, efficient-attention, flashattention, io]
aliases: [FlashAttention, IO-Aware Attention, Online Softmax Attention]
node_id: ARCH-54
prerequisites: ["[[Attention 的二次复杂度、内存与 IO 瓶颈]]", "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[稳定求和、点积与矩阵乘法]]"]
related: ["[[高效 Attention 与推理接口 MOC]]", "[[局部、分块与稀疏 Attention]]", "[[Transformer 形状、参数量与 FLOPs 总账]]"]
sources: ["[[S-2022-Dao-FlashAttention]]", "[[S-2023-Dao-FlashAttention2]]", "[[S-2019-Child-Sparse-Transformer]]"]
exercises: ["[[习题 - FlashAttention、精确计算与 IO Awareness]]"]
solutions: ["[[解答 - FlashAttention、精确计算与 IO Awareness]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-flashattention-io-online-softmax-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# FlashAttention、精确计算与 IO Awareness

> [!abstract] 核心问题
> FlashAttention 没有把 dense attention 近似成稀疏或低秩模型。它通过 tiling、online softmax 与反向重计算，让 $n\times n$ scores/weights 不必写回 HBM。于是 dense pair 算术仍为二次，但峰值中间存储和数据搬运大幅改变。

## 一、Naive 三阶段为什么搬运很多数据

标准执行可概括为：

1. $S=QK^\top/\sqrt{d_h}$，把 $S$ 写到 HBM；
2. $P=\operatorname{softmax}(S)$，读 $S$、写 $P$；
3. $O=PV$，读 $P,V$、写 $O$。

数学上输出只需 $O\in\mathbb R^{n\times d_v}$，但执行计划往返搬运两个 $n\times n$ 中间量。长序列时 HBM traffic 和存储成为瓶颈。

## 二、Tiling 的核心思想

把 Q 分成 query tiles $Q_i$，K/V 分成 key-value tiles $(K_j,V_j)$。在片上 SRAM 中：

1. 计算小 score tile $S_{ij}=Q_iK_j^T$；
2. 更新该 query tile 每行的 softmax 统计；
3. 立刻累加 $P_{ij}V_j$；
4. 丢弃 score tile，处理下一个 $j$。

最终只把 $O_i$ 和少量统计写回 HBM，不保存完整 $S,P$。

## 三、Online Softmax 为什么能分块

对一行 scores，已处理旧块的最大值、指数和、未归一化 value accumulator 记作

$$
m,\qquad
\ell=\sum_{a\in old}e^{s_a-m},
\qquad
u=\sum_{a\in old}e^{s_a-m}v_a.
$$

新块最大值为 $m_b$，令

$$
m'=\max(m,m_b).
$$

旧项改用新基准需要乘 $e^{m-m'}$，所以

$$
\ell'=e^{m-m'}\ell+
\sum_{b\in new}e^{s_b-m'},
$$

$$
u'=e^{m-m'}u+
\sum_{b\in new}e^{s_b-m'}v_b.
$$

遍历完所有 blocks 后

$$
o=u/\ell.
$$

这与 stable softmax 的 max-shift 是同一恒等式，只是把全行归约改成可合并状态。

## 四、Exact 到底是什么意思

FlashAttention 的“exact”指：在实数数学语义和同一 mask/dropout 合同下，目标仍是 dense softmax attention，不引入 low-rank/random/sparse 模型近似。

但 exact 不等于：

- bitwise 与 naive reduction 相同；
- 没有浮点误差；
- 算术复杂度变成 $O(n)$；
- 所有 shape/hardware 都更快；
- block-sparse 扩展仍是 dense exact。

浮点加法不结合，tiling 改变归约顺序；通常结果在容差内相近，而非逐 bit 相同。

## 五、Backward 为什么可以不保存 Attention Matrix

反向需要 softmax probabilities，但可保存每行 log-sum-exp/normalizer 和输出，随后按相同 Q/K blocks 重算 scores/probabilities。这用额外算术换 $n^2$ activation storage 和 HBM IO。

“重算”不是免费，但在算术吞吐远高于 HBM 带宽时可能更快。Checkpointing 的同类原则是：系统最优不一定是最少 FLOPs，而可能是更高 arithmetic intensity。

Dropout 要求前向/重算复现同一随机 mask，通常借助 counter-based RNG 或保存足够状态；否则梯度语义改变。

## 六、IO 复杂度与存储模型

FlashAttention 论文在两级 memory model 中分析 HBM↔SRAM 访问，并在一定 SRAM size 范围给出 IO 最优性。这里的定理对象包括：

- 矩阵形状；
- SRAM 容量 $M$；
- 数据必须从 HBM 读取/写回；
- 允许的计算模型。

不能把这一结论写成“任何 GPU 和任意 $d_h$ 上都绝对最优”。后续理论和 kernel 版本进一步细化不同 $M,d,n$ 区域。

## 七、FlashAttention-2 改了什么

FA2 仍计算同一 attention，主要优化：

- 减少非 matmul FLOPs；
- 在单个 head/sequence 内增加 thread-block 并行；
- 改善 warp work partition，减少 shared-memory 通信；
- 提高 occupancy 和 GEMM 利用率。

因此引用速度必须标注 FA1/FA2/后续版本、GPU、causal mode、head dimension、sequence length 和 library commit。Kernel microbenchmark、attention layer 和完整模型吞吐不可互换。

## 八、Mask、Variable Length 与 Decode

Causal mask 可在 tile 内跳过上三角 blocks/元素；padding 和 variable-length batch 需要 length metadata。若 padding 很多，固定 dense batch 可能浪费 tiles，packed/ragged kernel 会改变调度。

FlashAttention 主要解决 prefill/training 的 dense attention IO。单-token decode 的形状很窄，瓶颈常转向 KV cache bandwidth，需 paged attention、MQA/GQA/MLA 等另一组接口。不能因为名字都有 Attention 就认为 FA 自动压缩 cache。

## 九、正式图：二次算术为何可以配线性中间存储

这张图回答什么问题？怎样在不把 $n\times n$ 写回 HBM 的情况下，逐块得到同一个 stable softmax output？

![[00-知识库管理/_assets/figures/architecture/fig-flashattention-io-online-softmax-v1.svg|900]]

> [!figure] 图 1｜FlashAttention 的 memory hierarchy、online softmax merge 与 exact 边界。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_efficient_attention_v1.py]] 生成；图为算法结构示意，不复制论文 kernel 图或具体 tile size。

**怎样读图**：A 看 Q/K/V tiles 从 HBM 进入 SRAM，完整 scores/probabilities 从未写回；B 用 $(m,\ell,u)$ 的重标度状态合并新 score tile；C 精确区分“同一数学 attention”与 bitwise、线性算术、全硬件必快等错误延伸。

**图没有证明什么**：图没有给出特定 SRAM 容量下的 IO 下界证明，也没有估计 backward、dropout、variable-length 或 distributed communication 成本；它不能用来宣称任何带 FlashAttention 名称的库版本在所有形状都更快。

## 十、正确性测试

对参考 dense implementation 比较：

- forward output；
- dQ/dK/dV；
- causal/padding/sliding-window masks；
- dropout 固定 seed；
- fp32/bf16/fp16；
- all-masked rows 与极端 logits；
- odd lengths、不同 $d_h$、contiguous/noncontiguous layout。

比较应使用绝对+相对容差和 error distribution，不要求错误的 bitwise equality。

## 十一、性能测试

同时报告：

- kernel time 与 end-to-end time；
- achieved FLOP/s、HBM bytes/带宽；
- peak memory；
- forward/backward；
- warm-up、同步和计时方法；
- batch、heads、length、dtype、GPU 和软件版本。

短序列上 launch/tiling overhead 可能占主导；长序列上才显现 IO 优势。

## 十二、证据边界

- Online softmax merge：`I`；
- 指定存储模型中的 IO 上/下界：`T`；
- 论文/库的速度与显存：`E`；
- “IO 是真实瓶颈”：需对具体 shape/hardware profiling；
- exact kernel 不提供模型质量提升定理，只应在数值容差内保持原模型函数。

## 十三、学习出口

应能独立推导 $(m,\ell,u)$ 合并公式，解释前向 tiling/反向重算、准确区分 model approximation 与 IO optimization，并为一个新 kernel 设计正确性和性能两套测试。

