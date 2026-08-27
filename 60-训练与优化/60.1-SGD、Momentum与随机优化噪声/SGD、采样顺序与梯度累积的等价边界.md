---
type: theorem
status: verified
area: [training, optimization, gradient-accumulation]
node_id: TRN-03
aliases: [梯度累积等价条件, Gradient Accumulation]
prerequisites: ["[[训练系统的对象、状态与一步更新合同]]", "[[Mini-batch 梯度、平均求和与有效 Batch]]"]
related: ["[[Momentum、EMA、偏差修正与框架约定]]", "[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[随机种子、配对比较、置信区间与序贯决策]]"]
sources: ["[[S-2026-PyTorch-SGD-Semantics]]"]
exercises: ["[[习题 - SGD、采样顺序与梯度累积的等价边界]]"]
solutions: ["[[解答 - SGD、采样顺序与梯度累积的等价边界]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-sgd-accumulation-equivalence-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# SGD、采样顺序与梯度累积的等价边界

> [!abstract] 一句话结论
> 把 $K$ 个 micro-batch 的 gradient 在**同一参数与同一模型状态**上求和，按同一大 batch 目标归一化，并且只做一次非线性 gradient transform 和 optimizer step，才与一次大 batch update 等价。BatchNorm、逐 micro clipping、每次更新 optimizer state、重复加入 regularizer、不同随机实现和浮点规约顺序都能打破等价。

## 一、两种容易混淆的程序

设大 batch $I$ 被分成不相交 micro-batches $I_1,\ldots,I_K$，每块大小 $b_k$，总样本数 $B=\sum_kb_k$。

**程序 A：一次大 batch**

$$g_A=\frac1B\sum_{i\in I}\nabla\ell_i(\theta_t),
\qquad \theta_{t+1}=\mathcal U(\theta_t,s_t,g_A).$$

**程序 B：只累积 gradient**

$$g_B=\sum_{k=1}^K\frac{b_k}{B}
\left(\frac1{b_k}\sum_{i\in I_k}\nabla\ell_i(\theta_t)\right),$$

累积期间不改变 $\theta_t,s_t$，最后只调用一次 $\mathcal U$。

## 二、精确等价定理

> [!theorem] 梯度累积的代数等价
> 若（1）目标是 per-example loss 的可加权和；（2）所有 micro-batch 都在同一 $\theta_t$ 和相同决定性模型状态上求导；（3）每个样本的随机变量与大 batch 运行配对一致；（4）按 $b_k/B$ 归一化；（5）unscale、clipping、noise injection、optimizer step 与 scheduler 只在总梯度上执行一次；（6）使用精确算术，则 $g_B=g_A$，因而同一更新器给相同 $(\theta_{t+1},s_{t+1})$。

**证明**只用有限和的结合律：

$$
\begin{aligned}
g_B
&=\sum_{k=1}^K\frac{b_k}{B}\frac1{b_k}
\sum_{i\in I_k}\nabla\ell_i(\theta_t)\\
&=\frac1B\sum_{k=1}^K\sum_{i\in I_k}\nabla\ell_i(\theta_t)\\
&=\frac1B\sum_{i\in I}\nabla\ell_i(\theta_t)=g_A.
\end{aligned}
$$

每条条件都在保证“被相加的是同一批向量”。删除任何一条，都需要重新证明而不能继续引用此定理。

## 三、为什么“每个 micro-batch 做一步”不等价

取标量损失 $\ell_i(\theta)=\tfrac12(\theta-y_i)^2$，$\theta_0=0$，$y_1=1,y_2=3$，$\eta=0.1$。

一次大 batch gradient 是 $[(0-1)+(0-3)]/2=-2$，得到 $\theta_1=0.2$。

若依次做两步：

$$\theta'=0-0.1(-1)=0.1,$$

第二个 gradient 在新参数上是 $0.1-3=-2.9$，所以 $\theta''=0.39$。这已经是两个 optimizer steps，不是 gradient accumulation。

## 四、五类最重要的破坏因素

### 4.1 Batch-dependent forward：BatchNorm

BatchNorm 使用当前 micro-batch 的均值/variance。一个 $B=8$ 的 batch 与两个 $b=4$ micro-batches 会产生不同 normalized activations、loss、gradient 和 running statistics。即使最终相加，起点向量已经不同。

### 4.2 非线性 gradient transform：clipping

一般有

$$\operatorname{clip}(g_1)+\operatorname{clip}(g_2)
\ne\operatorname{clip}(g_1+g_2).$$

例如阈值 1，$g_1=2,g_2=-1$：左边 $1+(-1)=0$，右边 $\operatorname{clip}(1)=1$。

### 4.3 重复加入非数据项

若每个 micro loss 都加 $\lambda R(\theta)$ 而未除以 $K$，累积后 regularizer gradient 变成 $K\lambda\nabla R$。正确方式是把正则项只加一次，或每次按 $1/K$ 缩放。

### 4.4 optimizer/scheduler state 提前推进

Momentum buffer、Adam moments、step-based bias correction、warmup 和 weight decay 若每个 micro-step 都推进，就改变 state transition。即使参数暂时不更新，step counter 前进也可能使后续结果不同。

### 4.5 RNG 与有限精度

理论上 dropout 对 per-example additive loss 可通过配对相同 mask 保持等价；实际 vectorized 大 batch 与 sequential micro-batch 消耗 RNG 的顺序可能不同。浮点加法不满足严格结合律，规约树不同会产生末位差异：

$$(a+b)+c\ne a+(b+c)\quad\text{在有限精度中可能成立。}$$

因此应区分 exact algebraic equality、容差内 numerical equality 与最终统计 equivalence。

## 五、采样顺序为何也属于 SGD

固定数据集上常见策略：

- iid with replacement：每步可独立抽样，但一个 epoch 概念不自然；
- random reshuffling：每个 epoch 一次 permutation，再连续切 batch；
- sequential/curriculum：顺序携带结构，gradient noise 可能有长程相关；
- distributed sharding：每 rank 看到局部 shard，shuffle 与 `set_epoch` 决定全局顺序。

非线性目标下，顺序会通过参数轨迹产生作用。即便两个 epoch 使用同一 multiset，先后次序不同也一般不产生同一最终参数。

## 六、一个正确的 accumulation 归一化合同

若每个 micro-batch 都返回 **mean loss**，且大小相同 $b$，可把每个 loss 除以 $K$ 再 `backward()`：

$$\sum_{k=1}^K\nabla\frac{L_k^{mean}}K
=\frac1{Kb}\sum_{k,i\in I_k}\nabla\ell_i.$$

若 $b_k$ 不同或有效 token 数 $M_k$ 不同，不能简单除 $K$；应累计 loss sum，并最后除总有效计数 $M=\sum_kM_k$，或以 $M_k/M$ 加权每个 mean。

> [!warning] last partial batch
> 固定除以 accumulation steps 会错误缩小最后一个不完整窗口。合同必须根据真实有效样本/token 数处理，或明确丢弃不完整窗口。

## 七、图：等价证明的六道门

先看图回答：大 batch 与 accumulation 在哪一点合流，哪些操作必须放在合流以后？

![[00-知识库管理/_assets/figures/training-optimization/fig-sgd-accumulation-equivalence-v1.svg|900]]

> [!figure] 图 TRN-03　大 batch 与 micro-batch accumulation 的等价门和反例分支
> 绿色路径满足同参数、同目标、正确归一化、延后非线性处理与单次 step；红色分支展示 BatchNorm、per-micro clipping 和提前推进状态。来源：独立绘制。

**怎样读图**：从两条输入路径往中间的“总梯度”节点走；在合流前出现的任何 state mutation 或非线性处理都要单独审计。

**图没有证明什么**：流程图不保证 GPU kernel 的 bitwise equality，也不说明积累总能提升 wall-time；它只组织代数等价条件与常见反例。

## 八、在大模型训练中的应用

对 token loss，建议 checkpoint 记录：`micro_batch_sequences`、`tokens_per_microbatch`、`world_size`、`accumulation_steps`、`global_nonpad_tokens`、reduction、clip position、optimizer-step count 和 scheduler-step count。

若目标是模拟更大**优化器 batch**，gradient accumulation 可节省激活峰值内存；但它不能自动模拟：

- 大 batch BatchNorm statistics；
- 更高设备并行带来的 communication overlap；
- 不同 sequence packing 的 attention 计算图；
- 与 batch 共同重调的 LR 和 schedule；
- 更少 optimizer steps 对训练时域的影响。

## 九、本节回顾

- 精确等价的核心是：同参数上计算可加梯度，正确加权，最后只做一次非线性处理与 step；
- 参数更新、BatchNorm、clipping、regularizer 和 state counter 都可能破坏等价；
- 相同样本 multiset 不保证相同顺序轨迹；
- 浮点与 RNG 差异要和数学不等价分开诊断；
- 下一节 [[Momentum、EMA、偏差修正与框架约定]] 将说明 optimizer state 为什么不能在 micro-step 上随意推进。

## 练习与独立解答

- [[习题 - SGD、采样顺序与梯度累积的等价边界]]
- [[解答 - SGD、采样顺序与梯度累积的等价边界]]
