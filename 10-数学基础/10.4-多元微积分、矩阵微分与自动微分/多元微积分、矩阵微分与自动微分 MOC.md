---
type: moc
status: active
area: [math/calculus, math/matrix-calculus, ai/automatic-differentiation]
aliases: [微积分与自动微分 MOC, 矩阵微分 MOC, Automatic Differentiation MOC]
prerequisites: ["[[数学基础 MOC]]", "[[线性代数 MOC]]", "[[矩阵分析 MOC]]"]
related: ["[[数学基础完整课程地图与掌握标准]]", "[[练习与测验 MOC]]", "[[推导与实验 MOC]]"]
sources: ["OpenStax-Calculus-Volume-1", "OpenStax-Calculus-Volume-2-6.3", "OpenStax-Calculus-Volume-3-Chapter-4", "OpenStax-Calculus-Volume-3-4.4", "OpenStax-Calculus-Volume-3-4.6", "MIT-18.100A", "MIT-18.100B", "MIT-18.01SC", "MIT-18.02SC", "MIT-Calculus-Revisited-Gradient", "MIT-18.S096-Derivatives-Linear-Operators", "MIT-18.S096-General-Vector-Spaces", "MIT-18.S096-Jacobians-Matrix-Functions", "MIT-6.436J", "MIT-6.041SC", "TTU-Gateaux-Frechet-2025", "Axler-Riesz-6.42", "Boyd-Vandenberghe-Steepest-Descent", "Stanford-EE364A-Steepest", "JAX-JVP-Official", "JAX-JVP-VJP-Official", "JAX-JVP-API", "JAX-VJP-API", "JAX-Autodiff-Cookbook", "JAX-Checkpoint-Remat", "PyTorch-Func-Transforms", "PyTorch-Gradcheck-Official", "Baydin-2018-AD-Survey", "Griewank-Walther-Evaluating-Derivatives", "Pearlmutter-1994-HVP", "Su-3272-Cesaro", "Su-4187-Series-Approximation", "Su-8718-Smoothing", "Su-8757-Lipschitz-GAN", "Su-7469-Gradient-Clipping", "Su-7643-Taylor-Perturbation", "Su-7787-Finite-Learning-Rate", "Su-9070-LogSumExp", "Su-10958-JVP", "Su-2383-Determinant-Derivative", "Su-10366-Pseudoinverse", "Su-10592-Muon", "Su-11215-Manifold-Steepest"]
created: 2026-08-16
updated: 2026-08-27
---

# 多元微积分、矩阵微分与自动微分 MOC

> [!abstract] 本卷的核心任务
> 把“变化”变成可以计算、证明和实现的局部线性模型。课程从极限和连续性开始，依次建立一元导数、Taylor 余项、多元全微分、梯度/Jacobian/Hessian、链式法则与矩阵微分，最后解释自动微分系统真正传播的是 JVP、VJP 以及它们的复合。

## 一、范围与边界

### 本卷包含

- 标量、向量、矩阵和函数空间中的极限、连续性与局部线性化；
- 一元与多元微分、Taylor 余项、方向导数和 Fréchet 导数；
- 梯度、Jacobian、Hessian、JVP、VJP 与计算图；
- 矩阵变量的微分、迹技巧、隐式微分和谱分解求导；
- 前向、反向和高阶自动微分的数学对象、成本与失败边界；
- 与神经网络、隐式层、正规化流、二阶优化和可微分编程的接口。

### 本卷不替代

- 测度论、概率公理和期望收敛定理的完整证明：见后续 10.5；
- 凸性、KKT、收敛率和随机优化的系统理论：见后续 10.7；
- 浮点舍入、有限差分误差和求解器稳定性的完整分析：见[[数值线性代数 MOC]]；
- 一般 Banach/Fréchet 流形上的微分理论：见后续 10.10。

### 当前教学迁移路线

> [!important] 学习状态与材料迁移状态分开
> 下表只记录本轮“课程位置—问题链—贯穿例—公式七问—停靠线”是否完成。正文 frontmatter 与第三节中的 `draft` 仍表示学习者尚未完成闭卷、评分、订正和延迟迁移；`regression-passed` 不能把它升级为已掌握。

