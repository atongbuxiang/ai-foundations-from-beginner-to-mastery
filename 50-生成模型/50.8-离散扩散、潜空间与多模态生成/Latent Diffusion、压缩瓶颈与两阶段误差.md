---
type: derivation
status: verified
area: [generative-models, latent-diffusion, autoencoder, systems]
node_id: GEN-62
prerequisites: ["[[DDPM、DDIM 与离散时间扩散 MOC]]", "[[自编码器、重构与生成缺口]]", "[[VQ-VAE、离散 Tokenizer 与 Straight-Through Estimator]]"]
related: ["[[图像 Token、掩码生成与多模态条件分布]]", "[[DDCM、离散生成路线比较与证据地图]]"]
sources: ["[[S-2022-Rombach-LDM]]", "[[S-2019-Su-6760-VQ-VAE简明介绍]]"]
exercises: ["[[习题 - Latent Diffusion、压缩瓶颈与两阶段误差]]"]
solutions: ["[[解答 - Latent Diffusion、压缩瓶颈与两阶段误差]]"]
figure: "[[00-知识库管理/_assets/figures/generative-models/fig-latent-diffusion-compression-error-v1.svg]]"
created: 2026-08-25
updated: 2026-08-25
---

# Latent Diffusion、压缩瓶颈与两阶段误差

> [!abstract] 一句话结论
> Latent Diffusion Model（LDM）先用有损 autoencoder 把像素压成较小的连续 latent，再在 latent 上训练 diffusion。它以 representation bottleneck 换取计算节省；任何被 encoder–decoder 丢弃的信息都不可能由完美 latent prior 重新恢复。LDM 的 latent 通常连续，不能因为名字叫 latent 就当作 VQ token。

## 一、Pixel diffusion 的成本从哪里来

输入图像

$$x\in\mathbb R^{H\times W\times3}$$

若 diffusion U-Net 直接在像素分辨率工作，feature map 的主要 activation/卷积成本随空间位置数 $HW$ 增长。高分辨率还要求更大 receptive field 和更多多尺度 block。

LDM 先训练 encoder/decoder：

$$
z=E_\phi(x)\in\mathbb R^{h\times w\times c},
\qquad \hat x=D_\psi(z),
$$

常有 $h=H/f,w=W/f$。若 channel/architecture 近似不变，仅看空间位置，latent 主干的位置数缩小约

$$
\frac{HW}{hw}=f^2.
$$

但真实 speedup 不等于 $f^2$：latent channels $c$、attention resolution、decoder cost、memory bandwidth、batch size 和硬件 kernel 都会改变结果。

## 二、first stage 究竟学什么

autoencoder objective 常组合：

$$
\mathcal L_{AE}
=\lambda_{rec}\mathcal L_{pixel}
+\lambda_{perc}\mathcal L_{perceptual}
+\lambda_{adv}\mathcal L_{GAN}
+\lambda_{reg}\mathcal L_{latent}.
$$

不同项承担不同偏好：

- pixel loss 约束逐点 fidelity；
- perceptual loss 约束 pretrained feature 相似；
- adversarial loss 鼓励局部真实感，却可能 hallucinate；
- latent regularization 让 $z$ 的分布/尺度适合 second stage。

[[S-2022-Rombach-LDM]] 比较了不同 compression factors，核心不是“压得越小越好”，而是在细节保持与计算节省之间找工作点。

## 三、continuous latent 与 discrete token 的区别

### 3.1 KL-regularized continuous latent

encoder 输出连续 $z$，可能对 posterior 参数化并施加接近 Gaussian prior 的 KL regularization。diffusion 直接在 $\mathbb R^{h\times w\times c}$ 加 Gaussian noise。

### 3.2 VQ-regularized discrete latent

encoder 输出先 nearest-neighbor 到 codebook，得到离散 indices 和 code vectors。若 diffusion 在 code vectors 的连续 embedding 上加 Gaussian noise，状态在加噪后又离开有限 codebook；若在 indices 上用 transition matrix，则是 discrete diffusion。

所以必须写清：

| 问题 | 可能答案 |
|---|---|
| clean latent 是否离散 | continuous / codebook vector |
| noisy state 是否离散 | Gaussian continuous / categorical token |
| forward corruption | Gaussian kernel / stochastic matrix |
| decoder 输入 | continuous $z$ / code lookup |

“在 VQ latent 上做 diffusion”这句话不足以确定模型。

## 四、latent diffusion objective

冻结或联合处理 first stage 后，对数据 latent $z_0=E(x)$ 定义 Gaussian forward：

$$
z_t=\sqrt{\bar\alpha_t}z_0
+\sqrt{1-\bar\alpha_t}\varepsilon,
\qquad \varepsilon\sim N(0,I).
$$

噪声预测 objective：

$$
\mathcal L_{LDM}
=\mathbb E_{x,t,\varepsilon}
\left[\|\varepsilon-\varepsilon_\theta(z_t,t,c)\|_2^2\right],
$$

其中 $c$ 是可选 condition。生成：

$$z_T\sim N(0,I)\to z_0^{gen}\to x^{gen}=D(z_0^{gen}).$$

这与 pixel DDPM 的数学形式相同，但 data distribution 换成 encoder-induced $q_E(z)$，metric/scale 由 first stage 决定。

## 五、latent scale 为什么是模型合同

若 encoder latents 每维 variance 远离 1，却仍使用假定 unit-scale 的 noise schedule，实际 signal-to-noise ratio 会错位。常见实现用固定缩放 $s$：

