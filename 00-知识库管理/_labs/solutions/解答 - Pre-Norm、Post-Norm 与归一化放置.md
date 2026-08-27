---
type: solution
status: draft
area: [neural-networks/normalization, residual-networks, transformers]
topic: "[[Pre-Norm、Post-Norm 与归一化放置]]"
exercise: "[[习题 - Pre-Norm、Post-Norm 与归一化放置]]"
sources: ["[[S-2020-Xiong-Transformer-LayerNorm]]", "[[S-2022-Su-9009-PreNorm-PostNorm]]"]
created: 2026-08-23
updated: 2026-08-23
---
# 解答 - Pre-Norm、Post-Norm 与归一化放置

## A

### NN-NPP-A01
$$
\text{Pre: }x^+=x+F(N(x)),
$$

$$
J_{\mathrm{pre}}
=I+J_F(N(x))J_N(x).
$$

$J_N$ 在 $x$ 处，$J_F$ 在 $N(x)$ 处；扰动先过 $J_N$ 再过 $J_F$。

$$
\text{Post: }x^+=N(x+F(x)),
$$

$$
J_{\mathrm{post}}
=J_N(x+F(x))[I+J_F(x)].
$$

$J_F$ 在 $x$ 处，$J_N$ 在 residual sum $x+F(x)$ 处；$J_N$ 左乘整个 residual Jacobian。

### NN-NPP-A02
- “Pre-Norm 有 identity path”：真，单子层 Jacobian 显式含 $I$。
- “全网 Jacobian 必然接近单位阵”：假，$\prod(I+A_l)$ 仍可爆炸、收缩或非正规暂态放大。
- “Pre-Norm 不经过任何 norm”：假，branch 经过 norm，许多架构最后还有 final norm；只说 block 内 identity rail 不逐层经过 norm。

### NN-NPP-A03
- residual sum $x_L=x_0+\sum\Delta_l$：精确恒等式；
- Xiong 的初始化梯度/warm-up：特定模型假设下 mean-field 定理与实验；
- residual stream 增长导致相对层增量下降/深度稀释：需要增量幅度和相关性条件的解释；
- Pre/Post 最终任务效果：架构、调参和数据相关经验规律。

## B

### NN-NPP-B01
$F(x)=c$ 给出 $J_F=0$。

Pre：

$$
x^+=x+c,
\qquad J=I.
$$

Post：

$$
x^+=N(x+c),
\qquad J=J_N(x+c).
$$

$\varepsilon=0$ LayerNorm 的 $J_N$ 把共同 shift 与 centered radial direction 映为 0；Pre 的 $I$ 则原样传递这两类输入扰动。

### NN-NPP-B02
$$
J_{\mathrm{pre}}=I+aA,
\qquad
J_{\mathrm{post}}=A(I+aI)=(1+a)A.
$$

对 $Av=0$：

$$
J_{\mathrm{pre}}v=v,
\qquad
J_{\mathrm{post}}v=0.
$$

对 $At=\lambda t$：

$$
J_{\mathrm{pre}}t=(1+a\lambda)t,
$$

$$
J_{\mathrm{post}}t=(1+a)\lambda t.
$$

这是固定局部线性算子账本；真实两架构的 $A$ 求值点不一定相同。

### NN-NPP-B03
令

$$
A_l=J_{F_l}(N(x_l))J_N(x_l).
$$

若输出 $y=N_f(x_L)$，则

$$
J_{y\leftarrow x_0}
=J_{N_f}(x_L)
\prod_{l=L-1}^{0}(I+A_l).
$$

blocks 内有 identity rails，但输出仍被 final norm 的 Jacobian 左乘一次，所以“完全绕过所有 norm”不成立。

## C

### NN-NPP-C01
Pre：令 $z=N(x)$，则

$$
dz=J_N(x)dx,
$$

$$
dx^+=dx+J_F(z)dz
=\left[I+J_F(N(x))J_N(x)\right]dx.
$$

Post：令 $z=x+F(x)$，则

$$
dz=[I+J_F(x)]dx,
$$

$$
dx^+=J_N(z)dz
=J_N(x+F(x))[I+J_F(x)]dx.
$$

### NN-NPP-C02
递推望远镜求和：

