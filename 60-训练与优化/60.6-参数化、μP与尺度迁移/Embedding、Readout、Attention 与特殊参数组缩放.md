---
type: derivation
status: verified
area: [training, optimization, mup, embedding, attention]
node_id: TRN-46
aliases: [μP 特殊参数组, Embedding Readout Attention Scaling]
prerequisites: ["[[μP 的 Maximal Update 与宽度尺度推导]]", "[[μTransfer、Base Shape 与超参数零样本迁移]]", "[[Softmax 输出层、Logit 尺度与概率参数化]]"]
related: ["[[输入—输出权重共享与 Weight Tying]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[谱条件、高阶 μP 与参数更新稳定性]]"]
sources: ["[[S-2022-Yang-Tensor-Programs-V-MuTransfer]]", "[[S-2026-Microsoft-MuP-Implementation]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]", "[[S-2024-Su-10001-LoRA差分学习率]]", "[[S-2026-Su-11647-MuP之上3]]"]
exercises: ["[[习题 - Embedding、Readout、Attention 与特殊参数组缩放]]"]
solutions: ["[[解答 - Embedding、Readout、Attention 与特殊参数组缩放]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-mup-special-parameter-group-scaling-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Embedding、Readout、Attention 与特殊参数组缩放

> [!abstract] 一句话结论
> 参数 tensor 的秩或是否“长得像矩阵”不能决定 μP 规则。真正决定 scaling 的是 forward 中怎样使用它：是从一行查表、对 fan-in 求和、向有限词表读出、形成两个相关向量的内积，还是仅做逐坐标仿射。Embedding、LM head、bias/norm、attention 与 tied weights 必须逐角色建立 shape oracle。

## 一、用“使用语义”而非“存储形状”分类

设参数 $P$。先回答五问：

1. 输入维度中哪些随 scale 增长？
2. 输出维度中哪些随 scale 增长？
3. forward 是求和、选择、内积还是逐坐标乘？
4. backward 的梯度是 dense outer product、稀疏行还是共享角色之和？
5. optimizer 是否保留梯度尺度、逐坐标归一或按矩阵谱整形？

只有回答这些，`fan_in`、`fan_out` 和 LR exponent 才有语义。

## 二、Embedding：二维参数，但 forward 没有宽度求和

令词表大小 $V$、model width $d$，embedding table

$$
E\in\mathbb R^{V\times d}.
\tag{1}
$$

token $i$ 的输出是

$$
h=E_{i,:}.
\tag{2}
$$

这不是 $V$ 项或 $d$ 项之和，而是选择一行。因此若要求坐标 RMS 为 $O(1)$，相对于 width $d$，embedding entry 的初始尺度可保持 $d^0$；它仍可乘依赖固定 $V$ 或 base recipe 的常数。

### 稀疏梯度

对 token $i$，

$$
\frac{\partial L}{\partial E_{j,:}}
=\begin{cases}
g_i,&j=i,\\
0,&j\ne i.
\end{cases}
\tag{3}
$$

batch 中同一 token 出现多次时梯度相加/平均。于是 update scale 还依赖：

- token frequency；
- mean/sum reduction；
- sparse/dense optimizer semantics；
- vocabulary partition 与 data parallel；
- padding/masked tokens 是否计入分母。

把 $V$ 当普通 fan-in，用 hidden matrix 的 $1/\sqrt V$ 或 $1/V$ 宽度律，可能完全错过 lookup 语义。

## 三、Readout / LM Head：宽度项在 logits 中求和

不考虑 weight tying，设

$$
W^{out}\in\mathbb R^{d\times V},
\qquad z=hW^{out}.
\tag{4}
$$

每个 logit

$$
z_v=\sum_{j=1}^dh_jW^{out}_{jv}
\tag{5}
$$

包含 $d$ 项。标准随机初始化若 entry std 为 $d^{-1/2}$，初始 logit 为 $O(1)$；但训练梯度

$$
\frac{\partial L}{\partial W^{out}_{jv}}
=h_j(p_v-\mathbf1[v=t])
\tag{6}
$$

与 $h_j$ 对齐，若更新 entry 也是 $d^{-1/2}$，logit update 会按 $d\cdot d^{-1/2}=\sqrt d$ 爆炸。

μP 的一套 readout 合同取

$$
\operatorname{Std}(W^{out}_{jv})=\Theta(d^{-1}),
\qquad
\operatorname{RMS}(\Delta W^{out}_{jv})=\Theta(d^{-1}),
\tag{7}
$$

让初始化 logit 可趋零，而训练后对齐和产生

$$
\Delta z_v
=\sum_jh_j\Delta W^{out}_{jv}
=O(1).
\tag{8}
$$

这正是 `MuReadout` 需要单独存在的原因：它不是普通 hidden linear 的别名。

## 四、Weight Tying：一个参数同时扮演两种角色

语言模型常令

$$
W^{out}=E^\top.
\tag{9}
$$

同一个 $E$ 在输入端是 row lookup，在输出端却参与 $d$ 项求和。naive 做法会遇到冲突：

- embedding 角色希望 width-coordinate 为 $O(1)$；
- readout 角色希望有效输出权重为 $O(1/d)$；
- 梯度同时包含稀疏 input contribution 与 dense output contribution。

解决方向不是任选一张表，而是把**参数存储**与**forward multiplier**分开。例如共享一个 base-scale embedding parameter，在 readout 路径额外乘 width-dependent factor；实现中使用专门的 shared readout 接口。[[S-2026-Microsoft-MuP-Implementation]] 提供 `MuSharedReadout` 方向，具体版本语义需绑定访问日。

> [!warning] 共享权重改变反向合同
> 总梯度是输入角色和输出角色的和。两项的 sparsity、尺度和相关性不同；即使 forward multiplier 正确，optimizer moments 和 clipping 仍可能被某一角色支配。

## 五、Bias 与 Normalization：向量不是退化矩阵

### Bias

$$
y=xW+b.
\tag{10}
$$

$b_j$ 直接加到输出坐标，没有 fan-in 求和。其 update 对 feature 的作用也是 $\Delta y_j=\Delta b_j$。因此 hidden matrix 的 $1/n$ entry update 不能机械套给 bias；论文表把 all biases 与 input-like 参数放在同类 width 规则中，但 zero initialization 和具体 optimizer 常数仍需声明。

### LayerNorm/RMSNorm scale

以 RMSNorm 为例：

$$
y_j=\frac{x_j}{\operatorname{RMS}(x)+\epsilon}\gamma_j.
\tag{11}
$$

$\gamma_j$ 是逐坐标 multiplier。若归一化后的坐标为 $O(1)$，$\gamma_j=O(1)$ 可保持前向；其梯度和更新不通过 $n$ 项输入求和。把 norm weight 送进 Muon 或 hidden-matrix μP group，仅因为它是一维/二维 tensor，都缺乏几何依据。

[[S-2026-Su-11647-MuP之上3]] 从专门的行/列/RMS norm 最速方向讨论这些角色；课程采用“逐角色选范数”的原则，不把单一 optimizer 推荐视为普遍最优。

## 六、Attention：$1/\sqrt{d_h}$ 与 $1/d_h$ 控制不同阶段

单头 attention score

$$
s_{ab}=c_{d_h}\,q_a^\top k_b.
\tag{12}
$$

若初始化时 $q_j,k_j$ 近似独立、均值 0、方差 $O(1)$，则

$$
\operatorname{Var}(q^\top k)=\Theta(d_h).
\tag{13}
$$

标准选择 $c_{d_h}=d_h^{-1/2}$ 使初始 score 为 $O(1)$。这是 [[S-2021-Su-8620-Transformer初始化参数化与标准化]] 中的二阶方差逻辑。

μP 的 Transformer 版本使用 $c_{d_h}=\Theta(d_h^{-1})$（实现可乘 base-head-dimension 兼容常数）。于是若 $q,k$ 仍是独立初始化尺度，初始 score 为 $O(d_h^{-1/2})$ 并趋零；训练后 $q,k$ 的相关、对齐变化可按 $d_h$ 相干累积，使 score update 保持 $O(1)$。

二者没有简单的“谁更正确”：

- $1/\sqrt{d_h}$ 控制随机初始化内积；
- $1/d_h$ 为最大更新和跨宽训练合同保留尺度；
- zero-init query/readout 会改变初始化瞬态；
- softmax 温度、位置 bias 和 sequence length 还会共同影响饱和。

## 七、Head 数与 Head Dimension 是两条路径

因为

$$
d_{model}=h\,d_h,
\tag{14}
$$

把 $d_{model}$ 扩大可有至少两种路径：

### 路径 A：固定 $h$，增大 $d_h$

attention dot-product 的求和项增多，$c_{d_h}$ 必须随规模翻译。

### 路径 B：固定 $d_h$，增大 $h$

每个 head 内 score scaling 不变，但 output concatenation/projection、head averaging 和参数量变化。

### 路径 C：两者同时变化

base/delta 必须同时标记两个 infinite axes；只用 $d_{model}$ 一个 multiplier 可能错分 Q/K/V/O 的 fan-in/fan-out。

因此“跨 $d_{model}$ μTransfer”要报告 head path，而不只是总宽度。

## 八、Q/K/V/O 与非方阵

对 PyTorch-style $W\in\mathbb R^{d_{out}\times d_{in}}$，实际 forward 是 $xW^\top$；对数学行向量约定则常写 $W\in\mathbb R^{d_{in}\times d_{out}}$。转置一次就会交换 fan-in/fan-out。

对于 $d_{in}\ne d_{out}$，至少记录 aspect ratio

$$
\gamma=\frac{d_{out}}{d_{in}}.
\tag{15}
$$

若两者都扩展但比例变化，固定-ratio μP 表只给起点。Q/K/V projection、attention output projection 与 FFN up/down projection 必须各自标注 orientation。

## 九、LoRA 与低秩因子：组合层而非两张独立 Linear

设

$$
W_{eff}=W_0+\alpha AB,
\qquad
A\in\mathbb R^{d_{in}\times r},
B\in\mathbb R^{r\times d_{out}}.
\tag{16}
$$

feature update 为

$$
\Delta(xAB)
=x\Delta A\,B+xA\,\Delta B+x\Delta A\,\Delta B.
\tag{17}
$$

$A$、$B$ 的 gradient scale 互相依赖，zero-init 其中一因子还会使另一因子初始梯度为零。[[S-2024-Su-10001-LoRA差分学习率]] 提供量级入口，但 LoRA 的 rank $r$、model width、alpha convention 与 base weight 是否训练都必须进入合同；不能把 dense hidden rule分别套给 $A,B$ 就称 μP。

## 十、特殊参数组审计表

| 参数组 | Forward 聚合 | 主要 scale axes | 首要遥测 |
|---|---|---|---|
| embedding | row lookup | $d,V$, token support | row/update RMS、频率分层 |
| readout | 对 $d$ 求和 | $d,V$ | logit/update RMS |
| tied embedding/head | lookup + sum | $d,V$ | 两角色梯度与 moments |
| bias | 直接加 | output width | coordinate update |
| norm scale | 逐坐标乘 | normalized width | gamma/update、norm stats |
| Q/K | 投影 + dot product | $d_{model},h,d_h$ | q/k RMS、score、entropy |
| V/O | 加权和 + projection | head/model widths | head output、residual update |
| LoRA A/B | 两段乘积 | $d_{in},r,d_{out}$ | factor/combined update |

## 十一、图：特殊参数组为什么不能套一张表

先看图回答：Embedding 与 LM head 都是 $V\times d$ 相关矩阵，为什么 scaling 仍然相反？

![[00-知识库管理/_assets/figures/training-optimization/fig-mup-special-parameter-group-scaling-v1.svg|880]]

> [!figure] 图 TRN-46　Lookup、Readout、Attention 与共享参数的使用语义
> 左侧比较 embedding 的 row lookup 与 readout 的 width sum，中部展示 tying 后的双角色冲突，右侧把 attention 的随机内积尺度和训练对齐尺度分开；底部列出 bias/norm/LoRA 的专门出口。来源：依据 [[S-2022-Yang-Tensor-Programs-V-MuTransfer]]、[[S-2026-Microsoft-MuP-Implementation]]、[[S-2021-Su-8620-Transformer初始化参数化与标准化]] 与 [[S-2026-Su-11647-MuP之上3]] 原创绘制。

**怎样读图**：不要先看 tensor rank；先沿箭头看 forward 是选择、求和、点积还是乘积，再计算初始化随机和与训练对齐和，最后选择 parameter group 和 optimizer。

**图没有证明什么**：它没有给出所有框架/optimizer 的唯一数值表，也不保证词表、head path、sequence length、weight tying 或 LoRA rank 改变后自动迁移。

## 十二、初学者自检

1. embedding lookup 为什么不产生 $d$ 项的 forward sum？
2. μP readout 为什么允许初始 logit 趋零，却要求训练后 $\Delta z=O(1)$？
3. weight tying 为什么让一个参数同时承受两种 gradient geometry？
4. $1/\sqrt{d_h}$ 与 $1/d_h$ 分别控制怎样的累积？
5. 固定 head 数与固定 head dimension 的扩展路径有什么不同？
6. norm scale 为什么不应进入普通 hidden-matrix optimizer group？
7. LoRA 两因子的 differential LR 为什么必须从组合输出变化推导？

## 十三、本节出口

你应能对每个特殊参数组填写

$$
\text{usage}
\to\text{scale axes}
\to\text{random/aligned aggregation}
\to\text{init/update rule}
\to\text{telemetry},
$$

并拒绝“所有二维权重都按 hidden matrix 缩放”这类无条件 recipe。
