---
type: concept
status: draft
area: [math/numerical-linear-algebra, math/krylov-methods]
aliases: [Arnoldi 迭代, Arnoldi 正交化]
prerequisites: ["[[Lanczos 方法]]", "[[Hessenberg 化与 QR 特征值算法]]", "[[标准正交基与 Gram-Schmidt]]", "[[Schur 分解]]", "[[矩阵扰动]]"]
related: ["[[非正规矩阵、预解式与伪谱]]", "[[矩阵函数与矩阵指数]]", "[[SVD 算法与谱范数估计]]", "[[数值线性代数 MOC]]", "[[实验 - Arnoldi 非正规性、重正交与重启]]"]
sources: ["[[S-2023-Demmel-Krylov-Arnoldi-Lanczos]]", "[[S-2000-Netlib-Krylov-Eigensolver-Templates]]", "[[S-2002-Higham-数值算法准确性与稳定性]]"]
exercises: ["[[习题 - Arnoldi 方法]]"]
solutions: ["[[解答 - Arnoldi 方法]]"]
created: 2026-08-15
updated: 2026-08-27
---

# Arnoldi 方法

> [!abstract] 本章主问题
> Arnoldi 用矩阵—向量乘与逐步正交化，为一般方阵的 Krylov 子空间建立标准正交基，并把大算子压缩为小型上 Hessenberg 矩阵；它是非对称特征求解、GMRES 与 Krylov 矩阵函数的共同骨架，但非正规性、全历史正交成本和重启信息损失使“算出一个 Ritz 值”远非完整验收。

先用下图回答一个视觉问题：**一般矩阵为何需要长递推，Ritz residual 能证明什么，而重启必须保留什么信息？**

![[00-知识库管理/_assets/figures/numerical-analysis/fig-arnoldi-restart-nonnormal-v2.svg|880]]

> [!figure] 图 10.8.13｜Arnoldi 长递推、Ritz residual 与重启信息保留
> A 表示第 $j$ 步的 $Aq_j$ 必须投影掉全部已有 $q_1,\ldots,q_j$，从而形成上 Hessenberg $H_k$ 与 Arnoldi 关系；B 从 $H_ky=\theta y$ 构造 $u=Q_ky$，再由最后一项给出廉价 Ritz residual，同时区分正规矩阵的谱隙解释与非正规矩阵的条件数/伪谱解释；C 串联扩展、正交性检查、wanted Schur/Ritz 选择和锁定/重启。来源：独立绘制；理论接口参考 Demmel、Netlib Krylov Templates 与 Higham；生成脚本：[[plot_numerical_iterative_methods_v2.py]]；确定性结构示意，无随机种子。

**怎样读图。** 先沿 A 从 $w=Aq_j$ 读到“对所有旧基正交化”，这解释一般 Arnoldi 为何不是 Lanczos 三项递推；再由 B 把小矩阵 Ritz 对提升回原空间，并用 $\|Au-\theta u\|=|h_{k+1,k}e_k^Ty|$ 验收；最后读 C，把内存上限 $m$ 看成一次信息压缩：重启应保留目标不变子空间的 Schur/Ritz 信息，并继续报告 true residual、$\|Q^*Q-I\|$ 与 matvec 数。

**适用边界（图没有证明什么）。** 图不证明小 residual 必然对应小特征值误差；对强非正规矩阵，伪谱、左右特征向量条件性和暂态都可能主导解释。流程也省略 block、harmonic Ritz、shift–invert 与具体 implicit/thick restart 变体。一次或两次 MGS 的选择应由正交性监测、精度和通信成本决定，不能从示意图直接固定。

## 一、学习目标

完成本章后，你应能：

1. 从 Krylov 幂序列推导 Arnoldi 正交化；
2. 写出 $AQ_k=Q_kH_k+h_{k+1,k}q_{k+1}e_k^T$ 并解释上 Hessenberg 结构；
3. 手算一个非正规 $3\times3$ 例子；
4. 推导一般 Ritz 残差公式与 Galerkin 条件；
5. 区分 Ritz、Schur、harmonic Ritz 与 shift-and-invert 目标；
6. 解释非正规矩阵上谱、伪谱、特征向量条件数和暂态的角色；
7. 比较 MGS、二次正交、重启、锁定和块方法的成本；
8. 为 Jacobian、转移算子、注意力线性化和矩阵函数任务给出可验收契约。

