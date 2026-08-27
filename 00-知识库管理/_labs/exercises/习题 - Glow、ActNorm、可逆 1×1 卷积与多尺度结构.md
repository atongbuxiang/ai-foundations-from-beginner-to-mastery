---
type: exercise
status: draft
area: [generative-models, normalizing-flows]
topic: "[[Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"
solution: "[[解答 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构
## A. 识别与复述
### GEN35-A01
区分 ActNorm 与 BatchNorm 的训练初始化和推理依赖。
### GEN35-A02
写出可逆 $1\times1$ convolution 的单位置映射与整图 logdet。
### GEN35-A03
区分 squeeze 与 split/factor-out。
## B. 手算与建模
### GEN35-B01
$C=2,H=W=3,W=\operatorname{diag}(2,1/2)$。求整图 logdet。
### GEN35-B02
ActNorm scales 为 $(2,1/4)$，$H=W=2$。求单样本 logdet。
### GEN35-B03
输入形状 $[8,3,32,32]$ 经 $2\times2$ squeeze 后是什么形状？元素数是否变化？
## C. 推导与证明
### GEN35-C01
证明共享 $W$ 作用于 $HW$ 个位置时总 determinant 为 $(\det W)^{HW}$。
### GEN35-C02
用 LU 参数化推导 $\log|\det W|=\sum_c\log|s_c|$。
### GEN35-C03
证明保留所有 factor-out chunks 时最终 latent 总维数等于输入。
## D. 边界、反例与纠错
### GEN35-D01
反驳“determinant 远离 0 就说明矩阵条件良好”。
### GEN35-D02
反驳“ActNorm 每次 forward 都用当前 batch 重新标准化”。
### GEN35-D03
解释遗漏一个 split latent chunk 会怎样改变生成分布。
## E. AI 迁移
### GEN35-E01
列出一个 Glow step 的 forward/inverse 次序与三项 logdet。
### GEN35-E02
设计首批 ActNorm 初始化敏感性实验。
### GEN35-E03
为可逆 $1\times1$ conv 建立数值健康仪表板。
## 解答入口
[[解答 - Glow、ActNorm、可逆 1×1 卷积与多尺度结构]]

