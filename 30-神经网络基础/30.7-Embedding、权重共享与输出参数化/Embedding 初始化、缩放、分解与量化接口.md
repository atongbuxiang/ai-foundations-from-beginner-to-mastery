---
type: derivation
status: draft
area: [neural-networks/embedding-output, embedding-initialization, factorization, quantization, compression]
aliases: [Embedding Compression, Factorized Embeddings]
node_id: NN-56
prerequisites: ["[[Embedding Lookup、稀疏梯度与参数规模]]", "[[输入—输出权重共享与 Weight Tying]]", "[[方差传播与宽层均值场近似]]", "[[奇异值分解]]", "[[定理 - Eckart–Young–Mirsky]]"]
related: ["[[Embedding 几何、相似度与各向异性]]", "[[Softmax Bottleneck 与低秩限制]]", "[[随机化低秩近似与随机 SVD]]", "[[迭代改进、混合精度与残差校正]]"]
sources: ["[[S-2020-Lan-ALBERT]]", "[[S-2019-Baevski-Auli-Adaptive-Input]]", "[[S-2022-Tao-Quantized-Generative-LM]]", "[[S-2026-PyTorch-Embedding]]", "[[S-2023-Su-9698-Output-Embedding]]"]
exercises: ["[[习题 - Embedding 初始化、缩放、分解与量化接口]]"]
solutions: ["[[解答 - Embedding 初始化、缩放、分解与量化接口]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-embedding-scale-compression-v2.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# Embedding 初始化、缩放、分解与量化接口

> [!abstract] 本章主问题
> Embedding table 常是大词表模型的主要参数之一。初始化必须同时校准 lookup row norm 与 tied output logits；低秩分解、自适应维度和量化可减少参数或字节，却分别引入 rank constraint、frequency-dependent capacity 与 reconstruction error。完整比较要同时记函数类、训练状态、访问计算、kernel 和端到端质量。

## 课程位置与两遍学习路线

- **承接什么：** NN-49—55 已建立表的 lookup、几何、共享输出、概率 rank、近似输出和离散词表合同；
- **本页解决什么：** 比较初始化、运行时 scaling、低秩分解、自适应维度与量化分别改写哪个对象，并把参数、字节、误差、计算和质量分账；
- **后续为何需要：** 30.8 的正则化与泛化接口会继续改变训练函数和证据对象，必须先理解“压缩”不是一种不改变模型的免费存储操作。

**第一遍只做两个最小变换。** 对 $\mathcal E_\square$ 做最佳 rank-1 近似与一个标量量化，算清参数节省、Frobenius 残差和 tied-logit 误差。

**第二遍再进入真实部署。** 加入初始化方差、factorized gradients/gauge、frequency buckets、PTQ/QAT、scale/zero-point metadata、master weights、optimizer state 与 kernel latency。

### 问题链

1. 初始化 scale、每次 forward 的 runtime scale 与 normalization 为什么是三种不同函数？
2. $E=AB$ 何时节省参数，它同时施加了什么 rank constraint？
3. 最佳 SVD reconstruction error 如何传播到 lookup activation 和 tied output logits？
4. raw INT4 code bytes 为什么不是完整模型、训练状态或 wall-time 压缩率？
5. 量化误差界通过 Cauchy–Schwarz 成立，为什么仍不能推出 NLL/生成质量界？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal E_\square$ 上算出最佳 rank-1 的残差平方 $(17-5\sqrt5)/2$，再证明量化 row 2 的 logit error $1/2$ 达到 Cauchy 上界，就已掌握本页主干。

## 符号与对象账本

| 变换 | 改写对象 | 主要收益 | 必须支付/检查 |
|---|---|---|---|
| initialization scale | step-0 Parameter | 初始 row/logit 二阶矩 | 训练后不保持 |
| runtime scale / norm | 每次 forward 函数 | activation/logit 校准 | 梯度与函数改变 |
| $E=AB$ | 参数化与 rank | 参数/状态减少 | projection MAC、gauge、rank bias |
| adaptive dimension | 按频率分组的容量 | 期望参数/计算下降 | token reorder、tail quality |
| quantization | 连续值到有限 code | 参数带宽/存储下降 | scale metadata、重建误差、kernel |
| PTQ / QAT | 训练流程 | 部署简化 / 误差适应 | calibration data / fake-quant dynamics |

### 贯穿算例 $\mathcal E_\square$：Rank-1 与量化分别损失什么

沿用

$$
E=
\begin{bmatrix}
1&0\\0&1\\2&-1\\-1&3
\end{bmatrix}.
$$

其 Gram matrix 为

$$
E^{\mathsf T}E=
\begin{bmatrix}
6&-5\\-5&11
\end{bmatrix},
$$

eigenvalues，也就是 squared singular values，为

$$
\lambda_\pm=\frac{17\pm5\sqrt5}{2}.
$$

因此最佳 rank-1 近似 $E_1$ 满足

$$
\boxed{
\|E-E_1\|_F^2
=\lambda_-
=\frac{17-5\sqrt5}{2}
\approx2.909830
}.
$$

原表有 $Vd=8$ 个标量参数；写成 $A\in\mathbb R^{4\times1},B\in\mathbb R^{1\times2}$ 只有 $4+2=6$ 个，但整个表被限制在一个 row direction 上，而且 $A\mapsto cA,B\mapsto B/c$ 仍有 gauge。

再看 row 2：

$$
e_2=(2,-1).
$$

用步长 $\Delta=3/4$ 的对称 round-to-nearest 标量量化：

$$
Q_\Delta(e_2)=\left(\frac94,-\frac34\right),
\qquad
\varepsilon=Q_\Delta(e_2)-e_2
=\left(\frac14,\frac14\right).
$$

对 NN-51 的 $h=(1,1)$，原 logit 是 1，量化后是 $3/2$，于是

$$
\boxed{
|\Delta z_2|=\frac12
=|\varepsilon^{\mathsf T}h|
\le\|\varepsilon\|_2\|h\|_2
=\frac{\sqrt2}{4}\sqrt2
=\frac12
}.
$$

本例恰好取等，说明 row reconstruction error 可直接放大为 tied output logit error；但它仍未给出 Softmax NLL 或 autoregressive sequence risk 的充分界。

## 核心公式七问：压缩 Pareto Contract

$$
\boxed{
(\text{function class},\text{parameter/state bytes},\text{access compute},\text{error},\text{task quality},\text{latency})
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 防止把参数减少单独包装成“模型等价且更快” |
| 对象 | initialization、factorized/quantized Parameters、optimizer state 与部署 kernel |
| 来路 | 大词表的存储、带宽、状态和输出投影压力 |
| 步骤 | 固定 baseline→写变换→算 rank/bytes/error→恢复训练/推理状态→测质量与 latency |
| 读法 | 不同方案优化 Pareto 面的不同坐标，不存在脱离任务的唯一压缩率 |
| 检查 | SVD residual、dequant round-trip、logit intervention、PTQ/QAT、cold/warm latency |
| 去路 | ALBERT/adaptive input、低比特 LLM、product quantization 与 embedding serving |

### AI / 系统对应

推荐与语言模型常让 embedding 参数量最大，却未必让其 FLOPs 最大。低秩分解可能省带宽但增加 per-token projection；INT4 可能省 raw bytes 却因解量化或不规则 lookup kernel不加速。报告应同时给 Parameter、master weights、optimizer state、scale metadata、峰值显存、tokens/s 与质量曲线。

## 一、学习目标

读完本节，你应能：

1. 推导 embedding row norm 与 tied logit variance；
2. 区分 Parameter 初始化、运行时 embedding scaling 与 normalization；
3. 计算低秩 factorization 的参数阈值、rank 与 per-token 计算；
4. 推导 factorized table 的两支梯度和 gauge；
5. 用 SVD 说明最优静态 rank-$r$ 初始化；
6. 计算 frequency-adaptive dimensions 的完整参数账；
7. 推导 scalar quantization 的 row/logit error bound；
8. 区分 PTQ、QAT、inference storage 与 optimizer/master state；
9. 设计压缩率—质量—延迟的 Pareto 验收。

## 二、Embedding 初始化的第一本账：Row Norm

设

$$
E_{ij}\overset{\mathrm{iid}}\sim(0,\sigma_E^2),
\qquad E\in\mathbb R^{V\times d}.
$$

第 $i$ 行 $e_i$ 的期望平方范数：

$$
\boxed{
\mathbb E\|e_i\|_2^2
=\sum_{j=1}^d\mathbb E E_{ij}^2
=d\sigma_E^2
}.
$$

若希望初始 row norm 为 $O(1)$，自然选择

$$
\sigma_E^2=O(1/d).
$$

但 row norm 不是唯一目标。输入 embedding 后可能加 position/type embeddings、乘固定 scale、经过 LayerNorm 或进入残差流；完整 activation scale 要看这些组合。

## 三、第二本账：Tied Output Logit Variance

若同一 row 用作 output prototype：

$$
z_i=e_i^\mathsf Th.
$$

假设初始化时 $e_i$ 与 $h$ 近似独立、各分量零均值，且

$$
\operatorname{Var}(h_j)=q_h.
$$

则

$$
\boxed{
\operatorname{Var}(z_i)
\approx d\sigma_E^2q_h
}.
$$

所以同一个 $\sigma_E$ 同时决定 lookup row norm 和 output logit temperature。若 $q_h$ 或 row norm 随层/训练变化，初始校准也不会永久保持。

> [!warning] 独立近似边界
> tying 和训练会让 $e_i$ 与 $h$ 相关；频率、normalization、attention 和 optimizer 也改变分布。公式是初始化基线，必须用 logit RMS、entropy、max gap 与 gradient 实测校准。

## 四、参数初始化、运行时 Scaling 与 Normalization

三者不能混写：

1. **初始化 scale**：只改变 step 0 的 Parameter values；
2. **运行时 scale**：每次 forward 计算 $x=sE_i$，持续改变函数与反向梯度；
3. **normalization**：按 row/token 统计量变换方向/长度，并有自己的 epsilon/affine state。

例如把 embedding 乘 $\sqrt d$，若原分量方差约 $1/d$，可把分量方差提高到 $O(1)$；但 position embedding、residual stream 与 LayerNorm placement 会决定最终是否合适。不能把 $\sqrt d$ 当作所有架构的普遍常数。

## 五、Padding、频率与初始化后的非均匀训练

padding row 常需在初始化后显式置零或冻结 lookup gradient。高频 token 每步被访问更多，默认 sum gradient 下更新更大；低频 rows 长期接近初始化。于是平均 row norm 可能掩盖按频率桶的巨大差异。

应至少按频率/角色报告：

- row norm 与 quantiles；
- gradient/update norm；
- cosine drift from initialization；
- optimizer-state age；
- tied output contribution；
- padding/special rows。

## 六、统一低秩分解

把

$$
E\in\mathbb R^{V\times d}
$$

参数化为

$$
\boxed{
E=AB,
\qquad
A\in\mathbb R^{V\times r},
\quad
B\in\mathbb R^{r\times d}
}.
$$

参数量从

$$
Vd
$$

变成

$$
\boxed{Vr+rd=r(V+d)}.
$$

只有当

$$
r(V+d)<Vd
$$

才节省，即

$$
\boxed{
r<\frac{Vd}{V+d}
}.
$$

当 $V\gg d$ 时，阈值接近 $r<d$。

## 七、手算：$V=50{,}000,d=1024,r=128$

原表：

$$
Vd=51{,}200{,}000.
$$

factorized 参数：

$$
Vr+rd
=50{,}000\times128+128\times1024
$$

$$
=6{,}400{,}000+131{,}072
=6{,}531{,}072.
$$

FP16/BF16 只计参数本体：

$$
\text{full}=102.4\ \mathrm{MB},
$$

$$
\text{factorized}\approx13.062\ \mathrm{MB}.
$$

压缩约

$$
\frac{51.2}{6.531072}\approx7.84\times.
$$

但每次 lookup 先取 $A_{i:}\in\mathbb R^r$，再算

$$
e_i=A_{i:}B,
$$

增加约 $rd=131{,}072$ MAC/token；若预先物化 $AB$ 加速推理，又会恢复 $Vd$ 的表存储。参数与 latency 是两本账。

## 八、Rank Constraint 与函数类

由于

$$
\operatorname{rank}(AB)
\le r,
$$

所有 $V$ 个 rows 只能落在 $B$ 的 row span 中。若原最优 table 的有效秩高于 $r$，factorization 产生 approximation bias。

这与 Softmax bottleneck 有接口但不完全相同：

- input table rank 约束 token representations；
- tied output 又把该 rank 带到 output prototypes；
- projected tying 的有效 rank 还受 projection 限制；
- nonlinear downstream network 可弥补部分输入限制，但不能自动恢复被删除的独立 row degrees of freedom。

## 九、Factorized Lookup 的反向传播

单 token $i$：

$$
a_i=A^\mathsf Tq_i\in\mathbb R^r,
\qquad
e_i=B^\mathsf Ta_i\in\mathbb R^d.
$$

给定上游列梯度 $g\in\mathbb R^d$：

$$
\boxed{
\nabla_B\mathcal L=a_i g^\mathsf T
}.
$$

对 $a_i$：

$$
\nabla_{a_i}\mathcal L=Bg,
$$

因此

$$
\boxed{
\nabla_A\mathcal L=q_i(Bg)^\mathsf T
}.
$$

$A$ 的梯度仍是 row sparse，但共享 basis $B$ 每个访问 token 都会更新；系统上出现“小稠密 basis + 大稀疏 code table”的混合模式。

## 十、Factorization Gauge 与条件性

对任意可逆

$$
R\in\mathbb R^{r\times r},
$$

有

$$
(AR)(R^{-1}B)=AB.
$$

因此 factors 不可辨识。若 $R$ 很病态，$A$ 与 $B$ 的 norm 可极不平衡，函数 $E$ 不变却改变 gradient、weight decay 与有限精度。可用 balanced SVD init、factor norm monitoring、regularization 或定期 rebalancing 控制。

## 十一、SVD 给出静态最优 Rank-$r$ 初始化

若已有 full table

$$
E=U\Sigma V^\mathsf T,
$$

其 Frobenius 最优 rank-$r$ approximation 是

$$
E_r=U_r\Sigma_rV_r^\mathsf T.
$$

可取 balanced factors：

$$
A_0=U_r\Sigma_r^{1/2},
\qquad
B_0=\Sigma_r^{1/2}V_r^\mathsf T.
$$

误差为

$$
\|E-E_r\|_F^2=\sum_{k>r}\sigma_k^2.
$$

它只最小化 table reconstruction；task loss、rare rows、tied logits 与量化 sensitivity 可能需要加权或 task-aware fine-tuning。

## 十二、ALBERT 式 Embedding–Hidden 解耦

若原模型把 token 直接映到 hidden width $H$，词表参数为 $VH$。使用较小 embedding width $E_d$：

$$
\text{token row}\in\mathbb R^{E_d},
\qquad
x=P e\in\mathbb R^H,
$$

参数为

$$
VE_d+E_dH.
$$

它让 vocabulary capacity 不随 hidden width 等比例增长。注意 ALBERT 还使用跨层参数共享和不同预训练设计；实验收益不能全部归因于 factorized embedding。

## 十三、Frequency-Adaptive Dimension

把词表按频率分组 $g=1,\ldots,G$，组大小 $V_g$、dimension $d_g$：

$$
\sum_gV_g=V,
\qquad
d_1\ge d_2\ge\cdots\ge d_G.
$$

表参数为

$$
\sum_gV_gd_g.
$$

若每组投影到共同 hidden width $H$，还要加

$$
\sum_g d_gH
$$

或相应共享 projection。频率变化、domain shift 和 rare-but-critical tokens 会挑战“低频即低容量”的假设；token-to-group map 属于 checkpoint contract。

## 十四、Uniform Affine Quantization

对一个 row 或 block，选择 scale $s>0$ 与 zero-point $z_0$：

$$
q_j
=\operatorname{clip}
\left(
\operatorname{round}(e_j/s)+z_0,
q_{\min},q_{\max}
\right),
$$

反量化：

$$
\widehat e_j=s(q_j-z_0).
$$

若没有 clipping 且 round-to-nearest，则每坐标

$$
|\widehat e_j-e_j|\le\frac s2.
$$

于是 row error：

$$
\boxed{
\|\widehat e-e\|_2
\le\frac{\sqrt d\,s}{2}
}.
$$

若发生 clipping，还要额外加入超出量化区间的误差，简单 $s/2$ 界不再成立。

## 十五、从 Row Error 到 Logit Error

若 output logit 为

$$
z=e^\mathsf Th,
\qquad
\widehat z=\widehat e^\mathsf Th,
$$

则 Cauchy–Schwarz 给出

$$
\boxed{
|\widehat z-z|
\le\|\widehat e-e\|_2\|h\|_2
}.
$$

结合无 clipping row bound：

$$
|\widehat z-z|
\le\frac{\sqrt d\,s}{2}\|h\|_2.
$$

所以量化 scale、hidden norm 与 vocabulary margin 共同决定 argmax 是否改变。仅报告平均 weight MSE 不能证明 next-token distribution 稳定。

## 十六、手算：INT4 Raw Codes

仍取 $V=50{,}000,d=1024$。4-bit codes 原始位数：

$$
Vd\times4
=204{,}800{,}000\ \text{bits}.
$$

换成字节：

$$
25{,}600{,}000\ \text{bytes}=25.6\ \mathrm{MB}.
$$

相对 FP16 的 102.4 MB，raw codes 是 4 倍缩小。但真实存储还包含：

- per-tensor/per-row/per-block scales；
- zero-points；
- packing/alignment；
- codebooks（向量/乘积量化）；
- kernel workspace；
- tied output 的 dequant/matmul layout。

因此完整压缩率小于 raw $16/4=4$，除非 metadata 可忽略。

## 十七、Per-Tensor、Per-Row 与 Per-Block

- **per-tensor**：metadata 最少，但 outlier row 决定全表 scale；
- **per-row**：适应 token norm，metadata 为 $O(V)$；
- **per-block/channel**：更细动态范围，metadata/访存和 kernel 更复杂；
- **vector/product quantization**：每 row 保存 code indices，多个 codebooks 重构，误差/查表路径不同。

最佳粒度取决于 norm heterogeneity、硬件向量宽度、访问模式和是否作为 output matrix。

## 十八、PTQ、QAT 与训练状态

### Post-Training Quantization（PTQ）

训练 full precision 后校准/量化。便宜，但 rare/outlier rows、tied logits 与生成敏感性可能造成质量下降。

### Quantization-Aware Training（QAT）

forward 模拟 quantization，backward 常用 straight-through estimator。可适应误差，但 estimator、本体/scale 更新和最终 kernel 必须匹配。

### Training-State Boundary

即使 inference weight 是 INT4，训练可能仍保存：

- FP16/BF16 working copy；
- FP32 master weight；
- FP32 moments；
- gradients 与 calibration state。

所以 inference compression 不等于 training-memory compression。

## 十九、Tying 下的压缩接口

共享 $E$ 同时服务 gather 与 full-vocabulary matmul：

- row-wise quantized gather 可能很快；
- output GEMM 需要适配 packed layout 或 dequant；
- input reconstruction error 与 output logit error共享同一 codes；
-只量化一处却复制出另一份 dense output 会破坏 tying 和内存收益；
- factorized tying 需明确 $E=AB$ 后 output 是 $ABh$ 还是先缓存 $E$。

因此必须测试 Parameter/storage identity 和实际 kernel，而不只看 state-dict key 数。

## 二十、选择与验收的 Pareto 账本

每个方案至少报告：

1. **函数类**：rank、group dimensions、tying/projection；
2. **数值误差**：row MSE/max、cosine、logit/NLL perturbation；
3. **质量**：overall/rare/special-token NLL、top-k、校准；
4. **存储**：weights、metadata、optimizer、checkpoint；
5. **计算**：lookup latency、output GEMM、dequant、batch occupancy；
6. **通信**：shard bytes、all-to-all、checkpoint IO；
7. **训练**：收敛步数、update floor、QAT estimator；
8. **部署**：kernel 可用性、fallback 与 deterministic reload。

可以画 parameter bytes–latency–NLL 三维 Pareto，而不是只报一个“压缩率”。

## 二十一、常见误区

1. **“$1/\sqrt d$ 初始化总是正确”**：还取决于 hidden、runtime scale 与 tying；
2. **“factorization 只改存储”**：rank 和 lookup compute 都变；
3. **“参数少 8 倍就快 8 倍”**：kernel、projection 和带宽不同；
4. **“SVD 最优等于 task 最优”**：优化 norm 不同；
5. **“INT4 就精确压缩 4 倍”**：metadata/state/layout 未计；
6. **“平均 MSE 小就不改生成”**：rare row、margin 与 error direction 关键；
7. **“量化输入表不影响 tied output”**：共享 codes 同时扰动 logits；
8. **“推理内存就是训练内存”**：master/moments 可占主导。

## 二十二、图：Scale、Factorization 与 Quantization

先看图回答：为什么 $d\sigma_E^2$ 同时出现在 row norm 与 tied logit variance？$r=128$ 的分解节省多少参数却增加什么计算？INT4 的 25.6 MB 为什么不是完整部署/训练内存？

![[00-知识库管理/_assets/figures/neural-networks/fig-embedding-scale-compression-v2.svg|900]]

> [!figure] 图 30.7-08　Embedding 初始化二阶矩、低秩分解与 row-wise quantization
> 左栏并列 lookup row norm 与 tied output logit variance；中栏展示 $E=AB$、rank constraint 和 $51.2$M→$6.531$M 的参数手算；右栏给出 affine dequantization、row/logit error bound 及 FP16/INT4 raw bytes。来源：依据 ALBERT、adaptive input、Tao et al. 量化研究与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_embedding_output_advanced_v2.py]] 确定性生成。

