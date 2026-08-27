---
type: exercise
status: draft
area: [learning-theory/vc, combinatorics/capacity]
topic: "[[打散、增长与 VC 维]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[集合、元素与集合运算]]", "[[数学归纳、递归与组合计数]]"]
related: ["[[解答 - 打散、增长与 VC 维]]", "[[增长函数与经验二分模式]]"]
solution: "[[解答 - 打散、增长与 VC 维]]"
created: 2026-08-20
updated: 2026-08-20
---

# 习题 - 打散、增长与 VC 维

> [!abstract] 训练目标
> 能用正确量词判断一个固定点集是否被打散，分别构造 VC 下界与上界，并在 AI 模型报告中区分参数、函数类、训练拟合和组合容量。

## A. 识别与复述

### LT-VC-A01

给定 $C=\{x_1,\ldots,x_m\}$，分别定义 $h|_C$、$\mathcal H|_C$、$C$ 被打散和 $\operatorname{VCdim}(\mathcal H)$。写出 shattering 的完整量词。

### LT-VC-A02

判断并解释：“存在 $h\in\mathcal H$ 拟合 $C$ 上给定训练标签”等价于“$\mathcal H$ 打散 $C$”。

### LT-VC-A03

证明若 $\mathcal H_1\subseteq\mathcal H_2$，则 $\operatorname{VCdim}(\mathcal H_1)\le\operatorname{VCdim}(\mathcal H_2)$。该结论能否反推 class inclusion？

## B. 手算与构造

### LT-VC-B01

对 $h_t(x)=\mathbf1\{x\ge t\}$ 和点集 $C=\{-2,1,4\}$，列出全部可实现标签向量，并给每个向量一个可行 $t$。

### LT-VC-B02

对实轴区间类 $h_{a,b}=\mathbf1\{a\le x\le b\}$，在 $C=\{0,2,5\}$ 上列出全部可实现 labeling，指出唯一不可实现者，并解释原因。

### LT-VC-B03

一个有限 class 有 $|\mathcal H|=1000$。由 cardinality 最多能推出多大的 VC 维整数上界？若已知 VC 维为 3，能否反推出 $|\mathcal H|=8$？

## C. 推导与证明

### LT-VC-C01

证明 shattering 的 downward closure：若 $C$ 被打散，则每个 $B\subseteq C$ 都被打散。要求明确写出如何把 $B$ 上 labeling 补全到 $C$。

### LT-VC-C02

证明 $\mathbb R$ 上由开区间 $(a,b)$ 定义的 binary class 的 VC 维仍为 2。端点约定为什么不改变这个结论？

### LT-VC-C03

设 $\mathcal X=\mathbb R^d$，$\mathcal H$ 是 affine halfspaces。使用 $d+1$ 个 affinely independent points 证明 VC 下界 $d+1$；说明增广矩阵为何可逆。

## D. 边界、反例与纠错

### LT-VC-D01

纠正：“我找到了三个共线点，affine classifiers 不能打散它们，所以 $\mathbb R^2$ 中直线分类器的 VC 维小于 3。”

### LT-VC-D02

给出一个只有一个实参数但 VC 维无穷的函数类，并解释这为何不与线性模型中“维数约等于参数数”的结论冲突。

### LT-VC-D03

纠正：“VC 维越大，任何数据集上的 test error 就越大。”分别指出 VC 维的量词与 test error 还依赖的对象。

## E. AI 迁移

### LT-VC-E01

冻结 encoder $\phi(x)\in\mathbb R^{128}$，只训练一个带 bias 的 binary linear probe。写出 hypothesis class、典型 VC 上界/一般位置值，并列出两种使实际样本模式数显著更低的情形。

### LT-VC-E02

某报告写“网络有 $10^7$ 个参数，所以 VC 维等于 $10^7$”。给出一份最少包含五项的理论审计清单。

### LT-VC-E03

一个 prompt generator 在固定 50 个测试问题上找到一个 prompt 达到 100% 准确率。解释为什么这既不证明 50 点被 prompt class 打散，也不自动证明部署泛化；给出需要补充的两个不同证据。

## 分级提示

- `B01`：阈值只能产生 0 前缀、1 后缀；
- `B02`：区间选中的排序样本必须是连续 block；
- `B03`：求 $\lfloor\log_2 1000\rfloor$；
- `C03`：把 $x_i$ 增广为 $(x_i^\top,1)^\top$，令 score 等于 $\pm1$；
- `D02`：用一个实数二进制展开的第 $i$ 位定义 $h_\theta(i)$；
- `E03`：区分“一个 labeling 的拟合证据”和“全部 labelings / 未见数据的证据”。

## 解答入口

完成独立尝试后再打开：[[解答 - 打散、增长与 VC 维]]。
