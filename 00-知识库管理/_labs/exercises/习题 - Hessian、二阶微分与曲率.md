---
type: exercise-set
status: draft
area: [labs, math/calculus, math/linear-algebra, math/optimization, ai/automatic-differentiation]
prerequisites: ["[[Hessian、二阶微分与曲率]]", "[[Taylor 展开与余项]]", "[[Jacobian、JVP 与 VJP]]", "[[定理 - 有限维谱定理]]", "[[二次型与正定矩阵]]"]
related: ["[[多元链式法则与计算图]]", "[[矩阵微分、迹技巧与布局约定]]", "[[自动微分：前向、反向与高阶模式]]", "[[Newton 法、Gauss-Newton 与拟 Newton 法]]", "[[练习与测验 MOC]]"]
sources: ["MIT-18.S096-Second-Derivatives", "Boyd-Vandenberghe-Convex-Optimization", "JAX-Autodiff-Cookbook-HVP", "PyTorch-Jacobians-Hessians-HVP", "Pearlmutter-1994-HVP", "Martens-2020-Natural-Gradient-GGN", "Su-10588-Hessian-Approx"]
solutions: ["[[解答 - Hessian、二阶微分与曲率]]"]
created: 2026-08-17
updated: 2026-08-17
---

# 习题 - Hessian、二阶微分与曲率

> [!abstract] 训练目标
> 从“会列二阶偏导表”升级到“能把二阶导数视为对称双线性型；能用 Taylor、谱和方向曲率判断局部结构；能以 HVP 操作大型模型；能严格区分精确 Hessian、GN/GGN、Fisher 与梯度平方代理”。

## 作答规则

1. A–E 每级三题，共 15 题；
2. 每道计算题先写函数的输入/输出空间，再写一阶和二阶对象类型；
3. 必须区分 $D^2f[u,v]$、$v^\top Hv$ 与 $Hv$；
4. 使用 Hessian 对称性时写出所用光滑条件；
5. 二阶 Taylor 模型必须保留系数 $1/2$ 和余项条件；
6. 驻点分类中，半正定/半负定不能直接下结论；
7. HVP 实现题不得先物化完整 Hessian，除非明确用于小型验证；
8. 曲率近似题必须说明近似丢弃了哪一项、是否 PSD、依赖哪些假设；
9. 数值实验记录 dtype、随机种子、batch、loss reduction、正则和阻尼；
10. 独立完成前不要打开[[解答 - Hessian、二阶微分与曲率]]。

## A 级：对象、类型与逻辑边界

### CALC-HC-A01：翻译十六个二阶声明

逐条写出自然语言、对象类型和成立条件：

1. $D^2f(x)\in\mathcal B_2(X\times X;\mathbb R)$；
2. $D^2f(x)[u,v]=\bigl(D(Df)(x)[u]\bigr)[v]$；
3. $H_{ij}=D^2f(x)[e_i,e_j]$；
4. $D^2f(x)[u,v]=u^\top Hv$；
5. $H=D(\nabla f)(x)$；
6. $D^2f(x)[u,v]=D^2f(x)[v,u]$；
7. $f(x+h)=f(x)+g^\top h+\tfrac12h^\top Hh+o(\|h\|^2)$；
8. $\left.\tfrac{d^2}{dt^2}f(x+tv)\right|_{t=0}=v^\top Hv$；
9. $D^2f[u,v]=\tfrac14(q(u+v)-q(u-v))$；
10. $\lambda_{\min}\le v^\top Hv/\|v\|^2\le\lambda_{\max}$；
11. $Hv=D(\nabla f)(x)[v]$；
12. $H=[He_1\;\cdots\;He_n]$；
13. $H_{f\circ\phi}=J_\phi^\top H_fJ_\phi+\sum_i(\partial_if)H_{\phi_i}$；
14. $H_L=J_r^\top J_r+\sum_i r_iH_{r_i}$；
15. $G_{\mathrm{GGN}}=J_z^\top H_\ell J_z$；
16. $\operatorname{tr}(H)=\mathbb E[z^\top Hz]$，其中 $\mathbb E[zz^\top]=I$。

特别说明第 1–5 项哪些需要坐标或内积，第 6–10 项的光滑/对称条件，以及第 13–16 项不能被省略的假设。

### CALC-HC-A02：判断二十个断言

判断正误；错误项给最小反例或补充条件。

