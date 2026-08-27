---
type: solution
status: verified
area: [training, optimization, adaptive-optimization]
topic: "[[RMSProp、滑动二阶矩与非平稳尺度]]"
exercise: "[[习题 - RMSProp、滑动二阶矩与非平稳尺度]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - RMSProp、滑动二阶矩与非平稳尺度

> [!warning] 使用边界
> “约记住 $1/(1-\rho)$ 步”只是工程量级。半衰期、e-fold 和方差意义下的有效样本量回答不同问题。

## A. 识别与复述

### TRN10-A01
$v_t=\rho v_{t-1}+(1-\rho)g_t^2$，$\theta_t=\theta_{t-1}-\eta g_t/(\sqrt{v_t}+\epsilon)$（逐坐标）。$v_t$ 平滑的是 $g^2$，其期望目标是 $\mathbb E[g^2]$；方差是 $\mathbb E[g^2]-(\mathbb E g)^2$。只有均值为零时二者相同。

### TRN10-A02
单个历史样本权重按 $\rho^k$ 衰减。e-fold 尺度 $k_e=-1/\log\rho\approx1/(1-\rho)$；半衰期 $k_{1/2}=\log(1/2)/\log\rho$；无限 EMA 的 $N_{\rm eff}=(1+\rho)/(1-\rho)$。

### TRN10-A03
AdaGrad 给所有历史平方梯度永久权重 1；RMSProp 给距今 $k$ 步权重 $(1-\rho)\rho^k$，会指数遗忘。遗忘提高对尺度漂移的响应，却增加估计方差并可能让久未出现的风险重新被低估。

## B. 手算与构造

### TRN10-B01
$v_1=0.4$，$v_2=0.9(0.4)+0.4=0.76$，$v_3=0.9(0.76)+0.4=1.084$。方向分别为 $2/\sqrt{0.4}\approx3.162$、$2/\sqrt{0.76}\approx2.294$、$2/\sqrt{1.084}\approx1.920$。早期 $v_t$ 从零启动，故未修正方向偏大。

### TRN10-B02
切换前稳态 $v_0=a$。递推解为
$$v_k=b+\rho^k(a-b)=\rho^ka+(1-\rho^k)b.$$
新旧差距变成一半要求 $\rho^k=1/2$，故 $k=\log(1/2)/\log\rho$；非整数时取满足阈值的最小整数。

### TRN10-B03
$\rho=0.99$：$k_e=-1/\log0.99\approx99.5$；$k_{1/2}\approx68.97$；$N_{\rm eff}=1.99/0.01=199$。前两者描述单个冲击权重的衰减时间，后者把所有归一化权重的平方和换算成同方差的均匀样本数。

## C. 推导与证明

### TRN10-C01
反复代入：
$$v_t=\rho[\rho v_{t-2}+(1-\rho)g_{t-1}^2]+(1-\rho)g_t^2,$$
继续至 $v_0$，得到 $\rho^tv_0+(1-\rho)\sum_{j=1}^t\rho^{t-j}g_j^2$。也可用归纳法验证递推与初值。

### TRN10-C02
把 $g_j^2=q$ 代入几何和：$v_t=(1-\rho)q(1-\rho^t)/(1-\rho)=q(1-\rho^t)$。若 $g_t$ 同号且大小 $\sqrt q$，则方向大小为 $1/\sqrt{1-\rho^t}>1$，相对稳态被放大因子 $(1-\rho^t)^{-1/2}$。

### TRN10-C03
$$\sum_{k=0}^\infty w_k^2=(1-\rho)^2\sum_{k=0}^\infty\rho^{2k}=\frac{(1-\rho)^2}{1-\rho^2}=\frac{1-\rho}{1+\rho}.$$
取倒数即 $N_{\rm eff}=(1+\rho)/(1-\rho)$。它依赖独立同方差观测的方差匹配解释。

## D. 边界、反例与纠错

### TRN10-D01
EMA 没有硬窗口；第 101 步以前的样本权重不为零，最近 100 步权重也不均匀。$100$ 只是 $1/(1-\rho)$ 的量级；e-fold 约 99.5、半衰期约 69、$N_{\rm eff}$ 约 199，必须说明使用哪个定义。

### TRN10-D02
稳态正常 $g^2=1$，一次尖峰 $g_0^2=M^2$ 后，额外二阶矩为 $(1-\rho)M^2\rho^k$。若 $M=100,\rho=0.99$，初始额外量约 100，几十步后仍显著大于 1，正常梯度被大分母压缩。这是可计算的恢复时间，不应只描述为“训练不稳定”。

### TRN10-D03
Centered 版本使用 $\sqrt{v_t-m_t^2}$，uncentered 使用 $\sqrt{v_t}$。若梯度恒为 2，则稳态 $v=4,m=2$：uncentered RMS 为 2，centered 方差为 0（实际由 $\epsilon$ 主导）。两者的方向尺度完全不同。

## E. AI 迁移

### TRN10-E01
记录 raw gradient RMS/quantiles、$v_t$ RMS/quantiles、归一化方向 RMS、参数 delta RMS、尖峰发生时间、每层/参数组的恢复曲线与 clipping/overflow。若 raw gradient 已恢复而 $v_t$ 仍高、方向仍低，才支持“二阶矩记忆”解释。

### TRN10-E02
选多个 $\rho$，固定初始化、数据次序、LR 搜索预算与 curriculum 切换点；同时报告切换后的瞬态恢复时间、全程积分损失、最终验证指标和多 seed 区间。预注册相同 checkpoint 选择规则，避免只挑短记忆方法切换后最亮眼的一段。

### TRN10-E03
至少确认：平方平均递推的 decay 命名、$\epsilon$ 放在平方根内还是外、是否 centered、是否有 momentum、weight decay 是 coupled 还是 decoupled、maximize、初始化、更新顺序、稀疏梯度支持、foreach/fused 路径和 dtype。名字相同不保证 state transition 相同。

## 无提示重做

- [ ] 48 小时后从 step response 推回 EMA 记忆尺度。
- [ ] 一周后为一次梯度尖峰计算恢复到 10% 的步数。
