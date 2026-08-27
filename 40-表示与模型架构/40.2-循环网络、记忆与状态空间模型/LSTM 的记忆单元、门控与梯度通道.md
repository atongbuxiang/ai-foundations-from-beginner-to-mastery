---
type: concept
status: draft
area: [architecture, rnn, lstm]
aliases: [长短期记忆网络, LSTM 门控记忆]
node_id: ARCH-11
prerequisites: ["[[Vanilla RNN、BPTT 与梯度消失爆炸]]", "[[Sigmoid、Tanh 与饱和梯度]]", "[[激活、分支、广播与梯度累加]]"]
related: ["[[GRU、门控递推与 RNN 结构比较]]", "[[Highway、Dense Connection 与 Skip 结构比较]]", "[[连续与离散线性状态空间模型]]"]
sources: ["[[S-1997-Hochreiter-Schmidhuber-LSTM]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
exercises: ["[[习题 - LSTM 的记忆单元、门控与梯度通道]]"]
solutions: ["[[解答 - LSTM 的记忆单元、门控与梯度通道]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-lstm-cell-gradient-highway-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# LSTM 的记忆单元、门控与梯度通道

> [!abstract] 本节主问题
> LSTM 把对外 hidden state $h_t$ 与内部 cell state $c_t$ 分开，用 forget、input、output gates 控制保留、写入和读出。关键变化是 $c_t$ 的逐元素加法更新，为梯度提供一条可接近恒等的直接路径；它缓解而非无条件消除长期信用问题。

## 一、先声明采用哪个 LSTM

原始 1997 LSTM 与今天库中的 forget-gate LSTM 并不逐式相同。本节采用常见现代版本。拼接

$$
q_t=[h_{t-1};x_t]\in\mathbb R^{d_h+d_x},
$$

计算

$$
f_t=\sigma(W_fq_t+b_f),\quad
i_t=\sigma(W_iq_t+b_i),\quad
o_t=\sigma(W_oq_t+b_o),
$$

$$
\tilde c_t=\tanh(W_cq_t+b_c),
$$

再更新

$$
\boxed{c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t},
$$

$$
\boxed{h_t=o_t\odot\tanh(c_t)}.
$$

所有门和状态通常在 $\mathbb R^{d_h}$，$W_*\in\mathbb R^{d_h\times(d_h+d_x)}$。实现常把四组 affine 合并为一个矩阵乘法，数学上仍是四段输出。

## 二、三个门分别控制什么

- $f_t$：旧 cell 的逐维保留比例；
- $i_t$：候选写入强度；
- $o_t$：内部 cell 对外 hidden 的暴露程度；
- $\tilde c_t$：当前拟写入的有符号候选内容。

门值在 $(0,1)$，是连续控制系数，不是必须采样的 Bernoulli 随机变量，也不要求分量之和为 1。$f_t$ 和 $i_t$ 可以同时接近 1，所以更新不是凸组合；cell magnitude 因而可能累积。

## 三、一个两步手算

为突出 cell 路径，设标量门已给定：$c_0=2$，第一步 $(f_1,i_1,\tilde c_1)=(0.5,0.2,1)$，第二步 $(0.8,0.5,-0.4)$。则

$$
c_1=0.5\times2+0.2\times1=1.2,
$$

$$
c_2=0.8\times1.2+0.5\times(-0.4)=0.76.
$$

若 $o_2=0.9$，则 $h_2=0.9\tanh(0.76)\approx0.577$。注意 $h_2$ 不是 $c_2$；序列化流式状态时通常两者都要保存。

## 四、直接梯度通道为什么更友好

若暂时把门看作已计算的数，并只看 cell 的显式依赖，则

$$
\left.\frac{\partial c_t}{\partial c_{t-1}}\right|_{f_t,i_t,\tilde c_t\text{ fixed}}
=\operatorname{diag}(f_t).
$$

跨多步的直接项为

$$
\frac{\partial c_T}{\partial c_t}\supseteq
\operatorname{diag}\left(\prod_{k=t+1}^{T}f_k\right).
$$

当某维 $f_k\approx1$，该维可有接近恒等的长路径；vanilla tanh RNN 则每步必经 $W_{hh}$ 和激活导数。这是 LSTM 缓解梯度消失的核心结构理由。

## 五、为什么不能写成“彻底解决”

严格总导数还包含门对 $h_{t-1}$、$h_{t-1}$ 对 $c_{t-1}$ 的依赖。即使只看直接项，$0.99^{100}\approx0.366$，$0.95^{100}\approx0.0059$；“接近 1”在很长距离上也会累乘衰减。

此外：

- sigmoid 在大正负 preactivation 区间导数接近 0；
- output gate 小或 $\tanh(c_t)$ 饱和会削弱外部读出路径；
- truncated BPTT 可能在训练图中切断远距信用；
- cell 值可累积并进入数值/激活饱和区；
- 数据若不区分记忆策略，模型不会凭结构自动学会。

所以正确表述是：LSTM 提供可学习的近恒等加法路径，从结构上缓解经典 RNN 的长程优化困难。

## 六、forget gate bias 与时间尺度

若一维 cell 没有新写入且 forget gate 恒为 $f$，则 $c_t=f^tc_0$。定义 half-life $\tau_{1/2}$ 满足 $f^{\tau_{1/2}}=1/2$：

$$
\tau_{1/2}=\frac{\log(1/2)}{\log f}.
$$

当 $f=\sigma(b_f)$ 且输入影响暂小，较大的正 forget bias 给更长初始时间尺度。例如 $f\approx0.9$ 的 half-life 约 6.58 步，$f\approx0.99$ 约 68.97 步。但统一大 bias 也可能造成该忘的信息保留太久；初始化是先验，不是定理。

## 七、参数、算术与状态内存

若将四个 affine 合并，kernel 输出维 $4d_h$。忽略输出头：

$$
\text{parameters}=4d_h(d_x+d_h)+4d_h.
$$

单步主要矩阵乘加约与 $4d_h(d_x+d_h)$ 同阶。流式每层需保存 $(h_t,c_t)$，每样本 $2d_h$ 个 state scalars；vanilla RNN/GRU 通常只保存一个 $d_h$ hidden。训练还需门激活等中间量，不能用流式 state bytes 代替 training activation memory。

## 八、常见变体必须点名

- **peephole**：门直接读取 cell；
- **coupled input-forget gate**：如令 $i_t=1-f_t$；
- **projection LSTM**：hidden/output 通过低维 projection；
- **cell clipping / recurrent dropout**：改变数值与正则合同；
- **bidirectional LSTM**：离线表示可用未来，不再满足单向因果流式接口。

论文写“LSTM”而未给方程和实现设置时，复现信息是不完整的。

## 九、图：加法 cell 通道与遗忘乘积

先看图回答：cell state 的哪条路径不必每步穿过新的候选非线性，为什么 $f=0.99$ 跨很多步后仍不能称为永久记忆？

![[00-知识库管理/_assets/figures/architecture/fig-lstm-cell-gradient-highway-v1.svg|900]]

> [!figure] 图 40.2-03　LSTM cell highway、forget 乘积与保证边界
> 左栏展示保留与写入的加法更新；中栏比较不同 forget 值跨 50 步的直接项；右栏列出结构收益与仍需审计的失败点。来源：依据现代 LSTM 方程和原论文动机独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_sequence_ssm_v1.py]] 生成。

