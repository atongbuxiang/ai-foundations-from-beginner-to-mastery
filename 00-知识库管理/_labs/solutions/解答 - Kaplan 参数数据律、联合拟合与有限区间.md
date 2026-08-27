---
type: solution
status: verified
area: [training, scaling-laws, language-models]
topic: "[[Kaplan 参数数据律、联合拟合与有限区间]]"
exercise: "[[习题 - Kaplan 参数数据律、联合拟合与有限区间]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Kaplan 参数数据律、联合拟合与有限区间

> [!warning] 使用边界
> “Kaplan 风格”描述研究设计与经验结果，不是一个脱离参数计数、训练路径和数据口径的普遍指数。

## A. 识别与复述

### TRN50-A01
$N$ 是明确口径的参数数；$D$ 是模型实际消费的训练 token 数；$T$ 是优化时间，可用 update/checkpoint 表示；$C$ 是规定边界内的计算量。一步消费约为 batch tokens，故 steps 不等于 tokens；不同 sequence/batch 会改变每步 token。每 token FLOPs 又依赖模型、上下文和稀疏性，故 tokens 也不等于 FLOPs。

### TRN50-A02
边际 fit 固定或消除其他瓶颈，只描述一条切片；joint fit 同时描述 $N,D$ 的二维响应。无穷多个曲面可在所测两条切片上相同，却在内部具有不同加性、乘性或交互项，因此两条边际指数不能唯一决定联合面或 compute-optimal 路径。

### TRN50-A03
$G(N,D,T)=L_{obs}-L_\infty(N,D)$ 是有限优化时间、超参和数值失败留下的优化缺口。若大模型更难优化，较高的 observed loss 可能来自 $G$，而非容量收益耗尽或数据统计极限；需 checkpoint 轨迹、充分训练诊断或显式拟合 $T$ 才能分解。

## B. 手算与构造

### TRN50-B01
$32^{-0.2}=1/2$，$100^{-0.3}=10^{-0.6}\approx0.2512$。故
$$
L(1,1)=9,\quad L(32,1)=7.5,\quad
L(1,100)\approx5.256,\quad L(32,100)\approx3.756.
$$
在 $(32,1)$ 数据项 5 主导，在 $(1,100)$ 参数项 3 主导；$(1,1)$ 两者都大且数据项更大，$(32,100)$ 两项约 1.5 与 1.256，较平衡。

### TRN50-B02
小/大 total 参数为 0.15B 与 1.05B，尺度比为 $1.05/0.15=7$；non-embedding 比为 $1.0/0.1=10$。相同模型对“扩大多少倍”已有两种答案，足以改变横轴斜率。

### TRN50-B03
代入 $D=N^{1/2}$：
$$
L(N)=1+3N^{-0.2}+5N^{-0.15}.
$$
观测是一条两个幂项的和；有限窗口的单幂拟合得到介于 $0.15$ 与 $0.2$ 的表观指数，尾部由更慢的 $N^{-0.15}$ 主导。单路径无法分别控制两个瓶颈。

## C. 推导与证明

### TRN50-C01
固定 $D$，
$$
\frac{\partial\log L}{\partial\log N}
=\frac{N}{L}\frac{\partial L}{\partial N}
=-\alpha\frac{AN^{-\alpha}}{E+AN^{-\alpha}+BD^{-\beta}}.
$$
即使真实参数项指数固定，offset 或数据项越大，观测到的原始 loss 斜率越接近 0。

### TRN50-C02
取两个尺度 $N_2>N_1$。理想收益是 $L_\infty(N_1,D)-L_\infty(N_2,D)$；观测收益还要减去 $G(N_2,D,T)-G(N_1,D,T)$。若后者为正，观测收益更小，曲线更平，强制幂律时通常得到较小的参数指数或更高的 floor。

### TRN50-C03
沿路径 $D=kN^p$，
$$
L-E=AN^{-\alpha}+Bk^{-\beta}N^{-p\beta}.
$$
若 $\alpha=p\beta$，两项严格合并成 $(A+Bk^{-\beta})N^{-\alpha}$，无法分别识别；若接近，在有限动态范围内两列设计矩阵高度共线，参数方差极大。必须使用 crossed grid 或外部约束打破混淆。

## D. 边界、反例与纠错

### TRN50-D01
seen tokens = steps × batch sequences × effective sequence length。改变 batch 或 sequence 后，固定 steps 会改变 $D$；padding、packing 和 token mask 还会改变有效 token。公平参数律至少固定 tokenizer 下的 non-padding seen tokens，并报告 optimizer updates 作为另一维度。

### TRN50-D02
设 total $N_{tot}=N_{core}+N_{emb}$，而 $N_{emb}$ 近似固定。小尺度横轴中固定项占比大，$d\log N_{core}/d\log N_{tot}=N_{tot}/N_{core}$ 大于 1，导致对 total 的局部指数被扭曲。外推到 embedding 占比很小的大模型时，这个映射变化，固定指数不再可靠。

### TRN50-D03
科学问题若问“每个尺度经充分优化后能达到什么”，允许独立调参，但须报告搜索空间、选择规则和不确定性。资源规划若问“在总预算内怎么分配”，超参搜索是实际成本，必须纳入 compute/failure ledger；排除它只能回答 oracle-tuned 条件问题。

## E. AI 迁移

### TRN50-E01
选 $N=(N_0,2N_0,4N_0,8N_0)$ 与 $D=(D_0,2D_0,4D_0,8D_0)$ 做 16 个 crossed cells，每格至少多 seed；保存 25%、50%、75%、100% token checkpoints。共享预注册调参规则，同时记录 per-scale tuned 对照，拟合 $L_\infty(N,D)$ 与随 checkpoint 收敛的 $G$。

### TRN50-E02
审计表至少问：total/nonembedding/active/trainable 哪个 $N$；tokenizer、去 padding、unique/seen 哪个 $D$；model/hardware 哪个 $C$；每规模训练到什么停止规则；学习率、batch、warmup 如何缩放；是否用最优 seed；loss 的数据版本与聚合；embedding/last-layer compute 是否纳入；失败与搜索成本是否留痕。

### TRN50-E03
先统一纵轴 loss/数据/tokenizer，再统一参数和 compute 计数；比较模型 family、规模窗口与 $N$–$D$ 路径；检查训练充分度、超参是否 locked、误差模型、offset 与函数族；最后用共同原始点重拟合并做 held-out。只有对象合同和分析选择对齐后仍有不相容区间，才讨论真实经验差异。

## 无提示重做

- [ ] 从单条 $D=kN^p$ 路径重建不可辨识反例。
- [ ] 审计一篇论文的 $N,D,T,C$ 四维账本。
