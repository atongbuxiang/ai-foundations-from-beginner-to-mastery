---
type: concept
status: verified
area: [language-models, causal-lm, loss-contract]
node_id: LM-10
aliases: [CLM, Next-token loss, 因果语言建模]
prerequisites: ["[[概率语言模型、链式法则与自回归因子化]]", "[[Attention Mask、因果性与可见性合同]]"]
related: ["[[Prefix LM、UniLM 与序列到序列 Mask 合同]]", "[[NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"]
sources: ["[[S-2018-Radford-GPT]]"]
exercises: ["[[习题 - Causal LM 的 Shift、Attention Mask 与 Token Loss]]"]
solutions: ["[[解答 - Causal LM 的 Shift、Attention Mask 与 Token Loss]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-causal-shift-mask-loss-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Causal LM 的 Shift、Attention Mask 与 Token Loss

> [!abstract] 一句话结论
> Causal LM 的实现合同由三件互不替代的事组成：输入与标签错一位、位置 $t$ 的表示看不到目标及其未来、只有被指定的有效标签进入分子和分母。任一项错位，代码仍可能运行，却不再优化声称的自回归 NLL。

## 一、从概率项到训练行

把完整 token 序列固定为

$$
z=(\langle\mathrm{bos}\rangle,x_1,\ldots,x_T,\langle\mathrm{eos}\rangle).
$$

最直观的训练配对是

```text
input : BOS   x1   x2  ...  xT
label : x1    x2   x3  ...  EOS
index : 0     1    2   ...  T
```

第 $t$ 个 logit 必须预测同列 label，而它的可见输入只到同列 input 为止。若框架接收完整 `input_ids=z` 并在 loss 内部 shift，外部就不能再 shift 一次；“谁负责错位”属于 API 合同。

## 二、四个张量必须同时画出来

批大小 $B$、训练长度 $L$、词表大小 $V$ 时：

| 对象 | 形状 | 含义 |
|---|---|---|
| `input_ids` | $[B,L]$ | 模型实际读取的 token |
| `logits` | $[B,L,V]$ | 每个位置对下一 token 的未归一化分数 |
| `labels` | $[B,L]$ | 每个位置应预测的 token id |
| `loss_mask` | $[B,L]$ | 哪些标签计入目标 |
| `attention_mask/relation` | $[B,L,L]$ 或可广播形式 | 哪个 query 可读哪个 key |

`attention_mask` 控制信息流，`loss_mask` 控制统计量。一个位置可以“可被看见但不计损失”（提示词），也可以“自身计损失且只能看过去”（普通 answer token）。把二者混成一个布尔数组会遮蔽错误。

## 三、因果可见性关系

以输入索引 $i$ 为 query、$j$ 为 key，最基本的左到右关系为

$$
R_{ij}=\mathbf 1\{j\le i\}.
$$

在 attention logits 上通常加偏置

$$
A_{ij}=\begin{cases}
0,&R_{ij}=1,\\
-\infty,&R_{ij}=0.
\end{cases}
$$

于是 softmax 后不可见位置权重为零。实际实现还需与 padding、packed sequence 的文档块对角关系取交集。仅有三角 mask 不能阻止 pack 中后一篇文档读取前一篇文档；是否允许这种跨文档上下文必须显式决定。

## 四、token loss 的分子与分母

令 $m_{bt}\in\{0,1\}$ 是有效标签指示器，$y_{bt}$ 为标签，模型分布为

$$
p_{btv}=\operatorname{softmax}(\ell_{bt})_v.
$$

总 NLL 与 token 平均 NLL 分别为

$$
N=\sum_{b,t}m_{bt}\big[-\log p_{bt,y_{bt}}\big],\qquad
D=\sum_{b,t}m_{bt},\qquad
\mathcal L=\frac ND.
$$

当 $D=0$ 时不能静默除零或返回伪造的 0；应跳过 batch、重新采样，或给出受测试的明确行为。分布式训练时必须全局规约 $N$ 和 $D$ 后再相除，不能先对各设备局部平均再等权平均：设备有效 token 数不同时，两者估计量不同。

### 一个分母反例

设备 A 有 100 个有效 token、平均损失 1；设备 B 有 10 个有效 token、平均损失 3。

$$
\text{正确全局均值}=\frac{100\times1+10\times3}{110}\approx1.182,
$$

而设备均值的算术平均为 $2$。后者让短 batch 获得十倍相对权重。

## 五、泄漏为什么可能得到“漂亮”的 loss

若位置 $t$ 的表示读到 $x_{t+1}$，而同一位置标签正是 $x_{t+1}$，网络可以近似复制目标。训练 loss 快速下降不代表学会条件分布，只代表信息合同被破坏。

最小防泄漏测试：

1. 构造两条样本，它们的允许前缀完全相同、未来 token 不同；
2. 比较某个过去位置的 logits；
3. 在 `eval`、关闭 dropout 条件下，允许前缀位置的 logits 应一致；
4. 再故意移除 causal mask，测试应失败。

这类 metamorphic test 比“loss 能下降”更接近目标语义。

## 六、padding、packing 与 label ignore

- **右 padding**：padding key 通常不可见；对应 labels 设 ignore，分母排除。
- **左 padding**：需验证 position ids 与缓存索引；三角关系相对真实 token 的顺序仍应正确。
- **文档 packing**：若要求样本独立，relation 应为每篇文档内部下三角的块对角矩阵。
- **特殊 token**：BOS 通常只作输入；EOS 常作标签；PAD 通常二者都不作。这里只是常见合同，不是不可更改的自然法则。
- **prompt masking**：监督微调可让 prompt 可见但 labels ignore，只对 answer 区域算 loss；这不是纯预训练 CLM 的默认分母。

## 七、最小伪代码

```python
# z: [B, L+1]
inputs  = z[:, :-1]
targets = z[:, 1:]
logits  = model(inputs, causal_relation, document_ids)  # [B,L,V]
token_nll = cross_entropy(logits, targets, reduction="none")
valid = target_is_real & target_is_scored
numerator   = (token_nll * valid).sum()
denominator = valid.sum()
loss = numerator / denominator
```

若模型 API 自行 shift，伪代码应相应改写并加 alignment 单测。不能从变量名猜测库行为。

## 八、图：Shift、可见性与计分区

先看图回答：为什么 causal mask 正确仍不足以保证 loss 正确？

![[00-知识库管理/_assets/figures/language-models/fig-lm-causal-shift-mask-loss-v1.svg|900]]

> [!figure] 图 LM-10　Causal LM 的三份独立账本
> A 对齐 input 与 next-token label；B 画 query–key 可见性；C 分开 loss 分子、有效 token 分母和 ignore 区域。来源：本课程依据自回归 NLL 与 attention relation 独立绘制。

**怎样读图**：按同一位置竖直核对 input/label，再横向查看该 query 的可见 key，最后检查 label 是否进入 loss mask。

**图没有证明什么**：图不规定某个框架的 mask 极性、张量广播或 shift API，也不说明 teacher forcing 下的低 NLL 足以预测自由生成质量。

## 九、实现验收清单

- 固定一个 5-token 玩具序列，打印 inputs 与 labels；
- 检查 logits/labels 形状和 flatten 顺序；
- 用手算 softmax 对一个位置核对 NLL；
- 改 padding token，不应改变有效 token 的 $N,D$；
- 改未来 token，不应改变过去 logits；
- 分布式记录全局 numerator、denominator，而非只有 loss；
- 明确 BOS、EOS、PAD、prompt 与跨文档边界的处理。

## 十、本节出口

你应能从序列写出 shift 表、关系矩阵和 loss mask，并用同一个手算结果审计训练代码。下一节[[Masked LM 的 Corruption Law、伪似然与 BERT]]将把“只读过去”换成“观察被破坏的双向上下文”，同时保留同样严格的 sampler 与 denominator 账本。

## 练习与独立解答

- [[习题 - Causal LM 的 Shift、Attention Mask 与 Token Loss]]
- [[解答 - Causal LM 的 Shift、Attention Mask 与 Token Loss]]

