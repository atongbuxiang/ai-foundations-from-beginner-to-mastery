---
type: solution
status: draft
area: [neural-networks/gradient-checking, checkpointing, higher-order-differentiation]
topic: "[[Gradient Checking、Checkpointing 与高阶微分边界]]"
exercise: "[[习题 - Gradient Checking、Checkpointing 与高阶微分边界]]"
sources: ["[[S-1994-Pearlmutter-Fast-Exact-HVP]]", "[[S-2016-Chen-Sublinear-Memory]]", "[[S-2026-JAX-Autodiff-Checkpointing]]", "[[S-2026-PyTorch-Autograd-Gradcheck]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Gradient Checking、Checkpointing 与高阶微分边界
## A
### NN-GC-A01
中心差分独立比较 $g^Tv$ 与函数值方向差商；Taylor test 检查一阶模型余项是否呈 $O(h^2)$ slope；dot test 不用函数差分，检查实现的 JVP/VJP 是否互为伴随。三者证据来源不同，应组合使用。
### NN-GC-A02
checkpointing 在 forward 中只保存部分 boundary activations，在 backward 需要中间 residuals 时从 boundary 重放 forward。它用额外 FLOPs、latency 及可能的 communication 换较小 peak activation memory，不减少参数或 optimizer-state memory。
### NN-GC-A03
full Hessian 是 $n\times n$ 坐标表；HVP 是给定 $v$ 的 $Hv$，可 matrix-free 计算。在 ReLU kink 等不可微点 classical Hessian 不存在，框架仍可根据它的一阶 convention 继续返回某个数，该数不能冒充 classical Hessian。
## B
### NN-GC-B01
$$\frac{(2+h)^3-(2-h)^3}{2h}=12+h^2.$$
当 $h=0.01$，结果 $12.0001$，与真导数 12 差 $10^{-4}$。对三次多项式该式精确显示中心差分的 $h^2$ 截断项，暂不计浮点舍入。
### NN-GC-B02
$f(1)=\sin1$、$g=f'(1)=2\cos1$，所以 $R(h)=|\sin((1+h)^2)-\sin1-2h\cos1|$。在二阶光滑和 truncation-dominated 区间，$R(h/2)/R(h)\to1/4$。$h$ 过大时高阶项未进入渐近区，过小时 roundoff/cancellation 主导；在 kink 或 noisy function 上也不应期待该斜率。
### NN-GC-B03
$n/k+k=100/10+10=20$ activation units，对比全保存约 100 units。这是均匀链的粗略 peak 账本；真实图还要加上 boundary live tensors、workspace、parameters 与不同层的 bytes。
## C
### NN-GC-C01
对 $h>0$，$E'(h)=2C_1h-C_2u/h^2$。令其为 0，得 $h^3=C_2u/(2C_1)$，即 $h=[C_2u/(2C_1)]^{1/3}=O(u^{1/3})$。$C_1,C_2$ 含函数高阶导数和 scale，所以不能只由 dtype 给唯一步长。
### NN-GC-C02
令 $M(k)=n/k+k$，$M'(k)=-n/k^2+1$，零点 $k=\sqrt n$；$M''(k)=2n/k^3>0$，是最小值。代回得 $M=2\sqrt n=O(\sqrt n)$。整数层数取附近分割，不均匀 activation sizes 则要做加权分割。
### NN-GC-C03
$g(x)=\nabla f(x)$ 是 reverse-mode 得到的 vector function，对它沿 $v$ 做 JVP，$Dg(x)[v]=Hv$，所以是 forward-over-reverse。若 $f\in C^2$，$H=H^T$，因而 $u^THv=(Hu)^Tv=v^THu$；随机 $u,v$ 可作 HVP symmetry dot test。
## D
### NN-GC-D01
中心差分的 truncation 约随 $h^2$，roundoff 约随 $u/h$；FP64、FP32、FP16 的 $u$ 不同，输入/函数尺度和三阶导数也改变常数。`1e-6` 在 FP16 可根本无法改变输入，在高曲率函数上又可过大/过小；应做 relative scale 和 step sweep。
### NN-GC-D02
原 forward 用 mask $m_1$ 得 activation 与 local coefficient；checkpoint 丢弃它们。backward 重放时若 RNG 已前进，会采到 $m_2\ne m_1$；然后 VJP 用 $m_2$ 回传，实际求的是另一随机函数的局部导数，不是已计算 loss 的 derivative。
### NN-GC-D03
ReLU 在 0 连一阶 classical derivative 都不存在，更不存在 classical Hessian。框架若选 $\operatorname{ReLU}'(0)=0$，对这个 programmed rule 再求导可得 0，但这是 convention 的 derivative path，不能改写原函数的可微性。
## E
### NN-GC-E01
对象层确认 forward/loss/reduction；局部层验 JVP/VJP shape 与 dot test；子图层用 FP64 手算、中心差分、Taylor slope 和 reference unfused op；系统层对照 eager/compiled、checkpoint on/off、single/distributed、FP64/32/16。另测 kink、extreme values、alias 和 higher-order composition。
### NN-GC-E02
按 block 记录 saved activation bytes 和 recompute FLOPs/latency，标出 residual/skip 跨边界 live tensors、attention 大中间量和 temporary workspace；检查 dropout RNG、normalization/state 重放；识别 all-reduce/all-to-all 是否会重做。扫描多种分割，同时报 peak memory、step time、extra FLOPs、communication 和 gradient equivalence。
### NN-GC-E03
先报前向 nonlinear-solve residual 和局部唯一/条件性；再报 adjoint linear-solve residual。用多个 finite-difference steps 检 gradient/HVP，随机 $u,v$ 做 $u^THv$ 对称测试；逐渐收紧 forward/adjoint tolerance，检查导数误差是否随残差降低；对比 unrolled small-solver 作 reference，并审计 stopping-rule 和 branch 的高阶可微性。
