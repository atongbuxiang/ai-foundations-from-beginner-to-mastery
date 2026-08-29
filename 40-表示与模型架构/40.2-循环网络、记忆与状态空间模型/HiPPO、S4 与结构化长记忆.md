---
type: concept
status: draft
area: [architecture, state-space-models, hippo, s4]
aliases: [HiPPO S4, 结构化状态空间序列模型]
node_id: ARCH-15
prerequisites: ["[[Banach 空间、Hilbert 空间与正交投影]]", "[[连续与离散线性状态空间模型]]", "[[状态空间的递推—卷积对偶与并行扫描]]", "[[结构化矩阵与结构化扰动]]"]
related: ["[[选择性状态空间、Mamba 与证据边界]]", "[[内积空间]]", "[[S-2024-Su-10180-有理生成函数SSM]]"]
sources: ["[[S-2020-Gu-HiPPO]]", "[[S-2022-Gu-S4]]", "[[S-2024-Su-10114-HiPPO正交函数投影]]", "[[S-2024-Su-10137-HiPPO遗留问题]]", "[[S-2024-Su-10162-S4高效计算]]", "[[S-2024-Su-10180-有理生成函数SSM]]"]
exercises: ["[[习题 - HiPPO、S4 与结构化长记忆]]"]
solutions: ["[[解答 - HiPPO、S4 与结构化长记忆]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-hippo-s4-projection-structure-v1.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# HiPPO、S4 与结构化长记忆

> [!abstract] 本节主问题
> HiPPO 先把“记忆历史”定义成指定测度下对过去函数的在线最优投影，投影系数恰可满足线性动力学；S4 再利用 HiPPO 矩阵的 normal-plus-low-rank / diagonal-plus-low-rank 结构，高效生成长卷积核。这里的“最优”“长记忆”“高效”分别属于投影定理、架构参数化和条件化实验，不能合并成一个口号。

## 课程位置与两遍学习路线

- **承接什么：** ARCH-13—14 已说明固定 LTI 状态既能递推也能生成卷积；现在要回答“状态究竟应该压缩历史的什么信息”，以及长核怎样在结构上算得动；
- **本页解决什么：** 先把历史记忆定义成 Hilbert 空间投影，再说明投影系数为何可能形成 ODE，最后用 diagonal-plus-low-rank resolvent 解释 S4 的结构化计算路线；
- **后续为何需要：** ARCH-16 会放弃固定 LTI kernel，引入输入依赖选择性；因此本页必须先把 S4 的固定结构、正式保证和经验结果分层。

**第一遍只做二维投影。** 在 $[0,1]$ 上把线性历史 $u(t)=1+2t$ 投到两个正交基，手算系数并精确重构；由此理解“状态是系数”而不是隐喻。

**第二遍再进入结构化矩阵。** 区分投影误差、系数 ODE、离散化误差与学习误差，再用一个 $2\times2$ rank-one inverse 手算 Woodbury，理解 S4 为何关心 DPLR/Cauchy 结构。

### 问题链

1. 若说状态“记住历史”，必须先声明用什么函数空间、测度、范数和有限子空间吗？
2. 正交投影的“最优”究竟和哪些候选比较？
3. 为什么投影系数随当前时间变化时可能满足线性 ODE？
4. 有限阶系数能低误差重构，为什么仍不等于逐 token 无损检索？
5. 一般稠密 $A$ 的 resolvent 为什么难以长序列高效求值？
6. diagonal-plus-low-rank 怎样把大逆问题降成逐元素逆与小矩阵逆？
7. 投影定理、S4 结构效率和论文 benchmark 为什么必须属于三层证据？

> [!check] 第一遍停靠线
> 若你能复算 $u(t)=1+2t$ 在 $\phi_0=1,\phi_1=\sqrt3(2t-1)$ 下的系数 $(2,1/\sqrt3)$，说明一维截断误差为 $1/3$、二维重构误差为 0，再复核 rank-one inverse 为 $\frac1{11}\left[\begin{smallmatrix}4&-1\\-1&3\end{smallmatrix}\right]$，就完成了本页首遍。

## 符号与对象账本

| 对象 | 数学身份 | AI 中的身份 | 不能偷换成 |
|---|---|---|---|
| $u|_{[0,t]}$ | 截至当前的历史函数 | 连续化序列历史 | 单个 token $u_t$ |
| $\mu_t$ | 历史区间上的测度 | 远近记忆权重 | 无关归一化常数 |
| $\phi_n^{(t)}$ | $L^2(\mu_t)$ 正交基 | memory coordinates | 学得的任意 hidden basis |
| $c_n(t)$ | 投影系数 | HiPPO state component | 原历史样本本身 |
| $\hat u_t$ | 有限维投影重构 | state 可表达的历史摘要 | 无损 replay |
| $A=\Lambda-PQ^*$ | diagonal-plus-low-rank 结构 | S4 structured state matrix | 纯对角 SSM |
| $(I-z\bar A)^{-1}$ | resolvent | kernel/frequency generation 核心 | 任意下游非线性层 |

### 贯穿算例 $\mathcal S_\square$：先把“记忆”做成一个可验算投影

在 $[0,1]$ 上使用均匀测度和前两个正交归一基

$$
\phi_0(t)=1,\qquad
\phi_1(t)=\sqrt3(2t-1).
$$

它们满足

$$
\langle\phi_0,\phi_1\rangle=0,\qquad
\|\phi_0\|_2=\|\phi_1\|_2=1.
$$

选择一段最简单但非恒定的历史

$$
u(t)=1+2t.
$$

第一个投影系数是历史平均：

$$
c_0=\int_0^1(1+2t)\,dt=2.
$$

第二个系数记录线性趋势：

$$
\begin{aligned}
c_1
&=\int_0^1(1+2t)\sqrt3(2t-1)\,dt\\
&=\sqrt3\int_0^1(4t^2-1)\,dt\\
&=\frac{\sqrt3}{3}=\frac1{\sqrt3}.
\end{aligned}
$$

二维重构为

$$
\hat u(t)
=c_0\phi_0(t)+c_1\phi_1(t)
=2+(2t-1)
=1+2t,
$$

因此这个特定线性历史的二维投影误差为 0。若只保留常数基，则 $\hat u_1(t)=2$，平方误差为

$$
\int_0^1\left[(1+2t)-2\right]^2dt
=\int_0^1(2t-1)^2dt
=\frac13.
$$

这展示“增加一个状态坐标消除了本例的一阶趋势误差”，并不证明两个状态足以保存任意历史。

再看 S4 结构计算的最小代数原型。令

$$
M=\operatorname{diag}(2,3),\qquad
u=v=(1,1)^{\mathsf T}.
$$

则

$$
M+uv^{\mathsf T}
=\begin{bmatrix}3&1\\1&4\end{bmatrix}.
$$

Woodbury/Sherman–Morrison 给

$$
\begin{aligned}
(M+uv^{\mathsf T})^{-1}
&=M^{-1}
-\frac{M^{-1}uv^{\mathsf T}M^{-1}}
{1+v^{\mathsf T}M^{-1}u}\\
&=\frac1{11}
\begin{bmatrix}4&-1\\-1&3\end{bmatrix}.
\end{aligned}
$$

直接相乘可得单位阵。这个实数 $2\times2$ 例子只解释“对角逆＋低秩修正”的代数机制；S4 实际 resolvent 还涉及复数频点、离散化、共轭对称和 Cauchy-like kernel。

## 核心公式七问：有限维正交投影

$$
\boxed{
c_n(t)=\langle u,\phi_n^{(t)}\rangle_{L^2(\mu_t)},
\qquad
\hat u_t=\sum_{n=0}^{N-1}c_n(t)\phi_n^{(t)}.
}
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 用 $N$ 个坐标表示历史函数在指定子空间中的最佳近似 |
| 对象 | $\mu_t$ 定义权重，$\phi_n^{(t)}$ 定义坐标，$c_n(t)$ 是状态，$\hat u_t$ 是重构 |
| 来路 | Hilbert 空间正交投影定理：残差与整个候选子空间正交 |
| 步骤 | 先固定测度和正交基，再计算内积系数，最后线性组合重构 |
| 读法 | 状态的每一维记录历史沿一个基函数方向的分量 |
| 检查 | 基必须按声明的测度归一；投影残差应与各基正交；增大嵌套子空间不能增大最佳 $L^2$ 误差 |
| 去路 | HiPPO 寻找能在线更新这些系数的动力学；S4 利用相应矩阵结构高效生成长 kernel |

## 一、先把“记忆”变成数学问题

给定到当前时刻 $t$ 的输入历史 $u|_{[0,t]}$。选定随时间的 measure $\mu_t$ 和一组在 $L^2(\mu_t)$ 中正交归一的 basis

$$
g_0^{(t)},g_1^{(t)},\ldots,g_{N-1}^{(t)}.
$$

用前 $N$ 个系数压缩历史：

$$
c_n(t)=\left\langle u,g_n^{(t)}\right\rangle_{L^2(\mu_t)},\qquad
c(t)=(c_0,\ldots,c_{N-1})^\top.
$$

重构

$$
\hat u_t(s)=\sum_{n=0}^{N-1}c_n(t)g_n^{(t)}(s)
$$

是该 $N$ 维子空间中对 $u$ 的最佳 weighted-$L^2$ approximation。这里“最佳”只比较同一子空间、同一 norm 下的近似，不是下游分类 loss 最小。

## 二、测度定义了记忆偏好

$\mu_t$ 决定过去各处的重要性。例如：

- 滑动窗口 measure：只重视最近固定区间；
- exponentially decaying measure：越旧权重越小；
- scaling measure：把整个 $[0,t]$ 归一到固定参考区间，保留全史但分辨率随时标变化。

改变 measure 就改变内积、正交 basis、投影 coefficients 和“optimality”的目标。不能笼统说某个 HiPPO state 对所有时间尺度都最优。

## 三、为何投影系数形成 ODE

系数依赖 $t$，不仅因为历史增加，也因为 basis/measure 本身随 $t$ 变化。对

$$
c_n(t)=\int u(s)g_n^{(t)}(s)d\mu_t(s)
$$

求导，在合适正则条件和特定 basis/measure 结构下，boundary 新输入项与 basis 变化可整理成

$$
\boxed{\dot c(t)=A(t)c(t)+B(t)u(t).}
$$

某些构造经 time-rescaling 后得到常系数或可高效离散的系统。这一步正是 Hilbert projection 与 state-space model 的桥。

> [!important] 三层对象
> continuum projection coefficients、解析 coefficient ODE、有限步离散 recurrence 是三个对象；基截断、数值离散和有限精度分别带来不同误差。

## 四、一个低阶投影直觉

若在归一化历史区间上用前两个 Legendre-like basis，$c_0$ 近似记录加权平均，$c_1$ 记录一阶趋势。增大 $N$ 可记录更高阶变化，但：

- state 和计算随 $N$ 增加；
- 高频或不光滑历史的有限阶投影仍有误差；
- basis normalization 与区间变换改变矩阵具体数值；
- 投影能重构历史的 norm error，不等于任务需要逐 token 精确检索。

## 五、HiPPO 给了什么，没给什么

HiPPO 原论文形式化 online function approximation，并给出特定 polynomial measures 的 closed-form dynamics。课程采用：

- 在线投影作为有限状态记忆目标；
- 特定构造的 timescale 与 gradient 性质；
- 投影到 recurrent update 的系统路线。

不外推：

- 任意 learned modification 仍保持原 projection optimality；
- 任意 discretization/step size 保持连续保证；
- projection error 小必然使 downstream task error 小；
- state dimension 固定却能逐字无损恢复无限历史。

## 六、从 HiPPO 到可训练 SSM 层

离散 SSM 的 kernel 为

$$
K_j=C\bar A^j\bar B.
$$

若 $A$ 是一般稠密 $N\times N$ 矩阵，直接生成长核或频域 resolvent 的成本与数值条件可能不理想。S4 的核心不只是“用了 SSM”，而是保留/利用 HiPPO 矩阵的特殊结构，使 $A$ 可表示为 normal-plus-low-rank（NPLR），变换基后成为 diagonal-plus-low-rank（DPLR）形式，示意为

$$
A=V(\Lambda-PQ^*)V^*.
$$

这里 $\Lambda$ 对角，$PQ^*$ 是低秩修正，$^*$ 表示共轭转置。具体符号、rank 与校正依 S4 convention；课程只在声明约定后使用。

## 七、为什么“对角＋低秩”有用

生成函数/频域核含 resolvent

$$
C(I-z\bar A)^{-1}\bar B.
$$

对角矩阵的 inverse 可逐元素计算；低秩修正可借 Woodbury identity：

$$
(M+UV^*)^{-1}
=M^{-1}-M^{-1}U(I+V^*M^{-1}U)^{-1}V^*M^{-1}.
$$

这样大 inverse 被约化为对角 inverse、低秩小矩阵 inverse 和 Cauchy-like sums。S4 再在多个频点计算 generating function，经 inverse FFT 得长度 $L$ kernel，用 convolution 训练；流式则可转回 recurrence。

## 八、结构带来效率，也带来数值责任

“结构化”不是把公式写短。需要审计：

- $V$ 的 conditioning 与 complex parameterization；
- 连续 eigenvalues、step size 与离散 poles；
- Cauchy kernel 在接近 poles 时的数值范围；
- conjugate symmetry 如何得到 real output；
- kernel generation、FFT、activation 和 backward 的内存；
- 官方 kernel 与 fallback implementation 的速度差异。

后续 diagonal SSM 变体可进一步简化计算，但“代数更简单”不等于 S4 的理论和经验贡献作废。

## 九、S4 层不只是一个裸线性系统

真实 sequence block 往往包含：

- input/output projection 或 channel mixing；
- SSM convolution/recurrence；
- nonlinearity 与 gating；
- residual connection；
- normalization 和 dropout；
- 多层堆叠。

单个 SSM core 对输入是线性的，不代表整网线性。论文结果应归于完整 architecture、training recipe 和 data，而非仅归因一个 $A$ 矩阵。

## 十、科学空间四篇如何进入课程

| 科学空间文章 | 本节角色 | 课程补严 |
|---|---|---|
| [[S-2024-Su-10114-HiPPO正交函数投影]] | 从 orthogonal projection 推 HiPPO matrix | 加 Hilbert projection 条件 |
| [[S-2024-Su-10137-HiPPO遗留问题]] | 离散化、LegS 性质、Fourier basis | 加稳定域和误差分账 |
| [[S-2024-Su-10162-S4高效计算]] | DPLR/Cauchy 代数推导桥 | 由 S4 原论文核验算法归属 |
| [[S-2024-Su-10180-有理生成函数SSM]] | transfer-function/有理函数拓展 | 区分形式级数、收敛域与实验 |

这组文章的价值是让读者看见数学动机的连续性；正式保证仍回到 HiPPO/S4 原论文和线性代数、数值分析前置章节。

## 十一、图：投影目标到结构化计算

先看图回答：HiPPO 的“最优”发生在左、中栏的哪一个函数空间问题中，S4 又在哪一步把一般稠密计算改造成结构化 kernel？

![[00-知识库管理/_assets/figures/architecture/fig-hippo-s4-projection-structure-v1.svg|900]]

> [!figure] 图 40.2-07　HiPPO 的投影几何、系数 ODE 与 S4 计算路线
> 左栏把历史函数压缩成有限 coefficients；中栏强调 basis/measure 决定 ODE 与 optimality；右栏展示 HiPPO matrix、NPLR/DPLR、resolvent、Cauchy kernel、FFT convolution 的计算链。来源：依据 HiPPO/S4 原论文和科学空间 SSM 系列独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_sequence_ssm_v1.py]] 生成。

