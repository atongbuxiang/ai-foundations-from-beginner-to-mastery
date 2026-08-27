---
type: source
status: active
area: [sources, learning-theory, scale-sensitive-dimension]
source_type: paper
title: "Fat-Shattering and the Learnability of Real-Valued Functions"
author: [Peter L. Bartlett, Philip M. Long, Robert C. Williamson]
year: 1996
url: "https://doi.org/10.1006/jcss.1996.0033"
accessed: 2026-08-23
source_tier: A
license: "Journal article; retain citation, independent definitions/derivations, and author/DOI links"
venue: "Journal of Computer and System Sciences 52(3), 434–452"
scope_role: primary
temporal_role: classical-foundation
related: ["[[Fat-Shattering、回归与 Lipschitz 风险]]", "[[实值函数类、伪维与阈值化]]", "[[覆盖数、Metric Entropy 与 Chaining 入口]]"]
created: 2026-08-23
updated: 2026-08-23
---

# Fat-Shattering and Real-Valued Learnability

> [!abstract] 来源定位
> Bartlett、Long 与 Williamson 研究 $[0,1]$-valued 函数类的 fat-shattering function 与可学习性。它把 binary shattering 的“能否实现符号模式”升级为“能否以给定数值间隔实现符号模式”，是回归、margin 与 scale-sensitive entropy 的基础容量语言。

## 元数据与纳入

- 正式引用：Bartlett, P. L., Long, P. M. & Williamson, R. C. (1996), *JCSS* 52(3), 434–452；
- DOI：[10.1006/jcss.1996.0033](https://doi.org/10.1006/jcss.1996.0033)；
- 作者版本：[PDF](https://phillong.info/publications/fatshat.pdf)；
- 证据角色：fat-shattering 与 bounded real-valued learnability 的原始主线；
- 版权边界：不复制原图或长段文字，只保留独立定义、例子、关系链和正式链接。

## 本库调用的断言

1. fat-shattering dimension 依赖 resolution $\gamma$，并随 $\gamma$ 增大而不增；
2. thresholds 可逐点变化，margin convention 必须声明是 $\gamma$ 还是 $\gamma/2$；
3. scale-sensitive dimension 可控制实值函数类的 packing/covering，从而进入 uniform convergence 与 learnability；
4. pseudo-dimension 是 scale-free threshold capacity，不能替代具体 $\gamma$ 下的数值分辨率；
5. 回归风险还需 loss Lipschitz/range/tail 与 sampling 条件，fat dimension 不是单独的风险定理。

## 后续调用

- [[Fat-Shattering、回归与 Lipschitz 风险]]：定义、线性球例子与风险链；
- [[覆盖数、Metric Entropy 与 Chaining 入口]]：fat dimension 到 metric entropy 的桥；
- [[实值函数类、伪维与阈值化]]：与 pseudo-dimension 的尺度分工。
