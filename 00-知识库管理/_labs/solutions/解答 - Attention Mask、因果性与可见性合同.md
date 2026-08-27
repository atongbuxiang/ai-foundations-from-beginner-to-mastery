---
type: solution
status: draft
area: [architecture, attention, masking]
topic: "[[Attention Mask、因果性与可见性合同]]"
exercise: "[[习题 - Attention Mask、因果性与可见性合同]]"
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2024-Su-10347-位置编码与置换对称]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Attention Mask、因果性与可见性合同

## A. 识别与复述

### ARCH-MASK-A01
可见性是 $R\subseteq I_q\times I_k$；第 i 个 query 的可见集合为 $\mathcal V(i)=\{j:(i,j)\in R\}$。矩阵 mask 是 R 在特定索引次序下的编码。

### ARCH-MASK-A02
Key padding 删除无效 key 列，防止任何有效 query 读取 padding；query padding 标记某些输出行/损失无意义；causal mask 逐 pair 禁止未来列。三者可广播/合成，但轴与目的不同。

### ARCH-MASK-A03
Inclusive 允许 $j\le i$，strict 只允许 $j<i$。若输入已右移，inclusive diagonal 往往对应当前已知输入而非目标；若未右移则可能泄漏。必须把 token shift、label 索引与 diagonal 一并写清。

## B. 手算与建模

### ARCH-MASK-B01
$$\begin{bmatrix}1&0&0&0\\1&1&0&0\\1&1&1&0\\1&1&1&1\end{bmatrix}.$$

### ARCH-MASK-B02
后乘 0 得 $(.5,.3,0)$，和 .8；正确有效集归一为 $(.5/.8,.3/.8,0)=(.625,.375,0)$。

### ARCH-MASK-B03
Key-valid mask 可写 $(B,T_k)=(2,5)$：第一行为 $(1,1,1,0,0)$，第二行为 $(1,1,1,1,1)$，广播到 query/head。合成可见条件为 `key_valid[b,j] and j<=i`；还需保证有效 query 行至少含一项，并另屏蔽第一样本的 padding query outputs/loss。

## C. 推导与证明

### ARCH-MASK-C01
可见项加 0，禁止项加 $-\infty$，其指数分别为 $e^{s_{ij}}$ 与 0。分母只剩 $\sum_{l\in\mathcal V(i)}e^{s_{il}}$，故恰等于在有效集归一；要求有效集非空。

### ARCH-MASK-C02
Causal mask 令 $A_{ij}=0$ 对 $j>i$，所以 A 下三角。对角可见且 logit 有限，指数为正、分母正，故 $A_{ii}>0$。三角矩阵 determinant 是对角乘积，非零即满秩。

### ARCH-MASK-C03
输入重排给 $Q'=PQ,K'=PK,V'=PV$，score/mask 合成变 $P(S+M)P^T$。Row-softmax 与同步行列重排相容，权重为 $PAP^T$，输出 $PAP^TPV=PAV$。固定下三角 M 通常不满足 $PMP^T=M$，任意重排会改变先后关系，故只保留关系自同构。

## D. 边界、反例与纠错

### ARCH-MASK-D01
全遮蔽行加 mask 后为 $(-\infty,\ldots,-\infty)$。stable softmax 取 max 为 $-\infty$，相减产生未定义的 $-\infty-(-\infty)$，指数/归一可为 NaN；即使直接指数也得到全 0 后除 0。

### ARCH-MASK-D02
fp16 范围、bf16/fp32 指数下溢与 fused kernel 处理不同；$-10^9$ 可能先转成 $-\infty$，也可能作为有限值参与减最大值。若全行都是同一 finite sentinel，会给均匀分布。必须测试 dtype 与具体 kernel。

### ARCH-MASK-D03
例：把完整目标序列编码成一个双向 encoder feature，再作为 decoder 可见 memory；decoder self-attention 虽 causal，memory 已包含未来答案。其他例有 label 未右移、test answer 进入 retrieval index、缓存索引错位。

## E. AI 迁移

### ARCH-MASK-E01
固定前缀 $x_{\le i}$，创建两个样本仅在 $x_{>i}$ 不同；同一 eval 模式与 cache 状态下比较第 $\le i$ 位 logits/hidden。通过标准为数值容差内完全一致；同时在 $>i$ 位应可不同，避免测试根本未接入输入。

### ARCH-MASK-E02
令 $R(i,j)$ 当且仅当 $|i-j|\le w$ 且满足方向条件，或 j 属全局 token 集 G。为保证非空，可让 $i$ 自身可见或每段含 sentinel/global key。段间隔离时再加 segment(i)=segment(j)，并明确 global tokens 是否跨段。

### ARCH-MASK-E03
测试：(1) 一个极大被禁 logit 检查 True convention；(2) batch/head 不同图案查广播；(3) padding 延长不变性；(4) causal future pulse；(5) 全遮蔽声明；(6) finite/boolean sentinel 跨 dtype/kernel；(7) shifted input/label 的 diagonal gold test；(8) 每个有效行 row-sum=1、禁止权重=0、全 finite。
