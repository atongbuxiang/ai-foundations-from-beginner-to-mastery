---
type: concept
status: draft
area: [architecture, graph-neural-networks, expressivity, evidence]
aliases: [1-WL, Color Refinement, GNN 表达边界]
node_id: ARCH-24
prerequisites: ["[[聚合器、可辨识性与 Graph Isomorphism Network]]", "[[图网络深度、过平滑与过挤压]]", "[[图级读出、异构图与任务接口]]"]
related: ["[[图表示与消息传递神经网络 MOC]]", "[[科学空间 - 第四章专题来源地图]]"]
sources: ["[[S-2019-Xu-GIN]]", "[[S-2019-Morris-HigherOrder-WL]]", "[[S-2022-Su-9147-Hubness]]"]
exercises: ["[[习题 - WL 表达界、反例与 GNN 证据地图]]"]
solutions: ["[[解答 - WL 表达界、反例与 GNN 证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-wl-refinement-evidence-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# WL 表达界、反例与 GNN 证据地图

> [!abstract] 本节主问题
> 1-WL/color refinement 反复用“自身颜色 + 邻居颜色多重集”更新节点颜色。标准 injective MPNN 可模拟这类局部细化，但 1-WL 不能区分所有非同构图。表达上界说明架构类无法表示什么；benchmark 分数说明特定协议下学到了什么；二者都不能替代数据、优化和系统证据。

## 一、1-WL 算法

给每个节点初始颜色 $c_v^{(0)}$，可来自 node label/feature 的离散编码。第 $t$ 轮令

$$
c_v^{(t+1)}=\operatorname{HASH}\!\left(
c_v^{(t)},\{\!\{c_u^{(t)}:u\in\mathcal N(v)\}\!\}
\right),
$$

其中 HASH 对不同 pair injective。每轮比较两图的 color histogram；若不同，可判它们非同构。若最终相同，只能说 1-WL **没有区分**，不能判两图同构。

颜色名本身没有语义，只有相等/不等关系有意义；两图比较时必须用共同 hash dictionary。

## 二、为何标准 MPNN 不超过 1-WL

假设两个节点在第 $t$ 轮 WL 颜色相同，则它们有相同自身颜色和相同邻居颜色多重集。若 MPNN 初始表示只依颜色、message/update 参数共享且 aggregation permutation invariant，那么两节点收到相同消息多重集，输出表示也相同。

对层数归纳得到：1-WL 不能区分的节点/图，标准 MPNN 也不能凭训练把结构差异恢复出来。[[S-2019-Xu-GIN]] 与 [[S-2019-Morris-HigherOrder-WL]]分别从 aggregation 与 higher-order 视角建立这种联系。

这是**表示类上界**，不是说所有 MPNN 都恰好达到 1-WL；mean/max 碰撞会更弱，有限训练也可能达不到理论能力。

## 三、一个最小反例：六环与两个三角形

比较 $C_6$ 与 $C_3\sqcup C_3$。两图都有 6 个节点；若初始标签相同，每个节点 degree 都是 2。第一轮每个节点都看到“自身同色 + 两个同色邻居”，得到同一新颜色；以后完全重复。因此 1-WL 无法区分。

但两图显然不同：一个连通，一个有两个连通分量。反例说明局部 degree-regular 视图可掩盖全局连接结构。若额外提供 component ID，这已改变输入；若使用 global/higher-order mechanism，也已超出原标准 MPNN 合同。

## 四、GIN 的下界与上界要一起读

Injective sum aggregation、update 和 readout 使 GIN 达到 1-WL 的区分能力；上面的反例同时仍约束它。正确结论是

$$
\text{常见 MPNN}\ \le\ \text{1-WL},\qquad
\text{合条件 GIN}\ \approx\ \text{1-WL},
$$

而不是 “GIN = graph isomorphism”。等号/近似符号描述所规定图类上的区分关系，不是训练后每个参数实例的性能保证。

## 五、怎样超越标准局部上界

常见路线包括：

- higher-order $k$-WL / k-GNN，状态定义在节点元组上；
- subgraph GNN，以 rooted subgraph 为计算对象；
- unique/random IDs 或 positional/structural encodings；
- spectral/eigenvector features；
- global attention、virtual node 或 long-range edges；
- motif/cycle/counting features。

每条路线都改变输入或计算对象，并付出成本。$k$-tuple 状态数量可达 $O(n^k)$；随机 ID 还涉及不变性、方差与泛化。不能只说“超越 WL”而不说超越哪一阶、在哪类图、以何种资源。

## 六、结构表达不等于任务泛化

一个更能区分图的模型也可能：

- 在小数据上过拟合 graph ID 或 size shortcut；
- 优化困难，未实现理论区分；
- 对扰动边不鲁棒；
- 使用泄漏的 positional encoding；
- 在任务只需简单局部统计时浪费容量。

表达力回答“存在参数表示某函数吗”，泛化回答“由有限数据学到的函数在目标分布好吗”。二者需学习理论与实验共同连接。

## 七、图 benchmark 的证据合同

任何“模型更强”至少记录：

1. dataset version、graph construction、node/edge features；
2. task unit 与 transductive/inductive/temporal split；
3. target edge removal、negative sampling；
4. train/validation/test seed 与 hyperparameter budget；
5. parameter、FLOP、memory、wall-clock 对齐；
6. classical/feature-only/size/degree baselines；
7. 多次重复的均值、方差与显著性；
8. OOD graph size、degree、motif 或时间漂移。

单个 benchmark 排名属于特定协议的 E 级证据，不是 WL 定理，也不是普遍工程优势。

## 八、Science Space 的构图风险桥

科学空间目前没有 GCN/MPNN/GIN/WL 的完整主线，因此本节不让博客承担表达定理。[[S-2022-Su-9147-Hubness]]只用于提醒：若 benchmark 图由高维 embedding 的 kNN 构造，hubness 可能改变 degree distribution、message traffic 与 label propagation。模型提升可能来自特定构图偏差，必须对 $k$、metric、mutual-kNN 和 train-only construction 做敏感性分析。

## 九、图：颜色细化、反例与证据阶梯

先看图回答：为什么 B 栏两图从 uniform label 开始会永远得到同色？C 栏的 I/T/E/H/O 五层为何不能互相替代？

![[00-知识库管理/_assets/figures/architecture/fig-wl-refinement-evidence-v1.svg|900]]

> [!figure] 图 40.3-08　1-WL 颜色细化、六环反例与 GNN 证据层级
> 左栏给出一轮 color refinement，中栏比较 $C_6$ 与两个不相连三角形，右栏区分恒等手算、条件化定理、实验、机制假说和开放外推。来源：依据 GIN、Morris 等 WL 理论及本课程证据分级独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_gnn_v1.py]] 生成。

