---
type: exercise
status: draft
area: [neural-networks/regularization, stochastic-depth, droppath, residual-networks, effective-depth]
topic: "[[Stochastic Depth、DropPath 与有效深度]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Stochastic Depth、DropPath 与有效深度]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - Stochastic Depth、DropPath 与有效深度

## A

### NN-SDP-A01
写出原始 stochastic depth 与现代 inverted DropPath 的 train/eval 合同。两者的 $F_l$ scaling 分别放在哪个阶段？

### NN-SDP-A02
区分 physical depth、active depth、path length 与 effective depth。为什么 $\mathbb E[D]=2.75$ 不表示训练了固定 2.75 层网络？

### NN-SDP-A03
比较 batch-shared gate、per-sample/row gate 与 token/element gate 的随机性、统计耦合与执行难度。

## B

### NN-SDP-B01
四个 residual branches 的 survival probabilities 为 $(0.875,0.75,0.625,0.5)$。求 active depth $D$ 的均值、方差、全活跃概率和全删除概率。

### NN-SDP-B02
固定 $x_l$，令 $f=F_l(x_l)$、$R_l=b_lf/q_l$。求 $\mathbb E[R_l\mid x_l]$、$\operatorname{Cov}(R_l\mid x_l)$ 与任一坐标方差；解释 covariance 的秩。

### NN-SDP-B03
有四个 branches，计算成本 $C=(1,2,3,4)$，survival probabilities 沿用 B01。若能真正短路，求期望 branch compute；若总是先计算再乘 mask，branch compute 是多少？

## C

### NN-SDP-C01
对 $x_{l+1}=x_l+b_lF_l(x_l;\theta_l)/q_l$ 推导 local Jacobian、input VJP 与参数梯度；解释 $b_l=0$ 时 identity rail 保留了什么。

### NN-SDP-C02
推导 independent nonidentical Bernoulli gates 下 $D=\sum_l b_l$ 的 probability-generating function，并由其恢复均值与方差。

### NN-SDP-C03
证明固定 $x_l$ 下 inverted block 的 expected local Jacobian 等于 full block local Jacobian；再解释为何不能把这一等式直接乘过全网得到 expected end-to-end Jacobian。

## D

### NN-SDP-D01
审计命题：“DropPath rate 为 0.2，所以训练 FLOP 必然下降 20%。”列出实现、schedule、gate granularity 与固定成本方面的反例。

### NN-SDP-D02
分析带 BatchNorm residual branch 的 batch-shared gate 与 per-sample gate。讨论 running statistics、空分支、sample mixture 和 eval consistency。

### NN-SDP-D03
解释 activation checkpointing、distributed replicas 与 gate RNG 不一致如何使 forward/backward 或数据并行语义错误；给出验收测试。

## E

### NN-SDP-E01
设计 constant、linear-decay 与 stage-specific survival schedules 的公平比较，规定至少三类账本：质量、稳定性和计算。

### NN-SDP-E02
设计 DropPath 与 residual scaling（如 LayerScale/Fixup/ReZero 类参数化）的二维消融；指出为什么不能只复制另一个模型的 drop rate。

### NN-SDP-E03
为“随机深度改善泛化是因为网络更浅”写一份证据地图：列出优化、正则化、路径集成与计算四种机制所需的区分性测量。

## 解答入口

[[解答 - Stochastic Depth、DropPath 与有效深度]]
