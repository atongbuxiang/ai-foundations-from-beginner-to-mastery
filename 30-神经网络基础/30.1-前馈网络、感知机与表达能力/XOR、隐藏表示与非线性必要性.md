---
type: concept
status: draft
area: [neural-networks/feedforward, nonlinear-representation, xor]
aliases: [XOR Problem, 非线性必要性, Hidden Representation]
node_id: NN-05
prerequisites: ["[[人工神经元、仿射变换与决策超平面]]", "[[多层感知机与逐层前向计算]]", "[[凸集、凸组合与分离超平面]]"]
related: ["[[万能逼近定理、紧集与逼近误差]]", "[[深度分离、线性区域与表达效率]]", "[[表示学习的任务、表示与下游风险]]"]
sources: ["[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Zhang-Lipton-Li-Smola-D2L]]"]
exercises: ["[[习题 - XOR、隐藏表示与非线性必要性]]"]
solutions: ["[[解答 - XOR、隐藏表示与非线性必要性]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-xor-hidden-representation-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# XOR、隐藏表示与非线性必要性

> [!abstract] 本章主问题
> XOR 是最小但不肤浅的反例：四个点无法由输入空间中的一个超平面分开，却能被一个很小的非线性网络精确表示。真正发生的不是“神经元变聪明”，而是隐藏层先把输入重编码，使原先不可线性分离的类别在新表示中可被线性读出。

## 一、学习目标

完成本章后，应能：

1. 写出 XOR 真值表和二维点集；
2. 用不等式或 convex hull 证明 XOR 不线性可分；
3. 证明任意多层 affine-only 网络仍是 affine；
4. 手算一个 ReLU 网络精确实现 XOR；
5. 解释 activation pattern 怎样划分输入空间；
6. 区分“有限四点被拟合”与“在整个区域上表示某函数”；
7. 说明 hidden representation 如何改变可分性；
8. 区分非线性是必要条件与某种具体 activation 是唯一选择；
9. 识别表示压缩、碰撞和信息丢失；
10. 把 XOR 迁移到 embedding probe、feature engineering 与网络调试。

## 二、XOR 对象合同

取 $x_1,x_2\in\{0,1\}$，XOR 标签为“两个 bit 恰有一个为 1”：

| $x_1$ | $x_2$ | $y=x_1\oplus x_2$ |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

几何上，两个正类位于单位正方形的一条对角线，两个负类位于另一条对角线。单个 affine score 加 threshold 只能用一条直线分两侧。

## 三、不等式证明：一个超平面不可能完成 XOR

假设存在 $w_1,w_2,b$，并用正 score 表示 $y=1$。四点要求

$$
\begin{aligned}
b&<0 && (0,0)\text{ 为负类},\\
w_1+b&>0 && (1,0)\text{ 为正类},\\
w_2+b&>0 && (0,1)\text{ 为正类},\\
w_1+w_2+b&<0 && (1,1)\text{ 为负类}.
\end{aligned}
$$

中间两式相加给

$$
w_1+w_2+2b>0.
$$

第一式 $b<0$ 因而推出 $w_1+w_2+b>0$，与最后一式矛盾。所以不存在这样的超平面。

## 四、Convex Hull 证明

正类 convex hull 是连接 $(1,0)$ 与 $(0,1)$ 的线段；负类 convex hull 是连接 $(0,0)$ 与 $(1,1)$ 的线段。它们都包含中心点 $(1/2,1/2)$。

若两个有限点集能被严格超平面分离，它们的 convex hull 也必须落在超平面的两侧，因此 convex hull 不能相交。此处相交，故严格线性分离不可能。这个证明比四条不等式更容易推广到高维。

## 五、多层线性为什么仍然无能为力

若 activation 都是 identity，两层网络为

$$
f(x)=(xW^{(1)}+b^{(1)})W^{(2)}+b^{(2)}
=xW_{\rm eff}+b_{\rm eff}.
$$

仿射映射复合仍为仿射；任意增加 depth 或 width 都不能打破这个闭包。因此：

> [!important]
> 多层结构本身不产生非线性表达力；必须在层间插入不与 affine 复合闭合的运算。

Normalization、multiplicative gate、max 或 attention 也可能引入非线性；“必须使用 ReLU”不是结论。

## 六、一个精确的 ReLU 构造

令 $s=x_1+x_2\in\{0,1,2\}$，定义

$$
\boxed{
f(x_1,x_2)
=\operatorname{ReLU}(s)
-2\operatorname{ReLU}(s-1)
+\operatorname{ReLU}(s-2).
}
$$

逐点检查：

| $s$ | 三个 hidden activations | $f$ |
|---:|---|---:|
| 0 | $(0,0,0)$ | 0 |
| 1 | $(1,0,0)$ | 1 |
| 2 | $(2,1,0)$ | $2-2=0$ |

所以对四个 binary inputs，$f=x_1\oplus x_2$。这里第一层三个神经元共享方向 $(1,1)$，bias 分别为 $0,-1,-2$；输出权重为 $(1,-2,1)^\top$。

## 七、构造在连续区域上表示什么

对 $s\in\mathbb R$，上式是一个 triangular hat：

$$
f(s)=
\begin{cases}
0,&s\le0,\\
s,&0<s\le1,\\
2-s,&1<s\le2,\\
0,&s>2.
\end{cases}
$$

它不仅记住四点，还在 $x_1+x_2$ 方向上定义了连续分段线性延拓。但训练数据只规定四点标签；选择哪种区域外延拓属于 inductive bias，而不是 XOR 表自动给出的真理。

## 八、隐藏表示怎样改变可分性

令

$$
h(x)=
\begin{bmatrix}
\operatorname{ReLU}(s)\\
\operatorname{ReLU}(s-1)\\
\operatorname{ReLU}(s-2)
\end{bmatrix}.
$$

原输入空间的四点经 $h$ 变为

$$
(0,0,0),\quad(1,0,0),\quad(1,0,0),\quad(2,1,0).
$$

输出层用 $v=(1,-2,1)$ 线性读出。两个正类输入虽不同，却被映到同一 representation；这是有意丢弃“哪个 bit 为 1”的信息，只保留 XOR 任务所需信息。

## 九、Activation Pattern 与线性区域

ReLU 网络对每个神经元记录 $z_j>0$ 或 $z_j\le0$。在 activation pattern 固定的区域内，ReLU 等于固定 diagonal mask，整个网络退化为 affine map；跨越 $z_j=0$ 的边界时 mask 改变，局部 affine 公式也改变。

所以 ReLU 网络的全局非线性来自许多局部 affine pieces 的拼接，而非每个区域内部突然失去线性代数结构。

## 十、有限样本拟合不等于全局函数相等

对四个 XOR 点，有无穷多个函数都给相同标签：triangular hat、smooth sigmoid approximation、最近邻规则甚至 lookup table。它们在 $[0,1]^2$ 内部和区域外行为不同。

因此必须区分：

- training interpolation：只在观察点相等；
- domain equality：对声明域的所有输入相等；
- approximation：在某 norm 下误差小；
- classification agreement：只要求 threshold 后标签相同。

后续万能逼近定理讨论第三种，而不是有限点记忆。

## 十一、非线性也会丢失信息

ReLU 把所有负 pre-activation 压到 0；sigmoid 在大幅度区域近饱和；max 只保留获胜分支。因此 hidden representation 通常不是可逆变换。

信息丢失可以是优点：去掉与任务无关的变化；也可以是缺陷：两个本应区别的输入发生 representation collision。是否“好”必须相对于下游任务和数据分布判断。

## 十二、图：先折叠，再线性读出

先看图回答：原空间中的哪一种几何障碍，被 hidden map 改写成了可线性读出的坐标差？

![[00-知识库管理/_assets/figures/neural-networks/fig-xor-hidden-representation-v2.svg|900]]

> [!figure] 图 30.1-05　XOR 的不可分几何、ReLU hat 构造与隐藏表示
> 左栏用相交 convex hull 证明单超平面失败；中栏展示三个 ReLU hinge 拼成 triangular hat；右栏跟踪四个输入进入 hidden space 后如何被线性读出。来源：依据 Goodfellow–Bengio–Courville 与 D2L 的 XOR/MLP 教学结构独立绘制；由 [[00-知识库管理/_labs/code/plot_feedforward_expressivity_v2.py]] 确定性生成。

**怎样读图**：先确认原空间不存在严格分隔线，再按 $s=0,1,2$ 读取 hidden activation，最后检查输出权重怎样组合三个 hinge。

**图没有证明什么**：图没有证明任意非线性网络都能训练成功、该构造在噪声数据上泛化，或三单元是所有允许 activation/parameterization 下的唯一最小结构。

## 十三、AI 中的迁移

- linear probe 失败可能是表示中任务不可线性读出，而非标签没有规律；
- nonlinear probe 成功只说明更大 probe class 能拟合，不能自动归功于 encoder；
- Transformer FFN 用逐 token 非线性改变 feature geometry；
- gating 通过乘法产生 affine-only 网络无法生成的交互项；
- feature crossing 可把 XOR 类关系显式加入输入，但等于人工选择隐藏表示。

## 十四、常见错误

1. 只画四点，不给不可分证明；
2. 认为多放几层 identity 就能解决 XOR；
3. 把 ReLU 构造只在四点成立误说成唯一连续 XOR；
4. 把 hidden representation 当可逆坐标变换；
5. 把 nonlinear probe 的成功当 encoder 表示必然优越；
6. 把表达存在性当 optimization/generalization 保证；
7. 认为 XOR 证明某种 activation 对所有任务最好。

## 十五、本节回顾与掌握标准

> [!summary]
> - XOR 的两类 convex hull 相交，故单超平面不能严格分离；
> - affine-only 深网仍是 affine；
> - ReLU hinge 的线性组合能精确表示 binary XOR；
> - hidden layer 通过改变表示，使新的线性读出成为可能；
> - 有限点拟合、全域相等和 norm approximation 是不同命题。

能证明不可分（A/C）、手算 ReLU 构造（B）、区分有限/连续边界（D），并审计 linear/nonlinear probe 或 feature crossing（E）。

## 十六、练习与独立详解

- [[习题 - XOR、隐藏表示与非线性必要性]]
- [[解答 - XOR、隐藏表示与非线性必要性]]
