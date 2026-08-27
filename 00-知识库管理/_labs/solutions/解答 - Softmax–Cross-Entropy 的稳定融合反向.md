---
type: solution
status: draft
area: [neural-networks/losses, softmax, numerical-stability]
topic: "[[Softmax–Cross-Entropy 的稳定融合反向]]"
exercise: "[[习题 - Softmax–Cross-Entropy 的稳定融合反向]]"
sources: ["[[S-2022-Su-9070-logsumexp不等式]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Softmax–Cross-Entropy 的稳定融合反向
## A
### NN-SCE-A01
$z\in\mathbb R^K$ 是无约束 logits；$p_i=e^{z_i}/\sum_je^{z_j}$ 且 $p$ 在 probability simplex；target $y_i\ge0$ 且默认 $\sum_i y_i=1$；$\ell(z,y)=-\sum_i y_i\log p_i$。还要声明 class/sample weights、temperature、mask 和 batch reduction。
### NN-SCE-A02
$e^{z_i-a}/\sum_je^{z_j-a}=e^{z_i}/\sum_je^{z_j}$，公共因子 $e^{-a}$ 抵消。取 $a=\max z$ 使所有 exponent inputs 不大于 0 且有一项为 0，避免大正 logits 的 exponential overflow，不改变实数结果。
### NN-SCE-A03
$p-y$ 要求 $\sum_i y_i=1$、temperature $\tau=1$、无额外 class/sample scale，且是逐样本 unreduced loss。mean 还要除 valid count；temperature 给 $1/\tau$；未归一 target 给 $(\sum y)p-y$；weights/masks 对相应行或类再缩放。
## B
### NN-SCE-B01
减 $1000$ 后 exponentials 是 $(1,e^{-1},e^{-2})$，归一得 $p\approx(0.66524,0.24473,0.09003)$。真类 2 的 $\ell=-\log p_2\approx1.40761$，$\nabla_z\ell=p-e_2\approx(0.66524,-0.75527,0.09003)$。梯度和为 0。
### NN-SCE-B02
$\alpha=\sum_i y_i=3$，$\ell=3\operatorname{LSE}(z)-y^Tz$，故 $\nabla_z\ell=3p-(2,1,0)$。不是 $p-y$，因为每个 $\log p_i$ 中的 normalization term 被 target mass 总和 3 加权。
### NN-SCE-B03
三样本 mean 的每行 gradient 是 $(P_b-Y_b)/3$。若第 3 个是 padding 且被 mask，它的行梯度为 0，前两行分别为 $(P_b-Y_b)/2$；分母是 valid count 2，不是 batch storage size 3。
## C
### NN-SCE-C01
$d\operatorname{LSE}(z)=\sum_i\frac{e^{z_i}}{\sum_je^{z_j}}dz_i=p^Tdz$，而 $d(y^Tz)=y^Tdz$。所以 $d\ell=(p-y)^Tdz$，由欧氏内积下 gradient 的唯一性，$\nabla_z\ell=p-y$。
### NN-SCE-C02
$\partial p_i/\partial z_j=p_i\delta_{ij}-p_ip_j=p_i(\delta_{ij}-p_j)$，故 $J=\operatorname{diag}(p)-pp^T$。$\bar p_i=-y_i/p_i$，因 $J$ 对称，$J\bar p=-y+p\sum_i y_i=p-y$。该方法还显示 softmax 不需求逆。
### NN-SCE-C03
令 $s=z/\tau$，对 $s$ 的梯度是 $p^{(\tau)}-y$，而 $ds=dz/\tau$，故 $\nabla_z\ell=(p^{(\tau)}-y)/\tau$。若整个 distillation loss 再乘 $\tau^2$，对 logits 的该项变为 $\tau(p^{(\tau)}-y)$；这个外部 scale 是损失设计，不是 softmax 导数自动抵消。
## D
### NN-SCE-D01
取 $z=(1000,0)$ 且真类为第 2 类。naive $e^{1000}$ 溢出，softmax 可得 `(nan,0)` 或第二类概率 0，随后 NLL 为 `inf`。stable loss $1000+\log(1+e^{-1000})-0\approx1000$ 是有限的。
### NN-SCE-D02
$\ell$ 对自由 logits $z$ 的 Hessian 是 $\operatorname{diag}(p)-pp^T\succeq0$。但 $z=z_\theta(x)$ 是 parameters 的深层非线性函数，凸函数与任意非线性 inner map 复合不保凸。参数对称和多层乘积还会引入非凸曲率。
### NN-SCE-D03
softmax CE 适用于每样本只有一个互斥类，一类 probability 增加会挤压其他类。multi-label 如一张图同时有“狗”和“户外”，两标签可同时为 1，应用独立 sigmoid BCE；softmax 会错误强制二者竞争总质量 1。
## E
### NN-SCE-E01
对 $K$ 类，“全部类”定义应给真类 $1-\varepsilon+\varepsilon/K$、其他类 $\varepsilon/K$；“只错类”应给真类 $1-\varepsilon$、其他类 $\varepsilon/(K-1)$。测试直接检查 target vector、和为 1、loss 与 gradient，并选 $K=2,3$ 避免错实现偶然相同。
### NN-SCE-E02
每个 rank 计算 local NLL sum $S_r$ 和 valid token count $N_r$，all-reduce SUM 得 $S=\sum_rS_r$、$N=\sum_rN_r$，全局 loss $S/N$。gradient 可对 local sum backward 后 all-reduce SUM，再除 $N$；若 DDP 自动平均梯度，要显式补偿 world-size factor。padding rows 必须为 0。
### NN-SCE-E03
验证 $z+a\mathbf1$ 的 loss/probability/gradient 不变；测 $(1000,0)$、$(-1000,0)$ 的 finite loss/gradient；在 FP64 中心差分对照；比较 FP64/32/BF16/16 误差与 finite rate；测 one-hot/soft/smoothed/weighted targets；测 sum/mean/masked mean 和 distributed valid counts；与稳定未融合 reference 对照而不与 naive reference 对照。
