---
type: solution
status: verified
area: [training, optimization, curvature]
topic: "[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]"
exercise: "[[习题 - Hessian、GGN、Fisher 与经验 Fisher 对象总账]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Hessian、GGN、Fisher 与经验 Fisher 对象总账

> [!warning] 使用边界
> 矩阵名称不是定义。每次先写 derivative object、label law、expectation measure 与 reduction，再谈相等、PSD 或近似质量。

## A. 识别与复述

### TRN17-A01
令 $z=f_\theta(x)$、$J=\partial z/\partial\theta$。Hessian 是 $H=\nabla_\theta^2\mathbb E_{q_{data}}\ell$；GGN 是 $G=\mathbb E_{q_{data}}[J^\top H_z\ell J]$；true Fisher 是 $F=\mathbb E_{x\sim q(x),\,y\sim p_\theta(y\mid x)}[s_\theta s_\theta^\top]$，$s_\theta=\nabla_\theta\log p_\theta(y\mid x)$；empirical Fisher 是 $F_{emp}=n^{-1}\sum_i g_i g_i^\top$，$g_i=\nabla_\theta[-\log p_\theta(y_i\mid x_i)]$，其中 $y_i$ 是观测标签。前两者通常以数据目标为对象，后二者的关键差别是标签究竟来自模型还是数据样本。

### TRN17-A02
还必须核对：对什么标量求导、随机标签来自哪条 law、对哪些轴取 expectation/mean、先 mean 还是先 outer product、在哪个参数点、是否保留模型二阶导，以及正则项是否包含。Shape、对称性和 PSD 只描述代数外观，不能恢复生成对象。

### TRN17-A03
模型采样标签是：固定 $x$ 和当前 $\theta$，重新令 $y\sim p_\theta(\cdot\mid x)$，再对 score outer product 取期望。Empirical Fisher 则把训练集中已经观察到的 $y_i$ 当作固定样本；两者只在标签 law 对齐且抽样充分等条件下可能接近。

## B. 手算与构造

### TRN17-B01
score 关于 $\theta$ 为 $x(y-p)=2(y-0.8)$。因此
$$F=x^2p(1-p)=4\times0.8\times0.2=0.64.$$
若 $y=1$，单样本 outer product 是 $[2(0.2)]^2=0.16$；若 $y=0$，则为 $[2(-0.8)]^2=2.56$。同一参数点的 true Fisher 固定为 $0.64$，empirical 值却随观测标签改变。

### TRN17-B02
$J=2\theta$，$H_z\ell=1$，$\partial\ell/\partial z=z-1=\theta^2-1$，$\nabla^2f=2$。所以
$$G=J^2=4\theta^2,\qquad R=2(\theta^2-1),\qquad H=G+R=6\theta^2-2.$$
在 $\theta=0$，$G=0$ 而 $H=-2$：GGN 删除的模型二阶项正好承载负曲率。

### TRN17-B03
该 loss 对 $\theta$ 的二阶导恒为 1，线性均值模型的 GGN 也为 1。模型采样下 $y-\theta\sim\mathcal N(0,1)$，故 true Fisher $F=\mathbb E(y-\theta)^2=1$；但观测 $y=\theta$ 时单样本梯度为零，所以 $F_{emp}=0$。

## C. 推导与证明

### TRN17-C01
先写 $\partial_iL=\sum_k\ell_k\partial_i f_k$。再对 $\theta_j$ 求导：
$$\partial_{ji}L=\sum_{k,l}\ell_{kl}(\partial_jf_l)(\partial_if_k)+\sum_k\ell_k\partial_{ji}f_k.$$
矩阵化即 $J^\top H_z\ell J+\sum_k\ell_k\nabla^2f_k$。GGN 只保留第一项，所以它不是无条件的 Hessian 等价物。

### TRN17-C02
归一化给出 $\int p_\theta(y)dy=1$。在可交换求导与积分且支持不变时，$\mathbb E[s]=\int p\nabla\log p=\int\nabla p=\nabla1=0$。再对该等式求导，得到
$$0=\mathbb E[\nabla^2\log p+s s^\top],$$
故 $F=\mathbb E[ss^\top]=-\mathbb E[\nabla^2\log p]$。若支持随参数变化或正则性失败，边界项不能被静默删除。

### TRN17-C03
Bernoulli 的 $\log p(y\mid a)=ya-\log(1+e^a)$，score 为 $y-p$，故 $F=\operatorname{Var}(y)=p(1-p)$。负对数似然对 $a$ 的二阶导也是 $p(1-p)$。这个等号使用了 canonical natural coordinate 与 matching log-likelihood；换成任意 loss、非自然输出坐标或不同标签测度后不能直接搬用。

## D. 边界、反例与纠错

### TRN17-D01
Gaussian 均值例已经给出反例：在观测最优点 $y=\theta$，$F_{emp}=0$ 是 PSD，但真实 Hessian 与 true Fisher 都为 1。PSD 只保证二次型非负，不保证尺度、rank、eigenvectors 或目标曲率正确。

### TRN17-D02
取 Bernoulli $p=0.8,x=2$。模型标签期望给 $F=0.64$；若数据标签总为 0，empirical outer product 的总体极限为 $2.56$。二者均为非负标量，但 batch 增大只会更准确地估计各自的不同期望，不会把 $q_{data}(y\mid x)$ 变成 $p_\theta(y\mid x)$。

### TRN17-D03
可审计命题是：“对以自然参数表示的正则指数族条件分布，使用匹配负对数似然，并按模型条件分布对标签取期望时，输出空间 loss Hessian 等于输出 Fisher；经相同 Jacobian pullback 后，GGN 与该 Fisher 相等。”Population Hessian 还需模型适定、目标和取期望条件，empirical Fisher 还需额外采样近似。

## E. AI 迁移

### TRN17-E01
最小字段包括 `object_name`、`derivative_scalar`、`parameter_point`、`x_source`、`label_source`、`expectation_axes`、`loss_reduction`、`per_sample_or_batch_mean`、`regularizer_included`、`rank/trace/norm` 与采样 seed。特别要保存 `outer(mean_grad)` 还是 `mean(outer(per_sample_grad))`。

### TRN17-E02
在 $f(\theta)=\theta^2$ 的 squared-loss toy 中断言数值 Hessian 等于 $G+R$、$G\ge0$，且 $\theta=0$ 时 $G=0,H=-2$。在 Bernoulli toy 中对同一 $p$ 切换 $y=0/1$，断言 true Fisher 不变而 empirical outer product 改变；再用模型采样均值收敛到 true Fisher。

### TRN17-E03
追问矩阵定义、标签 law、reduction、相等定理的条件、rank/谱误差、inverse/damping 方法、下游 step 与 wall-clock 证据。若只凭 PSD、同 shape、名称、单一 batch 或训练 loss 改善就称“近似 Hessian”，应降级为经验性 preconditioner/heuristic，而非曲率等价结论。

## 无提示重做

- [ ] 48 小时后从指标链式法则重建 Hessian 分解。
- [ ] 一周后仅用两个一维反例删除“PSD ⇒ 好曲率”与“empirical Fisher ⇒ Fisher”。
