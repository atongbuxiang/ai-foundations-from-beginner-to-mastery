---
type: solution
status: draft
area: [architecture, attention, content-addressing]
topic: "[[内容寻址、Query、Key 与 Value]]"
exercise: "[[习题 - 内容寻址、Query、Key 与 Value]]"
sources: ["[[S-2015-Bahdanau-Attention]]", "[[S-2017-Vaswani-Transformer复杂度]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - 内容寻址、Query、Key 与 Value

## A. 识别与复述

### ARCH-QKV-A01
Query 表示当前读取需求；key 是候选项用于匹配的地址描述；value 是选中候选后返回的内容。Q 与 K 必须共享比较维度 $d_k$；K 与 V 必须共享候选数 $T_k$，但 value 宽可为另一个 $d_v$。

### ARCH-QKV-A02
$S=QK^T$ 与归一后的 $A$ 都是 $T_q\times T_k$；$O=AV$ 是 $T_q\times d_v$。内维检查为 $(T_q\times d_k)(d_k\times T_k)$ 与 $(T_q\times T_k)(T_k\times d_v)$。

### ARCH-QKV-A03
同源只说 $Q=XW_Q,K=XW_K,V=XW_V$ 都由 X 产生。只要三个投影不同，数值、维度和角色就不同；即使投影初始化偶然相同，训练也没有要求保持相同。

## B. 手算与建模

### ARCH-QKV-B01
$$o=.6(1,0)+.3(0,2)+.1(-1,1)=(.6-.1,.6+.1)=(.5,.7).$$

### ARCH-QKV-B02
$S=QK^T=I_2$。每行 softmax 权重为 $(e/(e+1),1/(e+1))$ 及其交换。因此
$$
O=\frac1{e+1}\begin{bmatrix}e&1\\1&e\end{bmatrix}
\begin{bmatrix}2&0\\0&4\end{bmatrix}
=\frac1{e+1}\begin{bmatrix}2e&4\\2&4e\end{bmatrix}.
$$

### ARCH-QKV-B03
$Q:(5,8)$，$K:(12,8)$，$V:(12,16)$，$A:(5,12)$，$O:(5,16)$。输出行数 5 来自 queries；候选轴 12 在 AV 中收缩。

## C. 推导与证明

### ARCH-QKV-C01
凸包定义正是所有 $\sum_j a_jv_j$，其中 $a_j\ge0$ 且 $\sum a_j=1$ 的集合。Attention 输出满足这些系数条件，故在凸包内；若允许负权或行和不为 1，则该结论不再保证。

### ARCH-QKV-C02
设置换矩阵 P 同步重排 $K'=PK,V'=PV$。score 变为 $qK'^T=qK^TP^T$，softmax 只重排列，故 $a'=aP^T$。输出 $a'V'=aP^TPV=aV$。

### ARCH-QKV-C03
唯一最大值不变的开放区域内，argmax 输出索引局部常数，对 scores 的普通导数为 0；跨越两个分数相等的决策边界时输出跳变，导数不存在。Softmax 对有限 logits 光滑，各候选一般都有梯度，但温度很低时会近似饱和。

## D. 边界、反例与纠错

### ARCH-QKV-D01
Key 只决定地址匹配，value 可独立投影。令 $k_1=k_2$，但 $v_1=(1,0),v_2=(-100,7)$；key 完全相同却 value 相差很大。因此除非模型/数据另加耦合假设，地址相似不推出内容相似。

### ARCH-QKV-D02
令 $v_1=v_2=v$。权重 $(1,0)$ 与 $(0,1)$ 都输出 v；更一般地，只要 value 矩阵有非平凡左零空间，存在 $a\ne b$ 但 $(a-b)V=0$。这也是仅凭权重推断功能贡献的障碍。

### ARCH-QKV-D03
取所有 values 都等于 0，则无论某 token 可见，输出都为 0，无法复制原 token。即使 values 有信息，softmax 权重可能平均、投影可能非单射、有限 head width 也可能丢失身份；可访问只说明有计算边。

## E. AI 迁移

### ARCH-QKV-E01
Query：decoder 当前 tokens，经 $W_Q$，shape $(B,T_{text},d_k)$；K/V：image patches 经各自投影，shape $(B,T_{patch},d_k/d_v)$；mask 屏蔽无效 patches，decoder 自回归性由其 self-attention 另管。记录 patch 顺序/2D position、image padding、跨模态 normalization；输出为 $(B,T_{text},d_v)$。

### ARCH-QKV-E02
固定 q,k,v 先保存权重/输出。只改 $v_2$：权重应逐元素不变，输出按 $a_2\Delta v_2$ 变化。恢复 v，只改 $k_2$：权重通常变化且所有项重新归一，输出随新权重变化。用确定性小矩阵和严格容差验证。

### ARCH-QKV-E03
若问题长 $T_q$、检索后 token 总长 $T_k$，则 Q $(B,T_q,d_k)$，K/V $(B,T_k,d_k/d_v)$，A $(B,T_q,T_k)$。保留每个 token 的 chunk/document ID、rank 与 source timestamp；屏蔽 padding/无权限文档。防止检索器或索引使用测试答案，记录 chunk duplication、截断和引用是否可追溯；“看到文档”不等于生成忠实引用。
