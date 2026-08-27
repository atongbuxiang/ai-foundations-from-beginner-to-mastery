---
type: derivation
status: verified
area: [generative-models, diffusion, conditional-generation, classifier-guidance]
node_id: GEN-65
prerequisites: ["[[条件概率、全概率与 Bayes 公式]]", "[[时间反演、score 与扩散生成动力学]]", "[[数据、噪声、速度与 Score 参数化]]"]
related: ["[[Classifier-Free Guidance、尺度与质量多样性前沿]]", "[[逆问题、约束采样与 Plug-and-Play 控制]]"]
sources: ["[[S-2022-Su-9257-条件控制生成]]", "[[S-2021-Dhariwal-Nichol-Classifier-Guidance]]"]
exercises: ["[[习题 - 条件生成、Bayes 分解与 Classifier Guidance]]"]
solutions: ["[[解答 - 条件生成、Bayes 分解与 Classifier Guidance]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-classifier-guidance-bayes-field-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 条件生成、Bayes 分解与 Classifier Guidance

> [!abstract] 一句话结论
> 条件生成的数学核心不是“把标签塞进网络”，而是把 unconditional log-density 的梯度加上 conditional evidence 的梯度。Classifier guidance 用一个在噪声层上训练的分类器近似后者；真正部署时还必须按 reverse SDE、probability-flow ODE 或离散 Gaussian kernel 的系数把这项转换成 drift/mean 修正。

## 一、先问：我们究竟要从什么分布采样

无条件生成目标是 $x\sim p(x)$。给定类别、文本或属性 $y$，目标变为

$$x\sim p(x\mid y).$$

扩散模型在中间噪声层处理 $x_t$，所以需要的是整族 conditional marginals

$$p_t(x_t\mid y),\qquad t\in[0,T],$$

而不只是干净数据上的 $p_0(x_0\mid y)$。这解释了为什么“拿一个只见过清晰图的分类器去指导高噪声图”通常不可靠：输入已经离开分类器的训练分布。

## 二、Bayes 到 conditional score：逐行推导

假设 $p_t(x)>0$、$p_t(y)>0$，并且关于 $x$ 可微。Bayes 公式给出

$$
p_t(x\mid y)=\frac{p_t(x)p_t(y\mid x)}{p_t(y)}.
$$

取对数：

$$
\log p_t(x\mid y)
=\log p_t(x)+\log p_t(y\mid x)-\log p_t(y).
$$

对 $x$ 求梯度。因为 $p_t(y)$ 不依赖 $x$，

$$
\nabla_x\log p_t(y)=0,
$$

所以

$$
\boxed{
s_t(x\mid y)=s_t(x)+\nabla_x\log p_t(y\mid x),
}
$$

其中 $s_t(x)=\nabla_x\log p_t(x)$。这一等式是精确的；近似来自网络、分类器和 finite sampler，而不是 Bayes 本身。

### 2.1 guidance scale 对应什么分布

把分类器梯度乘 $w$：

$$s_t^{(w)}(x)=s_t(x)+w\nabla_x\log p_t(y\mid x).$$

若这些 score 精确且归一化常数有限，则它是未归一密度

$$
\tilde p_t^{(w)}(x\mid y)
\propto p_t(x)p_t(y\mid x)^w
$$

的 score。$w=0$ 回到无条件，$w=1$ 是普通 conditional score，$w>1$ 相当于降低“条件温度”，会更偏向分类器确信区域。这不是免费收益：分布质量被重新集中，覆盖可能下降。

## 三、一个一维 Gaussian 例子

设无条件边缘

$$p_t(x)=\mathcal N(0,1),$$

条件证据形如

$$p_t(y\mid x)\propto\exp\left[-\frac{(x-a)^2}{2\tau^2}\right].$$

则

$$
s_t(x)=-x,
\qquad \nabla_x\log p_t(y\mid x)=-\frac{x-a}{\tau^2},
$$

guided score 为

$$
s_t^{(w)}(x)
=-\left(1+\frac{w}{\tau^2}\right)x+\frac{wa}{\tau^2}.
$$

令 score 为零得到 mode/mean

$$
\mu_w=\frac{wa}{\tau^2+w},
\qquad
\sigma_w^2=\frac{\tau^2}{\tau^2+w}.
$$

$w$ 增大时中心移向 $a$，方差缩小。这就是“条件更强、覆盖更窄”的最小可算版本。

## 四、怎样进入 reverse SDE 与 probability-flow ODE

对 forward SDE

$$dX_t=f(X_t,t)dt+g(t)dW_t,$$

score-based reverse dynamics 的漂移含 $g(t)^2s_t$。为了避免正/反向时钟符号混乱，本卷先写成系数接口：

$$
b_{rev}[s]=f-g^2s,
\qquad
b_{pf}[s]=f-\frac12g^2s.
$$

把 $s=s_t(x\mid y)$ 代入，classifier term 对 drift 的贡献分别是

$$
-g(t)^2w\nabla_x\log p_t(y\mid x)
$$

和

$$
-\frac12g(t)^2w\nabla_x\log p_t(y\mid x).
$$

这里的微分方程通常从 $T$ 积到 $0$，数值步长为负；因此不要只凭式子里的负号判断样本“朝哪走”。正确做法是：先固定时间参数化，再让 solver 处理有符号步长。

> [!warning] 系数不能丢
> “把 classifier gradient 加到 score”与“把同一个向量直接加到 $x$”不是同一算法。reverse SDE、PF-ODE、DDPM mean shift、DDIM noise prediction 各有自己的 $g^2$、$\sigma_t$、$\alpha_t$ 或步长系数。

## 五、离散 Gaussian 反向核中的均值平移

假设某一步无条件反向核近似为

$$p(x_{t-1}\mid x_t)=\mathcal N(x_{t-1};\mu,\Sigma).$$

条件后验正比于

$$p(x_{t-1}\mid x_t)\,p(y\mid x_{t-1}).$$

在 $\mu$ 附近一阶展开

$$
\log p(y\mid x_{t-1})
\approx \text{const}+g_y^\top(x_{t-1}-\mu),
\quad g_y=\nabla_x\log p(y\mid x)|_{x=\mu}.
$$

把它与 Gaussian log-density 合并并配方：

$$
-\frac12(x-\mu)^\top\Sigma^{-1}(x-\mu)+g_y^\top(x-\mu)
=-\frac12(x-\mu-\Sigma g_y)^\top\Sigma^{-1}(x-\mu-\Sigma g_y)+C.
$$

所以近似条件核仍为相同协方差、均值平移到

$$
\boxed{\mu_{guided}=\mu+\Sigma g_y.}
$$

若乘 scale $w$，位移为 $w\Sigma g_y$。这是小方差/局部线性近似；分类器曲率很大或步长很大时，高阶项不可忽略。

## 六、训练 noisy classifier

最直接做法从真实 $(x_0,y)$ 采样，按 forward process 得到 $x_t$，训练

$$
\min_\phi\ \mathbb E_{t,x_0,y,x_t}
[-\log p_\phi(y\mid x_t,t)].
$$

实现合同至少包括：

1. $t$ 或 noise level 是否输入分类器；
2. 时间采样分布；
3. 分类器看到的 normalization 与 diffusion 输入是否一致；
4. gradient 是对原始 pixel、latent 还是归一化张量求；
5. mixed precision 下 gradient scale；
6. 是否使用 adversarial/gradient regularization；
7. classifier forward+backward 的真实成本。

分类准确率高不代表 guidance gradient 好。分类只约束 logits 的值/排序，采样还依赖输入梯度的方向、尺度和局部光滑性。

## 七、失败模式

### 7.1 对抗方向

若分类器能被无意义高频模式高置信触发，guided sampler 可能生成“让分类器满意但人不满意”的样本。这是 reward/metric hacking 的早期形式。

### 7.2 高噪声失校准

高 $t$ 时类别信息弱，$p(y\mid x_t)$ 接近先验；若分类器仍给巨大梯度，通常说明校准或分布外行为有问题。

### 7.3 scale 与 diversity

$w$ 不是越大越好。一维例子已表明方差会缩小；高维时还可能出现色彩过饱和、纹理尖锐、mode/attribute coverage 下降。

### 7.4 参数化误配

把 score gradient 直接加到 noise prediction 会缺少 $-\sigma_t$ 一类换算；把 pixel classifier gradient 用在 latent $z_t$ 上还需 decoder/Jacobian 或 latent classifier。

## 八、科学空间研读框

[[S-2022-Su-9257-条件控制生成]] 从 Bayes 与 Gaussian 配方切入，帮助初学者看到“分类器不是替换生成模型，而是平移每一步反向分布”。课程作三点补严：

- 文章的离散均值平移与连续 conditional score identity 分层；
- 分类器须估计 noisy $p_t(y\mid x_t)$，不是只在 $x_0$ 上准确；
- [[S-2021-Dhariwal-Nichol-Classifier-Guidance]] 的 quality–diversity 结果是 ImageNet 协议证据，不升级为普遍规律。

## 九、图：Bayes 怎样弯曲 score field

先看图回答：蓝色 unconditional score、橙色 classifier evidence 和绿色 conditional score 分别由谁提供？scale 增大时为何不只是“更准确”？

![[00-知识库管理/_assets/figures/generative-models/fig-classifier-guidance-bayes-field-v1.svg|900]]

> [!figure] 图 50.9-01　从 Bayes 分解到 classifier-guided field
> 左侧展示 score 相加，中央展示一维 Gaussian evidence 的均值/方差变化，右侧列出进入不同 sampler 时的系数。来源：据 classifier guidance 原论文、科学空间 9257 与本节推导独立绘制。

**怎样读图**：先按“prior field + evidence field”读向量，再看 $w$ 增大如何把质量集中到证据高值区域，最后检查 sampler 方框中的 $g^2/2$ 或 covariance 系数。

**图没有证明什么**：图不证明 classifier gradient 语义可靠，不证明任意 $w>1$ 改善人类质量，也不证明有限步 sampler 精确采自 $p(x)p(y\mid x)^w$。

## 十、学习出口

- 能无提示推 Bayes conditional score identity；
- 能对一维 Gaussian 算出 $\mu_w,\sigma_w^2$；
- 能解释 SDE、PF-ODE 与 Gaussian mean shift 的系数为何不同；
- 能列出 noisy classifier 的梯度可靠性检查；
- [[习题 - 条件生成、Bayes 分解与 Classifier Guidance]]
- [[解答 - 条件生成、Bayes 分解与 Classifier Guidance]]
