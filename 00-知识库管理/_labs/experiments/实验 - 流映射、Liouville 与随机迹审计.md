---
type: experiment
status: draft
area: [math/ode, math/numerical-analysis, math/probability, ai/generative-modeling]
topic: "流映射、Liouville 与 Hutchinson trace"
prerequisites: ["[[流映射、Liouville 公式与连续正规化流]]", "[[Euler、Runge-Kutta 与离散化误差]]"]
related: ["[[习题 - 流映射、Liouville 公式与连续正规化流]]", "[[推导与实验 MOC]]", "[[刚性系统、绝对稳定域与隐式方法]]"]
code: "[[00-知识库管理/_labs/code/cnf_liouville_hutchinson_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/dynamics/plot-cnf-liouville-hutchinson-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - 流映射、Liouville 与随机迹审计

> [!abstract] 实验问题
> 本实验不训练神经网络，而是先建立 CNF 必须通过的三个确定性/统计校准门：非正规线性流能否同时表现强剪切和严格 Liouville 面积收缩；非线性状态与 log-density 能否由同一 RK4 增广程序以四阶收敛；Hutchinson 单 probe 的无偏性、精确方差与多 probe 标准误差是否可被枚举复现。

先看图回答：流映射的体积变化、增广 log-density ODE 的离散误差和 Hutchinson trace 的统计误差分别应由什么证据验收？

![[00-知识库管理/_assets/plots/dynamics/plot-cnf-liouville-hutchinson-v2.svg|880]]

> [!figure] 实验图｜流几何、Liouville 账本与随机迹方差
> A 对非正规线性流同时核对剪切、面积与 $\det e^{tA}$；B 用同一 RK4 增广系统比较 state/log-density 四阶误差和 Liouville residual；C 枚举 Hutchinson probe 验证无偏性与方差，再显示累计均值的随机波动。生成脚本：[[cnf_liouville_hutchinson_audit.py]]；固定 probe 序列，并对几何、阶和方差设断言。

**怎样读图。** A 不用最大奇异值替代 determinant；B state 和 logp 必须共享轨道但分别报误差；C 的单条累计均值不要求单调接近真值，要与理论标准误差一起解释。

**适用边界（图没有证明什么）。** 使用二维解析流、标量非线性 CNF 与一个小矩阵 trace；图不替代高维 adaptive solver、反向梯度、神经向量场或真实 wall-time/variance 研究。

> [!question] 本实验的判别问题
> 如何把几何守恒/压缩、数值积分误差与随机 trace 估计误差分账，使 CNF 的 log-likelihood 偏差可定位？

## 一、复现合同

运行：

```bash
python3 00-知识库管理/_labs/code/cnf_liouville_hutchinson_audit.py
```

环境：Python 3 标准库；不依赖 NumPy、SciPy、PyTorch 或网络。脚本固定 seed `20260819`，同时写出 SVG，并在 analytic identity、order 与 exact enumeration 不通过时非零退出。

确定性检查：

```bash
python3 00-知识库管理/_labs/code/cnf_liouville_hutchinson_audit.py
shasum -a 256 00-知识库管理/_assets/plots/dynamics/plot-cnf-liouville-hutchinson-v2.svg
```

当前 SVG SHA-256：

```text
366a3bc4a2a8e2475519dfd3225202c574cacbbab9e3cb899c273062aec6f774
```

## 二、轨道 A：非正规形变与 Liouville 面积

### 2.1 系统

$$
A=\begin{bmatrix}-1&8\\0&-2\end{bmatrix},
\qquad
e^{tA}=\begin{bmatrix}
e^{-t}&8(e^{-t}-e^{-2t})\\
0&e^{-2t}
\end{bmatrix}.
$$

在 $t=0.5$ 把单位正方形四点逐一映射，使用 shoelace formula 计算像平行四边形面积。同时由 trace 计算

$$
\det e^{tA}=e^{t\operatorname{tr}A}=e^{-3t}.
$$

### 2.2 结果

```text
det(exp(tA)) = 2.231301601484e-01
polygon_area = 2.231301601484e-01
sigma_max    = 2.03377970
sigma_min    = 0.10971206
```

两条独立路径在 $10^{-14}$ 内一致。最大奇异值却大于2，说明某方向长度可放大；两个奇异值的乘积仍是0.22313。实验钉住：

$$
\text{directional stretch}>1
\quad\text{可与}\quad
\text{total area contraction}<1
\quad\text{同时发生。}
$$

> [!warning] 不能推出
> 这个单矩阵实验不证明所有 negative-divergence system 都有 transient growth；它只作为“divergence 不是最大方向增长率”的构造反例。

## 三、轨道 B：非线性 CNF 的 state–logp 增广积分

### 3.1 解析 reference

取

$$
x'=-x^3,
\qquad
\ell'=3x^2,
\qquad
x_0=1.2,
\qquad
\ell_0=\log\mathcal N(x_0;0,1).
$$

解析值为

$$
x(t)=\frac{x_0}{\sqrt{1+2tx_0^2}},
$$

$$
J_t=(1+2tx_0^2)^{-3/2},
$$

$$
\ell(t)=\ell_0-\log J_t.
$$

在 $t=1$：

```text
exact_x    = 6.092076990802e-01
exact_logp = 3.948141972481e-01
jac        = 1.308435779811e-01
```

### 3.2 RK4 refinement

