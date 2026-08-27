---
type: experiment
status: draft
area: [math/lie-theory, math/numerical-analysis, ai/equivariant-learning]
topic: "Lie 指数、BCH 与群平均等变审计"
prerequisites: ["[[Lie 群、Lie 代数与对称性]]", "[[矩阵函数与矩阵指数]]", "[[前向误差与后向误差]]"]
related: ["[[习题 - Lie 群、Lie 代数与对称性]]", "[[解答 - Lie 群、Lie 代数与对称性]]", "[[推导与实验 MOC]]"]
code: "[[00-知识库管理/_labs/code/lie_group_bch_equivariance_audit.py]]"
figure: "[[00-知识库管理/_assets/plots/geometry/plot-lie-group-bch-equivariance-v2.svg]]"
created: 2026-08-19
updated: 2026-08-23
---

# 实验 - Lie 指数、BCH 与群平均等变审计

> [!abstract] 实验问题
> 本实验建立三道相互独立的 symmetry computation 门：SO(2) 的 matrix exponential 是否真的形成 one-parameter group，数值微分能以何阶恢复 generator；SO(3) 中不交换旋转为何使 generator 直接相加只剩二阶精度，BCH bracket correction 是否恢复三阶；有限 cyclic group 上的 Reynolds averaging 是否把任意 dense linear map 投影成严格 translation-equivariant 的 circulant map。

先看图回答：one-parameter group 的局部 generator、非交换乘积的 BCH 修正与有限群平均得到的等变映射，各自应呈现什么误差阶或残差？

![[00-知识库管理/_assets/plots/geometry/plot-lie-group-bch-equivariance-v2.svg|880]]

> [!figure] 实验图｜Lie 指数、BCH 阶与 Reynolds 等变化
> A 以 central difference 恢复 SO(2) generator 并核对群律；B 在 SO(3) 比较直接相加的二阶误差与含 bracket 的 BCH2 三阶误差；C 对 $C_{12}$ 逐步做 conjugation average，直到 shift-commutator 降至舍入误差并得到 circulant map。生成脚本：[[lie_group_bch_equivariance_audit.py]]；全确定性，并对阶、群不变量和等变缺陷设断言。

**怎样读图。** A 的微分阶与群律残差是两道门；B 两条斜率差异直接显示 commutator 项的必要性；C 只在平均完整个群后得到投影，部分平均的下降曲线不能称为严格等变。

**适用边界（图没有证明什么）。** SO(2)、小旋转 SO(3) 与有限 cyclic group 的矩阵例子不证明一般 Lie group 的全局指数覆盖，也不证明 learned equivariant model 的任务性能或连续群离散化误差。

> [!question] 本实验的判别问题
> 怎样用局部阶、全局群律和 commutator residual 区分“近似群结构”“BCH 截断正确”与“映射严格等变”？

> [!note] 一句话结论
> Track A 得到 generator central-difference error 的 observed order $1.99994083$；Track B 得到 naive $e^{X+Y}$ error order $1.99993423$ 与 BCH2 order $3.00005914$；Track C 把 shift-commutator relative defect 从 $1.27186994$ 降到 $1.6067\times10^{-16}$，并把 projected matrix 验证为 circulant。

## 一、复现合同

在知识库根目录运行：

```bash
python3 00-知识库管理/_labs/code/lie_group_bch_equivariance_audit.py
```

环境：Python 3 标准库；不依赖 NumPy、SciPy、Matplotlib、网络或随机种子。三条轨道完全确定。

双跑与字节级验收：

```bash
python3 00-知识库管理/_labs/code/lie_group_bch_equivariance_audit.py
python3 00-知识库管理/_labs/code/lie_group_bch_equivariance_audit.py --output /tmp/lie-group-audit.svg
cmp 00-知识库管理/_assets/plots/geometry/plot-lie-group-bch-equivariance-v2.svg /tmp/lie-group-audit.svg
xmllint --noout 00-知识库管理/_assets/plots/geometry/plot-lie-group-bch-equivariance-v2.svg
```

Canonical SVG SHA-256：

```text
762e867f6c80ffb7500ae3752c93fcef1db72db50021b775f4a82f890735bdad
```

