---
type: solution
status: verified
area: [training, optimization, numerical-computing]
topic: "[[Adam 的 Epsilon、数值稳定与实现分歧]]"
exercise: "[[习题 - Adam 的 Epsilon、数值稳定与实现分歧]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Adam 的 Epsilon、数值稳定与实现分歧

> [!warning] 使用边界
> 比较优化器必须先锁定公式。相同参数名不保证相同量纲、相同运算图或相同舍入轨迹。

## A. 识别与复述

### TRN12-A01
Root-out：$u=m/(\sqrt v+\epsilon_{out})$，所以 $\epsilon_{out}$ 与 $\sqrt v$ 同单位，即梯度单位。Root-in：$u=m/\sqrt{v+\epsilon_{in}}$，故 $\epsilon_{in}$ 与 $v$ 同单位，即梯度平方单位。数值都写 $10^{-8}$ 并不表示同一稳定尺度。

### TRN12-A02
若 $\sqrt v\gg\epsilon$，$u\approx m/\sqrt v$，接近自适应归一化区。若 $\sqrt v\ll\epsilon$，$u\approx m/\epsilon$，分母几乎固定，更新对梯度尺度近似线性而不再抵消。

### TRN12-A03
代数等价指在实数域可由恒等变换互推；实数运算等价允许不同写法给同一精确映射；有限精度等价还要求指定 dtype、舍入、融合、求值顺序和异常处理后结果一致。前两层不自动推出最后一层。

## B. 手算与构造

### TRN12-B01
$\sqrt v=10^{-8}$。Root-out：$u=10^{-6}/(2\times10^{-8})=50$。Root-in：分母 $\sqrt{10^{-16}+10^{-8}}\approx10^{-4}$，$u\approx0.01$。两者相差约 5000 倍，原因是同一字面 epsilon 具有不同单位。

### TRN12-B02
同步缩放后
$$u'=\frac{cm}{c\sqrt v+\epsilon}=\frac{m}{\sqrt v+\epsilon/c}.$$
与 $u=m/(\sqrt v+\epsilon)$ 的差异由 $r=\epsilon/\sqrt v$ 及缩放 $c$ 控制；精确比
$$\frac{u'}u=\frac{1+r}{1+r/c}.$$

### TRN12-B03
Root-out 在 $v=0$ 的分母为 $10^{-8}$。Root-in 要满足 $\sqrt{\epsilon_{in}}=10^{-8}$，故 $\epsilon_{in}=10^{-16}$。这只是零附近尺度匹配，不保证所有 $v$ 上两函数相同。

## C. 推导与证明

### TRN12-C01
当 $v>0$，分子分母同除 $\sqrt v$：
$$\frac m{\sqrt v+\epsilon}=\frac{m/\sqrt v}{1+\epsilon/\sqrt v}.$$
$r=\epsilon/\sqrt v$ 无量纲；$r\ll1$ 时 epsilon 可忽略，$r\gg1$ 时方向约 $m/\epsilon$。它比孤立报告 epsilon 更能判断工作区间。

### TRN12-C02
令 $x=g/\epsilon$。$|x|\ll1$ 时 $(1+x^2)^{-1/2}=1-\tfrac12x^2+O(x^4)$，故
$$u=\frac g\epsilon-\frac{g^3}{2\epsilon^3}+O(g^5/\epsilon^5).$$
$|g|\gg\epsilon$ 时
$$u=\operatorname{sign}(g)\left(1-\frac{\epsilon^2}{2g^2}+O(\epsilon^4/g^4)\right).$$
所以它在小梯度区近线性、大梯度区近 sign。

### TRN12-C03
$\epsilon=0$ 时 $u'=cm/\sqrt{c^2v}=m/\sqrt v$。固定 root-out epsilon 时
$$\frac{u'}u=\frac{cm}{c\sqrt v+\epsilon}\frac{\sqrt v+\epsilon}{m}
=\frac{\sqrt v+\epsilon}{\sqrt v+\epsilon/c}.$$
除非 $c=1$、$\epsilon=0$ 或 epsilon 可忽略，否则不等于 1。

## D. 边界、反例与纠错

### TRN12-D01
在 $m=10^{-9},\sqrt v=10^{-12}$ 时，root-out $\epsilon=10^{-8}$ 给 $u\approx0.1$；若 $\epsilon=10^{-4}$ 则 $u\approx10^{-5}$，相差约 $10^4$。epsilon 决定小尺度坐标的增益、尺度不变性断点和可能的 underflow 行为，并非只在精确零点生效。

### TRN12-D02
实现 A 用 $m/(\sqrt v+10^{-8})$；实现 B 用 $m/\sqrt{v+10^{-8}}$。二者日志都可打印同名 `eps=1e-8`，但量纲与数值映射不同。也可再叠加 epsilon 是否在 bias correction 前后的差异。

### TRN12-D03
恒等式 $(\sqrt v+\epsilon)^2=v+2\epsilon\sqrt v+\epsilon^2$，一般不等于 $v+\epsilon$。这不是舍入次序调整，而是改变函数；只有重新标定且在限定 regime 做近似时才可比较，并必须标注误差。

## E. AI 迁移

### TRN12-E01
按层记录 $\sqrt{\hat v}$ 的分位数及 $r_i=\epsilon/\sqrt{\hat v_i}$，同时记录 $m/\sqrt v$ 与实际 $m/(\sqrt v+\epsilon)$ 的 update RMS 比、zero/underflow 比例和 accumulator dtype。大量 $r_i\gg1$ 才表明 epsilon 主导。

### TRN12-E02
用固定小张量和显式梯度序列，逐步导出 $m,v$、bias factors、denominator、direction、delta 与 step；两框架禁用 weight decay/fusion 后先比一步，再比两步和 checkpoint 恢复。第一处分叉若在 denominator 定位 epsilon；在 $hat m/\hat v$ 定位修正；在 state counter 定位推进顺序。

### TRN12-E03
需检查固定 epsilon 导致的尺度断点、gradient clipping、coupled L2/decay、loss scaling 与 unscale 顺序、有限精度/underflow、状态是否同步缩放、不同参数组、schedule 与中途尺度切换。经典恒等式只覆盖正比例缩放的完整历史、相同状态变换和 epsilon 可忽略等条件。

## 无提示重做

- [ ] 48 小时后用量纲分析判断两个 epsilon 公式。
- [ ] 一周后设计跨框架一步更新的 state-by-state 对齐表。
