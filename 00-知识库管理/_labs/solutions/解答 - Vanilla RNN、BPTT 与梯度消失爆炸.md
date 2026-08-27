---
type: solution
status: draft
area: [architecture, rnn, optimization]
topic: "[[Vanilla RNN、BPTT 与梯度消失爆炸]]"
exercise: "[[习题 - Vanilla RNN、BPTT 与梯度消失爆炸]]"
sources: ["[[S-2013-Pascanu-RNN-Training-Difficulty]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Vanilla RNN、BPTT 与梯度消失爆炸

## A. 识别与复述

### ARCH-RNN-A01
$a_t=W_{hh}h_{t-1}+W_{xh}x_t+b_h$，$h_t=\phi(a_t)$，$o_t=W_{hy}h_t+b_y$。形状依次为 $d_h\times d_h,d_h\times d_x,d_h,d_y\times d_h,d_y$；这些对象在所有 $t$ 复用。

### ARCH-RNN-A02
BPTT 是把递推按时间展开后应用反向模式自动微分。一个共享参数在展开图中出现 $T$ 次，总导数等于每个使用点局部贡献之和，而不是只取最后一次。

### ARCH-RNN-A03
状态爆炸是 forward $h_t$ 变大；梯度爆炸是 backward 导数变大；梯度消失是远程信用接近零；梯度噪声是 minibatch 间估计波动。它们可同时发生但诊断量不同。

## B. 手算与建模

### ARCH-RNN-B01
$h_1=2,h_2=1,L=1/2$。$dL/dh_2=1$，故 $dL/dh_1=w=1/2$。$w$ 在两步使用：$dL/dw=(dL/dh_1)h_0+(dL/dh_2)h_1=0+2=2$。

### ARCH-RNN-B02
$h_1=\tanh(0.2)\approx0.197$，$h_2=\tanh(0.395)\approx0.376$。导数为 $[2(1-h_2^2)][2(1-h_1^2)]\approx(1.717)(1.922)\approx3.300$，短期发生放大。

### ARCH-RNN-B03
$\|g\|_2=5$，global clip 比例 $2/5$，得 $(1.2,1.6)$，方向不变。Elementwise clip 得 $(2,2)$，范数 $2\sqrt2>2$ 且方向改变。

## C. 推导与证明

### ARCH-RNN-C01
$h_t$ 对损失的影响分为当前 $\ell_t$ 和经 $h_{t+1}$ 影响未来损失。链式法则给 $g_t=\partial\ell_t/\partial h_t+(\partial h_{t+1}/\partial h_t)^Tg_{t+1}$。

### ARCH-RNN-C02
令 $\delta_t=dL/da_t=D_tg_t$。因 $a_t$ 对 $W_{hh}$ 的微分为 $dW_{hh}h_{t-1}$，Frobenius 配对得到局部梯度 $\delta_th_{t-1}^T$，对全部共享使用点相加。

### ARCH-RNN-C03
由次乘性，$\|J_{t+n}\cdots J_{t+1}v\|_2\le\prod_{k=t+1}^{t+n}\|J_k\|_2\|v\|_2\le\rho^n\|v\|_2$。这是充分上界，不是所有方向的等式。

## D. 边界、反例与纠错

### ARCH-RNN-D01
取 $W=\begin{bmatrix}0&M\\0&0\end{bmatrix}$。两特征值均为 0，故 $\rho(W)=0$；但 $\|W\|_2=M$，对 $v=(0,1)^T$ 一步放大为 $(M,0)^T$。虽 $W^2=0$，有限步仍可巨大。

### ARCH-RNN-D02
Clipping 只在总梯度已经很大时缩放更新。若早期信用经过 Jacobian 后已成为 $10^{-20}$，裁剪不会把它放大；数据可识别性、截断、门饱和和优化仍限制长依赖。

### ARCH-RNN-D03
范数乘积是最坏方向上界，实际向量可能进入后续矩阵的 null space。例：$J_1=\mathrm{diag}(2,0)$，$J_2=\mathrm{diag}(0,2)$，两者范数均 2，但 $J_2J_1=0$。

## E. AI 迁移

### ARCH-RNN-E01
构造目标必须依赖早期标记、控制互信息和 shortcut；retain 每步 $h_t$ 的梯度并画 $\log\|g_t\|$ 对距离；另做把早期标记随机化的性能差。若任务可解而早期梯度近零，支持优化瓶颈；若目标可由近期 shortcut 解，不能据梯度小下结论。

### ARCH-RNN-E02
Forward state 可跨窗口继续携带历史；反向在每 $K$ 步 detach；因此忽略跨边界参数导数，对完整 objective 通常有偏；激活内存从约 $O(T)$ 降为 $O(K)$。还应说明窗口 overlap 与 loss placement。

### ARCH-RNN-E03
顺序通常是 forward → scaled loss backward → unscale gradients → 检查非有限值 → global norm clip → optimizer step → scale update。记录 pre/post-clip norm、clip fraction、loss scale、overflow/skip、hidden RMS 与学习率；若在 unscale 前用未校正阈值，裁剪尺度错误。

