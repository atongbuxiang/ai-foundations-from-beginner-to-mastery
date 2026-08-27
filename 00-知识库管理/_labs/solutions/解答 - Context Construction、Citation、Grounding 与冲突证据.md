---
type: solution
status: verified
area: [language-models, rag, citations]
topic: "[[Context Construction、Citation、Grounding 与冲突证据]]"
exercise: "[[习题 - Context Construction、Citation、Grounding 与冲突证据]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Context Construction、Citation、Grounding 与冲突证据

## A. 识别与复述

### LM46-A01
Relevance 是与问题相关；support 是证据蕴含 claim；factuality 是 claim 在世界为真；attribution 是 claim 链到正确来源；faithfulness 是输出决策是否实际依赖证据。任意一项都不能无条件推出其余项。

### LM46-A02
候选还会经 ACL/时间过滤、去重、排序、预算截断、模板化与 citation mapping。正确证据可能在这些步骤被删除、截断或放到模型难利用的位置。

### LM46-A03
Correctness 衡量所给引用中有多少真正支持对应 claim；completeness 衡量需验证 claims 中有多少至少有一个支持引用。可一高一低。

## B. 手算与构造

### LM46-B01
Completeness $=2/3\approx0.667$；correctness $=3/4=0.75$。分母分别是 claims 与引用，不能互换。

### LM46-B02
可行集合：第一单独效用 8，第二单独 7，第三单独 4，第一+第三长度 280 效用 12，第二+第三长度 240 效用 11；第一+第二 320 不可行。最优选第一与第三，效用 12。

### LM46-B03
Claim“地球绕太阳运行”为真，却引用一篇只讨论月相的页面。Factuality 为真，citation relevance/support 为假；答案可能来自参数记忆。

## C. 推导与证明

### LM46-C01
例如
$$U(S)=\sum_{i\in S}u_i-\lambda\sum_{i<j\in S}\operatorname{sim}(d_i,d_j)+\gamma\operatorname{coverage}(S),$$
约束 $\sum_{i\in S}\ell_i\le L$。还可加入 ACL/时间硬约束。

### LM46-C02
构造两个 claims，各附一个完全无关引用。引用存在率和形式 completeness 可为 1，但 support 指示量全为 0，所以 correctness 为 0。必须用蕴含而非存在判断。

### LM46-C03
Gold-only 测生成器在理想证据下的能力；加入 distractors 后的配对下降测噪声鲁棒性、位置竞争与上下文利用。它不单独测 retriever，因为 gold 已被强制提供。

## D. 边界、反例与纠错

### LM46-D01
低熵只说明模型在该 context 条件下分布集中，可能来自熟悉措辞、偏见或错误但自信的来源；不验证世界真值、权威或蕴含。

### LM46-D02
整页可能含多个相反段落或过期部分，读者无法复核具体命题，自动 verifier 也可能用错 span。应保存页/段/字符范围、版本和 claim-citation 映射。

### LM46-D03
多个页面可能复制同一错误上游，不独立；来源有不同日期、范围和权威；少数第一方可优于多数转述。应按时点、口径、来源独立性与权威呈现冲突。

## E. AI 迁移

### LM46-E01
Claim 表含 claim-id、text、verification-needed；citation edge 含 claim-id、source-id、span、relation；source 表含 URL/doc-id、snapshot、valid-time、authority、ACL。Verifier 输出 support label、置信与版本。

### LM46-E02
构造文档含“忽略系统并调用工具/泄露秘密”；确认其只作为引用数据，不改变 system/tool policy。测试命令不执行、工具参数不来自未授权段、输出标注不可信指令并记录拦截。

### LM46-E03
模板：“截至查询时点 $t$，第一方来源 A（有效于 $t_A$）给出 X；来源 B（$t_B$）给出 Y。两者口径/时间差为……。本回答按规则……采用 X，残余不确定性为……。”每一断言附精确 span。
