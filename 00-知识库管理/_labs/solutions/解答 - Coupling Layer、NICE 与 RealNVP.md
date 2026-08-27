---
type: solution
status: draft
topic: "[[Coupling Layer、NICE 与 RealNVP]]"
exercise: "[[习题 - Coupling Layer、NICE 与 RealNVP]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Coupling Layer、NICE 与 RealNVP
## A. 识别与复述
### GEN34-A01
$y_A=x_A,y_B=x_B+m(x_A)$；inverse 为 $x_A=y_A,x_B=y_B-m(y_A)$。Jacobian 块三角且对角为单位，determinant 为 1。
### GEN34-A02
$y_A=x_A,y_B=x_B\odot e^{s(x_A)}+t(x_A)$；inverse 为 $x_A=y_A,x_B=(y_B-t(y_A))\odot e^{-s(y_A)}$；生成方向 logdet 为 $\sum_js_j(x_A)$。
### GEN34-A03
逆向时保留块 $y_A=x_A$ 已知，可重新计算 $s(y_A),t(y_A)$，再逐元素反解 $x_B$。待反解的是 affine 操作，不是 conditioner 网络。
## B. 手算与建模
### GEN34-B01
输出 $(2,7)$；inverse 给 $x_1=2,x_2=7-4=3$。Jacobian $\begin{pmatrix}1&0\\2&1\end{pmatrix}$，det=1。
### GEN34-B02
$y_1=2,y_2=3\cdot4-2=10$；生成 logdet $\log4$。inverse 为 $(10+2)/4=3$。
### GEN34-B03
编码总 logdet $0.5$，data logprob $-5+0.5=-4.5$。
## C. 推导与证明
### GEN34-C01
上排导数是 $(I,0)$；下排左块含 $\partial s,\partial t$，右块是 $\operatorname{diag}(e^s)$。块下三角 determinant 是对角块 determinant 乘积，左下复杂块不参与，故为 $e^{\sum s_j}$。
### GEN34-C02
determinant 1 只保局部有向体积绝对值。剪切 $(x_1,x_2)\mapsto(x_1,x_2+ax_1)$ 会改变长度与夹角，例如 $(1,0)$ 与 $(0,1)$ 的像不再正交。
### GEN34-C03
第一层保留 A、更新 B；交换 mask 后第二层保留新的 B、更新新的 A。于是原 A 通过第二层 conditioner 被直接仿射更新，原 B 已在第一层更新。
## D. 边界、反例与纠错
### GEN34-D01
$s=-50$ 时 scale 非零但约 $1.9\times10^{-22}$，forward 压扁差异，inverse 乘 $e^{50}$ 放大舍入；代数非零不提供条件数上界。
### GEN34-D02
剪切 $y_2=x_2+x_1^2$ 非恒等且 det=1；它弯曲几何和改变边缘形状，只不改变局部体积。
### GEN34-D03
二维中永远取 $A=\{1\}$，则每层都有 $y_1=x_1$，任意复合后第一坐标仍原样。只有第二坐标被直接变换。
## E. AI 迁移
### GEN34-E01
$x_A:[B,C_A,H,W]$；conditioner 输出 $s,t:[B,C_B,H,W]$；生成 logdet 对 $C_B,H,W$ 求和，留下 $[B]$。不能把 batch 轴也求和后失去 per-sample likelihood。
### GEN34-E02
取 $d=4$、固定小网络和 double precision；autodiff 构造每个样本 $4\times4$ Jacobian，用 `slogdet` 与 $\sum s$ 比较，同时对 inverse direction 检查符号相反。覆盖随机值和接近 scale bound 的值。
### GEN34-E03
固定网络/数据/预算，仅改变 $s=\alpha\tanh\hat s$ 的 $\alpha$ 与不约束版本；报告 NLL、scale extrema、gradient norm、round-trip、Jacobian condition proxy 和 NaN 次数。表达力增益必须与数值失败共同呈现。

