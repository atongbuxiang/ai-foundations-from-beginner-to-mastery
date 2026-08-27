---
type: concept
status: draft
area: [architecture, transformer, vision-transformer, patch-embedding]
aliases: [Vision Transformer, ViT, Patch Tokenization]
node_id: ARCH-38
prerequisites: ["[[Transformer Encoder 与双向表示]]", "[[局部连接、参数共享与平移等变性]]"]
related: ["[[Transformer 架构与组合方式 MOC]]", "[[Transformer 形状、参数量与 FLOPs 总账]]", "[[结构化输入、归纳偏置与架构比较坐标]]", "[[位置编码、结构编码与长度外推 MOC]]"]
sources: ["[[S-2021-Dosovitskiy-ViT]]", "[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2024-Su-10347-位置编码与置换对称]]"]
exercises: ["[[习题 - Vision Transformer、Patch Token 与二维结构]]"]
solutions: ["[[解答 - Vision Transformer、Patch Token 与二维结构]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-vit-patch-tokenization-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Vision Transformer、Patch Token 与二维结构

> [!abstract] 本节主问题
> ViT 的第一步不是“让 Transformer 直接看像素”，而是先规定二维图像如何变成一维 token 序列。Patch 大小决定序列长度、每个 token 的感受范围、细节损失和 attention 二次成本；位置表示负责补回 patchification 丢失的空间次序。

## 一、从图像张量到 Patch 矩阵

令一批图像为

$$
I\in\mathbb R^{B\times H\times W\times C},
$$

使用不重叠的 $P\times P$ patch，先假设 $P\mid H$ 且 $P\mid W$。网格大小与 patch 数为

$$
H_p=\frac HP,\qquad W_p=\frac WP,\qquad N=H_pW_p.
$$

每个 patch 展平成 $P^2C$ 维向量：

$$
X_{patch}\in\mathbb R^{B\times N\times(P^2C)}.
$$

线性投影到模型维度 $d$：

$$
Z_0=X_{patch}E+b,
\qquad E\in\mathbb R^{P^2C\times d},
\qquad Z_0\in\mathbb R^{B\times N\times d}.
$$

若加入一个 class token，送入 encoder 的长度是 $T=N+1$；若不用，则 $T=N$。

## 二、Patch Embedding 与卷积的精确等价

把投影 $E$ 的每个输出列重排成 $P\times P\times C$ kernel，就得到一个 kernel size $P$、stride $P$、输出通道 $d$ 的卷积。两者在同样 padding 与展平顺序下给出相同数值。

但这只是**第一层线性算子的实现等价**，不表示整个 ViT 具有 CNN 的全部归纳偏置。标准 ViT 后续全局 self-attention 不强制局部邻域，不天然具有卷积的平移等变与逐层扩大感受野结构。

## 三、二维空间如何进入序列

Patch 本身保留 $P\times P$ 局部像素，但把 $N$ 个 patch 排成序列后，self-attention 若没有 position 信息，对 token 排列具有置换等变性。常见处理包括：

- learned absolute position embedding；
- 二维相对位置 bias；
- 分解为 row/column position；
- 旋转或其他结构化 position encoding。

若使用一维绝对位置向量，必须声明二维网格到序号的映射，例如 row-major：

$$
n=rW_p+c.
$$

相邻序号不总是二维相邻：每行末尾到下一行开头在序号上相邻，却在图像中相距较远。

## 四、分辨率变化与位置插值合同

预训练在 $H_p\times W_p$ 网格、微调在 $H'_p\times W'_p$ 时，learned absolute grid 通常需：

1. 将 class token position 与 patch positions 分离；
2. 把 patch position reshape 回二维网格；
3. 在二维网格插值；
4. 再 flatten 并拼回 class position。

插值是工程选择，不保证学习到的空间函数真正可在任意分辨率外推。若训练/测试 aspect ratio、crop policy 或 patch alignment 改变，也可能产生位置错位。

## 五、不能整除时怎么办

若 $H$ 或 $W$ 不能被 $P$ 整除，必须显式选择：

- crop：丢弃边缘信息；
- pad：增加人工边界与 padding tokens；
- resize：改变图像几何/频率；
- variable/overlapping patches：改变 token 数与算子定义。

不能静默使用整数除法后仍声称覆盖了全部像素。对 padding patch，还需决定是否参与 attention 与 pooling。

## 六、Patch Size 的四笔账

固定 $H,W,C,d$，patch size 从 $P$ 改为 $2P$：

$$
N' = \frac{H}{2P}\frac{W}{2P}=\frac N4,
$$

所以 attention pair 数约降为 $1/16$。但每个 patch input dimension 从 $P^2C$ 变为 $4P^2C$，patch projection 参数从 $P^2Cd$ 增为 $4P^2Cd$；同时细小物体、边缘和局部纹理更早被压缩进单个 token。

反过来，若 $H,W$ 各翻倍而 $P$ 不变，则 $N$ 变为 $4N$、attention pairs 变为约 $16N^2$。因此“分辨率只翻倍”对全局 attention 不是两倍成本。

## 七、读出：Class Token 不是唯一答案

分类可使用：

- class token 的最终表示；
- 所有 patch tokens 的 mean pooling；
- attention pooling；
- 多尺度/局部 heads。

Class token 是一个可训练 query-like 汇聚槽位，但它仍通过多层 self-attention 间接收集信息。其 attention weights 不自动等于忠实区域解释。

检测、分割等 dense task 往往要保留二维 token grid，再经 decoder/FPN/upsampling 还原空间分辨率；只保留 class token 会丢失逐位置出口。

## 八、增强与几何一致性

Random crop、resize、flip、mixup/cutmix 会改变 patch 内像素与 patch 间几何。训练流水线必须同时检查：

- 图像增强之后才 patchify，还是 token 后增强；
- position grid 是否与最终 crop 对齐；
- label 是否对空间变换保持有效；
- padding/crop 产生的边界是否进入 pooling。

ViT 缺少部分卷积先验并不等于“没有任何先验”：patch size、共享 patch projection、position scheme、augmentation 与 class token 都是人为结构选择。

## 九、原论文证据怎样读

[[S-2021-Dosovitskiy-ViT]] 展示纯 Transformer encoder 在大规模监督预训练后对图像分类迁移的强结果。可采用的结论是：在论文的数据、模型和训练协议下，该架构能够达到有竞争力表现 `E`。

不能改写成：任何规模数据上 ViT 都优于 CNN；patchification 不损失信息；全局 attention 自动学到平移等变；或 class attention 是因果解释。这些都需新的条件或实验。

## 十、图：二维图像怎样变成 Token

先看图回答：$224\times224$ 图像取 $16\times16$ patch 会产生多少个 patch tokens？当 patch 变大一倍时，为何 attention pair 数约降到原来的 $1/16$？

![[00-知识库管理/_assets/figures/architecture/fig-vit-patch-tokenization-v1.svg|900]]

> [!figure] 图 40.5-06　ViT 的 patchification、位置注入与成本变化
> 图从二维网格、flatten/projection、class token 与 position 到 encoder input 登记完整 shape。来源：依据 ViT 的 patch embedding 定义独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_transformer_v1.py]] 生成。

