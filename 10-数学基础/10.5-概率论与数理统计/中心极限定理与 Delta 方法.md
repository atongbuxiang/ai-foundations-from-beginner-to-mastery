---
type: concept
status: draft
area: [math/probability, math/statistics, ai/uncertainty]
aliases: [CLT, central limit theorem, Delta method, 渐近正态性]
prerequisites: ["[[随机变量的收敛与大数定律]]", "[[期望、方差与矩]]", "[[多元高斯分布]]", "[[Taylor 展开与余项]]"]
related: ["[[浓缩不等式]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[Fisher 信息、Cramér–Rao 界与渐近正态性]]", "[[假设检验、置信区间与多重比较]]", "[[概率论与数理统计 MOC]]"]
sources: ["MIT-6.436J-Lecture-17-LLN-CLT-Berry-Esseen", "MIT-RES-6.012-Lecture-19-CLT", "MIT-18.655-Lecture-15-Limit-Theorems", "MIT-18.655-Lecture-16-Delta-Method", "MIT-18.655-Lecture-17-Multivariate-Delta", "Wasserman-All-of-Statistics", "van-der-Vaart-Asymptotic-Statistics"]
created: 2026-08-19
updated: 2026-08-27
---

# 中心极限定理与 Delta 方法

> [!abstract] 本章主问题
> 大数定律只说样本平均趋近真均值；中心极限定理进一步说明，在 iid、有限非零方差等条件下，误差乘上 $\sqrt n$ 后的**分布**趋于 Gaussian。Delta 方法把这一渐近分布通过可微函数传播；它们是近似工具，不是“小样本必正态”、有限样本误差上界或任意高维/重尾训练噪声的通行证。

## 学习目标

完成本节后，你应当能够：

1. 准确写出 iid CLT 的中心化、尺度和依分布收敛结论；
2. 区分 LLN、CLT、精确 Gaussian 闭包和有限样本浓缩；
3. 用特征函数与二阶展开理解 Gaussian 极限为何出现；
4. 使用 Berry–Esseen 形式判断三阶矩、偏度和样本量如何影响近似；
5. 处理 Binomial 正态近似、连续性修正和尾部误差；
6. 用 Cramér–Wold 推出多元 CLT，并核对协方差形状；
7. 推导一阶、二阶与多元 Delta 方法；
8. 审计小批量梯度噪声、网络初始化和指标不确定性中的 CLT 声明。

> [!question] 初学者读完必须能回答
> 1. 为什么和必须减去 $n\mu$ 并除以 $\sigma\sqrt n$ 才可能有非退化极限？
> 2. LLN、CLT、Gaussian 闭包与浓缩界分别回答哪一种问题？
> 3. “依分布趋于 Gaussian”为什么不等于有限 $n$ 已经精确 Gaussian？
> 4. Berry–Esseen 用什么矩条件控制哪一种误差，它为什么仍不保证极端尾部相对误差？
> 5. 一阶 Delta 方法如何把 $g'(\theta)$ 同时传播到误差尺度和渐近方差？
> 6. 当 $g'(\theta)=0$ 时，为什么必须改用二阶展开和新的缩放？
> 7. 多元 CLT 与多元 Delta 方法中应怎样检查维度和协方差传播？

## 进入正文前：LLN 压缩误差，CLT 放大并观察误差形状

> [!info] 课程位置
> 上一章已经证明 $\overline W_n-\mu\to0$；本章不再问误差是否消失，而是把它乘上 $\sqrt n$，寻找非退化的极限分布。Delta 方法随后把这个局部 Gaussian 误差通过可微函数传播。下一章的浓缩不等式会转向有限样本尾概率，而不是渐近分布形状。

> [!tip] 建议两遍阅读
> - 第一遍只掌握“中心化—乘 $\sqrt n$—得到 Gaussian 极限—乘梯度传播”四步，并复算下面的 $3/20$。
> - 第二遍再学习特征函数证明、Cramér–Wold、多元 CLT、Berry–Esseen、连续性修正、二阶 Delta 和退化边界。所有近似都要保留有限样本条件与误差审计。

> [!question] 本章的推导问题链
> 1. 样本平均误差为什么是 $n^{-1/2}$ 量级，而不是 $n^{-1}$？
> 2. 为什么必须中心化并乘 $\sqrt n$ 才能得到非退化极限？
> 3. 单个样本明明是四点离散分布，标准化平均为什么会趋向连续 Gaussian？
> 4. 多元极限中的协方差为什么必须保留坐标之间的 $1/20$？
> 5. 可微函数怎样通过梯度传播渐近协方差？
> 6. 一阶梯度为零时，为什么 $\sqrt n$ 尺度会给出退化结论？
> 7. CLT、Berry–Esseen 与浓缩界分别回答什么，为什么不能互相替代？

### 贯穿例：四原子样本的 Gaussian 极限与乘积统计量

继续令 $W_1,\ldots,W_n$ iid，每个样本都重新抽取自己的 $\Theta_i$。已有

$$
\mu=
\begin{bmatrix}1/2\\1/2\end{bmatrix},
\qquad
\Sigma=
\begin{bmatrix}
1/4&1/20\\
1/20&1/4
\end{bmatrix},
\qquad
\overline W_n=\frac1n\sum_{i=1}^nW_i.
$$

