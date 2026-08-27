---
type: solution
status: draft
area: [architecture, rnn, lstm]
topic: "[[LSTM 的记忆单元、门控与梯度通道]]"
exercise: "[[习题 - LSTM 的记忆单元、门控与梯度通道]]"
sources: ["[[S-1997-Hochreiter-Schmidhuber-LSTM]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - LSTM 的记忆单元、门控与梯度通道

## A. 识别与复述

### ARCH-LSTM-A01
对 $q_t=[h_{t-1};x_t]$，$f,i,o=\sigma(W_*q_t+b_*)$，$\tilde c=\tanh(W_cq_t+b_c)$；$c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t$，$h_t=o_t\odot\tanh(c_t)$。需声明这是现代 forget-gate 版本。

### ARCH-LSTM-A02
Forget 保留旧 cell，input 控制候选写入，output 控制 cell 的对外暴露。三个向量分别经 sigmoid，既不互斥也不要求和为 1，所以不是 categorical probability distribution。

### ARCH-LSTM-A03
$c_t$ 是内部加法记忆通道，$h_t$ 是经 output gate 和 tanh 暴露的状态。下一步门通常读取 $h_t$；流式标准 LSTM 必须同时保存 $(h_t,c_t)$。

## B. 手算与建模

### ARCH-LSTM-B01
$c_1=0.5(2)+0.25(-0.4)=0.9$。$h_1=0.8\tanh(0.9)\approx0.8(0.7163)=0.573$。

### ARCH-LSTM-B02
保留比例 $0.98^{50}\approx0.3642$。Half-life $\log(0.5)/\log(0.98)\approx34.31$ 步。

### ARCH-LSTM-B03
参数 $4d_h(d_x+d_h)+4d_h=4(32)(52)+128=6784$。每样本单层保存 $h,c$，共 $64$ 个标量；bytes 再乘 dtype 大小。

## C. 推导与证明

### ARCH-LSTM-C01
固定每步门和候选时，$\partial c_k/\partial c_{k-1}=\operatorname{diag}(f_k)$。相乘得 $\operatorname{diag}(\prod_{k=t+1}^Tf_k)$，逐元素乘积。

### ARCH-LSTM-C02
取对数得 $\tau=\log(1/2)/\log f$。令 $f=1-\epsilon$，$\log f\approx-\epsilon$，所以 $\tau\approx\log2/(1-f)$。

### ARCH-LSTM-C03
$c_{t-1}$ 还影响 $h_{t-1}=o_{t-1}\tanh(c_{t-1})$，后者进入 $q_t$，再改变 $f_t,i_t,o_t,\tilde c_t$，这些量又进入 $c_t$。因此总导数是直接 $f_t$ 项加多条间接链式项。

## D. 边界、反例与纠错

### ARCH-LSTM-D01
$0.99^{100}\approx0.366$，$0.99^{1000}\approx4.32\times10^{-5}$。每步只损失 1% 仍会随距离指数累积，不能称永久。

### ARCH-LSTM-D02
令 $c_0=0,f_t=i_t=1,\tilde c_t=1$，则 $c_t=c_{t-1}+1=t$。旧值与候选系数之和为 2，不是凸组合，cell 可线性增长。

### ARCH-LSTM-D03
大 bias 只是初始化时让 $f$ 偏大；输入和训练会改变门。任务可能要求快速 reset，大 $f$ 反而拖累；output/readout、BPTT 截断、数据与优化也决定是否利用长记忆。

## E. AI 迁移

### ARCH-LSTM-E01
核对 gate order、权重转置、input/recurrent bias 合并规则、peephole、projection、cell clipping、batch/layer/direction 轴、initial state、bidirectional 拼接、dtype 与 fused-kernel tolerance；用单步中间 gate 对齐。

### ARCH-LSTM-E02
用大 bias 近似：保持 $f\approx1,i\approx0,o\approx1$；清空 $f\approx0,i\approx0$；写入 $f\approx0,i\approx1$ 且候选已知；关闭输出 $o\approx0$ 同时检查 $c$ 仍更新。允许 sigmoid tolerance。

### ARCH-LSTM-E03
若 $L$ 层、hidden $d_h$、batch $B$、每标量 $s$ bytes，单向 state memory 为 $2LBd_hs$。双向层需两个方向且后向状态要求未来输入，无法在严格在线场景对当前帧给出同一离线输出。