$$
x_L-x_0
=\sum_{l=0}^{L-1}(x_{l+1}-x_l)
=\sum_{l=0}^{L-1}\Delta_l.
$$

若 $\Delta_l=c u$ 同向，$x_0$ 可忽略时

$$
\|x_l\|\approx lc,
\qquad
\frac{\|\Delta_l\|}{\|x_l\|}\approx\frac1l.
$$

若 $\Delta_l$ 两两正交，

$$
\left\|\sum_{j<l}\Delta_j\right\|^2
=\sum_{j<l}\|\Delta_j\|^2
\approx lc^2,
$$

故相对增量约 $1/\sqrt l$。随机不相关只是在期望平方 norm 意义下给类似阶，不是逐路径定理。

### NN-NPP-C03
令

$$
z_1=N_1(x),
\quad z_2=F(z_1),
\quad z_3=N_2(z_2),
\quad x^+=x+z_3.
$$

则

$$
J
=I+J_{N_2}(F(N_1(x)))
J_F(N_1(x))
J_{N_1}(x).
$$

外部 $I$ 是 identity rail；branch 内先过 $J_{N_1}$，再 $J_F$，最后 $J_{N_2}$。

## D

### NN-NPP-D01
在一个所有层共享的局部 eigen-direction 上令

$$
A_l=a>0.
$$

则

$$
J_{0\to L}=\prod_l(1+a)=(1+a)^L,
$$

指数增长。含 $I$ 只提供加法路径，不给 $A_l$ 的大小、符号、方向或相关性约束。

### NN-NPP-D02
求和恒等式没有给出：

1. $\Delta_l$ 的大小是否一致/有界；
2. 增量之间的相关性、方向与非线性组合；
3. “有效深度”的可测定义；
4. 是否存在保持参数/计算预算的浅网函数等价；
5. 训练后 $F_l$ 是否退化为近恒等或重复特征。

所以它只提供 residual decomposition，不能单独证明函数类等价。

### NN-NPP-D03
Xiong et al. 在特定 Transformer、初始化和 mean-field 假设下分析初始梯度：Post-LN 输出附近梯度可能偏大，warm-up 有助于稳定；其 Pre-LN 设置梯度更受控，并在论文实验中可减少 warm-up。论文没有证明跨架构最终精度排序，也没有证明任何 Pre-LN 配置永不需要 warm-up。

## E

### NN-NPP-E01
协议应：

- 明确每个 attention/FFN sublayer 的 placement 与 final norm；
- 对齐参数量、depth/width、epsilon、gain/bias；
- 使用相同主干初始化，分别记录 residual scaling/zero-last；
- 对两者分别公平搜索 LR/warm-up/clipping；
- 对齐 training tokens、wall time 与 tuning budget；
- 至少多 seed 报 failure rate；
- 分开响应：训练稳定性、收敛速度、最终 in-domain、迁移/微调，而非单一最优分数。

### NN-NPP-E02
设 attention 为 $A_l$、FFN 为 $F_l$：

$$
u_l=x_l+A_l(N_{l,1}(x_l)),
$$

$$
x_{l+1}=u_l+F_l(N_{l,2}(u_l)).
$$

因此

$$
J_{x_{l+1}\leftarrow x_l}
=\left[I+J_{F_l}(N_{l,2}(u_l))J_{N_{l,2}}(u_l)\right]
\left[I+J_{A_l}(N_{l,1}(x_l))J_{N_{l,1}}(x_l)\right].
$$

中间状态 $u_l$ 决定第二个 norm/branch 的求值点，不能省略。

### NN-NPP-E03
可证伪诊断：

- representation change $\|x_{l+1}-x_l\|/\|x_l\|$：测相对更新，不直接测函数可替代性；
- branch/residual RMS ratio：测尺度占比，不证明新方向/信息量；
- 随机方向 JVP/VJP gain：测局部敏感性样本，不给完整 singular spectrum；
- 删除/交换某层的 ablation：测特定数据上的功能影响，受重优化与分布影响。

若四者随深度共同显示相对增量趋零、局部算子近恒等且删层影响小，才给“深度稀释”更强证据；仍不是所有输入上的函数等价证明。

