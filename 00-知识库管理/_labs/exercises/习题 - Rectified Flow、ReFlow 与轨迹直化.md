---
type: exercise
status: draft
area: [generative-models, rectified-flow, reflow]
topic: "[[Rectified Flow、ReFlow 与轨迹直化]]"
solution: "[[解答 - Rectified Flow、ReFlow 与轨迹直化]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Rectified Flow、ReFlow 与轨迹直化
## A. 识别与复述
### GEN55-A01
写出 Rectified Flow 的直线 interpolation、target 与 population field。
### GEN55-A02
定义 material acceleration，并解释它与轨迹直线性的关系。
### GEN55-A03
按顺序复述一次 ReFlow 的五个步骤。
## B. 手算与建模
### GEN55-B01
对 $dZ/dt=tZ$ 求 exact flow，并计算从 $t=1$ 到 $0$ 的一步 Euler 结果。
### GEN55-B02
一条折线路径长度为 $3+4$，端点直线距离为 $5$。求 path-length ratio 并解释。
### GEN55-B03
若沿轨迹 velocity 为 $v(t)=a+bt$，求一步反向 Euler 与 exact integral 的误差。
## C. 推导与证明
### GEN55-C01
证明 RF population minimizer 是 $E[X_1-X_0\mid X_t=x,t]$。
### GEN55-C02
由链式法则推导 $d^2Z_t/dt^2=\partial_tv+J_vv$。
### GEN55-C03
推导一步 Euler endpoint error 的速度积分表达式。
## D. 边界、反例与纠错
### GEN55-D01
反驳“teacher segment 直线推出 model trajectory 直线”。
### GEN55-D02
为什么 convex transport cost 不增不等于一次 rectification 达到 OT？
### GEN55-D03
ReFlow 中为什么不能把模型生成的 $Z_0$ 当作无误差真实数据？
## E. AI 迁移
### GEN55-E01
设计 ReFlow 的配对生成与重训伪代码合同。
### GEN55-E02
设计直化审计：至少三个几何/动力学/数值指标。
### GEN55-E03
如何公平比较第 0、1、2 轮 ReFlow 的生成质量与成本？
## 解答入口
[[解答 - Rectified Flow、ReFlow 与轨迹直化]]
