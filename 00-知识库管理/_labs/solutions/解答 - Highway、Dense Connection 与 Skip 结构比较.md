---
type: solution
status: draft
area: [neural-networks/residual-stability, skip-connections, gating, dense-connectivity]
topic: "[[Highway、Dense Connection 与 Skip 结构比较]]"
exercise: "[[习题 - Highway、Dense Connection 与 Skip 结构比较]]"
sources: ["[[S-2015-Srivastava-Greff-Schmidhuber-Highway]]", "[[S-2017-Huang-DenseNet]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Highway、Dense Connection 与 Skip 结构比较

## A

### NN-HDS-A01

五元组是 $(source,transform,fusion,state\ shape,cost)$。additive residual 可写：同层输入 $x$、identity/projection $P$、addition、固定输出宽度、branch 参数/FLOPs 与双支读取。Dense concat 可写：block 内全部先前状态、identity 读取加新变换 $H_\ell$、channel concat、宽度 $C_0+\ell k$、增长的 activation/traffic 与 transition compression。

### NN-HDS-A02

$$
\begin{aligned}
\text{add: }&y=P(x)+F(x),\\
\text{Highway: }&y=T(x)\odot H(x)+[1-T(x)]\odot x,\\
\text{Dense: }&c_\ell=[c_{\ell-1},H_\ell(c_{\ell-1})],\\
\text{long skip: }&y_s=\operatorname{Fuse}(d_s,A_s(e_s)).
\end{aligned}
$$

### NN-HDS-A03

addition 要求两支在相同 shape 和语义坐标上逐项求和，因此两者身份在输出坐标中叠加。concatenation 给两支分配不同 channel 区段，旧坐标可被原样保存，混合推迟到后层；代价是状态宽度与读取量增加。

## B

### NN-HDS-B01

$$
T=\sigma(1)=0.7310586,
$$

$$
y=T(-1)+(1-T)2=2-3T=-0.193176.
$$

$$
T'=0.5T(1-T)=0.098306.
$$

因为 $H'=0$，

$$
y'=(1-T)+(H-x)T'
=0.268941-3(0.098306)
=-0.025977.
$$

漏掉 gate 导数会给错误值 $1-T=0.268941$，连符号都错。

### NN-HDS-B02

五层输入通道依次为

$$
48,64,80,96,112.
$$

最终通道

$$
48+5(16)=128.
$$

输入通道总和

$$
48+64+80+96+112=400.
$$

连接数

$$
5\times6/2=15.
$$

### NN-HDS-B03

$$
J=P+A
=\operatorname{diag}(1,0.5).
$$

秩为 2，两个坐标增益为 $1$ 和 $0.5$。projection shortcut 本身删除第二坐标，但 branch 在该例中补回了该方向。因此“shortcut 丢失”不必等于“整块丢失”；必须分析 $P+A$。

## C

### NN-HDS-C01

对

$$
y=T\odot H+(1-T)\odot x
$$

有

$$
dy=D_TJ_Hdx+D_HJ_Tdx+D_{1-T}dx-D_xJ_Tdx.
$$

合并 gate 项：

$$
J=D_TJ_H+D_{1-T}+D_{H-x}J_T.
$$

三项分别是 transform 传播、carry 传播和 gate 根据输入重新分配两支造成的贡献。

### NN-HDS-C02

$$
dc_\ell
=
\begin{bmatrix}
dc_{\ell-1}\\
J_{H_\ell}dc_{\ell-1}
\end{bmatrix},
$$

所以

$$
J_{c_\ell\leftarrow c_{\ell-1}}
=\begin{bmatrix}I\\J_{H_\ell}\end{bmatrix}.
$$

其上部恰为 $dc_{\ell-1}$，故任意扰动都作为原坐标的一部分保留。该结论依赖无 compression/crop/量化和精确 concat；它不说明后续输出一定使用这些坐标。

### NN-HDS-C03

第 1 层只读 $C_0$，每增加一层多出 $k$ 个先前输出，故第 $\ell$ 层输入为 $C_0+(\ell-1)k$。$L$ 层后累计新增 $Lk$，所以 $C_L=C_0+Lk$。所有层输入通道之和为

$$
\sum_{\ell=1}^L[C_0+(\ell-1)k]
=LC_0+k\frac{L(L-1)}2.
$$

## D

### NN-HDS-D01

检查 batch、height/width/time、channel、stride、padding origin、crop offset、位置编码、dtype/scale 与语义层级。合法 alignment $A$ 进入

$$
y=F(d)+A(e)
$$

的 Jacobian 为对 encoder 输入的 $J_A$，或 concat 时成为 stacked block。若 resize/crop 非可逆，其 nullspace 与边界效应必须报告。

### NN-HDS-D02

参数量计可训练标量；FLOPs 计算术；activation memory 计生命周期内保存张量；traffic 计数据搬移；critical path 计不可并行依赖。相同 FLOPs 可因 concat 读取成为 memory-bound；相同参数可有不同激活；相同峰值显存可用 checkpointing 换取更多 FLOPs；相同计算量也可因同步和 kernel granularity 有不同 latency。

### NN-HDS-D03

负 bias 使 $T$ 小、输出接近 carry，但也可能让 sigmoid 饱和，$T(1-T)$ 与 gate gradient 变小；低精度还可能把很小 $T$ 或 update 量化为零。至少记录 gate mean/quantiles、饱和比例、$\|J_T\|$ 或 gate-gradient norm、$\|H-x\|$、transform/carry RMS、gate update-to-weight、非零比例和不同 dtype 对照。

## E

### NN-HDS-E01

$O(L^2)$ 只精确描述 dense graph 的连接计数。参数量取决于 growth rate、bottleneck 与 kernel；FLOPs 取决于逐层输入通道和空间尺寸；显存取决于激活保存、实现与 checkpointing；有效路径还取决于 Jacobian、gate、后层混合、数据和训练。四者都不能仅由边数推出同一阶，更不能推出“独立”路径。

### NN-HDS-E02

可选固定输出 width 与目标参数/FLOP budget：add 用 projection，gate 为 $H,T$ 分配参数，concat 后立即用 projection 压回固定宽度。分别搜索宽度使参数/FLOPs 接近，并匹配数据、优化和调参预算。无法同时完全匹配的是原生状态宽度、activation lifetime、traffic、额外 gate latency 与表达约束；应给 Pareto 表而不是宣称单一公平点。

### NN-HDS-E03

令 decoder 时刻 $t$ 只能访问 encoder 的 $s\le t$。显式记录 $A_{t,s}$ mask、resize/crop 索引、padding 方向、缓存写入时间与跨 batch 状态。反事实测试：只修改未来输入 $e_{s>t}$，检查当前输出 $y_t$ 是否逐位不变；同时 hook attention/fusion 权重、清空缓存重放，并在 train/eval、增量/整序列两种模式重复。任何非零变化都构成泄漏证据。
