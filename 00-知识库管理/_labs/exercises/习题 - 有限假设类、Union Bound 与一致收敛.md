---
type: exercise
status: draft
area: [learning-theory/pac, probability/union-bound]
topic: "[[有限假设类、Union Bound 与一致收敛]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[泛化间隙与浓缩不等式接口]]", "[[浓缩不等式]]"]
related: ["[[解答 - 有限假设类、Union Bound 与一致收敛]]", "[[不可知 PAC、ERM 与双侧一致收敛]]"]
solution: "[[解答 - 有限假设类、Union Bound 与一致收敛]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - 有限假设类、Union Bound 与一致收敛

> [!abstract] 训练目标
> 能把 fixed-h 坏事件升级成 all-h 共同事件，用它合法控制 data-dependent ERM，并理解 $\log M$ 到底在数哪一种选择自由度。

## A. 识别与复述

### LT-FIN-A01

定义 finite-class uniform convergence event，并写出其 Hoeffding–Union Bound 失败概率。

### LT-FIN-A02

为什么 Union Bound 不需要 $B_{h_1},\ldots,B_{h_M}$ 独立？用 indicator inequality 证明。

### LT-FIN-A03

区分 pointwise convergence 与 uniform convergence。为什么学习输出的数据依赖性需要后者或其他算法级工具？

## B. 手算与构造

### LT-FIN-B01

设 $M=5000,m=8000,\delta=0.05$，计算有限类双侧统一置信半径。

### LT-FIN-B02

要使 uniform deviation 至多 $0.04$、失败概率至多 $0.01$，当 $M=10^4$ 时 Hoeffding–Union Bound 需要多少样本？向上取整。

### LT-FIN-B03

一个模型库有 12 个文件，但其中 4 组各含两个完全相同的预测函数，其余 4 个函数彼此不同。计算按 distinct functions 得到的 $M$，并比较误用 $M=12$ 对半径的影响方向。

## C. 推导与证明

### LT-FIN-C01

从 $B_h=\{|R_S(h)-R_P(h)|>\varepsilon\}$ 出发，完整推导

$$
\Pr\left(\sup_h|R_S(h)-R_P(h)|>\varepsilon\right)
\le2Me^{-2m\varepsilon^2}.
$$

### LT-FIN-C02

在事件 $\sup_h|R_S(h)-R_P(h)|\le\alpha$ 上，证明 $\rho$-approximate ERM 满足 class excess 不超过 $2\alpha+\rho$。若目标 excess 为 $\varepsilon$，给出 exact ERM 的样本量充分条件。

### LT-FIN-C03

设每个 $h_j$ 分配失败预算 $\delta_j>0$ 且 $\sum_j\delta_j\le\delta$。证明同时有

$$
|R_S(h_j)-R_P(h_j)|
\le\sqrt{\frac{\log(2/\delta_j)}{2m}}
$$

的概率至少为 $1-\delta$；说明这如何预告非均匀 Occam bound。

## D. 边界、反例与纠错

### LT-FIN-D01

纠正：“最终只发布一个模型，所以 multiple-comparison 中 $M=1$。”区分预先指定与用同一 validation set 从 $M$ 个候选中选择。

### LT-FIN-D02

构造一个 data-dependent 候选集 $\mathcal H_S$，使 $|\mathcal H_S|=1$，但唯一函数严重过拟合；说明为什么不能代入 $M=1$ 的 fixed-class bound。

### LT-FIN-D03

纠正：“有 $p$ 个实数参数的神经网络是大小为 $p$ 的有限类。”讨论 cardinality、函数等价与量化后的 approximation trade-off。

## E. AI 迁移

### LT-FIN-E01

设计 100 个 checkpoint 的 validation selection protocol：候选如何冻结、误差条如何同时校正、最终模型如何用一次独立 test 评估。

### LT-FIN-E02

某团队测试 20 个模型、15 个任务、4 个指标后挑最亮眼数字。给出一个保守的 family size，并讨论相关性为何不使 Union Bound 失效、但可能使它很松。

### LT-FIN-E03

一个 prompt optimizer 根据 validation 反馈连续生成新 prompt，直到分数不再提升。分析为什么预先固定的 $M$ 不存在，并提出三种可恢复有效保证的设计。

## 分级提示

- `B03`：4 对重复函数贡献 4 个 distinct functions，再加 4 个单独函数；
- `C02`：一次 deviation 用在输出，一次用在 comparator；
- `C03`：对第 $j$ 个假设应用失败概率 $\delta_j$ 的 fixed-h bound；
- `D02`：令唯一候选就是由 $S$ 构造的记忆器；
- `E02`：最粗计数是三者乘积。

## 解答入口

完成独立尝试后再打开：[[解答 - 有限假设类、Union Bound 与一致收敛]]。
