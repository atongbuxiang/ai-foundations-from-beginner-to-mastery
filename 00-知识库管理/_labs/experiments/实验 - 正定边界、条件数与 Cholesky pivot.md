---
type: experiment
status: draft
area: [labs, math/matrix-analysis, math/numerical-linear-algebra]
prerequisites: ["[[二次型与正定矩阵]]", "[[Cholesky 分解]]", "[[条件数]]"]
related: ["[[矩阵扰动]]", "[[数值线性代数 MOC]]", "[[推导与实验 MOC]]"]
code: "[[plot_cholesky_positive_definite_boundary.py]]"
figure: "[[00-知识库管理/_assets/plots/cholesky/plot-cholesky-pivot-condition-v2.svg]]"
figure_sha256: "4167f1592801d3323c5e7a21064068efd0bab7351b46b05c948dc5dc14b2924c"
sources: ["MIT-18.335-Cholesky"]
created: 2026-08-15
updated: 2026-08-23
---

# 实验 - 正定边界、条件数与 Cholesky pivot

> [!abstract] 实验结论
> 对二阶相关矩阵，相关系数 $\rho$ 趋近 1 时，最小特征值 $1-\rho$ 趋近 0，条件数发散，第二个 Cholesky 对角元同时趋近 0。分解尚未失败时，一个很小的 pivot 已经是在警告：矩阵接近半正定边界，某个方向几乎没有独立信息。

> [!question] 本实验的判别问题
> 在 Cholesky 真正遇到非正 pivot 之前，谱条件数与因子对角元能否给出同一正定性余量的连续预警？

## 研究问题

Cholesky 程序在遇到非正 pivot 时会失败。但在失败发生之前，能否从因子和谱量中看见连续的预警？

我们希望同时观察：

1. 正定性余量如何缩小；
2. 条件数如何恶化；
3. Cholesky 对角元如何接近 0；
4. 这些量如何表达同一个“两个变量接近完全相关”的结构事实。

## 可精确求解的模型

取

$$
\boldsymbol A_{\rho}
=\begin{bmatrix}
1&\rho\\
\rho&1
\end{bmatrix},
\qquad 0\le\rho<1.
$$

它的标准正交特征方向为

$$
\boldsymbol u_+=\frac1{\sqrt2}(1,1)^{\top},
\qquad
\boldsymbol u_-=\frac1{\sqrt2}(1,-1)^{\top},
$$

对应特征值

$$
\lambda_+=1+\rho,
\qquad
\lambda_-=1-\rho.
$$

当 $0\le\rho<1$ 时两者都为正，所以矩阵正定。二范数条件数为

$$
\kappa_2(\boldsymbol A_\rho)
=\frac{1+\rho}{1-\rho}.
$$

直接递推得到

$$
\boldsymbol L_\rho
=\begin{bmatrix}
1&0\\
\rho&\sqrt{1-\rho^2}
\end{bmatrix},
\qquad
\boldsymbol A_\rho=\boldsymbol L_\rho\boldsymbol L_\rho^{\top}.
$$

第二个对角元满足

$$
l_{22}
=\sqrt{1-\rho^2}
=\sqrt{(1-\rho)(1+\rho)}.
$$

因此同一个距离 $1-\rho$ 同时控制最小特征值、条件数和 Cholesky pivot。

## 预注册判断

> [!hypothesis] 假设
> 当 $\rho\to1^-$ 时，$\kappa_2\sim2/(1-\rho)$，而 $l_{22}\sim\sqrt{2(1-\rho)}$。条件数会发散，pivot 会趋近 0；在 $\rho=1$ 处矩阵降为秩 1，严格正定与正对角 Cholesky 同时消失。

## 变量设计

| 类型 | 变量 | 范围 | 说明 |
|---|---|---|---|
| 自变量 | $1-\rho$ | $10^{-6}$ 到 $1$，对数网格 | 到半正定边界的距离 |
| 因变量 | $\kappa_2(\boldsymbol A_\rho)$ | 精确公式 | 相对误差放大潜力 |
| 因变量 | $l_{22}$ | 精确公式 | 第二个 Cholesky 对角元 |
| 边界 | $\rho=1$ | 不含在扫描中 | 特征值为 $2,0$，矩阵奇异 |

## 环境与复现

| 项目 | 值 |
|---|---|
| Python | 标准库 |
| 随机性 | 无 |
| 线性代数库 | 无；使用 $2\times2$ 解析式 |
| 图格式 | 自包含 SVG |

复现命令：

~~~bash
python3 "00-知识库管理/_labs/code/plot_cholesky_positive_definite_boundary.py"
~~~

代码：[plot_cholesky_positive_definite_boundary.py](../code/plot_cholesky_positive_definite_boundary.py)

## 结果

