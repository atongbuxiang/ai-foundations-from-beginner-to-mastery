---
type: exercise-set
status: draft
area: [labs, math/linear-algebra, math/matrix-calculus]
prerequisites: ["[[Kronecker 积、向量化与矩阵方程]]"]
related: ["[[多线性映射、张量与缩并]]", "[[Schur 分解]]", "[[伴随算子]]", "[[练习与测验 MOC]]"]
sources: ["Petersen-Pedersen-Matrix-Cookbook", "SciPy-solve-sylvester"]
solutions: ["[[解答 - Kronecker 积、向量化与矩阵方程]]"]
created: 2026-08-16
updated: 2026-08-16
---

# 习题 - Kronecker 积、向量化与矩阵方程

> [!abstract] 训练目标
> 形成稳定的“对象—形状—排列—结构算法”链条：能手算 Kronecker/vec，能从指标重建公式，能把 Sylvester/Lyapunov 与矩阵 Jacobian 转成线性算子，并能识别 row-major、复共轭、显式物化和 K-FAC 近似中的边界。

## 作答规则

1. A–E 每级三题，共 15 题；
2. `vec` 一律使用正文中的列堆叠，若改约定必须明确说明；
3. 每个 Kronecker 公式都先写输入输出形状；
4. 矩阵方程题区分“存在唯一解”“良态”“推荐算法”；
5. AI 题区分精确代数等式与统计/数值近似。

## A 级：识别与复述

### LA-KV-A01：四种乘积与形状

给定

$$
A\in\mathbb R^{2\times3},
\quad
B\in\mathbb R^{4\times5},
\quad
u\in\mathbb R^2,
\quad
v\in\mathbb R^4.
$$

1. 求 $A\otimes B$ 的形状；
2. $AB$ 是否有定义？
3. $A\odot B$ 是否有定义？
4. $uv^T$ 与 $u\otimes v$ 分别是什么形状/对象？
5. 说明四种运算各自是否发生求和。

### LA-KV-A02：列 `vec` 与软件顺序

对

$$
X=\begin{bmatrix}1&2&3\\4&5&6\end{bmatrix},
$$

1. 写出本课程的 $\operatorname{vec}(X)$；
2. 写出 row-major flatten；
3. 两者之间是什么关系？
4. 在 NumPy 与 PyTorch 中分别怎样显式获得本课程的列 `vec`？

### LA-KV-A03：判断六个断言

判断并说明理由：

1. $A\otimes B=B\otimes A$；
2. $(A\otimes B)^*=A^*\otimes B^*$；
3. $\operatorname{rank}(A\otimes B)=\operatorname{rank}(A)+\operatorname{rank}(B)$；
4. $\kappa_2(A\otimes B)=\kappa_2(A)\kappa_2(B)$（可逆时）；
5. 列 `vec` 下 $\operatorname{vec}(AXB)=(A\otimes B)\operatorname{vec}(X)$；
6. Sylvester 方程唯一可解就一定数值良态。

## B 级：手算与构造

### LA-KV-B01：Kronecker 块手算

设

$$
A=\begin{bmatrix}1&-1\\2&0\end{bmatrix},
\qquad
B=\begin{bmatrix}1&2\\0&3\end{bmatrix}.
$$

1. 计算 $A\otimes B$；
2. 计算 $B\otimes A$；
3. 验证二者一般不相等；
4. 求 $\det(A\otimes B)$，分别用直接结构和行列式公式核对。

### LA-KV-B02：数值核对 vec 恒等式

设

$$
A=\begin{bmatrix}1&2\\0&1\end{bmatrix},
\quad
X=\begin{bmatrix}1&2\\3&4\end{bmatrix},
\quad
B=\begin{bmatrix}1&0\\1&1\end{bmatrix}.
$$

1. 直接计算 $Y=AXB$ 与 $\operatorname{vec}(Y)$；
2. 写出 $B^T\otimes A$；
3. 计算 $(B^T\otimes A)\operatorname{vec}(X)$；
4. 用形状和数值同时核对恒等式。

### LA-KV-B03：对角 Sylvester 方程

求解

$$
AX+XB=C,
$$

其中

$$
A=\operatorname{diag}(1,3),
\quad
B=\operatorname{diag}(2,4),
\quad
C=\begin{bmatrix}3&5\\10&14\end{bmatrix}.
$$

1. 逐元素求 $X$；
2. 写出向量化后的 $4\times4$ 系数矩阵；
3. 列出系数矩阵的四个特征值；
4. 验证解并说明唯一性。

## C 级：推导与证明

### LA-KV-C01：混合乘积与谱

1. 从简单张量 $x\otimes y$ 出发证明
   $$
   (A\otimes B)(C\otimes D)=AC\otimes BD;
   $$
2. 若 $Au_i=\lambda_i u_i$、$Bv_j=\mu_jv_j$，证明 $u_i\otimes v_j$ 是 $A\otimes B$ 的特征向量；
3. 在 $A,B$ 可对角化时说明为何得到全部 $nm$ 个特征方向。

### LA-KV-C02：从指标重建 vec 恒等式

设

$$
A\in\mathbb F^{m\times p},
\quad
X\in\mathbb F^{p\times q},
\quad
B\in\mathbb F^{q\times n}.
$$

不用引用正文结论，从

$$
(AXB)_{ij}=\sum_{r,s}a_{ir}x_{rs}b_{sj}
$$

和列 `vec` 索引出发，证明

$$
\operatorname{vec}(AXB)=(B^T\otimes A)\operatorname{vec}(X).
$$

### LA-KV-C03：Sylvester 唯一性与后验界

