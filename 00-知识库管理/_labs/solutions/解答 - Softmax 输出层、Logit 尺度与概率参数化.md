---
type: solution
status: draft
area: [neural-networks/embedding-output, softmax, categorical-output]
topic: "[[Softmax 输出层、Logit 尺度与概率参数化]]"
exercise: "[[习题 - Softmax 输出层、Logit 尺度与概率参数化]]"
sources: ["[[S-2022-Su-9070-logsumexp不等式]]", "[[S-2016-Goodfellow-Bengio-Courville-Deep-Learning]]", "[[S-2023-Su-9698-Output-Embedding]]"]
created: 2026-08-24
updated: 2026-08-24
---
# 解答 - Softmax 输出层、Logit 尺度与概率参数化

## A

### NN-SOP-A01

采用 row-vector batch convention，$W\in\mathbb R^{V\times d_h}$、$b\in\mathbb R^V$；hidden $H\in\mathbb R^{B\times T\times d_h}$ 经 $z=W h+b$ 得 $Z\in\mathbb R^{B\times T\times V}$，概率 $P$ shape 相同。softmax 只沿最后的 vocabulary/class 轴归一化，使每个 $(b,t)$ 位置的 $\sum_{v=1}^VP_{btv}=1$，不能跨 batch 或 sequence position 归一化。

### NN-SOP-A02

对任意标量 $c$，$z$ 与 $z+c\mathbf1$ 给出同一概率，所以公共 offset 不可辨识；可辨识的是 $V-1$ 个独立 logit differences 或 log odds。可固定 $\sum_i z_i=0$，也可固定一个参考类 $z_V=0$；数值计算常减去 $\max_i z_i$，这是为稳定性选择的输入相关 gauge。

### NN-SOP-A03

有限 $z_i$ 使 $e^{z_i}>0$ 且分母有限，因此每个 $p_i>0$；精确 $p_i=0$ 只能由 $z_i-z_j\to-\infty$ 的极限达到。若某类结构上不允许，工程合同应在 softmax 前用布尔 mask 将其扩展实数 logit 设为 $-\infty$，并保证至少一个有效类；有限的巨大负数只是在给定 dtype 下近似零。

## B

### NN-SOP-B01

$\tau=1$ 时，除以 $e^2+e+1$：

$$
p\approx(0.66524,0.24473,0.09003),
\qquad H\approx0.83240\ \text{nats}.
$$

$\tau=2$ 等于对 $(1,0.5,0)$ 做 softmax：

$$
p\approx(0.50648,0.30720,0.18632),
\qquad H\approx1.02019\ \text{nats}.
$$

argmax 都是第一类，但更高 temperature 缩小 logit differences，分布更平、熵更高。

### NN-SOP-B02

任何 logits 可写为 $z_i=\log p_i+c$。令和为零，取

$$
c=-\frac13\sum_i\log p_i.
$$

因为 $(\log0.5,\log0.3,\log0.2)\approx(-0.693147,-1.203973,-1.609438)$，均值约 $-1.168852$，故

$$
z\approx(0.475705,-0.035121,-0.440585).
$$

其和在舍入误差内为零。加任意 $a\mathbf1$ 后，分子分母同乘 $e^a$，概率不变。

### NN-SOP-B03

$e^{1001}$ 会远超常见浮点范围。减去最大值 1001 得 $(0,-1,-2)$，于是

$$
p=\frac{(1,e^{-1},e^{-2})}{1+e^{-1}+e^{-2}}
\approx(0.66524,0.24473,0.09003).
$$

$(1001,1000,999)=(2,1,0)+999\mathbf1$，shift invariance 保证结果相同；稳定算法避免先形成巨大指数。

## C

### NN-SOP-C01

$$
\operatorname{softmax}_i(z+c\mathbf1)
=\frac{e^{z_i+c}}{\sum_j e^{z_j+c}}
=\frac{e^ce^{z_i}}{e^c\sum_j e^{z_j}}
=p_i.
$$

并且

$$
\frac{p_i}{p_j}=\frac{e^{z_i}}{e^{z_j}}=e^{z_i-z_j},
$$

取对数即

$$
\boxed{\log(p_i/p_j)=z_i-z_j}.
$$

这也说明 categorical law 只有 $V-1$ 个可辨识自由度。

### NN-SOP-C02

令 $s=z/\tau$，one-hot target 为 $y$。对 $s$ 的标准结果是 $\nabla_sL=p-y$；链式法则给

$$
\boxed{\nabla_zL=\frac1\tau(p-y)}.
$$

