---
type: derivation
status: draft
area: [neural-networks/activations, glu, swiglu, gating]
aliases: [Gated Linear Unit, GEGLU, SwiGLU]
node_id: NN-22
prerequisites: ["[[Softplus、GELU、SiLU 与平滑门控]]", "[[线性层与仿射层的反向传播]]"]
related: ["[[多层感知机与逐层前向计算]]", "[[激活函数的数值稳定、尺度与经验选择]]"]
sources: ["[[S-2017-Dauphin-Gated-Convolutional-Networks]]", "[[S-2020-Shazeer-GLU-Variants]]", "[[S-2022-Su-8934-FLASH-GLU-GAU]]"]
exercises: ["[[习题 - GLU、GeGLU、SwiGLU 与乘性门]]"]
solutions: ["[[解答 - GLU、GeGLU、SwiGLU 与乘性门]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-glu-gated-ffn-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---
# GLU、GeGLU、SwiGLU 与乘性门

> [!abstract] 本章主问题
> GLU 不是把一个 activation 换成另一个，而是把两条 learned projections 做逐元乘法。它引入输入依赖的门和二阶交互，同时把标准两矩阵 FFN 变成三矩阵结构。比较必须匹配参数量、FLOPs、hidden width 与 fusion；“线性通道”也不等于无条件梯度捷径。

## 一、统一定义

对 row-batch $X:[B,d]$，令

$$
V=XW_v+b_v,
\qquad
G=XW_g+b_g,
$$

广义 gated unit 为

$$
H=V\odot\phi(G).
$$

- GLU：$\phi=\sigma$；
- ReGLU：$\phi=\operatorname{ReLU}$；
- GEGLU：$\phi=\operatorname{GELU}$；
- SwiGLU：$\phi=\operatorname{SiLU}$；
- Bilinear：$\phi(G)=G$。

接输出投影 $Y=HW_o+b_o$ 才构成完整 gated FFN。

## 二、反向传播完整推导

给 $\bar H=U$，由

$$
dH=dV\odot\phi(G)+V\odot\phi'(G)\odot dG
$$

得

$$
\bar V=U\odot\phi(G),
\qquad
\bar G=U\odot V\odot\phi'(G).
$$

因此

$$
\bar X=\bar VW_v^T+\bar GW_g^T,
$$

$$
\bar W_v=X^T\bar V,
\qquad
\bar W_g=X^T\bar G,
$$

bias 梯度沿 batch/token 轴求和。两条输入路径必须相加。

## 三、为什么乘性门增加表达

若暂取 bilinear gate、忽略 bias，

$$
H=(XW_v)\odot(XW_g).
$$

每个 hidden coordinate 是两个线性 form 的乘积，即输入的二次函数；再经 $W_o$ 可组合低秩 quadratic interactions。普通 $\phi(XW)$ 只有一条 projection；门控显式提供 feature-by-feature modulation。

## 四、“Gate”并不总在 0 到 1

GLU 的 sigmoid gate 在 $(0,1)$；GEGLU/SwiGLU 的 $\phi(G)$ 可为负，正侧也无界，因此更准确的说法是 multiplicative branch，而非概率开关。其 scale 与 sign 都能调制 value branch。

## 五、参数与 FLOP 账本

忽略 bias，标准 FFN $d\to h\to d$ 有约 $2dh$ 参数；gated FFN 有 $W_v,W_g,W_o$，约 $3dh_g$。匹配参数量需

$$
h_g\approx\frac23h.
$$

实际 hidden width 常为硬件 tile 的倍数；必须报告 rounding 后的真实参数、MAC、activation bytes 和通信，而不是只引用 $2/3$ 口诀。

## 六、梯度通道边界

GLU value branch 对 $V$ 的 slope 是 $\sigma(G)$，若 gate 饱和到 0，所谓“线性路径”也被关闭；gate branch slope 还含 $V\sigma'(G)$。GEGLU/SwiGLU 的 slope 可负或超 1。门控可改善信息选择，不提供深度无关的 Jacobian 下界。

## 七、实现与融合

两次 input projection 常可拼为一次大 GEMM 后 split；activation–multiply 可融合；output projection 仍是一大 GEMM。需要审计 tensor-parallel shard、bias、activation checkpoint、quantization scale 和 intermediate storage。减少 $h_g$ 只匹配主导参数，不保证各硬件 wall-clock 相同。

## 八、图：两条 projection 如何汇合

先看图回答：为什么 SwiGLU 与 GELU-FFN 在相同 hidden width 下不是公平比较？

![[00-知识库管理/_assets/figures/neural-networks/fig-glu-gated-ffn-v2.svg|900]]

> [!figure] 图 30.3-06　GLU family：双投影、乘性汇合与预算匹配
> 左栏是 value/gate 双路图；中栏给出 differential 与两路 VJP；右栏比较 $2dh$ 和 $3dh_g$ 账本及 fused execution。来源：依据 Dauphin 等 2017、Shazeer 2020 与科学空间对 GLU/GAU 的结构辨析独立绘制；由 [[00-知识库管理/_labs/code/plot_activation_advanced_v2.py]] 确定性生成。

**怎样读图**：先追踪两条 forward projections，再在 reverse 中看 $\bar X$ 的两项，最后核对 hidden width 和三矩阵成本。

**图没有证明什么**：图没有证明 gated FFN 在所有模型规模或任务更优，也没有证明参数匹配等同于 FLOP、memory 与 latency 全匹配。

## 九、实验验收与回顾

比较 baseline/GLU/GEGLU/SwiGLU 时至少跑同 hidden width、matched parameters、matched FLOPs 三轨；记录 gate/value distributions、两支 gradient norm、fusion、memory、吞吐与多 seed metric。原论文结果只支持其协议范围。

> [!summary]
> GLU family 的核心是双 learned projection 的逐元乘积。它改变表达阶数、梯度路径和三矩阵预算；激活名称只是 gate branch 的一个组成部分。

- [[习题 - GLU、GeGLU、SwiGLU 与乘性门]]
- [[解答 - GLU、GeGLU、SwiGLU 与乘性门]]
