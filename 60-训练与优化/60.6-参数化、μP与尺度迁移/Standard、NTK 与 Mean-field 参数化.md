---
type: derivation
status: verified
area: [training, optimization, parameterization, ntk, mean-field]
node_id: TRN-42
aliases: [Standard NTK Mean-field 对照, Infinite-Width Training Regimes]
prerequisites: ["[[模型尺度、稳定性指标与 Width-Depth 对象合同]]", "[[NTK、Lazy Training 与 Kernel Regime]]", "[[方差传播与宽层均值场近似]]"]
related: ["[[μP 的 Maximal Update 与宽度尺度推导]]", "[[Tensor Programs、坐标检查与无限宽极限]]", "[[Mean-Field、Feature Learning 与训练 Regime]]"]
sources: ["[[S-2018-Jacot-NTK]]", "[[S-2020-Yang-Tensor-Programs-II-NTK]]", "[[S-2021-Yang-Littwin-Tensor-Programs-IIb]]", "[[S-2021-Yang-Hu-Feature-Learning]]", "[[S-2025-Su-10770-MuP初探]]"]
exercises: ["[[习题 - Standard、NTK 与 Mean-field 参数化]]"]
solutions: ["[[解答 - Standard、NTK 与 Mean-field 参数化]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-parameterization-regime-feature-change-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Standard、NTK 与 Mean-field 参数化

> [!abstract] 一句话结论
> 参数化不只是初始化分布。它同时规定**训练变量怎样存储、forward 中乘什么宽度因子、各参数组用什么学习率时标**。两个网络可以在初始化时表示同一随机函数，却因坐标和 optimizer 不同，在无限宽下分别进入 lazy kernel、mean-field feature learning 或失稳/退化 regime。

## 一、先区分“函数相同”与“训练相同”

考虑单隐层网络

$$
f_n(x;\theta)
=c_n\sum_{i=1}^n a_i\phi(w_i^\top x).
\tag{1}
$$

若把

$$
\widetilde a_i=\lambda_n a_i,
\qquad
\widetilde c_n=\frac{c_n}{\lambda_n},
\tag{2}
$$

则对所有 $x$，初始函数完全相同。但 Euclidean gradient 会变：

$$
\frac{\partial f}{\partial a_i}
=c_n\phi_i,
\qquad
\frac{\partial f}{\partial \widetilde a_i}
=\widetilde c_n\phi_i
=\frac1{\lambda_n}\frac{\partial f}{\partial a_i}.
\tag{3}
$$

若两个坐标都机械使用同一个数值学习率，它们的函数更新不同。因此参数化至少包括：

$$
\mathcal P
=(\text{stored coordinates},\text{init law},\text{forward multipliers},\text{group LR}).
\tag{4}
$$

> [!warning] 术语边界
> “Standard parameterization”在不同论文和框架中可能指不同存储方式。教材使用某张规则表时，必须同时给出 layer orientation、初始化方差、forward multiplier、optimizer 和 LR；不能只写“Xavier/He 所以是 standard”。

## 二、随机和为什么有 $1/\sqrt n$ 与 $1/n$ 两种尺度

令 $z_i=a_i\phi(w_i^\top x)$ 独立近似、均值 0、方差 $q>0$。

### 中心极限定标

若

$$
c_n=n^{-1/2},
\tag{5}
$$

则

$$
\operatorname{Var}f_n(x)
=\frac1n\sum_{i=1}^n\operatorname{Var}(z_i)
=q.
\tag{6}
$$

初始化输出保持非退化随机尺度，典型极限是 Gaussian/GP 方向。

### 大数定律定标

若

$$
c_n=n^{-1},
\tag{7}
$$

则

$$
f_n(x)=\frac1n\sum_i z_i
\to \mathbb Ez_i.
\tag{8}
$$

零均值时初始输出趋于 0；非零均值时趋于确定性函数。这个缩放适合把神经元看作 particles 的经验分布，但必须配合训练时间/LR 才能得到非退化 feature dynamics。

这两种缩放回答不同问题：$1/\sqrt n$ 保留随机 fluctuation，$1/n$ 保留经验平均。

## 三、NTK-style：输出能动，单个特征几乎不动

取

$$
f_n(x)
=\frac1{\sqrt n}\sum_{i=1}^n
a_i\phi(w_i^\top x),
\quad a_i,w_i=O(1),
\tag{9}
$$

并用 $O(1)$ 的 full-batch gradient-descent learning rate。设单个样本的 loss derivative $\partial_f\ell=O(1)$。则

$$
\frac{\partial \ell}{\partial a_i}
=\frac1{\sqrt n}\partial_f\ell\,\phi_i
=O(n^{-1/2}),
\tag{10}
$$

$$
\frac{\partial \ell}{\partial w_i}
=\frac1{\sqrt n}\partial_f\ell\,a_i\phi_i'x
=O(n^{-1/2}).
\tag{11}
$$

有限步后

$$
\Delta a_i,\Delta w_i=O(n^{-1/2})\to0.
\tag{12}
$$

但输出变化会把 $n$ 个与梯度相关、近似同向的贡献相加。以 $a$ 路径的一阶项为例：

$$
\Delta f_n(x)
\approx\frac1{\sqrt n}
\sum_i\Delta a_i\phi_i(x)
=O(1).
\tag{13}
$$

于是出现关键现象：

- 单个 hidden unit 的参数和 feature change 消失；
- 集体输出仍可有 $O(1)$ 更新；
- 网络可由初始化处的一阶线性化描述。

对训练集预测向量 $f_\theta(X)$，线性化为

$$
f_{\theta_0+\Delta\theta}(X)
\approx f_{\theta_0}(X)+J_0\Delta\theta.
\tag{14}
$$

定义 empirical NTK

$$
K_\theta(X,X)=J_\theta J_\theta^\top.
\tag{15}
$$

若训练期间

$$
\lVert K_{\theta_t}-K_{\theta_0}\rVert\to0,
\tag{16}
$$

则平方损失下函数动力学近似

$$
\frac{df_t}{dt}
=-K_{\theta_0}(f_t-y).
\tag{17}
$$

这就是 kernel/lazy regime 的核心：模型学习主要通过固定 tangent features 的线性组合，而不是 $O(1)$ 地重塑 hidden representation。

## 四、Mean-field：把神经元当作会移动的粒子

改取经验平均表示

$$
f_n(x)
=\frac1n\sum_{i=1}^n
a_i\phi(w_i^\top x)
=\int a\phi(w^\top x)\,d\rho_n(a,w),
\tag{18}
$$

其中

$$
\rho_n=\frac1n\sum_{i=1}^n\delta_{(a_i,w_i)}
\tag{19}
$$

是 particle empirical measure。

此时单粒子梯度为 $O(1/n)$。若 base SGD learning rate 为 $O(n)$，或等价地把时间加速 $n$ 倍，则

$$
\Delta a_i,\Delta w_i=O(1).
\tag{20}
$$

经验分布 $\rho_n$ 可在极限中演化为 $\rho_t$，函数变成

$$
f_t(x)=\int a\phi(w^\top x)\,d\rho_t(a,w).
\tag{21}
$$

这里 hidden features 可以产生 $O(1)$ 运动。它不是固定 kernel 模型，而是分布/测度空间中的 nonlinear dynamics。

> [!important] 为什么不能只抄 LR $n$
> 式 (20) 来自式 (18) 的坐标与 full-batch SGD 约定。若把 $1/n$ 吸收到输出权重、改用 Adam、改变 loss reduction 或使用深网络，raw LR 表会改变；应追踪**实际 parameter update 和 feature update**，而不是迁移一个裸数字。

## 五、Standard Parameterization：有限模型默认不等于良好极限

常见框架对 hidden linear weight 使用

$$
W_{ij}\sim\mathcal N(0,1/\mathrm{fan\_in})
\tag{22}
$$

来稳定初始化 activation；这解决的是 forward-at-init。若所有参数组仍共享与 width 无关的 raw LR，则输入层、hidden matrix 和 output layer 的实际 feature update 可能处于不同量级。

[[S-2022-Yang-Tensor-Programs-V-MuTransfer]] 的标准参数化对照正说明：

- 初始化 activation 可以是 $O(1)$；
- 训练后某些层的 activation/update 随 width 爆炸，另一些层更新过慢；
- 把共享 LR 整体缩小可得到稳定 kernel-style limit，却会牺牲非退化 feature learning；
- 只重新调一个 global LR 不能修复各参数组之间的尺度失衡。

因此“SP 不好”不是说 He/Xavier 初始化错误，而是说**初始化规则 + 默认参数坐标 + 共享训练超参**未必构成可跨宽度迁移的完整合同。

## 六、四种 Regime 的对照必须带限定词

| 维度 | Standard（框架默认语境） | NTK-style | Mean-field | μP |
|---|---|---|---|---|
| 主要目标 | 有限宽初始化可训 | 固定 kernel 的非退化函数动力学 | 神经元分布的非线性演化 | 非发散条件下最大 feature update |
| 典型输出缩放 | fan-in init 吸收入权重 | $1/\sqrt n$ | $1/n$ | 按输入/hidden/output 角色分组 |
| 单元 feature motion | 可能失衡 | 固定有限步下趋零 | 可为 $O(1)$ | 设计为非退化 |
| NTK drift | 未保证 | 趋零 | 可非零 | 可保留 feature learning |
| raw LR | 框架默认/共享 | 与所选坐标配套 | 常需时间/LR 重标 | optimizer 与参数角色特定 |
| 风险 | 跨宽 optimum 漂移/失稳 | 过于 lazy | 深网和实现映射复杂 | shape/特殊参数组实现错误 |

这张表是“典型构造的导航”，不是把所有文献术语压成唯一公式。严格比较时必须回到具体网络和 $abc$-style exponent ledger。

## 七、Kernel 与 Feature Learning 怎样测

不要用“训练 loss 下降了”区分 regime。对固定 probe batch，至少记录：

### 1. 相对 feature change

$$
R_h^{(\ell)}(t)
=\frac{\operatorname{RMS}(h_t^{(\ell)}-h_0^{(\ell)})}
{\operatorname{RMS}(h_0^{(\ell)})+\varepsilon}.
\tag{23}
$$

### 2. Kernel drift

$$
R_K(t)
=\frac{\lVert K_t-K_0\rVert_F}
{\lVert K_0\rVert_F+\varepsilon}.
\tag{24}
$$

### 3. Linearization error

$$
E_{lin}(t)
=\frac{\lVert f_t-f_0-J_0(\theta_t-\theta_0)\rVert_2}
{\lVert f_t-f_0\rVert_2+\varepsilon}.
\tag{25}
$$

### 4. 跨宽斜率

对 $R_h(n)$ 或 $R_K(n)$ 拟合 $\kappa$。若 $R_h\propto n^{-1/2}$，支持 lazy 趋势；若趋于非零常数，支持 feature-learning 趋势。有限宽窗口只能称 evidence，不是定理证明。

> [!warning] Kernel drift 也不是唯一判据
> 某层 feature 改变不一定显著改变所测 kernel；不同 kernel norm、probe set 和训练时间会给出不同数值。应把 parameter、feature、kernel、linearization 与 loss 五层合看。

## 八、Tensor Programs 两层证据

[[S-2020-Yang-Tensor-Programs-II-NTK]] 处理初始化 NTK 的确定性极限和 GIA 检查；[[S-2021-Yang-Littwin-Tensor-Programs-IIb]] 进一步处理 NTK 参数化下的训练动力学。两层不可合并为一句“无限宽网络等于 kernel”：

1. 初始化 kernel 收敛；
2. 训练期间 kernel 是否冻结；
3. 训练时域是否固定；
4. 宽度是否沿定理规定比例增长；
5. 有限网络距极限多远。

[[S-2021-Yang-Hu-Feature-Learning]] 再说明：无限宽并不逻辑上等于 fixed kernel；选择 μP 一类参数化可以保留 feature-learning limit。

## 九、图：同一初始函数为何走向不同 Regime

先看图回答：为什么两种写法在 $t=0$ 的输出分布相同，却不能共用同一个学习率？

![[00-知识库管理/_assets/figures/training-optimization/fig-parameterization-regime-feature-change-v1.svg|880]]

> [!figure] 图 TRN-42　参数坐标、聚合尺度与训练 Regime
> 上部从同一个双层网络分出 $1/\sqrt n$ 的 fluctuation 路径、$1/n$ 的 empirical-measure 路径和按参数角色重平衡的 μP 路径；下部用 feature motion、kernel drift 与 output update 区分 lazy、feature-learning 和失稳。来源：依据 [[S-2021-Yang-Littwin-Tensor-Programs-IIb]]、[[S-2021-Yang-Hu-Feature-Learning]] 与 [[S-2025-Su-10770-MuP初探]] 原创绘制。

**怎样读图**：先看 forward 中和的归一化，再看这个因子储存在参数里还是显式 multiplier，最后看 optimizer 实际造成的单元运动与聚合后的输出运动。

**图没有证明什么**：图没有声称每个 $1/\sqrt n$ 网络都 lazy、每个 $1/n$ 网络都 mean-field；训练时标、参数组、相关性、深度和极限次序仍是必要条件。

## 十、常见误解

1. **无限宽 = NTK**：错误；parameterization 决定极限 regime；
2. **初始化函数相同 = 训练相同**：错误；Euclidean gradient 对重参数化并不保持不变；
3. **feature 参数变了 = feature learning**：应测表示而非只测权重；
4. **kernel drift 小 = 泛化一定差**：没有这种普适推论；
5. **mean-field = 前一卷的方差传播**：这里只是相关但不同的语义；前者是训练中的 particle distribution dynamics；
6. **SP 只有一个定义**：必须给出具体坐标和规则；
7. **把 LR 按 $n$ 乘就得到 mean-field**：只在对应 toy contract 下成立。

## 十一、初学者自检

1. 式 (2) 为什么保持函数不变，却改变 gradient coordinate？
2. $1/\sqrt n$ 与 $1/n$ 分别对应 CLT 的 fluctuation 和 LLN 的 empirical average，这对训练有什么影响？
3. 在式 (9) 中，单元更新为何趋零而输出更新仍为 $O(1)$？
4. NTK 初始化极限与 NTK 训练动力学为什么要由两层结果承担？
5. 你会用哪三个量区分 lazy 与 feature-learning 趋势？
6. 为什么“standard initialization 稳定”不能推出“standard training 跨宽稳定”？

## 十二、本节出口

你应能从具体网络写出：

$$
\text{stored parameter}
+\text{forward multiplier}
+\text{init scale}
+\text{optimizer/LR}
\Longrightarrow
\text{training regime}.
$$

下一节 [[μP 的 Maximal Update 与宽度尺度推导]] 将把这套判断变成 exponent ledger，并解释 μP 为什么必须分别处理 input、hidden、output 与 optimizer。