多元中心极限定理给出

$$
\sqrt n(\overline W_n-\mu)
\xrightarrow d
G_0,
\qquad
G_0\sim\mathcal N(0,\Sigma).
$$

单个 $W_i$ 只在四个点上取值，有限 $n$ 的平均也仍在有限格点上；结论是它们经过中心化和缩放后的**分布趋近**连续 Gaussian，不是有限 $n$ 时突然变成精确 Gaussian。

沿两个主方向投影，可以分别读出共同模式与差异模式：

$$
u_+^\top G_0\sim\mathcal N\left(0,\frac3{10}\right),
\qquad
u_-^\top G_0\sim\mathcal N\left(0,\frac15\right).
$$

这正是多元高斯一章中先算出的两个椭球方向。Cramér–Wold 的思想是：若每个固定线性投影都满足相应的一元 CLT，就能确定整个向量极限。

现在考虑非线性统计量

$$
\widehat q_n=g(\overline W_n),
\qquad
g(a,b)=ab.
$$

它估计的是两个边缘均值的乘积

$$
g(\mu)=\frac14.
$$

注意 $1/4$ 不是同一次观测共同成功的概率 $P(X_1=X_2=1)=3/10$；前者是边缘参数的乘积，后者包含依赖结构。对象不分清，计算再正确也会回答错问题。

$g$ 在 $\mu$ 处的梯度为

$$
\nabla g(\mu)
=\begin{bmatrix}\mu_2\\\mu_1\end{bmatrix}
=\begin{bmatrix}1/2\\1/2\end{bmatrix}.
$$

一阶展开可在本例中直接写成

$$
\begin{aligned}
g(\overline W_n)-g(\mu)
&=\frac12\left(\overline W_{n1}-\frac12\right)
+\frac12\left(\overline W_{n2}-\frac12\right)\\
&\quad+
\left(\overline W_{n1}-\frac12\right)
\left(\overline W_{n2}-\frac12\right).
\end{aligned}
$$

前两项是线性主项；每个坐标误差为 $O_P(n^{-1/2})$，所以最后的乘积余项是 $O_P(n^{-1})$，乘 $\sqrt n$ 后消失。Delta 方法于是给出

$$
\sqrt n\left(\widehat q_n-\frac14\right)
\xrightarrow d
\mathcal N\left(0,\nabla g(\mu)^\top\Sigma\nabla g(\mu)\right).
$$

渐近方差逐项计算为

$$
\begin{aligned}
\nabla g(\mu)^\top\Sigma\nabla g(\mu)
&=\frac14\left(
\frac14+2\cdot\frac1{20}+\frac14
\right)\\
&=\frac3{20}.
\end{aligned}
$$

如果错误地删除坐标协方差，便会得到 $1/8$，低估真实渐近方差。Delta 方法传播的不只是每个坐标的方差，还包括完整 covariance。

再看一阶方法失效的边界。令

$$
h(w)=\|w-\mu\|_2^2.
$$

因为 $\nabla h(\mu)=0$，一阶 Delta 只得到退化的零极限。必须使用二阶尺度：

$$
n\,h(\overline W_n)
\xrightarrow d
G_0^\top G_0
=\frac3{10}Z_+^2+\frac15Z_-^2,
$$

其中 $Z_+,Z_-$ 独立且服从 $\mathcal N(0,1)$。这说明导数为零不是“统计量没有波动”，而是主导波动发生在更小的 $n^{-1}$ 尺度并具有非 Gaussian 的二次型极限。

> [!note] 本轮符号账本
> | 符号 | 类型 | 解释 |
> |---|---|---|
> | $G_0$ | 二维中心 Gaussian | 标准化样本平均的极限 |
> | $\sqrt n$ | 确定性尺度 | 抵消平均误差的 $n^{-1/2}$ 收缩 |
> | $g(a,b)=ab$ | 标量可微函数 | 把两个样本均值变成乘积统计量 |
> | $\nabla g(\mu)$ | $2\times1$ 向量 | 一阶局部敏感度 |
> | $\nabla g^\top\Sigma\nabla g$ | 标量 | 传播后的渐近方差 |
> | $h(w)$ | 二次函数 | 梯度为零、需要二阶 Delta 的边界例 |

> [!analysis] 一阶 Delta 方法的公式七问
> 1. **为什么引入？** 许多估计量是基本样本平均的光滑函数，需要把已知极限传播到新统计量。
> 2. **对象是什么？** $T_n$ 是随机向量，$\theta$ 是固定极限，$g$ 是局部可微映射，Jacobian/梯度负责线性传播。
> 3. **条件是什么？** 需要 $r_n(T_n-\theta)\Rightarrow Z$、$g$ 在 $\theta$ 可微，并能控制 Taylor 余项在尺度 $r_n$ 下消失。
> 4. **怎样推出？** 写 $g(T_n)-g(\theta)=Dg(\theta)(T_n-\theta)+o_P(\|T_n-\theta\|)$，乘 $r_n$ 后用 Slutsky。
> 5. **协方差怎样传播？** 若 $Z\sim\mathcal N(0,\Sigma)$，则线性像具有协方差 $J\Sigma J^\top$；标量函数时是 $\nabla g^\top\Sigma\nabla g$。
> 6. **边界在哪里？** 梯度为零、不可微点、参数在边界、维度随 $n$ 增长或重尾无有限方差时，普通一阶结论可能退化或失效。
> 7. **AI 中对应什么？** perplexity、比率指标、校准误差和经过激活/归一化的估计量都需要误差传播；自动微分给梯度，却不会替你验证 CLT 与余项条件。

