---
type: solution
status: verified
area: [training, optimization, adaptive-optimization]
topic: "[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"
exercise: "[[习题 - Adam 的一阶二阶矩、偏差修正与逐坐标步长]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Adam 的一阶二阶矩、偏差修正与逐坐标步长

> [!warning] 使用边界
> 偏差修正是对零初始化 EMA 的期望修正，不是对随机比值、优化误差或泛化误差的无偏证书。

## A. 识别与复述

### TRN11-A01
逐坐标
$$m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\qquad v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,$$
$$\hat m_t=m_t/(1-\beta_1^t),\quad \hat v_t=v_t/(1-\beta_2^t),\quad
\theta_t=\theta_{t-1}-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.$$
$m,v,g,\theta$ 通常同 shape；step 可为参数组或参数状态，必须查实现。

### TRN11-A02
从零开始的 EMA 权重和只有 $1-\beta^t<1$，故对平稳均值会向零缩。分别除以 $1-\beta_1^t$ 与 $1-\beta_2^t$ 把缺失的总权重补回 1。

### TRN11-A03
$\eta$ 是参数组给定的 global LR；$1/(\sqrt{\hat v_i}+\epsilon)$ 是坐标乘子；$u_i=\hat m_i/(\sqrt{\hat v_i}+\epsilon)$ 是无 LR 的 normalized direction；参数位移为 $\Delta\theta_i=-\eta u_i$，若有 decay、clipping 或 schedule 还要写完整合同。

## B. 手算与构造

### TRN11-B01
第一步：$m_1=1,v_1=1$；$\hat m_1=2,\hat v_1=4$，$u_1=1$，$\Delta\theta_1=-0.1$。第二步：$m_2=0.5(1)+0.5(4)=2.5$，$v_2=0.75(1)+0.25(16)=4.75$；$\hat m_2=2.5/0.75=10/3$，$\hat v_2=4.75/0.4375=76/7$。故
$$u_2=\frac{10/3}{\sqrt{76/7}}\approx1.0114,\qquad\Delta\theta_2\approx-0.10114.$$

### TRN11-B02
$m_t=g(1-\beta_1^t)$、$v_t=g^2(1-\beta_2^t)$，故 $\hat m_t=g$、$\hat v_t=g^2$。当 $g>0$ 且 $\epsilon=0$，$u_t=g/|g|=1$；若 $g<0$ 则为 $-1$。

### TRN11-B03
$u=(1,0.1)$，所以 $\Delta\theta=(-0.01,-0.001)$。虽然一阶矩方向是 $(1,1)$，第二坐标的历史平方尺度大 100 倍，预条件后欧氏方向转向第一坐标。

## C. 推导与证明

### TRN11-C01
展开
$$m_t=(1-\beta_1)\sum_{j=1}^t\beta_1^{t-j}g_j.$$
线性期望及各时刻共同均值 $\mu$ 给
$$\mathbb E m_t=(1-\beta_1)\mu\frac{1-\beta_1^t}{1-\beta_1}=(1-\beta_1^t)\mu.$$
不需要时间独立，但需要这些边际均值相同且可积。

### TRN11-C02
同理
$$v_t=(1-\beta_2)\sum_{j=1}^t\beta_2^{t-j}g_j^2,$$
若所有 $j$ 有有限且相同二阶矩 $\nu$，则期望为 $(1-\beta_2^t)\nu$。这里需要二阶矩平稳；不要求独立来求均值，但后续方差/比值近似通常需要更强相关性条件。

### TRN11-C03
非线性函数 $f(x,y)=x/\sqrt y$ 一般不与期望交换，而且 $\hat m,hat v$ 由同一梯度历史构造、彼此相关。因此分别满足 $\mathbb E\hat m=\mu,\mathbb E\hat v=\nu$ 只约束两个边际一阶矩，不能决定 $\mathbb E f(\hat m,\hat v)$。只有退化变量或附加近似才能把比值替换为期望之比。

## D. 边界、反例与纠错

### TRN11-D01
令 $X=Y$，且 $Y$ 以等概率取 1、4。则 $\mathbb E X/\mathbb E Y=1$，但 $\mathbb E[X/\sqrt Y]=\mathbb E\sqrt Y=(1+2)/2=1.5$，而 $\mathbb E X/\sqrt{\mathbb E Y}=2.5/\sqrt{2.5}\approx1.581$。三者不同。

### TRN11-D02
实际位移是 $-\eta\hat m_i/(\sqrt{\hat v_i}+\epsilon)$，归一化比值可小于、等于或在某些变动序列中大于 1；各坐标还不同。只有恒定同号梯度、零 epsilon 等特殊情形才得到大小 $\eta$。

### TRN11-D03
偏差修正显式依赖 $t$。若真实 state 在第 1000 步却把 counter 重置为 0/1，分母 $1-\beta^t$ 改变；某些实现还由 step 决定 schedule 或 state dtype。即使 $m,v$ 恢复，$hat m,hat v$ 也会错。

## E. AI 迁移

### TRN11-E01
至少按层/参数组记录：global LR、$\operatorname{RMS}(g)$、$\operatorname{RMS}(m)$、$\operatorname{RMS}(\sqrt v)$、normalized update RMS、parameter delta RMS、parameter RMS，以及 decay/clip 的独立贡献。`lr` 只给外层倍率。

### TRN11-E02
选一维固定梯度序列如 $2,4$，用高精度手算或小参考实现得到每步 $m,v,\hat m,\hat v,\theta$；初始化参数与 optimizer 后逐步喂入显式梯度，断言所有状态和 step counter；另做 checkpoint 恢复和 skipped-step 测试。

### TRN11-E03
标准 accumulation 先把 micro-gradient 按约定合成一个 estimator，再在 optimizer step 更新一次 $m,v$。若每个 micro-batch 都推进状态，EMA 时间常数、偏差修正指数和非线性平方平均全变了；即使最终平均梯度相同，trajectory 也不等价。

## 无提示重做

- [ ] 48 小时后完整手算两步 Adam，不省略修正项。
- [ ] 一周后给出“矩无偏但比值不无偏”的新反例。
