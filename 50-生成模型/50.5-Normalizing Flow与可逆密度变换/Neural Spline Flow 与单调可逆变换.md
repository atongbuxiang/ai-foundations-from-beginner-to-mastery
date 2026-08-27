---
type: model
status: verified
area: [generative-models, normalizing-flows, splines]
node_id: GEN-38
prerequisites: ["[[Coupling Layer、NICE 与 RealNVP]]", "[[函数极限、连续性与收敛模式]]"]
related: ["[[Autoregressive Flow、MAF 与 IAF 的方向权衡]]", "[[Flow 的 Support、Dequantization、TARFLOW 与证据地图]]"]
sources: ["[[S-2019-Durkan-Neural-Spline-Flows]]", "[[S-2019-Ho-FlowPlusPlus]]"]
exercises: ["[[习题 - Neural Spline Flow 与单调可逆变换]]"]
solutions: ["[[解答 - Neural Spline Flow 与单调可逆变换]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-flow-spline-monotonicity-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Neural Spline Flow 与单调可逆变换

> [!abstract] 一句话结论
> Neural spline flow 不再把每个被更新坐标限制为一个 affine map，而是在有限区间内使用严格单调、连续可微、可解析求逆的分段有理二次函数。conditioner 预测 bin 宽、高和结点导数；正参数保证单调，最小 bin、边界匹配与稳定选根保证它在浮点中仍可用。

## 一、为什么 affine coupling 可能太僵

固定 conditioner 输出后，affine transform $y=ax+b$ 在整个坐标轴只有一个斜率。要表示局部“这里压缩、那里拉伸”，必须堆很多层。若把单坐标变换升级为可调的单调曲线，一层即可获得多处局部曲率，同时保持 triangular/coupling 外壳。

## 二、先掌握分箱参数合同

在区间 $[-B,B]$ 上选 $K$ 个 bins。输入 knot 为

$$-B=x^{(0)}<x^{(1)}<\cdots<x^{(K)}=B,$$

输出 knot 为

$$-B=y^{(0)}<y^{(1)}<\cdots<y^{(K)}=B.$$

宽和高分别为

$$w_k=x^{(k+1)}-x^{(k)}>0,\qquad
h_k=y^{(k+1)}-y^{(k)}>0,$$

且 $\sum_k w_k=\sum_k h_k=2B$。实现常令

$$
w_k=w_{min}+(2B-Kw_{min})\operatorname{softmax}(\hat w)_k,
$$

高同理；结点导数令 $d_k=d_{min}+\operatorname{softplus}(\hat d_k)>0$。这三类正性分别保证输入 bins 不重叠、输出 knots 严格上升、局部导数不翻转。

## 三、单个 rational-quadratic bin

在第 $k$ 个 bin，令

$$\xi=\frac{x-x^{(k)}}{w_k}\in[0,1],\qquad
\delta_k=\frac{h_k}{w_k}>0.$$

一种常用 rational-quadratic 形式为

$$
y=y^{(k)}+
\frac{h_k\left[\delta_k\xi^2+d_k\xi(1-\xi)\right]}
{\delta_k+\left(d_{k+1}+d_k-2\delta_k\right)\xi(1-\xi)}.
$$

它满足端点值 $x^{(k)}\mapsto y^{(k)}$、$x^{(k+1)}\mapsto y^{(k+1)}$，并把端点导数接成 $d_k,d_{k+1}$。相邻 bins 共享 knot 和导数，因此整体至少 $C^1$。

在正宽、高、导数与合法分母条件下，$dy/dx>0$，函数严格递增，从而每个 $y$ 有唯一 $x$。

## 四、为什么 inverse 仍解析

给定 $y$，先用 sorted output knots 找到所在 bin。把上式乘开并移项，可得到关于 $\xi$ 的二次方程

$$a\xi^2+b\xi+c=0.$$

选择落在 $[0,1]$ 的唯一根，再还原 $x=x^{(k)}+w_k\xi$。重要的是“二次可解”，不是必须背所有展开系数；实现必须检查：

- 根确在 $[0,1]$；
- 判别式因舍入出现微小负数时如何处理；
- $a\approx0$ 时退化为线性方程；
- 使用避免 catastrophic cancellation 的稳定二次公式。

## 五、logdet 与 tails

逐坐标 logdet 是

$$\log|dy/dx|,$$

coupling/autoregressive 外壳再对被变换坐标求和。不能以 finite difference 替代训练所需解析导数；finite difference 只适合作小维审计。

区间外常设 linear tails，例如 identity。要让边界连续可微，通常令端点映射为自身并令边界导数为 1。若 tail、端点导数或 logit preprocessing 口径不同，likelihood 会改变。

## 六、一个最小直觉例

设 $[-1,1]$ 分为两箱，输入 widths $(1,1)$，输出 heights $(0.5,1.5)$。左半区平均 slope 为 $0.5$，把空间压缩，density 相应升高；右半区平均 slope 为 $1.5$，把空间拉伸，density降低。结点导数决定两侧如何平滑连接，而不改变总区间端点。

若某 width 接近 0，即使仍为正，局部 slope/二次系数也可能极端，bin search 和 inverse 都不稳；这就是设置 $w_{min},h_{min},d_{min}$ 的原因。

## 七、conditioner 预测什么

在 coupling spline 中，$x_A$ 的网络为 $x_B$ 的每个元素输出约 $3K+1$ 个 raw 参数；在 autoregressive spline 中，第 $i$ 个坐标参数只依赖更早坐标。外壳决定并行方向，spline 只替换“每维可逆变换族”。因此 spline 不消除 MAF/IAF 的串行依赖。

## 八、证据与研究边界

[[S-2019-Durkan-Neural-Spline-Flows]]建立 rational-quadratic spline flow 的方法与实验；[[S-2019-Ho-FlowPlusPlus]]展示更丰富 coupling/dequantization 的另一条改进线。已建立的是方法和指定 benchmark；“spline 总优于 affine”依赖参数、预算、数据与实现，必须受控比较。

## 九、图：正参数如何变成严格单调曲线

先看图回答：宽、高与 knot derivative 三类参数分别控制哪一种几何自由度，哪个条件被删掉会直接破坏双射？

![[00-知识库管理/_assets/figures/generative-models/fig-flow-spline-monotonicity-v1.svg|900]]

> [!figure] 图 50.5-06　Rational-quadratic spline 的 knots、bins、局部斜率与 inverse 选根
> 左侧画严格递增 knots，右侧画参数化—bin search—二次选根流程。来源：据 neural spline flow 方法独立重绘。

**怎样读图**：先看每个输入 bin 和输出 bin 都有正尺寸，再看曲线穿过共享 knots 且切线为正；逆向先定位 output bin，不是在全曲线上盲目迭代。

**图没有证明什么**：示意曲线不代替 rational-quadratic 导数证明，不保证最小 bin 取值对所有 dtype 合适，也不证明更多 bins 必然提升泛化。

## 十、本节回顾与训练

- spline 增强逐坐标变换，不改变 coupling/autoregressive 外壳；
- 正 widths/heights 建立有序 knots，正 derivatives 保持局部单调；
- inverse 由 output bin search 和二次选根得到；
- minimum bin、tails、boundary derivative 和稳定选根是模型语义的一部分；
- analytic log derivative 进入 likelihood，finite difference 只做审计。

- [[习题 - Neural Spline Flow 与单调可逆变换]]
- [[解答 - Neural Spline Flow 与单调可逆变换]]

