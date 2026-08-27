---
type: solution
status: verified
area: [training, optimization, acceleration]
topic: "[[Nesterov、Lookahead 与动量形式的等价边界]]"
exercise: "[[习题 - Nesterov、Lookahead 与动量形式的等价边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Nesterov、Lookahead 与动量形式的等价边界

## A. 识别与复述

### TRN05-A01
Heavy-ball：$v_{t+1}=\mu v_t-\eta\nabla f(x_t)$，$x_{t+1}=x_t+v_{t+1}$，求值点是 $x_t$。NAG：$y_t=x_t+\mu v_t$，$g_t=\nabla f(y_t)$，$v_{t+1}=\mu v_t-\eta g_t$，$x_{t+1}=x_t+v_{t+1}$，求值点是 $y_t$。

### TRN05-A02
Nesterov look-ahead 是每一步用 velocity 外推求 gradient；Lookahead optimizer 通常让 fast weights 连续走 $k$ 步，再把 slow weights 朝 fast weights 插值。状态、时间尺度与更新式都不同。

### TRN05-A03
常 learning rate、常 momentum、无 dampening/额外 transforms、精确状态映射 $p_t=x_t+\mu v_t$、$b_t=-v_t/\eta$、一致初始化与索引。变化 LR/momentum 或 restart 后需重新推导。

## B. 手算与构造

### TRN05-B01
$y_0=1+.9(0)=1$；$g_0=1$；$v_1=.9(0)-.1(1)=-.1$；$x_1=1-.1=.9$；$y_1=.9+.9(-.1)=.81$。

### TRN05-B02
$b_1=.9(0)+1=1$；$p_1=p_0-.1(g_0+.9b_1)=1-.19=.81$，与上题 $y_1$ 相同。它不等于 base iterate $x_1=.9$。

### TRN05-B03
$\nabla f(x)=x^3=1$。Look-ahead point $1+.9(-.5)=.55$，gradient $=.55^3=.166375$。两者差很大，说明求值点不是装饰性符号。

## C. 推导与证明

### TRN05-C01
$p_{t+1}=x_{t+1}+\mu v_{t+1}=x_t+(1+\mu)v_{t+1}$；又 $x_t=p_t-\mu v_t$，故 $p_{t+1}=p_t-\mu v_t+(1+\mu)v_{t+1}$。代入 $v_{t+1}=\mu v_t-\eta g_t$，整理为 $p_t+\mu v_{t+1}-\eta g_t$。

### TRN05-C02
由 $b_{t+1}=-v_{t+1}/\eta$ 得 $\mu v_{t+1}=-\eta\mu b_{t+1}$，所以

$$p_{t+1}=p_t-\eta(g_t+\mu b_{t+1}).$$

同时 velocity recurrence 除以 $-\eta$ 得 $b_{t+1}=\mu b_t+g_t$。

### TRN05-C03
若 $f$ 二次连续可微，

$$\nabla f(x+\mu v)=\nabla f(x)+\mu H(x)v+R,$$

若 Hessian Lipschitz 常数为 $M$，可界 $\|R\|\le M\mu^2\|v\|^2/2$。Hessian correction 解释局部预见 curvature；它不是 NAG rate proof。

## D. 边界、反例与纠错

### TRN05-D01
取 $g_0=g_1=1,\mu=.9,\eta_0=.1,\eta_1=.01$。若用 buffer，第二步 $b_1=1.9$，对应 displacement $-.019$；朴素 velocity 从 $v_0=-.1$ 得 $v_1=-.1$。比例已不再由一个常 $-\eta$ 保持。

### TRN05-D02
框架 parameter $p_t$ 可以对应 classical derivation 的 $y_t$。梯度是在“当前存储的 $p_t$”计算，同时也正是在 classical NAG 的 look-ahead point 计算。正确判断需要变量映射；只比较源码是否显式写 `x + mu*v` 会误判。

### TRN05-D03
Dampening 改变 $b_{t+1}$ 中 $g_t$ 的系数，momentum schedule 改变 $p_t=x_t+\mu_tv_t$ 的定义。原推导中的系数抵消不再成立，必须加入 $\mu_t,\eta_t$ 的比值和索引。

## E. AI 迁移

### TRN05-E01
记录 $p_t$、raw $g_t$、更新后的 buffer $b_{t+1}$、实际 direction $d_t=g_t+\mu b_{t+1}$、$\Delta p_t$ 和 step index；用 float64 标量 quadratic 与手工 reference 比较前 3–5 步。

### TRN05-E02
询问精确方程/gradient point、velocity 是否含 LR、参数变量对应 base 还是 look-ahead、buffer 初始化、索引先后、dampening、momentum schedule、weight decay、框架/版本和 scheduler call order。

### TRN05-E03
固定模型、数据顺序、budget、reduction、decay 和调参规则；对各自合理 LR/momentum 做预注册搜索；记录 train/validation、gradient/update norm、局部 top curvature、mode oscillation/overshoot、steps、FLOPs 和 wall time，多 seed 报 interval。

## 无提示重做

- [ ] 从四行 classical NAG 独立推到 buffer 形式。
- [ ] 能指出框架 parameter 究竟对应 $x_t$ 还是 $y_t$。
