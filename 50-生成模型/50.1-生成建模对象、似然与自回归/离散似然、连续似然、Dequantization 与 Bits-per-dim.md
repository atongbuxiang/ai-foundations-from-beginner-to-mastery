---
type: derivation
status: verified
area: [generative-models, likelihood, image-generation]
aliases: [图像似然与去量化, BPD与Dequantization]
node_id: GEN-06
prerequisites: ["[[最大似然、交叉熵与前向 KL]]", "[[随机变量变换与密度换元]]", "[[基本不等式与界的构造]]"]
related: ["[[生成建模对象、似然与自回归 MOC]]", "[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"]
sources: ["[[S-2024-Su-10197-多模态自回归]]", "[[S-2016-Oord-PixelRNN]]", "[[S-2019-Ho-FlowPlusPlus-Dequantization]]"]
exercises: ["[[习题 - 离散似然、连续似然、Dequantization 与 Bits-per-dim]]"]
solutions: ["[[解答 - 离散似然、连续似然、Dequantization 与 Bits-per-dim]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-gen-dequant-bpd-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 离散似然、连续似然、Dequantization 与 Bits-per-dim

> [!abstract] 本节主问题
> 数字图像存储为离散像素质量，许多 Flow/continuous density model 却在连续空间上给密度。Dequantization 把每个离散 bin 展开为连续区域，并用连续 density 对该区域积分得到离散 mass；uniform/variational 训练通常优化这个离散 log mass 的下界。Bits-per-dim 只有在 log base、维度、bin 宽和缩放相同后才可比较。

## 一、密度可以无限高，质量仍不超过一

连续变量在点 $x$ 的 density $p(x)$ 可以大于 1；真正概率是区域积分。若把离散数据点直接交给任意灵活连续 density，模型可在每个点附近造越来越窄的尖峰，使 training density 任意大，而没有合理离散 mass 解释。这是 dequantization 的第一动机。

## 二、离散 mass 与连续 bin

设 $X\in\{0,1,\ldots,K-1\}^D$。对每个离散向量 $x$ 定义 unit bin

$$
B_x=x+[0,1)^D.
$$

若连续模型密度为 $p_\theta(y)$，它诱导的离散质量是

$$
P_\theta(X=x)=\int_{B_x}p_\theta(y)\,dy.
$$

只要所有 bins 无重叠地覆盖考虑的连续域，这些质量归一化。采样时先 $Y\sim p_\theta$，再用 floor/clip 映射回离散 $X$；域外质量如何处理必须写清。

## 三、Uniform dequantization 下界

令 $U\sim\operatorname{Unif}([0,1)^D)$，$Y=x+U$。因为 unit cube volume 为 1，Jensen 给出

$$
\begin{aligned}
\log P_\theta(x)
&=\log\int_{[0,1)^D}p_\theta(x+u)du\\
&=\log\mathbb E_U[p_\theta(x+U)]\\
&\ge \mathbb E_U[\log p_\theta(x+U)].
\end{aligned}
$$

所以对加均匀噪声后的连续 log density 做 MLE，优化的是离散 log mass 的 lower bound。只有当 $p_\theta(x+u)$ 在该 bin 内常数时 Jensen gap 为零。

## 四、Variational dequantization

取支持位于 $[0,1)^D$ 的可学习 $q_\phi(u\mid x)$，插入重要性比：

$$
\begin{aligned}
P_\theta(x)
&=\int q_\phi(u\mid x)
\frac{p_\theta(x+u)}{q_\phi(u\mid x)}du,\\
\log P_\theta(x)
&\ge\mathbb E_{q_\phi(u\mid x)}
\left[\log p_\theta(x+u)-\log q_\phi(u\mid x)\right].
\end{aligned}
$$

更精确地，gap 为

$$
D_{\mathrm{KL}}\bigl(q_\phi(u\mid x)\Vert p_\theta(u\mid x)\bigr),
$$

其中 $p_\theta(u\mid x)=p_\theta(x+u)/P_\theta(x)$ 是模型在 bin 内的后验。[[S-2019-Ho-FlowPlusPlus-Dequantization]]用 expressive flow 学 $q_\phi$ 以收紧下界。

## 五、缩放到 $[0,1]$ 的常数

若先令

$$
Z=\frac{X+U}{K},
$$

每个 bin 宽为 $1/K$。由变量替换 $Y=KZ$，

$$
\log p_Y(y)=\log p_Z(z)-D\log K.
$$

因此直接报告 $p_Z$ 的 continuous log density 时，若要与 unit-bin 离散口径对应，需要正确加减 $D\log K$。漏掉这个常数会让两个完全相同的模型仅因数据尺度不同而差 $\log_2 K$ bits/dim。

## 六、Bits per dimension

对 $D$ 个标量维度，离散模型常报告

$$
\operatorname{BPD}(x)
=-\frac{1}{D}\log_2 P_\theta(x)
=-\frac{1}{D\log 2}\log P_\theta(x).
$$

数据集报告再对样本平均。若用 dequantization lower bound $\mathcal L_{\mathrm{deq}}(x)\le\log P_\theta(x)$，则

$$
-\frac{\mathcal L_{\mathrm{deq}}(x)}{D\log2}
\ge \operatorname{BPD}(x),
$$

是离散 BPD 的上界；越低越好。

### 手算

一张 $2\times2$ 单通道图有 $D=4$。若模型给该离散图质量 $P(x)=2^{-12}$，则

$$
\operatorname{BPD}=\frac{12}{4}=3.
$$

若是 RGB，维度应计 $2\times2\times3=12$，除非论文明确按 pixel 而非 channel-dimension 归约。

## 七、离散 PixelCNN 不需要 dequantization 才能定义 likelihood

[[S-2016-Oord-PixelRNN]]直接对 256 个像素值建 categorical/discretized conditional mass，因而 exact discrete NLL 已有意义。Dequantization 是把离散数据交给连续 density 时的接口，不是所有图像生成模型的必需步骤。比较离散与连续模型时必须对齐 bins 和缩放。

## 八、常见口径错误

| 错误 | 后果 |
|---|---|
| 把 $p(x)$ 写成点概率 | 混淆单位与坐标尺度 |
| 对离散点直接拟合无限尖连续密度 | likelihood 可无意义上升 |
| 忘记 $-log q_\phi$ | variational objective 不再是所声明下界 |
| 噪声越出 bin | 不能无修改地解码回原离散值 |
| 忘记 $D\log K$ | BPD 跨预处理不可比 |
| 对 train-time noise 和 test-time integration 用不同协议 | estimand 改变 |
| 用低 BPD 推出高感知质量 | 评价对象错配 |

## 九、科学空间研读框与来源边界

[[S-2024-Su-10197-多模态自回归]]质疑“连续图像 patch 直接用 MSE”隐含的条件分布假设，为本节提供了一个更上游的问题：视觉对象究竟以离散 token、连续 feature 还是加噪变量进入生成模型？但文章没有承担 dequantization lower bound 或 BPD 常数的推导。课程因此只调用其对象选择问题，离散 Pixel likelihood 回查 [[S-2016-Oord-PixelRNN]]，variational bound 回查 [[S-2019-Ho-FlowPlusPlus-Dequantization]]。这也是“不为了多引用科学空间而把相邻直觉冒充正式来源”的实例。

## 十、图：一个离散点其实对应一整个 bin

先看图回答：连续 density 的哪一块面积才是离散质量；uniform 与 variational dequantization 分别怎样在 bin 内选点？

![[00-知识库管理/_assets/figures/generative-models/fig-gen-dequant-bpd-v1.svg|900]]

> [!figure] 图 50.1-06　离散 bin、连续密度、dequantization 下界与 BPD
> 左栏把整数值展开为 bins，中栏展示 bin 内积分与随机 dequantization，右栏登记 log base、维度和缩放常数。来源：依据 PixelRNN 的离散口径与 Flow++ 变分 dequantization 独立重绘。

**怎样读图**：先看阴影面积而非曲线某一点高度；再比较 uniform $q$ 与贴近 bin 后验的 variational $q$，最后沿右栏检查 BPD 的每个常数。

**图没有证明什么**：图不证明 variational $q$ 在有限训练中一定更好，也不说明较低 BPD 会带来较优语义或感知样本。

## 十一、前沿地位与研究边界

Dequantization 仍是 continuous model 处理离散数据的基础接口，也有 subset flows、importance-weighted/Rényi dequantization 和 categorical embeddings 等扩展。核心开放点不是“是否加随机噪声”一句话，而是 discrete mass、continuous support、bound tightness、sample decoding 与公平 evaluation 能否共同闭合。

## 十二、本节回顾

- 离散质量是连续 density 在 bin 上的积分；
- uniform dequantization 给 Jensen lower bound；variational dequantization 加 $-\log q$ 并可收紧；
- BPD 是按维度归一的负 log mass（base 2），bound 会给上界；
- bin width、数据缩放、通道数和 log base 必须对齐；
- likelihood 与感知质量仍是不同评价账。

## 十三、练习与独立详解

- [[习题 - 离散似然、连续似然、Dequantization 与 Bits-per-dim]]
- [[解答 - 离散似然、连续似然、Dequantization 与 Bits-per-dim]]
