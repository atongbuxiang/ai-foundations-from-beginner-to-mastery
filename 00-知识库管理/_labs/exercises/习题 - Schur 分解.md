---
type: exercise
status: draft
area: [math/linear-algebra, math/matrix-analysis, numerical-linear-algebra]
topic: Schur 分解
difficulty: [A, B, C, D, E]
prerequisites: ["[[Schur 分解]]", "[[QR 分解]]", "[[广义特征向量与 Jordan 结构]]"]
related: ["[[特征分解]]", "[[定理 - 有限维谱定理]]", "[[矩阵函数与矩阵指数]]", "[[矩阵扰动]]"]
solution: "[[解答 - Schur 分解]]"
created: 2026-08-15
updated: 2026-08-15
---

# 习题 - Schur 分解

> [!abstract] 训练目标
> 这组题检查五类能力：准确区分 Schur、QR、特征与 Jordan 分解；手算复/实 Schur 形式并验收；从不变旗标重建存在性证明；用最小反例守住正规性、实数域、唯一性与条件性边界；把重排 Schur 子空间迁移到线性 RNN/SSM 的状态与梯度分析。

## 使用方式

1. 先关闭正文和解答，独立完成 A、B；
2. C 题必须写出关键块矩阵等式，不能只引用“Schur 定理”；
3. D 题按“判断—最小反例或证明—断裂点—最小修正”作答；
4. E 题同时报告精确数学结论、数值验收量与建模含义；
5. 卡住时只看当前层级提示，不直接打开完整解答；
6. 标记 `independent / hinted / copied / blocked / careless`。

## A. 识别与复述

### LA-SCHUR-A01

逐条判断下列说法；错误时给出最小修正或反例。

1. 每个复方阵都有复 Schur 分解。
2. 每个实方阵都能被实正交矩阵相似为实上三角矩阵。
3. 复 Schur 形式的对角元按代数重数列出原矩阵的全部特征值。
4. Schur 向量全都是原矩阵的特征向量。
5. 前 $k$ 个 Schur 向量的张成空间对原矩阵不变。
6. 若矩阵正规，则任一上三角 Schur 形式都没有严格上三角元素。
7. 若复 Schur 形式为对角矩阵，则原矩阵正规。
8. Schur 分解中的酉矩阵和三角矩阵都唯一。
9. 实 Schur 形式中的每个 $2\times2$ 对角块编码一对共轭复特征值。
10. $A=QR$ 与 $A=QTQ^*$ 是同一种分解的两种写法。
11. 一步无位移 QR 迭代 $A_k=Q_kR_k$、$A_{k+1}=R_kQ_k$ 是酉相似变换。
12. 重构残差很小就足以证明每个计算特征值都有很小的前向误差。
13. 对复 Schur 形式，$\|\operatorname{tril}(T,-1)\|$ 可用于检查三角泄漏。
14. 对实 Schur 形式，应把所有第一条次对角线元素都当作计算误差。

作答记录：

- 状态：
- 用时：
- 错误类型：

## B. 手算、构造与验收

### LA-SCHUR-B01

考虑

$$
\boldsymbol A
=
\begin{bmatrix}
1&-1\\
1&3
\end{bmatrix},
\qquad
\boldsymbol q_1
=\frac1{\sqrt2}
\begin{bmatrix}1\\-1\end{bmatrix},
\qquad
\boldsymbol q_2
=\frac1{\sqrt2}
\begin{bmatrix}1\\1\end{bmatrix}.
$$

1. 求特征多项式、全部特征值、代数重数与几何重数，并判断 $A$ 是否可对角化。
2. 验证 $q_1,q_2$ 标准正交，并令
   $$
   Q=[q_1\ q_2].
   $$
3. 直接计算 $Aq_1$ 与 $Aq_2$，再由列坐标求
   $$
   T=Q^{\mathsf T}AQ.
   $$
