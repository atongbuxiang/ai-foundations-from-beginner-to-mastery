---
type: concept
status: draft
area: [architecture, rnn, gru]
aliases: [门控循环单元, GRU 方程约定]
node_id: ARCH-12
prerequisites: ["[[LSTM 的记忆单元、门控与梯度通道]]", "[[Vanilla RNN、BPTT 与梯度消失爆炸]]"]
related: ["[[Highway、Dense Connection 与 Skip 结构比较]]", "[[连续与离散线性状态空间模型]]"]
sources: ["[[S-2014-Cho-GRU]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]"]
exercises: ["[[习题 - GRU、门控递推与 RNN 结构比较]]"]
solutions: ["[[解答 - GRU、门控递推与 RNN 结构比较]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-gru-gate-conventions-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# GRU、门控递推与 RNN 结构比较

> [!abstract] 本节主问题
> GRU 用 update gate 在旧 hidden 与新候选之间逐维插值，用 reset gate 控制旧 hidden 怎样参与候选生成。它没有与 hidden 分离的 cell state，接口更紧凑；但不同资料的 update convention 和 reset 位置常不同，名称相同不保证数值图相同。

## 一、本节先锁定方程约定

令 $x_t\in\mathbb R^{d_x}$、$h_{t-1}\in\mathbb R^{d_h}$。采用“$z_t=1$ 表示写入新候选”的约定：

$$
r_t=\sigma(W_rx_t+U_rh_{t-1}+b_r),
$$

$$
z_t=\sigma(W_zx_t+U_zh_{t-1}+b_z),
$$

$$
\tilde h_t=\tanh\bigl(W_hx_t+U_h(r_t\odot h_{t-1})+b_h\bigr),
$$

$$
\boxed{h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t.}
$$

有些教材写成 $h_t=z_t\odot h_{t-1}+(1-z_t)\odot\tilde h_t$，把 $z$ 命名为保留比例。两者可通过 $z\leftrightarrow1-z$ 互换；比较时看方程，不看中文标签。

## 二、update gate 是逐维插值

对每个维度 $j$：

$$
h_{t,j}=(1-z_{t,j})h_{t-1,j}+z_{t,j}\tilde h_{t,j}.
$$

因为 $z_{t,j}\in(0,1)$，在固定候选的局部视角中这是旧值与新值的凸组合。不同维可有不同更新率：某维保留长期趋势，另一维快速跟踪当前输入。

若候选和门暂固定，直接导数含 $1-z_t$；因此小 $z_t$ 形成近 identity path。和 LSTM 一样，总 Jacobian 还包含 $z_t,r_t,\tilde h_t$ 对旧状态的导数，不能只保留直接项。

## 三、reset gate 控制候选看到什么

在本节 `reset-before` 方程中，$r_t$ 先逐维抑制 $h_{t-1}$，再乘 $U_h$。当 $r_t\approx0$，候选主要由当前 $x_t$ 决定；当 $r_t\approx1$，候选充分使用旧 hidden。

某些库采用

$$
\tilde h_t=\tanh(W_hx_t+r_t\odot(U_hh_{t-1}+b_{hh})+b_{ih}),
$$

即 `reset-after`。一般矩阵 $U_h$ 与逐元素 $\operatorname{diag}(r_t)$ 不可交换，所以

$$
U_h(r_t\odot h)\ne r_t\odot(U_hh)
$$

通常成立。二者参数数相近，却不是仅靠改名就相同的数值函数。

## 四、一个逐维手算

给定

$$
h_{t-1}=(2,-1),\quad \tilde h_t=(0,3),\quad z_t=(0.25,0.8),
$$

则

$$
h_t=(0.75,0.2)\odot(2,-1)+(0.25,0.8)\odot(0,3)=(1.5,2.2).
$$

第一维更新慢，第二维快速换成候选。门是向量而不是全 cell 一个标量，这是“多时间尺度”直觉的来源之一。

## 五、参数与计算账

本节三组 affine 各输出 $d_h$，合并计数为

$$
\text{parameters}=3d_h(d_x+d_h)+3d_h.
$$

现代标准 LSTM 对应 $4d_h(d_x+d_h)+4d_h$。同 $d_x,d_h$ 下 GRU 参数较少，流式只存 $h_t$ 而非 $(h_t,c_t)$。但实际 latency 取决于 fused kernel、batch、设备、memory layout 和实现；不能只用矩阵数判定谁更快。

## 六、RNN、GRU 与 LSTM 的结构合同

| 维度 | Vanilla RNN | GRU | LSTM |
|---|---|---|---|
| recurrent state | $h$ | $h$ | $(h,c)$ |
| 主要加法路径 | 无显式 gate | hidden interpolation | cell update |
| 常见 gates | 0 | reset + update | forget + input + output |
| 每步 affine 规模 | $1d_h$ | $3d_h$ | $4d_h$ |
| 流式 state scalars | $d_h$ | $d_h$ | $2d_h$ |
| 版本差异 | activation | update/reset convention | peephole/projection/gate order |

这张表是资源与计算图比较，不是性能排行榜。数据规模、任务时间结构、训练预算和实现可反转经验排序。

## 七、门控和状态空间的统一直觉

标量 GRU 直接路径近似

$$
h_t\approx(1-z_t)h_{t-1}+z_t\tilde h_t.
$$

若把 $\tilde h_t$ 看作输入驱动项，它类似 time-varying leaky integrator；$1-z_t$ 是输入依赖 retention。连续线性 SSM 离散后也有 $x_{t+1}=\bar Ax_t+\bar Bu_t$，但 GRU 的门和候选非线性依赖输入与状态。这个桥梁帮助理解 Mamba 的输入依赖选择性，但不能把 GRU 与线性 SSM 说成同一模型。

## 八、图：约定、插值与状态合同

先看图回答：本课程中 $z_t=1$ 偏向旧状态还是新候选，若换一份资料得到相反答案，应该比较名称还是显式方程？

![[00-知识库管理/_assets/figures/architecture/fig-gru-gate-conventions-v1.svg|900]]

> [!figure] 图 40.2-04　GRU update convention、逐维插值与三类 RNN 比较
> 左栏固定本课程方程；中栏展示旧状态和候选的逐维插值；右栏比较 RNN/GRU/LSTM 的状态、加法路径、门数与流式内存。来源：依据 Cho et al. 与常见实现差异独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_sequence_ssm_v1.py]] 生成。

