---
type: solution
status: verified
area: [training, optimization, gradient-accumulation]
topic: "[[SGD、采样顺序与梯度累积的等价边界]]"
exercise: "[[习题 - SGD、采样顺序与梯度累积的等价边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - SGD、采样顺序与梯度累积的等价边界

## A. 识别与复述

### TRN03-A01
同一参数/模型状态；per-example 可加目标；配对相同样本随机量；按真实 $b_k/B$ 或 token count 归一；非线性 transform 只在合流后一次；optimizer/scheduler state 只推进一次。精确等价还假定精确算术。

### TRN03-A02
Accumulation 冻结参数和 optimizer state，只把多个 backward 结果相加，最后一步。Per-micro stepping 会更新参数并重算后续 gradient，同时推进 momentum、decay、bias correction 和 schedule，算法是 $K$ 步 SGD。

### TRN03-A03
后一个样本的 gradient 在前面样本已经改变的参数上计算；非线性目标下更新不交换。顺序还影响 optimizer state、RNG 和 batch-dependent layers。

## B. 手算与构造

### TRN03-B01
大 batch gradient $=[(0-1)+(0-3)]/2=-2$，一步得 $0.2$。顺序两步：第一步 gradient $-1$ 得 $0.1$；第二步 gradient $0.1-3=-2.9$，得 $0.39$。

### TRN03-B02
正确 token mean $=(3\cdot2+7\cdot5)/(3+7)=41/10=4.1$。错误的等权 micro mean 为 $(2+5)/2=3.5$，它把两个 micro-batch 而非 token 等权。

### TRN03-B03
Per-micro：$clip(2)+clip(-1)=1-1=0$。合并后：$clip(2-1)=clip(1)=1$。非线性造成不等价。

## C. 推导与证明

### TRN03-C01
$\sum_k(b_k/B)(1/b_k)\sum_{i\in I_k}g_i=(1/B)\sum_k\sum_{i\in I_k}g_i=(1/B)\sum_{i\in I}g_i$。第一步消去 $b_k$，第二步使用 $I_k$ 不交且并为 $I$。

### TRN03-C02
每个 micro objective 为 $L_k+\lambda R$，累计 gradient 是 $\sum_k\nabla L_k+\sum_k\lambda\nabla R=\sum_k\nabla L_k+K\lambda\nabla R$。大 batch 若只含一次 regularizer 则系数应为 $\lambda$；故每块需除 $K$ 或最后单独加一次。

### TRN03-C03
顺序第二步使用 $g_2(\theta_1)$，其中 $\theta_1=\theta_0-\eta g_1(\theta_0)$。Batch gradient 使用 $[g_1(\theta_0)+g_2(\theta_0)]/2$。除非 $g_2$ 对该位移不变或发生特殊抵消，否则 $g_2(\theta_1)\ne g_2(\theta_0)$。

## D. 边界、反例与纠错

### TRN03-D01
取标量 activations：大 batch $[-1,1,9,11]$ 的均值 5；分成 $[-1,1]$ 与 $[9,11]$，micro means 是 0 与 10。BatchNorm 后的 normalized activations 和 running mean 都不同，因此 gradient 不再只是同一 per-example 项的重排。

### TRN03-D02
在常见浮点中取 $a=10^{20},b=-10^{20},c=1$：$(a+b)+c=1$，而 $a+(b+c)$ 中 $b+c$ 舍入为 $-10^{20}$，结果 0。不同规约树可产生末位乃至小量差异。

### TRN03-D03
每个 loss 除 $K$ 时最后 gradient 只有正确 mean 的 $K'/K$ 倍。修正为按实际 $K'$ 除，或累计 loss/token numerator 与真实 denominator，或丢弃最后窗口并明确数据口径。

## E. AI 迁移

### TRN03-E01
每个 micro loss 按目标归一后 `scale(loss).backward()`；非最后 micro 使用 `no_sync`；最后触发 all-reduce；随后 `unscale_`；检查 finite/overflow；对全局 gradient clip；`optimizer.step()`；`scaler.update()`；成功 step 时按约定推进 scheduler/EMA；最后 zero grad。

### TRN03-E02
MLP 无随机层：大 batch 与 accumulation gradients/updates 应在 dtype 容差内相同。加入 BatchNorm：预期不同并验证 running stats。加入 clipping：分别把 clip 放在 per-micro 和总梯度，验证反例；同时覆盖不等长最后窗口。

### TRN03-E03
数值：规约/RNG 不同；吞吐：串行 accumulation 不等于并行设备；通信：DDP 规约次数可不同；BN：统计 batch 不同；schedule：optimizer steps/seen tokens 的时钟不同。它只可能模拟同目标下的 optimizer batch update。

## 无提示重做

- [ ] 不看正文写出六道等价门。
- [ ] 手写一个能够故意触发三种失败分支的测试。
