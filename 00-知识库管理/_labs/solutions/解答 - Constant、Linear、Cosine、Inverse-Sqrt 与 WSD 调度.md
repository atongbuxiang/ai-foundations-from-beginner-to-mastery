---
type: solution
status: verified
area: [training, optimization, learning-rate, schedule]
topic: "[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]"
exercise: "[[习题 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度

> [!warning] 使用边界
> schedule 的面积只是控制量摘要；相同面积不保证相同轨迹，离散端点和 optimizer state 仍可能改变结果。

## A. 识别与复述

### TRN35-A01
归一化时间 $s\in[0,1]$ 下，constant 为 $\eta(s)=\eta_0$；linear-to-zero 为 $\eta_0(1-s)$；cosine-to-zero 为 $\frac{\eta_0}{2}[1+\cos(\pi s)]$。inverse-sqrt 常写 $\eta_t=C/\sqrt{t+t_0}$，需给 offset/匹配点与是否先 warmup。所有式子还需离散索引、horizon、final floor 和 clock 才能成为实现。

### TRN35-A02
$\sum\eta_t$ 是一阶漂移和 decoupled-decay 累积指数的近似尺度；$\sum\eta_t^2$ 常进入随机噪声方差和二阶余项。它们都不包含方向、曲率与相关结构，故应视为账本而非性能充分统计量。

### TRN35-A03
WSD 先用与未来停止时刻弱耦合的 warmup/stable trunk，再从选定 checkpoint 做 cooldown/decay branch。它避免 full-horizon decay 在延长训练时改写共同 trunk；但 cooldown 长度、形状、末端 LR 与 branch 选择仍依赖计划停止点，依赖被局部化而非消失。

## B. 手算与构造

### TRN35-B01
将 peak 归一化为 1：

| schedule | $\int_0^1\eta(s)ds$ | $\int_0^1\eta(s)^2ds$ |
|---|---:|---:|
| constant | $1$ | $1$ |
| linear | $1/2$ | $1/3$ |
| cosine | $1/2$ | $3/8$ |

cosine 与 linear 一阶面积相同，但 cosine 的平方面积更大，已说明“同面积”不足以同化两条路径。

### TRN35-B02
包含两个端点的 5 个 update 应使用 $t/(N-1)$：
$$
(1,0.75,0.5,0.25,0).
$$
若误用分母 $N=5$，得到 $(1,0.8,0.6,0.4,0.2)$，最后没有到零。反之若循环索引又多跑一次，可能产生第六个零值；实现必须同时核对数组长度和 endpoint。

### TRN35-B03
constant 的 shrinkage 为
$$
(1-0.2\cdot0.1)^5=0.98^5=0.9039207968.
$$
变 schedule 的 product 是
$$
0.96\cdot0.97\cdot0.98\cdot0.99\cdot1=0.90345024.
$$
两组 $\sum\eta_t$ 都为 1，但精确 product 略不同；只有小 $\eta\lambda$ 下 $\log(1-\eta\lambda)\approx-\eta\lambda$ 才主要由面积决定。

## C. 推导与证明

### TRN35-C01
令 $c(s)=[1+\cos(\pi s)]/2$，则
$$
\int_0^1c(s)ds=\frac12,
$$
因为 cosine 积分为零。平方为 $(1+2\cos\pi s+\cos^2\pi s)/4$，其中 $\int\cos=0,\int\cos^2=1/2$，故平方面积 $3/8$。linear 的对应值为 $1/2,1/3$。

### TRN35-C02
对递减函数 $x^{-1/2}$ 用积分夹逼：
$$
\int_1^{T+1}x^{-1/2}dx
\le\sum_{t=1}^Tt^{-1/2}
\le1+\int_1^Tx^{-1/2}dx,
$$
两侧都为 $2\sqrt T+O(1)$，故是 $\Theta(\sqrt T)$。平方后成为调和和 $\sum1/t=\Theta(\log T)$。

### TRN35-C03
设 warmup 长 $W$、stable 到 $S$、总长 $T$：
$$
\eta(t)=
\begin{cases}
\eta_0+(\eta_p-\eta_0)t/W,&0\le t\le W,\\
\eta_p,&W<t\le S,\\
\eta_f+(\eta_p-\eta_f)(T-t)/(T-S),&S<t\le T.
\end{cases}
$$
连接连续要求 warmup 末为 $\eta_p$、cooldown 初为 $\eta_p$、末为 $\eta_f$。离散实现还要决定 $W,S,T$ 是否是点数或间隔数；连续公式不能消除 $N$ 与 $N-1$ 的差异。

## D. 边界、反例与纠错

### TRN35-D01
在 $[0,1]$ 上 constant、linear、cosine 都可有 peak 1、final 分别设为相同端点，但 constant 面积 1，linear/cosine 面积 $1/2$；平方面积也为 $1,1/3,3/8$。所以相同 peak/final 不等于相同漂移、噪声或 decay budget。

### TRN35-D02
原 horizon 下
$$
\eta_t(T)=\tfrac12\eta_{max}[1+\cos(\pi t/T)],
$$
新 horizon 下是
$$
\eta_t(2T)=\tfrac12\eta_{max}[1+\cos(\pi t/(2T))].
$$
对 $0<t<T$，两个角度不同，且 cosine 在 $(0,\pi)$ 严格递减，所以值不同。已走过的参数与状态不能事后按新 LR 重算。

### TRN35-D03
停止时刻决定何时从 stable trunk 分支、cooldown 有多少步及末端到哪里；不同分支还改变 $\prod(1-\eta_t\lambda_t)$、选择候选数和计算预算。WSD 提供可复用 trunk，但不提供对任意停止点都完全相同的尾部算法。

## E. AI 迁移

### TRN35-E01
manifest 至少含 `clock, index_origin, num_updates, warmup_start/end/length, stable_length, cooldown_shape/length, final_floor, horizon, per_group_multiplier, overflow_advance, resume_counter, version`。自动断言数组长度、首末值、连接点、非负性、单调段、面积、平方面积与 resume 后下一值。

### TRN35-E02
主实验固定总 tokens/FLOPs、数据顺序、optimizer、peak 候选搜索预算和输出选择规则；每种 schedule 使用等量调参。可以把“各自预算内最佳”作为主比较，再做 peak-matched 与 area-matched 敏感性分析。不要只强行匹配一个面积后宣称完全公平，因为路径和状态耦合不同。

### TRN35-E03
复现还需离散公式、点数/间隔数、clock、warmup/decay 连接、final floor、parameter-group multiplier、overflow、resume 与 weight decay schedule。自动测试首/末/转折点，求 $\sum\eta,\sum\eta^2$，检查 monotonicity、负值、step count，并对一段中断—恢复轨迹逐字节比较 LR 日志。

## 无提示重做

- [ ] 48 小时后手算三条归一化曲线的两种面积。
- [ ] 一周后解释 WSD 转移而非消除 horizon dependency。
