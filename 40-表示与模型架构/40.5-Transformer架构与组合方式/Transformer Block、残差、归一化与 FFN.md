---
type: concept
status: draft
area: [architecture, transformer, residual, normalization, feed-forward]
aliases: [Transformer Block, Pre-LN Transformer, Post-LN Transformer]
node_id: ARCH-33
prerequisites: ["[[Multi-Head Attention、投影子空间与参数量]]", "[[残差块 Jacobian 与梯度直通]]", "[[LayerNorm 的逐样本几何与反向传播]]", "[[GLU、GeGLU、SwiGLU 与乘性门]]"]
related: ["[[Transformer 架构与组合方式 MOC]]", "[[Transformer Encoder 与双向表示]]", "[[Transformer 表达、稳定性与证据边界]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2020-Xiong-Transformer-LayerNorm]]", "[[S-2022-Wang-DeepNet]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]", "[[S-2022-Su-8994-Why-Residual]]", "[[S-2022-Su-9009-PreNorm-PostNorm]]", "[[S-2026-Chen-Attention-Residuals]]", "[[S-2026-Su-11664-Attention-Residuals]]"]
exercises: ["[[习题 - Transformer Block、残差、归一化与 FFN]]"]
solutions: ["[[解答 - Transformer Block、残差、归一化与 FFN]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-transformer-block-wiring-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Transformer Block、残差、归一化与 FFN

> [!abstract] 本节主问题
> 一个 Transformer block 不是“只有 Attention”，而是两类互补变换的交替：Attention 在 token/节点轴混合信息，FFN 在每个位置独立混合通道；每个子层外还有 residual、normalization 与随机正则。Pre-Norm 与 Post-Norm 不是代码顺序偏好，它们改变恒等路径是否经过 normalization Jacobian。

## 一、先把输入对象写清

令 residual stream

$$
X\in\mathbb R^{B\times T\times d}.
$$

标准 block 保持外部 shape 不变：输入与输出都是 $(B,T,d)$。内部含：

1. Multi-head self/cross-attention：token mixing；
2. position-wise FFN：channel mixing；
3. 两次 residual addition；
4. 两个 normalization；
5. 可选 attention/FFN dropout、residual dropout、DropPath 等。

外部 shape 相同是 residual 相加的必要条件；如果分支宽不同，必须先投影回 $d$。

## 二、Pre-Norm 的逐步执行

对 self-attention block，常见 Pre-LN 写为

$$
U=X+\mathcal D_a\big(\operatorname{MHA}(\operatorname{LN}_1(X))\big),
$$

$$
Y=U+\mathcal D_f\big(\operatorname{FFN}(\operatorname{LN}_2(U))\big).
$$

$\mathcal D$ 表示训练时随机正则，eval 时按合同关闭/缩放。许多现代语言模型还在堆叠末尾加 final norm：$H=\operatorname{LN}_f(X_L)$。

注意两次 LN 统计分别由 X 与 U 计算，不能复用。Attention mask 只进入 MHA，不进入 FFN。

## 三、Post-Norm 的逐步执行

原始 Transformer 的形式可写为

$$
U=\operatorname{LN}_1\big(X+\mathcal D_a(\operatorname{MHA}(X))\big),
$$

$$
Y=\operatorname{LN}_2\big(U+\mathcal D_f(\operatorname{FFN}(U))\big).
$$

名称 Pre/Post 是相对于每个 residual branch $F$ 而言：LN 在 $F$ 前还是 residual addition 后。只写“先 LN”而不画 residual 路径很容易误判混合结构。

## 四、Jacobian 为何不同

对一个抽象子层 $F$：

$$
\text{Pre: }y=x+F(N(x)),
\qquad
J_{pre}=I+J_F(N(x))J_N(x).
$$

恒等项 I 不被 $J_N$ 左乘。Post-LN 为

$$
\text{Post: }y=N(x+F(x)),
$$

$$
J_{post}=J_N(x+F(x))(I+J_F(x)).
$$

这两式是精确链式法则，但并未单独证明深层梯度范数。[[S-2020-Xiong-Transformer-LayerNorm]] 的更强初始化梯度结论还依 mean-field、宽度和随机假设。

## 五、FFN 到底做什么

最基本 FFN 对每个 token 行共享参数：

$$
\operatorname{FFN}(x)=\phi(xW_1+b_1)W_2+b_2,
$$

$$
W_1\in\mathbb R^{d\times d_{ff}},\quad
W_2\in\mathbb R^{d_{ff}\times d}.
$$

它不跨位置读取：对 $X$ 的每一行应用同一函数。因此 attention 先把其他位置的信息写进本位置表示，FFN 再对这些通道做非线性重组。

门控变体如 SwiGLU 常写

$$
\operatorname{SwiGLU}(x)=\big(\operatorname{SiLU}(xW_g)\odot xW_u\big)W_d,
$$

有三组主矩阵而非两组；参数/FLOP 总账必须重算，不能仍用 $2dd_{ff}$。

## 六、Residual 不只是“防梯度消失”

对缩放残差

$$
y=x+\varepsilon F(x;\theta),
$$

有

$$
\frac{\partial y}{\partial x}=I+\varepsilon J_F,\qquad
\frac{\partial y}{\partial\theta}=\varepsilon\frac{\partial F}{\partial\theta}.
$$

所以 $\varepsilon$ 同时调节状态 Jacobian 与参数更新通道。[[S-2022-Su-8994-Why-Residual]] 用 DeepNet 尺度分析解释这一点；课程保留精确 Jacobian，且把 $1/L$ 的确定性最坏累积、$1/\sqrt L$ 的随机方差尺度与训练 update scale 分账。

## 七、Pre/Post 的结论为何不能一句话裁决

[[S-2022-Su-9009-PreNorm-PostNorm]] 从精确展开

$$
x_L=x_0+\sum_{l=0}^{L-1}F_l(N(x_l))
$$

提出：若 residual stream 随深度增长而每层增量相对变小，Pre-LN 可能出现“深度稀释”。展开为 `I`；相邻深层近似相同、因此等效浅而宽属于有条件 `H/E`。

公平比较至少分别调：初始化、residual scale、warm-up、学习率、final norm、深度、训练 token 与任务。更易训练、最终 loss 更低、迁移更好和更鲁棒是四个不同结论。

## 八、DeepNorm 与深度相关参数化

[[S-2022-Wang-DeepNet]] 使用

$$
x_{l+1}=\operatorname{LN}(\alpha x_l+G_l(x_l;\theta_l))
$$

及深度相关初始化控制模型更新。[[S-2021-Su-8978-千层Transformer困难]] 对“增量爆炸”与 $\alpha/\lambda$ 尺度给出中文推导。具体系数随 encoder/decoder 结构而变，不能从一个简式跨架构复制。

千层训练成功是论文协议下的 `E`；update bound 是保留假设的 `T`；不等于任意任务都应无限加深。

## 九、2026 前沿：Attention Residuals

标准递推展开后是对历层分支的固定单位权累加。[[S-2026-Chen-Attention-Residuals]] 改为让当前层沿**深度轴**对先前表示做内容依赖 softmax 聚合；Block AttnRes 再用块级摘要降低历史激活与流水通信。

这改变的不只是 residual scale，而是跨层信息路由对象。[[S-2026-Su-11664-Attention-Residuals]] 提供设计演化脉络；正式 scaling/消融和大模型结果回查论文。它仍是版本化前沿证据，不是新默认 block，也不让 depth attention weights 自动成为因果解释。

## 十、Dropout、DropPath 与执行语义

- attention dropout 作用在权重或分支内部；
- residual dropout 作用在分支输出、相加前；
- DropPath/stochastic depth 以样本/层为单位跳过整个 branch；
- eval、checkpoint recomputation 与 distributed RNG 必须复现相同 mask；
- 把 dropout 放在 residual stream 主路径会改变恒等合同。

这些位置不同，不能统称“加了 0.1 dropout”。

## 十一、图：Block 接线

先看图回答：Pre-Norm 的哪条路径没有经过 LN Jacobian？为什么 FFN 虽对每个 token 独立，仍能处理上下文信息？

![[00-知识库管理/_assets/figures/architecture/fig-transformer-block-wiring-v1.svg|900]]

> [!figure] 图 40.5-01　Transformer block 的 Pre/Post-Norm 接线与 FFN
> 左中栏对照两种 residual wiring，右栏展示逐 token channel transform。来源：依据 Transformer、LayerNorm 与 residual Jacobian 独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_transformer_v1.py]] 生成。

