---
type: solution
status: draft
area: [neural-networks/embedding-output, padding, masking, special-tokens, vocabulary]
topic: "[[Padding、Mask、特殊符号与词表边界]]"
exercise: "[[习题 - Padding、Mask、特殊符号与词表边界]]"
sources: ["[[S-2026-PyTorch-Embedding]]", "[[S-2026-PyTorch-Large-Vocabulary-Loss]]", "[[S-2026-HuggingFace-Tokenizer-Special-Tokens]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Padding、Mask、特殊符号与词表边界

## A

### NN-PMS-A01

`padding_idx` 作用于 embedding table 的某一行及 lookup backward，常是 scalar ID；它不定义 attention。Attention padding mask 作用于 query–key edges，最终需广播到 $B\times H\times T_q\times T_k$ 或实现规定的等价 shape。Loss `ignore_index` 作用于 target positions，label 常为 $B\times T$，决定哪些 unreduced losses/gradients进入 reduction。Generation stop condition 作用于每条已生成 ID sequence 与结束状态，通常按 batch 维护 finished flag。四者所在算子、shape、梯度和时间阶段都不同。

### NN-PMS-A02

BOS 提供序列开始边界；EOS 是结束监督/停止候选；PAD 只做 batch 对齐；UNK 是词表外回退；MASK 是 MLM 中可见的 corruption 占位符；SEP 标记片段边界。Tokenizer 把它们登记为 special，主要影响拆分、自动插入和 decode skip 等行为。模型是否允许它们被 attention 看见、是否作为 target、是否忽略 loss、是否停止生成，分别由 architecture、labels/masks 和 decoder protocol 决定，不能由“special”这个集合自动推出。

### NN-PMS-A03

至少绑定 normalizer、pre-tokenizer、tokenization model、token→ID 与 ID→token 的完整 row order、special-role→ID、padding/truncation side、自动 special-token 插入规则和 tokenizer hash/version。模型侧绑定 $V$、input embedding/output head/bias shapes、tying/projection identity、quantization/sharding metadata，以及 optimizer/master state 的词表轴顺序。Checkpoint 还应保存迁移 map 与 generation allow/deny/stop IDs；只比较 vocabulary size 不足以识别语义错位。

## B

### NN-PMS-B01

标准一位右移为

$$
\text{input}=(\mathrm{BOS},a,b,c),
\qquad
\text{target}=(a,b,c,\mathrm{EOS}).
$$

补到长度 6 后可写成

$$
\text{input}=(\mathrm{BOS},a,b,c,\mathrm{PAD},\mathrm{PAD}),
$$

$$
\text{target}=(a,b,c,\mathrm{EOS},\mathrm{PAD},\mathrm{PAD}),
\qquad
m_{\rm loss}=(1,1,1,1,0,0).
$$

EOS 保留监督，因为模型要学习终止；补齐产生的两个 PAD positions 才被忽略。

### NN-PMS-B02

Valid-token mean：

$$
\frac{0.2+0.4+0.3+0.5+0.7}{5}=\frac{2.1}{5}=0.42.
$$

Sequence-equal mean：

$$
\frac12\left(\frac{0.6}{2}+\frac{1.5}{3}\right)=\frac12(0.3+0.5)=0.40.
$$

常见 `ignore_index` 配合 `mean` 是把 non-ignored losses 求和再除以有效元素数，更接近 0.42；它让长序列按有效 token 数获得更大权重。

### NN-PMS-B03

第三项替换成 $-\infty$ 时

$$
\operatorname{softmax}(2,1,-\infty)
=(0.7310586,0.2689414,0).
$$

替换成 $-10$ 时

$$
p_3=\frac{e^{-10}}{e^2+e^1+e^{-10}}\approx4.49\times10^{-6},
$$

前两项约为 $(0.7310553,0.2689402)$。有限数仍给被 mask 项正质量和非零导数；dtype、temperature 与 fused kernel 还会改变该残余量。

## C

### NN-PMS-C01

令 $M=\sum_jm_j>0$。把 $m_i$ 视作不求导的离散合同，则

$$
\frac{\partial L}{\partial\ell_i}=\frac{m_i}{M}.
$$

Ignored item 的梯度为 0；每个 valid item 权重为 $1/M$。多 rank 时正确全局目标是

$$
L=\frac{\sum_r\sum_{i\in r}m_i\ell_i}{\sum_r\sum_{i\in r}m_i}.
$$

若先算 local mean 再等权平均 ranks，相当于每个 rank 等权，而不是每个 token 等权；valid counts 不等时二者不同。应 all-reduce numerator 与 count，或按全局 count 正确缩放 local gradient。

### NN-PMS-C02

允许边可写为

$$
M_{ts}=\mathbf1[s\le t]\,
\mathbf1[\operatorname{seg}(s)=\operatorname{seg}(t)]\,
\mathbf1[s,t\text{ valid}].
$$

两段 $(1,2)$ 与 $(3,4,5)$ packed 后的矩阵（行是 query，列是 key）为

$$
M=
\begin{bmatrix}
1&0&0&0&0\\
1&1&0&0&0\\
0&0&1&0&0\\
0&0&1&1&0\\
0&0&1&1&1
\end{bmatrix}.
$$

只有 causal mask 会错误地让第二段读取第一段；segment condition 负责切断该泄漏。

### NN-PMS-C03

Stable Softmax 先算 $m=\max_jz_j$。全为 $-\infty$ 时 $m=-\infty$，随后 $z_j-m$ 是未定义的 $-\infty-(-\infty)$，可产生 NaN；即使 kernel 返回全零，也不再是和为 1 的概率。合法合同包括：其一，在数据/掩码层保证每个保留 query 至少一个 valid key，照常反向；其二，对全 mask row 明确返回零向量，并规定对 scores/value 的梯度全零；其三，加入 self/sentinel edge，使输出是该合法 edge 的 value 且按普通 attention 反向。也可以删除 padded query rows，本质上是第二类的结构化实现。

## D

### NN-PMS-D01

对同一 prompts 构造单样本、left-padded batch、right-padded batch；依据有效 token 顺序重建 position IDs，不让 PAD 消耗语义位置。比较每个有效位置 logits、从 last-valid index 取得的 next-token logits，以及逐步追加 KV cache 后的 logits；不能固定读取矩形张量最后一列。用同一 deterministic decode 设置检查 EOS/finished flags，只对已生成的 EOS 终止，不因 prompt padding 终止。测试不同长度混批、batch permutation、cache/no-cache 和 save/load；误差阈值按 dtype 预先定义。

### NN-PMS-D02

若按 `label == EOS_ID` 全部设为 ignore，就会把真实序列末尾的 EOS 监督删除。应同时保存原始 sequence length/position-origin mask：先构造 target，使真实末尾位置为 EOS，再在补齐位置写入同一个 ID 也无妨，但 loss-valid 由“位置是否来自真实 target”决定。例如 label 为 $(a,b,\mathrm{EOS},\mathrm{EOS},\mathrm{EOS})$ 时 mask 可为 $(1,1,1,0,0)$。Framework 可把后两个 labels 替换为独立 `ignore_index`（不必是词表 ID），或使用 unreduced loss 乘位置 mask；attention 与 generation 仍各自用 lengths/finished flags。

### NN-PMS-D03

显式错误包括新 ID 超出 input table 导致 gather 越界，或 output/label 超出 logits 维度导致 loss 报错。Silent errors 包括只扩 input 未扩 output/bias、tying 被复制打断、新 rows 随机但无 optimizer state、shard/quant scale 错位、generation deny list 漏新 ID、保存后 tokenizer 与 checkpoint 不一致。迁移应冻结 old-ID→new-ID map，原子 resize/reorder input、output、bias、tied identity、master/moments、quantization和 sharding metadata；定义新 rows 初始化，更新 config/hash/stop lists，随后做 row mapping、forward/backward、一步 optimizer、save/load 与 tokenizer round-trip 测试。

## E

### NN-PMS-E01

随机生成不同长度、padding side、segment packing 和 special-token 组合，检验：单样本与 padded batch 有效 logits/loss 等价；未来 suffix 变化不影响 causal prefix；ignored labels 的 logit gradient 为零且 denominator 正确；masked edges 概率/梯度满足实现合同；每个保留 query 无 NaN；PAD row 更新符合合同；PAD=EOS 不提前停止。把测试矩阵交叉到 eager/fused、FP32/BF16/FP16、train/eval、cache/no-cache，并对 vocabulary resize 做 save/load identity 与一步更新。Property failure 要保存最小反例、seed、dtype 和 kernel 名。

### NN-PMS-E02

Attention mask 只阻止若干信息边。PAD lookup row 仍可能被 weight decay或 tied output 更新；PAD target 若未 ignore 仍进入 loss；position IDs/last-valid index 仍可能错；某些 normalization 或 pooling 仍会把 padded positions 纳入统计；optimizer state 与 sparse updates 可能包含 PAD row；accuracy/NLL 若分母含 padding 会被稀释。故必须分别验证表示、边、loss、位置/状态、参数更新和指标 reduction，不能用一张 attention mask 替代整个 padding 合同。

### NN-PMS-E03

先定义 oracle：逐样本执行、同一 position reset、同一 causal objective。Packing 构造 block-diagonal causal edge mask、每段 position IDs、边界 loss mask（禁止前段末尾预测后段开头，除非任务定义如此）和 state/KV reset。关闭 dropout 或对齐随机 mask，固定数值 kernel 与 reduction；比较逐段有效 logits、unreduced losses、全局 numerator/count 及参数 gradients。再覆盖长度/顺序/空段边界、低精度与分布式 counts，并用 suffix mutation 检查跨段零影响。验收以预先声明的绝对/相对容差和无 NaN 为门槛。
