---
type: solution
status: verified
area: [language-models, rag]
topic: "[[参数记忆、外部记忆与 RAG 潜变量分解]]"
exercise: "[[习题 - 参数记忆、外部记忆与 RAG 潜变量分解]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 参数记忆、外部记忆与 RAG 潜变量分解

## A. 识别与复述

### LM41-A01
参数记忆编码在训练后权重中，难逐事实定位或删除；上下文记忆是本次请求中的 token，可检查但受窗口与位置限制；外部记忆是可寻址、可更新、带权限和来源的文档/数据库/工具。外部记忆最终仍需转成上下文，模型也可能混入参数先验。

### LM41-A02
$z$ 是当前输出所依赖的潜在文档或证据单元。训练/推理时通常只观察 $x,y$，未必观察唯一正确 $z$，所以要用 $p(z\mid x,\mathcal C)$ 加权 $p(y\mid x,z)$。

### LM41-A03
RAG-Sequence 对整个 $y$ 共用一个 $z$ 后再边缘化；RAG-Token 在每个 token 处对 $z$ 求和。拼接把多文档一次送入生成器，不显式计算上述 mixture，注意力融合也不等于概率边缘化。

## B. 手算与构造

### LM41-B01
$0.7\times0.8+0.3\times0.2=0.56+0.06=0.62$。结果不是两条件概率的简单平均，而是按检索权重加权。

### LM41-B02
保留质量为 $0.5+0.3=0.8$；新权重为 $(0.5/0.8,0.3/0.8)=(0.625,0.375)$。第三文档的 $0.2$ 被丢弃。

### LM41-B03
问题“法国首都是？”；retriever 错取一段无关体育新闻，模型靠参数记忆输出“巴黎”。此时 $G=1$，但 evidence recall 与 attribution 都为 0。

## C. 推导与证明

### LM41-C01
边缘化潜变量：
$$p(y\mid x,\mathcal C)=\sum_zp(y,z\mid x,\mathcal C).$$
再用乘法法则
$$p(y,z\mid x,\mathcal C)=p(z\mid x,\mathcal C)p(y\mid x,z,\mathcal C).$$
若给定 $z$ 后语料其余部分对 $y$ 无额外作用，末项简化为 $p(y\mid x,z)$。

### LM41-C02
Bayes 公式给
$$q(z\mid x,y^\star)=p(z\mid x,y^\star)=
\frac{p(z\mid x)p(y^\star\mid x,z)}
{\sum_{z'}p(z'\mid x)p(y^\star\mid x,z')}.$$
它是目标答案已知时各文档对边缘似然的归一化责任。

### LM41-C03
全后验分母含所有 $\mathcal C$；top-$K$ 分母只含 $\mathcal Z_K$。若被截断项总质量非零，保留项都被除以更小分母而放大，因此数值不等；只有截断质量为零或另有精确校正才相同。

## D. 边界、反例与纠错

### LM41-D01
向量库只实现一种外部索引。完整 RAG 还需语料/权限、chunk、query、检索与近似、重排、上下文、生成、引用和评估合同。任何一层缺失都无法把答案根因归为可验证证据链。

### LM41-D02
gold context 已固定检索为成功；剩余错误可来自上下文模板/位置、generator 能力、输出 parser、gold 不完整或任务歧义。继续指责 retriever 违反了单因子诊断。

### LM41-D03
系统形成版本分裂：原文新、向量/ANN 与 cache 旧。应重建受影响 chunks/embeddings/index，失效 replicas/cache，记录传播完成时间，并用已变更事实查询确认旧结果不再返回。

## E. AI 迁移

### LM41-E01
依次保存查询时点；语料是否含当时有效证据；gold span；exact/ANN 候选；最终 context 是否保留；输出命题、答案与引用。把失败标为 $A_C,A_R,A_X,A_Y$ 中最早失败及后续伴随失败。

### LM41-E02
Closed-book 测参数基线；normal RAG 测完整系统；gold-context 绕过语料/检索，测 context+generator 上界。三组必须用同一 generator、prompt 容量、parser 与题集。

### LM41-E03
Manifest 含 corpus snapshot、valid time、doc/chunk IDs、encoder/index build、replicas、cache key/TTL。删除时记录 tombstone→chunk→vector→replica→cache 的完成确认，并设回归查询验证。
