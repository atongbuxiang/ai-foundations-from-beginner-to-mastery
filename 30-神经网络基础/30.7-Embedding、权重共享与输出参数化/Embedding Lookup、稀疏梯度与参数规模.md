---
type: derivation
status: draft
area: [neural-networks/embedding-output, embedding, sparse-gradients, parameter-counting]
aliases: [Embedding Lookup Algebra, Sparse Embedding Gradient]
node_id: NN-49
prerequisites: ["[[基与坐标]]", "[[线性层、批量张量与参数计数]]", "[[激活、分支、广播与梯度累加]]", "[[多线性映射、张量与缩并]]"]
related: ["[[Embedding 几何、相似度与各向异性]]", "[[输入—输出权重共享与 Weight Tying]]", "[[Padding、Mask、特殊符号与词表边界]]", "[[Embedding 初始化、缩放、分解与量化接口]]"]
sources: ["[[S-2026-PyTorch-Embedding]]", "[[S-2013-Mikolov-Distributed-Representations]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]"]
exercises: ["[[习题 - Embedding Lookup、稀疏梯度与参数规模]]"]
solutions: ["[[解答 - Embedding Lookup、稀疏梯度与参数规模]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-embedding-lookup-sparse-gradient-v2.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Embedding Lookup、稀疏梯度与参数规模

> [!abstract] 本章主问题
> Embedding lookup 在代数上就是 one-hot 选择矩阵乘以参数表，在实现上却不应物化巨大 one-hot。反向传播是 scatter-add：同一 token 在一个 batch 中出现多次时，其各位置上游梯度必须累加到同一行。lookup 的 VJP 可稀疏，但 optimizer state、weight decay、分布式通信或共享输出层可能使整条训练链重新稠密。

## 一、学习目标

读完本节，你应能：

1. 写出词表、索引、embedding table 与输出张量的 shape；
2. 证明 lookup 等于 one-hot/selection-matrix multiplication；
3. 推导单位置、重复索引和 batch lookup 的权重梯度；
4. 区分数学零梯度、稀疏存储与稀疏 optimizer update；
5. 计算参数数目、权重存储和访问工作量；
6. 解释 `padding_idx`、frequency scaling、`max_norm` 与 weight sharing 的边界；
7. 审计大词表下的通信、optimizer state 与热点 token。

## 二、对象与 shape 合同

设词表大小为 $V$，embedding dimension 为 $d$。参数表

$$
E\in\mathbb R^{V\times d}
$$

的第 $i$ 行

$$
E_{i:}=e_i^\mathsf T
$$

是 token $i$ 的向量。对索引

$$
i\in\{0,1,\ldots,V-1\},
$$

lookup 定义为

$$
\boxed{x=E_{i:}\in\mathbb R^d}.
$$

若整数索引张量

$$
I\in\{0,\ldots,V-1\}^{B\times T},
$$

则输出

$$
X=E[I]\in\mathbb R^{B\times T\times d}.
$$

这里 $B$ 是 batch，$T$ 是序列长度。Embedding 不会把 $T$ 合并到 $d$；它只是给每个离散位置追加一个连续坐标轴。

## 三、单个 lookup 等于 one-hot 乘法

令标准基向量

$$
q_i\in\{0,1\}^V,
\qquad
(q_i)_j=\mathbf 1\{j=i\}.
$$

采用列向量 convention，

$$
E^\mathsf Tq_i
=\sum_{j=0}^{V-1}(q_i)_j e_j
=e_i.
$$

因此

$$
\boxed{
\operatorname{lookup}(E,i)=E^\mathsf Tq_i
}.
$$

这是一条精确代数恒等式，不是近似。实现不物化 $q_i$，因为 one-hot 长度是 $V$，绝大多数分量为零；直接 gather 第 $i$ 行即可。

## 四、序列 lookup 等于选择矩阵乘法

把 $n=BT$ 个位置展平为索引

$$
(i_1,\ldots,i_n).
$$

构造 selection matrix

$$
S=
\begin{bmatrix}
q_{i_1}^\mathsf T\\
\vdots\\
q_{i_n}^\mathsf T
\end{bmatrix}
\in\{0,1\}^{n\times V}.
$$

每行恰有一个 1，于是

$$
\boxed{X_{\mathrm{flat}}=SE\in\mathbb R^{n\times d}}.
$$

真实 gather 只需读 $n$ 行；显式 dense multiplication 却会做/表示与 $nVd$ 相关的工作。代数等价不代表算法复杂度等价。

## 五、单位置反向传播

令

$$
x=E^\mathsf Tq_i,
$$

上游列梯度

$$
g=\nabla_x\mathcal L\in\mathbb R^d.
$$

微分为

$$
dx=dE^\mathsf Tq_i.
$$

于是

$$
d\mathcal L
=g^\mathsf TdE^\mathsf Tq_i
=\operatorname{tr}\!\left((q_ig^\mathsf T)^\mathsf TdE\right),
$$

所以

$$
\boxed{
\nabla_E\mathcal L=q_ig^\mathsf T
}.
$$

这是一个 $V\times d$ 矩阵，但只有第 $i$ 行非零：

$$
(\nabla_E\mathcal L)_{j:}
=\mathbf1\{j=i\}g^\mathsf T.
$$

索引 $i$ 是离散控制流；通常不对整数 ID 求普通导数。

## 六、重复索引必须 scatter-add

对位置 $r=1,\ldots,n$，上游梯度为 $g_r$，索引为 $i_r$。总损失对 $E$ 的梯度是

$$
\boxed{
\nabla_E\mathcal L
=\sum_{r=1}^n q_{i_r}g_r^\mathsf T
}.
$$

第 $j$ 行为

$$
\boxed{
(\nabla_E\mathcal L)_{j:}
=\sum_{r:i_r=j}g_r^\mathsf T
}.
$$

所以 backward 不是“覆盖最后一次出现”，而是 scatter-add。同一 token 出现越多，默认 sum reduction 下梯度贡献通常越多；这既反映数据频率，也可能让高频 token 主导更新。

## 七、完整手算

令

$$
E=
\begin{bmatrix}
1&0\\
0&1\\
2&-1\\
-1&3
\end{bmatrix},
\qquad
I=(2,1,2).
$$

前向输出

$$
X=
\begin{bmatrix}
2&-1\\
0&1\\
2&-1
\end{bmatrix}.
$$

设上游梯度

$$
G=
\begin{bmatrix}
1&2\\
-1&0.5\\
3&-1
\end{bmatrix}.
$$

则

$$
\nabla_E\mathcal L
=
\begin{bmatrix}
0&0\\
-1&0.5\\
1+3&2-1\\
0&0
\end{bmatrix}
=
\boxed{
\begin{bmatrix}
0&0\\
-1&0.5\\
4&1\\
0&0
\end{bmatrix}
}.
$$

token 2 的两个位置贡献相加为 $(4,1)$。

## 八、frequency scaling 改变什么

一种工程选择是按当前 mini-batch 内 token 出现次数 $c_j$ 缩放：

$$
(\widetilde\nabla_E\mathcal L)_{j:}
=\frac1{c_j}\sum_{r:i_r=j}g_r^\mathsf T.
$$

在上例中，token 2 的 row gradient 从 $(4,1)$ 变成

$$
(2,0.5),
$$

token 1 不变。它把“按出现次数求和”改成“对该 batch 内出现位置求平均”，因此修改了优化目标的 stochastic weighting；它不是纯粹的无损加速。

还要声明频率统计域：当前 device microbatch、global data-parallel batch，还是长期 corpus frequency。三者不同。

## 九、三种“稀疏”必须分开

### 9.1 数学 support 稀疏

lookup-only VJP 的未访问行精确为零。

### 9.2 gradient storage 稀疏

框架可以只存 `(row_index, row_value)`，避免物化 $V\times d$ dense gradient。重复 indices 可能在 coalesce 前保留多条记录。

### 9.3 optimizer/update 稀疏

即使 gradient 稀疏，以下操作仍可能触及全部参数：

- dense Adam moments；
- decoupled weight decay；
- global gradient transformation；
- all-reduce dense buffer；
- 参数共享产生的 dense output gradient。

所以

$$
\text{sparse gradient tensor}
\not\Rightarrow
\text{sparse end-to-end training cost}.
$$

## 十、参数规模与存储

Embedding 参数数目是

$$
\boxed{N_{\mathrm{param}}=Vd}.
$$

若

$$
V=50{,}000,
\qquad
d=1024,
$$

则

$$
Vd=51{,}200{,}000
$$

个参数。只看 BF16/FP16 权重、每参数 2 bytes，十进制存储约为

$$
102.4\ \mathrm{MB}.
$$

训练还可能有 FP32 master weights、gradients、optimizer moments、分片 metadata 与通信 buffer；不能用“权重文件 102.4 MB”代表峰值训练显存。

## 十一、访问复杂度与带宽

对 $n=BT$ 个 IDs，lookup 算术/读取规模约为

$$
O(nd),
$$

而不是 $O(nVd)$。但它常是 memory-bound：

- ID 访问不连续，cache locality 较差；
- 高频 token 形成热点；
- 跨 shard lookup 需要 all-to-all 或 parameter-server traffic；
- 去重后通信量与 unique IDs 数相关，而非只与 $n$ 相关。

报告系统成本时应同时给 tokens、unique IDs、row bytes、cache hit、通信 bytes 与 wall time。

## 十二、padding、`max_norm` 与状态修改

`padding_idx` 常让指定行不从 lookup backward 获得梯度，但这不自动意味着：

- 该行永远为零；
- weight decay/手工赋值不会改它；
- tied output use 不会给它 dense gradient；
- 所有框架版本语义相同。

`max_norm` 则可能在 forward 时对被访问行原位重归一化。它不是普通无状态读取；若同一 weight 在 lookup 前还参与另一条可微计算，必须审计操作顺序、clone 与 autograd version counter。

特殊符号和 mask 的完整合同留到[[Padding、Mask、特殊符号与词表边界]]。

## 十三、Weight Tying 会改变稀疏性

若同一个 $E$ 还用作输出矩阵，

$$
z=Eh+b,
$$

则输出 softmax 的梯度通常对所有 $V$ 行非零：

$$
\nabla_E^{\mathrm{out}}\mathcal L
=(p-y)h^\mathsf T.
$$

共享参数的总梯度是

$$
\nabla_E
=\nabla_E^{\mathrm{lookup}}
+\nabla_E^{\mathrm{out}}.
$$

因此 input lookup 的 row-sparse 梯度不再保证共享 $E$ 的总梯度稀疏。这是[[输入—输出权重共享与 Weight Tying]]的核心接缝。

## 十四、常见误区

1. **“Embedding 不是矩阵乘法”**：代数上是，算法上用 gather；
2. **“重复 token 只更新一次”**：同一行更新一次，但值是所有位置贡献之和/约定平均；
3. **“未访问行永远不变”**：optimizer、decay、共享使用可改变它；
4. **“sparse=True 一定更快”**：optimizer、硬件、unique ratio 与通信决定；
5. **“词表 ID 有大小关系”**：ID 只是标签，重新编号并同步重排 $E$ 不改变函数；
6. **“参数数目就是推理激活显存”**：权重、KV/activation、临时 logits 是不同账本。

## 十五、图：选择、散射与系统稀疏性

先看图回答：为什么 indices $(2,1,2)$ 的前向会重复读同一行？反向为何得到 $\nabla E_2=(4,1)$？哪一步会让 lookup-only 的稀疏性消失？

![[00-知识库管理/_assets/figures/neural-networks/fig-embedding-lookup-sparse-gradient-v2.svg|900]]

> [!figure] 图 30.7-01　Embedding 的 selection-matrix 等价、scatter-add 与成本边界
> 左栏把 gather 展开为 $X=SE$；中栏显示重复索引的 row-gradient 累加；右栏区分参数规模、稀疏 gradient storage 与共享输出产生的稠密梯度。来源：依据 PyTorch 当前 Embedding 合同与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_embedding_output_foundations_v2.py]] 确定性生成。

