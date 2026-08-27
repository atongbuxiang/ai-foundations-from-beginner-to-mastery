---
type: solution
status: verified
area: [training, optimization, parameterization, ntk, mean-field]
topic: "[[Standard、NTK 与 Mean-field 参数化]]"
exercise: "[[习题 - Standard、NTK 与 Mean-field 参数化]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Standard、NTK 与 Mean-field 参数化

> [!warning] 使用边界
> 下列 toy scaling 绑定单隐层、固定有限步和所写坐标；深网、Adam、normalization 与不同极限次序需重新推导。

## A. 识别与复述

### TRN42-A01
四元组是 stored coordinates、initialization law、forward multipliers、parameter-group optimizer/LR。He 只给初始化方差；同一随机函数可把 $1/\sqrt n$ 存入权重或显式 multiplier，而 Euclidean gradient 随坐标改变；input/output group LR 和训练时标也决定 feature 是否冻结。

### TRN42-A02
- standard：有限框架默认的 fan-in init 与共享 recipe；误读为一个唯一渐近定义；
- NTK-style：保持非退化函数更新而固定有限步 feature motion 消失；误读为所有无限宽网络；
- mean-field：经验粒子分布在加速时间上演化；误读为普通初始化方差传播；
- μP：保持最大非发散 feature update；误读为一条裸 LR 除 width 规则。

### TRN42-A03
$$
K_\theta=J_\theta J_\theta^\top,\quad
R_K=\|K_t-K_0\|/\|K_0\|,
$$
feature change 为 $\|h_t-h_0\|/\|h_0\|$，linearization error 为 $\|f_t-f_0-J_0\Delta\theta\|/\|f_t-f_0\|$。它们分别依赖 probe、norm、时间和参数层；小 kernel drift 不证明泛化，小 feature change 不证明 output 不学，大 linearization error 也不说明机制一定有益。

## B. 手算与构造

### TRN42-B01
$$
\operatorname{Var}(f_n)=c_n^2n\cdot9.
$$
故 $c_n=1$ 时为 $9n$、发散；$c_n=n^{-1/2}$ 时为 9、非退化；$c_n=n^{-1}$ 时为 $9/n$、趋零。这分别体现无归一化、CLT fluctuation 与零均值 LLN average。

### TRN42-B02
若 $\partial_fL=O(1)$，
$$
\frac{\partial L}{\partial a_i}
=\frac1{\sqrt n}\partial_fL\,\phi_i=O(n^{-1/2}),
$$
$$
\frac{\partial L}{\partial w_i}
=\frac1{\sqrt n}\partial_fL\,a_i\phi_i'x=O(n^{-1/2}).
$$
$O(1)$ LR 和固定有限步使单元 motion 为 $O(n^{-1/2})\to0$。但输出一阶变化含 $n$ 个与梯度相关的 $n^{-1/2}\times n^{-1/2}$ 项，聚合为 $O(1)$。

### TRN42-B03
单粒子 motion 分别是 $O(1/n)$、$O(n^{-1/2})$、$O(1)$。LR $n$（或时间加速 $n$）给非退化 particle motion。这个 raw LR 只适用于该 $1/n$ 坐标和 SGD-style gradient。

## C. 推导与证明

### TRN42-C01
$$
\widetilde c_n\widetilde a_i=(c_n/\lambda_n)(\lambda_na_i)=c_na_i,
$$
故函数相同。梯度
$$
\frac{\partial f}{\partial\widetilde a_i}
=\widetilde c_n\phi_i
=\lambda_n^{-1}\frac{\partial f}{\partial a_i}.
$$
若希望 $a$ 的一步功能变化等价，$\Delta\widetilde a_i=\lambda_n\Delta a_i$，因此 SGD LR 应满足 $\widetilde\eta=\lambda_n^2\eta$。这展示 raw LR 不具备坐标不变性。

### TRN42-C02
连续梯度流 $\dot\theta=-\nabla_\theta L$。平方损失 $L=\frac12\|f-y\|^2$ 给
$$
\nabla_\theta L=J_0^\top(f-y).
$$
在线性化模型中
$$
\dot f=J_0\dot\theta
=-J_0J_0^\top(f-y)
=-K_0(f-y).
$$
若使用 LR/预条件，还会在右侧出现相应常数/metric。

### TRN42-C03
令 residual $r=f-y$，转到 eigenbasis $\widetilde r=Q^\top r$：
$$
\dot{\widetilde r}_k=-\lambda_k\widetilde r_k,
\qquad
\widetilde r_k(t)=e^{-\lambda_kt}\widetilde r_k(0).
$$
小 $\lambda_k$ 使训练 residual 衰减慢；泛化还依赖 target 与 eigenfunctions 对齐、噪声、正则和测试分布，不能由训练速率单独判断。

## D. 边界、反例与纠错

### TRN42-D01
无限宽只是极限轴。NTK 参数化在相应固定时域可得 kernel dynamics；mean-field 或 μP 选择不同 multiplier/LR，可保留 $O(1)$ feature motion。因此应写“某 parameterization、path、time 下的无限宽极限”，不能写“无限宽等于 NTK”。

### TRN42-D02
取 $f=ca$ 与 $\widetilde a=\lambda a,\widetilde c=c/\lambda$。平方损失的一步 SGD 在 $a$ 坐标输出变化约为 $-\eta c^2\partial_fL$；在 $\widetilde a$ 坐标用同一 $\eta$ 时约为 $-\eta c^2\partial_fL/\lambda^2$。初始函数相同，一步输出相差 $\lambda^2$。

### TRN42-D03
固定 kernel 仍可通过重新组合 tangent features 显著降低 loss，故“小 drift”不等于没学。大 drift 只说明线性化变化，可能来自有益表示学习，也可能来自失稳、饱和或错误参数化；最终需看功能、loss、失败和比较协议。

## E. AI 迁移

### TRN42-E01
可取 width $n=128,256,512,1024$，固定 depth/data/optimizer，记录 $t=0,1,8$ 与训练末端。统计 layerwise feature change、kernel drift、linearization error、parameter motion、loss。用初始化 Jacobian 的线性化模型做对照，并在多 seed 上拟合随 width 的 slope。

### TRN42-E02
manifest 应列 $W^1\in\mathbb R^{d_{in}\times n}$、hidden $W^\ell\in\mathbb R^{n\times n}$、readout $W^{out}\in\mathbb R^{n\times d_{out}}$；对每组写 init variance、是否有显式 $1/\sqrt n$ multiplier、optimizer、actual group LR。缺任何一项都无法知道同一初始函数的训练坐标，也不能跨宽比较。

### TRN42-E03
安全模板：
> 在固定架构、optimizer、数据与训练步窗口，width $n\in\{\cdots\}$ 上观察到 hidden relative feature change 与 empirical NTK drift 随 $n$ 下降，且初始化 Jacobian 线性化误差较小；这支持当前有限窗口的 NTK-like 趋势，不证明无限训练时域、其他参数化或测试泛化遵循固定 kernel。

## 无提示重做

- [ ] 48 小时后重建 $1/\sqrt n$ 网络的“单元不动、输出能动”推导。
- [ ] 一周后解释为何重参数化需要平方级 LR 换算。
