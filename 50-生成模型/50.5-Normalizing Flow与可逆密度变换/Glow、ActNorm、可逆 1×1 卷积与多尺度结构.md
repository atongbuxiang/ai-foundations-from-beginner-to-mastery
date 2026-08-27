---
type: model
status: verified
area: [generative-models, normalizing-flows, glow]
node_id: GEN-35
prerequisites: ["[[Coupling Layer、NICE 与 RealNVP]]", "[[线性方程组、消元与 LU 分解]]", "[[离散卷积、互相关与边界约定]]"]
related: ["[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]", "[[条件数]]"]
sources: ["[[S-2018-Su-5807-RealNVP与Glow]]", "[[S-2018-Kingma-Dhariwal-Glow]]", "[[S-2016-Dinh-RealNVP]]"]
exercises: ["[[习题 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"]
solutions: ["[[解答 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-flow-glow-multiscale-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Glow、ActNorm、可逆 1×1 卷积与多尺度结构

> [!abstract] 一句话结论
> Glow 的一个 flow step 由 ActNorm、可逆 $1\times1$ 通道混合和 affine coupling 组成。三者分别管尺度初始化、坐标混合和非线性变换；squeeze 与 split 重新组织计算和 latent factorization，但只要所有 split latent 都保留，就没有维度丢失。

## 一、为什么 RealNVP 之后还需要 Glow

固定 permutation 可以让不同维度轮流进入 coupling，但它不从数据学习“怎样混通道”。Glow 用可逆矩阵 $W\in\mathbb R^{C\times C}$ 替代固定 permutation，并用 ActNorm 避免小 batch 下 batch statistics 不稳定。关键不是模块名字，而是每一层都有可审计的 inverse 与 logdet。

## 二、ActNorm：一次数据初始化，不是 BatchNorm

对每个 channel，

$$y_{bchw}=s_c x_{bchw}+b_c,\qquad s_c\ne0.$$

若输入空间大小为 $H\times W$，单样本 logdet 为

$$\log|\det J|=HW\sum_{c=1}^C\log|s_c|.$$

第一次 batch 常用经验均值和标准差初始化 $b,s$，使输出近似零均值、单位方差；此后 $s,b$ 是普通可训练参数。推理时 forward 不依赖当前 batch，这是它与 BatchNorm 的本质区别。

> [!warning] 初始化不是定理
> 第一批是否代表总体、极小方差 channel 如何加 floor、分布偏移后尺度是否恶化，都要记录。data-dependent initialization 只选择起点，不提供长期归一化保证。

## 三、可逆 $1\times1$ convolution

在每个空间位置 $(h,w)$，把 channel vector $x_{hw}\in\mathbb R^C$ 映射为

$$y_{hw}=Wx_{hw},\qquad \det W\ne0.$$

同一个 $W$ 重复作用在 $HW$ 个位置，所以整体 Jacobian 是 $HW$ 个 $W$ 的块对角复本：

$$
\boxed{\log|\det J|=HW\log|\det W|.}
$$

逆是 $x_{hw}=W^{-1}y_{hw}$。不要显式求 inverse 再乘；数值实现应使用 triangular solve 或 factorization。

### 3.1 LU 参数化与条件性

若 $W=P L(U_{off}+\operatorname{diag}(s))$，则

$$\log|\det W|=\sum_c\log|s_c|$$

（permutation 和 unit-diagonal $L$ 的 determinant 绝对值为 1）。它把每步 determinant 从一般 $O(C^3)$ 降到 $O(C)$ 读取对角，但 forward mixing 仍需矩阵乘法。约束 $s_c\ne0$ 保证代数可逆，却不保证 $\sigma_{\min}(W)$ 远离 0；条件数仍应监测。

## 四、squeeze：改形状，不改总维数

典型 $2\times2$ squeeze 将

$$
B\times C\times H\times W
\longrightarrow
B\times4C\times(H/2)\times(W/2).
$$

每样本元素数仍是 $CHW$。它只是 permutation/reshape，$|\det|=1$，让局部空间邻域进入 channel mixing。若 $H,W$ 不是偶数，padding/cropping 必须另立合同。

## 五、split/factor-out：减少后续计算，不是扔掉信息

在某一级把 hidden $h$ 分成 $(z^{(1)},h')$，将 $z^{(1)}$ 作为本级 latent 不再经过后续昂贵层，$h'$ 继续流动。最终 latent 是

$$z=(z^{(1)},z^{(2)},\ldots,z^{(L)}),$$

总维数仍等于输入。density 通常分解为多个条件/先验项。若生成时遗漏任一 latent chunk 或把它固定为常数，才真正改变模型分布。

## 六、一个形状与 logdet 手算

输入 $C=2,H=W=2$，取

$$W=\begin{pmatrix}2&0\\0&1/2\end{pmatrix}.$$

$\det W=1$，所以四个位置的总 logdet 是 $4\log1=0$。若改成 $W=2I_2$，则 $\det W=4$，总 logdet 为 $4\log4=8\log2$。不能漏掉空间位置乘数 $HW$。

## 七、完整 step 的记账顺序

编码方向常依次执行：

1. ActNorm：更新状态，累加 $HW\sum_c\log|s_c|$；
2. invertible conv：累加 $HW\log|\det W|$；
3. affine coupling：累加 scale map 对所有被变换元素之和。

inverse 必须以相反顺序执行。这是函数复合的基本规律；“每层都可逆”不允许打乱逆序。

## 八、科学空间研读框

[[S-2018-Su-5807-RealNVP与Glow]]适合建立 NICE→RealNVP→Glow 的模块演化图景；[[S-2018-Kingma-Dhariwal-Glow]]承担正式架构和论文实验。课程额外要求 LU/solve、最小奇异值、首批初始化与 multiscale latent 完整性审计。

## 九、图：形状、混合与 latent factorization

先看图回答：squeeze 和 split 都改变张量外观，为什么前者是零 logdet 重排，后者却改变后续概率分解而仍不丢维？

![[00-知识库管理/_assets/figures/generative-models/fig-flow-glow-multiscale-ledger-v1.svg|900]]

> [!figure] 图 50.5-03　Glow step 与 multiscale 的形状—logdet—latent 三本账
> 上方是一层 ActNorm→可逆通道混合→coupling；下方区分 squeeze reshape 与 factor-out。来源：据 Glow/RealNVP 架构独立重绘。

**怎样读图**：每经过一个模块，分别读状态形状、局部 logdet 和 inverse。split 出去的 $z^{(1)}$ 仍在最终 latent 清单里，只是不再参加更深层计算。

**图没有证明什么**：图不证明 learned $W$ 条件良好，不证明首批 ActNorm 代表总体，也不证明多尺度 factorization 总能得到语义分层。

## 十、常见误用与本节回顾

- ActNorm 的推理结果不依赖当前 batch；
- 可逆 $1\times1$ conv 的 determinant 要乘 $HW$；
- LU 让 determinant 便宜，不自动消除病态；
- squeeze 保持元素总数；split 保留所有 latent chunks；
- inverse 要按模块相反顺序执行。

- [[习题 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]
- [[解答 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]
