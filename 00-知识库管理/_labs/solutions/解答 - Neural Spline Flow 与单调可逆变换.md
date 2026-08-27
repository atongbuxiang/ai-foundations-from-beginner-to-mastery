---
type: solution
status: draft
topic: "[[Neural Spline Flow 与单调可逆变换]]"
exercise: "[[习题 - Neural Spline Flow 与单调可逆变换]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Neural Spline Flow 与单调可逆变换
## A. 识别与复述
### GEN38-A01
正 widths 使输入 knots 严格有序，正 heights 使输出 knots 严格有序，正 derivatives 使局部切线不翻转并参与严格单调。最小正值还避免 bins/斜率接近退化。
### GEN38-A02
固定输出 $y$ 并在已定位的 bin 中把 rational equation 交叉相乘，得到 normalized coordinate $\xi$ 的二次方程；选唯一落在 $[0,1]$ 的根即可解析恢复 $x$。
### GEN38-A03
外壳决定 conditioner 依赖、Jacobian 三角性和并行方向；spline 决定每个被更新坐标采用的单调可逆函数族及其 log derivative。
## B. 手算与建模
### GEN38-B01
平均 slopes $\delta_1=0.5/1=0.5$，$\delta_2=1.5/1=1.5$。左 bin 压缩，右 bin 拉伸。
### GEN38-B02
可分配长度 $4-3(0.2)=3.4$。widths 为 $0.2+3.4(0.5)=1.9$、$0.2+3.4(0.25)=1.05$、$1.05$，总和 4。
### GEN38-B03
编码局部 logdet $\log0.25=-\log4$。若 $y$ 是 latent，$\log p_X=\log p_Y+\log0.25$；编码压缩体积，对相同 latent density 的 data density乘 0.25。方向必须按变量定义核对。
## C. 推导与证明
### GEN38-C01
定义 $x^{(0)}=-B,x^{(k)}=-B+\sum_{j<k}w_j$。每一增量 $w_k>0$，故严格递增；总和 $2B$ 给最后 knot $B$。
### GEN38-C02
相邻公式在共享 knot 都取同一 $y^{(k)}$，所以函数连续；左右导数都被参数化为同一 $d_k$，故一阶导数也连续，即 $C^1$。
### GEN38-C03
连续严格递增函数把输入区间双射到端点对应的输出区间；介值定理给存在，严格递增给至多一个，合并为唯一。
## D. 边界、反例与纠错
### GEN38-D01
$w=10^{-30}>0$ 仍会产生巨大局部系数、bin search 边界误差和 inverse cancellation。正性是代数条件，浮点还需 minimum bin、clipping 和 dtype-specific tests。
### GEN38-D02
区间外 identity 的导数是 1；若内部边界导数不为 1，函数值可连续但导数跳跃，不再 $C^1$，gradient/logdet 在边界不连续。
### GEN38-D03
二次方程有两个代数根，只有一个对应当前 bin 的 $\xi\in[0,1]$。选另一个根会落出 bin、使 forward(inverse(y)) 不等于 $y$，甚至造成不连续跳转。
## E. AI 迁移
### GEN38-E01
每个被变换标量通常需 $K$ widths、$K$ heights 和约 $K+1$ derivatives，即约 $3K+1$ raw 参数；乘 $C_B$（和空间位置）。具体边界导数固定时可少输出，必须按实现声明。
### GEN38-E02
随机及边界点检查 forward→inverse、inverse→forward；analytic log derivative 对小步 central difference/autodiff；所有 roots 在 bin；knots 值/导数左右一致；极小 bin、tail、float32/64 和大 raw parameter stress tests。
### GEN38-E03
控制外壳、conditioner 参数/compute、层数、训练 schedule、dequantization、数据和 seed；报告 NLL、样本、round-trip、condition extrema、latency/显存。若 spline 参数更多，应做参数或 FLOP matched 两种对照。