> [!question] 初学者读完必须能回答
> 1. 为什么一般矩阵的 $Aq_j$ 必须与全部旧基向量正交化？
> 2. Arnoldi 关系为何产生上 Hessenberg 而非三对角投影？
> 3. Ritz residual 公式怎样从最后一个 Arnoldi 项导出？
> 4. 为什么非正规矩阵上小 residual 不保证小特征值误差？
> 5. MGS 重正交与 $\|Q_k^*Q_k-I\|$ 监测怎样配合？
> 6. Restart 为什么可能擦除已经形成的谱过滤信息？
> 7. Wanted Schur/Ritz vectors、locking 与 true residual 如何组成可靠重启契约？

> [!note] 课程位置
> NUM-12 的 Lanczos 依靠对称性把正交化压缩为三项递推；本章删除 $A=A^T$ 这一条假设，观察“只与最近两个向量打交道”为何立刻失效。这里形成的一般 Arnoldi 基既服务非对称特征问题，也会在 NUM-16 中成为 FOM/GMRES 的投影骨架。

> [!tip] 建议两遍阅读
> 第一遍只跟随下面的 $3\times3$ 非正规矩阵，手算两次 matvec、$\bar H_2$、两个 Ritz residual 和第三步 breakdown；第二遍再进入伪谱、左右特征向量、harmonic Ritz、重正交与 restart。第一遍的目标不是背伪代码，而是亲眼看见“大矩阵作用—全历史正交化—小 Hessenberg—高维 residual”怎样闭环。

## 本章的推导问题链

1. 从 $q_1,Aq_1,A^2q_1,\ldots$ 出发，为什么必须把新向量对全部旧基正交化？
2. 第 $j$ 次 matvec 为什么只可能在 $H$ 的第 $j+1$ 行产生一个新非零元？
3. 两步 Arnoldi 怎样把三维非正规矩阵压缩为 $2\times2$ Hessenberg？
4. 小矩阵 eigenpair 怎样提升成原空间中的 Ritz pair？
5. 为什么一个 Ritz value 恰好等于真特征值，仍可能配着很大的 Ritz residual？
6. 第三步 residual 为零为什么表示 Krylov 空间已经不变，而不是算法失败？
7. 精确关系进入浮点后，正交性、非正规性和 restart 分别会破坏哪一层承诺？

## 贯穿算例：一个矩阵同时暴露非正规谱与长递推

第四波固定

$$
A=
\begin{bmatrix}
1&2&0\\
0&1&0\\
0&0&3
\end{bmatrix},
\qquad
q_1=\frac1{\sqrt3}(1,1,1)^T.
$$

$A$ 的特征值为 $1,1,3$，但左上 $2\times2$ 块是非平凡 Jordan block，所以 $A$ 非正规且不可对角化。后续 NUM-14 会计算同一 $A$ 的奇异值，NUM-15 会用它构造收敛但暂态放大的 Richardson 迭代，NUM-16 则研究 $H=A^TA$ 的预条件 Krylov 求解。

### 符号与对象账本

| 对象 | 定义 | 本例中的作用 |
|---|---|---|
| $\mathcal K_k(A,q_1)$ | $\operatorname{span}\{q_1,Aq_1,\ldots,A^{k-1}q_1\}$ | 只靠 matvec 逐步扩张的空间 |
| $Q_k$ | $[q_1,\ldots,q_k]$ | Krylov 空间的标准正交基 |
| $h_{ij}$ | $q_i^TAq_j$ | 第 $j$ 次正交化的投影系数 |
| $\bar H_k$ | $(k+1)\times k$ 上 Hessenberg 矩阵 | 记录 $AQ_k=Q_{k+1}\bar H_k$ |
| $H_k$ | $Q_k^TAQ_k$ | $k\times k$ Rayleigh–Ritz 投影 |
| $(\theta,y)$ | $H_ky=\theta y$ | 小空间 eigenpair |
| $u=Q_ky$ | Ritz vector | 提升回原空间的候选方向 |
| $r=Au-\theta u$ | Ritz residual | 候选 eigenpair 的后验证书 |

