---
type: concept
status: verified
area: [language-models, reasoning, search, test-time-compute]
node_id: LM-39
aliases: [Test-time Compute, 推理时扩展, 搜索与验证器]
prerequisites: ["[[Self-Consistency、Best-of-N 与 Pass-at-k]]", "[[渐近记号、增长率与复杂度]]"]
related: ["[[Chain-of-Thought、Scratchpad 与 Faithfulness]]", "[[Speculative Decoding、Acceptance 与分布精确性]]"]
sources: ["[[S-2023-Yao-Tree-of-Thoughts]]", "[[S-2021-Cobbe-Training-Verifiers]]", "[[S-2023-Lightman-Process-Supervision]]", "[[S-2024-Snell-Test-Time-Compute]]"]
exercises: ["[[习题 - Test-time Compute、Search、Verifier 与预算]]"]
solutions: ["[[解答 - Test-time Compute、Search、Verifier 与预算]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-icl-test-time-search-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Test-time Compute、Search、Verifier 与预算

> [!abstract] 一句话结论
> 推理时扩展不是“让模型多想一会儿”这一个旋钮，而是 proposal、状态表示、搜索队列、verifier、剪枝和停止组成的算法。收益必须在同一问题、policy 和多维成本下比较。

## 一、Test-time compute 包含什么

固定模型参数后，可在推理时增加：

- 单条响应长度；
- 独立/相关候选数；
- 搜索分支与深度；
- 自我修订轮数；
- verifier 或 reward model 调用；
- 工具、代码执行与外部环境交互。

这些资源不等价。生成 1000 个 token、并行生成 10 条各 100 token、串行搜索深度 10，可能有相似 token 总量，却有不同依赖深度、显存和 wall-clock。

## 二、把推理写成搜索问题

定义状态 $s$ 为已生成的部分解、外部环境和必要记忆。一个最小搜索器含：

1. proposal $\pi(a\mid s)$：生成下一 thought/action；
2. transition $s'=T(s,a)$：解析并执行；
3. value/verifier $V(s)$：估计状态质量；
4. queue rule：DFS、BFS、beam、best-first；
5. pruning：保留哪些分支；
6. terminal/stopping：何时输出。

没有这些对象，“用了 Tree-of-Thought”仍不足以复现。

## 三、搜索树的成本爆炸

若每节点展开 $b$ 个分支、深度 $d$，完整树节点数

$$
N_{tree}=1+b+\cdots+b^d=\frac{b^{d+1}-1}{b-1}.
$$

$b=2,d=3$ 时为 $15$；$b=5,d=6$ 时已为 $19531$。实际方法必须依靠 beam、剪枝、共享前缀或 early stop。

若每节点 proposal 平均 $L_p$ token、verifier 成本 $C_v$，粗略计算账为

$$
C\approx N_{expanded}(C_{policy}(L_p)+C_v)+C_{tools}.
$$

不能只报最终答案 token 数。

## 四、DFS、BFS、Beam 与 Best-first

- DFS：内存小、可深入，早期错误可能浪费长路径；
- BFS：按深度完整探索，分支成本快；
- beam：每层保留 top-$w$，依赖局部 score；
- best-first：全局按 value 展开，依赖 calibration；
- MCTS 类：用访问统计平衡探索/利用，接口与 rollout 成本更复杂。

[[S-2023-Yao-Tree-of-Thoughts]] 将 coherent thought 当节点，并在任务上组合生成、自评与 BFS/DFS。论文结果绑定其任务、prompt、搜索和 evaluator；不能把方法名当跨任务保证。

## 五、Outcome 与 Process Verifier

Outcome verifier 只看完整候选是否正确：

$$
V_{out}(x,r,y)\approx P(Y\text{ correct}\mid x,r,y).
$$

Process verifier 对步骤打分：

$$
v_t\approx P(r_{\le t}\text{ remains valid}\mid x).
$$

轨迹分数如何聚合必须声明，例如

$$
V_{min}=\min_t v_t,
\qquad
V_{prod}=\prod_t v_t,
\qquad
V_{sum}=\sum_t\log v_t.
$$

乘积/对数和会惩罚长链，最小值对单个低分极敏感，均值可能掩盖致命早错。

[[S-2023-Lightman-Process-Supervision]] 在特定 MATH 协议中比较步骤监督与结果监督。它提供重要证据，不构成“PRM 在所有领域总优”的定理。

## 六、Verifier 的两类误差

1. false positive：错误路径得高分，搜索被带入伪解；
2. false negative：非常规正确路径被剪掉，覆盖率下降。

搜索会主动寻找 verifier 的漏洞，所以静态 IID accuracy 不足。要测：

- score calibration 与 ranking AUC；
- 随搜索轮次增长的 reward–truth gap；
- 长度、格式、自信语气和答案泄漏偏置；
- 对 adaptive candidates 的性能；
- oracle coverage 与 chosen accuracy 的分离。

## 七、难度自适应预算

统一给每题相同 $C$ 可能浪费简单题、饿死困难题。可定义调度器

$$
C_i=g(u_i,\hat d_i,\text{remaining budget}),

$$

其中 $u_i$ 是不确定性，$\hat d_i$ 是难度估计。公平性要求：

- 难度估计不能偷看测试真值；
- 报每个难度分层的成本/准确率；
- 报总体预算约束，而非只看成功题；
- 调度失败和超时也计入。

[[S-2024-Snell-Test-Time-Compute]] 强调最优策略依题目难度、policy 与 verifier 改变。课程采用这一条件化结论，不把“小模型加推理预算总能胜大模型”写成定理。

## 八、多维成本向量

至少报告

$$
\mathbf C=(T_{in},T_{out},F,N_{call},N_v,L_{serial},M_{peak},\$),
$$

分别是输入/输出 token、FLOPs、模型调用、verifier 调用、串行延迟、峰值内存与费用。并行可以降低延迟但不降低总计算；KV cache 共享可降低某些成本但不改变逻辑搜索节点数。

一个标量预算只在明确权重和硬件后才有意义。

## 九、图解：搜索算法与预算账

先看图回答：如果只公布展开后的最好叶子，还缺哪六个算法对象？

![[00-知识库管理/_assets/figures/language-models/fig-lm-icl-test-time-search-v1.svg|900]]

> [!figure] 图 LM-39　Test-time search tree 与多维预算
> 上方标出不同 value 的搜索状态，下方把生成 token、FLOPs、verifier、串行延迟和峰值内存分开。图由本库重新绘制。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：从根到叶跟踪 proposal 与 transition，再检查 queue、pruning 和 stop；最后用整条成本向量比较方法，不以叶子文本长度代替总预算。

**图没有证明什么**：颜色只表示教学用评分，不证明 verifier 正确，也不证明树搜索优于独立采样。

## 十、最小公平对照

同一 policy 上至少比较：

- greedy direct；
- 单条长 CoT；
- $N$ 条独立样本；
- self-consistency；
- Best-of-N outcome verifier；
- process verifier + beam/search；
- oracle selector 上界。

对每种方法画 accuracy–tokens、accuracy–FLOPs 和 accuracy–latency 曲线，并报告 bootstrap 区间。若 verifier 是额外大模型，其训练与推理成本不能隐去。

## 十一、常见错误

- 把输出 token 数当总 compute；
- 方法间更换 policy 模型却归因于搜索；
- 用 task-specific 程序规则却称通用推理；
- verifier 在固定候选上好就假设搜索中不被利用；
- 只报成功题成本；
- 把并行低延迟说成低总算力；
- 按真实难度分配预算造成 oracle 泄漏；
- 不报告 early stop、超时和 parser failure。

## 十二、出口标准

完成本节后，应能将任一推理扩展方法写成 state/proposal/transition/value/queue/pruning/stop 七元合同，手算树规模，比较 outcome/process verifier，并设计多维预算匹配的 anytime 评测。

## 十三、来源与练习

- [[S-2023-Yao-Tree-of-Thoughts]]：显式 thought search；
- [[S-2021-Cobbe-Training-Verifiers]]：outcome verifier；
- [[S-2023-Lightman-Process-Supervision]]：process supervision；
- [[S-2024-Snell-Test-Time-Compute]]：难度条件下的预算分配；
- [[习题 - Test-time Compute、Search、Verifier 与预算]]；
- [[解答 - Test-time Compute、Search、Verifier 与预算]]。
