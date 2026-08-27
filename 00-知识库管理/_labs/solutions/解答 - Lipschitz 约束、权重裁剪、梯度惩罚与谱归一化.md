---
type: solution
status: draft
topic: "[[Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]"
exercise: "[[习题 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Lipschitz 约束、权重裁剪、梯度惩罚与谱归一化
## A. 识别与复述
### GEN21-A01
$|f(x)-f(y)|\le K\|x-y\|$ 全域；凸域可微且 $\|\nabla f\|_*\le K$ 全域是充分条件。
### GEN21-A02
clipping 约参数；GP 在 real–fake 插值令 norm→1；R1 在 real 令 norm→0；SN 归一层 operator norm。
### GEN21-A03
$Lip(f)\le\|W_L\|_{op}\prod_{\ell<L}k_\ell\|W_\ell\|_{op}$。
## B. 手算与建模
### GEN21-B01
ReLU 为 1-Lipschitz，上界 $3\cdot2=6$。
### GEN21-B02
$[(.5-1)^2+0+(2-1)^2]/3=1.25/3\approx.4167$。
### GEN21-B03
若 penalty 为 $\gamma E\|\nabla f\|^2/2$，则 $E=(1+4)/2=2.5$，乘 $\gamma/2=5$，结果为 $12.5$。
## C. 推导与证明
### GEN21-C01
$f(y)-f(x)=\int_0^1\nabla f(x+t(y-x))^\top(y-x)dt$，用 Hölder 得绝对值不超过 $K\|y-x\|$。
### GEN21-C02
$\|f(g(x))-f(g(y))\|\le K_f\|g(x)-g(y)\|\le K_fK_g\|x-y\|$。
### GEN21-C03
$Lip(I+h)\le Lip(I)+Lip(h)\le1+K_h$；residual addition 不是取最大值。
## D. 边界、反例与纠错
### GEN21-D01
有限点集外插一个窄平滑 bump，令采样点 gradient 保持 1、bump 中斜率任意大；有限检查不覆盖全域。
### GEN21-D02
参数 box 并非函数 Lipschitz ball；同 clip 值下深度/宽度改变常数，且 projection metric 也不同。
### GEN21-D03
上界还乘 activation，residual 和、norm layers；且每层上界可能松，所以不必恰等于1。
## E. AI 迁移
### GEN21-E01
用真正 convolution operator norm、各支路和、activation、normalization statistics 与 power-iteration residual组成上界。
### GEN21-E02
在 chords、real邻域、fake邻域和随机空间点测 gradient norm分布；构造离插值支持远的 adversarial points。
### GEN21-E03
匹配 architecture/updates/wall-clock；分别调 penalty frequency/strength，报告 critic capacity、gradient分布、质量/覆盖与 failure rate。
