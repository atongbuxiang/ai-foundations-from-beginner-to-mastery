---
type: method
status: verified
area: [training, optimization, muon, implementation-contract]
node_id: TRN-27
aliases: [Muon 完整状态机, Muon Optimizer Contract]
prerequisites: ["[[矩阵梯度、谱核范数对偶与 Matrix Sign]]", "[[Mini-batch 梯度、平均求和与有效 Batch]]", "[[Momentum、EMA、偏差修正与框架约定]]", "[[二次模型的学习率—动量稳定域与阻尼]]"]
related: ["[[Newton–Schulz Matrix Sign 的收敛与有限精度]]", "[[Muon 形状缩放、Update RMS 与版本差异]]", "[[Muon 的扩展证据、系统成本与迁移边界]]"]
sources: ["[[S-2024-Jordan-Muon]]", "[[S-2026-PyTorch-Muon]]", "[[S-2025-Su-11416-Muon优化器指南]]", "[[S-2025-Liu-Muon-Scalable-LLM]]"]
exercises: ["[[习题 - Muon 的动量、正交化与参数分组合同]]"]
solutions: ["[[解答 - Muon 的动量、正交化与参数分组合同]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-muon-state-transition-contract-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Muon 的动量、正交化与参数分组合同

> [!abstract] 一句话结论
> 可复现的 Muon 不是一句“对梯度正交化”，而是一条有版本的状态机：选择参数组，更新 momentum buffer，构造 Nesterov 矩阵，做有限步 Newton–Schulz，按 shape 调整学习率，再按明确顺序施加 decoupled weight decay。任一步语义不同，都可能是另一个优化器。

## 一、先写最小接口，而不是先写名字

对二维 hidden parameter $W_t\in\mathbb R^{A\times B}$ 与随机梯度 $G_t$，一条 Muon step 至少需要：

$$
\mathcal S_t=(W_t,B_t,t;\eta,\mu,\lambda,K,a,b,c,s),
$$

其中：

- $B_t$：momentum buffer；
- $\eta$：base learning rate；
- $\mu$：momentum；
- $\lambda$：decoupled weight decay；
- $K$：Newton–Schulz steps；
- $(a,b,c)$：奇多项式系数；
- $s(A,B)$：shape-dependent LR adjustment。

只记录 “Muon, lr=…” 不足以复现实验。

## 二、当前 PyTorch 语义：一条可逐行审计的状态机

以下按 [[S-2026-PyTorch-Muon]] 在 2026-08-26 的文档与源码描述；未来版本必须重新核验。

### 2.1 参数资格

Muon group 只接收二维 parameter。常见的 embedding、norm scale、bias 和 output head 需要放入 AdamW 或其他 optimizer group。这里的 “二维” 是实现合同，不是“所有矩阵都理论上适合 Muon”的证明。

### 2.2 EMA-style momentum buffer

当前源码等价于

$$
B_t
=\mu B_{t-1}+(1-\mu)G_t.
\tag{1}
$$

这是指数移动平均。随后若启用 Nesterov，形成

$$
M_t
=(1-\mu)G_t+\mu B_t.
\tag{2}
$$

若不启用，则 $M_t=B_t$。源码中的 lerp 操作实现上述 convex combination。

### 2.3 近似 polar/msign

先按实现规定缩放 $M_t$ 得到 $X_0$，再重复 $K$ 次

$$
X_{k+1}
=aX_k+bX_kX_k^TX_k+cX_kX_k^TX_kX_k^TX_k,
\tag{3}
$$

或根据 shape 用代数等价、乘法更便宜的排列。输出记为

$$
\widehat Q_t=\operatorname{NS}_K(M_t).
$$

它是 finite-step approximation，不在文档中偷写为精确 $\operatorname{msign}(M_t)$。

### 2.4 decay 与 update

当前实现的 decoupled weight decay 使用 base LR：

$$
W_t^{decay}=(1-\eta\lambda)W_t,
\tag{4}
$$

而方向更新使用 adjusted LR

$$
\eta_t^{adj}=\eta\,s(A,B),
\qquad
W_{t+1}=W_t^{decay}-\eta_t^{adj}\widehat Q_t.
\tag{5}
$$

若把 decay 也乘 $s(A,B)$，就改变了相对 regularization strength。

## 三、原始伪代码与当前实现为什么不能混用

早期/其他实现常见 sum-style buffer

$$
\widetilde B_t=\mu\widetilde B_{t-1}+G_t.
\tag{6}
$$

它与式 (1) 只在做相应 rescaling 且所有后续非线性操作可交换时才可能等价。Muon 中后续有归一化和 finite-step polynomial，不能无条件把 $(1-\mu)$ 吸收到 learning rate。

### 3.1 两步手算

令标量化示意 $B_0=0,\mu=0.9,G_1=2,G_2=-1$：

EMA-style：

$$
B_1=0.2,\qquad
B_2=0.9(0.2)+0.1(-1)=0.08.
$$

sum-style：

$$
\widetilde B_1=2,\qquad
\widetilde B_2=0.9(2)-1=0.8.
$$

此例恰好相差 10 倍，但若初始化、bias correction、Nesterov 混合、clipping 或分组规则不同，简单比例关系会破坏。checkpoint 中 buffer 的含义必须和加载它的 transition 一致。

## 四、参数分组不是清洁代码，而是算法定义

一个可审计的模型分组表应至少列出：

| 参数类别 | 典型 shape | 推荐起始 optimizer | 原因 |
|---|---:|---|---|
| hidden dense weight | 2D | Muon 候选 | 矩阵 polar update 有定义 |
| attention Q/K/V/O | 2D，可能 fused | Muon 候选，但记录切分方式 | joint 与 per-projection orthogonalization 不同 |
| embedding table | 2D | 常用 AdamW | 稀疏访问与 token-frequency geometry 不同 |
| output/lm head | 2D | 常用 AdamW | 与 logits、weight tying 和 vocab scale 强耦合 |
| bias / norm scale | 1D | AdamW/SGD | 不满足当前 Muon 2D 合同 |
| convolution kernel | 4D | 需明确 reshape 或不用 | reshape 会定义新的矩阵 geometry |

> [!warning] QKV 合并方式会改变算法
> 把 $W_Q,W_K,W_V$ 拼成一个大矩阵再做 polar，与分别对三块做 polar 一般不相等。前者允许跨块共享奇异子空间，后者保持 block boundary。必须把 grouping 写进配置和 checkpoint metadata。

## 五、梯度缺失、累积与分布式语义

### 5.1 grad is None 与零梯度不同

- grad is None 常表示该参数本步未参与计算；通常不更新 buffer、不 decay 或按框架合同处理；
- 显式零 tensor 表示参与计算但梯度为零，momentum 仍可能衰减并产生非零 update。

二者若被统一成零，会改变 sparse/conditional model 的状态。

### 5.2 gradient accumulation

若先累积 $k$ 个 microbatch 再调用 optimizer，Muon 看到的是聚合后的一个 $G_t$；若每个 microbatch 都更新 buffer，再延迟参数更新，状态轨迹不同。optimizer step 才是 $t$ 的定义，不能只报 global batch size。

### 5.3 distributed reduction

必须记录：

- gradient 在 orthogonalization 前还是后 all-reduce；
- tensor-parallel shard 上做局部 polar，还是 gather 后做全矩阵 polar；
- shape scaling 使用 global shape 还是 local shard shape；
- buffer 是 replicated、sharded 还是 partitioned。

一般而言，

$$
\operatorname{msign}\!\left(\sum_jG_j\right)
\ne\sum_j\operatorname{msign}(G_j),
$$

所以通信顺序不是实现细节。

## 六、状态、显存与 checkpoint

每个 Muon matrix 至少需要一个 momentum buffer，常见为 parameter-size 的一个 state tensor；临时 Newton–Schulz 还需要若干 workspace。总账应分别报告：

$$
\text{persistent state bytes},\quad
\text{peak temporary bytes},\quad
\text{communication bytes}.
$$

加载 checkpoint 时校验：

1. parameter name/shape 与 group membership；
2. buffer convention 是 EMA-style 还是 sum-style；
3. dtype 与 master-weight 策略；
4. shape adjustment mode；
5. Nesterov 开关与 NS coefficients/steps；
6. fused QKV 或 tensor-parallel layout 是否变化。

## 七、图：把“Muon step”拆成七个有版本的状态转移

先看图回答：若 momentum convention、QKV grouping 或 communication order 改变，哪一条状态边会使算法不再等价？

![[00-知识库管理/_assets/figures/training-optimization/fig-muon-state-transition-contract-v1.svg|900]]

> [!figure] 图 TRN-27　Muon 状态机、参数组与分布式合同
> 图从二维参数筛选开始，依次展示 EMA buffer、Nesterov、finite-step NS、shape adjustment、base-LR decay 和参数更新，并在下方标出 checkpoint 与 communication 分叉。来源：依据 [[S-2026-PyTorch-Muon]] 当前源码、[[S-2024-Jordan-Muon]] 原始实现说明独立绘制。

**怎样读图**：沿实线复现单步；遇到黄色菱形时，必须把选项和值写入实验配置。红色旁路表示常见但不等价的版本。

**图没有证明什么**：状态图只定义一次计算如何从输入和旧状态产生新状态，不证明该配置数值稳定、优化收敛，也不证明它在任何模型、数据或硬件上优于 AdamW。

## 八、最小可复现日志

    optimizer: muon
    implementation: torch.optim.Muon
    accessed_or_version: 2026-08-26
    parameter_filter: ndim == 2 and hidden_weight
    momentum: 0.95
    nesterov: true
    buffer_semantics: ema
    ns_steps: 5
    ns_coefficients: [3.4445, -4.7750, 2.0315]
    adjust_lr_fn: original
    base_lr: 0.001
    weight_decay: 0.1
    decay_uses_base_lr: true
    distributed_layout: global-gradient-before-local-update
    fallback_optimizer: adamw

这不是推荐超参数，而是“复现一条状态轨迹”所需字段的最小示例。

## 九、本节出口

你应能读源码画出精确 transition，解释为什么 momentum convention、grouping、decay order 与 communication order 都会改变算法，并为一次 checkpoint 迁移列出可验证的不变量。

## 练习与独立解答

- [[习题 - Muon 的动量、正交化与参数分组合同]]
- [[解答 - Muon 的动量、正交化与参数分组合同]]
