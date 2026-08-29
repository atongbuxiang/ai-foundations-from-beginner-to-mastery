---
type: concept
status: draft
area: [neural-networks/activations, sigmoid, tanh, saturation]
aliases: [Logistic Activation, Hyperbolic Tangent, Saturating Nonlinearities]
node_id: NN-18
prerequisites: ["[[激活函数的角色、选择准则与函数性质]]", "[[一元导数与中值定理]]", "[[数值稳定性]]", "[[标量链式法则与反向传播递推]]"]
related: ["[[ReLU、Leaky ReLU 与次梯度约定]]", "[[方差传播与宽层均值场近似]]", "[[Softmax–Cross-Entropy 的稳定融合反向]]"]
sources: ["[[S-2010-Glorot-Bengio-Training-Difficulty]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]"]
exercises: ["[[习题 - Sigmoid、Tanh 与饱和梯度]]"]
solutions: ["[[解答 - Sigmoid、Tanh 与饱和梯度]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-sigmoid-tanh-saturation-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# Sigmoid、Tanh 与饱和梯度

> [!abstract] 本章主问题
> sigmoid 与 tanh 都是平滑、有界、两端饱和的 S 形函数。它们的价值不应被“会梯度消失”一句话抹掉：sigmoid 是 Bernoulli 参数化与 gate 的核心，tanh 提供零中心 bounded state。真正需要推导的是斜率、均值、尺度和深层 Jacobian 怎样共同作用，以及何时应使用稳定的 log-domain 公式。

## 课程位置与两遍学习路线

- **承接什么：** NN-17 给出了统一选择合同，现在先研究最典型的 bounded smooth activations；
- **本页解决什么：** 精确量化 sigmoid/tanh 的值、最大斜率、饱和速度、中心性和稳定实现，而不是笼统说“梯度消失”；
- **后续为何需要：** NN-19 将对比无上界 rectifier，NN-20 再用指数负支折中中心性与非饱和正侧。

**第一遍只算函数值和斜率。** 在 $-2,0,2$ 三点手算，并观察 sigmoid 的输出偏正、tanh 的零中心以及两端斜率同时下降。

**第二遍再看深度与语义。** 把权重 Jacobian、输入尺度、温度、log-domain 公式和 gate/output role 加回，区分局部饱和与整网梯度行为。

### 问题链

1. sigmoid 与 tanh 的代数关系如何连接它们的值域和导数？
2. “饱和”应由输出接近边界还是导数接近零来定量？
3. tanh 零中心为何改善均值，却不能自动保证深层梯度稳定？
4. sigmoid hidden activation 常受限，为什么 Bernoulli head 和 gate 仍需要它？
5. 极大正负输入下怎样避免指数 overflow 和 `log(0)`？

> [!check] 第一遍停靠线
> 若你能复算 sigmoid/tanh 在三点上的值与斜率，并解释 $0.25$ 或 $1$ 的局部上界为何不是整网保证，就可以进入 rectifier；稳定 log-domain 与深层乘积留到第二遍。

## 符号与对象账本

| 对象 | 值域/shape | 在 AI 中的典型角色 | 关键边界 |
|---|---|---|---|
| $\sigma(z)$ | $(0,1)$ | Bernoulli parameter、gate | 非零中心、两端饱和 |
| $\tanh z$ | $(-1,1)$ | bounded recurrent state | 两端饱和 |
| $\sigma'(z)$ | $(0,1/4]$ | local gate sensitivity | 不是整网 gradient norm |
| $\tanh'(z)$ | $(0,1]$ | local state sensitivity | 仍与 weights 相乘 |
| logit $z$ | unbounded score | stable BCE/log-sigmoid 输入 | 不应先转低精度概率再取 log |

### 贯穿算例：三点上的饱和与中心

沿用 $s_\triangle=(-2,0,2)$。数值为

$$
\sigma(s_\triangle)\approx(0.119203,0.5,0.880797),\qquad
\sigma'(s_\triangle)\approx(0.104994,0.25,0.104994),
$$

$$
\tanh(s_\triangle)\approx(-0.964028,0,0.964028),\qquad
\tanh'(s_\triangle)\approx(0.070651,1,0.070651).
$$

在 upstream 全 1 时，这两行导数就是各自 VJP。tanh 在中心让信号保持、两端比 sigmoid 此处更小；sigmoid 输出均为正，但作为 gate 正好给出 $0$ 到 $1$ 的软开关。局部观察必须与输入分布和权重尺度一起解释。

## 核心公式七问：$\sigma'(z)=\sigma(z)(1-\sigma(z)),\;\tanh'(z)=1-\tanh^2z$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 用 forward output 稳定、廉价地重建 local VJP slope |
| 对象 | 导数与输入同 shape；两式分别依赖缓存的 probability/state |
| 来路 | 对 logistic quotient 求导；tanh 由双曲函数恒等式或 sigmoid 关系得到 |
| 步骤 | 先稳定算 output，再代入乘积；极端输入避免直接计算危险指数 |
| 读法 | 越接近值域边界，局部可变化空间越小，斜率越接近零 |
| 检查 | $z=0$ 时分别为 $1/4,1$；$|z|\to\infty$ 时均趋零 |
| 去路 | LSTM/GRU gates、binary heads、temperature scaling、vanishing-gradient 与 stable fused losses |

## 一、定义、值域与关系

Logistic sigmoid 定义为

$$
\sigma(x)=\frac{1}{1+e^{-x}},
\qquad \sigma:\mathbb R\to(0,1).
$$

双曲正切为

$$
\tanh x=\frac{e^x-e^{-x}}{e^x+e^{-x}},
\qquad \tanh:\mathbb R\to(-1,1).
$$

二者由尺度和平移联系：

$$
\boxed{\tanh x=2\sigma(2x)-1.}
$$

所以它们不是完全不同的曲线；tanh 把 sigmoid 的输出中心从 $1/2$ 移到 0，并把输入尺度放大 2 倍。

## 二、导数与最大斜率

直接求导：

$$
\sigma'(x)=\sigma(x)(1-\sigma(x)),
$$

因为 $0<\sigma<1$，

$$
0<\sigma'(x)\le\frac14,
$$

等号只在 $x=0$ 取得。tanh 则有

$$
(\tanh x)'=1-\tanh^2x=\operatorname{sech}^2x,
\qquad 0<(\tanh x)'\le1.
$$

两者都严格单调、$C^\infty$；sigmoid 不是 odd，tanh 是 odd。

## 三、饱和的定量含义

当 $x\to+\infty$，

$$
1-\sigma(x)\sim e^{-x},
\qquad
\sigma'(x)\sim e^{-x};
$$

当 $x\to-\infty$，

$$
\sigma(x)\sim e^x,
\qquad
\sigma'(x)\sim e^x.
$$

对 tanh，$|x|\to\infty$ 时

$$
1-|\tanh x|\asymp e^{-2|x|},
\qquad
\tanh'(x)\asymp e^{-2|x|}.
$$

“饱和”不是输出等于常数，而是输出接近端点且导数指数变小；在有限精度中，极端输入还可能直接舍入到端点。

## 四、中心附近的 Taylor 结构

在 0 附近，

$$
\sigma(x)=\frac12+\frac{x}{4}-\frac{x^3}{48}+O(x^5),
$$

$$
\tanh x=x-\frac{x^3}{3}+O(x^5).
$$

因此 sigmoid 中心斜率只有 $1/4$；tanh 中心附近更接近 identity。这解释局部梯度差异，但不能脱离权重尺度比较整层 Jacobian。

## 五、深层乘积：最坏界与典型行为分开

若标量链 $h_\ell=\sigma(w_\ell h_{\ell-1})$，则

$$
\left|\frac{\partial h_L}{\partial h_0}\right|
=\prod_{\ell=1}^{L}|w_\ell|\,\sigma'(z_\ell)
\le\prod_{\ell=1}^{L}\frac{|w_\ell|}{4}.
$$

若所有 $w_\ell=1$ 且 $z_\ell=0$，上界正好是 $4^{-L}$。但若权重很大，梯度可能暂时放大，同时 preactivation 更易落入饱和区；只有联合分布分析才有意义。

对 tanh，在 $z=0$ 斜率为 1，不代表深链保持梯度：$W_\ell$ 的奇异值、偏置和状态漂移仍可把 $z$ 推到饱和区。

## 六、均值漂移：sigmoid 与 tanh 的关键差异

若 $Z$ 关于 0 对称，则

$$
E[\sigma(Z)]=\frac12
$$

因为 $\sigma(z)+\sigma(-z)=1$；而

$$
E[\tanh Z]=0
$$

因为 tanh 是 odd。sigmoid 的正均值会进入下一层 preactivation，和偏置、权重列和共同造成漂移；tanh 在对称输入下更自然地保持零均值。

这不是“tanh 永远零中心”的定理：输入不对称、bias 非零或训练后权重相关都会破坏条件。

## 七、稳定计算 sigmoid

朴素 $1/(1+e^{-x})$ 在大负数处可能计算 $e^{-x}$ 溢出。稳定分支是

$$
\sigma(x)=
\begin{cases}
1/(1+e^{-x}),&x\ge0,\\
e^x/(1+e^x),&x<0.
\end{cases}
$$

对 log-likelihood 更不应先算 probability 再取 log：

$$
\log\sigma(x)=-\operatorname{softplus}(-x),
$$

$$
\log(1-\sigma(x))=-\operatorname{softplus}(x).
$$

这些重写同时避免 overflow 与接近 1 时的 cancellation。

## 八、Tanh 的稳定性与输出缓存

成熟数值库通常直接提供稳定 tanh kernel。反向可缓存输出 $h=\tanh z$：

$$
\bar z=\bar h(1-h^2).
$$

若低精度 forward 已把 $h$ 舍入为 $\pm1$，反向即返回 0；这既可能反映真实极小斜率，也可能包含量化造成的提前饱和。应按 dtype 报告饱和率。

## 九、温度与输入缩放

令

$$
\sigma_\tau(x)=\sigma(x/\tau).
$$

则

$$
\sigma_\tau'(x)=\frac1\tau\sigma(x/\tau)(1-\sigma(x/\tau)).
$$

较小 $\tau$ 让中心斜率变大、过渡区变窄，同时更快进入两端饱和。输入缩放不是只改变“锐利程度”，也改变 backward scale。

## 十、为何 gate 仍大量使用 sigmoid

门控 $y=\sigma(g)\odot v$ 需要 $[0,1]$ 系数来连续插值“关闭—打开”。对 $g$ 的梯度为

$$
\bar g=(\bar y\odot v)\odot\sigma(g)(1-\sigma(g)).
$$

饱和会让 gate 难以改变，但也可形成接近离散的稳定记忆/选择状态。是否有利取决于任务和 bias initialization；不能从 hidden MLP 的经验直接推出 gate 不应使用 sigmoid。

## 十一、输出层中的正确角色

对 binary logit $z$，Bernoulli negative log-likelihood 可写为

$$
\ell(z,y)=\operatorname{softplus}(z)-yz.
$$

其导数是

$$
\frac{\partial\ell}{\partial z}=\sigma(z)-y.
$$

训练时使用 fused logits loss 比“sigmoid 后 binary cross-entropy”更稳定；推理展示 probability 时再显式计算 sigmoid。

## 十二、完整手算

令 $z=2$，$h=\sigma(z)$，$L=-\log h$（target 为 1）。则

$$
h\approx0.880797,
\qquad
\frac{dL}{dh}=-\frac1h,
\qquad
\frac{dh}{dz}=h(1-h).
$$

相乘得

$$
\frac{dL}{dz}=h-1\approx-0.119203.
$$

分开计算的链式法则与 fused 结果一致；fused 形式在极端 $z$ 下数值更可靠。

## 十三、诊断协议

1. 记录各层 preactivation 落在 $|z|>4,8$ 的比例；
2. 记录 derivative histogram，而不只看 activation histogram；
3. 分 dtype 比较精确饱和与舍入到端点的比例；
4. 检查 bias/normalization 是否导致均值漂移；
5. 对 logits loss 使用稳定 fused reference；
6. 将 gate 与 ordinary hidden activation 分层报告；
7. 同时扫描 input scale、initialization 与 depth。

## 十四、图：曲线、斜率与深度乘积

先看图回答：为什么 tanh 的中心斜率为 1 仍不足以保证深网梯度不消失？

![[00-知识库管理/_assets/figures/neural-networks/fig-sigmoid-tanh-saturation-v2.svg|900]]

> [!figure] 图 30.3-02　Sigmoid/Tanh：输出饱和、导数窗口与深层乘积
> 左栏比较值域与中心位置；中栏显示导数只在有限输入窗口显著；右栏把 activation slope、weight gain 与 depth 合成 Jacobian ledger。来源：依据 Glorot–Bengio 2010、Goodfellow–Bengio–Courville 与 D2L 独立绘制；由 [[00-知识库管理/_labs/code/plot_activation_foundations_v2.py]] 确定性生成。

**怎样读图**：先在输入轴上定位 preactivation 分布，再读 derivative window，最后与每层权重 gain 相乘；不能只盯住曲线中心。

**图没有证明什么**：图没有证明 sigmoid/tanh 不能用于 gate、output link 或浅网络，也没有给出真实训练轨迹的梯度分布。

## 十五、常见错误

1. 把 sigmoid 的输出均值 $1/2$ 当成任意输入分布下的结论；
2. 认为 tanh 中心斜率 1 就不会 vanishing gradient；
3. 先算极端 probability 再取 log；
4. 忘记 temperature 的 $1/\tau$ 链式因子；
5. 把低精度舍入到端点与精确数学饱和混为一谈；
6. 因 hidden MLP 不常用 sigmoid 就否定其 gate/likelihood 角色。

## 十六、回顾与练习

> [!summary]
> sigmoid/tanh 的核心结构是“平滑、有界、中心有斜率、两端指数饱和”。是否出现深层梯度问题取决于 preactivation 分布与权重 Jacobian；稳定 logits-domain 实现和任务角色同样重要。

- [[习题 - Sigmoid、Tanh 与饱和梯度]]
- [[解答 - Sigmoid、Tanh 与饱和梯度]]
