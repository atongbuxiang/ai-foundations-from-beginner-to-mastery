---
type: exercise
status: draft
area: [generative-models, normalizing-flows]
topic: "[[Coupling Layer、NICE 与 RealNVP]]"
solution: "[[解答 - Coupling Layer、NICE 与 RealNVP]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Coupling Layer、NICE 与 RealNVP
## A. 识别与复述
### GEN34-A01
写出 additive coupling 的 forward、inverse 和 determinant。
### GEN34-A02
写出 affine coupling 的 forward、inverse 和 logdet。
### GEN34-A03
为什么 conditioner 本身无需可逆？
## B. 手算与建模
### GEN34-B01
$y_1=x_1,y_2=x_2+2x_1$，输入 $(2,3)$。求输出、inverse 与 Jacobian。
### GEN34-B02
$s(x_1)=\log4,t(x_1)=-x_1$，输入 $(2,3)$。求输出和 logdet。
### GEN34-B03
两层 affine coupling 的编码 logdet 分别为 $1.2,-0.7$，base logprob $-5$。求 data logprob。
## C. 推导与证明
### GEN34-C01
逐块求 affine coupling Jacobian，并证明 determinant 与 $\partial s/\partial x_A,\partial t/\partial x_A$ 无关。
### GEN34-C02
证明 additive coupling 保体积，但不必保距离或角度。
### GEN34-C03
说明交替 mask 后两层怎样使两个分块都能被直接改变。
## D. 边界、反例与纠错
### GEN34-D01
反驳“$e^s>0$ 所以 numerical inverse 一定稳定”。
### GEN34-D02
反驳“det=1 的 NICE 只能实现恒等映射”。
### GEN34-D03
构造固定同一 mask 导致一个坐标永不直接更新的例子。
## E. AI 迁移
### GEN34-E01
为图像 channel coupling 写出 $s,t$ 的输入输出形状与 logdet reduction axes。
### GEN34-E02
设计 analytic logdet 与显式 Jacobian 的小维测试。
### GEN34-E03
比较 bounded log-scale 与 unrestricted log-scale 的表达—稳定折中实验。
## 解答入口
[[解答 - Coupling Layer、NICE 与 RealNVP]]

