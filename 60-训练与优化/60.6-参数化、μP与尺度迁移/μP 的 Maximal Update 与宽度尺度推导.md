---
type: derivation
status: verified
area: [training, optimization, parameterization, mup]
node_id: TRN-43
aliases: [Maximal Update Parametrization, μP 宽度指数]
prerequisites: ["[[Standard、NTK 与 Mean-field 参数化]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[Mini-batch 梯度、平均求和与有效 Batch]]"]
related: ["[[Tensor Programs、坐标检查与无限宽极限]]", "[[Embedding、Readout、Attention 与特殊参数组缩放]]", "[[谱条件、高阶 μP 与参数更新稳定性]]"]
sources: ["[[S-2021-Yang-Hu-Feature-Learning]]", "[[S-2022-Yang-Tensor-Programs-V-MuTransfer]]", "[[S-2025-Su-10770-MuP初探]]", "[[S-2026-Su-11605-MuP之上2]]"]
exercises: ["[[习题 - μP 的 Maximal Update 与宽度尺度推导]]"]
solutions: ["[[解答 - μP 的 Maximal Update 与宽度尺度推导]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-mup-maximal-update-exponent-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# μP 的 Maximal Update 与宽度尺度推导

> [!abstract] 一句话结论
> μP 的核心不是背诵“某层学习率除以 width”，而是同时满足：初始化前向非退化、反向信号非退化、每层 feature update 不爆炸也不消失、输出更新为 $O(1)$。随机初始化的和按 $\sqrt n$ 累积，而训练更新常与激活/梯度对齐并按 $n$ 累积；两者的差异正是 width exponent 的来源。

## 一、Maximal Update 到底最大什么

考虑网络族 $f_n$。对 hidden layer $\ell$，希望固定有限训练时域内

$$
\operatorname{RMS}(h^{(\ell)}_{t,n})=\Theta(1),
\tag{1}
$$

并且一步或有限步 feature change

$$
\operatorname{RMS}(h^{(\ell)}_{t+1,n}-h^{(\ell)}_{t,n})
=\Theta(1).
\tag{2}
$$

若式 (2) 随 width 发散，训练不稳定；若趋于 0，极限会退化为 lazy feature。maximal update 的含义是在满足式 (1) 和输出稳定等约束下，选择仍不发散的最大 exponent，让式 (2) 尽量保持非退化。

它不是：

- 每个参数坐标都移动 $O(1)$；
- raw learning rate 数值最大；
- 每步 loss 降幅最大；
- 所有层使用同一个 optimizer 数字；
- width 与 depth 同时任意扩展的万能规则。

## 二、最关键的区别：随机和与对齐和

设 hidden vector $x\in\mathbb R^n$ 的坐标为 $O(1)$，线性层

$$
y_j=\sum_{i=1}^n x_iW_{ij}.
\tag{3}
$$

### 初始化是随机抵消

若 $W_{ij}$ 独立、均值 0、标准差 $n^{-1/2}$，则

$$
\operatorname{RMS}(y_j)
\asymp \sqrt n\,n^{-1/2}=O(1).
\tag{4}
$$

这里 $n$ 项主要按方差相加，得到 $\sqrt n$。

### 梯度更新是结构化对齐

对一批样本，线性层梯度具有外积结构。先看单样本：

$$
G_{ij}=x_i\delta_j,
\tag{5}
$$

其中 $\delta_j=\partial L/\partial y_j$。若更新坐标形如

$$
\Delta W_{ij}=-\gamma_n x_i\delta_j,
\tag{6}
$$

则由本次样本产生的 feature change 为

$$
\Delta y_j
=\sum_i x_i\Delta W_{ij}
=-\gamma_n\delta_j\sum_i x_i^2.
\tag{7}
$$

当 $\operatorname{RMS}(x)=\Theta(1)$ 时，$\sum_i x_i^2=\Theta(n)$，所以

$$
\Delta y_j=\Theta(n\gamma_n).
\tag{8}
$$

要使它为 $O(1)$，必须 $\gamma_n=O(1/n)$。这次各项不是独立零均值噪声，而是通过梯度与同一个 $x$ 对齐，按 $n$ 累积。

> [!important] 初学者必须记住的二分
> Gaussian-like initialization 常给 `CLT scale` $n^{-1/2}$；gradient-induced tensor-product update 常给 `LLN/coherent scale` $n^{-1}$。把更新也按随机抵消估计，会整整错一个 $\sqrt n$。

minibatch 时 $G=X^\top\Delta/B$ 是外积之和；数据相关性和 batch reduction 会改变常数与随机性，但“更新与当前特征不独立”的警告仍然成立。

## 三、三层 MLP：从前向到反向完整走一遍

固定输入/输出维度 $d_{in},d_{out}$，令两个 hidden width 都为 $n$。采用行向量约定：

$$
h^1=\phi(xW^1),\qquad
h^2=\phi(h^1W^2),\qquad
f=h^2W^3,
\tag{9}
$$

其中

$$
W^1\in\mathbb R^{d_{in}\times n},
\quad W^2\in\mathbb R^{n\times n},
\quad W^3\in\mathbb R^{n\times d_{out}}.
\tag{10}
$$

为突出 width 量级，假设 activation 及其导数在典型区间为 $O(1)$，loss 对 logit 的导数 $\delta^3$ 为 $O(1)$，并暂时忽略 bias、norm、batch 与 residual。

### 1. μP 初始化

一套与 [[S-2022-Yang-Tensor-Programs-V-MuTransfer]] 表 3 同约定的尺度是

$$
\operatorname{Std}(W^1)=\Theta(d_{in}^{-1/2}),
\tag{11}
$$

$$
\operatorname{Std}(W^2)=\Theta(n^{-1/2}),
\tag{12}
$$

$$
\operatorname{Std}(W^3)=\Theta(n^{-1}).
\tag{13}
$$

式 (11)—(12) 使 hidden activations 为 $O(1)$。式 (13) 比 standard readout 的 $n^{-1/2}$ 更小，所以随机初始化输出通常是 $O(n^{-1/2})$，趋向 0；实践也可直接 zero-init readout。关键不是让初始随机 logit 必为 $O(1)$，而是为训练后的对齐更新留出 $O(1)$ 通道。

### 2. Readout 的反向与更新

有

$$
\frac{\partial L}{\partial W^3_{jk}}
=h^2_j\delta^3_k=O(1).
\tag{14}
$$

若 SGD 的 readout LR 为 $\eta^3=\Theta(1/n)$，则

$$
\Delta W^3_{jk}=O(1/n).
\tag{15}
$$

聚合到输出：

$$
\Delta f_k
=\sum_{j=1}^nh^2_j\Delta W^3_{jk}
=O(1),
\tag{16}
$$

因为更新与 $h^2$ 对齐，$n$ 项相干累积。

### 3. Hidden matrix 的反向与更新

readout backprop 给

$$
\delta^2_j
\sim \sum_{k=1}^{d_{out}}W^3_{jk}\delta^3_k
=O(1/n),
\tag{17}
$$

因为 $d_{out}$ 固定。于是

$$
\frac{\partial L}{\partial W^2_{ij}}
=h^1_i\delta^2_j
=O(1/n).
\tag{18}
$$

SGD 使用 $O(1)$ LR 即得

$$
\Delta W^2_{ij}=O(1/n).
\tag{19}
$$

再由式 (7)—(8)，$h^1\Delta W^2$ 的每个输出坐标为 $O(1)$：hidden features 发生非退化更新。

### 4. Input matrix 的反向与更新

随机 hidden matrix 把 $\delta^2=O(1/n)$ 反传。每个 $\delta^1_i$ 是 $n$ 项、每项约 $n^{-1}\cdot n^{-1/2}$ 的随机和，因此

$$
\delta^1_i=O(1/n).
\tag{20}
$$

又因 $d_{in}$ 固定，

$$
\frac{\partial L}{\partial W^1_{ri}}
=x_r\delta^1_i
=O(1/n).
\tag{21}
$$

要让每个 first-layer neuron 的 preactivation $x\Delta W^1_{:i}$ 为 $O(1)$，SGD LR 需放大为

$$
\eta^1=\Theta(n).
\tag{22}
$$

于是 $\Delta W^1_{ri}=O(1)$。这看似比 hidden matrix 大很多，但 input fan-in 固定，没有 $n$ 项输入聚合，所以仍产生 $O(1)$ feature update。

## 四、为什么 SGD 与 Adam 的 raw LR 表不同

SGD 保留 gradient coordinate 的量级；Adam-like update 在 $\epsilon$ 不主导且 moments 已建立时近似消去逐坐标尺度：

$$
u_{ij}^{Adam}
\approx\frac{m_{ij}}{\sqrt{v_{ij}}}
=O(1).
\tag{23}
$$

因此同一个目标实际更新需要不同 base LR。

在上一节 MLP、论文表 3 的存储/方向约定下：

| 参数角色 | μP init variance | μP SGD LR | μP Adam LR |
|---|---:|---:|---:|
| input weight；all bias 按 input-like 分类 | $1/\mathrm{fan\_in}$ | $\mathrm{fan\_out}$ | $1$ |
| hidden matrix | $1/\mathrm{fan\_in}$ | $1$ | $1/\mathrm{fan\_in}$ |
| output/readout | $1/\mathrm{fan\_in}^2$ | $1/\mathrm{fan\_in}$ | $1/\mathrm{fan\_in}$ |

表中 $1$ 表示与 width 无关的 base-scale 常数，不是学习率数值必须等于 1。实际要乘可调 base multiplier，并处理 finite base width 的 ratio。

### 检查刚才的推导

- input gradient 是 $O(1/n)$：SGD 乘 $n$，Adam 归一后乘 $1$；
- hidden gradient 是 $O(1/n)$：SGD 原样得到 $O(1/n)$ 更新，Adam 需显式乘 $1/n$；
- readout gradient 是 $O(1)$：两者都需乘 $1/n$ 形成 $O(1/n)$ 更新。

这就是为什么只说“μP learning rate 随 width 变小”不完整：input SGD 恰恰随 fan-out 变大，hidden SGD 不变，而 hidden Adam 才随 fan-in 变小。

> [!warning] Adam 的条件
> 式 (23) 不是恒等式。在初始化早期、$\epsilon$ 主导、稀疏梯度、moment bias correction、clipping 或非平稳区，尺度消去会失效。μP exponent 表必须与 optimizer implementation 和 parameter groups 一起做坐标检查。

## 五、指数账本：不背表也能审计

对某个参数组 $W$ 写六个 exponent：

| 记号 | 含义 |
|---|---|
| $a$ | init entry RMS $\sim n^{-a}$ |
| $p$ | 显式 forward multiplier $\sim n^{-p}$ |
| $g$ | raw gradient entry RMS $\sim n^{-g}$ |
| $r$ | optimizer normalization 后 direction RMS $\sim n^{-r}$ |
| $b$ | group LR $\sim n^{-b}$ |
| $u=r+b$ | actual update entry RMS $\sim n^{-u}$ |

再分别计算：

### 随机初始化贡献

若输入宽度为 $n$ 且项近似独立，

$$
\text{init output RMS}
\sim n^{1/2-p-a}.
\tag{24}
$$

### 对齐更新贡献

若更新与输入外积对齐，

$$
\text{feature update RMS}
\sim n^{1-p-u}.
\tag{25}
$$

要同时为 $O(1)$，典型条件是

$$
p+a=\frac12,
\qquad
p+u=1.
\tag{26}
$$

readout 的初始输出可以有意趋零，因此第一式可改为“不发散”并允许严格小于 $O(1)$；但训练后的输出更新仍需第二式非退化。

## 六、完整 μP 合同还有哪些缺页

三层 MLP 推导故意省略了会改变规则的对象：

- bias 与 normalization vectors；
- embedding、LM head 和 weight tying；
- attention logit scaling；
- non-square hidden matrices 与不同 width ratio；
- residual depth accumulation；
- convolution、gating、MoE、low-rank factors；
- SGD momentum、AdamW decay、Muon/其他矩阵 optimizer；
- batch/sequence/data/training-time 迁移。

这些不是“细节以后再说”，而是 exponent ledger 的输入。TRN-46 将处理特殊参数组，TRN-47 将把 typical RMS 升级到 spectral/worst-case 条件。

## 七、图：一张表背后的四本账

先看图回答：为什么 hidden weight 的初始化是 $n^{-1/2}$，而训练更新却常需要 $n^{-1}$？

![[00-知识库管理/_assets/figures/training-optimization/fig-mup-maximal-update-exponent-ledger-v1.svg|880]]

> [!figure] 图 TRN-43　μP 的随机和、对齐和与参数角色账本
> 左上区分初始化的 $\sqrt n$ 累积和梯度更新的 $n$ 累积；中部沿 readout→hidden→input 完成一遍 backprop 量级；右侧把 SGD 与 Adam 的 direction normalization 翻译成不同 group LR。来源：依据 [[S-2021-Yang-Hu-Feature-Learning]]、[[S-2022-Yang-Tensor-Programs-V-MuTransfer]] 与 [[S-2025-Su-10770-MuP初探]] 原创绘制。

**怎样读图**：先确定参数是 input、hidden 还是 output，再从 gradient entry scale 进入 optimizer；最后检查实际 $\Delta W$ 经本层输入聚合后是否给出 $O(1)$ feature change。

**图没有证明什么**：图只覆盖固定深度、统一 hidden width 的教学 MLP，未覆盖 attention、normalization、tying、残差联合深度极限和长期训练。

## 八、常见错误

1. **初始化与更新都用 $\sqrt n$**：忽略梯度对齐；
2. **只缩 global LR**：无法同时修复 input/hidden/output；
3. **SGD 表抄给 Adam**：忽略 normalization；
4. **把 $O(1)$ 当数值 1**：量级常数仍是待调超参数；
5. **readout 初始趋零就是退化**：要看训练后输出更新是否非退化；
6. **参数 entry 更新小就是 lazy**：hidden matrix 有 $n$ 项聚合；
7. **表格脱离存储坐标**：把 multiplier 吸收入权重会改变 raw LR；
8. **一层推导外推全模型**：特殊参数组必须逐组审计。

## 九、初学者自检

1. 随机初始化为什么按 $\sqrt n$ 累积，而外积更新为什么可能按 $n$ 累积？
2. 在三层 MLP 中，为什么 μP readout 的初始化标准差是 $1/n$ 而非 $1/\sqrt n$？
3. hidden gradient 为 $O(1/n)$ 时，为什么 SGD LR 可为 $O(1)$、Adam LR 却需 $O(1/n)$？
4. input SGD LR 为什么反而随 fan-out 增大？
5. 式 (26) 的两个约束分别控制什么？
6. 如何通过实际 feature change 检查你没有把矩阵方向写反？

## 十、本节出口

你应能从一个固定网络的 forward/backward 推导出每个参数组的

$$
(\text{init},\text{gradient},\text{optimizer direction},\text{LR},\Delta W,\Delta h)
$$

宽度指数，而不是背一张无条件规则表。下一节 [[Tensor Programs、坐标检查与无限宽极限]] 将说明理论的 coordinate law 怎样落到有限模型的实现诊断。
