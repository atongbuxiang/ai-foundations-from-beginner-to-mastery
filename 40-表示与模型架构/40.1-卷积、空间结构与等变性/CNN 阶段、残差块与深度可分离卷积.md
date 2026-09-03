---
type: concept
status: draft
area: [architecture, cnn, efficient-architecture]
aliases: [CNN Stage 与 Block, Depthwise-Separable CNN]
node_id: ARCH-07
prerequisites: ["[[通道、卷积核、步幅、填充与膨胀的形状账本]]", "[[残差连接、深度与稳定性 MOC]]", "[[池化、下采样、混叠与不变性边界]]"]
related: ["[[堆叠卷积、感受野与有效感受野]]", "[[群卷积、等变网络与 CNN 证据地图]]", "[[Vision Transformer、Patch Token 与二维结构]]"]
sources: ["[[S-2016-He-ResNet]]", "[[S-2017-Howard-MobileNet]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]"]
exercises: ["[[习题 - CNN 阶段、残差块与深度可分离卷积]]"]
solutions: ["[[解答 - CNN 阶段、残差块与深度可分离卷积]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-cnn-stage-block-budget-v1.svg]]"
created: 2026-08-24
updated: 2026-09-03
---

# CNN 阶段、残差块与深度可分离卷积

> [!abstract] 本节主问题
> 现代 CNN 常按 stage 组织：在同一分辨率重复 block，在 stage 边界下采样并增宽通道。Residual path 管理深度与恒等信息，bottleneck/depthwise-separable block 管理空间混合、通道混合和资源。架构比较应重建 stage 表与成本，而非只背 AlexNet、ResNet、MobileNet 的名字。

## 导读：不要再把 CNN 读成一长串层名

当网络只有两三层时，逐层阅读还勉强可行。现代 CNN 往往有几十甚至上百层，如果仍从 `conv–norm–activation` 一行一行往下数，你会很快失去主线。更有用的读法是先找 stage：哪些 block 在同一分辨率重复，哪里发生下采样，哪里增加通道，哪一条 shortcut 负责把旧表示送到更深处。

这时 residual block 也不该只被记成“加一个 skip connection”。两条支路最终要相加，就必须落在完全相同的 shape；如果主支下采样或改变通道，旁路也要通过 projection 付出参数和算术。把旁路画成一条没有成本的细线，会掩盖 stage 边界真正发生的结构变化。

同样，depthwise-separable convolution 不只是“更便宜的卷积”。它先限定每个输入通道只有自己的空间模式，再用 pointwise matrix 做通道混合，所以减少成本的同时也改变了单层可表达的四维 kernel。我们会先精确算出 standard 与 separable 的参数/MAC 比，再问这种代数节省是否真的能转化为设备上的延迟收益。

## 课程位置与两遍学习路线

- **承接什么：** ARCH-04 已建立单层 shape/parameter/MAC 账，ARCH-05—06 已解释 stage 边界的采样代价与深层覆盖；
- **本页解决什么：** 把现代 CNN 写成可审计的 stage table，分开 shortcut、spatial mixing、channel mixing 与 depthwise factorization，并明确 AI 部署中的代数成本与设备成本；
- **后续为何需要：** ARCH-08 将检验更一般的对称性；40.5 的 Transformer block 和 40.8 的 MoE block 仍使用同样的“主支—旁路—shape—成本”合同。

**第一遍只画 block。** 对每条支路写输入/输出 shape，确认何时能 identity add、何时必须 projection；随后比较 standard 与 depthwise+pointwise 的参数和 MACs。

**第二遍审计表达与系统。** 从 effective kernel 的因式分解读出单层表达限制，再把 algebraic MACs 与 layout、带宽、fusion、batch 和目标设备分开。

### 问题链

1. 为什么现代 CNN 更适合按 stage 而不是按层名阅读？
2. Residual add 的两条支路必须满足什么 shape 合同？
3. $1\times1$ 与 $K\times K$ 分别混合哪些轴？
4. Depthwise+pointwise 为什么节省成本，又限制了哪类 kernel？
5. 下采样增宽时，主支和 projection shortcut 各付出多少预算？
6. 为什么更少参数/MACs 仍可能在真实设备上更慢？

> [!check] 第一遍停靠线
> 若你能对 $[1,32,28,28]$ 的 $3\times3$ 层算出 standard 的 9,216 参数与 7,225,344 MACs，以及 separable 的 1,312 参数与 1,028,608 MACs，就可以进入 ARCH-08。

## 符号与对象账本

| 对象 | Shape/类型 | Block 身份 | 审计问题 |
|---|---|---|---|
| $x$ | $[N,C,H,W]$ | stage 输入/shortcut 来源 | 两支 add 前 shape 是否相同 |
| $F(x)$ | 主支输出 | spatial/channel mixing | stride、norm、activation 放在哪里 |
| $P(x)$ | identity 或 projection | shortcut | 是否下采样、是否改变通道 |
| $D[c,a,b]$ | depthwise kernel | 每个 input channel 的空间模式 | 不跨通道混合 |
| $P[o,c]$ | pointwise matrix | 每个位置的通道混合 | 不扩大空间 RF |
| $K_{\mathrm{eff}}[o,c,a,b]$ | 复合有效 kernel | 单层可表达空间—通道耦合 | 对固定 $c$ 的空间切片受比例约束 |
| $C_{\mathrm{alg}},C_{\mathrm{device}}$ | 代数/设备成本 | MACs 与延迟、能耗 | 不可互相替代 |

### 贯穿算例 $\mathcal C_\square$：同一个空间混合的两种成本

把前三页的局部三点核提升为 $3\times3$ 空间核，并取

$$
X\in\mathbb R^{1\times32\times28\times28},
\qquad C_{out}=32,\quad K=3,\quad S=1.
$$

忽略 bias，standard convolution 的账为

$$
\#\theta_{\mathrm{std}}=32\cdot32\cdot9=9{,}216,
$$

$$
\mathrm{MACs}_{\mathrm{std}}=28^2\cdot9{,}216=7{,}225{,}344.
$$

Depthwise $3\times3$ 再接 pointwise $1\times1$ 的账为

$$
\#\theta_{\mathrm{sep}}=32\cdot9+32\cdot32=1{,}312,
$$

$$
\mathrm{MACs}_{\mathrm{sep}}=28^2\cdot1{,}312=1{,}028{,}608.
$$

比例精确为 $1{,}312/9{,}216=41/288\approx14.24\%$。这是算术合同，不是 latency 结论。

若 stage 边界改成 $32\to64$、stride 2，则主支 $3\times3$ 输出 $[1,64,14,14]$；shortcut 也必须用 stride-2 projection 得到同形状后才能相加。主支与 $1\times1$ projection 分别有 $18{,}432/2{,}048$ 个参数，不能把 projection 当作零成本图线。

## 核心公式七问：可分离 kernel 的结构限制

$$
K_{\mathrm{eff}}[o,c,a,b]=P[o,c]D[c,a,b].
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 把空间 filtering 与通道 mixing 分解，以减少四维 kernel 的参数和算术 |
| 对象 | $D[c,:,:]$ 是 input channel $c$ 的空间核，$P[o,c]$ 把该响应混合到 output channel $o$ |
| 来路 | depthwise 先产生每通道空间响应，pointwise 再在每个位置乘通道矩阵；线性复合得到乘积形式 |
| 步骤 | 固定 $c$ 时先应用 $D[c,:,:]$，随后每个 $o$ 只乘标量 $P[o,c]$；因此不同 $o$ 的空间切片共享同一方向 |
| 读法 | 每个输入通道只学习一个基本空间模式，各输出通道只能重新缩放和组合这些模式 |
| 检查 | $K=1$ 时 depthwise 退化为逐通道缩放；任意 standard kernel 若同一 $c$ 的两个 output 空间切片不成比例，就不能由单层此式精确表示 |
| 去路 | inverted residual 用 expansion/nonlinearity 缓解限制；40.7 的低秩 Attention 与 40.8 的稀疏专家也需区分成本节省和函数类改变 |

这一公式提醒我们：效率技巧从来不只是删掉乘法，它往往同时重写函数类。下面开始画 stage table 时，请始终把四个问题放在一起：shape 是否相容、信息从哪条支路流动、空间与通道分别在哪里混合，以及账面节省是否适配目标硬件。

## 一、从 Layer List 升级为 Stage Table

一个 stage 至少记录：输入/输出分辨率、通道、重复次数、block 类型、首次 stride、kernel/groups、shortcut、参数、MACs、activation bytes 和 receptive field。

典型金字塔：$56^2\times64\to28^2\times128\to14^2\times256$。若空间面积除 4、输入输出通道都乘 2，standard conv 的 $HWC_{in}C_{out}$ 量级近似保持；但 stage 第一层、bottleneck ratio 和实际 layout 会偏离。

## 二、Basic Residual Block

简化写成

$$
y=x+F(x;\theta).
$$

若 shape 相同可用 identity shortcut；若 stride 或 channel 改变，需 projection $P(x)$：

$$
y=P(x)+F(x).
$$

加法要求两支 shape 完全相同。Projection 不是装饰，它改变信息/参数并决定下采样对齐。残差的梯度、Pre-activation 与稳定性已在[[残差连接、深度与稳定性 MOC]]推导，本节关注它在 CNN stage 的形状接口。

## 三、Bottleneck Block

经典 bottleneck 用

$$
1\times1\ (C\to C_b)
\quad\to\quad
3\times3\ (C_b\to C_b)
\quad\to\quad
1\times1\ (C_b\to C_{out}).
$$

第一层压缩 channel，3×3 在较窄空间做 spatial mixing，最后恢复/扩张。其价值依 $C_b/C$；“1×1 不看邻居所以无用”是错误的，它在每个位置进行通道基变换和组合。

## 四、Depthwise-Separable Block

Depthwise $K\times K$ 对每个 channel 独立空间 filtering，pointwise $1\times1$ 混合 channels：

$$
X\xrightarrow{DW(K\times K)}Z\xrightarrow{PW(1\times1)}Y.
$$

它把标准 kernel 的四维耦合限制为“每通道空间核 + 跨通道线性组合”。参数/MAC 比约 $1/C_{out}+1/K^2$，见 [[S-2017-Howard-MobileNet]]。这是结构化低成本 factorization，不与任意标准 conv 完全等价。

## 五、表达限制从哪里来

标准 kernel $K[o,c,a,b]$ 可让每个 output-input channel pair 有独立空间 pattern。Depthwise+pointwise 的 effective kernel

$$
K_{eff}[o,c,a,b]=P[o,c]D[c,a,b],
$$

对固定 input channel $c$，不同 output channels 的空间 kernel 只能是同一 $D[c,:,:]$ 的标量倍数。增加中间 expansion、多个 block 与非线性可提高能力，但单层 factorization 有明确限制。

## 六、Inverted Residual 的思想接口

移动端常先用 pointwise 把低维输入扩到高维，在高维做 depthwise，再投影回低维，并在低维两端 shape 相同时加 shortcut。这里“inverted”指宽窄顺序相对经典 bottleneck 反转。

Linear bottleneck 的动机与 activation 在低维流形上的信息损失相关，但具体性能是经验设计；本节点不把某激活位置写成普遍定理。

## 七、Width、Depth 与 Resolution 缩放

- width multiplier $\alpha$：通道近似乘 $\alpha$，standard conv 参数/MAC 近似乘 $\alpha^2$；
- resolution multiplier $\rho$：两轴乘 $\rho$，MAC 近似乘 $\rho^2$；
- depth multiplier：重复 block 数近似线性增成本，同时扩大 RF/非线性深度。

取整、首尾层、depthwise/pointwise 比例会打破精确幂律，因此最终必须逐层重算。

## 八、为什么 FLOPs 少未必快

Standard $1\times1$ 常转成大 GEMM，设备利用率高；depthwise 每通道工作小、数据重用弱，可能受 memory bandwidth、launch 和 layout 限制。真实部署还受 batch size、quantization、fusion、cache、operator availability 影响。

所以报告至少包含：parameters、MACs/FLOPs、peak activation、latency、throughput、energy、目标硬件和 batch。

## 九、图：Pyramid、Block 与 Cost Factorization

先看图回答：CNN 的“深”究竟发生在同分辨率重复、跨 stage 下采样，还是 block 内通道展开？

![[00-知识库管理/_assets/figures/architecture/fig-cnn-stage-block-budget-v1.svg|900]]

> [!figure] 图 40.1-07　CNN stage 金字塔、残差 block 与可分离成本
> 左栏展示空间减半/通道增宽的 stage 预算；中栏把 spatial mix、channel mix 和 shortcut 分开；右栏对比 standard 与 depthwise+pointwise 的代数成本并提示 latency 边界。来源：依据 ResNet、MobileNet 与 D2L 独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_convolution_advanced_v1.py]] 生成。