### 第一步：一个 matvec 生成第一列 Hessenberg 系数

先算

$$
Aq_1=\frac1{\sqrt3}(3,1,3)^T,
\qquad
h_{11}=q_1^TAq_1=\frac73.
$$

减去已有方向：

$$
w_1=Aq_1-h_{11}q_1
=\frac1{3\sqrt3}(2,-4,2)^T.
$$

因此

$$
h_{21}=\|w_1\|_2=\frac{2\sqrt2}{3},
\qquad
q_2=\frac{w_1}{h_{21}}
=\frac1{\sqrt6}(1,-2,1)^T.
$$

这里已经可以检查 $q_1^Tq_2=0$。第一列关系为

$$
Aq_1=\frac73q_1+\frac{2\sqrt2}{3}q_2.
$$

### 第二步：一般矩阵必须重新投影到所有旧方向

第二次 matvec 为

$$
Aq_2=\frac1{\sqrt6}(-3,-2,3)^T.
$$

依次减去 $q_1,q_2$ 分量：

$$
h_{12}=q_1^TAq_2=-\frac{\sqrt2}{3},
\qquad
h_{22}=q_2^TAq_2=\frac23.
$$

剩余量恰为

$$
w_2=Aq_2-h_{12}q_1-h_{22}q_2
=\frac1{\sqrt6}(-3,0,3)^T.
$$

所以

$$
h_{32}=\sqrt3,
\qquad
q_3=\frac1{\sqrt2}(-1,0,1)^T.
$$

两步 Arnoldi 关系现在完全可见：

$$
AQ_2=Q_3\bar H_2,
\qquad
\bar H_2=
\begin{bmatrix}
7/3&-\sqrt2/3\\
2\sqrt2/3&2/3\\
0&\sqrt3
\end{bmatrix},
$$

而 Rayleigh–Ritz 使用前两行

$$
H_2=
\begin{bmatrix}
7/3&-\sqrt2/3\\
2\sqrt2/3&2/3
\end{bmatrix}.
$$

上 Hessenberg 的含义只是 $h_{ij}=0$ 当 $i>j+1$；它既不要求 $H_2$ 对称，也不保证 Ritz values 落在实谱区间内。

### 第三步：Ritz value 必须与 Ritz residual 一起读

$H_2$ 的 trace 为 $3$、determinant 为 $2$，所以 Ritz values 恰为

$$
\theta_1=1,
\qquad
\theta_2=2.
$$

对 $\theta_1=1$，可取单位小 eigenvector

$$
y_1=\frac13(1,2\sqrt2)^T.
$$

Arnoldi residual 公式给出

$$
\|Au_1-\theta_1u_1\|_2
=h_{32}|e_2^Ty_1|
=\sqrt3\frac{2\sqrt2}{3}
=\frac{2\sqrt6}{3}.
$$

注意：$\theta_1=1$ 虽然恰好是真特征值，提升向量 $u_1=Q_2y_1$ 却远不是合格 eigenvector。对 $\theta_2=2$，取 $y_2=(\sqrt2,1)^T/\sqrt3$，residual 仍为 $1$。这正是“只看 Ritz value 的小数位”会失败的最小反例。

### 第四步：全空间闭合产生精确 breakdown

加入 $q_3$ 后，$Q_3=[q_1,q_2,q_3]$ 已是 $\mathbb R^3$ 的正交基，并有

$$
H_3=Q_3^TAQ_3=
\begin{bmatrix}
7/3&-\sqrt2/3&\sqrt6/3\\
2\sqrt2/3&2/3&\sqrt3/3\\
0&\sqrt3&2
\end{bmatrix}.
$$

