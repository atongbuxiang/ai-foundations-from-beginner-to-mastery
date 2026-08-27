---
type: solution
status: verified
area: [language-models, evaluation, sampling]
topic: "[[Pass-at-k、Best-of-N、采样估计与选择偏差]]"
exercise: "[[习题 - Pass-at-k、Best-of-N、采样估计与选择偏差]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Pass-at-k、Best-of-N、采样估计与选择偏差

## A. 识别与复述

### LM59-A01
单样本成功率是随机取一次生成成功的概率；oracle pass@$k$ 是 $k$ 个候选至少一个正确；selector success 是实际选择器返回的一个候选正确；用户效用还扣除延迟、token、验证成本与失败风险。前者高不保证后者高。

### LM59-A02
$n$ 是为一道题实际生成并执行测试的总样本数，$c$ 是其中通过数，$k\le n$ 是想估计的候选子集大小。组合式对“从已生成的 $n$ 个样本中均匀不放回选 $k$ 个”求至少一个成功的概率。

### LM59-A03
$N$ 增大通常提高候选覆盖，但 selector 要从更大集合找一个，噪声最大值和 winner's curse 更严重；同时 prefill/decode、verifier 与延迟成本增长。故必须比较固定总预算下的端到端 utility，而不只是 oracle coverage。

## B. 手算与构造

### LM59-B01
$$
1-(1-.2)^k=1-.8^k.
$$
$k=1$ 为 $.2$；$k=3$ 为 $1-.512=.488$；$k=5$ 为 $1-.32768=.67232$。这是 iid 假设下的理论值。

### LM59-B02
失败样本有 $7$ 个：
$$
1-\frac{\binom72}{\binom{10}2}
=1-\frac{21}{45}
=\frac{24}{45}\approx .5333.
$$

### LM59-B03
四个候选中至少一个真实效用为 1，所以 oracle coverage 为 1。Selector 取分数最高的第一个候选，而其真实效用为 0，故 selected success 为 0。这正说明覆盖与选择是两道门。

## C. 推导与证明

### LM59-C01
$k$ 次都失败的概率在 iid 下为 $(1-p)^k$。至少一次成功是其补事件，所以概率为 $1-(1-p)^k$。若样本相关或每次成功率不同，该乘积必须改写。

### LM59-C02
从 $n$ 个样本均匀选 $k$ 个共有 $\binom nk$ 种；若没有任何成功，必须全部来自 $n-c$ 个失败样本，共 $\binom{n-c}k$ 种。取补得到
$$1-\frac{\binom{n-c}k}{\binom nk}.$$
若 $n-c<k$，无法选出全失败子集，约定组合数为 0，估计量等于 1。

### LM59-C03
设 selector 观察 $\hat u_i=u_i+\epsilon_i$ 并选 $i^\star=\arg\max_i\hat u_i$。被选事件偏向 $\epsilon_i$ 较大的候选，因此通常
$$\mathbb E[\epsilon_{i^\star}]>0,$$
即 $\hat u_{i^\star}$ 对真实 $u_{i^\star}$ 乐观。候选越多或噪声越大，极值选择偏差往往越强；需独立 verifier/test 重新测量。

## D. 边界、反例与纠错

### LM59-D01
每题生成 10 个候选，其中常有一个正确，故 pass@10 高；但 selector 偏好冗长、带错误调用的候选，实际 top-1 常错。若产品只返回 selector 的一个答案，用户看到的是低 selected success。

### LM59-D02
更大 $N$ 消耗更多 token、显存、验证器调用与排队时间；相关采样还可能只复制同一错误模式。若选择器噪声不降，更多候选甚至放大错误极值。因此不是免费，也不保证端到端单调。

### LM59-D03
正相关样本的有效独立次数小于 $k$，iid 公式通常高估新增覆盖；若采用刻意多样化且成功事件负相关，iid 公式又可能低估覆盖。可靠做法是保留题目内联合样本并在 item 层估计。

## E. AI 迁移

### LM59-E01
固定每题总生成 token、最大 wall time、GPU-seconds 与 verifier 调用数；A/B 使用相同题目与停止/失败规则。报告 pass@$k$、selected success、成本和 latency 分布，用 item-paired 区间比较，并画质量—成本 Pareto。

### LM59-E02
Selector 只能在 training/validation 上开发；隐藏 test 只用于最终选择结果的独立执行。保存所有候选、selector 原始分数与最终索引；若 verifier 使用同一 tests，就不能再把这些 tests 当独立用户成功证据。

### LM59-E03
定义：对目标题目总体，在固定采样预算下生成 $N$ 个答案，以预注册规范化后的 plurality 返回答案，测最终正确率。题目是独立单位、题内 samples 相关；区间对 item 做 paired bootstrap，另报 vote margin、样本分歧、token/latency 和失败。
