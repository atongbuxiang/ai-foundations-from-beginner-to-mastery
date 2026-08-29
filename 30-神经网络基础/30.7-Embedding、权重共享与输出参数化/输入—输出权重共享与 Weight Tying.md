---
type: derivation
status: draft
area: [neural-networks/embedding-output, weight-sharing, language-modeling, parameterization]
aliases: [Input Output Weight Tying, Shared Embedding Matrix]
node_id: NN-51
prerequisites: ["[[Embedding Lookup、稀疏梯度与参数规模]]", "[[Embedding 几何、相似度与各向异性]]", "[[激活、分支、广播与梯度累加]]", "[[矩阵微分、迹技巧与布局约定]]"]
related: ["[[Softmax 输出层、Logit 尺度与概率参数化]]", "[[Softmax Bottleneck 与低秩限制]]", "[[Embedding 初始化、缩放、分解与量化接口]]", "[[参数对称性、等价表示与可辨识边界]]"]
sources: ["[[S-2017-Press-Wolf-Weight-Tying]]", "[[S-2017-Inan-Khosravi-Socher-Weight-Tying]]", "[[S-2023-Su-9698-Output-Embedding]]"]
exercises: ["[[习题 - 输入—输出权重共享与 Weight Tying]]"]
solutions: ["[[解答 - 输入—输出权重共享与 Weight Tying]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-weight-tying-shared-gradient-v2.svg]]"
created: 2026-08-24
updated: 2026-08-29
---

# 输入—输出权重共享与 Weight Tying

> [!abstract] 本章主问题
> Weight tying 不是把两个矩阵“初始化成一样”，而是让输入 lookup 与输出 classifier 引用同一个 Parameter。它可省去一个 $V\times d$ 词表矩阵，却也施加 $U=E$ 的函数约束：同一行既是 token 的输入坐标，又是输出类别 prototype。反向传播必须把 row-sparse lookup VJP 与通常 row-dense output VJP 相加。

## 课程位置与两遍学习路线

- **承接什么：** NN-49 给出 lookup 的 row-sparse VJP，NN-50 说明 rows 的 norm 与方向会影响内积几何；
- **本页解决什么：** 把 input table 与 output classifier 合并为一个 Parameter，并在同一计算图中精确累加稀疏输入路径和稠密输出路径；
- **后续为何需要：** NN-52 的 logit scale、NN-53 的 rank bottleneck 与 NN-56 的初始化/压缩都取决于 tying 是否存在以及中间是否有 projection。

**第一遍只跟踪参数别名。** 画出 $E$ 的两个 use-sites，分别求 $\bar E_{\mathrm{in}}$ 与 $\bar E_{\mathrm{out}}$，最后在唯一 accumulator 中相加。

**第二遍再评估约束。** 比较 untied、direct tied、projected tied 的函数类、尺度、bias、词表对齐、optimizer state、checkpoint alias 与分布式 sharding。

### 问题链

1. “两个矩阵数值相同”为什么不等于“两个模块共享同一个 Parameter”？
2. direct tying 对 $d_e,d_h$ 和 token-to-row 身份提出什么条件？
3. lookup 路径为何 row-sparse，而 Softmax output 路径通常 row-dense？
4. 两条路径在同一 row 上相长或相消时，autograd 应怎样处理？
5. 省去 $Vd$ 参数为何同时改变函数类、梯度统计和词表表面的系统布局？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal E_\square$ 中把 lookup 梯度 $S^{\mathsf T}G$ 与 output 梯度 $\delta h^{\mathsf T}$ 相加，并说明未被 lookup 的第 0、3 行为何仍会更新，就已掌握本页主干。

## 符号与对象账本

| 对象 | untied | direct tied | projected tied |
|---|---|---|---|
| input table | $E\in\mathbb R^{V\times d_e}$ | shared $E\in\mathbb R^{V\times d}$ | shared $E\in\mathbb R^{V\times d_e}$ |
| output table | $U\in\mathbb R^{V\times d_h}$ | $U=E$ | effective $U=EP$ |
| hidden interface | $h\in\mathbb R^{d_h}$ | $d_h=d_e=d$ | $Ph\in\mathbb R^{d_e}$ |
| optimizer state | 两个 Parameter | 一个 Parameter | $E$ 与 $P$ |
| 函数约束 | 两空间独立 | prototype 即 input row | prototype 位于 $E$ 经 projection 的族 |

### 贯穿算例 $\mathcal E_\square$：稀疏 lookup 与稠密 output 在同一表相加

沿用 NN-49 的 $E,I,G$，故输入路径已经给出

$$
\bar E_{\mathrm{in}}
=
\begin{bmatrix}
0&0\\
-1&1/2\\
4&1\\
0&0
\end{bmatrix}.
$$

令共享输出端接收

$$
h=(1,1)^{\mathsf T},
\qquad b=0,
\qquad y=3.
$$

则

$$
z=Eh=(1,1,1,2)^{\mathsf T}.
$$

记 $D=3+\mathrm e$，Softmax–cross-entropy 的 logit gradient 为

$$
\delta=p-q_3
=\frac1D(1,1,1,-3)^{\mathsf T}.
$$

因此输出 use-site 贡献

$$
\bar E_{\mathrm{out}}
=\delta h^{\mathsf T}
=\frac1D
\begin{bmatrix}
1&1\\1&1\\1&1\\-3&-3
\end{bmatrix}.
$$

共享 Parameter 的最终梯度不是二选一，而是

$$
\boxed{
\bar E
=\bar E_{\mathrm{in}}+\bar E_{\mathrm{out}}
=
\begin{bmatrix}
D^{-1}&D^{-1}\\
-1+D^{-1}&1/2+D^{-1}\\
4+D^{-1}&1+D^{-1}\\
-3D^{-1}&-3D^{-1}
\end{bmatrix}
}.
$$

数值上 $D^{-1}\approx0.174878$。第 0、3 行未被本次 lookup 访问，却因 output normalization 获得非零梯度；第 1 行两种角色在第一坐标部分相消。这正是 tying 破坏“整表更新稀疏性”的最小证据。

## 核心公式七问：共享参数的 Use-Site 求和

$$
\boxed{
\bar E=\sum_{u\in\operatorname{uses}(E)}\operatorname{VJP}_u(\bar y_u)
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 正确处理同一 Parameter 在多个计算路径上的责任 |
| 对象 | 参数身份，不是两个恰好数值相等的 arrays |
| 来路 | 全微分中每个 use-site 的 $dE$ 系数必须合并 |
| 步骤 | 逐 use-site 求 VJP→对齐 shape/device→在同一 accumulator 求和→一次 optimizer update |
| 读法 | 参数只更新一次，但更新方向包含所有角色的联合信号 |
| 检查 | object identity、梯度 hook、untied ablation、词表映射与 checkpoint reload |
| 去路 | tied language-model head、多任务共享、ALBERT 参数共享与共享专家 |

### AI / 系统对应

大词表语言模型中，tying 可同时减少参数、optimizer state 与通信量，但 output matmul 仍读取整表；若分片策略让 lookup 按 rows、output projection 按 columns 分布，共享 Parameter 还会制造布局冲突。工程验收必须检查内存别名、梯度累加和 checkpoint 恢复后的真实身份。

## 一、学习目标

读完本节，你应能：

1. 写出 untied/tied 输入与输出矩阵的 shape；
2. 计算 direct tying 与带 projection tying 的参数节省；
3. 推导共享矩阵的 input/output 两条梯度；
4. 用数值例子展示同一 row 的相长、相消与稠密更新；
5. 区分真正参数共享、数值复制与初始化相等；
6. 解释 tying 对函数类、几何、稀疏性和 optimizer state 的影响；
7. 审计词表身份、维度、bias、初始化尺度和 checkpoint；
8. 把论文经验限制在模型与协议范围内。

## 二、Untied 语言模型头

设词表大小 $V$、输入 embedding dimension $d_e$、hidden dimension $d_h$。输入表

$$
E\in\mathbb R^{V\times d_e}
$$

把 token $i$ 编码为

$$
x_i=E^\mathsf Tq_i\in\mathbb R^{d_e}.
$$

输出矩阵

$$
U\in\mathbb R^{V\times d_h},
\qquad
b\in\mathbb R^V
$$

把 hidden state $h\in\mathbb R^{d_h}$ 变成

$$
\boxed{z=Uh+b\in\mathbb R^V}.
$$

untied 情况下，$E$ 与 $U$ 是两个独立参数；输入 token 的表示和输出 class prototypes 可自由演化。

## 三、Direct Weight Tying

若

$$
d_e=d_h=d
$$

且输入/输出使用同一 token-to-row 映射，可施加

$$
\boxed{U=E}.
$$

此时

$$
x_i=E^\mathsf Tq_i,
$$

$$
\boxed{z=Eh+b}.
$$

第 $j$ 类 logit 是

$$
z_j=e_j^\mathsf Th+b_j.
$$

所以 $e_j$ 同时承担：

- 输入端：token $j$ 的连续坐标；
- 输出端：检测 hidden state 与类别 $j$ 匹配程度的线性 prototype。

这是参数约束，不只是存储优化。

## 四、参数计数

维度相等时，untied 词表参数为

$$
N_{\mathrm{untied}}
=Vd+Vd+V
=2Vd+V,
$$

其中最后 $V$ 是 output bias。tied 为

$$
N_{\mathrm{tied}}=Vd+V.
$$

节省

$$
\boxed{Vd}
$$

个参数。

例：$V=50{,}000,d=1024$，节省

$$
51.2\ \text{million parameters}.
$$

若按 2-byte 权重存储，单权重副本约省 102.4 MB；训练时 optimizer state 的节省可能更大，但依 precision、sharding 和 optimizer 而定。

## 五、维度不等时的 projection tying

若 $d_h\ne d_e=d$，可加入

$$
P\in\mathbb R^{d\times d_h},
$$

写成

$$
\boxed{z=EPh+b}.
$$

令

$$
r=Ph\in\mathbb R^d,
$$

输出仍用 $E$ 的 rows 与 $r$ 配对。参数数目为

$$
Vd+dd_h+V.
$$

相对 untied 的 $Vd+Vd_h+V$，节省

$$
Vd_h-dd_h=d_h(V-d).
$$

只有当 $V>d$ 时才是正节省。projection 还改变输出几何和 rank，不能只看参数数目。

## 六、输入路径的梯度

对单个 lookup

$$
x_i=E^\mathsf Tq_i,
$$

若上游梯度为 $g_x\in\mathbb R^d$，则

$$
\boxed{
\nabla_E^{\mathrm{in}}\mathcal L
=q_i g_x^\mathsf T
}.
$$

只有第 $i$ 行非零；多个输入位置按 row scatter-add。

## 七、输出路径的梯度

direct tied head 为

$$
z=Eh+b.
$$

令 logit gradient

$$
\delta=\nabla_z\mathcal L\in\mathbb R^V.
$$

微分

$$
dz=dE\,h+E\,dh+db.
$$

所以

$$
\boxed{
\nabla_E^{\mathrm{out}}\mathcal L
=\delta h^\mathsf T
}.
$$

对 softmax cross-entropy，

$$
\delta=p-y.
$$

只要 $p_j>0$ 且 $h\ne0$，几乎所有输出 rows 都有非零梯度。输出使用因此通常是 row-dense。

同时

$$
\nabla_h\mathcal L=E^\mathsf T\delta,
\qquad
\nabla_b\mathcal L=\delta.
$$

## 八、共享参数的总梯度

若 $E$ 在同一计算图被使用多次，autograd 的基本规则是：每条 use-site VJP 在 shared accumulator 相加。

$$
\boxed{
\nabla_E\mathcal L
=\nabla_E^{\mathrm{in}}\mathcal L
+\nabla_E^{\mathrm{out}}\mathcal L
+\cdots
}.
$$

省略号包括序列中其他 lookup、辅助 head、regularizer 等。不能先更新 input $E$、再独立更新 output $U$；它们已经是一个参数对象。

## 九、三类数值手算

取 $V=3,d=2$，当前 input token 为 $i=1$，

$$
g_x=(0.2,-0.1),
$$

$$
h=(2,-1),
$$

$$
\delta=p-y=(0.1,-0.7,0.6).
$$

输入贡献：

$$
\nabla_E^{\mathrm{in}}
=
\begin{bmatrix}
0&0\\
0.2&-0.1\\
0&0
\end{bmatrix}.
$$

输出贡献：

$$
\nabla_E^{\mathrm{out}}
=\delta h^\mathsf T
=
\begin{bmatrix}
0.2&-0.1\\
-1.4&0.7\\
1.2&-0.6
\end{bmatrix}.
$$

总梯度：

$$
\boxed{
\nabla_E
=
\begin{bmatrix}
0.2&-0.1\\
-1.2&0.6\\
1.2&-0.6
\end{bmatrix}
}.
$$

第 1 行的 input 与 output contribution 部分相消；未作为 input 出现的 rows 0、2 仍由 output head 更新。这一个例子同时证明“共享梯度相加”和“lookup 稀疏性可被输出使用破坏”。

## 十、梯度冲突与协同

可用

$$
\cos\phi
=\frac{\langle g_{\mathrm{in}},g_{\mathrm{out}}\rangle}
{\|g_{\mathrm{in}}\|\|g_{\mathrm{out}}\|}
$$

诊断两种角色在某 row 或整个矩阵上的方向：

- $\cos\phi>0$：局部协同；
- $\cos\phi<0$：局部冲突/相消；
- 一条 norm 远大于另一条：共享参数主要由强路径塑形。

这只是 optimization diagnostic，不直接等于泛化。per-token row、频率 bucket、训练阶段与 layer norm/scale 都可能改变结果。

## 十一、Tying 改变函数类

untied 可独立选择 $E,U$；tied 必须满足

$$
U=E.
$$

因此 tied parameter set 是 untied parameter set 的子集。它可能：

- 作为结构正则减少过拟合；
- 让输入统计帮助稀有 output rows；
- 让输出稠密梯度训练很少被输入访问的 rows；
- 也可能因角色冲突降低适配能力。

“参数更少”不自动说明更高效或更准；必须同时测 loss、校准、吞吐、内存与任务表现。

## 十二、Tying 对几何的约束

untied 时，input space 可做 $A$ 重参数化并由后层逆变换补偿，而 output prototypes 独立。direct tying 要让同一 $E$ 同时满足两端，减少了这种自由度。

输出 logit

$$
z_j=\|e_j\|\|h\|\cos\theta_j+b_j
$$

把 row norm、hidden norm 和 angle 耦合。若 unit-normalize $E$ 或 $h$，就改变 output probability family；这不是纯可视化后处理。

## 十三、初始化与 logit variance

若 $e_{jk}$ 与 $h_k$ 近似独立、零均值，

$$
\operatorname{Var}(e_{jk})=\sigma_E^2,
\qquad
\operatorname{Var}(h_k)=q_h,
$$

则

$$
\operatorname{Var}(z_j)
\approx d\sigma_E^2q_h.
$$

输入 lookup 希望的 row scale 不必等于 output logits 希望的 scale。科学空间对 output embedding 的重访正是在提醒：直接复用参数不自动对齐两种尺度合同。可选 projection、normalization、显式 logit scale 或适配初始化，但每种都会改变梯度和函数。

## 十四、Bias、词表与特殊 token

通常只共享 weight，不共享 output bias：

$$
z=Eh+b.
$$

$b_j$ 可独立表达类别基线。若输入/输出词表不完全相同，例如翻译源/目标语言、不同 tokenizer、增加 output-only symbols，则 direct row-wise tying 未定义，除非先给出明确 row alignment 或 partial tying。

padding row 即使 input lookup 不更新，也可能经 output head 得到梯度；若 PAD 不应成为可预测类别，还需 output mask，而不是只设 `padding_idx`。

## 十五、实现：共享、复制与别名

三种代码语义不同：

1. **同一 Parameter**：两处模块引用相同对象，只有一个 gradient/optimizer state；
2. **初始化复制**：$U\leftarrow E$ 后仍为两个参数，下一步即分离；
3. **底层 storage alias**：可能绕过框架的 parameter 注册、state dict 或 optimizer 假设。

验收应检查：

- object identity/storage pointer；
- optimizer parameter list 是否只登记一次；
- checkpoint load 后是否仍 tied；
- quantization/sharding 是否保持共享；
- compiler 是否复制或 materialize；
- transpose/layout 是否符合输出 kernel。

## 十六、原始论文证据边界

Press–Wolf 与 Inan–Khosravi–Socher 在 2017 年的语言模型设置中给出 tying 的分析与经验支持。可靠转述是：

- output matrix 可作为 embedding 分析；
- tying 减少大词表参数；
- 在论文模型与协议中改善了若干结果。

不能无条件写成：现代任意 tokenizer/Transformer/多语言模型 tying 必然更优。模型 scale、norm、bias、projection、optimizer 与数据都会改变结论。

## 十七、图：共享矩阵与梯度求和

先看图回答：输入端为何只触及一行，输出端为何通常触及所有行？direct tying 需要哪个维度条件？参数节省为什么同时意味着函数约束？

![[00-知识库管理/_assets/figures/neural-networks/fig-weight-tying-shared-gradient-v2.svg|900]]

> [!figure] 图 30.7-03　Weight Tying 的双角色、共享 VJP 与参数账本
> 左栏把 input lookup 和 output projection 接到同一 $E$；中栏展示 row-sparse input gradient 与 row-dense output gradient 的相加；右栏比较 untied、direct tied 和 projection tied。来源：依据 Press–Wolf 2017、Inan et al. 2017 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_embedding_output_foundations_v2.py]] 确定性生成。