> [!success] 第一遍停靠线
> 应能写出 $\sqrt n(\overline W_n-\mu)\Rightarrow\mathcal N(0,\Sigma)$，解释单个离散样本与连续极限不矛盾；能从 $\nabla g(\mu)=(1/2,1/2)^\top$ 得到渐近方差 $3/20$；还应知道 $\nabla h(\mu)=0$ 时必须改用 $n$ 尺度和二次型极限。

## 阅读前检查

- [[随机变量的收敛与大数定律]]：依分布收敛、Slutsky 与样本平均；
- [[期望、方差与矩]]：中心化、标准化和高阶矩；
- [[多元高斯分布]]：线性投影、协方差与退化 Gaussian；
- [[Taylor 展开与余项]]：一阶/二阶局部展开。

## 先看一个具体问题：同一枚硬币的两种极限定理

令 $X_i\overset{iid}{\sim}\operatorname{Bernoulli}(p)$，

$$
S_n=\sum_{i=1}^nX_i,
\qquad
\overline X_n=\frac{S_n}{n}.
$$

弱大数定律说

$$
\overline X_n\xrightarrow Pp.
$$

它把误差压缩成一个点，却没有描述误差形状。CLT 考察被放大后的误差：

$$
\frac{\sqrt n(\overline X_n-p)}{\sqrt{p(1-p)}}
=\frac{S_n-np}{\sqrt{np(1-p)}}
\xrightarrow d\mathcal N(0,1).
$$

因此在 $n$ 足够大且近似质量可接受时，

$$
\overline X_n
\approx
\mathcal N\left(p,\frac{p(1-p)}n\right).
$$

这里的 $\approx$ 是有限样本分布近似，不是随机变量逐点相等。

## 一、为什么必须中心化与标准化

设 $X_i$ iid，均值 $\mu$、方差 $\sigma^2\in(0,\infty)$。和

$$
S_n=\sum_{i=1}^nX_i
$$

的均值与方差为

$$
\mathbb E[S_n]=n\mu,
\qquad
\operatorname{Var}(S_n)=n\sigma^2.
$$

若直接看 $S_n$，中心位置和波动尺度都随 $n$ 改变。先减去中心，再除以标准差：

$$
Z_n
=\frac{S_n-n\mu}{\sigma\sqrt n}
=\frac{\sqrt n(\overline X_n-\mu)}\sigma.
$$

检查：

$$
\mathbb E[Z_n]=0,
\qquad
\operatorname{Var}(Z_n)=1.
$$

> [!warning] 分母是 $\sqrt n$，不是 $n$
> 独立和的方差按 $n$ 增长，标准差按 $\sqrt n$ 增长。样本平均的标准差因此按 $1/\sqrt n$ 缩小，这就是 Monte Carlo 的平方根速率来源。

## 二、经典 iid 中心极限定理

> [!theorem] Lindeberg–Lévy CLT
> 设 $X_1,X_2,\dots$ iid，
> $$
> \mathbb E[X_1]=\mu,
> \qquad
> 0<\operatorname{Var}(X_1)=\sigma^2<\infty.
> $$
> 则
> $$
> \frac{\sum_{i=1}^nX_i-n\mu}{\sigma\sqrt n}
> \xrightarrow d\mathcal N(0,1).
> $$
> 等价地，
> $$
> \sqrt n(\overline X_n-\mu)
> \xrightarrow d\mathcal N(0,\sigma^2).
> $$

逐条解释：

- iid 是这一个版本的结构条件，不是所有 CLT 的必要条件；
- 有限非零方差定义了 $\sqrt n$ 尺度；
- 结论是依分布收敛，不是 a.s. 或依概率收敛到一个 Gaussian 随机变量；
- 极限描述标准化误差，不说 $X_i$ 自身接近 Gaussian；
- 不要求 $X_i$ 的三阶矩存在；三阶绝对矩主要用于经典 Berry–Esseen 速率。

## 三、Gaussian 极限从哪里来：特征函数证明路线

先标准化单个变量：

$$
Y_i=\frac{X_i-\mu}{\sigma},
\qquad
\mathbb E[Y_i]=0,
\qquad
\mathbb E[Y_i^2]=1.
$$

于是

$$
Z_n=\frac1{\sqrt n}\sum_{i=1}^nY_i.
$$

记 $Y_1$ 的特征函数为

$$
\varphi_Y(t)=\mathbb E[e^{itY_1}].
$$

在 $t=0$ 附近，由二阶矩存在和 Taylor 展开，

$$
\varphi_Y(t)
=1+it\mathbb E[Y_1]
-\frac{t^2}{2}\mathbb E[Y_1^2]
+o(t^2)
=1-\frac{t^2}{2}+o(t^2).
$$

独立性把和的特征函数变为乘积：

$$
\begin{aligned}
\varphi_{Z_n}(t)
&=\prod_{i=1}^n
\varphi_Y\left(\frac t{\sqrt n}\right)\\
&=\left[
1-\frac{t^2}{2n}+o\left(\frac1n\right)
\right]^n.
\end{aligned}
$$

