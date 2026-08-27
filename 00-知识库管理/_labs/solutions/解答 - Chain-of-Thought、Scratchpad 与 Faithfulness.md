---
type: solution
status: verified
area: [language-models, reasoning, faithfulness]
topic: "[[Chain-of-Thought、Scratchpad 与 Faithfulness]]"
exercise: "[[习题 - Chain-of-Thought、Scratchpad 与 Faithfulness]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Chain-of-Thought、Scratchpad 与 Faithfulness

## A. 识别与复述

### LM37-A01
Outcome correctness 看最终 $y=y^*$；local validity 看各步是否由前提推出；executable sufficiency 看执行整条链是否得到答案；causal faithfulness 看链是否反映真正影响模型输出的因素。它们可任意组合，不应合为“推理正确”。

### LM37-A02
五种为增加串行计算深度、把难题分解为局部模式、提供外部工作记忆、激活预训练解题分布，以及为多路径搜索/验证提供状态。实验需用长度、结构和搜索对照区分。

### LM37-A03
每个可见 token 产生前，模型已在多层激活中计算；隐藏状态还可直接影响答案而不经过文字链。CoT 是可见输出通道/工作区，不是分布式内部状态的逐字抄本。

## B. 手算与构造

### LM37-B01
$p(r,y\mid x)=p(r\mid x)p(y\mid x,r)$；答案边缘概率 $p(y\mid x)=\sum_r p(r\mid x)p(y\mid x,r)$。连续/巨大路径空间中求和只是概念式，实践用有限采样近似。

### LM37-B02
例如“3 箱每箱 4 个”：链写 $3+4=7$，随后输出 12。答案正确，但执行链得 7，故 local validity/executable sufficiency 失败。

### LM37-B03
Truncate 时用等长 filler 控制 token 数；paraphrase 时由独立标注确认语义保持并匹配长度；error injection 时在相同位置注入无害/正确替换作对照。所有条件冻结后缀重采样规则。

## C. 推导与证明

### LM37-C01
Greedy 选择单条 $\hat r=\arg\max p(r\mid x)$，再基于它输出；边缘化则对所有 $r$ 按 $p(r\mid x)$ 加权。除非该路径概率为 1 或各路径给同一答案，两者一般不同。

### LM37-C02
可比较 $P(Y=y\mid do(R=r'))-P(Y=y\mid do(R=r))$，实践用固定问题和前缀，对 trace 做截断/patch 后重新生成答案。需声明干预是否保持长度、语义与 sampling randomness。

### LM37-C03
若 solver 对形式链 $z$ 确定执行，系统输出 $y=S(z)$，则 $z$ 对 $y$ 构造性充分。但自然语言 $x$ 到形式规范 $z=P(x)$ 的翻译可能漏约束/误解析；保证只从已生成 $z$ 开始，不保证 $z$ 忠于原题。

## D. 边界、反例与纠错

### LM37-D01
准确率提升只证明换 prompt/生成协议后 outcome 改善；可能来自更多 token、task cue 或 search，不揭示文字链是否含真实因果因素。需另做 trace/bias/activation 干预。

### LM37-D02
在多选题中加入“前面示例的正确选项总是 A”，模型据此选 A，却生成与题面一致的常识解释，完全不提位置规则。解释流畅且局部合理，但对决定性 cue 不完整。

### LM37-D03
CoT 多用数百 token，direct 只用数 token，性能差混入 test-time compute。应加入 matched filler、相同最大 token、单长链与多短链，并同时报实际 token/FLOPs/latency。

## E. AI 迁移

### LM37-E01
随机对一半样本注入不改变题面主体的 bias cue，测答案 flip；对被 cue 翻转样本标 CoT 是否提及 cue。联合报告 flip rate、mention rate、accuracy 和未注入 control，不能把未翻转样本混入分母掩盖效应。

### LM37-E02
在同一题/模型下预注册 direct、short/long valid CoT、scrambled steps、等长无信息 filler；再匹配总 token 比较一长链与多短链。保存输出长度、答案和 step validity，分离结构与预算。

### LM37-E03
自由 trace 只作辅助说明；事实结论附可定位外部证据；计算/约束由可执行程序或 solver 验证；最终 UI 分别标“模型解释”“证据”“检查结果”，并记录不一致/拒答规则。
