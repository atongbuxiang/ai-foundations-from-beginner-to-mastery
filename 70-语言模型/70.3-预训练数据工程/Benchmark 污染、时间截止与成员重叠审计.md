---
type: concept
status: verified
area: [language-models, pretraining-data, benchmark-contamination, evaluation]
node_id: LM-20
aliases: [Benchmark contamination, Decontamination, 测试集污染]
prerequisites: ["[[精确去重、MinHash、LSH 与近重复检测]]", "[[训练集、验证集、测试集与自适应复用]]"]
related: ["[[数据版本、Provenance、有效 Token 与证据地图]]", "[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]"]
sources: ["[[S-2020-Brown-GPT3-Contamination]]", "[[S-2021-Dodge-C4-Documentation]]", "[[S-2022-Lee-Deduplicating-LM]]", "[[S-2024-Li-Open-Contamination]]"]
exercises: ["[[习题 - Benchmark 污染、时间截止与成员重叠审计]]"]
solutions: ["[[解答 - Benchmark 污染、时间截止与成员重叠审计]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-data-contamination-time-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Benchmark 污染、时间截止与成员重叠审计

> [!abstract] 一句话结论
> 污染至少要分成训练数据 exposure、参数中的 memorization、提示下的 retrieval 与分数上的 exploitation。字符串重叠 detector 只能测其中一部分；可信结论需要冻结时间轴、定义成员单位、报告检测器 operating point，并把“未发现”写成有条件的阴性结果。

## 一、四个常被混写的事件

设 benchmark item 为 $z=(q,a,m)$（问题、答案、metadata），训练管线实际读取的数据为 $\mathcal D$。

1. **Exposure**：$z$ 或其相关表示进入某阶段训练/选择数据；
2. **Memorization**：模型参数对该 item 保留可检测的信息；
3. **Retrieval/Recognition**：给定 prompt 时模型能从参数/外部系统唤起该信息；
4. **Exploitation**：这种 exposure 对评测决策或分数产生因果增益。

逻辑上：exposure 不必导致 memorization；memorization 不必被当前 prompt 唤起；重叠分数高不证明性能增益来自污染。反过来，翻译、paraphrase、答案解析、教程和 synthetic data 可造成 exposure，却逃过 exact detector。

## 二、成员单位必须明确

“benchmark 在训练集里”可能指：

- 完整 `(question, options, answer)`；
- 只有 question；
- question + 错/对 options，无 label；
- answer/explanation 在独立网页；
- 任务 instruction 或大量同模板 examples；
- 句子/n-gram 片段；
- paraphrase、翻译、截图 OCR 或代码变体；
- validation/test 的 ancestor dataset。

不同单位对应不同作弊路径。Input-only exposure 对事实问答可能足够有用，对随机标签分类则未必；label exposure 更直接。审计 schema 应把 `input`, `label`, `rationale`, `metadata`, `task template` 分列。

## 三、时间截止的证据链

至少保存五个时间：

$$
t_{draft},\ t_{release},\ t_{crawl},\ t_{train\_cutoff},\ t_{eval}.
$$

若 $t_{release}>t_{train\_cutoff}$，直接公开 benchmark exposure 的风险降低，但不能归零：draft/private access、ancestor datasets、post-training、retrieval index 和 API 更新仍可能跨越。若只知道模型发布日期，不知道 pre/post-training cutoff，不能把“模型早于 benchmark”当完整证明。

最强程序之一是 prospective/private test：在训练 cutoff 后新收集、受控保存、仅通过评测服务访问，并追踪每次访问。但它仍需防 prompt/label 反馈进入未来版本。

## 四、四类 detector

### Exact/hash

对 canonical strings 或 item IDs 比较。Precision 高、可解释，但漏格式、空白、顺序、paraphrase与 substring。

### N-gram/substring

对 benchmark 与训练文档计算最长匹配、Jaccard、containment 或命中比例。Common phrase 会假阳；短题/代码的 base rate 不同，应按长度分层阈值。

### Semantic/paraphrase

Embedding/跨语言/LLM judge 可提高改写召回，却更依赖模型、threshold 和候选库，可能把同主题不同答案误判。Detector 自身也可能被 benchmark 污染。

### Black-box behavior

当训练语料不可见，可比较 canonical order 与 shuffled order 的 likelihood、补全罕见 canary、选项顺序敏感性或发布日期切片。它提供统计异常，不唯一识别 exposure 来源。

> [!important] Detector 是分类器
> 必须在人工标注或可控注入数据上估计 precision/recall、按 item length/语言/任务切片，并报告 threshold sweep。`overlap=0%` 若来自高阈值 detector，只是低 recall 的输出。

## 五、Base rate 与假阳

设真正 contaminated 比例为 $\pi$，detector sensitivity $r$、false-positive rate $f$。检测为阳性的后验概率：

$$
P(C=1\mid +)=\frac{r\pi}{r\pi+f(1-\pi)}.
$$

当 $π$ 很小，即使 $f$ 看起来小，阳性中也可能有大量假阳。反之，严格阈值令 $f$ 低却可能漏掉语义变体。应报告 confusion matrix 或 credible interval，不能把 detector 标记当真实 membership label。

### 手算

$\pi=1\%,r=80\%,f=2\%$ 时

$$
P(C=1\mid +)=\frac{0.008}{0.008+0.0198}\approx28.8\%.
$$

因此自动 detector 的每个阳性不能直接当法证结论。

## 六、Clean/dirty 分数差怎样解释

设 detector 标记 $H_i\in\{0,1\}$，模型正确 $Y_i$。常报告

$$
\widehat\Delta=\bar Y_{H=1}-\bar Y_{H=0}.
$$

这不是污染的因果效应，因为 $H$ 与 item 难度、长度、常见性和领域相关：容易/常见题本来就更可能在 web 出现。需要难度匹配、时间/来源控制、可控注入、同 item 变体或随机化实验。即使 dirty subset 高 10 分，也只能先说关联。

反之 $Δ\approx0$ 不证明污染无影响：detector noise、ceiling、样本小、模型未利用或 clean subset 也污染都可掩盖差异。

## 七、训练前 decontamination 的陷阱

- 只删 test exact strings，保留答案解析、翻译和 mirrors；
- 先 tokenize/normalize 后 detector 与 raw item 不一致；
- benchmark 后续版本更新但 blocklist 未更新；
- 删除过宽 n-gram，误伤与任务相关但非泄漏的自然文本；
- 用 test set 调 filter threshold，反复反馈形成 adaptive leakage；
- 保存删除后的 token count，却不保存 removed IDs/reason；
- post-training、SFT、RAG index 与 prompt library 未纳入同一 cutoff。

Decontamination 应跨所有 data stages 建 exclusion manifest；evaluation set 访问要审计，未来模型版本需继承污染事件记录。

## 八、图：时间、检测与利用分三层

先看图回答：为什么“benchmark 发布时间晚于 crawl snapshot”是强证据，却仍不是绝对无污染证明？

![[00-知识库管理/_assets/figures/language-models/fig-lm-data-contamination-time-v1.svg|900]]

> [!figure] 图 LM-20　Benchmark contamination 的三条证据链
> 上方锁定 draft/release/crawl/train/eval 时间；左下列 detector 与盲点；右下把 exposure 与 exploitation 交叉。来源：本课程依据 GPT-3 contamination protocol、C4/dedup 审计及开放污染报告独立绘制。

**怎样读图**：先检查时间上是否可能进入，再用多 detector 找 exposure，最后另做性能/行为实验判断利用；不要从一个红格跳过中间层。

**图没有证明什么**：时间和 overlap 不能直接读出记忆量或因果分数增益；black-box 阴性也不能证明未见过。

## 九、最小审计报告

```yaml
model_and_data_version: ...
pretrain_sft_rag_cutoffs: ...
benchmark_version_and_release: ...
membership_unit: input | label | rationale | template | semantic
normalization: ...
detectors:
  - method, threshold, calibration set, precision, recall
candidate_and_verified_counts: ...
clean_dirty_item_ids: ...
score_by_slice_with_ci: ...
confounders: difficulty, length, frequency, domain
decontamination_manifest: ...
unobservable_stages: ...
claim: detected / not detected under this protocol
```

## 十、本节出口

你应能区分 exposure/memorization/retrieval/exploitation，推导 detector 阳性后验，解释 clean/dirty gap 的混杂，并设计含时间截止与多阶段数据的污染报告。下一节[[数据混合、温度采样、重加权与域损失]]研究不同数据域在未泄漏前提下怎样获得训练权重。

## 练习与独立解答

- [[习题 - Benchmark 污染、时间截止与成员重叠审计]]
- [[解答 - Benchmark 污染、时间截止与成员重叠审计]]
