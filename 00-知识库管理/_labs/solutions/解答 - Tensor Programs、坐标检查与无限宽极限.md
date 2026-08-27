---
type: solution
status: verified
area: [training, optimization, tensor-programs, infinite-width]
topic: "[[Tensor Programs、坐标检查与无限宽极限]]"
exercise: "[[习题 - Tensor Programs、坐标检查与无限宽极限]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Tensor Programs、坐标检查与无限宽极限

> [!warning] 使用边界
> Coordinate check 是当前 widths/steps/probes/statistics 的诊断；它既不扩展 theorem 适用域，也不直接验证超参数最优性。

## A. 识别与复述

### TRN44-A01
程序对象：宽向量变量、随机矩阵乘、逐坐标函数、经验平均；实际还要记录 shape/共享/状态。量词门：固定深度、固定宽度比例、固定有限训练步、有限 probe set、明确收敛模式。任何一项改变都可能需要新定理。

### TRN44-A02
GIA 把 backward 中的权重/转置当成与 forward 特征独立的新随机矩阵。实际上 $z=Wh$ 与 $W^\top\delta(z)$ 共享同一 $W$，$\delta$ 又依赖 $z$，存在闭环相关。只有满足相应结构检查时，独立捷径才可能给正确极限；否则 covariance/NTK 会算错。

### TRN44-A03
T1 检查 exponent 自洽；T2 检查 toy finite-sample moments；T3 检查真实实现的跨宽坐标趋势；T4 检查 loss、失败、HP drift 与 compute。T1/T2 不能替代真实代码，T3 不能替代超参数/性能，单次 T4 也不能反证所有理论假设。

## B. 手算与构造

### TRN44-B01
$$
\Sigma_z=2(0.3)+0.1=0.7.
$$
下一步需构造 $(u,v)$ 的二维 Gaussian joint covariance（含各自 variance 与 0.7 的 cross term），计算
$$
\mathbb E[\operatorname{ReLU}(u)\operatorname{ReLU}(v)].
$$
只知道 cross covariance 而无两边 variance 时还不足以给数值。

### TRN44-B02
width 每乘 4，RMS 乘 2，因此
$$
\widehat\kappa=\frac{\log2}{\log4}=\frac12.
$$
统计量约按 $\sqrt n$ 增长，支持爆炸趋势，不是水平。

### TRN44-B03
$$
m_1=\frac{n-1+|M|}{n},
\quad
m_2=\sqrt{\frac{n-1+M^2}{n}},
\quad
m_4=\left(\frac{n-1+M^4}{n}\right)^{1/4}.
$$
$m_4$ 对 $M^4$ 最敏感；当 $M\gg n^{1/4}$ 时其异常项已主导，而 $m_2$ 要到 $M\gg\sqrt n$ 才主导，$m_1$ 要到 $M\gg n$。

## C. 推导与证明

### TRN44-C01
条件在上一层 $h$ 上，
$$
\operatorname{Cov}(z_i(x),z_i(x')\mid h)
=\frac{\sigma_w^2}{n}\sum_jh_j(x)h_j(x')+\sigma_b^2.
$$
经验平均先由 LLN/程序定理趋于 $Q(x,x')$，得到 covariance 极限；随后多坐标随机和的 CLT/Gaussian program law给 joint Gaussian，才能把非线性期望写成 Gaussian integral。

### TRN44-C02
设误差界为 $e_{n,T}\le T/n$。对每个固定 $T$，$n\to\infty$ 时 $T/n\to0$；但若 $T(n)=n$，上界恒为 1，若 $T(n)=n^2$ 还发散。因此“对任意固定 $T$”的量词不能交换成“对随 $n$ 增长的 $T$”。

### TRN44-C03
可写
$$
\log m_{n,r}=c+\kappa\log n+b_r+\epsilon_{n,r},
$$
其中 $r$ 是 seed/block。少量 seed 使 slope 区间宽；width span 窄使分母 $\log(n_{max}/n_{min})$ 小；曲线弯曲时单一 slope 把局部趋势平均。应报告逐 width 点、残差、区间与最宽端反转，而非只报点估计。

## D. 边界、反例与纠错

### TRN44-D01
$m_1$ 可漏 heavy tail、operator norm、gradient/update、feature/logit 特殊瞬态；probe 可能不覆盖真实输入；只测早期固定步不覆盖长时；base/delta 或 scheduler metadata 仍可能在目标代码路径出错。更不包含 HP curve 和最终训练。

### TRN44-D02
在 width $n$ 的向量中，让一个坐标为 $n^{1/2}$，其余为 1。则
$$
m_1\approx1+n^{-1/2}\to1,
$$
但
$$
m_4^4\approx1+n,
$$
所以 $m_4\asymp n^{1/4}$。平均绝对值近似水平却有增长尾部。

### TRN44-D03
μP 可有意令 readout/attention 初始随机量按 $1/\sqrt n$ 收缩，为训练后的对齐更新留尺度。区分方法是记录预期表：$t=0$ 可下降，但 $t=1,2,\ldots$ 应转为水平且非零；同时检查 loss、feature/update。若训练后仍按负 slope 消失，才是失败信号。

## E. AI 迁移

### TRN44-E01
例如 widths $64$—$1024$，steps $0,1,2,4,8$，固定同一 probe batch/data order，至少 3 seeds；记录 $m_1,m_2,m_4$、gradient/update/feature/logit 与 spectral proxy。预先标记 readout/attention init 例外，门限包括 slope、最宽/最窄 ratio、非有限值与 loss/entropy collapse。

### TRN44-E02
- recurrent：同一矩阵跨 time 重复几次，state 是否依赖此前同一权重？
- tying：输入 lookup 与输出 transpose 是否共享参数，两个 gradient role 怎样相加？
- Q/K：是否真是独立参数，还是共享/转置/旋转变换；attention score 和 backward 是否再次使用它们？
不满足结构检查时不得替换为独立矩阵。

### TRN44-E03
候选：HP objective 本身随 data/time/regularization 变；proxy 太窄有 finite-width bias；coord 只测 moments 未测 feature/kernel；optimizer $\epsilon$/state 在真实训练区不同；target depth/aspect/head path 或 system reduction 改变；search noise/flat minimum 造成 argmin漂移。分别用更宽 proxy、完整 HP curves、额外 telemetry、optimizer-state sweep、轴隔离和多 seed 区分。

## 无提示重做

- [ ] 48 小时后重建 covariance recursion 与量词门。
- [ ] 一周后设计一个能让 $m_1$ 漏检、$m_4$ 抓到的反例。
