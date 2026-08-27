---
type: solution
status: verified
area: [language-models, constrained-generation]
topic: "[[Grammar-constrained Decoding、Schema 与结构化输出]]"
exercise: "[[习题 - Grammar-constrained Decoding、Schema 与结构化输出]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Grammar-constrained Decoding、Schema 与结构化输出

## A. 识别与复述

### LM53-A01
$L$ 是完整合法字符串集合；$\operatorname{Pref}(L)=\{s:\exists u,su\in L\}$ 是仍可补全的前缀。Accepting 表示当前串已在 $L$；live 表示未来仍能到达接受态。一个状态可同时 accepting 且 live，故“已经合法”不必然“必须停止”。

### LM53-A02
$A(q)=\{v:\delta^*(q,\mathrm{bytes}(v))\in Q_{\mathrm{live}}\}$。Token 可含多个字符、半个 Unicode 字节序列、多个终结符或转义；只看第一字符无法判断读完整个 token 后是否仍可完成。

### LM53-A03
语法层管括号、标点和有限文法；schema 层在编译器支持的方言/关键字内管类型、required、枚举等；语义层管跨字段关系与事实；行为层管授权、额度、副作用和审计。前两层也必须限定实现支持范围，后两层需独立校验。

## B. 手算与构造

### LM53-B01
$L=\{ab,ac\}$，前缀闭包为 $\{\epsilon,a,ab,ac\}$。空串与“a”非 accepting、但 live；“ab” accepting，若语言不允许继续则不再 continuable；“ad”既不 accepting 也不 live。

### LM53-B02
Valid set 是 $\{b,c\}$；$Z=.4+.3=.7$。新概率为 $q(b)=4/7\approx.5714$、$q(c)=3/7\approx.4286$，“d”与 EOS 为 0。Removed mass 为 $.3$，它提示模型原始分布有相当质量落在非法/过早结束项。

### LM53-B03
若当前需要 JSON 字符串内容，token“a 引号”的首字符“a”可作为内容，但其随后引号会提前关闭字符串；若接下来的 grammar 要求同一字段至少三个字符，该完整 token 进入 dead end。约束器必须对两个字符连续转移后才决定。

## C. 推导与证明

### LM53-C01
令 $Z=\sum_{u\in A}p(u)>0$。非负性显然，且
$$\sum_v \frac{p(v)\mathbf1[v\in A]}{Z}=\frac{\sum_{v\in A}p(v)}{Z}=1.$$
若 $Z=0$ 或 $A$ 为空，公式未定义，必须触发显式恢复合同。

### LM53-C02
首步有前缀 A、B，各概率 $.5$；A 后合法完成总概率 $.1$，B 后合法完成总概率 $.9$。两者均为 live，局部 mask 首步仍给 $(.5,.5)$；但对“最终落入 $L$”做全局条件后，首步责任度为 $(.05,.45)/.5=(.1,.9)$。局部只删立即死路，未按未来合法概率质量加权。

### LM53-C03
把所有 accepting states 放入集合，沿自动机反向边做 BFS/固定点闭包：若状态存在一条边到已知 live 状态，也标为 live，直到不再变化。有限自动机必终止；非 live 状态无法到达接受态。带栈解析器状态空间可能无限，需按 grammar 构造做符号可达分析或运行时保守判定。

## D. 边界、反例与纠错

### LM53-D01
对象“{city: Paris, country: Japan}”可完全符合字段类型、required 与 JSON 语法，却在语义上不一致。Schema pass 只支持结构主张；真实性需要知识源/业务规则，跨字段一致性需要 validator。

### LM53-D02
它会误放行首字符合法但后缀非法的多字符 token，也会误拒绝被 token 切开的 UTF-8/终结符。应在 byte 层对完整 token 增量转移，缓存 parser-state 与 token-id 的组合，并用多字节、转义和跨 token 终结符测试。

### LM53-D03
静默关闭使“保证结构合法”变成不可观察的偶发最佳努力，调用方可能执行非法工具参数。API 应返回 constraint-dead-end，保存 prefix/state/valid-set/removed mass；恢复若允许，必须由调用方显式选重试、修复或放宽。

## E. AI 迁移

### LM53-E01
Grammar 保证 JSON 结构；schema 限定 amount 为数值、currency 枚举、recipient 格式；语义 validator 检查余额、币种与收款人存在；policy 层做身份、额度与审批；执行层用幂等键、预览/确认和沙箱；完成后记录审计日志。模型输出不能跳过后四层。

### LM53-E02
保存 tokenizer 文件/hash、token→byte 表、normalization、grammar/schema 原文与 hash、dialect/支持关键字、compiler/runtime commit、parser 初态、EOS/空白/stop 规则、dead-end policy、processor 顺序、缓存版本、输入/output token IDs 与逐步 valid-set 摘要。

### LM53-E03
构造同时含纯语法、schema 边界、跨字段事实和危险工具动作的分层集。对 constrained/unconstrained 用同模型预算，多 seed 分别报 parse/schema pass、semantic accuracy、authorization violation、dead-end、removed mass 与 latency；不可把 parse pass 合并为总正确率。
