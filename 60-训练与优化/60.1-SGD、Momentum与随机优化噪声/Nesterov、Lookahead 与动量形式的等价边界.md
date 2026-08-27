---
type: derivation
status: verified
area: [training, optimization, acceleration]
node_id: TRN-05
aliases: [NAG 实现翻译, Nesterov Look-ahead]
prerequisites: ["[[Momentum、EMA、偏差修正与框架约定]]", "[[加速梯度、动量与下界]]"]
related: ["[[二次模型的学习率—动量稳定域与阻尼]]", "[[Warmup、早期曲率与优化器状态建立]]"]
sources: ["[[S-2013-Sutskever-Momentum]]", "[[S-2026-PyTorch-SGD-Semantics]]", "[[S-2018-Su-5655-SGD到动量加速]]"]
exercises: ["[[习题 - Nesterov、Lookahead 与动量形式的等价边界]]"]
solutions: ["[[解答 - Nesterov、Lookahead 与动量形式的等价边界]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-nesterov-lookahead-variable-map-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Nesterov、Lookahead 与动量形式的等价边界

> [!abstract] 一句话结论
> Heavy-ball 在当前位置求梯度；经典 Nesterov 先按旧 velocity 外推，再在外推点求梯度。PyTorch 常见的“当前点 gradient + momentum buffer”形式可在常 learning rate、常 momentum、无 dampening 且状态正确映射时解释为对 look-ahead 变量的代数重写；它不是把 $\nabla f(x+\mu v)$ 粗暴替换为 $\nabla f(x)$。

## 一、先区分三个名称

1. **Heavy-ball / classical momentum**：在当前 $x_t$ 求 $\nabla f(x_t)$；
2. **Nesterov accelerated gradient（NAG）**：在外推点 $y_t$ 求梯度；
3. **Lookahead optimizer（大写名称）**：维护 fast/slow 两套权重、每若干步插值，是另一种算法家族。

本节标题中的 `look-ahead` 是“前瞻求梯度”的普通描述，不等同于第三种优化器。

## 二、Heavy-ball 与 NAG 的求值点

Heavy-ball：

$$
v_{t+1}=\mu v_t-\eta\nabla f(x_t),
\qquad x_{t+1}=x_t+v_{t+1}.
$$

一个适于比较的 NAG 形式是

$$
\begin{aligned}
y_t&=x_t+\mu v_t,\\
g_t&=\nabla f(y_t),\\
v_{t+1}&=\mu v_t-\eta g_t,\\
x_{t+1}&=x_t+v_{t+1}.
\end{aligned}
$$

两者都保留 velocity，差别在 gradient evaluation point。若 $f$ 是非线性的，通常

$$\nabla f(x_t+\mu v_t)\ne\nabla f(x_t).$$

## 三、为什么框架公式看起来没有外推点

令框架实际存储的 parameter 变量就是 $p_t\triangleq y_t$。在常 $\eta,\mu$ 下，定义 gradient buffer

$$b_t=-v_t/\eta.$$

由 NAG velocity 递推可得

$$b_{t+1}=\mu b_t+g_t.$$

现在推导 look-ahead variable 的下一步：

$$
\begin{aligned}
p_{t+1}=y_{t+1}
&=x_{t+1}+\mu v_{t+1}\\
&=x_t+(1+\mu)v_{t+1}\\
&=(p_t-\mu v_t)+(1+\mu)v_{t+1}\\
&=p_t+\mu v_{t+1}-\eta g_t\\
&=\boxed{p_t-\eta(g_t+\mu b_{t+1})}.
\end{aligned}
$$

最后一行就是“先更新 buffer，再用 $g_t+\mu b_{t+1}$ 更新 parameter”的形式。这里 $g_t$ 确实在 $p_t=y_t$ 上求得；外推已经吸收到**变量定义**里，而不是消失了。

> [!theorem] 有条件的轨迹等价
> 常 $\eta$、常 $\mu$、无 dampening/decay/clip，且初始化满足 $p_0=x_0+\mu v_0$、$b_0=-v_0/\eta$ 时，上述 look-ahead NAG 与 buffer 形式在状态映射下生成对应轨迹。变化超参数或错误初始化时，不应继续声明逐步等价。

## 四、最小二次例子

取 $f(x)=\tfrac12x^2$，$x_0=1,v_0=0$，$\eta=0.1,\mu=0.9$。

NAG：$y_0=1$，$g_0=1$，$v_1=-0.1$，$x_1=0.9$，所以 $y_1=x_1+0.9v_1=0.81$。

Buffer 变量：$p_0=y_0=1$，$b_1=g_0=1$，

$$p_1=1-0.1(1+0.9\cdot1)=0.81,$$

正好等于 $y_1$，而不是等于 base iterate $x_1=0.9$。若把两种公式里同名的 parameter 都误认为 $x_t$，会错误判断算法不一致。

## 五、近似“前瞻”与真正函数求值

在 $x_t$ 附近做一阶 Taylor：

$$
\nabla f(x_t+\mu v_t)
\approx\nabla f(x_t)+\mu H_t v_t.
$$

所以 look-ahead gradient 提前感受到沿 velocity 方向的 curvature。这个式子需要 Hessian 存在且位移足够小；它是局部近似，不是 NAG 加速定理本身。

## 六、哪些变化会破坏简单翻译

| 变化 | 为什么有影响 |
|---|---|
| $\eta_t$ 变化 | $b_t=-v_t/\eta_t$ 的比例随时间变 |
| $\mu_t$ 变化 | $p_t=x_t+\mu_tv_t$ 的变量映射也变 |
| dampening | buffer 中当前 gradient 系数不再是 1 |
| bias correction | 早期方向被额外重标度 |
| coupled decay | gradient evaluation 与 decay 插入点改变 |
| clipping | 变换非线性，不能在变量映射中自由搬移 |
| restart | velocity/buffer 是否清零决定新初始条件 |

PyTorch 文档中的 Nesterov 还要求 momentum 非零且 dampening 为零；复现应以所用版本的实际约束为准。

## 七、NAG 的“加速”究竟指什么

在一般 $L$-smooth convex 函数类上，特定 Nesterov 序列可达到 function gap $O(1/t^2)$；gradient descent 的经典最坏情形是 $O(1/t)$。这是一条关于函数类、oracle 与精确定义算法的定理。

深度学习中开启 `nesterov=True` 后 validation 更好/更快属于经验问题，受 stochastic noise、schedule、normalization 和预算影响。不能仅凭“有 look-ahead”就继承一般凸定理。

## 八、图：变量重命名怎样藏起外推点

先看图回答：为什么 base iterate $x_t$、look-ahead point $y_t$ 与框架 parameter $p_t$ 不能混成一个符号？

![[00-知识库管理/_assets/figures/training-optimization/fig-nesterov-lookahead-variable-map-v1.svg|900]]

> [!figure] 图 TRN-05　NAG 几何求值点与 buffer 实现的变量映射
> 左侧展示 $x_t\to y_t$ 的前瞻，右侧把 $p_t=y_t$ 后得到 current-gradient plus buffer 更新；绿色等号只在图下注明的常参数条件下成立。来源：据 Sutskever 等与 PyTorch 公式重绘，推导与标注由本课程重新组织。

**怎样读图**：先沿左边区分 base position、velocity 与 gradient point，再跨过中间的状态字典；右侧“当前点”指 $p_t$，它已对应左侧的 $y_t$。

**图没有证明什么**：图不提供一般凸 $O(1/t^2)$ 的 potential proof，也不说明变化 LR、stochastic gradient 或框架其他选项仍逐步等价。

## 九、科学空间研读框与研究边界

[[S-2018-Su-5655-SGD到动量加速]]强调动力学和前瞻直觉；本节点用状态映射说明为什么不同论文/框架的公式表面不同。若比较实验，应直接导出两步 buffer、gradient 和 parameter，而不是只对照优化器名称。

## 十、本节回顾

- Heavy-ball 与 NAG 的关键差别是 gradient evaluation point；
- 框架变量可能已经是 look-ahead point；
- buffer 形式的等价需要常 LR/常 momentum 和正确初始化；
- `Lookahead` optimizer 是另一个算法，不应与 Nesterov look-ahead 混名；
- 下一节 [[二次模型的学习率—动量稳定域与阻尼]] 将用特征根而非箭头直觉判断振荡和发散。

## 练习与独立解答

- [[习题 - Nesterov、Lookahead 与动量形式的等价边界]]
- [[解答 - Nesterov、Lookahead 与动量形式的等价边界]]
