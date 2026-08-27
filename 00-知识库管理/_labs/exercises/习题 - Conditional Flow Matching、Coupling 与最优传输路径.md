---
type: exercise
status: draft
area: [generative-models, conditional-flow-matching, optimal-transport]
topic: "[[Conditional Flow Matching、Coupling 与最优传输路径]]"
solution: "[[解答 - Conditional Flow Matching、Coupling 与最优传输路径]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Conditional Flow Matching、Coupling 与最优传输路径
## A. 识别与复述
### GEN54-A01
定义 coupling，并写出它必须满足的两个边缘条件。
### GEN54-A02
independent coupling 与 quadratic OT coupling 分别优化/忽略什么？
### GEN54-A03
coupling 会影响 CFM 的哪些对象，即使 endpoint marginals 不变？
## B. 手算与建模
### GEN54-B01
对 $\{-1,+1\}$ 均匀分布，计算 identity 与 swap coupling 在线性插值中点的 target 均值和方差。
### GEN54-B02
给 source 点 $0,3$、target 点 $1,4$，比较同序配对与交叉配对的总平方成本。
### GEN54-B03
给 cost matrix $\begin{pmatrix}1&9\\4&0\end{pmatrix}$，求 batch size 2 的最小 assignment，并说明它不代表什么。
## C. 推导与证明
### GEN54-C01
证明一个 joint law 是合法 coupling 时，其直线插值端点边缘正确。
### GEN54-C02
写出并解释 $C_\pi=E\|U-E[U\mid X_t,t]\|^2$ 对 coupling 的依赖。
### GEN54-C03
陈述 quadratic OT displacement interpolation 与动态动能最小化的条件性关系。
## D. 边界、反例与纠错
### GEN54-D01
反驳“minibatch OT 就是 population OT”。
### GEN54-D02
反驳“端点平均距离更短必然意味着 finite-NFE 生成更好”。
### GEN54-D03
把 noise-$t=0$/data-$t=1$ 的代码转换到本卷方向时，哪些量要同时改变？
## E. AI 迁移
### GEN54-E01
设计 independent CFM 与 minibatch OT-CFM 的公平比较协议。
### GEN54-E02
列出 OT-CFM 实现必须记录的配置字段。
### GEN54-E03
设计一个路径交叉/conditional variance 的可视化和数值指标。
## 解答入口
[[解答 - Conditional Flow Matching、Coupling 与最优传输路径]]
