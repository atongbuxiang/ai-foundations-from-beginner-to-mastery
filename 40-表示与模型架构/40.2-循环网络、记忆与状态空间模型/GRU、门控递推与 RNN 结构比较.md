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
updated: 2026-09-03
---

# GRU、门控递推与 RNN 结构比较

> [!abstract] 本节主问题
> GRU 用 update gate 在旧 hidden 与新候选之间逐维插值，用 reset gate 控制旧 hidden 怎样参与候选生成。它没有与 hidden 分离的 cell state，接口更紧凑；但不同资料的 update convention 和 reset 位置常不同，名称相同不保证数值图相同。

## 导读：能不能用一个状态完成保留与写入

LSTM 用 $c_t$ 保存内部记忆，再用 $h_t$ 暴露其中一部分。GRU 选择了更紧凑的路线：不再维护独立 cell，而是让一个 update gate 直接决定旧 hidden 与新候选各占多少。这样流式接口只需携带一个状态，参数也更少；但“更紧凑”不等于在所有任务上更好，它只是作出了另一种存储与控制取舍。

本节最重要的第一步不是背门公式，而是锁定 convention。我们规定 $z_t=1$ 表示完全写入新候选，$z_t=0$ 表示完全保留旧状态。另一些教材恰好反过来定义。如果只看“update gate”这个名字，不看最终插值式，同一组权重可能被解释成完全相反的时间尺度。

第二个需要慢下来看的地方是 reset gate。把 gate 放在矩阵乘法之前，和放在矩阵乘法之后，一般不会得到相同结果，因为逐元素乘法与跨通道矩阵混合并不交换。我们会用一个 $2\times2$ 非对角矩阵把两种实现算成不同答案。这个反例说明，模型名称相同、参数数量相同，也不能保证计算图和权重格式兼容。

## 课程位置与两遍学习路线

- **承接什么：** LSTM 用 $(h_t,c_t)$ 和三类门拆开存储与暴露；本页研究能否用一个状态和两类门保留主要的加法更新优势；
- **本页解决什么：** 从“保留旧 hidden 还是写入新候选”的逐维插值推导 GRU，给出 reset-before/after 的不可交换反例，并把 RNN、GRU、LSTM 放进同一参数—状态—梯度合同；
- **后续为何需要：** ARCH-13 会把门控 retention 与离散状态转移并置，ARCH-16 的选择性 SSM 也会使用输入依赖的写入、保留与读出直觉。

**第一遍只锁定本课程约定。** 牢记本页 $z_t=1$ 表示更偏向新候选，手算二维插值，并从 $(1-z_t)$ 读出一条显式近恒等路径。

**第二遍审计实现差异。** 用矩阵不可交换反例区分 reset-before 与 reset-after，再核对 gate order、bias packing、状态轴和真实硬件 latency；模型名相同不是权重可直接互换的证据。

### 问题链

1. GRU 为什么能只保存一个 $h_t$，而 LSTM 通常要保存 $(h_t,c_t)$？
2. 本课程的 $z_t=0$ 与 $z_t=1$ 分别退化成什么更新？
3. update gate 为什么是逐维软插值，而不是整个状态共用的硬开关？
4. reset gate 作用在候选生成的哪一个位置？
5. 为什么 $U_h(r_t\odot h)$ 与 $r_t\odot(U_hh)$ 通常不相等？
6. 参数更少、状态更小，为什么仍不能直接推出墙钟更快或任务更准？
7. 跨框架迁移 GRU 权重时，哪些中间量必须逐项对齐？

> [!check] 第一遍停靠线
> 若你能按本页约定复算 $h_t=(1/2,1)$，写出显式直接系数 $(3/4,1/4)$，并用一个 $2\times2$ 矩阵证明 reset-before 与 reset-after 得到 $(1,0)$ 和 $(2,0)$，就完成了本卷前半段的首遍目标。

## 符号与对象账本

