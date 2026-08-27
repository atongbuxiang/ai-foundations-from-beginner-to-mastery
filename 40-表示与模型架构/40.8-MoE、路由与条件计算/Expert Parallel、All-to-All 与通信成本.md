---
type: concept
status: draft
area: [architecture, moe, distributed-systems, expert-parallel]
aliases: [Expert Parallelism, All-to-All, MoE Communication]
node_id: ARCH-63
prerequisites: ["[[Expert Capacity、Dispatch 与 Token Dropping]]", "[[条件计算、专家混合与稀疏激活]]"]
related: ["[[Loss-Free 路由、偏置更新与分配视角]]", "[[Transformer 形状、参数量与 FLOPs 总账]]"]
sources: ["[[S-2020-Lepikhin-GShard]]", "[[S-2022-Rajbhandari-DeepSpeed-MoE]]", "[[S-2022-Hwang-Tutel]]", "[[S-2022-Gale-MegaBlocks]]", "[[S-2024-DeepSeek-V3-MoE]]"]
exercises: ["[[习题 - Expert Parallel、All-to-All 与通信成本]]"]
solutions: ["[[解答 - Expert Parallel、All-to-All 与通信成本]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-moe-expert-parallel-alltoall-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Expert Parallel、All-to-All 与通信成本

> [!abstract] 核心问题
> Expert Parallel 把不同专家放在不同设备。它降低单设备专家权重压力，却要求 token 表示按路由结果跨设备 dispatch，再把专家输出送回 token owner。通信 payload 可以从 shape 精确记账；实际延迟还取决于拓扑、偏斜、小消息、重叠和尾部同步。

## 一、为什么需要 Expert Parallel

若有 $E$ 个专家、每个参数量 $P_e$，全部复制到每个设备需要 $EP_e$ 参数驻留。把专家均匀分到 $D$ 个设备，每设备约保存

$$
\frac ED P_e
$$

的专家参数。这样总容量可跨设备扩展。

代价是 token 与其专家可能不在同一设备。数据并行只在反向同步梯度；Expert Parallel 在每个 MoE layer 的前向和反向中都可能搬 token/gradient。

## 二、一次前向的六个阶段

1. 每个 token owner 本地计算 Router；
2. 生成 $(expert\ id,token\ id,gate)$；
3. 按目标设备 pack，并执行 dispatch All-to-All；
4. 每台设备按本地 expert 再分组，执行 FFN；
5. 将 expert output 做 combine All-to-All 送回原 owner；
6. 逆置换并按 gate 求和，接 residual。

反向还需相反方向传播 output gradients、expert input gradients，并更新 Router 与 expert parameters。

## 三、payload 的最低恒等账本

设路由组有 $T$ 个真实 token、每 token 选择 $k$ 个专家、hidden width 为 $d$、每标量 $s$ bytes。若每个 assignment 都发送完整 hidden vector，则 dispatch 的逻辑 payload 为

$$
Q_{\text{dispatch,logical}}=Tkd s.
$$

combine 返回同宽输出，再约为 $Tkds$。因此前向双向逻辑 payload 主项

$$
Q_{\text{fwd,logical}}\approx2Tkds.
$$

若一部分 assignment 的专家在本地，真正过网络的量乘 remote fraction $r$：

$$
Q_{\text{network}}\approx2rTkds+Q_{\text{metadata}}+Q_{\text{padding}}.
$$

Top-k 的同一 token 被复制 $k$ 份；若共享专家本地复制，其流量可能不经过 EP network。应按实际 placement 计算，不能只报 $Tkds$。

## 四、一个数值例子

令 $T=8192,k=2,d=4096,s=2$ bytes，假设 $r=0.75$。忽略 metadata/padding，前向跨网 payload 约为

$$
2\times0.75\times8192\times2\times4096\times2
=201{,}326{,}592\ \text{bytes}
\approx192\ \text{MiB}.
$$

这是每个 MoE layer、每个路由组的逻辑总量级，而不是单链路精确流量。collective 算法可能让字节经过多跳；各设备负载也可能不均。

## 五、为什么字节相同而延迟不同

网络时间的粗下界为

$$
t_{\text{comm}}\gtrsim \frac{Q}{B_{\text{effective}}}+N_{\text{msg}}\ell,
$$

其中 $B_{\text{effective}}$ 是有效带宽，$N_{\text{msg}}$ 是消息/轮数，$\ell$ 是启动延迟。但端到端还有：

- intra-node NVLink 与 inter-node fabric 的分层拓扑；
- token 偏斜导致某 device 接收更多；
- 许多小 expert buckets 降低带宽利用；
- pack/unpack、permutation 与 kernel launch；
- 计算—通信是否重叠；
- 最慢专家形成全局 straggler。

因此平均 payload 是 `I`，wall-clock 是具体协议 `E`。

## 六、负载均衡为什么也是通信优化

若设备 $d$ 的 assignment 数为 $N_d$，同步 MoE layer 的尾部至少受

$$
\max_dN_d
$$

控制。即使总通信量 $\sum_dN_d$ 不变，把 assignment 集中到一个设备也会增加接收带宽、expert compute 与同步等待。

均衡损失、loss-free bias 和 expert quota 因而同时服务于模型训练与系统尾延迟。但它们是否值得牺牲 task-optimal routing 是 Pareto 问题。

## 七、并行维度怎样交互

大模型常同时使用：

- DP：复制模型，分数据；
- TP：切分矩阵维度；
- PP：切分层；
- EP：切分专家；
- SP/CP：切分序列或 context。

若 expert 内又做 TP，token dispatch 后还可能 all-gather 或 reduce-scatter；若 Router 在 sequence shard 上，负载统计需要跨 shard 汇总；若 pipeline microbatch 太小，expert bucket 更碎。

公平报告必须给出 $(DP,TP,PP,EP,SP)$ 布局，而不是只写 GPU 数。

## 八、Tutel、DeepSpeed-MoE 与 MegaBlocks 的位置

[[S-2022-Hwang-Tutel]] 与 [[S-2022-Rajbhandari-DeepSpeed-MoE]] 重点在高效 MoE runtime、并行映射和通信/计算优化；[[S-2022-Gale-MegaBlocks]] 重点在 dropless block-sparse expert computation。它们优化的对象不同：collective、placement、调度和 local expert kernel 必须分别标注。

“使用 dropless kernel”不等于“没有 All-to-All”；“通信重叠”也不等于网络字节消失。

## 九、正式图：All-to-All 的完整往返

这张图回答什么问题？为什么只知道每 token 激活 $k$ 个专家仍不能预测延迟？

![[00-知识库管理/_assets/figures/architecture/fig-moe-expert-parallel-alltoall-v1.svg|900]]

> [!figure] 图 1｜Expert Parallel 的 dispatch/compute/combine、payload 账本与尾延迟因素。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_moe_v1.py]] 生成；拓扑为教学抽象，未复制系统论文图。

