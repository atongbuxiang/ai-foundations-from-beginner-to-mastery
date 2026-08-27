---
type: concept
status: draft
area: [architecture, moe, load-balancing, optimization]
aliases: [MoE Auxiliary Loss, Load Balancing Loss, Router Z-loss]
node_id: ARCH-60
prerequisites: ["[[Router、Gate、Top-k 与稀疏组合]]", "[[Expert Capacity、Dispatch 与 Token Dropping]]"]
related: ["[[Loss-Free 路由、偏置更新与分配视角]]", "[[MoE 门控归一化、证据地图与开放问题]]"]
sources: ["[[S-2017-Shazeer-Sparsely-Gated-MoE]]", "[[S-2020-Lepikhin-GShard]]", "[[S-2021-Fedus-Switch-Transformer]]", "[[S-2022-Zoph-ST-MoE]]", "[[S-2025-Su-10735-MoE辅助损失]]", "[[S-2026-Su-11760-MoE序列均衡]]"]
exercises: ["[[习题 - MoE 负载均衡辅助损失与偏置]]"]
solutions: ["[[解答 - MoE 负载均衡辅助损失与偏置]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-moe-aux-loss-load-gradient-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# MoE 负载均衡辅助损失与偏置

> [!abstract] 核心问题
> Router 若把大量 token 送往少数专家，会造成 overflow、低利用率与尾延迟。辅助损失用可微 proxy 鼓励均衡，但它把资源目标加入了学习目标。要理解它，必须分清离散使用率、连续概率、统计粒度与停止梯度。

## 一、为什么主任务损失不一定自动均衡

主任务只关心预测质量。若某个专家在早期偶然更好，Router 会给它更多 token；它得到更多梯度后可能进一步变好，形成富者愈富。其他专家因样本少而训练不足。

系统却希望每台设备工作接近，减少

$$
\max_j n_j
$$

及 overflow。任务目标与资源目标并不天然相同，所以需要显式约束、辅助目标或反馈控制。

## 二、Switch 风格两统计量损失

在含 $T$ 个 token 的路由组中，令 Top-1 选择指标为 $A_{ti}\in\{0,1\}$，soft Router probability 为 $p_{ti}$。定义

$$
f_i=\frac1T\sum_{t=1}^{T}A_{ti},
\qquad
P_i=\frac1T\sum_{t=1}^{T}p_{ti}.
$$

$f_i$ 是实际硬选择频率，$P_i$ 是连续平均概率。常见辅助项为

$$
L_{\text{bal}}=\lambda E\sum_{i=1}^{E}f_iP_i.
$$

在完全均匀时 $f_i=P_i=1/E$，于是未乘 $\lambda$ 的归一化量为

$$
E\sum_i\frac1E\frac1E=1.
$$

若所有 token 都偏向同一专家，$f_1=P_1=1$，该量变成 $E$，惩罚更大。

## 三、为什么用 $f_iP_i$ 而不只用 hard count

Top-k 指标 $A_{ti}$ 对 logits 几乎处处不可导。实践中通常把 $f_i$ 当作当前路由产生的统计量并 stop-gradient，而 $P_i$ 通过 softmax 向 Router 提供连续梯度。

在把 $f$ 视为常数时，

$$
\frac{\partial L_{\text{bal}}}{\partial p_{ti}}
=\frac{\lambda E}{T}f_i.
$$

热门专家 $f_i$ 大，其 probability 受到更强的降低压力。再通过 softmax Jacobian

$$
\frac{\partial p_i}{\partial z_j}=p_i(\delta_{ij}-p_j)
$$

把压力传播到 logits。

它是一个 proxy：真正关心的是 hard load/capacity，实际求导的是 soft probability。[[S-2025-Su-10735-MoE辅助损失]] 对“统计量怎样构造、梯度怎样传、粒度怎样选”做了很有价值的拆解。

## 四、一个四 token、两专家例子

假设硬选择为 $[1,1,1,2]$，则

$$
f=[0.75,0.25].
$$

若平均 soft probability 为 $P=[0.7,0.3]$，则归一化均衡项为

$$
E\sum_i f_iP_i
=2(0.75\times0.7+0.25\times0.3)=1.2.
$$

若完全均匀，值为 1。对 expert 1 的每个 $p_{t1}$，直接系数为 $2\lambda\cdot0.75/4=0.375\lambda$；expert 2 为 $0.125\lambda$。经过 softmax 交叉耦合，优化会相对压低热门专家。

## 五、为什么 $\lambda$ 不是普通正则强度

总目标为

$$
L=L_{\text{task}}+L_{\text{bal}}.
$$

$\lambda$ 太小，均衡信号不足；太大，Router 可能为了均匀而放弃任务上有益的专业化。并且 $L_{\text{task}}$ 的尺度会随 batch、token reduction、语言建模词表与 loss normalization 改变，所以同一数值的 $\lambda$ 不一定跨代码库可比。

必须同时报告：

- loss 是按 token mean 还是 sum；
- $L_{\text{bal}}$ 在 layer、sequence、microbatch 何处聚合；
- $f$ 是否 stop-gradient；
- padding token 是否计入；
- Top-1 与 Top-k 如何定义 $f_i$；
- 多层 aux loss 如何求和。

## 六、均衡粒度改变优化问题

可在 token group、microbatch、sequence、device group 或全局 batch 上统计。粒度越小，反馈越及时、通信越少，但估计噪声更大，且可能强迫每条短序列都均匀；粒度越大，统计更接近全局资源负载，却需要同步并引入延迟。

[[S-2026-Su-11760-MoE序列均衡]] 讨论了序列级均衡：若强迫每个 sequence 都接近完美均匀，可能压制真实的 token/主题差异。正确结论是“是否需要、需要多强”仍要按训练系统和任务检验，而非把全局均衡直接下推成逐序列定理。

## 七、负载均衡不止一个损失

早期稀疏 MoE 还使用 importance loss、load loss；ST-MoE 引入 Router z-loss 稳定 logits：

$$
L_z=\frac1T\sum_t\left(\log\sum_i e^{z_{ti}}\right)^2.
$$

$L_z$ 主要控制 Router logits 的尺度与数值稳定，不能替代负载均衡。一个目标让“用得均匀”，另一个让“log-sum-exp 不失控”。命名相邻但优化对象不同。

还可用 entropy、KL 到均匀分布、CV loss 或硬容量惩罚。不同 surrogate 的极小点、梯度和分布式统计成本并不相同。

## 八、均匀是否一定最优

从系统角度，完全均匀能最大化同构专家设备利用率；从任务角度，不同 token 分布未必需要完全相同的专家频率。共享专家、异构专家、长尾数据或分层网络都会改变合理目标。

所以应写成双目标或约束问题：

$$
\min_\theta L_{\text{task}}(\theta)
\quad\text{s.t.}\quad n_i\le C_i,
$$

或其拉格朗日松弛，而不是把“均匀”当作语义真理。辅助损失是用可训练性换取约束近似的工程选择。

## 九、正式图：均衡代理怎样产生梯度

这张图回答什么问题？为什么 hard frequency、soft probability 与全局负载不能用同一个符号替代？

![[00-知识库管理/_assets/figures/architecture/fig-moe-aux-loss-load-gradient-v1.svg|900]]

> [!figure] 图 1｜负载均衡辅助损失的两统计量、梯度路径与聚合粒度。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_moe_v1.py]] 生成；公式参考 Switch Transformer 与科学空间解读，未复制论文曲线。