1. 二阶导数的本体总是一个 $n\times n$ 数组；
2. 对标量函数，$D^2f(x)$ 接收两个方向并返回标量；
3. 对 $F:\mathbb R^n\to\mathbb R^m$，其二阶导数通常是输出值双线性映射；
4. 只要所有二阶偏导在一点存在，Hessian 就必定对称；
5. $f\in C^2$ 是 Hessian 对称的常用充分条件；
6. $Hv$ 与 $v^\top Hv$ 形状相同；
7. 若 $v^\top Hv=0$，则必有 $Hv=0$；
8. 若驻点 Hessian 正定，则该点是严格局部极小；
9. 若驻点 Hessian 半正定，则该点必为局部极小；
10. 严格凸 $C^2$ 函数的 Hessian 在每一点都必须正定；
11. 在开凸域上，$C^2$ 函数凸当且仅当 Hessian 处处 PSD；
12. 对任意 $A$，$\nabla(\tfrac12x^\top Ax)=Ax$；
13. HVP 可以在不形成完整 Hessian 的情况下计算；
14. 用 $n$ 个标准基 HVP 可以逐列恢复 $n\times n$ Hessian；
15. 对光滑标量函数，$u^\top Hv=v^\top Hu$；
16. Gauss–Newton 矩阵总等于非线性最小二乘的精确 Hessian；
17. 若输出损失 Hessian PSD，则 GGN PSD；
18. empirical Fisher 一般就是 mini-batch 损失 Hessian；
19. Hessian 的特征值在任意可逆重参数化下保持不变；
20. 自动微分框架返回二阶数组，就证明目标在该点经典二阶可微。

### CALC-HC-A03：为十五个任务选择最直接工具

可选工具包括：二阶 Fréchet 定义、二阶 Taylor 积分余项、方向限制、极化恒等式、谱分解、Rayleigh 商、Sylvester 惯性定律、full Hessian、HVP、梯度中心差分、双线性对称测试、Lanczos、Hutchinson、GN/GGN 分解、阻尼线性求解。

为下列任务选择最直接工具并说明边界：

1. 说明二阶对象为什么接收两个方向；
2. 定量控制二次局部模型误差；
3. 测量指定方向的二阶曲率；
4. 从所有方向二次型恢复混合项；
5. 找最大曲率方向；
6. 判断驻点是否存在下降方向；
7. 小型三参数模型打印全部二阶偏导；
8. 亿级参数模型计算一个 $Hv$；
9. 用独立数值方法核对 HVP；
10. 不形成 $H$ 检查其对称性；
11. 估计最大的几个 Hessian 特征值；
12. 随机估计 Hessian trace；
13. 从非线性最小二乘得到 PSD 曲率替代；
14. 比较驻点在两套可逆坐标中的正负惯性；
15. 近似求解 $(H+\lambda I)p=-g$。

## B 级：手算、形状与谱

### CALC-HC-B01：一个二维非凸函数的完整二阶审计

设

$$
f(x,y)=x^3+xy^2-2x+4y.
$$

1. 求 $\nabla f(x,y)$ 与 $H_f(x,y)$；
2. 说明 Hessian 在何种条件下对称；
3. 在 $a=(1,2)$ 处计算 $H(a)$；
4. 对 $v=(1,-1)^\top$ 计算 $Hv$ 和 $v^\top Hv$，解释二者为何一个非零而另一个为零；
5. 计算 $H(a)$ 的特征值，判断该点附近是否存在正、负方向曲率；
6. 说明为什么不能仅凭 Hessian 不定就称 $a$ 为“鞍点”；
7. 写出 $a$ 附近的二阶 Taylor 模型。

### CALC-HC-B02：非对称系数矩阵与二次优化

令

$$
A=
\begin{bmatrix}
2&4\\
-2&6
\end{bmatrix},
\qquad
b=
\begin{bmatrix}
-2\\-8
\end{bmatrix},
$$

$$
f(x)=\frac12x^\top Ax+b^\top x+3.
$$

1. 求 $A$ 的对称部分 $S$；
2. 证明 $x^\top Ax=x^\top Sx$；
3. 求 $\nabla f$ 和 Hessian；
4. 判断 $f$ 是否强凸，并给出可取的 $\mu,L$；
5. 求唯一驻点 $x_*$ 并分类；
6. 计算 Hessian 的谱条件数；
7. 对 $v=(2,-1)^\top$ 计算 HVP 与方向曲率；
8. 解释为什么直接写 $H=A$ 会与 Hessian 对称性冲突。

### CALC-HC-B03：softmax 交叉熵的输出空间曲率

设三分类 logits 为 $z\in\mathbb R^3$，

