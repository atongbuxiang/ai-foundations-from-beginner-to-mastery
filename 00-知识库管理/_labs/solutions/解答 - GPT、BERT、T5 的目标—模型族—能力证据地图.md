---
type: solution
status: verified
area: [language-models, evidence, gpt, bert, t5]
topic: "[[GPT、BERT、T5 的目标—模型族—能力证据地图]]"
exercise: "[[习题 - GPT、BERT、T5 的目标—模型族—能力证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - GPT、BERT、T5 的目标—模型族—能力证据地图

## A. 识别与复述

### LM16-A01
GPT 代表性配置：decoder-style causal stack，$p(x)=\prod_tp(x_t\mid x_{<t})$，只读过去。BERT：encoder 双向读取 corrupted input，只在 masked targets 拟合 $p(x_i\mid\tilde x)$。T5：encoder 双向读 span-corrupted source，decoder causal 且 cross-attends source，拟合 $p(y\mid\tilde x)=\prod_up(y_u\mid\tilde x,y_{<u})$。

### LM16-A02
`I` 是定义/构造直接成立；`T` 是在明确假设下的证明；`A` 是分析依赖的假设；`E` 是特定实验协议下结果；`H` 是待证伪机制解释；`O` 是范围有限的实践观察。标签帮助阻止从构造一步跳到普遍经验结论。

### LM16-A03
Text-to-text 把输入输出序列化为统一软件接口，但分类、翻译、摘要仍有不同数据生成、评价指标、成本矩阵与错误风险。字符串标签也不自动给出校准概率或最优决策规则。

## B. 手算与构造

### LM16-B01
至少控制：预训练数据与污染、参数量/深宽、训练 FLOPs/target 数、tokenizer/序列长度、迁移与调参预算、任务 head/解码、context length。否则“双向”和 observed accuracy 同时与多轴变化共变。

### LM16-B02
按定义实现的 causal mask 禁止未来可见为 `I`；T5 在数据集 X 更好为 `E`，需附协议；“双向性导致提升”是 `H`，若有只换 relation 的随机对照消融，可在该设置下升级为有条件的 `E`，仍不是普遍定理。

### LM16-B03
最小表的行是三种配置，列包括：raw-data hash、tokenizer、参数与架构、训练 FLOPs/bytes/targets、objective sampler、监督样本/调参 trials、任务指标与置信区间、吞吐/TTFT/显存、解码参数、多个 seed。每格不可比处显式标 N/A 或解释自然接口。

## C. 推导与证明

### LM16-C01
观察到 $F(o_1,a_1,d_1,\ldots)-F(o_0,a_0,d_0,\ldots)$ 同时包含所有坐标变化。Objective 的因果效应需要反事实 $F(o_1,a_0,d_0,\ldots)-F(o_0,a_0,d_0,\ldots)$；只有一组联合变化观测无法识别该反事实，除非加入强结构假设或控制实验。

### LM16-C02
CLM score 是链式 joint log-likelihood；MLM/PLL 是不同双向 conditionals 的和，未必规范化；T5 score 是给定 corrupted/source input 的 target conditional likelihood。事件空间与条件变量不同，哪怕都写成 token cross-entropy也不能直接等同。

### LM16-C03
Self-attention 约随序列长度平方增长；encoder–decoder 还含 source self、target self 与 source-target cross 项；decoder 生成逐步并使用 cache。目标 sampler 决定 source/target 长度，词表决定 softmax 代价。参数计数未固定激活长度、层调用次数与解码步数，故不决定 FLOPs。

## D. 边界、反例与纠错

### LM16-D01
把输入与类别 verbalizer 拼成序列，比较每个候选标签的 conditional log-likelihood；或在最终 token hidden state 加 classification head。Decoder-only 的 causal 骨架不阻止分类，差异在接口和效率。

### LM16-D02
Encoder 可在 iterative masked generation 中反复填空，可作为检索器/约束器/奖励模型指导另一个 generator，也可接非自回归或独立 decoder。它没有原生左到右 head，不等于不能成为生成系统组件。

### LM16-D03
现代设置改变了数量级规模与优化规律、训练数据/去重和 tokenizer、长上下文/指令微调/偏好对齐及推理系统。早期论文的任务基准也可能饱和或污染。历史结果可作实例，不能不经新实验外推。

## E. AI 迁移

### LM16-E01
至少记录：原文 claim；`I/T/A/E/H/O` 标签；概率对象与 mask/loss；模型/data/tokenizer/budget；metric/seed/uncertainty；对照组；作者实际证据；可推广范围；遗漏反事实。博客若引用论文，关键数字回链一级来源。

### LM16-E02
共享同一 tokenizer、raw corpus、参数量附近的同一 backbone；仅切换可实现的 CLM/MLM/span objective 与必要 output head；按 raw bytes 与 FLOPs 对齐，记录 target 数；统一优化 sweep 预算与下游数据，多 seed。承认 relation/output length 是 objective 的组成性中介，分别报告而非假装完全相同。

### LM16-E03
补交：任务与人群范围；数据/污染审计；模型规模与训练 FLOPs；tokenizer/上下文；objective；调参和监督预算；质量、安全、校准、稳健性、效率多指标；置信区间/seed；自然接口与解码；失败切片；时间/成本；可复现配置；“全面”的预注册聚合规则。否则应改写为“在指标 X、协议 Y 下更好”。

## 无提示重做

- [ ] 给任一能力主张贴证据标签并写外推边界。
- [ ] 设计一个只改变 objective 的反事实比较。
