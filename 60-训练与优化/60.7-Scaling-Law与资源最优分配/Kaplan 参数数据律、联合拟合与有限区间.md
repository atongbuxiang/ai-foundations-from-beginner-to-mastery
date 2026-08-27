---
type: derivation
status: verified
area: [training, scaling-laws, language-models, joint-modeling]
node_id: TRN-50
aliases: [Kaplan Scaling Laws, Joint Parameter Data Scaling]
prerequisites: ["[[经验 Scaling Law、幂律拟合与不可约项]]", "[[训练时域、Restart、Schedule-Free 与末端学习率]]", "[[模型尺度、稳定性指标与 Width-Depth 对象合同]]"]
related: ["[[Chinchilla、Compute-optimal 参数与数据分配]]", "[[IsoFLOP、训练算力口径与系统校正]]", "[[Scaling 实验设计、外推不确定性与证据地图]]"]
sources: ["[[S-2020-Kaplan-语言模型尺度定律]]", "[[S-2022-Hoffmann-计算最优训练]]", "[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]]", "[[S-2024-Pearce-Song-Reconciling-Kaplan-Chinchilla]]"]
exercises: ["[[习题 - Kaplan 参数数据律、联合拟合与有限区间]]"]
solutions: ["[[解答 - Kaplan 参数数据律、联合拟合与有限区间]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-kaplan-joint-bottleneck-surface-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Kaplan 参数数据律、联合拟合与有限区间

> [!abstract] 一句话结论
> 参数量 $N$、数据量 $D$ 与训练充分度不是三条可以各自独立外推的直线。单变量 scaling curve 只有在另外两个瓶颈被控制时才可解释；否则观测 slope 混合了模型受限、数据受限与优化受限。Kaplan 与 Chinchilla 的分歧正说明 parameter count、compute、warmup 和调参协议都属于“定律”的实验定义。

## 一、三类变量先分账

本卷使用：

- $N$：明确口径的模型参数量；
- $D$：训练中消费的 token 数，另行说明 unique/repeated；
- $C$：明确公式或测量方法的训练 compute；
- $T$：optimizer successful updates 或 token clock；
- $L$：固定 validation distribution 上的 terminal/selected loss。

同一个“1B 参数模型”可能指：

1. total stored parameters；
2. non-embedding parameters；
3. 每 token active parameters；
4. trainable parameters；
5. dense-equivalent parameters。

这些数字在大 dense model 中有时近似成比例，在小模型、巨大词表、weight tying 或 MoE 中并不等价。

## 二、Marginal Law 的条件语义

参数边际律常写成

$$
L_N(N)=E_N+A N^{-\alpha},
\tag{1}
$$

数据边际律常写成

$$
L_D(D)=E_D+B D^{-\beta}.
\tag{2}
$$

它们不是说“任意固定其他量时都成立”，而是说：

- 估计 $L_N$ 时，数据与优化不能先成为主要瓶颈；
- 估计 $L_D$ 时，模型容量与优化不能先饱和；
- loss、tokenizer、数据分布、架构 family 和训练选择保持一致。

若固定 $D$ 增大 $N$，曲线最终会撞上 data floor；若固定 $N$ 增大 $D$，最终会撞上 capacity floor。把撞墙之后的点仍拿来估计原 exponent，会得到更平的 slope。

## 三、一个教学用联合曲面

为训练推导，先考虑 additive reducible-loss 模型

$$
L_\infty(N,D)
=E+A N^{-\alpha}+B D^{-\beta}.
\tag{3}
$$

这里下标 $\infty$ 表示“给定 $N,D$ 后优化已充分”，不是 $N,D\to\infty$。

式 (3) 的优点是透明：

$$
\frac{\partial L_\infty}{\partial\log N}
=-\alpha A N^{-\alpha},
\qquad
\frac{\partial L_\infty}{\partial\log D}
=-\beta B D^{-\beta}.
\tag{4}
$$

它把参数和数据的边际收益分开。

缺点同样重要：

- 真实 $N,D$ 可能交互；
- 训练 tokens 与 unique data 不同；
- architecture/optimizer 可能随规模改变；
- $E$ 可能依赖 evaluation distribution。

所以式 (3) 是课程的可推导 baseline，不冒充 Kaplan 原文所有联合公式。

## 四、把优化不足加入曲面

实际观测 terminal loss 可写成

$$
L_{\rm obs}(N,D,T)
=L_\infty(N,D)+G(N,D,T;\mathcal O),
\tag{5}
$$

其中 $G\ge0$ 是在 optimizer/schedule $\mathcal O$ 下的 optimization gap。

一个教学模型是

$$
G=H(N,D)T^{-\gamma}.
\tag{6}
$$

若所有规模固定相同步数，而较大模型的 $H$ 更大或每步 token/FLOPs 不同，那么较大模型会显得“参数收益较小”。反过来，如果每个规模都独立调到最佳 checkpoint，选择预算又随规模增加，也会让大模型显得额外有利。

因此报告需要同时给：

- successful updates、seen tokens 和 FLOPs；
- warmup/decay 占比；
- 每规模超参数搜索预算；
- last/best/EMA checkpoint；
- optimization-gap proxy，例如继续训练后的 loss 改善。

## 五、Kaplan 结果的正确身份

[[S-2020-Kaplan-语言模型尺度定律]] 在其模型族与实验制度内观察到：

- loss 对 $N,D,C$ 的广范围经验规律；
- larger models 的样本效率优势；
- 固定 compute 下较大模型、较少数据、较早停止的 allocation。

正确表述是“在该协议的有限尺度范围内，某个经验函数族拟合并支持一种 compute allocation”。错误表述是“语言模型存在普遍不变的 Kaplan 指数”。

后续 [[S-2022-Hoffmann-计算最优训练]] 用更广 IsoFLOP 设计得到不同 allocation，正是经验科学修订，而不是数学定理互相矛盾。

## 六、为什么 Kaplan 与 Chinchilla 会分歧

### 1. Parameter counting

[[S-2024-Pearce-Song-Reconciling-Kaplan-Chinchilla]] 强调 total 与 non-embedding parameters。在小模型中若 vocab embedding 为 $Vd$、block 参数近似 $kLd^2$，则

$$
\frac{N_{\rm embed}}{N_{\rm block}}
\approx\frac{V}{kLd}.
\tag{7}
$$

随 $d,L$ 变化，这个比例不恒定。横轴口径变化会改变 finite-window slope。

### 2. Last-layer compute

大词表 readout 的 FLOPs 不总与 non-embedding $N$ 同比例；忽略它会使小模型 compute 估计偏差更大。

### 3. Warmup 与训练时域

若所有模型使用固定 warmup tokens，warmup 占总预算比例可随 run length 改变；若固定 steps，global batch 又会改变 warmup tokens。

### 4. Scale-dependent tuning

学习率、batch、$\beta_2$ 或 parameterization 若没有随规模重新公平调节，曲线包含 optimizer mismatch。[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]] 用复现干预展示这些因素可解释很大一部分分歧。

