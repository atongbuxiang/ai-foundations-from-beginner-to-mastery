---
type: experiment
status: draft
area: [labs, math/linear-algebra, math/numerical-linear-algebra]
prerequisites: ["[[标准正交基与 Gram-Schmidt]]", "[[QR 分解]]", "[[条件数]]"]
related: ["[[矩阵扰动]]", "[[数值线性代数 MOC]]", "[[推导与实验 MOC]]"]
code: "[[plot_gram_schmidt_stability.py]]"
figure: "[[00-知识库管理/_assets/plots/qr/plot-gram-schmidt-orthogonality-v2.svg]]"
figure_sha256: "12f5e0cb87bcf6a9ca520e69e0daf05ff968852c30ecd4f1634f3db7d23e01c6"
sources: ["MIT-18.335-Week-4"]
created: 2026-08-15
updated: 2026-08-23
---

# 实验 - Gram-Schmidt 与 QR 的正交性误差

> [!abstract] 实验结论
> 在精确算术中，经典 Gram–Schmidt（CGS）与修正 Gram–Schmidt（MGS）得到同一个正交化过程；在浮点算术中，当列向量越来越接近线性相关时，CGS 会更早丢失正交性。本实验在 $\kappa_2\approx1.2\times10^8$ 时测得 CGS 正交性缺陷约 $3.02\times10^{-1}$，MGS 约 $2.20\times10^{-9}$。

> [!question] 本实验的判别问题
> 为什么 $A\approx QR$ 的重构残差仍接近舍入地板时，CGS 生成的 $Q$ 已经可能严重不正交？

## 研究问题

需要区分三个容易混在一起的问题：

1. 输入矩阵在数学上是否满列秩？
2. 计算结果是否仍满足 $\boldsymbol A\approx\boldsymbol Q\boldsymbol R$？
3. 计算出来的 $\boldsymbol Q$ 是否仍满足 $\boldsymbol Q^{\top}\boldsymbol Q\approx\boldsymbol I$？

第三个问题并不会自动由第二个问题保证。本实验只改变输入的近相关程度，比较 CGS 与 MGS 的正交性误差。

## 预注册判断

> [!hypothesis] 假设
> 对同一个满秩矩阵族，条件数增大时两种算法都会更敏感；CGS 因为用原始列一次性计算全部投影系数，旧方向上的舍入误差更容易残留。MGS 每次从已经更新的残差中消去下一个方向，因此会把正交性保持到更大的条件数。

## 可精确分析的矩阵族

令 $\boldsymbol1\in\mathbb R^n$ 是全 1 向量，取

$$
\boldsymbol A_{\varepsilon}
=\boldsymbol1\boldsymbol1^{\top}
+\varepsilon\boldsymbol I,
\qquad n=12,
\qquad \varepsilon>0.
$$

每列都近似为 $\boldsymbol1$，只在自己的坐标上多出 $\varepsilon$。所以 $\varepsilon$ 越小，列越接近相同。

这个矩阵是对称正定的。沿 $\boldsymbol1$ 方向，特征值为 $n+\varepsilon$；在与 $\boldsymbol1$ 正交的 $n-1$ 维子空间上，特征值都是 $\varepsilon$。因此

$$
\kappa_2(\boldsymbol A_{\varepsilon})
=\frac{n+\varepsilon}{\varepsilon}.
$$

只要 $\varepsilon>0$，它在数学上始终满秩；实验观察到的正交性损失不是精确秩亏。

## 两种算法究竟差在哪里

在第 $j$ 步，CGS 先基于原列 $\boldsymbol a_j$ 计算全部系数：

$$
r_{ij}=\boldsymbol q_i^{\top}\boldsymbol a_j,
\qquad
\boldsymbol v_j
=\boldsymbol a_j-\sum_{i<j}r_{ij}\boldsymbol q_i.
$$

MGS 则维护不断更新的残差：

$$
\begin{aligned}
\boldsymbol v_j^{(0)}&=\boldsymbol a_j,\\
r_{ij}&=\boldsymbol q_i^{\top}\boldsymbol v_j^{(i-1)},\\
\boldsymbol v_j^{(i)}&=\boldsymbol v_j^{(i-1)}-r_{ij}\boldsymbol q_i.
\end{aligned}
$$

在精确算术中可以展开成同一个式子；在浮点算术中，每次内积和减法都会舍入，运算顺序因此具有实际后果。

## 变量与指标

| 类型 | 变量 | 范围 | 含义 |
|---|---|---|---|
| 自变量 | $\varepsilon$ | $10^{-1}$ 到 $10^{-8}$ | 列间差异尺度 |
| 派生量 | $\kappa_2(\boldsymbol A_\varepsilon)$ | 精确公式 | 输入问题的病态程度 |
| 主指标 | $\|\boldsymbol Q^{\top}\boldsymbol Q-\boldsymbol I\|_F$ | 越小越好 | 标准正交性缺陷 |
| 对照指标 | $\|\boldsymbol A-\boldsymbol Q\boldsymbol R\|_F/\|\boldsymbol A\|_F$ | 越小越好 | 重构残差 |

## 环境与复现

| 项目 | 值 |
|---|---|
| Python | 标准库实现；不调用 NumPy 或外部 QR |
| 浮点数 | CPython 双精度 float |
| 随机性 | 无 |
| 矩阵阶数 | $n=12$ |
| 图格式 | 自包含 SVG |

复现命令：

~~~bash
python3 "00-知识库管理/_labs/code/plot_gram_schmidt_stability.py"
~~~