**怎样读图**：先沿前向 ID 找被选择行，再把每个位置的上游向量按 ID 散射回表；最后从 gradient tensor 继续追踪 optimizer、decay、共享和通信。

**图没有证明什么**：图不证明 sparse gradient 在任意框架/硬件上更快，也不证明未访问行在完整训练步骤中一定不变。

## 十六、最小验收

1. 从标准基证明 lookup 等价；
2. 写出 $[B,T]\to[B,T,d]$ shape；
3. 推导单位置与重复索引的 VJP；
4. 复算 $I=(2,1,2)$ 的完整例子；
5. 区分三种 sparse；
6. 计算 $V=50{,}000,d=1024$ 的参数/权重存储；
7. 审计 frequency scaling、padding、max norm、weight tying 和 distributed lookup。

> [!summary]
> Embedding 是“参数化基向量表 + 离散选择算子”。前向 gather 避免 one-hot 物化，反向 scatter-add 保存重复 token 的全部贡献。真正的大词表工程难点不在这条等价式本身，而在参数/状态存储、稀疏 optimizer、通信和共享输出对稀疏性的破坏。

- [[Embedding、权重共享与输出参数化 MOC]]
- [[习题 - Embedding Lookup、稀疏梯度与参数规模]]
- [[解答 - Embedding Lookup、稀疏梯度与参数规模]]
