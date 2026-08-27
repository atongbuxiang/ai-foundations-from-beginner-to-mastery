---
type: concept
status: draft
area: [architecture, inference, kv-cache, grouped-query-attention]
aliases: [KV Cache, Multi-Query Attention, Grouped-Query Attention]
node_id: ARCH-55
prerequisites: ["[[Transformer Decoder 与自回归因果结构]]", "[[Multi-Head Attention、投影子空间与参数量]]", "[[Attention 的二次复杂度、内存与 IO 瓶颈]]"]
related: ["[[高效 Attention 与推理接口 MOC]]", "[[MLA、潜变量缓存与推理成本证据]]", "[[RoPE 的旋转推导、群表示与内积]]"]
sources: ["[[S-2019-Shazeer-MQA]]", "[[S-2023-Ainslie-GQA]]", "[[S-2024-Su-10091-MHA-MQA-GQA-MLA]]"]
exercises: ["[[习题 - KV Cache、MHA、MQA 与 GQA]]"]
solutions: ["[[解答 - KV Cache、MHA、MQA 与 GQA]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-kv-cache-mha-gqa-mqa-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# KV Cache、MHA、MQA 与 GQA

> [!abstract] 核心问题
> 自回归 decode 的每一步不应重算旧 token 的 K/V，因此缓存它们。MHA、GQA、MQA 的核心设计轴是：保留多少 query heads、为多少组 query heads 缓存独立 K/V。Cache scalar 公式是精确账本；质量和速度必须由训练与系统协议判断。

## 一、为什么需要 KV Cache

无 cache 时，生成第 $t$ 个 token 会把整个前缀 $x_{1:t}$ 再送入所有层，旧 token 的 Q/K/V、FFN 重复计算。使用 cache 后：

1. Prefill 一次计算 prompt 的每层 K/V；
2. 每步只计算新 token 的 hidden、Q/K/V；
3. 新 K/V append 到 cache；
4. 新 Q 与历史 K 做 score，并加权历史 V。

Cache 消除旧 token 整层重算，但每步仍读取历史 K/V。

## 二、统一 Head 记号

设 query head 数 $h_q$，KV head 数 $h_{kv}$，单头 K/V 维度 $d_h$，并要求 $h_q$ 能按组映射到 $h_{kv}$。

- MHA：$h_{kv}=h_q$；
- GQA：$1<h_{kv}<h_q$；
- MQA：$h_{kv}=1$。

第 $a$ 个 query head 使用 KV group

$$
g(a)=\left\lfloor\frac{a h_{kv}}{h_q}\right\rfloor.
$$

每组 query heads 的 Q 投影不同，但读取同一 K/V head。

## 三、张量 Shape

新 token query：

$$
Q_t\in\mathbb R^{B\times h_q\times1\times d_h}.
$$

历史 cache：

$$
K_{1:t},V_{1:t}\in
\mathbb R^{B\times h_{kv}\times t\times d_h}.
$$

逻辑计算时可把 K/V broadcast 到 query groups，但物理存储不应复制成 $h_q$ 份，否则失去 cache 优势。

## 四、Cache 总账

每层、每 token、每 batch item 的 K/V scalars 为

$$
2h_{kv}d_h.
$$

全模型：

$$
M_{KV}=2LBTh_{kv}d_hs\quad\text{bytes}.
$$

相对 MHA、保持 $d_h,h_q$ 不变时，GQA cache 比例为

$$
\frac{h_{kv}}{h_q},
$$

MQA 为 $1/h_q$。这只是 K/V payload；allocator metadata、page fragmentation、alignment、quantization scales 和 distributed replicas 还需另计。

### 数字例子

取 $L=32,B=8,T=32768,h_q=32,d_h=128,s=2$ bytes：

- MHA $h_{kv}=32$；
- GQA $h_{kv}=8$，payload 为 MHA 的 $1/4$；
- MQA $h_{kv}=1$，payload 为 MHA 的 $1/32$。

这解释了相同显存上为何能增大 batch 或 context。

## 五、参数量也会变化

忽略 bias：

$$
W_Q:d\times(h_qd_h),
$$

$$
W_K,W_V:d\times(h_{kv}d_h).
$$

因此 K/V projection parameters 随 $h_{kv}$ 下降。公平比较总参数时，论文可能把差额加到 FFN 或其他部件；若不记录这一点，质量差不能只归因于 KV sharing。

## 六、为什么 Decode 可能更快

第 $t$ 步所有 query heads 仍需对历史做 dot products，理论算术不按 $h_{kv}/h_q$ 同比例消失；shared K/V 可能在 kernel 中复用，但输出仍有 $h_q$ 个 heads。

主要收益是：

- cache payload 更小；
- 每步从 HBM 读取更少 K/V bytes；
- 更大 batch/context 能驻留显存；
- tensor parallel 下可能减少某些通信/复制。

若 decode 本来不是 bandwidth-bound，或 kernel 不能有效利用共享，速度收益会小于 cache 比例。

## 七、质量为何可能变化

MHA 每个 query head 有独立 K/V 投影；MQA 把所有 heads 的“被匹配坐标”和“被读取内容”共享，减少自由度。GQA 在两端之间连续调节。

但不能从自由度减少直接推出任务质量单调下降：训练可重新分配 query/output/FFN 表示，参数预算也可调整。实际需要 GQA group sweep、相同训练 tokens、多 seed 和下游评测。

[[S-2023-Ainslie-GQA]] 还研究从 MHA checkpoint 进行 uptraining。其“接近 MHA 质量、接近 MQA 速度”是论文模型与 uptraining 预算下的 `E`，不是所有 checkpoint 的无条件结论。

## 八、RoPE 与 Cache Offset

若 K 在写入 cache 前已经 RoPE 旋转，新 token 必须使用全局 position ID。Cache 中位置 0..$t-1$ 与新 query 位置 $t$ 的相对内积依赖正确 offset。

还需登记：

- cache 保存旋转前还是旋转后 K；
- partial rotary dimension；
- chunked prefill；
- left padding 与不同 batch cache lengths；
- sliding window eviction 后 position 是否继续全局增长。

任何错位都可能 shape 正常、输出错误。

## 九、科学空间的统一推导

[[S-2024-Su-10091-MHA-MQA-GQA-MLA]] 用统一 head notation 推导 MHA→MQA→GQA，并把目标明确落到 generation 的显存/带宽。尤其重要的是，它没有把 cache 减少直接写成算术等比例减少。

文章还指出 $h_{kv}$ 与 tensor parallel device 数的映射可能影响通信。这是系统设计线索，不是固定选择 $g=8$ 的普遍定理；设备拓扑、模型宽度和 kernel 会改变最优 group 数。

## 十、正式图：Head 数怎样变成 Cache Bytes

这张图回答什么问题？为什么 query heads 可以保持 8 个，而 KV heads 从 8 降到 4 再到 1？

![[00-知识库管理/_assets/figures/architecture/fig-kv-cache-mha-gqa-mqa-v1.svg|900]]

> [!figure] 图 1｜MHA、GQA、MQA 的 head mapping、cache scalar 与系统边界。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_efficient_attention_v1.py]] 生成；使用八 query heads 仅为可视化，公式适用于一般 $h_q,h_{kv}$。

