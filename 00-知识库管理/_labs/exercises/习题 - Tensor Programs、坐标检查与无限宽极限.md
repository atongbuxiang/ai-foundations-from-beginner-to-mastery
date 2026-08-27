---
type: exercise
status: verified
area: [training, optimization, tensor-programs, infinite-width]
topic: "[[Tensor Programs、坐标检查与无限宽极限]]"
solution: "[[解答 - Tensor Programs、坐标检查与无限宽极限]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Tensor Programs、坐标检查与无限宽极限

> [!abstract] 训练目标
> 能把程序依赖、极限量词、coordinate law 与有限宽 coord check 分层，识别 transpose reuse/GIA 和“水平曲线即证明”的错误。

## A. 识别与复述

### TRN44-A01
列出 Tensor Program 教学合同的四类程序对象和五类极限量词门。

### TRN44-A02
什么是 gradient independence assumption？为什么同一 $W$ 在 forward 和 $W^\top$ 在 backward 的复用会使朴素独立替换危险？

### TRN44-A03
说明 T1 手推、T2 统计模拟、T3 coordinate check 与 T4 训练迁移分别回答什么；哪些层不能被前一层替代？

## B. 手算与构造

### TRN44-B01
给定上一层两个输入的经验 covariance $Q(x,x')=0.3$、$\sigma_w^2=2$、$\sigma_b^2=0.1$，计算下一层 preactivation covariance。若 ReLU 的 Gaussian expectation 未给出，说明下一步需要计算什么积分对象。

### TRN44-B02
某层 coordinate RMS 在 width $n=128,512,2048$ 时分别为 $0.8,1.6,3.2$。拟合 log–log slope；判断更像水平、爆炸还是消失。

### TRN44-B03
用 $m_1,m_2,m_4$ 比较向量 $x=(1,\ldots,1,M)$ 的尾部敏感性。令总维度为 $n$，写出三者并讨论 $M\gg n^{1/4}$ 时谁先暴露异常。

## C. 推导与证明

### TRN44-C01
从条件 covariance 推导
$$
\Sigma_z(x,x')=\sigma_w^2Q(x,x')+\sigma_b^2,
$$
并说明经验平均收敛和 Gaussian 极限分别承担哪一步。

### TRN44-C02
证明固定任意有限 $T$ 的收敛结论不逻辑蕴含 $T(n)\to\infty$ 时收敛；用误差上界 $T/n$ 构造说明。

### TRN44-C03
为 log–log slope $\widehat\kappa$ 写一个最小回归模型，说明 seed、宽度窗口和曲线弯曲如何影响“$\kappa\approx0$”判断。

## D. 边界、反例与纠错

### TRN44-D01
反驳：“coord check 所有 $m_1$ 曲线水平，所以 μP 实现肯定正确。”至少列出四个漏检维度。

### TRN44-D02
构造 $m_1$ 近似稳定、但 $m_4$ 随 width 增长的稀有大坐标例子。

### TRN44-D03
为什么 output/attention logits 在 μP 初始化时收缩不一定是 bug？怎样区分预期瞬态与真正消失？

## E. AI 迁移

### TRN44-E01
为 Transformer coord check 写最小实验 manifest：widths、steps、probe、seeds、统计量、特殊例外和失败阈值。

### TRN44-E02
对 recurrent weight sharing、tied embedding、Q/K transpose 三类依赖分别写 GIA 审计问题。

### TRN44-E03
若 T3 通过但 T4 的最优 LR 明显漂移，提出至少五个互斥度较高的候选解释和区分实验。

## 作答与复盘

完成后查看 [[解答 - Tensor Programs、坐标检查与无限宽极限]]。复盘时把每条结论标记为 theorem assumption、finite simulation、implementation diagnostic 或 training evidence。
