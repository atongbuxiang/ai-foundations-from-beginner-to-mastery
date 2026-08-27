---
type: exercise
status: draft
area: [generative-models, normalizing-flows]
topic: "[[Residual Flow、可逆 ResNet 与 Logdet 估计]]"
solution: "[[解答 - Residual Flow、可逆 ResNet 与 Logdet 估计]]"
created: 2026-08-25
updated: 2026-08-25
---
# 习题 - Residual Flow、可逆 ResNet 与 Logdet 估计
## A. 识别与复述
### GEN37-A01
写出 $F=I+g$ 的充分可逆条件与 fixed-point inverse。
### GEN37-A02
写出 $\log\det(I+J_g)$ 的 trace series 及收敛条件。
### GEN37-A03
区分 inverse truncation、series truncation 与 Hutchinson sampling 三类误差。
## B. 手算与建模
### GEN37-B01
$F(x)=1.5x$，由 $y=3$、$x_0=0$ 做三次 $x_{k+1}=y-0.5x_k$，并与精确逆比较。
### GEN37-B02
$J_g=\operatorname{diag}(0.2,-0.4)$。求精确 $\log\det(I+J_g)$ 与前两项级数近似。
### GEN37-B03
$A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，Rademacher probe $v=(1,-1)^\top$。算 $v^TAv$ 并与 $\operatorname{tr}A$ 比较。
## C. 推导与证明
### GEN37-C01
用 Banach 不动点定理证明每个 $y$ 的 inverse 唯一。
### GEN37-C02
推导后验 inverse 误差界 $\|x_k-x^*\|\le L\|x_k-x_{k-1}\|/(1-L)$。
### GEN37-C03
证明 Hutchinson trace identity。
## D. 边界、反例与纠错
### GEN37-D01
说明 $L<1$ 是充分但非必要条件，给出线性反例。
### GEN37-D02
反驳“Hutchinson 无偏，所以有限阶 logdet 无偏”。
### GEN37-D03
构造 $L$ 接近 1 时数学可逆但 inverse 很慢的例子。
## E. AI 迁移
### GEN37-E01
设计 residual flow 的四账日志字段。
### GEN37-E02
比较增加 trace probes 与增加 series order 分别修复哪种误差。
### GEN37-E03
审计谱归一化提供全局 Lipschitz 证书的主张。
## 解答入口
[[解答 - Residual Flow、可逆 ResNet 与 Logdet 估计]]