| 波次 | ID 范围 | 认知主线 | 材料迁移 |
|---|---|---|---|
| A | CALC-01—04 | 极限/连续 → 一元导数 → Taylor 余项 → 多元偏导/方向导数 | `regression-passed` |
| B | CALC-05—08 | 全微分 → 梯度几何 → Jacobian/JVP/VJP → Hessian 曲率 | `regression-passed` |
| C | CALC-09—12 | 链式法则/计算图 → 矩阵微分 → solve/隐式微分 → log-det | `regression-passed` |
| D | CALC-13—16 | 谱导数 → 逆/隐函数定理 → 换元积分 → 自动微分系统 | `regression-passed` |
| CUM | CALC-CUM-01 | 卷级口试—闭卷—随机三轨—盲干预—延迟门 | `regression-passed / not-attempted` |

首波固定使用

$$
\phi(t)=\log(1+e^t),
\qquad
F(x,y)=\log(e^x+e^y),
$$

贯通 Softplus 的尾部极限、Sigmoid 导数、二阶 Taylor 余项与二维 LogSumExp 的方向导数。

> [!tip] 第一波停靠线
> 完成 CALC-01—04 后，应能为 $\phi(1/n)\to\log2$ 构造完整的 $\varepsilon$–$N$ 证书；推出 $\phi'(0)=1/2$ 与 $\phi''(0)=1/4$；写出 $\phi(h)=\log2+h/2+h^2/8+R_2(h)$ 并证明 $|R_2(h)|\le|h|^3/24$；最后从一元切片推出 $D_vF(0,0)=(v_1+v_2)/2$，同时说明偏导、方向导数与统一全微分不是同一层结论。

第二波继续固定使用二维 LogSumExp，并把它的梯度写成 Softmax：

$$
F(x_1,x_2)=\log(e^{x_1}+e^{x_2}),
\qquad
p(x)=\nabla F(x)=\operatorname{softmax}(x).
$$

在原点，四篇节点共享同一组可核对对象：

$$
DF(0)[h]=\frac{h_1+h_2}{2},
\qquad
\nabla F(0)=\frac12\begin{bmatrix}1\\1\end{bmatrix},
\qquad
J_p(0)=H_F(0)=\frac14
\begin{bmatrix}
1&-1\\
-1&1
\end{bmatrix}.
$$

> [!tip] 第二波停靠线
> 完成 CALC-05—08 后，应能证明 $F(h)=\log2+DF(0)[h]+r(h)$ 且 $r(h)/\|h\|\to0$；解释 $DF(0)$ 是线性泛函而梯度是它在指定内积下的向量表示；分别写出 $J_p(0)v$ 与 $J_p(0)^Tu$，说明前者传播切向量、后者拉回协向量；最后用 $q_+=(1,1)^T/\sqrt2$、$q_-=(1,-1)^T/\sqrt2$ 验证 Hessian 在共同平移方向曲率为 $0$、在差异方向曲率为 $1/2$。还应明确：换范数会改变“最陡方向”，但不会改变同一个全微分。

第三波固定使用

$$
A(\theta)=
\begin{bmatrix}
2+\theta&1\\
1&2
\end{bmatrix},
\qquad
A(\theta)x(\theta)=
\begin{bmatrix}1\\0\end{bmatrix},
\qquad
L(\theta)=\frac12\|x(\theta)\|_2^2+\frac12\log\det A(\theta).
$$

它把共享矩阵 $A$ 上的两条计算分支接到一起：solve 分支贡献 $-10/27$，log-det 分支贡献 $9/27$，最终

$$
\frac{dL}{d\theta}\bigg|_{\theta=0}
=-\frac1{27}.
$$

先用下图回答一个视觉问题：**同一个复合损失的 primal、JVP 与 VJP，怎样沿相反方向传播却得到完全一致的参数导数？**

![[00-知识库管理/_assets/figures/calculus-ad/fig-solve-logdet-chain-v2.svg|920]]

