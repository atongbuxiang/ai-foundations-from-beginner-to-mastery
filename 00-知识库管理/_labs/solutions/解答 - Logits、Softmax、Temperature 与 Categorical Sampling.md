---
type: solution
status: verified
area: [language-models, decoding]
topic: "[[Logits、Softmax、Temperature 与 Categorical Sampling]]"
exercise: "[[习题 - Logits、Softmax、Temperature 与 Categorical Sampling]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Logits、Softmax、Temperature 与 Categorical Sampling

## A. 识别与复述

### LM49-A01
Logit 是模型输出的未归一化实数分数；softmax probability 是对该向量归一化得到的原始 next-token 分布；rollout kernel 是经过 bias、penalty、mask、temperature、truncation 与重归一化后真正用于采样的分布。三者只有在没有任何 processor 时才可能后两者相同。

### LM49-A02
有限 $\tau>0$ 时除以同一正数，不改变 logit 排名。odds 变为 $\exp[(z_i-z_j)/\tau]$：降温放大差异，升温缩小差异。熵对温度非减，但 token 熵不能直接代表语义多样性或质量。

### LM49-A03
按固定 token 顺序构造累计和 $F_j=\sum_{i\le j}p_i$，取 $U\sim U[0,1)$，返回首个满足 $U<F_j$ 的 token。相同 $U$ 若使用不同排列会映射到不同 token，所以若要求轨迹级重现，遍历/排序及并列规则也必须固定。

## B. 手算与构造

### LM49-B01
减去最大值后权重为 $(1,e^{-1},e^{-2})\approx(1,.3679,.1353)$，和为 $1.5032$，故概率约为 $(.6652,.2447,.0900)$。用稳定 softmax 与直接 softmax 理论相同，数值更安全。

### LM49-B02
odds 为 $e^{1.4/\tau}$。$\tau=.7$ 时为 $e^2\approx7.389$；$\tau=1.4$ 时为 $e^1\approx2.718$。升温使两个 token 更接近，但不交换排名。

### LM49-B03
累计区间为 token 1: $[0,.5)$，token 2: $[.5,.8)$，token 3: $[.8,1)$。故 $.49\to1$，$.50\to2$，$.81\to3$。边界答案依赖明确的半开区间约定。

## C. 推导与证明

### LM49-C01
$$
\frac{e^{z_i+c}}{\sum_je^{z_j+c}}
=\frac{e^ce^{z_i}}{e^c\sum_je^{z_j}}
=\frac{e^{z_i}}{\sum_je^{z_j}}.
$$
因此 logits 只在加性常数的等价类上可识别。

### LM49-C02
写 $p_\beta(i)=e^{\beta z_i}/Z$，则 $H=\log Z-\beta E_\beta[z]$。利用 $d\log Z/d\beta=E[z]$ 与 $dE[z]/d\beta=\operatorname{Var}(z)$，有 $dH/d\beta=-\beta\operatorname{Var}(z)$。又 $d\beta/d\tau=-1/\tau^2$，故 $dH/d\tau=\operatorname{Var}_\tau(z)/\tau^3\ge0$。

### LM49-C03
链式法则给
$$q(y_{1:T}\mid x)=\prod_{t=1}^Tq(y_t\mid x,y_{<t}).$$
每个 $q_t$ 都是在实际生成历史上重算的 kernel；不能把各位置的边缘概率独立相乘。

## D. 边界、反例与纠错

### LM49-D01
$\tau=0$ 使 $z/\tau$ 未定义。Greedy 是单独的 argmax 算子；它可视为唯一最大项时 $\tau\to0^+$ 的分布极限。若最大项并列，softmax 极限在并列项均匀，而具体 greedy 还需 tie-break。

### LM49-D02
两请求固定同 seed 与模型；实现一用 per-request counter RNG，另一把 batch 中所有请求共享 RNG stream。Continuous batching 插入一个新请求后，第二实现多消耗随机数，原请求随后的 token 改变。两者可各自服从正确边缘分布，却不具同 seed 轨迹一致性。

### LM49-D03
例：原概率 $(.6,.25,.15)$、top-$p=.7$。先 top-$p$ 保留前两项；若先高温使分布接近均匀，达到 $.7$ 可能需要三项。候选 support 已改变，因此算子一般不交换。

## E. AI 迁移

### LM49-E01
至少保存 checkpoint/hash、input token IDs、tokenizer/template、每个 processor 的名称/参数/顺序、最终 support 与 sampler、RNG algorithm/device/state/counter、stop/max tokens、batch/scheduler、kernel/hardware 版本及 output token IDs/finish reason。

### LM49-E02
固定概率 $(.5,.3,.2)$，使用相互独立 seeds 采样例如 $N=100000$ 次；报告三项频数、理论期望、二项置信区间或多项 goodness-of-fit 检验。预注册显著性与容差，不用单次 seed 判断；同时测试 $U$ 在累计边界附近的单元案例。

### LM49-E03
固定模型、prompt 集、processor 顺序和 token 预算，只扫预注册温度。每温度用多 seed，分别报告 entropy/distinct/repetition 与事实准确、引用支持、安全指标及 CI；把多样性和事实质量作为不同坐标画 Pareto，而不是合成“创造力分数”。
