---
type: synthesis
status: verified
area: [generative-models, multimodal, image-tokenization, autoregressive, masked-modeling]
node_id: GEN-63
prerequisites: ["[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]", "[[Absorbing-state、Mask Diffusion 与并行迭代生成]]", "[[Teacher Forcing、暴露偏差与生成时分布漂移]]"]
related: ["[[Latent Diffusion、压缩瓶颈与两阶段误差]]", "[[DDCM、离散生成路线比较与证据地图]]"]
sources: ["[[S-2017-Oord-VQ-VAE]]", "[[S-2022-Chang-MaskGIT]]", "[[S-2024-Su-10197-多模态自回归]]", "[[S-2019-Su-6760-VQ-VAE简明介绍]]"]
exercises: ["[[习题 - 图像 Token、掩码生成与多模态条件分布]]"]
solutions: ["[[解答 - 图像 Token、掩码生成与多模态条件分布]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-image-token-multimodal-factorization-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# 图像 Token、掩码生成与多模态条件分布

> [!abstract] 一句话结论
> 把图像变成 tokens 只解决了“表示成有限 alphabet”的接口，尚未决定 joint distribution 怎样分解。Raster autoregressive、block/interleaved ordering、masked refinement 和 discrete diffusion 对应不同条件化结构与采样程序。多模态统一序列可以共享 Transformer，但 token 语义、位置、损失尺度和条件方向仍需显式设计。

## 一、从图像到 token sequence

令 tokenizer $T$ 把图像 $x$ 编为二维 token grid：

$$
K=T(x)\in\{1,\ldots,V\}^{h\times w}.
$$

选择一个 bijective ordering $\pi:\{1,\ldots,n\}\to\{1,
\ldots,h\}\times\{1,\ldots,w\}$，$n=hw$，得到 sequence

$$k_r=K_{\pi(r)}.$$

常见 raster order 先行后列，但 Hilbert curve、block order、coarse-to-fine 或 learned order 都可以。排序不改变无条件 joint distribution 的存在，却改变条件分布的难度、context locality、parallelism 和 finite model inductive bias。

## 二、自回归分解是恒等式，模型质量不是

任意 ordering 下，chain rule 给出

$$
p(k_{1:n})=\prod_{r=1}^np(k_r\mid k_{<r}).
$$

这是概率恒等式；它不说明 raster order 最优，也不说明有限 Transformer 能同样容易学所有 order。

条件文本 $y$ 下：

$$
p(k_{1:n}\mid y)
=\prod_{r=1}^np(k_r\mid k_{<r},y).
$$

若最终要 joint text-image model，可选择

$$p(y,k)=p(y)p(k\mid y)$$

或

$$p(y,k)=p(k)p(y\mid k),$$

甚至 interleaved factorization。它们表示同一 joint 的不同 chain rule 只在模型无限精确时等价；训练数据、attention mask 和 loss weighting 会让有限模型表现不同。

## 三、三个小例子理解 ordering

设 $2\times2$ tokens 为

$$
\begin{matrix}
a&b\\
c&d
\end{matrix}.
$$

Raster order 给

$$p(a)p(b\mid a)p(c\mid a,b)p(d\mid a,b,c).$$

Column order 给

$$p(a)p(c\mid a)p(b\mid a,c)p(d\mid a,c,b).$$

若 $b$ 与 $d$ 强相关，column order 会让生成 $d$ 时早已看到 $b$，但生成 $b$ 时没看到 $d$；双向 masked model 在预测某一 masked token 时可同时看四周。没有 order 能让所有 token 同时看到未来，除非改变训练/采样范式。

## 四、masked image token modeling

随机选择 mask set $M\subseteq\{1,
\ldots,n\}$，输入 $k_{\bar M}$ 与 mask symbols，训练

$$
\mathcal L_{mask}
=-\mathbb E_M\sum_{r\in M}
\log p_\theta(k_r\mid k_{\bar M},M,y).
$$

它让每个位置利用双向上下文，适合 inpainting 与并行 refinement。若一次采整个 $M$，常用 factorization

$$
p_\theta(k_M\mid k_{\bar M},y)
\approx\prod_{r\in M}p_\theta(k_r\mid k_{\bar M},M,y).
$$

真正的 joint conditional 一般不因子化；多轮 MaskGIT 通过重新预测/遮掩来协调。训练 mask distribution 与推理 trajectory 若差异很大，会形成另一种 exposure mismatch。

## 五、discrete diffusion prior

若 tokens 在每个位置按已知 $Q_t$ corruption，可训练

$$p_\theta(k_{t-1}\mid k_t,y)$$

或 $p_\theta(k_0\mid k_t,t,y)$。它与 masked modeling 的区别在于：

- 有显式 time/noise schedule；
- forward/reverse Markov chain 定义完整 generative process；
- 可写 ELBO 或 ratio objective；
- sampler steps 与 transition kernel 受 schedule 约束。

absorbing mask D3PM 是二者的交叉点，但普通 random-mask CE 不自动带出完整 reverse posterior。

## 六、统一 Transformer 仍需 modality contract

把文本和图像 tokens 拼接：

$$s=[\text{BOS},y_1,
\ldots,y_m,\text{BOI},k_1,
\ldots,k_n,\text{EOI}].$$

至少明确：

1. vocabulary 是共享还是分区；
2. modality/type embeddings；
3. 1D text position 与 2D image position 怎样编码；
4. attention mask 允许哪些方向；
5. text/image loss 如何加权；
6. tokenizer 是否冻结；
7. image token length 是否挤占 text context；
8. condition dropout、classifier-free 路径是否存在。

共享参数只说明函数模块复用，不证明两种模态已经对齐。对齐来自配对数据、objective、cross-modal attention 与优化结果。

## 七、科学空间 10197 的采用与边界

[[S-2024-Su-10197-多模态自回归]] 讨论把图像 patch/token 纳入自回归 sequence，以及 ordering 如何改变条件建模难度。课程采用其“图像也可看作序列随机变量”和“生成/理解可共享 joint modeling”的问题视角。

但必须分级：

- chain rule 与 fixed-variance Gaussian 下 MSE 对应 NLL 是可推导恒等式；
- 某种 ordering/架构的优劣是实验问题；
- “生成会促进理解”是研究假说，需要 matched-data、matched-compute、多任务消融验证；
- continuous patch regression、discrete token CE 与 diffusion loss 不是同一 objective。

## 八、tokenizer 质量如何影响多模态模型

### 8.1 Sequence length

下采样因子 $f$ 给 $n=HW/f^2$ tokens。减小 $f$ 保留细节但 attention/AR 长度上升；增大 $f$ 降成本但 representation bottleneck 加重。

### 8.2 Vocabulary 与 semantic load

大 $V$ 可减少 quantization error，但每个 softmax 更大、assignment 更稀疏。若 code 主要描述纹理，语言条件需要通过多 token 组合表达对象；若 code 更语义化，重构细节可能损失。

### 8.3 Frozen vs joint training

冻结 tokenizer 稳定 prior target，却把 representation ceiling 固定；joint training 可适配任务，但 code identities 漂移，使 prior 面临 non-stationary targets。若重训 tokenizer，旧 token dataset/cache 和 prior checkpoint 可能失效。

## 九、条件方向与任务

同一 joint 模型可形成不同 query：

| 任务 | 概率对象 | sampler/decoder |
|---|---|---|
| text-to-image | $p(k\mid y)$ | AR/mask/diffusion + image decoder |
| image caption | $p(y\mid k)$ | text AR |
| image editing | $p(k_M\mid k_{\bar M},y)$ | masked/conditional diffusion |
| visual QA | $p(a\mid k,q)$ | text AR/classifier |
| unconditional image | $p(k)$ | token prior + decoder |

“一个模型支持多任务”要检查是否实际训练相应 conditional、mask 和 decoding policy；从 joint distribution 的数学可能性不能直接推出 zero-shot 能力。

## 十、四类评估不可混写

1. **Tokenizer**：reconstruction distortion/rFID、token length、entropy；
2. **Prior likelihood**：token NLL/perplexity 或 diffusion bound；
3. **Conditional alignment**：caption/prompt consistency、grounding、human preference；
4. **System**：sequential depth、NFE、KV cache、throughput、decoder cost。

若两个系统 tokenizer 不同，直接比较 token perplexity 没有共同单位；一个容易预测但信息贫乏的 tokenizer 可能 perplexity 更低。

## 十一、图：同一 token grid 的四种概率分解

先看图回答：哪种路线必须选单向 ordering？哪种路线一次能看双向 context？哪一层的误差来自 tokenizer 而不是 prior？

![[00-知识库管理/_assets/figures/generative-models/fig-image-token-multimodal-factorization-v1.svg|900]]

> [!figure] 图 50.8-07　图像 token 的 ordering、mask、diffusion 与多模态 joint
> 左侧从图像到 token grid，中间并排画 raster AR、masked refinement 与 discrete diffusion，右侧画 text–image 条件方向和四类评价。来源：据 VQ-VAE、MaskGIT、科学空间 10197 与本节推导独立绘制。

**怎样读图**：先固定同一个 tokenizer output，再横向比较 prior 如何因子化；随后看 text 条件放在 joint 的哪一侧，最后对齐评价层。

**图没有证明什么**：图不证明统一序列必然产生跨模态对齐，不证明 masked sampler 是 exact joint sampler，也不证明某 ordering 对所有分辨率和任务最优。

## 十二、本节回顾与训练

- tokenizer 决定 alphabet/sequence，prior 决定 joint factorization；
- chain rule 对任意 order 成立，但有限模型学习难度不同；
- masked parallel generation 用同轮 factorization + 多轮协调换取短顺序深度；
- multimodal unified Transformer 仍需 type、position、mask、loss 和 direction 合同；
- tokenizer、prior、alignment、system 四类评估必须分开；
- [[习题 - 图像 Token、掩码生成与多模态条件分布]]
- [[解答 - 图像 Token、掩码生成与多模态条件分布]]
