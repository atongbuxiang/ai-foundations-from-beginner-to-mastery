---
type: exercise
status: verified
area: [training, optimization, ema, swa, checkpoint-averaging]
topic: "[[参数 EMA、SWA 与 Checkpoint Averaging]]"
solution: "[[解答 - 参数 EMA、SWA 与 Checkpoint Averaging]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 参数 EMA、SWA 与 Checkpoint Averaging

> [!abstract] 训练目标
> 分清参数、预测、teacher、checkpoint 与分布平均；能推导 EMA 权重并识别对称性、BN state、窗口时钟和选择预算的边界。

## A. 识别与复述

### TRN39-A01
区分参数 EMA、SWA、checkpoint soup、prediction ensemble 与 Mean Teacher。每种方法平均的对象是什么？是否反馈进训练？

### TRN39-A02
解释 EMA 的 decay、有效窗口与 half-life。为什么同一 $\beta$ 在每 step 更新和每 100 step 更新时物理含义不同？

### TRN39-A03
为什么参数平均后要特别处理 BatchNorm running statistics？LayerNorm 参数是否也有同样的“重估统计”问题？

## B. 手算与构造

### TRN39-B01
$\bar\theta_t=0.9\bar\theta_{t-1}+0.1\theta_t$，$\bar\theta_0=0$，$\theta_1=2,\theta_2=4,\theta_3=10$。计算三步结果及各 checkpoint 权重。

### TRN39-B02
求 $\beta=0.99$ 的近似有效窗口 $1/(1-\beta)$ 与 half-life $\ln(1/2)/\ln\beta$。若每 50 optimizer step 才更新一次，换算为 step。

### TRN39-B03
取模型 $f_\theta(x)=\theta^2x$，$\theta_1=1,\theta_2=3$，等权平均。比较 parameter-average prediction 与 prediction average。

## C. 推导与证明

### TRN39-C01
展开 EMA 递推为历史参数的加权和，包含初始化残余；给出 bias-normalized EMA 的公式。

### TRN39-C02
对 $f_\theta(x)$ 在 $\bar\theta$ 附近作二阶 Taylor，说明为何一阶项在加权平均下抵消，而二阶曲率造成参数平均与预测平均的差。

### TRN39-C03
证明若模型对参数是仿射函数，则 parameter average 与 prediction average 相等；说明神经网络通常在哪一步破坏该条件。

## D. 边界、反例与纠错

### TRN39-D01
构造两个功能相同但隐藏单元置换不同的网络，使直接参数平均功能变差。

### TRN39-D02
反驳“EMA 总比 last checkpoint 好”。从非平稳任务、过长窗口、早期坏状态与评估点错用中选两个反例。

### TRN39-D03
为什么 SWA/EMA 不能自动解释为贝叶斯后验平均？区分采样分布、权重、函数空间与不确定性校准。

## E. AI 迁移

### TRN39-E01
写 averaging manifest：对象、更新时钟、系数、burn-in、state inclusion、BN recalibration、train/eval point、保存格式与选择规则。

### TRN39-E02
设计 last、best、EMA、SWA、prediction ensemble 的公平比较；明确训练、存储、推理、选择和评估预算。

### TRN39-E03
为 teacher–student 训练画出闭环因果链，设计一个区分“平滑评估收益”和“teacher target 改变优化轨迹”的干预。

## 作答与复盘

先写清平均对象和反馈方向，再查看 [[解答 - 参数 EMA、SWA 与 Checkpoint Averaging]]。
