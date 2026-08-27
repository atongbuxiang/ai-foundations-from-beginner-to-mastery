---
type: solution
status: draft
area: [neural-networks/initialization, kaiming, rectifiers]
topic: "[[Kaiming、He 初始化]]"
exercise: "[[习题 - Kaiming、He 初始化]]"
sources: ["[[S-2015-He-Delving-Rectifiers]]", "[[S-2026-PyTorch-NN-Init]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Kaiming、He 初始化

## A

### NN-HEI-A01
对 symmetric $Z$，Leaky ReLU $\phi_a$ 的 forward factor 为 $E\phi_a(Z)^2/EZ^2=(1+a^2)/2$。其 derivative 在正/负侧为 $1,a$，continuous symmetric law 在两侧概率各 $1/2$，故 derivative second-moment factor 也为 $(1+a^2)/2$。ReLU 取 $a=0$，两者均为 $1/2$。

### NN-HEI-A02
令所选 fan 为 $f$。目标 variance 为 $v=2/[(1+a^2)f]$；normal std 为 $\sqrt v$；uniform bound 为 $\sqrt{3v}=\sqrt{6/[(1+a^2)f]}$。mode=fan-in 取 forward fan，mode=fan-out 取 backward fan；权重布局必须与 helper 约定一致。

### NN-HEI-A03
positive rate 是 $P(Z>0)$；second moment 是 $E[\phi(Z)^2]$；variance 还要减 $[E\phi(Z)]^2$。对 centered Gaussian ReLU，三者分别为 $1/2,q/2,q(1/2-1/(2\pi))$，数值和用途不同。

## B

### NN-HEI-B01
$f=256,a=0.1$，所以
$$v=\frac2{(1+0.01)256}=\frac2{258.56}\approx0.007735.$$
Normal std 约为 $\sqrt v\approx0.08795$；uniform bound 为 $\sqrt{3v}\approx0.15233$。

### NN-HEI-B02
普通 conv 权重 $[C_{\rm out},C_{\rm in},k_h,k_w]=[64,256,3,3]$。fan-in $=256\cdot9=2304$，fan-out $=64\cdot9=576$。ReLU fan-in variance 为 $2/2304=1/1152\approx8.681\times10^{-4}$；fan-out variance 为 $2/576=1/288\approx3.472\times10^{-3}$。

### NN-HEI-B03
利用 half-normal integral：
$$E[\operatorname{ReLU}(Z)]=\sqrt{\frac q{2\pi}},\qquad E[\operatorname{ReLU}(Z)^2]=\frac q2.$$
因此
$$\operatorname{Var}(\operatorname{ReLU}(Z))=\frac q2-\frac q{2\pi}=q\left(\frac12-\frac1{2\pi}\right).$$
这正说明 He scale 保存的不是 activation variance。

## C

### NN-HEI-C01
分半轴：
$$E[\phi_a(Z)^2]=E[Z^2\mathbf1_{Z>0}]+a^2E[Z^2\mathbf1_{Z\le0}]=\frac{1+a^2}{2}EZ^2.$$
若 linear fan scale 是 $1/f$，为抵消该 factor 要乘 gain squared $2/(1+a^2)$，所以 $g=\sqrt{2/(1+a^2)}$。

### NN-HEI-C02
forward 已由对称性得 $(1+a^2)/2$。除去 probability-zero kink，$\phi_a'(Z)^2$ 在正侧为 1、负侧为 $a^2$；symmetric continuous law 给两侧概率各 $1/2$，故 $E[\phi_a'(Z)^2]=(1+a^2)/2$。若有 0 点原子，还需声明框架在 kink 的 derivative convention。

### NN-HEI-C03
初始化 variance 是 $v=2/[(1+a_0^2)n_{\rm in}]$。训练时新的单层 forward factor 为
$$n_{\rm in}v\frac{1+a_t^2}{2}=\frac{1+a_t^2}{1+a_0^2}.$$
它大于、等于或小于 1 取决于 $|a_t|$ 相对 $|a_0|$；初始化不会自动随 learnable slope 重校准。

## D

### NN-HEI-D01
即使 centered symmetric law 下 preactivation second moment 保持，ReLU activation mean 为正，所以 variance 是 $q(1/2-1/(2\pi))$，不是 $q/2$。有限宽 positive rate、bias、correlation 和 training drift 还会进一步偏离；因此“variance 不变”把 second moment 与 variance 混淆了。

### NN-HEI-D02
令 $Z=M+\varepsilon$，其中 $M\gg\operatorname{sd}(\varepsilon)>0$，则 $P(Z>0)\approx1$，ReLU 几乎是 identity，second-moment factor 接近 1 而非 $1/2$。大负 bias 则 factor 接近 0。非对称输入同样使正负半轴承载的 squared mass 不等。

### NN-HEI-D03
normal 截断删掉 tails，若不 rescale，variance 降低；clipping 把大值压到阈值，也降低/改变 fourth moment；低精度 cast 会量化小值、合并 bins，极端时 underflow 成 0。nominal generator std 只描述截断/转换前，必须在最终 tensor 上测 sample moments。

## E

### NN-HEI-E01
对 dense、ordinary conv、grouped/depthwise conv 列出 weight shape、真实连接 fan 和框架 fan；为每类生成大量 weights，验 mean/variance/bound。用 symmetric Gaussian input 测 forward second moment、positive rate，并以随机 cotangent 做 VJP second moment/dot test。加入 transpose layout、non-tile shapes 和不同 dtype。

### NN-HEI-E02
固定深 ReLU MLP、输入、data order 与 base seeds，比较 Xavier $1/n$ 与 He $2/n$；深度扫描 10/50/100，记录每层 preactivation/activation second moment、positive rate、gradient moment、Jacobian estimates 和 loss。预期 Xavier 每个 ReLU block 约乘 $1/2$ 而衰减；He 只在假设成立的初始化邻域近似平稳。

### NN-HEI-E03
每个 checkpoint 记录 $a_t$ 分布、预测 multiplier $(1+a_t^2)/(1+a_0^2)$、实测 preactivation/activation/gradient moments、weight variance 与 normalization statistics；按 layer/seed 比较预测误差。设置固定-$a$ 对照和重新参数化/正则化对照，但不因相关曲线就宣称 slope drift 是训练故障的唯一原因。

