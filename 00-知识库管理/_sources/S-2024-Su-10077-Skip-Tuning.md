---
type: source
status: verified
area: [sources, generative-models, diffusion, sampling]
source_type: blog
title: "生成扩散模型漫谈（二十四）：少走捷径，更快到达"
author: 苏剑林
year: 2024
url: "https://spaces.ac.cn/archives/10077"
accessed: 2026-08-25
source_tier: C
scope_role: supporting
related: ["[[扩散 SDE、ODE Solver、步长与 NFE 总账]]"]
created: 2026-08-25
updated: 2026-08-25
---
# 科学空间：Skip-Tuning

> [!abstract] 来源定位
> 文章介绍在低步数采样时缩放 U-Net skip connections 的经验技巧，并用“非线性能力/高频细节—主干去噪”解释结果。课程把它放在 solver 之外的模型调用调节层，用来提醒 NFE 改善不只来自积分公式。

- 页面发布日期：2024-04-23。
- 采用：相同 sampler 下的 architecture-time intervention 与消融设计。
- 证据边界：“skip 主要负责高频、backbone 主要负责去噪”是解释框架，不是任意 U-Net/DiT 的一般分解定理。
- 公平比较要固定：checkpoint、schedule、NFE、guidance、precision，并扫 skip scale；DiT 残差类比仅作假说。
