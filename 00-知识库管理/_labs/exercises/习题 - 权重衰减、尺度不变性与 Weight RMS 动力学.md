---
type: exercise
status: verified
area: [training, optimization, adamw, weight-rms, scale-invariance]
topic: "[[权重衰减、尺度不变性与 Weight RMS 动力学]]"
solution: "[[解答 - 权重衰减、尺度不变性与 Weight RMS 动力学]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - 权重衰减、尺度不变性与 Weight RMS 动力学

> [!abstract] 训练目标
> 从 AdamW 一步更新重建历史记忆核和二阶能量递推；能说明 $\sqrt{\eta/\lambda}$ 只是在特定假设下的稳态近似，并把权重半径翻译成角更新。

## A. 识别与复述

### TRN38-A01
区分 coupled L2 regularization 与 decoupled weight decay。为什么在普通 SGD 中可能等价，在 Adam 中通常不等价？

### TRN38-A02
定义 $q_t=E\|\theta_t\|^2,r_t=E\|u_t\|^2,c_t=E\langle\theta_t,u_t\rangle$，解释三项在 Weight RMS 递推中的角色。

### TRN38-A03
什么是尺度不变参数？为什么 SGD raw-gradient 与 normalized-direction optimizer 的 angular LR 对 $\|w\|$ 有不同幂次？

## B. 手算与构造

### TRN38-B01
一维 AdamW 形式 $\theta_{t+1}=0.9\theta_t-0.1u_t$，$\theta_0=2$，$u_0=1,u_1=-1,u_2=2$。逐步计算 $\theta_1,\theta_2,\theta_3$，再用历史核复核。

### TRN38-B02
假设 $c=0,r=4$、常数 $\eta=0.01,\lambda=0.1$。用精确平稳递推求 $q_\star$，并与小 $\eta\lambda$ 近似 $q_\star\approx\eta r/(2\lambda)$ 比较。

### TRN38-B03
两阶段 schedule：前三步 $(\eta,\lambda)=(0.1,0.2)$，后二步 $(0.01,0.2)$，只考虑 decay。求总 shrinkage product，并与五步都用末段配置比较。

## C. 推导与证明

### TRN38-C01
展开时变递推 $\theta_{t+1}=a_t\theta_t-\eta_tu_t$，写出 $\theta_t$ 对 $\theta_0$ 与所有历史 $u_k$ 的精确核。

### TRN38-C02
推导 $q_{t+1}=a_t^2q_t+\eta_t^2r_t-2a_t\eta_tc_t$。在常数、$c=0$ 条件下求精确平衡，并导出 $\sqrt{\eta/\lambda}$ 阶的 RMS。

### TRN38-C03
设函数满足 $f(cw)=f(w)$。证明 $w^T\nabla f(w)=0$，再推导 SGD 与单位方向更新的小步 angular LR 标度。

## D. 边界、反例与纠错

### TRN38-D01
列出使 $\operatorname{RMS}(w)\propto\sqrt{\eta/\lambda}$ 失效的至少四个条件，并为其中一个构造数值反例。

### TRN38-D02
反驳“当前 $\eta/\lambda$ 相同就有相同 Weight RMS”。用不同历史 schedule 或非零 $c_t$ 给出反例。

### TRN38-D03
反驳“两个模型 Weight RMS 相同，所以函数更新相同”。利用尺度对称、Jacobian 或 optimizer direction 给出解释。

## E. AI 迁移

### TRN38-E01
为 Transformer 的 matrix、embedding、norm/bias 参数设计 decay 与 RMS 遥测分组；说明哪些组默认不应混合汇总。

### TRN38-E02
设计 LR/WD 阶跃实验以测量 Weight RMS 滞后。给出预测曲线、中介统计和稳态近似的验收/拒绝条件。

### TRN38-E03
审计“按 LR 动态调整 WD 可保持权重尺度”这一主张：区分瞬时公式、记忆核、相关项与最终功能指标。

## 作答与复盘

先独立推导历史核与 $q_t$ 递推，再查看 [[解答 - 权重衰减、尺度不变性与 Weight RMS 动力学]]。
