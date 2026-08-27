---
type: exercise
status: draft
area: [architecture, group-equivariance]
topic: "[[群卷积、等变网络与 CNN 证据地图]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 群卷积、等变网络与 CNN 证据地图]]"
created: 2026-08-24
updated: 2026-08-24
---

# 习题 - 群卷积、等变网络与 CNN 证据地图

## A. 识别与复述
### ARCH-GCNN-A01
定义 group action、orbit、equivariance 和 invariance。
### ARCH-GCNN-A02
为什么 group feature map 常多一个 orientation/group axis？
### ARCH-GCNN-A03
按 I/T/E/H/O 给“G-CNN 更好”拆成五层。

## B. 手算与建模
### ARCH-GCNN-B01
写出 $C_4=\{0°,90°,180°,270°\}$ 对 2×2 图像的轨道。
### ARCH-GCNN-B02
若 group feature 为 $[1,2,3,4]$，90° action 循环移位，求变换后的 feature 与 group-sum readout。
### ARCH-GCNN-B03
普通 CNN 有 32 channels；改成 8 base channels ×4 orientations。比较参数不能只看 output channels 的原因是什么？

## C. 推导与证明
### ARCH-GCNN-C01
完成正文 group correlation 的换元证明。
### ARCH-GCNN-C02
证明有限群上的 sum pooling 对 left action 不变。
### ARCH-GCNN-C03
证明等变层加逐 group-position shared nonlinearity仍等变。

## D. 边界、反例与纠错
### ARCH-GCNN-D01
给出标签不具旋转不变性的任务。
### ARCH-GCNN-D02
为什么任意角 image rotation 的插值会破坏格点精确等变？
### ARCH-GCNN-D03
反驳：“G-CNN 参数不增加，所以训练成本也不增加。”

## E. AI 迁移
### ARCH-GCNN-E01
为一个旋转等变模型设计 structure residual + task benchmark 双验收。
### ARCH-GCNN-E02
比较 graph node permutation equivariance 与 image rotation equivariance 的共同模板。
### ARCH-GCNN-E03
决定一个遥感任务是否采用 $C_4$、$D_4$ 或无 group tying，写决策清单。

## 解答入口
[[解答 - 群卷积、等变网络与 CNN 证据地图]]
