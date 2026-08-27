---
type: solution
status: verified
area: [training, optimization, generalization]
topic: "[[Critical Batch、隐式偏置与 SGD 证据地图]]"
exercise: "[[习题 - Critical Batch、隐式偏置与 SGD 证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Critical Batch、隐式偏置与 SGD 证据地图

## A. 识别与复述

### TRN08-A01
Step efficiency 看 optimizer updates；sample/token efficiency 看数据量；compute efficiency 看 FLOPs/energy；wall-clock efficiency 看实际时间。大 batch 可减少 steps、增加每 step samples、改善 throughput，四项不必同向。

### TRN08-A02
它表示继续增加 batch 对减少 steps 的边际收益变小，同时 sample/compute 开销上升。训练阶段、target、optimizer、LR 与系统都能改变该尺度；超过它仍可能稳定并有 wall-time 收益。

### TRN08-A03
代表结论：linearly separable data、homogeneous linear predictor、logistic/exponential-tail loss、特定 GD/步长与初始化条件下，loss→0、weight norm→∞，normalized direction→hard-margin SVM direction。它是方向渐近结论，不是有限时间深网/任意 SGD/Adam 定理。

## B. 手算与构造

### TRN08-B01
$B=64$：$S/S_{min}=1+256/64=5$，$E/E_{min}=1+64/256=1.25$。$B=256$：二者都为 2。$B=1024$：分别 1.25 与 5。

### TRN08-B02
总 examples 为 $10^7$。$B=1000$ 有 $10^4$ steps；$B=10000$ 只有 $10^3$ steps。固定 epoch 同时把 optimizer updates 减少十倍，故观察差异不能只归因于 gradient noise。

### TRN08-B03
两层无 bias ReLU：$f(x)=W_2\operatorname{ReLU}(W_1x)$。对 $c>0$，令 $W_1'=cW_1,W_2'=W_2/c$；正齐次性给 $f'=f$。但参数坐标位移/二阶导在两个层方向按不同 $c$ 缩放，raw Hessian eigenvalues 或邻域 sharpness 可任意改变。

## C. 推导与证明

### TRN08-C01
$S=S_{min}(1+B_n/B)$，故 $E=BS=S_{min}(B+B_n)$。当 $B\to0$ 的连续模型极限，$E_{min}=S_{min}B_n$，所以 $E/E_{min}=1+B/B_n$。

### TRN08-C02

$$\left(\frac S{S_{min}}-1\right)\left(\frac E{E_{min}}-1\right)
=\frac{B_n}{B}\frac B{B_n}=1.$$

$B=B_n$ 时两个 excess 都为 1，故总归一化成本都为 2；这是模型中的对称折中点，不必是 wall-time optimum。

### TRN08-C03
H1：减小 $B$ 在固定参数/采样合同下增大 update covariance；最低证据是推导加 Monte Carlo。H2：更大 noise 在 compute-matched training 中选择某个 invariant flatness/margin 指标；需受控多 seed trajectory 实验或特定模型定理。H3：该指标对 test risk 有增量预测/因果作用；需跨干预、预注册控制混杂，最好有函数空间理论或外部验证。

## D. 边界、反例与纠错

### TRN08-D01
上题的 $c$-rescaling 保持网络函数、预测和 generalization 完全相同，却改变 parameter-space curvature。故不 invariant 的 sharpness 不能单独充当函数泛化原因；需要 normalization、quotient/function-space 或其他 invariant 定义。

### TRN08-D02
固定 epoch 时 steps 改变；BN statistics batch 改变 forward；LR/warmup/decay schedule 可能未重调；大 batch 进入不同硬件/precision；不同调参次数带来 selection bias。未隔离这些变量，观测只是 batch intervention 的总效应。

### TRN08-D03
$B_{critical}$ 依赖 $G(\theta),C(\theta)$、target loss、数据相关性、optimizer/preconditioner、parameterization 和硬件。训练早晚 $\|G\|$ 变化就可使 noise scale 大变，更不用说换任务。

## E. AI 迁移

### TRN08-E01
A：small optimizer batch、small BN、固定高 steps；B：large batch、large BN、同 epochs；C：large batch、large BN、steps 匹配 A；D：large batch、ghost-small BN、steps 匹配 A。各组使用相同数据/seed pairing和预注册调参预算，报告多种成本。

### TRN08-E02
至少含 model/data/version、optimizer contract、local/global/effective batch、LR/schedule、optimizer steps、examples/tokens、estimated FLOPs/energy、step time/throughput/communication、peak memory、train loss、validation/test metric、seeds、mean/CI、tuning budget 和失败 run。

### TRN08-E03
可改为：“在预注册模型与训练协议中，测试假设：当测得 $\eta\lambda_{max}$ 长期接近静态阈值时，某些 validation 指标与 compute-matched controls 存在可重复关联；通过 LR 干预、曲率估计、更新尺度和多 seed 比较评估，但不预设该关联为因果或可跨任务外推。”

## 无提示重做

- [ ] 重建 critical-batch 双曲线并解释四种效率。
- [ ] 把任意一条泛化口号拆成可证伪箭头。
