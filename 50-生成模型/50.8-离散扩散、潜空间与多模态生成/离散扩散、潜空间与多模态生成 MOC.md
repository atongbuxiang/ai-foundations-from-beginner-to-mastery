---
type: moc
status: active
area: [generative-models, discrete-diffusion, latent-diffusion, tokenization, multimodal]
aliases: [生成模型第八卷, 离散与潜空间生成课程地图]
prerequisites: ["[[DDPM、DDIM 与离散时间扩散 MOC]]", "[[SDE、概率流 ODE 与 Flow Matching MOC]]", "[[常用离散分布]]", "[[条件概率、全概率与 Bayes 公式]]", "[[矩阵函数与矩阵指数]]"]
related: ["[[生成模型 MOC]]", "[[生成模型完整课程地图与掌握标准]]", "[[科学空间 - 第五章生成模型专题来源地图]]"]
created: 2026-08-25
updated: 2026-08-25
---

# 离散扩散、潜空间与多模态生成 MOC

> [!abstract] 分卷目标
> 本卷回答一个经常被混成一句话的问题：**“生成 token”究竟是在离散状态空间上建模、先把数据量化成 token、在连续压缩 latent 上扩散，还是把采样随机性编码成索引？** 我们从有限状态转移矩阵和 Bayes 后验开始，进入 absorbing mask 与 CTMC probability ratio；再建立 VQ/FSQ tokenizer、latent diffusion、视觉 token 与多模态条件分布；最后用 DDCM 把四条路线放进同一证据地图。课程对象、训练目标、采样器和评价四层始终分账。

## 一、八个核心节点

| ID | 节点 | 主要出口 | 状态 |
|---|---|---|---|
| GEN-57 | [[Categorical Diffusion、转移矩阵与离散后验]] | 由 $Q_t,\bar Q_t$ 推出闭式边缘、Bayes 后验与 D3PM ELBO | verified |
| GEN-58 | [[Absorbing-state、Mask Diffusion 与并行迭代生成]] | 区分 absorbing Markov kernel、masked objective 与 confidence refinement | verified |
| GEN-59 | [[连续时间 Markov 链、离散 Score 与采样]] | 用 generator、reverse rate 与 probability ratio 定义离散 score | verified |
| GEN-60 | [[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]] | 分开 hard forward、surrogate backward、codebook update 与 prior | verified |
| GEN-61 | [[Codebook Collapse、FSQ、Rotation、SimVQ 与 DiVeQ]] | 比较五类量化/梯度设计及其证据边界 | verified |
| GEN-62 | [[Latent Diffusion、压缩瓶颈与两阶段误差]] | 建立 pixel—latent 计算账和不可恢复信息边界 | verified |
| GEN-63 | [[图像 Token、掩码生成与多模态条件分布]] | 从 tokenizer 到 AR/masked/conditional joint 的完整对象合同 | verified |
| GEN-64 | [[DDCM、离散生成路线比较与证据地图]] | 比较 state、representation、latent 与 randomness 四种离散化 | verified |

## 二、先分清四种“离散”

| 路线 | 被离散化的对象 | 学习对象 | 典型输出 | 不能自动推出 |
|---|---|---|---|---|
| D3PM / mask diffusion | 数据状态 $x_t\in\{1,\ldots,K\}$ | reverse transition / clean-token posterior | 状态序列 | 有语义 tokenizer |
| VQ / FSQ | encoder latent $z=E(x)$ | encoder、decoder、quantizer | code index grid | 已学好 code prior |
| LDM | 通常是连续压缩 latent $z\in\mathbb R^{h\times w\times c}$ | latent score/denoiser | 连续 latent | 离散 token 或无损重构 |
| DDCM | reverse diffusion 的随机噪声选择 | 通常复用预训练 diffusion | 每步 noise code index | 局部语义 token 或 D3PM transition |

“都可写成整数序列”只是表示格式相似，不是概率模型等价。

## 三、全卷统一离散时间记号

有限 alphabet $\mathcal X=\{1,\ldots,K\}$。分布统一写成 **行向量**，转移矩阵统一为 row-stochastic：

$$
Q_t[i,j]=q(x_t=j\mid x_{t-1}=i),
\qquad Q_t\mathbf 1=\mathbf 1.
$$

令 $e_i$ 是第 $i$ 个 one-hot 行向量，累计核

$$
\bar Q_t=Q_1Q_2\cdots Q_t.
$$

因此

$$
q(x_t=\cdot\mid x_0=i)=e_i\bar Q_t.
$$

给定观测 $x_t=j$ 和干净状态 $x_0=k$，离散 Bayes 后验是

$$
q(x_{t-1}=i\mid x_t=j,x_0=k)
=\frac{(e_k\bar Q_{t-1})_iQ_t[i,j]}
{(e_k\bar Q_t)_j}.
$$

