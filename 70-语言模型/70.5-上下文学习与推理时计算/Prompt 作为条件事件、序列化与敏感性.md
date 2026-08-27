---
type: concept
status: verified
area: [language-models, prompting, in-context-learning]
node_id: LM-33
aliases: [Prompt 条件事件, Prompt 敏感性, 提示序列合同]
prerequisites: ["[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]", "[[指令、消息、Chat Template 与任务序列化合同]]"]
related: ["[[Zero-shot、Few-shot ICL、示例顺序与标签映射]]", "[[Model、API、Tokenizer、Template 版本与复现合同]]"]
sources: ["[[S-2020-Brown-GPT3-ICL]]", "[[S-2021-Zhao-Contextual-Calibration]]", "[[S-2020-Su-7764-MLM-PET]]"]
exercises: ["[[习题 - Prompt 作为条件事件、序列化与敏感性]]"]
solutions: ["[[解答 - Prompt 作为条件事件、序列化与敏感性]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-icl-prompt-conditional-event-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Prompt 作为条件事件、序列化与敏感性

> [!abstract] 一句话结论
> Prompt 不是一句抽象语义，而是送入模型的精确 token 前缀。只要 bytes、规范化、模板、特殊 token、答案前缀或 label token 变化，条件事件就可能变化；prompt sensitivity 因而是需要测量的实验对象。

## 一、从“问题”走到概率事件

设自然语言任务为 $q$，结构化字段为 $m$，模板为 $T_\phi$，tokenizer 为 $\operatorname{Tok}_\psi$。实际前缀是

$$
x=\operatorname{Tok}_\psi(T_\phi(m)).
$$

自回归模型回答序列 $y=(y_1,\ldots,y_L)$ 的概率为

$$
p_\theta(y\mid x)=\prod_{t=1}^{L}p_\theta(y_t\mid x,y_{<t}).
$$

因此“同一个问题”只是在人的任务层等价；模型层真正比较的是不同 $x$。如果两种写法产生 $x_A\neq x_B$，一般没有理由要求

$$
p_\theta(y\mid x_A)=p_\theta(y\mid x_B).
$$

这不是模型一定“脆弱”的定义，而是条件概率本来就允许随条件改变。研究问题应改写为：哪些不改变任务语义的干预会造成多大的行为变化？

## 二、一个 prompt 至少有八层对象

1. 任务语义：要预测什么；
2. 原始数据字段：问题、选项、上下文、元数据；
3. instruction：自然语言规则；
4. demonstrations：若干输入—输出对；
5. query：本次待预测输入；
6. rendered bytes：空格、换行、标点、Unicode 规范化后的字符；
7. token IDs：含 BOS、role marker、分隔符的整数序列；
8. 输出合同：候选 label token、生成边界、停止与 parser。

前六层相同也未必保证第七层相同：tokenizer revision、added-token 表或 normalization 规则可能变化。第七层相同而输出 parser 不同，也会得到不同 exact-match。

## 三、分类任务中的 label 不是抽象类别

假设类别集合为 $\mathcal C=\{c_1,c_2\}$，verbalizer 把类别映射为 token 序列 $v(c)$。模型打分应明确是

$$
s(c)=\log p_\theta(v(c)\mid x)
=\sum_{j=1}^{|v(c)|}\log p_\theta(v_j(c)\mid x,v_{<j}(c)).
$$

只比较第一个 token 会错误处理共享前缀；直接求和又可能偏向短 label。是否使用长度归一化

$$
s_\alpha(c)=\frac{s(c)}{|v(c)|^\alpha}
$$

属于评估协议，而不是无害实现细节。

### 手算例子：首 token 与整序列冲突

设两个标签为 red fox 与 red panda。第一 token red 的概率对两者完全相同，不能区分类别；第二 token 条件概率分别为 $0.7$ 与 $0.2$。只看第一 token 会平局，整序列对数概率才选择 red fox。

再设 positive 被分为一个 token，negative 被分为两个 token。若一方比较第一 token，另一方比较完整序列，所谓模型准确率差异其实混入了 scorer 差异。

## 四、空格和答案前缀为什么会改变结果

许多 tokenizer 将前导空格与词绑定为不同 token。Answer:positive 与 Answer: positive 可能产生不同 ID；大写 A、带括号 (A)、换行后的 A 也可能不同。它们在预训练中出现的频率和上下文不同，所以 label prior 不同。

一个最小审计应同时保存：

- prompt 的 UTF-8 bytes 与可见转义形式；
- rendered text 和 token IDs；
- query 结束位置与答案开始位置；
- 每个 label 的 token IDs；
- raw token log-prob、聚合分数与 parser 输出。

## 五、把敏感性写成估计量

设 $g$ 是保持任务语义的 prompt 变换，如改换行、交换同义 instruction 或改变选项字母。对样本 $i$，定义配对翻转

$$
F_i(g)=\mathbf 1\{\hat y_i(x_i)\neq \hat y_i(gx_i)\},
$$

总体翻转率

$$
\widehat{FR}(g)=\frac1n\sum_{i=1}^{n}F_i(g).
$$

准确率差

$$
\widehat\Delta(g)=\frac1n\sum_i
\left[\mathbf 1\{\hat y_i(gx_i)=y_i\}-\mathbf 1\{\hat y_i(x_i)=y_i\}\right].
$$

$\widehat\Delta$ 可能接近零而翻转率很高：一些答案由错变对，另一些由对变错。只报平均准确率会藏掉不稳定性。

若同时尝试 $M$ 个模板并报告最好一个，估计对象已经变为

$$
\max_{m\le M}\widehat A_m,
$$

它含选择乐观偏差。必须记录候选数、选择数据、规则和独立测试集。

## 六、内容空校准测量什么

Contextual calibration 用 N/A、空字符串等 content-free query 得到标签分布 $\hat p_{cf}(c)$，再调整任务输入的标签分数。其直觉是测量 prompt 和 label token 自身造成的偏置。

重要边界：

- content-free 输入不是自然界唯一的“零信息”事件；
- 它修正的是当前 label space 下的偏置，不保证置信度等于真实正确率；
- 若任务理解错误、示例泄漏或 parser 错误，校准不能修复；
- 必须在 calibration 之前固定 label tokenization。

## 七、图解：同一语义怎样变成三个条件事件

先看图回答：从语义任务到最终类别概率，哪些环节必须被版本化？

![[00-知识库管理/_assets/figures/language-models/fig-lm-icl-prompt-conditional-event-v1.svg|900]]

> [!figure] 图 LM-33　Prompt 条件事件与反事实变体
> 三条序列保留相同分类意图，却因语言、role marker、空格和 tokenizer 输出形成不同 token 前缀。图由本库依据 causal LM 条件概率合同重新绘制。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：先固定左侧任务，再沿每条分支核对 rendered bytes、token IDs 与答案边界；最后比较原始概率、预测翻转和正确率，而非只看最好分支。

**图没有证明什么**：示例数值只是教学用，不证明某种语言或模板更优，也不证明所有语义保持变换都会显著改变输出。

## 八、工程与研究合同

最小 prompt manifest 应含：model/checkpoint、API revision、tokenizer、chat template、完整 bytes、IDs、max context、label map、scoring rule、sampler、stop、parser、seed 和评测集版本。

敏感性实验至少分开：

1. format sweep：空格、换行、标点、role marker；
2. semantic paraphrase：同义 instruction；
3. label sweep：字母、数字、自然词、多 token；
4. order sweep：demonstration 与 option 的排列；
5. decoding sweep：greedy、温度、停止与答案抽取。

不要一次改变多个因子后把差异全归因于“prompt wording”。优先用配对样本、预注册变体和 bootstrap 区间。

## 九、常见错误

- 把 UI 中显示的文本当最终 token 序列；
- 忽略 assistant generation prefix；
- 用第一个 label token 代表多 token 类别；
- 只报告最佳模板，不报告搜索空间；
- 把 contextual calibration 与统计 calibration 混为一谈；
- 把零平均差误解为逐样本稳定；
- API 模型别名漂移后仍声称完全复现。

## 十、出口标准

完成本节后，应能从任一 prompt 重建 bytes→IDs→label scores→prediction 的全过程，手算多 token label 概率，设计配对 sensitivity sweep，并说明任务语义等价为何不推出模型条件事件相同。

## 十一、来源与练习

- [[S-2020-Brown-GPT3-ICL]]：零/单/少样本操作协议；
- [[S-2021-Zhao-Contextual-Calibration]]：格式与 label prior 的诊断；
- [[S-2020-Su-7764-MLM-PET]]：pattern/verbalizer 的中文问题入口；
- [[习题 - Prompt 作为条件事件、序列化与敏感性]]；
- [[解答 - Prompt 作为条件事件、序列化与敏感性]]。
