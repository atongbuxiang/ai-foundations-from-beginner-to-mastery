---
type: derivation
status: verified
area: [generative-models, diffusion, reverse-time, score]
node_id: GEN-50
prerequisites: ["[[从离散扩散到 VP、VE 与 sub-VP SDE]]", "[[时间反演、score 与扩散生成动力学]]", "[[条件概率、全概率与 Bayes 公式]]"]
related: ["[[Probability-flow ODE 与共享边缘分布]]", "[[Marginal Score、Conditional Score 与去噪等价]]", "[[Predictor–Corrector 与 Score-based 生成程序]]"]
sources: ["[[S-1982-Anderson-Reverse-Time-Diffusion]]", "[[S-2021-Song-Score-SDE]]", "[[S-2022-Su-9209-扩散模型SDE篇]]"]
exercises: ["[[习题 - Reverse-time SDE、时间反演与 Score Drift]]"]
solutions: ["[[解答 - Reverse-time SDE、时间反演与 Score Drift]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-reverse-sde-time-orientation-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Reverse-time SDE、时间反演与 Score Drift

> [!abstract] 一句话结论
> forward diffusion 的反向过程不是“把噪声项取负”，而是换到由未来观测定义的反向 filtration；Bayes 校正使反向 drift 多出 density score。对 $dX_t=f(X_t,t)dt+g(t)dW_t$，若仍用 $t$ 并从 $1$ 积到 $0$，反向 drift 是 $f-g^2\nabla\log p_t$；若用正向反时钟 $\tau=1-t$，则 drift 是 $-f+g^2\nabla\log p_t$。

## 一、问题：随机加噪为什么还能“反向”

forward 一步把许多可能的 $x_t$ 映到重叠的 $x_{t+h}$。噪声 realization 通常未知，因此不能逐样本求逆。reverse-time SDE 所做的是另一件事：给定当前 noisy state，按照正确的 reverse conditional law 随机采前一时刻，使整个反向过程的边缘依次经过 $p_t$ 并回到数据分布。

所以必须区分：

- **inverse map**：逐样本恢复同一个 forward noise path，通常做不到；
- **reverse process in law**：构造具有正确反向 transition law 的随机过程；
- **learned sampler**：用神经网络近似 score 后再有限步模拟，只有近似正确。

## 二、先固定 forward 对象

本节先取空间无关的标量扩散系数：

$$
dX_t=f(X_t,t)dt+g(t)dW_t,
\qquad t:0\uparrow1.
$$

令 $p_t(x)$ 是 $X_t$ 的密度，score 为

$$s_t(x)=\nabla_x\log p_t(x).$$

假设密度足够光滑且正、SDE 有合适的弱解和反向过程；这些不是装饰，若数据端在低维流形上导致密度奇异，score 和 time reversal 可能只在 $t>0$ 的平滑分布上定义。

## 三、从一小步 Bayes 看见 score correction

先把 $f,g$ 在很小时间段内视为局部常数。forward Euler 步为

$$
Y=X_{t+h}\approx X_t+f(X_t,t)h+g(t)\sqrt h\,\epsilon.
$$

令 $Z=X_t+f(X_t,t)h$。条件于 $Z$，$Y=Z+g\sqrt h\epsilon$ 是小 Gaussian corruption。Tweedie 型恒等式给出

$$
\mathbb E[Z\mid Y=y]
=y+g(t)^2h\nabla_y\log p_{t+h}(y)+o(h).
$$

又因 $Z=X_t+f h$，一阶近似下

$$
\mathbb E[X_t-Y\mid Y=y]
=\left[-f(y,t)+g(t)^2\nabla_y\log p_t(y)\right]h+o(h).
$$

右侧正是“向过去走一个正的反向时钟小步”时的条件均值。两项含义是：

1. $-f$ 撤销 deterministic forward drift；
2. $g^2s_t$ 用当前 density 的局部对数斜率修正 many-to-one 加噪造成的 posterior preference。

这段局部推导解释公式来源，但完整过程级结论由反向扩散定理承担，参见 [[S-1982-Anderson-Reverse-Time-Diffusion]]。

## 四、两种时间记法必须并列掌握

### 4.1 保持 $t$，从 $1$ 积到 $0$

score-based 文献常写

$$
\boxed{
dX_t=\left[f(X_t,t)-g(t)^2s_t(X_t)\right]dt
+g(t)d\bar W_t,
\qquad t:1\downarrow0.
}
$$

这里 $dt<0$。不要只看方括号的正负来判断实际位移方向；真实小步是 bracket 乘一个负时间增量。

### 4.2 定义正向反时钟 $\tau=1-t$

令 $Y_\tau=X_{1-\tau}$，$\tau:0\uparrow1$。因 $dt=-d\tau$，得到

$$
\boxed{
dY_\tau=
\left[-f(Y_\tau,1-\tau)
+g(1-\tau)^2s_{1-\tau}(Y_\tau)\right]d\tau
+g(1-\tau)d\widetilde W_\tau.
}
$$

这与上一公式完全一致，只是参数方向不同。程序中若 solver 只接受递增时间，可用第二种；若传入递减网格，可直接用第一种。**公式、时间网格和步长符号必须成套。**

## 五、为什么噪声项不是 $-g\,dW_t$

Brownian path 几乎处处不可微；forward 的 $W_t$ 也不适应 reverse filtration。反向过程使用新的 Brownian motion $\bar W$ 或 $\widetilde W$，其增量相对于反向信息流独立。

把 forward 保存下来的噪声逐项取负，会构造某个特定 coupling，却不是在只给当前 state 时的正确 reverse Markov kernel。生成任务只有 terminal sample 和 learned score，没有原 forward path 可供倒放。

## 六、Gaussian 平稳特例：最有效的符号检查

考虑常数 $\beta>0$ 的 VP/Ornstein–Uhlenbeck SDE：

$$dX_t=-\frac12\beta X_tdt+\sqrt\beta dW_t.$$

若 $X_0\sim N(0,I)$，则所有 $p_t=N(0,I)$，score 是 $s_t(x)=-x$。

在正向反时钟 $\tau$ 中，reverse drift 为

$$
-f+g^2s
=+\frac12\beta x+\beta(-x)
=-\frac12\beta x.
$$

它与 forward OU drift 相同，符合平稳可逆过程的直觉。若你算出 $+3\beta x/2$，通常是把 $t\downarrow$ 公式直接放进 $\tau\uparrow$ 程序而忘了换号。

## 七、非平稳 Gaussian 特例：score 如何决定回拉强度

令 forward 为纯 Brownian：

$$dX_t=dW_t,\qquad X_0\sim N(0,\sigma_0^2I).$$

则 $p_t=N(0,(\sigma_0^2+t)I)$，

$$s_t(x)=-\frac{x}{\sigma_0^2+t}.$$

正向反时钟 drift 是

$$-f+g^2s_t=-\frac{x}{\sigma_0^2+t}.$$

越靠近过去、方差越小，回拉越强。这个 drift 并不是人为加入的 denoising heuristic，而是由当前 marginal density 精确决定的 reverse conditional bias。

## 八、一般扩散矩阵时多出的项

若

$$dX_t=b(X_t,t)dt+G(X_t,t)dW_t,\qquad D=GG^\top,$$

且 $D$ 依赖空间，则在 $t:1\downarrow0$ 记法中，一般 reverse drift 形如

$$
b_{rev,i}
=b_i-\sum_j\partial_{x_j}D_{ij}
-\sum_jD_{ij}\partial_{x_j}\log p_t.
$$

只有 $D=g(t)^2I$ 与空间无关时，散度项消失并简化为 $f-g^2s_t$。因此不能把 scalar score-SDE 公式无修改地套到 state-dependent diffusion 或 manifold diffusion。

## 九、从真实 score 到神经网络 score

真实 $s_t=\nabla\log p_t$ 通常不可得，训练网络 $s_\theta(x,t)$ 后使用

$$f-g^2s_\theta$$

替代 exact reverse drift。令 score error $e_\theta=s_\theta-s_t$，则 drift error 是

$$-g(t)^2e_\theta(x,t).$$

因此相同的 unweighted score MSE 在不同 $t$ 对 reverse dynamics 的影响不同；$g^2$、时间权重、状态访问分布和 solver stability 都会放大或缩小误差。训练 loss 小不等于 finite-step terminal distribution 自动接近数据。

## 十、最小 reverse sampler 合同

用递减时间网格 $1=t_N>t_{N-1}>\cdots>t_0=0$，记 $h_k=t_{k-1}-t_k<0$。Euler–Maruyama 一步可写为

$$
X_{t_{k-1}}=X_{t_k}
+[f-g^2s_\theta](X_{t_k},t_k)h_k
+g(t_k)\sqrt{-h_k}\,z_k.
$$

必须审计：

- $h_k$ 在 drift 中保留负号，噪声标准差用 $\sqrt{-h_k}$；
- 最后一步是否注入随机噪声由 sampler 定义决定，不能沿用模板而不检查；
- 初始化 $X_1\sim p_1^{prior}$ 是否真匹配 forward terminal marginal；
- score 输出是 $s$、$\epsilon$、$x_0$ 还是 $v$，换算系数是否对应同一 SDE；
- NFE、random seed、corrector steps 与 solver error 单独记录。

## 十一、科学空间研读框

[[S-2022-Su-9209-扩散模型SDE篇]] 的优势是把反向 drift 写成“原 drift 加 density-gradient correction”的清晰中文链条。本节补严四点：

1. 明确文章公式采用 $t:1\downarrow0$；
2. 给出 $\tau=1-t$ 的程序友好版本；
3. 用 reverse filtration 解释为何不能倒放同一 Brownian noise；
4. 把 scalar $g(t)$ 特例与 state-dependent $D(x,t)$ 的散度项分开。

方法定义与现代 score-based 生成回查 [[S-2021-Song-Score-SDE]]；过程级 time reversal 回查 [[S-1982-Anderson-Reverse-Time-Diffusion]]。

## 十二、图：同一公式为何会出现两组符号

先看图回答：$f-g^2s$ 与 $-f+g^2s$ 哪一个是正确 reverse drift？为什么答案取决于横轴朝向而不是记忆口诀？

![[00-知识库管理/_assets/figures/generative-models/fig-reverse-sde-time-orientation-v1.svg|900]]

> [!figure] 图 50.7-02　reverse-time SDE 的两种时钟、同一生成方向
> 上轨保留 $t$ 并用负步长，下轨使用 $\tau=1-t$ 与正步长；右侧把 drift、noise 和 score error 分账。来源：据 Anderson 与 Score-SDE 公式独立绘制。

**怎样读图**：先沿箭头确认是数据→噪声还是噪声→数据，再读步长符号，最后才读 drift 方括号。上下两轨的实际小位移一致。

**图没有证明什么**：图不证明弱解存在，不证明 learned score 准确，也不证明 Euler–Maruyama 在任意 NFE 下保持目标分布。

## 十三、本节回顾与训练

- reverse-time SDE 是 law-level time reversal，不是逐样本 invert forward noise；
- $t\downarrow$ 与 $\tau\uparrow$ 两种记法等价，但 drift 符号不能混搭；
- score correction 来自 Bayes posterior preference；
- state-dependent diffusion 还需扩散矩阵散度项；
- continuous theorem、score approximation 和 finite-step sampler 是三层误差；
- [[习题 - Reverse-time SDE、时间反演与 Score Drift]]
- [[解答 - Reverse-time SDE、时间反演与 Score Drift]]
