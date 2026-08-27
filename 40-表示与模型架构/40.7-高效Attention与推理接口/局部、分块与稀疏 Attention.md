---
type: concept
status: draft
area: [architecture, efficient-attention, sparse-attention, locality]
aliases: [Sparse Attention, Local Attention, Block Sparse Attention]
node_id: ARCH-50
prerequisites: ["[[Attention Mask、因果性与可见性合同]]", "[[堆叠卷积、感受野与有效感受野]]", "[[图数据、节点重标号与置换对称性]]"]
related: ["[[高效 Attention 与推理接口 MOC]]", "[[Attention 的二次复杂度、内存与 IO 瓶颈]]", "[[长度外推、位置插值与 RoPE 缩放]]", "[[FlashAttention、精确计算与 IO Awareness]]"]
sources: ["[[S-2019-Child-Sparse-Transformer]]", "[[S-2020-Beltagy-Longformer]]", "[[S-2020-Zaheer-BigBird]]", "[[S-2019-Su-6853-Sparse-Attention]]", "[[S-2023-Su-9431-长度外推与局部注意力]]", "[[S-2023-Su-9844-Transformer-VQ]]"]
exercises: ["[[习题 - 局部、分块与稀疏 Attention]]"]
solutions: ["[[解答 - 局部、分块与稀疏 Attention]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-sparse-attention-pattern-path-kernel-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# 局部、分块与稀疏 Attention

> [!abstract] 核心问题
> Dense attention 把每对 token 都连边；稀疏 attention 选择 relation graph 的子集。真正需要同时回答四件事：删了多少边、信息要几层才能传播、哪些依赖被先验排除、实现是否真的跳过了被删计算。

## 一、从 Mask 改写成 Relation Graph

令允许关系集合为

$$
\mathcal E\subseteq\{(i,j):1\le i,j\le n\}.
$$

对 query $i$ 的邻域记作 $\mathcal N(i)=\{j:(i,j)\in\mathcal E\}$，稀疏 attention 为

$$
o_i=\sum_{j\in\mathcal N(i)}
\frac{\exp(s_{ij})}{\sum_{k\in\mathcal N(i)}\exp(s_{ik})}v_j.
$$

这仍是每行局部 softmax，但归一化集合已改变。即便删掉位置的 dense attention 权重原本很小，重新归一化也会改变所有保留权重。

## 二、Local Window：边数与感受野

双向半窗宽 $w$ 时，内部 token 至多连接 $2w+1$ 个 keys，edge 数约

$$
|\mathcal E|=O(nw).
$$

Causal window 只看最近 $w$ 个历史及自身，约 $O(nw)$。若 $w$ 固定，长度复杂度是线性的。

但单层 token $i$ 只收到距离 $w$ 内信息。堆叠 $L$ 层且窗口不变时，理想最远传播距离至多约 $Lw$。这只是图论 receptive field；真正贡献可能远小于最远可达范围，类似 CNN 的有效感受野。

> [!example] 传播而非直连
> 若 $w=2$，位置 0 的证据要影响位置 10，至少需要 5 层逐段传递。每一步还经历 softmax、value mixing、residual 与非线性，不能把“图上可达”当作“信息无损到达”。

## 三、Dilated、Strided 与 Block Patterns

### 3.1 Dilated / Atrous

让每个 query 连接 $i\pm r,i\pm2r,\ldots$。大步长能快速覆盖远距，却会漏掉某些 residue classes。常将密集局部边与稀疏远程边组合。

### 3.2 Block Sparse

把 token 分成 blocks，只计算选定 block pairs。优势是 GPU 更擅长规则 dense tiles，而不是逐元素稀疏；代价是 block 内可能计算并不需要的边，形成结构 padding。

### 3.3 Global Tokens

Longformer/BigBird 类设计让少量 global tokens 与所有位置相连。任意两点可经 global node 两跳通信，但 global state 也成为容量与带宽瓶颈。若 global token 数 $g=O(1)$，额外 edges 为 $O(ng)$；若 $g\propto n$，线性优势消失。

### 3.4 Random Edges

随机长边可以降低 attention graph 的直径并增加混合，但单个 seed 的连通与覆盖有随机性。理论结果通常要求边数、随机机制、层数与 global nodes 的特定条件，不能推广到任意“稀疏一些”的 mask。

## 四、稀疏图的三份证书

一个 pattern 至少需要：

1. **Edge ledger**：每行/每层实际计算多少 pairs；
2. **Path certificate**：目标依赖从 source 到 target 最短需要几层，是否被 causal 方向允许；
3. **Cut/bottleneck audit**：是否有大量远程信息必须穿过少量 global/block 边。

图神经网络中的 over-squashing 直觉同样适用：图直径短不代表瓶颈宽。

## 五、功能稀疏与系统稀疏

最重要的实现边界是：

```text
dense QK^T -> full n×n scores -> mask -inf -> dense softmax
```

这在数学上实现了 sparse relation，却仍计算/存储 dense matrix。要获得实际收益，需要 block indices、compressed layout 或专用 kernel，让硬件跳过被删 blocks。

不规则 sparsity 还会带来：

- index/metadata bytes；
- 分支与 gather/scatter；
- block padding；
- load imbalance；
- 低 occupancy 与 kernel launch 开销。

因此较少 edge 不保证 wall-clock 较短。

## 六、科学空间怎样帮助理解

[[S-2019-Su-6853-Sparse-Attention]] 很早就用矩阵和关联图解释 local、atrous、sparse patterns，并明确指出“只 mask dense matrix”不会自动提速。这条工程警告至今仍有效。

[[S-2023-Su-9431-长度外推与局部注意力]] 把 local mask 放进长度外推讨论：局部任务上，window 可防止测试时每行候选数暴涨，形成有力基线。但若任务需要窗口外证据，local 成功不能证明远程利用；这正是 ARCH-48 的评测边界。

[[S-2023-Su-9844-Transformer-VQ]] 提供另一种“聚类而非几何窗口”的稀疏/聚合路线：key 被量化到 codebook 后可按 code 汇总。它改变的是 key identity 分辨率，不等同固定局部图，适合用来比较“删边”和“合并关系”的不同误差入口。

## 七、正式图：一张稀疏图必须读出什么

这张图回答什么问题？为什么 edge count、跨层路径和可执行 sparse kernel 缺一不可？

![[00-知识库管理/_assets/figures/architecture/fig-sparse-attention-pattern-path-kernel-v1.svg|900]]

> [!figure] 图 1｜稀疏 Attention 的 pattern—path—kernel 三联图。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_efficient_attention_v1.py]] 生成；矩阵仅为六 token 示意，不对应某篇论文的原图或固定超参数。