脚本 assertions：

- SO(2) central difference observed order 在 $(1.995,2.005)$；
- SO(2) group law、orthogonality、determinant residual 均在舍入误差；
- SO(3) naive generator-sum order 在 $(1.99,2.01)$；
- BCH2 order 在 $(2.98,3.02)$；
- 最细尺度 BCH2 error 至少比 naive 小 100 倍；
- raw dense map equivariance defect $>0.25$；
- full $C_{12}$ average defect $<2\times10^{-15}$；
- circular convolution defect $<2\times10^{-16}$；
- full average columns 的 circulant residual $<2\times10^{-15}$。

## 二、Track A：SO(2) 的 global law 与 local generator

### 2.1 Analytic target

取

$$
J=\begin{bmatrix}0&-1\\1&0\end{bmatrix},
\qquad
R(t)=e^{tJ}.
$$

理论上

$$
R(s)R(t)=R(s+t),
$$

$$
R(t)^\top R(t)=I,
\qquad \det R(t)=1,
$$

$$
R'(0)=J.
$$

最后一式是“one-parameter group 的初速度就是 Lie algebra generator”。

### 2.2 Central difference 的误差阶

实验计算

$$
D_h=\frac{R(h)-R(-h)}{2h}.
$$

Taylor 展开：

$$
R(h)=I+hJ+\frac{h^2J^2}{2}+\frac{h^3J^3}{6}+O(h^4),
$$

$$
R(-h)=I-hJ+\frac{h^2J^2}{2}-\frac{h^3J^3}{6}+O(h^4).
$$

相减除以 $2h$：

$$
D_h=J+\frac{h^2J^3}{6}+O(h^4),
$$

故 Frobenius error 应为 $O(h^2)$。

### 2.3 结果

扫描

```text
h = 0.4, 0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625
```

得到

```text
so2_derivative_order = 1.99994083
group_law_max        < 5.0e-16
orthogonality_max    < 4.0e-16
determinant_residual < 3.0e-16
```

> [!warning] 证据边界
> 这里使用 analytic `sin/cos` 构造 $R(t)$。它验证公式和 finite-difference order，不审计一般 matrix-exponential algorithm 的 scaling-and-squaring、Fréchet conditioning 或低精度实现。

## 三、Track B：SO(3) 的 bracket 与 BCH

### 3.1 设置

取

$$
X=a\widehat e_1,
\qquad
Y=a\widehat e_2.
$$

目标有限变换按固定顺序定义为

$$
R_{\mathrm{target}}=e^Xe^Y.
$$

因

$$
[X,Y]=a^2\widehat e_3,
$$

比较两个近似：

$$
R_{\mathrm{naive}}=e^{X+Y},
$$

$$
R_{\mathrm{BCH2}}
=e^{X+Y+\frac12[X,Y]}.
$$

误差均取 Frobenius norm。

### 3.2 预期阶数

BCH 给

$$
\log(e^Xe^Y)
=X+Y+\frac12[X,Y]
+\frac1{12}[X,[X,Y]]
+\frac1{12}[Y,[Y,X]]+O(a^4).
$$

因此：

- 忽略 bracket 时，generator error 首项为 $O(a^2)$，group error也一般为 $O(a^2)$；
- 保留 $\frac12[X,Y]$ 后，首个遗漏 nested commutator 是 $O(a^3)$。

### 3.3 结果

```text
so3_naive_order = 1.99993423
so3_bch2_order  = 3.00005914
```

最细尺度上 BCH2 error 比 naive error 小超过 100 倍，符合 local asymptotic expansion。

> [!important] 顺序与符号
> 本实验目标固定为 $e^Xe^Y$，故 BCH 二阶项是 $+\frac12[X,Y]$。若交换执行顺序，变为 $e^Ye^X$，对应项为 $\frac12[Y,X]=-\frac12[X,Y]$。不写 composition convention 就讨论 bracket sign 是不完整的。

> [!warning] Local boundary
> BCH 是 $X,Y$ 足够小时的 local series。这里的 observed order不能证明任意大旋转、log branch附近或所有 Lie groups 上的 global convergence。

## 四、Track C：有限群平均把 dense map 投到 intertwiner

