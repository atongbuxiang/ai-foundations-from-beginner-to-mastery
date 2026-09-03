---
type: concept
status: draft
area: [architecture, graph-neural-networks, expressivity]
aliases: [GIN, Graph Isomorphism Network, 多重集聚合]
node_id: ARCH-20
prerequisites: ["[[消息传递神经网络的统一形式]]"]
related: ["[[WL 表达界、反例与 GNN 证据地图]]", "[[图级读出、异构图与任务接口]]", "[[图表示与消息传递神经网络 MOC]]"]
sources: ["[[S-2019-Xu-GIN]]", "[[S-2017-Zaheer-Deep-Sets]]", "[[S-2017-Hamilton-GraphSAGE]]"]
exercises: ["[[习题 - 聚合器、可辨识性与 Graph Isomorphism Network]]"]
solutions: ["[[解答 - 聚合器、可辨识性与 Graph Isomorphism Network]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-multiset-aggregation-gin-v1.svg]]"
created: 2026-08-24
updated: 2026-09-03
---

# 聚合器、可辨识性与 Graph Isomorphism Network

> [!abstract] 本节主问题
> 聚合器把任意大小、无固定顺序的邻居多重集压成定长向量。若两个不同多重集在这一步碰撞，后续任何 MLP 都无法恢复差异。mean 丢失整体倍数，max 丢失计数与非最大元素；sum 在受限可数域和合适映射下可做 injective 编码，GIN 据此达到标准消息传递类中的 1-WL 表达上界。

## 导读：不变不等于无损

到 ARCH-18 为止，我们一直强调 AGG 要对邻居顺序不变。这很容易让人产生一个危险的推断：只要它不变，它就应该把邻居信息都记住。但定长向量对变长多重集必然是一种压缩，压缩就可能发生碰撞：两个不同的输入在聚合后变成同一个数，后面再聪明的网络也只能看见这个数。

所以这一节的问题不是“哪个聚合器在论文排名更高”，而是“为了不变，我们愿意丢掉什么”。你将先用最小的多重集看到 mean、max 和裸 sum 各自的碰撞，再理解为什么 $\phi(x)$ 和中心节点的 self term 可以把其中一些碰撞拉开。

请把“injective”先理解成一个非常具体的要求：不同输入不能被压成同一个输出。等这个条件清楚后，“GIN 与 1-WL 一样强”就不再是一句标语：它是对聚合碰撞、局部更新和全局颜色细化之间关系的一个有条件结论。

## 课程位置与两遍学习路线

- **承接什么：** ARCH-18 说明 AGG 必须对邻居顺序不变，ARCH-19 给出一种归一化线性聚合；现在追问“不变压缩究竟丢掉了哪些邻域信息”；
- **本页解决什么：** 用同一组邻域多重集构造 mean、max 与裸 sum 的三类碰撞，再解释 GIN 为什么要求合适的 injective 映射、中心角色和图级 readout；
- **后续为何需要：** ARCH-21—24 的深度失效、图注意力、readout 和 1-WL 边界都要建立在“局部碰撞不可逆”这一事实之上。

**第一遍只追踪碰撞发生在哪一步。** 比较 $\{\!\{1,4\}\!\}$、其重复版本与 $\{\!\{2,3\}\!\}$；一旦 AGG 输出相同，后面的 MLP 再复杂也不能知道输入是哪一个。

**第二遍再读表达定理。** 明确可数定义域、有界 multiset size、injective $\phi$/update/readout 与有限实现之间的差距，并严格限定 GIN 达到的是标准 MPNN 的 1-WL 上界。

### 问题链

1. 为什么邻居必须建模为保留重复次数的 multiset？
2. mean 对整体复制不敏感，具体丢失了什么？
3. max 为什么看不见非最大元素与最大值 multiplicity？
4. 裸 sum 为什么保留数量尺度却仍可能碰撞？
5. $\sum_x\phi(x)$ 在什么受限条件下才可能成为 injective multiset encoding？
6. GIN 为什么要把中心节点以 $(1+\epsilon)h_i$ 单独加入？
7. “达到 1-WL”为什么既是表达能力结论，又不是一般图同构保证？

> [!check] 第一遍停靠线
> 若你能复算 mean/max 对 $\{\!\{1,4\}\!\}$ 与 $\{\!\{1,1,4,4\}\!\}$ 的碰撞，指出 sum 分别为 5 与 10；再说明裸 sum 又让 $\{\!\{1,4\}\!\}$ 与 $\{\!\{2,3\}\!\}$ 在 5 处碰撞，就完成了本页首遍。

## 符号与对象账本

| 对象 | 数学身份 | AI 中的身份 | 不能偷换成 |
|---|---|---|---|
| $X=\{\!\{x_1,\ldots,x_m\}\!\}$ | 邻域多重集 | unordered neighbor features | 去重集合 |
| $a(X)$ | 固定维聚合摘要 | AGG output | 原邻域的无损副本 |
| injective | 不同输入必得不同输出 | distinguishability condition | 训练后自动成立 |
| $\phi(x)$ | 聚合前元素映射 | neighbor encoder | 裸 identity 的必然增强 |
| cardinality | 多重集元素总数 | degree/count information | mean 自动保留的量 |
| $(1+\epsilon)h_i$ | 单独编码的中心贡献 | GIN self term | attention 概率 |
| 1-WL | 颜色细化辨识基准 | standard MPNN expressivity ceiling | 完整 graph-isomorphism oracle |

### 贯穿算例 $\mathcal G_\square$：三种摘要、三种信息边界

路径图中心节点的邻居特征为

$$
X=\{\!\{1,4\}\!\}.
$$

构造把每个邻居复制一次的

$$
Y=\{\!\{1,1,4,4\}\!\}.
$$

Mean 完全看不见整体倍数：

$$
\operatorname{mean}(X)=\frac52
=\operatorname{mean}(Y).
$$

Max 也碰撞：

$$
\max(X)=4=\max(Y),
$$

并且连“4 出现一次还是两次”都不知道。Sum 在这对输入上能区分 multiplicity：

$$
\sum X=5,\qquad \sum Y=10.
$$

但裸 sum 仍不是无条件 injective。令

$$
Z=\{\!\{2,3\}\!\},
$$

则

$$
\sum X=5=\sum Z.
$$

后续任意 $f$ 都满足 $f(\sum X)=f(\sum Z)$。要分开这一个具体碰撞，可先映射

$$
\phi(x)=(1,x,x^2).
$$

于是

$$
\sum_{x\in X}\phi(x)=(2,5,17),
\qquad
\sum_{z\in Z}\phi(z)=(2,5,13).
$$

第一坐标显式记录 cardinality，第二坐标是和，第三坐标增加二阶统计。本例说明“合适 $\phi$ 可以解除某个碰撞”，并不证明三维矩特征对任意连续多重集 injective。

对中心状态 $h_i=2$、$\epsilon=0$，GIN 在 MLP 前的输入为

$$
(1+\epsilon)h_i+\sum_{j\in\mathcal N(i)}h_j=2+5=7.
$$

若邻居整体复制，得到 $2+10=12$，所以 sum 路径保留了这次 degree 变化；若换成 $Z$，裸 sum 仍给 7，必须依赖更合适的前置编码才能分开。

## 核心公式七问：GIN 的局部更新

$$
\boxed{
h_i^{(k)}
=\operatorname{MLP}^{(k)}
\left(
(1+\epsilon^{(k)})h_i^{(k-1)}
+\sum_{j\in\mathcal N(i)}h_j^{(k-1)}
\right).
}
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 在保留邻居 multiplicity 的同时，区分中心角色并学习局部 multiset 编码 |
| 对象 | self term 与 neighbor sum 先组合，MLP 再做共享非线性更新 |
| 来路 | 1-WL 每轮把中心颜色与邻居颜色 multiset 一起做 injective hash 的神经对应 |
| 步骤 | 编码邻居、求和、加入加权中心状态，再经足够表达的 MLP |
| 读法 | “我原来是谁”和“我的邻居有哪些且各出现几次”共同决定新颜色 |
| 检查 | 打乱邻居顺序应不变；复制邻居应改变 sum；中心与同色邻居不能因无角色标记而混淆 |
| 去路 | ARCH-24 会说明即使局部步骤都理想 injective，1-WL 仍有全局非同构反例 |

现在可以回头看这个公式：它并不是在承诺“聚合后什么都不丢”，而是要你明确列出什么条件才不丢。一旦你能指出定义域、multiset 大小、$\phi$ 和 MLP 的假设，就能把“表达能力”与“训练后是否学到”分开，这也是读研究论文时最值得保留的边界意识。

## 一、为什么要讨论“可辨识性”

设邻域多重集为 $X=\{\!\{x_1,\ldots,x_m\}\!\}$。聚合器 $a(X)$ 若满足

$$
X\ne Y\quad\Rightarrow\quad a(X)\ne a(Y),
$$

则在该定义域上是 injective。若 $a(X)=a(Y)$，后续任意函数 $f$ 都有 $f(a(X))=f(a(Y))$；碰撞一旦发生不可逆。

多重集保留 multiplicity。例如 $\{\!\{1,1,3\}\!\}$ 与 $\{\!\{1,3\}\!\}$ 不同。把邻居先 `set()` 去重会直接删掉 degree/count 信息。

## 二、mean 的碰撞

$$
\operatorname{mean}\{\!\{1,3\}\!\}=2,
\qquad
\operatorname{mean}\{\!\{1,1,3,3\}\!\}=2.
$$

更一般地，把多重集每个元素复制 $k$ 次不改变 mean。因此 mean 适合消除 neighborhood size 尺度，却不能独立恢复 cardinality。若同时显式提供 degree，部分信息可补回，但仍要审计更一般碰撞。

## 三、max 的碰撞

逐坐标 max 有

$$
\max\{\!\{1,3\}\!\}=\max\{\!\{2,3,3\}\!\}=3.
$$

它忽略未达到最大值的元素和最大值出现次数。高维 learned features 可让不同元素在不同坐标“胜出”，但有限维 max 仍是对每坐标只保留一个极值的摘要，不能据此宣称对任意多重集 injective。

## 四、sum 为什么更有潜力

Sum 保留整体倍数：$\sum\{1,3\}=4$，$\sum\{1,1,3,3\}=8$。但原值直接求和也会碰撞，例如 $\{1,3\}$ 与 $\{2,2\}$。关键不是裸 sum，而是

$$
a(X)=\sum_{x\in X}\phi(x),
$$

在受限定义域上选择足够有表达力的 $\phi$。对可数标签和有界 multiset size，可构造 injective embedding；neural MLP 则近似这种映射。[[S-2017-Zaheer-Deep-Sets]] 给出集合不变函数的重要结构框架，但其精确定理条件不能省略成“sum 永远万能”。

## 五、为什么中心节点要单独编码

若只聚合闭邻域 $\{i\}\cup\mathcal N(i)$，可能无法区分“中心颜色”和“邻居出现同色”的角色。GIN 使用

$$
h_i^{(k)}=\operatorname{MLP}^{(k)}\!\left(
(1+\epsilon^{(k)})h_i^{(k-1)}+
\sum_{j\in\mathcal N(i)}h_j^{(k-1)}
\right).
$$

系数 $1+\epsilon$ 把 self contribution 与邻域 sum 组合。$\epsilon$ 可固定或学习；它不是“越大越好”的 attention 权重，而是可辨识构造的一部分。

## 六、GIN 的“与 1-WL 一样强”到底说什么

[[S-2019-Xu-GIN]] 在相应 neighborhood-aggregation GNN 类中分析表达力：若 aggregation、update 和 graph readout 都具有所需 injectivity，模型可达到 1-dimensional Weisfeiler–Lehman/color refinement 的区分能力。

必须保留四个限定：

1. 比较的是规定的消息传递模型类；
2. 初始 node labels/features 的合同相同；
3. injectivity 与足够容量是假设；
4. 1-WL 本身不能区分所有非同构图。

所以 GIN 不是通用 graph-isomorphism solver，也不因名字含 Isomorphism 就保证不同图输出不同。

## 七、有限维、连续特征与浮点数

理论构造常利用可数标签和有界多重集。实际连续特征、有限宽 MLP、训练误差与 float32 会引入近碰撞：两组不同 sum 可能数值极近，非线性饱和也可能压成同一输出。表达存在性、可训练性、数值可分性和泛化是四个不同问题。

## 八、GraphSAGE 聚合器比较

[[S-2017-Hamilton-GraphSAGE]] 讨论 mean、pooling 和 LSTM aggregator：

- mean：天然不变，稳定但丢 multiplicity scale；
- learned pooling：先逐元素非线性再 max，仍受 max 摘要边界；
- LSTM：普通实现依序列顺序，论文以随机排列使用，数学上并非严格 deterministic invariant；
- concatenating self 与 aggregate 可保留角色区别。

选择聚合器应从任务所需统计、可辨识性、噪声与成本共同判断。

## 九、图：两个碰撞与 GIN 条件链

先看图回答：A、B 两栏的信息分别在哪一步永久丢失？C 栏为何写的是“条件”而不是“sum + MLP 必然 injective”？

![[00-知识库管理/_assets/figures/architecture/fig-multiset-aggregation-gin-v1.svg|900]]

> [!figure] 图 40.3-04　Mean/max 聚合碰撞与 GIN 的 injectivity 条件
> 左栏展示 mean 的倍数碰撞，中栏展示 max 的计数碰撞，右栏给出 sum embedding、self 区分、MLP/readout 的条件链。来源：依据 GIN、Deep Sets 与 GraphSAGE 的原论文论证独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_gnn_v1.py]] 生成。