**怎样读图**：先沿 cell 的水平加法路径区分保留项和写入项，再把中栏的 $f$ 连乘解释为直接梯度路径上的可学习时间尺度，最后到右栏核对门饱和、截断 BPTT、数值漂移和任务可识别性。

**图没有证明什么**：它没有把固定的 $f$ 曲线当作训练后门值分布，也未证明所有 LSTM 任务都优于 GRU 或 Transformer。

## 十、最小实现自检

1. 把 $W_*$ 置零并手设 bias，核对门值；
2. 令 $f=1,i=0,o=1$ 的近似极限，检查 cell 保留；
3. 令 $f=0,i=1$，检查 cell 被候选替换；
4. 对一维两步例做 finite-difference gradient；
5. 核对 fused kernel 中 gate order；
6. 流式逐步输出与整段调用输出对齐；
7. reset 后两会话不得共享旧 $(h,c)$。

由于 sigmoid 不会在有限 bias 下精确等于 0 或 1，测试应使用充分大/小 bias 并设置 tolerance，而非期待 exact Boolean gate。

## 十一、常见错误

1. 把 $c_t$ 与 $h_t$ 当成同一状态；
2. 说三门构成概率分布或和为 1；
3. 只写 $\partial c_t/\partial c_{t-1}=f_t$ 却不说明这是固定门的直接项；
4. 从 forget bias 推出确定记忆长度；
5. 忘记流式部署需存两组状态；
6. 把 1997 原始结构与现代 forget-gate 方程混写；
7. 不核对框架 gate order 就迁移权重。

## 十二、掌握标准

> [!summary]
> - LSTM 分离 internal cell 与 exposed hidden；
> - forget/input/output gate 控制保留、写入与读出；
> - cell 的加法更新提供可接近恒等的直接梯度路径；
> - forget 连乘仍可衰减，门饱和和训练截断仍存在；
> - 方程变体、参数账和流式状态都要显式声明。

能复述四个向量的语义（A）、手算 cell/hidden（B）、推导直接梯度与 half-life（C）、纠正“完全解决长依赖”的断言（D），并审计真实 LSTM 实现的 gate order 与 state API（E）。

## 十三、练习与独立详解

- [[习题 - LSTM 的记忆单元、门控与梯度通道]]
- [[解答 - LSTM 的记忆单元、门控与梯度通道]]

## 参考来源

- [[S-1997-Hochreiter-Schmidhuber-LSTM]]
- [[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]
