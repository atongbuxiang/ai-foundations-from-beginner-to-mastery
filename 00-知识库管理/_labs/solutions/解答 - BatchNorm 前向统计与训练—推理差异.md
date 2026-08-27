---
type: solution
status: draft
area: [neural-networks/normalization, batch-normalization, inference]
topic: "[[BatchNorm 前向统计与训练—推理差异]]"
exercise: "[[习题 - BatchNorm 前向统计与训练—推理差异]]"
sources: ["[[S-2015-Ioffe-Szegedy-BatchNorm]]", "[[S-2026-PyTorch-Normalization-Semantics]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - BatchNorm 前向统计与训练—推理差异

## A

### NN-BNF-A01
对 $(N,C)$，固定 $c$ 归约 $n$，每组大小 $N$；对 $(N,C,H,W)$，固定 $c$ 归约 $(n,h,w)$，每组大小 $NHW$。两者 $\gamma,\beta$ 都是 $(C)$，按非 channel 轴广播；输出 shape 与输入相同。

### NN-BNF-A02
Current batch statistics 是本次输入的经验 $\mu_B,q_B$；population moments 是当前模型/数据分布下的理论 $\mu^\star,q^\star$；running buffers 是跨历史 batches 的状态估计。常见训练输出直接用 current $\mu_B,q_B$，同时用 batch observations 更新 running buffers；population moments 通常既不精确可得也不直接存储。

### NN-BNF-A03
访问日 PyTorch 2.13：训练 forward variance 用 correction=0；更新 running variance 的当前 observation 用 correction=1。更新
$$
s_{\rm new}=(1-a)s_{\rm old}+a s_t.
$$
track-running-stats 为 false 时不维护 buffers，eval 也用当前 batch statistics，故仍依赖 companions。

## B

### NN-BNF-B01
原 batch：
$$
\mu=2,\quad q=1,\quad\widehat x=(-1,1),\quad y=(-3,1).
$$
把 3 改成 5 后：
$$
\mu=3,\quad q=4,\quad\widehat x=(-1,1),\quad y=(-3,1).
$$
第一个输出没有改变。原因是 $m=2,\varepsilon=0$ 的特殊退化：任意两个不同数标准化后总是 $(-1,1)$ 或相反顺序。它不否定 batch coupling；取三点、非零 epsilon 或把两值变相等即可观察改变。例如 $(1,3,5)$ 改成 $(1,3,9)$ 时第一个 normalized value 从 $-\sqrt{3/2}$ 变为 $-10/\sqrt{104}$。

### NN-BNF-B02
正确更新：
$$
\bar\mu_{\rm new}=0.9(0)+0.1(4)=0.4,
$$
$$
\bar q_{\rm new}=0.9(1)+0.1(9)=1.8.
$$
若误把 0.1 当旧值系数：
$$
\bar\mu=0.1(0)+0.9(4)=3.6,
$$
$$
\bar q=0.1(1)+0.9(9)=8.2.
$$
两者有效时间尺度完全不同。

### NN-BNF-B03
固定 scale
$$
a=\gamma/\sqrt{\bar q}=4/2=2.
$$
故
$$
W'=aW=6,
\qquad
b'=a(b-\bar\mu)+\beta=2(2-5)-1=-7.
$$
原路径在 $x=1$ 时 $z=5$，BN 输出 $2(5-5)-1=-1$；折叠路径 $6(1)-7=-1$。

## C

### NN-BNF-C01
若 $z_i=w^{\mathsf T}x_i+b$ 且组内共享 $b$，
$$
z_i-\mu_z=w^{\mathsf T}x_i+b-(w^{\mathsf T}\mu_x+b)
=w^{\mathsf T}(x_i-\mu_x).
$$
证明不适用于：bias 在组内随位置变化；前层输出还有旁路消费者；BN 不做 centering；eval buffers 与当前 $b$/模型不配套；或 affine/分组使该 bias 不再共同。

### NN-BNF-C02
令 $\bar X=m^{-1}\sum_iX_i$。恒等式
$$
\sum_i(X_i-\bar X)^2
=\sum_i(X_i-\mu)^2-m(\bar X-\mu)^2.
$$
取期望，第一项为 $m\sigma^2$，第二项为
$$
m\operatorname{Var}(\bar X)=m(\sigma^2/m)=\sigma^2.
$$
故平方和期望为 $(m-1)\sigma^2$，除以 $m$ 得
$$
\mathbb E[q_B]=\frac{m-1}{m}\sigma^2.
$$
使用了 IID、有限二阶矩。

### NN-BNF-C03
eval 时
$$
y_c=\frac{\gamma_c}{\sqrt{\bar q_c+\varepsilon}}
(W_cx+b_c-\bar\mu_c)+\beta_c.
$$
令 $a_c=\gamma_c/\sqrt{\bar q_c+\varepsilon}$，收集 $x$ 与常数项即得
$$
W'_c=a_cW_c,\quad
b'_c=a_c(b_c-\bar\mu_c)+\beta_c.
$$
train-mode 的 $\mu_B,q_B$ 是当前整组 $X$ 的函数，不是固定参数；无法用一个对单样本固定的 $W',b'$ 表示。

## D

### NN-BNF-D01
BN 只使有限组 affine 前 mean 为 0、平方均值为 $q/(q+\varepsilon)$。任意偏斜、双峰、重尾 empirical distribution 都可满足这两个矩；channel 间 covariance 未处理；affine 还会改变 mean/scale。因此标准正态与 independence 都不成立。

### NN-BNF-D02
BN running update常写
$$
s_{t+1}=(1-a)s_t+a\,\widehat s_t,
$$
其中 $a$ 是新 observation 权重。Optimizer momentum 的经典速度式可写
$$
v_{t+1}=\rho v_t+g_t,\qquad
\theta_{t+1}=\theta_t-\eta v_{t+1},
$$
其中 $\rho$ 是旧速度保留系数。两者对象、单位和系数方向均不同；同名不代表同义。

### NN-BNF-D03
四个 microbatches 各自计算四套 $\mu_k,q_k$，所以 forward activations、loss 和每层 Jacobian 已不同；gradient accumulation 只在末端把四次 parameter gradients 相加，不能重建用完整 batch statistics 的计算图。Running buffers 还会更新四次而非一次。只有冻结统计量或显式跨 microbatch 汇总 sufficient statistics 才可能接近等价。

## E

### NN-BNF-E01
审计：(1) 保存 $\gamma,\beta$；(2) 保存 running mean/var 与 batch counter；(3) 确认 train/eval；(4) 确认 track state；(5) validation 前切 eval，防止污染；(6) fine-tune 时分别决定参数与 buffers 是否更新；(7) 比较部署域 moments；(8) folding 用最终固定 buffers；(9) folding 前后逐层/端到端对比；(10) 导出格式保留 dtype/epsilon；(11) rollback/checkpoint 重载 state；(12) 若 eval 仍用 batch stats，明确 batching contract。

### NN-BNF-E02
扫描 per-device batch size 与有效 $NHW$，固定 architecture、global optimizer batch、data order、augmentation、LR schedule、precision、normalization placement 与 paired seeds。逐层记录 $\mu_B,q_B$ 的跨 step 方差、running 与 held-out moments 差、固定 probe 的 train/eval output gap、nonfinite/clipping 和最终 metric 的 seed 分布。Spatial correlation 与 SyncBN 作为独立变量；不能把单 seed 最终 accuracy 差归因于 statistics。

### NN-BNF-E03
生成多个 channels 的 Conv/Linear，覆盖 bias on/off、随机非零 $\gamma,\beta$、多组 running stats 与 epsilon。先 eval 得参考 $Y$，按公式折叠后得 $Y'$；报告 max absolute、relative norm 与 task output error。fp32 以紧容差验算，fp16 分开报告 quantization/fused rounding。保存加载折叠前后各一次，确认 buffers/weights 不漂移；只声明固定 eval graph 等价，不推广到 train mode 或新统计域。

