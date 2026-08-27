---
type: solution
status: verified
area: [language-models, security, prompt-injection, tools]
topic: "[[Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"
exercise: "[[习题 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Prompt Injection、Indirect Injection 与 Tool-RAG 威胁模型

## A. 识别与复述

### LM67-A01
Direct injection 由攻击者直接控制用户输入；indirect injection 藏在网页、邮件、检索文档或工具结果等外部数据中；jailbreak 是诱使模型绕过行为政策的更广攻击，不必涉及外部数据或工具。三者可同时出现，但可控通道与系统后果不同。

### LM67-A02
$\mathcal T=(A,G,K,C,B,S)$：资产、目标、攻击者知识、可控通道、预算、成功条件。预算决定攻击者能否重试、适应和搜索；“单次失败”对可进行一万次查询的对手没有同等意义，故预算不是附注而是量词边界。

### LM67-A03
Semantic authority 是文本在任务中的建议/解释地位；execution authority 是改变外部状态的真实权限。模型可以理解或建议动作，但服务端身份、policy、schema 和审批才应决定执行。自然语言说“你无权限”不能撤销已暴露的 credential。

## B. 手算与构造

### LM67-B01
ASR $=18/200=.09$；benign utility $=276/300=.92$。还应给 prompt-family cluster 区间、失败原因、工具后果与版本，而非只报两点估计。

### LM67-B02
$$
1-(1-.03)^{20}=1-.97^{20}\approx1-.5438=.4562.
$$
约 45.6%。它只是在尝试独立且同分布时的基线；适应性攻击、确定性模型和共享 prompt family 会产生相关性。

### LM67-B03
数据流：用户请求→身份边界→检索器→外部文档信任边界→LLM planner→typed draft→policy/schema 边界→邮件预览→用户确认边界→发送器。发送器默认无自动执行，只有确认 token 与允许收件域同时满足才临时获得权限。

## C. 推导与证明

### LM67-C01
同一模型既生成提案又判断自身安全，共享被污染的上下文和失败机制；攻击可同时影响动作与自评。Reference monitor 应完整中介所有敏感操作、不可被普通输入修改、足够小可审计，并在模型外以确定性权限数据作决定。

### LM67-C02
可定义
$$
\operatorname{allow}(a,u,c)=
\mathbf1[I(u)\land V_{\rm schema}(a)\land
\operatorname{scope}(u,a)\land P(a,c)\land H(a,c)].
$$
先做解析/schema 和身份，避免无效输入进入复杂逻辑；再查最小 scope 与业务 policy；最后对仍高风险的合法动作做明确确认。任何一步失败即拒绝并留 reason code。

### LM67-C03
若系统对所有外部文档都拒绝，attack cases 无法达到工具后果，ASR 可接近 0；但 benign cases 也全部失败，$U_b\approx0$。防御目标是安全约束下最大化任务效用，不是单目标最小 ASR，因此必须联合报告。

## D. 边界、反例与纠错

### LM67-D01
Role/template 让模型学到优先级先验，但序列仍由 token 构成，没有形式化不可干扰保证；分布外内容、间接数据和模型错误都可破坏遵从。更关键的是工具权限不应由遵从概率决定。

### LM67-D02
假阳性：正常教程/合同引用祈使语句；文档中的用户真实任务说明含这些词。假阴性：同一意图用委婉/编码/跨语言表达；恶意效果通过数据结构、链接内容或多段组合实现而不含词表。词表过滤既损效用又覆盖有限。

### LM67-D03
降低了外部状态写入和伪造来源的风险；但仍有敏感查询泄露、搜索结果中的误导信息、过量读取、结果注入后影响最终回答、来源本身可信但被攻陷、日志隐私和 denial-of-wallet。Read-only 与签名缩小 blast radius，不使内容变真或无害。

## E. AI 迁移

### LM67-E01
入口身份与速率限制；检索 provenance/allowlist/时间；结构化 instruction-data 序列化；模型仅产 typed proposal；服务端 schema/业务规则；read/write 工具分离；短期 scoped credential；高风险 preview/确认；sandbox/限额/幂等/rollback；完整审计和 anomaly alert；版本化 adaptive red team。

### LM67-E02
固定集在版本冻结前锁定 attack family、预算、success oracle 与 benign set，只用于可比回归；adaptive 队伍只得到声明的信息和预算，以抽象目标类别生成变体，原始危险细节置于受限库。发现的新族进入下一版 test，不回填本版；报告查询成本、cluster success、人评和 benign regression。

### LM67-E03
共同字段：request/session/user pseudonymous ID、timestamp、model/tokenizer/template/policy/tool/schema revisions、来源文档 IDs/信任、proposal type 与参数 hash、risk class。决策字段：allow/deny、逐项 predicate、reason code、确认主体/token、credential scope。执行字段：executor ID、状态变更摘要、result hash、latency、retry、rollback ID；拒绝也保留同样版本与理由。
