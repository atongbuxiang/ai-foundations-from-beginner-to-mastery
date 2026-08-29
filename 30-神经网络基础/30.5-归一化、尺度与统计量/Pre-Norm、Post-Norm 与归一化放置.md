---
type: derivation
status: draft
area: [neural-networks/normalization, residual-networks, transformers]
aliases: [Pre-LN Post-LN, Normalization Placement]
node_id: NN-39
prerequisites: ["[[LayerNorm 的逐样本几何与反向传播]]", "[[计算图、拓扑序与前向执行]]", "[[局部微分、Jacobian、JVP 与 VJP]]"]
related: ["[[残差学习、恒等捷径与退化问题]]", "[[残差块 Jacobian 与梯度直通]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[小批量、混合精度、分布式与因果归一化边界]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 表达、稳定性与证据边界]]"]
sources: ["[[S-2020-Xiong-Transformer-LayerNorm]]", "[[S-2022-Su-9009-PreNorm-PostNorm]]", "[[S-2016-Ba-Kiros-Hinton-LayerNorm]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
exercises: ["[[习题 - Pre-Norm、Post-Norm 与归一化放置]]"]
solutions: ["[[解答 - Pre-Norm、Post-Norm 与归一化放置]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-pre-post-norm-jacobian-v2.svg]]"
created: 2026-08-23
updated: 2026-08-29
---

# Pre-Norm、Post-Norm 与归一化放置

> [!abstract] 本章主问题
> “Norm 放在残差前还是后”改变的不是排版，而是恒等路径是否被 normalization Jacobian 过滤。Pre-Norm 的单层 Jacobian 显式含 $I$；Post-Norm 把 $I+J_F$ 整体左乘 $J_N$。这解释训练路径差异，却仍不能单独推出深层稳定、最终精度或“有效深度”；这些更强结论需要初始化、残差尺度、相关性与实验协议。

## 课程位置与两遍学习路线

- **承接什么：** NN-35—37 已给出 LN/RMSNorm 的局部 Jacobian 与 null directions；NN-39 不再改变 norm 本身，而是改变它在 residual graph 中的求值位置；
- **本页解决什么：** 从计算图逐步推出 $I+J_FJ_N$ 与 $J_N(I+J_F)$，再用同一扰动展示 identity rail 是否被 norm 过滤；
- **后续为何需要：** 深层 Transformer 的初始化、残差缩放、warm-up 与最终性能讨论，都必须建立在正确的单层 Jacobian 和证据等级上。

**第一遍先画两张计算图。** 沿箭头写 differential，始终记住矩阵乘法顺序表示扰动实际经过算子的先后。

**第二遍再分析深层乘积。** 研究 eigendirections、层间相关性、final norm、dropout、双子层、residual scaling 和 mean-field 假设；不从单层公式直接跳到任务胜负。

### 问题链

1. Pre-Norm 的 identity path 为什么产生显式 $I$？
2. Post-Norm 中哪一步使 residual sum 的所有方向都先经过 $J_N$？
3. 一个共同平移扰动在 LN 的 null space 中时，两种放置分别怎样传播？
4. “每层含 $I$”为什么不等于整个网络 Jacobian 接近等距？
5. 哪些结论是 exact algebra，哪些只在初始化分布或具体实验协议下成立？

> [!check] 第一遍停靠线
> 若你能在 $\mathcal N_\square$ 第一行上写出 $J_N=(a/6)vv^{\mathsf T}$、$v=(1,-2,1)$，并证明共同平移扰动 $\boldsymbol1$ 经 Pre-Norm 保留、经 Post-Norm 被删除，就已掌握本页主干。

## 符号与对象账本

| 对象 | 定义 | 在 residual block 中的角色 | 易错点 |
|---|---|---|---|
| $N$ | LN、RMSNorm 等 normalization map | 改变 branch 输入或 residual sum | 忽略其求值点 |
| $F$ | attention/MLP 等子层 | residual update | 把整个多子层 block 压成同一 $F$ |
| $J_N,J_F$ | 各自在指定点的局部 Jacobian | 传播输入扰动 | 颠倒乘法顺序 |
| $I$ | identity differential | Pre-Norm 的显式直达 rail | 误读成全网 isometry 证书 |
| $\delta\boldsymbol x$ | 局部输入扰动 | 用于比较方向增益 | 只看标量 norm，不看方向 |

### 贯穿算例 $\mathcal N_\square$：共同平移能否走过一层

取共享张量第一行

$$
\boldsymbol x=(1,2,3),
\qquad
a=\sqrt{\frac32},
\qquad
N(\boldsymbol x)=a(-1,0,1),
$$

并取无 affine、$\varepsilon=0$ 的 LayerNorm。令

$$
\boldsymbol v=(1,-2,1)^{\mathsf T}.
$$

由 NN-36 的 Jacobian 公式可化为

$$
\boxed{
J_N(\boldsymbol x)
=\frac a6\boldsymbol v\boldsymbol v^{\mathsf T}
}
$$

它是 rank-1 operator，满足

$$
J_N\boldsymbol1=0,
\qquad
J_N\boldsymbol v=a\boldsymbol v.
$$

为隔离 placement，选择最简单的线性 branch

$$
F(\boldsymbol z)=\frac12\boldsymbol z,
\qquad
J_F=\frac12I.
$$

于是前向分别为

$$
\boldsymbol x_{\mathrm{pre}}^+
=\boldsymbol x+\frac12N(\boldsymbol x),
$$

$$
\boldsymbol x_{\mathrm{post}}^+
=N\!\left(\frac32\boldsymbol x\right)
=N(\boldsymbol x),
$$

最后一个等号使用 LN 在 $\varepsilon=0$ 下对正共同尺度的不变性。局部 Jacobian 则是

$$
J_{\mathrm{pre}}=I+\frac12J_N,
\qquad
J_{\mathrm{post}}=\frac32J_N.
$$

对共同平移扰动 $\delta\boldsymbol x=\boldsymbol1$：

$$
J_{\mathrm{pre}}\boldsymbol1=\boldsymbol1,
\qquad
J_{\mathrm{post}}\boldsymbol1=0.
$$

这就是“Pre-Norm 有未被 normalization 过滤的 identity rail”的精确含义。再对唯一切向方向 $\boldsymbol v$：

$$
J_{\mathrm{pre}}\boldsymbol v
=\left(1+\frac a2\right)\boldsymbol v,
\qquad
J_{\mathrm{post}}\boldsymbol v
=\frac{3a}{2}\boldsymbol v.
$$

两者都可能放大某些方向；显式 $I$ 不等于所有 singular values 都接近 1。

## 核心公式七问：Pre/Post-Norm Jacobian

$$
\boxed{
J_{\mathrm{pre}}
=I+J_F(N(x))J_N(x),
\qquad
J_{\mathrm{post}}
=J_N(x+F(x))[I+J_F(x)]
}.
$$

| 问题 | 本式的回答 |
|---|---|
| 目的 | 精确描述 norm placement 如何改写一层 residual perturbation map |
| 对象 | 固定输入点、固定 mask/dropout realization 下的局部 Jacobian |
| 来路 | 对两张不同计算图分别使用 chain rule 与 residual addition rule |
| 步骤 | 标求值点→沿前向写 differential→按经过顺序右乘输入扰动→合并 identity branch |
| 读法 | Pre 的 $I$ 绕过 $J_N$；Post 的整个 $I+J_F$ 被 $J_N$ 左乘 |
| 检查 | 用 constant branch 或 norm-null direction 验证两式不能互换；用 finite difference 检查顺序 |
| 去路 | Transformer depth stability、warm-up、DeepNorm/ReZero/Fixup、final norm 与 placement ablation |

### AI / 系统对应

真实 Transformer block 含 attention、MLP、dropout、两个或更多 norms，有时还有 residual scaling 与 final norm。比较 Pre/Post 时必须固定这些共同变量，并同时记录 step-0 Jacobian/gradient、训练稳定性、最终验证指标和计算预算。Xiong et al. 的初始化期 mean-field 结论与苏剑林的 residual expansion 提供机制线索，但都不能替代跨架构受控实验。

## 一、学习目标

读完本节，你应能：

1. 写出通用单子层的 Pre-Norm、Post-Norm 前向式；
2. 逐步推导两个 Jacobian，不混淆求值点与乘法顺序；
3. 说明 Pre-Norm 的 identity path 为什么“显式存在”但不等于全网等距；
4. 说明 Post-Norm 为什么会在每层过滤 normalization null/near-null directions；
5. 分析 constant branch 与线性化最小例子；
6. 区分 exact residual sum、相对增量近似与“深度稀释”假说；
7. 正确解读 Xiong et al. 的 mean-field/warm-up 结论；
8. 审计 final norm、双子层、dropout、残差缩放与 Sandwich placement。

## 二、先抽象一个残差子层

令

$$
\boldsymbol x\in\mathbb R^D
$$

是一个 token 的 residual-stream vector，

$$
N:\mathbb R^D\to\mathbb R^D
$$

是 LayerNorm、RMSNorm 或其他逐 token norm，

$$
F:\mathbb R^D\to\mathbb R^D
$$

是 attention 或 FFN 子层在固定其他输入/掩码下对该状态的局部映射。先忽略 dropout，写成：

$$
\boxed{
\text{Pre-Norm:}\quad
\boldsymbol x^+
=\boldsymbol x+F(N(\boldsymbol x))
},
$$

$$
\boxed{
\text{Post-Norm:}\quad
\boldsymbol x^+
=N(\boldsymbol x+F(\boldsymbol x))
}.
$$

Transformer block 通常含 attention 与 FFN 两个 residual sublayers；上述公式要连续应用两次，而不是把整 block 粗略当成一次 $F$ 后丢失中间 norm。

## 三、Pre-Norm Jacobian：恒等支路显式相加

令

$$
\boldsymbol z=N(\boldsymbol x).
$$

微分为

$$
d\boldsymbol x^+
=d\boldsymbol x+J_F(\boldsymbol z)d\boldsymbol z.
$$

又有

$$
d\boldsymbol z=J_N(\boldsymbol x)d\boldsymbol x.
$$

代入：

$$
d\boldsymbol x^+
=\left[
I+J_F(N(\boldsymbol x))J_N(\boldsymbol x)
\right]d\boldsymbol x.
$$

所以

$$
\boxed{
J_{\mathrm{pre}}(\boldsymbol x)
=I+J_F(N(\boldsymbol x))J_N(\boldsymbol x)
}.
$$

乘法顺序不能颠倒：输入扰动先经过 $J_N$，再经过 $J_F$，最后与 identity differential 相加。

## 四、Post-Norm Jacobian：整条残差和被左乘

令

$$
\boldsymbol z=\boldsymbol x+F(\boldsymbol x).
$$

先有

$$
d\boldsymbol z
=\left[I+J_F(\boldsymbol x)\right]d\boldsymbol x.
$$

再经过 normalization：

$$
d\boldsymbol x^+
=J_N(\boldsymbol z)d\boldsymbol z.
$$

因此

$$
\boxed{
J_{\mathrm{post}}(\boldsymbol x)
=J_N(\boldsymbol x+F(\boldsymbol x))
\left[I+J_F(\boldsymbol x)\right]
}.
$$

这里 $J_N$ 在 residual sum $\boldsymbol z$ 处求值，不是在 $\boldsymbol x$ 处。只写“Post-Norm 多乘一个 $J_N$”仍不够，必须保留求值点。

## 五、最小反例：constant branch

令

$$
F(\boldsymbol x)=\boldsymbol c
$$

为常向量，所以

$$
J_F=0.
$$

Pre-Norm 变为

$$
\boldsymbol x^+=\boldsymbol x+\boldsymbol c,
\qquad
J_{\mathrm{pre}}=I.
$$

Post-Norm 变为

$$
\boldsymbol x^+=N(\boldsymbol x+\boldsymbol c),
\qquad
J_{\mathrm{post}}=J_N(\boldsymbol x+\boldsymbol c).
$$

若 $N$ 是 $\varepsilon=0$ 的 LayerNorm，则共同平移方向和 centered radial direction 被 $J_N$ 删除。即使 residual branch 本身没有任何输入导数，Post-Norm 仍不会留下完整 identity Jacobian。

这个例子证明结构差异真实存在；它不证明一般深层网络中 Post-Norm 必然梯度消失。

## 六、局部线性化中的方向账本

把某一点的 normalization Jacobian 记为 $A$，把 branch Jacobian 简化为 $aI$。作为局部算子模型：

$$
J_{\mathrm{pre}}=I+aA,
$$

$$
J_{\mathrm{post}}=A(I+aI)=(1+a)A.
$$

若 $A\boldsymbol v=0$，则

$$
J_{\mathrm{pre}}\boldsymbol v=\boldsymbol v,
\qquad
J_{\mathrm{post}}\boldsymbol v=0.
$$

若 $A\boldsymbol t=\lambda\boldsymbol t$，则

$$
J_{\mathrm{pre}}\boldsymbol t=(1+a\lambda)\boldsymbol t,
$$

$$
J_{\mathrm{post}}\boldsymbol t=(1+a)\lambda\boldsymbol t.
$$

这张账本只比较固定局部线性算子，不声称真实 $A$ 在两种架构的求值点相同。它的作用是暴露“identity 加法”与“左侧 gate”的代数差别。

## 七、深层乘积：有 $I$ 不等于等距

对 $L$ 个 Pre-Norm 子层，记

$$
A_\ell
=J_{F_\ell}(N(x_\ell))J_N(x_\ell),
$$

则

$$
J_{0\to L}^{\mathrm{pre}}
=\prod_{\ell=L-1}^{0}(I+A_\ell).
$$

每个因子含 $I$，但乘积的 singular values 仍可能：

- 若 $A_\ell$ 沿同一扩张方向积累而爆炸；
- 若 $I+A_\ell$ 近奇异而收缩；
- 因非正规性出现暂态放大；
- 因层间相关性偏离独立近似。

对 Post-Norm，记

$$
B_\ell=J_N(x_\ell+F_\ell(x_\ell)),
\qquad
C_\ell=J_{F_\ell}(x_\ell),
$$

则

$$
J_{0\to L}^{\mathrm{post}}
=\prod_{\ell=L-1}^{0}B_\ell(I+C_\ell).
$$

每层都有一个 normalization Jacobian，但 $B_\ell$ 与 $C_\ell$ 的方向可能旋转；不能把标量 norm 上界当成精确谱。

## 八、反向传播视角

若上游 row-cotangent 为 $\bar x^+$，则 Pre-Norm：

$$
\bar x
=\bar x^+
+\bar x^+J_FJ_N.
$$

第一项是显式 identity gradient rail。

Post-Norm：

$$
\bar x
=\bar x^+J_N(I+J_F).
$$

上游先经过 $J_N$ 的 transpose 作用（row convention 中写在右侧），再分到 identity 与 branch。LayerNorm/RMSNorm 的 input-dependent projection与 gain 会共同影响该 rail。

## 九、Final Norm 不能漏记

许多 Pre-Norm Transformer 在所有 blocks 后还有 final norm：

$$
y=N_f(x_L).
$$

于是全网 Jacobian 是

$$
J_y
=J_{N_f}(x_L)
\prod_{\ell=L-1}^{0}(I+A_\ell).
$$

因此 Pre-Norm 不是“任何梯度都永远绕过所有 normalization”；准确说法是 block 内有未被每层 norm 过滤的 identity path，而最终读出之前可能仍经过一次 norm。

## 十、科学空间的残差展开：哪一步是精确的

Pre-Norm 递推

$$
x_{\ell+1}
=x_\ell+\Delta_\ell,
\qquad
\Delta_\ell=F_\ell(N(x_\ell))
$$

精确展开为

$$
\boxed{
x_L=x_0+\sum_{\ell=0}^{L-1}\Delta_\ell
}.
$$

这是代数恒等式。若进一步假设

$$
\|\Delta_\ell\|\approx c
$$

且 residual stream norm 随深度增长，那么相对层变化

$$
\frac{\|x_{\ell+1}-x_\ell\|}{\|x_\ell\|}
=\frac{\|\Delta_\ell\|}{\|x_\ell\|}
$$

可能下降。两种极端：

- 若增量大致同向，$\|x_L\|$ 可按 $L$ 增长，相对增量约 $1/L$；
- 若增量近似不相关，$\|x_L\|$ 可按 $\sqrt L$ 增长，相对增量约 $1/\sqrt L$。

但这一步需要分支幅度、相关性与 residual growth 假设。若 $\Delta_\ell$ 自适应放大、旋转到新方向或产生强非线性组合，“层变虚”并不由求和恒等式自动成立。

## 十一、“浅而宽”是解释假说，不是已证等价

科学空间把上述现象概括为 Pre-Norm 可能更像累加多个并行特征增量，从而“有效深度被稀释”。应保留三个层级：

1. **精确**：$x_L=x_0+\sum\Delta_\ell$；
2. **有条件近似**：若 $\|x_\ell\|$ 增长而 $\|\Delta_\ell\|$ 受控，相对层变化下降；
3. **解释/经验**：这是否导致某任务最终性能低于充分调参的 Post-Norm。

相邻 hidden states 接近不等于函数复合可被一个浅层网络精确替代；“有效深度”还需要一个可测定义，如 representation change、Jacobian distance、path contribution 或 functional ablation。

## 十二、Xiong et al. 的结论怎样正确读

Xiong et al. 2020 在其 Transformer、初始化和 mean-field 假设下分析：

- Post-LN 初始化时靠近输出层的参数梯度期望可能较大；
- warm-up 可缓解一开始用大步长造成的不稳定；
- 论文设置中的 Pre-LN 初始梯度更受控，并可在实验中减少 warm-up 依赖。

不应改写成：

- Post-Norm 在任何模型中都不能训练；
- Pre-Norm 永远不需要 warm-up；
- Pre-Norm 最终精度一定更高；
- 一般 Jacobian 恒等式已经证明论文全部 mean-field rate。

训练容易度、收敛后性能、迁移性能和算力预算是四个不同的响应变量。

## 十三、残差缩放与初始化会改写比较

更一般的子层可写为

$$
x^+=\alpha x+\beta F(N(x))
$$

或

$$
x^+=N(\alpha x+\beta F(x)).
$$

Jacobian 中 identity rail 变为 $\alpha I$，branch 变为 $\beta J_FJ_N$。因此 Pre/Post 标签本身不足以预测深度稳定性，还需记录：

- $\alpha,\beta$ 是否随深度缩放；
- branch 最后一层是否零初始化；
- attention/FFN 是否各有独立尺度；
- gain 参数初值；
- learning-rate/warm-up；
- dropout/stochastic-depth 的期望尺度。

这些内容在 [[ReZero、Fixup、DeepNorm 与深网缩放]] 继续展开。

## 十四、Sandwich Norm 与额外放置

一种抽象 Sandwich 形式是

$$
x^+=x+N_2(F(N_1(x))).
$$

其 Jacobian 为

$$
J
=I+J_{N_2}(F(N_1(x)))
J_F(N_1(x))
J_{N_1}(x).
$$

它保留外部 identity rail，同时在 branch 两侧加入 norm Jacobian。额外 normalization 可能控制 branch activation，也可能删除更多局部方向、增加 kernel/通信成本；不能只说“结合两者优点”。

类似地，attention 内 Q/K normalization、head-wise norm 或 FFN 中间 norm 都改变不同对象，必须重新画计算图，不能统称 Pre/Post。

## 十五、Dropout 与 stochastic branch

若

$$
x^+=x+M\odot F(N(x))
$$

且 $M$ 是 dropout mask，则条件于固定 mask：

$$
J=I+\operatorname{Diag}(M)J_FJ_N.
$$

不同 mask、RNG replay 与 train/eval 会改变 Jacobian 分布。Pre-Norm 的 identity rail仍在，但 branch 尺度取决于 inverted-dropout convention。Post-Norm 还会让随机 residual sum 改变 $J_N$ 的求值点。

## 十六、图：数据流、Jacobian rail 与证据等级

先看图回答：Pre-Norm 的 identity rail 在哪里绕过 norm？Post-Norm 的哪一步把残差和整体送入 $J_N$？哪些结论是恒等式，哪些只是有条件解释？

![[00-知识库管理/_assets/figures/neural-networks/fig-pre-post-norm-jacobian-v2.svg|900]]

> [!figure] 图 30.5-07　Pre/Post-Norm 的前向位置、反向 rail 与证据分层
> 左栏并列 $x+F(N(x))$ 和 $N(x+F(x))$ 的计算图；中栏把 $I+J_FJ_N$ 的直达 rail 与 $J_N(I+J_F)$ 的层层 gate 画成不同路径；右栏从 exact Jacobian、mean-field theorem、有条件 residual-growth 解释到任务经验逐级标注。来源：依据 Xiong et al. 2020、苏剑林 2022 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_normalization_advanced_v2.py]] 确定性生成。