若读到 column-vector convention，则所有乘法方向和矩阵都要统一转置；不能一半沿用论文、一半沿用本卷。

## 四、连续时间跳跃过程记号

CTMC generator 记为 $R_t$：

$$
R_t[i,j]\ge0\quad(i\ne j),
\qquad R_t[i,i]=-\sum_{j\ne i}R_t[i,j].
$$

行分布 $p_t$ 满足 forward equation

$$
\frac{d}{dt}p_t=p_tR_t.
$$

在 $p_t(j)>0$ 时，从状态 $j$ 反向跳到 $i$ 的精确 rate 为

$$
R_t^{rev}[j,i]=R_t[i,j]\frac{p_t(i)}{p_t(j)}.
$$

因此离散 score 的自然对象是边上的 probability ratio，而不是 $\nabla_x\log p_t(x)$；离散 alphabet 本身没有默认欧氏微分结构。

## 五、Tokenizer 的三份合同

任何 hard quantizer 都要分开写：

1. **前向合同**：送入 decoder 的究竟是 nearest code、rounded coordinate 还是带噪替代物；
2. **反向合同**：真实导数、STE、rotation、DiVeQ 等代理 Jacobian 是哪一个；
3. **参数更新合同**：codebook 用梯度、EMA、K-means 初始化、reseed 还是共享基底更新。

一个模型前向完全相同，也可能因代理梯度和优化器不同而训练成不同函数。相反，前向训练—推理不一致也不能靠“梯度可传”四个字掩盖。

## 六、两阶段生成误差账

令 encoder/quantizer 为 $T$，decoder 为 $D$，code prior 为 $p_\theta(c)$。生成过程是

$$
c\sim p_\theta(c),\qquad \hat x=D(c).
$$

至少保留四本账：

| 误差 | 问题 | 典型观测 |
|---|---|---|
| representation | $x$ 经 $T,D$ 后丢了什么 | reconstruction distortion、感知/语义误差 |
| prior | $p_\theta(c)$ 是否学到真实 token distribution | token NLL、sample coverage |
| sampler | finite AR/mask/diffusion steps 怎样近似 prior | NFE、顺序、温度、重遮掩 |
| decoder/evaluation | decoder artifacts 与指标偏好 | rFID、FID、rate–distortion、人评 |

重构好是好 tokenizer 的必要证据之一，但不是 prior 生成好的充分条件；sample FID 好也不能说明编码可逆或码率合理。

## 七、科学空间研读主线

| 文章 | 本卷作用 | 课程补严 |
|---|---|---|
| [[S-2019-Su-6705-从正态分布到Gumbel-Softmax]]、[[S-2022-Su-9085-从重参数看离散概率分布]] | noise-argmax、松弛与离散概率构造 | exact sample、relaxed sample、gradient estimator 分开 |
| [[S-2019-Su-6760-VQ-VAE简明介绍]] | VQ、STE、code loss 与 second-stage prior | 名称含 VAE 不等于标准连续 ELBO |
| [[S-2023-Su-9826-FSQ]] | scalar quantization 与 implicit codebook | “超越”限定论文协议与 code size |
| [[S-2024-Su-10489-VQ旋转技巧]]、[[S-2024-Su-10519-VQ编码表线性变换]] | surrogate Jacobian 与 optimizer path | 理论优雅、表达等价、训练改善三者分层 |
| [[S-2025-Su-11328-DiVeQ]] | 无显式 Aux Loss 的 VQ 梯度设计 | 博客机制推导标为分析/假说 |
| [[S-2025-Su-10711-DDPM离散编码]] | DDCM 的 noise-code 索引视角 | 与 D3PM、VQ、FSQ 对象严格区分 |
| [[S-2024-Su-10197-多模态自回归]] | image-as-sequence、ordering 与多模态 joint 设计 | 博客设想、实验证据与概率恒等式分层 |

一级定义由 [[S-2021-Austin-D3PM]]、[[S-2022-Campbell-Discrete-CTMC]]、[[S-2024-Lou-SEDD]]、[[S-2017-Oord-VQ-VAE]]、[[S-2024-Mentzer-FSQ]]、[[S-2022-Rombach-LDM]]、[[S-2022-Chang-MaskGIT]] 与 [[S-2025-Ohayon-DDCM]] 承担。

## 八、当前出口

- 数值审计：[[实验 - 离散扩散、量化与潜空间两阶段最小审计]]
- 累计门：[[50.8 分卷累计测验与复现门]]
- 前置卷：[[SDE、概率流 ODE 与 Flow Matching MOC]]
- 后继：[[生成模型完整课程地图与掌握标准#十二、50.9 采样器、条件控制、加速与评估（GEN-65—72）|50.9 采样、控制、加速与评价]]
