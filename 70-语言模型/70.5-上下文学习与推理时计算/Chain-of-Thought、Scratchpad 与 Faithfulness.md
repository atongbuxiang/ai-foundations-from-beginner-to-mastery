---
type: concept
status: verified
area: [language-models, reasoning, chain-of-thought, faithfulness]
node_id: LM-37
aliases: [Chain-of-Thought, CoT, Scratchpad, 推理忠实性]
prerequisites: ["[[Prompt 作为条件事件、序列化与敏感性]]", "[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]"]
related: ["[[Self-Consistency、Best-of-N 与 Pass-at-k]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2022-Wei-Chain-of-Thought]]", "[[S-2023-Turpin-Unfaithful-CoT]]", "[[S-2023-Lanham-CoT-Faithfulness]]"]
exercises: ["[[习题 - Chain-of-Thought、Scratchpad 与 Faithfulness]]"]
solutions: ["[[解答 - Chain-of-Thought、Scratchpad 与 Faithfulness]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-icl-cot-faithfulness-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Chain-of-Thought、Scratchpad 与 Faithfulness

> [!abstract] 一句话结论
> 先生成中间文本可以改变计算路径、增加串行计算和提供可检查状态，但可读的 reasoning trace 不自动是模型内部决策过程的忠实解释。准确、步骤正确、可执行与因果忠实必须分开测量。

## 一、直接回答与中间变量

Direct prompting 直接从问题 $x$ 生成答案 $y$：

$$
p_\theta(y\mid x).
$$

Chain-of-Thought 先生成可见推理链 $r$，再生成答案：

$$
p_\theta(r,y\mid x)=p_\theta(r\mid x)p_\theta(y\mid x,r).
$$

若把 $r$ 当潜变量，答案概率为

$$
p_\theta(y\mid x)=\sum_r p_\theta(r\mid x)p_\theta(y\mid x,r).
$$

实践中的 greedy CoT 只选一条高概率路径，不执行上式的完整边缘化；self-consistency 才用有限样本近似部分路径聚合。

## 二、CoT 为什么可能帮助

至少有五种不同机制假说：

1. 计算深度：额外 token 允许更多串行 Transformer steps；
2. 分解：把难映射拆成训练中更常见的局部模式；
3. 外部工作记忆：中间结果进入后续上下文；
4. task cue：推理格式激活预训练中的解题分布；
5. 搜索入口：生成多条路径后可验证、回溯或投票。

这些机制可能共存。只比较 direct 与 CoT 的最终准确率，无法辨认哪项贡献。

## 三、Scratchpad 的对象边界

Scratchpad 是供后续计算读取的中间状态，可以是：

- 自然语言步骤；
- 方程、表格或程序；
- 工具调用与返回值；
- 对用户不可见但模型可访问的中间 token；
- 外部搜索状态。

可见 CoT 是 scratchpad 的一种，不等于所有内部计算。Transformer 在生成每个可见 token 前已经完成多层隐藏计算；自然语言 trace 是这个分布式过程的输出接口。

## 四、四个不能混用的质量事件

设真实答案为 $y^*$，生成链为 $r=(r_1,\ldots,r_m)$：

1. outcome correctness：$y=y^*$；
2. local validity：每一步由前提合法推出；
3. executable sufficiency：按 $r$ 执行可得到 $y$；
4. causal faithfulness：改变决定输出的真实因素时，$r$ 相应反映该因素。

可能出现：

- 链含算术错误，但最后碰巧给对答案；
- 每步看似正确，却省略决定性外部知识；
- 链可执行得到答案，但模型其实走隐藏捷径；
- 答案错误，链却忠实呈现了模型的错误过程。

因此 faithfulness 不是 accuracy 的同义词。

## 五、一个最小反例

问题：3 箱、每箱 4 个球，共多少？生成链说“$3+4=7$，所以答案是 12”。最终答案正确，但文字步骤不支持它。此例同时满足 outcome correct、local invalid、executable insufficient。

反过来，链正确算出 12，parser 却抽取了步骤中的 7，则 reasoning 正确而 scored answer 错。必须分开 step checker 与 answer parser。

## 六、Faithfulness 需要先选定义

### 1. 对可见链的因果依赖

干预 $r$ 后答案是否变化：

$$
\Delta_r=P(Y=y\mid do(R=r'))-P(Y=y\mid do(R=r)).
$$

截断、改写、插入错误能测试模型是否读取 trace，但编辑后的文本可能分布外。

### 2. 解释完整性

若输入加入 bias cue $h$ 会翻转答案，而 CoT 不提 $h$，则在“应披露所有决定性可表述因素”的定义下不完整。[[S-2023-Turpin-Unfaithful-CoT]] 用答案位置等偏置展示合理化风险。

### 3. 可执行性

把链翻译成程序/逻辑式并由确定性 solver 执行。若最终答案由执行结果产生，则 trace 对该系统输出有构造性关系；但自然语言到形式规范的翻译仍可能错误。

### 4. 隐藏过程忠实

要求文字链对应内部表示中的因果计算，这是最强也最难的主张，通常需要 activation intervention，而非只读文本。

## 七、干预矩阵

[[S-2023-Lanham-CoT-Faithfulness]] 使用多类黑盒干预。课程统一记录：

| 干预 | 保持什么 | 改变什么 | 主要风险 |
|---|---|---|---|
| truncate | 前缀步骤 | 可用后续计算 | 长度/格式同时变 |
| paraphrase | 声称的语义 | 表面 token | 语义并非完全等价 |
| inject error | 大部分链 | 单一步骤 | 错误文本可能 OOD |
| filler replace | 长度 | 信息内容 | filler 自身改变模型状态 |
| bias cue | 题面主体 | 捷径因素 | cue 可能直接改变任务 |

每项都应同时报告答案 flip、正确率、trace mention/validity 和生成概率，而非一个总 faithfulness 分数。

## 八、CoT 增益的预算对照

CoT 比 direct 使用更多输出 token。若要判断增益来自“特定推理结构”还是“更多计算”，至少比较：

- direct + matched filler tokens；
- short vs long CoT；
- structured valid steps vs scrambled steps；
- hidden scratchpad vs visible rationale；
- 相同 token 预算下的一条长链 vs 多条短链。

Filler 不是完美对照，但能暴露“额外 token 预算”这一混杂。

## 九、图解：可见 trace 与隐藏路径

先看图回答：红色虚线为什么使“答案依赖 CoT”不能只由一段流畅文字确认？

![[00-知识库管理/_assets/figures/language-models/fig-lm-icl-cot-faithfulness-v1.svg|900]]

> [!figure] 图 LM-37　CoT 的可见通道、隐藏通道与反事实干预
> 问题同时改变隐藏状态与可见 trace，答案可能读取 trace，也可能沿隐藏路径直接形成；下方列出截断、改写、错误和 bias cue 干预。图由本库重新绘制。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先区分 $X,U,R,Y$ 四个对象，再问干预只改变哪一个；最后将 faithfulness 拆为依赖、充分、完整、可执行和反事实稳定。

**图没有证明什么**：红色虚线只表示可能的直接路径，不证明任一模型一定忽略可见 CoT，也不证明隐藏状态可被完整还原。

## 十、工程与研究合同

一次 CoT 结果至少保存：完整 prompt、reasoning cue、最大/实际 reasoning tokens、sampler、全部路径、答案抽取器、step validator、题目与污染版本。

Faithfulness 研究还要保存：干预函数、被编辑 step、编辑前后 token、是否重新采样后缀、同一 seed 是否可比、答题变化和人工标注规则。

高风险场景中，不应把模型自述直接展示为“决策依据”。更稳妥的系统可以把可执行计算、外部证据引用和确定性检查器与自由文本解释分账。

## 十一、常见错误

- 把 CoT 准确率提升称为内部推理可解释；
- 把最终答案正确当每一步正确；
- 用一个自动 judge 同时评正确性和 faithfulness；
- 修改 trace 后未控制长度和重新采样；
- 比较 direct/CoT 时忽略 token 预算；
- 把不提 bias cue 直接解释成模型完全不知道 cue；
- 把可执行形式链的保证外推到自然语言解析之前。

## 十二、出口标准

完成本节后，应能推导 rationale latent-variable 分解，构造“正确答案/错误链”的反例，设计截断、改写和 bias 干预，并明确自己测的是准确、局部有效、可执行还是因果忠实。

## 十三、来源与练习

- [[S-2022-Wei-Chain-of-Thought]]：CoT prompting 现象；
- [[S-2023-Turpin-Unfaithful-CoT]]：偏置与合理化干预；
- [[S-2023-Lanham-CoT-Faithfulness]]：trace intervention 矩阵；
- [[习题 - Chain-of-Thought、Scratchpad 与 Faithfulness]]；
- [[解答 - Chain-of-Thought、Scratchpad 与 Faithfulness]]。
