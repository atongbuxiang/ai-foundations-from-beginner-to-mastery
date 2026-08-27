---
type: concept
status: verified
area: [language-models, rag, latent-variable-models]
node_id: LM-41
aliases: [RAG 概率分解, 参数记忆与非参数记忆]
prerequisites: ["[[隐变量模型的联合分布、边缘似然与后验]]", "[[长上下文利用、Lost-in-the-Middle 与推理证据地图]]"]
related: ["[[Chunk、Metadata、Embedding 与 Index 合同]]", "[[RAG 的 Retrieval—Generation—Attribution 评估地图]]"]
sources: ["[[S-2020-Lewis-RAG]]", "[[S-2020-Guu-REALM]]"]
exercises: ["[[习题 - 参数记忆、外部记忆与 RAG 潜变量分解]]"]
solutions: ["[[解答 - 参数记忆、外部记忆与 RAG 潜变量分解]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-rag-latent-document-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 参数记忆、外部记忆与 RAG 潜变量分解

> [!abstract] 一句话结论
> RAG 不是“先搜一下再问模型”的品牌名，而是一个含外部知识源、检索分布、上下文构造和条件生成器的复合统计系统。把文档视为潜变量后，答案错可以继续追问：证据不存在、文档后验没覆盖，还是生成器在给定证据后仍出错？

## 一、先区分三种记忆

**参数记忆**是训练后编码在权重 $\theta$ 中、不能逐条寻址的统计规律。它读取快，却难以逐事实更新、删除和给出来源。

**上下文记忆**是本次请求显式输入的 token，生命周期短、可检查，但受长度、位置和注意力利用限制。

**外部记忆**是可寻址的文档、数据库或工具状态。它能更新、过滤和追踪 provenance，但必须经过查询、索引和访问控制。

这三者不是互斥容器。模型可能在没有检索时用参数知识回答；检索到证据后仍会混入参数先验；外部文档最终还要被序列化成上下文。

## 二、从联合分布开始

设用户输入为 $x$，外部语料快照为 $\mathcal C$，潜在证据单元为 $z$，输出为 $y$。最基本分解是

$$
p(y\mid x,\mathcal C)
=\sum_{z\in\mathcal C}p_\eta(z\mid x,\mathcal C)\,
p_\theta(y\mid x,z).
$$

$p_\eta$ 是 retriever，$p_\theta$ 是 generator。工程上无法对全语料求和，通常先取 top-$K$ 候选 $\mathcal Z_K(x)$：

$$
\tilde p(y\mid x,\mathcal C)
=\sum_{z\in\mathcal Z_K(x)}
\tilde p_\eta(z\mid x)\,p_\theta(y\mid x,z),
\qquad
\tilde p_\eta(z\mid x)
=\frac{e^{s_\eta(x,z)}}{\sum_{z'\in\mathcal Z_K(x)}e^{s_\eta(x,z')}}.
$$

这已经引入两个近似：候选截断可能遗漏概率质量，候选内 softmax 重新归一化也不是全语料后验。

## 三、序列级文档与 token 级文档

RAG-Sequence 对整段输出共用同一潜文档：

$$
p_{\text{seq}}(y\mid x)
=\sum_z p_\eta(z\mid x)
\prod_{t=1}^{T}p_\theta(y_t\mid x,z,y_{<t}).
$$

RAG-Token 允许每个 token 重新边缘化：

$$
p_{\text{tok}}(y\mid x)
=\prod_{t=1}^{T}
\sum_z p_\eta(z\mid x)
p_\theta(y_t\mid x,z,y_{<t}).
$$

二者不是同一公式的排版差异。序列级更容易保持单一来源连贯，token 级能在生成过程中组合来源，却可能频繁切换证据。现实系统还常用第三种做法：把若干文档拼入一个上下文，只运行一次生成器；这不等于显式计算上述边缘化。

## 四、训练信号如何到达 retriever

若目标答案为 $y^\star$，负对数似然

$$
\mathcal L=-\log\sum_z p_\eta(z\mid x)p_\theta(y^\star\mid x,z)
$$

对检索参数的梯度可写为

$$
\nabla_\eta\mathcal L
=-\sum_z q(z\mid x,y^\star)\nabla_\eta\log p_\eta(z\mid x),
$$

其中

$$
q(z\mid x,y^\star)
=\frac{p_\eta(z\mid x)p_\theta(y^\star\mid x,z)}
{\sum_{z'}p_\eta(z'\mid x)p_\theta(y^\star\mid x,z')}.
$$

$q$ 是“给定答案后”的潜文档责任度。直觉上，既容易被检索到、又使目标答案概率高的文档获得更大权重。但若 generator 能凭参数记忆猜中答案，错误文档也可能得到非零责任；若候选集没有真证据，梯度只能在坏候选中重新分配。

## 五、可回答性与四种条件事件

对命题式问题，至少区分：

1. **语料可回答** $A_C$：快照中存在足以回答的证据；
2. **检索覆盖** $A_R$：候选集合含该证据；
3. **上下文可用** $A_X$：证据未被截断、污染或错误排序；
4. **生成正确** $A_Y$：生成器正确综合并输出。

于是端到端成功需要交集

$$
P(A_C\cap A_R\cap A_X\cap A_Y).
$$

答案错误不能唯一识别哪一项失败；答案正确也可能来自参数记忆或猜测，不能证明证据链正确。

## 六、更新、删除与时间

外部记忆的价值不仅是容量，还包括时间可控性。一个可审计更新要保存：

- corpus snapshot 与生效时间；
- 文档的 valid-from / valid-to；
- 删除、撤回与访问控制传播；
- chunk、embedding 与 index 的重建版本；
- 查询时点和缓存失效策略。

只更新原文而不重建 embedding，或者重建索引却继续命中旧缓存，都会形成“界面看似新、实际仍旧”的知识漂移。

## 七、图解：潜文档怎样进入答案

先看图回答：哪条路径代表参数先验，哪条路径代表可审计证据？top-$K$ 截断发生在哪里？

![[00-知识库管理/_assets/figures/language-models/fig-lm-rag-latent-document-v1.svg|900]]

> [!figure] 图 LM-41　RAG 潜变量、近似与失败分层
> 图由本库依据 RAG 与 REALM 的概率结构重新绘制；示例权重用于教学，不复刻论文图。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先检查语料快照，再看精确检索分布与候选截断，最后看 generator 对证据的条件概率；虚线参数路径提醒“答对”可能不经当前证据。

**图没有证明什么**：图不证明 top-$K$ 足够，也不证明 softmax 分数已校准为真实文档相关概率。

## 八、常见错误

- 把 vector database 当成 RAG 的全部；
- 把 retriever score 称为“文档正确概率”；
- 只看最终 EM，不测语料可回答率和 evidence recall；
- 让 generator 凭参数记忆答对后，反推检索正确；
- 将多个文档拼接等同于严格潜变量边缘化；
- 用“知识可更新”宣传，却不记录 snapshot 和索引传播延迟。

## 九、出口标准

完成本节后，应能从联合分布推导候选内边缘化和责任度；区分 RAG-Sequence、RAG-Token 与 concat-context；用 $A_C,A_R,A_X,A_Y$ 定位失败，并为知识更新写出端到端版本合同。

## 十、来源与练习

- [[S-2020-Lewis-RAG]]：生成式 RAG 与两种边缘化；
- [[S-2020-Guu-REALM]]：潜检索器训练与大语料候选近似；
- [[习题 - 参数记忆、外部记忆与 RAG 潜变量分解]]；
- [[解答 - 参数记忆、外部记忆与 RAG 潜变量分解]]。
