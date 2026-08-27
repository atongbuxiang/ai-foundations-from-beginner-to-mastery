---
type: exercise
status: draft
area: [generative-models, flow-matching, continuity-equation]
topic: "[[连续性方程、概率路径与 Flow Matching]]"
solution: "[[解答 - 连续性方程、概率路径与 Flow Matching]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 连续性方程、概率路径与 Flow Matching
## A. 识别与复述
### GEN53-A01
区分 probability path、sample trajectory 与 velocity field。
### GEN53-A02
写出连续性方程的强形式和 test-function 弱形式。
### GEN53-A03
“simulation-free training”准确排除了什么，又没有排除什么？
## B. 手算与建模
### GEN53-B01
直线 conditional path $X_t=(1-t)X_0+tX_1$ 的速度是什么？
### GEN53-B02
$X_0,\epsilon\sim N(0,1)$ 独立，$X_t=\sqrt{1-t}X_0+\sqrt t\epsilon$。说明 marginal velocity 可为零而 conditional velocity 非零。
### GEN53-B03
若一维 $v_t(x)=cx$ 且 $X_0$ 均值为 $m_0$，用 test function $\varphi(x)=x$ 求均值演化。
## C. 推导与证明
### GEN53-C01
从粒子 ODE 推导连续性方程的弱形式。
### GEN53-C02
证明 $v_t(x)=E[U_t\mid X_t=x]$ 运输 conditional construction 的 marginal path。
### GEN53-C03
证明 CFM 与 FM population loss 相差 conditional variance 常数。
## D. 边界、反例与纠错
### GEN53-D01
反驳“给定 $p_t$ 就唯一决定 $v_t$”。
### GEN53-D02
反驳“conditional path 是直线，所以生成轨迹也是直线”。
### GEN53-D03
为什么训练无需 ODE simulation 不代表生成不需要 solver？
## E. AI 迁移
### GEN53-E01
写出一个最小 CFM training step 的对象、shape 和随机性合同。
### GEN53-E02
设计用 test functions 经验检查连续性方程的实验。
### GEN53-E03
如何审计 endpoint singularity 与 time parameterization 带来的 target 爆大？
## 解答入口
[[解答 - 连续性方程、概率路径与 Flow Matching]]
