---
type: solution
status: draft
area: [architecture, efficient-attention, sparse-attention, graph]
topic: "[[局部、分块与稀疏 Attention]]"
exercise: "[[习题 - 局部、分块与稀疏 Attention]]"
sources: ["[[S-2019-Child-Sparse-Transformer]]", "[[S-2020-Beltagy-Longformer]]", "[[S-2020-Zaheer-BigBird]]", "[[S-2019-Su-6853-Sparse-Attention]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - 局部、分块与稀疏 Attention

## A. 识别与复述

### ARCH-SPARSE-A01
令顶点是 tokens，有向边 $j\to i$ 表示 query $i$ 可读 key/value $j$。则
$$o_i=\sum_{j\in\mathcal N(i)}\frac{e^{s_{ij}}}{\sum_{k\in\mathcal N(i)}e^{s_{ik}}}v_j.$$
$\mathcal N(i)$ 同时决定分子可用信息与分母归一化全集；删除边后不能保留原 dense 分母。

### ARCH-SPARSE-A02
Local 保留邻近连续性；dilated/strided 用相同量级边覆盖更远距离；block-sparse 把规则对齐硬件块；global tokens 建立短路径/枢纽；random edges 改善连通性和图直径。它们可组合，但机制与风险不同。

### ARCH-SPARSE-A03
若仍计算完整 $n\times n$ score，再把不可见位置设 $-\infty$，输出函数稀疏但算术、存储和 HBM 搬运可能仍是 dense。系统稀疏还要求压缩/块索引与能跳过零块的专用 kernel。

## B. 手算与建模

### ARCH-SPARSE-B01
$\mathcal N(0)=\{0,1,2\}$，$\mathcal N(5)=\{3,4,5,6,7\}$，$\mathcal N(11)=\{9,10,11\}$。边数为 $3+4+8\cdot5+4+3=54$；中间 8 行各 5 条，边界逐渐截断。

### ARCH-SPARSE-B02
令位置从 0 开始，$|\mathcal N(i)|=\min(i+1,4)$。总边数
$$1+2+3+4+6\cdot4=34.$$

### ARCH-SPARSE-B03
四个 blocks 记为 0–3：0 看 0；1 看 0,1；2 看 1,2；3 看 2,3。共有 $1+2+2+2=7$ 个非零 block pairs；每对最多 $4^2=16$ 个 token pairs，所以上界 112。若还施加 token-level causal mask，实际数会更少。

## C. 推导与证明

### ARCH-SPARSE-C01
单层一条边最多跨 $r$ 个位置。任一 $L$ 层路径由 $L$ 条边组成，用三角不等式，位移绝对值至多各边位移之和 $Lr$。边界只会缩小可达集合；这给上界，不保证所有该范围位置都可达。

### ARCH-SPARSE-C02
若任意普通 token $a$ 能把信息送到 global $g$，且 $g$ 能送到 $b$，则路径 $a\to g\to b$ 长度为 2。可达性只是存在有限维通道；很多 token 的信息在 $g$ 处聚合会出现容量/优化瓶颈，所以不能推出无损传输。

### ARCH-SPARSE-C03
Dense 权重为 $e^{s_j}/\sum_{k\in D}e^{s_k}$。删除 $D\setminus N$ 后保留原权重，其和为 $\sum_{j\in N}e^{s_j}/\sum_{k\in D}e^{s_k}<1$（只要删去有限 score）。Sparse softmax 应除以 $\sum_{k\in N}e^{s_k}$ 才是邻域上的概率分布。

## D. 边界、反例与纠错

### ARCH-SPARSE-D01
取 8 个点、每点出度 1。Pattern A 为长度 8 的有向环，直径 7；Pattern B 可把若干边集中到中心形成双向星状近似（在相同总边预算下补方向），直径约 2–3。边数相近，远程路径完全不同，故还要报告连通、直径、瓶颈与多层可达性。

### ARCH-SPARSE-D02
两个 causal blocks，每块两个 tokens。若第一个 query block 的 block mask 错误允许读取第二 key block，那么位置 0/1 可见位置 2/3。block adjacency 的矩形 shape 都合法，只有检查 token-level 条件 $j\le i$ 或做未来 token 扰动测试才能发现泄漏。

### ARCH-SPARSE-D03
$O(nw)$ 只数有效边；不规则 gather、index memory、padding 到 block、低 occupancy 和 launch 常数可能让小/中长度 sparse kernel 更慢。Dense GEMM/FlashAttention 高度优化，真实 crossover 依 block size、dtype、shape 与硬件。

## E. AI 迁移

### ARCH-SPARSE-E01
每个 token 看左右局部窗口，标题/问题 token/段落摘要作为 global tokens；正文到问题经 global 建短路径。需验证 global 选择规则、任意答案证据的图距离与对 global 数的敏感性。跨段精确匹配、多个分散证据和 global bottleneck 是重点失败任务。

### ARCH-SPARSE-E02
用同一 Q/K/V 构造 dense score，加完全相同的 token-level mask 得 reference；比较 forward 与 Q/K/V gradients。覆盖 causal 边界、首尾不满 block、left/right padding、packed sequence 隔离、全 mask 行、global token、不同长度与非整 block，并设未来扰动负对照。

### ARCH-SPARSE-E03
控制参数量、训练 token、上下文/有效 token、optimizer、seed、dtype 和硬件；分别扫 window/global/random budget。报告有效边与 padded block 边、图路径指标、kernel 时间、端到端训练/推理、显存、短长任务质量和多 seed。Dense baseline 使用同等成熟 kernel，不能只比理论 FLOPs。
