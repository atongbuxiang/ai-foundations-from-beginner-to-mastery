---
type: concept
status: verified
area: [training, optimization, curvature, counterexamples]
node_id: TRN-21
aliases: [Empirical Fisher 陷阱, GGN 近似边界]
prerequisites: ["[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[协方差、相关性与条件期望]]", "[[非凸优化、鞍点与深度网络损失地形]]"]
related: ["[[Adam 的尺度不变性、Sign 近似与 Update RMS]]", "[[K-FAC、Kronecker 分块与阻尼合同]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2019-Kunstner-Empirical-Fisher]]", "[[S-2020-Martens-Natural-Gradient-Curvature]]", "[[S-2024-Su-10588-Hessian近似与自适应学习率]]"]
exercises: ["[[习题 - GGN、经验 Fisher 与曲率近似陷阱]]"]
solutions: ["[[解答 - GGN、经验 Fisher 与曲率近似陷阱]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-ggn-empirical-fisher-counterexamples-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# GGN、经验 Fisher 与曲率近似陷阱

> [!abstract] 一句话结论
> PSD、由 gradient outer product 构成、或在某个极限接近 Hessian，都不足以证明一个矩阵是可靠曲率。GGN 的近似误差是被删去的模型二阶项；empirical Fisher 的偏差来自标签测度与 non-central gradient moment。最有教育意义的检验不是大模型曲线，而是能让这些差异精确暴露的标量反例。

## 一、把“近似 Hessian”拆成三种不同问题

给候选矩阵 $C(\theta)$，至少要分别问：

1. **代数对象**：$C$ 是否由 Hessian 分解中删除某一项得到？
2. **统计对象**：$C$ 是否在某个数据/模型分布下无偏估计另一个矩阵？
3. **优化效果**：$(C+\lambda I)^{-1}g$ 是否产生有用方向？

前两问不自动推出第三问；第三问的经验成功也不能反推前两问成立。

## 二、GGN 遗漏的精确二阶项

对 $z=f_\theta(x)$：

$$
H=G+R,\qquad
G=J^TH_z\ell J,\qquad
R=\sum_k\ell_{z_k}\nabla_\theta^2f_k.
$$

若输出 loss convex，$G\succeq0$；但 $R$ 可含正/负曲率。称 GGN 为“PSD Hessian approximation”时，必须同时报告 $R$ 在研究点为何可能小：

- 模型近线性；
- residual/output gradient 小；
- 或指定期望下 cancellation。

### 2.1 非线性最小二乘反例

令

$$
f_\theta=\theta^2,\qquad
L(\theta)=\frac12(\theta^2-1)^2.
$$

有 $J=2\theta$、residual $r=\theta^2-1$，

$$
G=J^TJ=4\theta^2,\qquad
H=G+r\,f''=4\theta^2+2(\theta^2-1)=6\theta^2-2.
$$

在 $\theta=0$，$G=0$，但 $H=-2$。GGN 看见 flat PSD block，真实 Hessian 看见 negative curvature；这不是数值误差，而是近似定义删掉了 $rf''$。

## 三、Empirical Fisher 可在最优点退化为零

考虑 unit-variance Gaussian mean model $p_\theta(y)=\mathcal N(\theta,1)$，一个观测 $y$ 的 NLL：

$$
L(\theta)=\frac12(\theta-y)^2+\text{const}.
$$

于是

$$
H=G=F=1,\qquad F_{emp}=(\theta-y)^2.
$$

对这个样本的最优点 $\theta=y$，empirical Fisher 恰为 0，而 Hessian/true Fisher 仍为 1。离最优点很远时 EF 又随 residual 平方任意变大。它不是稳定的 curvature proxy。

### 3.1 为什么 true Fisher 仍为 1

Score 为 $s=y'-\theta$，但 true Fisher 用 $y'\sim\mathcal N(\theta,1)$：

$$
F=\mathbb E[(y'-\theta)^2]=1.
$$

EF 使用固定 observed $y$；二者只是公式外形相似，随机标签来源不同。

## 四、Batch-mean outer product 是第三个对象

两个 scalar per-sample gradients $g_1=1,g_2=-1$：

$$
\frac12(g_1^2+g_2^2)=1,
$$

但

$$
\left(\frac{g_1+g_2}{2}\right)^2=0.
$$

因此用训练代码里已经 reduction 的 batch gradient 外积，不能替代 per-sample EF。矩阵情形还会丢 rank：单个 batch mean outer product rank 至多 1。

## 五、相等关系的量词阶梯

### 5.1 Fisher = expected negative score Hessian

需要支持、可积性与交换求导积分的 regularity，而且期望仍在模型分布下。

### 5.2 Fisher = GGN

常见充分结构是负对数似然的输出分布属于指数族，网络输出为 natural parameter。若输出坐标不是 natural parameter，需带相应 pullback，不能只按名字写等号。

### 5.3 Population Hessian = Fisher

在模型正确指定、数据由某个 $p_{\theta^*}$ 产生，并在 $\theta^*$ 等条件下，可由信息恒等式得到。Misspecification 或离开 optimum 后不保留。

### 5.4 Empirical Fisher 接近 Fisher

除大样本外，还需 observed-label 分布接近当前 model-label 分布；过参数化模型在训练数据上 residual 近零时，EF 甚至会塌缩而 Fisher 不塌缩。

## 六、PSD 不是质量证书

任意 $A^TA$ 都 PSD，但可能：

- rank 太低，重要方向完全为零；
- eigenvectors 与 Hessian 错位；
- eigenvalues scale 严重错误；
- 来自噪声而非 curvature；
- damping 后方向几乎退化成 gradient descent。

更合格的矩阵近似诊断包括：

$$
\frac{\|C-H\|}{\|H\|},
\quad
\frac{v^TCv}{v^THv},
\quad
\cos((C+\lambda I)^{-1}g,(H+\lambda I)^{-1}g),
$$

以及 predicted/actual reduction。每个指标仍需声明 norm、方向分布和 damping。

## 七、Gradient second moment 的另一种合法解释

[[S-2019-Kunstner-Empirical-Fisher]]指出，empirical Fisher 的 population 对象是 gradient 的非中心二阶矩，可用于 noise/variance adaptation 的解释。[[S-2024-Su-10588-Hessian近似与自适应学习率]]则在近最优、Hessian 稳定、trajectory covariance 近各向同性等条件下联系 $\mathbb E[gg^T]$ 与 $H^2$。

这两条解释并不矛盾：同一统计量可同时含 signal、noise 和局部 curvature 经轨迹分布过滤后的信息。正确说法是“在这些假设下可作为 scale proxy”，不是“它本来就是 Fisher/Hessian”。

## 八、图：三个最小反例删除三条错误等号

先看图回答：哪个反例暴露 negative curvature，哪个暴露 label-measure mismatch，哪个暴露 reduction/rank 错误？

![[00-知识库管理/_assets/figures/training-optimization/fig-ggn-empirical-fisher-counterexamples-v1.svg|900]]

> [!figure] 图 TRN-21　GGN、Fisher 与 EF 的三类不等价证书
> 左侧用 $f=\theta^2$ 展示 GGN 漏掉模型二阶负曲率；中间用 Gaussian mean 展示 optimum 处 EF=0、F=H=1；右侧用 $(1,-1)$ 展示 batch-mean outer product 为 0 而 per-sample second moment 为 1。来源：依据 [[S-2019-Kunstner-Empirical-Fisher]] 与课程独立构造。

**怎样读图**：每个反例只删除一个常见错误等号，保留其余对象；不要用一个例子替代全部相等条件审计。

**图没有证明什么**：反例不说明 GGN/EF 永远无用；它只证明不能无条件以曲率身份使用。

## 九、AI 审计清单

看到 `fisher`, `ggn`, `gradient_covariance` 或 `second_order` 变量名时，检查：per-sample 还是 batch mean、labels 来自 data 还是 model、loss reduction、centered/non-centered、damping、rank、batch/EMA、参数 sharing、JVP/VJP 路径、更新方向 cosine 与 model ratio。

## 练习与独立解答

- [[习题 - GGN、经验 Fisher 与曲率近似陷阱]]
- [[解答 - GGN、经验 Fisher 与曲率近似陷阱]]
