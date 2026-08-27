---
type: concept
status: verified
area: [language-models, inference, serving]
node_id: LM-54
aliases: [LLM Serving, KV 缓存, 连续批处理]
prerequisites: ["[[KV Cache、MHA、MQA 与 GQA]]", "[[自回归模型的表达、成本、失效模式与证据地图]]"]
related: ["[[Speculative Decoding、Acceptance 与分布精确性]]", "[[解码质量、延迟、吞吐、随机性与证据地图]]", "[[Model、API、Tokenizer、Template 版本与复现合同]]"]
sources: ["[[S-2022-Yu-Orca]]", "[[S-2023-Kwon-PagedAttention]]", "[[S-2022-Dao-FlashAttention]]"]
exercises: ["[[习题 - Prefill、Decode、KV Cache 与 Continuous Batching]]"]
solutions: ["[[解答 - Prefill、Decode、KV Cache 与 Continuous Batching]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-serving-kv-scheduler-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Prefill、Decode、KV Cache 与 Continuous Batching

> [!abstract] 一句话结论
> Prefill 一次处理已有上下文，decode 此后逐轮产生 token；KV cache 用显存换掉对旧 token 的重复 K/V 投影。真正的服务性能由模型计算、KV 内存、请求到达与长度分布、迭代调度共同决定。

## 一、一次请求的两相状态机

输入含 $S$ 个 token，输出含 $O$ 个 token。请求先进入 **prefill**：对整个 prompt 建立隐藏状态与每层 KV cache，并得到第一个 next-token logits；随后进入 **decode**：每轮把一个新 token 送入模型，读取历史 KV，生成下一 token。

两相的并行结构不同：

- prefill 有较长的 token 维度并行，矩阵乘通常更大，常偏 compute-bound；
- decode 的单请求每轮 query length 为 1，必须等待上个 token，常偏 memory-bandwidth/launch-bound；
- 多请求 batching 可让 decode 把许多“一行”拼成较大的工作量，但它没有消除单请求的因果串行。

最粗略的延迟分解为

$$
T_{\mathrm{request}}
=T_{\mathrm{queue}}+T_{\mathrm{prefill}}
+\sum_{t=1}^{O}T_{\mathrm{decode},t}
+T_{\mathrm{post}}.
$$

因此首 token 延迟 TTFT 主要覆盖 queue+prefill，而 token 间延迟 TPOT/TBT 主要观察 decode；两者不可互相替代。

## 二、KV cache 为什么存在

在第 $\ell$ 层，旧 token 的 key/value 为

$$
K_{1:t}^{(\ell)},\quad V_{1:t}^{(\ell)}.
$$

生成第 $t+1$ 个 token 时，只需计算新 token 的 $q_{t+1},k_{t+1},v_{t+1}$，并让 query 读取已有 $K,V$。没有 cache，就会在每轮重复计算整个前缀的 K/V 与中间状态。

对 decoder-only 模型，**每个已存 token** 的 KV 字节近似为

$$
b_{\mathrm{token}}
=L\times2\times n_{kv}\times d_h\times b,
$$

其中 $L$ 是层数，2 对应 K 与 V，$n_{kv}$ 是 KV head 数，$d_h$ 是 head dimension，$b$ 是每元素字节数。总量约为

$$
B_{KV}=N_{\mathrm{live\ tokens}}b_{\mathrm{token}}.
$$

例：$L=32,n_{kv}=8,d_h=128,b=2$，每 token 为 $32\times2\times8\times128\times2=131072$ bytes，即 128 KiB；一条 4096-token 序列约 512 MiB，尚未计 allocator metadata 与其他 workspace。

> [!note] MHA、GQA 与 MQA
> MHA 常有 $n_{kv}=n_q$；GQA 让多组 query heads 共享较少 KV heads；MQA 可取 $n_{kv}=1$。KV 公式必须用 $n_{kv}$，不能无条件用 attention head 总数。

## 三、attention FLOPs 与持久 KV 不是一回事

FlashAttention 通过分块与重计算减少 attention 中间矩阵的高带宽内存读写，改善 exact attention 的 IO；它不等于消除跨 decode 步持久保存的 KV cache。服务分析至少分开：

- 权重与算子临时 activation/workspace；
- attention 中间矩阵的 IO；
- 生命周期跨越多个 decode iteration 的 persistent KV；
- allocator 的内部/外部碎片。

把“FlashAttention 更省内存”直接外推为“KV 容量按同比例下降”，属于对象层混淆。

## 四、从连续数组到分页 KV

若每个请求预留 `max_length` 的连续 KV，短输出会产生内部浪费；请求动态增长、结束和释放又可能造成外部碎片。分页思想把逻辑 token 序列映射到固定大小物理 blocks：

$$
\text{logical block }j
\longmapsto
\text{physical block }\pi_r(j).
$$

请求只在需要时分配新 block；非连续物理块由 block table 寻址。它还允许多个序列对公共 prompt 或 beam prefix 做引用计数/copy-on-write 共享。

若 block 容量为 $P$ token，请求长度 $n$ 的最后一块内部空位小于 $P$，而不是浪费到整个最大长度。但分页仍有 block table、最后一块浪费、寻址与管理成本，不是零开销。

## 五、static batching 与 continuous batching

静态批处理等一批请求同时开始、一起结束。若输出长度不齐，已完成槽位空转；若等待凑批，queue latency 上升。Continuous batching 在每个 iteration 边界重新组成 active batch：完成请求立即离开，新请求可进入 prefill 或 decode。

可将 scheduler 状态写为

$$
\mathcal S_t=
(Q_t,P_t,D_t,M_t),
$$

其中 $Q$ 是等待队列，$P$ 是 prefill 集合，$D$ 是 decode 集合，$M$ 是可用 KV blocks。一次调度既决定谁运行，也决定多少 token 被 prefill、是否抢占/重算/换出。

策略冲突包括：

- 大 prefill batch 提高吞吐，却会阻塞正在 decode 的请求并抬高 TBT；
- 优先 decode 稳定交互延迟，却可能让长 prompt 饥饿；
- 高并发提高设备利用率，却增加 queue 与 KV 压力；
- 抢占释放 KV，却会引入 swap 或 recompute 成本。

## 六、吞吐、延迟与 goodput

吞吐可写 tokens/s 或 requests/s，但二者依赖输入/输出长度。只报告平均 latency 会隐藏尾部。服务报告至少含：

$$
\text{TTFT},\quad
\text{TPOT/TBT},\quad
p50/p95/p99,\quad
\text{tokens/s},\quad
\text{goodput under SLO}.
$$

goodput 是满足服务目标的有效请求率。例如 SLO 要求 TTFT≤1 s 且 p99 TBT≤100 ms，则超过条件的完成请求不计入 goodput，即使总 tokens/s 很高。

所有数字需绑定 model/checkpoint、dtype/quantization、GPU 与互联、tensor/pipeline parallel、prompt/output length distribution、arrival process、concurrency、warmup 和 scheduler 配置。

## 七、图解：KV 内存板与迭代调度

**读图问题**：三个不同长度请求怎样在 iteration 边界进入和离开 batch，它们的逻辑 token 又如何映射到不连续的物理 KV blocks？

![[00-知识库管理/_assets/figures/language-models/fig-lm-serving-kv-scheduler-v1.svg|900]]

> [!figure] 图 LM-54　请求从 prefill 到 decode 的状态变化与分页 KV
> **生成：**本库按 prefill/decode 状态机与 paged-KV 映射确定性绘制；上方是调度时间轴，下方是教学 block table，颜色只编码请求。

**怎样读图**：先横向读取各请求的 prefill 与逐 token decode，再在 iteration 边界观察加入、完成和回收；随后把逻辑块映射到下方物理槽，确认共享只适用于未分叉的只读前缀。

**图没有证明什么**：更紧凑的 KV 版图或更高设备占用率不必然带来更低 p99 TTFT/TBT；PagedAttention 也不直接提高模型输出质量，真实性能仍依赖硬件、负载和实现。

## 八、常见错误与出口标准

错误包括：把 prefill/decode 混成一个平均值；把上下文窗口等同 KV 实际占用；KV 公式误用 query head 数；把 FlashAttention 等同 KV 分页；只报峰值吞吐；忽略到达率和长度分布；固定 batch 的结论外推 continuous batching。

完成本节后，应能按模型结构手算 KV bytes，解释 prefill 与 decode 的并行差异，画出迭代 scheduler 状态，识别分页缓解哪种碎片，并写出可比较的 latency/throughput/goodput 实验合同。

## 九、来源与练习

- [[S-2022-Yu-Orca]]；
- [[S-2023-Kwon-PagedAttention]]；
- [[S-2022-Dao-FlashAttention]]；
- [[习题 - Prefill、Decode、KV Cache 与 Continuous Batching]]；
- [[解答 - Prefill、Decode、KV Cache 与 Continuous Batching]]。