$H_3$ 与 $A$ 正交相似，故特征值精确为 $1,1,3$；下一正交 residual 为零，即 $h_{4,3}=0$。有限维模型中的这次 breakdown 表示 Krylov 空间已成为不变子空间。

### 核心公式七问：$\|Au-\theta u\|_2=|h_{k+1,k}e_k^Ty|$

1. **公式从哪来？** 把 $u=Q_ky$ 和 $H_ky=\theta y$ 代入 Arnoldi 分解，$Q_kH_ky-\theta Q_ky$ 完全抵消。
2. **为什么只剩一个方向？** $AQ_k$ 超出 $\operatorname{range}(Q_k)$ 的部分只在最后一列，方向是 $q_{k+1}$。
3. **为什么计算便宜？** $h_{k+1,k}$ 已由正交化得到，$e_k^Ty$ 只是小 eigenvector 的末分量。
4. **Residual 小保证什么？** 它给出候选特征对的后向误差；非正规矩阵的特征值/向量前向误差还取决于左右几何与伪谱。
5. **为何要直接 residual 抽查？** 浮点正交缺陷、restart 变换和递推舍入会使廉价等式逐渐偏离真实 $Au-\theta u$。
6. **Breakdown 怎样分类？** 真正的 $h_{k+1,k}=0$ 表示不变子空间闭合；接近零时必须用相对尺度判断，并区分 lucky、数值和不稳定除法。
7. **AI 中如何用？** 只提供 JVP 的 Jacobian、状态空间更新与 Koopman 算子都可用 Arnoldi，但最大实部、最大模和最大奇异值是三种不同目标。

> [!warning] 教学模型边界
> 三维例子能精确暴露非正规投影与 residual 语义，却无法展示长时间正交性损失和多次 restart。它还含 defective eigenvalue，故不能套用基于良态特征向量矩阵的普通误差界；实际任务应同时报告 true residual、正交缺陷、matvec 数和目标谱选择规则。

> [!success] 第一遍停靠线
> 应能从 $q_1$ 独立算出 $q_2,q_3$ 与 $\bar H_2$，由 trace/determinant 得到 Ritz values $1,2$，再算出 residual $2\sqrt6/3$ 与 $1$。还要能解释：Ritz value 命中真谱不等于 Ritz vector 已准确，$h_{4,3}=0$ 则表示整个三维不变空间已经闭合。

## 二、从 Lanczos 到 Arnoldi：删去哪条假设

Lanczos 假设 $A=A^T$。现在只要求

$$
A\in\mathbb C^{n\times n},
$$

不要求正规、更不要求对称。Krylov 子空间仍是

$$
\mathcal K_k(A,q_1)=\operatorname{span}\{q_1,Aq_1,\ldots,A^{k-1}q_1\}.
$$

但对称性恒等式

$$
q_i^*Aq_j=(Aq_i)^*q_j
$$

不能再把所有久远方向系数消掉。新向量通常要与**全部旧基向量**正交，因此 Arnoldi 是长递推。

> [!warning] 最重要的概念边界
> “矩阵的特征值都为实数”不推出矩阵对称或正规；“投影小矩阵恰好近似对称”也不能授权三项递推。必须验证算子结构本身。

## 三、逐步正交化

从 $\|q_1\|=1$ 开始，第 $j$ 步：

$$
w=Aq_j.
$$

依次去掉旧方向：

$$
h_{ij}=q_i^*w,\qquad w\leftarrow w-q_ih_{ij},\qquad i=1,\ldots,j.
$$

最后

$$
h_{j+1,j}=\|w\|_2,\qquad q_{j+1}=w/h_{j+1,j}.
$$

于是单列关系为

$$
Aq_j=\sum_{i=1}^{j+1}q_ih_{ij}.
$$

因为第 $j$ 列只出现到第 $j+1$ 行，系数矩阵是上 Hessenberg。

### 3.1 伪代码

