---
type: concept
status: verified
area: [training, mixed-precision, optimizer-state]
course_id: TRN-58
prerequisites: ["[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[随机梯度与小批量估计]]"]
related: ["[[随机舍入、无偏性与微小更新保留]]", "[[数据并行、All-Reduce 与全局 Batch 语义]]", "[[训练 Telemetry、损失梯度更新与激活总账]]"]
sources: ["[[S-2017-Micikevicius-Mixed-Precision-Training]]", "[[S-2023-NVIDIA-混合精度训练]]", "[[S-2026-PyTorch-AMP]]", "[[S-2019-Kalamkar-BFLOAT16-Training]]", "[[S-2022-Micikevicius-FP8-Formats]]"]
created: 2026-08-26
updated: 2026-08-26
---

# Loss Scaling、Master Weight 与低精度梯度累积

> [!abstract] 本节目标
> 从链式法则推导 loss scaling，解释动态 scale 的状态机；把“尝试反向”“成功 optimizer update”“scheduler/EMA/global step”分成不同时间，并正确处理 accumulation、clipping、DDP 与 master weights。

## 一、Loss scaling 不改变精确梯度方向

原 loss 为 $L(\theta)$，选正 scale $S$，定义

$$
\widetilde L=S L.
\tag{1}
$$

在精确算术中链式法则给

$$
\nabla_\theta\widetilde L=S\nabla_\theta L,
\qquad
g=\frac{1}{S}\widetilde g.
\tag{2}
$$

所以 unscale 后方向与原梯度完全相同。它的数值目的只是把反向中间量搬到格式的可表示窗口，不是增加 significand bits，也不是改变学习率。

若关键梯度绝对值落在 $[g_{min},g_{max}]$，低精度安全区近似为 $[q_{min},q_{max}]$，理想 scale 需同时满足

$$
\frac{q_{min}}{g_{min}}\lesssim S\lesssim\frac{q_{max}}{g_{max}}.
\tag{3}
$$

若左端大于右端，一个全局 $S$ 根本无法同时保住最小与最大梯度；需 per-tensor scale、更大 range 或高精度路径。

## 二、动态 GradScaler 是有状态控制器

一个简化状态机是：

1. 用当前 $S_t$ 放大 loss 并 backward；
2. unscale gradients；
3. 检查 Inf/NaN；
4. 若非有限：跳过 optimizer update，令 $S_{t+1}=bS_t$，$0<b<1$；
5. 若有限：执行 update，累计成功计数；连续 $K$ 次成功后令 $S_{t+1}=aS_t$，$a>1$。

因此至少有三个时钟：

$$
t_{attempt},\qquad t_{backward},\qquad t_{update}.
$$

发生 overflow 时，前两者可能推进而 $t_{update}$ 不推进。若 scheduler、EMA、weight decay、optimizer moments 或 checkpoint 名义 step 仍推进，就不再等价于“这个 batch 被安全跳过”。

[[S-2026-PyTorch-AMP]] 的当前实现允许 `scaler.step(optimizer)` 因非有限梯度跳过真正 update。训练循环必须显式决定 scheduler/EMA/logging 怎样对齐成功更新。

## 三、为什么需要 FP32 master weight

若模型权重只以低精度 $w_q$ 驻留，微小更新满足

$$
|\eta g|<\tfrac12\operatorname{ulp}(w_q),
$$

则

$$
Q(w_q-\eta g)=w_q,
\tag{4}
$$

更新被完全吞掉。master-weight 路线维护

$$
w_{32}^{t+1}=w_{32}^t-\eta g_{32}^t,\qquad
w_q^{t+1}=Q(w_{32}^{t+1}),
\tag{5}
$$

多个小更新可先在 FP32 中累积，跨过低精度格点后再反映到 forward copy。[[S-2017-Micikevicius-Mixed-Precision-Training]] 把它与 FP16 loss scaling 联合提出。

但不是所有现代 BF16/FP8 系统都用同一套 master policy；必须查 optimizer 与框架实际 storage，而不是把历史 recipe 当 API 保证。

## 四、Micro-batch accumulation 的正确归一化

设一个 optimizer update 由 $K$ 个 micro-batch 组成，第 $k$ 个有 $b_k$ 个有效样本，sample gradient 为 $g_{ki}$。全局样本平均应是

$$
g=\frac{1}{\sum_kb_k}\sum_{k=1}^K\sum_{i=1}^{b_k}g_{ki}.
\tag{6}
$$

若每个 micro-batch loss 已做 mean 且 $b_k=b$，可对每个 loss 除以 $K$ 后 backward；也可先累加和，再统一除以 $K$。若最后一个 micro-batch 更小，简单平均 $K$ 个 local means 会错误地让小 batch 权重过大。

