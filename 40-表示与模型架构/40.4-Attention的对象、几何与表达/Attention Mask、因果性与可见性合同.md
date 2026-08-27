---
type: concept
status: draft
area: [architecture, attention, masking, causality]
aliases: [Causal Mask, Padding Mask, Attention Visibility]
node_id: ARCH-27
prerequisites: ["[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[函数、映射、关系与等价类]]", "[[图数据、节点重标号与置换对称性]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[Self-Attention、Cross-Attention 与张量形状]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2024-Su-10347-位置编码与置换对称]]", "[[S-2023-Su-9529-DecoderOnly低秩猜想]]"]
exercises: ["[[习题 - Attention Mask、因果性与可见性合同]]"]
solutions: ["[[解答 - Attention Mask、因果性与可见性合同]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-mask-visibility-contract-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Attention Mask、因果性与可见性合同

> [!abstract] 本节主问题
> Mask 不是 softmax 后把几格颜色涂黑，而是定义 query 与 key 之间的**可见关系**。Padding、causal、局部和结构 mask 回答的问题不同；若归一化顺序、boolean convention 或全遮蔽行为不明确，模型可能数据泄漏、行和错误或直接产生 NaN。

## 一、把 Mask 写成二元关系

令 query 索引集为 $I_q$、key 索引集为 $I_k$。可见性是关系

$$
R\subseteq I_q\times I_k.
$$

对每个 query $i$，可见集合

$$
\mathcal V(i)=\{j:(i,j)\in R\}.
$$

Attention 应在这个集合上归一：

$$
a_{ij}=
\begin{cases}
\dfrac{e^{s_{ij}}}{\sum_{\ell\in\mathcal V(i)}e^{s_{i\ell}}},&j\in\mathcal V(i),\\[6pt]
0,&j\notin\mathcal V(i).
\end{cases}
$$

这比“mask 是一个矩阵”更根本：矩阵只是关系在某组索引顺序下的表示。

## 二、常见 Mask 的不同语义

| 类型 | 被禁止的 pair | 主要目的 |
|---|---|---|
| Key padding mask | key 是补齐占位符 | 有效 query 不读取伪 token |
| Query padding mask | query 本身是占位符 | 通常屏蔽输出或 loss，不一定改变其他行 |
| Inclusive causal mask | $j>i$ | 自回归位置 $i$ 可看自己和过去 |
| Strict causal mask | $j\ge i$ | 不看自己；需另有状态/shift 合同 |
| Local/window mask | $|i-j|>w$ 或越出方向窗口 | 限制感受野与成本 |
| Structural mask | pair 不满足图/模态/块关系 | 注入任务结构 |

Key padding 与 query padding 不能互换：前者删除 score 的列可见性，后者决定某些输出行是否有意义。

## 三、因果 Mask 编码什么“因果”

自回归因子分解为

$$
p(x_{1:T})=\prod_{i=1}^T p(x_i\mid x_{<i}).
$$

若训练输入采用右移 token，第 $i$ 个表示可以读取到与预测 $x_i$ 对应的已知前缀；具体 inclusive/strict 约定必须与 shift 对齐。Causal mask 保证计算图中没有从未来 token 到当前预测的直接 attention 边，但它不证明数据处理无泄漏：标签拼接、缓存错位、双向特征或 split 污染仍可能泄漏。

> [!warning] “Causal” 有两个层次
> 这里首先是**自回归可见性**，不是因果推断中的 intervention/identifiability。一个 causal mask 的语言模型并不会因此自动学到现实世界的因果图。

## 四、为什么必须在 Softmax 前 Mask

正确做法是

$$
A=\operatorname{softmax}(S+M),\qquad
M_{ij}=\begin{cases}0,&(i,j)\in R,\\-\infty,&\text{otherwise}.
\end{cases}
$$

错误做法是先 $\tilde A=\operatorname{softmax}(S)$，再把禁止项乘 0。此时有效项行和小于 1。例：原权重 $(0.5,0.3,0.2)$，屏蔽第三项后变 $(0.5,0.3,0)$，行和 $0.8$；正确重归一应为 $(0.625,0.375,0)$。

后乘 mask 只有在再除以有效项和、并正确处理全零行时才等价；通常直接 pre-softmax mask 更清楚且更稳定。

## 五、Boolean 与 Additive Convention

常见 API 可能规定：

- `True = keep` 或 `True = block`；
- mask shape 为 $(T_q,T_k)$、$(B,T_q,T_k)$ 或可广播到 $(B,h,T_q,T_k)$；
- additive mask 使用 $0/-\infty$，或 fused kernel 内部处理；
- padding mask 与 causal flag 由 kernel 组合。

因此不能只写“传入 mask”。测试应构造极端 logits，让被屏蔽位置即使原 score 最大也得到恰好 0 权重，并检查每个有效行的和。

## 六、全遮蔽行与有限负数

若 $\mathcal V(i)=\varnothing$，没有合法概率分布。对全 $-\infty$ 行做“减最大值”会出现 $-\infty-(-\infty)$，可能产生 NaN。

安全合同可选：

1. 数据/结构保证每行至少有一个可见 key；
2. 为每行加入允许的 self/sentinel key；
3. kernel 明确定义全遮蔽行为并在输出/loss 跳过该行；
4. 主动报错。

用 `-1e9` 代替 $-\infty$ 依 dtype 而异：在某些低精度中会饱和成 $-\infty$，在另一些情形仍为有限数；若所有项都相同有限负值，softmax 反而会给均匀分布。

## 七、Mask 与置换对称性

无位置、无非对称 mask 的 self-attention 对 token 同步重排是等变的。引入 mask 后，只有同时保持关系的重排才保留对称性。若 $P$ 是置换矩阵，mask 也必须变为

$$
M' = PMP^\top.
$$

固定的下三角 causal mask 不对任意置换保持不变；它把“先后”写入关系。[[S-2024-Su-10347-位置编码与置换对称]] 用这一点说明：即使没有显式 position vector，非对称 mask 本身也可能提供顺序结构。课程只采用精确的对称性结论，不把“NoPE 总够用”当普遍经验定律。

## 八、因果 Attention 矩阵为何可满秩

对 inclusive causal softmax，$A$ 是下三角矩阵。只要对角位置可见且 logit 有限，

$$
A_{ii}>0.
$$

于是

$$
\det A=\prod_{i=1}^T A_{ii}>0,
$$

故 $A$ 严格满秩。[[S-2023-Su-9529-DecoderOnly低秩猜想]] 用这个事实讨论 decoder-only；本课程把“正对角下三角矩阵满秩”标为 `I`，把“因此解释 decoder-only 总体优势”保留为 `H`。满秩也不代表条件数好或有效秩高。

## 九、Leakage 与单元测试

最小测试套件：

1. **未来脉冲**：只改变未来 token，确认当前输出不变；
2. **屏蔽最大值**：让禁止项 score 极大，确认权重仍为 0；
3. **行和**：每个非空有效行权重和为 1；
4. **padding 一致性**：相同有效序列加不同 padding 长度，结果一致；
5. **all-masked**：核的预期行为明确且无静默 NaN；
6. **broadcast**：不同 batch/head 使用不同 mask 时不串用；
7. **shift audit**：输入、label 和 causal diagonal 对齐。

## 十、图：可见关系与计算顺序

先看图回答：左栏第 4 个 query 为什么能看 4 个 key？中栏 query padding 为什么通常不等同于删除 key 列？

![[00-知识库管理/_assets/figures/architecture/fig-attention-mask-visibility-contract-v1.svg|900]]

> [!figure] 图 40.4-03　Attention mask 的可见性矩阵与安全计算顺序
> 左栏显示 inclusive causal 关系，中栏分开三类 mask，右栏给出 score—mask—softmax 顺序。来源：依据 Transformer causal masking 与关系表示独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_attention_v1.py]] 生成。