```text
q₁ = b / ‖b‖₂
for j = 1,...,k
    w = A qⱼ
    for i = 1,...,j
        hᵢⱼ = qᵢ* w
        w = w - qᵢ hᵢⱼ
    end
    可选：再次对 Qⱼ 做同样投影并累加系数
    hⱼ₊₁,ⱼ = ‖w‖₂
    若相对 breakdown：停止或换起点
    qⱼ₊₁ = w / hⱼ₊₁,ⱼ
end
```

这里写的是 modified Gram–Schmidt（MGS）。一次 MGS 在良态情形通常够用；当新向量已几乎落入旧空间，二次正交化显著更稳。

## 四、Arnoldi 分解

把前 $k$ 列合并：

$$
AQ_k=Q_{k+1}\bar H_k,
$$

其中

$$
Q_k=[q_1,\ldots,q_k],\qquad
\bar H_k=
\begin{bmatrix}
H_k\\h_{k+1,k}e_k^T
\end{bmatrix}.
$$

等价地，

$$
\boxed{AQ_k=Q_kH_k+h_{k+1,k}q_{k+1}e_k^T.}
$$

精确算术中 $Q_k^*Q_k=I$，左乘 $Q_k^*$ 得

$$
H_k=Q_k^*AQ_k.
$$

### 4.1 为什么只保证 Hessenberg

在构造第 $j$ 列时，$Aq_j$ 可投影到所有 $q_1,\ldots,q_j$，再加 $q_{j+1}$；因此 $h_{ij}=0$ 只在 $i>j+1$。没有对称性便不能推出上方远带为零。

### 4.2 与显式 Hessenberg 化的区别

[[Hessenberg 化与 QR 特征值算法]]用相似变换把整个稠密矩阵约化，成本约 $O(n^3)$；Arnoldi 只构造所需维数的投影，适合只提供 `matvec` 的大规模算子。两者都出现 Hessenberg，但一个是全矩阵预处理，一个是局部 Krylov 投影。

## 五、Rayleigh–Ritz 与残差认证

求小问题

$$
H_ky=\theta y,\qquad \|y\|=1,
$$

并提升到原空间

$$
x=Q_ky.
$$

代入 Arnoldi 分解：

$$
\begin{aligned}
r&=Ax-\theta x\\
&=h_{k+1,k}q_{k+1}e_k^Ty.
\end{aligned}
$$

因此精确算术中

$$
\boxed{\|r\|_2=|h_{k+1,k}e_k^Ty|.}
$$

而

$$
Q_k^*r=0
$$

是 Galerkin 条件。

> [!tip] 廉价但不盲信
> 末分量公式无需再做一次 matvec，适合每轮筛选；最终结果应抽查直接残差，尤其在重启、低精度或正交性已劣化时。

### 5.1 尺度化停止

单位 $x$ 可用

$$
\eta(\theta,x)=
\frac{\|Ax-\theta x\|_2}{\|A\|_2+|\theta|}
$$

或使用可计算的算子范数估计。它衡量一个后向误差尺度；对非正规矩阵，小后向误差并不自动给出小特征值前向误差。

## 六、完整手算：非正规矩阵

取

$$
A=\begin{bmatrix}1&1&0\\0&2&1\\0&0&3\end{bmatrix},
\qquad
q_1=\frac1{\sqrt2}(1,0,1)^T.
$$

$A$ 的特征值是 $1,2,3$，但 $A\ne A^T$。

### 6.1 第一步

$$
Aq_1=\frac1{\sqrt2}(1,1,3)^T,
\qquad h_{11}=q_1^TAq_1=2.
$$

$$
w=Aq_1-2q_1=\frac1{\sqrt2}(-1,1,1)^T.
$$

所以

$$
h_{21}=\sqrt{\frac32},\qquad
q_2=\frac1{\sqrt3}(-1,1,1)^T.
$$

### 6.2 第二步

$$
Aq_2=\frac1{\sqrt3}(0,3,3)^T.
$$

第一投影系数

$$
h_{12}=q_1^TAq_2=\sqrt{\frac32}.
$$

去掉 $q_1$ 后，再有

$$
h_{22}=q_2^TAq_2=2.
$$

最终余量

