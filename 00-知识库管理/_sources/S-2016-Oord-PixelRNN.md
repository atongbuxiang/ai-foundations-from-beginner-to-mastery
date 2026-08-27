---
type: source
status: verified
area: [sources, generative-models/autoregressive, image-generation]
source_type: paper
title: "Pixel Recurrent Neural Networks"
author: [Aaron van den Oord, Nal Kalchbrenner, Koray Kavukcuoglu]
year: 2016
url: "https://arxiv.org/abs/1601.06759"
accessed: 2026-08-25
source_tier: A
scope_role: core
temporal_role: classical
related: ["[[概率链式分解、顺序选择与自回归生成]]", "[[离散似然、连续似然、Dequantization 与 Bits-per-dim]]"]
created: 2026-08-25
updated: 2026-08-25
---

# van den Oord et al.：Pixel Recurrent Neural Networks

> [!abstract] 来源定位
> PixelRNN 将二维图像按固定顺序展开，以离散像素条件分布直接建模 raw image likelihood，并比较离散质量函数与加均匀噪声后的连续密度口径。课程采用其二维自回归、离散似然与 BPD 历史接口；样本观感和当年 likelihood 排名只保留在原实验设置中。

## 关键对象

若像素及通道经顺序 $\pi$ 展开，

$$
p(\boldsymbol{x})=\prod_{i=1}^{D}p\bigl(x_{\pi(i)}\mid x_{\pi(<i)}\bigr).
$$

每个离散 conditional 都归一化，因此联合质量函数可精确求值。论文还说明：在 unit-width bins 下，以 piecewise-uniform continuous density 表示离散质量，可保持相应 log-likelihood 数值；若数据缩放到 $[0,1]$，还需加入 bin-width Jacobian 常数。

## 课程边界

- raster order 是归纳偏置，不是概率链式法则唯一允许的顺序；
- exact likelihood 不意味着并行 exact sampling；
- crisp samples 与 coverage/semantic quality 需独立评价；
- dequantization 的 lower-bound 口径在 [[S-2019-Ho-FlowPlusPlus-Dequantization]] 补严。

