---
type: exercise
status: draft
area: [generative-models, normalizing-flows]
topic: "[[Neural Spline Flow 与单调可逆变换]]"
solution: "[[解答 - Neural Spline Flow 与单调可逆变换]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Neural Spline Flow 与单调可逆变换
## A. 识别与复述
### GEN38-A01
正 widths、heights、derivatives 分别保证什么？
### GEN38-A02
为什么 rational-quadratic spline 的 inverse 可解析？
### GEN38-A03
coupling/autoregressive 外壳与 spline transform 各负责什么？
## B. 手算与建模
### GEN38-B01
$[-1,1]$ 两个输入 widths $(1,1)$、输出 heights $(0.5,1.5)$。求两 bin 平均 slopes。
### GEN38-B02
$2B=4,K=3,w_{min}=0.2$，softmax 权重 $(1/2,1/4,1/4)$。求三 widths。
### GEN38-B03
若单调 transform 在一点 $dy/dx=0.25$，编码方向 $x\to y$ 的局部 logdet 是多少？该处 density 如何变化？
## C. 推导与证明
### GEN38-C01
证明正 widths 且总和 $2B$ 产生严格递增输入 knots。
### GEN38-C02
说明共享 knot values/derivatives 为何给分段函数 $C^1$ 连续。
### GEN38-C03
说明严格单调加连续为何保证每个输出 bin 内 inverse 唯一。
## D. 边界、反例与纠错
### GEN38-D01
反驳“参数为正就一定数值稳定”。
### GEN38-D02
若 identity tail 边界导数不是 1，会发生什么光滑性问题？
### GEN38-D03
为什么二次公式任取一个根会破坏 inverse？
## E. AI 迁移
### GEN38-E01
计算 coupling spline conditioner 的输出通道量级。
### GEN38-E02
设计 spline 的 forward/inverse/logdet 单元测试。
### GEN38-E03
公平比较 affine 与 spline coupling 应控制什么？
## 解答入口
[[解答 - Neural Spline Flow 与单调可逆变换]]