## 七、有限区间怎样制造指数偏差

设 block parameters 为 $a d^2$、embedding 为 $b d$。真实 loss 对 block scale 为

$$
L-E=K(ad^2)^{-\alpha}.
\tag{8}
$$

但若横轴误用 total

$$
N_{\rm total}=ad^2+bd,
\tag{9}
$$

则局部 elasticity 是

$$
-\frac{d\log(L-E)}{d\log N_{\rm total}}
=\alpha
\frac{d\log(ad^2)}{d\log N_{\rm total}},
\tag{10}
$$

更直接计算得

$$
\frac{d\log(ad^2)}{d\log(ad^2+bd)}
=2\frac{ad+b}{2ad+b}.
\tag{11}
$$

当 $d$ 小、embedding 占比大时，该因子接近 2；当 block 主导时趋近 1。也就是说，参数口径的非线性关系本身就能让局部 exponent 随尺度漂移。

## 八、联合拟合的验收问题

给定 $(N_i,D_i,T_i,L_i)$，不要直接把所有点塞进式 (3)。先问：

1. 是否有相同 $N$、不同 $D$ 的切片？
2. 是否有相同 $D$、不同 $N$ 的切片？
3. 是否有近似相同 $C$ 的 IsoFLOP slices？
4. 每个 cell 是否优化充分且预算匹配？
5. 参数与 compute 口径是否在所有规模一致？
6. 最大 scales 是否留作 held-out？

若只有一条共同增长路径 $D\propto N^q$，则

$$
L-E=A N^{-\alpha}
+B' N^{-q\beta},
\tag{12}
$$

观测曲线很难单独识别 $\alpha,\beta$。这叫设计层面的不可识别，不是更强优化器能修复的问题。

## 九、图：三个瓶颈与联合曲面

先看图回答：为什么沿单条对角 scale path 下降良好，仍不能知道改善来自 $N$ 还是 $D$？哪个面板表示优化 gap 污染了本应相同的联合曲面？

![[00-知识库管理/_assets/figures/training-optimization/fig-kaplan-joint-bottleneck-surface-v1.svg|900]]

> [!figure] 图 TRN-50-01　Model、data、optimization 三瓶颈与联合识别
> 来源：课程原创教材图；左侧用三个一维截面区分 parameter-limited、data-limited、optimization-limited；右侧用 $N\times D$ 网格说明只有多方向切片才能识别联合曲面。概念依据：[[S-2020-Kaplan-语言模型尺度定律]]、[[S-2024-Porian-Resolving-Compute-Optimal-Scaling]]。

**怎样读图**：先找到哪个 gap 主导，再看实验是否同时改变 $N,D,T$；最后检查同 compute 或同一变量切片是否存在。

**图没有证明什么**：示意曲面不等于 Kaplan 的具体拟合函数，也不证明三个 gap 可严格相加；它用于识别设计混杂。

## 十、允许与禁止的结论

允许：

> 在固定 tokenizer、数据分布、block family、parameter count 和优化协议下，观测窗口内的 joint model 在 held-out scale 上达到给定误差。

禁止：

> 我们画出了 $N,D$ 的两条直线，所以任意未来语言模型的 compute-optimal 比例已经确定。

前者是有限范围经验陈述，后者跨越了函数族、训练充分度、系统口径和 regime change。
