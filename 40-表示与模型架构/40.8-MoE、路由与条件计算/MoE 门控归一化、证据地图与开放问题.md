---
type: concept
status: draft
area: [architecture, moe, gating, evidence, open-problems]
aliases: [MoE Gating Normalization, MoE Evidence Map]
node_id: ARCH-64
prerequisites: ["[[Router、Gate、Top-k 与稀疏组合]]", "[[Loss-Free 路由、偏置更新与分配视角]]", "[[细粒度专家、共享专家与动态激活]]"]
related: ["[[MoE、路由与条件计算 MOC]]", "[[科学空间 - 第四章专题来源地图]]"]
sources: ["[[S-2021-Roller-Hash-Layers]]", "[[S-2026-Su-11750-Hash-Routing-tid2eid]]", "[[S-2026-Su-11782-MoE门控归一化]]", "[[S-2026-Su-11848-K3-MoE-Attention]]"]
exercises: ["[[习题 - MoE 门控归一化、证据地图与开放问题]]"]
solutions: ["[[解答 - MoE 门控归一化、证据地图与开放问题]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-moe-gating-normalization-evidence-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# MoE 门控归一化、证据地图与开放问题

> [!abstract] 核心问题
> MoE 还没有一个脱离协议的“最佳门控”。Softmax、Sigmoid、ReLU、Top-k 前后归一化、可学习 Router 与固定 Hash routing 都改变不同接口。本节把可复算恒等式、有限条件理论、实验、解释假说和开放问题分层，作为 40.8 的证据收束。

## 一、Softmax 的几何：竞争的单纯形

Softmax score 满足

$$
a_i=\frac{e^{z_i}}{\sum_j e^{z_j}},
\qquad a_i>0,\quad \sum_i a_i=1.
$$

所有 score 位于概率单纯形。提高一个 logit 不只提高自己的权重，还会通过分母降低其他权重。Jacobian 为

$$
J_{ij}=a_i(\delta_{ij}-a_j).
$$

它表达的是相对竞争，适合“固定总门控质量在专家间分配”的语义。

## 二、Sigmoid 的几何：独立适配度

Sigmoid score

$$
a_i=\sigma(z_i)
$$

只受自身 logit 影响，$\partial a_i/\partial z_j=0$（$i\ne j$）。它可解释为每个 expert 独立适配程度；总和不固定。若随后强制 Top-k，再在选中集合 Re-Norm，竞争被推迟到 selection/normalization 接口。

ReLU $a_i=\max(0,z_i)$ 则允许精确零和未归一的幅度，但负半轴普通梯度为零。三者没有脱离后续 Top-k 与 Re-Norm 的优劣排序。

## 三、哪些变换不改排名

若 $g$ 严格单调递增，则

$$
\operatorname{TopK}(g(z),k)=\operatorname{TopK}(z,k)
$$

（无 tie 时）。Softmax、Sigmoid 都保持 logits 排名，所以在只用 index 的 forward 中可能选同一专家。

但以下量仍改变：

- 选中 weight 数值；
- 未选专家是否进入分母；
- Router Jacobian 与饱和；
- 辅助损失看到的 soft statistic；
- 数值稳定与低精度误差。

因此“Top-k 集合相同”只能推出 selection equivalence，不能推出 model/training equivalence。

## 四、Top-k 后 Re-Norm 的三个极端

### $k=E$

没有稀疏 selection。Softmax 后再 Re-Norm 不变；Sigmoid 后 Re-Norm 成为归一化 sigmoid mixture。

### $k=1$

任何正 score 在选中后都归一为 1，task loss 经普通 mixture weight 对 score 的导数为零。Router 必须依靠其他路径学习，或 selection 本身由非普通梯度估计。

### 不做 Re-Norm

选中 score 总和可随输入变化，相当于额外的门控幅度。它可能有表达力，也可能导致层尺度漂移；RMSNorm/residual 位置会影响结果。

[[S-2026-Su-11782-MoE门控归一化]] 的最大价值，是把 score activation、selection、selected weight 与 backward estimator 拆开讨论，并给出 Top-1 边界。文章中的概率/第一性原理解释仍包含近似，应标为 `H/T`，不能直接升级成跨规模性能定理。

## 五、固定 Hash Routing 是什么对照

可学习 Router 不是 MoE 的逻辑必需条件。Hash Layers 把 token id 通过固定函数映射到 expert：

$$
i=h(\text{token id}).
$$

它消除 Router 训练与在线 score 计算，也可事先设计负载，但相同 token 在所有上下文中通常去同一专家，表达条件受限。

[[S-2026-Su-11750-Hash-Routing-tid2eid]] 讨论按 token frequency 贪心构造 tid→eid 的方案，并指出一个重要不可行边界：若某个 token 自身频率已超过单个专家目标容量，而它又不能拆到多个专家，就不可能达到严格均衡。

这可以直接用鸽巢原理表达。若频率 $c_{max}>N/E$，任何单值 hash 都有

$$
\max_i n_i\ge c_{\max}>N/E.
$$

这是固定单专家映射的结构边界，而非实现缺陷。

## 六、证据阶梯 I/T/E/H/O

### I — Identity / accounting

shape、参数量、Top-k index、Re-Norm 恒等式、payload bytes。给定定义即可复算。

### T — Theorem under assumptions

平衡 assignment 的最优性、特定随机/凸条件下的收敛、容量概率界。必须把假设写在结论旁。

### E — Experiment

给定模型、数据、seed、硬件和软件的 loss、吞吐、负载与消融。只在协议内成立。

### H — Hypothesis / interpretation

专家学到语义、共享专家承载公共知识、难 token 需要更多专家、某 gate “更自然”。这些观点可指导实验，但不能替代实验。

### O — Open problem

跨规模最优门控、稳定专业化、动态预算的因果分配、非平稳路由控制和系统—任务联合 Pareto。

## 七、近期整体系报告怎样读

[[S-2026-Su-11848-K3-MoE-Attention]] 涉及 Stable LatentMoE、RMSNorm、Quantile Balancing 和近似全局 quantile 等组合。应采用：

- 明确的结构与算法接口；
- 可复算的量化/分位数近似；
- 报告协议内的开发证据。

不应据此声称：每个组件都已被独立消融、外部复现，或该组合在所有训练规模上最优。系统报告是重要 `E/H`，但不是独立第三方定理。

## 八、正式图：门控几何与证据强度

这张图回答什么问题？为什么一个漂亮的门控解释不能直接推出跨规模优胜？

![[00-知识库管理/_assets/figures/architecture/fig-moe-gating-normalization-evidence-v1.svg|900]]

> [!figure] 图 1｜Softmax/Sigmoid score geometry、Top-1 Re-Norm 边界与证据阶梯。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_moe_v1.py]] 生成；未复制科学空间或论文原图。