$$
\ell(z,y)=\log\sum_{i=1}^3e^{z_i}-y^\top z,
$$

且当前

$$
p=\operatorname{softmax}(z)
=
\begin{bmatrix}
1/2\\1/3\\1/6
\end{bmatrix}.
$$

1. 推导 $\nabla_z\ell=p-y$；
2. 推导 $H_z=\operatorname{Diag}(p)-pp^\top$；
3. 写出此处的 $3\times3$ Hessian；
4. 验证 $H_z\mathbf1=0$ 并解释不变性来源；
5. 证明 $v^\top H_zv=\operatorname{Var}_{i\sim p}(v_i)\ge0$；
6. 对 $v=(1,-1,0)^\top$ 计算 $Hv$ 与 $v^\top Hv$；
7. 说明标签 $y$ 为什么不出现在 Hessian 中；
8. 若 $z=z(\theta)$，写出 GGN–vector product 的 JVP → 输出 HVP → VJP 三步。

## C 级：证明、反例与坐标

### CALC-HC-C01：Taylor、方向曲率与极化

设 $f\in C^2$ 于包含线段 $x+th$、$t\in[0,1]$ 的开集。

1. 令 $\phi(t)=f(x+th)$，推导 $\phi'$ 与 $\phi''$；
2. 由一维积分公式证明

$$
f(x+h)=f(x)+Df(x)[h]
+\int_0^1(1-t)D^2f(x+th)[h,h]\,dt;
$$

3. 证明若 $D^2f$ 在 $x$ 连续，则余项为 $o(\|h\|^2)$；
4. 若 Hessian 是 $\rho$-Lipschitz，证明余项绝对值不超过 $\rho\|h\|^3/6$；
5. 证明 $q(v)=D^2f(x)[v,v]$ 满足极化恒等式；
6. 解释为什么知道所有 $q(v)$ 足以恢复对称双线性型，但只知道坐标轴方向 $q(e_i)$ 不够。

### CALC-HC-C02：二阶最优性与凸性边界

1. 证明驻点处 $H\succ0$ 蕴含严格局部极小；
2. 证明驻点处 Hessian 不定蕴含鞍点；
3. 分别用 $x^4$、$-x^4$、$x^4-y^4$ 说明零 Hessian 可能对应极小、极大或鞍点；
4. 证明开凸域上的 $C^2$ 函数满足

$$
f\text{ 凸}\iff H_f(x)\succeq0\quad\forall x;
$$

5. 给出严格凸但某点 Hessian 不正定（只半正定）的例子；
6. 解释定义域凸性为何不能从二阶判据中删去；
7. 若 $\mu I\preceq H\preceq LI$，推导二侧二次界。

### CALC-HC-C03：非线性重参数化的额外项

设 $x=\phi(z)$，$\widetilde f(z)=f(\phi(z))$。

1. 用分量法推导

$$
H_{\widetilde f}
=
J_\phi^\top H_fJ_\phi
+
\sum_i\frac{\partial f}{\partial x_i}H_{\phi_i};
$$

2. 说明仿射 $\phi(z)=Sz+c$ 时第二项为何消失；
3. 说明驻点处第二项为何消失；
4. 对

$$
f(x_1,x_2)=\frac12(x_1^2+x_2^2),
\qquad
\phi(z_1,z_2)=(z_1,e^{z_2}),
$$

在 $z=(0,0)$ 处分别用直接求导和变换公式计算 $H_{f\circ\phi}$；
5. 指出若错误地只保留 $J_\phi^\top H_fJ_\phi$ 会漏掉什么；
6. 解释为什么普通 Hessian 特征值不是一般非线性重参数化不变量。

## D 级：自动微分、验证与数值实验

### CALC-HC-D01：设计一套 HVP 三层验证实验

考虑

$$
f(x)=\sum_{i=1}^n\log(1+e^{a_i^\top x})
+\frac\lambda2\|x\|^2,
$$

其中 $a_i$ 固定。

1. 推导解析梯度、Hessian 和 HVP；
2. 写出不形成 Hessian 的解析 HVP；
3. 写 forward-over-reverse HVP 伪代码；
4. 设计梯度中心差分检查，扫描至少七个 $\varepsilon$；
5. 设计 $u^\top Hv\approx v^\top Hu$ 对称性检查；
6. 设计一阶/二阶 Taylor 残差缩放检查；
7. 说明预期误差曲线为什么先下降后上升；
8. 列出随机性、dtype、reduction、正则项和参数树方面的实验记录。

### CALC-HC-D02：高阶 AD 接口与模式审计

