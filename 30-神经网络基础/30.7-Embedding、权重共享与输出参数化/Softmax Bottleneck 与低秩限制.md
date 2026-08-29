---
type: derivation
status: draft
area: [neural-networks/embedding-output, softmax-bottleneck, rank, language-modeling]
aliases: [Softmax Bottleneck, Log-Probability Rank]
node_id: NN-53
prerequisites: ["[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[核、像与秩零化度定理]]", "[[奇异值分解]]", "[[参数对称性、等价表示与可辨识边界]]"]
related: ["[[输入—输出权重共享与 Weight Tying]]", "[[Sampled、Hierarchical 与 Adaptive Softmax]]", "[[有效秩]]", "[[随机化低秩近似与随机 SVD]]"]
sources: ["[[S-2018-Yang-Softmax-Bottleneck]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Su-9698-Output-Embedding]]"]
exercises: ["[[习题 - Softmax Bottleneck 与低秩限制]]"]
solutions: ["[[解答 - Softmax Bottleneck 与低秩限制]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-softmax-bottleneck-rank-v2.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# Softmax Bottleneck 与低秩限制

> [!abstract] 本章主问题
> 单独看一个 context，自由 logits 可以表示任意严格正 categorical distribution；Softmax bottleneck 说的不是这件事。它说：当很多 contexts 必须共用同一个低维线性 output head 时，所有 centered log-probability vectors 只能落在一个低维仿射子空间。若目标条件分布跨 contexts 的可辨识 log-ratio matrix 秩更高，模型无论怎样训练都不能精确表示它。

## 课程位置与两遍学习路线

- **承接什么：** NN-52 证明一个 context 的自由 logits 可表示任意严格正 categorical distribution，并指出 common shift 是 gauge；
- **本页解决什么：** 把多个 contexts 的条件分布堆成矩阵，双重中心化后识别共享低维 output head 的 rank 上限；
- **后续为何需要：** 大词表近似、weight tying 与 embedding factorization 都可能改变 rank budget，必须先分清“计算近似”和“表达族限制”。

**第一遍只做中心化与秩。** 将 $P^*$ 逐元素取 log，先消去每个 context 的 Softmax row shift，再消去跨 context 共享的 output bias，比较目标 rank 与 hidden width。

**第二遍再讨论风险。** 检查零频率平滑、context sampling、经验谱噪声、encoder 可达性，以及 Frobenius 低秩误差能否转成 KL/NLL 下界。

### 问题链

1. 一个 context 上的 Softmax 满射为什么不排除跨 contexts 的 bottleneck？
2. vocabulary centering 消除了哪个 gauge，context centering又消除了哪个参数方向？
3. 为什么标准线性 head 满足 $\operatorname{rank}(J_N\log P_\theta C_V)\le d$？
4. target rank 大于 $d$ 时，结论是优化失败还是函数类不包含目标？
5. tail singular energy 为何只是 log-ratio 几何误差，不能直接冒充 perplexity 下界？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal E_\square$ 的四 context 目标上得到 $D^*=(\log7)C_4$、$\operatorname{rank}(D^*)=3$，并据此说明 $d=2$ 线性 head 无法精确表示它，就已掌握本页主干。

## 符号与对象账本

| 对象 | shape | 被消除的冗余 / 保留的信息 |
|---|---:|---|
| $P^*$ | $N\times V$ | 目标条件概率表 |
| $L^*=\log P^*$ | $N\times V$ | log-probability；要求严格正或先声明平滑 |
| $C_V$ | $V\times V$ | 消去每个 context 的 common logit shift |
| $J_N$ | $N\times N$ | 消去 context-independent output bias |
| $D^*=J_NL^*C_V$ | $N\times V$ | 可辨识的跨 context log-ratio 变化 |
| $H W^{\mathsf T}$ | $N\times V$ | 标准线性 head 的 rank-$d$ 因子化 |

### 贯穿算例 $\mathcal E_\square$：四词目标需要三个可辨识方向

保持 $V=4,d=2$，并取四个 contexts，使每个 context 分别偏好一个 token：

$$
P^*_{ij}=
\begin{cases}
0.7,&i=j,\\
0.1,&i\ne j.
\end{cases}
$$

令

$$
C_4=I_4-\frac14\mathbf1\mathbf1^{\mathsf T}.
$$

因为

$$
L^*=\log P^*
=(\log0.1)\mathbf1\mathbf1^{\mathsf T}+(\log7)I_4,
$$

左右中心化会删除常数项：

$$
\boxed{
D^*=C_4L^*C_4=(\log7)C_4
}.
$$

$C_4$ 的 eigenvalues 是 $1,1,1,0$，所以

$$
\operatorname{rank}(D^*)=3,
$$

而 $d=2$ 的标准线性 head 必有

$$
\operatorname{rank}(J_NL_\theta C_V)\le2.
$$

因此不存在任何 $H\in\mathbb R^{4\times2}$ 与共享 $W\in\mathbb R^{4\times2}$ 能精确重现这张目标概率表。若仅按 Frobenius norm 做最佳 rank-2 近似，三个非零 singular values 都是 $\log7$，故至少留下

$$
\boxed{
\min_{\operatorname{rank}(M)\le2}\|D^*-M\|_F^2
=(\log7)^2
}.
$$

这是可辨识 log-ratio 空间的误差地板；转成 NLL/KL 仍需概率下界、context 权重与 Softmax 曲率条件。

## 核心公式七问：双重中心化 Rank Contract

$$
\boxed{
D_\theta=J_N(\log P_\theta)C_V
=J_NHW^{\mathsf T}C_V,
\qquad
\operatorname{rank}(D_\theta)\le d
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 测量跨 contexts 可辨识条件分布变化的线性维数 |
| 对象 | 严格正的 context-by-vocabulary 概率表 |
| 来路 | Softmax row gauge、output bias 与 low-dimensional shared head |
| 步骤 | 概率取 log→右乘 $C_V$→左乘 $J_N$→算 rank/spectrum→与 $d$ 比较 |
| 读法 | target rank 超预算是表达障碍，不是训练轮数不足 |
| 检查 | smoothing、SVD tolerance、context resampling、untied/tied 与 nonlinear-head ablation |
| 去路 | Mixture of Softmaxes、nonlinear heads、adaptive vocabularies 与输出分解 |

### AI / 系统对应

真实语言模型的 context 数远大于可直接成表的规模，通常只能在采样 contexts 上估计谱。经验高 rank 可能来自有限样本噪声和零频率处理；经验低 rank 也可能只是采样覆盖不足。可信报告应给 tokenizer、context distribution、平滑常数、奇异值区间和下游 NLL，而不是只展示一张谱图。

## 一、学习目标

读完本节，你应能：

1. 区分单 context 的 Softmax 满射与跨 context 的共享参数限制；
2. 把条件分布排成 context-by-vocabulary matrix；
3. 用 vocabulary centering 消去 Softmax row-shift gauge；
4. 再用 context centering 消去 output bias，推出 sharp rank bound；
5. 手算一个 $4\times4$ 高秩目标分布；
6. 解释 SVD approximation error 与 cross-entropy error 的区别；
7. 说明 Mixture of Softmaxes 为什么能越出单一低秩族；
8. 审计 empirical rank、零频率、平滑、tokenizer 和样本噪声边界。

## 二、先消除一个表面矛盾

给定一个固定 context $c$ 和任意严格正概率向量

$$
p^*\in\Delta_{V-1}^{\circ},
$$

取

$$
z_i=\log p_i^*,
$$

就有

$$
\operatorname{softmax}(z)=p^*.
$$

所以问题不是“Softmax 对一个点能不能表示任意分布”。问题是是否存在同一组 $W,b$，使所有 contexts 都满足

$$
z(c)=Wh(c)+b.
$$

当 $h(c)\in\mathbb R^d$ 且 $d\ll V$ 时，跨 context 的 logits 不能各自自由选择。

## 三、把条件语言模型写成矩阵

取 $N$ 个 contexts $c_1,\ldots,c_N$，词表大小为 $V$。把 hidden states 作为行：

$$
H=
\begin{bmatrix}
h(c_1)^\mathsf T\\
\vdots\\
h(c_N)^\mathsf T
\end{bmatrix}
\in\mathbb R^{N\times d}.
$$

令 output rows 为 $W\in\mathbb R^{V\times d}$、bias 为 $b\in\mathbb R^V$。logit matrix 是

$$
Z=HW^\mathsf T+\mathbf1_Nb^\mathsf T
\in\mathbb R^{N\times V}.
$$

逐行 Softmax 后，log-probability matrix $L_\theta$ 的元素为

$$
(L_\theta)_{ij}
=Z_{ij}-a_i,
\qquad
a_i=\log\sum_{v=1}^V e^{Z_{iv}}.
$$

矩阵写法：

$$
\boxed{
L_\theta=Z-a\mathbf1_V^\mathsf T
}.
$$

$a\mathbf1_V^\mathsf T$ 就是每个 context 的 Softmax normalization row shift。

## 四、Vocabulary Centering 消去 Gauge

定义词表方向的 centering matrix

$$
C_V=I_V-\frac1V\mathbf1_V\mathbf1_V^\mathsf T.
$$

它满足

$$
\mathbf1_V^\mathsf TC_V=0,
\qquad
C_V^2=C_V.
$$

右乘 $C_V$：

$$
L_\theta C_V
=ZC_V-a\mathbf1_V^\mathsf TC_V
=ZC_V.
$$

因此

$$
\boxed{
L_\theta C_V
=HW^\mathsf TC_V+\mathbf1_Nb^\mathsf TC_V
}.
$$

$L C_V$ 是每个 context 的 centered log-probability，也可看作一组 log-ratio coordinates。它不随每行 logits 加常数而改变。

由 rank subadditivity 立刻得到较粗的界：

$$
\operatorname{rank}(L_\theta C_V)
\le d+1.
$$

其中额外的 1 来自 output bias 在所有 contexts 上重复的一行方向。

## 五、Context Centering 给出更锋利的界

定义 context centering matrix

$$
J_N=I_N-\frac1N\mathbf1_N\mathbf1_N^\mathsf T.
$$

由于 $J_N\mathbf1_N=0$，左乘后 bias 也消失：

$$
J_NL_\theta C_V
=J_NHW^\mathsf TC_V.
$$

于是

$$
\boxed{
\operatorname{rank}(J_NL_\theta C_V)\le d
}.
$$

这就是跨 contexts 的**可辨识 log-ratio rank bound**。它同时去掉：

- Softmax 对每个 context 的 common logit shift；
- 对所有 contexts 共同的 output bias；
- 不影响条件分布差异的 grand mean。

因此不能拿未经 centering 的 raw logit/log-probability rank 直接宣布 bottleneck。

## 六、有限 Context Table 上的精确表征判据

令目标严格正条件分布为 $P^*\in(0,1)^{N\times V}$，逐元素取对数：

$$
L^*=\log P^*.
$$

定义双重中心化矩阵

$$
D^*=J_NL^*C_V.
$$

若标准线性 head 能精确表示 $P^*$，则必要条件是

$$
\operatorname{rank}(D^*)\le d.
$$

若把 $N$ 个 hidden rows 当作可自由选择的表参数，这个条件也是充分的：对 $D^*$ 做 rank-$d$ factorization，令其成为 $HW^\mathsf T$ 的双重中心化部分；context-independent column component 交给 $b$，row-constant component 由 Softmax gauge 吸收。

> [!warning] 充分性边界
> 真实网络的 $h(c)$ 不是 $N$ 个自由参数，而是由同一个 encoder 对输入计算得到。即使 table rank 条件满足，encoder 也未必能产生所需 hidden rows。因此 rank 通过只消除了一类 output-head 障碍，不证明整个网络可实现目标。

## 七、完整手算：对角占优目标

取 $N=V=4$，每个 context 偏好不同 token：

$$
P^*_{ij}=
\begin{cases}
0.7,&i=j,\\
0.1,&i\ne j.
\end{cases}
$$

每行确实归一化，因为 $0.7+3\times0.1=1$。其 log matrix 可写为

$$
L^*
=(\log0.1)\mathbf1\mathbf1^\mathsf T
+(\log7)I_4.
$$

左右 centering 后，constant term 消失：

$$
D^*=J_4L^*C_4
=(\log7)C_4.
$$

$C_4$ 在 $\mathbf1$ 方向特征值为 0，在其正交补上特征值为 1，所以

$$
\boxed{
\operatorname{rank}(D^*)=3
}.
$$

因此 hidden dimension $d<3$ 的标准线性 head 不可能精确表示这个四-context table。它不是训练失败，而是函数类中没有目标。

## 八、Rank 不足时的最佳线性近似

对目标双中心矩阵做 SVD：

$$
D^*=U\Sigma V^\mathsf T,
\qquad
\sigma_1\ge\cdots\ge\sigma_r>0.
$$

任何 rank 不超过 $d$ 的矩阵 $M$ 都满足 Eckart–Young–Mirsky 下界：

$$
\min_{\operatorname{rank}(M)\le d}
\|D^*-M\|_F^2
=\sum_{k>d}\sigma_k^2.
$$

这给出 centered log-ratio 的几何误差地板。但训练优化的是 cross-entropy/KL，而不是未加权 Frobenius norm；高概率 token、context 权重与 Softmax 曲率会改变同样矩阵误差对应的风险。因此不能把 tail singular energy 直接叫作 perplexity 下界，除非再建立相应不等式和概率下界条件。

## 九、Bias、Weight Tying 与其他附加约束

output bias 只平移所有 contexts 共享的 vocabulary log-ratio baseline，已被 $J_N$ 消去；它不能增加 context-varying rank。

若 weight tying 强制

$$
W=E,
$$

则 head 不仅有 rank budget，还与输入 embedding geometry、初始化与两条梯度耦合。相同 $d$ 下，tying 的函数族是 untied head 的子集或受 projection 约束的变体。

若使用 projection

$$
z=EPh+b,
$$

有效 context-varying rank 不超过

$$
\operatorname{rank}(P)\le\min(d_e,d_h).
$$

只报告 hidden width 而不报告 projection rank 会高估 output rank budget。

## 十、Mixture of Softmaxes 为什么能突破

Mixture of Softmaxes（MoS）定义

$$
p(w\mid c)
=\sum_{k=1}^K\pi_k(c)
\frac{\exp z_{k,w}(c)}{\sum_v\exp z_{k,v}(c)},
$$

其中

$$
\pi_k(c)\ge0,
\qquad
\sum_k\pi_k(c)=1.
$$

取对数后出现

$$
\log\sum_k \pi_k(c)p_k(w\mid c),
$$

这不是某个单一低秩 logit matrix 加 row shift。`log of sum` 的非线性让结果可越出标准 rank-$d$ family。

但 MoS 不是免费午餐：

- 通常要计算 $K$ 个 component heads 或相应共享变体；
- mixture components 有置换对称性；
- components 可能坍缩成相同分布；
- 更高表达力不保证优化、校准或 wall time 更好；
- $K$ 有限时仍是受限函数族。

## 十一、其他“突破”方式改变了什么

1. **增大 $d$**：直接提高 rank budget，也提高 head/hidden 成本；
2. **非线性 output decoder**：改变跨 context 的函数族，但仍需计算 $V$ 个 scores；
3. **latent-variable/energy model**：改变 normalization 与训练方法；
4. **层次化词表**：改变 probability factorization，不只是加速原 head；
5. **改变 tokenizer**：改变 $V$、目标矩阵和 context 定义，不能当作同一问题无缝比较；
6. **检索或候选集合**：改变支持集或评价条件，必须审计漏召回。

## 十二、怎样估计经验 Bottleneck

真实语料没有直接给出完整 $P^*(w\mid c)$。经验估计至少要处理：

- 同一 context 很少重复，条件频率极稀疏；
- zero count 导致 $\log0=-\infty$，必须声明 smoothing；
- $N,V$ 与采样方式决定最大可见 rank；
- 高频与低频 token 噪声差异巨大；
- singular values 在有限样本下有估计偏差；
- tokenizer、context truncation 与 special tokens 改变矩阵本身。

可行协议包括聚合 context classes、teacher distribution、held-out model probing 或低维 synthetic calibration；每种方法估计的对象不同。

## 十三、常见误区

1. **“Softmax 本身低秩”**：Softmax 是非线性映射；低秩来自共享线性 logits family；
2. **“一个 context 也受 bottleneck”**：自由 logits 对 simplex interior 没有此 rank 问题；
3. **“raw $\log P$ rank 就是答案”**：需先处理 row-shift gauge，最好双重中心化；
4. **“rank 高就是语言质量好”**：噪声也能给高秩；rank 只是表达诊断；
5. **“训练 loss 高必是 bottleneck”**：优化、数据、encoder、regularization 与系统 bug 都可能导致；
6. **“MoS 一定更好”**：表达上限、训练行为和成本必须分账。

## 十四、图：目标秩、模型秩与突破方式

先看图回答：为什么目标 $4\times4$ table 的 centered rank 是 3？为什么 output bias 只能贡献共同 baseline？MoS 改变的是矩阵 rank 数值，还是整个 log-probability family？

![[00-知识库管理/_assets/figures/neural-networks/fig-softmax-bottleneck-rank-v2.svg|900]]

> [!figure] 图 30.7-05　Softmax bottleneck 的目标矩阵、线性秩界与突破路径
> 左栏给出对角占优的四-context 分布并消去 row shift；中栏从 $Z=HW^T+\mathbf1b^T$ 推出 vocabulary-centered rank 界；右栏区分增大维度、非线性 decoder 与 Mixture of Softmaxes。来源：依据 Yang et al. 的原始 bottleneck/MoS 论文与本节双重中心化推导绘制；由 [[00-知识库管理/_labs/code/plot_embedding_output_advanced_v2.py]] 确定性生成。

**怎样读图**：先确认矩阵的行是 contexts、列是 tokens；再右乘 $C_V$ 去掉 Softmax gauge，必要时左乘 $J_N$ 去掉 bias；最后比较目标 singular spectrum 与有效 rank budget。

**图没有证明什么**：图不证明自然语言的真实 rank 固定为某个数，也不证明高秩 head 必然有更低 perplexity、良好校准或更高系统效率。

## 十五、最小验收

1. 解释单 context universality 与跨 context bottleneck 不矛盾；
2. 写出 $H,W,b,Z,L$ 的 shapes；
3. 推导 $LC_V=ZC_V$；
4. 推导 $J_NLC_V=J_NHW^TC_V$ 与 rank bound；
5. 复算 $P^*_{ii}=0.7$ 的 rank-3 例子；
6. 区分 SVD 几何误差与 cross-entropy 风险；
7. 解释 bias、projection tying 和 encoder constraints；
8. 写出 MoS 并说明 `log(sum)` 为什么越出单一线性族；
9. 设计 empirical rank 的 smoothing/采样审计。

> [!summary]
> Softmax bottleneck 是共享低维 output parameterization 的跨-context 表达限制。双重中心化把不可辨识的 row shift 和 context-independent bias 剥离后，标准线性 head 的目标矩阵秩不超过 hidden dimension；高于该预算的目标需要更大维度、不同 decoder 或 mixture/latent structure，但 rank 诊断本身不等于任务质量证明。

- [[Embedding、权重共享与输出参数化 MOC]]
- [[习题 - Softmax Bottleneck 与低秩限制]]
- [[解答 - Softmax Bottleneck 与低秩限制]]
