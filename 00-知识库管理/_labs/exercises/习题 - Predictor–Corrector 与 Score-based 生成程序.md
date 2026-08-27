---
type: exercise
status: draft
area: [generative-models, score-based-models, samplers]
topic: "[[Predictor–Corrector 与 Score-based 生成程序]]"
solution: "[[解答 - Predictor–Corrector 与 Score-based 生成程序]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Predictor–Corrector 与 Score-based 生成程序
## A. 识别与复述
### GEN31-A01
Predictor 与 corrector 分别近似什么对象？
### GEN31-A02
为什么只有 corrector 不能完成从 $p_T$ 到 $p_0$ 的生成？
### GEN31-A03
列出 PC sampler 的 score、solver、mixing 与 deployment 四层误差。
## B. 手算与建模
### GEN31-B01
时间网格 50 步，predictor 每步 1 次 score，corrector 每层 2 步且每步 1 次 score。忽略最后去噪，求总 NFE。
### GEN31-B02
一步 corrector 中 $\|s\|=5,\|z\|=10$，希望 drift/noise norm ratio 为 $r=0.1$。由本节公式求 $\alpha$。
### GEN31-B03
固定层 score 为 $s(x)=-x$，$x=2,\epsilon=0.1,z=0.5$。计算一次 corrector 更新。
## C. 推导与证明
### GEN31-C01
由 $\|\epsilon s\|/\|\sqrt{2\epsilon}z\|=r$ 解出 $\epsilon$。
### GEN31-C02
解释为何 fixed-time Langevin 的目标是 $p_t$：将 $s_t=\nabla\log p_t$ 代入对应 SDE。
### GEN31-C03
说明 exact predictor 后再应用以当前 marginal 为 invariant 的 exact corrector kernel，为什么 marginal 不变；有限 learned 实现为什么不继承该结论。
## D. 边界、反例与纠错
### GEN31-D01
反驳“corrector 能直接观察并抵消 predictor 的数值误差”。
### GEN31-D02
反驳“加入更多 corrector steps 总会在相同 wall time 下改善样本”。
### GEN31-D03
为何把时间步数当成 NFE 会不公平评价 PC？
## E. AI 迁移
### GEN31-E01
设计 predictor-only、corrector-only 与 PC 的 compute-matched ablation。
### GEN31-E02
写出一个 PC 复现日志的最小字段集合。
### GEN31-E03
比较 ULA corrector 与 MALA corrector 的理论收益和工程成本。
## 解答入口
[[解答 - Predictor–Corrector 与 Score-based 生成程序]]