**怎样读图**：A 将离散 $f_i$ 与连续 $P_i$ 画成两组柱，再以 $E\sum f_iP_i$ 耦合；B 从总损失分出 hard statistic 与 soft gradient path，强调 stop-gradient/proxy；C 展示 token→microbatch→sequence→global 的统计尺度及相应代价。

**图没有证明什么**：图没有证明均匀负载必然提高任务质量，也没有证明某个 $\lambda$ 或统计粒度跨模型最优；它只说明一种常见 proxy 如何连接系统目标与连续梯度。

## 十、实验审计

至少同时画：

1. task loss 与 aux loss；
2. 每层每专家 hard counts；
3. soft probability means；
4. max/mean、CV、entropy；
5. drop rate 与 capacity utilization；
6. Router logit/entropy 时间序列；
7. token 类型、语言或位置分组后的负载；
8. 吞吐与 p95 step time。

做 $\lambda=0$、小、中、大的 sweep，并保持总训练 tokens、seed、capacity 与 expert placement 一致。若均衡改善但 task loss 变差，应报告 Pareto，而不是只选一个指标。

## 十一、证据边界与学习出口

- $f_i,P_i,L_{bal}$ 定义及 stop-grad 下梯度：`I`；
- 给定概率模型下均衡 proxy 的性质：`T`；
- Switch/ST-MoE 或具体模型的稳定性结果：`E`；
- “逐序列均衡抑制语义专业化”：待控制实验的 `H`；
- 跨模型最优统计粒度与系数：`O`。

学完本节，应能手算一个 batch 的 $f,P,L_{bal}$，推导它对 soft probability 的直接梯度，解释为何该目标是 proxy，并设计同时观察质量、负载与系统性能的消融。