### 4.1 Cyclic action 与 defect

令 $S\in\mathbb R^{12\times12}$ 是 one-step cyclic shift，$C_{12}=\{I,S,\ldots,S^{11}\}$。Linear map $A$ translation-equivariant 当且仅当

$$
AS=SA.
$$

定义 relative defect

$$
\delta(A)
=\frac{\|AS-SA\|_F}{\|A\|_F}.
$$

Raw $A$ 用确定性的 trigonometric formula生成，刻意不是 circulant。

### 4.2 Reynolds average

对前 $m$ 个 elements：

$$
P_m(A)=\frac1m\sum_{k=0}^{m-1}S^{-k}AS^k.
$$

$m=12$ 时遍历全部 finite group，得到 exact Reynolds projector

$$
P(A)=\frac1{12}\sum_{k=0}^{11}S^{-k}AS^k.
$$

证明 $P(A)S=SP(A)$：

$$
P(A)S
=\frac1{12}\sum_{k=0}^{11}S^{-k}AS^{k+1}.
$$

把 index cyclically relabel，等于

$$
S\frac1{12}\sum_{k=0}^{11}S^{-k}AS^k=SP(A).
$$

### 4.3 结果

```text
raw_equivariance_defect = 1.271869939357e+00
full_group_defect       = 1.606668481447e-16
circular_conv_defect    = 0.000000000000e+00
```

脚本还检查 full-average matrix 的每一列等于第一列的 cyclic shift，最大列 residual $<2\times10^{-15}$。因此投影结果不仅 commutes with $S$，也显式恢复了 circulant/convolution structure。

### 4.4 Partial averaging 为什么不构成 proof

当 $m<12$，sampled subset一般不在 left multiplication或cyclic index shift下封闭。上述换指标会产生集合外元素，故没有 exact commutation保证。图中 partial averages可下降或波动；只有 full finite group average有结构证明。

对 compact continuous group，full sum可换 normalized Haar integral；对 noncompact group没有 normalized uniform probability，选 finite window或sampling distribution会改变目标。

## 五、三轨联合解释

三条轨道分别回答不同层次的问题：

| Track | 从哪里到哪里 | 验证对象 | 不验证什么 |
|---|---|---|---|
| A | algebra generator → one-parameter group | local derivative + exact SO(2) law | 一般 exp solver / global log |
| B | two generators → noncommutative product | bracket/BCH local order | large-angle global BCH |
| C | arbitrary linear map → equivariant subspace | finite-group orthogonal projection | learned nonlinear model accuracy |

联合起来才形成完整链：generator 描述连续变换的初速度；bracket记录组合顺序；group averaging把对称要求变成可执行的 model-space projection。

## 六、建议改参

完成基础复现后至少做一项：

1. Track A 把 central difference 换 forward difference，验证 order 从 2 变 1；
2. Track B 交换 $e^Xe^Y$ 为 $e^Ye^X$，同时翻转 commutator correction；
3. Track B 改用平行 axes，验证 $[X,Y]=0$ 时 naive composition 到舍入误差正确；
4. Track C 改 $n=7,16$，检查 full average仍得到 circulant matrix；
5. Track C 加 zero-boundary convolution，比较 cyclic shift residual；
6. 用 float32 array library重做，分离 truncation区与 rounding floor。

## 七、结论可写到什么强度

可以写：

- 本确定性矩阵设置恢复了 SO(2) generator 的二阶 central-difference law；
- 在指定 SO(3) 小旋转族上，BCH bracket correction 把局部误差从二阶降到三阶；
- 对 $C_{12}$ 的 full finite-group average，在 double precision下把 shift-commutator defect降到机器精度并恢复 circulant结构。

不可以写：

- 所有 Lie group 的 exponential 都可由本方法稳定计算；
- BCH 在任意尺度收敛；
- group averaging总能改善 learning accuracy；
- finite sampled residual证明 continuous exact equivariance；
- 强制更多 symmetry 总能提高泛化。

> [!important] 状态语义
> 脚本、SVG、assertions、双跑与渲染通过，只证明实验工具 `composed / reproducible`。学习者尚未独立复现、改参、解释失败轨道，故本章仍为 `draft / not-attempted`。
