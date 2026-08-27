---
type: concept
status: draft
area: [neural-networks/residual-stability, skip-connections, gating, dense-connectivity]
aliases: [Skip Connection Taxonomy, Highway and Dense Connections]
node_id: NN-46
prerequisites: ["[[残差学习、恒等捷径与退化问题]]", "[[GLU、GeGLU、SwiGLU 与乘性门]]", "[[线性层、批量张量与参数计数]]", "[[局部微分、Jacobian、JVP 与 VJP]]"]
related: ["[[Pre-Activation、Pre-Norm 与 Post-Norm 残差]]", "[[深度、有效路径与稳定性证据地图]]", "[[Embedding Lookup、稀疏梯度与参数规模]]"]
sources: ["[[S-2015-Srivastava-Greff-Schmidhuber-Highway]]", "[[S-2017-Huang-DenseNet]]", "[[S-2016-He-ResNet]]", "[[S-2016-Veit-Residual-Paths]]"]
exercises: ["[[习题 - Highway、Dense Connection 与 Skip 结构比较]]"]
solutions: ["[[解答 - Highway、Dense Connection 与 Skip 结构比较]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-skip-fusion-taxonomy-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Highway、Dense Connection 与 Skip 结构比较

> [!abstract] 本章主问题
> “有一条跳连”不足以定义架构。加法 residual、Highway 门控、DenseNet 拼接和 encoder–decoder long skip 分别通过求和、逐坐标插值、状态扩张与跨尺度传输融合信息，因此具有不同的 shape 合同、Jacobian、参数/激活成本和失效方式。统一比较必须先写 source–transform–fusion–state 五元组。

## 一、学习目标

读完本节，你应能：

1. 用统一五元组描述任意 skip connection；
2. 推导 additive residual 与 coupled Highway 的完整 Jacobian；
3. 解释 Highway 中为什么不能漏掉 gate-derivative 项；
4. 写出 DenseNet 的通道增长、连接数与状态 Jacobian；
5. 区分 addition 的坐标对齐与 concatenation 的坐标保留；
6. 计算 projection、alignment、activation memory 与 memory traffic；
7. 解释图上路径数为什么不等于独立模型数、有效路径或 wall-clock 加速。

## 二、统一五元组

对任何 skip，逐项登记：

$$
\boxed{
(\text{source},\ \text{transform},\ \text{fusion},\ \text{state shape},\ \text{cost})
}.
$$

- **source**：跳过哪些层，从哪个分辨率/时间位置来；
- **transform**：identity、projection、gate、resize、crop 或 attention；
- **fusion**：add、multiply/interpolate、concatenate 或 cross-attend；
- **state shape**：宽度是否固定、增长或压缩；
- **cost**：参数、FLOPs、保存激活、内存流量、通信和串行依赖。

“U-Net 有 skip”“DenseNet 很密”“ResNet 相加”只是名称；五元组才是可推导合同。

## 三、additive residual

最一般的加法块写为

$$
y=P(x)+F(x),
$$

其中 $P$ 可为 identity 或 projection。若两支输出都在 $\mathbb R^D$，则

$$
\boxed{
J_y(x)=J_P(x)+J_F(x)
}.
$$

当 $P=I$ 时得到 $I+J_F$。加法的优点是输出宽度固定，后层不必显式接收不断增长的通道；代价是两支必须具有相同 shape，并默认每个相加坐标属于同一语义坐标系。

若两支尺度严重失配，数值上较小支路可能被 residual stream 淹没；若坐标未对齐，相加会把不同语义强制叠在一起。

## 四、Highway 的门控插值

coupled transform/carry gates 的经典形式是

$$
\boxed{
y=T(x)\odot H(x)+[1-T(x)]\odot x
}.
$$

其中

$$
T(x)\in(0,1)^D
$$

常由 sigmoid 产生。也可写成

$$
y=x+T(x)\odot[H(x)-x].
$$

所以 Highway 不是简单地给 residual branch 乘一个常数；$T$ 本身依赖输入。

## 五、Highway 的完整 Jacobian

记

$$
D_T=\operatorname{Diag}(T(x)),
\qquad
D_{H-x}=\operatorname{Diag}(H(x)-x).
$$

对

$$
y=T\odot H+(1-T)\odot x
$$

逐项微分：

$$
dy=D_TJ_Hdx+D_HJ_Tdx+D_{1-T}dx-D_xJ_Tdx.
$$

整理为

$$
\boxed{
J_y
=D_TJ_H+D_{1-T}+D_{H-x}J_T
}.
$$

三项分别代表：

1. transform branch 的局部传播；
2. frozen-gate 下的 carry；
3. gate 因输入变化而重新分配两支权重。

若把 $T$ 当常数，会漏掉第三项；即使 $T\approx0$，若 $H-x$ 很大且 $J_T$ 不小，gate-derivative 项仍可能重要。

## 六、Highway 标量手算：近 carry 也能相消

令

$$
x=2,
\qquad
H(x)=-1,
\qquad
T(x)=\sigma(0.5x).
$$

则

$$
T(2)=\sigma(1)\approx0.7310586,
$$

$$
y=2-3T\approx-0.193176.
$$

gate 导数为

$$
T'(2)=0.5T(1-T)\approx0.098306.
$$

因为 $H'=0$，

$$
\frac{dy}{dx}
=(1-T)+(H-x)T'
\approx0.268941-3(0.098306)
\approx-0.025977.
$$

若漏掉 gate 导数，会错误得到 $0.268941$，甚至误判导数符号。门控可以保护 carry，也可以通过动态重分配造成相消。

## 七、为什么负 gate bias 有用但不是定理

对 sigmoid gate，令初始 bias 较负可使 $T\approx0$，于是

$$
y\approx x.
$$

这给优化提供近 carry 的初始基线。但偏得过负会使 sigmoid 饱和，$J_T$ 很小、gate 打开缓慢；输入尺度还会改变实际 $T$ 分布。因此必须同时记录 gate mean、saturation fraction、gate gradient 与 branch/carry RMS。

## 八、Dense Connection：融合是拼接

Dense block 中第 $\ell$ 层接收所有先前特征：

$$
z_\ell
=H_\ell([x_0,z_1,\ldots,z_{\ell-1}]).
$$

若定义累计状态

$$
c_{\ell-1}=[x_0,z_1,\ldots,z_{\ell-1}],
$$

则

$$
c_\ell=[c_{\ell-1},H_\ell(c_{\ell-1})].
$$

在可微点，

$$
\boxed{
J_{c_\ell}
=
\begin{bmatrix}
I\\
J_{H_\ell}
\end{bmatrix}
}.
$$

旧坐标被原样保存在累计状态的前部；这与 addition 把两支压到同一坐标不同。但后续层是否读取、压缩或忽略旧坐标，仍由其参数决定。

## 九、growth rate 与通道计数

设 block 输入通道数为 $C_0$，每层新产生 $k$ 个通道，$k$ 称为 growth rate。第 $\ell$ 层输入宽度是

$$
C_0+(\ell-1)k,
$$

$L$ 层后的宽度是

$$
\boxed{C_L=C_0+Lk}.
$$

例：

$$
C_0=64,
\qquad
k=32,
\qquad
L=4,
$$

则最终通道数

$$
C_4=64+4\times32=192.
$$

四层输入通道总计

$$
64+96+128+160=448.
$$

这个 448 不是最终状态宽度，而是忽略 kernel spatial factor 后，四次 convolution 的 input-channel 工作量账本。

## 十、Dense 连接数与成本

第 $\ell$ 层有 $\ell$ 个前驱节点（含 block 输入），总连接数为

$$
\sum_{\ell=1}^L\ell
=\frac{L(L+1)}2.
$$

但连接数 $O(L^2)$ 不直接等于：

- 参数量 $O(L^2)$，因为 bottleneck、growth rate 和共享 kernel 形状会改变计数；
- FLOPs 或 wall time 的精确阶；
- 必须同时驻留显存的独立副本数；
- 独立子网络数。

现代实现可用预分配、checkpointing、fusion 减少复制，但累计特征的读取 traffic 仍需测量。transition layer 的 $1\times1$ convolution 与 pooling 可压缩通道/分辨率，因而会终止“全部坐标永久保留”的简单叙述。

## 十一、long skip：跨尺度与对齐

encoder–decoder 架构常把早期高分辨率特征直接送到后期 decoder：

$$
e_s
\longrightarrow
A_s(e_s)
\longrightarrow
\operatorname{Fuse}(d_s,A_s(e_s)).
$$

$A_s$ 可能包括 crop、resize、projection 或 attention。此类 long skip 的目标常是恢复局部空间细节，而不是只解决极深优化。必须检查：

1. spatial/temporal resolution 是否对齐；
2. channel 与 dtype 是否对齐；
3. padding/crop 是否引入位置偏差；
4. add 还是 concat；
5. encoder activation 保存造成的显存生命周期；
6. 因果模型中是否从未来位置泄漏。

## 十二、四种融合的比较

| 结构 | 典型式 | 状态宽度 | 直接项 | 主要代价/风险 |
|---|---|---:|---|---|
| additive residual | $P(x)+F(x)$ | 固定 | $J_P$ | shape/语义对齐、尺度干涉 |
| Highway | $TH+(1-T)x$ | 固定 | $D_{1-T}$ | gate 参数、饱和、$J_T$ 耦合 |
| Dense concat | $[c,H(c)]$ | 逐层增长 | stacked $I$ | 激活存储与读取 traffic |
| long skip | $\operatorname{Fuse}(d,A(e))$ | 依 fusion | 依对齐图 | 跨尺度对齐、长生命周期 |

没有一种结构在所有维度占优。参数相同不代表 activation memory 相同，FLOPs 相同不代表 memory-bound kernel 的 wall time 相同。

## 十三、路径数不等于有效路径

图结构中可枚举许多 source-to-output routes，但真实贡献还依赖：

- 路径上 Jacobian 的有序乘积；
- activation/gate mask；
- 路径共享的参数与中间状态；
- addition 的相消或 concat 后的选择；
- 数据、损失和训练时间。

因此“有 $2^L$ 种 branch 选择”只是一种代数计数入口。它不证明存在 $2^L$ 个独立模型，也不说明每条路径等权。

## 十四、图：skip 融合分类

先看图回答：四种 skip 分别怎样融合状态？Highway Jacobian 中哪一项最容易漏？Dense block 的最终宽度与累计输入工作量为什么是两个数？

![[00-知识库管理/_assets/figures/neural-networks/fig-skip-fusion-taxonomy-v2.svg|900]]

> [!figure] 图 30.6-06　skip connection 的融合算子、门控导数与宽度账本
> 左栏按 add/gate/concat/long skip 分类；中栏突出 Highway 的 $\operatorname{Diag}(H-x)J_T$；右栏以 $C_0=64,k=32,L=4$ 展示 Dense block 宽度增长。来源：依据 Srivastava et al. 2015、Huang et al. 2017 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_residual_advanced_v2.py]] 确定性生成。

