---
type: source
status: active
area: [sources, online-convex-optimization, online-gradient-descent]
source_type: paper
title: "Online Convex Programming and Generalized Infinitesimal Gradient Ascent"
author: [Martin Zinkevich]
year: 2003
url: "https://www.cs.cmu.edu/~maz/publications/ICML03.pdf"
accessed: 2026-08-23
source_tier: A
license: "Author-hosted scholarly source; retain citation and convexity conditions"
venue: "ICML 2003"
scope_role: primary
temporal_role: foundational
related: ["[[Online Gradient Descent 与 Mirror Descent]]"]
created: 2026-08-23
updated: 2026-08-23
---
# Online Convex Programming
> [!abstract] 来源定位
> 建立 projected online gradient method 与 static/dynamic regret 基线。本库调用投影势能证明；bounded domain 与 gradients 不省略。
## 本库调用
1. OCO protocol；
2. projected gradient update；
3. Euclidean telescope；
4. $O(\sqrt T)$ regret；
5. path-length/dynamic comparator 接口。
