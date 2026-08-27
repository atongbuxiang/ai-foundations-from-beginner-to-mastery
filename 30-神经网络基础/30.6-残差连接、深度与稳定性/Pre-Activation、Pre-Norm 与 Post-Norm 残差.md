---
type: derivation
status: draft
area: [neural-networks/residual-stability, normalization-placement, convolutional-networks, transformers]
aliases: [Residual Placement, Pre-Activation and Pre-Norm]
node_id: NN-45
prerequisites: ["[[残差块 Jacobian 与梯度直通]]", "[[Pre-Norm、Post-Norm 与归一化放置]]", "[[BatchNorm 前向统计与训练—推理差异]]", "[[LayerNorm 的逐样本几何与反向传播]]"]
related: ["[[Highway、Dense Connection 与 Skip 结构比较]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[小批量、混合精度、分布式与因果归一化边界]]", "[[Transformer Block、残差、归一化与 FFN]]", "[[Transformer 表达、稳定性与证据边界]]"]
sources: ["[[S-2016-He-Identity-Mappings]]", "[[S-2020-Xiong-Transformer-LayerNorm]]", "[[S-2022-Su-9009-PreNorm-PostNorm]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]", "[[S-2016-Ba-Kiros-Hinton-LayerNorm]]"]
exercises: ["[[习题 - Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"]
solutions: ["[[解答 - Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-residual-placement-contract-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# Pre-Activation、Pre-Norm 与 Post-Norm 残差

> [!abstract] 本章主问题
> “把激活或归一化放在残差相加之前还是之后”会改变整块 Jacobian 的乘法顺序。full pre-activation CNN 与 Transformer Pre-Norm 都保留显式 $I$，而 post-activation/Post-Norm 会把残差和整体交给后置算子的 Jacobian；但两组术语的内部算子、归约轴、状态语义和训练—推理行为不同，不能因公式外壳相似就视为同一种架构。

## 一、学习目标

读完本节，你应能：

1. 准确写出 original post-activation、full pre-activation、Transformer Pre-Norm 与 Post-Norm；
2. 按计算顺序推导四个局部 Jacobian；
3. 解释“显式 identity rail”为什么是结构事实而不是稳定定理；
4. 用二维例子证明后置非线性可删除 residual sum 的方向；
5. 区分 CNN pre-activation 与 Transformer Pre-Norm；
6. 审计 projection、final norm、dropout、双子层与 BatchNorm train/eval；
7. 把结构恒等式、条件理论和架构实验放在不同证据层。

## 二、先建立统一的算子合同

设状态为

$$
x\in\mathbb R^D,
$$

$F$ 是 residual branch，$P$ 是放在 branch 输入前的预处理，$Q$ 是 residual addition 后的后处理。最一般的单块写法是

$$
\boxed{
x^+=Q\!\left(S(x)+F(P(x))\right)
},
$$

其中 $S$ 是 shortcut。只有当

$$
S=I,
\qquad
Q=I
$$

时，after-addition 才存在未经额外算子过滤的恒等轨。

对可微点，链式法则给出

$$
\boxed{
J_{x^+}
=J_Q\!\left(S(x)+F(P(x))\right)
\left[J_S(x)+J_F(P(x))J_P(x)\right]
}.
$$

这一个公式可以定位几乎所有“放置”差异：看 $J_Q$ 是否在最左侧、$J_S$ 是否真为 $I$、$J_P$ 作用在哪个 branch。

## 三、original ResNet：post-activation residual unit

忽略卷积细节，原始残差单元可抽象为

$$
y=x+F(x),
\qquad
x^+=\phi(y),
$$

故

$$
\boxed{
J_{\mathrm{postact}}(x)
=J_\phi(x+F(x))[I+J_F(x)]
}.
$$

虽然相加点出现了 $I+J_F$，但输出还要经过 $J_\phi$。若 $\phi$ 是 ReLU，某些坐标在该点为负，则对应行被置零；“shortcut 是 identity”不能抵消 after-addition activation 的门控。

> [!warning] 名称陷阱
> 有些实现把 branch 内部的 `conv–BN–ReLU` 顺序也称为 post-activation。分析时不要只看标签，要把完整前向式写出来，尤其要问：相加之后是否仍有 ReLU/Norm？

## 四、full pre-activation ResNet

full pre-activation 把 BN/ReLU 等预处理移到 branch 的权重层之前，并让 addition 后不再立即经过激活。抽象为

$$
\boxed{
x^+=x+F(P(x))
}.
$$

因此

$$
\boxed{
J_{\mathrm{preact}}(x)
=I+J_F(P(x))J_P(x)
}.
$$

关键不是“激活消失了”，而是激活和归一化只在 branch 微分项中；shortcut differential $dx$ 不穿过 $J_P$。反向传播时，若上游列梯度为 $g^+$，

$$
g
=g^++J_P(x)^\mathsf T J_F(P(x))^\mathsf T g^+.
$$

第一项是显式 rail。不过两项仍可相消，深层乘积

$$
\prod_\ell[I+J_{F_\ell}J_{P_\ell}]
$$

仍可病态；“有直接项”不等于 singular values 恒为 1。

## 五、Transformer Pre-Norm 与 Post-Norm

对一个 attention 或 FFN residual sublayer，Pre-Norm 写为

$$
\boxed{
x^+=x+F(N(x))
},
$$

所以

$$
\boxed{
J_{\mathrm{PreNorm}}
=I+J_F(N(x))J_N(x)
}.
$$

Post-Norm 写为

$$
\boxed{
x^+=N(x+F(x))
},
$$

所以

$$
\boxed{
J_{\mathrm{PostNorm}}
=J_N(x+F(x))[I+J_F(x)]
}.
$$

Post-Norm 的 $J_N$ 必须在 residual sum 的求值点计算。LayerNorm 会沿平移方向产生零方向，并在 centered radial direction 上出现由 $\varepsilon$ 决定的小增益；因此它不是一个无害的标量系数。

## 六、为什么 CNN pre-activation 不等于 Transformer Pre-Norm

两者共享

$$
x^+=x+F(P(x))
$$

这个结构外壳，但内部合同不同：

| 项目 | CNN full pre-activation | Transformer Pre-Norm |
|---|---|---|
| 常见 $P$ | BN 与 ReLU 的组合 | LayerNorm 或 RMSNorm |
| 归约轴 | batch/channel/spatial 语义 | 通常逐 token feature 轴 |
| 状态 | feature map | residual-stream token vectors |
| branch | convolution stack | attention 或 FFN |
| train/eval | BN 统计通常改变 | LN/RMSNorm 通常不依赖 running stats |
| 非光滑性 | ReLU mask 常直接出现 | norm 通常光滑到 $\varepsilon$；branch 仍可非光滑 |

所以可以复用 Jacobian 模板，却不能复用全部统计、因果、系统和经验结论。

## 七、二维手算：后置激活怎样删掉一维

令

$$
A=
\begin{bmatrix}
0&-2\\
0.2&0
\end{bmatrix},
\qquad
x=
\begin{bmatrix}
1\\-1
\end{bmatrix}.
$$

### 7.1 pre-activation

取

$$
G_{\mathrm{pre}}(x)=x+A\operatorname{ReLU}(x).
$$

因为 $x_1>0,x_2<0$，

$$
D_x=J_{\operatorname{ReLU}}(x)
=\operatorname{diag}(1,0).
$$

于是

$$
J_{\mathrm{pre}}
=I+AD_x
=
\begin{bmatrix}
1&0\\
0.2&1
\end{bmatrix},
$$

其行列式为 1，局部满秩。

### 7.2 post-activation

取

$$
G_{\mathrm{post}}(x)=\operatorname{ReLU}(x+Ax).
$$

先算

$$
x+Ax
=
\begin{bmatrix}
3\\-0.8
\end{bmatrix},
$$

故 after-addition mask 也是

$$
D_y=\operatorname{diag}(1,0).
$$

于是

$$
J_{\mathrm{post}}
=D_y(I+A)
=
\begin{bmatrix}
1&-2\\
0&0
\end{bmatrix},
$$

秩为 1。这里没有声称 pre-activation 总是可逆；例子只证明后置 ReLU 可以把 residual sum 的一个局部方向完全删掉。

## 八、非光滑点与次梯度

在 ReLU 输入为 0 的点，经典导数不存在。框架通常选择某个约定次梯度，但：

- 不同约定不改变函数连续性，却会改变该点的自动微分结果；
- 单点 Jacobian 不代表邻域所有 activation regions；
- 用有限差分验证时，跨过 kink 会同时采到两侧线性区。

因此报告应写“在指定 activation mask 的局部 Jacobian”，而不是“全局 Jacobian 就是该矩阵”。

## 九、projection shortcut 的位置

若形状改变，shortcut 可能是 $S(x)=Px$。full pre-activation 变为

$$
x^+=Px+F(P_0(x)),
$$

Jacobian 为

$$
J=P+J_FJ_{P_0}.
$$

如果 $P$ 降维，恒等 rail 已经不存在；即使 addition 后没有激活，也不能宣称全空间信息直通。若 branch 与 shortcut 分别改变 spatial resolution，还必须登记 stride、padding 与 channel alignment。

## 十、双子层、final norm 与 dropout

标准 Transformer block 常连续包含 attention 与 FFN：

$$
u=x+F_{\mathrm{attn}}(N_1(x)),
$$

$$
y=u+F_{\mathrm{ffn}}(N_2(u)).
$$

总 Jacobian 是两个因子的有序乘积，不可把 $F_{\mathrm{attn}}+F_{\mathrm{ffn}}$ 当成同一点的并行和。若末端还有 final norm，最终输入—输出 Jacobian仍会被 $J_{N_f}$ 左乘。

dropout 使训练期 block 成为随机映射：固定 mask 后可写条件 Jacobian；跨 mask 的 expected Jacobian、Jacobian norm 的期望和 deterministic evaluation Jacobian 是三个不同对象。

## 十一、BatchNorm 的 train/eval 状态

CNN pre-activation 中若 $P$ 含 BatchNorm：

- train mode 的输出依赖同批其他样本，单样本 Jacobian 不是完整对象；
- eval mode 使用 running statistics，Jacobian 变为逐样本 affine scaling 与后续 mask；
- microbatch、SyncBN 和冻结统计会改变 $J_P$；
- running-state update 不是普通反向传播参数梯度。

因此“pre-activation 保留 $I$”是对 shortcut 的精确说法，不代表 branch 的统计合同在 train/eval 相同。

## 十二、结构解释与经验结论分账

可以无条件由前向式推出：

1. 哪个 Jacobian 因子在 identity sum 外侧；
2. 哪条 differential 不穿过 activation/norm；
3. projection 是否替换了 $I$。

不能只由结构式推出：

1. 任意深度梯度稳定；
2. Pre-Norm 或 pre-activation 最终精度更高；
3. warm-up 一定不需要；
4. 某放置对所有模型尺度都更优。

He et al. 的 pre-activation 消融、Xiong et al. 的 mean-field 分析与科学空间的深度稀释解释分别属于实验、条件理论与机制视角，必须保留各自假设。

## 十三、图：四种放置合同

先看图回答：哪个公式的恒等项没有被后置 Jacobian 左乘？为什么 CNN full pre-activation 与 Transformer Pre-Norm 只能说“结构外壳相同”？二维例子中的秩下降发生在哪一步？

![[00-知识库管理/_assets/figures/neural-networks/fig-residual-placement-contract-v2.svg|900]]

> [!figure] 图 30.6-05　残差放置的前向式、Jacobian 与局部秩反例
> 左栏并列四种合同；中栏区分 CNN 的 BN/ReLU 预处理与 Transformer 的逐 token norm；右栏用二维局部矩阵展示 after-addition ReLU 删除方向。来源：依据 He et al. 2016、Xiong et al. 2020 与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_residual_advanced_v2.py]] 确定性生成。

