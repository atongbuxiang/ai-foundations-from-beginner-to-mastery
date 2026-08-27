---
type: exercise
status: draft
area: [generative-models, numerical-analysis, diffusion]
topic: "[[扩散 SDE、ODE Solver、步长与 NFE 总账]]"
solution: "[[解答 - 扩散 SDE、ODE Solver、步长与 NFE 总账]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 扩散 SDE、ODE Solver、步长与 NFE 总账
## A. 识别与复述
### GEN68-A01
区分 local truncation error、global discretization error 与 learned field error。
### GEN68-A02
为什么“20 steps”不能直接等于“20 NFE”？
### GEN68-A03
区分 SDE solver 的 strong error、weak error 与 Monte Carlo metric error。
## B. 手算与建模
### GEN68-B01
用一步 Euler 和 Heun 从 $x(0)=1$ 近似 $\dot x=x$ 到 $t=.5$，计算与 $e^{.5}$ 的误差。
### GEN68-B02
预算 20 NFE：Euler、每步 2 NFE 的 Heun、warm-up 3 NFE 后每步 1 NFE 的 multistep 各可做多少主步？
### GEN68-B03
给 $t_n=(1,.5,.1,0)$，写出从 $T$ 到 0 的有符号步长。
## C. 推导与证明
### GEN68-C01
由 Taylor 展开推 Euler local $O(h^2)$ 与 Heun local $O(h^3)$。
### GEN68-C02
写出用 Gronwall 分离 field error 与 terminal mismatch 的上界。
### GEN68-C03
说明 DPM-Solver 解析线性部分为何可能降低误差常数，但不消除 model error。
## D. 边界、反例与纠错
### GEN68-D01
反驳“二阶方法在同 NFE 下必优于一阶方法”。
### GEN68-D02
给出向量积分平均不一定等于某个共同函数值的例子。
### GEN68-D03
解释 extreme CFG 为什么可能改变最佳 time grid/solver。
## E. AI 迁移
### GEN68-E01
设计 oracle ODE 与 learned ODE 的双层 solver benchmark。
### GEN68-E02
写一个完整 NFE/latency 记录表。
### GEN68-E03
审计论文“5 steps 超越 20 steps”至少需要追问哪些变量？
## 解答入口
[[解答 - 扩散 SDE、ODE Solver、步长与 NFE 总账]]
