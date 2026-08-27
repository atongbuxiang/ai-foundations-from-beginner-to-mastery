---
type: solution
status: draft
area: [architecture, transformer, encoder, bidirectional]
topic: "[[Transformer Encoder 与双向表示]]"
exercise: "[[习题 - Transformer Encoder 与双向表示]]"
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2019-Devlin-BERT]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Transformer Encoder 与双向表示

## A. 识别与复述

### ARCH-ENC-A01
Token IDs 为 $(B,T)$；lookup、position/type 相加后 $X_0\in\mathbb R^{B\times T\times d}$；每个 block 都输出 $(B,T,d)$，最终 $H=X_L$ 仍是 $(B,T,d)$。Attention 对 key 轴加权后为每个 query 留下一行，FFN 也逐行返回，因此 encoder 不自动 pooling。

### ARCH-ENC-A02
双向指同一有效序列内，第 $i$ 个 query 通常允许读取任意有效 key $j$，不强制 $j\le i$。它不表示可以读取数据集中的未来样本，也不表示完成因果推断；也不表示无需 padding mask 或 position。

### ARCH-ENC-A03
Encoder 是计算骨架和可见关系；MLM 是只在选定 targets 上恢复 token 的目标；corruption recipe 决定怎样选择、替换或保留被遮盖输入；downstream head 决定 token/pool 表示怎样映到任务输出。这四者可以分别改变。

## B. 手算与建模

### ARCH-ENC-B01
对三个有效 query，key columns 的 relation 是
$$
\begin{bmatrix}
1&1&1&0&0\\
1&1&1&0&0\\
1&1&1&0&0
\end{bmatrix}.
$$
后两条 padding query rows可继续计算但必须在输出/loss/pooling 排除，或额外把这些 rows 清零；只屏蔽 key columns 不会自动清零 query rows。

### ARCH-ENC-B02
Masked mean 只平均三个有效 states：
$$
\frac{(1,0)+(3,2)+(2,4)}3=(2,2).
$$
两个 padding states 无论为何值都不应进入分母或分子。

### ARCH-ENC-B03
Token embedding 为 $Vd=30000\cdot768=23{,}040{,}000$。Learned absolute positions 为 $Td=512\cdot768=393{,}216$。若有 type embedding、bias 或输出 head，要另计。

## C. 推导与证明

### ARCH-ENC-C01
令置换矩阵 $P$ 作用在 token 轴。共享线性投影满足 $Q(PX)=P Q(X)$，K/V 同理；score 变为 $P(QK^\top)P^\top$。Row-softmax 与同步置换 mask 满足
$$
\operatorname{softmax}(PSP^\top)=P\operatorname{softmax}(S)P^\top.
$$
故 attention 输出为 $PAV$。逐行 FFN、LayerNorm 与 residual 也与 $P$ 对易，逐层归纳得 $F(PX)=PF(X)$。

### ARCH-ENC-C02
Padding query row 仍可对有效 key columns 归一化，得到其加权和，所以一般非零。若 pooling 写成
$$
z=\frac{\sum_i m_iH_i}{\sum_i m_i},
$$
其中有效行 $m_i=1$、padding 行为 0，且有效行输出对 padding 内容/长度不变，则 pooled output 不受 padding rows 影响。

### ARCH-ENC-C03
标准 block 主要 MAC 为 Q/K/V/O 投影 $4BTd^2$、QK/AV $2BT^2d$、普通 FFN $2BTdd_{ff}$。双向 relation 允许几乎全部 $T^2$ pairs；dense kernel 通常仍构造/处理整张 score。Mask 语义本身不等于稀疏算法。

## D. 边界、反例与纠错

### ARCH-ENC-D01
一个有效 state 为 2。Pad 到长度 2 时若 padding state 为 0，错误 mean 为 1；pad 到长度 4 时错误 mean 为 0.5。正确 masked mean 始终为 2。即使 padding embedding 初始为 0，经 attention/FFN 后也未必为 0。

### ARCH-ENC-D02
双向只描述已提供样本内部 token 的 relation。例如离线句子分类时整句本来就是观测输入；读取右侧词不是穿越时间。现实因果需要干预、混杂控制和因果 estimand，不能由 attention direction 得到。

### ARCH-ENC-D03
序列 $(a,b)$ 与 $(b,a)$ 在无 position 的 encoder 下只导致输出 rows 同步置换；若随后 mean pooling，二者得到同一向量。因此需要 position/structure 或非对称 outlet 才能一般地区分顺序。

## E. AI 迁移

### ARCH-ENC-E01
Padding：同一有效序列 pad 到不同长度，比较有效 rows 与 logits；改变 padding token values 也应不变。Position：交换两个真实 tokens 时，若 position IDs 固定，输出应反映顺序变化；若连 position 一起同步置换，检验等变。Pooling：用人工 states 核对 mask 分子/分母、全 padding 行的报错/约定及梯度只流向有效行。

### ARCH-ENC-E02
固定 backbone、预训练 checkpoint、数据 split、训练 steps、head 参数预算与调参预算。分别接 CLS、masked mean、attention pooling；对 attention pooling补足额外参数，并可给 CLS/mean 匹配容量 head。多 seed 报质量、校准、长度分层、padding 鲁棒、吞吐和表示各向异性；不能只挑单一任务最佳值。

### ARCH-ENC-E03
记录 encoder 接线/规模、MLM/corruption 细节、训练数据与 token、优化预算、head 和 fine-tuning protocol。用消融或匹配预算 comparator 分别检验 objective、数据量、架构。原论文结果标 E；“双向结构导致全部提升”只能在相应控制下支持，不能由总分反推机制。
