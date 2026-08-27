---
type: solution
status: draft
area: [neural-networks/embedding-output, large-vocabulary, sampled-softmax, hierarchical-softmax, adaptive-softmax]
topic: "[[Sampled、Hierarchical 与 Adaptive Softmax]]"
exercise: "[[习题 - Sampled、Hierarchical 与 Adaptive Softmax]]"
sources: ["[[S-2005-Morin-Bengio-Hierarchical-Softmax]]", "[[S-2015-Jean-Large-Vocabulary-NMT]]", "[[S-2017-Grave-Adaptive-Softmax]]", "[[S-2026-PyTorch-Large-Vocabulary-Loss]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Sampled、Hierarchical 与 Adaptive Softmax

## A

### NN-LVO-A01

Flat full-softmax 对目标 $y$ 的 NLL 是

$$
\ell=-z_y+\log\sum_{j=1}^V e^{z_j}.
$$

训练这个 exact loss 需要目标 logit 和全 $V$ 类 partition；若用标准反向，还要全类概率/等价充分统计量。输出 exact 全词表概率需要全部 $V$ 个归一化 logits。Global top-$k$ 不一定要物化所有概率，但必须精确找出全词表最大 $k$ 个 scores；没有可证明的索引/剪枝时仍需扫描全 $V$。所以“只要 target probability”与“返回全部概率”及“全局搜索”是三份不同计算合同。

### NN-LVO-A02

- Full softmax：对 flat categorical model 精确归一化。
- Sampled softmax：通常是 flat loss/gradient 的候选子集估计；其 sampled-set Softmax 和为 1，不代表原 $V$ 类模型被精确归一化。
- Negative sampling：多个 data-vs-noise binary probabilities 合法，但不直接给一个和为 1 的 $V$ 类 categorical law。
- Hierarchical softmax：对所定义的概率树精确归一化；它不是原 flat-head 参数化的无损实现。
- Adaptive softmax：对 head–tail 分解定义的 adaptive model 精确归一化；full `log_prob` 可恢复其全类概率，但函数族已改变。

“是否归一化”必须连同概率空间和参数化一起说。

### NN-LVO-A03

树路径有顺序依赖与不规则访存，难以形成高利用率大 GEMM；batch 中 tokens 走不同路径会分支发散；节点参数 gather、kernel launch 与树索引有固定开销；平衡只控制深度，不控制缓存命中和分片通信；dense head 可利用高度优化的矩阵核；生成时 global top-$k$ 还可能展开许多分支。因此标量决策数的渐近式不能直接推出硬件 wall time。

## B

### NN-LVO-B01

$Z=1+2+3=6$。单样本估计的取值为

$$
\widehat Z=
\begin{cases}
1/(1/2)=2,&p=1/2,\\
2/(1/3)=6,&p=1/3,\\
3/(1/6)=18,&p=1/6.
\end{cases}
$$

所以

$$
\mathbb E\widehat Z=\tfrac12(2)+\tfrac13(6)+\tfrac16(18)=6.
$$

但

$$
\mathbb E\log\widehat Z
=\tfrac12\log2+\tfrac13\log6+\tfrac16\log18
\approx1.4256
<\log6\approx1.7918.
$$

这个小例子直接展示：partition estimate 无偏，不等于 log-partition 无偏。

### NN-LVO-B02

路径概率

$$
P(w\mid h)=0.8\times0.7\times0.9=0.504,
$$

NLL 为

$$
-\log0.504\approx0.6852.
$$

只在最后一步走相反分支的 sibling leaf 概率为

$$
0.8\times0.7\times(1-0.9)=0.056.
$$

它们共享前两段 probability mass，这正是树参数共享的统计结构。

### NN-LVO-B03

Head 成本为 $2000+4=2004$。期望 tail 成本：

$$
0.08(1000)+0.05(2000)+0.02(4000)+0.01(8000)=340.
$$

所以总期望约为

$$
2004+340=2344
$$

个 labels，是 full 50000 的约 $50000/2344\approx21.33$ 倍缩减。它只是一项 label-count proxy；tail dimensions、同 batch 多 cluster、kernel 与访存仍未计入。

## C

### NN-LVO-C01

$\log x$ 在 $x>0$ 上严格凹。Jensen 不等式给出

$$
\mathbb E\log\widehat Z
\le\log\mathbb E\widehat Z
=\log Z.
$$

若期望存在，严格凹函数取等号当且仅当 $\widehat Z$ 几乎处处为常数；例如 proposal 与未归一化目标完全匹配，使每个 importance weight 相同。一般采样有方差，所以严格小于。Loss 包含 $\log Z$，且 gradient 涉及估计量比值与参数相关采样项；对 $Z$ 的无偏性不能穿过非线性，必须对具体 estimator 重新推导 bias/consistency。

### NN-LVO-C02

对任意节点 $n$，定义 $S(n)$ 为从 $n$ 出发到其子树所有 leaves 的条件概率和。若 $n$ 是叶，空路径概率为 1，所以 $S(n)=1$。若 $n$ 是内部节点，左右子节点为 $l,r$，归纳假设给出 $S(l)=S(r)=1$，于是

$$
S(n)=P(l\mid n,h)S(l)+P(r\mid n,h)S(r)
=P(l\mid n,h)+P(r\mid n,h)=1.
$$

有限树自 leaves 向上归纳至根，即得全部叶概率和为 1。证明只用局部归一化和完整叶覆盖，不要求左右子树等深，故也覆盖不平衡树。

### NN-LVO-C03

高频词 $w\in\mathcal H$ 时

$$
P(w\mid h)=P_{\rm head}(w\mid h).
$$

若 $w\in C_g$，

$$
P(w\mid h)=P_{\rm head}(C_g\mid h)P_g(w\mid C_g,h).
$$

Head 对每个样本都算，成本 $C_{\rm head}$；cluster $g$ 只在 target 落入它时计算，该事件概率为 $\pi_g$，故全期望公式给出

$$
\mathbb E C=C_{\rm head}+\sum_g\pi_gC_g.
$$

它遗漏类别维度对应的 hidden projection、batch 中 unique clusters、矩阵形状、kernel launch、缓存/带宽、参数分片通信、full log-prob evaluation 与 global top-$k$ 解码。

## D

### NN-LVO-D01

必须明确 $q$ 是 with- 还是 without-replacement、修正项用 $Kq(j)$ 还是 expected count、重复类别是保留多项还是合并并乘 multiplicity。采到正类时应删除、当作额外 occurrence，还是使用 accidental-hit correction，也要固定；不同选择改变 loss。小词表测试可取 $V=3,K=2$，枚举所有有序样本对，逐一手算 candidate multiset、corrected logits、loss 与 gradient，再按采样概率求精确期望，与实现的 Monte Carlo 均值和 full-softmax gradient 比较。还要覆盖 $q_j=0$、重复负类、两次正类与极端 logits。

### NN-LVO-D02

Adaptive rows/cluster gates 按旧 ID 的频率顺序训练。新 tokenizer 重排后，同一个整数指向不同 token，模型 shape 仍合法，却会把词义、head/tail membership 和 cluster conditional row全部错配。Checkpoint 应保存 tokenizer hash、token→ID 列表、frequency ordering、cutoffs、div value、每组 dimensions 与参数 row checksums；加载时强制比对。合法迁移需先构造 old-ID→new-ID map，同时重排 input/output rows、bias、tail rows、optimizer/master state、quantization metadata 和 generation lists，再做已知 tokens 的 round-trip 与 logit-equivalence test。

### NN-LVO-D03

最低限度应在同一 held-out tokenization 上报告 exact full/adaptive NLL 与 perplexity，并把 training surrogate 单独列出；比较相同训练 token、硬件、有效 batch、调参预算下的 wall time、峰值内存和通信。生成侧要测 candidate/global top-$k$ recall、decode tokens/s、P50/P95 latency、质量和 rare-token buckets。再报告采样 $K/q$、accidental-hit policy、full-eval 额外成本和多随机种子。没有这些，训练 loss 的数值甚至未必与 full baseline 同量纲，无法支持 perplexity或 decoding 结论。

## E

### NN-LVO-E01

Natural protocol 允许各方法使用推荐的 proposal、树、cutoffs、tail dimensions 与调参，固定数据、tokenizer、硬件和训练 token，比较最佳 quality–memory–time Pareto。Matched-contract protocol 尽量固定 backbone、总参数/计算预算、optimizer、batch 与 exact evaluation；若函数族无法相同，就明确把差异标为结构效应。两条轨道都报告 exact NLL、训练 surrogate、频率桶质量、top-$k$、参数/optimizer bytes、训练/解码吞吐、P95 latency、峰值内存、collective bytes、energy/time 和多种子区间。Full-eval 与建树/采样器成本也应计入。

### NN-LVO-E02

令候选集合为 $C(h)$。若 gold token 不在 $C(h)$，任何 reranker 都无法选中它，所以 end-to-end recall 不超过 candidate recall；若任务是复原 exact global top-$k$，最终 recall@k 也受 oracle top-$k$ 被候选覆盖的比例上限。应分别报告 candidate recall、conditional reranker quality 和总质量。延迟账包括 query encoding、索引查找、网络/分片通信、候选去重、候选 row gather、rerank、top-$k$ merge、fallback full scan 及索引更新；P95/P99 比均值更能暴露长尾。

### NN-LVO-E03

Hierarchical softmax 的 leaves 的确对树模型精确归一化，这里的 exact 是“无 sampling bias 地计算树概率”。但它用路径 Bernoulli 乘积替代 flat $w_j^\mathsf Th$ 的单次共享归一化，函数族与梯度共享结构随树改变；训练目标是 tree-model NLL，不是对任意既有 flat logits 的代数快捷计算。树的平衡、语义/频率组织还引入统计归纳偏置。最后，$O(\log V)$ 只计路径节点，不保证分支式小算子胜过 dense GEMM。故“归一化精确”成立，“原 flat model 的 exact 实现”和“必然更快”均不成立。
