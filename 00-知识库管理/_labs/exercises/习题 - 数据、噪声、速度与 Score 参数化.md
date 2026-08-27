---
type: exercise
status: draft
area: [generative-models, diffusion]
topic: "[[数据、噪声、速度与 Score 参数化]]"
solution: "[[解答 - 数据、噪声、速度与 Score 参数化]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 数据、噪声、速度与 Score 参数化
## A. 识别与复述
### GEN43-A01
写出 $x_t$ 与 $v_t$ 的旋转定义和 inverse。
### GEN43-A02
写出 noise optimum 与 marginal score 的关系。
### GEN43-A03
区分代数等价、Bayes-optimum 等价与训练等价。
## B. 手算与建模
### GEN43-B01
$a=0.8,\sigma=0.6,x_0=2,\epsilon=-1$。求 $x_t,v$ 并反算。
### GEN43-B02
$a=0.3,\sigma=\sqrt{0.91},x_t=1,\hat\epsilon=0.2$。求 $\hat x_0$。
### GEN43-B03
$\sigma=0.5,E[\epsilon|x_t]=-0.3$。求 marginal score。
## C. 推导与证明
### GEN43-C01
证明参数化矩阵正交并保持平方范数。
### GEN43-C02
推导 $\|\delta\epsilon\|^2=SNR\|\delta x_0\|^2$。
### GEN43-C03
从 conditional score identity 推导 marginal score。
## D. 边界、反例与纠错
### GEN43-D01
说明 $a_t\to0$ 时 noise-to-data 换算为何病态。
### GEN43-D02
反驳“单个 pair 的 $-\epsilon/\sigma$ 就是 marginal score”。
### GEN43-D03
解释 clipping $\hat x_0$ 后为什么四种输出不再严格可逆等价。
## E. AI 迁移
### GEN43-E01
设计四参数化互换的单元测试。
### GEN43-E02
怎样公平比较 epsilon、x0、v heads？
### GEN43-E03
为每个 log-SNR bin 建立 error dashboard。
## 解答入口
[[解答 - 数据、噪声、速度与 Score 参数化]]

