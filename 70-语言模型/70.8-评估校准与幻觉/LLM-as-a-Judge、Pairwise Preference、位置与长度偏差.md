---
type: concept
status: verified
area: [language-models, evaluation, llm-as-a-judge]
node_id: LM-62
aliases: [LLM Judge, 成对偏好评估]
prerequisites: ["[[语言模型评估对象、任务单位与 Benchmark 合同]]", "[[Exact Match、F1、BLEU、ROUGE 与语义指标边界]]"]
related: ["[[能力—行为—系统评估协议与证据地图]]"]
sources: ["[[S-2023-Zheng-LLM-Judge]]", "[[S-2024-Wang-Fair-Evaluators]]", "[[S-2024-Dubois-Length-Controlled-AlpacaEval]]"]
exercises: ["[[习题 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"]
solutions: ["[[解答 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-eval-judge-bias-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# LLM-as-a-Judge、Pairwise Preference、位置与长度偏差

> [!abstract] 一句话结论
> LLM judge 是一个带 prompt、顺序、版本和自身误差的测量仪器，不是真值函数。Pairwise 评估必须交换位置、保留 tie/冲突、审计长度与家族偏差，并在独立人标锚点上验证。

## 一、把裁判写成随机变量

给任务 $x$、候选 $a,b$、顺序 $o$、rubric $r$、judge 配置 $J$：

$$
Z\sim q_J(z\mid x,a,b,o,r).
$$

$Z\in\{A,B,\text{tie},\text{invalid}\}$。即使 temperature=0，API/model 更新或 parser 也可变。需要保存 judge checkpoint/date、system prompt、rubric、candidate labels、order、seed、raw rationale/output 和 parser。

绝对打分 1—10 有尺度漂移与不同 judge 的不可比；pairwise 通常更简单，但仍依基线和候选集合。

## 二、位置交换审计

对同一对回答评两次：

$$
Z_{AB}=J(x,A,B),\qquad
Z_{BA}=J(x,B,A).
$$

映射回真实候选身份后，理想一致。定义 swap consistency：

$$
\operatorname{SC}
=\frac1n\sum_i
\mathbf1[\operatorname{id}(Z_{AB,i})
=\operatorname{id}(Z_{BA,i})].
$$

若 AB 判 A 胜、BA 仍判“第一个”胜，则是位置翻转冲突。聚合策略可要求两次一致才记胜，冲突记 tie/交人工；不能只取有利顺序。

随机化单次位置使总体位置偏差在期望上缓和，但单样本仍噪；双评能测出冲突，成本也翻倍。

## 三、Win rate 与 tie

对模型 M 相对 baseline B：

$$
\operatorname{WR}
=\frac{W+\lambda T}{W+L+T},
$$

常取 $\lambda=.5$，但必须声明。Invalid/parse failure 是否进分母也要预注册。Prompt 是基本独立单位；同一 prompt 的 AB/BA 和多 judge 结果不能当独立样本。

循环偏好可能存在：A>B、B>C、C>A。单一 Elo/Bradley–Terry 排名假设潜在一维强度，需检查拟合、顺序效应和 matchup coverage。

## 四、长度偏差与 mediator

Judge 可能偏好更长、更详尽的答案。Raw win rate 混合：

$$
\text{model}\to\text{content quality}\to Z
$$

与

$$
\text{model}\to\text{length}\to Z.
$$

Length-controlled AlpacaEval 用回归估计当长度差设为 0 时的反事实偏好。它依赖模型形式、overlap/positivity 与“控制后无未测混杂”等假设；不是简单把两个回答截成同长。

同时报告 raw WR、length-controlled WR 和长度分布。若目标用户本就偏好详尽，长度可能是效用的一部分而非纯偏差；rubric 必须定义。

## 五、其他常见偏差

- **self-enhancement/family bias**：judge 偏好自身或熟悉风格；
- **verbosity/style**：标题、列表、礼貌、引用外观替代内容；
- **reference anchoring**：先看到参考影响评分；
- **knowledge gap**：judge 不知道领域事实；
- **rubric leakage**：候选迎合可见判分词；
- **shared failure**：generator 与 judge 同样相信错误。

缓解包括匿名 labels、随机/双向顺序、多个异质 judge、人类锚点、事实工具、rubric 分维、adversarial probes；没有一个技巧能消除所有偏差。

## 六、人类锚点与 agreement

在人标集上建立 confusion matrix，报告：

- pairwise accuracy / tie-aware agreement；
- judge 与人类及人类之间的一致性；
- 按领域、长度差、难度、模型家族切片；
- disagreement adjudication；
- calibration/abstention；
- 成本与 latency。

“与人类 80% 一致”需说明哪群人、何种 majority、tie 如何处理及 chance baseline。人类也不是无噪真值；领域任务需合格 annotators。

## 七、选择与泄漏

若用 judge J 反复优化模型，再用同 J 报 test，系统会学习 judge 的偏好代理。应有：

1. development judge/rubric；
2. frozen independent test judge；
3. human or executable anchor；
4. unseen adversarial prompts；
5. 原始输出公开以供复审。

Judge version 漂移会让时间序列不可比。保存输出后尽量离线重评多个 judge 版本；无法固定闭源 API 时明确 evaluation date。

## 八、图解：位置交换、长度路径与人类锚点

**读图问题**：同一对回答交换 A/B 位置后为何会改变判决，长度差又如何沿另一条路径影响 judge，哪些冲突必须交给人类锚点？

![[00-知识库管理/_assets/figures/language-models/fig-lm-eval-judge-bias-v1.svg|900]]

> [!figure] 图 LM-62　AB/BA 交换矩阵、长度 mediator 与多裁判校准
> **生成：**本库按 pairwise judge、swap consistency 与 length-control 因果图绘制；胜负格和人标数是教学示意。

**怎样读图**：先把 AB/BA 结果映射回候选身份，识别一致胜、稳定 tie 和位置冲突；再沿长度 mediator 区分 raw 与 controlled estimand，最后用人类/可执行真值审计 judge。

**图没有证明什么**：双向顺序一致不证明 judge 正确，长度控制也不消除知识、家族和风格偏差；多个相似 judge 的多数票仍可能共享同一系统错误。

## 九、常见错误与出口标准

错误包括：judge 名替代版本；不换位；删除 tie；同 prompt 多判当独立；只报相关系数；长度控制当截断；开发/测试同 judge；judge rationale 当证据。

完成本节后，应能计算 swap consistency/tie-aware WR，设计 length/confound audit，构造 judge 偏差探针，按 prompt 做区间，并写含人类锚点与版本冻结的裁判协议。

## 十、来源与练习

- [[S-2023-Zheng-LLM-Judge]]；
- [[S-2024-Wang-Fair-Evaluators]]；
- [[S-2024-Dubois-Length-Controlled-AlpacaEval]]；
- [[习题 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]；
- [[解答 - LLM-as-a-Judge、Pairwise Preference、位置与长度偏差]]。
