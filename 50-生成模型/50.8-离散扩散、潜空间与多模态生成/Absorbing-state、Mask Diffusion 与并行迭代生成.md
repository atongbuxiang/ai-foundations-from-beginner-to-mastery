---
type: derivation
status: verified
area: [generative-models, discrete-diffusion, masked-modeling]
node_id: GEN-58
prerequisites: ["[[Categorical Diffusion、转移矩阵与离散后验]]", "[[条件概率、全概率与 Bayes 公式]]"]
related: ["[[连续时间 Markov 链、离散 Score 与采样]]", "[[图像 Token、掩码生成与多模态条件分布]]"]
sources: ["[[S-2021-Austin-D3PM]]", "[[S-2022-Chang-MaskGIT]]"]
exercises: ["[[习题 - Absorbing-state、Mask Diffusion 与并行迭代生成]]"]
solutions: ["[[解答 - Absorbing-state、Mask Diffusion 与并行迭代生成]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-absorbing-mask-diffusion-refinement-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Absorbing-state、Mask Diffusion 与并行迭代生成

> [!abstract] 一句话结论
> 吸收式 mask diffusion 的 forward kernel 非常简单：真实 token 每步以一定概率保持，否则跳到 mask；mask 一旦出现就不返回。它给出闭式遮掩概率与解析 posterior。MaskGIT 式并行迭代生成与它共享“从 mask 恢复 token”的直觉，但置信度重遮掩 sampler 不自动等于某个 D3PM 精确反向链。

## 一、什么叫 absorbing state

令真实词表为 $\{1,ldots,K\}$，再加入特殊状态 $m=K+1$。在第 $t$ 步，真实 token 以 $\alpha_t$ 保持，以 $1-\alpha_t$ 变成 mask；mask 永远保持：

$$
q(x_t=j\mid x_{t-1}=i)=
\begin{cases}
\alpha_t,&i\le K,j=i,\\
1-\alpha_t,&i\le K,j=m,\\
1,&i=m,j=m,\\
0,&\text{otherwise}.
\end{cases}
$$

“吸收”是 Markov 链术语：一旦进入 $m$，forward process 以后都留在 $m$。它不是说反向生成不能从 mask 回到真实 token；反向链正是在学习这种恢复。

## 二、闭式边缘为什么只有两种结果

给定干净 token $x_0=i$，forward 过程中既不会跳到另一个真实 token，也不会从 mask 返回。因此到时刻 $t$ 只有两种可能：仍是 $i$，或已经是 $m$。

定义累计保留率

$$
\bar\alpha_t=\prod_{s=1}^t\alpha_s.
$$

要在时刻 $t$ 仍保持 $i$，每一步都必须保留，所以

$$
\boxed{q(x_t=i\mid x_0=i)=\bar\alpha_t,\qquad
q(x_t=m\mid x_0=i)=1-\bar\alpha_t.}
$$

这与 Bernoulli survival 完全一致。训练时可先抽 $u\sim U(0,1)$，若 $u<\bar\alpha_t$ 保留，否则置 mask；无需逐步模拟。

## 三、解析 posterior：观测没被 mask 与已被 mask

### 3.1 若 $x_t=i$ 是真实 token

由于 forward 不会把别的真实 token 变成 $i$，且 mask 不能返回，所以必然

$$
q(x_{t-1}=i\mid x_t=i,x_0=i)=1.
$$

这类位置没有新信息需要恢复。

### 3.2 若 $x_t=m$

候选 $x_{t-1}$ 只有两个：上一时刻仍是 $i$，最后一步才 mask；或上一时刻已是 mask。

两条未归一权重：

$$
w_{clean}=\bar\alpha_{t-1}(1-\alpha_t),
$$

$$
w_{mask}=1-\bar\alpha_{t-1}.
$$

两者之和是

$$
\bar\alpha_{t-1}(1-\alpha_t)+1-\bar\alpha_{t-1}
=1-\bar\alpha_t.
$$

因此

$$
\boxed{
q(x_{t-1}=i\mid x_t=m,x_0=i)
=\frac{\bar\alpha_{t-1}(1-\alpha_t)}{1-\bar\alpha_t},}
$$

$$
\boxed{
q(x_{t-1}=m\mid x_t=m,x_0=i)
=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}.}
$$

这解释了 reverse step 的两个动作：要么继续保持 mask，要么在本步揭示一个 clean token。若揭示，token identity 由模型对 $x_0$ 的预测提供。

## 四、序列时怎样采样

对长度 $n$ 的 token sequence，常见 forward 假设各位置给定 $x_0$ 后独立 mask：

$$
q(x_t\mid x_0)=\prod_{r=1}^nq(x_t^{(r)}\mid x_0^{(r)}).
$$

这让训练采样便宜，却不意味着数据 token 独立；去噪网络看到整段 $x_t$，可以学习跨位置相关性。

反向一步可按如下思路：

1. 对未 mask 位置保持原 token；
2. 网络输出每个 mask 位置的 clean-token distribution；
3. 根据解析 reveal probability 决定哪些位置本步解除 mask；
4. 对被揭示位置采 token，其余保持 mask。

