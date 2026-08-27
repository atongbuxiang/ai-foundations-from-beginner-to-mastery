---
type: derivation
status: verified
area: [generative-models, diffusion, inverse-problems, posterior-sampling]
node_id: GEN-67
prerequisites: ["[[条件生成、Bayes 分解与 Classifier Guidance]]", "[[条件概率、全概率与 Bayes 公式]]", "[[时间反演、score 与扩散生成动力学]]"]
related: ["[[Classifier-Free Guidance、尺度与质量多样性前沿]]", "[[扩散 SDE、ODE Solver、步长与 NFE 总账]]"]
sources: ["[[S-2022-Chung-DPS]]", "[[S-2024-Su-10055-信噪比与大图生成下]]"]
exercises: ["[[习题 - 逆问题、约束采样与 Plug-and-Play 控制]]"]
solutions: ["[[解答 - 逆问题、约束采样与 Plug-and-Play 控制]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-inverse-problem-posterior-guidance-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 逆问题、约束采样与 Plug-and-Play 控制

> [!abstract] 一句话结论
> 逆问题不是“每步把图像投影回观测”这么简单。Bayes posterior 需要 prior score 与 noisy-time likelihood score；但观测 $y$ 通常作用在未知干净样本 $x_0$ 上，所以 $p(y\mid x_t)$ 要积分掉 $x_0$。DPS/PnP 方法用 denoised $\hat x_0(x_t)$、近似 likelihood、projection 或 proximal step 代替这个难积分，必须明确它们是近似 sampler，而非自动精确 posterior。

## 一、逆问题合同

令未知信号 $x_0\in\mathbb R^d$，观测

$$
y=\mathcal A(x_0)+\eta,
$$

其中 $\mathcal A$ 可是 mask、blur、downsampling、Fourier magnitude 或非线性成像，$\eta$ 是已知或假设的噪声。目标 posterior

$$
p(x_0\mid y)\propto p_0(x_0)p(y\mid x_0).
$$

若 $\eta\sim\mathcal N(0,\sigma_y^2I)$，

$$
\log p(y\mid x_0)
=-\frac{1}{2\sigma_y^2}\|y-\mathcal A(x_0)\|^2+C.
$$

线性 $\mathcal A(x)=Ax$ 时，

$$
\nabla_{x_0}\log p(y\mid x_0)
=\frac1{\sigma_y^2}A^\top(y-Ax_0).
$$

这里的 $A^\top$ 是 adjoint，不一定是矩阵逆。

## 二、真正需要的是 $p(y\mid x_t)$

扩散采样在 $x_t$ 上运行。Bayes identity 给出

$$
\nabla_{x_t}\log p_t(x_t\mid y)
=s_t(x_t)+\nabla_{x_t}\log p_t(y\mid x_t).
$$

但 measurement model 定义的是 $p(y\mid x_0)$。两者关系为

$$
\boxed{
p_t(y\mid x_t)
=\int p(y\mid x_0)p(x_0\mid x_t)\,dx_0.
}
$$

这个积分是主要困难。把 $x_t$ 直接送进 $A$，等价于假设 measurement 作用在 noisy state，通常改变了问题。

## 三、用 $\hat x_0$ 做 plug-in 近似

Gaussian corruption

$$x_t=\alpha_t x_0+\sigma_t\epsilon$$

下，若 score 精确，Tweedie 型恒等式给 posterior mean

$$
\hat x_0(x_t,t)
=\mathbb E[x_0\mid x_t]
=\frac{x_t+\sigma_t^2s_t(x_t)}{\alpha_t}.
$$

最简单 plug-in likelihood 是

$$
\log p_t(y\mid x_t)
\approx \log p(y\mid \hat x_0(x_t,t)).
$$

对线性 Gaussian measurement，链式法则给

$$
\nabla_{x_t}\log p(y\mid\hat x_0)
=J_{\hat x_0}(x_t)^\top
\frac{A^\top(y-A\hat x_0)}{\sigma_y^2}.
$$

若代码对 $\hat x_0$ `detach`，则 $J_{\hat x_0}$ 被替换，优化对象改变；若保留梯度，要承担 denoiser JVP/VJP 与显存成本。两者都应显式报告。

## 四、一维线性 Gaussian：精确项与 plug-in 差在哪

设

$$
x_0\sim\mathcal N(0,\tau_0^2),
\quad x_t=\alpha x_0+\sigma\epsilon,
\quad y=ax_0+\eta,
\quad \eta\sim\mathcal N(0,\sigma_y^2).
$$

条件 Gaussian 公式给

$$
x_0\mid x_t\sim\mathcal N(kx_t,c),
$$

其中

$$
k=\frac{\alpha\tau_0^2}{\alpha^2\tau_0^2+\sigma^2},
\qquad
c=\frac{\tau_0^2\sigma^2}{\alpha^2\tau_0^2+\sigma^2}.
$$

积分掉 $x_0$：

$$
y\mid x_t\sim\mathcal N(akx_t,\sigma_y^2+a^2c).
$$

所以精确 likelihood score 是

$$
\boxed{
\nabla_{x_t}\log p(y\mid x_t)
=\frac{ak(y-akx_t)}{\sigma_y^2+a^2c}.
}
$$

plug-in 取 $\hat x_0=kx_t$，会使用

$$
\frac{ak(y-akx_t)}{\sigma_y^2},
$$

忽略 posterior uncertainty $a^2c$，因此高噪声时往往把 measurement gradient 放大过头。这是最重要的初学者反例：**posterior mean 插值不是对积分的无偏替代。**

## 五、四类控制算法不要混写

### 5.1 Likelihood guidance

把近似 $\nabla_{x_t}\log p(y\mid x_t)$ 加入 score/drift。它最接近 Bayes 形式，但依赖 likelihood approximation 与 scale。

### 5.2 Hard projection

在每步或末端做

$$x\leftarrow\Pi_{\{z:\mathcal A(z)=y\}}(x).$$

适合近无噪声线性约束，但对 noisy observations 会过拟合噪声；nonconvex set 的 projection 可能多值或难算。

### 5.3 Proximal/data-consistency step

对

$$g(x)=\frac1{2\sigma_y^2}\|y-Ax\|^2$$

做

$$
x\leftarrow\operatorname{prox}_{\lambda g}(z)
=\arg\min_x\left\{g(x)+\frac1{2\lambda}\|x-z\|^2\right\}.
$$

它在 prior proposal 与 measurement fit 间软权衡，但与某个 posterior sampler 等价需要额外条件。

### 5.4 Plug-and-Play denoising

把 diffusion denoiser 当 prior operator 嵌入迭代算法。除非 denoiser 真是某个显式 prior 的 proximal/score 且算法条件满足，fixed point 不自动等于 Bayesian posterior sample。

## 六、DPS 的课程定位

[[S-2022-Chung-DPS]] 面向 noisy linear/nonlinear inverse problems，把 diffusion sampling 与基于 $\hat x_0$ 的 measurement gradient 组合。课程采用其“posterior score = prior + likelihood correction”的算法骨架，但把以下内容标为近似：

- $p(y\mid x_t)$ 的 plug-in；
- learned $\hat x_0$ 与真实 conditional mean 的差；
- gradient normalization/step scale；
- finite reverse solver；
- 非线性 operator 的 Jacobian 与局部几何。

重建 PSNR 高只能说明 point estimate 接近某个 reference；posterior sampling 还需 calibration、coverage 和 sample diversity。

## 七、实验协议

至少报告：

1. forward operator $A/\mathcal A$、boundary condition 与 adjoint test；
2. measurement noise 分布和真实/假设 $\sigma_y$；
3. diffusion prior 训练域；
4. $\hat x_0$ 公式、是否 clipping/detach；
5. correction scale 随 $t$ 的 schedule；
6. sampler、NFE、random seed 与 initial noise 配对；
7. data consistency、perceptual fidelity、posterior coverage/calibration；
8. 多个 posterior samples，而非只展示最佳一张；
9. misspecified operator/noise 的鲁棒性；
10. 与 MAP、传统正则化和无 guidance prior 的基线。

## 八、图：从 measurement 到 noisy-time posterior

先回答：观测箭头为什么指向 $x_0$ 而不是 $x_t$？中间积分被哪种近似替换？hard projection 与 likelihood guidance 的目标相同吗？

![[00-知识库管理/_assets/figures/generative-models/fig-inverse-problem-posterior-guidance-v1.svg|900]]

> [!figure] 图 50.9-03　逆问题 posterior guidance 的三层近似
> 图从 $p(y\mid x_0)$ 经 latent integral 到 $p(y\mid x_t)$，再分出 plug-in、projection 与 proximal/PnP 路线。来源：据 DPS 原论文与本节 Gaussian 推导独立绘制。

**怎样读图**：先沿概率路径看积分，再沿算法路径看 $\hat x_0$、Jacobian 和 correction scale；最后把 reconstruction metric 与 posterior metric 分开。

**图没有证明什么**：图不证明 plug-in gradient 无偏，不证明 hard consistency 适合 noisy data，也不证明某个 fixed point 是精确 posterior sample。

## 九、学习出口

- 能写出 $p(y\mid x_t)$ 的积分，而非把 $x_t$ 当 $x_0$；
- 能手推一维 Gaussian 的精确 likelihood score；
- 能解释 detach 为什么改变梯度对象；
- 能区分 likelihood guidance、projection、prox 与 PnP；
- [[习题 - 逆问题、约束采样与 Plug-and-Play 控制]]
- [[解答 - 逆问题、约束采样与 Plug-and-Play 控制]]
