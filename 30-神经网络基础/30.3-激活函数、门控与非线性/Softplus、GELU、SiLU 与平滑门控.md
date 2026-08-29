---
type: derivation
status: draft
area: [neural-networks/activations, softplus, gelu, silu]
aliases: [Smooth Rectifiers, Gaussian Error Linear Unit, Swish]
node_id: NN-21
prerequisites: ["[[Sigmoid、Tanh 与饱和梯度]]", "[[ReLU、Leaky ReLU 与次梯度约定]]", "[[常用连续分布与指数族]]"]
related: ["[[GLU、GeGLU、SwiGLU 与乘性门]]", "[[激活函数的数值稳定、尺度与经验选择]]"]
sources: ["[[S-2016-Hendrycks-Gimpel-GELU]]", "[[S-2018-Elfwing-Uchibe-Doya-SiLU]]", "[[S-2017-Ramachandran-Zoph-Le-Swish]]", "[[S-2020-Su-7309-GELU近似]]", "[[S-2021-Su-8718-ReLU光滑近似]]"]
exercises: ["[[习题 - Softplus、GELU、SiLU 与平滑门控]]"]
solutions: ["[[解答 - Softplus、GELU、SiLU 与平滑门控]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-smooth-activation-operators-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# Softplus、GELU、SiLU 与平滑门控

> [!abstract] 本章主问题
> Softplus 平滑 max，GELU 用 Gaussian CDF 门控，SiLU/Swish 用 sigmoid 自门控。它们都接近 ReLU，却在负侧、单调性、导数上界、二阶曲率与 kernel 代价上不同。“平滑”不是一个单指标，近似公式也必须携带误差、dtype 与 backward 一致性。

## 课程位置与两遍学习路线

- **承接什么：** NN-17—20 已比较饱和、kink、泄漏和指数负支；本页进一步问“平滑 ReLU”究竟平滑了哪个对象；
- **本页解决什么：** 区分 soft maximum、Gaussian probability gate 与 sigmoid self-gate，并同时比较函数、斜率、曲率和稳定实现；
- **后续为何需要：** NN-22 会把 self-gate 扩展成两条 learned projections 的乘积，NN-24 再把 exact/approx kernel 纳入经验选择。

**第一遍只复算统一三点。** 分别计算 Softplus、GELU、SiLU 的输出和一阶导，观察中心值、负侧符号和 slope 是否越过 $[0,1]$。

**第二遍再审计曲率与实现。** 检查 convexity、非单调区、exact/approx 误差、dtype、fusion 和 double backward；“平滑”不能替代完整合同。

### 问题链

1. Softplus 平滑的是 max，GELU/SiLU 平滑的是 gate，这两种构造差在哪里？
2. 为什么 GELU/SiLU 可以在负区输出负值且局部导数为负？
3. 一阶光滑是否自动意味着全局 convex 或更容易优化？
4. tanh/sigmoid 近似 GELU 时，forward 接近是否保证 derivative 也接近？
5. AI kernel 中 exact、approximate、dtype 与 backward flag 为什么必须共同记录？

> [!check] 第一遍停靠线
> 若你能在 $s_\triangle$ 上复算三种输出和斜率，并解释 Softplus 为何 convex 而 GELU/SiLU 不是，就可以进入乘性门；曲率变号与实现误差留到第二遍。

## 符号与对象账本

| 对象 | 构造 | 在 AI 中的角色 | 关键边界 |
|---|---|---|---|
| $\operatorname{softplus}_\beta$ | temperature LSE | positive scale/smooth rectifier | 中心值非零、全局 convex |
| $x\Phi(x)$ | Gaussian probability gate | GELU hidden activation | exact/approx 实现不同 |
| $x\sigma(x)$ | sigmoid self-gate | SiLU/Swish hidden activation | 负侧非单调 |
| $\phi'(x),\phi''(x)$ | local slope/curvature | VJP 与高阶 AD | 不等于整网稳定性 |
| approximation flag | implementation contract | compiler/kernel 选择 | 训练推理不一致会改函数 |

### 贯穿算例：同一三点上的三种平滑机制

沿用 $s_\triangle=(-2,0,2)$，取 $\beta=1$。得到

$$
\operatorname{softplus}(s_\triangle)\approx(0.126928,0.693147,2.126928),\quad
\operatorname{softplus}'(s_\triangle)\approx(0.119203,0.5,0.880797),
$$

$$
\operatorname{GELU}(s_\triangle)\approx(-0.045500,0,1.954500),\quad
\operatorname{GELU}'(s_\triangle)\approx(-0.085232,0.5,1.085232),
$$

$$
\operatorname{SiLU}(s_\triangle)\approx(-0.238406,0,1.761594),\quad
\operatorname{SiLU}'(s_\triangle)\approx(-0.090784,0.5,1.090784).
$$

三者中心 slope 都是 $1/2$，但 Softplus 中心值为 $\log2$ 且输出为正；GELU/SiLU 允许小负输出与负 slope。下一页将把 sigmoid/SiLU 作为 learned gate branch，而不是孤立 elementwise curve。

## 核心公式七问：$\operatorname{SiLU}(x)=x\sigma(x)$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 让输入值按自身产生的 soft gate 连续调制 |
| 对象 | value 与 gate 来自同一 scalar；输出、输入同 shape |
| 来路 | 恒等 value branch $x$ 与 sigmoid gate $\sigma(x)$ 的乘积 |
| 步骤 | derivative 必须用 product rule：$\sigma+x\sigma(1-\sigma)$ |
| 读法 | 负输入被软抑制但可保留小负值，正大输入渐近 identity |
| 检查 | $x=0$ 输出 0、斜率 $1/2$；两端分别趋 0 与 identity |
| 去路 | SwiGLU、smooth FFN、fused activation 与 higher-order optimization |

## 一、Softplus：带温度的 Smooth Max

对 $\beta>0$，

$$
\operatorname{softplus}_\beta(x)=\frac1\beta\log(1+e^{\beta x}).
$$

导数与二阶导为

$$
s'(x)=\sigma(\beta x),
\qquad
s''(x)=\beta\sigma(\beta x)(1-\sigma(\beta x))>0.
$$

所以它严格递增、严格凸、$C^\infty$，值域 $(0,\infty)$。由 log-sum-exp 界，

$$
\boxed{\operatorname{ReLU}(x)\le s(x)\le\operatorname{ReLU}(x)+\frac{\log2}{\beta}.}
$$

$\beta\to\infty$ 时一致逼近 ReLU，但中心曲率 $s''(0)=\beta/4$ 增大，极限函数在 0 失去光滑性。

## 二、Softplus 的稳定实现

朴素 `log(1+exp(x))` 会在大正数溢出、在大负数丢失小量。稳定恒等式是

$$
\operatorname{softplus}(x)=\max(x,0)+\log(1+e^{-|x|}),
$$

实现上使用 `log1p`。它还常用于 positive scale parameterization，但输出严格大于 0 不等于离 0 有固定下界。

## 三、GELU：Gaussian Probability Gate

令 $\Phi,\varphi$ 为标准正态 CDF/PDF：

$$
\operatorname{GELU}(x)=x\Phi(x)
=\frac x2\left(1+\operatorname{erf}\frac{x}{\sqrt2}\right).
$$

可把它读作 $x$ 乘“Gaussian threshold 被通过”的概率。导数与二阶导为

$$
g'(x)=\Phi(x)+x\varphi(x),
$$

$$
g''(x)=(2-x^2)\varphi(x).
$$

因此 GELU 不是全局 convex；它在 $|x|=\sqrt2$ 处改变曲率，负侧存在小的非单调区，导数可略小于 0 或大于 1。

## 四、SiLU/Swish：Sigmoid Self-Gating

$$
\operatorname{SiLU}_\beta(x)=x\sigma(\beta x).
$$

$\beta=1$ 通常称 SiLU/Swish。导数为

$$
f'(x)=\sigma(\beta x)+\beta x\sigma(\beta x)(1-\sigma(\beta x)).
$$

它 $C^\infty$，正侧渐近 identity，负侧渐近 0，但在一段负区间非单调。$\beta\to0$ 时 $f(x)\to x/2$；$\beta\to\infty$ 时逐点趋 ReLU（0 点均为 0）。

## 五、三种“平滑 ReLU”并不相同

| 函数 | 负无穷极限 | 单调 | convex | 中心值/斜率 |
|---|---:|---|---|---|
| Softplus | $0^+$ | 是 | 是 | $(\log2/\beta,1/2)$ |
| GELU | $0^-$ | 否 | 否 | $(0,1/2)$ |
| SiLU | $0^-$ | 否 | 否 | $(0,1/2)$ |

Softplus 是 soft maximum；GELU/SiLU 是 self-gating。平滑卷积 ReLU 与 Gaussian kernel 实际产生 $x\Phi(x)+\varphi(x)$，不等于 GELU；必须分清“平滑阶跃再乘 $x$”和“直接卷积整条 ReLU”。

## 六、GELU 近似与合同

常见近似包括

$$
\frac x2\left[1+\tanh\!\left(\sqrt{\frac2\pi}(x+0.044715x^3)\right)\right]
$$

及 $x\sigma(1.702x)$。近似选择必须声明：拟合区间、forward 最大误差、derivative 误差、dtype、硬件 kernel 和 checkpoint compatibility。训练与推理若使用不同近似，函数本身已经改变。

## 七、局部斜率与深层边界

GELU/SiLU 的 derivative 并不被 $[0,1]$ 限制；局部 slope 略超 1 不自动导致梯度爆炸，负 slope 也不表示全局 non-monotone network 必然不稳定。仍需分析 $D_\ell W_\ell$ 的方向乘积、normalization 与 residual scaling。

## 八、数值与自动微分

- exact GELU 依赖 erf/CDF；approximate GELU 依赖 tanh 或 sigmoid；
- Softplus 用 `max + log1p(exp(-abs))`；
- SiLU 应复用稳定 sigmoid，不显式计算大正指数；
- fused forward/backward 必须使用同一 approximation flag；
- double backward 要验证二阶公式，而非只复用一阶近似。

## 九、图：同一 ReLU 邻域的三种构造

先看图回答：为什么 Softplus 的 convexity 不能外推给 GELU/SiLU？

![[00-知识库管理/_assets/figures/neural-networks/fig-smooth-activation-operators-v2.svg|900]]

> [!figure] 图 30.3-05　Softplus、GELU、SiLU 的构造、斜率与曲率
> 左栏区分 soft-max 与 probability self-gate；中栏叠加函数和 derivative window；右栏记录 exact/approximate kernel、误差与 dtype 合同。来源：依据 Hendrycks–Gimpel、Elfwing–Uchibe–Doya、Ramachandran–Zoph–Le 及科学空间相关推导独立绘制；由 [[00-知识库管理/_labs/code/plot_activation_advanced_v2.py]] 确定性生成。

**怎样读图**：先认构造算子，再读 derivative/curvature，最后检查实现选的是 exact 还是 approximation。

**图没有证明什么**：图没有证明平滑函数普遍优于 ReLU，也没有证明某个近似在所有输入、导数阶数和硬件上等价。

## 十、验证协议与回顾

扫描输入区间与 dtype，比较 forward、一阶和二阶导；记录 activation/derivative moments、wall-clock、fusion 和模型指标。对负侧非单调区专门采样；对 Softplus positive output 检查 underflow 与最小 scale。

> [!summary]
> Softplus 平滑 max；GELU 与 SiLU 平滑 gate。三者的代数对象、曲率、数值路径和深层尺度不同，近似必须作为可审计实现合同。

- [[习题 - Softplus、GELU、SiLU 与平滑门控]]
- [[解答 - Softplus、GELU、SiLU 与平滑门控]]
