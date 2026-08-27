---
type: derivation
status: verified
area: [training, optimization, adam]
node_id: TRN-11
aliases: [Adam 状态机, Adam 偏差修正]
prerequisites: ["[[RMSProp、滑动二阶矩与非平稳尺度]]", "[[Momentum、EMA、偏差修正与框架约定]]", "[[期望、方差与矩]]"]
related: ["[[Adam 的 Epsilon、数值稳定与实现分歧]]", "[[Adam 收敛反例、AMSGrad 与条件化保证]]", "[[梯度噪声协方差、Noise Scale 与 SDE 近似]]"]
sources: ["[[S-2015-Kingma-Ba-Adam]]", "[[S-2024-Su-10588-Hessian近似与自适应学习率]]", "[[S-2025-Su-11267-Adam-Update-RMS]]", "[[S-2026-Framework-Adaptive-Optimizer-Semantics]]"]
exercises: ["[[习题 - Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"]
solutions: ["[[解答 - Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-adam-state-bias-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Adam 的一阶二阶矩、偏差修正与逐坐标步长

> [!abstract] 一句话结论
> Adam 同时保存 gradient mean 的 EMA 与 gradient square 的 EMA，用 bias correction 消除零初始化对这两个矩估计的早期缩小，再取“平滑方向 ÷ 局部 RMS”。修正后的两个矩可各自无偏于平稳矩，但它们的比值并不因此无偏；完整算法还必须声明 step index、epsilon、decay 和 skip 语义。

## 一、完整抽象更新

令 optimizer step 从 $t=1$ 开始，$m_0=v_0=0$。经典 Adam 写成

$$
\begin{aligned}
g_t&=\nabla_\theta L_t(\theta_{t-1}),\\
m_t&=\beta_1m_{t-1}+(1-\beta_1)g_t,\\
v_t&=\beta_2v_{t-1}+(1-\beta_2)g_t^2,\\
\widehat m_t&=\frac{m_t}{1-\beta_1^t},\\
\widehat v_t&=\frac{v_t}{1-\beta_2^t},\\
u_t&=\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon},\\
\theta_t&=\theta_{t-1}-\eta_tu_t.
\end{aligned}
$$

所有平方、根号和除法逐坐标进行。$v_t$ 是 raw second moment，不是 variance：

$$
\mathbb E[g^2]=\operatorname{Var}(g)+\mathbb E[g]^2.
$$

## 二、bias correction 从哪里来

若 $g_t$ 来自平稳序列且 $\mathbb E[g_t]=\mu$，展开一阶状态：

$$
m_t=(1-\beta_1)\sum_{s=1}^{t}\beta_1^{t-s}g_s.
$$

因此

$$
\mathbb E[m_t]=(1-\beta_1^t)\mu.
$$

零初始化让权重和小于 1；除以 $1-\beta_1^t$ 后

$$
\mathbb E[\widehat m_t]=\mu.
$$

同理，若 $\mathbb E[g_t^2]=\nu$：

$$
\mathbb E[v_t]=(1-\beta_2^t)\nu,
\qquad
\mathbb E[\widehat v_t]=\nu.
$$

> [!warning] 修正矩，不修正比值
> 一般有 $\mathbb E[\widehat m_t/\sqrt{\widehat v_t}]\ne \mathbb E[\widehat m_t]/\sqrt{\mathbb E[\widehat v_t]}$。bias correction 不等于 Adam direction 的无偏性，更不等于参数更新对 population gradient 无偏。

## 三、第一步为什么近似 sign update

第一步有

$$
m_1=(1-\beta_1)g_1,
\qquad
v_1=(1-\beta_2)g_1^2.
$$

修正后

$$
\widehat m_1=g_1,
\qquad
\widehat v_1=g_1^2,
$$

所以

$$
u_1=\frac{g_1}{|g_1|+\epsilon}.
$$

当 $|g_1|\gg\epsilon$，非零坐标近似 $\operatorname{sign}(g_1)$；当 $|g_1|\ll\epsilon$，则近似 $g_1/\epsilon$。这只是第一步和局部 regime，不代表整个 Adam 永远等于 SignSGD，因为后续 $m_t$ 与 $v_t$ 聚合不同历史。

## 四、两步完整手算

取单坐标 $g_1=2,g_2=0$，$\beta_1=0.5,\beta_2=0.75,\epsilon=0$。

第一步：

$$
m_1=1,\quad v_1=1,\quad
\widehat m_1=2,\quad\widehat v_1=4,\quad u_1=1.
$$

第二步：

$$
m_2=0.5,\qquad v_2=0.75.
$$

偏差修正分母为

$$
1-\beta_1^2=0.75,
\qquad
1-\beta_2^2=0.4375=\frac7{16}.
$$

所以