**怎样读图**：先沿 stage 记录 shape，再进入 block 看两类 mixing，最后把理论 MACs 与设备测量分开。

**图没有证明什么**：图不证明任何固定 channel doubling 是最优，也不证明 separable block 在每种硬件上更快。

## 十、一个小型成本比较

$H=W=28,C_{in}=C_{out}=128,K=3$，batch 1：standard MACs

$$
28^2\cdot128^2\cdot9\approx115.6\text{M}.
$$

Depthwise+pointwise：

$$
28^2(128\cdot9+128^2)\approx13.75\text{M},
$$

约为 11.9%。但中间需写/read depthwise activation，实际 latency 比必须实测。

## 十一、架构历史怎样使用

LeNet/AlexNet/VGG 展示局部共享、GPU 与深度积累；ResNet 展示 residual stage；MobileNet 展示 separable 与部署折衷。历史节点用于理解设计约束，不应变成型号背诵或 SOTA 排名。现代 backbone 还会混合大 kernel、attention、ConvNeXt 式 block 等，本章统一用 mixing—shape—cost 坐标分析。

## 十二、常见错误

1. 把 stage 与单层混为一谈；
2. shape 变了仍使用 identity shortcut；
3. 把 $1\times1$ 说成不做信息混合；
4. 认为 depthwise+pointwise 与任意 standard conv 完全等价；
5. 用 width multiplier 的近似平方律代替逐层账；
6. 把 parameters/FLOPs/latency/energy 合并为“效率”；
7. 只报设备最快设置，不说明 batch/dtype/kernel。

## 十三、回顾与掌握标准

> [!summary]
> - stage 在固定分辨率重复 block，并在边界改变尺度；
> - shortcut 必须满足 shape 合同；
> - bottleneck 与 separable block 分配空间/通道 mixing；
> - factorization 降成本也限制单层 kernel；
> - 代数成本与部署效率需要两套证据。

## 十四、练习与独立详解

- [[习题 - CNN 阶段、残差块与深度可分离卷积]]
- [[解答 - CNN 阶段、残差块与深度可分离卷积]]

## 参考来源

- [[S-2016-He-ResNet]]
- [[S-2017-Howard-MobileNet]]
- [[S-2023-Zhang-Lipton-Li-Smola-D2L]]