代码：[plot_gram_schmidt_stability.py](../code/plot_gram_schmidt_stability.py)

## 结果

先用图回答：**随着列相关性增强，CGS 与 MGS 的正交性缺陷何时分叉，逐元素 Gram 误差又把失真定位到哪里？**

![[00-知识库管理/_assets/plots/qr/plot-gram-schmidt-orthogonality-v2.svg|880]]

> [!figure] 实验图｜同一 QR 恒等式下的正交性分叉
> 左图在 $A_\varepsilon=\boldsymbol1\boldsymbol1^T+\varepsilon I$ 上比较 $\|Q^TQ-I\|_F$；右图固定 $\varepsilon=10^{-7}$，逐元素展示 CGS 与 MGS 的 Gram 误差。生成脚本：[[plot_gram_schmidt_stability.py]]；标准库确定性实现，并对 $\kappa_2\approx1.2\times10^8$ 时的正交性分离和重构残差设断言。

**怎样读图。** 先沿左图横轴观察红、蓝曲线何时跨越多个数量级，再到右图查看深色非对角块：CGS 的列间内积已显著偏离 0，而 MGS 仍接近单位阵。重构残差必须另查，不能从这张正交性图自动推出。

**适用边界（图没有证明什么）。** 该矩阵族高度结构化，教学实现也不是生产 BLAS；图不证明 MGS 对任意病态输入足够稳定，更不替代 Householder QR、重正交化或列主元策略。

关键输出：

| $\varepsilon$ | 精确 $\kappa_2$ | CGS 正交缺陷 | MGS 正交缺陷 | CGS 相对重构残差 | MGS 相对重构残差 |
|---:|---:|---:|---:|---:|---:|
| $10^{-1}$ | $1.21\times10^2$ | $4.40\times10^{-13}$ | $1.26\times10^{-14}$ | $0$（浮点计算值） | $9.84\times10^{-17}$ |
| $10^{-3}$ | $1.20\times10^4$ | $5.97\times10^{-9}$ | $1.18\times10^{-12}$ | $0$（浮点计算值） | $9.02\times10^{-17}$ |
| $10^{-5}$ | $1.20\times10^6$ | $2.55\times10^{-5}$ | $6.00\times10^{-11}$ | $3.07\times10^{-17}$ | $1.36\times10^{-16}$ |
| $10^{-7}$ | $1.20\times10^8$ | $3.02\times10^{-1}$ | $2.20\times10^{-9}$ | $0$（浮点计算值） | $1.17\times10^{-16}$ |
| $10^{-8}$ | $1.20\times10^9$ | $9.47$ | $1.48\times10^{-8}$ | $0$（浮点计算值） | $1.18\times10^{-16}$ |

## 分析

### 小重构残差不等于正交性良好

在这份直接实现里，两种方法都能把输入重构到舍入误差量级；CGS 的若干重构残差甚至因这个特殊矩阵和运算顺序恰好计算为浮点零。但当 $\varepsilon=10^{-7}$ 时，CGS 的列已经明显不正交。

所以检查 QR 实现不能只检查

$$
\boldsymbol A\approx\boldsymbol Q\boldsymbol R,
$$

还必须独立检查

$$
\boldsymbol Q^{\top}\boldsymbol Q\approx\boldsymbol I.
$$

### MGS 改善稳定性，但不是万能消除条件性

MGS 把误差推迟了许多个数量级，但它的误差也随条件数上升。对严重病态问题，实际数值库通常优先采用 Householder QR；若必须保持极高正交性，还可能使用重正交化。算法更稳定不能让输入本身携带不存在的信息。

### 对 AI 工作的意义

当数据矩阵、激活特征或低秩适配器的列高度相关时：

- 训练损失或重构误差小，不保证学到的方向彼此可解释；
- 正交约束、子空间相似度和投影算子依赖 $\boldsymbol Q$ 的实际正交性；
- 需要同时报告数值秩、条件数估计、重构残差与正交性缺陷；
- 生产实现应使用成熟库的 Householder QR 或带列主元 QR，而不是照搬教学版循环。

## 一致性检查

- [x] 每个 $\varepsilon>0$ 时矩阵精确满秩。
- [x] 条件数使用解析特征值计算，不依赖待比较算法。
- [x] CGS 与 MGS 使用相同输入、精度和误差指标。
- [x] 表格由脚本打印，图由同一组函数生成。
- [x] 同时检查重构残差与正交性缺陷。

## 结论边界

> [!warning] 不可外推之处
> 这是一个结构化的稠密方阵族，用于隔离舍入误差机制。它不等价于测量某个 BLAS/LAPACK 库、GPU 内核、混合精度训练或稀疏 QR 的实际性能。

- Python 循环不是高性能实现；实验比较的是运算顺序，不是运行速度。
- 热图只显示一个 $n=12$ 截面。
- MGS 优于 CGS 不代表它在所有需求上优于 Householder QR 或 SVD。
- 条件数很大时，列空间本身也会对数据扰动敏感；算法误差与问题条件性必须分开报告。

## 下一步

- [ ] 加入二次重正交化，比较一次 MGS 与 MGS2。
- [ ] 使用成熟数值库比较 Householder QR 与带列主元 QR。
- [ ] 把输入改为低精度模拟，观察误差转折点如何提前。

## 来源

- [[标准正交基与 Gram-Schmidt]]。
- [[QR 分解]]。
- [MIT 18.335 Week 4：Classical/Modified Gram–Schmidt、Householder QR 与 loss of orthogonality](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/pages/week-4/)。
