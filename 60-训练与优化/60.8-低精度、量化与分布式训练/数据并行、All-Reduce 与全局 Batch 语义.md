---
type: concept
status: verified
area: [training, distributed-training, data-parallelism]
course_id: TRN-61
prerequisites: ["[[随机梯度与小批量估计]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]"]
related: ["[[Tensor、Pipeline、Sequence 与 Expert Parallel]]", "[[ZeRO、FSDP、激活重计算与 Offload]]", "[[通信 Roofline、非确定性与分布式训练证据地图]]"]
sources: ["[[S-2026-PyTorch-DDP]]", "[[S-2009-Patarasuk-Bandwidth-Optimal-AllReduce]]", "[[S-2026-NVIDIA-NCCL-Collectives]]", "[[S-2026-PyTorch-AMP]]"]
created: 2026-08-26
updated: 2026-08-26
---

# 数据并行、All-Reduce 与全局 Batch 语义

> [!abstract] 本节目标
> 从全局样本平均独立推导 data-parallel gradient，正确处理 local mean/sum、world size、gradient accumulation、uneven token counts 与 loss scaling；能写出 ring All-Reduce 的消息量，并理解数学等价不保证逐比特等价。

## 一、数据并行复制什么、切分什么

同步 data parallel（DP）通常：

- 每个 data-parallel rank 保有同一模型副本；
- batch 沿样本/token 维切分；
- 各 rank 独立 forward/backward；
- 梯度经 collective 聚合；
- 所有 rank 以相同 optimizer state transition 更新。

参数副本一致依赖三个条件：相同初态、相同聚合梯度、相同更新控制流。只要一个 rank 因 overflow、unused parameter、异常数据或 scheduler 时钟走不同分支，副本就可能失同步。

## 二、从全局经验风险推导正确梯度

rank $r$ 有 $b_r$ 个有效样本，样本损失为 $\ell_{ri}(\theta)$。全局样本平均是

$$
L(\theta)=\frac{1}{B}\sum_{r=1}^P\sum_{i=1}^{b_r}\ell_{ri}(\theta),
\qquad B=\sum_{r=1}^Pb_r.
\tag{1}
$$

定义 local mean gradient

$$
g_r=\frac1{b_r}\sum_{i=1}^{b_r}\nabla\ell_{ri}.
$$

则真正的全局梯度是

$$
g=\sum_{r=1}^P\frac{b_r}{B}g_r.
\tag{2}
$$

只有 $b_r$ 全相等时，才简化为

$$
g=\frac1P\sum_{r=1}^Pg_r.
\tag{3}
$$

这就是常见“local mean + All-Reduce average”的数学来源，而不是框架习惯。

## 三、Local sum/mean × Collective sum/mean 的四格表

假设每 rank 样本数相等为 $b$：

| local loss reduction | collective | 得到的量 | 修正 |
|---|---|---|---|
| mean | average | 全局 mean | 无 |
| mean | sum | $P$ 倍全局 mean | 除以 $P$ 或调 LR，但需声明 |
| sum | sum | 全局 sum | 除以 $Pb$ 才是 mean |
| sum | average | $b$ 倍全局 mean | 除以 $b$ |

[[S-2026-PyTorch-DDP]] 当前文档特别提醒：若 local loss 用 sum，DDP averaging 与单设备对 $P b$ 样本做 sum 的梯度会相差 world size 因子。

## 四、Global batch 只乘 data-parallel degree

若每个 DP rank 每个 micro-batch 有 $b$ 个样本，accumulation steps 为 $K$，DP degree 为 $P_{DP}$，且无丢弃/不等长，则

$$
B_{global}=bK P_{DP}.
\tag{4}
$$

不能把 tensor-parallel 或 pipeline-parallel devices 再乘进去：它们协作计算同一批样本，不增加独立数据副本。一个 64-GPU job 若 $TP=8,PP=4$，则可用 $DP=2$；global batch 只乘 2。

## 五、Gradient accumulation 的二维账本

一个 optimizer update 由 micro-step $k=1,\ldots,K$ 和 DP rank $r=1,\ldots,P$ 组成：

$$
g=\frac{1}{\sum_{r,k}b_{rk}}
\sum_{r,k}\sum_{i=1}^{b_{rk}}g_{rki}.
\tag{5}
$$

常见实现用前 $K-1$ 次 `no_sync` 本地累积，最后一次做一次 collective。若每次 local loss 都是 mean，再简单除 $K$，只在 $b_{rk}$ 相等时正确。variable-length language modeling 更合理的是按 non-padding token 数加权。

必须记录：micro-batch samples、non-padding tokens、sequence packing、accumulation window、last partial batch、drop_last 与 sampler padding。

## 六、Uneven inputs 与样本权重

