---
type: solution
status: draft
area: [neural-networks/normalization, layer-normalization, geometry]
topic: "[[LayerNorm 的逐样本几何与反向传播]]"
exercise: "[[习题 - LayerNorm 的逐样本几何与反向传播]]"
sources: ["[[S-2016-Ba-Kiros-Hinton-LayerNorm]]", "[[S-2026-PyTorch-Normalization-Semantics]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - LayerNorm 的逐样本几何与反向传播

## A

### NN-LN-A01
统计组数 $BT$，每组大小 $D$。保留 singleton 时 mean/variance shape 为 $(B,T,1)$；$\gamma,\beta$ 均为 $(D)$，共 $2D$ 个参数并沿 $B,T$ 广播；输出 $(B,T,D)$。

### NN-LN-A02
$$
\mu=\overline x,\quad q=\overline{(x-\mu)^2},\quad
\widehat x=(x-\mu)/r,\quad
y=\gamma\odot\widehat x+\beta.
$$
令 $g=\nabla_yL$、$u=\gamma\odot g$：
$$
dx=\frac1r(u-\overline u\,1-\widehat x\,\overline{u\widehat x}),
$$
$$
d\beta=g,\qquad d\gamma=g\odot\widehat x
$$
并对所有 $b,t$ 累加参数梯度。$\gamma$ 是逐 feature 向量，先改变每个上游坐标；若把它当 scalar 提到括号外，会错误交换“非均匀对角伸缩”和组内投影。

### NN-LN-A03
“不依赖 batch size”对标准 LayerNorm$(D)$ 的统计规则为真；“Jacobian diagonal”为假，因为同 token mean/variance 耦合 features；“含 LN 模型 train/eval 相同”为假，只有 LN 自身统计规则相同，Dropout、sampling 等仍可不同。

## B

### NN-LN-B01
$$
\mu=2,\quad c=(-1,0,1),\quad q=2/3,\quad r=\sqrt{2/3},
$$
$$
\widehat x=(-\sqrt{3/2},0,\sqrt{3/2}).
$$
所以
$$
y=(-\sqrt{3/2},1,\sqrt{3/2}).
$$
Affine 前 mean 为 0；affine 后 mean 为
$$
\frac{-\sqrt{3/2}+1+\sqrt{3/2}}3=\frac13.
$$

### NN-LN-B02
$$
u=\gamma\odot g=(1,2,0),\quad
\overline u=1,
$$
$$
\overline{u\widehat x}=-\sqrt{3/2}/3.
$$
代入得
$$
dx=(-\sqrt{3/8},\sqrt{3/2},-\sqrt{3/8})
\approx(-0.6124,1.2247,-0.6124).
$$
$$
d\beta=(1,1,0),\qquad
d\gamma=(-\sqrt{3/2},0,0).
$$
检查 $1^{\mathsf T}dx=0$；$c=(-1,0,1)$，故 $c^{\mathsf T}dx=0$。

### NN-LN-B03
$D=1$：
$$
\mu=x_1,\ q=0,\ \widehat x=0,\ y=\beta,\ J=0.
$$
$D=2$ 令 $d=x_1-x_2\ne0$：
$$
c=(d/2,-d/2),\quad q=d^2/4,
$$
$$
\widehat x=(\operatorname{sign}d,-\operatorname{sign}d).
$$
在不穿过 $d=0$ 的邻域输出不变，故 $\varepsilon=0$ 的局部 Jacobian 为零。

## C

### NN-LN-C01
$1^{\mathsf T}\widehat x=0$，所以位于 $1^\perp$。又
$$
\|\widehat x\|^2
=\frac{\|c\|^2}{q}
=\frac{Dq}{q}=D.
$$
$1^\perp$ 维数 $D-1$，再施加一个独立的固定半径约束，非退化交集局部维数 $D-2$。这对应删除共同平移与 centered radius 两个自由度。

### NN-LN-C02
$$
J=\frac1r(P-\widehat x\widehat x^{\mathsf T}/D).
$$
在 $1$ 上 eigenvalue 0；在 $\widehat x$ 上为 $\varepsilon/(q+\varepsilon)^{3/2}$；在同时正交于二者的 $D-2$ 维子空间上为 $1/r$。若 $\gamma$ 非均匀，
$$
J_{\rm LN}=\operatorname{Diag}(\gamma)J.
$$
左乘对角矩阵通常破坏对称性和原 eigendirections；输入输出欧氏增益应看奇异值。零 gain 还可能增加 rank loss。

### NN-LN-C03
对 $x'=ax+b1$，
$$
c'=ac,\qquad q'=a^2q.
$$
共同平移 $b$ 消失。$a>0,\varepsilon=0$ 时
$$
\widehat{x'}=ac/(a\sqrt q)=\widehat x.
$$
$\varepsilon>0$ 时
$$
\widehat{x'}=\frac c{\sqrt{q+\varepsilon/a^2}},
$$
与原值的差为
$$
c\left[
(q+\varepsilon/a^2)^{-1/2}
-(q+\varepsilon)^{-1/2}
\right].
$$
只有 $\varepsilon=0$、$a=1$ 或 epsilon 相对可忽略时消失。

## D

### NN-LN-D01
对同 token，
$$
\frac{\partial\widehat x_i}{\partial x_k}
=\frac1r(\mathbf1[i=k]-1/D-\widehat x_i\widehat x_k/D).
$$
$i\ne k$ 时通常非零，所以 feature $k$ 改变 shared mean/variance并影响 feature $i$。不跨样本只表示不同 $(b,t)$ 的 groups 独立。

### NN-LN-D02
LayerNorm 自身 train/eval 都用当前 token statistics，但 Transformer 还可能有 Dropout、stochastic depth、KV cache 路径、sampling、precision/fused kernel 与动态 shape 差异。因此只能断言 LN 的 state/mode 语义相同，不能推广到完整模型。

### NN-LN-D03
LayerNorm$(C,H,W)$ 对每个固定 $n$ 联合归约所有 $c,h,w$，一张图只有一组 statistics，affine 参数 shape 为 $(C,H,W)$。每像素 channel normalization 则固定 $(n,h,w)$、只归约 $c$，每图有 $HW$ 组；若 affine per-channel，参数 shape 是 $(C)$。二者统计组、参数量、空间耦合和 invariance 都不同。

## E

### NN-LN-E01
安全合同：输入 $(B,T,D)$，normalized shape 仅 $D$，固定 $(b,t)$ 归约 features；过去 token 的输出不读取其他 token。错误合同：normalized shape $(T,D)$ 或自定义在 $t'\ge t$ 上联合统计。最小反例取 $B=1,T=2,D=2$，固定第一个 token，改变第二个未来 token；错误合同下第一个 token 的 mean/variance和输出改变，安全合同不变。还需保证 attention/loss mask 正确。

### NN-LN-E02
构造 $x=o1+\delta$，扫描 offset $o$、contrast scale、$D$ 与 epsilon；用 float64 reference，对 fp32/fp16/bf16 以及显式高/低 precision accumulation 比较 pre-affine mean、energy、max output error、$1^{\mathsf T}dx$、radial inner product、gradcheck error 与 nonfinite。Separate 扫描 vector gain。结论绑定 kernel、hardware、dtype 和 shape，不用单一随机输入。

### NN-LN-E03
计算图：$c\to h(c)\to(\Delta\gamma,\Delta\beta)$；$X\to\widehat X$；再
$$
Y=(\gamma_0+\Delta\gamma)\odot\widehat X
+(\beta_0+\Delta\beta).
$$
若 $c$ 为 $(B,K)$，输出 $(B,D)$ 后在 $T$ 广播；若为 $(B,T,K)$，输出 $(B,T,D)$。Loss 同时回传到 LN base parameters、conditioning head 和 condition encoder。若 conditioning head 最后一层全零，初始 $\Delta\gamma,\Delta\beta=0$，head 因输入 activation 非零通常第一步可学；更早 condition encoder 的梯度会被 zero head 暂时阻断，待 head 离零后再学习。

