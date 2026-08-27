---
type: concept
status: draft
area: [architecture, attention, tensor-shapes, symmetry]
aliases: [Self-Attention, Cross-Attention, QKV Shape Ledger]
node_id: ARCH-28
prerequisites: ["[[内容寻址、Query、Key 与 Value]]", "[[Attention Mask、因果性与可见性合同]]", "[[稳定求和、点积与矩阵乘法]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[Multi-Head Attention、投影子空间与参数量]]", "[[Attention 失效模式、反例与证据地图]]"]
sources: ["[[S-2015-Bahdanau-Attention]]", "[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2020-Yun-Transformer-Universal-Approximation]]", "[[S-2024-Su-10347-位置编码与置换对称]]"]
exercises: ["[[习题 - Self-Attention、Cross-Attention 与张量形状]]"]
solutions: ["[[解答 - Self-Attention、Cross-Attention 与张量形状]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-self-cross-shapes-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Self-Attention、Cross-Attention 与张量形状

> [!abstract] 本节主问题
> Self-attention 与 cross-attention 并非两套公式，而是 Q/K/V 的来源合同不同。最可靠的理解方法是每次都写出 $T_q,T_k,d_k,d_v$：score 的行来自 query，列来自 key，value 与 key 共用候选轴，输出继承 query 行和 value 宽。

## 一、统一算子

先定义

$$
\mathcal A(Q,K,V;M)
=\operatorname{softmax}_{row}\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V.
$$

只要

$$
Q\in\mathbb R^{T_q\times d_k},\quad
K\in\mathbb R^{T_k\times d_k},\quad
V\in\mathbb R^{T_k\times d_v},
$$

就有

$$
QK^\top:T_q\times T_k,\quad
A:T_q\times T_k,\quad
AV:T_q\times d_v.
$$

Self/cross 的区别不在最后这三行，而在 Q/K/V 是从哪里投影出来。

## 二、Self-Attention

给定一条长度 $T$ 的表示

$$
X\in\mathbb R^{T\times d_{model}},
$$

令

$$
Q=XW_Q,\quad K=XW_K,\quad V=XW_V,
$$

其中

$$
W_Q,W_K\in\mathbb R^{d_{model}\times d_k},\quad
W_V\in\mathbb R^{d_{model}\times d_v}.
$$

于是 $T_q=T_k=T$。Self 指三者来自同一 token 集，不表示 $Q=K=V$；也不表示每个 token 只看自己。可见范围由 mask 决定。

## 三、Cross-Attention

设 query stream 与 memory stream 分别为

$$
X_q\in\mathbb R^{T_q\times d_q},\qquad
X_m\in\mathbb R^{T_k\times d_m}.
$$

可取

$$
Q=X_qW_Q,\qquad K=X_mW_K,\qquad V=X_mW_V.
$$

Q 来自“需要被更新/解码”的对象，K/V 来自“供读取的 memory”。$T_q$ 与 $T_k$ 可以完全不同；输入宽 $d_q,d_m$ 也可不同，只要投影后 Q/K 的比较宽同为 $d_k$。

[[S-2015-Bahdanau-Attention]] 的译码状态读取 encoder states 正是这一接口。现代用途还包括：文本 query 读取图像 patches、latent 读取高分辨率输入、decoder tokens 读取语音/检索 memory。

## 四、一个完整 Shape Ledger

假设 batch $B=8$，$T_q=32$，$T_k=128$，$d_{model}=512$，$d_k=64$，$d_v=80$。忽略多头：

| 张量 | shape | 元素数 |
|---|---:|---:|
| Q | $(8,32,64)$ | 16,384 |
| K | $(8,128,64)$ | 65,536 |
| V | $(8,128,80)$ | 81,920 |
| score/weight | $(8,32,128)$ | 32,768 |
| output | $(8,32,80)$ | 20,480 |

计算主项约为 $O(BT_qT_k(d_k+d_v))$，另加投影成本。不能只说 $O(T^2)$：cross-attention 的 pair 数是 $T_qT_k$，两边长度的增长方式可能不同。

## 五、无位置 Self-Attention 的置换等变性

令 $P$ 为 token 置换矩阵，$X'=PX$。则

$$
Q'=PQ,\quad K'=PK,\quad V'=PV.
$$

无固定非对称 mask 时，

$$
Q'K'^\top=P(QK^\top)P^\top.
$$

Row-softmax 与同步行列重排相容：

$$
\operatorname{softmax}_{row}(PSP^\top)
=P\operatorname{softmax}_{row}(S)P^\top.
$$

所以

$$
\mathcal A(PX)=P\mathcal A(X).
$$

这就是 token 重排等变。加入绝对位置、相对 bias 或固定 causal mask 会改变对称性合同。

## 六、Cross-Attention 的两种重排

若只重排 memory 的 key/value pairs：$K'=P_kK,V'=P_kV$，则

$$
QK'^\top=QK^\top P_k^\top,
$$

score 列与 value 行同步重排，输出不变：

$$
\mathcal A(Q,P_kK,P_kV)=\mathcal A(Q,K,V).
$$

若重排 queries：$Q'=P_qQ$，输出相同地重排行：

$$
\mathcal A(P_qQ,K,V)=P_q\mathcal A(Q,K,V).
$$

因此 cross-attention 对 memory pair 的顺序本可不变，对 query 顺序等变；position/structure 可进一步破坏或细化这些对称性。

## 七、表达定理应怎样读

[[S-2020-Yun-Transformer-Universal-Approximation]] 在明确条件下给出：无位置编码 Transformer 可逼近紧致域上的连续 permutation-equivariant seq-to-seq 函数；加入适当位置编码后可处理一般连续序列到序列函数。

这属于存在性定理：

- 它要求目标连续与规定的紧致域/范数；
- 构造所需深宽可随精度增长；
- 不保证 SGD 找到参数；
- 不给有限样本泛化、鲁棒或效率保证。

所以“通用逼近”不能替代 shape、mask、优化和数据证据。

## 八、常见任务接口

| 场景 | Query 来源 | Key/Value 来源 | 主要风险 |
|---|---|---|---|
| Encoder self-attention | 输入 tokens | 同一输入 | padding/position |
| Decoder causal self-attention | 已生成前缀 | 同一前缀 | future leakage/cache |
| Encoder–decoder cross | decoder states | encoder memory | source padding/length |
| 多模态融合 | 某模态/latent | 另一模态 | tokenization 与尺度不平衡 |
| Retrieval-augmented | generation states | retrieved chunks | 检索泄漏、来源身份丢失 |
| Perceiver-style latent | learned latents | 大输入集合 | bottleneck 与 coverage |

接口名称不能替代对象说明：总要写明每条轴代表什么、mask 如何构造、position 如何注入。

## 九、Science Space 的对称性桥

[[S-2024-Su-10347-位置编码与置换对称]] 的价值是把“模型不知道顺序”改写成可证明的等变性命题。课程采用同步重排的代数推导；对不同位置方案的经验优劣留到后续位置编码卷，不在本节用类比裁决。

## 十、图：Self/Cross 的统一 Shape

先看图回答：cross-attention 为什么输出有 $T_q$ 行而不是 $T_k$ 行？self-attention 的三条投影为什么可共享输入却不能合并成一个角色？

![[00-知识库管理/_assets/figures/architecture/fig-attention-self-cross-shapes-v1.svg|900]]

> [!figure] 图 40.4-04　Self-attention、cross-attention 与 shape ledger
> 左栏展示同源不同投影，中栏展示 query/memory 分源，右栏逐步核对矩阵乘法。来源：依据 Bahdanau 与 Transformer 的 attention 定义独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_attention_v1.py]] 生成。

