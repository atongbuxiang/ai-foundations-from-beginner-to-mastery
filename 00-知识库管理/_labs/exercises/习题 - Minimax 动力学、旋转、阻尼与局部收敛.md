---
type: exercise
status: draft
area: [generative-models, gan, game-dynamics]
topic: "[[Minimax 动力学、旋转、阻尼与局部收敛]]"
solution: "[[解答 - Minimax 动力学、旋转、阻尼与局部收敛]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Minimax 动力学、旋转、阻尼与局部收敛
## A. 识别与复述
### GEN22-A01
定义 game vector field、stationary、local Nash 与 dynamic stability。
### GEN22-A02
为什么 GAN vector field 一般不是 scalar potential gradient？
### GEN22-A03
TTUR 理论需要哪些额外条件？
## B. 手算与建模
### GEN22-B01
对 $\min_x\max_yxy$ 写同步 GDA 矩阵与特征值。
### GEN22-B02
$\eta=.1$ 时一步 radius-squared 放大多少倍？
### GEN22-B03
连续 bilinear ODE 求 $d(x^2+y^2)/dt$。
## C. 推导与证明
### GEN22-C01
证明固定正步长同步 GDA 向外发散。
### GEN22-C02
为 $xy+\frac\lambda2x^2-\frac\lambda2y^2$ 推连续 Jacobian 并判稳定。
### GEN22-C03
推一阶 extragradient 在 bilinear game 的更新矩阵。
## D. 边界、反例与纠错
### GEN22-D01
给 stationary 非 local Nash 例子。
### GEN22-D02
反驳 loss 平稳等于收敛到 Nash。
### GEN22-D03
反驳“WGAN-GP 有有限 critic steps 就保证收敛”。
## E. AI 迁移
### GEN22-E01
设计记录旋转、gradient angle 与更新范数的训练审计。
### GEN22-E02
公平比较 GDA、extragradient、TTUR。
### GEN22-E03
说明 EMA 改部署样本但不等于训练 game 收敛。
## 解答入口
[[解答 - Minimax 动力学、旋转、阻尼与局部收敛]]

