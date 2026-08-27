---
type: solution
status: verified
area: [language-models, decoding, inference-acceleration]
topic: "[[Speculative Decoding、Acceptance 与分布精确性]]"
exercise: "[[习题 - Speculative Decoding、Acceptance 与分布精确性]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Speculative Decoding、Acceptance 与分布精确性

## A. 识别与复述

### LM55-A01
Draft 廉价地从 $q$ 提候选；target 计算同历史下的 $p$；acceptance 保留两分布的重叠质量 $\min(p,q)$；拒绝时 residual $(p-q)_+$ 补回 target 相对 draft 缺失的质量。Target 没被跳过，只把多个位置合入一次验证。

### LM55-A02
Distribution exact 表示边缘输出序列分布与 target sampler 相同；fixed-seed identical 要求 RNG 消耗、数值与调度轨迹也对齐；wall-clock faster 是硬件成本结论。第一项可由概率证明，后两项需更强实现合同与 benchmark。

### LM55-A03
$\alpha=\sum_x\min(p_x,q_x)=1-\operatorname{TV}(p,q)$。它是对 proposal $X\sim q$ 的平均接受概率，也是两分布重叠系数。

## B. 手算与构造

### LM55-B01
逐 token proposal 条件接受率为 A: $\min(1,.5/.35)=1$；B: $.3/.45=2/3$；C: 1。平均接受率为 $.35(1)+.45(2/3)+.2(1)=.85$，拒绝率 $.15$。$(p-q)_+=(.15,0,0)$，故拒绝 residual 全部采 A。

### LM55-B02
$E[A]=\sum_{k=1}^4.8^k=.8+.64+.512+.4096=2.3616$。这是独立同率近似下接受的 draft token 数，不含全部接受后可能追加的 target bonus。

### LM55-B03
基线生成 3 tokens 约 $30$ ms；speculative 一轮成本 $8+13+1=22$ ms，提交 3 tokens，估计 speedup $30/22\approx1.36$。这不是 $3$ 倍，因为 draft 与验证也耗时。

## C. 推导与证明

### LM55-C01
Proposal 并接受 $x$ 的质量为 $q_x\min(1,p_x/q_x)=\min(p_x,q_x)$。总拒绝率 $R=\sum_x(p_x-q_x)_+$；拒绝后 $x$ 的无条件质量为 $R[(p_x-q_x)_+/R]=(p_x-q_x)_+$。相加为 $\min(p_x,q_x)+(p_x-q_x)_+=p_x$。

### LM55-C02
对每项，$\min(p,q)=(p+q-|p-q|)/2$。求和得
$$\sum_x\min(p_x,q_x)=\frac{1+1-\sum_x|p_x-q_x|}{2}=1-\frac12\sum_x|p_x-q_x|.$$
右侧即 $1-\operatorname{TV}(p,q)$。

### LM55-C03
位置 $i+1$ 的 target/draft 条件分布依赖位置 $i$ 实际提交的 token。若 $x_i$ 被拒并由 residual 换成 $y_i$，原先后续候选是在含 $x_i$ 的历史上提出/验证，不再对应含 $y_i$ 的历史；继续接受会破坏条件链。故首拒绝后丢弃后缀并从新历史重启。

## D. 边界、反例与纠错

### LM55-D01
$q(x)=0$ 的 token不会被 proposal，因此不计算实际候选的 $p/q$；若 $p(x)>0$，其全部质量出现在 $(p-q)_+$ residual 中。实现应安全计算 clipped differences/normalization，不能因除零把 target support 丢掉。

### LM55-D02
接受率只决定候选被利用程度。速度还取决于 draft cost、target 验证 shape、$\gamma$、bonus、kernel launch、batch/concurrency、KV 回滚和内存。高负载时普通 batching 已很高效，speculation 甚至可能降低吞吐。

### LM55-D03
Speculative 路径会为 proposal、accept/reject、residual 消耗不同数量/顺序随机数；并行归约和 scheduler 也会改变数值或 RNG stream。只要每条路径的无条件分布仍为 $p$，逐 seed 字节不同不否定 distribution exact。

## E. AI 迁移

### LM55-E01
用 3-token 分布枚举理论 $p$，实现 baseline 与 speculative，独立采样大量次数；比较频率/CI 与两样本检验。覆盖 $p=q$、disjoint/partial support、$q=0<p$、极小 residual、EOS/processor。另写确定性质量守恒断言，不只依赖 Monte Carlo。

### LM55-E02
每轮保存 history hash、draft tokens 与逐位 $q$、target $p$、uniforms、accept ratios/results、首拒绝位置、residual、committed/bonus tokens、discarded KV、draft/verify 时间、batch shape、KV bytes、processor/tokenizer/stop 版本与最终 finish reason。

### LM55-E03
冻结 target、workload、scheduler 与 SLO；正交扫描 draft 模型/量化和 $\gamma$。报告逐位置 acceptance、committed/target-call、draft/verify 开销、TTFT/TBT p99、throughput/goodput、KV 与质量等价检验。在相同并发/arrival trace 上找 Pareto，不以接受率单独选型。
