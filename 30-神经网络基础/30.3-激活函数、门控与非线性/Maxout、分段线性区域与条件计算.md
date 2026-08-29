---
type: concept
status: draft
area: [neural-networks/activations, maxout, conditional-computation]
aliases: [Maxout Networks, Max-Affine Units]
node_id: NN-23
prerequisites: ["[[ReLU、Leaky ReLU 与次梯度约定]]", "[[凸函数、Jensen 不等式与上图集]]", "[[次梯度、共轭函数与 Fenchel 对偶]]"]
related: ["[[深度分离、线性区域与表达效率]]", "[[激活函数的数值稳定、尺度与经验选择]]"]
sources: ["[[S-2013-Goodfellow-Maxout-Networks]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]"]
exercises: ["[[习题 - Maxout、分段线性区域与条件计算]]"]
solutions: ["[[解答 - Maxout、分段线性区域与条件计算]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-maxout-upper-envelope-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---
# Maxout、分段线性区域与条件计算

> [!abstract] 本章主问题
> Maxout 单元从 $k$ 个 learned affine candidates 中取最大值，因此单个单元就是 convex piecewise-linear upper envelope。winner 决定局部梯度，tie 决定不可微边界。它扩大 region 与参数预算，但“只选一个输出”并不表示前向无需计算全部 candidates。

## 课程位置与两遍学习路线

- **承接什么：** NN-22 用连续乘法让两条 branches 共同决定输出；Maxout 改为先计算多条 affine candidates，再由 hard winner 选择局部公式；
- **本页解决什么：** 从 upper envelope 推出 convex PWA、winner gradient、tie subdifferential 与 dense-compute/conditional-routing 边界；
- **后续为何需要：** NN-24 会把候选数 $k$ 的表达收益与参数、MAC、winner starvation 和统计证据共同审计。

**第一遍只找 winner。** 对每个输入列出全部 candidates、最大值、winner 与局部 slope；遇到 tie 单独标记，不强行写唯一 gradient。

**第二遍再看几何与系统。** 推导 polyhedral regions、subdifferential、candidate permutation invariance、dense candidate cost 与真正 sparse conditional compute 的差异。

### 问题链

1. pointwise maximum 为什么生成 convex piecewise-affine function？
2. unique winner 时梯度为何等于该 affine candidate 的 slope？
3. tie 点为何只有 directional derivative/subdifferential，而没有唯一 Fréchet derivative？
4. 输出只保留 winner，为什么 forward 通常仍需计算全部 $k$ 个 candidates？
5. candidate 长期不获胜时，参数学习会发生什么？

> [!check] 第一遍停靠线
> 若你能在 $s_\triangle$ 上找出三个 winner、输出 $(2,0.5,2)$ 与 slope $(-1,0,1)$，并解释这不等于跳过其他候选计算，就可以进入经验选择；tie 几何留到第二遍。

## 符号与对象账本

| 对象 | 类型 | 在 AI Maxout 单元中的身份 | 关键边界 |
|---|---|---|---|
| $a_r(x)=w_r^Tx+b_r$ | affine candidate | 候选局部专家 | 先计算才知道 winner |
| $h(x)=\max_ra_r(x)$ | upper envelope | unit output | 单个 unit convex |
| $r^*(x)$ | winner index | backward route/cache | 接近 tie 时不稳定 |
| $A(x)$ | active/tied set | subgradient vertices | tie 时无唯一 gradient |
| winner frequency/margin | empirical diagnostics | starvation 与稳定性证据 | 不等于部署加速 |

### 贯穿算例：三个 affine candidates 的硬选择

沿用 $s_\triangle=(-2,0,2)$，取

$$
a_1(s)=s,\qquad a_2(s)=-s,\qquad a_3(s)=0.5.
$$

逐点 candidate vectors 为 $(-2,2,0.5)$、$(0,0,0.5)$、$(2,-2,0.5)$，因此

$$
h(s_\triangle)=(2,0.5,2),\qquad r^*(s_\triangle)=(2,3,1),\qquad h'(s_\triangle)=(-1,0,1).
$$

三个 probe 都有 unique winner，故局部 slope 明确；但在 $s=\pm0.5$ 等边界会出现 tie，需要 subdifferential 或程序 convention。即使最终只保留三个 winner，dense forward 仍计算了九个 candidate scores。

## 核心公式七问：$h(x)=\max_{1\le r\le k}(w_r^Tx+b_r)$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 从多个 learned affine pieces 中按输入选择局部响应 |
| 对象 | $k$ 个 affine candidates、winner set 与 scalar/unit output |
| 来路 | pointwise maximum/upper-envelope construction |
| 步骤 | 先全部求值，再 reduce max 并缓存 winner；reverse 将 cotangent 路由给 active candidates |
| 读法 | 输入空间被 candidate dominance inequalities 划成 polyhedral regions |
| 检查 | $k=2$ 且 candidates 为 $0,x$ 时得到 ReLU；tie 时不得写唯一 slope |
| 去路 | max-affine splines、mixture routing、winner starvation、region counts 与 conditional compute |

## 一、定义与 Shape

对输入 $x\in\mathbb R^d$，一个 rank-$k$ maxout unit 为

$$
h(x)=\max_{r\in\{1,\ldots,k\}}(w_r^Tx+b_r).
$$

输出 $m$ 个 units 时，权重可记为 $W:[m,k,d]$、bias $b:[m,k]$；先形成 $[B,m,k]$ candidates，再沿 $k$ 轴 reduce max，得到 $[B,m]$。

## 二、Convex Piecewise-Affine 结构

affine functions 的 pointwise maximum 是 convex：

$$
h(tx+(1-t)y)\le th(x)+(1-t)h(y).
$$

每个 winner region 由线性不等式

$$
(w_r-w_s)^Tx\ge b_s-b_r
$$

的交定义，因此是 polyhedron；在其内部 $h=w_r^Tx+b_r$。并非每个 candidate 都一定在 upper envelope 上出现。

## 三、梯度、Tie 与 Directional Derivative

若唯一 winner 为 $r^*$，则

$$
\nabla h(x)=w_{r^*}.
$$

若 active set $A(x)$ 含多个 ties，convex subdifferential 为

$$
\partial h(x)=\operatorname{conv}\{w_r:r\in A(x)\}.
$$

directional derivative 是

$$
h'(x;v)=\max_{r\in A(x)}w_r^Tv,
$$

它通常不是 $v$ 的线性函数，所以 tie 点没有 Fréchet derivative。框架的 first-winner 或 equal-split 只是 VJP convention。

## 四、ReLU 是 Maxout 特例

$$
\operatorname{ReLU}(x)=\max(0,x)
$$

是 $k=2$、两个 affine candidates 为 0 与 $x$ 的固定 maxout。learned maxout 同时学习斜率与截距，可形成更一般的 convex PWL unit。

## 五、网络何时不再 Convex

单个 maxout unit 对输入 convex，但后续若以负权组合、再做多层复合，整体一般非convex。例如 $|x|=\max(x,-x)$ convex，而 $-|x|$ 用负 output weight 即 concave。不能把 unit-level convexity 外推给 loss landscape。

## 六、表达、区域与预算

$k$ 增加候选 pieces 和局部选择能力，也把第一投影参数/MAC/activation storage 近似乘 $k$。region 数不等于 $k^m$ 的自动实现：候选可能永不获胜，不同 units 的 partitions 也受几何约束。

## 七、条件计算的误区

常规 dense 实现必须先计算全部 $k$ 个 affine candidates 才知道 winner；只在 backward 把梯度路由给 winner，并不节省 forward GEMM。真正 conditional compute 需要预路由、稀疏专家或专用 kernel，同时处理 load balance 与通信。

## 八、Winner Starvation 与 Tie 稳定性

长期不获胜的 candidate 接收零参数梯度，可能出现 winner starvation。接近 tie 时，小输入/舍入扰动可切换 winner，函数值连续但 gradient 跳变。应报告 winner frequency、margin（第一与第二 candidate 差值）和 dead-candidate rate。

### 把 tie 算清：不可导不等于无法分析

对贯穿算例，$a_1=a_3$ 发生在 $s=0.5$，$a_2=a_3$ 发生在 $s=-0.5$。以 $s=0.5$ 为例，active slopes 是 $\{1,0\}$，所以

$$
\partial h(0.5)=[0,1],
\qquad
h'(0.5;v)=\max(v,0).
$$

当 $v>0$ 时，向右移动会进入 $a_1$ 的区域，方向导数是 $v$；当 $v<0$ 时，向左移动仍由常数候选 $a_3$ 获胜，方向导数是 $0$。因为 $\max(v,0)$ 不是 $v$ 的线性函数，这里不存在唯一的 Fréchet derivative。

> [!warning] 程序返回的一个数不是新定理
> 若框架在 tie 时返回 slope $1$、$0$ 或平分值，它实现的是一条 backward convention。它可以是合法的 subgradient，却不会让原函数在 tie 点变得可导。

### 一张最小 winner 审计表

| probe | top-1 | top-2 | margin | 反向路由 |
|---|---:|---:|---:|---|
| $s=-2$ | $a_2=2$ | $a_3=0.5$ | $1.5$ | 只给 $a_2$ |
| $s=0$ | $a_3=0.5$ | $a_1=a_2=0$ | $0.5$ | 只给 $a_3$ |
| $s=2$ | $a_1=2$ | $a_3=0.5$ | $1.5$ | 只给 $a_1$ |

margin 比 winner index 多回答一个问题：路由离切换边界有多远。训练时若大量样本 margin 接近零，即使各 candidate 的 winner frequency 看似均衡，gradient routing 仍可能对量化和微小扰动敏感。

## 九、图：Upper Envelope 与梯度路由

先看图回答：为什么输出只保留一条线，却仍需计算全部候选？

![[00-知识库管理/_assets/figures/neural-networks/fig-maxout-upper-envelope-v2.svg|900]]

> [!figure] 图 30.3-07　Maxout：upper envelope、polyhedral regions 与 winner ledger
> 左栏画多条 affine candidates 及 upper envelope；中栏把 input space 分成 winner regions/tie boundaries；右栏区分 dense candidate compute、winner VJP 与真正 conditional execution。来源：依据 Goodfellow 等 2013 原论文及教材独立绘制；由 [[00-知识库管理/_labs/code/plot_activation_advanced_v2.py]] 确定性生成。

**怎样读图**：先看所有候选都被计算，再看 max 选择改变局部 affine map，最后区分 gradient routing 与 compute skipping。

**图没有证明什么**：图没有给出高维 region 数的精确公式，也没有证明 maxout+dropout 的旧 benchmark 优势可迁移到现代架构。

## 十、验收与回顾

测试 unique winner gradient、tie convention、重复最大值、candidate permutation invariance、winner margin、dead candidates、参数/MAC/bytes 与 fused reduction。对 finite difference 避开 tie，tie 处只审计程序规则。

> [!summary]
> Maxout 是 learned max-affine upper envelope：局部 winner 给梯度，ties 给 subdifferential，$k$ 同时增加表达与成本。梯度稀疏不等于前向条件计算。

- [[习题 - Maxout、分段线性区域与条件计算]]
- [[解答 - Maxout、分段线性区域与条件计算]]