4. 验证 $A=QTQ^{\mathsf T}$，并说明哪一列必为特征向量、哪一列不是。
5. 对整数 $k\ge0$ 求 $T^k$ 与 $A^k$ 的闭式。
6. 求 $e^{tT}$ 与 $e^{tA}$ 的闭式。
7. 用精确算术计算下列四个验收量：
   $$
   \|A-QTQ^{\mathsf T}\|_F,
   \qquad
   \|Q^{\mathsf T}Q-I\|_F,
   \qquad
   \|\operatorname{tril}(T,-1)\|_F,
   \qquad
   \|Aq_1-2q_1\|_2.
   $$
8. 计算
   $$
   \|T\|_F^2-\sum_i|\lambda_i|^2,
   $$
   并解释这个量在本例中怎样反映严格上三角耦合。
9. 再考虑实旋转矩阵
   $$
   R=
   \begin{bmatrix}
   0&-1\\1&0
   \end{bmatrix}.
   $$
   说明它为什么不存在实上三角 Schur 形式，但 $Q=I_2,T=R$ 为什么是合法的实 Schur 形式；最后给出一个复 Schur 形式。

作答记录：

- 状态：
- 用时：
- 错误类型：

## C. 推导与证明

### LA-SCHUR-C01

设 $V$ 是 $n$ 维复内积空间，$A:V\to V$ 为线性算子。

1. 设 $(q_1,\ldots,q_n)$ 是标准正交基，
   $$
   V_k=\operatorname{span}(q_1,\ldots,q_k).
   $$
   证明：$A$ 在这组基下的矩阵上三角，当且仅当每个 $V_k$ 都对 $A$ 不变。
2. 从代数学基本定理出发，用维数归纳完整证明复 Schur 定理。必须说明：
   - 为什么存在单位特征向量 $q_1$；
   - 将 $q_1$ 扩充成标准正交基后为什么出现块
     $$
     \begin{bmatrix}\lambda&*\\0&B\end{bmatrix};
     $$
   - 为什么可对压缩块 $B$ 使用归纳；
   - 为什么归纳得到的基仍是原空间的标准正交基。
3. 设 $A=QTQ^*$，$T$ 上三角。证明：
   $$
   \sigma(A)=\{t_{11},\ldots,t_{nn}\}
   $$
   （计重数），并推出
   $$
   \operatorname{tr}(A)=\sum_i t_{ii},
   \qquad
   \det(A)=\prod_i t_{ii}.
   $$
4. 证明上三角正规矩阵必为对角矩阵，并由此推出：复矩阵酉可对角化，当且仅当它正规。
5. 将 $Q=[Q_1\ Q_2]$、$T$ 分块为
   $$
   T=
   \begin{bmatrix}
   T_{11}&T_{12}\\
   0&T_{22}
   \end{bmatrix}.
   $$
   证明
   $$
   AQ_1=Q_1T_{11}.
   $$
   再证明正交投影 $P=Q_1Q_1^*$ 与 $A$ 可交换，当且仅当 $T_{12}=0$。
6. 对一步无位移 QR 迭代
   $$
   A_k=Q_kR_k,
   \qquad
   A_{k+1}=R_kQ_k,
   $$
   证明
   $$
   A_{k+1}=Q_k^*A_kQ_k.
   $$
   定义 $Z_m=Q_0Q_1\cdots Q_{m-1}$，证明
   $$
   A_m=Z_m^*A_0Z_m.
   $$
7. 设
   $$
   T=
   \begin{bmatrix}
   \lambda&\eta\\0&\mu
   \end{bmatrix}.
   $$
   先由递推证明
   $$
   T^k=
   \begin{bmatrix}
   \lambda^k&\eta\sum_{j=0}^{k-1}\lambda^{k-1-j}\mu^j\\
   0&\mu^k
   \end{bmatrix}.
   $$
   再对多项式 $f$ 证明
   $$
   f(T)_{12}
   =
   \begin{cases}
   \eta\dfrac{f(\lambda)-f(\mu)}{\lambda-\mu},&\lambda\ne\mu,\\[1.2ex]
   \eta f'(\lambda),&\lambda=\mu.
   \end{cases}
   $$

