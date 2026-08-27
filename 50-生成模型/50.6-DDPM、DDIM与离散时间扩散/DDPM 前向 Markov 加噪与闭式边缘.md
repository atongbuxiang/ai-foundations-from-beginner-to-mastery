---
type: derivation
status: verified
area: [generative-models, diffusion, probability]
node_id: GEN-41
prerequisites: ["[[多元高斯分布]]", "[[条件概率、全概率与 Bayes 公式]]", "[[联合分布、边缘分布与独立性]]"]
related: ["[[DDPM 反向后验、ELBO 与逐步 KL]]", "[[扩散简化损失、时间加权、Schedule 与 SNR]]"]
sources: ["[[S-2022-Su-9119-DDPM拆楼建楼]]", "[[S-2022-Su-9164-DDPM贝叶斯去噪]]", "[[S-2020-Ho-DDPM]]", "[[S-2015-SohlDickstein-Diffusion]]"]
exercises: ["[[习题 - DDPM 前向 Markov 加噪与闭式边缘]]"]
solutions: ["[[解答 - DDPM 前向 Markov 加噪与闭式边缘]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ddpm-forward-marginal-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# DDPM 前向 Markov 加噪与闭式边缘

> [!abstract] 一句话结论
> DDPM 的 forward process 是固定的线性 Gaussian Markov chain。虽然它逐步加噪，却可把独立 Gaussian 噪声合并，从 $x_0$ 一次采到任意 $x_t$：$x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$。这使训练无需真的跑前 $t$ 步。

## 一、对象与符号先固定

数据 $x_0\in\mathbb R^d$ 来自 $q_{data}$。给定 schedule $\beta_1,\ldots,\beta_T\in(0,1)$，定义

$$\alpha_t=1-\beta_t,
\qquad \bar\alpha_t=\prod_{s=1}^t\alpha_s,
\qquad \bar\alpha_0=1.$$

forward kernel 是

$$
\boxed{q(x_t\mid x_{t-1})=
\mathcal N(x_t;\sqrt{\alpha_t}x_{t-1},\beta_tI).}
$$

等价重参数化为

$$x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{\beta_t}\epsilon_t,
\qquad \epsilon_t\overset{iid}\sim\mathcal N(0,I).$$

$q$ 固定，不由 neural network 训练；模型参数只进入后续 reverse chain。

## 二、两步推导看清噪声怎样合并

第一步：

$$x_1=\sqrt{\alpha_1}x_0+\sqrt{\beta_1}\epsilon_1.$$

第二步代入：

$$
\begin{aligned}
x_2
&=\sqrt{\alpha_2}x_1+\sqrt{\beta_2}\epsilon_2\\
&=\sqrt{\alpha_1\alpha_2}x_0
+\sqrt{\alpha_2\beta_1}\epsilon_1
+\sqrt{\beta_2}\epsilon_2.
\end{aligned}
$$

后两项是独立零均值 Gaussian，协方差相加为

$$
(\alpha_2\beta_1+\beta_2)I
=[\alpha_2(1-\alpha_1)+(1-\alpha_2)]I
=(1-\alpha_1\alpha_2)I.
$$

所以可合写为 $\sqrt{1-\bar\alpha_2}\epsilon$，其中新 $\epsilon\sim N(0,I)$；它分布相等，不是逐样本等于原来的某一个 $\epsilon_t$。

## 三、一般闭式边缘

归纳得到

$$
\boxed{q(x_t\mid x_0)=
\mathcal N(x_t;\sqrt{\bar\alpha_t}x_0,(1-\bar\alpha_t)I),}
$$

以及一次采样式

$$
\boxed{x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,
\qquad \epsilon\sim\mathcal N(0,I).}
$$

### 3.1 归纳步骤

假设 $x_{t-1}\mid x_0$ 均值为 $\sqrt{\bar\alpha_{t-1}}x_0$、方差为 $(1-\bar\alpha_{t-1})I$。经一步线性 Gaussian 变换：

$$
E[x_t\mid x_0]=\sqrt{\alpha_t\bar\alpha_{t-1}}x_0
=\sqrt{\bar\alpha_t}x_0,
$$

$$
\operatorname{Var}(x_t\mid x_0)
=\alpha_t(1-\bar\alpha_{t-1})I+\beta_tI
=(1-\bar\alpha_t)I.
$$

## 四、最小手算

取 $d=1$，$\beta_1=0.1,\beta_2=0.2$，则 $\alpha_1=0.9,\alpha_2=0.8,\bar\alpha_2=0.72$。若 $x_0=2$，

$$x_2\mid x_0=2\sim\mathcal N(2\sqrt{0.72},0.28).$$

均值约 $1.697$，标准差约 $0.529$。schedule 的 variance 是 $0.28$，采样时乘的是其平方根；漏平方根是最常见代码错误之一。

## 五、为什么末端接近标准 Gaussian

若 $\bar\alpha_T\approx0$，则

$$q(x_T\mid x_0)\approx\mathcal N(0,I)$$

并几乎忘记 $x_0$。但有限 $T$ 时通常不是严格相等；prior mismatch 项

$$D_{KL}(q(x_T\mid x_0)\|p(x_T))$$

仍出现在 ELBO。把“约等于标准噪声”写成恒等式会掩盖端点误差。

## 六、SNR 与可辨认程度

令 $a_t=\sqrt{\bar\alpha_t}$、$\sigma_t=\sqrt{1-\bar\alpha_t}$，则

$$\operatorname{SNR}_t=\frac{a_t^2}{\sigma_t^2}
=\frac{\bar\alpha_t}{1-\bar\alpha_t}.$$

小 $t$ 高 SNR，$x_t$ 仍接近数据；大 $t$ 低 SNR，噪声占主导。SNR 是相对于数据已按声明尺度归一化后的信号—噪声比；换数据缩放会改变口径。

## 七、训练张量合同

图像 batch $x_0:[B,C,H,W]$；采样 $t:[B]$，从预计算表 gather $a_t,\sigma_t$ 并 reshape 为 $[B,1,1,1]$；采样 $\epsilon$ 与 $x_0$ 同形；构造 $x_t=a_tx_0+\sigma_t\epsilon$。不同样本可取不同 $t$，不能错把 batch 共享 scalar 当唯一合法实现。

数值上用 float64 预计算 $\log\bar\alpha_t=\sum_{s\le t}\log(1-\beta_s)$，再 cast；大 $T$ 下直接 float16 cumprod 易 underflow。

## 八、科学空间研读框

[[S-2022-Su-9119-DDPM拆楼建楼]]的“拆楼”准确对应固定 forward corruption；[[S-2022-Su-9164-DDPM贝叶斯去噪]]进入累计噪声和后验。注意博客早期文章的 $\alpha_t,\beta_t$ 是一步 signal/noise amplitude，本卷的 $\beta_t$ 是 variance；必须先翻译再比较公式。

## 九、图：逐步 Markov 与一次采样为何等价

先看图回答：训练时为何可以跳过 $x_1,\ldots,x_{t-1}$，而这又为什么不把整个 joint path 删除？

![[00-知识库管理/_assets/figures/generative-models/fig-ddpm-forward-marginal-v1.svg|900]]

> [!figure] 图 50.6-01　DDPM 的逐步 forward chain、累计 signal 与闭式边缘
> 上方是 Markov path，下方把独立 Gaussian 噪声合成一个 marginal noise。来源：据 DDPM Gaussian forward process 独立绘制。

**怎样读图**：沿上方看 joint path 的条件结构；沿下方看给定 $x_0,t$ 时的边缘采样捷径。闭式边缘只替代训练取 $x_t$ 的计算，不声明中间路径不存在。

**图没有证明什么**：图不证明 learned reverse 准确，不证明有限 $T$ 的 $x_T$ 严格标准正态，也不证明任意非 Gaussian corruption 都有同样闭式。

## 十、本节回顾与训练

- forward 是固定 Gaussian Markov chain；
- $\bar\alpha_t$ 是乘积，不是 $\sum\alpha_t$；
- 独立 Gaussian 线性组合仍 Gaussian，方差相加；
- 一次采样给同一 conditional marginal，不给同一逐步 noise realization；
- [[习题 - DDPM 前向 Markov 加噪与闭式边缘]]
- [[解答 - DDPM 前向 Markov 加噪与闭式边缘]]
