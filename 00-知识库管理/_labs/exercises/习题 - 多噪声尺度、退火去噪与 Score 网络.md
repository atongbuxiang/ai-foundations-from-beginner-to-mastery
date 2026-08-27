---
type: exercise
status: draft
area: [generative-models, score-based-models]
topic: "[[多噪声尺度、退火去噪与 Score 网络]]"
solution: "[[解答 - 多噪声尺度、退火去噪与 Score 网络]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - 多噪声尺度、退火去噪与 Score 网络
## A. 识别与复述
### GEN29-A01
Gaussian smoothing 为什么能缓解数据位于低维流形时的 score 定义问题？
### GEN29-A02
写出 noise-conditional DSM 目标，并区分 noise-level sampling 与 loss weighting。
### GEN29-A03
列出 annealed Langevin 的初始化、尺度循环、步长、每层步数和最后去噪合同。
## B. 手算与建模
### GEN29-B01
$\sigma_{max}=8,\sigma_{min}=1,L=4$，用几何序列计算全部 $\sigma_i$。
### GEN29-B02
$d$ 维 Gaussian conditional-score target 为 $-\varepsilon/\sigma$。求其期望平方范数；什么权重能平衡不同 $\sigma$ 的 target scale？
### GEN29-B03
对对称双 Gaussian mixture，证明任意 $\sigma$ 下中点 score 为 0，并说明这不表示中点是 mode。
## C. 推导与证明
### GEN29-C01
证明 $p_\sigma=p_0*\varphi_\sigma$；若 $p_0$ 是离散点质量，写出 $p_\sigma$ 的形式。
### GEN29-C02
推导几何 noise ladder 的通式，使首尾恰为 $\sigma_{max},\sigma_{min}$。
### GEN29-C03
对一步 $x^+=x+\alpha s+\sqrt{2\alpha}z$，写出 drift/noise norm ratio，并解释为何 $\alpha\propto\sigma^2$ 只是特定 scaling heuristic。
## D. 边界、反例与纠错
### GEN29-D01
反驳“score 为零的点一定是高密度 mode”。
### GEN29-D02
反驳“只训练最小噪声尺度就一定最接近真实数据，所以生成最好”。
### GEN29-D03
反驳“最后 Tweedie 去噪只删除噪声，不改变样本分布”。
## E. AI 迁移
### GEN29-E01
设计一个双峰 toy 实验比较单尺度与多尺度 sampling 的模式覆盖。
### GEN29-E02
为 NCSN 复现写出必须报告的 noise/training/sampling 字段。
### GEN29-E03
给出 ablation，区分多尺度改进来自训练覆盖、warm start 还是更高 NFE。
## 解答入口
[[解答 - 多噪声尺度、退火去噪与 Score 网络]]

