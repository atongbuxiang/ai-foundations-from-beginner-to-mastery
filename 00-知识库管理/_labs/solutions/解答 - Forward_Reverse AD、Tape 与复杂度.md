---
type: solution
status: draft
area: [neural-networks/automatic-differentiation, complexity]
topic: "[[Forward_Reverse AD、Tape 与复杂度]]"
exercise: "[[习题 - Forward_Reverse AD、Tape 与复杂度]]"
sources: ["[[S-2018-Baydin-AD-Survey]]", "[[S-2008-Griewank-Walther-Evaluating-Derivatives]]", "[[S-2026-JAX-Autodiff-Checkpointing]]", "[[S-2026-PyTorch-Autograd-Gradcheck]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Forward/Reverse AD、Tape 与复杂度
## A
### NN-AD-A01
symbolic differentiation 操作解析表达式并可产生 expression swell；finite difference 用 $f(x\pm hv)$ 近似导数，有 truncation/roundoff 权衡；AD 在程序 trace 上组合 primitive 局部导数，没有 finite-difference truncation，但仍有工作精度舍入和程序语义边界。
### NN-AD-A02
至少包含 primitive identity；parent/output IDs；shape/dtype/device/axis metadata；local VJP 所需 residuals；alias/version、mode、RNG/state 等执行语义。实现还可记 cost、stream 和 rematerialization policy。
### NN-AD-A03
一个 JVP 用一个 input seed $v$；一个 VJP 用一个 output seed $u$。以 basis seeds 形成 full $m\times n$ Jacobian，forward 需 $n$ 个列 seeds，reverse 需 $m$ 个行 seeds。批量化可并行它们，但独立方向信息量不变。
## B
### NN-AD-B01
$x+v\varepsilon$ 先经 square 变成 $x^2+2xv\varepsilon$，再经 sine 变成 $\sin(x^2)+2xv\cos(x^2)\varepsilon$，最后加 $x+v\varepsilon$。所以 primal 是 $\sin(x^2)+x$，tangent 是 $[2x\cos(x^2)+1]v$。
### NN-AD-B02
$a=x_1x_2$，$\dot a=3(1)+2(-1)=1$；$b=\sin a$，$\dot b=\cos6$；$\dot y=\dot b+\dot x_1=\cos6+1$。reverse seed 1 给 $\nabla y=(1+3\cos6,2\cos6)$，与 $v=(1,-1)$ 点积得 $1+\cos6$，和 JVP 一致。
### NN-AD-B03
$f$ 的 $n=20,m=3$：forward 需 20 sweeps，reverse 需 3，选 reverse。$g$ 的 $n=2,m=100$：forward 需 2，reverse 需 100，选 forward。这是基于扫描数的默认，实际还应 benchmark vectorization 和 memory。
## C
### NN-AD-C01
对 $v_i=\phi_i(v_{p_1},…,v_{p_k})$，全微分 $dv_i=\sum_jD_j\phi_i[dv_{p_j}]$。把 $dv$ 理解为由初始 input tangent 引起的方向扰动，就得 $\dot v_i=\sum_jD_j\phi_i[\dot v_{p_j}]$。parents 必须先有 tangent，故按 forward 拓扑序。
### NN-AD-C02
$dL$ 中节点 $v$ 通过所有 children $c$ 出现，$dL|_{dv}=\sum_c\langle\bar c,D_vc[dv]\rangle=\langle\sum_cD_vc^*\bar c,dv\rangle$，故 $\bar v=\sum_cD_vc^*\bar c$。要先获得所有 $\bar c$，因而逆拓扑；sum 就是 fan-out accumulation。
### NN-AD-C03
一个 forward seed 主成本为 $O(C)$，$n$ 个 basis seeds 给 $O(nC)$；一个 reverse seed 为 $O(C)$ 算术加 residual memory，$m$ 个给 $O(mC)$。vectorization 可合并 kernels、降 overhead 并改善 throughput，但 full Jacobian 仍需 $n$ 个独立 input directions 或 $m$ 个 output covectors 才能恢复所有 entries。
## D
### NN-AD-D01
AD 的 exactness 是“不用小 $h$ 做截断近似，按 primitive rules 精确应用链式法则”。primitive 值与 derivative 仍用浮点计算，可 overflow/underflow/cancel；在 ReLU kink 等处 classical derivative 不存在，框架只能返回 convention。
### NN-AD-D02
令 $f(x)=x^2$ if $x>0$，else $-x$。在 $x=1$ trace 只执行 square，AD 返 $2$；在 $x=-1$ 返 $-1$，都是对当次分支的局部导数。在 0 左导数 $-1$、右导数 0，函数不可微；else trace 返 $-1$ 不能改变这一事实。
### NN-AD-D03
`vmap` 把 100 个 seeds 放到一个 batch axis 上同时运行，API 调用次数可为 1，但它仍计算 100 个独立线性作用并存储对应结果。算术、memory 和输出信息不会凭空变成单方向。
## E
### NN-AD-E01
标量 loss 对巨量 parameters 选 reverse。tape 主要包含 layer inputs/outputs、Q/K/V 投影与 attention 所需 statistics/masks、MLP pre/post activations、normalization means/variances、dropout masks/RNG 以及 residual-stream live tensors。应按 bytes 而非只按 node count 盘点。
### NN-AD-E02
保留逐样本 losses $\ell_b$ 或对 model 做 functionalization，然后用每个 output basis seed 的 VJP 并通过 `vmap` 批量化，输出 parameter-tree 前加 batch axis。若先对 $\ell_b$ 取 mean，batch axis 被归约，reverse 只能得聚合 gradient，不能唯一恢复每样本贡献。
### NN-AD-E03
声明 primal/tangent/cotangent tree 和 shape/dtype/device；对多输入做局部 JVP/VJP 伴随 dot test；FP64 方向差分对照；测 broadcast/reduction 和 repeated indices；审计 saved tensors 的 alias/version；对 JVP-of-VJP/VJP-of-JVP 做 HVP 交叉；在 kink、complex 和低精度处单独规定边界。
