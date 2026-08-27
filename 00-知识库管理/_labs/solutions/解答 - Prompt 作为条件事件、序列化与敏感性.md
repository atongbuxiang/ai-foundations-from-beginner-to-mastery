---
type: solution
status: verified
area: [language-models, prompting, in-context-learning]
topic: "[[Prompt 作为条件事件、序列化与敏感性]]"
exercise: "[[习题 - Prompt 作为条件事件、序列化与敏感性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Prompt 作为条件事件、序列化与敏感性

## A. 识别与复述

### LM33-A01
任务语义是人定义的预测目标；rendered bytes 是模板、空格、Unicode 等处理后的确切字节；token IDs 是 tokenizer 真正交给模型的整数；parser 把生成文本/IDs 变成评分对象。任一接口变化都可改变最终结果。

### LM33-A02
模型条件化于 $x=\operatorname{Tok}(T(m))$，不是人的语义等价类。语义等价改写只约束人的任务判断，不约束 token 前缀、位置和预训练频率相同，所以 $p(y\mid x)$ 没有相等保证。

### LM33-A03
Contextual calibration 用内容空输入估计当前 prompt/label 的输出偏置并做变换；统计 calibration 要求预测概率与事件频率匹配。前者可改善标签偏置，却不自动满足后者的 reliability 条件。

## B. 手算与构造

### LM33-B01
两标签第一个 token 都是 red，只看首 token 必然同分。完整序列在共同首 token 概率相消后比较 $0.7$ 与 $0.2$，因此选择 red fox。

### LM33-B02
四个翻转率分别为 $0/10=0$、$3/10=0.3$、$2/10=0.2$、$1/10=0.1$；等权平均为 $(0+0.3+0.2+0.1)/4=0.15$。若模板被抽样的概率不同，应按部署概率加权。

### LM33-B03
Manifest 可保存 raw bytes 为 Answer:positive 与 Answer: positive，分别记录 label IDs 如 [9132] 与 [2457]、tokenizer hash、template、answer offset、raw log-probs 和 parser。关键是把肉眼空格差异与最终 ID 差异同时保存。

## C. 推导与证明

### LM33-C01
链式法则给 $\log p(v(c)\mid x)=\sum_j\log p(v_j\mid x,v_{<j})$。长度归一化除以 $|v|^\alpha$ 会改变类别排序；它是在定义 scorer，不是代数上必然正确的步骤，必须固定并验证。

### LM33-C02
取两个样本：变换前一对一错，变换后前者由对变错、后者由错变对。总准确率仍为 $1/2$，差为零，但两项预测都翻转，翻转率为 1。

### LM33-C03
对象是 $\max_{m\le M}\widehat A_m$，不是随机或预先固定模板的准确率。有限验证集噪声使最大值偏向偶然高估；若同一数据又作最终报告，选择偏差未被独立测试消除。

## D. 边界、反例与纠错

### LM33-D01
UI 可能隐藏控制 token、规范化空白或自动模板；同一可见文本也可由不同 tokenizer 得到不同 IDs。必须比较最终 IDs、special-token map 与 generation boundary。

### LM33-D02
red fox/red panda 已给出平局例。反转例可令标签 A 为 [u]、B 为 [u,v]：首 token scorer 同分/偏 A，而完整序列因 $p(v\mid u)$ 很高选择 B；更一般地共享前缀会使首 token 丢失判别信息。

### LM33-D03
无法复现实际条件事件、label scorer 或评分输出。至少补 tokenizer/template revision、bytes/IDs、label IDs、generation/stop、parser 和 API/model revision；原字符串只能证明部分可见输入。

## E. AI 迁移

### LM33-E01
四轴分别预注册：格式的空格/换行；语义改写的同义 instruction；标签的 A/B、自然词及多 token；解码的 greedy/temperature/stop。其余对象冻结，做配对预测、翻转率和区间，避免一次改多轴。

### LM33-E02
字段含 provider/model revision、request timestamp、system/developer/user messages、template/flags、tokenizer、rendered bytes/IDs、label map/scorer、temperature/top-p/seed、max tokens/stop、raw response、parser version 和 dataset hash。

### LM33-E03
对每个样本保存基准与变体是否正确及是否翻转；按样本有放回 bootstrap，重算准确率差和翻转率区间。主报告给所有预注册模板分布，最佳模板只作为带选择规则的次要结果。
