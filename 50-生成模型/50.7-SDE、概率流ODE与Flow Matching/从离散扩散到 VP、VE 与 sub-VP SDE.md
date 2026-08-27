---
type: derivation
status: verified
area: [generative-models, diffusion, sde]
node_id: GEN-49
prerequisites: ["[[DDPM 前向 Markov 加噪与闭式边缘]]", "[[随机过程、Brownian 运动与二次变差]]", "[[Itô 引理与随机微分方程]]"]
related: ["[[Reverse-time SDE、时间反演与 Score Drift]]", "[[Probability-flow ODE 与共享边缘分布]]", "[[扩散简化损失、时间加权、Schedule 与 SNR]]"]
sources: ["[[S-2022-Su-9209-扩散模型SDE篇]]", "[[S-2021-Song-Score-SDE]]", "[[S-2020-Ho-DDPM]]"]
exercises: ["[[习题 - 从离散扩散到 VP、VE 与 sub-VP SDE]]"]
solutions: ["[[解答 - 从离散扩散到 VP、VE 与 sub-VP SDE]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-vp-ve-subvp-sde-ledger-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 从离散扩散到 VP、VE 与 sub-VP SDE

> [!abstract] 一句话结论
> 连续时间扩散不是把离散下标 $t$ 换成实数那么简单；关键是令一步 drift 为 $O(\Delta t)$、噪声标准差为 $O(\sqrt{\Delta t})$。DDPM 的小步极限给出 variance-preserving（VP）SDE；只增大噪声尺度而不衰减信号得到 variance-exploding（VE）SDE；sub-VP 保留 VP 的均值衰减但选择更小的瞬时扩散，使条件方差变为 $(1-e^{-B(t)})^2$。

## 一、为什么要从离散过程走向连续时间

在 [[DDPM 前向 Markov 加噪与闭式边缘]] 中，forward chain 是

$$
x_k=\sqrt{1-\beta_k}\,x_{k-1}+\sqrt{\beta_k}\,\epsilon_k.
$$

它已经足以训练和采样。引入连续时间不是为了把模型说得更“高级”，而是为了得到三个新能力：

1. 用一个 SDE 统一不同离散步数和 schedule；
2. 利用 Fokker–Planck、时间反演与 ODE 理论构造新 sampler；
3. 把 score diffusion、probability-flow ODE 与 Flow Matching 放进同一密度演化语言。

但连续模型只描述理想极限；真正程序仍要离散化，因此不能删除 timestep、solver 与 NFE 这本账。

## 二、局部缩放：为什么噪声是 $\sqrt{\Delta t}$

把连续时间区间分成小步 $h=\Delta t$，令离散 variance schedule 写成

$$\beta_k=\beta(t_k)h+o(h).$$

对平方根作一阶展开：

$$
\sqrt{1-\beta(t)h}
=1-\frac12\beta(t)h+o(h).
$$

因此一步 DDPM 变成

$$
X_{t+h}-X_t
=-\frac12\beta(t)X_t h
+\sqrt{\beta(t)}\sqrt h\,\epsilon_t
+o(h).
$$

条件均值和协方差分别是

$$
\mathbb E[\Delta X_t\mid X_t=x]
=-\frac12\beta(t)x h+o(h),
$$

$$
\operatorname{Cov}(\Delta X_t\mid X_t=x)
=\beta(t)hI+o(h).
$$

这正对应 Itô SDE

$$
\boxed{dX_t=-\frac12\beta(t)X_tdt+\sqrt{\beta(t)}dW_t.}
$$

若把噪声误写成 $g(t)dt\,\epsilon$，累计方差约为 $T/h$ 个 $O(h^2)$ 之和，即 $O(h)\to0$；随机性会在极限中消失。Brownian 增量必须满足 $\Delta W_t\sim N(0,hI)$，所以量级是 $\sqrt h$。

## 三、线性 SDE 的统一闭式

三种扩散都可先放进线性各向同性模板

$$
dX_t=a(t)X_tdt+g(t)dW_t.
$$

定义积分因子

$$
m(t)=\exp\left(\int_0^t a(s)ds\right).
$$

由 Itô 乘积法则，$Y_t=X_t/m(t)$ 满足

$$
dY_t=\frac{g(t)}{m(t)}dW_t.
$$

积分后得到

$$
X_t=m(t)X_0+m(t)\int_0^t\frac{g(s)}{m(s)}dW_s.
$$

给定 $X_0=x_0$，随机积分是 Gaussian，故

$$
\boxed{X_t\mid X_0=x_0\sim
N\left(m(t)x_0,
m(t)^2\int_0^t\frac{g(s)^2}{m(s)^2}ds\ I\right).}
$$

这个公式是本节的总检查器：任何声称的 VP/VE/sub-VP 边缘，都应同时满足均值 ODE 和方差 ODE

$$M'(t)=a(t)M(t),\qquad
V'(t)=2a(t)V(t)+g(t)^2,\qquad V(0)=0.$$

## 四、VP SDE：总方差趋向稳定

令

$$B(t)=\int_0^t\beta(s)ds,$$

VP SDE 为

$$
\boxed{dX_t=-\frac12\beta(t)X_tdt+\sqrt{\beta(t)}dW_t.}
$$

此时 $a(t)=-\beta(t)/2$，所以 signal coefficient 为

$$m_{VP}(t)=e^{-B(t)/2}.$$

方差满足 $V'=-\beta V+\beta$。直接验算

$$V_{VP}(t)=1-e^{-B(t)}$$

确实有 $V'_{VP}=\beta e^{-B}=\beta(1-V_{VP})$。因此

$$
\boxed{X_t=e^{-B(t)/2}X_0+\sqrt{1-e^{-B(t)}}\,\epsilon,
\quad\epsilon\sim N(0,I).}
$$

若数据每维方差已标准化为 1，则

$$\operatorname{Var}(X_t)=e^{-B(t)}\operatorname{Var}(X_0)+1-e^{-B(t)}=1,$$

这解释了 variance-preserving 的名字。它是边缘总方差意义下的“保持”，不是每个样本范数不变。

### 4.1 与 DDPM 系数的对应

离散 DDPM 的 $\bar\alpha_k=\prod_{j\le k}(1-\beta_j)$。当 $\beta_j=\beta(t_j)h$ 很小时，

$$
\log\bar\alpha_k
=\sum_{j\le k}\log(1-\beta(t_j)h)
\approx-\sum_{j\le k}\beta(t_j)h
\to-B(t).
$$

所以 $\sqrt{\bar\alpha_k}\to e^{-B(t)/2}$，$1-\bar\alpha_k\to1-e^{-B(t)}$。连续边缘正是离散闭式边缘的极限。

## 五、VE SDE：信号不衰减，噪声尺度增长

VE 令 drift 为零：

$$dX_t=g(t)dW_t.$$

定义累计噪声方差

$$\Sigma(t)=\int_0^t g(s)^2ds.$$

则

$$
\boxed{X_t=X_0+\sqrt{\Sigma(t)}\epsilon,
\qquad X_t\mid X_0\sim N(X_0,\Sigma(t)I).}
$$

若预先指定单调噪声尺度 $\sigma(t)$，可取

$$g(t)^2=\frac{d}{dt}\sigma(t)^2.$$

这里有两种常见端点约定：

- 若 $\Sigma(0)=0$，则 $X_0$ 是未加噪数据，$\Sigma(t)=\sigma(t)^2-\sigma(0)^2$；
- 有些实现从很小的 $\sigma_{min}>0$ 开始，把 $p_0$ 实际定义为数据的轻微 Gaussian 平滑。

看到 $X_t=X_0+\sigma(t)\epsilon$ 时，必须问清 $\sigma(0)$ 是否为零，不能同时把两种约定代入一个公式。

VE 之所以叫 variance-exploding，是因为数据自身不缩小，而外加方差持续增大；有限终点只要噪声相对数据尺度足够大，就可近似一个易采样 reference law，但不是自动等于固定 $N(0,I)$。

## 六、sub-VP SDE：同一均值衰减，更小条件方差

sub-VP 保持 VP drift，却取

$$
\boxed{
dX_t=-\frac12\beta(t)X_tdt
+\sqrt{\beta(t)\left(1-e^{-2B(t)}\right)}dW_t.}
$$

于是 signal coefficient 仍为 $e^{-B/2}$。方差 ODE 是

$$V'=-\beta V+\beta(1-e^{-2B}).$$

候选解

$$V_{subVP}(t)=(1-e^{-B(t)})^2$$

的导数为

$$
2(1-e^{-B})\beta e^{-B}
=2\beta e^{-B}-2\beta e^{-2B},
$$

而 ODE 右侧为

$$
-\beta(1-2e^{-B}+e^{-2B})
+\beta(1-e^{-2B})
=2\beta e^{-B}-2\beta e^{-2B}.
$$

两者相等且 $V(0)=0$，故

$$
\boxed{X_t\mid X_0=x_0\sim
N\left(e^{-B(t)/2}x_0,(1-e^{-B(t)})^2I\right).}
$$

因为 $0\le1-e^{-B}\le1$，有

$$
(1-e^{-B})^2\le1-e^{-B},
$$

所以 sub-VP 的 conditional variance 不超过 VP；“sub”指这一点，不是 drift 更小，也不是总方差严格保持。

## 七、三种过程放到同一表中

| 过程 | drift $f(x,t)$ | $g(t)^2$ | 条件均值系数 | 条件方差 |
|---|---:|---:|---:|---:|
| VP | $-\frac12\beta x$ | $\beta$ | $e^{-B/2}$ | $1-e^{-B}$ |
| VE | $0$ | $\Sigma'$ | $1$ | $\Sigma(t)$ |
| sub-VP | $-\frac12\beta x$ | $\beta(1-e^{-2B})$ | $e^{-B/2}$ | $(1-e^{-B})^2$ |

最可靠的实现方法不是背表，而是逐项检查：

1. $g^2(t)\ge0$；
2. $m(0)=1,V(0)=0$；
3. $m'=am$；
4. $V'=2aV+g^2$；
5. 小步条件协方差为 $g(t)^2hI+o(h)$。

## 八、一个初学者应能手算的例子

取常数 $\beta(t)=2$，$t=0.5$，则 $B(t)=1$。

- VP：$m=e^{-1/2}\approx0.6065$，$V=1-e^{-1}\approx0.6321$；
- sub-VP：同一 $m$，但 $V=(1-e^{-1})^2\approx0.3996$；
- 若 VE 选 $g(t)^2=2$，则 $m=1$，$V=2t=1$。

三者的 $t$ 数值相同并不意味着 noise level 相同；比较模型时要按 log-SNR、边缘方差或同一端点 corruption 对齐，而非只对齐“时间 0.5”。

## 九、训练、生成与数值三条路径

**训练取样**：若闭式边缘已知，可直接采

$$X_t=m(t)X_0+\sqrt{V(t)}\epsilon,$$

无需 Euler 模拟 forward SDE。这里得到的是同一 conditional marginal，不是同一 Brownian path。

**生成动力学**：需要 learned score 进入 reverse-time SDE 或 probability-flow ODE；forward 闭式本身不能生成数据。

**数值实现**：连续系数 $\beta(t),g(t)$ 与离散表格的参数单位不同。若 Euler–Maruyama 步长为 $h$，噪声项必须是 $g(t)\sqrt{|h|}\epsilon$；$g(t)h\epsilon$ 与 $g(t)\epsilon$ 都错。

## 十、科学空间研读框

[[S-2022-Su-9209-扩散模型SDE篇]] 从离散小步和 $\sqrt{dt}$ 噪声切入，对初学者很有效。本节在此基础上补了：

- 由条件矩而非形式符号识别 SDE；
- 用积分因子统一求三类 closed-form marginal；
- 明确博客/论文中的 $\alpha_t,\sigma_t,\beta(t)$ 可能分别表示 amplitude、variance 或 rate；
- 把 fixed-time noising sampler 与完整 multi-time process 分开。

一级定义与 VP/VE/sub-VP 体系回查 [[S-2021-Song-Score-SDE]]。本节只陈述前向过程；反向时间条件留给 GEN-50。

## 十一、图：drift、diffusion 与边缘方差各管哪一件事

先看图回答：为什么 VP 与 sub-VP 可以有同一 signal decay，却有不同 conditional variance？VE 又为什么不能用“保持总方差”来解释？

![[00-知识库管理/_assets/figures/generative-models/fig-vp-ve-subvp-sde-ledger-v1.svg|900]]

> [!figure] 图 50.7-01　VP、VE 与 sub-VP 的系数—边缘账本
> 左栏比较 drift/diffusion，中央比较均值和条件方差，右栏用方差 ODE 检查闭式。来源：据 Score-SDE 公式与本节推导独立绘制。

**怎样读图**：先横向追踪一行：系数 $a,g$ 决定 $m,V$；再纵向比较 VP/sub-VP 的同均值异方差，和 VE 的不衰减信号。

**图没有证明什么**：图不证明任一 schedule 在有限网络下更好，不证明末端 prior 严格匹配，也不证明同一 fixed-time marginal 唯一确定 Brownian path coupling。

## 十二、本节回顾与训练

- 连续极限的 drift 是 $O(h)$，噪声标准差是 $O(\sqrt h)$；
- 线性 SDE 的均值和方差分别满足一阶 ODE；
- VP、VE、sub-VP 的名字描述不同的 signal/noise 设计，不是性能排序；
- 闭式 noising 只替代 forward marginal 模拟，不替代 reverse sampler；
- [[习题 - 从离散扩散到 VP、VE 与 sub-VP SDE]]
- [[解答 - 从离散扩散到 VP、VE 与 sub-VP SDE]]
