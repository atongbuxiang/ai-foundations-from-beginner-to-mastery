---
type: solution
status: verified
area: [training, optimization, ema, swa, checkpoint-averaging]
topic: "[[参数 EMA、SWA 与 Checkpoint Averaging]]"
exercise: "[[习题 - 参数 EMA、SWA 与 Checkpoint Averaging]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 参数 EMA、SWA 与 Checkpoint Averaging

> [!warning] 使用边界
> 坐标平均只有在模型状态可对齐时才有功能意义；prediction ensemble、teacher feedback 与后验平均是不同对象。

## A. 识别与复述

### TRN39-A01
EMA 对单条轨迹的参数作指数加权；SWA 对尾段/周期采样 checkpoint 常近似等权；checkpoint soup 通常合并若干独立 fine-tuned 模型；prediction ensemble 平均 logits/probability 等输出；Mean Teacher 用 student 参数 EMA 形成 teacher 并产生后续 target。前四者是否反馈取决于协议，Mean Teacher 明确形成训练闭环。

### TRN39-A02
恒定 decay $\beta$ 的旧样本权重按 $\beta^k$ 衰减；粗略有效窗口是 $1/(1-\beta)$，half-life 是 $\ln(1/2)/\ln\beta$ 次 EMA 更新。同一 $\beta$ 若每 100 step 才更新一次，按 optimizer step 的窗口和半衰期放大 100 倍，所以必须同时记录时钟。

### TRN39-A03
BN 的 running mean/variance 是非梯度参数状态，通常不等于各 checkpoint 统计的坐标平均；用平均参数推理前常需在数据上重估。LayerNorm 在当前样本/特征上即时计算统计，没有同类 running state，但其可学习 scale/bias 仍是参数，需正常平均并检查对齐。

## B. 手算与构造

### TRN39-B01
$$
\bar\theta_1=0.2,
\quad
\bar\theta_2=0.9(0.2)+0.4=0.58,
$$
$$
\bar\theta_3=0.9(0.58)+1=1.522.
$$
展开为 $0.1\theta_3+0.09\theta_2+0.081\theta_1+0.729\bar\theta_0$；代入得到 $1+0.36+0.162=1.522$。

### TRN39-B02
有效窗口约为 $1/(1-0.99)=100$ 次 EMA 更新。half-life
$$
h=\frac{\ln0.5}{\ln0.99}\approx68.97
$$
次更新。每 50 optimizer step 更新一次时，对应约 5000-step 窗口与 3448-step half-life（离散取整规则需另声明）。

### TRN39-B03
参数平均为 $\bar\theta=2$，故 $f_{\bar\theta}(x)=4x$。预测平均为
$$
\tfrac12(1^2x+3^2x)=5x.
$$
差 $x$ 来自参数—函数映射的二次曲率。

## C. 推导与证明

### TRN39-C01
递推展开为
$$
\bar\theta_t=\beta^t\bar\theta_0
+(1-\beta)\sum_{k=1}^t\beta^{t-k}\theta_k.
$$
若初始化项只是人为从零开始带来的残余，可用
$$
\tilde\theta_t=
\frac{\bar\theta_t-\beta^t\bar\theta_0}{1-\beta^t}
$$
归一化历史权重。若 $\bar\theta_0=\theta_0$ 且它本就是有效样本，则是否去除残余属于算法选择而非必然修正。

### TRN39-C02
令 $\delta_k=\theta_k-\bar\theta$ 且 $\sum\alpha_k\delta_k=0$。Taylor 展开：
$$
f(\theta_k)\approx f(\bar\theta)+J\delta_k+\frac12\delta_k^TH_f\delta_k.
$$
加权后线性项消失，但二阶项留下
$$
\sum_k\alpha_k f(\theta_k)-f(\bar\theta)
\approx\frac12\sum_k\alpha_k\delta_k^TH_f\delta_k.
$$
轨迹跨度和参数曲率共同控制差异。

### TRN39-C03
若 $f_\theta(x)=A(x)\theta+b(x)$，则
$$
f_{\sum\alpha_k\theta_k}(x)=A\sum\alpha_k\theta_k+b
=\sum\alpha_k[A\theta_k+b]
$$
（用 $\sum\alpha_k=1$）。深网中层间乘法和激活使整体对所有参数不再仿射，因此通常不满足。

## D. 边界、反例与纠错

### TRN39-D01
两隐单元 ReLU 网络 A：hidden weights $(1,-1)$、output weights $(1,-1)$，给 $f_A(x)=\operatorname{ReLU}(x)-\operatorname{ReLU}(-x)=x$。网络 B 同时交换两个 hidden 与 output 坐标：weights $(-1,1)$、outputs $(-1,1)$，功能仍为 $x$。直接坐标平均后 hidden 和 output weights 全为 0，模型输出 0。功能相同不保证未对齐参数可平均。

### TRN39-D02
非平稳任务后段目标已改变，长窗口 EMA 混入旧任务参数，可能落后于 last；或者早期大量坏状态、burn-in 不足，使 EMA 长期受污染。另一常见错误是训练维护 EMA 却评估 raw 参数或反之。EMA 是带时间常数的低通滤波，不存在逐任务普适支配。

### TRN39-D03
贝叶斯后验平均要求参数样本来自定义的 posterior（或可解释近似）、权重对应 posterior mass，并在函数/预测层积分。优化轨迹的 EMA/SWA 点彼此相关、采样温度和体积权重未校准，还受对称性与 basin 影响。它们可有经验上的平滑/ensemble 关系，但不自动给正确不确定性。

## E. AI 迁移

### TRN39-E01
manifest 应含 `average object, source trajectory/run IDs, coefficient rule, update clock, burn-in, sampling interval, initialization, included parameter/buffer states, BN recalibration data, train gradient point, eval point, serialization dtype, resume state, candidate selection`。跨 run soup 还要记录对齐/匹配策略。

### TRN39-E02
所有候选共享训练 run 时要去重训练成本，同时列 checkpoint 存储/加载；prediction ensemble 计入多倍推理 FLOPs/延迟。best/EMA/SWA 使用相同验证访问次数与候选网格，最终 test 只用于锁定后评估。报告 last、方法原生点及 BN 重估前后，避免给某法额外选择优势。

### TRN39-E03
闭环是 `student θ_t → EMA teacher φ_t → teacher target → student loss/gradient → θ_{t+1}`。干预可固定同一 student 轨迹，离线仅对 checkpoint 做 EMA，测“平滑评估”；再运行在线 teacher 但让 target 来自固定/随机对照，比较轨迹中介。只有在线反馈组改变后续梯度并带来增益，才支持 teacher-target 机制。

## 无提示重做

- [ ] 48 小时后展开 EMA 权重与初始化残余。
- [ ] 一周后构造置换对称使参数平均失败的网络。