**怎样读图**：先核对 $V,d,d_h$，再沿两个 use sites 做 VJP，最后检查共享是否在 optimizer、checkpoint、sharding 与推理图中仍然真实存在。

**图没有证明什么**：图不证明 tying 在所有模型上降低 perplexity，也不证明减少参数不会带来表达、尺度或优化代价。

## 十八、最小验收

1. 写出 untied/tied/projection-tied 的 shape 与前向式；
2. 推导三种参数计数；
3. 推导 input/output gradient；
4. 复算 $V=3,d=2$ 的共享梯度；
5. 解释 row-sparse 为何变 dense；
6. 分析函数类、几何与初始化尺度；
7. 区分 Parameter sharing、copy 与 storage alias；
8. 设计跨 tokenizer/scale 的公平消融。

> [!summary]
> Weight tying 是一个计算图与参数化约束：一个矩阵承受输入编码和输出分类两种角色，所有 VJP 在同一 accumulator 求和。它节省词表规模参数，也改变稀疏性、几何、初始化和函数类。只有同时写清 shape、梯度与系统别名，才算真正理解“共享”。

- [[Embedding、权重共享与输出参数化 MOC]]
- [[习题 - 输入—输出权重共享与 Weight Tying]]
- [[解答 - 输入—输出权重共享与 Weight Tying]]