$$
\widehat m_2=\frac23,
\qquad
\widehat v_2=\frac{12}{7},
\qquad
u_2=\frac{2/3}{\sqrt{12/7}}\approx0.509.
$$

即使当前 gradient 为零，momentum 仍产生参数更新；与此同时 second moment 也在衰减。只看当前 gradient 无法恢复 Adam step。

## 五、两个 EMA 的时标为什么通常不同

$\beta_1$ 控制方向平均，$\beta_2$ 控制尺度平均。常见设置让 $\beta_2>\beta_1$，意味着 denominator 比 numerator 记得更久：

$$
\tau_m\approx\frac1{1-\beta_1},
\qquad
\tau_v\approx\frac1{1-\beta_2}
$$

只是接近 1 时的 e-folding 近似。长 $v$ 时标令尺度平滑，但可能在 regime change 时滞后；短 $m$ 时标让方向更快跟踪，却保留更多噪声。两个超参数不是独立的“平滑旋钮”，它们通过比值共同决定 $u_t$。

## 六、逐坐标学习率应怎样定义

可以把更新写成

$$
\Delta\theta_{t,i}
=-\alpha_{t,i}\widehat m_{t,i},
\qquad
\alpha_{t,i}=\frac{\eta_t}{\sqrt{\widehat v_{t,i}}+\epsilon}.
$$

$\alpha_{t,i}$ 是对平滑梯度 $\widehat m_{t,i}$ 的逐坐标系数；而

$$
\frac{\Delta\theta_{t,i}}{g_{t,i}}
$$

在 momentum 存在时并不是同一个量，甚至当前 $g_{t,i}=0$ 时也不可定义。论文里说 effective learning rate 前，应明确相对哪个 direction。

## 七、Adam 保存的不是 Hessian

[[S-2024-Su-10588-Hessian近似与自适应学习率]]给出一个有用但条件很强的解释：若在局部最优附近

$$
g\approx H(\theta-\theta^*)
$$

且参数偏移协方差近似各向同性，则

$$
\mathbb E[gg^\top]\approx\sigma^2HH^\top.
$$

这时 gradient square 的长期平均可能携带 curvature scale 信息。但 Adam 只保存坐标对角、沿实际随机轨迹的 raw moments；它没有 Hessian 的 off-diagonal/eigenvectors，也不处理负曲率。正确说法是“在额外假设下可作尺度 proxy”，不是“Adam 是近似 Newton”。

## 八、完整实现合同

一个可复现 Adam 配置至少包含：

| 对象 | 必须记录 |
|---|---|
| 状态 | $m,v,t$；AMSGrad 还含 $v^{max}$ |
| 超参 | LR schedule、$\beta_1,\beta_2,\epsilon$ |
| epsilon | 根号内/外、修正前/后、单位 |
| decay | coupled L2 还是 decoupled AdamW；参数组 |
| step | 从 0/1 计，何时递增，overflow/empty grad 是否跳过 |
| 执行 | dtype、foreach/fused、capturable、分布式归约 |

当前 PyTorch Adam 还允许 `decoupled_weight_decay=True`，不能再仅凭类名 `Adam` 推断 decay 语义。

## 九、图：Adam 一步里的五本小账

先看图回答：bias correction 修正的是哪两个状态？epsilon 和 learning rate 分别在哪一层？

![[00-知识库管理/_assets/figures/training-optimization/fig-adam-state-bias-ledger-v1.svg|900]]

> [!figure] 图 TRN-11　Adam 的时序、矩状态与偏差修正
> 图从 raw gradient 依次进入 $m_t,v_t$、bias correction、normalized direction 和 parameter update；下方用第一步/稳态对照说明“矩无偏”不等于“比值无偏”。来源：依据 [[S-2015-Kingma-Ba-Adam]] 与当前框架文档独立绘制。

**怎样读图**：沿时间顺序逐框核对输入和状态；遇到 checkpoint 时，从 $m,v,t$ 三件套恢复，而不是只保存参数。

**图没有证明什么**：图不证明 Adam 的 direction 是 population gradient 的无偏估计，也不提供非凸全局收敛保证。

## 十、本节回顾

- Adam 的 numerator 与 denominator 记忆不同历史；
- bias correction 恢复平稳矩的期望，不修正 ratio；
- 第一步近似 soft-sign，但长期不等于 SignSGD；
- $v_t$ 是 raw second moment，不是 variance 或 Hessian；
- 下一节 [[Adam 的 Epsilon、数值稳定与实现分歧]]专门审计小梯度区和框架公式。

## 练习与独立解答

- [[习题 - Adam 的一阶二阶矩、偏差修正与逐坐标步长]]
- [[解答 - Adam 的一阶二阶矩、偏差修正与逐坐标步长]]
- 卷级复现：[[实验 - 自适应优化器状态、尺度与反例数值审计]]
