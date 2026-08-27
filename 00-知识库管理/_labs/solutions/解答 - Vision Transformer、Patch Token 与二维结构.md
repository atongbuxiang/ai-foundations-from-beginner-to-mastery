---
type: solution
status: draft
area: [architecture, transformer, vision-transformer, patch-embedding]
topic: "[[Vision Transformer、Patch Token 与二维结构]]"
exercise: "[[习题 - Vision Transformer、Patch Token 与二维结构]]"
sources: ["[[S-2021-Dosovitskiy-ViT]]", "[[S-2017-Vaswani-Transformer复杂度]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Vision Transformer、Patch Token 与二维结构

## A. 识别与复述

### ARCH-VIT-A01
整除时
$$
N=(H/P)(W/P),\quad
X_{patch}\in\mathbb R^{B\times N\times P^2C},
\quad
Z=X_{patch}E\in\mathbb R^{B\times N\times d}.
$$
若加 class token，encoder length 为 $T=N+1$。

### ARCH-VIT-A02
把线性投影列重排为 $P\times P\times C$ kernels，用 kernel size/stride 都为 $P$、相同 padding与通道/flatten顺序的 convolution，可数值等价地生成 patch embeddings。等价只覆盖第一层线性算子，不覆盖后续 attention、局部连接层级或平移等变偏置。

### ARCH-VIT-A03
Class token 用一个学习槽位经多层交互做序列读出；masked mean无额外 query参数且平均所有有效 patches；dense readout保留 $H_p\times W_p$ grid用于检测/分割。三者输出 shape、空间信息与归纳偏置不同。

## B. 手算与建模

### ARCH-VIT-B01
$H_p=W_p=224/16=14$，所以 $N=196,T=197$。Patch input width $16^2\cdot3=768$，projection 主权重为
$$
P^2Cd=768\cdot768=589{,}824.
$$
若计 bias 再加 768。

### ARCH-VIT-B02
$H,W$ 各乘 2，网格两轴各乘 2，故 $N$ 乘 4；全局 attention pair 数约 $N^2$，乘 $16$。Class token只产生低阶交叉项，不改变主缩放。

### ARCH-VIT-B03
Crop 可把高度裁到 224，得到 $14\times14$ patches但丢 6 行像素；pad 可补到 240，得到 $15\times14$ patches并引入 10 行人工边界，需 mask/pooling合同；resize 到如 224 会重采样全部高度、改变几何与频率但维持 $14\times14$ grid。三者不是同一数据分布。

## C. 推导与证明

### ARCH-VIT-C01
设 patch向量按固定次序列出 $I[rP+u,cP+v,k]$。Linear output channel $o$ 为
$$
z_{r,c,o}=\sum_{u,v,k}I[rP+u,cP+v,k]E_{(u,v,k),o}+b_o.
$$
令 convolution kernel $K_{u,v,k,o}=E_{(u,v,k),o}$，stride $P$，恰得到同一式；flatten $(r,c)$ 即同一 token序列。

### ARCH-VIT-C02
$P'=2P$ 时
$$
N'=\frac{H}{2P}\frac{W}{2P}=\frac N4,\qquad
(N')^2=\frac{N^2}{16}.
$$
Patch projection参数从 $P^2Cd$ 变为 $(2P)^2Cd=4P^2Cd$。所以 attention work下降而输入 projection参数增加，且更早聚合局部细节。

### ARCH-VIT-C03
无 position时，共享 Q/K/V、row-softmax、逐 token FFN与residual满足 $F(PX)=PF(X)$，故对 patch permutation等变。Mean readout
$$
m(PH)=\frac1N\mathbf1^\top PH=\frac1N\mathbf1^\top H=m(H)
$$
因为 $\mathbf1^\top P=\mathbf1^\top$，所以变为置换不变。

## D. 边界、反例与纠错

### ARCH-VIT-D01
Stride-$P$ 卷积只是一次不重叠局部线性投影；后续标准 ViT每层可全局连接，不强制小 kernel共享、平移等变或逐层扩大感受野。CNN还包含多层局部连接、下采样和相应边界行为。实现同一个 patch算子不能推出整网偏置相同。

### ARCH-VIT-D02
在 $W_p=14$ 的 row-major grid中，序号 13 对应 $(r,c)=(0,13)$，序号 14 对应 $(1,0)$；一维相邻但二维 Manhattan 距离为 $|1-0|+|0-13|=14$，不是相邻 patch。

### ARCH-VIT-D03
新网格的 row/column坐标与旧序号不同。直接截断会只保留旧网格前部而偏向某些区域；重复会把不相邻位置赋相同向量，并可能把 class position混进 patch positions。应先分离特殊 token、reshape二维、按坐标插值并记录 aspect ratio假设。

## E. AI 迁移

### ARCH-VIT-E01
对可整除人工图像，patchify后unpatchify应逐像素相等；用坐标编码像素验证 patch顺序和 channels-first/last；覆盖 $B>1,C>1$。对不可整除分别验证 crop像素集合、pad值/valid mask与目标shape；错误策略应显式报错。再做 projection与等价 convolution数值对照。

### ARCH-VIT-E02
固定数据、增强、预训练 token/steps、模型总参数或明确预算、optimizer和resolution；扫描 $P$，重调合理 $d/L$时记录调参预算。报告小物体/边缘等细节分层指标、总体质量、attention/总FLOPs、峰值显存、训练吞吐、推理延迟、patch projection参数和多 seed。不能只报 $N^2$。

### ARCH-VIT-E03
卡片记录 CNN/ViT参数和训练FLOPs、预训练数据规模/标签、resolution、augmentation/regularization、optimizer、训练步数、迁移协议和调参预算。比较总体与数据规模分层结果、鲁棒/平移测试、吞吐和显存。ViT原论文的大数据结果标E，不外推小数据或任意视觉任务。
