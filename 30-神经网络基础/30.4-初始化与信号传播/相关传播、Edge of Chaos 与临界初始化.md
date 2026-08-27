---
type: derivation
status: draft
area: [neural-networks/initialization, correlation-propagation, edge-of-chaos]
aliases: [Correlation Propagation, Edge of Chaos, Critical Initialization]
node_id: NN-29
prerequisites: ["[[方差传播与宽层均值场近似]]", "[[协方差、相关性与条件期望]]", "[[相图、平衡点与局部稳定性|不动点、吸引域与局部稳定性]]"]
related: ["[[正交初始化与 Dynamical Isometry]]", "[[反向梯度方差与 Fan-In_Fan-Out 权衡|反向梯度方差与 Fan-In/Fan-Out 权衡]]", "[[深度、有效路径与稳定性证据地图]]"]
sources: ["[[S-2016-Poole-Transient-Chaos]]", "[[S-2017-Schoenholz-Deep-Information-Propagation]]", "[[S-2017-Pennington-Dynamical-Isometry]]"]
exercises: ["[[习题 - 相关传播、Edge of Chaos 与临界初始化]]"]
solutions: ["[[解答 - 相关传播、Edge of Chaos 与临界初始化]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-correlation-edge-of-chaos-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---
# 相关传播、Edge of Chaos 与临界初始化

> [!abstract] 本章主问题
> 两个不同输入经过很多随机层以后，是仍能彼此区分，还是表示逐渐变成几乎同一个方向？单输入 variance 稳定只守住每个点的长度尺度；两输入 correlation map 才描述相对几何。Edge of Chaos 是该动力系统在 $c=1$ 附近的局部临界条件，不是“模型位于混沌边缘就必然最好”的经验口号。

## 一、为什么只看一个输入不够

NN-25 研究一个输入 $x$ 的 preactivation second moment

$$
q_\ell(x)=\mathbb E[(z_i^{(\ell)}(x))^2].
$$

即使对所有层都有 $q_\ell(x)=1$，仍可能出现两种完全不同的表示几何：

- 所有输入最后都指向几乎同一方向，网络失去区分能力；
- 相近输入的微小差异被快速放大，有限宽噪声和梯度方向变得敏感。

因此必须同时追踪两个输入 $x,x'$ 的 covariance 与 normalized correlation。

## 二、两输入的随机对象合同

对第 $\ell$ 层同一 neuron，定义

$$
q_{11}^{(\ell)}=\mathbb E[z_i^{(\ell)}(x)^2],\qquad
q_{22}^{(\ell)}=\mathbb E[z_i^{(\ell)}(x')^2],
$$

$$
q_{12}^{(\ell)}
=\mathbb E[z_i^{(\ell)}(x)z_i^{(\ell)}(x')],
\qquad
c_\ell=\frac{q_{12}^{(\ell)}}{\sqrt{q_{11}^{(\ell)}q_{22}^{(\ell)}}}.
$$

$c_\ell\in[-1,1]$ 只要 covariance matrix 半正定。它是初始化 ensemble 下同一随机网络对两个输入的相关性，不是数据集中两个坐标的 Pearson correlation，也不是训练后某一 mini-batch 的精确样本相关系数。

## 三、宽层下的 Bivariate Gaussian 表示

若两个输入的 marginal second moment 已到同一固定点 $q_*$，宽层近似把一对 preactivation 写成

$$
U=\sqrt{q_*}Z_1,
$$

$$
V=\sqrt{q_*}
\left(cZ_1+\sqrt{1-c^2}Z_2\right),
\qquad Z_1,Z_2\overset{\text{iid}}\sim\mathcal N(0,1).
$$

直接验算可得

$$
\mathbb E[U^2]=\mathbb E[V^2]=q_*,
\qquad
\mathbb E[UV]=q_*c.
$$

这一重参数化把二维 Gaussian integral 变成对两个独立标准正态的期望，便于数值积分与 Monte Carlo 检验。

## 四、Covariance Map 的逐层递推

对共享权重的两条前向路径，零均值独立初始化给出

$$
q_{12}^{(\ell+1)}
=\sigma_w^2\,
\mathbb E[\phi(U)\phi(V)]
+\sigma_b^2.
$$

在 equal-variance 固定点 $q_*$ 上，相关性 map 为

$$
\boxed{
\mathcal C(c)
=\frac{\sigma_w^2\,
\mathbb E[\phi(U)\phi(V)]+\sigma_b^2}{q_*}
},
\qquad c_{\ell+1}=\mathcal C(c_\ell).
$$

为什么 bias covariance 是 $+\sigma_b^2$？因为同一网络对两个输入使用同一个 bias；若错误地为两条路径抽独立 bias，这一项会消失，研究对象也变了。

## 五、$c=1$ 固定点与局部增益

当两个输入完全相同，$U=V$，且 $q_*$ 满足单输入固定点方程

$$
q_*=\sigma_w^2\mathbb E[\phi(\sqrt{q_*}Z)^2]+\sigma_b^2,
$$

于是 $\mathcal C(1)=1$。在可微与可交换微分/积分的条件下，Gaussian integration by parts（也可由 Price identity 表述）给出

$$
\boxed{
\chi_1=\mathcal C'(1)
=\sigma_w^2\mathbb E\!\left[
\phi'(\sqrt{q_*}Z)^2
\right].
}
$$

注意它与反向梯度递推中的 derivative moment 形式相同，但问题不同：这里研究两个输入距离在深度方向如何变化；反向递推研究 cotangent 的平均平方长度。

## 六、Ordered、Critical 与 Chaotic 三个局部制度

令 $\varepsilon_\ell=1-c_\ell$ 很小。对 $c=1$ 线性化：

$$
\varepsilon_{\ell+1}
\approx\chi_1\varepsilon_\ell.
$$

于是：

| 制度 | 条件 | $c=1$ 附近的含义 |
|---|---:|---|
| ordered | $\chi_1<1$ | 差异指数收缩，输入趋向不可区分 |
| critical / edge | $\chi_1=1$ | 一阶既不收缩也不放大，需看高阶项 |
| chaotic | $\chi_1>1$ | $c=1$ 不稳定，微小差异先被放大 |

“chaotic”在这里是随机函数深度动力学的术语，不表示训练 loss 必然发散，也不表示确定性网络在时间上具有经典混沌的全部性质。

## 七、Correlation Depth Scale

在 ordered 区且 $0<\chi_1<1$ 时，局部差异近似

$$
\varepsilon_L\approx \chi_1^L\varepsilon_0
=\exp\!\left(-\frac{L}{\xi_c}\right)\varepsilon_0,
$$

其中

$$
\boxed{\xi_c=-\frac{1}{\log\chi_1}}.
$$

当 $\chi_1\uparrow1$ 时，$\xi_c$ 变大，相关性信息能传播更深。但临界处线性项不足以决定速率；可能出现 polynomial 而非 exponential 的接近，不能把“$\xi_c=\infty$”误读成任意深度都无损。

## 八、ReLU 的可手算临界例子

若 $U,V$ 是 variance 为 $q$、correlation 为 $c$ 的 centered Gaussian，则

$$
\mathbb E[\operatorname{ReLU}(U)\operatorname{ReLU}(V)]
=\frac{q}{2\pi}
\left[
\sqrt{1-c^2}+(\pi-\arccos c)c
\right].
$$

取 $\sigma_b^2=0,\sigma_w^2=2$，单输入 second moment 临界，相关性 map 变成

$$
\boxed{
\mathcal C_{\mathrm{ReLU}}(c)
=\frac1\pi
\left[
\sqrt{1-c^2}+(\pi-\arccos c)c
\right].
}
$$

其导数为

$$
\mathcal C_{\mathrm{ReLU}}'(c)
=1-\frac{\arccos c}{\pi},
$$

所以 $\mathcal C'(1)=1$。这说明 He scale 的 zero-bias ReLU 位于这一 mean-field 意义下的临界边界；它不说明有限 ReLU 网络拥有 dynamical isometry，因为 ReLU derivative matrix 会产生大量零方向。

## 九、Edge of Chaos 不是单一最优超参数

至少要拒绝四个过度结论：

1. **局部不等于全局**：$\mathcal C'(1)=1$ 只控制 $c\approx1$；远离 1 的 map 仍需完整分析。
2. **初始化不等于训练全过程**：权重—activation 相关性随训练产生，原 mean-field map 会漂移。
3. **相关稳定不等于谱稳定**：平均 pairwise geometry 不能控制 Jacobian 的最小/最大 singular value。
4. **临界不等于任务最优**：数据、width、normalization、residual、optimizer 与训练预算都会改变选择。

## 十、结构化网络中的改写义务

- Convolution 共享 kernel，使不同位置的 covariance 形成空间 kernel，而非单个标量。
- Residual addition 引入 skip 与 branch 的 covariance，临界尺度依赖 depth scaling。
- Normalization 用样本或 feature 统计量耦合坐标，改变 map。
- Attention 同时传播 token—token covariance 与 softmax 非线性，不能沿用 MLP 二元积分。

因此 Edge-of-Chaos 公式必须和架构一起声明，不能作为无模型下标的“普适初始化定律”。

## 十一、图：从两输入 Gaussian 到相图

先看图回答：$\chi_1$ 控制的是 correlation map 的哪个局部对象？为什么 $\chi_1=1$ 仍不足以推出全 Jacobian 稳定？

![[00-知识库管理/_assets/figures/neural-networks/fig-correlation-edge-of-chaos-v2.svg|900]]

> [!figure] 图 30.4-05　相关传播、临界斜率与深度尺度
> 左栏建立共享随机网络下的二输入 covariance；中栏比较 ordered/critical/chaotic map 与对角线；右栏把局部斜率变成 depth scale，并列出从 correlation 到 Jacobian spectrum 的证据缺口。来源：依据 Poole et al. 2016、Schoenholz et al. 2017 与 Pennington et al. 2017 独立绘制；由 [[00-知识库管理/_labs/code/plot_initialization_advanced_v2.py]] 确定性生成。

**怎样读图**：先确认两条输入路径共享同一权重与 bias，再在 $c=1$ 处比较 map 斜率，最后沿右栏检查当前证据只支持局部 pairwise geometry，还是已经测到方向谱。

**图没有证明什么**：图没有证明临界初始化对任意任务最优，没有证明有限宽网络等于 Gaussian process，也没有把 correlation depth 外推为训练收敛率或泛化界。

## 十二、可复现实验协议

1. 选定 activation、$\sigma_w,\sigma_b$ 与输入 correlation grid。
2. 用二维 Gaussian Monte Carlo 估计 $\mathcal C(c)$，同时计算解析/数值积分参照。
3. 在多个 width、depth、seed 的有限网络中记录 empirical correlation trajectory。
4. 在 $c\approx1$ 用有限差分估计 $\chi_1$，改变步长检查数值稳健性。
5. 同时记录 JVP/VJP norm 与极端 singular estimate，展示 correlation 稳定可能与谱病态并存。

报告应区分 integration error、finite-width error、seed variation 与训练后 drift。

> [!summary]
> 单输入 moment map 管长度，两输入 correlation map 管相对几何；$\chi_1=\mathcal C'(1)$ 决定 $c=1$ 附近的 ordered/critical/chaotic 制度。Edge of Chaos 是带假设的局部初始化理论，不是跨架构、跨任务的最优性宣言。

- [[习题 - 相关传播、Edge of Chaos 与临界初始化]]
- [[解答 - 相关传播、Edge of Chaos 与临界初始化]]
