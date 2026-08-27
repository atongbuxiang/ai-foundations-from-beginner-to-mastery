---
type: solution
status: draft
area: [architecture, efficient-attention, performer, random-features]
topic: "[[Performer、随机特征与近似误差]]"
exercise: "[[习题 - Performer、随机特征与近似误差]]"
sources: ["[[S-2021-Choromanski-Performer]]", "[[S-2020-Su-7921-Performer随机投影]]", "[[S-2021-Su-8338-Performer到线性Attention]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Performer、随机特征与近似误差

## A. 识别与复述

### ARCH-PERF-A01
缩放后的未归一化 softmax kernel 为 $K(q,k)=\exp(q^\top k/\sqrt{d_h})$。Attention 还需对每个 query 的可见 keys 计算分母 $\sum_jK(q,k_j)$，再以 $K/\sum K$ 加权 V；近似未归一化 kernel 不等于已完成 normalized attention。

### ARCH-PERF-A02
对 $\omega\sim\mathcal N(0,I)$，单样本正 feature 可写为 $g_\omega(x)=\exp(\omega^\top x-\|x\|^2/2)$。取 $m$ 个 draws，$\phi(x)=m^{-1/2}(g_{\omega_1}(x),\ldots,g_{\omega_m}(x))$，则 $\widehat K(q,k)=\phi(q)^\top\phi(k)=m^{-1}\sum_rg_{\omega_r}(q)g_{\omega_r}(k)$。

### ARCH-PERF-A03
输出是两个相关随机估计量之比 $\hat N/\hat D$。期望不与非线性倒数交换，通常 $\mathbb E[\hat N/\hat D]\ne\mathbb E\hat N/\mathbb E\hat D=N/D$；小 denominator 还会放大相关误差。

## B. 手算与建模

### ARCH-PERF-B01
$g_0(1)=e^{-1/2}$，$g_0(2)=e^{-2}$，乘积为 $e^{-5/2}\approx0.0821$；真实 $e^{qk}=e^2\approx7.389$。无偏性是对 $\omega$ 的期望陈述，单个 draw 可以离期望很远。

### ARCH-PERF-B02
真实 ratio 为 $2$；扰动后为 $6.3/2.9\approx2.17241$，变化 $0.17241$。一阶变化为 $\delta N/D-N\delta D/D^2=0.3/3-6(-0.1)/9=0.16667$，接近但不完全相同。

### ARCH-PERF-B03
理想独立有限方差下标准误差按 $m^{-1/2}$，从 64 到 256 缩小为原来的 $\sqrt{64/256}=1/2$。feature state、feature 计算和 $S\in\mathbb R^{m\times d_v}$ 的主内存/MAC 约增 4 倍。

## C. 推导与证明

### ARCH-PERF-C01
令 $a=q+k$。高斯矩母函数给 $\mathbb E e^{\omega^\top a}=e^{\|a\|^2/2}$，故
$$\mathbb E[g_\omega(q)g_\omega(k)]=e^{-(\|q\|^2+\|k\|^2)/2}e^{\|q+k\|^2/2}=e^{q^\top k}.$$
缩放可吸收到 q/k，使目标变为 $e^{q^\top k/\sqrt d}$。

### ARCH-PERF-C02
写成 $(N+\delta N)D^{-1}(1+\delta D/D)^{-1}$，用 $(1+x)^{-1}=1-x+O(x^2)$：
$$\frac{N+\delta N}{D+\delta D}-\frac ND=\frac{\delta N}{D}-\frac{N\delta D}{D^2}+O(\|\delta\|^2).$$
第二项含 $D^{-2}$，说明小分母尤其放大 denominator error。

### ARCH-PERF-C03
固定随机矩阵 $\Omega$ 后，所有 tokens 使用同一映射 $\phi_\Omega$，于是任意 pair 的估计来自同一个 Gram/kernel realization，且 cached state 与新 query 兼容。若每 token 重采样，query/key features 不再共享同一基，内积估计恒等式和历史 state 坐标都变了；这不是同一个可缓存模型。

## D. 边界、反例与纠错

### ARCH-PERF-D01
令随机变量 $X$ 以相同概率取 1、3；设 $\hat N=X$、$\hat D=X$。二者期望都为 2，所以目标期望之比为 1；这里 ratio 仍为 1。要得到有偏，令 $\hat N=1$ 恒定、$\hat D$ 取 1/2、3/2，均值为 1，则 $\mathbb E[\hat N/\hat D]=(2+2/3)/2=4/3\ne1$。numerator、denominator 都无偏，ratio 有偏。

### ARCH-PERF-D02
$g_\omega(q)g_\omega(k)$ 是 log-normal 型量；二阶矩包含 $e^{2\|q+k\|^2}$ 一类快速增长项，大 norm/同向向量可形成重尾。把 $q,k$ 按 $d^{-1/4}$ 缩放、控制 norm、稳定计算和正交/结构化 draws 可缓解，但不把有限-$m$ 误差自动消除。

### ARCH-PERF-D03
增加 $m$ 降低固定 Q/K kernel Monte Carlo error 的趋势，不等于训练后任务性能单调：容量、正则化、优化噪声、数值 overflow、训练时间、kernel 实现与随机 seed 都会同时变化。单调性需要实验而非从 $1/\sqrt m$ 直接推出。

## E. AI 迁移

### ARCH-PERF-E01
同一批 Q/K/V，先报告逐 pair kernel relative error；再报告每行分母与 normalized weights 的 TV/$L_1$；再报告 attention output norm/cosine；最后把误差传播到 block/final logits 和任务预测。按 norm、位置、长度与 denominator 分桶，给 p50/p90/p99 和 seed 置信区间。

### ARCH-PERF-E02
随机矩阵应是模型 state：初始化 seed 与生成算法版本入配置/checkpoint；训练 replica 明确共享还是独立且可复现；eval 固定；加载 checkpoint 恢复同一矩阵而非重采样；cached prefix 与后续 decode 必须用同一 realization；分布式 shard/serialization 保持坐标和 dtype 一致。

### ARCH-PERF-E03
取对数网格 $m$，在固定 checkpoint 近似和从头训练两种协议下分别测 kernel/ratio/output error 分位数、state bytes、峰值显存、prefill/decode latency、吞吐与长序列任务质量。报告多 seed、crossover、失败/OOM 和与 dense exact baseline 的差值。
