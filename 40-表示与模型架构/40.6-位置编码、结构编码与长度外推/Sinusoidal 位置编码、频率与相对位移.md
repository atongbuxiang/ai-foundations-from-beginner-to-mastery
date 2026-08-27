---
type: concept
status: draft
area: [architecture, positional-encoding, sinusoidal, frequency]
aliases: [Sinusoidal Position Encoding, 正弦位置编码, Fourier Position Features]
node_id: ARCH-43
prerequisites: ["[[置换对称性与位置编码的必要性]]", "[[基与坐标]]", "[[矩阵函数与矩阵指数]]"]
related: ["[[位置编码、结构编码与长度外推 MOC]]", "[[RoPE 的旋转推导、群表示与内积]]", "[[长度外推、位置插值与 RoPE 缩放]]", "[[位置分辨率、混叠与长度外推评测]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2021-Su-8231-Sinusoidal位置编码追根溯源]]", "[[S-2024-Su-10122-RoPE底数选择]]"]
exercises: ["[[习题 - Sinusoidal 位置编码、频率与相对位移]]"]
solutions: ["[[解答 - Sinusoidal 位置编码、频率与相对位移]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-sinusoidal-frequency-shift-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Sinusoidal 位置编码、频率与相对位移

> [!abstract] 本节主问题
> Sinusoidal position encoding 把每个位置映为多组不同频率的正弦/余弦相位。它的关键不是“波形看起来平滑”，而是平移 $\Delta$ 在每个二维频率块中恰好对应一个只依赖 $\Delta$ 的旋转矩阵。

## 一、统一写法

令模型维度 $d$ 为偶数，频率

$$
\omega_i=b^{-2i/d},
\qquad i=0,\dots,d/2-1,
$$

其中原始 Transformer 常取 $b=10000$。为方便旋转推导，定义每个二维块

$$
p_i(n)=
\begin{bmatrix}
\cos(\omega_i n)\\
\sin(\omega_i n)
\end{bmatrix}.
$$

完整位置向量是各块拼接：

$$
p(n)=p_0(n)\oplus p_1(n)\oplus\cdots\oplus p_{d/2-1}(n)
\in\mathbb R^d.
$$

有些实现按 $(\sin,\cos)$ 排列，或把频率写为 $1/b^{2i/d}$；只要配对与旋转符号一致，数学等价。不能只看变量名判断布局。

## 二、每个频率对应一个波长

$$
\lambda_i=\frac{2\pi}{\omega_i}.
$$

高频通道 $\omega_i$ 大、波长短：相邻位置相位变化大，局部分辨率高，但较短距离后周期重复。

低频通道 $\omega_i$ 小、波长长：覆盖更长范围，但相邻位置向量差异小。

几何频率表让多个尺度同时存在，类似多位“相位钟”。它不保证编码在任意有限精度和任意长度上都一一对应。

## 三、平移为什么成为旋转

定义

$$
R(\phi)=
\begin{bmatrix}
\cos\phi&-\sin\phi\\
\sin\phi&\cos\phi
\end{bmatrix}.
$$

利用加法公式：

$$
\cos(a+b)=\cos a\cos b-\sin a\sin b,
$$

$$
\sin(a+b)=\sin a\cos b+\cos a\sin b,
$$

得到

$$
p_i(n+\Delta)=R(\omega_i\Delta)p_i(n).
$$

因此给定相对位移 $\Delta$，存在一个与绝对位置 $n$ 无关的 block-diagonal 矩阵 $R_\Delta$，使

$$
p(n+\Delta)=R_\Delta p(n).
$$

这是精确恒等式 I。

## 四、内积怎样只保留相对位移

同一频率块：

$$
p_i(m)^\top p_i(n)
=\cos(\omega_i m)\cos(\omega_i n)
+\sin(\omega_i m)\sin(\omega_i n)
=\cos(\omega_i(m-n)).
$$

完整内积

$$
p(m)^\top p(n)
=\sum_{i=0}^{d/2-1}\cos(\omega_i(m-n))
$$

只依赖 $m-n$，形成平移不变的多频核。

注意：Transformer 实际通常计算

$$
(e_m+p_m)W_Q
\quad\text{与}\quad
(e_n+p_n)W_K
$$

的内积，其中有 content-content、content-position、position-content 和 position-position 四类交叉项；不能把整个 attention score 简化为上述纯位置核。

## 五、线性变换为何能读取相对位移

因为

$$
p(n+\Delta)=R_\Delta p(n),
$$

模型理论上可通过二维块的线性组合将位置 $n$ 的表示变成偏移 $\Delta$ 的位置特征。这是原始 Transformer 选择 sinusoidal 的一个动机。

但“存在 $R_\Delta$”不等于训练会学出所有 $\Delta$ 对应操作；若训练从未出现大位移、参数与目标也未要求使用，函数式定义本身不能补足学习证据。

## 六、频率核与远程衰减

归一化位置核可写

$$
K_b(\Delta)
=\frac{2}{d}\sum_{i=0}^{d/2-1}\cos(\omega_i\Delta).
$$

在一些频率分布和平均意义下，$K_b(\Delta)$ 可能随 $|\Delta|$ 整体下降，但有限频率余弦和一般会振荡，不保证逐点单调。

[[S-2021-Su-8231-Sinusoidal位置编码追根溯源]] 从绝对位置表达相对关系与远程衰减等要求给出反推解释；其中 Taylor 小位置扰动、近似矩阵和频率选择属于带假设 H，不应与上述三角恒等式 I 混在一起。

## 七、混叠与近似碰撞

单一频率有周期：

$$
p_i(n+2\pi/\omega_i)=p_i(n)
$$

（连续位置意义）。离散整数上是否精确重复取决于频率与 $2\pi$ 的算术关系，但有限精度下相位近似相同即可造成数值碰撞。

对两个位置 $m,n$，可比较

$$
\|p(m)-p(n)\|^2
=2\sum_i[1-\cos(\omega_i(m-n))].
$$

若多频相位同时接近 $2\pi$ 的整数倍，距离会很小。位置是否“可分辨”因此依：

- 频率集合与 base；
- 最大长度；
- 计算/存储 dtype；
- 参数投影是否保留这些方向；
- attention logits 的其他内容项和噪声。

## 八、底数 Base 改变了什么

[[S-2024-Su-10122-RoPE底数选择]] 提醒 base $b$ 同时改变最低频率和频率密度。更大 $b$ 通常引入更慢通道、延长某些相位尺度，但可能让低频邻位变化更小；更小 $b$ 提高局部分辨率，却可能更快经历周期。

Base 选择至少是多目标问题：

1. 训练长度内相邻位置区分；
2. 目标最大长度的相位覆盖；
3. 远距离语义聚合先验；
4. dtype 相位计算精度；
5. 不同 head/layer 是否共享频率；
6. 长短任务性能。

满足某条平均核不等式不等于任务最优。

## 九、数值实现

高位置 $n$ 与频率相乘后再计算 sin/cos。低精度直接保存大 angle 可能丢失相位 reduction 精度；常见实现预计算高精度 sin/cos 再 cast，或在更高精度计算 position phases。

测试需覆盖：

- 奇偶 head dimension 与 pair layout；
- sin/cos interleaved 或 half-split；
- cache offset；
- position IDs 非整数/插值时的广播；
- 长位置不同 dtype；
- $p(n+\Delta)$ 与 $R_\Delta p(n)$ 数值误差。

## 十、图：多尺度相位钟

先看图回答：高频和低频通道分别牺牲了什么？为什么中栏恒等式能说明相对位移结构，却不能证明长序列任务性能？

![[00-知识库管理/_assets/figures/architecture/fig-sinusoidal-frequency-shift-v1.svg|900]]

> [!figure] 图 40.6-03　Sinusoidal 的频率阶梯、平移旋转与分辨率—混叠权衡
> 左栏把多频通道画成不同转速的相位钟，中栏给出精确平移和内积恒等式，右栏区分短/长周期及有限精度。来源：依据三角加法公式与 Transformer frequency table 独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_position_v1.py]] 生成。

