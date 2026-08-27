---
type: solution
status: verified
area: [language-models, privacy, memorization]
topic: "[[Memorization、Exposure、Canary 与训练数据抽取]]"
exercise: "[[习题 - Memorization、Exposure、Canary 与训练数据抽取]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Memorization、Exposure、Canary 与训练数据抽取

## A. 识别与复述

### LM65-A01
Inclusion 是记录是否进入某版训练数据；memorization 是该记录的加入是否使模型行为带有实例级影响；verbatim reproduction 是输出是否满足预注册逐字/规范化匹配；extractability 是指定攻击者在访问和预算内能否找到；privacy harm 还要求内容受保护、可关联主体并产生影响。前一事件都不是后一事件的充分条件。

### LM65-A02
Canary 是从已知随机分布生成并人工插入训练数据的合成稀有字符串。至少固定生成分布/候选空间、插入次数与位置、上下文/前缀、tokenizer 与评分规则；还应加入未插入 control、tie 规则、训练版本和伦理限制。

### LM65-A03
Rank 是按损失从低到高时 canary 的位置；exposure 为
$$
\log_2|\mathcal R|-\log_2\operatorname{rank}.
$$
Bit 表示搜索空间压缩的二进制对数量级：exposure 每增加 1，rank 相对整个候选空间再缩小约 2 倍。

## B. 手算与构造

### LM65-B01
$$
\operatorname{exposure}=24-9=15\text{ bits}.
$$
相对无排序的 $2^{24}$ 个候选，排序后约需检查前 $2^9$ 个，缩小 $2^{15}=32768$ 倍。它只在该 scoring oracle 和候选空间下成立。

### LM65-B02
第三个候选损失为 $3.0$，其余七个都小于它，所以 rank 为 8。空间大小也是 8：
$$
\operatorname{exposure}=\log_2 8-\log_2 8=0.
$$
它没有得到比随机空间更有利的排序。

### LM65-B03
每行可存 canary_id、六位值的盐化哈希、inserted/control、生成 seed、候选空间定义、上下文模板 hash、插入次数、文档/位置、token IDs、训练 shard/version、loss、rank、exposure、查询预算和匹配结果。原始值应加密/限权，报告只显示无害掩码。

## C. 推导与证明

### LM65-C01
若 rank 从 $r$ 变为 $2r$，攻击需检查的候选数加倍，即多一 bit 搜索；$\log_2(2r)=\log_2r+1$。以完整空间的搜索 bits $\log_2|\mathcal R|$ 减当前 rank bits，就得到被模型排序节省的 bits。

### LM65-C02
每次失败概率为 $1-p$，独立 $B$ 次全部失败为 $(1-p)^B$，故至少成功一次为
$$
1-(1-p)^B.
$$
现实查询常因相同 prompt family、模型确定性和适应性选择而相关；此式只能作 iid 基线，不能替代实测 cluster/attack-family 成功率。

### LM65-C03
模型可由公开知识、后训练、RAG、工具或用户上下文学到同一字符串；同一事实也可能被多处独立表达。因此观察 $Y=$“复现”不能唯一识别原因 $Z=$“训练包含”。替代来源如当前检索网页和系统提示中的示例。

## D. 边界、反例与纠错

### LM65-D01
1000 次是有限、特定 sampler/prefix 的负结果。若真实单次成功率很低、需要不同前缀、API 隐藏 logits 或记忆只表现为 loss 差异，采样会漏检。结论只能是“该版本在该接口、预算和规则下未观察到成功”，并给二项上界。

### LM65-D02
候选空间必须在观察 rank 前固定。事后保留最好一千个等于使用模型输出选择分母，会人为增大 $\log|\mathcal R|-\log rank$ 或改变 rank 的含义；其 sampling distribution 不再对应原实验，属于选择泄漏。

### LM65-D03
高 exposure、低伤害：随机合成代号在白盒 logits 中排名极高，但从未对应真实主体且线上接口不可见。低 exposure、高风险：某真实敏感信息不能由枚举候选排序，却在一个常见触发上下文中单次逐字输出并可关联个人。Exposure 不是伤害的充分统计量。

## E. AI 迁移

### LM65-E01
合同写明：仅离线授权模型；白盒/黑盒字段；只用合成 canary；每 attack family 的 query/token/人工预算；固定 prefix、sampler、seed 数与候选空间；exact/normalized 匹配；人工核验双人脱敏；达到预算或严重告警即停止；原始输出加密、最小访问并设删除期限。

### LM65-E02
用同一 raw corpus 构造 dedup on/off，除重复处理外锁定 tokenizer、token 数、训练步数/算力和模型配方；在多个重复级别插入多组 canary/control。独立单位应是 canary family 或训练 run，不是同一 canary 的多次采样。主要混杂为有效 token/步数、文档混合和 dedup 对普通数据分布的改变。

### LM65-E03
先隔离 request ID 与版本、限制传播；由授权人员脱敏确认 exact/near match；排查 user context、system prompt、RAG/tool 与公开来源；查 data/checkpoint lineage 和时间；在合成复现实验中测试机制；量化受影响版本、接口和预算；触发访问撤销/过滤/重训或删除评估；最终结论标注支持、替代解释、未知与通知范围。
