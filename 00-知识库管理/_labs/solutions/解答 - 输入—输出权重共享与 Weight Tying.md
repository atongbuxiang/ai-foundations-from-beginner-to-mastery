---
type: solution
status: draft
area: [neural-networks/embedding-output, weight-tying, shared-parameters]
topic: "[[输入—输出权重共享与 Weight Tying]]"
exercise: "[[习题 - 输入—输出权重共享与 Weight Tying]]"
sources: ["[[S-2017-Press-Wolf-Weight-Tying]]", "[[S-2017-Inan-Khosravi-Socher-Weight-Tying]]", "[[S-2023-Su-9698-Output-Embedding]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - 输入—输出权重共享与 Weight Tying

## A

### NN-WTY-A01

输入表 $E\in\mathbb R^{V_{\rm in}\times d_e}$，lookup 输出在 $\mathbb R^{d_e}$；hidden $h\in\mathbb R^{d_h}$；untied 输出矩阵 $U\in\mathbb R^{V_{\rm out}\times d_h}$，$z=Uh+b\in\mathbb R^{V_{\rm out}}$。直接令 $U=E$ 需要 $V_{\rm in}=V_{\rm out}=V$、$d_e=d_h=d$，且每个 row index 在输入和输出两侧指同一 token 语义。shape 相等但行映射不同仍不能直接共享。

### NN-WTY-A02

只有两处模块引用同一个 Parameter object，autograd 才把两条路径的 VJP 加到一个 `.grad`，optimizer 也只维护一份 state。初始化复制只保证 step 0 数值相同，之后两参数独立更新。每步后同步是带约束的双参数算法：同步前已有两份梯度和 optimizer state，更新顺序及平均规则都会改变轨迹，不能称为普通 tying。

### NN-WTY-A03

参数上，tying 删除一张 $V\times d$ 词表矩阵；函数上，它强制输入坐标与输出类 prototype 使用同一行向量，排除了任意独立的 $(E,U)$；优化上，同一行同时收到 lookup 和全词表 classifier 的梯度，两任务可能协同或冲突。checkpoint 变小只是这些结构变化的结果，并非完整定义。

## B

### NN-WTY-B01

保留输出 bias $b\in\mathbb R^V$：

$$
N_{\rm untied}=2Vd+V
=102{,}400{,}000+50{,}000
=102{,}450{,}000,
$$

$$
N_{\rm tied}=Vd+V
=51{,}200{,}000+50{,}000
=51{,}250{,}000.
$$

节省 $Vd=51{,}200{,}000$，占原计数约 $49.98\%$。不是严格 50%，因为 bias 没有被删除；模型其他参数也会进一步降低全模型节省比例。

### NN-WTY-B02

忽略两边共同的输出 bias，untied 需要

$$
Vd+Vd_h=50{,}000(512+1024)=76{,}800{,}000.
$$

projected tying 需要

$$
Vd+dd_h
=25{,}600{,}000+512\times1024
=26{,}124{,}288.
$$

因此节省

$$
76{,}800{,}000-26{,}124{,}288=50{,}675{,}712.
$$

$P$ 不是随 $V$ 增长的词表矩阵，但必须计入模型参数；若计 bias，两式都再加 $50{,}000$，差值不变。

### NN-WTY-B03

input 贡献只在 row 1：

$$
G_{\rm in}=
\begin{bmatrix}0&0\\0.2&-0.1\\0&0\end{bmatrix}.
$$

output 贡献为 outer product：

$$
G_{\rm out}=(p-y)h^\mathsf T
=\begin{bmatrix}
0.2&-0.1\\
-1.4&0.7\\
1.2&-0.6
\end{bmatrix}.
$$

所以

$$
\nabla_E\mathcal L=
\begin{bmatrix}
0.2&-0.1\\
-1.2&0.6\\
1.2&-0.6
\end{bmatrix}.
$$

row 1 的两条梯度方向相反一部分，必须先相加再由 optimizer 更新一次。

## C

### NN-WTY-C01

lookup 路径 $x=E^\mathsf Tq_i$ 的 VJP 已给出

$$
\nabla_E L_{\rm in}=q_i g_x^\mathsf T.
$$

输出路径 $z=Eh+b$ 满足 $dz=dE\,h$。令 $\delta=\nabla_zL=p-y$，则

$$
dL=\delta^\mathsf TdE\,h
=\operatorname{tr}[(\delta h^\mathsf T)^\mathsf TdE],
$$

故

$$
\boxed{\nabla_E L=q_i g_x^\mathsf T+(p-y)h^\mathsf T}.
$$

有限 logits 下 softmax 的 $p_j>0$；除特殊抵消或 $h=0$ 外，$(p_j-y_j)h$ 对每个 row 都非零，所以第二项通常稠密。

### NN-WTY-C02

令 $r=Ph\in\mathbb R^d$、$z=Er+b$、$\delta=\nabla_zL$。逐层反向：

$$
\nabla_E L_{\rm out}=\delta r^\mathsf T,
\qquad
\nabla_rL=E^\mathsf T\delta,
$$

$$
\boxed{
\nabla_PL=(E^\mathsf T\delta)h^\mathsf T,
\qquad
\nabla_hL=P^\mathsf TE^\mathsf T\delta
}.
$$

若同一 $E$ 还用于输入 lookup，要再加 $q_i g_x^\mathsf T$。direct tying 是 $d=d_h$ 且 $P=I$（固定不学习）的特例。

### NN-WTY-C03

在独立近似下

$$
z_i=\sum_{j=1}^d E_{ij}h_j,
$$

每项零均值且方差 $\sigma_E^2q_h$，交叉项期望为零，因此

$$
\operatorname{Var}(z_i)\approx d\sigma_E^2q_h.
$$

要让 logits 保持 $O(1)$，需 $d\sigma_E^2q_h=O(1)$；若 $q_h\approx1$，即 $\sigma_E^2=O(1/d)$。这只是初始化二阶矩近似；tying 后 $e_i$ 与 $h$ 可能相关，训练中也应实测 logit RMS 和 entropy。

## D

### NN-WTY-D01

先断言 `embedding.weight is output.weight` 或底层 storage pointer 相同；错误复制会失败。构造 loss 同时经过 lookup 和 head，核对共享权重的 `.grad` 等于分支 VJP 之和且只出现一个 Parameter ID。检查 optimizer parameter groups/state dict 中该对象只有一份 state。保存—加载后再次验证 object/storage identity，并做一步确定性更新；若只比较初始数值，复制实现会伪装成正确 tying。

### NN-WTY-D02

lookup branch 不给 padding row 梯度，但 output branch 的 $(p_j-y_j)h$ 仍会更新它，所以“该 Parameter row 永远冻结”与“只在输入端忽略 padding”是两种不同语义。合同一：padding 不属于可预测词表，将对应 output logit mask 为 $-\infty$、loss target 禁止它，并冻结该共享 row。合同二：允许输出端训练该 prototype，但输入端返回独立的固定零向量或对该 row lookup `detach`；此时不要声称共享 row 冻结。

### NN-WTY-D03

单 batch 的负 cosine 可能是有益折中、噪声或尺度极小的偶然值；最终更新还受其他样本、optimizer preconditioner 与长期目标影响。应按频率桶和 row 记录两支 gradient norm、cosine、总更新及 loss change 的时间序列，配合 untied 对照。再做受控干预：调整两支 loss/learning-rate、gradient projection 或暂时 stop 一支，并用 validation NLL、稀有词与收敛速度判断。只有持续冲突且缓解后外部指标稳定改善，才支持“冲突有害”。

## E

### NN-WTY-E01

三组使用同一 tokenizer、数据顺序、总训练 token、有效 batch、optimizer family 与调参预算；projected 组把 $P$ 的参数和 FLOP 计入。报告全模型/词表参数、峰值显存、step/token 吞吐、validation perplexity 和频率分桶 NLL；同时记录 logit RMS/entropy、input/output 分支梯度范数与 cosine、update-to-weight ratio。可再给 matched-compute 与 matched-parameter 两条轨道，避免 tying 的容量节省被额外宽度偷偷消费。

### NN-WTY-E02

tying 删除的是独立输出矩阵，函数类从所有 $(E,U)$ 缩到 $U=E$ 或 $U=EP$；若 $d_h\ne d$ 还需 projection。它固定输入几何与输出 prototype 的关系，并让两条梯度共用 optimizer state；输入/输出词表行语义不一致时甚至不合法。虽然某些任务上这种归纳偏置可改善泛化，不能由参数计数推出表达能力严格不变或性能无代价。

### NN-WTY-E03

先建立显式语义映射 $M$：只对规范化字符串、special-token role 和分词边界均一致的 token 共享 row；其余输入、输出各保留私有参数。实现可用 shared core table 加两侧 index map，或把交集 rows gather 到共同 Parameter。测试必须检查映射双射/冲突、special token、Unicode normalization，并用人工小词表验证 logits 对应名称；绝不能直接把相同整数 ID 当作语义相同。
