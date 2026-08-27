---
type: concept
status: verified
area: [language-models, decoding, constrained-generation]
node_id: LM-53
aliases: [语法约束解码, 结构化生成]
prerequisites: ["[[Logits、Softmax、Temperature 与 Categorical Sampling]]", "[[数学归纳、递归与组合计数]]"]
related: ["[[EOS、停止规则、重复惩罚与退化循环]]", "[[Speculative Decoding、Acceptance 与分布精确性]]", "[[Model、API、Tokenizer、Template 版本与复现合同]]"]
sources: ["[[S-2023-Geng-Grammar-Constrained]]", "[[S-2023-Willard-Louf-Guided-Generation]]"]
exercises: ["[[习题 - Grammar-constrained Decoding、Schema 与结构化输出]]"]
solutions: ["[[解答 - Grammar-constrained Decoding、Schema 与结构化输出]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-prefix-automaton-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Grammar-constrained Decoding、Schema 与结构化输出

> [!abstract] 一句话结论
> 语法约束解码把“下一 token 概率最大”改成“在仍可能完成合法字符串的 token 中选择”。它可以给出语法层保证，却不能单独保证字段语义、事实正确、工具权限或副作用安全。

## 一、先区分三个集合

设字符或字节字母表为 $\Sigma$，目标语言为 $L\subseteq\Sigma^*$。例如，某个 JSON Schema 所允许的全部有限字符串组成 $L$。生成到前缀 $s$ 时，最重要的不是只问 $s\in L$，而是问它是否**仍可完成**：

$$
\operatorname{Pref}(L)
=\{s\in\Sigma^*: \exists u\in\Sigma^*,\ su\in L\}.
$$

于是要分清：

- $s\in L$：现在已经是一个完整合法输出；
- $s\in\operatorname{Pref}(L)$：现在虽未完成，但仍存在合法后缀；
- $s\notin\operatorname{Pref}(L)$：已经进入死路，未来添加任何字符都不能补救。

“已接受”与“可继续”并不互斥。例如正则语言 `a*` 中，空串已经合法，也仍可继续接 `a`。解析器必须同时保存 accepting 与 continuable 两个状态，不能以“当前合法”冒充“必须停止”。

## 二、自动机或解析器状态

对正则语言，可用 DFA/NFA 状态 $q_t$；对括号嵌套、JSON 或上下文无关文法，通常需要带栈的 parser state。统一写成

$$
q_{t+1}=\delta(q_t,b(v)),
$$

其中 $b(v)$ 是 token $v$ 解码得到的字节串，而非假定它只有一个字符。若读入整段 $b(v)$ 后仍处于可完成状态，则 $v$ 在当前可用：

$$
A(q_t)=\{v\in V:\delta^*(q_t,b(v))\in Q_{\mathrm{live}}\}.
$$

$Q_{\mathrm{live}}$ 表示能抵达某个接受态的状态集合。只检查 token 的第一个字符会漏掉诸如 `true`、转义序列、UTF-8 多字节字符或横跨多个语法单元的 token。

## 三、mask、重归一化与分布含义

原始模型给 $p_t(v)$，局部语法 mask 后常用

$$
q_t(v)=
\frac{p_t(v)\mathbf 1[v\in A(q_t)]}
{\sum_{u\in A(q_t)}p_t(u)}.
$$

分母 $Z_t=\sum_{u\in A(q_t)}p_t(u)$ 是当前合法质量。$Z_t$ 很小时，约束器会把原本极小的质量放大；输出虽然合语法，却可能暴露模型其实并不“想”走这条路径。应把 $Z_t$ 或 removed mass $1-Z_t$ 记入 trace。

> [!warning] 局部 mask 不等于全局条件分布
> 一般不能把逐步重归一化写成 $p(y\mid y\in L)$。全局条件分布还会考虑每个前缀未来能产生多少概率质量；局部 mask 只删除立即不可能完成的 token。两者只有在附加条件下才相同。

若 $A(q_t)=\varnothing$，系统出现 dead end。可靠实现要说明是报错、回退、修复、重新提示，还是解除约束；静默采样一个非法 token 会让“保证”失效。

## 四、tokenization 是约束器的一部分

文法多在字符/字节层定义，语言模型却在 token 层移动，因此必须处理四种边界：

1. 一个 token 含多个字符，如整个键名或标点组合；
2. 一个字符由多个字节组成，token 可能切在 UTF-8 中间；
3. 一个语法终结符跨多个 token；
4. 不同 token 序列可能解码成相同文本。

稳妥流程是：文法编译为对字节串工作的状态机；对候选 token 的完整 byte sequence 做增量转移；缓存 `(parser_state, token_id)` 的结果；在 tokenizer 或 grammar 版本改变后使缓存失效。

## 五、JSON Schema 的保证边界

可以把约束分成四层：

| 层 | 例子 | 语法约束能否独自保证 |
|---|---|---|
| 词法/语法 | 引号闭合、逗号位置、枚举文本 | 通常可以 |
| schema 结构 | required 字段、类型、有限枚举 | 编译器支持相应子集时可以 |
| 语义一致性 | `start_date <= end_date`、城市与邮编匹配 | 通常不可以 |
| 行为安全 | 工具是否获授权、金额是否合理、调用有无副作用 | 不可以 |

复杂正则、数值范围、跨字段依赖、递归 schema 或 Unicode 语义可能只得到部分支持。报告“支持 JSON Schema”时必须列出 dialect、支持关键字、递归深度、数值与字符串限制。

## 六、停止、空白与歧义

结构化生成仍需要 EOS 和停止合同：

- 解析器首次进入 accepting state 时，是立即停止，还是允许尾随空白？
- EOS 是否只在 accepting state 放行？
- stop string 若截断在字符串字面量内部，返回的是无效 JSON 还是报错？
- 文法有歧义时，parser state 如何合并，概率是否重复计算？

一个常见策略是：只有 accepting state 才允许 EOS；生成到上限但未接受则明确标记 truncated/invalid；不要把截断结果包装成成功对象。

## 七、性能账

约束器每步至少做候选过滤、parser 转移与 mask。成本受词表大小、状态缓存命中率、grammar 复杂度和 batch 内状态分歧影响。可记录：

$$
\text{mask density}_t=\frac{|A(q_t)|}{|V|},
\qquad
\text{overhead}=
\frac{\text{latency}_{\mathrm{constrained}}}
{\text{latency}_{\mathrm{unconstrained}}}-1.
$$

mask 很稀疏不必然更快：若实现先计算全词表 logits 再在 CPU 上逐项检查，parser/同步开销可能占主导。性能结论必须绑定实现、硬件、batch、输出长度和 grammar。

## 八、图解：从前缀状态到 token mask

**读图问题**：为什么 token 的第一个字符看似合法仍可能进入死路，而 parser 的 accepting state 又为何不足以保证工具调用安全？

![[00-知识库管理/_assets/figures/language-models/fig-lm-decoding-prefix-automaton-v1.svg|900]]

> [!figure] 图 LM-53　可完成前缀、完整 token 转移与约束边界
> **生成：**本库按 prefix closure、自动机转移与 token-byte mask 定义绘制；右侧安全分层是课程审计框架，不是某一库的 API 截图。

**怎样读图**：沿绿色边检查读完整个 token bytes 后仍能到达接受态的 prefix；再看红色候选如何在 token 后半段进入死路，最后从语法层一路核对到权限与副作用层。

**图没有证明什么**：进入接受态最多证明满足已实现的 grammar/schema 子集，不证明字段事实正确、跨字段一致、用户已授权或工具调用无危险副作用；这些都需独立验证。

## 九、常见错误与出口标准

错误包括：把合法前缀等同完整字符串；只检查 token 首字符；忽略 tokenizer 版本；把局部 mask 当全局条件分布；遇到空集合静默放宽；把结构合法宣传为语义正确。

完成本节后，应能定义 $L$ 与 $\operatorname{Pref}(L)$，手算一个 token-level valid set，解释重归一化改变的分布，设计 dead-end/EOS 合同，并为结构化工具调用再加语义校验、授权和副作用隔离。

## 十、来源与练习

- [[S-2023-Geng-Grammar-Constrained]]；
- [[S-2023-Willard-Louf-Guided-Generation]]；
- [[习题 - Grammar-constrained Decoding、Schema 与结构化输出]]；
- [[解答 - Grammar-constrained Decoding、Schema 与结构化输出]]。