**怎样读图**：A 把 Softmax 限制在总和为一的直线/单纯形，而 Sigmoid 点可独立分布；B 逐步推到 Top-1 Re-Norm 权重恒为 1、普通权重路径梯度为零；C 从 I、T、E、H 到 O 检查每条结论实际站在哪一级。

**图没有证明什么**：二维几何只是接口示意，没有证明 Softmax/Sigmoid 的表示优劣；证据阶梯也不贬低假说，而是防止把解释性故事写成无条件事实。

## 九、40.8 的开放问题清单

1. **任务最优与系统均衡能否统一？** 是否存在可扩展的约束优化器，在不显著损伤 task loss 下满足设备容量？
2. **Router 学到什么？** 选择与专家输出范数、梯度收益、语义、频率分别有何因果关系？
3. **专家专业化是否稳定？** 换 seed、数据顺序或规模后，专家功能能否对齐？
4. **动态计算给谁？** 如何估计多激活一个专家的反事实边际收益，而非用当前 loss/entropy 代替？
5. **怎样跨拓扑部署？** 专家放置、路由与 collective 是否应联合优化？
6. **dropless 的质量贡献是什么？** 来自不丢 token、更多实际 FLOPs，还是更好 kernel？
7. **门控归一化的尺度律是什么？** $E,k$ 与训练规模变化时最优 activation/Re-Norm 是否改变？
8. **固定与可学习路由的边界？** 频率 hash、语义 hash 与 learned Router 的容量—适应性 Pareto 在哪里？

## 十、评审一项 MoE 主张的最小表格

| 层级 | 必须提供 |
|---|---|
| 模型函数 | logits、activation、selection、mixing、shared path |
| 容量语义 | group、$C$、drop/pad/dropless、fallback |
| 优化 | task/aux/bias/STE、统计粒度、更新时序 |
| 成本 | total/active params、MAC、residency、network bytes |
| 系统 | DP/TP/PP/EP/SP、拓扑、kernel、dtype、版本 |
| 质量 | tokens、数据、seed、loss/任务、消融 |
| 负载 | mean/max/CV、drop、$k_t$、时间序列 |
| 证据标签 | I/T/E/H/O 与适用范围 |

## 十一、40.8 总结与学习出口

MoE 的核心不是一句“稀疏激活”，而是一条从输入相关选择到分布式执行的完整链：

$$
\text{score}\to\text{selection}\to\text{capacity}\to
\text{dispatch}\to\text{expert}\to\text{combine}\to\text{feedback}.
$$

学完本节与 40.8，应能：

- 分离 total/active/resident parameters 与 MAC/bytes/latency；
- 写完整 forward/backward 路由合同；
- 手算 capacity、aux loss、bias 与 assignment；
- 解释 shared/fine-grained/dynamic/EP 的独立作用；
- 用 I/T/E/H/O 限定科学空间、论文和系统报告中的结论。