> [!figure] 图 10.4-C｜第三波桥接图：primal、JVP 与 VJP 的同值验算
> A 展示共享矩阵上的 solve/log-det 分支；B 前推切向量并分别记录两条方向导数；C 解伴随系统，把两条矩阵协向量在 $A$ 处累加，最后与参数方向 $E_{11}$ 配对。来源：独立绘制；生成与精确断言：[[plot_calculus_operator_figures_v2.py]]；确定性有理数算例，无随机种子。

**怎样读图。** 第一遍按 A→B 顺序重算 primal 与 JVP；第二遍从损失反向读 C，并核对共享变量处的加法。图中三个 $-1/27$ 分别来自直接标量求导、JVP 和 VJP 配对，它们是三条独立证据，不是三种不同导数。

**适用边界。** 例中 $A_0$ 对称正定且 $\kappa_2(A_0)=3$，因此适合检查类型、转置和正负号，却没有模拟近奇异系统的数值困难；一般问题还必须报告前向残差、伴随残差和条件性。

> [!tip] 第三波停靠线
> 完成 CALC-09—12 后，应能画出 $\theta\to A\to(x,q;r)\to L$ 的分支计算图；从 $A\,dx=db-(dA)x$ 算出 $\dot x=(-4/9,2/9)^T$；用 $A^\top\lambda=x$ 得到 $\bar A_{\mathrm{solve}}=-\lambda x^\top$；从 $d\log\det A=\operatorname{tr}(A^{-1}dA)$ 得到 $\bar A_{\log\det}=A^{-\top}/2$；最后说明为何两条贡献在 $A$ 处相加，并用 Frobenius 配对恢复 $dL/d\theta=-1/27$。还应能指出 $\theta\downarrow-3/2$ 时 solve 与 log-det 同时逼近奇异边界。

第四波固定使用

$$
T_\tau
=R_\tau\operatorname{diag}(2e^\tau,1),
\qquad
A_\tau=T_\tau T_\tau^\top,
\qquad
x=T_\tau z,\quad z\sim\mathcal N(0,I_2).
$$

在 $\tau=0$，有

$$
A_0=\operatorname{diag}(4,1),
\qquad
\dot A_0=
\begin{bmatrix}8&3\\3&0\end{bmatrix},
\qquad
\dot\lambda_1=8,\quad \dot u_1=e_2.
$$

对固定观测 $x_*=(1,2)^T$，换元后的负对数似然满足

$$
\ell'(0)=-\frac34,
$$

而 forward 与 reverse AD 必须复现同一个数。另一方面，在 $\tau_*=-\log2$，

$$
A_{\tau_*}=I,
\qquad
T_{\tau_*}=R_{\tau_*}.
$$

特征基此时不唯一，但底层映射仍是条件数为 $1$ 的全局微分同胚。

先用下图回答一个视觉问题：**谱坐标失效、Jacobian 奇异和程序求导规则失败，为什么是三类不能混为一谈的问题？**

![[00-知识库管理/_assets/figures/calculus-ad/fig-spectral-flow-ad-chain-v2.svg|920]]

> [!figure] 图 10.4-D｜第四波桥接图：谱对象、可逆换元与程序导数
> A 分离简单谱导数与重谱基退化；B 说明同一个 $T_\tau$ 仍保持正 determinant，并把标准 Gaussian 推到数据空间；C 用只含光滑原语的程序得到相同 JVP/VJP，同时标出“绕道任意重谱特征基”会改变程序可微性。来源：独立绘制；生成与精确断言：[[plot_calculus_operator_figures_v2.py]]；确定性解析算例，无随机种子。

**怎样读图。** 先在 A 中问失效的是谱值、单个基还是整个子空间；再到 B 检查真正控制逆映射与换元的是 $\det T_\tau$ 和最小奇异值；最后在 C 比较直接光滑程序与经 eigendecomposition 改写的程序。函数相同不保证任意中间表示具有同样良好的导数规则。

**适用边界。** 本例的 $T_\tau$ 是全局可逆线性映射，因此比一般非线性 flow 简单；它用于隔离三类失败对象，而不证明任意局部非奇异网络都是全局双射，也不覆盖非单射、维数变化或随机离散程序。

