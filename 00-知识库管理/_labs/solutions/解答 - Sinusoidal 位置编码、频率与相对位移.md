---
type: solution
status: draft
area: [architecture, positional-encoding, sinusoidal, frequency]
topic: "[[Sinusoidal 位置编码、频率与相对位移]]"
exercise: "[[习题 - Sinusoidal 位置编码、频率与相对位移]]"
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2021-Su-8231-Sinusoidal位置编码追根溯源]]", "[[S-2024-Su-10122-RoPE底数选择]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Sinusoidal 位置编码、频率与相对位移

## A. 识别与复述

### ARCH-SIN-A01
对 $i=0,\ldots,d/2-1$，可写
$$p_{n,2i}=\sin(n\omega_i),\quad p_{n,2i+1}=\cos(n\omega_i),\quad \omega_i=b^{-2i/d}.$$
频率随 $i$ 几何下降；周期 $T_i=2\pi/\omega_i$，故 base 越大，后部慢频周期越长。sin/cos 次序可交换，但实现必须一致。

### ARCH-SIN-A02
单个 sine 平移后会混入 cosine，不能由自身乘一个标量表示；成对通道构成二维相位点，平移就是固定旋转。每一对像不同转速的钟，多频拼接提供从局部到全局的尺度。

### ARCH-SIN-A03
加法公式与相对内积是实数精确恒等式（I）；有限 dtype 下只有近似成立，误差随相位归约和长度变化；模型是否从这些特征学会检索、计数或外推是训练协议下的经验结论（E），不是代数自动推出。

## B. 手算与建模

### ARCH-SIN-B01
依次为 $(1,0),(0,1),(-1,0),(0,-1),(1,0)$。位置 0 与 4 精确碰撞，展示单频周期性。

### ARCH-SIN-B02
$p(1)=(1/2,\sqrt3/2)$，$p(3)=(-1,0)$。旋转角 $2\pi/3$，
$$R(2\pi/3)p(1)=p(3)=(-1,0),$$
具体相乘可由角度相加 $\pi/3+2\pi/3=\pi$ 验证。

### ARCH-SIN-B03
$\omega=(1,0.1,0.01,0.001)$，周期约 $(6.283,62.83,628.3,6283)$。这是理想连续值；实现中的频率生成、通道顺序和 dtype 要另审计。

## C. 推导与证明

### ARCH-SIN-C01
用列向量次序 $(\cos,\sin)$：
$$\begin{bmatrix}\cos\omega(n+\Delta)\\\sin\omega(n+\Delta)\end{bmatrix}
=\begin{bmatrix}\cos\omega\Delta&-\sin\omega\Delta\\\sin\omega\Delta&\cos\omega\Delta\end{bmatrix}
\begin{bmatrix}\cos\omega n\\\sin\omega n\end{bmatrix}.$$
这正是三角加法公式逐项展开。

### ARCH-SIN-C02
内积为 $\cos\omega m\cos\omega n+\sin\omega m\sin\omega n=\cos\omega(m-n)$。多频直接求和：$p(m)^\top p(n)=\sum_i\cos[\omega_i(m-n)]$；若有通道权重则变为加权和。

### ARCH-SIN-C03
$z_n=e^{i\omega n}$，因此 $z_{n+\Delta}=e^{i\omega\Delta}z_n$。复数乘单位相位在实部—虚部坐标中就是 $R(\omega\Delta)$；复共轭乘积 $\bar z_mz_n=e^{i\omega(n-m)}$ 的实部给出相对余弦。

## D. 边界、反例与纠错

### ARCH-SIN-D01
公式在任意 $n$ 可算，只证明输入接口有定义。测试位置的相位组合未必在训练中被正确解释；attention 可见 token 数、softmax 归一化、数值误差和任务分布也随长度变化。无限可计算不等于无限可利用。

### ARCH-SIN-D02
若周期为整数 $T$，$n$ 与 $n+T$ 编码相同，如上一题的 0 与 4。多频精确共同周期可能很长或不存在，但有限精度下只需所有相位差落入容差便近似碰撞；长度增长还会放大相位计算/归约误差。

### ARCH-SIN-D03
增大 base 让低频更低、周期更长，远处更不易重复；但相邻位置相位差 $\omega_i$ 也变小，慢频通道更难区分邻位。最终是覆盖范围与分辨率的多尺度分配，不是“越大越好”。

## E. AI 迁移

### ARCH-SIN-E01
从配置重算期望 $\omega_i$，检查单调性和端点；随机 $n,\Delta$ 比较平移旋转、内积相对性与每对 norm=1；分别用 fp64/fp32/bf16、训练内/外长度记录误差。测试奇数 rotary dimension、错误通道顺序和超大相位的失败行为。

### ARCH-SIN-E02
固定模型、训练 token、数据和推理设置，在 $L_0,2L_0,4L_0$ 上先验证位置值可生成与无 NaN，再测固定目标 token 的 loss、不同 target position 的检索/推理和效率。加入不含远程依赖的局部基线，防止仅因样本更长改变平均指标。

### ARCH-SIN-E03
对齐参数量（位置表单列）、hidden/head dimensions、训练位置分布、最大可见域、optimizer/token budget、微调与测试长度、cache/dtype。分开报告短程回归、外推质量、参数/计算和数值稳定；RoPE/绝对相加的注入点不同，不能只按一个最终分数归因。
