---
type: derivation
status: verified
area: [training, optimization, information-geometry]
node_id: TRN-20
aliases: [Natural Gradient, Fisher Metric]
prerequisites: ["[[镜像下降、Bregman 几何与自然梯度]]", "[[Hessian、GGN、Fisher 与经验 Fisher 对象总账]]", "[[交叉熵与 KL 散度]]", "[[互信息与依赖性]]"]
related: ["[[K-FAC、Kronecker 分块与阻尼合同]]", "[[GGN、经验 Fisher 与曲率近似陷阱]]", "[[Stiefel、谱球面、旋转 Muon 与约束更新]]"]
sources: ["[[S-1998-Amari-Natural-Gradient]]", "[[S-2020-Martens-Natural-Gradient-Curvature]]", "[[S-2015-Martens-Grosse-KFAC]]"]
exercises: ["[[习题 - 自然梯度、KL 局部几何与坐标不变性]]"]
solutions: ["[[解答 - 自然梯度、KL 局部几何与坐标不变性]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-natural-gradient-kl-coordinates-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 自然梯度、KL 局部几何与坐标不变性

> [!abstract] 一句话结论
> Ordinary gradient 是欧氏坐标下的最速方向；natural gradient 用模型分布的局部 KL/Fisher metric 衡量“同样大的改变”。Exact infinitesimal direction 对光滑可逆重参数化具有协变性，但 finite step、damping、近似 Fisher、离散 solver 和 parameter-wise clipping 都会削弱这一性质。

## 一、为什么 Euclidean gradient 依赖坐标单位

给一阶变化

$$
L(\theta+p)\approx L(\theta)+g^Tp.
$$

若约束 $\|p\|_2\le\epsilon$，最陡下降方向是 $-g$。但把参数从米换成厘米，Euclidean unit ball 的形状相对模型函数改变，ordinary gradient 数值也改变。

对概率模型，更自然的问题是：在预测分布只允许小幅改变时，哪一步使 loss 的一阶下降最大？

## 二、KL 的二阶展开产生 Fisher metric

固定输入分布，考虑

$$
D_{KL}(p_\theta\|p_{\theta+p}).
$$

在 regularity 条件下，零阶为 0，一阶因 score 均值为零而消失，二阶为

$$
D_{KL}(p_\theta\|p_{\theta+p})
=\frac12p^TF(\theta)p+O(\|p\|^3).
$$

于是局部 trust-region 子问题

$$
\min_p g^Tp
\quad\text{s.t.}\quad
\frac12p^TFp\le\varepsilon
$$

给出 natural-gradient 方向。

## 三、拉格朗日推导与尺度

假设 $F\succ0$。Lagrangian

$$
\mathcal L(p,\lambda)=g^Tp+\frac\lambda2(p^TFp-2\varepsilon).
$$

驻点满足

$$
g+\lambda Fp=0,\qquad p=-\lambda^{-1}F^{-1}g.
$$

代回边界得

$$
p^*=-\sqrt{\frac{2\varepsilon}{g^TF^{-1}g}}F^{-1}g.
$$

因此 $F^{-1}g$ 是方向；外层 learning rate 或 KL radius 决定长度。只写 `natural_grad = F^{-1}g` 会漏掉 metric norm 与 step acceptance。

若 $F$ 奇异，可用 pseudoinverse $F^\dagger g$，但需满足 $g$ 对 metric nullspace 的兼容性。Null direction 可能表示参数 gauge/symmetry：改变参数却不改变分布。

## 四、坐标变换下为什么方向一致

设同一模型用新坐标 $\theta=\phi(\xi)$，Jacobian $J=\partial\theta/\partial\xi$ 可逆。链式法则给

$$
g_\xi=J^Tg_\theta,\qquad F_\xi=J^TF_\theta J.
$$

于是

$$
F_\xi^{-1}g_\xi
=J^{-1}F_\theta^{-1}g_\theta.
$$

把 $\xi$ 坐标的小位移推回参数空间：

$$
J\Delta\xi=-\eta F_\theta^{-1}g_\theta=\Delta\theta.
$$

这是一阶/infinitesimal 对齐。有限 Euler step 后 $\phi(\xi+\Delta\xi)$ 一般不严格等于 $\phi(\xi)+J\Delta\xi$；若 $J$ 随位置变化，二阶误差出现。

## 五、Bernoulli 的两套坐标手算

用 logit $\theta$ 表示 $p=\sigma(\theta)$，观察 $y=1$。NLL gradient

$$
g_\theta=p-1,\qquad F_\theta=p(1-p).
$$

取 $p=.8$：$g_\theta=-.2,F_\theta=.16$，natural descent direction 为

$$
-F_\theta^{-1}g_\theta=1.25.
$$

若直接用概率 $p$ 作坐标，

$$
g_p=-1/p=-1.25,\qquad F_p=\frac1{p(1-p)}=6.25,
$$

所以 natural direction 为

$$
-F_p^{-1}g_p=.2.
$$

因为 $dp/d\theta=p(1-p)=.16$，logit 位移 1.25 推到概率切空间是 $.16(1.25)=.2$。数值不同，表示的 infinitesimal distribution change 相同。

## 六、哪些改动破坏精确不变性

### 6.1 Euclidean damping

$$
(F+\lambda I)^{-1}g
$$

中的 $I$ 随坐标变换并不按 Fisher tensor 变换，所以固定数值 $\lambda$ 会引入坐标偏好。Damping 提高稳定性，却不是免费的 invariant operation。

### 6.2 结构近似

Diagonal Fisher、block diagonal、K-FAC、低秩/采样估计会丢信息；它们可能保留某些 affine layer reparameterization 性质，但不能直接继承 exact Fisher 的全部结论。

### 6.3 Finite optimizer machinery

Momentum、clipping、Adam grafting、weight decay、parameter groups、finite CG tolerance 与低精度都定义额外坐标结构。真正可复现的声明应是“在哪一类变换、哪个近似和多大误差下近似对齐”。

## 七、Natural gradient、Newton 与 mirror descent

- Newton 用 objective Hessian 的 quadratic model；Hessian 可不定，且其坐标变换含额外二阶项；
- Natural gradient 用 distribution manifold 的 Fisher metric，PSD，但不直接包含任意 task objective 的全部 curvature；
- Mirror descent 用势函数/Bregman divergence 定义非欧几何；当局部 Hessian metric 与 Fisher 对齐时可建立局部联系，但全局 Bregman divergence 不等于任意方向 KL。

三者都可写“inverse metric times gradient”，但 metric 的来源、变换法则和 globalization 不同。

## 八、图：同一分布变化的两套坐标

先看图回答：普通梯度为何随坐标 unit ball 改变，而 Fisher 椭球如何把两套坐标的切向量对齐？

![[00-知识库管理/_assets/figures/training-optimization/fig-natural-gradient-kl-coordinates-v1.svg|900]]

> [!figure] 图 TRN-20　KL trust region、Fisher pullback 与重参数化
> 左侧由 KL 二阶展开推导 $F^{-1}g$；中间用 logit/probability 坐标展示 tangent pushforward；右侧列 finite step、damping、近似 metric 三个断点。来源：依据 [[S-1998-Amari-Natural-Gradient]] 与 [[S-2020-Martens-Natural-Gradient-Curvature]] 独立绘制。

**怎样读图**：先分别计算两套坐标中的普通梯度与 Fisher，再用 Jacobian pushforward 比较表示同一分布变化的切向量；不应要求不同坐标中的参数数字、梯度数字或有限步终点相同。

**图没有证明什么**：图不保证 finite-LR K-FAC/diagonal natural gradient 在任意重参数化下给相同训练轨迹，也不把 Fisher 等同于真实 loss Hessian。

## 九、AI 接口与验收

实现需记录 Fisher 的 label sampling、input measure、damping、solve residual、KL estimate、accepted step、metric quadratic norm与parameter delta。至少用一个可逆 rescaling toy model比较两坐标的 predicted KL 和 function-space change，而非只比较 parameter vector。

## 练习与独立解答

- [[习题 - 自然梯度、KL 局部几何与坐标不变性]]
- [[解答 - 自然梯度、KL 局部几何与坐标不变性]]