$$
w=\frac1{\sqrt3}\left(\frac12,1,-\frac12\right)^T,
$$

故

$$
h_{32}=\frac1{\sqrt2},\qquad
q_3=\frac1{\sqrt6}(1,2,-1)^T.
$$

前两步投影为

$$
H_2=
\begin{bmatrix}
2&\sqrt{3/2}\\
\sqrt{3/2}&2
\end{bmatrix},
\qquad
\bar H_2=
\begin{bmatrix}
2&\sqrt{3/2}\\
\sqrt{3/2}&2\\
0&1/\sqrt2
\end{bmatrix}.
$$

此例的 $H_2$ 偶然对称，但这不是 Arnoldi 的一般性质。它的 Ritz 值

$$
2\pm\sqrt{3/2}\approx3.2247, 0.7753
$$

甚至越过 $A$ 的实谱区间 $[1,3]$。这不矛盾：非正规矩阵的 Rayleigh 商落在数值域，而数值域可比谱的凸包更大；对称矩阵的 Ritz 交错直觉在此失效。

## 七、非正规性：为什么残差仍不等于前向准确

若 $A=V\Lambda V^{-1}$ 可对角化，则微扰可被 $\kappa(V)$ 放大。粗略地，Bauer–Fike 型语言给出：扰动后特征值可落在以原特征值为中心、半径与 $\kappa(V)\|E\|$ 成正比的区域。$V$ 病态时，小残差只证明附近有一个小扰动问题，不一定把 $\theta$ 锁在某个原特征值附近。

更适合一般矩阵的三个对象是：

- 右残差 $Ax-\theta x$；
- 左残差 $A^*z-\bar\theta z$；
- 左右夹角 $|z^*x|$，它控制简单特征值条件数。

当 $z^*x$ 很小时，特征值高度敏感。此时还应观察[[非正规矩阵、预解式与伪谱]]中的伪谱与 Schur 子空间，而不是只输出更多小数位。

## 八、Ritz、Schur 与 harmonic Ritz

### 8.1 普通 Ritz

普通 Ritz 值是 $H_k$ 的特征值，通常更自然地解析谱的外缘。若 $H_k$ 本身非正规，其特征向量也可能病态。

### 8.2 Schur 向量

对 $H_k$ 做小型 Schur 分解

$$
H_k=ZTZ^*,
$$

提升 $Q_kZ$ 可得到有序近似不变子空间。对聚簇或非正规问题，Schur 向量常比逐个 Ritz 特征向量更稳定，锁定也更自然。

### 8.3 harmonic Ritz

若目标靠近移位 $\sigma$，普通 Ritz 可能优先逼近外围。harmonic Ritz 让残差对 $A\mathcal K_k$ 或移位后的像空间满足 Petrov–Galerkin 条件，常用于内部特征值与重启 GMRES。它不是“自动更准确”，而是把近似条件对准内部目标。

### 8.4 shift-and-invert

对

$$
B=(A-\sigma I)^{-1}
$$

运行 Arnoldi，原本靠近 $\sigma$ 的特征值映射成最大模。不要显式求逆；固定移位应复用分解或可靠的预条件求解，并以原问题残差验收。

## 九、breakdown 与不变子空间

若精确算术中

$$
h_{j+1,j}=0,
$$

则 $A\mathcal K_j\subseteq\mathcal K_j$，当前空间已经不变；$H_j$ 包含该不变子空间上的精确谱。这是 happy breakdown。

浮点中应用相对测试，例如比较 $h_{j+1,j}$ 与 $\|Aq_j\|$、$\|A\|$ 估计和容差。若还需更多谱方向，可换一个与已知空间正交的新起点，形成 deflation/块策略。

## 十、有限精度正交化

### 10.1 一次 MGS

每次更新立即使用新余量，通常比经典 Gram–Schmidt 稳定，但当余量比 $Aq_j$ 小很多时，旧方向消除会受消去误差限制。

### 10.2 二次 MGS

再次计算

