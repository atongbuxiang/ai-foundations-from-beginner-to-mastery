---
type: concept
status: verified
area: [language-models, supervised-finetuning, teacher-forcing, loss-mask]
node_id: LM-26
aliases: [SFT 目标, Response-only loss, Teacher forcing]
prerequisites: ["[[指令、消息、Chat Template 与任务序列化合同]]", "[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]"]
related: ["[[指令数据质量、混合、多轮状态与选择偏差]]", "[[Chain-of-Thought、Scratchpad 与 Faithfulness]]"]
sources: ["[[S-2022-Chung-Flan]]", "[[S-2023-Zhou-LIMA]]", "[[S-2026-HuggingFace-Chat-Templates]]"]
exercises: ["[[习题 - 监督微调、Teacher Forcing 与 Response-only Loss]]"]
solutions: ["[[解答 - 监督微调、Teacher Forcing 与 Response-only Loss]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-sft-loss-contract-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 监督微调、Teacher Forcing 与 Response-only Loss

> [!abstract] 一句话结论
> SFT 仍是 next-token maximum likelihood；特殊之处在于样本如何序列化、哪些 token 被当作监督 target、每个 turn 怎样加权。Teacher forcing 定义训练条件历史，response-only mask 定义 estimand，二者都不能由“SFT”三个字自动推出。

## 一、从条件监督到 token NLL

设一个监督示例含 prompt $x=(x_1,\ldots,x_m)$ 与目标回答 $y=(y_1,\ldots,y_n)$。条件语言模型目标为

$$
p_\theta(y\mid x)
=\prod_{t=1}^{n}
p_\theta(y_t\mid x,y_{<t}),
$$

对应 response-only NLL：

$$
\mathcal L_{\text{resp}}
=-\sum_{t=1}^{n}
\log p_\theta(y_t\mid x,y_{<t}).
$$

这里每个 $y_{<t}$ 都来自 gold response，这就是 teacher forcing。它不是模型自由生成出来的历史。

如果把 system/user/assistant 全序列记为 $z=(z_1,\ldots,z_L)$，通用实现是

$$
N(\theta)=\sum_{t=1}^{L-1}m_t
\big[-\log p_\theta(z_{t+1}\mid z_{\le t})\big],
\qquad
D=\sum_{t=1}^{L-1}m_t,
$$

$$
\mathcal L=N/D.
$$

$m_t$ 决定 shift 后第 $t+1$ 个 token 是否计入 loss。

## 二、先 shift，再谈 mask

给完整序列：

$$
[\text{USER},Q,\text{ASSISTANT},A_1,A_2,\text{EOS}],
$$

inputs 和 labels 必须只错开一次：

| input | USER | Q | ASSISTANT | $A_1$ | $A_2$ |
|---|---|---|---|---|---|
| next label | Q | ASSISTANT | $A_1$ | $A_2$ | EOS |

若 response-only 只监督 assistant 内容和 EOS，loss mask 对应 labels：

$$
m=[0,0,1,1,1].
$$

注意第一个被监督位置的 **input** 是 ASSISTANT marker，label 是 $A_1$。很多 off-by-one 错误会把 marker 自身当作回答 target，或漏掉首回答 token。

框架若在 model 内部自动 shift，外部不要再 shift；最小测试应打印 input IDs、labels、内部对齐与每位置 loss。

## 三、Full-sequence 与 response-only 在优化什么

### Full-sequence loss

它也预测 system/user/template tokens：

$$
\mathcal L_{\text{full}}
=-\sum_{t=1}^{L-1}\log p_\theta(z_{t+1}\mid z_{\le t}).
$$

优点是所有 token 都提供监督，可能帮助学习格式；缺点是长 user prompt 会主导 denominator，模型被训练去模拟用户文本，且跨数据集比较更受 prompt 长度影响。

### Response-only loss

它只计目标 assistant 区域：

$$
\mathcal L_{\text{resp}}
=-\frac{1}{D_{\text{resp}}}
\sum_t m_t^{\text{assistant}}\ell_t.
$$

这更贴近“给定 prompt 生成回答”的条件风险，但仍需明确：

- assistant marker 是否计分；
- EOS 是否计分；
- reasoning/rationale 和 final answer 是否同权；
- tool call 与普通文本是否同权；
- 多轮中所有 assistant turns 还是仅最后一轮。

不存在脱离任务的唯一 mask。

## 四、多轮样本有三种常见 estimand

一段对话含 assistant turns $k=1,\ldots,K$，第 $k$ 轮有效 target 数为 $D_k$，loss sum 为 $N_k$。

### 每 token 等权

$$
\mathcal L_{\text{token}}
=\frac{\sum_kN_k}{\sum_kD_k}.
$$

长回答贡献更大。

### 每 turn 等权

$$
\mathcal L_{\text{turn}}
=\frac1K\sum_k\frac{N_k}{D_k}.
$$

短回答的单 token 权重更大。

### 每 conversation 等权

先对每段对话求均值，再跨对话平均。长对话和短对话同权，但其中 turn 如何加权仍需定义。

三者都是合法 estimand；错误在于代码做一种、论文写另一种或完全不写 denominator。

## 五、Teacher forcing 与自由生成

训练时：

$$
p_\theta(y_t\mid x,y_{<t}^{*}),
$$

推理时：

$$
p_\theta(\hat y_t\mid x,\hat y_{<t}),
\qquad
\hat y_{<t}\sim\mathcal D(p_\theta).
$$

如果早期生成错误，后续条件历史就偏离 gold history，这常被称为 exposure bias。需把三件事分开：

1. 条件历史分布不同是定义事实；
2. 它是否造成某个任务错误是经验问题；
3. scheduled sampling、sequence-level loss 或 preference/RL 方法是否改善，是需要预算匹配的因果实验。

不能把所有生成错误都归因于 exposure bias，也不能因为 teacher forcing 有分布差就断言 token NLL 不合理。

## 六、Attention relation 与 loss mask 是两张表

Response-only mask 只规定哪些 next-token errors 计入目标；它通常不阻止 assistant token attend user/system。事实上，回答必须读取 prompt。

对 packed 多对话 batch，还需：

$$
R_{ij}=1\{j\le i\}1\{\text{conversation}(i)=\text{conversation}(j)\}.
$$

若只 ignore 跨样本 label、却允许后样本读前样本，后样本的 response loss 仍可利用别人的内容。[[Packing、文档边界、Position ID 与 Loss Mask]]的 relation 合同继续适用。

## 七、长度、截断与空监督样本

当序列超过 context window：

- 从左截断可能删除 system 或问题，只剩 response；
- 从右截断可能删除 EOS/final answer；
- 按 token 截断可能切断 tool JSON；
- 按 turn 截断能保结构，但改变历史。

每个 batch 必须断言：

$$
D=\sum_tm_t>0.
$$

若 response 全被截断而 $D=0$，样本应被拒绝或重新构造；静默用 0 loss 会扭曲 sample counts，除 0 则产生 NaN。

## 八、分布式 reduction

设备 $d$ 有 $N_d,D_d$。正确的全局每有效 target mean 是

$$
\mathcal L_{\text{global}}
=\frac{\sum_dN_d}{\sum_dD_d}.
$$

错误做法是

$$
\frac1M\sum_d\frac{N_d}{D_d},
$$

它让每个设备同权而非每 target 同权。若各设备有效 token 数不同——多轮、packing、response-only 时非常常见——两者不等。

还要检查梯度累积和 dynamic batching 是否以同一个全局 denominator 缩放。

## 九、图解：同一序列的三种目标

先看图回答：为什么 full-sequence mask 与 response-only mask 会在同一 input/label 上得到不同梯度？

![[00-知识库管理/_assets/figures/language-models/fig-lm-adapt-sft-loss-contract-v1.svg|900]]

> [!figure] 图 LM-26　SFT 四张量与 teacher-forcing 边界
> 上部固定 serialized tokens 和一次 shift，随后分别画 full-sequence 与 response-only mask；下部对照 gold history 条件与 sampled history 条件。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：逐列先找 input→next label，再看 mask；不要从 token 颜色直接猜 loss。最后比较训练/推理中 $A_2$ 的条件历史。

**图没有证明什么**：它不证明 response-only 总优于 full loss，不证明 exposure bias 是性能差的唯一原因，也不覆盖所有框架的内部 shift 约定。

## 十、最小实现与研究合同

实现应输出：

- template/tokenizer/model revision；
- input IDs、labels、attention relation、loss mask；
- 每序列/turn 的 $N,D$；
- prompt、assistant、tool、rationale 各 target share；
- truncation reason 与 $D=0$ 计数；
- global reduction 的 numerator/denominator；
- train/eval 时 generation template、sampler 与 stop。

研究比较 full vs response-only 时，必须固定 raw conversations、template、有效 targets 或 FLOPs、optimizer、checkpoint selection 和评估解码。若一方因 mask 更稀疏而训练更多 steps，要同时报告 unique examples 与 target exposure。

## 本节出口

你应能给任意多轮 token 序列写出 inputs、shifted labels、relation、loss mask、$N,D$，并解释 teacher forcing 与自由生成的条件差异。下一节把单个样本提升为指令数据分布：[[指令数据质量、混合、多轮状态与选择偏差]]。

## 练习与独立解答

- [[习题 - 监督微调、Teacher Forcing 与 Response-only Loss]]
- [[解答 - 监督微调、Teacher Forcing 与 Response-only Loss]]

