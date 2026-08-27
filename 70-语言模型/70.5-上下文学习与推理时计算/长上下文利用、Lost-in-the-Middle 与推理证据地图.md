---
type: concept
status: verified
area: [language-models, long-context, evaluation, reasoning]
node_id: LM-40
aliases: [长上下文利用, Lost-in-the-Middle, 有效上下文窗口]
prerequisites: ["[[Test-time Compute、Search、Verifier 与预算]]", "[[位置分辨率、混叠与长度外推评测]]"]
related: ["[[参数记忆、外部记忆与 RAG 潜变量分解]]", "[[Contamination、Prompt Sensitivity、Robustness 与不确定性]]"]
sources: ["[[S-2024-Liu-Lost-in-the-Middle]]", "[[S-2024-Hsieh-RULER]]", "[[S-2020-Brown-GPT3-ICL]]"]
exercises: ["[[习题 - 长上下文利用、Lost-in-the-Middle 与推理证据地图]]"]
solutions: ["[[解答 - 长上下文利用、Lost-in-the-Middle 与推理证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-icl-long-context-evidence-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 长上下文利用、Lost-in-the-Middle 与推理证据地图

> [!abstract] 一句话结论
> API 接受 $T$ 个 token 只定义声明窗口；模型能否在不同位置、干扰和任务复杂度下检索、组合并正确输出，才定义任务条件化的有效上下文。不存在脱离协议的单一“真实窗口”。

## 一、四种经常混淆的长度

1. declared context：接口允许的最大 input + output token；
2. trained length：训练时序列长度分布；
3. numerically supported length：位置方案和 kernel 能运行；
4. effective context：某任务/阈值下仍能利用的长度。

前三项都不能自动推出第四项。模型可在 128K 输入上不报错，却只可靠使用开头与结尾的证据；也可在困惑度平稳时失败于多跳聚合。

## 二、长上下文任务不是一个难度轴

至少分开：

- single retrieval：找一条唯一 needle；
- multi-needle：找多条证据并全部返回；
- multi-hop tracing：按依赖链组合；
- aggregation：计数、求和或比较全局集合；
- QA with distractors：识别相关文档后回答；
- ICL at length：从许多 demonstrations 学映射；
- generation constraint：答案格式和引用位置。

模型在 single needle 接近满分，不证明能做 aggregation 或多跳推理。

## 三、位置必须成为自变量

设相关证据位置比例为

$$
r=\frac{\text{evidence start token}}{T}\in[0,1].
$$

对固定长度 $T$，扫描 $r$，得到

$$
A(T,r,q,d),
$$

其中 $q$ 是任务类型，$d$ 是干扰强度。[[S-2024-Liu-Lost-in-the-Middle]] 在多种被测模型/任务中观察到开头和结尾较好、中部较差的非单调位置效应。

正确结论是经验条件式：在这些模型、prompt 与任务中存在位置效应。它不是由 causal mask 或 RoPE 单独推出的普遍结构定理。

## 四、有效上下文是一个函数或集合

给预注册阈值 $\tau$，可定义任务 $q$、干扰 $d$ 下的保守有效长度

$$
T_{eff}(q,d;\tau)
=\max\left\{T:\min_r A(T,r,q,d)\ge\tau\right\}.
$$

用 $\min_r$ 是为了防止只在尾部放 needle 得到乐观窗口。也可报告位置平均或分位数，但必须说明。

若不同任务得到 64K、32K、8K，就不应压成“模型真实窗口为 32K”而不带任务。更诚实的对象是一张

$$
\text{length}\times\text{position}\times\text{task}\times\text{distractor}
$$

能力张量。

## 五、RULER 补了什么

[[S-2024-Hsieh-RULER]] 不只做 vanilla needle retrieval，还改变 needle 类型/数量，并加入 multi-hop tracing、aggregation 等可控任务。它的价值是：

- 长度和复杂度可系统扫描；
- 有明确自动真值；
- 可画 degradation curve；
- 可区分“找得到”与“组合得对”。

边界同样重要：synthetic 字符串与真实长文在语义结构、噪声和预训练熟悉度上不同。Synthetic success 是必要诊断之一，不是现实文档理解充分证明。

## 六、长上下文 ICL 的特殊混杂

增加 demonstrations 时，至少同时改变：

- 示例数量 $K$；
- token 长度 $T$；
- 各例位置与到 query 的距离；
- 类别频率和顺序；
- truncation 风险；
- attention/KV compute。

若性能先升后降，可能是更多示例的信息收益与更长上下文的位置/干扰成本相抵。要区分可做：

1. 固定 $T$，用短/长 demos 改 $K$；
2. 固定 $K$，填充无关文本改 $T$；
3. 固定集合，扫描顺序和 query 位置；
4. 对相同信息做摘要/检索压缩；
5. 保存被 truncation 的精确 token。

## 七、位置曲线可能来自哪些因素

- causal recency 与 output 相邻性；
- 训练数据中重要信息常在标题/结尾；
- position encoding 外推误差；
- attention dilution 与干扰相似性；
- prompt 指令位置；
- parser/答案格式；
- 数据集构造偏差。

观察 U 形曲线不能辨认上述原因。需要交换 position encoding、固定训练分布、做 attention/activation intervention 或改变 prompt 才能建立机制。

## 八、长上下文的成本账

标准 full attention 的 prefill attention 项随长度近似 $O(T^2d)$，KV cache 随 $O(Td)$ 增长；具体 kernel、GQA、稀疏/线性 attention 会改变常数或复杂度。

评测要同时报：

- tokenizer 后实际 $T$，不是字符数；
- prefill/decode latency；
- peak memory 与 KV dtype；
- truncation/sliding policy；
- max output 是否挤占 input budget；
- batch 与并发。

仅把 context window 标称值当产品能力，会忽略利用质量和成本。

## 九、图解：长度 × 位置 × 任务

先看图回答：为什么左侧一条 U 形曲线和右侧一张矩阵都不能单独给出无条件窗口？

![[00-知识库管理/_assets/figures/language-models/fig-lm-icl-long-context-evidence-v1.svg|900]]

> [!figure] 图 LM-40　位置效应与任务条件化有效窗口
> 左侧是教学用 evidence-position 曲线，右侧用 length × task 矩阵展示 retrieval、multi-needle、multi-hop 与 aggregation 的不同退化速度。图由本库依据 Lost-in-the-Middle 与 RULER 的审计思想重新绘制，数值非论文复刻。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先在固定长度横向扫描证据位置，再在固定任务纵向增加长度；最后用预注册阈值定义该任务的 effective context。

**图没有证明什么**：示意数值不属于任一模型；U 形不是所有模型的定理，矩阵也不证明 synthetic task 等于现实理解。

## 十、完整评测矩阵

| 轴 | 最小取值 |
|---|---|
| length | 2K/4K/8K/…至声明上限 |
| position | start/quarter/middle/three-quarter/end |
| relevant count | 0/1/multiple |
| task | retrieve/multi-hop/aggregate/QA/ICL |
| distractor | 数量、相似度、冲突证据 |
| output | exact/ordered/citation/abstain |
| prompt | instruction 位置与模板 |
| model system | tokenizer、position scaling、kernel、quantization |

每个格子保存 seed、生成器版本和失败例；报告曲线与置信区间，不只报告声明上限处的一个平均数。

## 十一、证据地图

- I：tokenizer、max input/output 与 truncation 实现；
- T：attention/position 复杂度或对称性结论；
- E：特定模型在 length-position-task 矩阵的结果；
- A：由多项实验推断的可能机制；
- H：尚待干预验证的训练分布/位置假说；
- O：版本漂移、API 限制和异常失败。

Lost-in-the-Middle 与 RULER 主要提供 E；不能未经干预直接升级为“RoPE 导致”的 T。

## 十二、常见错误

- 把可输入长度当可利用长度；
- 只把 needle 放末尾；
- single retrieval 成功后声称长文推理成功；
- 用字符数代替实际 token；
- 忽略 output reserve 造成输入截断；
- 不记录 position-scaling 或 tokenizer 版本；
- 合并不同任务成单一窗口；
- 从 synthetic benchmark 直接推断真实工作负载。

## 十三、出口标准

完成本节后，应能区分声明、训练、数值支持和有效窗口；能设计 length × position × task × distractor 矩阵；能用阈值定义 $T_{eff}$ 并解释 Lost-in-the-Middle/RULER 各自提供什么证据、缺什么证据。

## 十四、来源与练习

- [[S-2024-Liu-Lost-in-the-Middle]]：证据位置效应；
- [[S-2024-Hsieh-RULER]]：可控长上下文任务；
- [[S-2020-Brown-GPT3-ICL]]：长 prompt 中 demonstrations 的历史接口；
- [[习题 - 长上下文利用、Lost-in-the-Middle 与推理证据地图]]；
- [[解答 - 长上下文利用、Lost-in-the-Middle 与推理证据地图]]。
