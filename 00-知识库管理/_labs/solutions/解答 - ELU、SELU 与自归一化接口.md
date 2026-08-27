---
type: solution
status: draft
area: [neural-networks/activations, elu, selu, self-normalization]
topic: "[[ELU、SELU 与自归一化接口]]"
exercise: "[[习题 - ELU、SELU 与自归一化接口]]"
sources: ["[[S-2016-Clevert-ELU]]", "[[S-2017-Klambauer-SNN]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - ELU、SELU 与自归一化接口

## A

### NN-SELU-A01
ReLU 负侧恒 0、导数 0、负极限 0，正齐次且产生 exact sparsity；leaky 负侧 $ax$、导数 $a$、极限 $-\infty$，正齐次且通常无 exact zeros；ELU 负侧 $\alpha(e^x-1)$、导数 $\alpha e^x$、极限 $-\alpha$，不正齐次且极负区饱和。三者正侧都为 identity（SELU 另乘 scale）。

### NN-SELU-A02
ELU 在 0 左右值均 0，所以任意 $\alpha$ 连续；左右一阶导为 $\alpha,1$，仅 $\alpha=1$ 时 $C^1$；此时左右二阶导为 $1,0$，仍非 $C^2$。经典 SELU 的 $\alpha\approx1.6733$，scale $\lambda$ 同乘两侧，左右导为 $\lambda\alpha$ 与 $\lambda$，所以在 0 不可微。

### NN-SELU-A03
在论文指定的宽前馈、初始化与近独立/Gaussian 条件下，层间 population moments 形成 map $(\mu',\nu')=F(\mu,\nu)$，SELU constants 使 $(0,1)$ 为 fixed point，并在给定域具有吸引/有界性质。BatchNorm 则用当前 batch/运行统计量显式重中心缩放；SELU 不读取 batch statistics，也不保证每 batch 精确 moments。

## B

### NN-SELU-B01
$\alpha=1$：$x=-20$ 时 output $e^{-20}-1\approx-0.999999998$、derivative $e^{-20}\approx2.06\times10^{-9}$；$x=-1$ 时 output $e^{-1}-1\approx-0.632121$、derivative $e^{-1}\approx0.367879$；0 的值为 0，左右导均 1；$x=2$ output 2、derivative 1。低精度可能在 $-20$ 直接饱和到 $-1$、导数 underflow 为 0，近 0 朴素减法有 cancellation。

### NN-SELU-B02
设 $c=-\lambda\alpha$、$D\sim\mathrm{Bernoulli}(q)$，$\widetilde X=DX+(1-D)c$。独立时 $E\widetilde X=(1-q)c$，$E\widetilde X^2=q+(1-q)c^2$，故 variance 为 $q+q(1-q)c^2$。取 $a=[q+q(1-q)c^2]^{-1/2}$、$b=-a(1-q)c$，则 $Y=a\widetilde X+b$ 的均值 0、方差 1。代 $q=0.9$ 即得具体 correction。

### NN-SELU-B03
令 $A=e^{1/2}\Phi(-1)-1/2$、$B=e^2\Phi(-2)-2e^{1/2}\Phi(-1)+1/2$。则均值为 $\lambda[1/\sqrt{2\pi}+\alpha A]$；二阶矩为 $\lambda^2[1/2+\alpha^2B]$。fixed point 要求前者 0、在均值为 0 时后者 1，这两式分别确定 $\alpha$ 与 $\lambda$。

## C

### NN-SELU-C01
`expm1(x)` 按定义返回 $e^x-1$，故数学等价。近 0 时 $e^x=1+x+x^2/2+\cdots$，先舍入 $e^x$ 再减 1 会消掉 leading digits；专用实现直接计算 $x+x^2/2+\cdots$ 或等价 range reduction，保持相对精度。

### NN-SELU-C02
均值方程 $1/\sqrt{2\pi}+\alpha A=0$ 给 $\alpha=-[\sqrt{2\pi}A]^{-1}$；再由 $\lambda^2(1/2+\alpha^2B)=1$ 得 $\lambda=(1/2+\alpha^2B)^{-1/2}$，数值即经典常数。$F(s_*)=s_*$ 只说明从该点出发不动；例如 $F(s)=2s$ 也固定 0 却排斥，因此还需邻域收缩/稳定条件。

### NN-SELU-C03
$\rho(J_F(s_*))<1$ 通常只给局部线性稳定迹象；要用 Banach，需选择闭合完备域 $D$，证明 $F(D)\subseteq D$，并给统一 $\|F(s)-F(t)\|\le q\|s-t\|$、$q<1$，还要初始 state 在 $D$。连续可微时可用域内 Jacobian norm 上界而非只看固定点谱半径。

## D

### NN-SELU-D01
理论对象是近似 population moment recursion。有限 batch 的 sample mean/variance 本来就随机；有限 width、相关 units、bias、非 Gaussian input 和训练后 weights 还会偏离 map。即便期望固定，也不推出每次 realization 精确等于固定点。

### NN-SELU-D02
ordinary inverted dropout 令 $Y=DX/q$，保持 mean 但把 variance 放大约 $1/q$，且 dropped value 为 0 而非 SELU 负饱和值，改变后续输入分布。alpha dropout 用 $c=-\lambda\alpha$ 替换 dropped units，再做 affine correction，使理想输入均值/方差仍为 $(0,1)$；它修的是前两 moments，不恢复完整分布。

### NN-SELU-D03
若两个独立、均值 0、方差 1 的 branches 相加 $Y=X+F(X)$，即便粗略视为独立也有 $\operatorname{Var}Y=2$；若相关，variance 为 $2+2\operatorname{Cov}(X,F(X))$。plain chain 的 $F(0,1)=(0,1)$ 不包含这条 addition，moment map 已变，必须加 residual scaling/correlation analysis。

## E

### NN-SELU-E01
构造不同初始 $(\mu_0,\nu_0)$ 的 synthetic Gaussian inputs，固定宽度、LeCun-normal weights 与 zero bias，逐层估计 $(\mu_l,\nu_l)$；比较到 $(0,1)$ 的规范化距离并拟合局部 ratio $d_{l+1}/d_l$。扫描 width/depth/seeds 和理论域；若 ratios 在邻域稳定小于 1且置信区间受控，可称经验局部收缩。再扰动 bias、相关输入、weight variance、dropout，明确何处失效；不能由有限层曲线证明全局 contraction。

### NN-SELU-E02
主张缺失对象合同：Transformer 有 residual addition、attention-induced correlation、LayerNorm 的 tokenwise statistics、gated/FFN structure 与训练后相关权重，不满足原 plain FNN moment map。替换还改变函数、kernel cost 与 initialization，删 LayerNorm 改变优化路径。需要专门推导 residual/attention moment map、scale law、gradient spectrum，并做 matched-compute 多 seed 消融；原 SELU theorem 不能直接授权。

### NN-SELU-E03
用 FP64 `expm1` reference 扫描 $[-100,20]$ 与 0 邻域 ULP；检查 FP16 的负饱和值、derivative underflow、NaN/Inf、monotonicity 与 branch continuity。zero kink 只验规定 VJP；非 kink 做 central/Taylor/dot tests，另测 double backward。覆盖 contiguous/strided shapes、fusion、alpha/lambda constants、determinism，并报告 throughput、memory traffic 与相对 ReLU/exp kernel 的代价。
