---
type: source
status: verified
area: [sources, ai/transformers, ai/attention, algorithms/complexity]
source_type: paper
title: "Attention Is All You Need"
author: "Ashish Vaswani et al."
year: 2017
url: "https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html"
accessed: 2026-08-19
source_tier: A
license: "NeurIPS proceedings; metadata and independent summary only"
scope_role: core
temporal_role: foundational
related: ["[[渐近记号、增长率与复杂度]]", "[[内容寻址、Query、Key 与 Value]]", "[[Scaled Dot-Product Attention 与 Softmax 数值语义]]", "[[Attention Mask、因果性与可见性合同]]", "[[Self-Attention、Cross-Attention 与张量形状]]", "[[Multi-Head Attention、投影子空间与参数量]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer Encoder 与双向表示]]", "[[Transformer Decoder 与自回归因果结构]]", "[[Encoder–Decoder 与 Cross-Attention]]", "[[Transformer 形状、参数量与 FLOPs 总账]]", "[[S-2020-Su-7546-线性Attention]]"]
created: 2026-08-19
updated: 2026-08-19
---

# Attention Is All You Need：定义与复杂度接口

> [!abstract] 来源定位
> Transformer 原始论文定义 scaled dot-product attention 与 multi-head attention，并在 Table 1 比较 Self-Attention、recurrent、convolutional 与 restricted Self-Attention 的每层 complexity、最少 sequential operations 和 maximum path length。MATH-08 调用它说明 work、span 与路径长度是不同资源；ARCH-25—29 调用它建立 Q/K/V、mask、shape 与多头投影的正式对象。

## 核心证据

论文在表示宽度$d$、序列长度$n$的抽象下给出：

| Layer | Per-layer work | Sequential operations | Maximum path |
|---|---:|---:|---:|
| Self-Attention | $O(n^2d)$ | $O(1)$ | $O(1)$ |
| Recurrent | $O(nd^2)$ | $O(n)$ | $O(n)$ |
| Convolutional | $O(knd^2)$ | $O(1)$ | $O(\log_k n)$ |
| Restricted Self-Attention | $O(rnd)$ | $O(1)$ | $O(n/r)$ |

这张表是特定层抽象，不等于完整Transformer block的所有projection、MLP、activation、backward或wall-clock。

## MATH-08补充

完整dense attention常需登记$\Theta(BTd^2+BT^2d)$ work，以及显式score的$\Theta(BhT^2)$元素。原论文表格与该式不矛盾：前者以核心layer对比突出pairwise mixing，后者用于完整shape audit。

## 限制

- $O(1)$ sequential operations不表示$O(1)$ work；
- 原论文实测硬件与现代kernel不同，wall-clock数字不作当前性能依据；
- Causal mask、KV cache、GQA与tiling需要另立制度；
- Complexity advantage不自动等于quality advantage。
