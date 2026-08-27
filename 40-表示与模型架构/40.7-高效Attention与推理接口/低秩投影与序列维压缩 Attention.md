---
type: concept
status: draft
area: [architecture, efficient-attention, low-rank, sequence-compression]
aliases: [Linformer, Low-Rank Attention, Sequence Projection Attention]
node_id: ARCH-51
prerequisites: ["[[奇异值分解]]", "[[定理 - Eckart–Young–Mirsky]]", "[[Attention 矩阵的秩、瓶颈与有效秩]]"]
related: ["[[高效 Attention 与推理接口 MOC]]", "[[核特征、线性 Attention 与结合律重排]]", "[[MLA、潜变量缓存与推理成本证据]]", "[[随机化低秩近似与随机 SVD]]"]
sources: ["[[S-2020-Wang-Linformer]]", "[[S-2025-Su-10847-矩阵的有效秩]]", "[[S-2021-Su-8610-线性Transformer反例]]", "[[S-2022-Su-8934-FLASH-GLU-GAU]]"]
exercises: ["[[习题 - 低秩投影与序列维压缩 Attention]]"]
solutions: ["[[解答 - 低秩投影与序列维压缩 Attention]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-low-rank-sequence-compression-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# 低秩投影与序列维压缩 Attention

> [!abstract] 核心问题
> “Attention 低秩”至少可能指 logits、softmax weights、output 或 K/V 序列。Linformer 类方法真正做的是沿 sequence axis 把 $n$ 个 K/V 压成 $k$ 个槽位。必须明确压哪条轴、用什么 norm、误差怎样穿过 softmax，以及新长度怎样处理投影参数。

## 一、先区分四个矩阵对象

单头中：

$$
Q,K\in\mathbb R^{n\times d_h},\quad
V\in\mathbb R^{n\times d_v},
$$

$$
Z=QK^\top/\sqrt{d_h}\in\mathbb R^{n\times n},
\quad A=\operatorname{softmax}_{row}(Z),
\quad O=AV.
$$

这里：

- $\operatorname{rank}(Z)\le d_h$ 是精确线性代数事实；
- softmax 是逐元素非线性再归一化，$A$ 可为满秩；
- $O$ 的 rank 受 $A,V,d_v$ 共同限制；
- “effective rank 小”依定义、样本和阈值，不是唯一对象。

所以从 logits rank 小，不能直接推出 attention matrix 可用同一个 $k$ 无损压缩。

## 二、Linformer 型序列轴投影

取

$$
E,F\in\mathbb R^{k\times n},\qquad k\ll n,
$$

定义

$$
K'=EK\in\mathbb R^{k\times d_h},\qquad
V'=FV\in\mathbb R^{k\times d_v}.
$$

随后计算

$$
O'=\operatorname{softmax}
\left(\frac{QK'^\top}{\sqrt{d_h}}\right)V'.
$$

Score shape 从 $n\times n$ 变为 $n\times k$，主 pairwise 复杂度从 $O(n^2d_h)$ 变为 $O(nkd_h)$；但还要计入 $EK,FV$ 的投影成本。若 $E,F$ 是 dense $k\times n$，每层每头投影也需要 $O(nkd)$。

“线性于 $n$”依赖 $k$ 固定或远慢于 $n$ 增长。若为维持质量让 $k\propto n$，渐近优势消失。

## 三、这是压缩，不是简单换结合顺序

Kernel linear attention 利用可分解相似度做精确结合律重排；Linformer 插入了 $E,F$，改变 K/V 序列本身。除非 $E,F$ 在目标子空间上无损，否则它是模型近似/新架构。

同样，MLA 把每个 token 的 KV channel 压到 latent，压的是 feature axis；Linformer 把 sequence length 压到 $k$，压的是 token axis。两者都叫低秩，却有不同缓存和因果语义。

## 四、从 SVD 到误差传播

若只考虑近似 $K\approx\hat K$，则 logits 误差

$$
\Delta Z=\frac{Q(K-\hat K)^\top}{\sqrt{d_h}},
$$

满足

$$
\|\Delta Z\|_F
\le \frac{\|Q\|_2\|K-\hat K\|_F}{\sqrt{d_h}}.
$$

Eckart–Young–Mirsky 告诉我们：对一个固定矩阵、指定 unitary-invariant norm，截断 SVD 给最佳 rank-$k$ 近似。但学习型 $E$ 不是逐样本 SVD；它要在数据分布和长度间共享。

下一步还有 softmax。对单行 $p=\operatorname{softmax}(z)$，Jacobian 为

$$
J=\operatorname{diag}(p)-pp^\top.
$$

因此 logits 的小扰动通过局部 Jacobian 传播；当 attention 很尖锐、margin 接近翻转或多项竞争时，输出行为可比平均谱误差更敏感。最终

$$
O-\hat O=(A-\hat A)V+\hat A(V-\hat V),
$$

必须同时登记 attention-weight error 与 value-compression error。

## 五、为什么平均低秩不等于逐样本安全

常见失败包括：

- 平均 singular tail 小，但关键 rare token 位于尾部方向；
- 某层/某 head 低秩，另一层不是；
- 短序列有效 rank 小，长序列增长；
- logits 低秩，softmax 后 effective rank 改变；
- Frobenius error 小，却在单个关键 query 上产生大相对误差。

因此应报告 layer×head×length×sample 的谱分布和任务干预，而不只是一条平均曲线。

## 六、Causal 与未来泄漏

若 $E$ 把整段 K 混合成 $k$ 个槽，再让早期 query 读取这些槽，槽中可能含未来 token。Bidirectional encoder 没有这个问题；causal decoder 必须使用 prefix-compatible projection、分块状态、递推更新或显式因果结构。

这是非常重要的边界：一个对 full sequence 数学形状正确的 $E\in\mathbb R^{k\times n}$，不一定是合法自回归算子。

## 七、长度外推与参数合同

若 $E,F$ 的列数等于训练最大长度 $n_0$，测试到 $n_1>n_0$ 时需要：

- 插值/扩展投影；
- 使用长度无关的结构化投影；
- 分块重复/共享；
- 或重新训练。

每种选择改变 sequence coordinates 和近似子空间。能够 resize 参数不等于保持训练时低秩性质，更不等于远程任务成功。

## 八、科学空间的 rank 与 crossover 补充

[[S-2025-Su-10847-矩阵的有效秩]] 提醒不同 effective-rank 定义不可混写。用 stable rank、entropy rank 或阈值 rank 支持低秩假设时，应给公式、对象和阈值。

[[S-2021-Su-8610-线性Transformer反例]] 则提醒：即使把 pairwise 项从 $n^2$ 降为 $nk$，额外投影、FFN 和 kernel 常数仍可能让短长度无收益。[[S-2022-Su-8934-FLASH-GLU-GAU]] 对 causal linear/low-rank 方案的训练并行与 crossover 也提供工程问题入口，但其具体阈值不是通用定理。

## 九、正式图：低秩假设怎样变成可审计合同

这张图回答什么问题？为什么“谱尾很小”只是从序列压缩到最终任务误差之间的第一道门？

![[00-知识库管理/_assets/figures/architecture/fig-low-rank-sequence-compression-v1.svg|900]]

> [!figure] 图 1｜序列轴压缩、谱尾与实现/外推合同。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_efficient_attention_v1.py]] 生成；谱柱为概念示意，不来自某个模型的实测 singular values。

**怎样读图**：A 先确认 $E,F$ 乘在 sequence axis，score 从 $n\times n$ 变为 $n\times k$；B 把保留谱与尾部误差连接到 logits—softmax—output 传播链；C 逐项检查 $k$ 是否增长、投影是否共享、causal 是否泄漏、新长度怎样处理以及投影成本是否计入。

**图没有证明什么**：示意谱下降没有证明真实 attention 在所有层、样本和长度都低秩，也没有证明 rank-$k$ logits 近似会保持最终预测；更没有证明 learned projection 等于逐样本最优 SVD，或在 causal decoder 中天然合法。

## 十、公平实验

至少比较 dense、相同参数的 low-rank、随机/固定/学习投影；控制模型、训练 tokens、最大长度和调参预算。报告：

- $k$ sweep 与质量—成本 Pareto；
- layer/head/length 谱；
- attention output 相对误差与最终任务；
- target-position/rare retrieval；
- causal leakage tests；
- projection time、peak memory 与 end-to-end wall-clock。

## 十一、证据边界

- Shape、rank 上界和 norm inequality：`I`；
- 截断 SVD 最优性：带指定矩阵/norm 的 `T`；
- learned $E,F$ 的质量与加速：`E`；
- “语言 attention 天然低秩”：必须限定对象/分布/长度，通常是 `H/E`；
- 可压缩性不是可辨识性或解释性结论。

## 十二、学习出口

应能从 $E,F$ 的 shape 重建 Linformer 型前向与成本，给出一条 logits 误差界，指出 causal/长度合同，并解释它与 kernel reordering、MLA feature compression 的根本差别。