> [!tip] 第四波停靠线
> 完成 CALC-13—16 后，应能从 $\dot A_0$ 推出 $\dot\lambda_1=8$ 与 $\dot u_1=e_2$；由 $\det T_\tau=2e^\tau>0$ 区分局部逆定理与本例的全局线性可逆；从 $x=T_\tau z$ 写出密度换元并算得 $\ell'(0)=-3/4$；再用逐原语 forward/reverse trace 复现该导数。最后必须能解释：$\tau=-\log2$ 破坏的是逐列谱基，而不是 $T_\tau$、概率密度或直接程序本身。

> [!success] 10.4 材料迁移完成
> CALC-01—16 与 CALC-CUM 的初学者入口、问题链、贯穿例、公式解释、图文单元和回归门均已完成。各正文保持 `draft`，表示学习者仍需完成闭卷作答、订正和延迟复做；材料 `regression-passed` 只说明课程资产通过静态与计算验收。

## 二、依赖总图

~~~mermaid
flowchart LR
    L["CALC-01 极限、连续性与收敛"] --> D["CALC-02 一元导数"]
    D --> T["CALC-03 Taylor 与余项"]
    L --> P["CALC-04 偏导与方向导数"]
    P --> F["CALC-05 Fréchet 导数"]
    F --> G["CALC-06 梯度与最陡方向"]
    F --> J["CALC-07 Jacobian / JVP / VJP"]
    F --> H["CALC-08 Hessian 与曲率"]
    J --> C["CALC-09 链式法则与计算图"]
    C --> M["CALC-10 矩阵微分与迹技巧"]
    M --> I["CALC-11/12 隐式、逆与 log-det"]
    M --> S["CALC-13 谱分解的导数"]
    F --> IF["CALC-14 逆/隐函数定理"]
    C --> V["CALC-15 换元与积分变换"]
    C --> AD["CALC-16 自动微分"]
    J --> AD
    H --> AD
~~~

> [!note] 读图说明
> 箭头表示主要认知依赖，不表示只能按单一路线学习。CALC-04 可以在一元 Taylor 后半并行预习；CALC-11—15 可分任务并行，但 CALC-16 必须能熟练区分导数算子、JVP 和 VJP 后再验收。

## 三、16 个核心节点

| ID | 节点 | 本章必须回答的问题 | 状态 |
|---|---|---|---|
| CALC-01 | [[函数极限、连续性与收敛模式]] | “越来越接近”究竟由哪些量词、度量和概率声明定义？ | draft |
| CALC-02 | [[一元导数与中值定理]] | 局部变化率怎样控制有限区间误差？ | draft |
| CALC-03 | [[Taylor 展开与余项]] | 局部多项式近似何时可靠，余项怎样定量？ | draft |
| CALC-04 | [[多元函数、偏导数与方向导数]] | 多个输入方向如何分别变化，为什么偏导存在仍可能不可微？ | draft |
| CALC-05 | [[全微分与 Fréchet 导数]] | 最佳线性近似如何统一标量、向量和矩阵导数？ | draft |
| CALC-06 | [[梯度、方向导数与最陡方向]] | 梯度为何依赖内积，“最陡”需要什么度量？ | draft |
| CALC-07 | [[Jacobian、JVP 与 VJP]] | 完整 Jacobian、前向作用和反向作用有什么形状/成本差异？ | draft |
| CALC-08 | [[Hessian、二阶微分与曲率]] | 二阶局部模型怎样编码方向曲率与病态性？ | draft |
| CALC-09 | [[多元链式法则与计算图]] | 局部线性映射如何按计算图顺序复合？ | draft |
| CALC-10 | [[矩阵微分、迹技巧与布局约定]] | 矩阵导数怎样避免转置、布局与分母/分子约定冲突？ | draft |
| CALC-11 | [[逆矩阵、线性求解与隐式微分]] | 不显式求逆时怎样稳定传播解的导数？ | draft |
| CALC-12 | [[行列式、log-det 与迹的导数]] | 体积、Gaussian likelihood 与 flow Jacobian 的导数从何而来？ | draft |
| CALC-13 | [[特征值、特征向量与 SVD 的导数]] | 简单谱、重复谱、子空间和次梯度怎样分层？ | draft |
| CALC-14 | [[逆函数定理与隐函数定理]] | 局部可逆和隐式解的存在唯一性由哪个 Jacobian 保证？ | draft |
| CALC-15 | [[多重积分、换元公式与积分变换]] | 密度与期望在变量变换后为什么出现 Jacobian determinant？ | draft |
| CALC-16 | [[自动微分：前向、反向与高阶模式]] | AD 计算什么、保存什么、为什么不等于符号微分或有限差分？ | draft |

