---
type: exercise-set
status: draft
area: [labs, math/matrix-analysis, math/matrix-calculus, ai/automatic-differentiation]
prerequisites: ["[[矩阵函数的 Fréchet 导数]]"]
related: ["[[矩阵函数与矩阵指数]]", "[[Kronecker 积、向量化与矩阵方程]]", "[[伴随算子]]", "[[练习与测验 MOC]]"]
sources: ["Higham-2008-Functions-of-Matrices", "Higham-Relton-2014-Higher-Frechet", "AlMohy-Higham-2009-Expm-Frechet"]
solutions: ["[[解答 - 矩阵函数的 Fréchet 导数]]"]
created: 2026-08-16
updated: 2026-08-16
---

# 习题 - 矩阵函数的 Fréchet 导数

> [!abstract] 训练目标
> 把“会对标量函数求导”升级为“能操作矩阵空间上的一阶线性算子”：既能手算 $L_f(A,E)$，也能在块矩阵、除差、Kronecker、Sylvester 和伴随 VJP 之间切换，并能识别重复谱、非正规性、显式 Jacobian 和差分验证中的失败边界。

## 作答规则

1. A–E 每级三题，共 15 题；
2. 每题先声明 $A,E,L_f(A,E)$ 的 shape；
3. 写 $f'(A)E$ 时必须证明相应可交换条件；
4. 反向题使用 Frobenius 内积并明确转置/共轭转置；
5. 数值题区分函数条件性、算法稳定性和验证误差；
6. 不允许通过显式逐元素 Jacobian 逃避算子推导。

## A 级：识别与复述

### MA-FR-A01：四种“导数对象”

设

$$
f:\mathbb R^{n\times n}\to\mathbb R^{n\times n}.
$$

分别说明以下对象的输入、输出与 shape：

1. 方向作用 $L_f(A,E)$；
2. 完整线性算子 $L_f(A)$；
3. 列 `vec` 下的 Kronecker 矩阵 $K_f(A)$；
4. 反向传播中的伴随作用 $L_f(A)^*(G)$；
5. 为什么说“$f$ 的导数是一个 $n\times n$ 矩阵”通常不完整？

### MA-FR-A02：判断八个断言

判断并说明理由：

1. Fréchet 可微蕴含每个方向的 Gâteaux 导数存在；
2. 每个方向导数存在就蕴含 Fréchet 可微；
3. $L_{z^2}(A,E)=2AE$ 对任意 $A,E$ 成立；
4. $L_f(\lambda I,E)=f'(\lambda)E$；
5. 重复特征值必然使平滑矩阵函数不可微；
6. 在 Frobenius 范数下 $\|L_f(A)\|=\|K_f(A)\|_2$；
7. 后向稳定算法一定给出小前向误差；
8. 反向传播需要 $L_f(A)^{-1}$。

### MA-FR-A03：除差与重复谱

对 $f(z)=z^2$ 和特征值

$$
\lambda_1=1,
\quad
\lambda_2=1,
\quad
\lambda_3=3,
$$

1. 写出 $3\times3$ 除差矩阵 $F$；
2. 哪些条目使用 $f'(\lambda)$？
3. 若 $A=Q\operatorname{diag}(1,1,3)Q^*$，写出 $L_f(A,E)$；
4. 说明答案为什么与 $AE+EA$ 一致。

## B 级：手算与构造

### MA-FR-B01：平方函数的非交换反例

令

$$
A=\begin{bmatrix}0&1\\0&0\end{bmatrix},
\qquad
E=\begin{bmatrix}0&0\\1&0\end{bmatrix},
\qquad
f(A)=A^2.
$$

1. 计算 $AE,EA$；
2. 求 $L_f(A,E)$；
3. 计算 $2AE$ 并说明标量捷径失败；
4. 直接展开 $(A+hE)^2$，验证一阶式；
5. 写出一般 $2\times2$ 矩阵 $A$ 对应的 Kronecker Jacobian 公式。

### MA-FR-B02：对角矩阵指数的除差手算

令

$$
A=\operatorname{diag}(0,1),
\qquad
E=\begin{bmatrix}1&2\\3&4\end{bmatrix}.
$$

1. 写出指数函数的除差矩阵；
2. 求 $L_{\exp}(A,E)$；
3. 分别计算 $e^AE$ 与 $Ee^A$；
4. 验证三者一般不同；
5. 用所得结果核对交换子恒等式
   $$
   AL-LA=e^AE-Ee^A.
   $$

### MA-FR-B03：SPD 平方根的 Sylvester 方程

令

$$
A=\operatorname{diag}(1,4),
\qquad
E=\begin{bmatrix}2&3\\3&8\end{bmatrix}.
$$

1. 求 $X=A^{1/2}$；
2. 解 $XZ+ZX=E$；
3. 用平方根除差公式重新计算 $Z$；
4. 验证 $Z$ 为 Hermitian；
5. 若把 $A$ 的第二个特征值改为 $\varepsilon^2$，指出哪个分量最先变敏感。

## C 级：推导与证明

### MA-FR-C01：多项式与块矩阵定理

1. 用归纳法证明
   $$
   L_{z^k}(A,E)
   =\sum_{j=0}^{k-1}A^jEA^{k-1-j};
   $$
2. 证明
   $$
   \begin{bmatrix}A&E\\0&A\end{bmatrix}^{k}
   =
   \begin{bmatrix}
   A^k&L_{z^k}(A,E)\\0&A^k
   \end{bmatrix};
   $$
3. 推广到任意多项式 $p$；
4. 解释推广到一般解析矩阵函数还需要什么工具或条件；
5. 说明块公式为什么不等于“生产中必须计算 $2n$ 阶函数”。

### MA-FR-C02：指数积分公式与伴随

