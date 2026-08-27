---
type: solution
status: draft
area: [neural-networks/normalization, batch-normalization, backpropagation]
topic: "[[BatchNorm 反向传播、尺度不变性与噪声]]"
exercise: "[[习题 - BatchNorm 反向传播、尺度不变性与噪声]]"
sources: ["[[S-2015-Ioffe-Szegedy-BatchNorm]]", "[[S-2018-Santurkar-BatchNorm-Optimization]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - BatchNorm 反向传播、尺度不变性与噪声

## A

### NN-BNB-A01
令 $r=\sqrt{q+\varepsilon}$、上游 $g_i=\partial L/\partial y_i$：
$$
d\beta=\sum_i g_i,\qquad
d\gamma=\sum_i g_i\widehat x_i,
$$
$$
\boxed{
dx_i=\frac{\gamma}{r}
\left(g_i-\overline g-\widehat x_i\overline{g\widehat x}\right)
}.
$$
其中
$$
\overline g=m^{-1}\sum_i g_i,\qquad
\overline{g\widehat x}=m^{-1}\sum_i g_i\widehat x_i.
$$

### NN-BNB-A02
Train mode：
$$
\frac{\partial y_i}{\partial x_k}
=\frac{\gamma}{r}
\left(\mathbf1[i=k]-\frac1m-\frac1m\widehat x_i\widehat x_k\right).
$$
$i\ne k$ 时后两项通常非零，因为 $x_k$ 改变共享 mean/variance。Eval 固定 buffers：
$$
\frac{\partial y_i}{\partial x_k}
=\frac{\gamma}{\sqrt{\bar q+\varepsilon}}\mathbf1[i=k],
$$
是 diagonal。

### NN-BNB-A03
BN noise：(1) data-dependent；(2) group-shared/cross-sample correlated；(3) ratio 中的非加性噪声；(4) 跨层传播；(5) train/eval 特定且受 batch construction/device 影响。Dropout 通常给各单元/结构抽 Bernoulli mask，可在明确实现下近似独立乘性噪声；BN 的随机量由样本值共同决定，不能用同一 mask 模型替代。

## B

### NN-BNB-B01
$$
\mu=0,\quad q=2/3,\quad r=\sqrt{2/3},
$$
$$
\widehat x=(-\sqrt{3/2},0,\sqrt{3/2}).
$$
对 $g=(1,0,0)$：
$$
\overline g=1/3,\qquad
\overline{g\widehat x}=-\sqrt{3/2}/3.
$$
代入：
$$
dx=\left(\frac1{2\sqrt6},-\frac1{\sqrt6},\frac1{2\sqrt6}\right)
\approx(0.2041,-0.4082,0.2041).
$$
和为 0；又
$$
x^{\mathsf T}dx=-\frac1{2\sqrt6}+\frac1{2\sqrt6}=0.
$$
第二个检查在 $\varepsilon=0$ 验证 radial gradient 被删除。

### NN-BNB-B02
$$
d\beta=3+(-1)=2,
$$
$$
d\gamma=3(-1)+(-1)(1)=-4.
$$
又
$$
\overline g=1,\qquad
\overline{g\widehat x}=(-3-1)/2=-2.
$$
对两个位置，括号分别为
$$
3-1-(-1)(-2)=0,
$$
$$
-1-1-(1)(-2)=0.
$$
故 $dx=(0,0)$。$m=2,\varepsilon=0$ 的 normalized output 在两值次序不变的局部区域是常量 $\pm(1,-1)$，没有连续切向自由度；loss 仍能更新 $\gamma,\beta$。

### NN-BNB-B03
scale factor 为
$$a=10/2=5.$$
由 $\nabla_{aw}L=a^{-1}\nabla_wL$，raw gradient norm 变为原来的 $1/5$。相对 angular step 还除以 parameter norm 的 5 倍，约为原来的 $1/25$。这是忽略 epsilon、regularizer、optimizer state 与 finite-step 高阶项的局部律。

## C

### NN-BNB-C01
设 $c=Px$、$P=I-11^{\mathsf T}/m$。则
$$
d\mu=m^{-1}1^{\mathsf T}dx,\qquad dc=Pdx.
$$
由 $1^{\mathsf T}c=0$，
$$
dq=\frac2m c^{\mathsf T}dc
=\frac2m c^{\mathsf T}dx.
$$
再由 $r=(q+\varepsilon)^{1/2}$，
$$
dr=\frac1{mr}c^{\mathsf T}dx.
$$
最后
$$
d(c/r)=\frac1rPdx-\frac c{r^2}dr
=\frac1rPdx-\frac1{mr^3}cc^{\mathsf T}dx.
$$
用 $c=r\widehat x$ 得
$$
d\widehat x=\frac1r(P-\widehat x\widehat x^{\mathsf T}/m)dx.
$$
关键正交关系是 $c^{\mathsf T}1=0$。

### NN-BNB-C02
从 VJP：
$$
1^{\mathsf T}dx
=\frac1r\left(1^{\mathsf T}u-\overline u\,m
-1^{\mathsf T}\widehat x\,\overline{u\widehat x}\right)=0.
$$
对 radial direction，
$$
J\widehat x
=\frac1r\left(P\widehat x
-\widehat x\frac{\|\widehat x\|^2}{m}\right).
$$
$P\widehat x=\widehat x$ 且 $\|\widehat x\|^2/m=q/(q+\varepsilon)$，所以 eigenvalue
$$
\frac1r\left(1-\frac q{q+\varepsilon}\right)
=\frac{\varepsilon}{(q+\varepsilon)^{3/2}}.
$$

### NN-BNB-C03
对 $a$ 求导 $L(aw)$：
$$
\frac d{da}L(aw)=w^{\mathsf T}\nabla L(aw)=0.
$$
取 $a=1$ 得 $w^{\mathsf T}\nabla_wL=0$。令 $v=aw$，尺度不变函数的 chain rule 给
$$
\nabla_vL(v)=a^{-1}\nabla_wL(w).
$$
切向参数变化大小约 $\eta\|g\|$，角度变化再除以 $\|w\|$；两者分别按 $a^{-1}$ 与 $a$ 缩放，故角度步长按 $a^{-2}$。

## D

### NN-BNB-D01
逐元素 scale 只对应把 $\mu,q$ 错当常数。训练时 $x_k$ 还通过 $d\mu$ 与 $dq$ 影响所有 normalized outputs，必须出现 $-\overline g$ 与 $-\widehat x\,\overline{g\widehat x}$。只有 eval 固定 buffers 时才退化为逐元素 $\gamma/\sqrt{\bar q+\varepsilon}$。

### NN-BNB-D02
$\varepsilon>0$ 时平移方向仍为零，但 radial eigenvalue 非零。$q=0$ 时 $\widehat x=0$，
$$
J=P/\sqrt\varepsilon,
$$
对 $m>1$ 只有共同平移一个零方向，其余 contrasts 被放大。$m=1$ 时 $P=0$，整个一维 Jacobian 为零，不能称有两个线性无关零方向。因此“两零奇异值”只适用于 $m\ge2,q>0,\varepsilon=0$，且 $m=2$ 时恰好全零。

### NN-BNB-D03
epsilon 破坏精确不变性；weight decay 直接依赖 norm；adaptive/momentum state 记住历史 scale；gradient clipping、finite precision 和 skip path 也会引入 norm 效应。即使函数值沿正 scale ray 不变，raw gradient 与角度步长依赖 norm，所以 learning rate 仍重要；weight decay 还可通过缩小 norm 改变有效方向学习率。

## E

### NN-BNB-E01
用 float64、非退化小 batch，定义 scalar loss $L=\langle Y,G\rangle$，对 $X,\gamma,\beta$ 做 central difference；step 取若干数量级并观察误差 U 形曲线。Train mode固定同一完整 batch且禁用 buffer side-effect干扰数值差分；eval 固定 buffers单独检查 diagonal formula。报告 max/relative error。加入 constant 与 near-constant groups、非零 epsilon，预期 constant 处不使用 $\varepsilon=0$。

### NN-BNB-E02
固定目标样本 $x_1$，替换 companions 而保持 loss seed 只落在目标输出；使用 loss sum，避免 mean reduction 自带 $1/m$。用 autodiff/JVP 计算 $\partial y_i/\partial x_k$，报告 off-diagonal block norm；eval 重复应接近 0。再用显式手算 Jacobian核验。改变 batch size 时同时固定 target 和 seed，不把参数 gradient averaging 混入。

### NN-BNB-E03
扫描对数尺度 $a$。无 weight decay 基线记录 $L(aw)-L(w)$、$\|g(aw)\|a/\|g(w)\|$、$(aw)^{\mathsf T}g(aw)$ 与一次更新方向夹角；在 $a^2q\gg\varepsilon$ 区域这些量应分别接近 0、1、0 和 $a^{-2}$ 律。再独立打开 epsilon、weight decay、momentum/adaptive optimizer，展示偏离。只有在声明的区域、多尺度与容差都满足时才称“近似尺度不变”。

