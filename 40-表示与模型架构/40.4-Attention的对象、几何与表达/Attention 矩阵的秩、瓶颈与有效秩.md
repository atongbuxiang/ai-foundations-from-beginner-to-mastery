---
type: concept
status: draft
area: [architecture, attention, matrix-rank, expressivity]
aliases: [Attention Rank, Logit Rank, Effective Rank of Attention]
node_id: ARCH-31
prerequisites: ["[[Multi-Head Attention、投影子空间与参数量]]", "[[Attention 的几何、核与概率视角]]", "[[奇异值分解]]", "[[有效秩]]"]
related: ["[[Attention 的对象、几何与表达 MOC]]", "[[Attention 失效模式、反例与证据地图]]", "[[Attention Mask、因果性与可见性合同]]"]
sources: ["[[S-2020-Bhojanapalli-LowRank-Attention]]", "[[S-2021-Dong-Pure-Attention-RankCollapse]]", "[[S-2025-Su-10847-矩阵的有效秩]]", "[[S-2021-Su-8610-线性Transformer反例]]", "[[S-2023-Su-9529-DecoderOnly低秩猜想]]"]
exercises: ["[[习题 - Attention 矩阵的秩、瓶颈与有效秩]]"]
solutions: ["[[解答 - Attention 矩阵的秩、瓶颈与有效秩]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-attention-rank-effective-rank-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Attention 矩阵的秩、瓶颈与有效秩

> [!abstract] 本节主问题
> “Attention 是低秩的”这句话若不说明计算对象，几乎必然误导。Logit $L=QK^\top$、softmax 权重 $A$、输出 $O=AV$、多头拼接和层间表示有不同 rank；softmax 是非线性的，能把低秩 logit 变成满秩权重。严格秩又对微小奇异值极敏感，必须与数值秩和有效秩分开。

## 一、先建立四本 Rank 账

| 对象 | shape | 直接可得的 rank 界 |
|---|---:|---:|
| Logit $L=QK^\top$ | $T_q\times T_k$ | $\operatorname{rank}L\le d_k$ |
| Weight $A=\operatorname{softmax}_{row}(L+M)$ | $T_q\times T_k$ | 非线性后不能沿用 $d_k$ 界 |
| Output $O=AV$ | $T_q\times d_v$ | $\operatorname{rank}O\le\min(\operatorname{rank}A,\operatorname{rank}V)$ |
| Token representation $H^{(\ell)}$ | $T\times d$ | 受完整 block、residual、MLP 等影响 |

第一行来自矩阵乘积秩不等式：

$$
\operatorname{rank}(QK^\top)
\le\min(\operatorname{rank}Q,\operatorname{rank}K)\le d_k.
$$

这条恒等式不能越过 row-softmax 直接贴到 A 上。

## 二、最小反例：Rank-1 Logit 变成满秩权重

取

$$
L=\begin{bmatrix}0&0\\0&1\end{bmatrix}
=\begin{bmatrix}0\\1\end{bmatrix}
\begin{bmatrix}0&1\end{bmatrix},
$$

故 $\operatorname{rank}L=1$。逐行 softmax：

$$
A=\begin{bmatrix}
1/2&1/2\\
1/(1+e)&e/(1+e)
\end{bmatrix}.
$$

其行列式

$$
\det A=\frac{e-1}{2(1+e)}>0,
$$

所以 $\operatorname{rank}A=2$。这已否定“attention weight rank 永远不超过 $d_k$”的说法。

原因是 row-wise exponential 与 normalization 是非线性；非线性映射一般不保矩阵秩。

## 三、低秩瓶颈论文究竟说什么

[[S-2020-Bhojanapalli-LowRank-Attention]] 研究：在给定输入/投影维度下，哪些 stochastic attention matrices 能由 dot-product + softmax 参数化表达，以及 head dimension 何时限制可达集合。

它比 $\operatorname{rank}(QK^\top)\le d_k$ 更细，但不能压成错误口号：

- 论文讨论可表示性与维度条件；
- softmax 后矩阵可满秩；
- “满秩”仍不表示任意 row-stochastic matrix 可达；
- 增大 head width 解开某些瓶颈，不保证训练与泛化。

阅读任何 low-rank attention 结果都要写序列长度、head dimension、输入是否可自由选、mask、softmax 方向与量词。

## 四、Causal Attention 的严格满秩

Inclusive causal mask 使 $A$ 下三角。若每个对角 logit 有限，则 $A_{ii}>0$，所以

$$
\det A=\prod_iA_{ii}>0.
$$

因此任意这样的有限 softmax causal attention matrix 严格满秩。[[S-2023-Su-9529-DecoderOnly低秩猜想]] 以此提出架构解释；本节只把行列式结论视为 `I`。

满秩不等于：

- 最小奇异值不小；
- 条件数良好；
- inverse 在浮点中稳定；
- 所有方向对任务有用；
- decoder-only 因此必优。

## 五、Linear Attention 的秩界不同

若显式 affinity factorization 为

$$
\tilde A=\Phi_Q\Phi_K^\top,\qquad
\Phi_Q\in\mathbb R^{T_q\times r},\ \Phi_K\in\mathbb R^{T_k\times r},
$$

则

$$
\operatorname{rank}\tilde A\le r.
$$

若 normalized weight 为

$$
A=D^{-1}\tilde A,\qquad D=\operatorname{Diag}(\tilde A\mathbf1),
$$

且所有分母非零，则左乘可逆对角矩阵不改变 rank：

$$
\operatorname{rank}A=\operatorname{rank}\tilde A\le r.
$$

这与 softmax 的“低秩 logit 可变满秩”形成关键对比。[[S-2021-Su-8610-线性Transformer反例]] 用 feature width/低秩提醒：降低 token complexity 可能需要更大 $r$ 才保持效果；具体倍数属于特定实验，不是通用定律。

## 六、输出 Rank 与 Value Bottleneck

$$
O=AV
$$

给出

$$
\operatorname{rank}O\le\min(\operatorname{rank}A,\operatorname{rank}V,T_q,d_v).
$$

即使 A 满秩，若 $V$ 只有一列或所有 value 共线，输出仍低秩。反过来，A 低秩也限制可传出的 token variation。

加入 $W_O$ 不会增加矩阵 rank 超过输入 rank；但 residual $X+OW_O$ 的 rank 可高于 attention branch。分析完整 block 不能只取 A 的谱。

## 七、多头如何影响 Rank

每个 head 输出 $O_r=A_rV_r$，拼接

$$
O_{cat}=[O_1|\cdots|O_h].
$$

有粗界

$$
\operatorname{rank}O_{cat}
\le\min\left(T_q,\sum_r\operatorname{rank}O_r\right).
$$

多个 heads 可在列空间上互补，但若 heads 功能重复或 $W_O$ 再压缩，实际有效维数未必增加。严格 rank 的上界不能替代谱与干预测量。

## 八、严格秩为何常常不够

矩阵只要有极小但非零奇异值，严格秩就计为一维。噪声和浮点使“几乎低秩”仍严格满秩。因此需声明指标：

### 1. 阈值数值秩

$$
r_\varepsilon(A)=\#\{i:\sigma_i>\varepsilon\}
$$

必须写绝对/相对阈值和 dtype。

### 2. Stable rank

$$
r_s(A)=\frac{\|A\|_F^2}{\|A\|_2^2}
=\frac{\sum_i\sigma_i^2}{\sigma_1^2}.
$$

### 3. 谱熵 Effective Rank

令 $p_i=\sigma_i/\sum_j\sigma_j$，

$$
r_{ent}(A)=\exp\left(-\sum_ip_i\log p_i\right).
$$

[[S-2025-Su-10847-矩阵的有效秩]] 强调“有效秩”是一个定义家族。不同公式、归一化和零矩阵约定不可混用；也不能以相关性把 effective rank 变成性能因果指标。

## 九、Pure Attention 的深度退化

[[S-2021-Dong-Pure-Attention-RankCollapse]] 在规定的 pure self-attention 模型、范数与参数条件下证明：没有 skip connection 与 MLP 时，token residual component 可随深度双指数衰减，趋向 rank-one/token uniformity。

精确边界：

- 对象是 pure attention stack；
- 结论依论文假设与度量；
- 含 residual、MLP、normalization、position、causal mask 的完整 Transformer 不在同一结论内；
- 实际模型需逐层测 $H^{(\ell)}$ 的谱和 token 差异。

这个负面定理说明架构组件有结构作用，不是完整 Transformer 必然坍缩的宣判。

## 十、Rank Audit 的最小协议

1. 写清对象：logit、weight、output 还是 hidden state；
2. 写 mask、layer、head、样本、长度与 dtype；
3. 同时报 strict rank（仅小矩阵/容差）、奇异值谱和至少一种明确定义的 effective rank；
4. 报最大/最小奇异值与 condition proxy；
5. 与随机、均匀、identity、causal 基线比较；
6. 关联任务指标时做干预或纵向分析，不只画相关散点；
7. 对 linear attention 记录 feature width $r$；
8. 对多头报告 per-head 与 concatenated/output spectra。

## 十一、图：四本 Rank 账

先看图回答：中栏矩阵为什么严格满秩却仍可能数值病态？右栏两组谱为何严格 rank 都是 6？

![[00-知识库管理/_assets/figures/architecture/fig-attention-rank-effective-rank-v1.svg|900]]

> [!figure] 图 40.4-07　Logit/weight/output rank 与有效秩
> 左栏分开三处矩阵，中栏展示 causal 正对角满秩，右栏比较平坦与集中奇异值谱。来源：依据 rank 恒等式、causal triangular 结构与有效秩定义独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_attention_v1.py]] 生成。

