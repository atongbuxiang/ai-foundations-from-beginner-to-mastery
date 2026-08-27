---
type: solution
status: verified
area: [training, optimization, spectral-analysis]
topic: "[[Update-to-Weight Ratio、谱与尺度诊断]]"
exercise: "[[习题 - Update-to-Weight Ratio、谱与尺度诊断]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Update-to-Weight Ratio、谱与尺度诊断

## A. 识别与复述

### TRN67-A01
Global 为 $\|\Delta\|/\|\theta\|$；layer 常用 $\|\Delta W_l\|_F/\|W_l\|_F$；unit 对行/列语义单元计算；spectral 为 $\|\Delta W\|_2/\|W\|_2$。不同分组、Frobenius/operator norm、epsilon 与是否含 decay 会改变数值和问题，故必须写进合同。

### TRN67-A02
LARS 用 layer weight norm 对 raw gradient/含 decay 方向给 trust ratio；LAMB 先作 Adam-like coordinate preconditioning 再 layer scaling；AGC 对 unit gradient-to-weight ratio 裁剪；telemetry UWR 观察最终写回 delta，不必参与控制。

### TRN67-A03
参数谱描述 $W$ 的 operator amplification；更新谱描述本步 $\Delta W$ 集中方向；Hessian 谱描述 loss 对参数方向的局部曲率。三者对象和空间不同，相关不等价。

## B. 手算与构造

### TRN67-B01
Frobenius UWR $=0.1/20=0.005$；spectral UWR $=0.08/8=0.01$。最坏方向相对变化是能量比的两倍，说明 scalar 口径会改变诊断。

### TRN67-B02
rank-one 唯一奇异值 1，故 $\|\Delta W\|_F=1$、entry RMS $=1/\sqrt{10^4}=0.01$、spectral norm 1、stable rank $=1^2/1^2=1$。

### TRN67-B03
ReLU 正齐次使函数保持：$0.1W_2\phi(10W_1x)=W_2\phi(W_1x)$。weight/gradient/update 的坐标尺度改变；除非更新也按保持函数几何的规则变换，两层 norm 比会不同，普通 UWR 非函数不变量。

## C. 推导与证明

### TRN67-C01
若非零奇异值为 $\sigma_1\ge\cdots\ge\sigma_r$，则 $\sigma_1^2\le\sum_i\sigma_i^2\le r\sigma_1^2$。开方得不等式；stable rank $\sum_i\sigma_i^2/\sigma_1^2\in[1,r]$，零矩阵需另定义。

### TRN67-C02
写 $v_0=\sum_i c_iq_i$，则 $(A^\top A)^kv_0=\sum_i c_i\sigma_i^{2k}q_i$。归一后次方向相对 top 方向按 $(\sigma_i/\sigma_1)^{2k}$ 衰减；谱隙小或 $c_1$ 很小会慢，有限步只是估计。

### TRN67-C03
在 $Hq_i=\lambda_iq_i$ 上，$z_{t+1}=(1-\eta\lambda_i)z_t$；收敛需 $|1-\eta\lambda_i|<1$，即对正 eigenvalue $0<\eta\lambda_i<2$。深网 Hessian 随轨迹变、可非凸，optimizer/mini-batch 也不同，故只是局部参照。

## D. 边界、反例与纠错

### TRN67-D01
大层 weight norm 1000、update 1，小层 norm 0.01、update 0.01；global ratio 约 0.001，却小层 UWR=1。全局被大层分母支配。

### TRN67-D02
有限步估计受初始对齐、谱隙和数值误差影响，通常回收 Rayleigh/向量 norm 估计；若初始向量正交 top singular vector，甚至永远漏掉。应报 iteration、restart/residual 和误差性质。

### TRN67-D03
UWR 过小可导致停滞或低精度吞更新；等价重参数化可任意改变 layer ratio而函数相同。稳定/质量还依曲率、方向、噪声、特征变化与 horizon。

## E. AI 迁移

### TRN67-E01
按 embedding rows、Q/K/V/O、MLP up/down、readout 分组；矩阵同时记 Frobenius/spectral ratio、stable rank，unit 按输出行；bias/norm 用绝对 update+专用 epsilon；tied weight 只计一次参数并分别记两路 gradient contribution；分开 task/decay delta，绑定 phase 和 clock。

### TRN67-E02
构造相同 Frobenius norm 的 $\Delta_1=uv^\top$ 与满秩近各向同性 $\Delta_2$；比较 entry RMS（匹配）、top singular、stable rank、随机输入和 top-direction feature change。重复 power/Krylov 估计并用小矩阵 exact SVD 校准。

### TRN67-E03
可说三种观测在同一窗口共同上升，与方向性尺度/局部曲率机制相容；不能说某一个导致另两个或必然导致失败。下一步固定 checkpoint/data，独立操纵 LR/层级 scaling/谱约束，配 negative control 层，检查中介先后与 paired quality/failure。
