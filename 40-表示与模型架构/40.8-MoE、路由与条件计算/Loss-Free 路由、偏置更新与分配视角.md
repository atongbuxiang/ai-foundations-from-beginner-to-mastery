---
type: concept
status: draft
area: [architecture, moe, routing, optimization, assignment]
aliases: [Loss-Free Balancing, Auxiliary-Loss-Free Routing, Quantile Balancing]
node_id: ARCH-61
prerequisites: ["[[MoE 负载均衡辅助损失与偏置]]", "[[Expert Capacity、Dispatch 与 Token Dropping]]"]
related: ["[[细粒度专家、共享专家与动态激活]]", "[[Expert Parallel、All-to-All 与通信成本]]"]
sources: ["[[S-2021-Lewis-BASE-Layers]]", "[[S-2024-DeepSeek-V3-MoE]]", "[[S-2025-Su-10757-MoE-Loss-Free]]", "[[S-2026-Su-11619-MoE-Quantile-Balancing]]", "[[S-2026-Su-11626-MoE动态激活]]"]
exercises: ["[[习题 - Loss-Free 路由、偏置更新与分配视角]]"]
solutions: ["[[解答 - Loss-Free 路由、偏置更新与分配视角]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-moe-lossfree-assignment-feedback-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Loss-Free 路由、偏置更新与分配视角

> [!abstract] 核心问题
> “Loss-Free”精确地说，是不把负载均衡项直接加到主训练损失中；它不表示没有均衡机制。常见方案维护专家偏置，根据过载/欠载反馈更新，从而改变后续 Top-k。另一条路线把路由写成带配额的全局分配，并把专家偏置理解成容量约束的对偶价格。

## 一、为什么想移除辅助损失

辅助均衡令

$$
L=L_{\text{task}}+\lambda L_{\text{bal}}.
$$

它能改善资源利用，却可能让 Router 为了均匀而偏离主任务最优。若希望把“预测谁适合该 token”和“纠正设备拥塞”分开，可以让 task loss 只训练模型参数，再用外部状态控制 expert selection。

这是控制与优化接口的重构，不是取消负载目标。

## 二、选择分数与组合权重分离

令 Router 原始 affinity 为 $s_{ti}$，为专家维护 bias $b_i$。一种 loss-free 合同是

$$
I_t=\operatorname{TopK}_i(s_{ti}+b_i,k),
$$

但选中后的混合权重仍只由原始 affinity 决定：

$$
w_{ti}=\frac{\exp(s_{ti})}{\sum_{j\in I_t}\exp(s_{tj})},
\qquad i\in I_t.
$$

$b_i$ 改变“谁被选”，不直接改变“被选后占多大权重”。这个分离有助于避免负载校正 bias 直接扭曲专家输出幅度。

但模型函数仍然变了：只要 $b_i$ 改变 Top-k 集合，输出专家就可能改变。因此“bias 不参与 gate weight”不等于“bias 不影响训练”。

## 三、最简单的反馈更新

在第 $r$ 个更新窗口，观察专家负载 $n_i^{(r)}$ 与目标 $q_i$。定义误差

$$
e_i^{(r)}=n_i^{(r)}-q_i.
$$

一种符号反馈是

$$
b_i^{(r+1)}=b_i^{(r)}-\eta\,\operatorname{sign}(e_i^{(r)}).
$$

过载专家 $e_i>0$，bias 下调；欠载专家 bias 上调。也可用比例更新

$$
b_i^{(r+1)}=b_i^{(r)}-\eta e_i^{(r)},
$$

或 EMA、clipping 与自适应步长。

[[S-2025-Su-10757-MoE-Loss-Free]] 用反馈控制视角解释了这种方法：它绕过 aux loss 对主任务梯度的直接干扰，但新增了状态 $b$、更新率 $\eta$、统计窗口与延迟。

## 四、一个两专家反馈例子

设目标负载 $q=[4,4]$，当前负载 $n=[6,2]$，初始 $b=[0,0]$，$\eta=0.1$。符号更新给出

$$
b'=[-0.1,+0.1].
$$

对下一个 token，若原始分数 $s=[0.55,0.50]$，原本选择 expert 1；校正后

$$
s+b'=[0.45,0.60],
$$

会选择 expert 2。这个例子直接证明 bias 可以在不进入 mixture weight 的情况下改变离散路由。

但若 $\eta$ 太大，负载可能在两个专家间振荡；若统计滞后，bias 修正的是旧分布；若数据分布漂移，固定 target 也可能不合理。

## 五、把路由写成全局分配

给定 token–expert score $s_{ti}$，可写成整数规划：

$$
\max_{A\in\{0,1\}^{T\times E}}
\sum_{t=1}^{T}\sum_{i=1}^{E}A_{ti}s_{ti},
$$

满足

$$
\sum_iA_{ti}=k,
\qquad
\sum_tA_{ti}\le C_i.
$$

第一条保证每 token 的专家数，第二条保证每 expert 配额。这一形式把“局部 Top-k 后再救火”改成“直接求容量约束下的整体高分 assignment”。BASE Layers 使用平衡 assignment 的思想；它更接近目标约束，却可能引入昂贵的全局求解与通信。

## 六、对偶价格为何像专家 bias

放松 $A\in[0,1]$，为容量约束引入对偶变量 $\beta_i\ge0$。拉格朗日函数含

$$
\sum_{t,i}A_{ti}(s_{ti}-\beta_i)+\sum_i\beta_iC_i.
$$

在固定 $\beta$ 时，每个 token 倾向选择较大的 $s_{ti}-\beta_i$。过度稀缺的专家对偶价格 $\beta_i$ 上升，等价于在选择分数中加入负 bias。

这给出一个统一解释：loss-free bias 可看作在线近似对偶更新；它不必是 loss gradient，但仍在尝试满足资源约束。

## 七、Quantile Balancing 与门槛

若不强制每 token 恰好选 $k$，而要求每个专家大致接收固定 quota，可为专家 $i$ 选择阈值 $\beta_i$：

$$
A_{ti}=\mathbf1[s_{ti}>\beta_i].
$$

$\beta_i$ 取该专家 score 分布的相应分位数，就能控制选中数量。[[S-2026-Su-11619-MoE-Quantile-Balancing]] 将其与线性规划对偶、交替更新和 BASE/BIP 类方法联系起来。

它的优势是将“每专家配额”转成一维 quantile；难点是精确全局分位数需要汇总大量 score，分布式中常用 histogram 或近似 quantile。近似误差、有限迭代与 stale statistics 都要进入证据表。

## 八、动态激活中的更新时序

在流式或迭代算法中，阈值/偏置的更新顺序会改变结果。应明确：

1. 用旧 $\beta^{(r)}$ 路由当前 batch；
2. 观察当前 score/load；
3. 更新得到 $\beta^{(r+1)}$；
4. 下一 batch 才使用新阈值。

若代码在同一 batch 内先估计阈值再回头路由，得到的是另一算法。[[S-2026-Su-11626-MoE动态激活]] 对这一点和 EMA/漂移问题作了明确提醒。

## 九、正式图：反馈控制与全局分配

这张图回答什么问题？loss-free bias 与 assignment dual 为什么相关，但又不能视为同一个已证明算法？

![[00-知识库管理/_assets/figures/architecture/fig-moe-lossfree-assignment-feedback-v1.svg|900]]

> [!figure] 图 1｜Bias feedback、容量约束 assignment 与证据分级。**图源与生成**：本仓库原创 SVG，由 [[00-知识库管理/_labs/code/plot_architecture_moe_v1.py]] 生成；中间玩具矩阵为教学构造，未复制论文或博客原图。

**怎样读图**：A 沿“加 bias 路由→观测负载误差→反向调 bias”的闭环读；B 把 token–expert score 写成配额 assignment，并将 dual price/quantile 与 bias 联系；C 把 arg-top-k 恒等事实、分配理论、系统实验和漂移稳定性分别标为 I/T/E/O。

**图没有证明什么**：图没有证明简单符号反馈会收敛，也没有证明在线 bias 精确求解全局 assignment。延迟、步长、分布漂移和离散 Top-k 都可能造成振荡或次优。

## 十、如何比较 Aux-Loss 与 Loss-Free

保持模型、Router、capacity、expert placement、训练 tokens 与随机种子一致，至少比较：

- task loss / downstream quality；
- hard load、drop、CV、max/mean；
- $b_i$ 时间序列和振荡；
- Router entropy 与 specialization；
- tokens/s、All-to-All bytes、p95 step time；
- 对 $\lambda$ 或 $\eta$ 的 sweep；
- 分布突变后的恢复时间。

若 loss-free 版本不用 aux loss，却改变 score activation、capacity 或共享专家，就不能把差异归因于“无辅助损失”。

## 十一、证据边界与学习出口

- bias 改变 Top-k、assignment 约束、对偶形式：`I`；
- LP relaxation、特定更新条件下的收敛：有条件 `T`；
- DeepSeek-V3 或其他模型报告的均衡与质量：其协议下 `E`；
- 在线 bias 近似 shadow price：`H/T`，依具体算法；
- 非平稳分布下的跨规模稳定最优更新：`O`。

学完本节，应能手算一次 bias 更新、写出容量约束 assignment、从拉格朗日函数解释专家价格，并准确说明“loss-free 不等于 training-free”。

