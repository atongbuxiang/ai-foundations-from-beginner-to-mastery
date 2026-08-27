---
type: solution
status: draft
area: [architecture, moe, routing]
topic: "[[Router、Gate、Top-k 与稀疏组合]]"
exercise: "[[习题 - Router、Gate、Top-k 与稀疏组合]]"
sources: ["[[S-2017-Shazeer-Sparsely-Gated-MoE]]", "[[S-2026-Su-11782-MoE门控归一化]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Router、Gate、Top-k 与稀疏组合

## A. 识别与复述

### ARCH-ROUTER-A01
至少包括 logits、score activation/temperature、Top-k axis 与 $k$、selected-weight normalization、capacity/overflow、tie-break、noise 的 train/eval 语义、combine 规则和 backward estimator。少一项都可能留下不同实现。

### ARCH-ROUTER-A02
Activation 把 logits 变成 scores；selection 把连续向量变成离散 index 集；selected normalization 决定选中专家的组合系数。三者可独立替换。

### ARCH-ROUTER-A03
严格递增变换在无 tie 时保持次序和 Top-k index；它不保持数值、和、Jacobian、Re-Norm 前权重、辅助统计或训练动力学。

## B. 手算与建模

### ARCH-ROUTER-B01
$e^2,e^1,e^{-1}$ 之和约 $10.475$，三分类 softmax 约为 $[0.7054,0.2595,0.0351]$。Top-2 为前两项；Re-Norm 后为 $[0.7311,0.2689]$。

### ARCH-ROUTER-B02
Re-Norm 输出为 $0.7311\cdot4-0.2689\approx2.6555$。不 Re-Norm 为 $0.7054\cdot4-0.2595\approx2.5621$；index 相同但函数不同。

### ARCH-ROUTER-B03
可用稳定 index 优先选 $\{0,1\}$，也可用带 seed 的随机 tie-break 选任意两项。前者跨运行确定，后者只在 seed、RNG 和并行顺序固定时可复现；不稳定 GPU sort 还可能随 kernel 改变。

## C. 推导与证明

### ARCH-ROUTER-C01
若 $a_i=e^{z_i}/Z$，则对 $i\in I$，
$$\frac{a_i}{\sum_{j\in I}a_j}=\frac{e^{z_i}/Z}{\sum_{j\in I}e^{z_j}/Z}=\frac{e^{z_i}}{\sum_{j\in I}e^{z_j}}.$$
全局分母消去；selection 仍由全部 logits 排名决定。

### ARCH-ROUTER-C02
$I=\{i^*\}$ 时 $w_{i^*}=a_{i^*}/a_{i^*}=1$。在 $a_{i^*}>0$ 且 index 不变的邻域，商法则给 $(a-a)/a^2=0$；hard index 的普通导数也几乎处处为零。

### ARCH-ROUTER-C03
当第 $k$ 与第 $k+1$ 大分数有严格间隙时，足够小扰动不改排序，index 集合为常数。边界是至少两个候选在 cutoff 处相等/交叉的超曲面，那里选择跳变或不唯一。

## D. 边界、反例与纠错

### ARCH-ROUTER-D01
二者可有同一 Top-k index，但 softmax scores 耦合且和为 1，sigmoid 独立且总和可变；Re-Norm 前后权重、Jacobian、aux statistics 和饱和区均不同。因此只能说特定 selection 等价。

### ARCH-ROUTER-D02
可由 soft auxiliary loss、straight-through/连续松弛、noisy routing 的概率梯度、未 Re-Norm gate amplitude，或独立 bias feedback 更新。任一条都必须明确实现语义。

### ARCH-ROUTER-D03
训练噪声改变探索、负载和梯度方差；推理去噪改变 assignment 分布，可能令专家 batch、quality 与 capacity overflow 转移。需同时评估 train/eval 路由一致性和去噪后的负载。

## E. AI 迁移

### ARCH-ROUTER-E01
用已知 logits 检查 activation 数值、Top-k index/order、tie、Re-Norm 和 mixture；覆盖 $k=1,E$、相等/极端 logits、overflow、train/eval noise。再以有限差分分别核对 selected-weight path 与明确采用的 estimator。

### ARCH-ROUTER-E02
做四格 Softmax/Sigmoid × Re-Norm on/off，保持 logits layer、$k$、capacity、aux、seed 与训练预算一致。报告 loss、Router gradient/logit scale、entropy、load/drop、expert output norm 和吞吐；多 seed 分离随机差异。

### ARCH-ROUTER-E03
询问 score 函数与温度、Top-k 前后顺序、是否 Re-Norm、noise、tie-break、group/capacity/drop、combine、task/aux/STE 梯度、train/eval 差异、dtype/kernel，以及是否公开配置与测试。