**怎样读图**：A 的圆是 query heads、方块是实际 KV heads；连线表示多 query heads 共享一组 K/V。B 用 $2BTh_{kv}d_h$ 直接数每层 payload。C 再把 bandwidth、参数、质量、并行通信和最终 latency 分开，防止把 cache 比例当速度比例。

**图没有证明什么**：图没有证明 MQA 质量必低于 GQA，也没有证明 GQA 的最优 group 数；它省略 allocator/page、量化 scale、通信 replica 和 kernel layout，因此不能直接给出总显存或端到端吞吐。

## 十一、Serving 接口

版本化 cache schema 至少包含：layer、batch/sequence ID、KV-head layout、position offset、valid length、page/block table、dtype/quant scale、device shard 和 rotary state。Continuous batching 还要处理序列加入/结束、page 回收和不同长度调度。

Cache quantization 是另一条轴：payload bytes 可继续下降，但引入量化误差、scale metadata 和 dequant kernel。不能把 hkv 压缩与 dtype 压缩的效果合并归因。

## 十二、公平实验

在 $h_{kv}\in\{h_q,h_q/2,h_q/4,1\}$ 上：

- 对齐总参数或明确不对齐；
- 固定训练 tokens/optimizer/position；
- 测 loss、retrieval/reasoning 和多 seed；
- 分开 prefill/decode latency；
- 扫描 batch×context×output length；
- 报 cache payload、allocated memory、HBM bandwidth、TP communication；
- full forward 与 cached decode 做逐行等价测试。

## 十三、证据边界

- Head mapping、参数与 cache scalar 公式：`I`；
- MQA/GQA 质量与速度：`E`；
- “KV sharing 是最优容量分配”：`H/O`；
- 更小 cache 通常利于 bandwidth，但是否成为 end-to-end speedup 要 profiling；
- Cache 优化不证明模型能有效使用更长上下文。

## 十四、学习出口

应能从任意 config 精确算 MHA/GQA/MQA 参数与 cache payload，画出 query-to-KV mapping，解释 decode bandwidth，并审计 RoPE offset、physical broadcast 和 full/cache 等价。

