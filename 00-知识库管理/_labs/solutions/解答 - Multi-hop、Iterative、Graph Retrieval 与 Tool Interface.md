---
type: solution
status: verified
area: [language-models, multi-hop-retrieval]
topic: "[[Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]"
exercise: "[[习题 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Multi-hop、Iterative、Graph Retrieval 与 Tool Interface

## A. 识别与复述

### LM47-A01
重复同一 query、并行多个来源或 retry 都是多次调用，却没有用前一步 observation 改变后一步信息需求。多跳的关键是证据/实体关系和状态依赖，而非调用计数。

### LM47-A02
至少有状态、动作、外部观察、状态转移与停止/预算。实践还要 policy、verifier、错误/回退和 provenance ledger。

### LM47-A03
Decompose-first 先固定子问题；交错策略随观察更新 query；图遍历沿显式节点/边扩展。它们分别偏向并行性、自适应性和结构约束，失败模式也不同。

## B. 手算与构造

### LM47-B01
在独立假设下 joint recall $=0.8\times0.7=0.56$。真实系统第二跳依赖第一跳，需直接统计联合事件。

### LM47-B02
$s_0=(q,\varnothing,\varnothing,B=2)$；$a_0=$search A relation；$o_1=$span 表明 A→B；$s_1$ 加实体 B；$a_1=$search B country；$o_2=$span 表明 B→C；verifier 检查两 span 后 answer C。每步保存 query、IDs、时间和成本。

### LM47-B03
第一次无新增证据时改写一次或走反证分支；第二次返回已见 ID，触发 duplicate-loop 检测。剩余一次不应盲重试：若无独立 query 策略则 abstain，并记录 stop_reason=no_new_evidence。

## C. 推导与证明

### LM47-C01
$s_t=(x,H_t,E_t,B_t)$，$a_t\sim\pi(\cdot\mid s_t)$，工具给 $o_t$，$s_{t+1}=F(s_t,a_t,o_t)$。预算更新含调用、token 与时间；终止动作 answer/abstain 需 verifier 条件。

### LM47-C02
第二跳 query 仅在第一跳命中后被正确构造，所以 $P(E_2\mid E_1)$ 与 $P(E_2\mid\neg E_1)$ 不同。联合率是 $P(E_1)P(E_2\mid E_1)$，只有独立时才为 $r_1r_2$。

### LM47-C03
Oracle first-hop 只固定第一证据，仍测试 query update、第二跳、融合与生成；oracle all-evidence 绕过全部检索，主要测试 context/reasoning/generation。两者差距定位后续检索能力，后者不是前者替代品。

## D. 边界、反例与纠错

### LM47-D01
模型可先凭隐藏状态/参数知识得答案，再生成流畅 CoT；也可在注入错误步骤后答案不变。可读性只证明文本存在，faithfulness 需删改步骤、bias cue、patch 等因果干预。

### LM47-D02
初始问药物 A 的批准状态；第一篇提到公司 B，系统改搜“公司 B 新闻”，再搜其股价，最终偏离批准状态，这是 query drift。若只搜“证明 A 已批准”则是 confirmation loop。

### LM47-D03
Reflection token 是模型对 relevance/support/utility 的预测，可能失准或共享 generator 偏差。需要人工/独立标签测 precision、recall、calibration，不能把被评对象自身判断当 gold。

## E. AI 迁移

### LM47-E01
字段含 call-id、parent-state、tool/schema/version、query/filter/K、corpus/index、returned doc/span IDs/scores、timestamp、latency/cost/error、next-state、used-by-claim。原始 observation 与模型摘要分开。

### LM47-E02
建立人工 retrieval-needed 标签；计算 retrieve gate precision/recall，特别报告 false negative 的答案风险和 false positive 的成本/噪声。按参数已知、时效、私有、多跳、不可回答切片。

### LM47-E03
逐题保存每 hop 的 evidence hit、joint chain、supporting facts、answer、calls/tokens/p50-p99、循环与 stop reason。主表给 joint success 与成本 Pareto，并有 oracle first-hop/all-evidence。
