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
updated: 2026-08-23
---
# Maxout、分段线性区域与条件计算

> [!abstract] 本章主问题
> Maxout 单元从 $k$ 个 learned affine candidates 中取最大值，因此单个单元就是 convex piecewise-linear upper envelope。winner 决定局部梯度，tie 决定不可微边界。它扩大 region 与参数预算，但“只选一个输出”并不表示前向无需计算全部 candidates。

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