对一个标量神经网络损失 $L(\theta)$，比较：

1. `hessian(L)(theta)`；
2. `jvp(grad(L), (theta,), (v,))[1]`；
3. `grad(lambda t: vdot(grad(L)(t), v))(theta)`；
4. 用基向量重复调用 HVP；
5. 对参数 pytree/tuple 分别求二阶块。

要求：

- 标出每种方法形成的对象、时间/存储量级和典型使用场景；
- 解释 forward-over-reverse 与 reverse-over-reverse；
- 说明何时 $v$ 必须 `stop_gradient`/视为常量；
- 说明自定义 VJP/JVP、原地更新、随机层和算子覆盖如何破坏高阶微分；
- 设计一个小模型 full Hessian 与 HVP 一致性测试；
- 不得用“框架支持”替代实际 profiling。

### CALC-HC-D03：矩阵自由谱报告

你只有一个确定性曲率算子 `curv(v)`，可能是精确 Hessian、GGN 或 empirical Fisher。

设计一份实验，估计：

1. 最大代数特征值；
2. 最小代数特征值或负曲率证据；
3. trace 的 Hutchinson 估计与置信不确定性；
4. 阻尼系统 $(C+\lambda I)s=b$ 的残差；
5. 不同 batch 和随机种子下的波动。

报告必须包含：曲率对象定义、对称性检查、迭代算法、迭代次数、停止条件、随机 probe 分布、batch/reduction/正则、dtype、阻尼和残差。解释为什么只报告“最大特征值很大”不足以支持模型尖锐度结论。

## E 级：结构化推导与 AI 迁移

### CALC-HC-E01：Gauss–Newton 何时漏掉关键负曲率

设

$$
r(x,y)=
\begin{bmatrix}
x^2-1\\xy
\end{bmatrix},
\qquad
L(x,y)=\frac12\|r(x,y)\|^2.
$$

1. 求 $J_r$、$H_{r_1}$、$H_{r_2}$；
2. 写出精确 Hessian 分解

$$
H_L=J_r^\top J_r+r_1H_{r_1}+r_2H_{r_2};
$$

3. 在 $(0,0)$ 处计算精确 Hessian 与 GN，说明 GN 漏掉的负曲率；
4. 在根 $(1,0)$ 处计算二者并解释为何相等；
5. 找出一个非根点，定量比较 $v^\top H_Lv$ 与 $v^\top Gv$；
6. 说明“残差小”为什么只是 GN 合理性的一个条件而非完整保证；
7. 讨论阻尼 GN 与精确 Newton 在此例中的可能行为。

### CALC-HC-E02：矩阵变量最小二乘的 Hessian 算子

设

$$
f(X)=\frac12\|AXB-C\|_F^2,
$$

其中

$$
A\in\mathbb R^{r\times m},
\quad
X\in\mathbb R^{m\times n},
\quad
B\in\mathbb R^{n\times s}.
$$

1. 用微分和 Frobenius 配对推导梯度；
2. 推导 Hessian 作用 $\mathcal H_X[\Delta]$；
3. 证明自伴随性

$$
\langle U,\mathcal H[V]\rangle_F
=
\langle\mathcal H[U],V\rangle_F;
$$

4. 证明 $\mathcal H$ PSD；
5. 写出列优先 `vec` 下的 Kronecker 矩阵；
6. 给出严格正定的充要秩条件；
7. 设计不形成 Kronecker 矩阵的 HVP 和 CG 接口；
8. 说明 $A$ 或 $B$ 秩亏时有哪些零曲率方向。

### CALC-HC-E03：设计一份神经网络曲率审计报告

选择一个小型分类网络和固定数据子集，比较以下对象：

- 精确 Hessian HVP；
- GGN–vector product；
- 模型 Fisher 或明确命名的 empirical Fisher；
- 梯度平方的对角移动平均代理。

报告至少回答：

1. 四个对象的精确定义和期望/样本约定；
2. 哪些对象保证 PSD，哪些保留负曲率；
3. 怎样用相同向量比较四种曲率作用；
4. 怎样验证精确 HVP 和 GGN 作用；
5. 怎样估计极端特征值、trace 与阻尼逆作用；
6. batch、reduction、权重衰减和随机层如何控制；
7. 参数缩放或归一化改变 Hessian 谱时如何解释；
8. 如何审计“Adam 在近似 Hessian”这一说法的假设；
9. 哪些结论只能称为经验观察，哪些有解析保证；
10. 如何保证实验可复现、可证伪，而不是只展示支持预期的图。
