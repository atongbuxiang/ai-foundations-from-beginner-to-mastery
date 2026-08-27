---
type: solution
status: draft
area: [neural-networks/normalization, vision, parameterization]
topic: "[[InstanceNorm、GroupNorm 与 WeightNorm]]"
exercise: "[[习题 - InstanceNorm、GroupNorm 与 WeightNorm]]"
sources: ["[[S-2016-Ulyanov-Vedaldi-Lempitsky-InstanceNorm]]", "[[S-2018-Wu-He-GroupNorm]]", "[[S-2016-Salimans-Kingma-WeightNorm]]", "[[S-2026-PyTorch-Normalization-Systems]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - InstanceNorm、GroupNorm 与 WeightNorm

## A

### NN-NGW-A01
InstanceNorm2d 固定 $(n,c)$、归约 $(h,w)$；组数 $NC$，组大小 $HW$，常见 affine 为 $(C)$ 并沿 $N,H,W$ 广播。

GroupNorm$(G)$ 固定 $(n,g)$、归约组内 $C/G$ 个 channels 与 $(h,w)$；组数 $NG$，组大小 $(C/G)HW$，常见 affine 仍为 $(C)$。两者输出都保持 $(N,C,H,W)$。

### NN-NGW-A02
$G=1$ 时 GN 与归约 $(C,H,W)$ 的 LN 统计核心相同；但 GN affine 为 per-channel $(C)$，LN$((C,H,W))$ 为 per-element $(C,H,W)$。

$G=C$ 时 GN 与 IN 的统计核心都固定 $(n,c)$ 归约 $(H,W)$；但 affine defaults、running-state 能力与 API 仍可能不同。完整等价需要统计组、variance/epsilon、affine sharing 和 state 全部一致。

### NN-NGW-A03
WeightNorm 的输入对象是权重参数，而不是 activation：

$$
w=g\frac v{\|v\|}.
$$

它没有 batch statistics/running buffers，不引入样本 companions，train/eval 的有效权重公式相同。它不保证 activation 均值/方差，也不固定完整矩阵 spectral norm 或层 Lipschitz 常数。

## B

### NN-NGW-B01
IN 对每个 pair 独立：

$$
(1,3)\to(-1,1),
\quad
(5,7)\to(-1,1),
$$

$$
(0,4)\to(-1,1).
$$

$(2,2)$ 方差 0；$\varepsilon=0$ 未定义，$\varepsilon>0$ 时 centered numerator 为 0，输出 $(0,0)$。

GN $G=2$：第一组 $(1,3,5,7)$ 有 $\mu=4,q=5$，输出

$$
\frac1{\sqrt5}(-3,-1,1,3).
$$

第二组 $(2,2,0,4)$ 有 $\mu=2,q=2$，输出

$$
(0,0,-\sqrt2,\sqrt2).
$$

### NN-NGW-B02
$$
r=5,
\quad u=(3/5,4/5),
\quad w=10u=(6,8).
$$

$$
dg=s^{\mathsf T}u=\frac35+\frac85=\frac{11}{5}.
$$

$$
(I-uu^{\mathsf T})s
=(1,2)-\frac{11}{5}(3/5,4/5)
=(-8/25,6/25).
$$

乘 $g/r=2$：

$$
dv=(-16/25,12/25).
$$

$$
v^{\mathsf T}dv
=3(-16/25)+4(12/25)=0.
$$

### NN-NGW-B03
这里 $HW=1$：

- $G=1$：组大小 $m=4$，非零组方差时可保留 $m-2=2$ 个切向方向；
- $G=2$：每组 $m=2$，$\varepsilon=0$、两值不同时 normalized core 局部只剩符号，Jacobian 几乎处处为 0；
- $G=4$：每组 $m=1$，centering 删除全部输入，$\varepsilon>0$ 时 core 恒为 0。

所以应看 $(C/G)HW$，不能只看 $G$。

## C

### NN-NGW-C01
令 $r=\|v\|,u=v/r$。有

$$
dr=u^{\mathsf T}dv,
$$

$$
du=\frac1r dv-\frac v{r^2}dr
=\frac1r(I-uu^{\mathsf T})dv.
$$

对 $w=gu$：

$$
dw=u\,dg+g\,du.
$$

令 $s=\nabla_wL$，由 $dL=s^{\mathsf T}dw$ 收集系数：

$$
dg=s^{\mathsf T}u,
$$

$$
dv=\frac g r(I-uu^{\mathsf T})s.
$$

$I-uu^{\mathsf T}$ 是投到单位球面切空间 $u^\perp$ 的正交投影。

### NN-NGW-C02
对 $a>0$：

$$
g\frac{av}{\|av\|}
=g\frac{av}{a\|v\|}
=g\frac v{\|v\|}.
$$

在 $av$ 处，单位方向仍是 $u$，但 denominator 变成 $ar$：

$$
\nabla_{av}L
=\frac g{ar}(I-uu^{\mathsf T})s
=\frac1a\nabla_vL.
$$

固定坐标学习率下，放大 $\|v\|$ 会缩小 raw direction gradient；相同有效权重的不同 gauge 具有不同参数步长，因此 optimizer/weight decay 语义需审计。

### NN-NGW-C03
对组向量 $x\in\mathbb R^m$，$\varepsilon=0,q>0$，centered norm Jacobian 是

$$
J=\frac1r\left(P-\frac1m\widehat x\widehat x^{\mathsf T}\right),
\quad
P=I-\frac1m11^{\mathsf T}.
$$

$1$ 与 $\widehat x$ 是两个线性无关零方向；同时正交于二者的子空间维数为 $m-2$，其 eigenvalue 为 $1/r$。故 rank 为 $m-2$。GN 的每组若很小，就只保留很少连续局部方向；$m=1,2$ 是严重退化。

## D

### NN-NGW-D01
取 $C=2,H=W=2$。GN$(1,2)$ affine 只有 $2C=4$ 个参数；LayerNorm$((2,2,2))$ affine 有

$$
2CHW=16
$$

个参数。即使 normalized core statistics 相同，后者可以对每个空间位置使用不同 gain/bias，完整函数族不同。

### NN-NGW-D02
例如 PyTorch InstanceNorm2d 允许 `track_running_stats=True`。训练时用当前 instance statistics 并更新 buffers；eval 时改用 running estimates。此时 train/eval 是不同统计路径。只有明确 `track_running_stats=False` 等合同后，才能说两种 mode 都使用当前输入统计。

### NN-NGW-D03
取矩阵

$$
W=\begin{bmatrix}1&0\\1&0\end{bmatrix}.
$$

两行的 Euclidean norm 都为 1，可由 per-row WeightNorm 的 $g_1=g_2=1$ 实现。但

$$
W^{\mathsf T}W
=\begin{bmatrix}2&0\\0&0\end{bmatrix},
$$

所以

$$
\|W\|_2=\sqrt2>1.
$$

行范数固定不控制行之间的对齐，也不固定完整 spectral norm。

## E

### NN-NGW-E01
公平协议至少固定 backbone、参数量/训练 schedule、augmentation、optimizer、预训练与 image resolution；分别调合理 learning rate。记录 actual group size、BN batch-stat variance、GN group count、activation/gradient norms、wall time 和多 seed accuracy。Wu–He 的特定 ResNet/检测/分割结果不能直接推出任意 backbone、数据域或现代训练配方上 GN 必胜。

### NN-NGW-E02
IN 删除每个样本、每 channel 的空间均值与尺度，可能抹去绝对 CT/MRI intensity、全局病灶亮度或扫描协议信号。方案包括：保留原强度旁路/全局统计作为额外 features；只在部分 channels 使用 IN；用 GN/LN 对照；做强度保持与强度扰动两轨实验；按设备/病人分层评价，确认收益不是泄漏扫描器标签。

### NN-NGW-E03
- LN：对每个 hidden vector 归约 features，无 companions；直接控制 activation，但会删除共同 shift。
- GN：需定义 hidden channels 的 group 结构；无 batch 依赖，但组内 features 耦合，适合有合理 channel grouping 的张量。
- WN：只重参数化 recurrent/generator weights，无 activation statistics；保留样本独立，但改变 optimizer/weight-decay 坐标。

选择取决于目标是控制 activation geometry 还是 weight geometry、是否需要 shift 不变性、隐藏 shape/group 是否有语义，以及是否接受参数化带来的优化状态变化。