**怎样读图**：先逐箭头标记哪一步是非线性，禁止把上一步的 rank 界直接搬下去；再把中栏的 determinant 事实与右栏的谱集中诊断并列，体会 strict rank 与 usable dimension 的差别。

**图没有证明什么**：它没有证明所有 bidirectional attention 低秩、causal 模型更优，也没有证明某个 effective-rank 公式与性能有因果关系。

## 十二、常见错误

1. 把 $\operatorname{rank}(QK^\top)\le d_k$ 直接写给 softmax A；
2. 把满秩等同可表达任意 stochastic matrix；
3. 把 A 满秩等同 O 满秩；
4. 忽略 V 与 $d_v$ bottleneck；
5. 把不同 effective rank 公式混在一张曲线；
6. 不写阈值/dtype 就报数值秩；
7. 把 causal 满秩事实升级为 decoder-only 优越性定理；
8. 把 pure attention 退化外推含 residual/MLP 的完整 Transformer；
9. 用谱相关性声称性能因果。

## 十三、掌握标准

> [!summary]
> - Logit rank、softmax weight rank、output rank 与 hidden-state rank 是不同对象；
> - row-softmax 可把 rank-1 logit 变成满秩权重；
> - factorized linear attention 的 normalized affinity 在非零分母下仍受 feature rank 限制；
> - strict rank、conditioning、数值秩和有效秩必须分别定义。

能手算最小反例（A/B）、证明 causal/full-rank 与 linear-rank 界（C）、纠正错误论文口号（D），并完成 per-layer/per-head spectral audit（E）。

## 十四、练习与独立详解

- [[习题 - Attention 矩阵的秩、瓶颈与有效秩]]
- [[解答 - Attention 矩阵的秩、瓶颈与有效秩]]

## 参考来源

- [[S-2020-Bhojanapalli-LowRank-Attention]]
- [[S-2021-Dong-Pure-Attention-RankCollapse]]
- [[S-2025-Su-10847-矩阵的有效秩]]
- [[S-2021-Su-8610-线性Transformer反例]]
- [[S-2023-Su-9529-DecoderOnly低秩猜想]]
