---
type: derivation
status: verified
area: [training, optimization, stochastic-processes]
node_id: TRN-07
aliases: [Gradient Noise Scale, SGD Diffusion Approximation]
prerequisites: ["[[Mini-batch 梯度、平均求和与有效 Batch]]", "[[Itô 引理与随机微分方程]]", "[[二次模型的学习率—动量稳定域与阻尼]]"]
related: ["[[Critical Batch、隐式偏置与 SGD 证据地图]]", "[[Fokker-Planck 方程与概率流 ODE]]", "[[学习率、局部损失变化与相对更新尺度]]"]
sources: ["[[S-2017-Mandt-SGD-SDE]]", "[[S-2018-McCandlish-Noise-Scale]]", "[[S-2025-Su-11260-学习率与Batch-Size均衡]]", "[[S-2025-Su-11280-学习率与Batch-Size平均场]]"]
exercises: ["[[习题 - 梯度噪声协方差、Noise Scale 与 SDE 近似]]"]
solutions: ["[[解答 - 梯度噪声协方差、Noise Scale 与 SDE 近似]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-sgd-noise-sde-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 梯度噪声协方差、Noise Scale 与 SDE 近似

> [!abstract] 一句话结论
> SGD noise 是向量随机误差，关键对象是条件 covariance $C(\theta)$ 而不是一个“噪声大小”。对 iid batch mean，离散 update covariance 为 $\eta^2C/B$；在连续时间 $t=k\eta$ 下，它与扩散振幅 $\sqrt{\eta/B}C^{1/2}$ 的 SDE 做局部二阶矩匹配。这个 SDE 是小步长、弱意义近似，不是逐路径恒等式。

## 一、把 gradient 拆成信号与噪声

固定历史 $\mathcal F_t$ 与当前参数 $\theta_t$，写

$$
\widehat G_{B,t}=G(\theta_t)+\xi_t,
\qquad \mathbb E[\xi_t\mid\mathcal F_t]=0.
$$

若单样本 gradient covariance 为 $C(\theta_t)$ 且 batch iid，则

$$\operatorname{Cov}(\xi_t\mid\mathcal F_t)=\frac{C(\theta_t)}B.$$

SGD update

$$\theta_{t+1}=\theta_t-\eta G(\theta_t)-\eta\xi_t$$

的随机增量 covariance 是

$$
\boxed{\operatorname{Cov}(\Delta\theta_t^{noise}\mid\mathcal F_t)
=\frac{\eta^2}{B}C(\theta_t).}
$$

增大 $B$ 与减小 $\eta$ 都降低 update noise，但对 drift 的影响不同：drift 大小随 $\eta$，noise standard deviation 随 $\eta/\sqrt B$。

## 二、Noise Scale 的一个透明定义

取 Euclidean squared norm，利用

$$
\mathbb E\|\widehat G_B\|^2
=\|G\|^2+\frac{\operatorname{tr}C}{B}.
$$

定义 simple gradient noise scale

$$
\boxed{\mathcal B_{simple}(\theta)
=\frac{\operatorname{tr}C(\theta)}{\|G(\theta)\|^2}.}
$$

当 $B=\mathcal B_{simple}$ 时，batch gradient 的 noise squared norm 与 signal squared norm 在期望上相当。这是一个有解释力的尺度，不是唯一合法定义；preconditioner、parameterization 和选择的 norm 都会改变它。

> [!warning] 在 stationary point 附近会变得难估
> 当 $\|G\|$ 很小时，比值可急剧增大，分母估计偏差也严重。应报告 numerator、denominator、估计窗口和置信不确定性，而不是只画 noise-scale ratio。

## 三、从离散 SGD 到 SDE：逐步匹配尺度

令连续时间 $s=t\eta$，考虑 SDE

$$
d\Theta_s=-G(\Theta_s)ds
+\sqrt{\frac\eta B}\,C(\Theta_s)^{1/2}dW_s.
$$

Euler–Maruyama 用时间步 $\Delta s=\eta$ 离散：

$$
\Delta\Theta
=-\eta G(\Theta)
+\sqrt{\frac\eta B}C^{1/2}\Delta W,
$$

其中 $\Delta W\sim\mathcal N(0,\eta I)$。所以 diffusion increment covariance 是

$$
\frac\eta B C\cdot\eta
=\frac{\eta^2}B C,
$$

正好匹配离散 SGD 的条件二阶矩。

> [!warning] 两种常见写错
> 若时间取 $s=t\eta$，diffusion coefficient 是 $\sqrt{\eta/B}$，不是 $\eta/B$；若时间取 optimizer-step $t$ 而不重标度，drift/diffusion 写法会不同。先声明时间单位，再比较“温度”。

## 四、局部二次下的 Ornstein–Uhlenbeck 模型

在局部最优点 $\theta^*$ 附近令 $u=\theta-\theta^*$，近似 $G(\theta)\approx Hu$、$C(\theta)\approx C_*$：

$$du=-Hu\,ds+\sqrt{\frac\eta B}C_*^{1/2}dW_s.$$

若 $H$ stable，stationary covariance $\Sigma$ 满足 continuous Lyapunov equation

$$
\boxed{H\Sigma+\Sigma H^T=\frac\eta B C_*.}
$$

若 $H$ 与 $C_*$ 可在同一正交基对角化，则第 $i$ 个方向

$$\Sigma_i=\frac{\eta c_i}{2B\lambda_i}.$$

同样 noise covariance 在低曲率方向产生更宽 stationary spread。这是“平坦方向探索”的局部数学版本，但依赖 OU 条件。

## 五、为什么 SGD 一般不等于 Bayesian posterior sampling

Bayesian posterior 的局部 covariance 通常与 inverse Hessian 和 dataset size 有关；SGD stationary covariance 还取决于 $C_*$、$\eta/B$、preconditioner 和 discretization。只有在额外矩阵关系与调参条件下才可近似匹配。

[[S-2017-Mandt-SGD-SDE]]的贡献正是在明确近似条件下讨论这种匹配；课程不把论文标题缩写成“SGD 自动做 Bayes”。

## 六、非 Gaussian、相关与有偏噪声

SDE 近似可能在以下情形失败或需要修正：

- random reshuffling 产生跨 step 负相关；
- data augmentation、curriculum 或 replay buffer 使分布随时间变化；
- heavy-tail gradient 使二阶矩不足以描述跳跃；
- BatchNorm 让 estimator 不再是固定 per-example gradients 的平均；
- clipping 引入 bias；
- momentum 把 state 扩为 position–velocity，并改变 colored-noise spectrum；
- finite $\eta$ 太大，局部 diffusion/weak approximation 不准确。

如果 noise 有非零自相关 $\Gamma_k=\operatorname{Cov}(\xi_t,\xi_{t+k})$，长期扩散强度涉及

$$\Gamma_0+\sum_{k\ge1}(\Gamma_k+\Gamma_k^T),$$

而不只是单步 $C/B$。

## 七、最小手算

一维 objective $F(\theta)=\tfrac12\lambda\theta^2$，单样本 noise variance $c$。取 $\lambda=2,c=8,\eta=0.01,B=4$。

SDE diffusion coefficient

$$\sqrt{\eta c/B}=\sqrt{0.02}\approx0.1414.$$

stationary variance

$$\Sigma=\frac{\eta c}{2B\lambda}
=\frac{0.08}{16}=0.005.$$

若把 $B$ 翻倍而其他条件近似不变，局部 variance 减半；但真实训练中 $C$ 和访问的区域也可能随 batch 改变。

## 八、图：离散 covariance 怎样变成扩散系数

先看图回答：$C/B$、$\eta^2C/B$ 与 $\sqrt{\eta/B}C^{1/2}$ 分别属于 gradient、一步 update 还是连续 SDE？

![[00-知识库管理/_assets/figures/training-optimization/fig-sgd-noise-sde-ledger-v1.svg|900]]

> [!figure] 图 TRN-07　SGD noise 的 estimator—update—SDE—OU 四层总账
> 图按对象单位排列 covariance 缩放，并在右侧列出 diffusion 近似的条件门。来源：据 Mandt 等和 batch covariance 恒等式独立重绘。

**怎样读图**：从 batch gradient 开始，每跨一层都检查乘了一个 $\eta$ 还是换了时间单位；最后的 OU 椭圆只描述局部 stationary covariance。

**图没有证明什么**：图不证明 gradient noise 是 Gaussian、不证明全程存在 stationary distribution，也不证明更大的 stationary spread 会改善 validation。

## 九、科学空间研读框

[[S-2025-Su-11260-学习率与Batch-Size均衡]]和[[S-2025-Su-11280-学习率与Batch-Size平均场]]提供 learning-rate–batch coupling 的连续视角。本节点用明确时间缩放和 covariance 单位补严：离散一步、连续单位时间与最终泛化不能跨层跳跃。

## 十、本节回顾

- gradient noise 是 covariance geometry，不只是标量 variance；
- iid batch mean 给 $C/B$，update 给 $\eta^2C/B$；
- 在 $s=t\eta$ 下，SDE diffusion coefficient 是 $\sqrt{\eta/B}C^{1/2}$；
- OU stationary covariance 解 Lyapunov equation；
- SDE 与 Bayesian 解释都需要强条件；
- 下一节 [[Critical Batch、隐式偏置与 SGD 证据地图]] 将把 noise scale 与训练效率、泛化证据分开。

## 练习与独立解答

- [[习题 - 梯度噪声协方差、Noise Scale 与 SDE 近似]]
- [[解答 - 梯度噪声协方差、Noise Scale 与 SDE 近似]]
