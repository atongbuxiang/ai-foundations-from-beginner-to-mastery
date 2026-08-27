---
type: exercise
status: draft
area: [math/linear-algebra, math/matrix-analysis]
topic: 广义特征向量与 Jordan 结构
difficulty: [A, B, C, D, E]
prerequisites: ["[[广义特征向量与 Jordan 结构]]", "[[特征多项式与重数]]"]
related: ["[[特征分解]]", "[[Schur 分解]]", "[[矩阵函数与矩阵指数]]", "[[矩阵扰动]]"]
solution: "[[解答 - 广义特征向量与 Jordan 结构]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - 广义特征向量与 Jordan 结构

> [!abstract] 训练目标
> 这组题检查五类能力：准确识别广义特征对象；从核空间增长、重数和最小多项式恢复 Jordan 块；重建关键证明；用最小反例守住标量域与数值边界；把 Jordan 多项式因子迁移到状态传播、梯度和可微特征分解。

## 使用方式

1. 先关闭正文和解答，独立完成 A、B；
2. C 题必须写出关键中间式，不能只引用“Jordan 定理”；
3. D 题按“判断—反例或证明—断裂点—最小修正”作答；
4. E 题同时报告精确数学结论和浮点工程建议；
5. 卡住时只看当前层级提示，不直接打开完整解答；
6. 标记 `independent / hinted / copied / blocked / careless`。

## A. 识别与复述

### LA-JORD-A01

设 $\boldsymbol A\in\mathbb F^{n\times n}$，$\lambda$ 是其特征值。逐条判断下列说法；错误时写出最小修正或反例。

1. 每个普通特征向量都是广义特征向量。
2. 每个广义特征向量都不是普通特征向量。
3. 零向量属于 $G_\lambda(\boldsymbol A)$，但不称为广义特征向量。
4. 若 $(\boldsymbol A-\lambda I)^5\boldsymbol v=0$，则 $\boldsymbol v$ 的阶一定是 $5$。
5. 在 $n$ 维空间中，
   $$
   G_\lambda(\boldsymbol A)
   =\ker(\boldsymbol A-\lambda I)^n.
   $$
6. 若
   $$
   \ker(\boldsymbol A-\lambda I)^k
   =
   \ker(\boldsymbol A-\lambda I)^{k+1},
   $$
   则所有更高次幂的核空间也相等。
7. 对一个特征值，Jordan 块数量等于代数重数。
8. 对一个特征值，最大 Jordan 块大小等于其在最小多项式中的指数。
9. 若 $a_\lambda=g_\lambda$，则所有对应于 $\lambda$ 的 Jordan 块都是 $1\times1$。
10. 任意实方阵在 $\mathbb R$ 上都有 Jordan 形式。
11. 一个 Jordan 基总能选成标准正交基。
12. 精确矩阵的 Jordan 块大小可以由
    $$
    \dim\ker(\boldsymbol A-\lambda I)^k
    $$
    的序列唯一恢复。
13. 若 $\rho(\boldsymbol A)=1$，则 $\{\boldsymbol A^k\}_{k\ge0}$ 一致有界。
14. 一般浮点矩阵宜用 Schur 分解研究谱与不变子空间，而不是显式计算 Jordan 形式。

作答记录：

- 状态：
- 用时：
- 错误类型：

## B. 手算与构造

### LA-JORD-B01

考虑矩阵

$$
\boldsymbol A
=
\begin{bmatrix}
2&1&0&0&0\\
0&2&1&0&0\\
0&0&2&0&0\\
0&0&0&-1&1\\
0&0&0&0&-1
\end{bmatrix}
\in\mathbb R^{5\times5}.
$$

1. 写出 $p_{\boldsymbol A}(t)$，列出每个特征值的代数重数。
2. 计算
   $$
   d_k(2)=\dim\ker(\boldsymbol A-2I)^k,
   \qquad k=1,2,3,
   $$
   以及
   $$
   d_k(-1)=\dim\ker(\boldsymbol A+I)^k,
   \qquad k=1,2.
   $$
3. 从增长量
   $$
   \Delta_k(\lambda)=d_k(\lambda)-d_{k-1}(\lambda)
   $$
   恢复每个特征值的 Jordan 块大小。
4. 求 $a_\lambda$、$g_\lambda$、缺陷 $a_\lambda-g_\lambda$，并判断 $\boldsymbol A$ 是否可对角化。
5. 写出最小多项式 $m_{\boldsymbol A}(t)$，并验证它整除特征多项式。
6. 写出两条 Jordan 链，注明每个向量的阶。
7. 对整数 $k\ge0$，写出 $\boldsymbol A^k$ 的闭式矩阵。
8. 写出 $e^{t\boldsymbol A}$ 的闭式矩阵。
9. 取
   $$
   \boldsymbol h_0
   =
   \begin{bmatrix}0&0&1&0&1\end{bmatrix}^{\mathsf T},
   $$
   求 $\boldsymbol h_k=\boldsymbol A^k\boldsymbol h_0$，指出多项式因子来自哪条链。