**怎样读图**：先问 fusion 是否改变状态宽度，再检查 direct differential 的形式，最后把参数/FLOPs 与 activation/memory traffic 分开计算。

**图没有证明什么**：图不证明某一种 skip 在固定参数、固定算力或固定显存下必然更优，也不把视觉连线数解释为独立 ensemble 数量。

## 十五、最小验收

1. 用五元组描述四类 skip；
2. 推导 Highway 的三项 Jacobian；
3. 复算标量 gate 例子的输出与导数；
4. 推导 Dense cumulative-state Jacobian；
5. 复算 $C_0=64,k=32,L=4$ 的宽度与通道工作量；
6. 解释 transition compression 和 long-skip alignment；
7. 为参数、FLOPs、activation memory、traffic 与有效路径分别写指标。

> [!summary]
> skip connection 不是一个单一技巧，而是一组融合算子。加法保宽但要求坐标对齐，Highway 用数据依赖 gate 分配 carry/transform，Dense concat 保留旧坐标却扩大状态，long skip 跨尺度传输细节。真正的比较对象是 shape、Jacobian 与系统成本，而不是示意图上有多少根线。

- [[残差连接、深度与稳定性 MOC]]
- [[习题 - Highway、Dense Connection 与 Skip 结构比较]]
- [[解答 - Highway、Dense Connection 与 Skip 结构比较]]
