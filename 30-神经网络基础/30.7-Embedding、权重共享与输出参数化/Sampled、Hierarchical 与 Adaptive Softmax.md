---
type: comparison
status: draft
area: [neural-networks/embedding-output, large-vocabulary, sampled-softmax, hierarchical-softmax, adaptive-softmax]
aliases: [Large Vocabulary Output Methods, 大词表 Softmax]
node_id: NN-54
prerequisites: ["[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[条件概率、全概率与 Bayes 公式]]", "[[渐近记号、增长率与复杂度]]"]
related: ["[[Softmax Bottleneck 与低秩限制]]", "[[Embedding Lookup、稀疏梯度与参数规模]]", "[[交叉熵与 KL 散度]]", "[[遮蔽预测、Teacher–Student 与自监督目标]]"]
sources: ["[[S-2005-Morin-Bengio-Hierarchical-Softmax]]", "[[S-2015-Jean-Large-Vocabulary-NMT]]", "[[S-2017-Grave-Adaptive-Softmax]]", "[[S-2026-PyTorch-Large-Vocabulary-Loss]]", "[[S-2013-Mikolov-Distributed-Representations]]"]
exercises: ["[[习题 - Sampled、Hierarchical 与 Adaptive Softmax]]"]
solutions: ["[[解答 - Sampled、Hierarchical 与 Adaptive Softmax]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-large-vocabulary-output-methods-v2.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# Sampled、Hierarchical 与 Adaptive Softmax

> [!abstract] 本章主问题
> 大词表方法并不是同一种“近似 Softmax”。Full softmax 精确计算 flat categorical model；sampled methods 只看候选子集并近似训练目标或梯度；hierarchical softmax 对一个树模型做精确归一化；adaptive softmax 利用长尾频率改变层次与维度，使期望成本下降。必须先问“近似了什么”，再比较速度和质量。

## 课程位置与两遍学习路线

- **承接什么：** NN-52 固定了 exact flat Softmax 的概率与 NLL，NN-53 区分了 output head 的表达限制；
- **本页解决什么：** 把 sampling estimator、binary noise objective、tree factorization 与 frequency-adaptive factorization 分成四种不同统计对象；
- **后续为何需要：** padding/词表事务和 embedding 压缩都会影响 class IDs、分桶与参数布局，大词表方案不能脱离 tokenizer 和部署合同讨论。

**第一遍只问“概率对象是否相同”。** 对每个方法写出 normalization domain、训练 loss、exact evaluation 与 decoding 所需工作。

**第二遍再比较成本。** 记录 target-dependent candidate count、matrix shape、sampling/routing、GPU occupancy、通信和 full-vocabulary evaluation，而不是只比较 $O(V)$ 与 $O(\log V)$。

### 问题链

1. importance estimator 对 $Z$ 无偏，为什么对 $\log Z$ 和 NLL 仍可能有偏？
2. sampled softmax、negative sampling 与 NCE 的优化对象分别是什么？
3. hierarchical softmax 为什么是新树模型的 exact probability，而非原 flat head 的无损加速？
4. adaptive softmax 节省的是最坏成本还是按 token frequency 加权的期望成本？
5. 训练时只看目标子集，为什么 exact perplexity 与 global top-$k$ 仍可能恢复全词表成本？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal E_\square$ 中证明单样本 importance estimator 满足 $\mathbb E\widehat Z=Z$，却得到 $\mathbb E\log\widehat Z=\log4+5/4<\log Z$，就已掌握本页最关键的对象边界。

## 符号与对象账本

| 方法 | normalization / loss 对象 | exact 性质 | 主要成本变量 |
|---|---|---|---|
| full Softmax | flat $V$ 类 categorical NLL | 对 flat head exact | $Vd$、$BTV$ |
| sampled method | proposal 下的 loss/gradient estimator | 依具体修正，常有 bias/variance | $K$、proposal、去重/路由 |
| negative sampling | data-vs-noise binary losses | 不是 normalized $V$ 类 NLL | negatives 与 noise law |
| hierarchical Softmax | root-to-leaf conditional product | 对树模型 exact | path length、branching/kernel |
| adaptive Softmax | head gate × target-tail conditional | 对 adaptive model exact | cutoff、frequency mass、tail width |

### 贯穿算例 $\mathcal E_\square$：无偏 Partition 估计仍产生有偏 NLL

沿用 NN-52 的

$$
z=(1,1,1,2),
\qquad
Z=3\mathrm e+\mathrm e^2=\mathrm e(3+\mathrm e).
$$

从四类中均匀采一个 $s$，即 $q(s)=1/4$，并令

$$
\widehat Z=\frac{e^{z_s}}{q(s)}=4e^{z_s}.
$$

前三类各给 $4\mathrm e$，目标类给 $4\mathrm e^2$，所以

$$
\mathbb E\widehat Z
=\frac34(4\mathrm e)+\frac14(4\mathrm e^2)
=Z.
$$

但

$$
\boxed{
\mathbb E\log\widehat Z
=\frac34\log(4\mathrm e)+\frac14\log(4\mathrm e^2)
=\log4+\frac54
\approx2.636294
},
$$

而

$$
\log Z=1+\log(3+\mathrm e)\approx2.743668.
$$

Jensen gap 为

$$
\boxed{
\log Z-\mathbb E\log\widehat Z
=\log\frac{3+\mathrm e}{4}-\frac14
\approx0.107374>0
}.
$$

对目标 $y=3$，把 $\log\widehat Z$ 直接代入 NLL 会得到期望 $\log4-3/4\approx0.636294$，低于 exact NLL $0.743668$。这不是“采样更好”，而是优化/估计对象已经有偏。

## 核心公式七问：大词表方法的概率—成本合同

$$
\boxed{
(\text{model law},\text{training estimator},\text{exact eval},\text{decoding},\text{system cost})
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 在声称加速前确认统计对象是否仍与 full Softmax 相同 |
| 对象 | flat、sampled、binary、tree 或 adaptive categorical parameterization |
| 来路 | 大词表 projection/normalization 的计算与内存压力 |
| 步骤 | 写模型 law→写训练 estimator→判 bias/variance→定义 exact eval→测 decoding/system |
| 读法 | 候选数下降不自动保留目标，也不自动转化为 wall time |
| 检查 | 小词表 exact enumeration、proposal coverage、leaf-sum、frequency reorder 与 full-log-prob |
| 去路 | sampled training、retrieval-augmented vocab、hierarchical classifier 与 adaptive head |

### AI / 系统对应

LLM 训练可以用 fused full cross-entropy、vocabulary parallelism 或 sampling；检索系统则可能先召回候选再局部归一化。二者都必须说明局部分母是否用于训练概率、候选选择是否依赖 target，以及部署时如何计算全局 top-$k$。缺少这些信息的“Softmax 加速”不可复现。

## 一、学习目标

读完本节，你应能：

1. 写出 full-vocabulary loss 与 $O(Vd)$ 成本账；
2. 解释 importance estimate 对 partition 可无偏、取 log 后仍有偏；
3. 区分 sampled softmax、negative sampling 与 NCE；
4. 证明合法 hierarchical tree 的叶概率和为 1；
5. 写出 adaptive softmax 的 head–tail probability；
6. 计算一个 frequency-weighted expected cost；
7. 区分训练、exact evaluation 与 decoding 的成本；
8. 设计兼顾 NLL、召回、通信和 wall time 的公平验收。

## 二、Full Softmax 是基准合同

对 hidden $h\in\mathbb R^d$、词表 rows $w_j$ 与 bias $b_j$：

$$
z_j=w_j^\mathsf Th+b_j,
$$

目标为 $y$ 时 exact negative log-likelihood 是

$$
\boxed{
\ell_{\mathrm{full}}
=-z_y+\log\sum_{j=1}^V e^{z_j}
}.
$$

每个位置要形成 $V$ 个 logits，dense projection 约为 $O(Vd)$ MAC，normalization 另有 $O(V)$ max/sum/exp。对 $BT$ 个位置，logit tensor 可能达到 $BTV$。

它的优点是对象清楚：

- 所有类别共享一个 flat normalization；
- loss 是精确 categorical NLL；
- gradient 是 $p-y$；
- exact perplexity 与训练目标一致。

任何加速方案都应以这个概率/成本合同为参照，而不是只与一个未优化实现比较。

## 三、Sampling 的第一个陷阱：Unbiased $Z$ 不等于 Unbiased $\log Z$

令 partition function

$$
Z=\sum_{j=1}^V e^{z_j}.
$$

从 proposal $q$ 独立采样 $s_1,\ldots,s_K$，可构造

$$
\widehat Z
=\frac1K\sum_{k=1}^K\frac{e^{z_{s_k}}}{q(s_k)}.
$$

若 $q(j)>0$ 覆盖所有类别，则

$$
\mathbb E[\widehat Z]=Z.
$$

但是 loss 需要 $\log Z$。由 Jensen inequality：

$$
\mathbb E[\log\widehat Z]
\le\log\mathbb E[\widehat Z]
=\log Z.
$$

所以“partition estimator 无偏”不能推出“log-likelihood 或 gradient 无偏”。实际 sampled-softmax variants 还会处理必含正样本、重复样本、without-replacement、accidental hits 和 correction logits；必须按具体实现推导。

## 四、Sampled Softmax 的一般结构

一个典型训练步骤只构造集合

$$
S=\{y\}\cup\{s_1,\ldots,s_K\},
\qquad K\ll V,
$$

并对 sampled logits 做 proposal correction，例如使用

$$
\widetilde z_j=z_j-\log(Kq(j))
$$

的某种变体，再在 $S$ 上归一化。

它可把 output-row 读取与局部 matmul 从 $V$ 缩到约 $K+1$，但代价包括：

- estimator bias/variance；
- proposal sampling 与去重；
- 高频 accidental hits；
- 分布式 sampled-row routing；
- 训练目标和 exact full NLL 的偏离；
- rare-class coverage 不稳定。

$K\to V$ 或使用特定精确修正时可逼近 full objective，但不能只凭名称断言等价。

## 五、Negative Sampling 不是小型 Full Softmax

经典 negative sampling 常优化

$$
\ell_{\mathrm{neg}}
=-\log\sigma(s_y)
-\sum_{k=1}^K\log\sigma(-s_{n_k}).
$$

这是“数据 pair vs noise pair”的多个 binary logistic objectives，不要求所有 $V$ 类概率和为 1。它可学习有用表示，却不是同一个 flat categorical NLL。

Noise-Contrastive Estimation（NCE）又是另一份合同：把未归一化模型与已知 noise distribution 做分类，可连同 normalization constant 一起估计。在某些极限/条件下与 MLE 有联系，但不能把 negative sampling、NCE 与 sampled softmax 三者互换。

## 六、Hierarchical Softmax 改写概率模型

把 $V$ 个 tokens 放在一棵二叉树的 leaves。对 token $w$，从根到叶的路径为内部节点

$$
n_1(w),\ldots,n_{m(w)}(w),
$$

方向编码 $s_t(w)\in\{-1,+1\}$。定义局部 decision：

$$
P(s_t\mid h,n_t)
=\sigma\!\left(s_t u_{n_t}^\mathsf Th\right).
$$

词概率为

$$
\boxed{
P(w\mid h)
=\prod_{t=1}^{m(w)}
\sigma\!\left(s_t(w)u_{n_t(w)}^\mathsf Th\right)
}.
$$

只计算路径上的 $m(w)$ 个 decisions。平衡树时

$$
m(w)=O(\log V).
$$

## 七、为什么所有叶概率和为 1

在每个内部节点，左右 conditional probabilities 满足

$$
P(L\mid n,h)+P(R\mid n,h)=1.
$$

从任意 node 出发，定义其子树所有叶的总条件概率。叶节点总和为 1；若左右子树各自条件和为 1，则父节点下的总和是

$$
P(L\mid n,h)\cdot1
+P(R\mid n,h)\cdot1
=1.
$$

由树结构归纳，根节点下全部 leaves 概率和为 1。

所以 hierarchical softmax 对**树模型**是 exact normalized probability，不是对原 flat logits 的随机近似。

## 八、Tree 选择改变统计与系统

树决定哪些 tokens 共享早期 decisions：

- balanced tree 控制最坏 path length；
- Huffman/frequency tree 降低期望 path length；
- semantic tree 让相似词共享上层，但先验可能错误；
- learned tree 引入离散结构优化与稳定性问题；
- GPU 上逐路径分支未必比大矩阵乘法高效。

因此 $O(\log V)$ 是标量节点数，不是端到端 wall time 保证。

## 九、Adaptive Softmax 的 Head–Tail 分解

把高频 tokens 放进 head，低频 tokens 分成 $G$ 个 tail clusters。head categories 包含：

$$
\mathcal H=\{\text{高频词}\}\cup\{C_1,\ldots,C_G\}.
$$

若 $w$ 是高频词：

$$
P(w\mid h)=P_{\mathrm{head}}(w\mid h).
$$

若 $w\in C_g$：

$$
\boxed{
P(w\mid h)
=P_{\mathrm{head}}(C_g\mid h)
P_g(w\mid C_g,h)
}.
$$

训练某个 rare target 时，只展开它所在的 $C_g$。进一步让 tail dimension 随频率下降：

$$
d_g=\left\lfloor\frac{d}{\text{div}^{\,g}}\right\rfloor,
$$

就同时减少参数与 cluster matmul 成本。

## 十、Expected Cost 而非最坏 Cost

设 head 总 categories 为 $H$，cluster $g$ 的局部计算成本为 $C_g$，目标落在该 cluster 的概率质量为 $\pi_g$。粗略期望账本：

$$
\boxed{
\mathbb E[C]
=C_{\mathrm{head}}
+\sum_{g=1}^G\pi_gC_g
}.
$$

手算例：$V=10{,}000$，head 有 1000 个常用词和 3 个 cluster gates，因此每个 target 先评估 1003 个 head categories。若总 tail mass 为 $0.10$，被访问的 tail 平均含 3000 个词，则按“评估 label 数”近似：

$$
1003+0.10\times3000=1303.
$$

这显著小于 10000，但仍不是 FLOP 或 wall time：tail dimension、batch 中访问多少 clusters、kernel launch 和 shard placement 都会改变真实结果。

## 十一、四类方法的对象表

| 方法 | 训练时计算 | 概率是否归一化 | 相对 flat model 改变什么 |
|---|---|---|---|
| Full softmax | 全 $V$ logits | 是 | 基准 |
| Sampled softmax/IS | 正样本 + $K$ candidates | 视 estimator/目标而定 | 常近似 flat loss/gradient |
| Negative sampling | $K+1$ binary scores | 不给 flat categorical normalization | 换成 data-vs-noise objective |
| Hierarchical softmax | root-to-leaf path | 对树模型是 | 改写 factorization/共享结构 |
| Adaptive softmax | head + target tail | 对 adaptive model 是 | 频率层次 + 变维参数化 |

“exact”后面必须跟对象：exact flat softmax、exact tree probability 或 exact adaptive probability不是同一句话。

## 十二、训练、评估与解码必须分开

### 12.1 训练

可只需 target probability 或 sampled candidates。主要看 gradient bias/variance、吞吐和 optimizer row traffic。

### 12.2 Exact NLL / Perplexity

若声称 full-vocabulary categorical NLL，必须对同一概率模型精确归一化。sampled training 可在 evaluation 时恢复 full softmax；adaptive implementation 也可用 full `log_prob` 遍历所有 clusters，但成本回升。

### 12.3 Decoding / Top-k

生成需要找高概率 tokens。即使单个 target loss 很便宜，global top-k 仍可能需要：

- 展开多个 clusters；
- candidate retrieval + rerank；
- 上界剪枝；
- 分片 top-k merge。

只报告 teacher-forced training speed 不能证明 autoregressive decoding 更快。

## 十三、实现与分布式审计

大词表系统至少记录：

1. 每步 unique output rows；
2. proposal sampling/去重时间；
3. head/tail batch occupancy；
4. matmul shapes 与 achieved FLOP/s；
5. parameter/optimizer shard bytes；
6. all-to-all、all-gather 或 top-k collective bytes；
7. full-eval 频率与额外时间；
8. rare-token loss、coverage 和 tail latency。

某官方实现要求 class IDs 按频率排序并由 `cutoffs` 分桶；这属于 checkpoint/tokenizer contract。词表重排而不重排参数会 silent corruption。

## 十四、公平实验协议

同时提供两条轨道：

### Natural Protocol

每种方法使用其推荐结构与调参，在相同数据、token 数和硬件上比较 Pareto frontier。

### Matched Contract

尽可能固定 hidden backbone、词表、训练 token、optimizer budget 与 evaluation probability，报告：

- exact full/adaptive NLL；
- sampled training surrogate；
- top-k/rare-word quality；
- parameters 与 optimizer state；
- train tokens/s 与 decode tokens/s；
- peak memory、通信和 energy/time。

若函数类不同，就明确写“结构—效率权衡”，不能宣称纯 kernel speedup。

## 十五、常见误区

1. **“采样 $K$ 类就是 exact $K$-class softmax”**：它不是原 $V$-class normalization；
2. **“$\widehat Z$ 无偏，所以 $\log\widehat Z$ 无偏”**：Jensen 已否定；
3. **“negative sampling 是 sampled softmax 的别名”**：概率目标不同；
4. **“hierarchical 是原 flat head 的无损实现”**：它改变参数共享；
5. **“$O(\log V)$ 一定比 GEMM 快”**：算法计数不等于硬件效率；
6. **“adaptive 对均匀类别同样好”**：它依赖长尾质量；
7. **“训练快就代表 decoding 快”**：目标路径与 global top-k 不同。

## 十六、图：Full、Sampled、Tree 与 Adaptive

先看图回答：为什么 balanced tree 的 14 个 decisions 不能直接与 dense 10000 logits 比 wall time？为什么 hierarchical probability 是 exact，而 sampled estimate 仍可能有偏？adaptive 节省的是最坏成本还是期望成本？

![[00-知识库管理/_assets/figures/neural-networks/fig-large-vocabulary-output-methods-v2.svg|900]]

> [!figure] 图 30.7-06　大词表输出方法的候选数、概率树与期望成本
> 左栏用同一 toy vocabulary 对比 full、sample 与 balanced-tree 的标量候选/决策数；中栏展示合法二叉树的路径概率乘积；右栏用 head 1003 categories、tail mass 0.10 手算 adaptive expected labels 1303。来源：依据 Morin–Bengio、Jean et al.、Grave et al. 与 PyTorch 当前接口绘制；由 [[00-知识库管理/_labs/code/plot_embedding_output_advanced_v2.py]] 确定性生成。

**怎样读图**：先确定每栏优化的是 flat loss、sampling estimator 还是新概率 factorization；随后看 target-dependent compute，最后把矩阵 shape、batching 和 full-eval/decoding 补回成本账。

**图没有证明什么**：图不证明 tree 在任意 GPU 上最快，也不证明 toy expected labels 等于 FLOP，更不证明 sampled surrogate 的数值可直接当作 exact perplexity。

## 十七、最小验收

1. 写出 full softmax NLL 与成本；
2. 证明 $\widehat Z$ 可无偏而 $\log\widehat Z$ 有偏；
3. 区分 sampled softmax、negative sampling 与 NCE；
4. 推导 tree path probability 并证明 leaves sum to 1；
5. 写出 adaptive head–tail probability；
6. 复算 1303 的 expected-label toy；
7. 分开训练、exact evaluation 与 decoding；
8. 设计 quality/memory/communication/wall-time 公平协议。

> [!summary]
> 大词表加速必须先声明概率对象。Sampling 通常近似 flat loss 或 gradient；hierarchical/adaptive 对重新参数化的概率模型做精确局部归一化；negative sampling 则是另一种 binary objective。复杂度符号只给候选规模，最终收益还由频率、矩阵维度、batch occupancy、通信与 evaluation/decoding 合同决定。

- [[Embedding、权重共享与输出参数化 MOC]]
- [[习题 - Sampled、Hierarchical 与 Adaptive Softmax]]
- [[解答 - Sampled、Hierarchical 与 Adaptive Softmax]]