**怎样读图**：先由左栏确定 $z=1$ 的写入语义，再追中栏两条插值箭头和 reset 的乘法位置，最后按 recurrent state、加法路径、门数与流式内存逐项比较 RNN、GRU、LSTM，而不是按模型名做总排名。

**图没有证明什么**：门数和 state bytes 不证明 accuracy、训练速度或长期记忆谁更好。

## 九、权重迁移为何容易错

跨框架迁移至少核对：

1. gate packing 顺序，如 $(r,z,n)$ 或 $(z,r,n)$；
2. update gate 是保留还是写入；
3. reset-before / reset-after；
4. input/recurrent bias 是否分开；
5. row-major 权重是否需转置；
6. initial state shape 与 batch/layer/direction 轴；
7. bidirectional 输出拼接顺序。

可靠方法是构造单步小整数权重和输入，对每个 gate、候选、最终 hidden 做中间值对齐，而不是只比长序列最终 loss。

## 十、什么时候选哪一种

- 小型流式、state memory 受限：GRU 的单状态接口可能有吸引力；
- 需要显式 cell/hidden 分离或已有成熟部署栈：LSTM 仍是可靠基线；
- 研究梯度和动力学：vanilla RNN 是最透明的对照；
- 超长并行训练：应同时比较 convolution/SSM/Attention 等接口，而不是只在三种 RNN 内选择。

选择应建立在目标任务的 validation、延迟分位数、峰值内存、训练稳定与维护成本上。

## 十一、常见错误

1. 不声明 update convention 就比较公式；
2. 认为 reset-before 与 reset-after 可无条件交换；
3. 把 gate 当成硬开关或概率分布；
4. 从参数少直接推出墙钟更快；
5. 从某一 benchmark 推出 GRU 永远胜过 LSTM；
6. 忽略 bidirectional GRU 不适合严格在线因果；
7. 迁移权重时只对最终输出、不对 gate 中间量。

## 十二、掌握标准

> [!summary]
> - GRU 以 update gate 对旧 hidden 和候选逐维插值；
> - reset gate 改变候选生成时旧状态的作用；
> - update 语义和 reset 位置存在实现差异；
> - GRU 只有一个 recurrent state，通常比 LSTM 紧凑；
> - 架构比较必须分方程、状态、参数、硬件和经验结果。

能按选定约定复述方程（A）、手算二维更新（B）、推导直接梯度和参数账（C）、构造 reset 不可交换反例（D），并完成跨框架 GRU 权重审计（E）。

## 十三、练习与独立详解

- [[习题 - GRU、门控递推与 RNN 结构比较]]
- [[解答 - GRU、门控递推与 RNN 结构比较]]

## 参考来源

- [[S-2014-Cho-GRU]]
- [[S-2023-Zhang-Lipton-Li-Smola-D2L]]