$$
c=Q_j^*w,\qquad w\leftarrow w-Q_jc,\qquad h_{1:j,j}\leftarrow h_{1:j,j}+c.
$$

“twice is enough”是常见经验而非无条件定理；需要用

$$
\omega_k=\|Q_k^*Q_k-I\|
$$

验收。

### 10.3 通信代价

在分布式环境，内积要求全局归约；长递推的瓶颈可能是 $O(k)$ 次同步，而非 $Aq$ 的 FLOPs。块 Arnoldi 和 communication-avoiding 变体用更多局部计算换较少同步，但会改变稳定性分析。

## 十一、成本模型

若单次 matvec 成本为 $C_A$，$k$ 步近似：

$$
\text{matvec}=kC_A,\qquad
\text{orthogonalization}=O(nk^2),\qquad
\text{storage}=O(nk),
$$

小型 Hessenberg 特征分解约 $O(k^3)$。当 $k$ 增长时，正交和内存最终会压过 matvec，这正是重启存在的工程原因。

## 十二、重启不是“清空再来”

### 12.1 显式重启

取当前最有希望的 Ritz/Schur 向量作为新起点。若只保留一个向量，可能丢失多方向信息并反复重学。

### 12.2 厚重启

保留 $p$ 个目标 Schur/Ritz 方向作为初始块，再扩展到最大维数 $m$。适合聚簇或多特征对。

### 12.3 隐式重启

对 $H_m$ 做移位 QR，将不需要的方向用多项式过滤掉，同时在不显式形成高次幂的情况下压缩 Arnoldi 分解。核心不是“少存一些”，而是**选择保留哪部分谱信息**。

### 12.4 锁定与净化

收敛方向进入 locked Schur block，活动子空间与其正交；对内部目标可配合 harmonic extraction 或 refined Ritz vector。报告中应区分 active、converged、locked 和 rejected。

## 十三、收敛的多项式视角

任一 $x\in\mathcal K_k$ 都是 $p_{k-1}(A)q_1$。对可对角化矩阵，理想多项式应在目标特征值处大、在非目标谱处小；但非正规时还受 $V^{-1}$ 放大，单看特征值分布不足。对近 Jordan 结构，$p(A)$ 还依赖导数 $p'(\lambda),p''(\lambda),\ldots$。

因此：

- 对称问题可主要谈谱间隙与多项式逼近；
- 非正规问题必须把特征向量条件、数值域/伪谱和暂态一起纳入。

## 十四、与 GMRES 和矩阵函数

### 14.1 GMRES

求 $Ax=b$，令 $r_0=b-Ax_0$。Arnoldi 对 $\mathcal K_k(A,r_0)$ 给出

$$
A Q_k=Q_{k+1}\bar H_k.
$$

令 $x_k=x_0+Q_ky$，残差最小化化成小最小二乘：

$$
\min_y\|\|r_0\|e_1-\bar H_ky\|_2.
$$

所以 Arnoldi 是 GMRES 的代数骨架；但“GMRES 的 harmonic Ritz 值”是收敛诊断，不应与直接特征求解任务混为一谈。

### 14.2 矩阵函数作用

对 $f(A)b$，

$$
f(A)b\approx\|b\|Q_k f(H_k)e_1.
$$

这避免形成 $f(A)$。误差依赖 $f$ 在与谱/数值域相关区域的逼近、非正规放大及 Krylov 维数。指数积分器、Markov/Koopman 演化和线性化动力学常使用此结构。

## 十五、AI 与科学计算应用

### 15.1 非对称 Jacobian

深度网络或优化动力学的 Jacobian $J$ 一般非对称。只用 JVP 即可做 Arnoldi；若要左右条件数还需 VJP 估计左向量。目标可以是最大实部（局部稳定性）而非最大模，二者不可混淆。

### 15.2 注意力/状态空间线性化

线性化转移算子的谱半径关联长程传播，但非正规暂态可能在谱半径小于一时仍产生大放大。应同时估计 $\|J^t\|$、数值半径或奇异值，而非只看特征值。

### 15.3 Koopman 与转移算子