**怎样读图**：沿残差主路径逐算 shape，再对每个 addition 写 Jacobian；不要把竖直流程图当作没有旁路。右栏的 FFN 权重对位置共享，但输入已携带 attention 汇入的上下文。

**图没有证明什么**：它没有证明 Pre-LN 或 Post-LN 普遍更优，也没有证明 DeepNorm/AttnRes 在未测试架构上稳定或更高效。

## 十二、常见错误与掌握标准

常见错误：漏掉第二个 residual/LN；把 FFN 当跨 token 卷积；Pre/Post 只看代码第一行；门控 FFN 仍按两矩阵计参；用 residual 恒等式证明最终性能；把 dropout 位置混用；把 2026 前沿实验写成通用定理。

> [!summary]
> Block 保持 $(B,T,d)$，交替 token mixing 与 channel mixing；Pre/Post 改变 normalization Jacobian 的位置；residual scale 同时影响状态与参数通道；深度稳定性需联合接线、初始化、优化和证据等级。

能逐张量重建 block（A/B）、推导 Jacobian 与 FFN 参数（C）、构造错误接线/尺度反例（D），并完成 Pre/Post/DeepNorm/AttnRes 的公平 evidence card（E）。

## 十三、练习与独立详解

- [[习题 - Transformer Block、残差、归一化与 FFN]]
- [[解答 - Transformer Block、残差、归一化与 FFN]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2020-Xiong-Transformer-LayerNorm]]
- [[S-2022-Wang-DeepNet]]
- [[S-2021-Su-8620-Transformer初始化参数化与标准化]]
- [[S-2022-Su-8994-Why-Residual]]
- [[S-2022-Su-9009-PreNorm-PostNorm]]
- [[S-2026-Chen-Attention-Residuals]]
- [[S-2026-Su-11664-Attention-Residuals]]
