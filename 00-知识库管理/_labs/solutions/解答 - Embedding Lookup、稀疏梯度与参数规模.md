---
type: solution
status: draft
area: [neural-networks/embedding-output, embedding, sparse-gradients]
topic: "[[Embedding Lookup、稀疏梯度与参数规模]]"
exercise: "[[习题 - Embedding Lookup、稀疏梯度与参数规模]]"
sources: ["[[S-2026-PyTorch-Embedding]]", "[[S-2013-Mikolov-Distributed-Representations]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Embedding Lookup、稀疏梯度与参数规模

## A

### NN-ELS-A01

参数表为 $E\in\mathbb R^{V\times d}$；单个 token 的输出是 $x=E_{i:}\in\mathbb R^d$；$I\in\{0,\ldots,V-1\}^{B\times T}$ 的批量输出是 $X\in\mathbb R^{B\times T\times d}$。每个离散位置独立选择一行，因此 $B,T$ 仍标记样本和位置，新增的末轴 $d$ 才是连续表示坐标。把 $T$ 合并进 $d$ 会丢掉“一位置一向量”的张量合同。

### NN-ELS-A02

数学零梯度只说本次 loss 的导数中该行系数为零。稀疏存储是把非零行及其索引编码为 sparse tensor；同一个数学梯度也可存成 dense tensor。optimizer step 还可能包含 momentum、Adam moment、weight decay、参数约束或跨设备同步：即使当前 data gradient 为零，旧动量或 decoupled decay 仍可改变参数。因此三者依次属于导数、表示和状态转移三本账。

### NN-ELS-A03

- `padding_idx`：该索引可返回固定 padding row，并阻止标准 lookup backward 对它累积梯度；它同时涉及前向语义与反向合同。
- `scale_grad_by_freq`：把一个 mini-batch 内某 token 行的累计梯度除以其出现次数，改变反向尺度。
- `max_norm`：超过阈值的被访问行在 forward 中被重整化，因而会原地改变参数值；它不是单纯的 backward clipping。
- `sparse=True`：请求把 weight gradient 表示为稀疏行更新；它不自动改变前向数学函数，也不保证 optimizer、decay 和通信都稀疏。

### NN-ELS-B01

三个索引依次为 $2,1,2$，所以

$$
S=
\begin{bmatrix}
0&0&1&0\\
0&1&0&0\\
0&0&1&0
\end{bmatrix}.
$$

直接相乘得到

$$
SE=
\begin{bmatrix}
2&-1\\
0&1\\
2&-1
\end{bmatrix},
$$

恰好等于逐位置 gather。

### NN-ELS-B02

row 2 收到第一、第三个位置之和，row 1 收到第二个位置：

$$
\nabla_E\mathcal L=
\begin{bmatrix}
0&0\\
-1&0.5\\
1+3&2-1\\
0&0
\end{bmatrix}
=
\begin{bmatrix}
0&0\\
-1&0.5\\
4&1\\
0&0
\end{bmatrix}.
$$

token 2 出现两次，按频次平均后该行为 $(2,0.5)$；token 1 只出现一次，仍为 $(-1,0.5)$。未访问行仍为零。

### NN-ELS-B03

$$
Vd=50{,}000\times1024=51{,}200{,}000.
$$

只计权重本体，FP32 为 $51.2\times4=204.8$ MB，FP16/BF16 为 $51.2\times2=102.4$ MB（十进制 MB）。若训练参数本体为 2 字节，另有 4 字节 FP32 master weight 和两个各 4 字节 moment，则每参数 $2+4+8=14$ 字节，共 $716.8$ MB。这里尚未计梯度、临时 buffer、对齐、分片副本和通信 buffer。

## C

### NN-ELS-C01

标准基 $q_i$ 只有第 $i$ 项为 1，故

$$
E^\mathsf Tq_i=\sum_{j=0}^{V-1}(q_i)_j e_j=e_i.
$$

若上游列梯度为 $g$，则 $dx=dE^\mathsf Tq_i$，从而

$$
d\mathcal L
=g^\mathsf TdE^\mathsf Tq_i
=\operatorname{tr}\!\left[(q_i g^\mathsf T)^\mathsf T dE\right].
$$

按 Frobenius 配对识别系数：

$$
\boxed{\nabla_E\mathcal L=q_i g^\mathsf T}.
$$

该 outer product 只有第 $i$ 行非零。

### NN-ELS-C02

前向是 $X=SE$，上游梯度为 $G=\nabla_X\mathcal L$。微分

$$
d\mathcal L=\langle G,SdE\rangle_F
=\langle S^\mathsf TG,dE\rangle_F,
$$

所以

$$
\boxed{\nabla_E\mathcal L=S^\mathsf TG}.
$$

$S^\mathsf T$ 的第 $j$ 行会选出所有满足 $i_r=j$ 的 $G_{r:}$ 并相加，即

$$
(\nabla_E\mathcal L)_{j:}=\sum_{r:i_r=j}G_{r:}.
$$

若 backward 采用 overwrite，重复 token 只保留最后一次贡献，就不再实现线性映射 $S$ 的伴随。

### NN-ELS-C03

若 token-sum loss 为 $L_\Sigma=\sum_{r=1}^n\ell_r$，则 token-mean 为 $L_\mu=L_\Sigma/n$，因此每一行都统一缩放：

$$
\nabla_E L_\mu=\frac1n\sum_r q_{i_r}g_r^\mathsf T.
$$

frequency scaling 则对第 $j$ 行除以本 batch 中该 token 的次数 $c_j$：

$$
(\nabla_E L)_{j:}=\frac1{c_j}\sum_{r:i_r=j}g_r^\mathsf T.
$$

前者给每个位置相同全局权重，后者近似让每种已出现 token 的行获得相同总权重；当频次不等时二者明显不同，若再叠加 mean 还会产生额外 $1/n$。

## D

### NN-ELS-D01

结论不成立。`sparse=True` 最多让 lookup data gradient 以稀疏行表示；普通 AdamW 通常不接受该稀疏梯度合同，支持稀疏梯度的 optimizer 集合受框架版本限制。对全表执行 dense decoupled weight decay 仍触碰 $Vd$ 参数；dense all-reduce 仍通信完整梯度；Adam 的 dense moments 也可能保持全表状态。只有 gather、gradient encoding、optimizer state/update、decay 和 collective 全部按 touched rows 设计并测量，端到端成本才可能按访问行缩放。

### NN-ELS-D02

`max_norm` 可在 embedding forward 中原地改写被访问的 weight rows。若此前已经用同一 Parameter 计算了另一个需要原值来求梯度的量，autograd 的 version counter 会发现原地修改，或更糟的是自定义系统静默使用前后不一致的值。安全做法是先完成所需的可微变换并在 embedding 前使用明确的 clone，或把重整化移到 optimizer step 后的 `no_grad` 投影阶段；必须声明 checkpoint 中保存投影前还是投影后的状态。

### NN-ELS-D03

不能。lookup 贡献只有被访问行非零，但输出 softmax 的共享梯度通常是 $(p-y)h^\mathsf T$；只要 $p_j>0$ 且 $h\ne0$，几乎每个词表行都有非零贡献，总和因而稠密。至少应分别监控 input/output 两支的 nonzero-row fraction、各行梯度范数/两支 cosine，以及全量输出带来的通信与 optimizer update 字节数。不要用 input branch 的 sparsity 推断共享 Parameter 的总 sparsity。

## E

### NN-ELS-E01

取 B01 的 $E$ 与索引 $(2,1,2,0)$，把最后一个位置设为 `padding_idx=0`。定义

$$
L=\sum_r g_r^\mathsf T E_{i_r:}
$$

并选 $g_1=(1,2),g_2=(-1,0.5),g_3=(3,-1),g_4=(7,7)$。无 frequency scaling 时预期 row 2 为 $(4,1)$、row 1 为 $(-1,0.5)$、padding row 0 为零；开启 scaling 后 row 2 为 $(2,0.5)$。断言应同时检查 exact row values、稀疏索引集合不含 0、重复索引已合并或 coalesce 后相等；将第三个上游梯度改为零可抓住“按最后一次覆盖”的 silent bug。

### NN-ELS-E02

固定数据顺序、tokenizer、模型函数、有效 batch、optimizer 目标与训练 token 数，比较：dense baseline；稀疏 row optimizer；按 vocabulary range/hash 分片的方案。每组调参预算一致，并报告 held-out loss/稀有词 loss、峰值 device/host memory、step time 与吞吐、每步发送字节与 collective 等待、每 shard 的访问频率和 p99 热点负载。故障恢复要验证 optimizer state、padding row、分片映射和 RNG 恢复后下一步更新逐元素一致；否则“更快”可能来自丢状态或不同训练语义。

### NN-ELS-E03

lookup 的算术强度低不等于系统成本低。参数量为 $Vd$；每 token 要从内存读 $d$ 个值，容易受带宽而非 FLOP 限制；Adam 类状态可把本体放大到多份；checkpoint、加载和容错时间随参数量增长；分片系统还要路由 ID、处理热点并交换更新。若同一表用作输出 head，每个位置还要形成并归一化 $V$ 个 logits，梯度通常稠密。增大 $V,d$ 因而同时推高容量、带宽、状态、存储、通信和输出计算。
