---
type: derivation
status: verified
area: [generative-models, vector-quantization, tokenizer, representation-learning]
node_id: GEN-60
prerequisites: ["[[自编码器、重构与生成缺口]]", "[[变分推断、ELBO 与证据分解]]", "[[Monte Carlo、重要性采样与方差缩减]]", "[[K-Means、聚类风险与不可辨识性]]"]
related: ["[[Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]]", "[[Latent Diffusion、压缩瓶颈与两阶段误差]]", "[[图像 Token、掩码生成与多模态条件分布]]"]
sources: ["[[S-2017-Oord-VQ-VAE]]", "[[S-2019-Su-6760-VQ-VAE简明介绍]]", "[[S-2017-Jang-Gumbel-Softmax]]"]
exercises: ["[[习题 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"]
solutions: ["[[解答 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-vqvae-forward-backward-prior-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator

> [!abstract] 一句话结论
> VQ-VAE 先把 encoder 的连续向量映射到最近 codebook vector，再让 decoder 从量化表示重构；整数 code index 就是 token。训练必须分别说明 hard nearest-neighbor forward、STE surrogate backward、codebook/commitment update。若要生成新样本，还必须训练第二阶段 prior；autoencoder 本身并不会凭空采出有意义 token grid。

## 一、为什么需要离散 tokenizer

普通 autoencoder 学

$$z=E_\phi(x),\qquad \hat x=D_\psi(z).$$

若 $z$ 是高维连续张量，decoder 可能重构很好，但后续 prior 要在连续空间上建模。VQ 引入有限 codebook

$$\mathcal E=\{e_1,
\ldots,e_K\},\qquad e_k\in\mathbb R^d,$$

并对每个 latent vector $z_r$ 选择最近 code：

$$
k_r=\arg\min_{1\le k\le K}\|z_r-e_k\|_2^2,
\qquad q_r=e_{k_r}.
$$

若 encoder 输出 $h\times w$ 个向量，整张图被编码成 $h\times w$ 个整数 $k_r$。这和文本 tokenizer 相似：都把输入变成有限 alphabet sequence；但图像 code 的语义、可逆性和局部性由训练学得，不是天然词义。

## 二、hard forward 为什么不可直接反传

考虑一维两个 codes $e_1<e_2$。nearest-neighbor map 是

$$
q(z)=
\begin{cases}
e_1,&z<(e_1+e_2)/2,\\
e_2,&z>(e_1+e_2)/2.
\end{cases}
$$

它在每个 Voronoi cell 内是常数，真实导数为零；在边界跳变，不可导。若严格用真实导数，重构 loss 对 encoder 的梯度几乎处处为零，encoder 无法从 decoder 获得方向信息。

## 三、STE 的前向/反向双合同

定义 stop-gradient $\operatorname{sg}[u]$：前向值等于 $u$，反向导数设为零。构造

$$
\boxed{z_q=z+\operatorname{sg}[q-z].}
$$

前向：

$$z_q=z+(q-z)=q,$$

所以 decoder 真正看到 hard code vector。反向：

$$\frac{\widetilde\partial z_q}{\partial z}=I,$$

因此把 decoder 对 $z_q$ 的梯度原样传给 encoder。

波浪线是重要提醒：这是程序指定的 **surrogate derivative**，不是 hard nearest-neighbor map 的真实 Jacobian。STE 可以有实践价值，但不能把它写成数学微分恒等式。

## 四、为什么还要两项量化损失

仅用上式，重构梯度传给 encoder，却不会经 $q$ 传给 codebook。标准 VQ-VAE objective 常写成

$$
\mathcal L
=\mathcal L_{rec}(x,D_\psi(z_q))
+\underbrace{\|\operatorname{sg}[z]-q\|_2^2}_{\text{codebook loss}}
+\beta\underbrace{\|z-\operatorname{sg}[q]\|_2^2}_{\text{commitment loss}}.
$$

三项的梯度职责：

| 项 | 更新对象 | 直觉 |
|---|---|---|
| reconstruction | decoder + 经 STE 的 encoder | 保存任务相关信息 |
| codebook | code vectors | 把 code 拉向分配给它的 encoder outputs，类似 K-means center update |
| commitment | encoder | 防止 $z$ 任意漂离所选 code，控制尺度和切换 |

不同实现可能给 codebook loss 额外权重，或把 $\beta$ 记在另一项；复现必须写公式而不是只写“用了 VQ loss”。

## 五、EMA codebook update

另一种常见方案不让 optimizer 直接更新 $e_k$，而维护每个 code 的 assignment count 和向量和：

$$
N_k\leftarrow\rho N_k+(1-\rho)n_k,
$$

$$
M_k\leftarrow\rho M_k+(1-\rho)
\sum_{r:k_r=k}z_r,
$$

$$
e_k\leftarrow\frac{M_k}{N_k+\varepsilon}.
$$

它像在线 K-means。这里 $\varepsilon$、Laplace smoothing、distributed all-reduce、空 code reset 都会影响结果。把 gradient update 换成 EMA 不只是“同一公式的快速实现”，而是改变 optimizer dynamics。

## 六、一个二维 Voronoi 例子

设 codes

$$e_1=(0,0),\quad e_2=(2,0),\quad e_3=(0,2),$$

encoder 输出 $z=(1.4,0.3)$。平方距离为

$$
d_1^2=1.4^2+0.3^2=2.05,
$$

$$
d_2^2=(-0.6)^2+0.3^2=0.45,
$$

$$
d_3^2=1.4^2+(-1.7)^2=4.85.
$$

所以 hard token 是 $k=2$，forward decoder 输入 $q=e_2$。若 decoder 回传梯度 $g=(0.7,-0.2)$，标准 STE 令 encoder 收到同一个 $g$，尽管真实 nearest-neighbor map 在该 cell 内导数为零。

若只更新所选 code 的 codebook loss，则 $e_2$ 朝 $z$ 移动，$e_1,e_3$ 本批不动。这正是低利用率 code 难以复活的优化原因之一，GEN-61 会比较解决方案。

## 七、为什么 VQ-VAE 仍需要 prior

训练 tokenizer 后，数据诱导 empirical code distribution

$$
q_{data}(k_{1:n})
=P_{x\sim p_{data}}(T(x)=k_{1:n}).
$$

要生成，必须学 prior，例如 autoregressive：

$$
p_\theta(k_{1:n})
=\prod_{r=1}^np_\theta(k_r\mid k_{<r}),
$$

或 masked/diffusion prior。采样流程是

$$
k_{1:n}\sim p_\theta,
\qquad \hat x=D_\psi(e_{k_1},\ldots,e_{k_n}).
$$

[[S-2019-Su-6760-VQ-VAE简明介绍]] 特别强调了这条两阶段路线，并指出 VQ-VAE 名称虽含 VAE，其常用训练形式更像 hard discrete autoencoder + learned prior。原始论文确有概率建模解释，但不能直接把标准 Gaussian VAE 的 reparameterized ELBO 公式搬来。

## 八、两阶段误差怎样分

对真实 $x$，tokenizer reconstruction 是

$$x\to k=T(x)\to \hat x=D(k).$$

它测表示损失。生成时则是

$$k\sim p_\theta(k)\to \tilde x=D(k),$$

还多了 prior mismatch。即使 tokenizer 重构近乎完美，prior 若生成了训练分布中罕见/不协调的 code combinations，样本仍会差。反之，感知 loss 很强的 decoder 可能让 sample 看起来锐利，却用 hallucination 掩盖高 distortion。

至少报告：

- pixel/perceptual reconstruction 与 reconstruction FID；
- codebook utilization、perplexity/entropy 与 dead-code rate；
- prior token NLL 或 masked objective；
- end-to-end sample metrics 与人工检查；
- token grid shape、$K,d$、bitrate 的真实定义。

## 九、Gumbel–Softmax 与 VQ 的关系

VQ 是 nearest code by distance；Gumbel–Softmax 是对 categorical logits 的连续松弛。可以把负距离当 logits：

$$a_k=-\|z-e_k\|^2/\tau,$$

再做 soft/hard selection，但这样会改变 forward、梯度和训练 objective。标准 VQ-VAE 不需要 Gumbel noise 才能定义 token。

[[S-2017-Jang-Gumbel-Softmax]] 的 finite-temperature sample 位于 simplex；VQ hard forward 位于有限 code vectors。两者都在处理离散选择的梯度困难，但不能把 temperature bias、STE bias 与 nearest-neighbor quantization error 合并成一个“离散误差”。

## 十、Tokenizer 不是越大越好

增大 $K$ 可以降低最近邻 distortion，却带来：

- 更稀疏的 code assignment，dead codes 更易出现；
- prior 的 alphabet 更大，softmax/建模更难；
- 名义 bits/token 为 $\log_2K$，但实际 entropy 可能远低；
- 相同 token grid 下 nominal bitrate 上升。

相反，减小空间 token 数能降低 prior sequence length，但每个 token 必须承载更多信息，重构和语义瓶颈加重。最佳点是 rate–distortion–prior complexity 的联合折衷，不是单看 utilization。

## 十一、图：一条 forward、三条 backward、再接一个 prior

先看图回答：decoder 的重构梯度怎样绕过 hard argmin 到 encoder？codebook 又从哪里得到更新？为什么生成阶段还要单独画 prior？

![[00-知识库管理/_assets/figures/generative-models/fig-vqvae-forward-backward-prior-v1.svg|900]]

> [!figure] 图 50.8-04　VQ-VAE 的 hard forward、surrogate backward 与 second-stage prior
> 黑色实线是前向值，红色虚线是代理梯度，蓝色线是 codebook/EMA 更新，右侧单独画 prior sampling。来源：据 VQ-VAE 原论文与科学空间 6760 独立绘制。

**怎样读图**：先沿 $x\to z\to k\to q\to\hat x$ 读 forward；再从 reconstruction loss 反向看 STE；随后看 codebook/commitment 两个局部更新；最后转到 prior 生成路径。

**图没有证明什么**：图不证明 STE 无偏，不证明 code utilization 高就有好语义，也不证明好的重构自动产生好的生成 prior。

## 十二、本节回顾与训练

- VQ 把连续 encoder output 映射到有限 codebook，整数 index 才是 token；
- hard nearest-neighbor 真实导数几乎处处为零，STE 是代理梯度；
- reconstruction、codebook、commitment 三项更新职责不同；
- EMA、gradient、reset 和初始化属于优化器合同；
- VQ autoencoder 之外还需 learned prior 才能生成；
- [[习题 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]
- [[解答 - VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]
