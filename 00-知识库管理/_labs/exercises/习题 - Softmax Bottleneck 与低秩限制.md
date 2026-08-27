---
type: exercise
status: draft
area: [neural-networks/embedding-output, softmax-bottleneck, rank]
topic: "[[Softmax Bottleneck 与低秩限制]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Softmax Bottleneck 与低秩限制]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Softmax Bottleneck 与低秩限制

## A

### NN-SBR-A01
对 $N$ 个 contexts、词表大小 $V$、hidden width $d$，写出 $H,W,b,Z,L$ 的 shape，并说明 $L$ 与 $Z$ 每行相差什么。

### NN-SBR-A02
为什么“Softmax 对单个严格正概率向量是满射”与“共享线性 output head 存在 bottleneck”不矛盾？分别指出两句话量化了哪些对象。

### NN-SBR-A03
写出 vocabulary centering matrix $C_V$ 与 context centering matrix $J_N$。各自消除了哪一种不可辨识或共享成分？

## B

### NN-SBR-B01
取 $N=V=4$，目标分布满足 $P_{ii}=0.7$、$P_{ij}=0.1 (i\ne j)$。证明每行归一化，写出 $L=\log P$，并求 $J_4LC_4$ 的秩与非零奇异值。

### NN-SBR-B02
若 $d=2$、output bias 存在，分别给出 $\operatorname{rank}(LC_V)$ 与 $\operatorname{rank}(J_NLC_V)$ 的上界。为什么二者相差至多 1？

### NN-SBR-B03
设 projected tying 的 logits 为 $Z=H P^\mathsf TE^\mathsf T+\mathbf1b^\mathsf T$，其中 $H\in\mathbb R^{N\times d_h}$、$P\in\mathbb R^{d_e\times d_h}$、$E\in\mathbb R^{V\times d_e}$。给出双中心化 log-probability 的秩上界。

## C

### NN-SBR-C01
从 $L=Z-a\mathbf1_V^\mathsf T$ 出发，完整推导
$$
J_NLC_V=J_NHW^\mathsf TC_V
$$
以及 $\operatorname{rank}(J_NLC_V)\le d$。

### NN-SBR-C02
设严格正目标表 $P^*$ 的 $D^*=J_N(\log P^*)C_V$ 满足 $\operatorname{rank}(D^*)\le d$。在“每个 context 的 hidden row 可自由选择”的有限表模型中，构造一个精确表示，说明为什么该条件也是充分的。

### NN-SBR-C03
对 $D^*=U\Sigma V^\mathsf T$，写出最佳 rank-$d$ Frobenius approximation 及残差。为什么这个残差不能不加条件地称为 cross-entropy 或 perplexity 下界？

## D

### NN-SBR-D01
你从语料计数得到一个稀疏 context-by-token 表，很多单元为零。设计 empirical-rank 估计流程，必须处理 smoothing、context 聚合、频率权重、样本噪声和 tokenizer 版本。

### NN-SBR-D02
某实验发现目标矩阵的经验秩高于 hidden width，便宣称训练 loss 的全部差距都由 Softmax bottleneck 导致。指出至少四个不能由该观察排除的替代原因，并给出诊断对照。

### NN-SBR-D03
比较 untied、direct-tied 与 rank-$r$ projected-tied output heads 的 rank budget。设计代码级测试，避免只从配置中的 `hidden_size` 猜测真实预算。

## E

### NN-SBR-E01
设计 standard softmax、增大 $d$、Mixture of Softmaxes 三组研究实验。要求区分函数类、参数/FLOP、优化难度、exact NLL、校准与 wall time。

### NN-SBR-E02
反驳：“只要把 output bias 加上，任何高秩条件分布都能表示。”必须用双重中心化解释 bias 能改变什么、不能改变什么。

### NN-SBR-E03
提出一个 synthetic benchmark，使目标 centered log-ratio rank 可控，并说明如何分别验证 rank barrier、encoder barrier 与优化 barrier。