**怎样读图**：先为两个输入多重集逐项计算聚合值，确认碰撞发生在 MLP 之前；再把右栏每一框都当作必要审计项，尤其检查定义域、multiset size、有限容量和 graph readout。

**图没有证明什么**：它没有证明训练得到的有限 MLP 真正实现了理论 injective map，也没有证明 GIN 超过 1-WL。

## 十、常见错误

1. 把 multiset 写成去重 set；
2. 说 mean “忽略 degree”却未说明可额外输入 degree；
3. 认为 learned max pooling 自动 injective；
4. 把裸 sum 当作无条件 injective；
5. 忽略中心节点与邻居角色；
6. 把理论表达上界当作优化或泛化保证；
7. 把 1-WL 等同完整图同构算法。

## 十一、掌握标准

> [!summary]
> - 聚合器的碰撞会造成不可恢复的信息损失；
> - mean 丢倍数，max 丢计数和非最大元素；
> - sum 需配合合适 $\phi$ 和定义域条件才可 injective；
> - GIN 在明确假设下达到 1-WL，而非解决一般图同构。

能构造三类碰撞（A/B）、解释 injective multiset map（C）、反驳“GIN 区分所有图”（D），并设计聚合器消融（E）。

## 十二、练习与独立详解

- [[习题 - 聚合器、可辨识性与 Graph Isomorphism Network]]
- [[解答 - 聚合器、可辨识性与 Graph Isomorphism Network]]

## 参考来源

- [[S-2019-Xu-GIN]]
- [[S-2017-Zaheer-Deep-Sets]]
- [[S-2017-Hamilton-GraphSAGE]]
