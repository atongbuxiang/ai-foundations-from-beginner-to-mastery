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
updated: 2026-09-03
---

# WL 表达界、反例与 GNN 证据地图

> [!abstract] 本节主问题
> 1-WL/color refinement 反复用“自身颜色 + 邻居颜色多重集”更新节点颜色。标准 injective MPNN 可模拟这类局部细化，但 1-WL 不能区分所有非同构图。表达上界说明架构类无法表示什么；benchmark 分数说明特定协议下学到了什么；二者都不能替代数据、优化和系统证据。

## 导读：图网络什么时候真的“看懂了”一张图

前面几节分别告诉我们消息怎样沿边传播、聚合器怎样压缩多重集，以及深度和结构编码会怎样改变可见信息。现在应该追问一个更根本的问题：如果两张图在每一轮局部观察中都看起来一样，网络是否还能凭空发现它们的全局差别？1-WL（Weisfeiler–Leman color refinement）提供了一个极其有用的思维实验：让每个节点反复交换“自己的颜色和邻居颜色多重集”，然后检查两张图的颜色直方图是否分开。

这个实验的价值不在于把所有 GNN 简化成一个算法，而在于给出一条可证明的表达上界。只要模型仍然是共享参数、局部消息传递和 permutation-invariant aggregation，那么 1-WL 无法区分的局部结构，模型也不能靠训练将其恢复。与此同时，上界不是性能排行榜：即使 GIN 在条件下达到 1-WL，也不意味着它能解决每个任务，更不意味着某个 benchmark 的高分证明了普遍泛化。

本节先手算六环与两个三角形的反例，再说明 MPNN 上界和 GIN 下界如何同时成立，最后把 higher-order、位置编码和全局机制放入一张证据地图。读完后，你应当能清楚回答三个层次的问题：“模型原则上能表示什么？”“在给定训练协议下学到了什么？”“换到另一类图或任务后还能否成立？”

## 课程位置与两遍学习路线

- **承接什么：** ARCH-20 的聚合器碰撞和 ARCH-21 的深度失效说明局部信息可能不可逆丢失；本页把这种局部限制提升为可证明的图级表达边界。
- **本页解决什么：** 定义 1-WL、证明标准 MPNN 不超过它、构造六环反例，并把理论表达、实验性能和泛化证据分层。
- **后续为何需要：** 40.4—40.8 会引入稠密 attention、Transformer 和条件计算；本页的证据纪律将帮助我们区分“改变了可见性/计算对象”与“只换了参数化”。

**第一遍只玩颜色细化游戏。** 给所有节点同一个初始颜色，逐轮列出自身颜色与邻居多重集；你会直接看到两个 2-regular 图为何永远保持同样的颜色直方图。

**第二遍再连接模型与实验。** 用归纳法把 WL 颜色相等映射到 MPNN 表示相等，再检查 benchmark 的 split、构图、参数预算和 OOD 评测，防止把表达上界误写成泛化保证。

### 问题链

1. 为什么 WL 必须比较多重集而不是邻居的排列顺序？
2. “没有区分”为什么不能推出“两图同构”？
3. MPNN 的局部等变结构怎样给出 1-WL 上界？
4. GIN 的 injective sum 到底达到了什么程度？
5. higher-order、位置编码和 global attention 改变了哪一个合同？

> [!check] 第一遍停靠线
> 若你能完整跑完 $C_6$ 与 $C_3\sqcup C_3$ 的两轮颜色更新，并说出 hash 名字为何没有语义，就可以进入 MPNN 归纳证明和证据地图。

## 符号与对象账本

| 对象 | 数学身份 | AI 中的身份 | 不要偷换成 |
|---|---|---|---|
| $c_v^{(t)}$ | 第 $t$ 轮节点颜色 | 离散结构摘要 | 有固定语义的类别名 |
| $M_v^{(t)}$ | 邻居颜色多重集 | 局部可见结构 | 有顺序的邻居列表 |
| $\chi_G^{(t)}$ | 颜色直方图 | 图级 WL 观测 | 图同构的完整证书 |
| HASH | 理想 injective 编码 | 规范化编号字典 | 可学习的神谕 |
| 1-WL | 颜色细化算法 | MPNN 的表达参照 | 所有 GNN 的上界 |
| $k$-WL | 节点元组上的细化 | higher-order 图模型 | 只加深普通 GNN |

### 贯穿算例 $\mathcal G_\square$：六环与两个三角形为何相撞

令 $\mathcal G_\square=(C_6,C_3\sqcup C_3)$，并给所有节点同一个初始颜色 $a$。两张图每个节点的邻居多重集都为 $\{a,a\}$，所以第一轮全部得到同一个新颜色

$$
c_v^{(1)}=\operatorname{HASH}(a,\{\!\{a,a\}\!\})=:b.
$$