## 四、四阶段学习路线

### 阶段 A：极限与局部线性化

1. [[函数极限、连续性与收敛模式]]；
2. [[一元导数与中值定理]]；
3. [[Taylor 展开与余项]]；
4. [[多元函数、偏导数与方向导数]]；
5. [[全微分与 Fréchet 导数]]。

阶段验收：能从量词定义证明一个极限，能给出偏导存在但不可微的反例，并能把 $o(\|h\|)$ 与普通“小量”区分开。

### 阶段 B：一阶与二阶算子

6. [[梯度、方向导数与最陡方向]]；
7. [[Jacobian、JVP 与 VJP]]；
8. [[Hessian、二阶微分与曲率]]；
9. [[多元链式法则与计算图]]；
10. [[矩阵微分、迹技巧与布局约定]]。

阶段验收：面对任意输入/输出形状，先写导数作为线性映射，再选择是否物化 Jacobian；能手工完成一张小计算图的 JVP 与 VJP。

### 阶段 C：结构化函数与隐式对象

11. [[逆矩阵、线性求解与隐式微分]]；
12. [[行列式、log-det 与迹的导数]]；
13. [[特征值、特征向量与 SVD 的导数]]；
14. [[逆函数定理与隐函数定理]]；
15. [[多重积分、换元公式与积分变换]]。

阶段验收：能把矩阵求解、谱分解和变量换元的导数写成明确的线性方程或伴随问题，并指出秩亏、重根和 Jacobian 奇异时结论在哪一步失效。

### 阶段 D：自动微分系统

16. [[自动微分：前向、反向与高阶模式]]。

阶段验收：能依据输入/输出维数选择 forward/reverse mode，解释 checkpointing、stop-gradient、in-place、控制流和高阶导数的数学与系统边界。

## 五、必须维持的五个区分

| 容易混淆的对象 | 正确区分 |
|---|---|
| 极限存在 vs 数值上看起来稳定 | 前者是无限尾部量词，后者只是有限样本证据 |
| 方向导数 vs Fréchet 可微 | 所有方向极限存在仍可能没有统一线性余项 |
| 导数线性映射 vs 某个 Jacobian 矩阵 | 矩阵是选择坐标后的表示，JVP/VJP 可不物化它 |
| 数学导数 vs 数值求导 | AD 按程序链式法则给导数；有限差分还含截断和舍入误差 |
| 梯度 vs 微分 | 微分属于对偶空间；梯度由内积把它表示为向量 |

## 六、AI 调用地图

| AI 场景 | 本卷真正被调用的对象 | 主要失败边界 |
|---|---|---|
| 反向传播 | 逐层 VJP 与链式法则 | 形状、广播、不可微点、数值溢出 |
| 梯度检查 | Taylor 余项与有限差分 | 步长过大有截断误差，过小有舍入消去 |
| 隐式层/优化层 | 线性求解与隐函数定理 | Jacobian 奇异、迭代未收敛、反向求解不稳定 |
| 白化、谱层与矩阵优化器 | 矩阵函数、SVD/eig 的 Fréchet 导数 | 重根、谱间隙消失、秩变化 |
| 正规化流 | 多元换元和 log-det | 映射非双射、Jacobian 奇异、log-det 成本 |
| 大模型训练 | VJP、checkpointing 与混合精度 | 内存、随机控制流、低精度累积、梯度缩放 |
| 统计学习 | 函数列的一致收敛与随机收敛 | 只证明逐参数收敛却对训练后参数作结论 |

## 七、当前稳定结论与缺口