softmax Jacobian 对 $s$ 为 $\operatorname{Diag}(p)-pp^\mathsf T$，再乘一次 $1/\tau$：

$$
\boxed{
\nabla_z^2L=\frac1{\tau^2}
\left[\operatorname{Diag}(p)-pp^\mathsf T\right]
}.
$$

该矩阵是 categorical one-hot 的 covariance，半正定，且 $\mathbf1$ 是零特征方向，对应 shift gauge。

### NN-SOP-C03

写 $\beta=1/\tau$、$A(\beta)=\log\sum_i e^{\beta z_i}$。熵

$$
H=-\sum_i p_i\log p_i=A(\beta)-\beta\,\mathbb E_p[z].
$$

由 $A'(\beta)=\mathbb E_p[z]$ 与 $d\mathbb E_p[z]/d\beta=\operatorname{Var}_p(z)$，

$$
\frac{dH}{d\beta}=-\beta\operatorname{Var}_p(z).
$$

又 $d\beta/d\tau=-1/\tau^2$，所以

$$
\boxed{
\frac{dH}{d\tau}
=\frac{\operatorname{Var}_p(z)}{\tau^3}\ge0
}.
$$

有限 $\tau$ 下等号当且仅当所有具有正概率的 logits 相等；softmax 对所有类给正概率，因此等价于全部 $z_i$ 相同。

## D

### NN-SOP-D01

小概率可能在 probabilities tensor 中下溢为零，随后 `log(0)` 得 $-\infty$；大 logits 也可能在先 exponentiate 时溢出。对 target $y$ 应直接计算

$$
L=-z_y+\operatorname{LSE}(z)
=-z_y+m+\log\sum_j e^{z_j-m},
\quad m=\max_jz_j.
$$

框架的 fused cross-entropy/log-softmax 还能减少中间张量和舍入，并使用已知的 $p-y$ backward；无需先物化概率再取 log。

### NN-SOP-D02

padding mask 在 encoder/attention 中阻止 padded key/value 被读，并在 loss reduction 中排除 padded query/target 位置；causal mask 施加于 attention score matrix，禁止位置 $t$ 读取未来位置；词表禁用 mask 才施加于 output logits 的 vocabulary 轴，再做 softmax。有限负常数 $-M$ 仍有 $e^{-M}>0$ 的实数概率，且在低精度、缩放或 temperature 改变后可能不再足够小；$-\infty$ mask 才表达扩展实数上的精确禁用语义。

### NN-SOP-D03

正温度缩放不改变 logits 排序，所以 top-1 accuracy 可完全不变；它改变概率置信度，若模型原本已较合适，降低 temperature 会过度自信，使正确样本的少量收益被错误样本的大 NLL 惩罚压过，ECE 也可上升。temperature 是校准参数，应只在独立 validation/calibration split 上拟合，最后一次性评估 test；在 test 上调温会泄漏。

## E

### NN-SOP-E01

冻结 $z_0(x)$ 与预测边界，扫描 $z=s z_0$，$s>0$。同一测试样本的 argmax/accuracy 理论上不变（无 ties/数值异常时）；entropy 随 $s$ 增大通常下降。NLL 和 ECE 可能先改善后恶化，因为存在最佳校准尺度；对 cross-entropy 的 logit gradient 是 $s$ 所在图的链式组合，需同时报告对 scaled logits 与对 base logits 的范数。另记录 exp/LSE 非有限率、最大 logit 与 dtype；每个 $s$ 由 validation 选择，test 只评一次。

### NN-SOP-E02

对单个上下文，只要允许自由选择 $V$ 个 logits，就能表示任意严格正 categorical law（边界为极限）。但线性 head 共享 $W,b$，所有上下文满足 $z(x)=Wh(x)+b$；若把多个上下文的 log-probability vectors 排成矩阵，它们被限制在由 hidden dimension、bias 与 softmax gauge 决定的低维仿射族中。故“点上满射”不推出“跨上下文函数族无限制”；这正是后续 Softmax Bottleneck 节点要形式化的区别。

### NN-SOP-E03

基线必须真实形成或分片计算 $H W^\mathsf T$，记录 FLOP、kernel throughput、参数/激活/temporary memory；用分布式 max 和 sum-exp 的 collective 字节与延迟完成精确归一化。训练报告 exact held-out NLL、perplexity、top-k、ECE，并按频率分桶；近似 sampled/hierarchical/adaptive 方案要在同一 token、参数/compute 预算下比较，额外报告其训练目标偏差，以及用 exact full-softmax evaluation 得到的最终 NLL。还需记录 checkpoint/optimizer 分片与 failure recovery，避免只比较局部 kernel 时间。