**怎样读图**：A 从 token owner 跨设备送到 expert owner，并记住还要逆置换返回；B 用 assignments×hidden width×dtype 建立逻辑字节账，再加入方向、metadata 与 local share；C 从 topology、skew、buckets、overlap、straggler 和 kernel 六项解释 volume 与 latency 的差距。

**图没有证明什么**：图没有给出某 collective 的精确链路流量或速度，也没有证明 EP 一定比专家复制节省端到端成本；权重显存、网络与 expert kernel 之间存在硬件相关的交换。

## 十、基准测试最低协议

固定 checkpoint 与 batch 后，扫：

- $T,k,d,E$；
- EP group size 与 experts/device；
- intra/inter-node placement；
- capacity/drop/dropless；
- token 分布的均匀、Zipf 与极端偏斜；
- dtype、quantization、block size；
- overlap on/off；
- DP/TP/PP/EP/SP 组合。

记录 logical/physical network bytes、每 rank send/recv、all-to-all time、pack/unpack、expert GEMM、overlap ratio、p50/p95/p99 step time、最忙 rank 和端到端 tokens/s。

## 十一、证据边界与学习出口

- payload shape 与 assignment 数：`I`；
- 给定 collective/topology 的通信复杂度：`T`；
- Tutel/DeepSpeed/MegaBlocks 的硬件测量：其协议下 `E`；
- “均衡改善主要通过尾延迟”：需 profiler 支持的 `H/E`；
- 跨集群最优并行布局：`O`。

学完本节，应能从 $T,k,d,s,r$ 算出 dispatch+combine 逻辑字节，画出一次 EP 往返，并说明为何平均通信量无法替代最大 rank 负载与延迟分布。

