---
type: concept
status: verified
area: [language-models, evaluation, perplexity, bits-per-byte]
node_id: LM-15
aliases: [PPL, BPB, Cross-tokenizer evaluation]
prerequisites: ["[[概率语言模型、链式法则与自回归因子化]]", "[[Tokenizer 评估、多语言公平、安全与证据地图]]"]
related: ["[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]", "[[Masked LM 的 Corruption Law、伪似然与 BERT]]"]
sources: ["[[S-2020-Salazar-MLM-Scoring]]", "[[S-2018-Radford-GPT]]"]
exercises: ["[[习题 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"]
solutions: ["[[解答 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-nll-ppl-bpb-denominator-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较

> [!abstract] 一句话结论
> Perplexity 是平均 token NLL 的指数，只在概率对象、数据、tokenizer、边界 token 与 denominator 一致时可直接比较。跨 tokenizer 时应回到同一原始字节串上的总 log-likelihood，并用 bits-per-byte 等共同单位；否则“更小 PPL”可能只是 token 更长。

## 一、从总 NLL 到 Perplexity

对自回归模型的有效预测事件集合 $\mathcal I$，定义

$$
N=\sum_{i\in\mathcal I}-\log p_\theta(y_i\mid c_i),
\qquad D=|\mathcal I|.
$$

使用自然对数时，平均 token NLL 与 perplexity 为

$$
\overline\ell_{\mathrm{tok}}=\frac ND,
\qquad \operatorname{PPL}=\exp\left(\frac ND\right).
$$

若使用以 2 为底的对数，则

$$
\operatorname{PPL}=2^{N_{\mathrm{bits}}/D}.
$$

直观上 PPL 是条件分布几何平均概率的倒数：

$$
\operatorname{PPL}
=\left(\prod_{i\in\mathcal I}p_\theta(y_i\mid c_i)\right)^{-1/D}.
$$

“等效平均分支数”只是帮助直觉的说法；只有在均匀分布等特殊情况下，它才真等于候选数。

## 二、手算与单位换算

若三个有效 token 的目标概率为 $0.5,0.25,0.5$，则

$$
N=-\log(0.5\times0.25\times0.5)=\log16,
$$

$$
\overline\ell=\frac{\log16}{3},\qquad
\operatorname{PPL}=16^{1/3}\approx2.52.
$$

若这段原始文本编码为 8 bytes，则

$$
\operatorname{BPB}=\frac{N_{\mathrm{nats}}}{8\ln2}
=\frac{4\ \mathrm{bits}}{8\ \mathrm{bytes}}=0.5\ \mathrm{bits/byte}.
$$

BPB 的“byte”应是锁定原始编码（通常 UTF-8）后的 byte 数，不是模型内部 byte-level token 数。

## 三、为什么跨 tokenizer PPL 不可比

同一字符串 `internationalization`：

- tokenizer A 可能切成 1 个 token；
- tokenizer B 可能切成 5 个 token。

即使两个模型给完整字符串完全相同的概率 $10^{-5}$，有

$$
\operatorname{PPL}_A=(10^{-5})^{-1/1}=10^5,
$$

$$
\operatorname{PPL}_B=(10^{-5})^{-1/5}=10.
$$

B 的 token PPL 小得多，却没有给字符串更高概率。分母单位改变已经足够翻转表面结论。

> [!important] 共同单位的前提
> 要比较 BPB，模型必须对同一组原始 byte strings 定义可求的概率。若 normalization 丢失信息、tokenizer 是随机的、多个 token 序列可 decode 为同一 byte string，字符串概率可能需要对所有潜在 tokenization 求和，不能总把一个 canonical encoding 的概率当完整字符串概率。

## 四、同 tokenizer 比较也可能不公平

以下任何差异都会改变 $N$ 或 $D$：

- 是否预测 BOS、EOS、换行和文档分隔 token；
- padding、prompt、prefix、特殊 token 是否 ignore；
- 长文档按 sliding window 时，每个 token 获得多少左上下文；
- 第一个 chunk 的 warm-up token 是否计分；
- 文档是否拼接，是否允许跨文档上下文；
- OOV/byte fallback 与 normalization 是否一致；
- loss 先按序列平均还是按 token 全局平均。

因此报告 PPL 必须同时报告 numerator、denominator 和 tokenization fingerprint。只保存一个标量无法审计。

## 五、滑动窗口评测

固定上下文上限 $C$ 时，长序列常分块评估。若每个窗口长度为 $C$、stride 为 $s$，应只计窗口中新出现的 $s$ 个 target，旧 token 只提供上下文，避免重复计分。

对位置 $t$，理想上下文为最近 $C$ 个 token：

$$
c_t=x_{\max(1,t-C):t-1}.
$$

评测程序应断言每个目标位置恰计一次，并记录实际 context length 分布。stride 改变不应在语义相同的正确实现中重复改变总 denominator。

## 六、MLM 的 pseudo-perplexity 不是 CLM PPL

MLM 可定义

$$
\operatorname{PPPL}(x)=
\exp\left(-\frac1T\sum_{i=1}^{T}
\log p_\theta(x_i\mid x_{-i})\right).
$$

它使用双向 clean context（除当前位置），而 CLM PPL 使用左前缀；条件信息不同，且 MLM 条件未必对应规范化 joint。PPPL 可在同协议内比较 masked models 或做排序特征，但不能与 CLM PPL 数值并排解释为相同概率对象。

## 七、PPL 能说明与不能说明什么

在同分布、同合同下，更低测试 NLL 表示模型给观测 token 序列更高平均 log probability，是概率预测质量的重要指标。但它不单独保证：

- factuality、安全性、无偏性或指令遵循；
- 采样文本的人类偏好；
- 长上下文利用而非局部频率拟合；
- 低资源语言公平；
- 训练数据未泄漏进测试集。

PPL 对 rare catastrophic error 很敏感，这正是 log score 的性质；同时少量数据污染也会显著美化结果。

## 八、图：同一个 numerator，不同 denominator

先看图回答：为什么完整字符串概率相同而 token PPL 可以不同？

![[00-知识库管理/_assets/figures/language-models/fig-lm-nll-ppl-bpb-denominator-v1.svg|900]]

> [!figure] 图 LM-15　NLL、PPL 与 BPB 的单位账本
> 左侧固定 total NLL；中部展示不同 token count 产生不同 PPL；右侧以共同 UTF-8 byte denominator 转换为 BPB。来源：本课程依据语言模型似然与编码单位定义独立绘制。

**怎样读图**：先比较 numerator 是否来自同一原始文本，再问 denominator 是 token、character、byte 还是预测事件，最后核对 log base。

**图没有证明什么**：图不证明 BPB 对任何 tokenizer 都自动可算，也不表示 BPB 能替代任务质量、安全或效率评价。

## 九、建议的评测记录

```yaml
dataset_hash: ...
raw_encoding: UTF-8
normalization: ...
tokenizer_hash: ...
special_tokens: ...
context_length: ...
window_stride: ...
document_boundary_policy: ...
scored_event_definition: ...
total_nll_nats: ...
effective_tokens: ...
raw_bytes: ...
ppl: exp(total_nll_nats / effective_tokens)
bpb: total_nll_nats / (raw_bytes * ln(2))
```

## 十、本节出口

你应能从目标概率手算 NLL、PPL 与 BPB，构造跨 tokenizer PPL 失真的反例，并审计 sliding-window denominator。下一节[[GPT、BERT、T5 的目标—模型族—能力证据地图]]将用这些合同重新比较经典模型，避免按品牌名推断能力。

## 练习与独立解答

- [[习题 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]
- [[解答 - NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]

