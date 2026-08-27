---
type: concept
status: verified
area: [language-models, evaluation, factuality, grounding]
node_id: LM-61
aliases: [幻觉分解, 事实性与归因]
prerequisites: ["[[Context Construction、Citation、Grounding 与冲突证据]]", "[[语言模型评估对象、任务单位与 Benchmark 合同]]"]
related: ["[[Proper Scoring、Calibration、ECE 与 Selective Generation]]", "[[能力—行为—系统评估协议与证据地图]]"]
sources: ["[[S-2023-Min-FActScore]]", "[[S-2021-Petroni-KILT]]", "[[S-2023-Gao-ALCE]]", "[[S-2023-Su-9632-NBCE]]"]
exercises: ["[[习题 - Hallucination、Factuality、Grounding 与 Attribution 分解]]"]
solutions: ["[[解答 - Hallucination、Factuality、Grounding 与 Attribution 分解]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-eval-factuality-lattice-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Hallucination、Factuality、Grounding 与 Attribution 分解

> [!abstract] 一句话结论
> “幻觉”不是一个可直接计数的自然类别。应把输出拆成原子命题，并分别判断世界事实、给定来源支持、上下文一致、引用指向与生成因果依赖；同一句话可在这些轴上呈现不同真值。

## 一、先定义命题与时点

把回答 $y$ 分解为 atomic claims

$$
C(y)=\{c_1,\ldots,c_m\}.
$$

“2026 年 8 月 26 日，X 公司 CEO 为 A，且公司位于 B”至少含时间、职务、人名、地点多个可独立核验命题。分解太粗会让部分真/部分假无法标；分解太细会把语义依赖拆坏。需记录 decomposition protocol 与 annotator。

每个 claim 要绑定：

- claim type：事实、意见、预测、指令、数学推导；
- valid time 与 query time；
- relevant population/world；
- 可接受来源集合与权威优先级；
- unknown/ambiguous 是否允许。

未来预测不应被强迫标成当前 false；不可核验也不等于 false。

## 二、五个不同事件

对 claim $c$、世界状态 $W_t$、给定 context $X$、引用 span $e$：

1. **Factuality** $F(c,W_t)$：命题在目标世界/时点是否为真；
2. **Source support** $S(e,c)$：证据 span 是否蕴含该精确命题；
3. **Grounding** $G(c,X)$：输出是否与指定上下文一致/可由其支持；
4. **Attribution correctness** $A(e,c)$：引用是否精确指向支持源；
5. **Faithfulness/causal use** $U(c,e)$：系统是否真的依赖该证据形成命题。

可能组合：

- 事实为真但引用无关：$F=1,A=0$；
- 来源支持旧信息但当前世界已变：$S=1,F=0$；
- 回答与错误 context 一致：$G=1,F=0$；
- 参数记忆答对且附上支持引用：$F=S=A=1$，但 $U$ 未知；
- 无引用的正确常识：$F=1$，attribution 不适用或 completeness 失败，取决于任务合同。

## 三、Atomic factual precision

FActScore 风格的 claim precision：

$$
\operatorname{FactPrecision}
=\frac{\#\{c_i:\text{supported by designated source}\}}
{\#\{c_i:\text{eligible atomic facts}\}}.
$$

它不惩罚遗漏的重要事实，因此不是 factual recall。回答只说一个安全真命题可得高 precision，却信息不足。若任务有 gold fact set $G$，可另算 coverage/recall；开放世界下 gold 常不完备。

Unknown 的分母处理必须声明：记错、排除或单列会改变分数。更透明的输出是 supported/contradicted/unknown/unverifiable 四项计数。

## 四、Citation 两个分母

设回答有 $M$ 个需引用 claims，其中 $K$ 个带引用；共有 $J$ 个 citations，其中 $J_s$ 个真正支持对应 claim：

$$
\operatorname{CitationCompleteness}=\frac{K}{M},
\qquad
\operatorname{CitationCorrectness}=\frac{J_s}{J}.
$$

Completeness 高不代表 citation 正确；correctness 高也可能只给少量引用。还需 source quality、时效、span precision 与冲突处理。

## 五、Intrinsic、extrinsic 与 task contract

摘要任务常将：

- 与 source 矛盾称 intrinsic hallucination；
- source 未提供的新信息称 extrinsic hallucination。

但 extrinsic 不必然为假：模型可能补充正确常识。若任务要求“只根据文档”，它违反 grounding contract；若任务允许外部知识，则需世界核验。术语必须跟 task contract 绑定。

RAG 任务还要区分 corpus 不含证据、retriever 没取到、context 丢失、generator 未使用、答案错、引用错。把所有下游失败都叫“模型幻觉”会阻断根因诊断。

## 六、自动评估也是一条 RAG

自动 factuality judge 常执行：

$$
\text{claim decomposition}
\to\text{retrieval}
\to\text{support classifier/judge}
\to\text{aggregation}.
$$

它有自己的 corpus、retrieval recall、NLI/judge error 与版本。自动分数应在独立 human-labeled set 上报告 claim-level confusion matrix、unknown、inter-annotator disagreement，并保留原始 spans。不能用同一个 generator 既生成又无审计地裁判。

## 七、冲突、时间与来源权威

若两来源冲突，先检查 effective time、版本与定义，再按预注册权威层级处理。可标：

$$
\{\text{supported},\text{contradicted},
\text{mixed},\text{unknown}\}.
$$

“多数网页都这么说”不是可靠聚合：复制链会制造伪独立多数。保存 provenance，去重转载，优先原始/官方来源并展示真实冲突。

## 八、图解：一个命题的五轴事件晶格

**读图问题**：为什么同一个 claim 可以事实正确却引用错误、与 context 一致却世界为假，自动 judge 又在哪些层产生新的误差？

![[00-知识库管理/_assets/figures/language-models/fig-lm-eval-factuality-lattice-v1.svg|900]]

> [!figure] 图 LM-61　World—source—context—citation—causal-use 五轴分解
> **生成：**本库按 atomic claim、R/G/A 与时点来源协议绘制；方格组合为教学反例，不是某个 benchmark 的混淆矩阵。

**怎样读图**：先对一个 atomic claim 逐列判世界、source、context、citation 和 causal use，再沿下方自动评估链检查 decomposition、retrieval 与 judge；不要从任一单列推断其他列。

**图没有证明什么**：事件定义清楚不意味着世界真值容易获得，也不证明自动 judge 足够可靠；开放世界、时效冲突、来源复制和命题歧义仍需人工/领域审计。

## 九、常见错误与出口标准

错误包括：整段一个标签；unknown 当 false；grounded 当 factual；有引用当支持；支持当因果使用；只算 precision 不算 coverage；自动 judge 无人标校准；忽略时点。

完成本节后，应能分解 atomic claims，构造五事件反例，计算 factual/citation 分母，设计冲突与 unknown 协议，并把自动事实评估自身写成可审计检索—裁判系统。

## 十、来源与练习

- [[S-2023-Min-FActScore]]；
- [[S-2021-Petroni-KILT]]；
- [[S-2023-Gao-ALCE]]；
- [[S-2023-Su-9632-NBCE]]；
- [[习题 - Hallucination、Factuality、Grounding 与 Attribution 分解]]；
- [[解答 - Hallucination、Factuality、Grounding 与 Attribution 分解]]。
