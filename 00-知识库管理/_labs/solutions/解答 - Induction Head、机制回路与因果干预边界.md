---
type: solution
status: verified
area: [language-models, mechanistic-interpretability, induction-heads]
topic: "[[Induction Head、机制回路与因果干预边界]]"
exercise: "[[习题 - Induction Head、机制回路与因果干预边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Induction Head、机制回路与因果干预边界

## A. 识别与复述

### LM36-A01
Prefix matching 测当前 token 是否注意到先前由相同前缀引出的候选位置；copying 测该 head 的输出是否提高被注意 token 的相同 token logit。二者分别约束选址与写回效果。

### LM36-A02
QK 用 query-key 相似度和 mask 决定 attention weights，即“看哪里”；OV 将被选 value 映射回 residual stream，即“写什么”。同一 attention pattern 可因 OV 不同产生相反 logit 效应。

### LM36-A03
Necessity 是移除后行为下降，sufficiency 是植入/保留即可产生行为，mediation 是输入到输出效应经该路径传递多少，redundancy 是其他回路可补偿。同一回路可功能真实却非必要。

## B. 手算与构造

### LM36-B01
第二个 A 是 current A，第一个 A 是 earlier A；被复制的是 earlier A 紧随的 B。预测位置是问号，目标变为 B。

### LM36-B02
令 head 在 query 对早先 B 的 attention 为 0.9，但 $W_UW_OW_Vh_B$ 在 B-logit 坐标为 -2。它高度看 B，却降低 B 概率，故 attention weight 不能单独解释输出。

### LM36-B03
Clean 为随机序列 $s$ 重复两次；corrupted 将第一遍中 A 后的 B 换成 C；patch 把 clean run 中候选位置/特定 head 激活注入 corrupted run。比较最终 B/C logits 与重复段 NLL，并用无关位置 patch 作 control。

## C. 推导与证明

### LM36-C01
$o_t=\sum_s\alpha_{ts}W_OW_Vh_s$，若 unembedding 为 $W_U$，直接 logit 贡献 $\Delta\ell_t=W_Uo_t=\sum_s\alpha_{ts}W_UW_OW_Vh_s$。这把 attention weight 与 token/logit 方向相乘。

### LM36-C02
第一头把位置 $s-1$ 的 token A 信息写到位置 $s$ 的 key；第二头用当前 A 的 query 匹配该 key，于是注意位置 $s$，而 $s$ 的 token 是 B；其 OV 将 B 方向写回并提升 B logit。

### LM36-C03
设两个冗余 heads $h_1,h_2$ 都实现复制，且下游取其和/最大。单独移除 $h_1$ 时 $h_2$ 补偿，行为差近零；同时移除才下降。因此小单头效应只否定“独占必要”，不否定功能或联合必要。

## D. 边界、反例与纠错

### LM36-D01
注意力图只给某层头的权重，不给 value 内容、OV 方向、残差/MLP 后续处理或因果必要性。解释至少要加 direct logit、干预和替代路径。

### LM36-D02
精确结果量词限特定层数、attention-only 结构、训练分布和重复任务。大模型含 MLP、更多层与冗余回路；观察相似 head 是外推证据，不是同一机制的形式证明。

### LM36-D03
零向量可能从未在自然激活分布出现，并改变 LayerNorm 尺度。替代可用 mean/resampled ablation、从 matched corrupted example patch、pattern-preserving value replacement，并与随机头/位置同规模干预比较。

## E. AI 迁移

### LM36-E01
在重复随机 token 上算每头 prefix score 与 direct copying score，预注册阈值；matched controls 按层、head norm 和平均 attention entropy 配对。报告二维分布，不只挑一个漂亮头。

### LM36-E02
先测 clean/corrupted gap，再逐头/成对 ablation；activation patch 从 clean 到 corrupted。恢复比例为 $(M_{patch}-M_{corr})/(M_{clean}-M_{corr})$，同时报告 over-recovery、随机 patch 和多任务副作用。

### LM36-E03
先验证翻译行为与随机 label 控制；定位跨语言 prefix/copy pattern；做 direct logit 和 activation patch；消融后测翻译而非仅复制；检验其他语言/模型；最后比较 alternative heads/MLP 与联合干预，才能从相关升级到局部因果机制。
