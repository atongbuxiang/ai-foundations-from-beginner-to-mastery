---
type: synthesis
status: verified
area: [generative-models, diffusion, compression, evidence-map]
node_id: GEN-64
prerequisites: ["[[DDPM、DDIM 与离散时间扩散 MOC]]", "[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]", "[[Categorical Diffusion、转移矩阵与离散后验]]"]
related: ["[[Latent Diffusion、压缩瓶颈与两阶段误差]]", "[[图像 Token、掩码生成与多模态条件分布]]"]
sources: ["[[S-2025-Ohayon-DDCM]]", "[[S-2025-Su-10711-DDPM离散编码]]", "[[S-2021-Austin-D3PM]]", "[[S-2024-Mentzer-FSQ]]", "[[S-2022-Rombach-LDM]]"]
exercises: ["[[习题 - DDCM、离散生成路线比较与证据地图]]"]
solutions: ["[[解答 - DDCM、离散生成路线比较与证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-ddcm-discrete-route-evidence-map-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# DDCM、离散生成路线比较与证据地图

> [!abstract] 一句话结论
> DDCM 不把图像状态或 encoder latent 量化，而是把预训练 diffusion 反向采样每一步的 Gaussian noise 限制到有限 codebook；noise indices 组成 bit-stream。它展示了“离散编码采样随机性”这一独立路线。与 D3PM、VQ/FSQ、LDM 比较时，必须先对齐被离散化对象、是否需要训练、码率、采样步数和重构定义。

## 一、从 DDPM reverse sampler 开始

标准反向一步写成

$$
x_{t-1}=\mu_\theta(x_t,t)+\sigma_t\varepsilon_t,
\qquad \varepsilon_t\sim N(0,I).
$$

从 $x_T\sim N(0,I)$ 开始，整条 sample 由初始噪声和各步噪声决定。若维度为 $d$、步数为 $T$，可以把 sampler 看成一个确定性映射

$$
F_\theta:(\varepsilon_T,\varepsilon_{T-1},
\ldots,\varepsilon_1)\mapsto x_0.
$$

这里“确定性”是给定所有随机数和模型后输出确定；模型本身仍是随机生成程序。

## 二、DDCM 的有限 noise codebooks

对每一步预先采 $K$ 个 Gaussian vectors：

$$
\mathcal C_t=\{\varepsilon_{t,1},
\ldots,\varepsilon_{t,K}\},
\qquad \varepsilon_{t,k}\overset{iid}{\sim}N(0,I).
$$

固定它们后，反向一步改成

$$
\boxed{x_{t-1}=\mu_\theta(x_t,t)
+\sigma_t\varepsilon_{t,k_t},
\qquad k_t\in\{1,
\ldots,K\}.}
$$

若 $k_t$ 均匀采样，输出由整数序列决定。名义 code length 约

$$B=T\log_2K$$

bits，另加初始 $x_T$ 的处理、模型/codebook 共享成本和 entropy coding overhead。原 DDCM 每个时间步使用独立 codebook；共享单一 codebook 是另一实验，不应默认为等价。

## 三、为什么小 $K$ 仍可能有多样性

即使 $K=2$，长度 $T$ 的 index sequences 也有 $2^T$ 种组合。非线性 denoiser 每一步把当前状态与 code noise 混合，组合可产生大量输出。

但 $K^T$ 只是名义序列数，不能推出：

- 映射 $F_\theta$ 是一一对应；
- 所有组合可产生高质量样本；
- 输出近似均匀或覆盖 data modes；
- 实际 entropy 等于 $T\log K$；
- 小 codebook 在任意 model/sampler 上保持 FID。

[[S-2025-Ohayon-DDCM]] 的“很小 codebook 仍保持质量”是重要实验发现，不是组合计数定理。

## 四、给定目标图像怎样编码

目标是为给定 $x^*$ 找 index sequence，使 DDCM reconstruction 接近 $x^*$。穷举 $K^T$ 不可行。DDCM 把选择看成 conditional generation：在时刻 $t$，denoiser 给当前 clean estimate $\hat x_{0,\theta}(x_t,t)$，残差

$$r_t=x^*-\hat x_{0,\theta}(x_t,t)$$

指出应该往哪里修正。若 code vectors norm 近似相同，可选择

$$
k_t^*=\arg\max_k\langle\varepsilon_{t,k},r_t\rangle.
$$

然后用该 code 完成一步，继续下一时刻。最终 index sequence 是有损编码；decoder 是同一 diffusion sampler 加固定 codebooks。

该 greedy rule 并不全局最优化最终 distortion，因为早期选择会改变后续状态和可选轨迹。它的有效性来自 posterior-guidance 近似与实验，而不是动态规划最优性。

## 五、从 guided Gaussian 到有限集合权重

若目标条件使理想噪声分布从 $N(0,I)$ 平移为

$$N(m_t,I),$$

而我们只能从有限 $\mathcal C_t$ 选择，则一个一致的离散近似是按目标密度重权：

$$
P(k_t=k\mid x_t,x^*)
\propto\exp\left[-\frac12
\|\varepsilon_{t,k}-m_t\|^2\right].
$$

若所有 $\|\varepsilon_{t,k}\|$ 近似相同，展开平方得到

$$
P(k_t=k\mid\cdot)
\propto\exp(\langle\varepsilon_{t,k},m_t\rangle),
$$

最大概率选择才化为最大内积。[[S-2025-Su-10711-DDPM离散编码]] 特别指出：直接 deterministic argmax 在 $K\to\infty$ 时会趋向选择“最补偿残差”的极端 code，不自动恢复原 Gaussian stochastic sampler；按 density 权重采样更接近正确连续极限。

这是一条很重要的方法论：有限 codebook approximation 应问 **$K\to\infty$ 是否恢复目标分布**，而不只看小 $K$ 的单张重构。

## 六、DDCM 的优点与实际瓶颈

### 6.1 优点

- 可复用预训练 DDPM，不必另训 tokenizer；
- index sequence 天然 1D 时间顺序，无需把 2D grid 重新排序；
- sampling 与 compression/conditional generation 在同一构造中；
- codebook 是共享随机性，发送端/接收端只传 indices。

### 6.2 瓶颈

- 编码需要逐步运行 diffusion，速度与 sampler 步数绑定；
- 减少 $T$ 同时减少码长并改变 reconstruction/quality，不能只当普通 acceleration；
- 每步搜索 $K$ 个 $d$ 维 codes，朴素成本 $O(TKd)$；
- codebooks 的存储/共享、seed、dtype 和生成算法属于 codec specification；
- noise code index 未必具备局部语义，作为多模态 LLM token 的可学习性仍需验证。

## 七、四条路线的对象级比较

| 维度 | D3PM / Mask | VQ / FSQ | LDM | DDCM |
|---|---|---|---|---|
| 离散化对象 | 数据/latent token state | encoder representation | 通常不离散，压缩连续 latent | reverse noise choice |
| forward corruption | stochastic matrix / CTMC | 无 diffusion 必需 | Gaussian latent noise | 复用 Gaussian reverse sampler |
| 新训练 | reverse denoiser | tokenizer + prior | autoencoder + latent denoiser | 可复用 pretrained diffusion |
| 编码输出 | corrupted/clean state tokens | spatial code grid | continuous tensor | temporal noise indices |
| 生成步骤 | reverse transitions | prior sample + decoder | latent sampler + decoder | finite-code reverse sampler |
| 主要 floor | reverse/model/schedule | quantization + prior | AE bottleneck + prior | codebook restriction + greedy encode |
| 码率含义 | 需定义序列 coding | token entropy / grid | 非 codec 除非再量化 | index stream + shared model/codebooks |

路线可以组合：例如 VQ tokens 上做 D3PM prior，或 continuous LDM decoder 配合其他 codec。但组合后要重新定义对象，不能沿用单一方法的名义性能。

## 八、证据层级

| 层级 | 可写结论 | 例子 |
|---|---|---|
| I 恒等/定义 | 由程序或代数直接成立 | DDCM 给定 indices 后输出确定；名义序列数 $K^T$ |
| T 条件定理 | 写全假设的概率/极限结论 | density-weighted empirical measure 在条件下逼近目标 |
| E 协议实验 | 数据、checkpoint、steps、metric 下观察 | 小 $K$ 时 FID/重构保持 |
| H 机制假说 | 可证伪解释 | temporal indices 可能更适合 1D prior |
| O 开放问题 | 尚无充分证据 | DDCM 是否可扩展为通用多模态 tokenizer |

科学空间 10711 中的作者复现属于额外 E 级证据；其长期影响判断属于 H/O，不升级为 T。

## 九、最小复现清单

- base diffusion checkpoint、parameterization、$T$、$\sigma_t$；
- 每步 codebook 是否独立、$K,d$、PRNG、seed、dtype；
- $x_T$ 固定/编码/共享策略；
- random generation 是均匀 index 还是 density-weighted；
- encoding objective、greedy/beam/search rule；
- code norm 是否归一、maximum-inner-product 实现；
- nominal/entropy-coded bitrate 与 model/codebook amortization；
- reconstruction distortion、perceptual metric、generation diversity；
- encoding/decoding wall-clock、NFE 与 search cost。

缺任一关键项，“DDCM 只需 K=2”都无法成为可复现实验陈述。

## 十、图：四种离散化到底切在哪里

先看图回答：D3PM、VQ、LDM、DDCM 分别在 data state、representation、continuous latent、randomness 的哪条线上做文章？

![[00-知识库管理/_assets/figures/generative-models/fig-ddcm-discrete-route-evidence-map-v1.svg|900]]

> [!figure] 图 50.8-08　DDCM 与四条离散/潜空间生成路线的对象—证据地图
> 左栏画被离散化对象，中栏画训练与采样路径，右栏按 I/T/E/H/O 标注可主张结论。来源：据 DDCM 原论文、科学空间 10711 与本卷各节点独立绘制。

**怎样读图**：先纵向选择路线，再横向检查“离散发生在哪里”；最后只在对应证据层读取结论，不从组合计数跳到生成质量。

**图没有证明什么**：图不证明 DDCM 是更好的语义 tokenizer，不证明名义 bits 等于实际率失真，也不证明四条路线不能组合或存在普遍最优路线。

## 十一、本节回顾与训练

- DDCM 离散的是 reverse sampler 的 noise choice；
- 小 codebook 的组合数很大，但不等于高质量可达输出同样多；
- greedy max-inner-product encoding 是局部 guidance 近似，不是全局最优证明；
- density-weighted finite sampling 比纯 argmax 更有希望恢复连续极限；
- D3PM、VQ/FSQ、LDM、DDCM 先按对象比较，再谈性能；
- [[习题 - DDCM、离散生成路线比较与证据地图]]
- [[解答 - DDCM、离散生成路线比较与证据地图]]
