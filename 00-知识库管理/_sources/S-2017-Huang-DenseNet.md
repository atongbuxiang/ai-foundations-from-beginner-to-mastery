---
type: source
status: draft
area: [sources, neural-networks, dense-connectivity, convolutional-networks]
source_type: paper
title: "Densely Connected Convolutional Networks"
author: "Gao Huang; Zhuang Liu; Laurens van der Maaten; Kilian Q. Weinberger"
year: 2017
url: "https://openaccess.thecvf.com/content_cvpr_2017/html/Huang_Densely_Connected_Convolutional_CVPR_2017_paper.html"
venue: "CVPR 2017"
accessed: 2026-08-23
source_tier: A
license: "CVF open-access paper；本库仅保存独立摘要、必要公式与链接"
scope_role: core
temporal_role: foundational
related: ["[[Highway、Dense Connection 与 Skip 结构比较]]", "[[残差学习、恒等捷径与退化问题]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Huang et al.：DenseNet

> [!abstract] 来源定位
> 论文提出 dense block：每层接收该 block 内所有先前特征图的拼接，并用 growth rate 控制新增通道。它承担 concatenative skip 的原始结构、连接计数与实验；本库另行审计激活存储、内存流量、transition compression 与“特征复用”的证据边界。

## 原始结构

$$
z_\ell=H_\ell([x_0,z_1,\ldots,z_{\ell-1}]),
$$

其中 $[\cdot]$ 表示沿通道轴拼接。若初始通道数为 $C_0$、每层新增 $k$ 个通道，则第 $\ell$ 层输入通道数为

$$
C_0+(\ell-1)k.
$$

包含 $L$ 层的 dense block 在把输入节点也计入连接端点时共有 $L(L+1)/2$ 条前向连接。

## 断言审计

| ID | 断言 | 类型 | 条件/边界 | 本库判断 |
|---|---|---|---|---|
| DN-C1 | 每层可直接读取所有先前特征 | 结构 | 同一 dense block、空间尺寸对齐 | 精确 |
| DN-C2 | 最终通道为 $C_0+Lk$ | 计数 | 无 transition compression | 精确 |
| DN-C3 | 拼接自动更省显存 | 系统外推 | 保存激活、kernel fusion、checkpointing 均相关 | 不成立 |
| DN-C4 | DenseNet 普遍优于 ResNet | 经验外推 | 数据、参数/FLOP/内存预算与调参不同 | 原论文不足以支持 |

## 本库使用边界

“feature reuse”是结构动机与实验解释，不是每个旧坐标都被后层有效使用的定理。拼接保留坐标身份，但混合、压缩与舍弃仍由后续算子决定。

