---
type: solution
status: verified
area: [training, optimization, parameterization, mup]
topic: "[[μP 的 Maximal Update 与宽度尺度推导]]"
exercise: "[[习题 - μP 的 Maximal Update 与宽度尺度推导]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - μP 的 Maximal Update 与宽度尺度推导

> [!warning] 使用边界
> 表格采用固定深度、统一 hidden width、行向量 forward 与 Tensor Programs V 表 3 的无额外 parameter-multiplier 版本；换坐标、optimizer 或特殊层必须重译。

## A. 识别与复述

### TRN43-A01
maximal 指在前向、输出和训练稳定约束下，选择仍不发散的最大 width 量级，使 hidden feature update 不趋零。raw LR 还乘 optimizer direction 和 group scale；hidden matrix 每个 entry 更新 $1/n$ 仍可经 $n$ 项聚合形成 $O(1)$ feature change，因此不要求每坐标 $O(1)$。

### TRN43-A02
初始化权重近似独立、零均值，和的方差相加，幅度按 $\sqrt n$；gradient update 常为 $x_i\delta_j$ 外积，与再次乘入的同一个 $x_i$ 对齐，$\sum_ix_i^2$ 按 $n$。若更新与输入真正独立零均值，仍可能按 $\sqrt n$；必须审计相关性。

### TRN43-A03
在指定表约定下：
- input weights/all biases：init variance $1/\mathrm{fan\_in}$，SGD LR $\mathrm{fan\_out}$，Adam LR $1$；
- hidden：init variance $1/\mathrm{fan\_in}$，SGD LR $1$，Adam LR $1/\mathrm{fan\_in}$；
- output：init variance $1/\mathrm{fan\_in}^2$，SGD/Adam LR 都为 $1/\mathrm{fan\_in}$。
$1$ 表示 width-invariant base constant；方向、base-width ratio 和矩阵 orientation 必须一并声明。

## B. 手算与构造

### TRN43-B01
$$
\Delta y=-\gamma_n\delta\sum_i1=-2n\gamma_n.
$$
$n=100$ 时三者分别为 $-20,-2,-0.02$。随 $n$ 看：$1/\sqrt n$ 给 $\sqrt n$ 爆炸；$1/n$ 给常数非退化；$1/n^2$ 给 $1/n$ 消失。

### TRN43-B02
$$
\delta^2_j=\sum_{k=1}^{d_{out}}W^3_{jk}\delta^3_k=O(1/n),
$$
因为输出维固定。又 $\nabla W^2_{ij}=h^1_i\delta^2_j=O(1/n)$。SGD 保留梯度尺度，用 LR $O(1)$；Adam direction 近似 $O(1)$，需 LR $O(1/n)$。

### TRN43-B03
width multiplier 为 $1024/256=4$。若 base LR 是 base-coordinate 常数，hidden Adam actual group LR 为 $\eta_0/4=5\times10^{-4}$，readout 同为 $5\times10^{-4}$；input Adam LR 保持 $2\times10^{-3}$。真实实现还需按各 tensor 的 base fan-in 计算，不是简单按总 model width。

## C. 推导与证明

### TRN43-C01
$W^3=O(1/n)$、有限 $d_{out}$ 给 $\delta^2=O(1/n)$；故 $\nabla W^2=h^1\otimes\delta^2=O(1/n)$。再反传
$$
\delta^1_i=\sum_{j=1}^nW^2_{ij}\delta^2_j.
$$
$W^2_{ij}=O(n^{-1/2})$、$\delta^2_j=O(n^{-1})$，在初始化近似随机抵消下幅度为
$$
\sqrt n\cdot n^{-1/2}\cdot n^{-1}=n^{-1}.
$$
因此固定输入坐标 $x_r=O(1)$ 时 $\nabla W^1_{ri}=x_r\delta^1_i=O(1/n)$。训练后依赖增强时需由 Tensor Programs/实测补严。

### TRN43-C02
随机和有 $n$ 项，单项尺度 $n^{-p-a}$，故 output RMS 为
$$
n^{1/2-p-a}.
$$
对齐更新有 $n$ 项，单项尺度 $n^{-p-u}$，故 feature update 为
$$
n^{1-p-u}.
$$
两者非退化常数给
$$
p+a=\frac12,\qquad p+u=1.
$$
readout 可允许初始输出严格更小，但训练更新仍需第二个条件。

### TRN43-C03
若 $g=O(1/n)$，且 $m=O(1/n),v=O(1/n^2)$，
$$
\frac{m}{\sqrt v+\epsilon}\approx O(1)
$$
仅在 $\epsilon\ll1/n$。此时 hidden LR 需 $1/n$。若 $\epsilon\gg1/n$，
$$
\frac{m}{\sqrt v+\epsilon}\approx\frac{O(1/n)}{\epsilon},
$$
direction 仍含 $1/n$，原表的“Adam 消尺度”近似失效；早期 bias correction 与非平稳 moments 也需检查。

## D. 边界、反例与纠错

### TRN43-D01
input SGD gradient 为 $O(1/n)$，为了得到 $O(1)$ input-neuron motion，LR 反而为 $O(n)=\mathrm{fan\_out}$；hidden SGD gradient 本身已是 $O(1/n)$，LR 为 $O(1)$。只有 hidden/output Adam 等组在该表中显式随 fan-in 变小。

### TRN43-D02
令 $\Delta W_{ij}=\varepsilon_{ij}/n$，符号独立于 $x$。对固定 $j$，$\sum_ix_i\Delta W_{ij}$ 典型为 $\sqrt n/n=1/\sqrt n$；若 $\Delta W_{ij}=x_i\delta_j/n$，则为 $\delta_j\sum_ix_i^2/n=O(1)$。entry RMS 同为 $1/n$，feature update 不同。

### TRN43-D03
μP readout 初始 std $1/n$ 让随机 logit 为 $1/\sqrt n$，但训练后与 hidden activation 对齐的 $1/n$ update 可给 $O(1)$ logit change；zero initial logits 还对应均匀初始预测。若若干步后 logit/update仍随 width 消失、loss 不响应或 coord check 斜率错误，才支持退化失败。

## E. AI 迁移

### TRN43-E01
示例行：input $a=1/2$（相对固定 $d_{in}$ 无 width exponent）、raw grad $1/n$、SGD direction $1/n$、LR $n$、$\Delta W=1$、$\Delta h=1$；hidden init $1/\sqrt n$、grad $1/n$、SGD/Adam direction 分别 $1/n/1$、LR $1/1n$、$\Delta W=1/n$、$\Delta h=1$；readout init/update $1/n$、两 optimizer LR $1/n$、$\Delta z=1$。需按具体坐标重写。

### TRN43-E02
$t=0$ 记录 init entry/activation/logit；$t=1$ 保存 raw grad、moment-normalized direction、actual group LR、$\Delta W$、$\Delta h$；到 $t=8$ 看趋势。init 已漂移指向 fan/init；raw grad正确而 actual update错指向 group/scheduler；小梯度区 direction随 width保留 $1/n$ 指向 $\epsilon$；entry update正确但 $\Delta h$ 错指向相关性/orientation。

### TRN43-E03
先声明实际 forward 是 $xW$ 还是 $xW^\top$；从 base/delta 检查哪一维是 fan-in/fan-out；手算一层 init/gradient/feature exponent；打印每组实际 init std 和 LR；用多 width one-step coord check 验证；再用有限差分或 autograd 对 custom orientation 做小尺寸梯度检查。

## 无提示重做

- [ ] 48 小时后从 readout 倒推完整三层 exponent。
- [ ] 一周后解释为什么 Adam 与 SGD 表不同。
