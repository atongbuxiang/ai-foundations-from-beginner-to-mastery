---
type: solution
status: draft
area: [neural-networks/initialization, gradient-propagation]
topic: "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]"
exercise: "[[习题 - 反向梯度方差与 Fan-In_Fan-Out 权衡|习题 - 反向梯度方差与 Fan-In/Fan-Out 权衡]]"
sources: ["[[S-2010-Glorot-Bengio-Training-Difficulty]]", "[[S-2015-He-Delving-Rectifiers]]", "[[S-2017-Schoenholz-Deep-Information-Propagation]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - 反向梯度方差与 Fan-In/Fan-Out 权衡

## A

### NN-FAN-A01
Forward：$z=Wh+b$、$h^+=\phi(z)$，每个 $z_j$ 汇总 fan-in 个输入。Reverse：给 $\delta=\partial L/\partial z$，有 $\bar h=W^T\delta$，再乘前层 $\phi'$；每个 $\bar h_i$ 汇总 fan-out 个输出 cotangents。矩阵相同，转置使求和长度互换。

### NN-FAN-A02
$c(q)=E[\phi(Z)^2]/E[Z^2]$ 是 forward activation 的二阶增益；$d(q)=E[\phi'(Z)^2]$ 是 local derivative 的二阶增益。若 weight variance 为 $v$，$\chi_f=n_{\rm in}vc(q)$、$\chi_b=n_{\rm out}vd(q)$ 分别近似一层 forward/backward second-moment multiplier。

### NN-FAN-A03
每坐标 gradient second moment 是随机坐标的 $E[\delta_i^2]$；norm 是所有坐标平方和，期望约为宽度乘前者；Jacobian Frobenius scale 是 singular values squared 的和/平均；spectrum 还记录每个 singular value、尤其 extremes。相同平均能量可对应极不相同的方向性条件数。

## B

### NN-FAN-B01
linear 有 $c=d=1$。fan-in variance $1/64$ 给 $(\chi_f,\chi_b)=(1,4)$；fan-out variance $1/256$ 给 $(1/4,1)$；Xavier variance $2/(64+256)=1/160$ 给 $(64/160,256/160)=(0.4,1.6)$。三者回答不同守护目标。

### NN-FAN-B02
$$0.95^{100}\approx5.92\times10^{-3},\qquad1.05^{100}\approx131.50.$$
单层只有 5% 的缩放偏差，沿 100 层乘积后分别缩小约 169 倍或放大约 132 倍；因此要用 log-gain/depth product，而不是只看单层接近 1。

### NN-FAN-B03
第一层 $512\to128$ 用 ReLU fan-in He：$v=2/512$、$d=1/2$，所以 backward multiplier
$$\chi_{b,1}=128(2/512)(1/2)=1/4.$$
第二层 $128\to512$：$v=2/128$，故
$$\chi_{b,2}=512(2/128)(1/2)=4.$$
两层产品为 1，但 bottleneck 中间梯度先放大/缩小，有限精度、非线性和 optimizer 看得到这个中间失衡。

## C

### NN-FAN-C01
$u_i=\sum_jW_{ji}\delta_j$。展开
$$Eu_i^2=\sum_jE[W_{ji}^2\delta_j^2]+\sum_{j\ne k}E[W_{ji}W_{ki}\delta_j\delta_k].$$
在零均值独立权重、忽略其与 $\delta$ 的依赖且 cotangent 同尺度时，交叉项为 0，第一项为 $n_{\rm out}vE\delta^2$。再假设 $\phi'(z)$ 与 $u$ 的 squared magnitude 可拆，得到 $E(\delta^-)^2\approx n_{\rm out}vE[\phi'(z)^2]E\delta^2$。

### NN-FAN-C02
同时守恒要求
$$n_{\rm in}vc(q)=1,\qquad n_{\rm out}vd(q)=1.$$
消去 $v$ 得兼容条件 $n_{\rm in}c(q)=n_{\rm out}d(q)$；此时唯一共同值为 $v=1/[n_{\rm in}c(q)]=1/[n_{\rm out}d(q)]$。若不满足，任何 scalar variance 都只能选择目标或折中。

### NN-FAN-C03
取
$$J_\varepsilon=\operatorname{diag}\!\left(\sqrt{2-\varepsilon^2},\varepsilon\right),\qquad0<\varepsilon<1.$$
其平均 squared singular value 为 $[(2-\varepsilon^2)+\varepsilon^2]/2=1$，所以 isotropic direction-average energy 守恒；condition number 为 $\sqrt{2-\varepsilon^2}/\varepsilon\to\infty$。平均平方增益 1 不排除一个方向几乎消失。

## D

### NN-FAN-D01
$\delta^{(\ell)}$ 由后续层和当前 forward activations 决定，而当前 activations 又使用 $W^{(\ell)}$；因此 $W^{(\ell)}$ 与 $\delta^{(\ell)}$ 一般共享随机因果路径。把 $E[W^2\delta^2]$ 拆开只是宽极限/conditioning 下的近似，需要定理或实验验证，训练后尤其不严格。

### NN-FAN-D02
gradient norm 只汇总 squared singular-direction gains。上题 $J_\varepsilon$ 的平均能量固定，但第二方向乘 $\varepsilon$，可任意接近 0；若任务信号恰在该方向，仍出现方向性消失。还可能少数方向爆炸来补偿大量方向收缩。

### NN-FAN-D03
Residual 的 reverse Jacobian 含 $I+J_F$ 和 cross terms；normalization 的 derivative 会在 normalized axes 上耦合坐标并投影/缩放；mean loss 相比 sum loss多 $1/B$ 或 $1/N_{\rm token}$。这些因素都不在 plain $n_{\rm out}vd$ 中，必须写进新计算图和尺度账本。

## E

### NN-FAN-E01
选择 width profiles：等宽、单次扩宽/压窄、交替 bottleneck；modes：fan-in/fan-out/Xavier；activations：linear/tanh/ReLU/SiLU。对深度、seed 做 factorial run，初始化前后记录 $q,r,\delta$ moments、one-step $\chi$ 与 cumulative log-gain，并估计 top/bottom singular values。固定输入、loss reduction 和无 residual/norm 的基线，再逐项加入结构。

### NN-FAN-E02
账本从 unreduced per-example/token loss 开始，依次记录 local derivative、mean/sum divisor、microbatch accumulation、loss-scale factor、unscale、data-parallel all-reduce 的 sum/mean、gradient clipping、optimizer preconditioner。每一步保存理论倍率与实测 norm/finite rate；同一报告同时给 scaled 与 unscaled gradient，避免把 AMP scale 当网络稳定性。

### NN-FAN-E03
若 layerwise moment 已出现系统 drift，先修 fan/activation/reduction；若 scalar moments近稳但训练仍慢、方向敏感、condition estimate 上升或不同随机 probe gain 分散，则升级到 JVP/VJP power iteration、Lanczos/随机 SVD。若 residual/norm 存在，直接使用完整 block Jacobian；只有当 spectrum 也受控，才允许比“平均尺度正常”更强的结论。