作答记录：

- 状态：
- 用时：
- 错误类型：

## C. 推导与证明

### LA-JORD-C01

设 $T:V\to V$，$\dim V=n<\infty$，并固定 $\lambda\in\mathbb F$。记

$$
N=T-\lambda I,
\qquad
K_k=\ker N^k.
$$

1. 证明
   $$
   K_0\subseteq K_1\subseteq K_2\subseteq\cdots.
   $$
2. 证明：若 $K_k=K_{k+1}$，则 $K_{k+j}=K_k$ 对所有 $j\ge0$ 成立。
3. 用维数论证证明 $K_n=K_{n+1}=\cdots$，从而说明
   $$
   G_\lambda(T)=\ker(T-\lambda I)^n.
   $$
4. 证明 $G_\lambda(T)$ 对 $T$ 不变。
5. 设
   $$
   \boldsymbol v_1,\ldots,\boldsymbol v_r
   $$
   满足
   $$
   N\boldsymbol v_1=0,
   \qquad
   N\boldsymbol v_{j+1}=\boldsymbol v_j.
   $$
   证明这组向量线性无关，并逐列写出 $T$ 在该有序基下的矩阵。
6. 假设 $T$ 的特征多项式在 $\mathbb F$ 上分裂。写出从“广义特征空间直和分解”到“Jordan 形式存在”的完整证明链；每一步注明使用的定理或构造。
7. 固定 $\lambda$，设对应块大小为 $r_1,\ldots,r_b$。证明
   $$
   d_k
   =
   \dim\ker(T-\lambda I)^k
   =
   \sum_{i=1}^{b}\min(k,r_i),
   $$
   并推出
   $$
   d_k-d_{k-1}
   =
   \#\{i:r_i\ge k\}.
   $$
8. 由第 7 问证明 Jordan 块大小除排列外唯一，并推出：
   $$
   a_\lambda=\sum_i r_i,
   \qquad
   g_\lambda=b,
   $$
   且最小多项式中 $(t-\lambda)$ 的指数是 $\max_i r_i$。

作答记录：

- 状态：
- 用时：
- 错误类型：

## D. 边界、反例与纠错

### LA-JORD-D01

对每条说法完成“判断—最小反例或证明—断裂点—最小修正”。

1. “只要特征值重复，矩阵就存在非平凡 Jordan 块。”
2. “同一特征值的代数重数与几何重数已经唯一决定其全部 Jordan 块。”
3. “若一个实矩阵唯一的实特征值是 $0$，它必幂零。”
4. “所有特征值都位于单位圆内或单位圆上，就足以保证矩阵幂有界。”
5. “Jordan 形式与 Schur 形式只是写法不同，数值稳定性没有本质差异。”
6. “若 $\boldsymbol v$ 是三阶广义特征向量，则
   $(\boldsymbol A-\lambda I)^2\boldsymbol v=0$。”
7. “相同特征多项式与相同最小多项式足以保证矩阵相似。”
8. “实对称矩阵的重复特征值可能形成 $J_2(\lambda)$。”
9. “若深度学习框架能返回 `eig`，其特征向量梯度在重复特征值处也一定有限且唯一。”

要求至少使用以下对象中的四个：

$$
2I_2,
\qquad
J_2(1),
\qquad
J_3(0)\oplus J_1(0),
\qquad
J_2(0)\oplus J_2(0),
\qquad
\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
$$

第 7 问可考虑维数 $6$、单一特征值 $0$ 的两个块划分：

$$
3+3,
\qquad
3+2+1.
$$

作答记录：

- 状态：
- 用时：
- 错误类型：

## E. AI 迁移

### AI-JORD-E01

一个二维线性状态模块反复应用同一个转移矩阵：

$$
\boldsymbol h_{k+1}
=
\boldsymbol A\boldsymbol h_k,
\qquad
\boldsymbol h_0
=
\begin{bmatrix}0\\1\end{bmatrix}.
$$

比较

$$
\boldsymbol A_1
=
\begin{bmatrix}1&0\\0&1\end{bmatrix},
\qquad
\boldsymbol A_2
=
\begin{bmatrix}1&1\\0&1\end{bmatrix},
\qquad
\boldsymbol A_{\varepsilon}
=
\begin{bmatrix}1&1\\\varepsilon&1\end{bmatrix},
\quad \varepsilon>0.
$$

