---
type: concept
status: verified
area: [training, distributed-training, model-parallelism]
course_id: TRN-62
prerequisites: ["[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[多线性映射、张量与缩并]]"]
related: ["[[ZeRO、FSDP、激活重计算与 Offload]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]", "[[条件计算、专家混合与稀疏激活]]"]
sources: ["[[S-2019-Shoeybi-Megatron-LM]]", "[[S-2019-Huang-GPipe]]", "[[S-2022-Korthikanti-Sequence-Parallelism]]", "[[S-2022-Rajbhandari-DeepSpeed-MoE]]", "[[S-2026-NVIDIA-NCCL-Collectives]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Tensor、Pipeline、Sequence 与 Expert Parallel

> [!abstract] 本节目标
> 不靠缩写记忆并行法，而是对每个算子写 global shape、local shard、forward/backward collective、复制状态和数据语义；能解释 TP、PP、SP/CP、EP 切的是不同轴，hybrid mesh 也不一定是所有 degree 的简单乘积。

## 一、五种并行首先是五种切分轴

| 并行 | 主切分轴 | 同一组 devices 在处理什么 | 典型通信 |
|---|---|---|---|
| data parallel | batch/sample | 不同样本、同一模型 | gradient All-Reduce/ReduceScatter |
| tensor parallel | hidden/head/intermediate | 同一层、同一样本的矩阵分片 | All-Reduce/AllGather/ReduceScatter |
| pipeline parallel | layer/depth | 同一样本的不同层 stage | point-to-point activation/gradient |
| sequence/context parallel | sequence tokens | 同一样本的不同 token/activation shard | AllGather/ReduceScatter/attention exchange |
| expert parallel | expert index/token routing | 同一 MoE 层的不同专家与路由 token | All-to-All |

名称不能代替 shape：不同论文中的 “sequence parallel” 可能指 tensor-parallel 配套 activation 分片，也可能指长上下文 attention 的 context parallel，通信完全不同。

## 二、Tensor parallel：从一个线性层推导

设

$$
X\in\mathbb R^{B\times H},\qquad W\in\mathbb R^{H\times K},\qquad Y=XW.
$$

### Column parallel

把输出维切成 $T$ 份：

$$
W=[W_1,\ldots,W_T],\qquad Y_i=XW_i.
\tag{1}
$$

每 rank 持有完整 $X$ 与 $K/T$ 输出。若下一算子能消费分片 $Y_i$，可延后 AllGather。

### Row parallel

把输入维切分：

$$
X=[X_1,\ldots,X_T],\qquad
W=\begin{bmatrix}W_1\\ \vdots\\ W_T\end{bmatrix},\qquad
Y=\sum_{i=1}^TX_iW_i.
\tag{2}
$$

各 rank 先算 partial $Y_i$，再 All-Reduce 求和。[[S-2019-Shoeybi-Megatron-LM]] 通过 column/row pair 让 MLP 中间非线性在分片上执行，并把同步放到合适边界。

backward 还需按转置图重新推导；只列 forward collective 不完整。

## 三、Attention 的切分

多头 attention 的 head 维天然可分：每 TP rank 计算一组 heads 的 $Q,K,V$ 与局部 attention，再在 output projection 处聚合。若 head 数不能被 TP degree 整除，需不均匀切分、复制 KV heads 或改变并行设计。

对 sequence 长度 $S$，完整 attention score 为 $[B,h,S,S]$。沿 head 切与沿 sequence 切是不同问题；后者需交换远端 $K,V$ 或分块在线 softmax statistics。

## 四、Pipeline parallel：bubble 从时间表推导

把 $L$ 层分到 $P$ 个 stages，一个 mini-batch 切成 $M$ 个 micro-batches。对同步 GPipe-style fill/drain 且各 stage 时间相等，forward-only 利用率近似

$$
\eta_{pipe}\approx\frac{M}{M+P-1}.
\tag{3}
$$

$P-1$ 是填充/排空 bubble。训练 schedule 还包含 backward；1F1B、interleaving 与 virtual stages 会改变公式和 activation 驻留。

stage 边界每个 micro-batch 发送 activation

$$
A\in\mathbb R^{b\times S\times H}
$$

并在 backward 发送同 shape gradient。stage 平衡应按 profiler 时间、memory 和通信，而不是简单平均层数。

## 五、Micro-batch 的双重身份

pipeline micro-batch 用于填充 stage；gradient accumulation micro-batch 用于组成一个 optimizer update。二者可相同但概念不同。改变 $M$ 可能同时改变：

- pipeline bubble；
- activation memory；
- GEMM shape/efficiency；
- gradient accumulation 时钟；
- normalization/dropout 与随机数消费。

所以性能调参不能假设数值语义自动不变。

## 六、Sequence parallel 与 selective recomputation

[[S-2022-Korthikanti-Sequence-Parallelism]] 在 tensor-parallel group 内，将 LayerNorm、dropout 等沿 sequence 可独立的 activation 切分，降低每 rank activation 驻留；进入需要完整 hidden/特定布局的算子时再 AllGather/ReduceScatter。

它不意味着标准 self-attention 的每个 token 可完全独立，因为每个 query 依赖全体 keys/values。长上下文 context parallel 还需 ring attention、all-to-all 或 KV exchange 等额外合同。

## 七、Expert parallel：token 路由改变通信分布

MoE 中 router 为每个 token 选 top-$k$ experts。若专家分布在 $E$ 个 ranks：

1. 本地 token 按目标 expert 打包；
2. All-to-All 把 token activation 发到 expert owner；
3. 专家计算；
4. 反向 All-to-All 返回结果并按 gate 权重组合。

通信 bytes 近似与 routed token 数、hidden size、dtype 和 top-$k$ 成正比，但最慢 rank 由最大 token load 决定。capacity factor、drop token、padding 与 load-balancing loss 同时影响质量和性能。

[[S-2022-Rajbhandari-DeepSpeed-MoE]] 提供大规模 expert-parallel 系统证据，但其吞吐数字不脱离模型、拓扑和路由配置使用。

## 八、Hybrid process mesh

常见逻辑坐标可写

$$
(r_{DP},r_{TP},r_{PP},r_{EP},r_{CP}).
$$

但 degree 未必全部独立相乘：sequence parallel 常复用 TP group；expert parallel 可能只在 MoE 层启用，并与 expert-data parallel 形成不同 group；pipeline stage 内才定义 TP/EP 子网格。

必须列出每个 process group 的成员，而不是只写 `DP=8, TP=8, PP=4, EP=8`。

## 九、每个并行节点的通信合同

对每个 collective/point-to-point 记录：

| 字段 | 示例 |
|---|---|
| global/local shape | $[B,S,H]\to[B,S,H/T]$ |
| group | TP group within one PP stage |
| op | AllReduce sum / AllGather / AllToAll |
| phase | forward / backward / router |
| dtype/count | BF16, $BSH/T$ elements |
| layout | contiguous/strided/packed |
| semantics after op | replicated、sharded、partial sum |
| overlap dependency | 哪个 downstream op 等待它 |

只报告通信次数会漏掉 message size，只报告 bytes 会漏 latency 与关键路径。

## 十、图解：把并行名称还原成 process mesh

带着一个问题读图：**某个“TP×PP×DP”配置里，每个设备坐标到底切了哪个 tensor，collective 又局限在哪个通信组？**

![[00-知识库管理/_assets/figures/training-optimization/fig-parallelism-axis-process-mesh-v1.svg|900]]

> [!figure] 图 TRN-62-01　Process mesh、切分轴与 collective 合同
> 来源：自绘机制图；tensor parallel 依据 [[S-2019-Shoeybi-Megatron-LM]]，pipeline 依据 [[S-2019-Huang-GPipe]]，sequence parallel 依据 [[S-2022-Korthikanti-Sequence-Parallelism]]，expert parallel 结合 [[S-2022-Rajbhandari-DeepSpeed-MoE]]。

**怎样读图**：左栏把设备视为 $(d,t,p)$ 坐标而非一个总 world size；右栏逐轴写清被切维度、输入输出 shape、collective 和同步点。真实 hybrid job 还应补 expert/context 轴及各 group 成员。

**图没有证明什么**：网格不表示所有并行轴都正交或代价可相乘，也没有给出最优 mesh；实际最优取决于层 shape、topology、capacity、bubble、负载均衡与 quality contract。

## 十一、选择并行方案的顺序

1. 先由单设备 capacity 判断哪类状态/activation 放不下；
2. 再由单层 shape 找可切分维度；
3. 为每个候选画 collective timeline；
4. 在真实 topology 上估 latency/bandwidth 与 overlap；
5. 检查 global batch、随机性和质量语义是否改变；
6. 用 time-to-quality、peak memory 和 failure rate 决策。

“更多并行维度”不是目标；最好的 mesh 是在质量约束内让关键路径与峰值内存共同可行。