**怎样读图**：先手算每个节点的“自身颜色 + 邻居颜色 multiset”，确认两个 2-regular 图的 histogram 始终相同；再将“模型能表示”“训练能学到”“某数据集得分”“跨分布有效”分别放到不同证据层。

**图没有证明什么**：它没有证明这是一切 GNN 的反例，也没有证明 higher-order 或 positional encoding 在任意任务上更好。

## 十、常见错误

1. WL 未区分就判两图同构；
2. 两图使用不同 hash dictionary；
3. 把 GIN 名字当同构保证；
4. 把 MPNN 上界外推所有图模型；
5. 把更高表达力当更好泛化；
6. 用 benchmark 排名证明理论严格更强；
7. 构图使用 test embedding 或忽略 hubness；
8. 说“超越 WL”却不写阶数、图类和成本。

## 十一、掌握标准

> [!summary]
> - 1-WL 用自身颜色和邻居颜色多重集迭代细化；
> - 标准 MPNN 一般不超过 1-WL，GIN 在条件下达到该上界；
> - $C_6$ 与两个三角形给出直观反例；
> - 表达定理、实验性能、泛化和系统效率是不同证据。

能运行小图 WL（A/B）、证明 MPNN 上界归纳（C）、构造/解释反例（D），并写出完整 benchmark evidence card（E）。

## 十二、练习与独立详解

- [[习题 - WL 表达界、反例与 GNN 证据地图]]
- [[解答 - WL 表达界、反例与 GNN 证据地图]]

## 参考来源

- [[S-2019-Xu-GIN]]
- [[S-2019-Morris-HigherOrder-WL]]
- [[S-2022-Su-9147-Hubness]]