| $N$ | state endpoint error | logp endpoint error |
|---:|---:|---:|
| 10 | $3.82968245\times10^{-7}$ | $5.49138951\times10^{-5}$ |
| 20 | $1.54498252\times10^{-8}$ | $3.04897941\times10^{-6}$ |
| 40 | $1.91798899\times10^{-9}$ | $1.77798761\times10^{-7}$ |
| 80 | $1.45591650\times10^{-10}$ | $1.07079247\times10^{-8}$ |
| 160 | $9.84301529\times10^{-12}$ | $6.56574350\times10^{-10}$ |

相邻 observed orders：

```text
state: 4.63156235, 3.00992417, 3.71959492, 3.88668347
logp : 4.17077293, 4.10000923, 4.05349447, 4.02757670
```

State 在中间 refinement 有 pre-asymptotic cancellation，因此不强行要求每个相邻斜率都恰为4；最细一档恢复到3.8867。Log-density 稳定逼近四阶。解析 Liouville residual 为0（浮点打印精度下）：

$$
|\ell(1)-\ell(0)+\log J_1|=0.
$$

### 3.3 为什么两条 error curve 都要报

在实际 CNF 中，状态轨迹误差会改变 divergence 的采样位置，trace 近似与 log-density quadrature 又引入额外误差。State endpoint 准确不代表 likelihood 准确；logp 准确也可能来自误差抵消。因此验收必须同时看：

- state reference error；
- log-density reference error；
- Liouville identity residual；
- solver refinement；
- 若用 stochastic trace，再加 probe uncertainty。

## 四、轨道 C：Hutchinson 的 exact enumeration

### 4.1 测试矩阵

$$
B=\begin{bmatrix}
1&2&-1&0.5\\
0&-2&3&1\\
4&-1&0.5&2\\
0&2&-3&3
\end{bmatrix},
\qquad \operatorname{tr}B=2.5.
$$

枚举 $d=4$ 时全部 $2^4=16$ 个 Rademacher 向量，而不是用大样本近似 theorem。令

$$
S=\frac{B+B^T}{2}.
$$

理论方差：

$$
\operatorname{Var}(\varepsilon^TB\varepsilon)
=4\sum_{i<j}S_{ij}^2
=27.25.
$$

Gaussian probe 对同一矩阵的理论方差为

$$
2\|S\|_F^2=55.75.
$$

### 4.2 枚举结果

```text
true trace             = 2.50000000
exact enumeration mean = 2.50000000
enumeration variance   = 27.25000000
Rademacher theory      = 27.25000000
Gaussian theory        = 55.75000000
```

均值和方差都在 $10^{-14}$ 内命中理论。

### 4.3 固定 seed 的累计均值不是单调误差曲线

| probes $m$ | cumulative mean | absolute error | theoretical SE |
|---:|---:|---:|---:|
| 1 | -2.000000 | 4.500000 | 5.220153 |
| 4 | -2.000000 | 4.500000 | 2.610077 |
| 16 | 0.187500 | 2.312500 | 1.305038 |
| 64 | 1.968750 | 0.531250 | 0.652519 |
| 256 | 2.027344 | 0.472656 | 0.326260 |
| 1024 | 2.290039 | 0.209961 | 0.163130 |

理论 standard error 按 $m^{-1/2}$ 单调下降；单条随机 realization 的实际绝对误差不保证每次加 probe 都单调下降。本结果用于防止把一条 seed 曲线误当成收敛定理。

## 五、通过条件与失败注入

脚本当前断言：

1. matrix determinant 与 polygon area 都匹配 $e^{-3t}$；
2. 最大奇异值大于1，确实存在方向拉伸；
3. state/logp endpoint error 随 refinement 下降；
4. 最细 state order 与 logp 后两档 order 进入四阶区；
5. nonlinear Liouville identity 达到浮点精度；
6. 16 个 Rademacher probes 的 exact mean/variance 匹配理论；
7. Rademacher/Gaussian 理论方差分别为27.25/55.75。

建议的失败注入：

- 把增广方程误写成 $\ell'=-3x^2$，观察 Liouville residual/endpoint logp 失败；
- 把矩阵 trace 误写为 eigenvalue norm，观察面积 identity 失败；
- 在 variance 公式中直接使用非对称 $B$ 的全部 off-diagonal，观察与枚举不符；
- RK4 的 $\ell$ 使用更新后 $x$ 做 Euler step，观察 logp order 降低；
- 改 probe 为 biased signs，检查均值偏移。

## 六、结论边界

本实验已经验证：

- 两个具体解析系统上的 Liouville 体积/密度公式；
- 一个增广 CNF ODE 的 RK4 convergence；
- 一个 $4\times4$ 非对称矩阵上 Hutchinson mean/variance 的精确枚举；
- 绘图与数值结果可由标准库确定性复现。

本实验没有验证：

- 任意 neural vector field 的 global existence 或全空间可逆；
- adaptive solver 与随机 RHS 的一般收敛；
- 训练后 CNF likelihood 无偏；
- high-dimensional wall-time advantage；
- sample quality 或真实数据泛化。

这些结论必须通过 DYN-FLOW-D/E 题中的 solver card、coupled trajectory、gradient 与 population evidence 逐级升级。

## 七、复现实验记录

| 日期 | 环境 | 结果 | 状态 |
|---|---|---|---|
| 2026-08-19 | Python 3 standard library | 全部断言通过，SVG hash 固定 | composed / not-attempted by learner |

> [!note] 状态说明
> “脚本由课程施工过程运行通过”不等于学习者已经独立复现。学习者需在不看结果表的情况下先预测趋势、运行、修改至少一个矩阵与一个初值、注入一次失败，并解释为什么失败，才可把实验状态升级为 `reproduced`。