1. 推导 $AX+XB=C$ 的向量化系统；
2. 在 $A,B$ 可三角化时证明 Kronecker 和的特征值是 $\lambda_i(A)+\lambda_j(B)$；
3. 推出唯一可解条件；
4. 若
   $$
   \operatorname{sep}(A,-B)
   =\min_{X\ne0}\frac{\|AX+XB\|_F}{\|X\|_F},
   $$
   证明任意解满足
   $$
   \|X\|_F\le\frac{\|C\|_F}{\operatorname{sep}(A,-B)}.
   $$

## D 级：边界、反例与纠错

### LA-KV-D01：row-major 公式错位

使用 B02 的 $A,X,B$。

1. 写出 row-major flatten $\operatorname{rvec}(X)$；
2. 直接计算 $(B^T\otimes A)\operatorname{rvec}(X)$；
3. 与 row-major flatten $(AXB)$ 比较；
4. 解释为什么公式失败，以及怎样用交换矩阵或重新推导修复。

### LA-KV-D02：显式物化的内存灾难

设 $X\in\mathbb R^{2000\times2000}$，考虑 Sylvester 方程的向量化系统，采用 float64。

1. 未知向量长度是多少？
2. 显式稠密系数矩阵有多少元素？
3. 仅存储该矩阵大约需要多少 TB（按 $1\text{ TB}=10^{12}$ bytes）？
4. 给出至少三种不物化的替代路线，并说明 `vec` 形式仍有什么理论价值。

### LA-KV-D03：特征值离零但 separation 很小

令

$$
A_K=\begin{bmatrix}1&K\\0&2\end{bmatrix},
\qquad
B=[0],
$$

把 $X$ 看成 $2\times1$ 向量。

1. $AX+XB=C$ 的唯一性是否随 $K$ 改变？
2. 取 $x=(-K,1)^T$，计算 $A_Kx$；
3. 给出 $\operatorname{sep}(A_K,0)$ 的一个随 $K$ 下降的上界；
4. 说明为何一般非正规矩阵不能只看 $\min_i|\lambda_i(A)|$ 判断矩阵方程条件性。

## E 级：AI 迁移

### AI-KV-E01：K-FAC 的精确式与近似式

线性层 $y=Wx$，其中

$$
W\in\mathbb R^{d_{out}\times d_{in}},
$$

输出反向信号为 $\delta$。

1. 推导单样本 $G=\nabla_W\ell$；
2. 在列 `vec` 下证明 $\operatorname{vec}(G)=x\otimes\delta$；
3. 推导单样本梯度外积的 Kronecker 结构；
4. 写出 K-FAC 的期望因子化，并明确哪一步不是恒等式。

### AI-KV-E02：可分离协方差

设

$$
\Sigma=\Sigma_c\otimes\Sigma_r,
$$

其中 $\Sigma_c\in\mathbb R^{n\times n}$、$\Sigma_r\in\mathbb R^{m\times m}$ 均 SPD。

1. 求 $\Sigma^{-1}$；
2. 求 $\log\det\Sigma$；
3. 求 $\kappa_2(\Sigma)$；
4. 若真实协方差只近似可分离，指出模型误差与数值误差应怎样分开报告。

### AI-KV-E03：隐式层中的矩阵线性化

某隐式层反向方程为

$$
AX+XB=C,
$$

其中 $A\in\mathbb R^{m\times m}$、$B\in\mathbb R^{n\times n}$。

1. 写出理论 Jacobian/线性系统；
2. 给出唯一性条件；
3. 为什么实现中不应显式形成 Jacobian？
4. 设计一个可信求解报告，至少包含 residual、backward error/conditioning、结构算法和 dtype 四类信息。

## 分级提示

### 方向提示

- B01：先按 $[a_{ij}B]$ 排块；
- B02：直接算得 $AXB$ 后再核对 Kronecker 路线；
- B03：$(AX+XB)_{ij}=(a_i+b_j)x_{ij}$；
- C03：将线性算子 $\mathcal L(X)=AX+XB$ 与向量化矩阵对应；
- D03：最小奇异值不大于任意试探向量的输出/输入范数比；
- E01：$\nabla_W\ell=\delta x^T$。

### 结构提示

- 先固定 `vec` 顺序，再写转置和 Kronecker 因子顺序；
- 唯一性看算子是否可逆，条件性看最小奇异值/separation；
- AI 题把精确坐标恒等式、概率近似和浮点计算分三层。

### 计算提示

- B02 中 $AXB=\begin{bmatrix}17&10\\7&4\end{bmatrix}$；
- B03 四个分母是 $3,5,5,7$，但列 `vec` 中排列需自行核对；
- D02 系数矩阵边长为 $4\times10^6$；
- D03 中 $A_K(-K,1)^T=(0,2)^T$。

## 作答记录

| 题号 | 首次状态 | 错误类型 | 回链节点 | 间隔重做 |
|---|---|---|---|---|
| LA-KV-A01—A03 |  |  | [[Kronecker 积、向量化与矩阵方程]] |  |
| LA-KV-B01—B03 |  |  | [[Kronecker 积、向量化与矩阵方程]] |  |
| LA-KV-C01—C03 |  |  | [[Kronecker 积、向量化与矩阵方程]] |  |
| LA-KV-D01—D03 |  |  | [[Kronecker 积、向量化与矩阵方程]] |  |
| AI-KV-E01—E03 |  |  | [[Kronecker 积、向量化与矩阵方程]] |  |

完整解答见[[解答 - Kronecker 积、向量化与矩阵方程]]。