利用极限 $(1+a_n/n)^n\to e^a$，得到

$$
\varphi_{Z_n}(t)\to e^{-t^2/2}.
$$

$e^{-t^2/2}$ 正是标准 Gaussian 的特征函数。由 Lévy 连续性定理，

$$
Z_n\xrightarrow d\mathcal N(0,1).
$$

### 每个条件用在哪里

| 条件 | 证明中的位置 |
|---|---|
| 相同分布 | 所有因子使用同一个 $\varphi_Y$ |
| 独立 | 和的特征函数分解为乘积 |
| 有限均值/方差 | 在零点做二阶展开并得到 $0,1$ 系数 |
| $\sigma^2>0$ | 标准化分母合法 |

这条证明路线解释了“许多小而相对均衡的独立贡献”为什么只留下前两阶信息；它不证明有限 $n$ 已经近似良好。

## 四、LLN、CLT、精确 Gaussian 与浓缩的分工

| 工具 | 研究对象 | 典型结论 | 不提供什么 |
|---|---|---|---|
| LLN | $\overline X_n$ | $\overline X_n\to\mu$ | 误差形状、精确速率 |
| CLT | $\sqrt n(\overline X_n-\mu)$ | 分布趋于 Gaussian | 当前 $n$ 的严格尾界 |
| Gaussian 闭包 | Gaussian 变量的线性和 | 有限 $n$ 精确 Gaussian | 非 Gaussian 输入的自动精确性 |
| 浓缩不等式 | 有限 $n$ 偏离概率 | 显式上界 | 通常不描述中心区域完整形状 |
| Berry–Esseen | CLT CDF 近似误差 | $O(n^{-1/2})$ 上界 | 尾部相对误差和最优常数的普遍保证 |

如果 $X_i$ 本来就是 Gaussian，则 $S_n$ 对每个有限 $n$ 都精确 Gaussian，不需要 CLT。CLT 的价值在于输入可以是 Bernoulli、Exponential 等非 Gaussian 分布。

## 五、图示：标准化和、Gaussian 极限与 Delta 线性化

先用下图回答一个视觉问题：**标准化为何产生 Gaussian 极限，有限样本误差如何表述，非线性函数又怎样传播这个极限？**

![[00-知识库管理/_assets/figures/probability/fig-clt-delta-method-v2.svg|880]]