| 节点 | 已建立 | 仍需验收 |
|---|---|---|
| [[函数极限、连续性与收敛模式]] | 数列/函数极限、连续/一致连续、逐点/一致/$L^p$、a.s./概率/$L^p$/分布收敛及 AI 接口 | 学习者闭卷证明、重做反例和跨统计/优化迁移 |
| [[一元导数与中值定理]] | 差商与局部线性、可微边界、求导规则、Fermat/Rolle/Lagrange/Cauchy/Darboux、有限差分与 AI 接口 | 学习者闭卷重建证明、反例复现和梯度检查实作 |
| [[Taylor 展开与余项]] | 唯一局部多项式、Peano/Lagrange/Cauchy/积分余项、解析性反例、误差预算、下降引理、差分/噪声/logsumexp 接口 | 学习者闭卷重建重复 Rolle 证明、误差证书与 AI 声明审计 |
| [[多元函数、偏导数与方向导数]] | 多元极限与路径、偏导/方向导数/全微分层级、连续偏导充分条件、混合偏导、JVP 与随机方向检查 | 学习者闭卷重建三层反例、统一界证明与自动微分声明审计 |
| [[全微分与 Fréchet 导数]] | 有界线性导数、统一小 o 余项、唯一性/连续性、Gâteaux/Hadamard/Fréchet 层级、双线性与矩阵乘法、JVP 和局部条件性 | 学习者闭卷重建两层反例、双线性余项证明、形状审计与导数验证协议 |
| [[梯度、方向导数与最陡方向]] | 微分/梯度类型、Riesz 表示、加权度量、对偶范数、$\ell_p$ 与矩阵最陡方向、坐标变换、SignSGD/FGSM/Muon 几何 | 学习者闭卷重建 Riesz/Hölder/SVD 对偶证明、完成坐标与 AI 一阶几何审计 |
| [[Jacobian、JVP 与 VJP]] | 导数算子/坐标表/JVP/VJP 类型、对偶与加权伴随、列/行构造成本、批量线性层、矩阵自由作用和三层验证协议 | 学习者闭卷重建对偶回拉与坐标变换、完成 batch/广播/API 审计和代码复现 |
| [[Hessian、二阶微分与曲率]] | 二阶 Fréchet 双线性型、Hessian 对称与 Taylor 曲率、谱/凸性、HVP、重参数化、GN/GGN/Fisher 分工和三层验证 | 学习者闭卷重建二阶余项与坐标变换、完成 HVP/谱/曲率近似实验和 AI 报告 |
| [[多元链式法则与计算图]] | Fréchet 余项证明、Jacobian/JVP/VJP 复合、DAG 动态规划、分支/广播/共享参数、二阶复合与深层稳定性 | 学习者闭卷重建证明、手算反向图并完成真实框架梯度审计 |
| [[矩阵微分、迹技巧与布局约定]] | Frobenius 配对、微分/梯度类型、迹循环边界、双侧最小二乘、二次迹、JVP/VJP、vec 布局、结构化变量与 batch/广播 | 学习者闭卷重建一般二次迹与受约束梯度，完成非方阵伴随测试和真实线性层审计 |
| [[逆矩阵、线性求解与隐式微分]] | 一般隐式切向/伴随、线性 solve 与 inverse 导数、多右端、固定点、优化/KKT 层、展开反传差异、残差/条件与矩阵自由求解 | 学习者闭卷重建伴随模板，比较有限迭代/隐式梯度并报告前向与反向误差 |
| [[行列式、log-det 与迹的导数]] | adjugate/Jacobi 两层公式、奇异秩边界、稳定 logabsdet、trace 函数、Gaussian、flow、低秩更新与随机迹估计 | 学习者闭卷完成三路推导，复现 Cholesky/Gaussian/flow 计算并审计近奇异行为 |
| [[特征值、特征向量与 SVD 的导数]] | 对称简单谱、非正规左右向量、重复谱方向分裂、谱投影、SVD 旋转方程、次梯度、PCA/白化/谱归一化审计 | 学习者闭卷重建特征/SVD 导数，完成 gap 扫描、规范对齐和子空间不变性实验 |
| [[逆函数定理与隐函数定理]] | 局部逆存在/正则性、压缩证明骨架、隐函数块构造、水平集切空间、条件半径、flow/DEQ/KKT 局部与全局边界 | 学习者闭卷陈述并重建证明，完成分支、最小奇异值和全局可逆声明审计 |
| [[多重积分、换元公式与积分变换]] | Riemann/Fubini/Tonelli、线性与非线性换元、极/球坐标、Gaussian、密度推前、flow、重参数化与维数改变 | 学习者闭卷推导 Gaussian/flow 公式，完成非单射、支持集与微分—积分交换审计 |
| [[自动微分：前向、反向与高阶模式]] | 双数与 Wengert list、JVP/VJP、forward/reverse 成本、tape/checkpoint、高阶组合、程序语义、自定义规则、隐式梯度与四层验证 | 学习者闭卷手算 JVP/VJP/HVP，复现 checkpoint 与伴随测试，并审计控制流、随机性、归约尺度和高阶可组合性 |