1. 证明 $\boldsymbol A_1$ 与 $\boldsymbol A_2$ 有相同特征多项式和谱半径，但 Jordan 结构不同。
2. 分别求
   $$
   \boldsymbol h_k^{(1)}=\boldsymbol A_1^k\boldsymbol h_0,
   \qquad
   \boldsymbol h_k^{(2)}=\boldsymbol A_2^k\boldsymbol h_0.
   $$
   解释为什么只看谱半径会漏掉关键行为。
3. 若终端损失为
   $$
   L=\frac12\|\boldsymbol h_K\|_2^2,
   $$
   求
   $$
   \nabla_{\boldsymbol h_0}L
   $$
   在 $\boldsymbol A_1$、$\boldsymbol A_2$ 下的闭式，并比较其增长阶。
4. 求 $\boldsymbol A_\varepsilon$ 的两个特征值，说明一个大小为 $O(\varepsilon)$ 的矩阵扰动为什么能产生大小为 $O(\sqrt\varepsilon)$ 的谱分裂。
5. 求 $\boldsymbol A_\varepsilon$ 的两个特征向量的一种选择，说明当 $\varepsilon\to0^+$ 时特征向量基为什么趋于病态。
6. 你在浮点训练日志中观察到两个非常接近 $1$ 的特征值。能否据此断言权重矩阵具有精确 $J_2(1)$ 结构？给出一份至少包含四项的诊断清单。
7. 若模型只需要稳定传播和一个二维近重复谱子空间，你会优先报告 Jordan 块、单个特征向量，还是 Schur 不变子空间？说明选择、条件和局限。

作答记录：

- 状态：
- 用时：
- 错误类型：

## 分级提示

### LA-JORD-A01

- **一级提示**：先区分“向量”“空间”“块数量”“块大小”和“总维数”。
- **二级提示**：普通特征向量对应阶 $1$；最大块看最小多项式，块总大小看代数重数。
- **三级提示**：实旋转矩阵负责暴露分裂条件；$J_2(1)^k$ 负责暴露谱半径不足。

### LA-JORD-B01

- **一级提示**：矩阵已经按 $3+2$ 分块；先分别处理 $J_3(2)$ 与 $J_2(-1)$。
- **二级提示**：对大小为 $r$ 的块，$\dim\ker N^k=\min(k,r)$。
- **三级提示**：使用
  $$
  (\lambda I+N)^k
  =\sum_j\binom{k}{j}\lambda^{k-j}N^j,
  \qquad
  e^{t(\lambda I+N)}
  =e^{\lambda t}\sum_j\frac{t^j}{j!}N^j.
  $$

### LA-JORD-C01

- **一级提示**：核空间链只需要“多作用一次仍为零”；稳定性证明先处理下一层。
- **二级提示**：链线性无关时，取最高非零下标并作用恰当次幂。
- **三级提示**：每个 Jordan 块对 $d_k$ 的贡献是 $\min(k,r)$；一阶差分就是该块是否仍能贡献新方向的指示函数。

### LA-JORD-D01

- **一级提示**：$2I_2$ 有重根但无非平凡块；旋转矩阵暴露实数域边界。
- **二级提示**：块划分 $3+1$ 与 $2+2$ 有相同 $a,g$；块划分 $3+3$ 与 $3+2+1$ 有相同特征多项式和最小多项式。
- **三级提示**：数值稳定性比较时，检查换基矩阵是一般可逆还是正交/酉。

### AI-JORD-E01

- **一级提示**：$J_2(1)^k=I+kN$。
- **二级提示**：
  $$
  \nabla_{\boldsymbol h_0}L
  =(\boldsymbol A^K)^{\mathsf T}\boldsymbol h_K.
  $$
- **三级提示**：$\boldsymbol A_\varepsilon$ 的特征值为 $1\pm\sqrt\varepsilon$；可选特征向量为 $[1,\pm\sqrt\varepsilon]^{\mathsf T}$。

## 自评标准

| 层级 | 达标表现 |
|---|---|
| A | 能不混淆阶、块数量、块总大小与最大块大小 |
| B | 能从核增长恢复块并正确求幂、指数和状态 |
| C | 能独立重建核稳定、链独立与块唯一性证明 |
| D | 能主动补上分裂、正规性和浮点容差条件 |
| E | 能把多项式瞬态、反向传播与 Schur 诊断连成完整论证 |

完成后对照[[解答 - 广义特征向量与 Jordan 结构]]，只修正具体断点；不要用“看懂了解答”替代隔日重新独立作答。