**怎样读图**：先在左栏确定历史函数、投影 norm、measure 与有限 basis，再沿中栏追踪 coefficients 怎样形成 ODE，最后沿右栏的 HiPPO matrix、NPLR/DPLR、resolvent、Cauchy kernel 与 FFT convolution 逐步核算结构收益。

**图没有证明什么**：流程图没有给复杂度常数、数值误差或 benchmark 优势，也没有把 projection optimality 等同任务最优。

## 十二、证据分层

- **T / theorem**：指定 measure/subspace 下 orthogonal projection 的最佳近似；HiPPO 原论文特定构造的保证；
- **D / derivation**：本节从 coefficient ODE 到 discretized SSM、从 DPLR 到 resolvent 的课程推导；
- **E / empirical**：S4 论文在当时 benchmark 上的精度/速度；
- **H / hardware**：官方 kernel、FFT/Cauchy 实现及目标设备测量；
- **O / open**：对现代语言任务、极长外推、检索准确与新硬件的普遍结论。

“长距离 benchmark 表现好”不是严格证明模型保留了每个久远 token；应加入 state reconstruction、needle/retrieval、长度外推和扰动实验。

## 十三、常见错误

1. 不声明 measure 就说 HiPPO “最优记忆”；
2. 把有限阶 projection 说成无损保存历史；
3. 混淆连续 projection、ODE、discretization 和 learned layer；
4. 把 S4 简化成“对角矩阵”；
5. 只算 FLOPs，不看 Cauchy/FFT kernel 与 IO；
6. 把裸 SSM core 的线性性外推到整网；
7. 用论文 benchmark 数字作为所有任务/硬件的定理；
8. 把博客高质量推导当成原论文唯一证明来源。

## 十四、掌握标准

> [!summary]
> - HiPPO 把历史记忆定义为指定测度下的在线函数投影；
> - 投影 coefficients 在特定结构下满足线性 ODE；
> - S4 利用 NPLR/DPLR 与 Cauchy-like 计算高效生成长核；
> - 投影最优、结构效率与经验任务结果属于不同证据层；
> - Science Space 提供数学理解主线，原论文负责正式归属和保证。

能解释 measure/basis/coefficient（A）、手算低阶投影和 kernel（B）、推导 coefficient/resolve 结构（C）、纠正“最优/无损/万能”断言（D），并审计 S4 的 kernel、precision、官方实现和证据范围（E）。

## 十五、练习与独立详解

- [[习题 - HiPPO、S4 与结构化长记忆]]
- [[解答 - HiPPO、S4 与结构化长记忆]]

## 参考来源

- [[S-2020-Gu-HiPPO]]
- [[S-2022-Gu-S4]]
- [[S-2024-Su-10114-HiPPO正交函数投影]]
- [[S-2024-Su-10137-HiPPO遗留问题]]
- [[S-2024-Su-10162-S4高效计算]]
- [[S-2024-Su-10180-有理生成函数SSM]]