作答记录：

- 状态：
- 用时：
- 错误类型：

## D. 边界、反例与纠错

### LA-SCHUR-D01

对每条说法完成“判断—最小反例或证明—断裂点—最小修正”。

1. “因为 $A=QTQ^*$，所以 $Q$ 的每一列都是 $A$ 的特征向量。”
2. “同一个矩阵的 Schur 分解唯一。”
3. “每个实方阵都存在实正交矩阵，使 $Q^{\mathsf T}AQ$ 上三角。”
4. “只要 $\mathcal S=\operatorname{range}(Q_1)$ 对 $A$ 不变，正交投影 $P=Q_1Q_1^*$ 就与 $A$ 可交换。”
5. “Schur 坐标是酉坐标，所以所有特征值都对扰动良态。”
6. “$A=QR$ 已经给出了 $A$ 的 Schur 分解。”
7. “一个上三角正规矩阵仍可能保留非零严格上三角元素。”
8. “两个矩阵只要有相同的 Schur 对角线，就必相似。”
9. “若计算得到的 Schur 重构残差接近机器精度，则每个特征值相对误差也接近机器精度。”

要求至少使用以下对象中的四个：

$$
\begin{bmatrix}1&1\\0&2\end{bmatrix},
\qquad
\begin{bmatrix}0&-1\\1&0\end{bmatrix},
\qquad
I_2,
\qquad
J_2(1),
\qquad
\begin{bmatrix}0&1\\\varepsilon&0\end{bmatrix}.
$$

作答记录：

- 状态：
- 用时：
- 错误类型：

## E. AI 迁移：稳定 Schur 子空间、瞬态与反向传播

### AI-SCHUR-E01

一个三维线性状态模块满足

$$
\boldsymbol h_{k+1}=\boldsymbol A\boldsymbol h_k,
\qquad
\boldsymbol A=\boldsymbol Q\boldsymbol T\boldsymbol Q^{\mathsf T},
$$

其中 $Q\in\mathbb R^{3\times3}$ 正交。为把重点放在 Schur 动力学而不是复变量微分约定上，本题取所有状态和参数为实数，且

$$
\boldsymbol T
=
\begin{bmatrix}
r&\gamma&\beta\\
0&r&0\\
0&0&u
\end{bmatrix},
\qquad
0<r<1<u,
\qquad
\gamma,\beta\in\mathbb R\setminus\{0\}.
$$

记 $Q=[Q_1\ q_3]$，其中 $Q_1$ 由前两列组成；定义 Schur 坐标

$$
\boldsymbol y_k=Q^{\mathsf T}\boldsymbol h_k.
$$

1. 证明 $\mathcal S=\operatorname{range}(Q_1)$ 是 $A$ 的稳定不变子空间，并说明“稳定”在这里指什么。
2. 令 $P=Q_1Q_1^{\mathsf T}$。证明 $AP\ne PA$，并解释这为什么不否定 $\mathcal S$ 的不变性。
3. 取 $h_0=Qe_2$。求 $y_k$ 与 $\|h_k\|_2$ 的闭式，并指出即使 $0<r<1$，哪个多项式因子仍能制造有限时间瞬态。
4. 令
   $$
   L=\frac12\|h_K\|_2^2.
   $$
   先证明
   $$
   \nabla_{y_0}L=(T^K)^{\mathsf T}y_K.
   $$
   再求该梯度的三个分量。为简化记号，令
   $$
   a=r^K,
   \qquad
   b=\gamma Kr^{K-1},
   \qquad
   c=\beta\frac{u^K-r^K}{u-r}.
   $$
   解释为什么第三个梯度分量可能非零，尽管当前前向轨迹没有不稳定坐标分量。