1. 从指数双重级数证明
   $$
   L_{\exp}(A,E)
   =\int_0^1e^{(1-s)A}Ee^{sA}\,ds;
   $$
2. 推导 $AE=EA$ 时的简化；
3. 使用 Frobenius 内积证明
   $$
   L_{\exp}(A)^*(G)=L_{\exp}(A^*,G);
   $$
4. 对实矩阵标量损失
   $$
   \ell(A)=\langle G,e^A\rangle_F
   $$
   求 $\nabla_A\ell$；
5. 说明为什么这里使用的是伴随而不是逆。

### MA-FR-C03：平方导数的 Kronecker 形式与条件数

1. 对 $f(A)=A^2$ 证明
   $$
   K_f(A)=I\otimes A+A^T\otimes I;
   $$
2. 令 $A=\operatorname{diag}(\alpha,\beta)$，按列 `vec` 写出 $K_f(A)$；
3. 求 Frobenius 诱导的绝对条件数；
4. 当 $\alpha=-\beta$ 时解释为什么某些方向的一阶响应为零；
5. 这是否说明整个导数算子为零？

## D 级：边界、反例与纠错

### MA-FR-D01：方向导数存在但不是 Fréchet 导数

定义

$$
\phi(x,y)=
\begin{cases}
\dfrac{x^3}{x^2+y^2},&(x,y)\ne(0,0),\\[0.8em]
0,&(x,y)=(0,0).
\end{cases}
$$

再定义矩阵值函数

$$
F(A)=\phi(a_{11},a_{22})I_2.
$$

1. 求 $\phi$ 在原点沿方向 $(a,b)$ 的方向导数；
2. 用 $(1,0),(0,1),(1,1)$ 证明方向结果不线性；
3. 推出 $F$ 在零矩阵处不 Fréchet 可微；
4. 说明这个反例反驳了哪种常见推理。

### MA-FR-D02：重复谱、eig 基与矩阵函数

令

$$
A=\lambda I_n,
\qquad
f(z)=e^z.
$$

1. 求 $L_f(A,E)$；
2. $A$ 的特征向量基是否唯一？
3. 为什么直接对 eig 向量求导可能没有唯一答案？
4. 为什么这不妨碍 $e^A$ 的 Fréchet 导数存在？
5. 给出一条实现纪律，避免把 $1/(\lambda_i-\lambda_j)$ 的裸公式用在重复谱上。

### MA-FR-D03：验证与物化的双重陷阱

设 $A,E\in\mathbb R^{3000\times3000}$。

1. $K_f(A)$ 有多少行列和元素？
2. float64 显式存储需要多少 PB（$1\text{ PB}=10^{15}$ bytes）？
3. 为什么只在 $h=10^{-16}$ 做一次前向差分不能证明导数错误或正确？
4. 设计一个至少含五个 $h$ 的验证方案；
5. 给出不物化 $K_f(A)$ 的 JVP、VJP 和伴随测试路线。

## E 级：AI 迁移

### AI-FR-E01：连续时间 SSM 的可训练离散化

设

$$
A_d(A,\Delta)=e^{\Delta A},
$$

其中 $A\in\mathbb R^{n\times n}$、$\Delta>0$。

1. 对 $A$ 的方向 $E$ 推导 $dA_d$；
2. 对标量 $\Delta$ 求偏导；
3. 解释两种导数为何一个需要 Fréchet 算子、另一个可写成普通乘积；
4. 若损失上游为 $G$，写出对 $A$ 的 VJP；
5. 给出非正规 $A$ 下至少三项训练诊断。

### AI-FR-E02：阻尼白化层的隐式导数

令

$$
C\succcurlyeq0,
\qquad
A=C+\varepsilon I\succ0,
\qquad
W=A^{-1/2}.
$$

1. 令 $X=A^{1/2}$，推导 $dX$ 的 Sylvester 方程；
2. 推导 $dW$；
3. 若 $C$ 的最小特征值趋近 $0$，说明 $\varepsilon$ 如何影响导数；
4. 为什么重复特征值不是使用裸 eig-gap 分母的理由？
5. 比较“展开有限步 Newton–Schulz 反传”和“对精确逆平方根做隐式反传”的对象差别。

### AI-FR-E03：矩阵指数层的反向契约与验收

某层前向为

$$
Y=e^A,
$$

损失给出上游 $G$。

1. 写出精确 VJP；
2. 写出一个不形成 $n^2\times n^2$ Jacobian 的实现接口；
3. 写出伴随点积测试；
4. 写出中心差分标量损失测试；
5. 给出一份包含分支、dtype、条件性、算法映射与精确函数映射区别的最小验收报告。

## 分级提示

### 方向提示

- B02：先在特征坐标中逐元素乘除差矩阵；
- B03：对角 $X$ 下，Sylvester 方程逐元素解耦；
- C02：把两个指数展开，使用 Beta 积分收集总次数；
- C03：对 $AE$ 和 $EA$ 分别使用列 `vec` 恒等式；
- D01：方向导数存在不代表它对方向是线性的；
- E02：把逆平方根拆成“平方根 + 逆”。

### 结构提示

- 块公式、除差公式与 Kronecker 形式不是三种不同导数；
- JVP 保留方向 $E$，VJP 把上游 $G$ 经伴随拉回；
- 重复谱用连续除差，非正规性用基条件/separation/伪谱诊断；
- 结构化输入只允许结构切空间中的扰动。

### 数值提示

- D03 中 $3000^2=9\times10^6$；
- 差分检查应在截断误差区看到斜率，再进入舍入误差地板；
- 伴随测试只需能应用 $L_f$ 和 $L_f^*$；
- 大规模 action 不等于完整形成 $L_f(A,E)$。

