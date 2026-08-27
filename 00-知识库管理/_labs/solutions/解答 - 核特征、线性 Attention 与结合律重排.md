---
type: solution
status: draft
area: [architecture, efficient-attention, kernel, linear-attention]
topic: "[[核特征、线性 Attention 与结合律重排]]"
exercise: "[[习题 - 核特征、线性 Attention 与结合律重排]]"
sources: ["[[S-2020-Katharopoulos-Linear-Transformer]]", "[[S-2020-Su-7546-线性Attention]]", "[[S-2021-Su-8338-Performer到线性Attention]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - 核特征、线性 Attention 与结合律重排

## A. 识别与复述

### ARCH-KERNEL-A01
$$o_i=\frac{\sum_{j\in\mathcal N(i)}\kappa(q_i,k_j)v_j}{\sum_{j\in\mathcal N(i)}\kappa(q_i,k_j)}.$$
分子是按相似度加权的信息和；分母把权重归一化并决定尺度；$\mathcal N(i)$ 是 mask/关系图定义的可见集合。三者任一变化都可能改变算子。

### ARCH-KERNEL-A02
$$S=\sum_j\phi(k_j)v_j^\top=\Phi(K)^\top V\in\mathbb R^{r\times d_v},\quad z=\sum_j\phi(k_j)\in\mathbb R^r,$$
$$o_i=\frac{\phi(q_i)^\top S}{\phi(q_i)^\top z}.$$

### ARCH-KERNEL-A03
若目标 kernel 本来就是有限维内积，左右结合只改变乘法顺序，数学函数相同。若把 softmax kernel $e^{q^\top k}$ 替换为 $(\operatorname{ELU}(q)+1)^\top(\operatorname{ELU}(k)+1)$，这是另一个 kernel/模型；线性复杂度来自新 feature factorization，不是 exact softmax。

## B. 手算与建模

### ARCH-KERNEL-B01
kernel weights 为 $2$ 与 $2+2=4$，输出 $(2\cdot3+4\cdot5)/(2+4)=26/6=13/3$。状态 $S=(1,0)3+(1,2)5=(8,10)$，$z=(2,2)$；$\phi(q)^\top S=26$、$\phi(q)^\top z=6$，相同。

### ARCH-KERNEL-B02
materialized kernel matrix 有 $n^2=16{,}777{,}216$ 标量。状态 $S$ 有 $rd_v=8192$，$z$ 有 64；若还保留 features，则各有 $nr=262{,}144$。核心中间矩阵从 $n^2$ 降为 $rd_v$，但输入/output/features 与实现 workspace 另计。

### ARCH-KERNEL-B03
一种具体例：$\phi(k_t)=(1,k_t)$，$v=(1,2,4)$，$k=(0,1,2)$，且 $\phi(q_t)=(1,1)$。则 $(S_1,z_1)=((1,0),(1,0))$，$o_1=1$；$(S_2,z_2)=((3,2),(2,1))$，$o_2=5/3$；$(S_3,z_3)=((7,10),(3,3))$，$o_3=17/6$。每步只加入当前 outer product 与 feature。

## C. 推导与证明

### ARCH-KERNEL-C01
令 $\Phi(Q)\in\mathbb R^{n\times r}$、$\Phi(K)\in\mathbb R^{n\times r}$、$V\in\mathbb R^{n\times d_v}$。矩阵乘法结合律给
$$(\Phi(Q)\Phi(K)^\top)V=\Phi(Q)(\Phi(K)^\top V),$$
两边 shape 均 $n\times d_v$。逐项看是 $\sum_j\sum_a\phi_a(q_i)\phi_a(k_j)v_j$，有限和可交换。

### ARCH-KERNEL-C02
归纳证明。$t=1$ 显然。若 $S_{t-1}=\sum_{j\le t-1}\phi(k_j)v_j^\top$，递推加当前项即 $S_t=\sum_{j\le t}\cdots$；$z_t$ 同理。代入输出式正是显式 causal 求和的分子/分母。

### ARCH-KERNEL-C03
窗口为最近 $w$ 项时，
$$S_t=S_{t-1}+\phi(k_t)v_t^\top-\mathbf1_{t>w}\phi(k_{t-w})v_{t-w}^\top,$$
$z_t$ 同样加新减旧。若 $\mathcal N(i)$ 随 query 任意变化，不同 $i$ 需要不同子集和，单一 $S,z$ 无法同时表示所有子集，除非 mask 另有可递推结构。

## D. 边界、反例与纠错

### ARCH-KERNEL-D01
取 scalar numerator state $S=1$，query feature $\phi(q)=1$，denominator state $z=\epsilon>0$，输出 $1/\epsilon$；将 $z$ 改为 $2\epsilon$，绝对扰动只有 $\epsilon$，输出却减半。复杂度只数操作/状态，不保证 denominator 远离 0。

### ARCH-KERNEL-D02
有限维 factorization 只说明得到某个 kernel。精确 softmax 需对所有允许 $q,k$ 满足 $\phi(q)^\top\phi(k)=e^{q^\top k/\sqrt d}$；任意正 feature map 并不满足。随机 features 也通常只是估计，不是有限样本严格相等。

### ARCH-KERNEL-D03
状态只有固定 $rd_v+r$ 个实数；结合律证明它足以回答当前 feature family 的聚合查询，不证明能恢复历史 token 序列或回答任意未来查询。不同历史可映到同一状态，产生不可区分性；容量结论依 feature/state/model 假设。

## E. AI 迁移

### ARCH-KERNEL-E01
随机生成正 feature Q/K 与 V。Reference 显式构造 $K_{ij}=\phi(q_i)^\top\phi(k_j)$，应用 full 或 causal mask后逐行归一化；implementation 用全局/前缀 $S,z$。比较 numerator、denominator 与 output，覆盖小分母、padding、reset、batch 和 dtype；错误漏分母作为负对照。

### ARCH-KERNEL-E02
先在固定 Q/K 上测 feature inner product 对 softmax kernel 的绝对/相对误差；再测 row-normalized weights/output；然后在同预算训练比较任务质量与多 seed；最后在同硬件 shape 网格测吞吐/延迟。不能用某一层好转替代另外三层证据。

### ARCH-KERNEL-E03
核对 feature 定义、缩放与 positivity；mask 是否有可递推结构；分母 epsilon/稳定归约；causal scan 顺序；accumulation dtype；padding 是否不进状态；每条序列/segment reset；distributed state 合并；训练/推理 feature 一致；reference 与 gradient 测试。
