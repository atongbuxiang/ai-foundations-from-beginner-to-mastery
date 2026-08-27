---
type: solution
status: draft
area: [neural-networks/embedding-output, softmax-bottleneck, rank]
topic: "[[Softmax Bottleneck 与低秩限制]]"
exercise: "[[习题 - Softmax Bottleneck 与低秩限制]]"
sources: ["[[S-2018-Yang-Softmax-Bottleneck]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Su-9698-Output-Embedding]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Softmax Bottleneck 与低秩限制

## A

### NN-SBR-A01

把 hidden states 按 context 排成 $H\in\mathbb R^{N\times d}$，output rows 为 $W\in\mathbb R^{V\times d}$，bias 为 $b\in\mathbb R^V$。于是

$$
Z=HW^\mathsf T+\mathbf1_Nb^\mathsf T\in\mathbb R^{N\times V}.
$$

逐行 Softmax 后 $L=\log P\in\mathbb R^{N\times V}$，且

$$
L=Z-a\mathbf1_V^\mathsf T,
\qquad
a_i=\log\sum_{v=1}^V e^{Z_{iv}}.
$$

所以 $L$ 与 $Z$ 的第 $i$ 行只差同一个常数 $a_i$；这是 Softmax 的 row-shift gauge。

### NN-SBR-A02

单 context 命题允许为一个 $p\in\Delta_{V-1}^{\circ}$ 自由选择一整个 $V$ 维 logit 向量，取 $z=\log p$ 即可。Bottleneck 命题同时量化许多 contexts，并要求它们的 logits 都由同一 $W,b$ 和低维 $h(c)\in\mathbb R^d$ 生成。前者是逐点存在性，后者是共享参数下的函数族约束；自由度合同不同，因而不矛盾。

### NN-SBR-A03

$$
C_V=I_V-\frac1V\mathbf1_V\mathbf1_V^\mathsf T,
\qquad
J_N=I_N-\frac1N\mathbf1_N\mathbf1_N^\mathsf T.
$$

右乘 $C_V$ 从每行减去词表均值，消去对每个 context 加 common logit 的不可辨识方向。左乘 $J_N$ 从每列减去 context 均值，进一步消去所有 contexts 共用的 output-bias baseline。双中心化后保留的是随 context 变化的可辨识 log-ratios。

## B

### NN-SBR-B01

每行和为 $0.7+3(0.1)=1$。令 $\mathbf1\in\mathbb R^4$，逐元素对数可写成

$$
L=(\log0.1)\mathbf1\mathbf1^\mathsf T+(\log7)I_4.
$$

因为 $J_4=C_4$，且 $C_4\mathbf1=0$、$C_4^2=C_4$，

$$
J_4LC_4=(\log7)C_4.
$$

$C_4$ 是投影到 $\mathbf1^\perp$ 的正交投影，特征值也是奇异值 $(1,1,1,0)$。因此结果的秩为 3，非零奇异值均为 $\log7\approx1.94591$。

### NN-SBR-B02

只做 vocabulary centering：

$$
LC_V=HW^\mathsf TC_V+\mathbf1b^\mathsf TC_V,
$$

所以当 $d=2$ 时 $\operatorname{rank}(LC_V)\le2+1=3$。再做 context centering，rank-one bias 项被 $J_N\mathbf1=0$ 消去，故

$$
\operatorname{rank}(J_NLC_V)\le2.
$$

差的 1 正是 context-independent、但可在 vocabulary 方向变化的 bias row；它不能制造 context-varying rank。

### NN-SBR-B03

双中心化后

$$
J_NLC_V=J_NHP^\mathsf TE^\mathsf TC_V.
$$

乘积秩不超过任一因子秩，因此

$$
\operatorname{rank}(J_NLC_V)
\le \min\{\operatorname{rank}(H),\operatorname{rank}(P),\operatorname{rank}(E),N-1,V-1\}.
$$

特别地，它不超过 $\operatorname{rank}(P)\le\min(d_e,d_h)$。配置中的 $d_h$ 并不自动等于有效 output-rank budget。

## C

### NN-SBR-C01

由 $\mathbf1_V^\mathsf TC_V=0$，

$$
LC_V=(Z-a\mathbf1_V^\mathsf T)C_V=ZC_V.
$$

代入 $Z=HW^\mathsf T+\mathbf1_Nb^\mathsf T$，再左乘 $J_N$：

$$
J_NLC_V=J_NHW^\mathsf TC_V+J_N\mathbf1_Nb^\mathsf TC_V.
$$

第二项因 $J_N\mathbf1_N=0$ 为零，故得到所求恒等式。最后用乘积秩界：

$$
\operatorname{rank}(J_NLC_V)
\le\min\{\operatorname{rank}(J_NH),\operatorname{rank}(W^\mathsf TC_V)\}
\le d.
$$

### NN-SBR-C02

令 $L^*=\log P^*$、$D^*=J_NL^*C_V$。对 $L^*$ 作双向均值分解：

$$
L^*=D^*+\mathbf1_N\beta^\mathsf T+r\mathbf1_V^\mathsf T,
$$

其中可取

$$
\beta^\mathsf T=\frac1N\mathbf1_N^\mathsf TL^*C_V,
\qquad
r=\frac1V L^*\mathbf1_V.
$$

若 $\operatorname{rank}(D^*)\le d$，取任意 rank factorization $D^*=HW^\mathsf T$，并令 output bias $b=\beta$。于是 logits

$$
Z=HW^\mathsf T+\mathbf1_Nb^\mathsf T=L^*-r\mathbf1_V^\mathsf T.
$$

$Z$ 只是在 $L^*$ 每行减去一个常数，所以 $\operatorname{softmax}(Z)=\operatorname{softmax}(L^*)=P^*$。充分性依赖 hidden rows 可自由设置；共享 encoder 未必能实现这些行。

### NN-SBR-C03

若 $D^*=U\Sigma V^\mathsf T$，最佳 rank-$d$ 近似为

$$
D_d=U_{:d}\Sigma_{:d}V_{:d}^\mathsf T,
\qquad
\|D^*-D_d\|_F^2=\sum_{k>d}\sigma_k^2.
$$

这是 centered log-ratio 上的未加权平方误差。Cross-entropy/KL 经 Softmax 非线性计算，并受 context 分布、高低概率类别、logit 曲率和最小概率控制；perplexity 又是 NLL 的指数。没有把这些对象联系起来的上下界时，不能把 tail energy 直接重命名为 NLL 或 perplexity 下界。

## D

### NN-SBR-D01

先冻结 tokenizer/version 与 context 定义，再按预先声明的 context classes 聚合 held-out counts。对零计数采用有记录的 Dirichlet/additive、backoff 或 teacher smoothing，并做多个强度的 sensitivity analysis；对每行形成 $\widehat P$ 后计算 $J\log\widehat P C$。用 bootstrap 重采样 contexts/tokens，报告 singular values 的置信区间而非单一数值；同时分别给出未加权谱、按 context 频率加权谱和按 token 频率桶的稳定性。最后用 synthetic known-rank table 校准估计器偏差，并把 vocabulary size、截断、special tokens、聚合规则与随机种子写入实验合同。

### NN-SBR-D02

高经验秩不能排除：encoder 无法生成所需 hidden rows；非凸优化停在较差解；regularization/early stopping 主动限制有效自由度；有限样本、smoothing 和计数噪声抬高经验秩；tokenizer/数据错配；数值或实现错误。对照应包括自由 hidden-table 模型以隔离 encoder、增大 $d$ 与 MoS 以改变 head family、多随机种子/更强 optimizer 以检查优化、known-rank synthetic data 以校准估计、以及同一 tokenizer 上的 full-data/held-out 重复估计。只有相应干预按 rank 预测稳定消除差距，才能把证据归向 bottleneck。

### NN-SBR-D03

Untied head 的预算至多 $\min(d_h,V-1,N-1)$；direct tying 还受 $\operatorname{rank}(E)$ 限制；projected tying 至多 $\operatorname{rank}(P)$、$\operatorname{rank}(E)$ 与 $d_h$ 的最小值。代码测试应解析真实 forward graph，检查 output Parameter identity、矩阵 shapes、projection 是否存在及其数值秩/奇异值，并在一组 hidden probes 上直接形成 centered logits 求数值秩。还要测试 load/quantize 后是否发生静默复制、截断或低秩 adapter；配置字段只能作提示，不能代替运行时证据。

## E

### NN-SBR-E01

固定 tokenizer、数据顺序、encoder family、训练 token、调参预算与 exact evaluation。Standard 组用宽度 $d$；width 组增加 $d$ 并计入 backbone/head 参数与 FLOP；MoS 组改变 component 数 $K$，报告 component collapse 与 mixture entropy。共同报告 exact validation NLL/perplexity、校准、频率桶质量、参数/optimizer bytes、训练与生成 wall time、峰值显存和多种子区间。另给 matched-parameter 与 natural-best 两条轨道：前者隔离结构，后者比较可获得的 Pareto frontier。更高经验 rank 只作中间诊断，不替代最终质量指标。

### NN-SBR-E02

Bias 产生 $\mathbf1_Nb^\mathsf T$，它可以改变所有 contexts 共用的 vocabulary baseline，因此可能把 $\operatorname{rank}(LC_V)$ 增加至多 1。但

$$
J_N(\mathbf1_Nb^\mathsf T)C_V=0,
$$

所以它对 context-varying centered log-ratios 没有贡献。若目标 $J_NL^*C_V$ 的秩大于 $d$，任何 bias 都无法补上缺失方向；“raw matrix 看起来秩更高”不等于跨-context 表达预算提高。

### NN-SBR-E03

先选正交矩阵 $U\in\mathbb R^{N\times r}$、$V\in\mathbb R^{V\times r}$，令列分别与全一向量正交，构造 $D=U\operatorname{diag}(s_1,\ldots,s_r)V^\mathsf T$。加入任意 column baseline $\mathbf1b^\mathsf T$ 与 row shift $a\mathbf1^\mathsf T$，再逐行 Softmax 得到严格正 $P^*$；其双中心 log-ratio rank 为 $r$。用自由 hidden table + 充分优化测试纯 rank barrier：$d\ge r$ 应可拟合，$d<r$ 有误差地板。再换成受限 encoder 测 encoder barrier；最后在已知可实现的 $d\ge r$ 设置中改变初始化、优化器和训练时长测 optimization barrier。三层必须分别有 oracle/过参数化对照。
