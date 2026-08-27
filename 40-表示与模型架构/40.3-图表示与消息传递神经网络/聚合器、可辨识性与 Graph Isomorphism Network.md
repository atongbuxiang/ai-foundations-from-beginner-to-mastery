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
updated: 2026-08-24
---

# 聚合器、可辨识性与 Graph Isomorphism Network

> [!abstract] 本节主问题
> 聚合器把任意大小、无固定顺序的邻居多重集压成定长向量。若两个不同多重集在这一步碰撞，后续任何 MLP 都无法恢复差异。mean 丢失整体倍数，max 丢失计数与非最大元素；sum 在受限可数域和合适映射下可做 injective 编码，GIN 据此达到标准消息传递类中的 1-WL 表达上界。

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

