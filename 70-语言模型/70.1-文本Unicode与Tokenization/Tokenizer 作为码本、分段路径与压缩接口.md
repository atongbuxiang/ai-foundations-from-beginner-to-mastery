---
type: concept
status: verified
area: [language-models, tokenization, information-theory]
node_id: LM-03
aliases: [Tokenizer 数学对象, 分词码本]
prerequisites: ["[[Unicode、字节、码点、字素簇与规范化合同]]", "[[自信息、熵与编码长度]]"]
related: ["[[BPE、合并规则与确定性编码解码]]", "[[WordPiece、词表构建与最长匹配边界]]", "[[Unigram LM、Viterbi、EM 与 Subword Regularization]]"]
sources: ["[[S-2018-Kudo-Richardson-SentencePiece]]", "[[S-2018-Su-5476-最小熵原理词库构建]]", "[[S-2023-Su-9752-BytePiece]]"]
exercises: ["[[习题 - Tokenizer 作为码本、分段路径与压缩接口]]"]
solutions: ["[[解答 - Tokenizer 作为码本、分段路径与压缩接口]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-tokenizer-codebook-lattice-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Tokenizer 作为码本、分段路径与压缩接口

> [!abstract] 一句话结论
> Tokenizer 不是“把句子切开”的单一函数，而是基本单元、规范化器、有限码本、分段算法、ID 映射、特殊符号和解码器的组合。它同时改变序列长度、embedding/softmax 参数、注意力成本和概率评价单位。

## 一、一个完整 tokenizer 是七元组

把 tokenizer 写作

$$
\mathcal T=(N,\Sigma,V,C,A,id,D),
$$

其中：

- $N$：文本 normalization/pre-tokenization；
- $\Sigma$：基本单元字母表，如 Unicode 字符或 bytes；
- $V\subseteq\Sigma^*$：有限 token 码本；
- $C$：控制/特殊 token 及其角色；
- $A$：给定字符串选择分段路径的算法；
- $id:V\cup C\to\{0,\ldots,|V|+|C|-1\}$：token 到整数；
- $D$：从 token/ID 序列恢复文本或 bytes 的解码器。

只保存 `vocab.json` 通常不够：BPE 还需有序 merges，WordPiece 需续接/unknown 约定，Unigram 需 piece score，现代模型还需 normalizer、pretokenizer、special tokens 和 chat template。

## 二、分段是 DAG 上的路径

令基本单元串 $x=x_1\cdots x_n$。建有向无环图，顶点是位置 $0,\ldots,n$；若子串 $x_{i+1:j}\in V$，就连边 $i\to j$，标签为该 token。任何从 $0$ 到 $n$ 的路径都是合法分段：

$$
\mathcal S_V(x)=\{(v_1,\ldots,v_m):v_1\circ\cdots\circ v_m=x\}.
$$

算法 $A$ 决定选哪条路径：

- BPE 按 learned merge ranks 重放；
- WordPiece 常用 longest-match-first；
- Unigram LM 用最大概率/Viterbi 或从路径后验采样；
- 纯字典分词可最少 token、最短码长或加任务代价。

同一个词表不必给出同一个 encode，因为 $A$ 仍可能不同。

## 三、可逆性到底要求什么

最强的 byte round-trip 是

$$
D(A(b))=b\qquad\forall b\in\{0,\ldots,255\}^*.
$$

若先做 normalization，只能承诺

$$D(A(x))=N(x),$$

而非原始 $x$。若 normalizer 折叠空白或 NFKC，原字节不可恢复。UNK 也会造成多对一映射。

> [!definition] 完备覆盖
> 对承诺输入域中任意 $x$，分段集合 $\mathcal S_V(x)$ 非空。字符全覆盖、byte fallback 或 UNK 都可使编码“总是返回”，但只有前两者可能保留原内容；UNK 不是无损覆盖。

## 四、Tokenizer 为什么像压缩接口

设语料总 byte 数为 $B$，编码后 token 数为 $T$。可报告

$$r_{b/t}=\frac{B}{T}\quad\text{bytes per token},
\qquad
f_{t/b}=\frac{T}{B}\quad\text{tokens per byte}.
$$

这只是序列长度压缩，不是完整无损编码的 bit rate：每个 token ID 若用固定宽度存储还需约 $\lceil\log_2|V|\rceil$ bits，token 分布的熵编码又是另一对象。更大的词表通常提高 bytes/token，却增加：

- input/output embedding 参数约 $2|V|d$（若 tied 则约 $|V|d$）；
- softmax 计算/通信；
- 稀有 token 的估计困难；
- tokenizer 模型和缓存占用。

## 五、序列长度怎样进入模型成本

若原文本经 tokenizer 产生长度 $T$，dense self-attention 的 pairwise 项近似 $O(T^2d)$，投影/FFN 为 $O(Td^2)$；输出 softmax 还与 $|V|$ 有关。将 token 数减少一半不代表总 FLOPs 必然减为四分之一，因为线性投影、softmax、padding、batching 和硬件 kernel 同时变化。

一个公平比较至少有两种口径：

1. **固定原始文本/bytes**：比较不同 tokenizer 的 token、FLOPs、wall time 和质量；
2. **固定 token budget**：比较模型各自看到多少原始信息，但这不再是相同文本预算。

两者回答不同问题。

## 六、概率也随 tokenization 改变坐标

若 tokenizer 可逆且分段确定，字符串 $x$ 与 token 序列 $z=A(x)$ 一一对应时，可定义

$$p_X(x)=p_Z(A(x)).$$

但 per-token NLL

$$-\frac1{|z|}\log p_Z(z)$$

的分母依赖 tokenizer，不能跨词表直接比较。更稳妥的是对相同 raw bytes 报告

$$\operatorname{BPB}(x)=-\frac{\log_2p_Z(A(x))}{|x|_{bytes}}.$$

若 encode 随机、normalization 多对一或含 UNK，需要进一步对分段/原像求和，不能直接使用上述一一映射。

## 七、图：码本、路径和资源三角

先看图回答：同一个 `abc` 有几条分段路径？为什么“最少 token”不是无条件最优？

![[00-知识库管理/_assets/figures/language-models/fig-lm-tokenizer-codebook-lattice-v1.svg|900]]

> [!figure] 图 LM-03　Tokenizer 的路径、合同与资源权衡
> A 把分段表示为 DAG 路径，B 列出词表/分段/解码三项基本合同，C 展示短序列、小词表覆盖和参数稀疏性的 Pareto 权衡。来源：本课程独立绘制。

**怎样读图**：先枚举所有覆盖全串的路径，再问算法选哪条；最后把 $T$、$|V|$、coverage 和下游任务放进同一预算表。

**图没有证明什么**：三角形没有给出唯一最优点；最优点依语料、模型维度、硬件和任务改变。

## 八、科学空间的接口

[[S-2018-Su-5476-最小熵原理词库构建]]把 $-\log p(v)$ 作为码长直觉；这依赖 unigram/product 近似，不能称为自然语言的绝对 entropy。[[S-2023-Su-9752-BytePiece]]明确拆出基本单元、分词算法与训练算法，这个三分法被本课程吸收；其压缩率实验仍需与词表、语料、normalization 和下游预算绑定。

## 九、本节出口

学完应能拿到任意 tokenizer 文件后回答：输入域是什么、怎样规范化、词表覆盖什么、分段算法是什么、能否 byte round-trip、特殊 token 怎样处理，以及改变 tokenizer 后哪些模型指标失去可比性。

接下来分别研究三条算法主线：[[BPE、合并规则与确定性编码解码]]、[[WordPiece、词表构建与最长匹配边界]]和[[Unigram LM、Viterbi、EM 与 Subword Regularization]]。

## 练习与独立解答

- [[习题 - Tokenizer 作为码本、分段路径与压缩接口]]
- [[解答 - Tokenizer 作为码本、分段路径与压缩接口]]