**怎样读图**：把每一对 sin/cos 当作二维单位向量；位置增加 $\Delta$ 就沿圆旋转 $\omega_i\Delta$。然后横向比较不同频率：没有某一只钟同时拥有无限局部分辨率和无限无重复范围。

**图没有证明什么**：它没有证明默认 base=10000 最优、频率核逐距离单调衰减，或函数式位置在训练长度外自动可用；这些需假设和实验。

## 十一、常见错误与掌握标准

常见错误：sin/cos 配对顺序与旋转矩阵不一致；漏掉 $2\pi$ 把频率当波长；从位置内积只依差值推出完整 attention只依差值；认为连续公式就没有 OOD；把多频编码称为绝对无碰撞；把 β 进制类比当离散编码定理；忽略大 position 的低精度相位误差。

> [!summary]
> Sinusoidal 把位置编码成多组二维相位，满足 $p(n+\Delta)=R_\Delta p(n)$ 和位置内积只依 $m-n$。高频提供局部分辨率、低频提供长尺度；base、最大长度与有限精度共同决定近似混叠。代数相对性不等于学习或外推保证。

能从加法公式重建旋转（A/B）、分析核与位置距离（C）、构造单频/有限精度碰撞（D），并对 base、dtype、长度写数值审计（E）。

## 十二、练习与独立详解

- [[习题 - Sinusoidal 位置编码、频率与相对位移]]
- [[解答 - Sinusoidal 位置编码、频率与相对位移]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2021-Su-8231-Sinusoidal位置编码追根溯源]]
- [[S-2024-Su-10122-RoPE底数选择]]