**怎样读图**：先数横纵 patch 网格得到 $N$，再检查每个 patch 的输入维 $P^2C$ 和投影输出 $d$；最后把 $T=N$ 或 $N+1$ 代入 attention 的 $T^2$ 项。不要从图像像素数直接跳到 Transformer 长度。

**图没有证明什么**：图不证明大 patch 在质量上更好，也不证明一维位置插值能无损外推到任意分辨率或 aspect ratio。

## 十一、常见错误与掌握标准

常见错误：忘记 class token 导致序列长少一；把 patch projection 参数误写成 $Nd$；声称卷积实现让 ViT 获得完整 CNN 偏置；分辨率翻倍只把 attention 成本乘二；忽略不能整除与 position 插值；用 class attention 直接作因果归因。

> [!summary]
> ViT 先把 $H\times W\times C$ 图像变为 $N=(H/P)(W/P)$ 个 $P^2C$ 向量，再投影为 $d$ 维 tokens。Patch projection 可由 stride-$P$ 卷积等价实现；patch size 同时控制细节、参数与 $N^2$ 成本；二维位置与分辨率变化必须有显式合同。

能手算 patch shapes（A/B）、推导 patch/attention 成本缩放（C）、构造位置错位与边界反例（D），并审计一个视觉训练流水线的数据—几何—成本证据（E）。

## 十二、练习与独立详解

- [[习题 - Vision Transformer、Patch Token 与二维结构]]
- [[解答 - Vision Transformer、Patch Token 与二维结构]]

## 参考来源

- [[S-2021-Dosovitskiy-ViT]]
- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2024-Su-10347-位置编码与置换对称]]