若某些 rank 更早耗尽数据，继续用初始 world size 除法会让每个已处理样本保持相同名义权重；改用剩余 rank 数则等价于一个动态变小的 DP group，并会放大尾部样本。[[S-2026-PyTorch-DDP]] 的 join 语义提供相关开关，但“选哪个”是 estimand 选择，不只是性能选项。

DistributedSampler 为了每 rank 等长可能复制或丢弃样本。若不报告，名义 epoch、unique samples 和 global batch 都会失真。

## 七、All-Reduce 的代数分解

对每 rank 大小为 $M$ bytes 的梯度，ring All-Reduce 可分成：

1. reduce-scatter：每 rank 最终得到全局 reduction 的一个 shard；
2. all-gather：交换 shards，使每 rank 得到完整结果。

对 $P$ ranks，大消息主导下每 rank 通信量约

$$
V_{ring}=2\frac{P-1}{P}M.
\tag{6}
$$

同时需要 $2(P-1)$ 个环阶段，故简化时延模型为

$$
T_{ring}\approx2(P-1)\alpha+2\frac{P-1}{P}\frac{M}{B_{eff}}.
\tag{7}
$$

$\alpha$ 是每阶段 latency，$B_{eff}$ 是有效链路带宽。[[S-2009-Patarasuk-Bandwidth-Optimal-AllReduce]] 支持带宽下界与 ring 路线；现代 [[S-2026-NVIDIA-NCCL-Collectives]] 仍会按拓扑和消息大小选择其他算法。

## 八、Bucket 与 overlap

若等整个 backward 结束才 All-Reduce，step time 近似

$$
T\approx T_f+T_b+T_{comm}+T_{opt}.
$$

DDP 把梯度按 bucket 分组，在 bucket ready 时启动通信，理想情况下可隐藏一部分：

$$
T\approx T_f+\max(T_b,T_{comm}^{overlap})+T_{tail}+T_{opt}.
\tag{8}
$$

bucket 太小会增加 latency，太大会推迟首个 collective；参数注册/ready 顺序、unused parameter 和网络 contention 决定真实 overlap。

## 九、Loss scaling 与全局 overflow

若每 rank 用同一 scale $S$，可先聚合 scaled gradients 再统一除 $S$；但任何 rank 出现 Inf/NaN 时，所有 ranks 必须一致跳过。finite flag 可做 global OR/max collective。

若各 rank scale 不同，直接 All-Reduce scaled gradient 得

$$
\frac1P\sum_rS_rg_r,
$$

无法用一个 $S$ 反缩放成全局平均。per-rank dynamic scale 必须先本地 unscale 或同步 scale 状态。

## 十、数学等价不等于逐比特等价

实数加法满足结合律，浮点加法不满足。不同 ring/tree、bucket、world size 和 ready order 会改变括号：

$$
((g_1+g_2)+g_3)+g_4
\ne
(g_1+g_2)+(g_3+g_4)
$$

在有限精度中可能逐比特不同。合理验证分三层：collective algebra oracle；数值容差；多 seed 的训练质量/失败分布。逐比特不同不自动表示算法错误，但失去容差或统计结论必须调查。

## 十一、图解：先保全局 estimator，再审通信尾巴

带着一个问题读图：**三个 rank 的有效样本数不相等时，“平均三个 local mean”为什么不一定等于全局 sample mean？**

![[00-知识库管理/_assets/figures/training-optimization/fig-data-parallel-global-batch-allreduce-v1.svg|900]]

> [!figure] 图 TRN-61-01　样本加权全局梯度与 ring All-Reduce
> 来源：自绘机制图；collective 结构依据 [[S-2009-Patarasuk-Bandwidth-Optimal-AllReduce]]、[[S-2026-NVIDIA-NCCL-Collectives]]，DDP 合同依据 [[S-2026-PyTorch-DDP]]。

**怎样读图**：左栏把每个 rank 的梯度和 $s_r$ 与有效样本数 $n_r$ 都保留到 collective 之后，最终只除一次 $\sum_r n_r$；右栏再把 ring 的 reduce-scatter/all-gather 字节量与 bucket-ready、延迟项和未遮蔽尾巴分开。

**图没有证明什么**：环图不表示 NCCL 在任意 topology 都固定采用同一算法，也没有包含 protocol、channel、contention 和实际 overlap；代数等价也不推出逐比特等价。

## 十二、最小 DP manifest

记录 DP group/ranks、local sample/token count、loss reduction、collective operator/divisor/dtype、accumulation与 `no_sync`、sampler padding、uneven join、bucket、overflow consensus、optimizer/scheduler clocks、data order 和 communication bytes/time。缺少其中任何一项，“从 1 GPU 扩到 64 GPU 等价”都不可复核。
