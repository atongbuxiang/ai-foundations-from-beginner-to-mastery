---
type: exercise
status: verified
area: [training, optimization, spectral-analysis]
topic: "[[Update-to-Weight Ratio、谱与尺度诊断]]"
solution: "[[解答 - Update-to-Weight Ratio、谱与尺度诊断]]"
created: 2026-08-26
updated: 2026-08-26
---

# 习题 - Update-to-Weight Ratio、谱与尺度诊断

## A. 识别与复述

### TRN67-A01
定义 global、layer、unit 与 spectral UWR，并说明分组/范数为何属于定义。

### TRN67-A02
比较 LARS、LAMB、AGC 与 realized-update telemetry 所归一的对象。

### TRN67-A03
区分参数谱、更新谱与 Hessian 曲率谱。

## B. 手算与构造

### TRN67-B01
$\|W\|_F=20$、$\|\Delta W\|_F=0.1$、$\|W\|_2=8$、$\|\Delta W\|_2=0.08$。计算 Frobenius 与 spectral UWR。

### TRN67-B02
一个 $100\times100$ rank-one 更新唯一奇异值为 1。计算 Frobenius norm、entry RMS、spectral norm 与 stable rank。

### TRN67-B03
二层 ReLU 网络作 $(W_1,W_2)\mapsto(10W_1,0.1W_2)$。函数是否改变？若 update 不同比例重缩放，普通 layer UWR 为什么可能改变？

## C. 推导与证明

### TRN67-C01
证明 $\|A\|_2\le\|A\|_F\le\sqrt{r}\|A\|_2$，并由此给出 stable rank 范围。

### TRN67-C02
推导 power iteration 作用于 $A^\top A$ 时各特征方向系数如何按 $\sigma_i^{2k}$ 缩放，说明谱隙作用。

### TRN67-C03
固定二次函数 $L=\frac12\theta^\top H\theta$，推导 GD 在 eigen-direction 上的稳定条件，并解释为何不能直接当深网全程定理。

## D. 边界、反例与纠错

### TRN67-D01
反驳：“global UWR 正常，所以每层都正常。”构造一个大层掩盖小层异常的例子。

### TRN67-D02
反驳：“有限步 power iteration 的结果就是 exact spectral norm。”

### TRN67-D03
反驳：“UWR 越小训练越稳定且越好。”给出过小 update 和坐标重参数化反例。

## E. AI 迁移

### TRN67-E01
为 Transformer 分组设计 UWR/spectrum telemetry，特别处理 embedding、bias、norm 和 tied weights。

### TRN67-E02
设计实验区分“RMS 正常但 rank-one 更新尖峰”与各向同性更新。

### TRN67-E03
某 run 的 $\rho_{spec}$、top Hessian eigenvalue 和 feature change 同时上升。写出能说和不能说的结论及下一步干预。