5. 证明
   $$
   \|h_k\|_2=\|y_k\|_2,
   \qquad
   \|\nabla_{h_0}L\|_2=\|\nabla_{y_0}L\|_2,
   $$
   并说明这项结论能排除哪一类“坐标假象”、不能排除哪一类真实动力学增长。
6. 若使用 SciPy 的复 Schur 重排，希望把单位圆内的两个特征值放到左上角，应选择怎样的排序谓词或内置选项？返回的 `sdim` 应是多少？
7. 为一次数值实验设计最少四个验收量，至少覆盖：分解重构、正交/酉性、稳定子空间不变性和谱排序。
8. 一个模型把状态矩阵直接参数化为对角矩阵。与一般 Schur 三角块相比，它删去了什么动力学；这为什么既可能是高效归纳偏置，也可能漏掉有限时间耦合？

作答记录：

- 状态：
- 用时：
- 错误类型：

## 分级提示

### LA-SCHUR-A01

- **一级提示**：先区分“存在性”“唯一性”“实/复域”“上三角/准上三角”。
- **二级提示**：Schur 向量的真实语义是前缀不变空间；正规性才把三角形式压成对角形式。
- **三级提示**：实旋转矩阵负责暴露 $2\times2$ 块边界；近 Jordan 扰动负责暴露残差与前向条件性的差别。

### LA-SCHUR-B01

- **一级提示**：先算 $Aq_1,Aq_2$；它们在 $(q_1,q_2)$ 中的坐标就是 $T$ 的两列。
- **二级提示**：本例 $T=2I+N$ 且 $N^2=0$。
- **三级提示**：旋转矩阵的复特征向量可选为 $[1,-i]^{\mathsf T}$ 与 $[1,i]^{\mathsf T}$，归一化后组成酉矩阵。

### LA-SCHUR-C01

- **一级提示**：矩阵第 $j$ 列只涉及前 $j$ 个基向量，正好等价于每个前缀空间不变。
- **二级提示**：正规上三角矩阵的证明可比较第一行范数与第一列范数，再归纳到右下角主块。
- **三级提示**：$P$ 在 Schur 坐标中是 $\operatorname{diag}(I,0)$；直接分别乘 $TP$ 与 $PT$。

### LA-SCHUR-D01

- **一级提示**：用 $J_2(1)$ 同时检查“列全是特征向量”“相同对角线”和“正规上三角”三类说法。
- **二级提示**：对 $\begin{bmatrix}1&1\\0&2\end{bmatrix}$，$\operatorname{span}(e_1)$ 不变，但其正交补不变吗？
- **三级提示**：$\begin{bmatrix}0&1\\\varepsilon&0\end{bmatrix}$ 的特征值是 $\pm\sqrt\varepsilon$；比较输入扰动阶与谱移动阶。

### AI-SCHUR-E01

- **一级提示**：$T$ 的左上 $2\times2$ 主块闭合，所以前两个坐标构成不变子系统。
- **二级提示**：
  $$
  T^K=
  \begin{bmatrix}
  a&b&c\\0&a&0\\0&0&u^K
  \end{bmatrix}.
  $$
- **三级提示**：当前 $y_0=e_2$ 给出 $y_K=[b,a,0]^{\mathsf T}$，但反传必须乘整个 $(T^K)^{\mathsf T}$，不能只看实际前向坐标。

## 自评标准

| 层级 | 达标表现 |
|---|---|
| A | 能不混淆 Schur/QR、Schur 向量/特征向量、上三角/准上三角 |
| B | 能手算缺陷矩阵和旋转矩阵的 Schur 形式，并报告四类验收量 |
| C | 能独立重建存在性、正规特例、不变子空间与 QR 相似迭代证明 |
| D | 能用最小反例主动补上域、正规性、唯一性和条件性条件 |
| E | 能把稳定谱簇、非正规瞬态、反向传播、重排与数值验收连成完整分析 |

完成后对照[[解答 - Schur 分解]]，只修正具体断点；隔日至少重新独立完成 B、C5、D4 与 E3–E5。
