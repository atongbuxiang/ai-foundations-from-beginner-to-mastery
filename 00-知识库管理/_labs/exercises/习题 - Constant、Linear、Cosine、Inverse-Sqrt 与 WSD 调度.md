---
type: exercise
status: verified
area: [training, optimization, learning-rate, schedule]
topic: "[[Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]"
solution: "[[解答 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度

> [!abstract] 训练目标
> 能从端点、面积、平方面积、时域和状态耦合比较 schedule；会区分“曲线名字相同”与“离散实现相同”。

## A. 识别与复述

### TRN35-A01
给出 constant、linear decay、cosine decay 与 inverse-square-root schedule 的连续形式，并声明各自需要哪些参数。

### TRN35-A02
为什么总面积 $\sum_t\eta_t$ 与平方面积 $\sum_t\eta_t^2$ 都值得报告？它们分别近似控制什么？

### TRN35-A03
解释 WSD 的 stable trunk、decay branch 与 horizon contract。它消除了什么依赖，又把什么依赖移到了 cooldown？

## B. 手算与构造

### TRN35-B01
峰值 $\eta_0=1$、连续区间 $s\in[0,1]$。计算 constant、linear-to-zero 与 cosine-to-zero 的面积及平方面积。

### TRN35-B02
离散 linear decay 有 $N=5$ 个 update，要求第一个值为 1、最后一个值为 0。写出序列。若误用分母 $N$，终点是多少？

### TRN35-B03
AdamW 只看 decay：$\theta_{t+1}=(1-\eta_t\lambda)\theta_t$。令 $\lambda=0.1$，比较五步 constant $\eta=0.2$ 与序列 $(0.4,0.3,0.2,0.1,0)$ 的精确 shrinkage product。

## C. 推导与证明

### TRN35-C01
推导 cosine-to-zero 在 $[0,1]$ 的面积和平方面积，并与 linear 比较。

### TRN35-C02
证明 inverse-square-root tail 的累计面积为 $\Theta(\sqrt T)$、平方面积为 $\Theta(\log T)$。可用积分夹逼。

### TRN35-C03
构造 warmup + stable + cooldown 的连续分段函数，给出连接点连续条件；再说明连续不保证离散 endpoint 无 off-by-one。

## D. 边界、反例与纠错

### TRN35-D01
反驳“peak LR 与 final LR 相同的两个 schedule 优化预算相同”。用面积或平方面积给出数值反例。

### TRN35-D02
为什么把训练从 $T$ 延长到 $2T$ 时重新计算 full-horizon cosine，会改写前 $T$ 步？给出任意 $0<t<T$ 的公式比较。

### TRN35-D03
反驳“WSD 对停止时刻完全不敏感”。指出 cooldown 长度、分支点、选择 checkpoint 与累计 weight decay 的依赖。

## E. AI 迁移

### TRN35-E01
写一个 schedule manifest：包括时钟、端点、warmup/stable/cooldown 长度、离散索引、失败 step 行为、per-group scale 与 resume 规则。

### TRN35-E02
设计 constant、cosine、inverse-sqrt、WSD 四组 compute-matched 实验。你会匹配 peak、面积还是搜索预算？说明主比较和敏感性分析。

### TRN35-E03
审计论文图中只给一条 LR 曲线的做法：列出复现还缺的最小信息，并给出一个自动化 endpoint/area assertion 清单。

## 作答与复盘

先手算端点、面积、平方面积与 shrinkage product，再查看 [[解答 - Constant、Linear、Cosine、Inverse-Sqrt 与 WSD 调度]]。