## 八、卷级累计验收

| 验收件 | 覆盖与作用 | 当前状态 |
|---|---|---|
| [[阶段测验 - 多元微积分、矩阵微分与自动微分（10.4）]] | 20分钟口试 + 270分钟、100分A—E闭卷，覆盖CALC-01—16 | `regression-passed / not-attempted` |
| [[阶段测验解答 - 多元微积分、矩阵微分与自动微分（10.4）]] | 完整证明、口试红线、传播手算、反例与程序审计 | `sealed until first attempt` |
| [[实验 - 微积分、矩阵微分与自动微分累计复现门]] | `attempt_id + scorer nonce`随机指定Taylor/FD、JVP/VJP/HVP或implicit/spectral轨；含盲参数干预 | `regression-passed / not-attempted` |
| [[calculus_ad_cumulative_contract_audit.py]] | 题—解隔离、四波解析模型、状态表面、Wiki链接、累计SVG与canonical双跑 | `regression-passed` |

### 卷末证据时间线

```mermaid
flowchart LR
    O["20分钟无提示口试"] --> W["270分钟闭卷"]
    W --> F["冻结原稿与首错"]
    F --> N["scorer nonce随机轨"]
    N --> B["盲参数预测/干预"]
    B --> S["详解订正"]
    S --> R48["48小时换机制"]
    R48 --> R14["14天陌生程序迁移"]
```

累计卷不以框架API记忆代替数学对象，也不以finite difference代替证明。材料回归通过只表示验收链可执行；在口试、闭卷、随机轨、盲干预、48小时重建和14天迁移全部完成前，CALC-01—16保持`draft / not-attempted`。

### 四波统一模型族与三条证明主链

| 四波模型族 | 贯穿节点 | 必须反复重建的链 |
|---|---|---|
| $\phi(t)=\log(1+e^t)$、$F(x,y)=\log(e^x+e^y)$ | CALC-01—04 | 量词极限→一元导数→Taylor余项→多元方向/统一可微 |
| $F$与$p=\nabla F=\operatorname{softmax}$ | CALC-05—08 | Fréchet算子→metric表示→JVP/VJP→Hessian方向曲率 |
| 共享$A(\theta)$的solve/log-det图 | CALC-09—12 | primal DAG→matrix differential→tangent/adjoint→共享cotangent累加 |
| $T_\tau$、$A_\tau=T_\tau T_\tau^T$与Gaussian换元 | CALC-13—16 | simple谱→local/global可逆→density change→逐原语AD语义 |

三条跨波证明主链是：`统一局部余项`决定可微性与Taylor；`operator composition / adjoint`决定JVP、VJP与HVP；`invertibility / gap / branch`决定隐式、谱和换元公式的适用域。任何实验曲线都只能审计这些合同，不能替代它们。

## 九、来源与证据分工