> [!figure] 图 10.5.12｜CLT 的标准化、有限样本近似与 Delta 局部传播
> A 对比偏斜单项与中心化、$\sqrt n$ 标准化后的和；B 把有限 $n$ 的 CDF 与 Gaussian CDF 区分，并标出 Berry–Esseen 型误差；C 用 $g$ 在 $\theta$ 附近的切线表示一阶 Delta 传播。来源：独立绘制；生成脚本：[[plot_probability_limits_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** A 同时检查中心和尺度，不能只看曲线“变钟形”；B 把两条 CDF 的最大竖直差理解为一种有限样本近似指标；C 从估计误差沿切线传播，斜率 $g'(\theta)$ 决定一阶极限的缩放。

**适用边界（图没有证明什么）。** 钟形曲线只是机制示意，不代表任意有限样本近似都好；Berry–Esseen 还需要有限三阶绝对中心矩，并主要控制 CDF 绝对误差；切线图只覆盖 $g'(\theta)\neq0$ 的一阶情形，零导数、不可微点和高维增长需另行分析。

## 六、Berry–Esseen：有限样本近似误差的第一把尺

设 $X_i$ iid，均值 $\mu$，方差 $\sigma^2>0$，并且三阶绝对中心矩

$$
\rho=\mathbb E|X_1-\mu|^3<\infty.
$$

> [!theorem] Berry–Esseen 形式
> 存在与分布和 $n$ 无关的普适常数 $C$，使
> $$
> \sup_{x\in\mathbb R}
> \left|
> P\left(
> \frac{S_n-n\mu}{\sigma\sqrt n}\le x
> \right)-\Phi(x)
> \right|
> \le
> \frac{C\rho}{\sigma^3\sqrt n}.
> $$

无量纲比率

$$
\frac\rho{\sigma^3}
$$

衡量标准化后的三阶绝对尾部规模。它大时，即使 $n$ 看起来不小，上界也可能很松。

### 正确解释

- 上界控制整个 CDF 的最大绝对差；
- 速率是 $1/\sqrt n$，常数和分布尾部同样重要；
- 它不保证极小尾概率的**相对误差**好；
- 三阶矩不存在不代表 CLT 必然失败，只代表这条经典速率界不可用；
- 对格点分布，连续性修正可以显著改善中央区域近似。

## 七、Binomial 正态近似与连续性修正

若 $S_n\sim\operatorname{Binomial}(n,p)$，则

$$
\mu_S=np,
\qquad
\sigma_S=\sqrt{np(1-p)}.
$$

要近似

$$
P(a\le S_n\le b),
$$

把整数柱 $a,\dots,b$ 对应为连续区间 $[a-1/2,b+1/2]$：

$$
P(a\le S_n\le b)
\approx
\Phi\left(\frac{b+1/2-np}{\sqrt{np(1-p)}}\right)
-
\Phi\left(\frac{a-1/2-np}{\sqrt{np(1-p)}}\right).
$$

### 手算：$n=100,p=0.5$ 的中央概率

求 $P(45\le S_{100}\le55)$。均值 $50$，标准差 $5$。连续性修正后端点为 $44.5,55.5$：

$$
z_L=\frac{44.5-50}{5}=-1.1,
\qquad
z_U=1.1.
$$

因此

$$
P(45\le S_{100}\le55)
\approx\Phi(1.1)-\Phi(-1.1)
=2\Phi(1.1)-1
\approx0.7286.
$$

检查：区间关于均值对称，结果应使用对称 CDF；概率位于 $[0,1]$。

> [!warning] “$np$ 和 $n(1-p)$ 大于某阈值”只是经验规则
> 近似质量还取决于要算中央区间还是极端尾部、需要绝对还是相对误差，以及 $p$ 是否接近边界。高风险尾概率应比较精确 Binomial、saddlepoint 或可靠数值方法。

## 八、CLT 何时失败或收敛很慢

### 8.1 无限方差：$\sqrt n$ 尺度可能错误

若 $X_i$ 为标准 Cauchy，则

$$
\frac1n\sum_{i=1}^nX_i
\overset d=X_1.
$$

样本平均不会向有限均值集中，经典 CLT 条件失败。某些重尾分布的和会在不同尺度下趋于 stable law，而非 Gaussian。

### 8.2 一个项支配总和

对非同分布三角阵，若单个项占总方差的不可忽略比例，Gaussian 平滑机制可能失败。Lindeberg 条件以总方差 $s_n^2$ 为尺度，要求大跳跃贡献消失：

$$
\frac1{s_n^2}
\sum_k
\mathbb E\left[
(X_{n,k}-\mu_{n,k})^2
\mathbf1_{\{|X_{n,k}-\mu_{n,k}|>\varepsilon s_n\}}
\right]\to0.
$$

### 8.3 依赖与非平稳

时间序列、MCMC、训练梯度和增强样本可能相关。依赖 CLT 往往把方差改为 long-run variance：

$$
\sigma_{\mathrm{LR}}^2
=\gamma_0+2\sum_{k\ge1}\gamma_k,
$$

其中 $\gamma_k$ 是滞后协方差。把它错当 $\gamma_0$ 会低估标准误。

### 8.4 高维不是逐坐标 CLT 的免费并集

固定维度多元 CLT 不自动给随 $d$ 快速增长时的 uniform approximation。逐坐标近似好，也不保证最大值、范数或尾部联合事件近似好。

## 九、多元中心极限定理

设 $X_i\in\mathbb R^d$ iid，

$$
\mathbb E[X_i]=\mu\in\mathbb R^d,
\qquad
\operatorname{Cov}(X_i)=\Sigma\in\mathbb R^{d\times d},
$$

且二阶矩有限。则

> [!theorem] 固定维度多元 CLT
> $$
> \sqrt n(\overline X_n-\mu)
> \xrightarrow d\mathcal N_d(0,\Sigma).
> $$

$\Sigma$ 可以半正定而非正定，此时极限 Gaussian 可能退化在低维子空间上。

### Cramér–Wold 证明路线

对任意固定 $a\in\mathbb R^d$，

$$
a^\top\sqrt n(\overline X_n-\mu)
=\sqrt n\left(
\frac1n\sum_{i=1}^na^\top X_i-a^\top\mu
\right).
$$

这是标量 iid 平均。其单项方差为

$$
\operatorname{Var}(a^\top X_i)=a^\top\Sigma a.
$$

由标量 CLT，

$$
a^\top\sqrt n(\overline X_n-\mu)
\xrightarrow d
\mathcal N(0,a^\top\Sigma a).
$$

因为所有线性投影都收敛到目标多元 Gaussian 的投影，Cramér–Wold 装置给出向量收敛。

## 十、Delta 方法：把渐近误差送过非线性函数

### 10.1 一维一阶 Delta 方法

> [!theorem] 一维 Delta 方法
> 若
> $$
> \sqrt n(T_n-\theta)\xrightarrow d Z,
> $$
> 且 $g$ 在 $\theta$ 可微，则
> $$
> \sqrt n\bigl(g(T_n)-g(\theta)\bigr)
> \xrightarrow d g'(\theta)Z.
> $$
> 特别地，若 $Z\sim\mathcal N(0,\tau^2)$，则极限为
> $$
> \mathcal N(0,[g'(\theta)]^2\tau^2).
> $$

### 10.2 逐步证明

可微性意味着存在余项 $r(t)$，满足当 $t\to\theta$ 时

$$
g(t)-g(\theta)
=g'(\theta)(t-\theta)+r(t)(t-\theta),
\qquad r(t)\to0.
$$

由 $\sqrt n(T_n-\theta)=O_P(1)$ 可推出 $T_n\xrightarrow P\theta$，所以

$$
r(T_n)\xrightarrow P0.
$$

两边乘 $\sqrt n$：

$$
\sqrt n[g(T_n)-g(\theta)]
=\bigl(g'(\theta)+r(T_n)\bigr)
\sqrt n(T_n-\theta).
$$

第一因子依概率收敛到 $g'(\theta)$，第二因子依分布收敛到 $Z$。由 Slutsky 定理，乘积依分布收敛到 $g'(\theta)Z$。

> [!intuition] Delta 方法就是随机 Taylor 展开
> $T_n$ 以 $n^{-1/2}$ 尺度靠近 $\theta$；在这个越来越小的邻域里，$g$ 的切线主导。导数不仅改变中心附近斜率，也把渐近标准差乘上 $|g'(\theta)|$。

## 十一、Delta 方法手算例子

### 11.1 对数变换

设 $\overline X_n$ 满足

$$
\sqrt n(\overline X_n-\mu)
\xrightarrow d\mathcal N(0,\sigma^2),
\qquad \mu>0.
$$

取 $g(x)=\log x$，$g'(\mu)=1/\mu$，因此

$$
\sqrt n(\log\overline X_n-\log\mu)
\xrightarrow d
\mathcal N\left(0,\frac{\sigma^2}{\mu^2}\right).
$$

有限样本近似方差为

$$
\operatorname{Var}(\log\overline X_n)
\approx\frac{\sigma^2}{n\mu^2}.
$$

若 $\overline X_n$ 可能非正，log 根本没有定义；“概率趋向正值”不等于每个有限样本都安全。

### 11.2 odds 的不确定性

若 $\widehat p_n$ 是 Bernoulli 样本比例，$p\in(0,1)$，取

$$
g(p)=\frac p{1-p},
\qquad
g'(p)=\frac1{(1-p)^2}.
$$

因为

$$
\sqrt n(\widehat p_n-p)
\xrightarrow d\mathcal N(0,p(1-p)),
$$

所以

$$
\sqrt n\left(
\frac{\widehat p_n}{1-\widehat p_n}
-\frac p{1-p}
\right)
\xrightarrow d
\mathcal N\left(0,\frac{p}{(1-p)^3}\right).
$$

$p\uparrow1$ 时导数和渐近方差爆炸，说明边界附近线性近似很敏感。

## 十二、导数为零：二阶 Delta 方法

若 $g'(\theta)=0$，一阶结论退化为零，不能据此断言统计量没有波动。假设 $g$ 二阶可微，$g''(\theta)\ne0$：

$$
g(T_n)-g(\theta)
=\frac12g''(\theta)(T_n-\theta)^2
+o_P((T_n-\theta)^2).
$$

若 $\sqrt n(T_n-\theta)\xrightarrow dZ$，则

$$
n[g(T_n)-g(\theta)]
\xrightarrow d
\frac12g''(\theta)Z^2.
$$

### 手算：平方函数在零点

令 $T_n=\overline X_n$，$\mu=0$，且

$$
\sqrt n\overline X_n\xrightarrow d\mathcal N(0,\sigma^2).
$$

取 $g(x)=x^2$，$g'(0)=0$、$g''(0)=2$：

$$
n\overline X_n^2
\xrightarrow d Z^2
=\sigma^2\chi_1^2.
$$

正确尺度从 $\sqrt n$ 变成 $n$，极限也不再 Gaussian。

## 十三、多元 Delta 方法

设 $T_n\in\mathbb R^d$，$\theta\in\mathbb R^d$，

$$
\sqrt n(T_n-\theta)
\xrightarrow d\mathcal N_d(0,\Sigma).
$$

令

$$
g:\mathbb R^d\to\mathbb R^k
$$

在 $\theta$ 可微，Jacobian

$$
J_g(\theta)\in\mathbb R^{k\times d}.
$$

则

> [!theorem] 多元 Delta 方法
> $$
> \sqrt n(g(T_n)-g(\theta))
> \xrightarrow d
> \mathcal N_k
> \left(0,
> J_g(\theta)\Sigma J_g(\theta)^\top
> \right).
> $$

形状检查：

$$
(k\times d)(d\times d)(d\times k)=k\times k.
$$

### 比率统计量

取 $g(a,b)=a/b$，$b\ne0$，

$$
\nabla g(a,b)
=\begin{bmatrix}1/b\\-a/b^2\end{bmatrix}.
$$

若 $(A_n,B_n)$ 的渐近协方差为 $\Sigma/n$，则

$$
\operatorname{Avar}\left(\frac{A_n}{B_n}\right)
=\frac1n\nabla g(\theta)^\top
\Sigma\nabla g(\theta).
$$

忽略 $A_n,B_n$ 的协方差会漏掉交叉项，可能高估也可能低估不确定性。

## 十四、方差稳定化

若估计量 $T_n$ 的近似方差依赖均值参数：

$$
\operatorname{Var}(T_n)
\approx\frac{v(\theta)}n,
$$

希望选择 $g$ 使

$$
[g'(\theta)]^2v(\theta)
$$

近似为常数。可令

$$
g'(\theta)\propto\frac1{\sqrt{v(\theta)}}.
$$

### Poisson 例子

若 $T_n=\overline X_n$ 且 $X_i\sim\operatorname{Poisson}(\lambda)$，则

$$
v(\lambda)=\lambda.
$$

取 $g(\lambda)=2\sqrt\lambda$，则 $g'(\lambda)=1/\sqrt\lambda$，所以

$$
[g'(\lambda)]^2v(\lambda)=1.
$$

这是一阶渐近稳定，不是小 $\lambda$ 时的精确等方差。Anscombe 等修正会处理有限样本偏差。

## 十五、studentization 与 plug-in

经典 CLT 含未知 $\sigma$：

$$
\frac{\sqrt n(\overline X_n-\mu)}\sigma
\xrightarrow d\mathcal N(0,1).
$$

若样本标准差 $S_n\xrightarrow P\sigma>0$，由 Slutsky，

$$
\frac{\sqrt n(\overline X_n-\mu)}{S_n}
\xrightarrow d\mathcal N(0,1).
$$

这叫 studentization。它不等于有限 $n$ 下精确 Student-$t$ 分布；精确 $t$ 结论还需要 Gaussian 样本等结构。

Delta 方差中的未知 $\theta,\Sigma$ 常用一致估计 plug in：

$$
\widehat V
=J_g(T_n)\widehat\Sigma_nJ_g(T_n)^\top.
$$

需要检查导数在估计点稳定、协方差估计一致且分母不接近零。

## 十六、可靠数值与实验诊断

### 16.1 标准化不要制造消去或溢出

计算

$$
\frac{S_n-n\mu}{\sigma\sqrt n}
$$

时，若 $S_n$ 和 $n\mu$ 都极大且接近，直接相减可能丢失有效位。可使用中心化在线更新、pairwise reduction 或先累计 $X_i-\mu$；若 $\mu$ 也估计得到，要区分同一数据重复使用带来的依赖。

### 16.2 Gaussian CDF 的尾部

极小尾概率应使用 `logcdf`、`logsf` 或专门的 survival function。直接算

$$
1-\Phi(z)
$$

在大正 $z$ 时会发生灾难性消去并返回零。

### 16.3 检查近似不能只画直方图

建议同时报告：

1. 多个 $n$ 下的标准化统计量；
2. empirical CDF 与 $\Phi$ 的最大差；
3. Q–Q 图，特别标注尾部；
4. skewness、极端值和三阶绝对矩估计；
5. 目标尾概率的精确/模拟对照；
6. 多随机种子与 Monte Carlo 标准误。

直方图 bin 宽会影响视觉，不能单独验证 CLT。

### 16.4 自动微分不等于 Delta 条件已满足

框架可以计算 $J_g(T_n)$，但不能自动证明：

- $T_n$ 有 $\sqrt n$ 渐近分布；
- $g$ 在真参数处可微；
- Jacobian 在边界附近稳定；
- plug-in 协方差一致；
- 有限样本正态近似可接受。

## 十七、AI 中的具体调用

| 场景 | 随机和/估计量 | CLT/Delta 提供 | 关键条件 | 失败模式 |
|---|---|---|---|---|
| 小批量梯度 | $\bar g_B\in\mathbb R^p$ | 固定方向上的近似 Gaussian 噪声 | 条件独立、有限协方差、无单样本支配 | 重尾、重复数据、高维最大方向、参数非平稳 |
| 网络初始化 | preactivation $h_j=\sum_iW_{ji}x_i$ | 宽度大时单元边缘 Gaussian 动机 | 权重独立、尺度平衡、Lindeberg 型条件 | 权重共享、强相关、attention/归一化耦合 |
| Monte Carlo loss | $\widehat L_m=m^{-1}\sum f(Z_i)$ | 标准误 $\sigma/\sqrt m$ | iid/依赖 CLT、有限方差 | 重要性权重重尾、MCMC 自相关 |
| 评估指标比率 | precision、rate、归一化 loss | multivariate Delta 协方差传播 | 分母远离零、joint CLT | 稀有类别分母小、忽略协方差 |
| perplexity | $\operatorname{PPL}=e^{\bar\ell}$ | log-loss 的方差经 exp 传播 | 序列依赖处理、矩与 Jacobian | 长序列相关、exp 放大右尾 |
| ensemble 平均 | 预测向量均值 | 固定维度方向 CLT | 成员独立/弱依赖 | 共享数据和初始化造成强相关 |

### 17.1 小批量梯度的精确声明模板

在固定 $\theta$、固定方向 $v\in\mathbb R^p$ 下，若单样本梯度 $g_i(\theta)$ 条件 iid、有限方差，则

$$
\sqrt B\,v^\top(\bar g_B-\nabla R(\theta))
\xrightarrow d
\mathcal N(0,v^\top\Sigma_g(\theta)v).
$$

这不等于整个高维梯度向量在有限 batch 下“就是 isotropic Gaussian”，也不等于跨训练步噪声同分布。

### 17.2 网络宽度的 Gaussian 极限

对固定输入 $x\in\mathbb R^d$，若

$$
h=\sum_{i=1}^dW_ix_i,
$$

各项独立、均值零、方差尺度平衡且没有单项支配，CLT 支持 $h$ 近似 Gaussian。若 $x_i$ 极度稀疏且一个坐标占主导，或权重共享产生强依赖，Lindeberg 机制可能失效。

把宽度极限推广到多层、多个输入的联合过程需要额外证明；这才连接 Gaussian process/NTK 理论，不能由单个标量 CLT 一步得到。

### 17.3 指标的 Delta 审计

若测试集得到 token 平均负对数似然 $\bar\ell_n$，且有 joint/依赖 CLT，perplexity 为

$$
g(\bar\ell_n)=e^{\bar\ell_n}.
$$

Delta 近似标准误为

$$
\operatorname{SE}(e^{\bar\ell_n})
\approx e^{\bar\ell_n}\operatorname{SE}(\bar\ell_n).
$$

若 token 同属文档而强相关，不能把 token 数直接当独立 $n$；应按文档 cluster、long-run variance 或 bootstrap 结构处理。

## 十八、常见误区与纠错

### 误区 1：样本量超过 30 就必然正态

不存在脱离分布、统计量和误差目标的普适阈值。偏斜、重尾、稀有事件和尾概率可能需要远大样本量。

### 误区 2：CLT 说样本数据变成 Gaussian

CLT 描述标准化的和/均值的分布。原始 $X_i$ 的分布不随 $n$ 改变。

### 误区 3：CLT 给出 $P(|\bar X_n-\mu|>\varepsilon)$ 的严格上界

CLT 是渐近分布近似。严格有限样本上界应看 Chebyshev、Hoeffding、Bernstein 等；Berry–Esseen 只在附加矩条件下控制 CDF 误差。

### 误区 4：只要独立就能用经典 CLT

还需有限非零方差和同分布；非同分布版本要检查 Lindeberg/Lyapunov 等条件。

### 误区 5：Delta 方法对任何非线性都成立

需要在真参数处可微。边界、绝对值尖点、argmax、阈值函数和分母为零都要单独处理。

### 误区 6：$g'(\theta)=0$ 意味着没有误差

一阶项消失时要提高展开阶数并改变归一化尺度，极限可能为 $\chi^2$ 型而非 Gaussian。

### 误区 7：逐坐标正态近似等于高维联合近似

最大值、选择后统计量和范数依赖联合尾部；维度随样本增长时需高维 CLT 或 Gaussian comparison 工具。

## 十九、前沿地位与研究边界

| 地位 | 内容 | 本节边界 |
|---|---|---|
| 经典定理 | iid CLT、多元 CLT、Berry–Esseen、Delta、Slutsky | 条件与收敛意义完整保留 |
| 已建立推广 | Lindeberg–Feller、依赖 CLT、martingale CLT、stable limits | 只给接口，后续随机过程/渐近统计展开 |
| 现代 AI 理论 | 宽网络 Gaussian process、NTK、SGD 扩散近似 | 需要模型特定极限，不能只引用经典 CLT |
| 经验规律 | 梯度噪声“看起来 Gaussian” | 必须说明层、方向、batch、训练阶段和尾部检验 |
| 开放问题 | 高维、重尾、非平稳、自适应训练中的精确极限与有限宽修正 | 不宣称单一普适噪声模型 |

## 二十、本节回顾

- **CLT 研究什么？** $\sqrt n$ 放大的样本平均误差的极限分布。
- **为什么是 Gaussian？** 独立性把特征函数变为乘积，中心化后的二阶展开在极限中留下 $e^{-t^2/2}$。
- **与 LLN 有何不同？** LLN 把误差压到零；CLT 放大误差并描述形状。
- **有限样本怎样审计？** 看 Berry–Esseen 条件、偏度/尾部、连续性修正和直接模拟/精确计算。
- **Delta 方法做什么？** 用真参数处 Jacobian 把基本估计量的渐近误差传播到光滑函数。
- **导数为零怎么办？** 用二阶 Delta，通常尺度变为 $n$ 且极限非 Gaussian。
- **AI 中最危险的外推是什么？** 把固定方向、固定参数、低维的 CLT 说成整个训练梯度在所有阶段都是 iid isotropic Gaussian。
- **后继是什么？** [[浓缩不等式]]补有限样本尾界，[[Fisher 信息、Cramér–Rao 界与渐近正态性]]把 Delta/CLT 用于参数估计。

## 二十一、掌握检查

- [ ] 能写出 CLT 两种等价标准化并检查均值/方差；
- [ ] 能复述特征函数证明中的四个关键步骤；
- [ ] 能解释 Berry–Esseen 的误差度量与三阶矩条件；
- [ ] 能带连续性修正计算 Binomial 中央概率；
- [ ] 能构造无限方差或单项支配的失败例子；
- [ ] 能用 Cramér–Wold 推导固定维多元 CLT；
- [ ] 能完整证明一阶 Delta 并处理二阶退化；
- [ ] 能算 $J\Sigma J^\top$ 并核对形状；
- [ ] 能审计一个 AI 中的 Gaussian-noise 声明是否超出定理。

## 二十二、练习与解答

- 习题：[[习题 - 中心极限定理与 Delta 方法]]；
- 独立解答：[[解答 - 中心极限定理与 Delta 方法]]；
- 阶段入口：[[练习与测验 MOC]]。

## 二十三、来源

- MIT 6.436J, Lecture 17, *Laws of Large Numbers and Central Limit Theorem*：CLT、特征函数与 Berry–Esseen；
- MIT RES.6-012, Lecture 19, *The Central Limit Theorem*：初学者直觉、Binomial 与连续性修正；
- MIT 18.655, Lectures 15–17：极限定理、一维/多元 Delta 与渐近统计接口；
- Wasserman, *All of Statistics*：CLT、Delta、plug-in 与一致性；
- van der Vaart, *Asymptotic Statistics*：渐近工具的严谨统一框架。
