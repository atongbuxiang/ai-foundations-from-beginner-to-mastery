---
type: derivation
status: draft
area: [neural-networks/normalization, layer-normalization, geometry]
aliases: [LayerNorm Geometry, LayerNorm Backward]
node_id: NN-36
prerequisites: ["[[归一化的对象、轴与不变性]]", "[[局部微分、Jacobian、JVP 与 VJP]]", "[[正交投影]]"]
related: ["[[RMSNorm、均值移除与缩放不变性]]", "[[Pre-Norm、Post-Norm 与归一化放置]]", "[[小批量、混合精度、分布式与因果归一化边界]]"]
sources: ["[[S-2016-Ba-Kiros-Hinton-LayerNorm]]", "[[S-2026-PyTorch-Normalization-Semantics]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]"]
exercises: ["[[习题 - LayerNorm 的逐样本几何与反向传播]]"]
solutions: ["[[解答 - LayerNorm 的逐样本几何与反向传播]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-layernorm-token-geometry-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---

# LayerNorm 的逐样本几何与反向传播

> [!abstract] 本章主问题
> 常见 Transformer LayerNorm 对每个 token 的 feature vector 独立执行“投影到共同平移方向的正交补，再按 centered RMS 归一半径，最后逐 feature affine”。它不依赖 batch size，也没有 running statistics；但同一 token 内所有 features 的前向与反向仍然密集耦合。$\varepsilon$、normalized shape 和低维退化决定了精确不变性与 Jacobian 谱。

## 一、学习目标

读完本节，你应能：

1. 对 $(B,T,D)$ 输入明确写出 LayerNorm$(D)$ 的统计组和参数形状；
2. 把 LayerNorm 解释为 centering projection 加 radial normalization；
3. 推导共同平移、正尺度、负尺度下的精确与近似性质；
4. 对 vector gain $\boldsymbol\gamma$ 完整推导 $dX,d\gamma,d\beta$；
5. 写出无 affine normalization Jacobian 的三个 eigenspaces；
6. 解释 $D=1$ 与 $D=2$ 的严重退化；
7. 区分“不跨 batch 耦合”和“不耦合任何元素”；
8. 审计 normalized shape、token causality、padding 与 mixed precision 边界。

## 二、从 BatchNorm 换轴，而不是换掉数学

对 Transformer 隐藏状态

$$
X\in\mathbb R^{B\times T\times D},
$$

最常见 LayerNorm$(D)$ 对每个固定 $(b,t)$ 取向量

$$
\boldsymbol x_{bt}=X_{b,t,:}\in\mathbb R^D
$$

独立计算统计量。不同 batch 样本、不同 token 不共享 $\mu,q$；但可学习参数

$$
\boldsymbol\gamma,\boldsymbol\beta\in\mathbb R^D
$$

在所有 $(b,t)$ 上共享。

因此：

- statistics count 是 $D$；
- groups count 是 $BT$；
- affine parameters count 是 $2D$；
- 没有 running mean/variance；
- train 与 eval 都从当前 token vector 计算统计量。

## 三、正式定义

先只看一个 token：

$$
\boldsymbol x=(x_1,\ldots,x_D)^{\mathsf T}\in\mathbb R^D.
$$

定义

$$
\mu=\frac1D\sum_{j=1}^D x_j,
\qquad
\boldsymbol c=\boldsymbol x-\mu\boldsymbol1,
$$

$$
q=\frac1D\sum_{j=1}^D c_j^2,
\qquad
r=\sqrt{q+\varepsilon},
$$

$$
\widehat{\boldsymbol x}=\frac{\boldsymbol c}{r},
$$

$$
\boxed{
\boldsymbol y
=\boldsymbol\gamma\odot\widehat{\boldsymbol x}
+\boldsymbol\beta
}.
$$

访问日 PyTorch 2.13 的 LayerNorm 使用 biased variance，也就是 denominator $D$；对 normalized shape 含多个尾维时，它会在最后若干维联合归约，并让 affine 参数与该 normalized shape 同形。

## 四、完整前向手算

取

$$
\boldsymbol x=(1,2,3),
\quad
\boldsymbol\gamma=(1,2,1),
\quad
\boldsymbol\beta=(0,1,0),
\quad
\varepsilon=0.
$$

先算

$$
\mu=2,
\qquad
\boldsymbol c=(-1,0,1),
$$

$$
q=\frac{1+0+1}{3}=\frac23,
\qquad
r=\sqrt{\frac23}.
$$

于是

$$
\widehat{\boldsymbol x}
=\left(-\sqrt{\frac32},0,\sqrt{\frac32}\right),
$$

$$
\boxed{
\boldsymbol y
=\left(-\sqrt{\frac32},1,\sqrt{\frac32}\right)
}.
$$

affine 前的均值为 0、平方均值为 1；affine 后的均值不再必为 0。第二个坐标虽然 normalized value 为 0，仍因 $\beta_2=1$ 输出 1。

## 五、几何：超平面与球面的交

定义 centering projection

$$
P=I-\frac1D\boldsymbol1\boldsymbol1^{\mathsf T}.
$$

第一步

$$
\boldsymbol c=P\boldsymbol x
$$

把 $\boldsymbol x$ 投到

$$
\boldsymbol1^\perp
=\{\boldsymbol z:\boldsymbol1^{\mathsf T}\boldsymbol z=0\},
$$

这是维数 $D-1$ 的超平面。

当 $\varepsilon=0$ 且 $\boldsymbol c\ne0$，

$$
\|\widehat{\boldsymbol x}\|^2
=\frac{\|\boldsymbol c\|^2}{q}
=\frac{Dq}{q}
=D.
$$

所以无 affine 的 LayerNorm 把输入送到

$$
\boldsymbol1^\perp
\cap
\{\boldsymbol z:\|\boldsymbol z\|=\sqrt D\},
$$

一个维数 $D-2$ 的球面。共同平移方向与 centered radial magnitude 被删除，只保留 centered direction。

逐 feature 的 $\boldsymbol\gamma$ 随后把球面各坐标异向伸缩，$\boldsymbol\beta$ 再平移；最终输出不再位于该球面。

## 六、不变性公式

令

$$
\boldsymbol x'=a\boldsymbol x+b\boldsymbol1.
$$

有

$$
\mu'=a\mu+b,
\qquad
\boldsymbol c'=a\boldsymbol c,
\qquad
q'=a^2q.
$$

故

$$
\widehat{\boldsymbol x'}
=\frac{a\boldsymbol c}{\sqrt{a^2q+\varepsilon}}.
$$

结论：

- 对任意 $b$，共同平移被精确删除；
- $a>0,\varepsilon=0$ 时 $\widehat{\boldsymbol x'}=\widehat{\boldsymbol x}$；
- $a<0,\varepsilon=0$ 时 $\widehat{\boldsymbol x'}=-\widehat{\boldsymbol x}$；
- $\varepsilon>0$ 时正尺度只近似抵消；
- 非共同的逐 feature shift/scale 一般改变 centered direction。

原论文所说的 per-training-case rescaling invariance 必须在这些条件下读取，而不是把 LayerNorm 当作对任意 feature transformation 都不变。

## 七、反向推导：先处理 vector gain

令上游梯度

$$
\boldsymbol g=\nabla_{\boldsymbol y}L.
$$

因为 affine 是逐坐标的，定义

$$
\boldsymbol u=\boldsymbol\gamma\odot\boldsymbol g.
$$

对一个 token，参数局部贡献是

$$
\boxed{
\frac{\partial L}{\partial\boldsymbol\beta}
=\boldsymbol g
},
$$

$$
\boxed{
\frac{\partial L}{\partial\boldsymbol\gamma}
=\boldsymbol g\odot\widehat{\boldsymbol x}
}.
$$

真实 batch 中，$\boldsymbol\gamma,\boldsymbol\beta$ 在 $B,T$ 上共享，所以还要对所有 token 累加：

$$
\nabla_{\boldsymbol\beta}L
=\sum_{b,t}\boldsymbol g_{bt},
$$

$$
\nabla_{\boldsymbol\gamma}L
=\sum_{b,t}\boldsymbol g_{bt}\odot
\widehat{\boldsymbol x}_{bt}.
$$

## 八、输入 VJP

与上一节同样，从

$$
d\widehat{\boldsymbol x}
=\frac1r
\left(
P-\frac1D\widehat{\boldsymbol x}\widehat{\boldsymbol x}^{\mathsf T}
\right)d\boldsymbol x
$$

得到

$$
\boxed{
\nabla_{\boldsymbol x}L
=\frac1r
\left[
\boldsymbol u
-\overline u\,\boldsymbol1
-\widehat{\boldsymbol x}\,
\overline{u\widehat x}
\right]
},
$$

其中

$$
\overline u=\frac1D\sum_j u_j,
\qquad
\overline{u\widehat x}
=\frac1D\sum_j u_j\widehat x_j.
$$

注意不能先把 scalar $\gamma$ 提到括号外，因为 LayerNorm 常用的是 vector gain。正确顺序是先形成

$$
\boldsymbol u=\boldsymbol\gamma\odot\boldsymbol g,
$$

再做两次组内投影。

## 九、Jacobian 的 eigenspaces

先看无 affine 的

$$
J_{\text{norm}}
=\frac1r
\left(
P-\frac1D\widehat{\boldsymbol x}\widehat{\boldsymbol x}^{\mathsf T}
\right).
$$

当 $q>0$：

### 9.1 共同平移方向

$$
J_{\text{norm}}\boldsymbol1=0.
$$

### 9.2 centered radial direction

$$
J_{\text{norm}}\widehat{\boldsymbol x}
=\frac{\varepsilon}{(q+\varepsilon)^{3/2}}
\widehat{\boldsymbol x}.
$$

### 9.3 正交于二者的方向

若

$$
\boldsymbol v\perp\boldsymbol1,
\qquad
\boldsymbol v\perp\widehat{\boldsymbol x},
$$

则

$$
J_{\text{norm}}\boldsymbol v=\frac1r\boldsymbol v.
$$

因此在 $\varepsilon=0$ 时有两个零方向，剩余 $D-2$ 个切向方向的 eigenvalue 为 $1/\sqrt q$。加入非均匀 $\boldsymbol\gamma$ 后，

$$
J_{\text{LN}}
=\operatorname{Diag}(\boldsymbol\gamma)J_{\text{norm}},
$$

通常不再对称，奇异值也不只是简单列出 $\gamma_j/r$；但输入端的平移/径向 null directions 仍由 $J_{\text{norm}}$ 决定，除非 $\varepsilon$ 或零 gain 改变秩。

## 十、低维退化不是边角问题

### 10.1 $D=1$

$$
\mu=x_1,\qquad c_1=0,\qquad\widehat x_1=0.
$$

输出恒为 $\beta_1$，输入梯度为 0。LayerNorm 一个标量 feature 会删除全部输入信息。

### 10.2 $D=2,\varepsilon=0$

若 $x_1\ne x_2$，令 $d=x_1-x_2$，则

$$
\widehat{\boldsymbol x}
=\left(\operatorname{sign}d,-\operatorname{sign}d\right).
$$

在不跨过 $d=0$ 的局部区域，输出是常量，所以 Jacobian 几乎处处为 0。几何上，$D-2=0$，球面只剩两个点。

### 10.3 $\varepsilon>0$

$\varepsilon$ 让径向导数变成非零，缓解精确退化，但小 variance 处仍可能有大 scale $1/\sqrt\varepsilon$。这说明 hidden width、epsilon 与 dtype 必须一起审计。

## 十一、带 vector gain 的反向手算

沿用

$$
\boldsymbol x=(1,2,3),
\qquad
\boldsymbol\gamma=(1,2,1),
\qquad
\varepsilon=0,
$$

令

$$
\boldsymbol g=(1,1,0).
$$

则

$$
\boldsymbol u
=\boldsymbol\gamma\odot\boldsymbol g
=(1,2,0),
$$

$$
\overline u=1,
\qquad
\overline{u\widehat x}
=-\frac13\sqrt{\frac32}.
$$

代入得

$$
\boxed{
\nabla_{\boldsymbol x}L
=\left(
-\sqrt{\frac38},
\sqrt{\frac32},
-\sqrt{\frac38}
\right)
}
$$

即约

$$
(-0.6124,\ 1.2247,\ -0.6124).
$$

检查：

$$
\boldsymbol1^{\mathsf T}\nabla_{\boldsymbol x}L=0,
$$

$$
\boldsymbol c^{\mathsf T}\nabla_{\boldsymbol x}L=0.
$$

参数梯度的单 token 贡献为

$$
\nabla_{\boldsymbol\beta}L=(1,1,0),
$$

$$
\nabla_{\boldsymbol\gamma}L
=\left(-\sqrt{\frac32},0,0\right).
$$

## 十二、LayerNorm 与 BatchNorm 的反向依赖图

| 问题 | BatchNorm train | BatchNorm eval | LayerNorm$(D)$ |
|---|---|---|---|
| 一个样本是否依赖 companions | 是 | 否 | 否 |
| 一个 token 的 features 是否耦合 | 视归约布局 | eval 固定 scale | 是 |
| 是否有 running state | 常有 | 读取 | 无 |
| train/eval statistics | 不同 | fixed buffers | 相同当前输入 |
| 反向投影组 | batch/spatial per channel | 无组投影 | per token features |

“LayerNorm 不依赖 batch”只排除了跨样本统计耦合；它绝不意味着 Jacobian 是 diagonal。

## 十三、normalized shape 决定语义

以输入 $(B,T,D)$ 为例：

- LayerNorm$(D)$：每个 token 独立归约 features；
- LayerNorm$((T,D))$：每个样本把所有 token/features 联合归约；
- 只在选定 subset features 上归约：需自定义分组/切片，参数 shape 也随之变化。

若联合归约 $T$，未来 token 会改变过去 token 的统计量；在自回归模型中，这可能造成因果泄漏。标准 per-token LayerNorm$(D)$ 不读取其他 token，因此不由 normalization 本身泄漏未来；完整模型仍需检查 attention mask 与其他跨 token 操作。

## 十四、padding 与变长序列

常见 LayerNorm$(D)$ 对每个 token 自己的 feature vector 操作，padding token 不会进入真实 token 的统计组。但 padding token 自身仍会被归一化，并可能经后续未正确 mask 的 attention/loss 产生影响。

若 normalized shape 包含 $T$，或自定义归一化跨时间聚合，则必须使用 mask-aware count；不同长度的 padding 比例会改变真实 token 的输出。

## 十五、训练与推理相同，不等于整个模型 deterministic

LayerNorm 自身两种 mode 都使用当前输入统计量，不维护 running state。仍可能存在：

- Dropout 或 stochastic depth；
- sampling/beam search 路径差异；
- mixed-precision reduction order；
- dynamic shape/fused kernel 差异；
- 输入本身含随机增强或噪声。

准确说法是“LayerNorm 的统计规则不因 train/eval mode 改变”，不是“含 LayerNorm 的模型训练推理完全相同”。

## 十六、数值稳定与实现边界

### 16.1 variance 计算

直接使用

$$
\operatorname{mean}(x^2)-\operatorname{mean}(x)^2
$$

在大 offset、小 variance 时可能发生消去。成熟 kernel 通常使用稳定 reduction/更高 accumulation precision；手写实现必须用极端输入验证。

### 16.2 小 variance

当 $q\ll\varepsilon$，

$$
\widehat{\boldsymbol x}\approx
\frac{P\boldsymbol x}{\sqrt\varepsilon},
$$

输入 contrast 被固定大 gain 放大。$\varepsilon$ 太小可能使低精度敏感，太大又显著改变尺度不变性和输出能量。

### 16.3 affine 参数

即使 normalized core 稳定，过大的 $\|\boldsymbol\gamma\|_\infty$ 仍可放大输出与反向。诊断需分别记录 pre-affine $\widehat x$ 和 post-affine $y$。

## 十七、图：逐 token 几何与反向

先看图回答：LayerNorm$(D)$ 为什么不跨 batch，却仍在 token 内产生 dense gradient coupling？投影到 $\boldsymbol1^\perp$ 后，$D=2$ 为什么没有可连续保留的切向自由度？

![[00-知识库管理/_assets/figures/neural-networks/fig-layernorm-token-geometry-v2.svg|900]]

> [!figure] 图 30.5-04　LayerNorm 的 token 分组、超平面—球面几何与低维退化
> 左栏在 $(B,T,D)$ 网格中给每个 token 单独圈出 feature 组，并显示 $\gamma,\beta\in\mathbb R^D$ 跨 token 共享；中栏把 $\boldsymbol x$ 先投影到 $\boldsymbol1^\perp$、再归到半径 $\sqrt D$ 的球面；右栏展示 token 内 dense VJP、train/eval 同统计路径，以及 $D=1$ 恒定、$D=2$ 只剩两点的退化。来源：依据 Ba–Kiros–Hinton 2016、PyTorch 2.13 文档与本节 differential 独立绘制；由 [[00-知识库管理/_labs/code/plot_normalization_foundations_v2.py]] 确定性生成。

**怎样读图**：先用左栏确定统计不跨 $(B,T)$，再用中栏数被删除的两个自由度，最后在右栏区分“跨 token 独立”和“token 内 feature Jacobian 非对角”。

**图没有证明什么**：图没有证明 LayerNorm 在所有序列模型中优于 BatchNorm/RMSNorm，也没有证明 Pre-Norm 或 Post-Norm 的深层训练性质；残差放置和系统精度属于后续节点。

## 十八、AI 调用与研究边界

### 18.1 RNN

原论文强调每个 time step 从当前 hidden units 计算 statistics，无需为不同时间维护 running buffers，适合变长/online 序列。经验结果来自当时 RNN 设置，不直接量化现代 LLM。

### 18.2 Transformer

LayerNorm 常作用于 attention/FFN 残差流的 $D$ 轴。它控制 token 内共同 offset/scale，并通过 $\gamma,\beta$ 保留可学习坐标尺度；Pre/Post placement 决定 identity path 与 Jacobian composition，在 NN-39 单独推导。

### 18.3 Conditional LayerNorm

若

$$
\boldsymbol\gamma=\boldsymbol\gamma(c),
\qquad
\boldsymbol\beta=\boldsymbol\beta(c),
$$

条件信息通过 affine 参数调制 normalized representation。统计核心相同，但参数函数、梯度路径和表达能力已改变，不能只按“同一种 LayerNorm”归档。

## 十九、最小验收

1. 对 $(B,T,D)$ 明确列出 statistics/parameter/output shape；
2. 用 $D=3$ 手算 forward/backward；
3. float64 central difference 验证 vector-gain VJP；
4. 验证每 token 的 $dx$ 和为 0；
5. 在 $\varepsilon=0$ 验证 centered radial inner product 为 0；
6. 检查 $D=1,D=2$；
7. 改变其他 batch 样本，确认目标 token 不变；
8. 改变同 token 任一 feature，确认全组输出/梯度变化；
9. train/eval 比较 LayerNorm 本身完全一致；
10. 扫描 offset、scale、epsilon、dtype 与 normalized shape。

> [!summary]
> LayerNorm$(D)$ 是逐 token 的“中心化方向归一 + per-feature affine”。它删除共同平移与近似径向尺度，保留 $D-2$ 维切向几何；不跨 batch，但在 token 内前向和反向都密集耦合。轴、$\varepsilon$ 与低维宽度共同决定真实算子。

- [[归一化、尺度与统计量 MOC]]
- [[习题 - LayerNorm 的逐样本几何与反向传播]]
- [[解答 - LayerNorm 的逐样本几何与反向传播]]

