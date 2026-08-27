---
type: concept
status: verified
area: [language-models, reasoning, sampling, estimators]
node_id: LM-38
aliases: [Self-Consistency, Best-of-N, Pass-at-k, 多样本推理]
prerequisites: ["[[Chain-of-Thought、Scratchpad 与 Faithfulness]]", "[[常用离散分布]]"]
related: ["[[Test-time Compute、Search、Verifier 与预算]]", "[[Pass-at-k、Best-of-N、采样估计与选择偏差]]"]
sources: ["[[S-2023-Wang-Self-Consistency]]", "[[S-2021-Chen-Codex-PassAtK]]", "[[S-2021-Cobbe-Training-Verifiers]]"]
exercises: ["[[习题 - Self-Consistency、Best-of-N 与 Pass-at-k]]"]
solutions: ["[[解答 - Self-Consistency、Best-of-N 与 Pass-at-k]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-icl-sampling-selection-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Self-Consistency、Best-of-N 与 Pass-at-k

> [!abstract] 一句话结论
> 多采样产生的是候选集合。Pass-at-k 测集合里是否至少有一个正确解，self-consistency 用答案频数聚合，Best-of-N 用 verifier 选择；覆盖率、聚合规则和选择准确率是三件不同的事。

## 一、统一随机对象

固定问题 $x$、模型和 sampler，从分布

$$
(R_j,Y_j)\sim p_\theta(r,y\mid x),\qquad j=1,\ldots,N
$$

获得 $N$ 条 reasoning path 与最终答案。还需定义 canonicalizer $C$，将等价输出归为同一答案：

$$
A_j=C(Y_j).
$$

若 1/2、0.5 与 50% 没被规范化，self-consistency 会错误拆票；若 parser 把步骤中的数字当最终答案，所有估计量都被污染。

## 二、Self-Consistency 是经验众数

[[S-2023-Wang-Self-Consistency]] 的基本规则是

$$
\hat a_{SC}=\arg\max_a\sum_{j=1}^{N}\mathbf 1\{A_j=a\}.
$$

必须声明 tie-break、invalid output 和拒答怎样处理。它近似的是答案分布的 mode，不是正确答案的 oracle。

### 手算

五条路径输出 A,B,A,C,A，则 A 得 3/5，self-consistency 选择 A。即使 A 错，规则仍会稳定地选错。

若每条独立样本正确率为 $p=0.6$，三票多数正确概率为

$$
{3\choose2}p^2(1-p)+p^3=3(0.36)(0.4)+0.216=0.648.
$$

提升依赖独立性和错误答案不形成更强相关多数。

## 三、Pass-at-k 是 oracle coverage

若每次独立、同分布且单次成功概率为 $p$，有放回抽 $k$ 次至少一次成功概率为

$$
1-(1-p)^k.
$$

代码评测中常先生成 $n$ 个样本，其中 $c$ 个通过测试，再估计从这 $n$ 个样本无放回选 $k$ 个至少一个成功：

$$
\widehat{\operatorname{pass@k}}
=1-\frac{\binom{n-c}{k}}{\binom nk},
$$

当 $n-c<k$ 时为 1。

### 手算

$n=5,c=2,k=3$：

$$
1-\frac{\binom33}{\binom53}=1-\frac1{10}=0.9.
$$

它表示三选中至少包含一个通过单测的程序，不表示系统能从三个候选中识别哪个正确。

## 四、Best-of-N 需要 verifier

给评分器 $V(x,R_j,Y_j)$，选择

$$
j^*=\arg\max_j V(x,R_j,Y_j).
$$

Best-of-N top-1 成功需要两个事件：

1. candidate coverage：集合中存在正确解；
2. selection：verifier 把某个正确解排在最高。

定义 oracle coverage $O_N$ 与 chosen success $S_N$，则选择 regret 可写

$$
\operatorname{regret}_N=O_N-S_N\ge0.
$$

若覆盖率高而 chosen success 低，瓶颈在 verifier；若覆盖率本身低，再强 selector 也无解可选。

[[S-2021-Cobbe-Training-Verifiers]] 在数学解答上展示 generator + verifier 路线。必须报告 verifier 是否见过同分布数据、是否读取最终答案、是否偏好长度/格式。

## 五、相关样本与有效样本量

相同 prompt、相同高概率模式会使候选高度相关。若用等相关近似，某个统计量的有效样本量可粗略写作

$$
N_{eff}\approx\frac{N}{1+(N-1)\rho}.
$$

当 $N=20,\rho=0.5$，$N_{eff}\approx1.9$。这不是所有离散答案的精确定理，但提醒我们：20 条措辞不同、核心错误相同的 CoT 不等于 20 份独立证据。

多样性应从答案、解题策略、首个错误位置和语义聚类分别测，而非只用文本 edit distance。

## 六、三种方法的目标不同

| 方法 | 需要真值/验证器 | 输出 | 主要失败 |
|---|---|---|---|
| self-consistency | 不需外部真值 | 众数答案 | 错误模式形成多数 |
| pass-at-k | 评测时需 oracle | 覆盖率 | 部署无法识别成功者 |
| Best-of-N | 需 learned/rule verifier | 一个候选 | reward hacking、排序误差 |
| executable tests | 需可执行规范 | 通过测试候选 | tests 不完备 |

它们不能只用一个“多样本准确率”统称。

## 七、预算与停止

多样本预算至少包括

$$
C=N\cdot E[L_{gen}]+C_{verify}+C_{parse},
$$

还要报告并行 latency 与 serial latency。若一个方法生成 100 条、另一个只生成 1 条，比较 top-1 而不报成本没有解释力。

可用 anytime curve 报 $k=1,2,4,8,\ldots$ 的 coverage/chosen accuracy。Adaptive stopping 应基于预注册置信阈值或答案稳定性，并计入看过多少样本。

## 八、图解：覆盖、聚合与选择

先看图回答：为什么 pass-at-k 很高仍可能无法改善用户看到的答案？

![[00-知识库管理/_assets/figures/language-models/fig-lm-icl-sampling-selection-v1.svg|900]]

> [!figure] 图 LM-38　多路径采样的三种读法
> 左侧同一 prompt 产生五条路径；右侧分别给出答案投票、oracle coverage 与 verifier selection，并把共享预算单独列账。图由本库重新绘制。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先看候选集合中有几个正确，再看答案是否归一为同一类，最后问选择器是否能把正确候选提到第一。

**图没有证明什么**：五条路径是教学示意，不证明 self-consistency 或 verifier 在任意任务上更好，也不假设样本真正独立。

## 九、最小报告协议

- prompt/model/sampler/temperature/top-p/seed；
- $N$、每条最大与实际 token；
- raw outputs、canonicalizer、invalid/tie rule；
- unique answer/strategy 数；
- pass@k 的 $n,c,k$ 与估计公式；
- oracle coverage、chosen accuracy、selection regret；
- verifier 训练集、score calibration 与盲测；
- token、FLOPs、调用、延迟和失败请求预算。

## 十、常见错误

- 把 majority agreement 当置信度或真值；
- 用有放回公式解释固定样本池的无放回估计；
- 把 pass@k 当用户 top-1；
- 只报 Best-of-N，不报 oracle coverage；
- 用测试真值选择候选却称 verifier-free；
- 忽略答案 canonicalization；
- 把相关 paths 当独立 Bernoulli trials；
- 增加 $N$ 后不匹配总 token 与 latency。

## 十一、出口标准

完成本节后，应能手算 binomial majority 和 pass-at-k 组合式，区分 coverage、aggregation 与 selection，计算 selection regret，并为多样本推理画出预算匹配的 anytime curve。

## 十二、来源与练习

- [[S-2023-Wang-Self-Consistency]]：答案边缘化式聚合；
- [[S-2021-Chen-Codex-PassAtK]]：无放回 pass-at-k 估计；
- [[S-2021-Cobbe-Training-Verifiers]]：候选生成与 outcome verifier；
- [[习题 - Self-Consistency、Best-of-N 与 Pass-at-k]]；
- [[解答 - Self-Consistency、Best-of-N 与 Pass-at-k]]。
