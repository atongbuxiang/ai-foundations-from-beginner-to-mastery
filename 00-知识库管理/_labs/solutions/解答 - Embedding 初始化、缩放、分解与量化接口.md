---
type: solution
status: draft
area: [neural-networks/embedding-output, embedding-initialization, factorization, quantization]
topic: "[[Embedding 初始化、缩放、分解与量化接口]]"
exercise: "[[习题 - Embedding 初始化、缩放、分解与量化接口]]"
sources: ["[[S-2020-Lan-ALBERT]]", "[[S-2019-Baevski-Auli-Adaptive-Input]]", "[[S-2022-Tao-Quantized-Generative-LM]]", "[[S-2026-PyTorch-Embedding]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Embedding 初始化、缩放、分解与量化接口

## A

### NN-ECQ-A01

对第 $i$ 行，

$$
\mathbb E\|e_i\|_2^2
=\sum_{j=1}^d\mathbb E E_{ij}^2
=d\sigma_E^2.
$$

若目标是平方范数与维度无关的 $O(1)$，需 $d\sigma_E^2=O(1)$，即 $\sigma_E^2=O(1/d)$、标准差 $O(d^{-1/2})$。这是期望平方范数的标度；row norm 的集中程度还依分布尾部，实际输入/输出尺度还受后续 normalization 与 tying 影响。

### NN-ECQ-A02

初始化 scale 只决定 step 0 的 Parameter 值，之后由优化轨迹改变；forward 固定 scale 每次都乘在激活上，并按链式法则持续缩放梯度；LayerNorm/RMSNorm 根据当前 token 的统计量非线性归一化，还含 epsilon、可能的 centering 和可学习 affine。它们对函数、Jacobian、不变性与训练状态的作用不同，即使某一批数据上的输出 norm 恰好相等，也不能互换。

### NN-ECQ-A03

低秩分解 $E=AB$ 把整表限制在 rank-$r$ 行空间，主要改变全局函数类并增加 projection 计算。Frequency-adaptive dimension 给不同频率组不同 $d_g$，主要改变 token-group capacity 与投影结构，未必等于一张统一 rank-$r$ 表。量化把连续 weights 映射为有限 codes，主要引入 reconstruction/logit error；若训练可适应，最终函数也会改变，但它的直接合同是位宽、scale、clipping 与误差。

## B

### NN-ECQ-B01

Full table：

$$
Vd=50{,}000\times1024=51{,}200{,}000
$$

个参数，FP16 本体为 $102{,}400{,}000$ bytes。分解后：

$$
Vr+rd=50{,}000(128)+128(1024)=6{,}531{,}072,
$$

FP16 本体为 $13{,}062{,}144$ bytes，压缩

$$
51{,}200{,}000/6{,}531{,}072\approx7.84\times.
$$

每个 token gather 一个 $r$ 维 code 后还要乘 $B\in\mathbb R^{r\times d}$，约增加 $rd=131{,}072$ MAC。若缓存物化后的 full rows，则这部分计算下降但 $Vd$ 存储回来。

### NN-ECQ-B02

Raw INT4 codes 为

$$
51{,}200{,}000\times4/8=25{,}600{,}000
$$

bytes，是 FP16 的 $1/4$。每 64 weights 一个 FP16 scale，共

$$
51{,}200{,}000/64=800{,}000
$$

个 scales，即 $1{,}600{,}000$ bytes。总计 $27{,}200{,}000$ bytes，为 FP16 的 $26.5625\%$，实际压缩约 $3.76\times$。这仍未计 zero-points、alignment、index、workspace 与 fallback copy。

### NN-ECQ-B03

无 clipping、round-to-nearest 时

$$
\|\widehat e-e\|_2\le\frac{\sqrt d\,s}{2}
=\frac{32(0.02)}2=0.32.
$$

由 Cauchy–Schwarz，

$$
|\widehat z-z|
\le\|\widehat e-e\|_2\|h\|_2
\le0.32(10)=3.2.
$$

这是很松的最坏界；若有 clipping，第一步界本身失效，必须另加 clipping residual。

## C

### NN-ECQ-C01

令上游列梯度 $g=\nabla_eL\in\mathbb R^d$。因 $e=B^\mathsf Ta$，

$$
dL=g^\mathsf TdB^\mathsf Ta+g^\mathsf TB^\mathsf Tda,
$$

所以

$$
\nabla_BL=ag^\mathsf T,
\qquad
\nabla_aL=Bg.
$$

又因 $a=A^\mathsf Tq_i$，

$$
\boxed{\nabla_AL=q_i(Bg)^\mathsf T},
\qquad
\boxed{\nabla_BL=ag^\mathsf T}.
$$

$q_i$ 是 one-hot，因此 $A$ 只有第 $i$ 行收到 lookup 梯度；共享 basis $B$ 的 outer product 通常稠密。

### NN-ECQ-C02

对任意可逆 $R\in\mathbb R^{r\times r}$，

$$
(AR)(R^{-1}B)=A(RR^{-1})B=AB.
$$

但若 $R$ 条件数很大，一个 factor norm 可被放大、另一个缩小；梯度要经过不同尺度的链式变换，有限精度下小量可能下溢、大量可能溢出。普通 weight decay 是 $\|A\|_F^2+\|B\|_F^2$，并不对该 gauge 不变，因此还会选择不同代表元。函数 $AB$ 相同不意味着优化器状态、更新轨迹与量化误差相同。

### NN-ECQ-C03

若 $E=U\Sigma V^\mathsf T$，令

$$
A_0=U_r\Sigma_r^{1/2},
\qquad
B_0=\Sigma_r^{1/2}V_r^\mathsf T.
$$

则 $A_0B_0=U_r\Sigma_rV_r^\mathsf T=E_r$，并且

$$
\|E-E_r\|_F^2=\sum_{k>r}\sigma_k^2.
$$

这只对所有 entries 等权的静态 Frobenius reconstruction 最优。真实任务对 token 频率、rare/special rows、输入路径、tied logits 与 margins 加权不同，且 downstream network 可适应；因此仍需 task-aware fine-tuning 和 held-out NLL/生成验收。

## D

### NN-ECQ-D01

以 $P$ 个参数为例，训练内存不能只记 $0.5P$ bytes 的 INT4 codes。还可能有 dequantized FP16/BF16 working copy $2P$、FP32 master $4P$、gradient $2P$ 或 $4P$、Adam moments $8P$，再加 scales/zero-points、temporary dequant buffers、activations、saved tensors、attention workspace、communication buckets 与 allocator fragmentation。QAT 还可能保存 fake-quant statistics。应从运行时 Parameter/optimizer tensors 与 allocator snapshot逐项核对峰值，并区分 persistent、per-step 与 peak workspace；权重量化通常没有触及主导的 activations 或 optimizer state。

### NN-ECQ-D02

保存前后验证 input gather 与 output projection 引用同一 packed codes/scales object 或明确的共享 codec，而不是各有一份；遍历 state dict、storage pointers 与实际 allocated bytes 检查重复。用小词表枚举比较量化/反量化后的 input rows、全类 logits、NLL 和 top-$k$，并按频率/角色分桶。Profiler 要确认 gather 与 GEMM 都命中预期 quantized kernel，没有 silent dequant-to-dense fallback；再测 batch-size/P50/P95 latency、峰值 workspace和 save/load 后 identity。若某路径必须物化 dense copy，就将它明确计入 tying与内存合同。

### NN-ECQ-D03

持续记录训练分桶频率与部署滑窗频率的 ratio、JS/KL drift，并按 token 监控 NLL、gradient/update norm、row norm、OOV/回退率和关键业务错误。为 rare-but-critical tokens 设置语义 allowlist，不仅按频率分配容量。触发阈值后可把 token 提升到更高维组、增加 residual adapter/code、重新训练分桶，或暂时回退 uniform embedding；迁移需同步 token→group map、projections、optimizer和 checkpoint。用历史/新域混合验证并设置可逆版本，避免线上直接原地重排。

## E

### NN-ECQ-E01

固定 tokenizer、数据、backbone、训练 token、调参预算与 exact evaluation；full 为 reference，rank-$r$ 扫 $r$，adaptive 扫分桶/dimensions，INT8/INT4 分开 PTQ 与 QAT。报告参数 rank/函数类、overall 与频率/特殊-token NLL、校准/top-$k$/生成回归、weight/logit error、weights/metadata/master/moments bytes、训练吞吐、lookup/output P50/P95、峰值 workspace、通信与 energy。给 natural-best 与 matched-quality/parameter 两类 frontier，并保留多随机种子区间。只有 nondominated points 才进入部署候选。

### NN-ECQ-E02

至少有六本账：raw parameter count；实际 weight bytes（metadata/alignment）；训练 state（master、gradient、moments）；activation/workspace peak；计算量与矩阵 shape；memory bandwidth/cache；kernel availability/fallback；通信与 checkpoint IO；收敛步数；质量下降导致的额外计算。低秩还会增加 per-token projection，量化还会增加 dequant，压缩率也不自动改变不相关的 backbone。因而 8 倍参数缩减既不推出 8 倍训练内存，也不推出 8 倍端到端延迟。

### NN-ECQ-E03

先设全局与频率/角色分桶门槛：row $L_2$/cosine/max error、hidden-norm 条件下的 logit perturbation、目标/竞争 token margin 翻转率、exact NLL 与 calibration delta。对 EOS/BOS/PAD、控制 token、低频实体和安全关键词建立固定 regression prompts，检查 top-$k$、停止行为与长序列生成；多 seed/域外集也要通过。发布条件应是所有硬门满足且 latency/bytes 确有收益；监控线上分桶 drift 与错误率，一旦越阈即切回已保存的 full/较高位宽 checkpoint。回滚包必须连同 tokenizer、scales、kernel version 与 mapping 一起版本化。
