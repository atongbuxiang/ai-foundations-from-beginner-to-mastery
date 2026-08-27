---
type: solution
status: verified
area: [training, optimization, regularization]
topic: "[[L2 正则、Coupled Decay 与 AdamW]]"
exercise: "[[习题 - L2 正则、Coupled Decay 与 AdamW]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - L2 正则、Coupled Decay 与 AdamW

> [!warning] 使用边界
> “weight decay”首先是一步状态转移。配置名、论文名称与框架默认值都不能替代方程。

## A. 识别与复述

### TRN15-A01
$\nabla[L+\lambda\|\theta\|^2/2]=g+\lambda\theta$。无 momentum、无预条件且同一 LR 的 SGD 给
$$\theta^+=\theta-\eta g-\eta\lambda\theta=(1-\eta\lambda)\theta-\eta g,$$
因此与乘法收缩等价。若参数组、schedule 或更新顺序不同，仍需按合同核对。

### TRN15-A02
Coupled：把 $g_t+\lambda\theta_t$ 送入一阶/二阶状态，再由预条件器更新，示意为 $\theta^+=\theta-\eta P_t(g+\lambda\theta)$。AdamW：$m,v$ 只从 task $g$ 更新，参数另做 $\theta^+=\theta-\eta P_tg-\eta\lambda\theta$。前者使正则历史进入 state，后者分账。

### TRN15-A03
不同框架/类可能把同名参数实现为 gradient augmentation、直接 shrink、乘 LR 或不乘 LR；还可能排除 bias/norm、使用 fused kernel 或在 maximize 下改符号。必须查方程、源码/官方文档和一步测试。

## B. 手算与构造

### TRN15-B01
Coupled 位移为 $-0.1P(0.2,0.2)=(-0.02,-0.002)$，新参数 $(0.98,0.998)$。AdamW 直接收缩 $-0.1(0.2)(1,1)=(-0.02,-0.02)$，新参数 $(0.98,0.98)$。前者在欧氏坐标中各向异性。

### TRN15-B02
倍率 $(1-0.01)^{100}=0.99^{100}\approx0.366032$；$e^{-1}\approx0.367879$。指数近似很近，但不是精确相等，差来自 $\log(1-x)=-x-x^2/2-\cdots$。

### TRN15-B03
三步倍率
$$M=(1-0.1\cdot0.2)(1-0.05\cdot0.2)(1-0.01\cdot0.2)=0.98\cdot0.99\cdot0.998=0.9682596.$$
一阶指数近似 $\exp[-0.2(0.1+0.05+0.01)]=e^{-0.032}\approx0.968507$。

## C. 推导与证明

### TRN15-C01
直接展开上一式即可得到 SGD 等价。若 momentum 更新 $m_t=\beta m_{t-1}+g_t+\lambda\theta_t$，正则项被历史累计；直接 decay 则 $m_t=\beta m_{t-1}+g_t$，只在当前参数上收缩。即使当步看似都含 $-\eta\lambda\theta_t$，未来 $m$ 不同，轨迹不等价。

### TRN15-C02
纯 decay 递推 $\theta_t=(1-\eta_t\lambda_t)\theta_{t-1}$，归纳得乘积。令 $x_t=\eta_t\lambda_t$，
$$\log M_T=\sum_t\log(1-x_t)=-\sum_tx_t-\frac12\sum_tx_t^2+O(\sum_t|x_t|^3).$$
故 $M_T\approx e^{-\sum_tx_t}$，leading log-error 为 $-\tfrac12\sum_tx_t^2$。

### TRN15-C03
记 $a=1-\eta\lambda$。稳态方差 $S$ 满足 $S=a^2S+\eta^2$，故
$$S=\frac{\eta^2}{1-a^2}=\frac{\eta^2}{2\eta\lambda-\eta^2\lambda^2}=\frac{\eta}{2\lambda-\eta\lambda^2}.$$
当 $\eta\lambda\ll1$，$S\approx\eta/(2\lambda)$，所以 RMS $\approx\sqrt{\eta/(2\lambda)}$。

## D. 边界、反例与纠错

### TRN15-D01
取 $g=0,P=\operatorname{diag}(1,0.1),\theta=(1,1)$。Coupled L2 位移与 $(1,0.1)$ 成正比，decoupled decay 与 $(1,1)$ 成正比；只要第二坐标非零就不同。一般 $P\ne cI$ 时正则梯度也被预条件，破坏欧氏各向同性收缩。

### TRN15-D02
AdamW 常见倍率是 $1-\eta_t\lambda_t$，所以同一 $\lambda$ 配不同 LR 或 schedule 会给不同累计收缩。`decoupled` 指不把正则梯度送入自适应 state，不表示从 LR 因子中独立。

### TRN15-D03
公式需要：线性稳定递推、常数 $\eta,\lambda$、零均值 unit-variance $u_t$、时间独立/与参数独立、稳态、无初始化残留、无跨坐标相关、无 task drift，并忽略 $O(\eta\lambda)$ 修正。真实层还受 signal、schedule、normalization、parameter groups 和非平稳训练影响。

## E. AI 迁移

### TRN15-E01
逐参数记录 module/path、shape、role、decay group、理由和实际 optimizer group id。bias、LayerNorm/RMSNorm scale、embedding、输出头、共享权重与低秩适配参数常需单独决定；名称匹配会漏掉自定义模块、weight tying 或错误命名，应按模块类型与参数身份验证。

### TRN15-E02
先用零均值可控噪声、常 LR/decay 跑多 seed 至多个理论 time constants，扫 $\eta,\lambda$；记录 $\mathbb E\theta_t^2$ 的解析有限时解 $a^{2t}S_0+\eta^2(1-a^{2t})/(1-a^2)$、稳态估计与置信区间。再改变初始化和时长，验证早期偏离而非删除它。

### TRN15-E03
计算每个参数组的精确累计 $M=\prod_t(1-\eta_t\lambda_t)$，并同时报告 log shrink $\sum_t\log(1-\eta_t\lambda_t)$。若目标是相同 shrink，应解出使 $M$ 匹配的 $\lambda$；还要对齐训练步数、group exclusion 和 schedule 时钟。

## 无提示重做

- [ ] 48 小时后从随机递推推导 Weight RMS。
- [ ] 一周后用真实 optimizer config 重建各参数组累计 shrink。
