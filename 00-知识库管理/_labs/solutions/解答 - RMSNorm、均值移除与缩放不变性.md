---
type: solution
status: draft
area: [neural-networks/normalization, rmsnorm, geometry]
topic: "[[RMSNorm、均值移除与缩放不变性]]"
exercise: "[[习题 - RMSNorm、均值移除与缩放不变性]]"
sources: ["[[S-2019-Zhang-Sennrich-RMSNorm]]", "[[S-2026-PyTorch-Normalization-Systems]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - RMSNorm、均值移除与缩放不变性

## A

### NN-RMS-A01
固定 $(b,t)$ 组成一组，共 $BT$ 组，每组 $D$ 个数。保留 singleton 时 $q,r$ shape 为 $(B,T,1)$；$\gamma$ shape 为 $(D)$，标准无 bias 参数量为 $D$；无 running state，train/eval 都从当前 token 统计；输出 $(B,T,D)$。

### NN-RMS-A02
令 $h(x)=x/\sqrt{D^{-1}\|x\|^2+\varepsilon}$。

- $x\mapsto x+b1$：一般不变性不成立；
- $x\mapsto ax,a>0$：$\varepsilon=0$ 精确不变，$\varepsilon>0$ 一般只近似；
- $a<0,\varepsilon=0$：$h(ax)=-h(x)$，是变号等变而非不变；
- 逐 feature scale：除非所有 scale 相同且为正，一般改变方向。

### NN-RMS-A03
访问日 PyTorch RMSNorm 默认只有 per-element gain，无 additive bias；LayerNorm 默认有 per-element gain 和 bias。RMSNorm `eps=None` 使用 opmath dtype 的 machine epsilon，而 LayerNorm 常见默认是 $10^{-5}$。epsilon 改变输出能量、径向 eigenvalue 和小 variance gain，因此不显式对齐会同时比较“算法种类”和“epsilon 合同”。

## B

### NN-RMS-B01
$$
q=\frac{1+4+4}{3}=3,
\qquad r=\sqrt3,
$$

$$
\widehat x=\frac1{\sqrt3}(1,2,2),
$$

$$
y=\gamma\odot\widehat x
=\frac1{\sqrt3}(1,4,2).
$$

检查：

$$
\frac13\|\widehat x\|^2
=\frac13\frac{1+4+4}{3}=1,
$$

$$
\overline{\widehat x}=\frac5{3\sqrt3}\ne0.
$$

### NN-RMS-B02
$$
u=\gamma\odot g=(1,2,0),
$$

$$
\overline{u\widehat x}
=\frac13\left(\frac1{\sqrt3}+\frac4{\sqrt3}\right)
=\frac5{3\sqrt3}.
$$

因此

$$
dx=\frac1{\sqrt3}
\left[(1,2,0)-\frac59(1,2,2)\right]
=\frac1{9\sqrt3}(4,8,-10).
$$

单组参数梯度

$$
d\gamma=g\odot\widehat x
=\frac1{\sqrt3}(1,2,0).
$$

检查：

$$
x^{\mathsf T}dx
=\frac{4+16-20}{9\sqrt3}=0,
$$

$$
1^{\mathsf T}dx=\frac2{9\sqrt3}\ne0.
$$

### NN-RMS-B03
$$
f(x)=x(x^2+\varepsilon)^{-1/2},
$$

$$
f'(x)
=(x^2+\varepsilon)^{-1/2}
-x^2(x^2+\varepsilon)^{-3/2}
=\frac{\varepsilon}{(x^2+\varepsilon)^{3/2}}.
$$

$\varepsilon>0$ 时 $x=0$ 导数为 $1/\sqrt\varepsilon$。$\varepsilon=0,x\ne0$ 时 $f(x)=\operatorname{sign}(x)$，局部导数为 0；$x=0$ 处函数未定义且左右极限不同。

## C

### NN-RMS-C01
令

$$
q=\frac1D x^{\mathsf T}x,
\qquad r=(q+\varepsilon)^{1/2}.
$$

则

$$
dq=\frac2D x^{\mathsf T}dx,
\qquad
dr=\frac1{2r}dq=\frac1{Dr}x^{\mathsf T}dx.
$$

对 $\widehat x=x/r$：

$$
d\widehat x
=\frac1r dx-\frac{x}{r^2}dr
=\frac1r dx-\frac{x x^{\mathsf T}}{Dr^3}dx.
$$

用 $x=r\widehat x$：

$$
d\widehat x
=\frac1r\left(I-\frac1D\widehat x\widehat x^{\mathsf T}\right)dx.
$$

故所求 Jacobian 成立。

### NN-RMS-C02
若 $v\perp x$，也就 $v\perp\widehat x$，于是

$$
Jv=\frac1r v.
$$

这样的切向空间维数为 $D-1$。径向：

$$
J\widehat x
=\frac1r\left(1-\frac{\|\widehat x\|^2}{D}\right)\widehat x.
$$

而

$$
\frac{\|\widehat x\|^2}{D}=\frac q{q+\varepsilon},
$$

所以径向 eigenvalue 是

$$
\frac1r\frac{\varepsilon}{q+\varepsilon}
=\frac{\varepsilon}{(q+\varepsilon)^{3/2}}.
$$

$\varepsilon=0,x\ne0$ 时径向 eigenvalue 为 0，其他 $D-1$ 个为 $1/\sqrt q$，故秩 $D-1$。

### NN-RMS-C03
令 $I_j=\mathbf1\{j\in S\}$。均匀无放回时

$$
\mathbb E I_j=\frac{k}{D}.
$$

因此

$$
\mathbb E q_S
=\frac1k\sum_jx_j^2\mathbb E I_j
=\frac1k\frac{k}{D}\sum_jx_j^2=q.
$$

但输出含非线性函数 $(q_S+\varepsilon)^{-1/2}$。一般 Jensen/非线性期望给出

$$
\mathbb E[(q_S+\varepsilon)^{-1/2}]
\ne(q+\varepsilon)^{-1/2},
$$

且分母与被输出坐标可能相关，所以 normalized output 一般有偏。

## D

### NN-RMS-D01
取 $x=(1,2)$、$\varepsilon=0$：

$$
\widehat x=\frac{(1,2)}{\sqrt{5/2}},
$$

其均值

$$
\frac{3}{2\sqrt{5/2}}>0.
$$

RMSNorm 未执行 centering。LayerNorm 先减 $\mu=(1+2)/2$，所以 affine 前分量和严格为 0。

### NN-RMS-D02
fp16 最大有限值约 $65504$，先平方的阈值约

$$
\sqrt{65504}\approx255.94.
$$

故 $x=300$ 的平方已可能 overflow。稳定方案取 $a=\max|x_j|$：

$$
r=a\sqrt{\frac1D\sum_j(x_j/a)^2+\varepsilon/a^2},
$$

或在更高精度做 product/reduction。最终结果范围小不能保证中间表达式安全。

### NN-RMS-D03
$q=0$ 时两种 denominator 分别是

$$
\sqrt q+\varepsilon=\varepsilon,
\qquad
\sqrt{q+\varepsilon}=\sqrt\varepsilon.
$$

除非 $\varepsilon\in\{0,1\}$，它们不相等。且 $q\downarrow0$ 时第一式对 $q$ 的导数含 $1/(2\sqrt q)$ 而发散，第二式导数为 $1/(2\sqrt{q+\varepsilon})$，有限；输出能量和 Jacobian 也不同。

## E

### NN-RMS-E01
最小公平合同：

- 轴：都只归约 token feature $D$；
- affine：明确 LN 的 bias 是否删除，gain shape 相同；
- epsilon：显式设为同值；
- 初始化：相同主干参数与 gain 初值；
- 训练：相同 tokens/steps、optimizer，并分别公平调 learning rate；
- 系统：报告 shape、dtype、fusion、kernel latency 与 memory traffic；
- 指标：训练失败率、收敛步数、wall time、validation/迁移分开报告，多 seed。

### NN-RMS-E02
若四卡各持有 $D/4$ coordinates，local

$$
q_r=\frac{4}{D}\sum_{j\in r}x_j^2
$$

会给每个 shard 不同 denominator；global RMS 需要

$$
S=\sum_r\sum_{j\in r}x_j^2,
\qquad q=S/D.
$$

因此对每个 token all-reduce `sum of squares`（若 shard sizes 不等还需 count），再统一 rsqrt。collective 的 product/accumulation dtype 也属于合同。

### NN-RMS-E03
测试矩阵应含：

1. float64 reference 与 random $D=1,2,3,128$；
2. central-difference/dot-test 验证 VJP 和 $d\gamma$；
3. $a x$ 扫描验证 $\varepsilon=0$ 正尺度不变；
4. 共同 shift 确认输出应改变；
5. zero/constant/tiny variance 与显式 epsilon；
6. 大 magnitude 检查 square overflow；
7. fp16/bf16/fp32 与 accumulator 组合；
8. unfused reference 对 fused forward/backward 的绝对、相对误差和 NaN/Inf；
9. 非连续 layout、尾维 shape 与 tensor-parallel global reduction。