**怎样读图**：A 中比较 dense、local、dilated 与 global+local 的非零结构；B 中把单层直连与多层传播分开，并看到 global token 的短路径/瓶颈二面性；C 中确认 dense mask 只改变功能，block indices 加专用 kernel 才可能改变系统成本。

**图没有证明什么**：图没有证明某个 pattern 在任何任务都优于 dense attention，也没有证明随机边或 global token 一定保留全部远程信息；示意 edge 数更少也不保证特定硬件更快，必须测真实 block size、padding、occupancy 和 end-to-end 质量。

## 八、表达理论怎样不被误读

BigBird 一类工作在特定 sparse graph 下给出通用逼近/Turing-completeness 结果。正确解释是：给定足够资源，某些函数存在参数可表示。它没有给出：

- SGD 一定找到该参数；
- 有限深宽所需资源可接受；
- 任意 local-only pattern 都满足相同定理；
- 该 sparse model 在目标 benchmark 必然胜出。

存在性、可训练性、样本效率与 wall-clock 是四个层次。

## 九、位置、Padding 与 Packing 合同

Sparse relation 必须和以下规则共同定义：

- padding token 不得进入邻域或 softmax denominator；
- packed samples 的 blocks 必须隔离；
- causal blocks 内仍要三角 mask，不能因 block 粗化泄漏未来；
- global token 是否双向可见要按 encoder/decoder 分开；
- crop/chunk 边界应使用局部还是跨块 memory，需要显式说明。

## 十、公平比较协议

比较 dense 与 sparse 时至少固定 tokenizer、模型参数、训练 tokens、上下文分布、优化器和精度。分别报告：

- 理论 edge count 与实际 executed tiles；
- attention layer 与 end-to-end latency；
- 峰值显存和 HBM traffic；
- local-only、global-token、random-edge 消融；
- target position 与 source-target distance；
- 删除/移动远程证据的干预测试。

## 十一、证据边界

- 给定 pattern 的 edge 数、最短路：`I`；
- 随机图连通/直径结果：写明概率模型的 `T`；
- 论文任务质量与 kernel 加速：`E`；
- “自然语言主要是局部依赖”：`H`，必须按任务检查；
- 图上可达不等于模型实际利用，长上下文声明仍需 [[位置分辨率、混叠与长度外推评测]]。

## 十二、学习出口

拿到任意 sparse mask，应能算 edge count、最短传播层数、global bottleneck，检查 causal/padding/packing，并判断实现是否真的避免 dense $n^2$ 物化。