若每个位置独立揭示，单步 conditional 会因子化；模型的全局相关性通过共享上下文 logits 间接进入，但同一步多个 token 的联合采样仍是条件独立近似。

## 五、随机 mask 训练目标处在哪一层

常见 masked-token objective 是

$$
\mathcal L_{mask}
=\mathbb E_{x_0,t,x_t}
\left[-\sum_{r:x_t^{(r)}=m}
\log p_\theta(x_0^{(r)}\mid x_t,t)
\right].
$$

它训练 clean-token prediction。要把它称为某个 diffusion ELBO，必须指定：

- forward mask schedule $\bar\alpha_t$；
- 时间采样与位置权重；
- reverse kernel 如何由 $x_0$ prediction 组成；
- 是否额外加入非 mask 位置 loss。

仅说“BERT 也做 mask，所以 BERT 就是 diffusion”缺少 generative terminal law、reverse sampling chain 与 likelihood objective，最多是训练形式类比。

## 六、MaskGIT 的并行迭代生成

[[S-2022-Chang-MaskGIT]] 的典型采样程序是：

1. 从全 mask token grid 开始；
2. 一次并行预测所有 mask 位置；
3. 对候选 token 采样并得到每位置 confidence；
4. 保留高置信 token，把低置信位置重新 mask；
5. 按 schedule 逐轮减少 mask 数，直到全部确定。

若第 $s$ 轮要保留的 mask ratio 为 $\gamma(s/S)$，则下一轮 mask 数约为

$$
M_{s+1}=\left\lceil n\gamma\!\left(\frac{s+1}{S}\right)\right\rceil.
$$

重要的是：**被揭示 token 还可能被重新 mask**。这不同于严格 reverse absorbing chain 中“已揭示后通常保持”的单调路径。MaskGIT 用 confidence 修正早期错误，是一个有效 sampler design，但它的 transition 必须按实际程序定义，不能自动套用前节解析 posterior。

## 七、并行为什么快，又为什么不是免费午餐

长度 $n$ 的 raster autoregressive model 需要约 $n$ 个顺序 network evaluations；MaskGIT 用 $S\ll n$ 轮并行更新，关键路径显著缩短。但每轮仍处理整张 token grid，而且包含 top-k/排序、重遮掩和随机采样。

更深的统计代价是：一轮同时给多个位置采样时，常用

$$
p_\theta(x_A\mid x_{\bar A})
\approx\prod_{r\in A}p_\theta(x_r\mid x_{\bar A}),
$$

把本轮待填集合 $A$ 条件独立化。多轮 refinement 让模型重新协调，但它不是从 exact joint conditional 一次采样。轮数、mask schedule、温度和 confidence rule 共同决定质量—成本折衷。

## 八、一个 schedule 手算

假设 $\alpha_1=0.9,\alpha_2=0.8,\alpha_3=0.5$，则

$$
\bar\alpha_3=0.9\times0.8\times0.5=0.36.
$$

给定 $x_3=m$，上一时刻仍为 clean 的 posterior probability 是

$$
\frac{\bar\alpha_2(1-\alpha_3)}{1-\bar\alpha_3}
=\frac{0.72\times0.5}{0.64}=0.5625.
$$

也就是说，已知第三步看到 mask，有 56.25% 概率是最后一步才被遮掩，43.75% 概率更早已 mask。后期若 $1-\alpha_t$ 很大，reverse step 会一次揭示更多 token。

## 九、图：严格吸收链与置信度 refinement 的分岔

先看图回答：哪一条路径允许“刚填好的 token 再被遮回去”？哪一条 reveal probability 可由 forward schedule 解析算出？

![[00-知识库管理/_assets/figures/generative-models/fig-absorbing-mask-diffusion-refinement-v1.svg|900]]

> [!figure] 图 50.8-02　Absorbing diffusion 与 MaskGIT refinement
> 上半部展示单个 token 的吸收式 forward/reverse posterior，下半部展示 token grid 的并行预测—置信度排序—重遮掩循环。来源：据 D3PM、MaskGIT 与本节推导独立绘制。

**怎样读图**：先看上半部的单调 mask survival，再看下半部非单调的重遮掩；二者共享 clean-token predictor，但 sampler transition 不同。

**图没有证明什么**：图不证明 MaskGIT 是某个 absorbing D3PM 的精确 sampler，不证明 confidence 等于 joint correctness，也不证明固定轮数在所有分辨率下保持同等质量。

## 十、本节回顾与训练

- absorbing mask 的 closed-form marginal 是 Bernoulli survival；
- 已 mask 后验只有“上一时刻 clean”与“上一时刻已 mask”两项；
- masked cross-entropy 要加 schedule/reverse 定义才能成为完整生成模型；
- MaskGIT 的 confidence re-mask 是非单调 refinement，不应伪装成解析 reverse kernel；
- 并行减少顺序深度，但引入同轮 conditional factorization 与多轮协调；
- [[习题 - Absorbing-state、Mask Diffusion 与并行迭代生成]]
- [[解答 - Absorbing-state、Mask Diffusion 与并行迭代生成]]