第二轮开始时，两图每个节点仍是颜色 $b$、度数仍为 2，于是继续得到同一个 $c$，以后每轮都不会分开。可是在图的全局性质上，$C_6$ 连通而 $C_3\sqcup C_3$ 有两个连通分量。这个精确碰撞说明的是“1-WL 没有区分”，不是“两图同构”；如果加入 component ID、全局 token 或 higher-order 状态，输入或计算对象已经改变。

把同一个算例再翻译成 MPNN 语言：只要初始表示相同、message/update 参数共享、aggregate 对邻居顺序不敏感，两图每一层收到的消息多重集就相同，训练也没有一条路径能凭空恢复被局部合同抹掉的全局连通性。

## 核心公式七问

1. **为什么是多重集？** 同色邻居出现两次与出现一次是不同结构，去重会丢掉 degree/count 信息。
2. **HASH 需要可学习吗？** 理论定义只要求不同输入组合得到不同编号；神经网络实现再用参数化函数近似这种区分。
3. **颜色相同意味着什么？** 只意味着在当前轮的局部观察下不可区分，不意味着节点或图在所有性质上相同。
4. **上界归纳的关键假设是什么？** 初始特征相容、参数共享、局部消息和 permutation-invariant 聚合四者缺一不可。
5. **GIN 的 injective sum 保证什么？** 在有限特征域、足够容量和合适 readout 条件下达到 1-WL 的区分能力，而非一般图同构算法。
6. **怎样真正超越 1-WL？** 改变状态对象（$k$-tuple/subgraph）、输入编码或可见性，例如 higher-order、结构位置和全局边。
7. **benchmark 分数属于哪一层？** 它只属于给定数据、split、预算和随机种子的实验证据，不能替代理论边界。

### Evidence card 的最小字段

| 层次 | 必须写清 | 典型结论形式 |
|---|---|---|
| I：恒等算例 | 图、初始颜色、每轮更新 | 两图 histogram 是否相同 |
| T：理论 | 模型类、聚合器、图类、条件 | MPNN 不超过 1-WL |
| E：实验 | 数据、split、预算、重复次数 | 某协议下的均值与方差 |
| H：机制假说 | 位置编码、构图、shortcut 检查 | 性能变化的可能原因 |
| O：外推 | OOD 图规模、度数、时间 | 结论能否迁移 |

**反例的正确用法。** 一个 WL 反例首先是对模型类的否定性证据：它说明“仅凭当前合同不能保证区分”。它不是对所有数据集的性能预测，也不是要求真实任务必须包含同样的图对。实验时应把反例作为单元测试，再把更大的随机图、真实图和分布外图作为泛化测试；理论、单元测试和 benchmark 各自回答不同问题。

在写论文或笔记时，最好把反例的前提完整抄出：初始特征是否相同、图是否有方向和边类型、聚合器是否严格不变、是否加入了位置编码。只要其中一个前提改变，原来的不可区分结论就可能不再适用；“超越 1-WL”必须说明究竟放宽了哪个前提，以及为此支付了多少计算或数据代价。

> [!tip] 写作提示
> 先写清楚“在什么合同下不能区分”，再写“改变哪个合同后可能区分”；不要只写“表达力更强”。

## 一、1-WL 算法

给每个节点初始颜色 $c_v^{(0)}$，可来自 node label/feature 的离散编码。第 $t$ 轮令

$$
c_v^{(t+1)}=\operatorname{HASH}\!\left(
c_v^{(t)},\{\!\{c_u^{(t)}:u\in\mathcal N(v)\}\!\}
\right),
$$

其中 HASH 对不同 pair injective。每轮比较两图的 color histogram；若不同，可判它们非同构。若最终相同，只能说 1-WL **没有区分**，不能判两图同构。

这里的 HASH 可以理解为一个只负责“编号”的理想字典：不同的 $(自身颜色, 邻居多重集)$ 得到不同的新颜色，相同的组合得到相同的新颜色。颜色标签本身没有“红色代表三角形”之类的固定含义；跨图比较时必须使用同一字典，真正有意义的只有相等关系和直方图是否一致。


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

这两个符号描述的是“可区分的图对集合”之间的包含关系，而不是某次训练的准确率排序。$\le$ 表示标准 MPNN 不会区分更多 WL 已经无法区分的图；$\approx$ 表示在 injective aggregation、足够容量和合适 readout 等条件下，GIN 可以达到 1-WL 的区分能力。它们都没有说模型一定学到那组参数，更没有说 1-WL 能解决所有图任务。

因此不能把结论写成 “GIN = graph isomorphism”。等号/近似符号描述的是所规定图类上的区分关系，不是训练后每个参数实例的性能保证。

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
