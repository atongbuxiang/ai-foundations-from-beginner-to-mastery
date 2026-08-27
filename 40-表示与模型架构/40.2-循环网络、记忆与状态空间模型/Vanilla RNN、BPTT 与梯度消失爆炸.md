---
type: concept
status: draft
area: [architecture, rnn, optimization]
aliases: [简单循环神经网络, 时间反向传播]
node_id: ARCH-10
prerequisites: ["[[序列因果性、隐藏状态与递推计算]]", "[[标量链式法则与反向传播递推]]", "[[矩阵范数]]"]
related: ["[[LSTM 的记忆单元、门控与梯度通道]]", "[[数值稳定性]]", "[[Lyapunov 稳定性与能量函数]]"]
sources: ["[[S-2013-Pascanu-RNN-Training-Difficulty]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
exercises: ["[[习题 - Vanilla RNN、BPTT 与梯度消失爆炸]]"]
solutions: ["[[解答 - Vanilla RNN、BPTT 与梯度消失爆炸]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-rnn-bptt-jacobian-product-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Vanilla RNN、BPTT 与梯度消失爆炸

> [!abstract] 本节主问题
> Vanilla RNN 在时间上重复同一个非线性映射。前向传播由递推产生，BPTT 则在展开计算图上应用链式法则。远距离信用必须穿过时间 Jacobian 的有序乘积，因此会按方向衰减、放大或旋转；用单个循环矩阵的谱半径不能完整概括一般非线性、时变轨迹。

## 一、从完整形状开始

设

$$
x_t\in\mathbb R^{d_x},\quad h_t\in\mathbb R^{d_h},\quad y_t\in\mathbb R^{d_y}.
$$

一个简单 RNN 为

$$
a_t=W_{hh}h_{t-1}+W_{xh}x_t+b_h,\qquad h_t=\phi(a_t),
$$

$$
o_t=W_{hy}h_t+b_y,\qquad y_t=\psi(o_t).
$$

形状为 $W_{hh}\in\mathbb R^{d_h\times d_h}$、$W_{xh}\in\mathbb R^{d_h\times d_x}$、$W_{hy}\in\mathbb R^{d_y\times d_h}$。参数随时间共享；“展开成深网络”只是计算图视角，不会复制独立参数。

## 二、BPTT 就是展开图上的反向传播

若总损失 $\mathcal L=\sum_{t=1}^{T}\ell_t(h_t)$，状态 $h_t$ 同时影响当前损失和未来状态。定义总伴随

$$
g_t:=\frac{d\mathcal L}{dh_t}.
$$

从链式法则得反向递推

$$
\boxed{g_t=\frac{\partial \ell_t}{\partial h_t}+J_{t+1}^{\top}g_{t+1}},
$$

其中

$$
J_t:=\frac{\partial h_t}{\partial h_{t-1}}
=D_tW_{hh},\qquad D_t=\operatorname{diag}(\phi'(a_t)).
$$

于是远处损失对早期状态的贡献含

$$
\frac{\partial \ell_T}{\partial h_t}
=\frac{\partial \ell_T}{\partial h_T}
J_TJ_{T-1}\cdots J_{t+1},
$$

行/列梯度约定可能让转置位置不同，但“有序乘积”不变。

## 三、参数梯度为何要沿时间求和

$W_{hh}$ 在每一步都被使用，因此

$$
\frac{d\mathcal L}{dW_{hh}}
=\sum_{t=1}^{T}\frac{\partial\mathcal L}{\partial a_t}h_{t-1}^{\top},
$$

其中 $\partial\mathcal L/\partial a_t=D_tg_t$。自动微分会累加共享参数的所有使用点；若手写只保留最后一步贡献，就不再是 BPTT。

## 四、标量例子看清指数效应

令 $h_t=\tanh(wh_{t-1}+ux_t)$，则

$$
\frac{\partial h_T}{\partial h_t}
=\prod_{k=t+1}^{T}w\bigl(1-h_k^2\bigr).
$$

若轨迹接近零且 $|w|<1$，每项约为 $|w|$，乘积指数衰减；若 $|w|>1$ 且未饱和，可能放大；进入 $|h_k|\approx1$ 的 tanh 饱和区后，$1-h_k^2\approx0$，即使 $|w|>1$ 也可能消失。

这说明只看 $w$ 不够，还要看状态轨迹和激活导数。

## 五、多维情形：奇异值比口号更可靠

由次乘性

$$
\left\|J_T\cdots J_{t+1}\right\|_2
\le\prod_{k=t+1}^{T}\|J_k\|_2.
$$

若所有 $\|J_k\|_2\le\rho<1$，得到充分的指数衰减上界；若上界大于 1，只说明“可能很大”，不能证明实际梯度一定爆炸，因为方向可能旋转或抵消。

对固定线性 RNN $h_t=Wh_{t-1}$，$W^n$ 的长期行为与 eigenvalues、Jordan/non-normal structure 相关。谱半径 $\rho(W)<1$ 保证 $W^n\to0$，但有限时间可因 non-normality 出现 transient amplification；一般非线性 RNN 的 $J_t=D_tW$ 又随时间变化，更不能仅凭 $\rho(W)$ 裁决。

## 六、消失、爆炸分别造成什么

- **梯度消失**：早期输入对当前损失的训练信号接近数值零，难学长程信用；
- **梯度爆炸**：梯度范数或局部方向骤增，造成大更新、overflow/NaN 或训练剧烈抖动；
- **状态爆炸**：forward hidden value 本身发散，与梯度爆炸相关但不等同；
- **梯度噪声大**：随机 batch 方向波动，也不等于时间 Jacobian 爆炸。

诊断时至少分别记录 hidden RMS/max、preactivation saturation、per-time gradient、global grad norm 和 finite-value checks。

## 七、gradient clipping 能做什么

全局范数裁剪常写成

$$
\tilde g=g\min\left(1,\frac{\tau}{\|g\|_2+\varepsilon}\right).
$$

当 $\|g\|\le\tau$ 不变；超阈值时保留方向并缩小范数。它可防止一次爆炸梯度造成过大步长，但：

- 不恢复已消失的早期信号；
- 阈值依赖参数尺度、优化器和混合精度；
- 应明确是在 unscale 前还是后裁剪；
- per-value clipping 会改变方向，和 global norm clipping 不同。

## 八、其他缓解手段的作用点

| 方法 | 主要改变 | 不能自动保证 |
|---|---|---|
| orthogonal/unitary 初始化 | 初始循环矩阵尺度 | 非线性轨迹长期保持 |
| ReLU/合适激活 | 减少某些饱和 | 状态和梯度不爆炸 |
| residual/gating | 增加接近 identity 的路径 | 任意长度信用无损 |
| normalization | 控制部分激活统计 | Jacobian 乘积所有方向稳定 |
| truncated BPTT | 降低内存与反向长度 | 超过截断窗的精确信用 |
| gradient clipping | 限制爆炸更新 | 修复消失梯度 |

门控 RNN 的关键不是“更多参数”，而是构造可学习的加法/近恒等路径，详见后两节。

## 九、截断 BPTT 的估计量边界

若每 $K$ 步 detach 状态，反向图不穿过窗口边界。forward 仍可携带更久历史，但参数更新忽略跨窗口的梯度项。这通常降低显存和计算，却对完整序列目标引入偏差。

“模型能在 forward 保存 1000 步信息”与“损失能通过 BPTT 教它如何在 1000 步前写入”是两个问题。

## 十、图：梯度是有方向的时间乘积

先看图回答：为什么同一个时间 Jacobian 乘积能让不同方向分别衰减、近似保持或放大，四种缓解措施又分别作用在哪一段？

![[00-知识库管理/_assets/figures/architecture/fig-rnn-bptt-jacobian-product-v1.svg|900]]

> [!figure] 图 40.2-02　BPTT 的时间 Jacobian、方向性与缓解边界
> 左栏给出反向有序乘积；中栏展示不同方向的衰减、保持与放大；右栏区分 clipping、gating、orthogonal 初始化和截断的作用。来源：依据 Pascanu–Mikolov–Bengio 的分析与链式法则独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_sequence_ssm_v1.py]] 生成。

**怎样读图**：先从末端损失逆着红色链条读有序乘积，再把中栏三条曲线理解为不同奇异方向而非三个独立模型，最后将 clipping、gating、orthogonal initialization 与 truncation 对准各自能改变的计算环节。

**图没有证明什么**：示意曲线不是某个训练 run 的测量，也没有声称保持所有 Jacobian 范数就能保证泛化。

## 十一、一个可执行的诊断顺序

1. 用短序列做 finite-difference/gradcheck，排除实现错误；
2. 记录每个时间步的 $\|\partial\mathcal L/\partial h_t\|$；
3. 记录 $\|h_t\|$ 与 tanh/sigmoid 饱和比例；
4. 增大 $T$，画 log-gradient 对时间距离；
5. 再分别测试 clipping、初始化、门控或截断；
6. 把训练稳定和长程任务正确率分开报告。

只看最终 loss 不能区分“任务不需要长程”“优化没学到”与“数据有泄露”。

## 十二、常见错误

1. 把 $W_{hh}$ 的谱半径当作任意非线性 RNN 梯度的充分判据；
2. 用范数上界大于 1 证明实际梯度必爆炸；
3. 忘记共享参数梯度要跨时间求和；
4. 把状态爆炸、梯度爆炸和随机噪声混同；
5. 说 clipping “解决了”消失梯度；
6. 截断反向后仍声称优化完整长序列 objective；
7. 混合精度下在错误的缩放阶段裁剪。

## 十三、掌握标准

> [!summary]
> - BPTT 是展开计算图上的链式法则；
> - 长程信用含时变 Jacobian 的有序乘积；
> - 消失/爆炸具有方向性，谱半径不是一般充分描述；
> - clipping 限制爆炸更新但不恢复消失信号；
> - truncated BPTT 保留 forward state，却截断参数信用。

能写出前向和反向形状（A）、手算标量 BPTT（B）、推导参数梯度及范数上界（C）、构造谱半径误导或 clipping 无效反例（D），并设计 per-time gradient 诊断实验（E）。

## 十四、练习与独立详解

- [[习题 - Vanilla RNN、BPTT 与梯度消失爆炸]]
- [[解答 - Vanilla RNN、BPTT 与梯度消失爆炸]]

## 参考来源

- [[S-2013-Pascanu-RNN-Training-Difficulty]]
- [[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]