- OpenStax *Calculus Volume 1*：初学者极限与连续性的课程入口；
- MIT 18.100B Real Analysis：数列、度量空间、逐点/一致收敛以及交换极限的严格主线；
- MIT 6.436J/6.041SC：随机变量收敛模式与反例；
- OpenStax 与 MIT 18.01SC/18.100A：一元导数、中值定理、证明链与假设边界；
- OpenStax *Calculus Volume 2* 与 MIT 18.100A/18.100B：Taylor 多项式、Peano/Lagrange/积分余项、误差界和解析性边界；
- OpenStax *Calculus Volume 3* 与 MIT 18.02SC：多元函数、路径极限、偏导、方向导数和连续偏导充分条件；
- OpenStax §4.4、MIT 18.S096 与 TTU 应用分析讲义：全微分、导数线性算子、Gâteaux/Fréchet 层级与函数空间入口；
- OpenStax §4.6 与 MIT *Calculus Revisited*：方向导数、欧氏梯度和最陡方向的本科教学入口；
- Axler 的 Riesz 表示与 Boyd/Stanford 的对偶范数、最陡下降材料：微分—梯度类型和一般范数几何的规范证据；
- MIT 18.S096、JAX/PyTorch 官方文档与 JMLR AD 综述：Jacobian 线性算子表示、JVP/VJP、forward/reverse mode、当前 API 与成本边界；
- MIT 18.S096、Boyd、Pearlmutter、JAX/PyTorch 与 JMLR natural-gradient 综述：二阶双线性型、Hessian/凸性、HVP、GGN/Fisher 的理论与接口边界；
- JAX/PyTorch 官方 gradcheck 文档：方向有限差分、形状和软件验证语义；
- 科学空间：Cesàro 平均、一致逼近、ReLU 光滑化、Lipschitz/梯度训练与 AI 问题入口，不承担一般分析定理的唯一证据；
- 科学空间的参数扰动、有限学习率与 logsumexp 文章为 Taylor 的 AI 问题入口，不替代余项定理的教材证据；
- 科学空间的扩散速度场 JVP 与训练梯度文章承担多元方向变化的 AI 问题入口；
- 科学空间的行列式与低秩近似文章承担矩阵变量一阶展开的问题入口，不替代统一余项定理；
- Magnus–Neudecker、MIT 18.S096 与 Matrix Cookbook 交叉承担矩阵微分、vec/布局和公式核对；公式表不替代类型、假设和证明；
- 隐函数定理、数值线性代数与 DEQ/模块化隐式微分文献共同承担 solve、fixed point、argmin/KKT 的正则性和求解误差边界；
- 科学空间《行列式的导数》提供余子式与 $\det(I+tA)$ 的问题入口，Jacobi 通式、奇异点、稳定 log-det、Gaussian 与 flow 由教材和原始论文补齐；
- 科学空间《SVD的导数》提供矩阵恒等式微分入口；Davis–Kahan、Wedin、矩阵扰动和谱函数教材负责 gap、重谱、子空间与非正规边界；
- Spivak、Rudin、Krantz–Parks 与流形教材承担逆/隐函数的局部存在唯一、证明骨架和水平集几何；数值求解稳定性继续与 NLA 分卷交叉验证；
- OpenStax、Spivak 与实分析教材承担多重积分、Fubini/Tonelli 和换元定理；Real NVP/Glow 等论文承担 flow 的结构化 Jacobian 应用；
- 科学空间的 Muon 与流形最陡下降文章承担矩阵参数几何的问题入口，不替代 Riesz/对偶范数定理或离散收敛证明；
- Baydin 等的 JMLR 综述、Griewank–Walther、Pearlmutter 以及 JAX/PyTorch 官方文档共同承担自动微分的历史、累积模式、高阶组合、checkpoint 和当前实现语义；科学空间材料继续只承担 AI 问题入口，不替代这些系统证据。

## 十、下一步

CALC-01—16 已全部建立正文、视觉与 A–E 训练材料，10.4 因而达到 **16/16 正文覆盖**。卷级题卷、独立详解、随机三轨累计复现门和[[calculus_ad_cumulative_contract_audit.py]]已组成“口试—闭卷—随机轨—盲干预—48小时—14天”闭环，材料状态为`regression-passed`。所有节点仍保持`draft / not-attempted`：下一阶段进入[[概率论与数理统计 MOC]]；不能因文件齐全直接升级个人状态。

### 2026-08-23 图像标准化验收

- CALC-01—16 共 16 个节点已全部迁移为 v2 教材图；
- 16/16 使用根目录稳定路径、明确显示宽度、引图问题、标准图注、读图说明与适用边界；
- 16/16 生成脚本可重复运行，SVG 结构、XML 与 1200 px 渲染已通过；
- 章内旧版图引用与相对图片路径均为 0；本结论仅表示图像迁移通过，不改变节点的学习验收 `draft` 状态。