**怎样读图**：先用二阶矩校准未压缩 baseline；再分别记录 factorization 的 rank/compute 与 quantization 的 reconstruction/logit error；最后把 metadata、master state 和真实 kernel 加回系统账。

**图没有证明什么**：图不证明 $r=128$ 或 INT4 适合任意任务，也不证明 raw parameter bytes 会按相同比例转化为 wall-time、energy 或质量收益。

## 二十三、最小验收

1. 推导 row norm 与 tied logit variance；
2. 区分 init/runtime scale/normalization；
3. 推导 $r<Vd/(V+d)$；
4. 复算 6,531,072 参数与 7.84x；
5. 推导 $A,B$ 的 lookup gradients 与 gauge；
6. 写出 truncated-SVD balanced factors；
7. 给出 adaptive-dimension 完整参数账；
8. 推导 $\sqrt d\,s/2$ row error 和 logit bound；
9. 复算 INT4 raw 25.6 MB；
10. 设计 rank/error/state/kernel/quality Pareto 验收。

> [!summary]
> Embedding 的规模治理不是单一压缩技巧。初始化先决定 row 与 logit 的二阶矩；低秩/自适应维度改变可表示空间；量化把连续 rows 映到有限 codes 并引入可传播到 logits 的误差。只有把函数类、误差、训练状态、访问计算、output tying 与端到端质量同时入账，参数减少才成为可信的系统收益。

- [[Embedding、权重共享与输出参数化 MOC]]
- [[习题 - Embedding 初始化、缩放、分解与量化接口]]
- [[解答 - Embedding 初始化、缩放、分解与量化接口]]
