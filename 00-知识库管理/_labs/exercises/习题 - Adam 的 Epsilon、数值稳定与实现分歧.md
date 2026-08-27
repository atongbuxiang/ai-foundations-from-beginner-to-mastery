---
type: exercise
status: verified
area: [training, optimization, numerical-computing]
topic: "[[Adam 的 Epsilon、数值稳定与实现分歧]]"
solution: "[[解答 - Adam 的 Epsilon、数值稳定与实现分歧]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Adam 的 Epsilon、数值稳定与实现分歧

> [!abstract] 训练目标
> 把 $\epsilon$ 视为有单位的算法参数，能量化 root-out/root-in 分歧、尺度断点和有限精度风险。

## A. 识别与复述

### TRN12-A01
写出 root-out $m/(\sqrt v+\epsilon)$ 与 root-in $m/\sqrt{v+\epsilon}$，说明两种 $\epsilon$ 的单位为何不同。

### TRN12-A02
在 root-out 形式中，给出 $\sqrt v\gg\epsilon$ 与 $\sqrt v\ll\epsilon$ 两个极限区间的近似更新。

### TRN12-A03
区分代数公式等价、实数运算等价与有限精度实现等价。

## B. 手算与构造

### TRN12-B01
$m=10^{-6},v=10^{-16},\epsilon=10^{-8}$。分别计算 root-out 与 root-in 的方向，量化比值。

### TRN12-B02
root-out 中把全部梯度和历史状态按正数 $c$ 一致缩放。推导新旧方向之差由哪个无量纲比控制。

### TRN12-B03
若希望 root-in 与 root-out 在零 $v$ 附近有相同分母尺度 $10^{-8}$，root-in 的 $\epsilon$ 应取多少？

## C. 推导与证明

### TRN12-C01
证明 root-out 方向可写成 $(m/\sqrt v)/(1+\epsilon/\sqrt v)$，并解释 $\epsilon/\sqrt v$ 是 regime parameter。

### TRN12-C02
对 soft-sign 模型 $u(g)=g/\sqrt{g^2+\epsilon^2}$，推导小梯度与大梯度渐近式。

### TRN12-C03
证明当 $\epsilon=0$、$c>0$ 且状态同步缩放 $m'=cm,v'=c^2v$ 时方向不变；加入固定 $\epsilon$ 后给出精确比值。

## D. 边界、反例与纠错

### TRN12-D01
反驳：“$\epsilon$ 只是避免除零，所以只要非零，取值不影响训练。”

### TRN12-D02
构造两个打印配置都显示 `eps=1e-8`、但实际更新不同的实现合同。

### TRN12-D03
为什么把 `sqrt(v)+eps` 代数重排为 `sqrt(v+eps)` 不是合法的性能优化？

## E. AI 迁移

### TRN12-E01
低精度训练中如何诊断某层进入 epsilon-dominated regime？

### TRN12-E02
设计一次跨框架 Adam 对齐测试，要求能定位 epsilon、bias correction 和 step order 的第一处分叉。

### TRN12-E03
若 loss 整体乘 $c$ 后最佳 LR 改变，为什么不能立刻断言 Adam 没有尺度不变性？列出需要审计的断点。

## 作答与复盘

所有数值题注明公式版本、dtype 与 $\epsilon$ 所在位置。独立完成后打开 [[解答 - Adam 的 Epsilon、数值稳定与实现分歧]]。