先用图回答：**当 $1-\rho$ 沿对数尺度趋近 0 时，条件数发散与第二个 Cholesky pivot 消失是否由同一个边界距离控制？**

![[00-知识库管理/_assets/plots/cholesky/plot-cholesky-pivot-condition-v2.svg|880]]

> [!figure] 实验图｜正定边界的谱警报与消元警报
> 对 $A_\rho=\begin{bmatrix}1&\rho\\\rho&1\end{bmatrix}$ 扫描 $1-\rho\in[10^{-6},1]$：左图画 $\kappa_2=(1+\rho)/(1-\rho)$，右图画 $l_{22}=\sqrt{1-\rho^2}$。生成脚本：[[plot_cholesky_positive_definite_boundary.py]]；解析公式、无随机数，并对边界端点的条件数与 pivot 设断言。

**怎样读图。** 两个面板共用“到边界的距离”横轴；向左移动时，红线向上、蓝线向下。它们不是两个无关指标，而是分别从全局谱敏感度和逐步 Schur 补读取同一个差分方向信息消失。

**适用边界（图没有证明什么）。** 二阶相关矩阵允许闭式分析；图不证明任意大型稀疏矩阵的小 pivot 都只由最小特征值决定，也不替代缩放、置换、pivoted Cholesky 或舍入误差分析。

关键采样点：

| $\rho$ | $1-\rho$ | $\kappa_2$ | $l_{22}$ |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 |
| 0.5 | 0.5 | 3 | 0.866025 |
| 0.9 | 0.1 | 19 | 0.435890 |
| 0.99 | 0.01 | 199 | 0.141067 |
| 0.999 | 0.001 | 1999 | 0.044710 |

## 逐步解释

### 最小特征值表示差分方向的信息

沿 $\boldsymbol u_-=(1,-1)^{\top}/\sqrt2$，二次型能量是

$$
\boldsymbol u_-^{\top}\boldsymbol A_\rho\boldsymbol u_-=1-\rho.
$$

当两个变量接近完全同向变化时，数据几乎不能区分它们的差。小特征值不是一个抽象数字，而是在说这个差分方向的信息接近消失。

### 小 pivot 是逐步消元中的同一信号

第一步已经用第一个变量解释了与第二个变量的相关部分。剩余量是 Schur 补

$$
1-\rho^2,
$$

它正是 $l_{22}^2$。所以小 pivot 表示：在解释掉第一个方向之后，第二个变量新增的独立能量很小。

### jitter 如何改变边界

把矩阵改成

$$
\boldsymbol A_\rho+\varepsilon\boldsymbol I
$$

会把特征值平移为 $1+\rho+\varepsilon$ 和 $1-\rho+\varepsilon$。最小特征值被托起，条件数下降，Cholesky 更容易成功。但这等价于改变协方差或核矩阵：它是正则化，不是无代价的数值魔法。

## 对 AI 工作的意义

- 高相关特征、重复 token 表示或过窄的数据子空间会产生小特征值；
- 高斯模型和核方法的 log-determinant、白化与线性求解会首先感受到这些方向；
- 只记录“Cholesky 成功”过于粗糙，还应监控最小对角元、条件数估计和 jitter 尺度；
- 若矩阵理论上应正定却出现明显负 pivot，应先查非对称、NaN、错误缩放和建模公式，而不是无限增大 jitter。

## 一致性检查

- [x] 特征值、条件数与 Cholesky 因子均由手工解析式给出。
- [x] $\rho=0$ 时恢复单位矩阵与单位因子。
- [x] $\rho\to1^-$ 时最小特征值和 $l_{22}$ 均趋近 0。
- [x] $\det(\boldsymbol A_\rho)=1-\rho^2=l_{11}^2l_{22}^2$。
- [x] 表格与 SVG 由同一脚本生成并检查。

## 结论边界

> [!warning] 不可外推之处
> 本实验展示的是正定矩阵本身的条件性，不测量某个具体 Cholesky 库在舍入误差下的失败阈值，也不覆盖带主元的半正定分解。

- 高维矩阵可能有多个小特征方向，单个最小 pivot 还受变量顺序影响。
- Cholesky 对角元不是矩阵特征值；这里二者因简单模型而有清晰关系。
- 对非对称或不定矩阵，应使用与结构相符的其他分解，不能强套 Cholesky。

## 下一步

- [ ] 在高维相关矩阵上比较最小特征值与最小 Cholesky 对角元。
- [ ] 注入非对称舍入扰动，比较先对称化与直接报错的风险。
- [ ] 研究 pivoted Cholesky 对低秩核矩阵的近似。

## 来源

- [[二次型与正定矩阵]]。
- [[Cholesky 分解]]。
- [MIT 18.335：Cholesky Factorization and Specialized Solvers](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/pages/resource-index/)。