$$\tilde z=sE(x),$$

使训练 latent 的方差量级合适。生成后 decoder 输入要除回 $s$。

因此 checkpoint 不只是 U-Net 权重，还包括：encoder、decoder、latent scale、normalization、posterior sampling/mean policy 和 downsampling factor。漏掉 scale 能让公式完全正确而图像完全错误。

## 六、条件如何进入：以 cross-attention 为例

条件 encoder 给序列

$$C\in\mathbb R^{m\times d_c}.$$

U-Net feature 展平为

$$H\in\mathbb R^{n\times d_h}.$$

cross-attention：

$$
Q=HW_Q,\quad K=CW_K,\quad V=CW_V,
$$

$$
\operatorname{Attn}(H,C)
=\operatorname{softmax}\left(\frac{QK^\top}{\sqrt d}\right)V.
$$

它允许 latent spatial positions 查询 text/layout condition。cross-attention 只是条件注入架构，不等于条件概率已精确学到，也不保证 prompt-grounding；classifier-free guidance 等采样控制留到 50.9。

## 七、两阶段误差的形式分解

设真实图像 $X$，表示重构

$$X^{AE}=D(E(X)).$$

latent model 生成 $Z^\theta$，最终

$$X^\theta=D(Z^\theta).$$

对任意满足三角不等式的距离 $d$，可插入一个理想 latent sample $Z^*=E(X^*)$：

$$
d(X^*,D(Z^\theta))
\le d(X^*,D(E(X^*)))
+d(D(E(X^*)),D(Z^\theta)).
$$

第一项是 representation/decoder floor；第二项包含 latent prior 和 decoder sensitivity。若 decoder 对 latent 是 $L_D$-Lipschitz，还可粗界

$$
d(D(z),D(z'))\le L_D\|z-z'\|.
$$

但感知距离往往不是简单范数，decoder 也可能局部高敏感；这个上界是审计接口，不是实际 FID 分解公式。

## 八、不可恢复信息：一个反例

假设 encoder 把所有 $2\times2$ checkerboard 高频模式平均池化成同一个常数 latent。两张图 $x^{(a)},x^{(b)}$ 的低频相同、高频相反，却满足

$$E(x^{(a)})=E(x^{(b)}).$$

无论 latent diffusion 多完美，decoder 输入都相同，确定性 decoder 不可能同时精确恢复两张。若 decoder 随机 hallucinate 高频，它最多按 conditional distribution 猜测，不能知道原样本丢掉的位。

这就是 data processing 的直觉：second stage 不能从没有被 first stage 保留的信息中恢复 instance-specific truth。

## 九、压缩因子、通道与 bitrate

连续 latent 的“压缩率”不能只用 $f^2$ 表示。原像素浮点维数 $3HW$，latent 浮点维数 $chw$，dimension ratio 是

$$
r_{dim}=\frac{chw}{3HW}=\frac{c}{3f^2}.
$$

但训练中 float tensor 不是压缩 bitstream；若要谈码率，需要量化和 entropy coding。VQ token 的 nominal bits/image 为

$$hw\log_2K,$$

实际可压缩码率取决于 token entropy/prior。不要把 compute compression、representation dimension、lossy codec bitrate 混成同一个“压缩倍数”。

## 十、与 VQ 科学空间文章的接口

[[S-2019-Su-6760-VQ-VAE简明介绍]] 把离散 tokenizer 与 second-stage prior 分开；LDM 也有 first/second stage，但 second stage 多在连续 latent 上建模。两者共享“先压缩再生成”的工程范式，却有不同的状态空间、forward noise、loss 和 rate 解释。

一个可靠的项目报告应先写 first-stage reconstruction table，再写 latent model table，最后写 end-to-end generation；不能只展示最终样本图而省略 bottleneck floor。

## 十一、图：计算节省与不可恢复误差同时出现

先看图回答：空间下采样在哪一步节省 diffusion 主干计算？representation floor 又在哪一步已经确定？

![[00-知识库管理/_assets/figures/generative-models/fig-latent-diffusion-compression-error-v1.svg|900]]

> [!figure] 图 50.8-06　Latent diffusion 的计算—信息—误差三账
> 左侧比较 pixel/latent tensor shape，中间画 first-stage bottleneck 与 second-stage diffusion，右侧分解 representation、prior、solver、decoder/evaluation 误差。来源：据 LDM 原论文与本节推导独立绘制。

**怎样读图**：先沿尺寸箭头算 $HW\to hw$，再沿生成箭头看 $z_T\to z_0\to x$；最后看哪些误差在 first stage 已不可逆，哪些属于 learned prior/sampler。

**图没有证明什么**：图不证明 $f^2$ 的理论 wall-clock 加速，不证明感知 autoencoder 保留所有任务信息，也不证明 latent diffusion 与 pixel diffusion 在无限容量下具有相同最优分布。

## 十二、本节回顾与训练

- LDM 多在连续压缩 latent 上做 Gaussian diffusion；latent 不等于 token；
- 空间下采样节省主干计算，却设定 representation floor；
- latent scaling、encoder/decoder 与 schedule 同属 checkpoint 合同；
- computation compression、dimension ratio 与 codec bitrate 是不同量；
- 两阶段报告必须先 tokenizer/AE，再 latent prior，最后 end-to-end；
- [[习题 - Latent Diffusion、压缩瓶颈与两阶段误差]]
- [[解答 - Latent Diffusion、压缩瓶颈与两阶段误差]]
