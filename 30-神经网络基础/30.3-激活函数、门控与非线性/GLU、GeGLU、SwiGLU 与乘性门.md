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
updated: 2026-08-29
---
# GLU、GeGLU、SwiGLU 与乘性门

> [!abstract] 本章主问题
> GLU 不是把一个 activation 换成另一个，而是把两条 learned projections 做逐元乘法。它引入输入依赖的门和二阶交互，同时把标准两矩阵 FFN 变成三矩阵结构。比较必须匹配参数量、FLOPs、hidden width 与 fusion；“线性通道”也不等于无条件梯度捷径。

## 课程位置与两遍学习路线

- **承接什么：** NN-21 的 SiLU 是同一 scalar 自门控；GLU family 将 value 与 gate 改成两条可独立学习的 projections；
- **本页解决什么：** 从乘积微分推出 value/gate 两路 VJP，并把表达交互、三矩阵预算和 gate semantics 分账；
- **后续为何需要：** NN-23 将把软乘性调制换成 hard max winner，NN-24 再进行 matched-budget 比较。

**第一遍只画两支再相乘。** 给定 $V,G$，先算 gate output 和 $H=V\odot\phi(G)$，再用 product rule 分别回传到两支。

**第二遍再算系统预算。** 比较 $2dh$ 与 $3dh_g$、hidden width rounding、activation bytes、fusion、tensor parallel 与实际 latency。

### 问题链

1. self-gating 与两条 learned projections 的门控有什么表达差异？
2. 为什么 $\bar V$ 和 $\bar G$ 的公式不对称？
3. GLU gate 在 $(0,1)$，为何 GEGLU/SwiGLU 不能解释为概率开关？
4. 参数匹配为何要求 gated hidden width 约为普通 FFN 的 $2/3$？
5. “线性 value path”为什么不能保证梯度永不消失？

> [!check] 第一遍停靠线
> 若你能用统一 $V,G$ 算出 GLU/SwiGLU 输出与两路 cotangent，并在输入共享时说明 $\bar X$ 要相加，就可以进入 Maxout；预算与 fusion 留到第二遍。

## 符号与对象账本

| 对象 | shape | 在 AI gated FFN 中的身份 | reverse 结果 |
|---|---|---|---|
| $V=XW_v+b_v$ | hidden shape | value/content branch | $\bar V=U\odot\phi(G)$ |
| $G=XW_g+b_g$ | hidden shape | learned gate branch | $\bar G=U\odot V\odot\phi'(G)$ |
| $H=V\odot\phi(G)$ | hidden shape | multiplicatively selected feature | 接 output projection |
| $W_v,W_g,W_o$ | 三组矩阵 | gated FFN parameters | 约 $3dh_g$ 主参数 |
| $U=\bar H$ | hidden shape | upstream cotangent | 同时驱动两路 VJP |

### 贯穿算例：同一 value branch 的 GLU 与 SwiGLU

沿用 $G=s_\triangle=(-2,0,2)$，取 $V=(1,-1,2)$、$U=(1,1,1)$。GLU 给

$$
H_{\rm GLU}=V\odot\sigma(G)\approx(0.119203,-0.5,1.761594),
$$

$$
\bar V\approx(0.119203,0.5,0.880797),\qquad
\bar G\approx(0.104994,-0.25,0.209987).
$$

SwiGLU 给

$$
H_{\rm SwiGLU}=V\odot\operatorname{SiLU}(G)\approx(-0.238406,0,3.523188),
$$

$$
\bar V\approx(-0.238406,0,1.761594),\qquad
\bar G\approx(-0.090784,-0.5,2.181568).
$$

SwiGLU 的“gate”可负且无界，因此是 multiplicative branch，不是概率。若 $V,G$ 都来自同一 $X$，最终 $\bar X$ 必须合并两路 projection 的贡献。

## 核心公式七问：$dH=dV\odot\phi(G)+V\odot\phi'(G)\odot dG$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 同时描述 value 变化与 gate 变化如何影响乘性输出 |
| 对象 | $V,G,H$ 同 hidden shape；$dV,dG$ 来自不同 learned projections |
| 来路 | 对 Hadamard product 应用逐坐标 product rule |
| 步骤 | 固定 gate 得 value 项，固定 value 得 gate 项；reverse 再各自走 affine VJP |
| 读法 | 内容通过多少由 gate 决定，gate 的学习强度又被当前 value 缩放 |
| 检查 | $V=0$ 时 gate branch 暂无梯度；$\phi(G)=0$ 时 value branch 被关闭 |
| 去路 | Transformer SwiGLU FFN、bilinear interactions、conditional modulation 与 budget matching |

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
