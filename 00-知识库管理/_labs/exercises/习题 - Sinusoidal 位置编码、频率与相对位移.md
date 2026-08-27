---
type: exercise
status: draft
area: [architecture, positional-encoding, sinusoidal, frequency]
topic: "[[Sinusoidal 位置编码、频率与相对位移]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Sinusoidal 位置编码、频率与相对位移]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - Sinusoidal 位置编码、频率与相对位移

## A. 识别与复述

### ARCH-SIN-A01
写出标准 sinusoidal position encoding 的成对通道公式，并解释 base、频率与周期的关系。

### ARCH-SIN-A02
为什么 sine 与 cosine 必须成对理解？用“相位钟”而非“神秘曲线”解释。

### ARCH-SIN-A03
区分精确代数性质、有限精度性质和训练后模型行为三层结论。

## B. 手算与建模

### ARCH-SIN-B01
在单频 $\omega=\pi/2$ 下，计算位置 $n=0,1,2,3,4$ 的二维编码 $[\cos(\omega n),\sin(\omega n)]$。

### ARCH-SIN-B02
设 $p_\omega(n)=[\cos\omega n,\sin\omega n]^\top$，取 $\omega=\pi/3,n=1,\Delta=2$，手算 $p(n+\Delta)$ 与 $R(\omega\Delta)p(n)$。

### ARCH-SIN-B03
对 $d=8,\text{base}=10000$，列出四个频率 $\omega_i=\text{base}^{-2i/d}$ 与近似周期 $2\pi/\omega_i$。

## C. 推导与证明

### ARCH-SIN-C01
从三角加法公式推导 $p_\omega(n+\Delta)=R(\omega\Delta)p_\omega(n)$。

### ARCH-SIN-C02
证明 $p_\omega(m)^\top p_\omega(n)=\cos(\omega(m-n))$，再推广到多频拼接。

### ARCH-SIN-C03
用复数 $z_n=e^{i\omega n}$ 重写平移性质，并说明它与二维实旋转表示的对应。

## D. 边界、反例与纠错

### ARCH-SIN-D01
反驳：“sinusoidal 编码可以计算任意位置，所以 Transformer 必然无限长度外推。”

### ARCH-SIN-D02
构造单频编码发生精确周期碰撞的两个不同位置；再说明多频只能缓解而非自动消除有限精度混叠。

### ARCH-SIN-D03
解释把 base 调大为何同时增加慢频覆盖、降低某些通道的局部分辨率，而不是单向改进。

## E. AI 迁移

### ARCH-SIN-E01
写一个测试频率表、平移旋转恒等式、范数与 dtype 误差的最小审计方案。

### ARCH-SIN-E02
设计一项从训练长度到多档测试长度的实验，分离位置函数可定义性与语言建模质量。

### ARCH-SIN-E03
比较固定 sinusoidal、可学习绝对表与 RoPE 时，列出必须对齐的参数、训练和推理变量。

## 解答入口

[[解答 - Sinusoidal 位置编码、频率与相对位移]]
