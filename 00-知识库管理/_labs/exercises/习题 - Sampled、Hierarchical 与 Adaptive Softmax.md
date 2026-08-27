---
type: exercise
status: draft
area: [neural-networks/embedding-output, large-vocabulary, sampled-softmax, hierarchical-softmax, adaptive-softmax]
topic: "[[Sampled、Hierarchical 与 Adaptive Softmax]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Sampled、Hierarchical 与 Adaptive Softmax]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Sampled、Hierarchical 与 Adaptive Softmax

## A

### NN-LVO-A01
写出 flat full-softmax NLL。训练一个目标位置、计算 exact 全词表概率和执行 global top-$k$，三者各需要哪些输出量？

### NN-LVO-A02
分别判断 full softmax、sampled softmax、negative sampling、hierarchical softmax、adaptive softmax 是否给出归一化 categorical probability；答案必须注明“相对于哪个模型”。

### NN-LVO-A03
为什么 $O(\log V)$ 个树节点不保证比 $V$ 类 dense GEMM 的端到端 wall time 更短？列出至少四个系统因素。

## B

### NN-LVO-B01
设 $V=3$，$e^{z}=(1,2,3)$，proposal $q=(1/2,1/3,1/6)$，$K=1$。列出重要性估计量 $\widehat Z=e^{z_s}/q(s)$ 的可能值，验证 $\mathbb E\widehat Z=Z$，并比较 $\mathbb E\log\widehat Z$ 与 $\log Z$。

### NN-LVO-B02
一棵二叉树中，某 token 路径的三个正确分支概率为 $0.8,0.7,0.9$。求该 token 概率与 NLL。若另一叶只在最后一步取相反分支，它的概率是多少？

### NN-LVO-B03
Adaptive softmax 的 head 含 2000 个常用词与 4 个 cluster gates。四个 tail 的概率质量分别为 $(0.08,0.05,0.02,0.01)$，访问成本分别为 $(1000,2000,4000,8000)$ 个局部 labels。按 label 数近似计算期望成本，并与 $V=50{,}000$ 的 full 输出比较。

## C

### NN-LVO-C01
证明：即使 $\widehat Z>0$ 且 $\mathbb E\widehat Z=Z$，一般仍有 $\mathbb E\log\widehat Z<\log Z$。何时取等号？这为什么会影响 loss/gradient 论证？

### NN-LVO-C02
用结构归纳证明合法 hierarchical probability tree 的全部 leaves 概率和为 1。证明必须覆盖不平衡树。

### NN-LVO-C03
写出 adaptive softmax 中 head token 与 tail token 的概率公式，并推导期望类别计算量
$$
C_{\rm head}+\sum_g\pi_gC_g.
$$
指出它遗漏了哪些真实 FLOP/系统量。

## D

### NN-LVO-D01
一个 sampled-softmax 实现允许负样本重复，且可能采到正类。列出 proposal correction、multiplicity 与 accidental-hit 三方面必须定义的合同，并设计小词表枚举测试。

### NN-LVO-D02
某 adaptive-softmax checkpoint 在新 tokenizer 中重排了 token IDs，但保留了原 cutoffs 和参数。解释 silent corruption，并给出保存、加载与迁移时的原子校验项。

### NN-LVO-D03
某论文只报告 sampled training loss 和训练 tokens/s，便声称“perplexity 与 decoding 都优于 full softmax”。设计最低限度的复核协议。

## E

### NN-LVO-E01
设计 full、sampled、hierarchical、adaptive 四方法的公平大词表基准。要求同时给出 natural protocol 与 matched-contract protocol。

### NN-LVO-E02
若生成时使用 candidate retriever 再 rerank，建立 end-to-end 质量分解，说明 candidate recall 如何给最终 top-$k$ 设上限，并列出延迟账。

### NN-LVO-E03
反驳：“Hierarchical softmax 是 full softmax 的 exact $O(\log V)$ 实现。”给出概率归一化、函数族、训练目标、树结构和硬件五层论证。
