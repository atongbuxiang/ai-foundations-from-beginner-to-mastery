---
type: solution
status: verified
area: [training, numerical-computing, mixed-precision]
topic: "[[Loss Scaling、Master Weight 与低精度梯度累积]]"
exercise: "[[习题 - Loss Scaling、Master Weight 与低精度梯度累积]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Loss Scaling、Master Weight 与低精度梯度累积

> [!warning] 使用边界
> 以下状态机是算法合同，不替代当前框架文档；尤其要实测 scale 增长、overflow consensus、fused optimizer 与 skipped-step 行为。

## A. 识别与复述

### TRN58-A01
loss scaling 把小 gradient 临时放大，减少 backward 中 underflow；master weight 让参数更新在更细格点上累积；accumulation 把多个 micro-batch 的 gradient estimator 合成目标大 batch。前者不改善参数 storage ulp，后两者也不会救已经在 backward 变成 0 的梯度，因此不能替代。

### TRN58-A02
attempt 是一次训练循环尝试，backward 是完成一次反传，successful update 是 finite 且真正改变 optimizer state 的事件。moments 与 decoupled decay通常只随成功 update 前进；EMA、scheduler 可有不同设计，但必须绑定并记录。若 overflow 时 scheduler 仍前进，学习率序列已不同。

### TRN58-A03
状态至少为 $(S,growth,backoff,interval,streak)$。finite：执行更新，$streak\leftarrow streak+1$；到 interval 后 $S\leftarrow growth\cdot S$ 并清零 streak。overflow：skip update，$S\leftarrow backoff\cdot S$，清零 streak。分布式条件是所有 rank 对 finite/overflow 使用同一 consensus。

## B. 手算与构造

### TRN58-B01
保留最小量要求 $S2^{-30}\ge2^{-24}$，故 $S\ge2^6=64$；避免最大量溢出要求 $S2^8\le2^{15}$，故 $S\le2^7=128$。粗略安全区间为 $[64,128]$。真实系统还要为中间激活、瞬时 outlier 与 rounding 留余量。

### TRN58-B02
总和 $(3,6)+(5,1)=(8,7)$，总样本 4，所以正确 mean 为 $(2,1.75)$。两个 local mean 为 $(1,2)$ 与 $(5,1)$，简单平均得 $(3,1.5)$；它给每个 micro-batch 等权，而非每个样本等权。

### TRN58-B03
依次为：成功后 $S=1024,u=1$；第二次成功触发增长，$S=2048,u=2$；overflow 后 $S=1024,u=2$；成功后仍 $1024,u=3$；再成功触发 $S=2048,u=4$。attempt 数为 5，successful-update 数为 4。

## C. 推导与证明

### TRN58-C01
$S$ 对参数视为常数，故 $\nabla_\theta(SL)=S\nabla_\theta L$；除以同一 $S$ 恢复精确梯度，方向不变。有限精度中，scale 会改变 underflow/overflow、舍入、融合与 finite-check 路径，所以“精确代数不变”不等于执行逐比特不变。

### TRN58-C02
记 $clip_\tau(g)=g\min(1,\tau/\|g\|)$。先 clip $Sg$ 再除 $S$：
$$
\frac1Sclip_\tau(Sg)=g\min\left(1,\frac{\tau}{S\|g\|}\right)=clip_{\tau/S}(g).
$$
阈值随动态 $S$ 改变。正确顺序是先 unscale，再 inspect/clip。

### TRN58-C03
若低精度参数当前相邻格距为 $\Delta(w)$，$|\eta u_t|<\Delta(w)/2$ 时一次 round-to-nearest 更新可能回到原值。master copy $w^{32}$ 每次在 FP32 上执行 $w^{32}\leftarrow w^{32}-\eta u_t$，多次小量不会在低精度副本处反复清零；需要 forward 时才 cast，累计超过边界后副本发生可见变化。

## D. 边界、反例与纠错

### TRN58-D01
若两个 micro-batch 大小 3 与 1，只除 micro-step 数等权其 local means，得到题 B02 的错误 $(3,1.5)$。variable-length LM 中 padding mask 还使有效 token 数不同；应累计 loss/gradient sum 与有效 count，最后除总 count。

### TRN58-D02
若 rank 0 overflow 而 skip、rank 1 finite 而 step，参数立即不同；下一轮 collective 混合来自不同模型的梯度，moments、scheduler 和 RNG 也会分叉。必须把 nonfinite flag 做全局 OR，并让所有 rank 同时 step 或同时 skip。

### TRN58-D03
初始学习率 $\eta_0$，前三次 overflow。若 scheduler 每 attempt 乘 0.9，第四次首次更新用 $0.9^3\eta_0$；若绑定 successful update，则仍用 $\eta_0$。EMA 若提前推进，也会多次吸收同一参数。没有参数 step 不等于没有算法状态变化。

## E. AI 迁移

### TRN58-E01
流程：清梯度；对前 $K-1$ 个 micro-step 在 `no_sync` 中做 scaled loss backward，并累计 sum/count；最后一个触发 DDP reduction；按全局 count 归一、unscale；对 nonfinite 做跨 rank OR；finite 时 clip→optimizer step→成功时钟上的 scheduler/EMA，overflow 时全员 skip；更新 scaler；再 zero-grad。任何 fused 路径都要验证等价次序。

### TRN58-E02
每 attempt 一行：attempt/backward/update id、rank、scale before/after、growth streak、loss/activation/gradient amax、zero/subnormal/Inf/NaN count、unscaled norm、clip coefficient、local/global overflow flag、optimizer/scheduler/EMA 是否推进、有效 sample/token count、step time。这样才能区分数值异常与控制流副作用。

### TRN58-E03
三组基线至少为 FP32；完整目标 policy；单因素变体如 FP32 accumulate、固定 scale、FP32 reduction。配对 data/init seeds，报告 learning curve、最终质量区间、skip/失败率、更新数、wall time、peak memory。以达到同一质量阈值的时间与资源验收，单 step 更快但多训练/多失败不算胜利。

## 无提示重做

- [ ] 48 小时后重画 finite/overflow 状态机。
- [ ] 一周后仅凭 telemetry 判断一次学习率时钟错位。