**怎样读图**：先顺前向箭头确认 norm 的求值点，再反向追踪 identity 信号是否先过 $J_N$，最后只在右栏对应证据等级内使用结论。

**图没有证明什么**：图没有证明 Pre-Norm 或 Post-Norm 跨任务占优，也没有给出深层 Jacobian singular spectrum；后者还取决于每层方向、相关性、残差尺度和训练演化。

## 十七、可执行比较协议

公平比较至少固定或分别优化：

1. 参数量、depth、width 与 attention/FFN 结构；
2. normalization 类型、epsilon、gain/bias；
3. final norm；
4. initialization 与 residual scaling；
5. learning-rate、warm-up、optimizer 与 clipping；
6. dropout/stochastic depth；
7. 训练 tokens、wall time 与调参预算；
8. 训练稳定性、最终 validation、迁移与 calibration 分开报告。

诊断量至少包含：

- 每层 residual/branch RMS 比；
- update-to-weight ratio；
- activation/gradient norm；
- 局部 JVP/VJP 增益；
- representation change $\|x_{\ell+1}-x_\ell\|/\|x_\ell\|$；
- 多 seed failure rate。

## 十八、最小验收

1. 从 differential 重建两个 Jacobian；
2. 说明每个 Jacobian 的求值点；
3. 用 constant branch 验证 $I$ 与 $J_N$ 差异；
4. 对局部 eigen-direction 手算 Pre/Post gain；
5. 展开 $L$ 层 Pre-Norm residual sum；
6. 指出“相对增量下降”所需的额外假设；
7. 把 Xiong 论文结论限制在其设定；
8. 把 final norm 加入全网 Jacobian；
9. 写出 Sandwich Jacobian；
10. 设计公平的 warm-up/placement 对照。

> [!summary]
> Pre-Norm 的结构优势是 block Jacobian 中有显式 $I$；Post-Norm 则让 residual sum 经过 input-dependent $J_N$。这是严格代数。深层稳定、有效深度和最终性能是在该代数之上、需要额外假设与实验的更强问题。

- [[归一化、尺度与统计量 MOC]]
- [[习题 - Pre-Norm、Post-Norm 与归一化放置]]
- [[解答 - Pre-Norm、Post-Norm 与归一化放置]]
