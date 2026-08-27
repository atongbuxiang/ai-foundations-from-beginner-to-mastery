---
type: concept
status: verified
area: [language-models, decoding, beam-search]
node_id: LM-50
aliases: [Beam Search 与长度偏差, 序列搜索]
prerequisites: ["[[Logits、Softmax、Temperature 与 Categorical Sampling]]", "[[数学归纳、递归与组合计数]]"]
related: ["[[EOS、停止规则、重复惩罚与退化循环]]", "[[Test-time Compute、Search、Verifier 与预算]]"]
sources: ["[[S-2018-Su-5861-Seq2Seq与Beam-Search]]", "[[S-2020-Meister-Beam-Search]]", "[[S-2020-Su-7259-Exposure-Bias]]"]
exercises: ["[[习题 - Greedy、Beam Search、Sequence Score 与 Length Penalty]]"]
solutions: ["[[解答 - Greedy、Beam Search、Sequence Score 与 Length Penalty]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-beam-tree-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Greedy、Beam Search、Sequence Score 与 Length Penalty

> [!abstract] 一句话结论
> Greedy 每步局部取最大，beam 只保留有限个高分前缀；二者都不自动优化人类质量。更宽 beam 只能减少特定搜索目标下的部分 pruning error，不能修复长度偏差、模型错配或任务指标与 log-prob 的错位。

## 一、sequence score

含 EOS 的序列分数

$$
\log p(y_{1:T},\mathrm{EOS}\mid x)
=\sum_{t=1}^{T}\log p(y_t\mid x,y_{<t})
+\log p(\mathrm{EOS}\mid x,y_{\le T}).
$$

每项 log-prob 不大于 0，所以继续追加 token 使未归一化总分不增。不同长度比较常偏短，但程度仍由 EOS 概率与任务决定。

Greedy 每步取

$$
\hat y_t=\arg\max_vp(v\mid x,\hat y_{<t})
$$

且不回溯。首步 $P(A)=0.6,P(B)=0.4$；若 $P(\mathrm{EOS}\mid A)=0.5$、$P(\mathrm{EOS}\mid B)=0.99$，greedy 路径为 $0.30$，B 路径为 $0.396$，局部最大不是完整最大。

## 二、beam 的状态

宽度 $K$ 的 beam 维护至多 $K$ 个前缀与累计分

$$
s(y_{\le t})=\sum_{j=1}^{t}\log p(y_j\mid x,y_{<j}).
$$

每步从最多 $K|V|$ 个扩展中保留 top $K$。Completed 是否与 active 同表、何时 early stop、ties 如何破坏，都属于算法。

Beam 一般不是 exact dynamic programming：两个 token 前缀即使末 token 相同，KV state 和条件分布也不同，不能合并。

## 三、beam width 与三种质量

1. search score：找到的最高模型分数；
2. search error：是否遗漏目标分数更高的序列；
3. task quality：BLEU、正确率、人评或效用。

更宽 beam 保留更多候选，但 exact MAP 仍可能短、普通、重复或不符合任务偏好。搜索更准不等于模型/目标更对。

## 四、length penalty 重新定义目标

常见形式

$$
s_\alpha(y)=\frac{\log p(y\mid x)}{\ell(y)^\alpha}
$$

或

$$
s_\alpha(y)=\frac{\log p(y\mid x)}
{\left(\frac{5+\ell(y)}6\right)^\alpha}.
$$

二者不同。因 log-prob 为负，除以大于 1 的长度因子使长序列分数更接近 0。$\alpha$ 是任务调参，不是链式法则；归一化分数一般不是序列 log-prob。Coverage penalty、min length、forced EOS 也改变目标或可行集合。

## 五、完成与 early stop

对纯累计 log-prob，未来增量至多 0，active prefix 当前分数是其所有延伸的上界。可用 best active upper bound 与 completed score 比较。

加入非单调 length reward、coverage、grammar 或 verifier 后，原 bound 可能失效；必须重新推导 admissible upper bound。

## 六、暴露偏差不是 beam 的同义词

Teacher forcing 用真实历史，free-running 用模型历史；这是前缀分布错配。Beam 只改变 rollout 选择，不能保证修复训练目标。Search error、exposure bias、length bias、模型 miscalibration 必须分账。

## 七、图解：beam 如何错过、保留与停止

**读图问题**：局部最优前缀为什么可能输给另一条完整路径，beam width 2 在哪一步保留信息、又在哪一步不可逆剪枝？

![[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-beam-tree-v1.svg|900]]

> [!figure] 图 LM-50　Greedy、beam-2 与完整枚举的搜索树
> **生成：**本库按教学条件概率树确定性绘制；节点同时标 prefix、累计 log-score 与 active/completed 含义，虚线表示被剪路径。

**怎样读图**：先沿 greedy 单支观察局部选择，再比较 beam-2 同时保存的两个前缀及下一步累计分；最后把 active 与 completed 分开，检查 length score 和 early-stop 上界。

**图没有证明什么**：小树中 beam-2 找到该评分函数的最佳路径，不推出任意模型或任务用 beam-2 足够，也不推出更宽 beam 会提高外部任务指标或降低 exposure bias。

## 八、报告合同与出口

保存 beam width、candidate expansion、raw/normalized score、length 是否含 EOS/prompt、min/max length、finished/active policy、early-stop、tie、processor、cache 与 parser。

完成本节后，应能构造 greedy 反例，手算 beam 表，区分三种质量，解释 length penalty，并检查 early-stop bound。

## 九、来源与练习

- [[S-2018-Su-5861-Seq2Seq与Beam-Search]]；
- [[S-2020-Meister-Beam-Search]]；
- [[S-2020-Su-7259-Exposure-Bias]]；
- [[习题 - Greedy、Beam Search、Sequence Score 与 Length Penalty]]；
- [[解答 - Greedy、Beam Search、Sequence Score 与 Length Penalty]]。