数据驱动算子常非正规且带采样噪声。Arnoldi 输出应配合残差、bootstrap/数据扰动稳定性和不变子空间角，而不是把所有 Ritz 点解释成物理模态。

### 15.4 低秩适配与训练动力学

若更新算子非对称，Arnoldi 可发现旋转/增长模态；但若任务真正关心最大放大，则应转向奇异值或 Hermitian dilation，而不是把谱半径当谱范数。

## 十六、可信实现契约

```text
operator: shape、dtype、JVP/matvec、是否确定性
target: largest magnitude / largest real part / near sigma / invariant subspace
start: seed、block width、与已锁定空间的正交化
subspace: m、restart、retained dimension、locking
orthogonalization: MGS passes、触发阈值、orthogonality metric
extraction: Ritz / Schur / harmonic / refined
stopping: direct and cheap residual、operator scale
conditioning: left-right angle 或扰动稳定性
cost: matvec、adjoint matvec、inner solves、reductions、memory
exceptions: breakdown、stagnation、unconverged、duplicate/unstable modes
```

## 十七、常见失败模式

| 失败 | 原因 | 修正 |
|---|---|---|
| 对一般矩阵强行三项递推 | 缺少对称性 | 使用完整 Arnoldi |
| 用 Ritz 值变化代替残差 | 值停滞不等于方程满足 | 报告尺度化直接残差 |
| 小残差就宣称高前向精度 | 非正规敏感性 | 左右向量、伪谱/扰动检查 |
| restart 时只清空基 | 丢失已学谱信息 | 厚/隐式重启与锁定 |
| 最大模当最大实部 | 稳定性目标混淆 | 明确排序函数 |
| 显式形成 Jacobian | 内存和构造成本巨大 | JVP/VJP 算子接口 |
| 只报 FLOPs | 内积同步可能主导 | 报告 reductions 与 passes |

## 十八、实验与复现

[[实验 - Arnoldi 非正规性、重正交与重启]]使用确定性非正规上三角矩阵，验证：

1. 最大 Ritz 对的直接残差与尾项公式一致；
2. 两次 MGS 在 9 位舍入模拟中显著抑制正交缺陷；
3. 保留目标 Ritz 向量的 $m=6$ 重启仍能持续降低残差。

图由 [plot_arnoldi_restart_nonnormal.py](</Users/tong/Nodes/basic/00-知识库管理/_labs/code/plot_arnoldi_restart_nonnormal.py>) 生成。

## 十九、掌握检查

- [ ] 能从逐列正交化写出 Arnoldi 分解；
- [ ] 能推导 Ritz 廉价残差；
- [ ] 能手算本章 $3\times3$ 前两步；
- [ ] 能解释为何非正规 Ritz 值可越过实谱区间；
- [ ] 能区分普通、harmonic、Schur 与 shift-invert 提取；
- [ ] 能解释重启保留信息和二次 MGS 的目的；
- [ ] 能为 JVP 算子写出目标、停止与敏感性验收。

## 二十、课程闭环与后继

- 习题：[[习题 - Arnoldi 方法]]；
- 独立解答：[[解答 - Arnoldi 方法]]；
- 实验：[[实验 - Arnoldi 非正规性、重正交与重启]]；
- 奇异值算法：[[SVD 算法与谱范数估计]]；
- 非正规理论：[[非正规矩阵、预解式与伪谱]]、[[矩阵扰动]]；
- 矩阵函数：[[矩阵函数与矩阵指数]]。

## 来源与证据边界

- [[S-2023-Demmel-Krylov-Arnoldi-Lanczos]]：Arnoldi 分解、成本、Ritz 残差和 Lanczos 特化；
- [[S-2000-Netlib-Krylov-Eigensolver-Templates]]：重正交、内部特征值、重启与生产实现边界；
- [[S-2002-Higham-数值算法准确性与稳定性]]：后向误差与有限精度语言。

手算等式是精确算术结论；一般矩阵的收敛不能只由特征值间距预测；实验中的重启曲线证明该构造上的机制，不提供任意问题的统一迭代次数。
