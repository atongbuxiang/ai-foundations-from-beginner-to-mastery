---
type: solution
status: verified
area: [language-models, tokenization, evaluation]
topic: "[[Tokenizer 评估、多语言公平、安全与证据地图]]"
exercise: "[[习题 - Tokenizer 评估、多语言公平、安全与证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Tokenizer 评估、多语言公平、安全与证据地图

## A. 识别与复述

### LM08-A01
它们分别以 UTF-8 bytes、Unicode code points、UAX #29 grapheme clusters、外部语言 word segmentation 为分母；跨语言解释与版本依赖不同，不能统称“每字符”。

### LM08-A02
可逆/UNK/fallback；长度均值/尾部；词表大小/使用率；embedding/FLOPs/wall time；BPB/下游/鲁棒；special injection/confusable/控制字符/length DoS。

### LM08-A03
不使用特定语言规则只是实现属性。不同 UTF-8 长度、形态、语料比例与词表资源会造成 token/价格/截断/质量差异；公平需定义群体和成本结果。

## B. 手算与构造

### LM08-B01
总体按文档均值 $(900\cdot1+100\cdot4)/1000=1.3$；等组均值 $(1+4)/2=2.5$。总体 1.3 隐藏组 B 的四倍成本。

### LM08-B02
A 2.5 bytes/token，B 2.0。$BPB_A=800/(1000\ln2)\approx1.154$；$BPB_B=760/(1000\ln2)\approx1.096$。B 序列更长却字符串概率指标更好，说明压缩与模型 NLL不可互推。

### LM08-B03
同一文档的 token 数是 paired outcome；token 位置高度相关且数量由 tokenizer 决定，把 token 当 iid 会伪增样本量。应对文档/来源 block 的长度差 bootstrap，保留配对。

## C. 推导与证明

### LM08-C01
由全期望 $E[F]=\sum_gP(G=g)E[F|g]=\sum_g\pi_gF_g$。若组比例在数据集间变化，或某 tokenizer 在小组好/坏但总体由大组主导，总体排序可掩盖甚至逆转组内差异。

### LM08-C02
固定 token steps 比较每个 tokenizer 坐标下相同 update/序列预算，但原始 bytes 不同；固定 raw corpus 比较相同内容覆盖，却 token/FLOPs/steps 不同。前者不是数据等量，后者不是计算等量。

### LM08-C03
例如 A 4 bytes/token、special injection failure 5%；B 3 bytes/token、failure 0%。在吞吐优先权重下 A 可能优，在高风险工具系统 B 占优。没有声明效用/约束就无唯一排序。

## D. 边界、反例与纠错

### LM08-D01
可用巨型稀有词表缩短序列，却增加 softmax/参数、估计稀疏和 OOD 失败；模型质量由目标、数据和训练决定。高压缩只是一个系统变量。

### LM08-D02
总体可由英语大组主导；少数语言 P95 fertility/截断率仍极高。必须报告各组分布与 worst-group/宏平均。

### LM08-D03
零宽/bidi、homoglyph/confusable、literal special token 注入、invalid UTF-8/replacement、极端 combining/长度放大、decode cleanup/log discrepancy、模板版本漂移。

## E. AI 迁移

### LM08-E01
固定 corpus/hash、Unicode/normalization、vocab budget、tokenizer/version；预定义语言/域/攻击切片；primary round-trip/fertility/BPB；分别固定 raw、token、FLOPs；paired seeds/docs；报告区间、失败样例和不可比项。

### LM08-E02
每语言 tokens/request、tokens/grapheme、P95/P99、truncation、美元/千请求、TTFT/total latency 与 refusal/error；报告 worst-group ratio 与宏平均，控制请求任务难度/长度。

### LM08-E03
256 bytes 可覆盖是设计恒等式/实现不变量；指定语料、词表、配置下 bytes/token 数是实验 `E`；“byte 统计更均匀/语言无关”是 `H/E`；“所以更公平、更准或普遍更好”是未经下游/群体/预算验证的越界外推。

## 无提示重做

- [ ] 从一张总体平均表恢复至少三种可能被隐藏的群体风险。
- [ ] 为真实 tokenizer 写一页 Pareto model card。