加入 loss scale 后，一种一致流程是：

$$
\widetilde g_{acc}=\sum_{k=1}^KS\,w_k g_k,\qquad
g=\widetilde g_{acc}/S,
\tag{7}
$$

其中 $w_k=b_k/\sum_jb_j$。同一 accumulation window 内通常保持同一个 $S$，在 optimizer update 前统一 unscale 与 finite check。

## 五、顺序：unscale → inspect/clip → step

若 scaled gradient 是 $\widetilde g=Sg$，直接做 norm clipping

$$
\widetilde g\leftarrow\widetilde g\min\left(1,\frac\tau{\|\widetilde g\|}\right)
$$

等价于对真实梯度使用阈值 $\tau/S$，阈值随动态 scale 漂移。正确语义通常是：

1. backward/accumulate scaled gradients；
2. unscale；
3. 记录 finite、norm、分位数；
4. clip/regularize；
5. optimizer step；
6. scaler update；
7. 仅在成功 update 后推进与 optimizer 对齐的 scheduler/EMA。

## 六、与 DDP `no_sync` 的交互

数据并行 accumulation 常在前 $K-1$ 个 micro-batches 用 `no_sync`，最后一次才触发 collective。此时必须声明：

- local gradient buffer 是 scaled 还是 unscaled；
- collective 对 sum 还是 average；
- reduction dtype；
- overflow 是每 rank 本地判断还是全局 OR；
- 任一 rank overflow 时是否所有 ranks 同步跳过 update。

若 rank A 跳过而 rank B 更新，参数副本立即失同步。finite flag 本身也需要一致的 collective/控制流。

## 七、BF16 为什么常不需要、却也不禁止 scaling

BF16 与 FP32 有相同 exponent 位数，gradient range 通常足够，因此经典 loss scaling 动机较弱；但 BF16 fraction 更粗，不能靠 scaling 修复相对舍入精度。某些中间算子、通信压缩或 FP8 backward 仍可能需要 scale。结论应是“按 telemetry 判断”，不是“BF16 永不 scale”。

## 八、Skips 必须进入训练账本

每个 update window 至少记录：

| 字段 | 目的 |
|---|---|
| scale before/after | 重建控制器状态 |
| attempted/successful update | 区分训练时钟 |
| first nonfinite tensor/rank | 定位根因 |
| pre/post-unscale grad stats | 核对单位 |
| pre/post-clip norm | 核对控制器 |
| optimizer/scheduler/EMA counters | 检查是否错位 |
| accumulated sample/token count | 核对全局平均 |
| reduction dtype/world size | 核对 distributed 语义 |

“overflow 后自动恢复”若不报告 skip 率和 step 对齐，可能隐藏有效训练步数减少、学习率提前衰减或 moment history 断裂。

## 九、最小失败反例

设 scheduler 每次 attempt 都把学习率乘 $0.9$，但前 3 次因 overflow 未更新。第 4 次首次成功时，学习率已变为 $0.9^3\eta_0$；而理想的“跳过无效 step”语义应仍为 $\eta_0$。两者即使最终没有 NaN，也已是不同算法。

同理，若 decoupled weight decay 在 skipped step 仍执行，参数会在没有数据梯度时衰减；若 EMA 推进，teacher 会重复吸收同一 student state。

## 十、图解：一次 overflow 改变了哪些时钟

带着一个问题读图：**若 backward 已执行但 optimizer step 被跳过，scheduler、EMA、weight decay 与随机状态应否前进？**

![[00-知识库管理/_assets/figures/training-optimization/fig-loss-scaling-step-clock-v1.svg|900]]

> [!figure] 图 TRN-58-01　Dynamic loss scaling 状态机与多时钟合同
> 来源：自绘机制图；mixed-precision 逻辑依据 [[S-2017-Micikevicius-Mixed-Precision-Training]] 与 [[S-2026-PyTorch-AMP]]。

**怎样读图**：沿左栏走完 scale→backward→unscale→全局 finite consensus；随后把 NO 与 YES 分支分别映射到右栏时钟。特别检查 unscale、finite check、clip、step 的先后次序，以及各 rank 是否对 skip 达成一致。

**图没有证明什么**：状态机没有承诺所有框架版本都以相同条件增长 scale，也没有规定 scheduler/EMA 的唯一正确政策；这些必须在实验 manifest 中声明并以成功更新数对齐。

## 十一、验收协议

一个 mixed-precision 实验至少比较 FP32 reference、目标 policy 与“仅改一个部件”的诊断变体；报告 loss/quality、skip fraction、scale trajectory、zero/subnormal/nonfinite、update count、wall time、峰值内存与确定性层级。只有质量与资源同时达门，才能称该 policy 有效。