**怎样读图**：把每个绿色格读成一条允许的计算边，而不是“一个较小权重”；沿右栏确认禁止关系在归一化前已成为零概率，并主动寻找可能没有绿色格的行。

**图没有证明什么**：它没有证明数据流水线没有其他泄漏，也没有证明 causal mask 等于现实世界因果结构，或 full-rank causal attention 一定表达更好。

## 十一、常见错误

1. 把 key padding 与 query padding 当同一轴；
2. softmax 后直接乘 mask 且不重归一；
3. 未核对 `True` 是 keep 还是 block；
4. 广播维度使一个样本/头的 mask 泄到另一个；
5. 用有限负数却假设严格零；
6. 忽略全遮蔽行；
7. causal diagonal 与 shifted labels 错一位；
8. 以 causal attention 的名字替代泄漏测试；
9. 把满秩等同高有效秩或更优架构。

## 十二、掌握标准

> [!summary]
> - Mask 定义 query-key 的二元可见关系；
> - padding、causal、local 与 structural mask 有不同语义；
> - 禁止关系应在 softmax 前进入 logits，全遮蔽行须显式定义；
> - causal mask 改变置换对称性，inclusive causal attention 可严格满秩。

能画出不同 mask（A/B）、证明 pre-softmax masking 与有效集归一等价（C）、构造 all-masked/broadcast/leakage 反例（D），并为模型实现完整 mask contract test（E）。

## 十三、练习与独立详解

- [[习题 - Attention Mask、因果性与可见性合同]]
- [[解答 - Attention Mask、因果性与可见性合同]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2024-Su-10347-位置编码与置换对称]]
- [[S-2023-Su-9529-DecoderOnly低秩猜想]]
