---
type: solution
status: draft
area: [neural-networks/activations, maxout]
topic: "[[Maxout、分段线性区域与条件计算]]"
exercise: "[[习题 - Maxout、分段线性区域与条件计算]]"
sources: ["[[S-2013-Goodfellow-Maxout-Networks]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Maxout、分段线性区域与条件计算

## A

### NN-MAX-A01
rank-$k$ unit 为 $h_j(x)=\max_{1\le r\le k}(w_{jr}^Tx+b_{jr})$。对 batch $X:[B,d]$、$m$ 个输出，可取 $W:[m,k,d]$、$b:[m,k]$；candidate tensor 为 $C:[B,m,k]$，沿末轴 reduce-max 后输出 $H:[B,m]$，argmax 通常为 $I:[B,m]$。

### NN-MAX-A02
唯一 winner $r^*$ 时 classical gradient 是 $w_{r^*}$。tie 的数学对象是集合 $\partial h(x)=\operatorname{conv}\{w_r:r\in A(x)\}$，而不是唯一向量；框架为可执行 VJP 选择 first/last winner、equal split 或其他规定。数学 subdifferential 描述所有合法局部支撑斜率，framework convention 只选其中一种反传语义。

### NN-MAX-A03
gradient routing 指 backward 只把 cotangent 发给获胜 candidates；但 winner 必须在看过候选值后才知道，普通 dense forward 仍计算全部 $k$ 个 affine maps。forward conditional compute 要先以更便宜的 router 决定只执行哪些分支，并需要稀疏 kernel/专家调度；二者不是同一节省。

## B

### NN-MAX-B01
$$h(x)=\max(x,-x,1)=\begin{cases}-x,&x\le-1,\\1,&-1\le x\le1,\\x,&x\ge1.\end{cases}$$
$x<-1$ 的 winner 是 $-x$，$-1<x<1$ 是常数 1，$x>1$ 是 $x$；$x=-1$ 时 $-x$ 与 1 tie，$x=1$ 时 $x$ 与 1 tie。端点处函数连续但导数分别从 $-1$ 跳到 0、从 0 跳到 1。

### NN-MAX-B02
例如 $a_1(x)=x_1$、$a_2(x)=x_2$ 在 $x=0$ tie。取方向 $v=(1,-2)$，则
$$h'(0;v)=\max(\nabla a_1^Tv,\nabla a_2^Tv)=\max(1,-2)=1.$$
反方向给 $h'(0;-v)=\max(-1,2)=2\ne-1$，所以方向导数不是关于 $v$ 的线性映射，tie 点没有 Fréchet derivative。

### NN-MAX-B03
普通 $d\to m$ dense layer 约有 $md$ 权重、每样本 $md$ MAC，并输出/保存 $Bm$ 值。$k=4$ maxout 约有 $4md$ 权重、$4Bmd$ MAC，reduce 前逻辑 candidate storage 为 $4Bm$ 值，另有 $Bm$ argmax/output；融合 reduction 可减少物化 storage，却不消除四组 affine 计算。

## C

### NN-MAX-C01
对 $h(x)=\max_r a_r(x)$ 和 $t\in[0,1]$，每个 affine $a_r$ 满足
$$a_r(tx+(1-t)y)=ta_r(x)+(1-t)a_r(y)\le th(x)+(1-t)h(y).$$
对 $r$ 取最大仍保持右侧上界，因此 $h(tx+(1-t)y)\le th(x)+(1-t)h(y)$，即 $h$ convex。

### NN-MAX-C02
candidate $r$ 获胜当且仅当对所有 $s$ 有 $(w_r-w_s)^Tx\ge b_s-b_r$；这是有限个闭半空间的交，故为 convex polyhedron（也可能为空或低维）。若某条 affine function 在所有 $x$ 上都被其他 candidates 的 upper envelope 严格压住，其 region 为空，训练数据上也永不获胜。

### NN-MAX-C03
取固定 candidates $a_1(x)=0,a_2(x)=x$ 即得 $\max(0,x)=\operatorname{ReLU}(x)$。但 unit convex 不保证全网 convex：$u(x)=\max(x,-x)=|x|$ convex，接一个输出权重 $-1$ 得 $-u(x)=-|x|$，它是 concave 而非 convex。负线性组合或一般复合都会破坏 unit-level 结论。

## D

### NN-MAX-D01
令 candidates 为 $a_1(x)=0$、$a_2(x)=x$、$a_3(x)=x-1$。对所有 $x$，$a_3<a_2$，所以第三条永远不在 upper envelope；$k=3$ 只产生两个可见 pieces。高维中 region 为空、仅在 measure-zero 集合获胜或被数据支持集避开都很常见。

### NN-MAX-D02
argmax 依赖所有候选值；在没有额外结构时，少算一条就可能漏掉真正最大值。backward 的稀疏梯度发生在 dense candidate GEMM 和 max reduction 之后，最多减少某些梯度写入，不会把 forward MAC 自动除以 $k$。真正跳算必须改变路由架构与 kernel。

### NN-MAX-D03
在 tie 附近，$x\pm\varepsilon v$ 可能落入不同 winner regions，中心差分混合两侧斜率，结果依方向、步长与舍入而变。测试应把 unique-winner 点的步长限制在 margin 不变的邻域并与对应 $w_{r^*}$ 比较；tie 点不做 classical gradient check，而是验证 documented tie VJP、方向导数或 subgradient inclusion。

## E

### NN-MAX-E01
覆盖唯一 winner、首尾 tie、三重 tie、candidate permutation、负零、NaN/Inf 和非连续 layout。明确 NaN propagation 与 tie-breaking 规则，检查 forward、argmax、input/weight/bias gradients、重复运行 determinism；若 permutation 改变 tie convention，函数值仍应 invariant，并把梯度差限制为已声明边界。

### NN-MAX-E02
逐 unit/candidate 统计 winner frequency $p_{jr}$、第一第二大值 margin、连续未获胜步数和参数梯度范数；按层画熵 $-\sum_rp_{jr}\log p_{jr}$ 与 dead rate。用数据分片与多 seed 给区间，并区分“全数据永不获胜”与“某 batch 暂未获胜”。若干预，可比较 bias reset、噪声或负载均衡项，但不把监测指标直接当质量提升。

### NN-MAX-E03
Maxout 通常 dense 计算全部 candidates，选一个值并只向 winner 路由梯度；MoE top-$k$ 先由 router 选少数专家，再只执行所选大模块，节省依赖稀疏 dispatch、capacity 与负载均衡；ReLU sparsity 是 dense affine 后把负输出置零，普通硬件仍已完成 GEMM。三者都有“零/选择”，但计算发生的时间点与可跳过的工作不同。

