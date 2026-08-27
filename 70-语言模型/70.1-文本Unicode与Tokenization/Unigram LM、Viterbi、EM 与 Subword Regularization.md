---
type: concept
status: verified
area: [language-models, tokenization, unigram-lm, dynamic-programming]
node_id: LM-06
aliases: [Unigram Tokenizer, 子词正则化]
prerequisites: ["[[Tokenizer 作为码本、分段路径与压缩接口]]", "[[数学归纳、递归与组合计数]]", "[[最大似然估计与 MAP]]", "[[交叉熵与 KL 散度]]"]
related: ["[[BPE、合并规则与确定性编码解码]]", "[[WordPiece、词表构建与最长匹配边界]]"]
sources: ["[[S-2018-Kudo-Subword-Regularization]]", "[[S-2018-Kudo-Richardson-SentencePiece]]", "[[S-2023-Su-9768-Tokenizer-Viterbi-Sampling]]", "[[S-2018-Su-5476-最小熵原理词库构建]]"]
exercises: ["[[习题 - Unigram LM、Viterbi、EM 与 Subword Regularization]]"]
solutions: ["[[解答 - Unigram LM、Viterbi、EM 与 Subword Regularization]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-unigram-viterbi-em-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Unigram LM、Viterbi、EM 与 Subword Regularization

> [!abstract] 一句话结论
> Unigram tokenizer 把分段当潜变量：每个 piece 有概率，整串的概率是所有合法路径概率之和。Viterbi 只找最高概率路径；forward-backward 计算边缘似然和期望计数；采样则保留分段不确定性，三者不能互换。

## 一、概率模型与分段潜变量

词表 $V$ 中每个 piece $v$ 有概率 $p(v)>0$，满足

$$\sum_{v\in V}p(v)=1.$$

给字符串 $x$，合法分段集合为 $\mathcal S_V(x)$。路径 $s=(v_1,\ldots,v_m)$ 的 unigram 概率是

$$p(s)=\prod_{i=1}^{m}p(v_i).$$

因为分段 $S$ 未观测，字符串的边缘概率是

$$
\boxed{p(x)=\sum_{s\in\mathcal S_V(x)}p(s).}
$$

这不是说自然语言 token 独立；它是用于选择分段/词表的局部生成模型。真正 Transformer 语言模型仍会建模 token 间上下文依赖。

## 二、手算 `ab`

词表及概率：$p(a)=0.4,p(b)=0.3,p(ab)=0.2$，其余 token 占 0.1。`ab` 有两条路径：

$$
s_1=(a,b),\quad p(s_1)=0.4\times0.3=0.12;
$$

$$
s_2=(ab),\quad p(s_2)=0.2.
$$

因此

$$p(ab)=0.12+0.2=0.32.$$

MAP/Viterbi 分段是 $(ab)$，概率 0.2；但它的后验概率为

$$p(s_2\mid x)=0.2/0.32=0.625,$$

并不是 1。把 Viterbi path probability 0.2 当成字符串 marginal 0.32 是常见错误。

## 三、Viterbi：在 log semiring 上找最优路径

令 $dp[j]$ 是覆盖前 $j$ 个基本单元的最小负对数代价：

$$
dp[0]=0,\qquad
dp[j]=\min_{i<j:x_{i:j}\in V}
\{dp[i]-\log p(x_{i:j})\}.
$$

同时保存 backpointer 即可回溯 MAP 分段。若最大 piece 长度为 $L$，用 trie 枚举候选时典型复杂度约 $O(nL)$，而非枚举指数多条路径。

并列最优路径仍需 deterministic tie-break，或明确返回任意 MAP。

## 四、Forward：把 max 换成 log-sum-exp

定义前向概率

$$
\alpha[0]=1,\qquad
\alpha[j]=\sum_{i<j:x_{i:j}\in V}\alpha[i]p(x_{i:j}).
$$

则 $\alpha[n]=p(x)$。长串必须在 log-space 计算：

$$
\log\alpha[j]=\operatorname{LSE}_{i}
\big(\log\alpha[i]+\log p(x_{i:j})\big).
$$

Viterbi 使用 min/max semiring，forward 使用 sum-product/log-sum-exp semiring；动态规划图相同，代数运算不同。

## 五、Backward 与期望 token 计数

从位置 $i$ 到末尾的 backward probability：

$$
\beta[n]=1,\qquad
\beta[i]=\sum_{j>i:x_{i:j}\in V}p(x_{i:j})\beta[j].
$$

某条边 $i\to j$、token $v=x_{i:j}$ 的后验使用概率为

$$
\gamma_{ij}(v)=
\frac{\alpha[i]p(v)\beta[j]}{p(x)}.
$$

对全语料求和得到期望计数

$$\widehat c(v)=\sum_x\sum_{(i,j):x_{i:j}=v}\gamma_{ij}(v).$$

在固定词表的 M-step 中，unigram MLE 更新为

$$p^{new}(v)=\frac{\widehat c(v)}{\sum_{u\in V}\widehat c(u)}.$$

这给出 EM 的核心。实际 tokenizer 训练还会从大 seed vocabulary 中剪枝、重估，再达到目标词表大小；剪枝准则和近似属于实现合同。

## 六、Subword Regularization：从后验采样路径

训练下游模型时，不总取 MAP，而从温度化路径分布采样：

$$
q_\alpha(s\mid x)
=\frac{p(s)^\alpha}{\sum_{s'\in\mathcal S(x)}p(s')^\alpha}.
$$

- $\alpha\to\infty$：集中到 MAP；
- $\alpha=1$：原路径后验；
- $0<\alpha<1$：分布更平，分段更多样；
- $\alpha\to0^+$：趋向对合法路径近似均匀，而非对 token 均匀。

采样可作为输入噪声，减少模型对单一分段的依赖；是否提升鲁棒性属于特定任务实验 `E`，并非由概率定义自动推出。

## 七、图：MAP、边缘化与 EM 循环

先看图回答：`ab` 的最佳路径概率为什么小于字符串总概率？

![[00-知识库管理/_assets/figures/language-models/fig-lm-unigram-viterbi-em-v1.svg|900]]

> [!figure] 图 LM-06　Unigram 分段 lattice、Viterbi/forward 与 EM
> A 给出两条路径，B 对比 max 与 sum，C 展示后验计数—概率更新—剪枝循环。来源：本课程依据 Kudo 的 Unigram LM 独立绘制。

**怎样读图**：先枚举小 lattice 验证总概率，再把 Viterbi 的 `max` 换成 forward 的 `sum`，最后用 edge posterior 累积期望计数。

**图没有证明什么**：图没有给出大型词表的最佳剪枝策略，也不保证分段采样一定改善下游模型。

## 八、科学空间的推导接口

[[S-2023-Su-9768-Tokenizer-Viterbi-Sampling]]从 Viterbi 结构讨论随机分段。课程要求把采样器输出与 exact enumeration 对齐；若目标为 $q_\alpha$，每条路径经验频率应在抽样误差内匹配其归一化概率。后续“完美采样”讨论见科学空间 [9811](https://spaces.ac.cn/archives/9811)，在进入核心证据前需逐式复核。

[[S-2018-Su-5476-最小熵原理词库构建]]的码长直觉对应 $-\sum_i\log p(v_i)$；当我们边缘化多条分段时，字符串码长是 $-\log\sum_s p(s)$，一般不等于 MAP 路径码长。

## 九、三类失败检查

- **覆盖失败**：某位置没有 outgoing edge，导致 $p(x)=0$；需要基本字符/byte fallback 或 UNK；
- **数值失败**：直接乘长序列概率下溢；使用 log-sum-exp 和有限检查；
- **统计失败**：过大的 piece 可由少量样本支撑，剪枝/先验与 held-out code length 需记录。

下一节[[Byte-level、Byte Fallback、特殊 Token 与 Chat Template]]会解决任意输入覆盖与控制通道问题。

## 练习与独立解答

- [[习题 - Unigram LM、Viterbi、EM 与 Subword Regularization]]
- [[解答 - Unigram LM、Viterbi、EM 与 Subword Regularization]]