**怎样读图**：先沿每条投影线标记“来源序列”，再把 score 的行列分别贴到 Q/K，最后从 $AV$ 看出输出沿 query 轴逐行返回 value-width 内容。

**图没有证明什么**：它没有证明 self 与 cross 在性能上可互换，没有证明无位置 Transformer 能学习任意离散算法，也没有计入多头、KV cache 和 kernel 的全部系统成本。

## 十一、常见错误

1. 认为 self-attention 必有 $Q=K=V$；
2. cross-attention 强行要求 $T_q=T_k$；
3. 让 Q/K 投影后的最后一维不同；
4. 让 K/V 的候选轴不同步；
5. 把输出行数写成 $T_k$；
6. 在复杂度中只写一个 $T^2$，丢失 cross 两边长度；
7. 忽略固定 mask/position 对置换对称性的改变；
8. 把通用逼近存在性当训练与泛化保证。

## 十二、掌握标准

> [!summary]
> - Self/cross 共享统一 attention 算子，区别是 Q/K/V 来源；
> - score 为 $T_q\times T_k$，输出为 $T_q\times d_v$；
> - 无位置、无非对称 mask 的 self-attention 对同步 token 重排等变；
> - cross-attention 对 K/V pair 同步重排不变、对 query 重排等变。

能无提示完成 shape ledger（A/B）、证明两类重排性质（C）、定位广播/长度反例（D），并为一个多模态或检索系统写完整 attention interface card（E）。

## 十三、练习与独立详解

- [[习题 - Self-Attention、Cross-Attention 与张量形状]]
- [[解答 - Self-Attention、Cross-Attention 与张量形状]]

## 参考来源

- [[S-2015-Bahdanau-Attention]]
- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2020-Yun-Transformer-Universal-Approximation]]
- [[S-2024-Su-10347-位置编码与置换对称]]
