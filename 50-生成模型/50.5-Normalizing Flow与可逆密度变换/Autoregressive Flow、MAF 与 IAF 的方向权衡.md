---
type: model
status: verified
area: [generative-models, normalizing-flows, autoregressive]
node_id: GEN-36
prerequisites: ["[[概率链式分解、顺序选择与自回归生成]]", "[[Coupling Layer、NICE 与 RealNVP]]"]
related: ["[[层次 VAE、表达性先验与近似后验 Flow]]", "[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"]
sources: ["[[S-2017-Papamakarios-MAF]]", "[[S-2016-Kingma-IAF]]", "[[S-2018-Su-5977-fVAEs]]", "[[S-2025-Su-10667-TARFLOW]]"]
exercises: ["[[习题 - Autoregressive Flow、MAF 与 IAF 的方向权衡]]"]
solutions: ["[[解答 - Autoregressive Flow、MAF 与 IAF 的方向权衡]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-flow-maf-iaf-directions-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Autoregressive Flow、MAF 与 IAF 的方向权衡

> [!abstract] 一句话结论
> MAF 与 IAF 使用相同的三角依赖思想，却把“并行可知的条件量”放在相反变量一侧。MAF 给定完整数据时可并行评价密度、生成通常串行；IAF 给定完整 base noise 时可并行变换/采样、反求数据密度通常串行。说它们互为逆是代数事实，不是计算成本结论。

## 一、三角 Jacobian 从哪里来

按顺序 $1,\ldots,d$，若第 $i$ 个输出只依赖当前坐标和更早坐标，则 Jacobian 为三角矩阵，determinant 等于对角元素乘积。自回归网络通过 mask 保证这种依赖，而不是在训练后“碰巧”得到三角结构。

## 二、MAF：数据到噪声的方向便宜

定义编码方向

$$
\boxed{z_i=\frac{x_i-\mu_i(x_{<i})}{\sigma_i(x_{<i})}},
\qquad \sigma_i>0.}
$$

给定完整 $x=(x_1,\ldots,x_d)$，masked network 一次 forward 可同时输出所有 $\mu_i(x_{<i}),\sigma_i(x_{<i})$。Jacobian $\partial z/\partial x$ 的第 $i$ 个对角为 $1/\sigma_i$，所以

$$
\log\left|\det\frac{\partial z}{\partial x}\right|
=-\sum_i\log\sigma_i(x_{<i}).
$$

但从 $z$ 生成时，先求 $x_1$，才可求依赖 $x_1$ 的 $x_2$，依此类推：

$$x_i=\mu_i(x_{<i})+\sigma_i(x_{<i})z_i.$$

因而存在长度约 $d$ 的串行临界路径；缓存可减少重复计算，但不能删除数学依赖。

## 三、IAF：噪声到样本的方向便宜

定义生成/变分变换方向

$$
\boxed{x_i=\mu_i(z_{<i})+\sigma_i(z_{<i})z_i.}
$$

因为完整 $z$ 一开始全部已知，masked network 可并行产生所有参数，随后逐元素得到全体 $x_i$。生成方向 logdet 为

$$
\log\left|\det\frac{\partial x}{\partial z}\right|
=\sum_i\log\sigma_i(z_{<i}).
$$

反求 $z$ 时却要先由 $x_1$ 得 $z_1$，再算 $z_2$，因此 data density evaluation 通常串行。IAF 特别适合 VAE：训练时 base sample $z_0$ 已知，变分密度的 change-of-variables 也沿生成的已知路径记账。

## 四、三维手算：看清依赖而不是只看公式

设 $\sigma_i=1$，

$$
z_1=x_1,\qquad z_2=x_2-x_1,\qquad z_3=x_3-(x_1+x_2).
$$

给定 $x=(1,3,8)$，可同时算得 $z=(1,2,4)$。反向则必须依次：

$$x_1=z_1=1,\quad x_2=z_2+x_1=3,\quad x_3=z_3+x_1+x_2=8.$$

Jacobian 是 unit lower triangular，logdet 为 0。代数计算量都不大，但 parallel depth 完全不同。

## 五、MAF、IAF、coupling 的关系

Coupling 可看作特殊 triangular flow：一组坐标的 conditioner 不依赖被变换组内更早坐标，于是 forward 和 inverse 都可在组内并行，但单层表达更受限。MAF/IAF 使用更细粒度 autoregressive dependency，表达力与串行方向成本随之增加。

| 结构 | 给定 $x$ 算 density | 从 base 采样 | 单层更新 |
|---|---|---|---|
| coupling | 并行 | 并行 | 一部分不变 |
| MAF | 并行 | 串行 | 全部坐标可变 |
| IAF | 串行 | 并行 | 全部坐标可变 |

“并行”是 dependency-level 陈述；真实 wall time 还取决于模型大小、硬件、kernel、batch 和缓存。

## 六、posterior flow 不等于 exact data likelihood

在 VAE 中令 $u\sim q_0(u\mid x)$，$z=F_x(u)$。只要 $F_x$ 对 $u$ 可逆，就能计算 $q(z\mid x)$，其 logdet 进入 ELBO。但 decoder $p_\theta(x\mid z)$ 仍可能不可逆，边缘

$$p_\theta(x)=\int p(z)p_\theta(x\mid z)dz$$

仍不可精确计算。[[S-2018-Su-5977-fVAEs]]提供很好的接口直觉，但不能把“后验 flow”误写成“数据 flow”。

## 七、TARFlow 为什么“一步”仍可能慢

[[S-2025-Zhai-TARFlow]]把图像 patch 排序后使用 Transformer autoregressive flow。core transform 仍服从三角方向账：某一方向一次 Transformer call 可并行，inverse/sample 方向存在 serial autoregressive calls。论文中的强结果还组合 Gaussian augmentation、post-denoise 和 guidance；这些在 GEN-40 分账。

因此“一步生成模型”若只表示没有扩散时间网格，并不等于一次并行网络调用或最低 latency。必须报告 transformer calls、序列长度、batch、hardware 和 wall time。

## 八、图：同一个三角双射的两种计算图

先看图回答：为什么 MAF 的已知前缀是 $x_{<i}$，IAF 的已知前缀是 $z_{<i}$，从而交换了并行任务？

![[00-知识库管理/_assets/figures/generative-models/fig-flow-maf-iaf-directions-v1.svg|900]]

> [!figure] 图 50.5-04　MAF 与 IAF 的已知变量、三角 Jacobian和串行临界路径
> 蓝色横向表示一次 masked forward 可并行得到的量，琥珀色阶梯表示必须逐坐标解出的方向。来源：据 MAF/IAF 原论文方向合同独立重绘。

**怎样读图**：不要先背“MAF 快/IAF 快”，先写调用任务和一开始已知的完整向量。能把所有 conditioner 输入一次性提供给 masked network 的方向才可并行。

**图没有证明什么**：图不预测具体 GPU latency，不证明任一方向统计表达力更强，也不意味着串行方向无法通过缓存、block ordering 或工程优化加速。

## 九、本节回顾与训练

- triangular dependency 使 logdet 变成对角求和；
- MAF：$x\to z$ density 并行，$z\to x$ sampling 串行；
- IAF：$z\to x$ transform 并行，$x\to z$ density 串行；
- posterior flow 增强 $q(z\mid x)$，不自动精确化 $p(x)$；
- “一步”不能替代 network-call 与 wall-time 账。

- [[习题 - Autoregressive Flow、MAF 与 IAF 的方向权衡]]
- [[解答 - Autoregressive Flow、MAF 与 IAF 的方向权衡]]

