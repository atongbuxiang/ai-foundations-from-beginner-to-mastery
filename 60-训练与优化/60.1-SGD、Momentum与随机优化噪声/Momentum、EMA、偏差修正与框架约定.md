---
type: derivation
status: verified
area: [training, optimization, momentum]
node_id: TRN-04
aliases: [动量约定翻译, Momentum Convention]
prerequisites: ["[[SGD、采样顺序与梯度累积的等价边界]]", "[[加速梯度、动量与下界]]"]
related: ["[[Nesterov、Lookahead 与动量形式的等价边界]]", "[[二次模型的学习率—动量稳定域与阻尼]]", "[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"]
sources: ["[[S-1964-Polyak-Heavy-Ball]]", "[[S-2013-Sutskever-Momentum]]", "[[S-2026-PyTorch-SGD-Semantics]]", "[[S-2018-Su-5655-SGD到动量加速]]"]
exercises: ["[[习题 - Momentum、EMA、偏差修正与框架约定]]"]
solutions: ["[[解答 - Momentum、EMA、偏差修正与框架约定]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-momentum-convention-translation-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Momentum、EMA、偏差修正与框架约定

> [!abstract] 一句话结论
> “momentum=0.9”不是完整算法：有人保存未归一化 gradient buffer，有人保存含 learning rate 的 parameter velocity，也有人保存 gradient EMA。常 learning rate 下它们可通过尺度变换互译；学习率变化、初始化、dampening 与 bias correction 会让早期和后续轨迹分叉。

## 一、为什么要保存过去梯度

若狭长二次谷的一个方向曲率大、另一个方向曲率小，plain GD 会在陡峭方向反复换号，在平缓方向进展慢。Momentum 用状态累积方向一致的 gradient，并让交替方向部分抵消。

> [!intuition] 直觉对应哪个公式
> “惯性”对应递推中的 $\mu b_{t-1}$；“阻尼/遗忘”对应 $0\le\mu<1$；“当前力”对应 $g_t$。物理比喻只解释符号角色，稳定性仍由离散特征根决定。

## 二、三种常见 convention

令 $g_t=\nabla F_t(\theta_t)$。

### 2.1 Gradient-buffer convention

$$b_t=\mu b_{t-1}+g_t,
\qquad \theta_{t+1}=\theta_t-\eta b_t.$$

### 2.2 Parameter-velocity convention

$$v_t=\mu v_{t-1}-\eta g_t,
\qquad \theta_{t+1}=\theta_t+v_t.$$

若 $\eta$ 为常数且初始状态满足 $v_{-1}=-\eta b_{-1}$，则逐步有

$$\boxed{v_t=-\eta b_t},$$

所以两种写法产生同一参数序列。

### 2.3 Gradient-EMA convention

$$m_t=\mu m_{t-1}+(1-\mu)g_t,
\qquad \theta_{t+1}=\theta_t-\alpha m_t.$$

零初始化且同一 gradient sequence 下，$m_t=(1-\mu)b_t$。要匹配 buffer 版本，需 $\alpha=\eta/(1-\mu)$。如果沿用同一个数值 learning rate，EMA 版本的 steady-state update 小约 $1-\mu$ 倍。

## 三、展开递推：Momentum 是怎样加权历史的

若 $b_{-1}=0$，递推展开为

$$
b_t=\sum_{k=0}^t\mu^{t-k}g_k.
$$

所以最近 gradient 权重 1，向过去按几何级数衰减。若 gradient 恒为 $g$，则

$$b_t=\frac{1-\mu^{t+1}}{1-\mu}g,$$

稳态极限为 $g/(1-\mu)$。这解释了为何 buffer convention 的有效步长会被放大约 $1/(1-\mu)$；也解释了不能只比较名义 LR。

EMA 的权重和为 $1-\mu^{t+1}<1$，零初始化导致早期向零偏。bias-corrected EMA

$$\widehat m_t=\frac{m_t}{1-\mu^{t+1}}$$

在恒定 gradient 下立刻恢复 $g$。但把 $\widehat m_t$ 用于更新会真实改变早期轨迹，它不是只影响日志的“无害修正”。

## 四、变化 learning rate 时，简单互译失效

buffer 版本若每步用 $\eta_t$，令 $v_t=-\eta_t b_t$，则

$$
v_t
=-\eta_t(\mu b_{t-1}+g_t)
=\mu\frac{\eta_t}{\eta_{t-1}}v_{t-1}-\eta_tg_t.
$$

这与朴素 velocity 递推 $v_t=\mu v_{t-1}-\eta_tg_t$ 只有在 $\eta_t=\eta_{t-1}$ 时相同。LR decay 放在 buffer 外还是 velocity 内，会改变历史梯度的重标度。

> [!warning] checkpoint 不能只保存“momentum tensor”
> 若从一种 convention 切到另一种，必须连同当前 LR、buffer 的定义、step index、dampening 和初始化一起翻译；否则相同 tensor 数值并不代表相同物理/算法状态。

## 五、PyTorch 当前 SGD 合同

根据 [[S-2026-PyTorch-SGD-Semantics]]，PyTorch 在 momentum 非零时使用近似以下顺序：

$$
\begin{aligned}
g_t&\leftarrow g_t+\lambda\theta_t\quad\text{（若 coupled weight decay）},\\
b_t&=\begin{cases}
g_t,&\text{首个 step},\\
\mu b_{t-1}+(1-\tau)g_t,&\text{之后},
\end{cases}\\
\theta_{t+1}&=\theta_t-\eta_t b_t
\quad\text{（非 Nesterov）}.
\end{aligned}
$$

$\tau$ 是 dampening。首个 buffer 直接设为 $g_t$，所以 dampening 不作用于第一步；这和“buffer 从零并统一递推”不总相同。

## 六、两步手算与 convention 翻译

取 $g_0=2,g_1=-1$，$\mu=0.9,\eta=0.1$，零初始 buffer。

Gradient buffer：

$$b_0=2,\quad\Delta\theta_0=-0.2;$$
$$b_1=0.9(2)-1=0.8,\quad\Delta\theta_1=-0.08.$$

Velocity：$v_0=-0.2$，$v_1=0.9(-0.2)-0.1(-1)=-0.08$，与 $v_t=-0.1b_t$ 一致。

EMA：$m_0=0.2,m_1=0.9(0.2)+0.1(-1)=0.08$。若使用 $\alpha=1=\eta/(1-\mu)$，updates 仍是 $-0.2,-0.08$；若误用 $\alpha=0.1$，则缩小十倍。

## 七、频率与噪声视角

对给定 gradient sequence，EMA 是一阶低通滤波器。$z$ 域形式为

$$M(z)=\frac{1-\mu}{1-\mu z^{-1}}G(z).$$

它抑制快速换号的高频分量，但也产生 phase lag；当真实 gradient 方向快速变化时，“平滑”可能意味着追随过时方向。Momentum 不是无条件降噪器，更不是对所有 curvature 都加速。

## 八、图：三个同名 Momentum 怎样互译

先看图回答：哪个状态保存 gradient，哪个状态保存 parameter displacement，LR 在递推内部还是外部？

![[00-知识库管理/_assets/figures/training-optimization/fig-momentum-convention-translation-v1.svg|900]]

> [!figure] 图 TRN-04　Gradient buffer、velocity 与 EMA 的尺度字典
> 三条更新路径用等式连接常 LR 下的状态；琥珀断点标出变化 LR、bias correction、dampening 与首步初始化。来源：据 Polyak、Sutskever 等和 PyTorch 当前文档重新组织并独立绘制。

**怎样读图**：先在每个框中找 state 的单位，再沿绿色等价箭头检查需要的缩放。遇到断点时，不再沿用等价式，而应逐步模拟更新。

**图没有证明什么**：图只给 convention translation，不证明 momentum 在非凸随机目标上一定更快，也不把 gradient filtering 等同于 generalization improvement。

## 九、科学空间研读框

[[S-2018-Su-5655-SGD到动量加速]]用动力学语言解释惯性与阻尼，适合建立整体直觉。本节点补上三件容易被直觉省略的事：状态单位、框架初始化与变化 LR 下的非等价。[[S-1964-Polyak-Heavy-Ball]]承担 deterministic quadratic 的正式历史来源，[[S-2013-Sutskever-Momentum]]承担深度学习变体与实证背景。

## 十、AI 中的调用与边界

模型中每个 parameter group 都可能有独立 $\eta,\mu,\lambda$；sparse embedding、normalization parameter 和 bias 还可能使用不同 decay。分布式训练中 buffer 在 all-reduced gradient 上更新还是 rank-local 更新，决定它是否代表全局 gradient history。

> [!research] 前沿地位
> Momentum 的线性系统理论在固定二次目标上完整清楚；深网中 Hessian 随轨迹变化、noise 非平稳、normalization 带尺度对称，经典最优参数不能直接迁移。经验上 momentum 很重要，但“滤掉 noise”“跨过局部极小”“模拟质量点”分别是不同解释模型。

## 十一、本节回顾

- buffer、velocity、EMA 的单位和 LR placement 不同；
- 常 LR 下可尺度互译，变化 LR 时一般不可；
- bias correction 改变早期更新，不只是估计展示；
- PyTorch 首个 buffer、dampening 与 Nesterov 顺序必须按文档核对；
- 下一节 [[Nesterov、Lookahead 与动量形式的等价边界]] 将区分“梯度在哪里计算”和“参数变量如何重命名”。

## 练习与独立解答

- [[习题 - Momentum、EMA、偏差修正与框架约定]]
- [[解答 - Momentum、EMA、偏差修正与框架约定]]