| 对象 | 数学身份 | AI 中的身份 | 不能偷换成 |
|---|---|---|---|
| $z_t$ | 候选写入比例 | update gate | 所有资料都同义的“保留门” |
| $1-z_t$ | 旧 hidden 保留比例 | 直接 identity-path 系数 | 完整 recurrent Jacobian |
| $r_t$ | 旧 hidden 进入候选的调制向量 | reset gate | 清零最终状态的 reset API |
| $\tilde h_t$ | 输入与受控旧状态生成的候选 | candidate hidden | 已经更新完成的 $h_t$ |
| $h_t$ | 单一递推状态 | GRU 流式缓存 | LSTM 的 cell state |
| reset-before | $U_h(r_t\odot h)$ | 一类 GRU 实现 | reset-after 的改名版本 |
| reset-after | $r_t\odot(U_hh+b)$ | 另一类 GRU 实现 | 与前者普遍数值等价 |

### 贯穿算例 $\mathcal S_\square$：插值账与不可交换反例

先只看最终更新。给定

$$
h_{t-1}=(1,-2),\qquad
\tilde h_t=(-1,2),\qquad
z_t=\left(\frac14,\frac34\right),
$$

按本课程“$z$ 是写入比例”的约定，

$$
\begin{aligned}
h_t
&=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t\\
&=\left(\frac34,\frac14\right)\odot(1,-2)
+\left(\frac14,\frac34\right)\odot(-1,2)\\
&=\left(\frac12,1\right).
\end{aligned}
$$

在候选与门暂时固定的局部视角中，旧状态的显式直接系数为

$$
1-z_t=\left(\frac34,\frac14\right).
$$

第一维慢更新，第二维快更新；这给出了“同一 hidden 的不同维可有不同时间尺度”的最小实例。

再固定

$$
U_h=\begin{bmatrix}1&1\\0&1\end{bmatrix},\qquad
r=(1,0),\qquad h=(1,1).
$$

reset-before 得

$$
U_h(r\odot h)
=U_h(1,0)^{\mathsf T}
=(1,0)^{\mathsf T},
$$

而 reset-after 得

$$
r\odot(U_hh)
=(1,0)\odot(2,1)
=(2,0)^{\mathsf T}.
$$

两者不等，因为一般矩阵混合通道与逐元素 gate 不可交换。只有 $U_h$ 为相容对角结构、$r$ 为共同标量或落入其他特殊情形时，结果才可能一致。

沿用 ARCH-11 的 $d_x=3,d_h=4$，GRU 参数量为

$$
3d_h(d_x+d_h)+3d_h
=3\cdot4\cdot7+12=96,
$$

流式只保存 $d_h=4$ 个状态标量；相同维度的现代 LSTM 对应 128 个参数和 8 个状态标量。这是结构账，不是准确率或墙钟排行榜。

## 核心公式七问：GRU 的门控插值

$$
\boxed{h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t.}
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 用单一状态在旧信息和当前候选之间逐维选择更新速率 |
| 对象 | $h_{t-1}$ 是旧状态，$\tilde h_t$ 是候选内容，$z_t$ 是本页约定下的写入比例 |
| 来路 | 将 LSTM 的保留/写入直觉耦合成和为 1 的 hidden 插值，同时取消独立 cell/output gate |
| 步骤 | 先由 $r_t$ 调制旧状态并生成候选，再由 $z_t$ 混合旧状态与候选 |
| 读法 | 每个维度分别决定“保留多少旧值、换入多少新值” |
| 检查 | $z=0$ 应精确保留，$z=1$ 应精确采用候选；换资料时必须检查它是否把 $z$ 定义成保留比例 |
| 去路 | 固定小 $z$ 类似慢 leaky integrator；输入依赖 $z_t$ 为选择性状态更新提供直觉桥梁 |

因此，比较 GRU、LSTM 和 vanilla RNN 时，不应只列门的数量。我们需要同时比较状态接口、直接梯度通道、参数与缓存、实现 convention 以及真实设备行为。下面先把本页约定完整写出，再从两个退化端点检查它是否符合我们刚才的语言解释。

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