**怎样读图**：先从前向式找最外层算子，再从右向左按计算顺序写微分；最后检查 $I$ 是裸露相加，还是被 $J_\phi/J_N$ 整体过滤。

**图没有证明什么**：局部秩反例不证明所有 post-activation/Post-Norm 网络都会秩亏，也不证明 pre-activation/Pre-Norm 在所有任务上更优。

## 十四、最小验收

1. 从统一 $Q(S(x)+F(P(x)))$ 推导总 Jacobian；
2. 写出四种放置的前向式和 Jacobian；
3. 复算二维例子的两个矩阵与秩；
4. 说明 ReLU 非光滑点的报告方式；
5. 区分 CNN pre-activation 与 Transformer Pre-Norm；
6. 把 projection、双子层、final norm、dropout 与 BN train/eval 加回合同；
7. 为“更稳”“更准”“更深”分别写出所需证据。

> [!summary]
> 残差放置的第一原则是先写前向算子，再按顺序写 Jacobian。full pre-activation 与 Pre-Norm 把预处理限制在 branch 内，从而显式保留 shortcut differential；post-activation 与 Post-Norm 则让 residual sum 经过后置算子。这个结构差异真实而重要，但它只是稳定性分析的起点。

- [[残差连接、深度与稳定性 MOC]]
- [[习题 - Pre-Activation、Pre-Norm 与 Post-Norm 残差]]
- [[解答 - Pre-Activation、Pre-Norm 与 Post-Norm 残差]]
