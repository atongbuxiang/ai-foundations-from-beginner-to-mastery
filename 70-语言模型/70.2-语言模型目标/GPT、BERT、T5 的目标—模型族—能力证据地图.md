---
type: concept
status: verified
area: [language-models, evidence, gpt, bert, t5]
node_id: LM-16
aliases: [GPT BERT T5 对比, 语言模型证据地图]
prerequisites: ["[[概率语言模型、链式法则与自回归因子化]]", "[[Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]", "[[Prefix LM、UniLM 与序列到序列 Mask 合同]]"]
related: ["[[Decoder-Only、Prefix 与架构家族比较]]", "[[语言模型完整课程地图与掌握标准]]"]
sources: ["[[S-2018-Radford-GPT]]", "[[S-2019-Devlin-BERT]]", "[[S-2020-Raffel-T5]]", "[[S-2020-Su-7867-中文T5]]", "[[S-2020-Su-7764-MLM-PET]]", "[[S-2021-Su-8209-T5-PEGASUS]]"]
exercises: ["[[习题 - GPT、BERT、T5 的目标—模型族—能力证据地图]]"]
solutions: ["[[解答 - GPT、BERT、T5 的目标—模型族—能力证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-gpt-bert-t5-evidence-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# GPT、BERT、T5 的目标—模型族—能力证据地图

> [!abstract] 一句话结论
> GPT、BERT、T5 是“目标、可见性、架构、数据、规模、迁移与解码”多轴配置的历史实例，而不是三条由名字决定的能力定律。比较它们时必须先对齐研究问题和预算，再把构造事实、理论结论、原论文实验和后续经验分层。

## 一、先拆掉品牌式比较

“GPT 擅长生成、BERT 擅长理解、T5 两者兼顾”可作入门记忆，却不是因果解释。一个模型的观测能力至少由下列变量共同决定：

$$
\text{Outcome}=F(
\text{objective},\text{architecture},\text{visibility},
\text{tokenizer},\text{data},\text{scale},\text{optimization},
\text{transfer},\text{decoding},\text{evaluation}).
$$

不同论文通常同时改变多个变量。若不能做控制变量实验，就只能陈述相关证据和合理机制，不能把差异唯一归因于预训练目标。

## 二、三种经典配置

| 轴 | GPT（2018 实例） | BERT（2019 实例） | T5（2020 实例） |
|---|---|---|---|
| 主要预训练目标 | 左到右 CLM | MLM，并含论文特定辅助目标 | span corruption 的 text-to-text |
| 概率对象 | $p(x)=\prod_t p(x_t\mid x_{<t})$ | corrupted context 上的 masked conditionals | $p(y\mid\widetilde x)=\prod_u p(y_u\mid\widetilde x,y_{<u})$ |
| 主体架构 | Transformer decoder 风格 | Transformer encoder | Transformer encoder–decoder |
| source 可见性 | 过去 token | corrupted input 内双向 | encoder source 内双向 |
| 输出接口 | 自回归 token sequence / task head | token/classification head，常微调 | 统一 text-to-text decoder |
| 预训练—下游桥梁 | 输入变换 + 微调 | task head + 微调 / cloze 化 | task prefix + text target |
| 原生生成路径 | 直接 ancestral decoding | 需迭代填空或另设解码程序 | decoder 自回归生成 |

表中描述的是代表性论文配置，不覆盖后来所有同名系列。例如“GPT”不能自动代表今天任意 decoder-only LLM；“BERT”也不能涵盖所有 encoder masked models。

## 三、目标诱导的直接训练信号

### GPT/CLM

每个非首 token 都可成为 target，训练信号稠密；条件只含左侧信息，部署自回归生成与目标分解一致。但给定右上下文的 token 表示不是训练条件的一部分。

### BERT/MLM

每次只对抽中的位置计分，单 batch 直接 target 较稀疏；每个 target 可利用双向 corrupted context，适合产生全局条件表示。标准 MLM 不直接提供一个单次左到右联合 likelihood。

### T5/span corruption

encoder 读压缩后的双向 source，decoder 连续生成被删 spans；它同时训练 source encoding、cross-attention 与自回归 target。输出序列通常比 clean input 短，但 encoder–decoder 每层计算结构不同。

这些是由合同直接推出的机制事实，不等于下游排行榜结论。

## 四、计算与服务接口不能漏掉

同参数量不等于同 FLOPs 或同内存：

- decoder-only 生成时每个新 token 复用 KV cache，但上下文 cache 随序列增长；
- encoder-only 对固定输入一次双向编码，分类任务无需逐 token 解码；
- encoder–decoder 先计算固定 encoder memory，decoder 每步有 self-attention 与 cross-attention；
- span corruption 的 source/target 长度由 sampler 决定；
- tokenizer fertility 会改变三类模型的实际序列长度。

若问题是在线生成成本，BERT 的分类吞吐不是相关对照；若问题是固定文本分类，强制所有模型生成长标签串也可能偏置比较。

## 五、能力主张的证据分层

本库采用以下标签：

- `I`（Identity/Construction）：由定义或代码构造直接成立；
- `T`（Theory）：在明确假设下可证明；
- `A`（Assumption）：分析或实验依赖、尚未由结果验证；
- `E`（Experiment）：指定数据、模型、预算和指标下的实验；
- `H`（Hypothesis）：待检验机制解释；
- `O`（Observation）：实践观察或案例，外推范围有限。

示例：

| 主张 | 标签 | 边界 |
|---|---|---|
| 标准 causal relation 禁止 query 读取未来 key | `I` | 前提是实现与定义一致 |
| 期望 log loss 在真实条件分布处最小 | `T` | 充分表达、总体风险与 proper scoring 假设 |
| 双向 context 因而提升某分类任务 | `H/E` | 需对齐数据、参数、预算的消融 |
| T5 把论文中的多任务统一为 text-to-text | `I/E` | 接口统一，不是指标和决策统一 |
| 中文 T5 在某配置上有良好生成结果 | `O/E` | 依赖模型、数据、任务与解码参数 |

## 六、怎样设计公平的三方实验

先选择 estimand，例如：

> 在固定原始训练字节、近似训练 FLOPs、参数范围和监督数据下，三种预训练配置对中文摘要的样本效率与部署成本有何差异？

然后至少控制或记录：

1. **数据**：相同原始语料、去重、语言/领域采样与 contamination audit；
2. **tokenizer**：最好共享；若不共享，报告 raw bytes、fertility 与 BPB；
3. **预算**：训练 FLOPs、有效 target token、wall-clock 与能耗均留账；
4. **模型**：参数量、层深/宽、context length 与 normalization；
5. **迁移**：相同监督样本与调参预算，分别允许架构自然接口；
6. **评价**：任务质量、校准、稳健性、安全、吞吐、首 token 延迟、峰值显存；
7. **重复性**：多个 seed、置信区间和失败样本分析。

完全控制所有轴通常不可能，因此结果应写成“在此协议下”的条件结论。

## 七、反事实问题比标签更有价值

为了判断某能力来自哪里，应问：

- 保持架构不变，只换 CLM/MLM/span objective 会怎样？
- 保持目标不变，只换单栈 prefix 与 encoder–decoder 会怎样？
- target-token 数相同但 FLOPs 不同时，哪种预算更符合问题？
- 去掉 task prefix、mode tag 或 NSP 后结果怎样？
- 将 tokenizer fertility 与原始 byte budget 对齐后优势是否保留？
- 用同一解码搜索和输出长度约束后，生成差异是否保留？

这些问题把“模型名称比较”改造成可证伪的实验设计。

## 八、图：从目标到能力主张的证据链

先看图回答：为什么从“BERT 使用双向 MLM”不能一步推出“BERT 的理解能力更强”？

![[00-知识库管理/_assets/figures/language-models/fig-lm-gpt-bert-t5-evidence-v1.svg|900]]

> [!figure] 图 LM-16　GPT、BERT、T5 的多轴配置与证据分层
> 图把目标/架构/可见性放在左侧，把数据/规模/迁移/解码作为中介轴，再把能力结论按 `I/T/A/E/H/O` 分类。来源：本课程依据 GPT、BERT、T5 原始论文与中文实践材料独立绘制。

**怎样读图**：从一条能力主张逆向追踪它依赖的全部配置轴，标出哪些是定义、哪些是实验、哪些只是解释假设。

**图没有证明什么**：图不裁定哪个模型族“总体最好”，不把历史论文结果外推到现代规模，也不认为所有能力都能被一个 benchmark 完整测量。

## 九、读论文与博客的最小审计表

```yaml
claim: ...
evidence_type: I | T | A | E | H | O
probability_object: ...
corruption_sampler: ...
attention_relation: ...
loss_region_and_denominator: ...
architecture: ...
data_and_tokenizer: ...
training_budget: ...
transfer_and_decoding: ...
metric_and_uncertainty: ...
scope_of_generalization: ...
missing_counterfactual: ...
```

原论文是配置与当时实验的一级来源；博客适合提供推导、中文语境和实践线索，但应沿链接回到论文/代码核验关键数字。科学空间的中文 T5、T5 PEGASUS 与 MLM/PET 条目在本库均作为具体案例，不替代普遍因果证据。

## 十、卷终出口

完成本节后，你应能对任意语言模型配置回答五个问题：它对什么概率对象建模？输入怎样破坏或分段？谁能看见谁？哪些位置进入 loss、分母是什么？能力主张属于哪类证据？这五问是进入下一卷训练数据与规模理论前的最低研究资格。

## 练习与独立解答

- [[习题 - GPT、BERT、T5 的目标—模型族—能力证据地图]]
- [[解答 - GPT、BERT、T5 的目标—模型族—能力证据地图]]
