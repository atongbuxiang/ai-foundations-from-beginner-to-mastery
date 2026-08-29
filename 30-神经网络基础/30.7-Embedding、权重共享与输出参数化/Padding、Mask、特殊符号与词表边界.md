---
type: framework
status: draft
area: [neural-networks/embedding-output, padding, masking, special-tokens, vocabulary]
aliases: [Padding and Mask Contracts, Special Token Contract]
node_id: NN-55
prerequisites: ["[[Embedding Lookup、稀疏梯度与参数规模]]", "[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[计算图、拓扑序与前向执行]]", "[[条件概率、全概率与 Bayes 公式]]"]
related: ["[[遮蔽预测、Teacher–Student 与自监督目标]]", "[[Embedding Lookup、稀疏梯度与参数规模]]", "[[输入—输出权重共享与 Weight Tying]]", "[[Softmax–Cross-Entropy 的稳定融合反向]]"]
sources: ["[[S-2026-PyTorch-Embedding]]", "[[S-2026-PyTorch-Large-Vocabulary-Loss]]", "[[S-2026-HuggingFace-Tokenizer-Special-Tokens]]", "[[S-2017-Vaswani-Transformer复杂度]]"]
exercises: ["[[习题 - Padding、Mask、特殊符号与词表边界]]"]
solutions: ["[[解答 - Padding、Mask、特殊符号与词表边界]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-padding-mask-special-token-contracts-v2.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# Padding、Mask、特殊符号与词表边界

> [!abstract] 本章主问题
> PAD、BOS、EOS、UNK、MASK 等都是词表中的整数 ID，但它们在 tokenizer、embedding、attention、loss 和 generation 中扮演不同角色。`padding_idx`、attention mask、`ignore_index` 与 stop token 是四份独立合同；只设置其中一个，不会自动补齐另外三个。词表一旦变化，embedding、output head、bias、weight tying、optimizer state 与 checkpoint 也必须原子同步。

## 课程位置与两遍学习路线

- **承接什么：** NN-49 已说明 token ID 控制 lookup，NN-51 说明 tied output 可更新未被 lookup 的 rows，NN-52/54 固定了 normalization axis；
- **本页解决什么：** 把同一个 special-token ID 在 embedding、attention、loss 与 decoding 四个子系统中的职责拆开，并建立词表变更的原子事务；
- **后续为何需要：** embedding 分解/量化与任何 checkpoint 部署都必须保持 token-to-row 映射，否则 shape 正确也会发生静默语义错位。

**第一遍只跟踪一个 PAD。** 在具体输入—目标序列上分别写 lookup padding、query–key visibility、valid-loss support 和 generation stop，不让一个布尔 mask 代替四份合同。

**第二遍再扩展生命周期。** 加入 BOS/EOS/UNK/MASK、left/right padding、all-masked rows、packing/segment reset、词表扩容与 optimizer/checkpoint 原子迁移。

### 问题链

1. `padding_idx=0` 为什么只约束 lookup backward，不能自动屏蔽 attention、loss 或 tied output？
2. causal mask、key padding mask 与 query-valid mask 如何组合成一张 edge matrix？
3. `ignore_index` 的 mean reduction 分母为什么必须是有效 target 数而非张量长度？
4. all-masked attention row 为什么可能产生 NaN，它应由数据合同还是 kernel convention 处理？
5. tokenizer 只改 token-to-ID 顺序但 $V$ 不变，为什么仍会静默损坏模型？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal E_\square$ 的四位置序列中写出 3 个有效 target、组合后的三角 attention edges，并解释 PAD row 的 lookup 梯度为零但 tied-output 梯度仍可非零，就已掌握本页主干。

## 符号与对象账本

| 合同 | 作用对象 | PAD 时的典型动作 | 不会自动完成 |
|---|---|---|---|
| tokenizer role | integer ID / sequence assembly | 插入 PAD、BOS、EOS | 模型 mask 与参数 resize |
| embedding padding | $E_{p:}$ 的 lookup use-site | 不累加 lookup VJP | weight decay / tied output freeze |
| attention mask | query–key edges | 删除无效 key/query edges | loss exclusion |
| loss mask | target positions | 从 numerator 与 denominator 排除 | hidden-state computation |
| decoding contract | generated IDs | EOS stop、PAD 禁止/允许 | 训练时 attention/loss mask |
| vocabulary transaction | 所有 vocabulary axes | 同步 reorder/resize/state | 自动语义对齐 |

### 贯穿算例 $\mathcal E_\square$：同一个 PAD ID 的四份职责

把原四词表的 rows 解释为

$$
0=\mathrm{PAD},\quad1=A,\quad2=B,\quad3=\mathrm{EOS}.
$$

取 causal-LM 输入、目标与有效标记

$$
x=(2,1,2,0),
\qquad
y=(1,2,3,0),
\qquad
m=(1,1,1,0).
$$

若逐位置未约简 loss 为

$$
\ell=(0.2,0.4,0.6,9.0),
$$

则正确的 ignored-token mean 是

$$
\boxed{
\mathcal L
=\frac{\sum_t m_t\ell_t}{\sum_t m_t}
=\frac{0.2+0.4+0.6}{3}
=0.4
}.
$$

分母不是 4，PAD 位置的 9.0 也不进入 numerator。若同时屏蔽无效 query/key，合法 attention edge matrix 可写成

$$
A_{ts}=\mathbf1\{t<3\}\mathbf1\{s<3\}\mathbf1\{s\le t\}
=
\begin{bmatrix}
1&0&0&0\\
1&1&0&0\\
1&1&1&0\\
0&0&0&0
\end{bmatrix}.
$$

最后一行是 all-masked query，必须由上层跳过或由 kernel 明确返回零并阻断梯度，不能把 $\operatorname{softmax}(-\infty,\ldots,-\infty)$ 当作普通概率。

若设置 `padding_idx=0`，位置 3 不向 $E_{0:}$ 写 lookup gradient；但 direct tying 时，NN-51 已算出 output use-site 对第 0 行仍有

$$
\bar E_{0:,\mathrm{out}}=D^{-1}(1,1)\ne0.
$$

因此“padding row 冻结”还需处理 weight decay、output mask 或参数拆分，不能只设置 lookup API 参数。

## 核心公式七问：离散序列四层 Mask Contract

$$
\boxed{
(\text{ID role},\text{lookup update},\text{attention edges},\text{loss support},\text{decode rule})
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 防止一个 special-token 配置被误认为端到端语义 |
| 对象 | token IDs、参数 rows、query–key edges、targets 与生成状态机 |
| 来路 | 同一整数在多个子系统中承担不同控制职责 |
| 步骤 | 固定词表 hash→声明 roles→逐层生成 masks→核 denominator→测试 decode/restore |
| 读法 | 每层只约束自己的对象，层间必须显式组合 |
| 检查 | tiny-sequence truth table、all-masked row、PAD=EOS、left/right padding 与 vocab permutation |
| 去路 | packed sequence、KV cache、multimodal special tokens 与 tokenizer migration |

### AI / 系统对应

生产系统中的词表更新应像数据库 schema migration：tokenizer 文件、input/output weights、bias、optimizer states、quantization scales、serving config 与 cache version 必须作为一个不可分割版本发布。只做 `resize_token_embeddings` 而不验证 row mapping，可能得到 shape 全部合法却语义完全错位的模型。

## 一、学习目标

读完本节，你应能：

1. 写出 tokenizer–vocabulary–model 的版本化合同；
2. 区分常见 special tokens 的语义角色；
3. 分开 embedding padding、attention mask、loss mask 与 decoding mask；
4. 正确构造 causal language model 的 shifted inputs/targets；
5. 推导 ignored-token mean reduction 的分母；
6. 组合 causal、padding 与 segment masks；
7. 解释 all-masked row、left/right padding 与 PAD=EOS 的边界；
8. 安全完成词表扩容、参数 resize 和 checkpoint 恢复。

## 二、词表不是一份孤立的 Token→ID 字典

一个可复现的离散输入合同至少包含：

$$
\mathcal V=
(\text{normalizer},\text{pre-tokenizer},\text{model},
\text{token-to-id},\text{special roles},\text{version/hash}).
$$

模型还要满足 shape 约束：

$$
E\in\mathbb R^{V\times d},
\qquad
W_{\mathrm{out}}\in\mathbb R^{V\times d_h},
\qquad
b\in\mathbb R^V.
$$

若 tokenizer 产生 ID $V$，但表只有 rows $0,\ldots,V-1$，lookup 越界；更危险的是 token-to-id 顺序变化但 shape 不变，此时模型会静默把整张语义表错位。

因此 checkpoint 必须绑定 tokenizer files/hash、special-token IDs、vocabulary size 与 row order，而不只是保存 Parameter tensors。

## 三、常见 Special Tokens 的角色表

| 角色 | 典型符号 | 常见用途 | 不自动意味着什么 |
|---|---|---|---|
| padding | PAD | batch 对齐 | 不自动从 attention/loss 移除 |
| beginning | BOS | 标记序列开始、提供首个输入 | 不一定是预测目标 |
| end | EOS | 监督序列结束、generation stop | 不等于 padding |
| unknown | UNK | 词表外回退 | 不表示缺失值机制 |
| masked content | MASK | MLM corruption 占位符 | 不等于 attention 不可见 |
| separator | SEP | 分隔片段/句对 | 不自动阻止跨段 attention |
| classification | CLS | 聚合/分类位置 | 不自动拥有全局信息 |
| task/modality | control tokens | 任务、角色、图像等边界 | 不保证训练语义正确 |

“special”只是 tokenizer/模型登记的角色集合。是否参与预测、被 attention 看见、从 loss 忽略或触发停止都需另行定义。

## 四、同一个 PAD ID 的四份合同

### 4.1 Embedding Padding

`padding_idx=p` 常让 lookup backward 不对 $E_{p:}$ 累积梯度。它只作用于参数表的 lookup path。weight decay、手工修改或 tied output path 仍可能改变该行。

### 4.2 Attention Padding Mask

它作用于 query–key edges，通常阻止真实 query 读取 padded keys；是否也屏蔽 padded queries 取决于后续是否丢弃这些 positions。

### 4.3 Loss Ignore Mask

它作用于 target positions，使对应 loss 不进入总和与梯度。框架 `ignore_index` 是这份合同的一种实现。

### 4.4 Generation/Decoding Contract

它定义哪些 IDs 可生成、哪些触发停止、哪些在 decode 时跳过。PAD 不应仅因在输入中无效就自动成为 EOS。

四者的 shape、算子位置和失效模式都不同。

## 五、Teacher Forcing 的一位错位

原始 token sequence 为

$$
(x_1,x_2,\ldots,x_T).
$$

典型 causal LM 构造：

$$
\text{input}=(\mathrm{BOS},x_1,\ldots,x_T),
$$

$$
\text{target}=(x_1,x_2,\ldots,x_T,\mathrm{EOS}).
$$

模型位置 $t$ 的 hidden state 预测下一项 target。若错误地让 input 与 target 同位，模型可能直接复制当前 token，或 loss 与 causal mask 错一位。

批量 padding 后，target 中 PAD positions 要明确 ignore；EOS 通常仍是有效监督，因为模型需要学习何时结束。

## 六、手算：Token Mean 与 Sequence Mean 不同

设两条序列有效 token losses 分别为

$$
(0.2,0.4),
\qquad
(0.3,0.5,0.7).
$$

全 batch valid-token mean 是

$$
\ell_{\mathrm{token}}
=\frac{0.2+0.4+0.3+0.5+0.7}{2+3}
=\frac{2.1}{5}=0.42.
$$

先逐序列平均、再平均序列：

$$
\ell_{\mathrm{seq}}
=\frac12\left(
\frac{0.6}{2}+\frac{1.5}{3}
\right)
=0.40.
$$

默认 `mean` 常按 non-ignored elements 计分母，相当于长序列贡献更多 token weight。若研究问题要求每条样本等权，就必须显式先做 per-sequence reduction。

分布式训练还要全局合并 numerator 与 valid count：平均每 rank 的 local means 在 valid counts 不等时是错的。

## 七、Attention Mask 是边的集合

对 scores

$$
S\in\mathbb R^{B\times H\times T_q\times T_k},
$$

定义允许边 indicator

$$
M_{bhts}\in\{0,1\}.
$$

数学上希望

$$
\widetilde S_{bhts}=
\begin{cases}
S_{bhts},&M_{bhts}=1,\\
-\infty,&M_{bhts}=0.
\end{cases}
$$

然后沿 key 轴做 Softmax。常见允许条件是多个 masks 的交：

$$
M=M_{\mathrm{causal}}
\land M_{\mathrm{key\ padding}}
\land M_{\mathrm{segment}}
\land M_{\mathrm{task}}.
$$

这里 mask 作用的是 edges，不是只给每个 token 一个“有效/无效”标签。

## 八、Causal、Padding 与 Segment Mask 不能互换

### Causal Mask

对 self-attention，通常允许

$$
s\le t,
$$

禁止 query $t$ 读取未来 key $s>t$。

### Padding Mask

禁止读取为 batch 对齐添加的 keys。它与时间先后无关。

### Segment/Block Mask

packing 多条样本进一个长序列时，必须阻止不同样本互相 attention；仅有 causal mask 仍会让后一个 packed sample 读取前一个 sample。

### Loss Mask

即使 attention edges 已正确，boundary、prompt、padding 或只训练 assistant spans 的 positions 是否进入 loss 仍需独立 mask。

## 九、有限负数 Mask 的数值边界

若 scores 为 $(2,1,0)$，屏蔽第三项并用 $-\infty$：

$$
p=(0.73106,0.26894,0).
$$

若改成有限 $-10$：

$$
p_3
=\frac{e^{-10}}{e^2+e^1+e^{-10}}
\approx4.49\times10^{-6},
$$

并非数学上的零。低精度、temperature 或 fused-kernel convention 会改变“足够负”的意义。

实现可使用 dtype-aware minimum/additive mask 或布尔 mask 的 fused contract，但必须验证：

- masked probability 精确/数值为零；
- masked logits 不产生梯度；
- valid logits 与 unmasked reference 相同；
- 不同 dtype 和 kernel 路径一致。

## 十、All-Masked Row 是未定义条件分布

若某个 query 的全部 keys 都被设为 $-\infty$，则 stable Softmax 会遇到

$$
m=\max_j(-\infty)=-\infty,
$$

随后 $-\infty-(-\infty)$ 产生 NaN，或者实现返回全零但不再是概率和 1。

必须给出显式合同，例如：

1. 保证每个保留 query 至少有一个 valid key；
2. 删除 padded query rows；
3. 为该行指定零输出并阻断梯度；
4. 保留 self/sentinel edge。

不要把 kernel 恰好返回的值当作模型定义。

## 十一、Left Padding、Right Padding 与 Position IDs

训练 encoder 时左右 padding 常可由正确 mask 消去；autoregressive generation 则更敏感：

- batched prompts 的“最后有效 token”位置不同；
- absolute position IDs 是否从 pad 后重新编号；
- KV cache append 的 position；
- logits 从哪一个 sequence position 读取；
- EOS/PAD 的 stop 判定。

只更换 `padding_side` 而不重算 position IDs/last-valid index，可能使同一 prompt 在 batch 内外给出不同输出。

## 十二、PAD 与 EOS 复用的精确边界

有些 decoder-only 系统令

$$
\mathrm{PAD\_ID}=\mathrm{EOS\_ID}.
$$

这可以工作，但必须靠 masks 区分“原序列中的 EOS target”和“对齐产生的 padding”。典型风险：

- 按 token ID 忽略 loss 会把真实 EOS 监督也删掉；
- generation 看到 prompt padding ID 就误判已结束；
- attention mask 丢失时 padding 被当作多次 EOS content；
- 统计 EOS 频率时混入 padding；
- tied output row 同时承担 stop prototype 与 padding input。

安全做法是保留显式 attention/loss masks 和 sequence lengths，以位置来源而非仅 ID 决定语义。

## 十三、UNK、MASK 与“不可见”不是同义词

UNK 是 tokenizer 对未覆盖输入的离散回退，模型通常应该看见并处理它。MASK 在 masked-language modeling 中代表被破坏位置，模型更必须通过上下文预测原 token；它不是 attention mask。SEP/CLS 也常主动参与 attention 与 loss/readout。

因此名称中出现 `MASK` 不代表把 attention score 设为 $-\infty$。

## 十四、Packed Sequence 的四项审计

把多条短序列拼到一个 block 可减少 padding 浪费，但必须同时处理：

1. **attention block boundaries**：不能跨样本读；
2. **position IDs**：每段 reset 还是全局递增；
3. **loss boundary**：前一段末尾不能预测后一段 BOS，除非任务如此定义；
4. **state/cache**：RNN/SSM/KV state 是否在段边界 reset。

packing 改变的是计算布局，不应静默改变训练样本的条件分布。

## 十五、词表扩容与缩减

添加 $m$ 个 tokens 后，新词表大小

$$
V'=V+m.
$$

至少同步：

- tokenizer encoder/decoder；
- input embedding rows；
- untied output rows 与 bias；
- tied Parameter identity；
- quantization scales/codebooks；
- optimizer moments/master weights；
- sharding metadata；
- generation allow/deny lists；
- checkpoint config 与 tokenizer hash。

新 rows 的初始化也需声明：随机、已有 token 平均、分词组合或继续预训练。只 resize tensor 不保证新 token 已学会。

删除/重排 tokens 更危险：必须显式 old-ID→new-ID map 重排所有词表轴状态；不能只截断最后几行，除非被删除 tokens 确实位于末尾且所有映射同步。

## 十六、最小测试矩阵

| 测试 | 应验证 |
|---|---|
| 单样本 vs padded batch | 有效位置 logits 一致 |
| left vs right padding | 在正确 position/mask 下输出一致 |
| PAD row backward | lookup contribution 为零或符合合同 |
| loss ignore | ignored position gradient 为零、分母正确 |
| causal suffix mutation | prefix logits 不变 |
| packed vs unpacked | 每段有效 logits/loss 一致 |
| all-masked row | 显式行为、无 NaN |
| add token save/load | row mapping、tying、optimizer state 保持 |
| PAD=EOS generation | 不提前 stop、真实 EOS 仍监督 |

这些测试应覆盖 eager/fused、训练/推理和目标 dtype，而不只测一个 Python reference。

## 十七、常见误区

1. **“设了 `padding_idx` 就完成 padding”**：attention/loss/decode 仍未定义；
2. **“special token 自动不进 loss”**：是否监督由 labels/mask 决定；
3. **“MASK token 就是 attention mask”**：一个是输入内容，一个是边约束；
4. **“有限大负数就是 $-\infty$”**：概率仍可能非零；
5. **“忽略项后 mean 除以原长度”**：常见 API 除以 non-ignored count；
6. **“PAD=EOS 只省一个 ID”**：它耦合 stop、loss 与 input row 角色；
7. **“新增 token 只改 tokenizer”**：所有词表轴参数和状态都要 resize。

## 十八、图：错位、Attention Edges 与词表生命周期

先看图回答：为什么 EOS 是有效 target 而 PAD 不是？为什么 q3 的 all-masked row 不能任由 Softmax 解释？添加 token 时为什么 optimizer state 也属于原子更新？

![[00-知识库管理/_assets/figures/neural-networks/fig-padding-mask-special-token-contracts-v2.svg|900]]

> [!figure] 图 30.7-07　Teacher forcing、attention mask 与 vocabulary lifecycle
> 左栏展示 BOS 输入、next-token target 与 valid-loss denominator；中栏把 causal+padding mask 画成 query–key edge matrix，并标出 all-masked row；右栏要求 tokenizer、input/output 参数、optimizer 和 decode contract 原子同步。来源：依据 PyTorch Embedding/CrossEntropy、Hugging Face tokenizer 与 Transformer mask 合同绘制；由 [[00-知识库管理/_labs/code/plot_embedding_output_advanced_v2.py]] 确定性生成。

**怎样读图**：先沿位置轴检查 input/target shift，再沿二维 attention edge 检查可见性，最后沿词表生命周期检查 ID、row、state 与 generation role 是否同步。

**图没有证明什么**：图不规定所有模型都必须使用同一 BOS/EOS/PAD 方案，也不证明某个有限负 mask 值在所有 dtype/kernel 中等价于 $-\infty$。

## 十九、最小验收

1. 写出词表/模型 shape 合同；
2. 区分八类 special token 角色；
3. 分开四种 padding/mask；
4. 构造 shifted input/target；
5. 复算 token mean 0.42 与 sequence mean 0.40；
6. 组合 causal/padding/segment masks；
7. 解释 finite mask 与 all-masked row；
8. 审计 left/right padding、PAD=EOS 与 packing；
9. 给出 vocabulary resize 的原子清单与测试。

> [!summary]
> 离散序列系统的正确性依赖多份相互独立的合同：token ID 的角色、embedding row 的更新、attention edges、loss support、reduction denominator 和 generation stop。任何一个 mask 正确都不能替代其余层；词表变化则必须把所有词表轴参数、状态和部署配置作为一个版本化事务更新。

- [[Embedding、权重共享与输出参数化 MOC]]
- [[习题 - Padding、Mask、特殊符号与词表边界]]
- [[解答 - Padding、Mask、特殊符号与词表边界]]
