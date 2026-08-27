---
type: derivation
status: draft
area: [neural-networks/regularization, stochastic-depth, droppath, residual-networks, effective-depth]
aliases: [Stochastic Depth, DropPath, Residual Branch Dropout]
node_id: NN-60
prerequisites: ["[[残差学习、恒等捷径与退化问题]]", "[[残差块 Jacobian 与梯度直通]]", "[[Dropout 的随机掩码、期望与 Inverted Scaling]]", "[[随机、对抗与自适应序列的区别]]"]
related: ["[[深度、有效路径与稳定性证据地图]]", "[[残差缩放、Lipschitz 界与深度稳定性]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]", "[[Pre-Activation、Pre-Norm 与 Post-Norm 残差]]"]
sources: ["[[S-2016-Huang-Stochastic-Depth]]", "[[S-2017-Larsson-FractalNet-DropPath]]", "[[S-2026-PyTorch-Dropout-Stochastic-Depth]]", "[[S-2014-Srivastava-Dropout]]"]
exercises: ["[[习题 - Stochastic Depth、DropPath 与有效深度]]"]
solutions: ["[[解答 - Stochastic Depth、DropPath 与有效深度]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-stochastic-depth-effective-paths-v2.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Stochastic Depth、DropPath 与有效深度

> [!abstract] 本章主问题
> Residual block 的 identity rail 允许训练时随机删除整条 residual branch，而不破坏 state shape。现代 Inverted DropPath 常用 $x_{l+1}=x_l+b_lF_l(x_l)/q_l$，在固定 $x_l$ 下匹配完整 block 的条件均值；同时使 branch 二阶矩放大、活跃 block 数成为 Poisson-binomial 随机变量。实际 FLOP 是否下降取决于 branch 是否真正短路，而不是输出最后是否乘了零。

## 一、学习目标

读完本节，你应能：

1. 写出原始 stochastic depth 与现代 inverted DropPath 两种合同；
2. 推导 residual state、branch 和 local Jacobian 的条件期望；
3. 推导 branch covariance 与参数/input gradients；
4. 把活跃 block 数写成 Poisson-binomial 随机变量；
5. 计算 linear survival schedule 的均值、方差和极端路径概率；
6. 区分 physical depth、active depth、path length 与 effective depth；
7. 区分 batch-shared、per-sample 和更细 gate；
8. 解释“先算后乘零”为什么通常不省 FLOP；
9. 审计 normalization state、checkpoint RNG、分布式和 schedule 交互；
10. 设计质量—稳定性—计算三账验收。

## 二、为什么 Residual Block 能删除整条 Branch

标准残差块：

$$
x_{l+1}=x_l+F_l(x_l;\theta_l).
$$

若 identity/projection rail 已把 shape 对齐，即使不计算 $F_l$，仍可定义

$$
x_{l+1}=x_l.
$$

这与普通串联层不同。若串联网络是

$$
x_{l+1}=F_l(x_l),
$$

直接删除 $F_l$ 未必保证 shape、语义或后续输入分布合法。Stochastic depth 的结构基础不是“任何层都能 drop”，而是 residual rail 提供合法 bypass。

## 三、现代 Inverted DropPath 合同

令 block $l$ 的 survival probability 为

$$
q_l\in(0,1],
$$

gate 为

$$
b_l\sim\operatorname{Bernoulli}(q_l).
$$

训练态：

$$
\boxed{
x_{l+1}
=x_l+\frac{b_l}{q_l}F_l(x_l;\theta_l)
}.
$$

evaluation：

$$
\boxed{
x_{l+1}=x_l+F_l(x_l;\theta_l)
}.
$$

条件于固定 $x_l$：

$$
\mathbb E_{b_l}[x_{l+1}\mid x_l]
=x_l+F_l(x_l).
$$

这与 element dropout 的 inverted scaling 同构，但随机对象是整条 branch tensor，通常一个 sample 的所有 channel/spatial/token coordinates 共享同一个 scalar gate。

## 四、原始 Scaling 合同

历史 stochastic depth 常写为训练态

$$
x_{l+1}=x_l+b_lF_l(x_l),
$$

测试态

$$
x_{l+1}=x_l+q_lF_l(x_l).
$$

它在局部状态层面匹配

$$
\mathbb E[x_l+b_lF_l(x_l)\mid x_l]
=x_l+q_lF_l(x_l).
$$

Inverted 版本把 $q_l$ 的缩放移到训练 branch，并在 eval 使用 full branch。两者可通过参数尺度建立联系，但在 normalization、weight decay、初始化、有限精度和 optimizer dynamics 下不是逐步相同的训练算法。读论文/代码时必须识别是哪一种。

## 五、Branch 的方差与坐标 Covariance

定义随机 branch contribution

$$
R_l=\frac{b_l}{q_l}F_l(x_l).
$$

条件均值：

$$
\mathbb E[R_l\mid x_l]=F_l(x_l).
$$

条件 covariance：

$$
\boxed{
\operatorname{Cov}(R_l\mid x_l)
=\frac{1-q_l}{q_l}
F_l(x_l)F_l(x_l)^\mathsf T
}.
$$

因为一个 scalar gate 共享整条 branch，conditional covariance 是由 $F_lF_l^\mathsf T$ 给出的 rank-one 结构。逐坐标：

$$
\operatorname{Var}(R_{l,i}\mid x_l)
=\frac{1-q_l}{q_l}F_{l,i}(x_l)^2.
$$

并且

$$
\mathbb E\|R_l\|_2^2
=\frac1{q_l}\|F_l(x_l)\|_2^2.
$$

所以均值匹配仍伴随 branch energy 放大。深层使用很小 $q_l$ 时，偶尔存活的 branch 可能产生大 residual jump。

## 六、Local Jacobian 与梯度

固定 gate realization：

$$
J_l
=\frac{\partial x_{l+1}}{\partial x_l}
=I+\frac{b_l}{q_l}J_{F_l}(x_l).
$$

当 $b_l=0$：

$$
J_l=I.
$$

当 $b_l=1$：

$$
J_l=I+\frac1{q_l}J_{F_l}.
$$

条件于固定 $x_l$：

$$
\mathbb E_{b_l}[J_l\mid x_l]
=I+J_{F_l}(x_l).
$$

但不要推出

$$
\mathbb E[J_L\cdots J_1]
=\prod_l\mathbb E[J_l].
$$

因为后层 Jacobian 的 evaluation point 依赖前层 gates，随机矩阵也一般不独立/可交换。

令上游梯度为 $g_{l+1}$。输入 VJP：

$$
\boxed{
g_l
=g_{l+1}
+\frac{b_l}{q_l}J_{F_l}(x_l)^\mathsf Tg_{l+1}
}.
$$

参数梯度：

$$
\boxed{
\nabla_{\theta_l}\mathcal L
=\frac{b_l}{q_l}
\left(\frac{\partial F_l}{\partial\theta_l}\right)^\mathsf T
g_{l+1}
}.
$$

若 $b_l=0$，branch 参数本次 data-gradient 为零，但输入仍沿 identity rail 收到 $g_{l+1}$。Weight decay/optimizer state 的更新边界仍需另行声明。

## 七、什么是“有效深度”

设共有 $L$ 个 gated residual blocks，定义活跃 block 数

$$
\boxed{
D=\sum_{l=1}^Lb_l
}.
$$

若 gates 独立但 $q_l$ 可不同，则 $D$ 服从 Poisson-binomial distribution：

$$
\mathbb E[D]=\sum_lq_l,
$$

$$
\boxed{
\operatorname{Var}(D)=\sum_lq_l(1-q_l)
}.
$$

概率生成函数为

$$
G_D(t)
=\prod_{l=1}^L\left((1-q_l)+q_lt\right).
$$

$t^k$ 的系数就是 $P(D=k)$。

这里 $D$ 只数活跃 residual transformations。物理网络仍有 $L$ 个 parameterized blocks，identity states 仍跨越所有位置；“有效深度”也不等于 function composition 的唯一复杂度指标。

## 八、完整手算：四层 Linear Schedule

设最深 block survival 为

$$
q_L=0.5,
$$

使用

$$
q_l=1-\frac lL(1-q_L),
\qquad l=1,\ldots,L.
$$

取 $L=4$：

$$
(q_1,q_2,q_3,q_4)
=(0.875,0.75,0.625,0.5).
$$

期望活跃深度：

$$
\mathbb E[D]
=0.875+0.75+0.625+0.5
=\boxed{2.75}.
$$

方差：

$$
\operatorname{Var}(D)
=0.875(0.125)+0.75(0.25)
$$

$$
\quad+0.625(0.375)+0.5(0.5)
=\boxed{0.78125}.
$$

全部活跃概率：

$$
P(D=4)=\prod_lq_l
=0.205078125.
$$

全部删除概率：

$$
P(D=0)=\prod_l(1-q_l)
=0.005859375.
$$

即使期望深度是 2.75，训练实际看到的是 $D=0,1,2,3,4$ 的混合，不能用一个固定 2.75 层网络替代其联合训练语义。

## 九、Survival Schedule 是结构先验

常见 schedule：

### Constant

$$
q_l=q.
$$

各层同 rate，简单但不区分浅/深 branch。

### Linear Decay

$$
q_l=1-\frac lL(1-q_L).
$$

浅层更常保留，深层更强正则；这是经典选择，不是普遍最优定理。

### Stage/Block-Specific

按 resolution、width、branch cost、pretrained sensitivity 或 gradient statistics 设置。

调 schedule 时必须报告使用的是 survival $q_l$ 还是 drop $p_l=1-q_l$。一些实现传入逐层增长的 `drop_path_rate`，数值方向与 survival 正好相反。

## 十、Batch Gate 与 Row Gate

### Batch-Shared Gate

mask shape 可为

$$
(1,1,\ldots,1).
$$

整个 batch 同时保留或删除 block。优点是若 gate 为 0，可真正跳过完整 branch kernel；缺点是同一步所有样本共享 architecture noise，batch averaging 不会降低这部分 gate variance。

### Per-Sample / Row Gate

mask shape 常为

$$
(B,1,\ldots,1).
$$

每个样本独立选择 branch，但同一样本所有 feature coordinates 共享。它增加样本多样性，却通常让同一 batch 中既有保留又有删除样本，GPU 实现常先计算全 batch branch 再逐 row 乘 mask，因而不省主要 FLOP。

### Token/Element Gate

若 gate 细化到 token 或 channel，就不再是通常意义的整 branch stochastic depth；output covariance、compute 和语义都改变。

## 十一、DropPath 术语的历史与现代用法

FractalNet 的 drop-path 在多路径 fractal architecture 中随机删除整条结构路径，旨在减少路径间共适应。Residual stochastic depth 则依赖 identity rail 随机 bypass residual branch。

现代视觉/Transformer 代码常把 per-sample residual-branch gate 命名为 `DropPath`。因此看到名称时不要反推结构，应直接检查：

- mask shape；
- gate 作用在 branch、block 还是多分支集合；
- 是否有 identity rail；
- 是否 inverted scaling；
- train/eval 行为；
- 是否真正 conditional execution。

## 十二、Compute：先算再乘零不等于随机浅网

设 branch $l$ 成本为 $C_l$。

若 batch gate 为 0 时真正不调用 $F_l$，理想期望 branch compute 约为

$$
\boxed{
\mathbb E[C_{\rm branch}]
=\sum_lq_lC_l
}.
$$

还需加 gate、control flow、load imbalance 与编译开销。

若实现总是先算

$$
r_l=F_l(x_l)
$$

再做

$$
x_{l+1}=x_l+(b_l/q_l)r_l,
$$

则主要 $F_l$ FLOP 已发生，计算量近似 full network；收益只能来自 regularization，不应报告成 train-short speedup。

Per-sample row gate 要真正节省计算需动态压缩 active rows、执行 branch、再 scatter 回 batch；gather/scatter、变形 matmul 和小 batch occupancy 可能抵消收益。

## 十三、Normalization 与 State 边界

考虑

$$
x_{l+1}=x_l+\frac{b_l}{q_l}
F_l(\operatorname{Norm}(x_l)).
$$

### LayerNorm/RMSNorm

无 running buffer，但 branch 被计算后再 drop 时仍付出 normalization/branch 成本；mask 放在 Norm 前后也定义不同函数。

### BatchNorm

若先计算 branch 再 mask，BatchNorm running statistics 每步更新，即使输出被删除；若 batch gate 为 0 时真正跳过 branch，该步 BN state 不更新。两者 evaluation buffer 不同。

原始 stochastic-depth CNN 的 BN/short-circuit 语义不能直接等同现代 Pre-Norm Transformer 的 DropPath。

### Projection Shortcut

若 rail 不是 identity 而是 $P_lx_l$，删除 branch 后仍执行 projection：

$$
x_{l+1}=P_lx_l.
$$

它的成本和 Jacobian 不是 $I$，所以“梯度直通”与 expected compute 账都要改写。

## 十四、与 Residual Scaling 的交互

若 baseline 已有 branch scale $\alpha_l$：

$$
x_{l+1}=x_l+\alpha_lF_l(x_l),
$$

加入 inverted DropPath：

$$
x_{l+1}=x_l+\alpha_l\frac{b_l}{q_l}F_l(x_l).
$$

条件 branch variance 为

$$
\frac{1-q_l}{q_l}\alpha_l^2F_lF_l^\mathsf T.
$$

所以 $q_l$ 与 $\alpha_l$ 共同决定 residual noise scale。DeepNorm、Fixup、ReZero、LayerScale 等已有 depth scaling 时，不能独立复制另一个模型的 DropPath rate；应联合校准 branch RMS、update ratio 与 Jacobian statistics。

## 十五、RNG、重算与分布式

必须明确：

1. gates 按 step、microbatch、sample 还是 token 采；
2. data-parallel ranks 是否独立；
3. pipeline stages 是否共享 path realization；
4. gradient checkpoint 是否复现 forward gate；
5. accumulation microbatches 是否重采；
6. batch-shared short-circuit 是否造成 ranks 计算不均；
7. 编译器是否为随机 control flow 生成 graph break/fallback；
8. evaluation 是否完全关闭 gate 或执行 MC paths。

若不同 ranks 共享 gate，可增加同步/相关性；若独立 gates，则各 rank 梯度来自不同 subnetwork。两者都可合法，但有效 batch variance 不同。

## 十六、泛化与优化解释的证据边界

可能机制包括：

- 训练时缩短部分 gradient paths；
- 让不同深度 subnetworks 共享参数；
- 对 residual transformations 注入结构噪声；
- 降低对特定深层路径组合的依赖；
- batch-shared 真短路时减少训练计算。

这些不是同一句话，也不由最终 accuracy 自动识别。要声称“优化改善”，应测收敛、gradient/Jacobian、训练 loss；要声称“regularization 改善”，应在 matched optimization/compute 下看 held-out risk；要声称“省计算”，必须 profiler 证明 branch 未执行。

## 十七、公平实验协议

至少比较：

1. no DropPath；
2. constant schedule；
3. linear schedule；
4. batch gate；
5. row gate；
6. original vs inverted scaling；
7. true short-circuit vs mask-after-compute。

共同报告：

- $q_l/p_l$ 全 schedule；
- empirical active-depth distribution；
- train/validation NLL 与多 seed；
- gradient/branch RMS、update ratio、Jacobian norm；
- BN/running-state policy；
- achieved FLOP/s、kernel count、tokens/images per second；
- P50/P95 step time 与 distributed imbalance；
- full-depth evaluation 与可选 MC-path evaluation。

Matched-compute 与 natural-best 两条轨道应分开，避免把节省的训练算力重新用于更宽/更深模型后仍宣称纯正则化收益。

## 十八、常见误区

1. **“DropPath 就是 element Dropout”**：随机对象和 covariance 不同；
2. **“均值匹配，所以整网预测均值匹配”**：后续 state/非线性依赖 gates；
3. **“期望 Jacobian 等于全深网络，所以深层乘积也等价”**：随机 evaluation points 与乘积不交换；
4. **“mask 为零就省掉 branch FLOP”**：先算后 mask 不省；
5. **“有效深度 2.75 就是固定 2.75 层网络”**：训练是离散深度混合；
6. **“batch gate 与 row gate 相同”**：样本相关性与短路能力不同；
7. **“DropPath 名称定义唯一”**：FractalNet 与现代 residual 用法需分开；
8. **“已有 residual scaling 不影响 rate”**：二者共同决定 noise scale；
9. **“随机深度一定改善泛化”**：需架构/任务实证。

## 十九、图：Residual Rail、Depth Law 与实现语义

先看图回答：为什么 $b_l=0$ 时 branch 参数梯度为零而 input gradient 仍有 identity rail？四个 survival probabilities 怎样给出 $E[D]=2.75$ 与 $\operatorname{Var}(D)=0.78125$？为什么 row gate 通常比 batch gate 更难真正省 FLOP？

![[00-知识库管理/_assets/figures/neural-networks/fig-stochastic-depth-effective-paths-v2.svg|900]]

> [!figure] 图 30.8-04　Stochastic Depth 的随机 residual branches、survival schedule 与有效深度账
> 左栏展示 identity rail 和整 branch gate；中栏用四层 linear schedule 计算 Poisson-binomial active depth moments；右栏区分 batch/row gate、mask-after-compute 与 true short-circuit。来源：依据 Huang et al.、FractalNet、torchvision 当前 stochastic-depth 接口与本节独立推导绘制；由 [[00-知识库管理/_labs/code/plot_random_regularization_foundations_v2.py]] 确定性生成。

**怎样读图**：先沿 rail 确认 state shape 始终合法，再把每个 gate 当作 Bernoulli variable 计算路径统计，最后检查实现是否在 branch 之前做 control flow，还是只在输出端乘零。

**图没有证明什么**：图不证明 linear schedule 最优，不证明 $E[D]$ 足以描述训练函数族，也不证明 stochastic depth 在所有架构、normalization 和硬件上同时提升质量与速度。

## 二十、最小验收

1. 写出 original 与 inverted 两种 train/eval 合同；
2. 推导 state/branch conditional mean；
3. 推导 branch covariance 与平方范数；
4. 推导 local Jacobian、input VJP 与参数梯度；
5. 写出 Poisson-binomial generating function；
6. 复算四层 schedule 的均值、方差与极端概率；
7. 区分四种 depth 概念；
8. 比较 batch/row gate 与 FractalNet/modern DropPath；
9. 审计 true skip、normalization state、residual scale 与 RNG；
10. 设计质量—稳定性—计算三账实验。

> [!summary]
> Stochastic Depth/现代 DropPath 把 Bernoulli gate 放在整条 residual branch 上。Inverted scaling 在单块固定输入下恢复 full branch 均值，却放大 branch energy；删除 branch 时参数 data-gradient 为零，identity rail 仍传输入梯度。活跃 block 数由 survival schedule 定义为 Poisson-binomial 分布，而真实算力收益只有在 branch 被条件短路时成立。术语、mask axis、normalization state、residual scaling 与 RNG 都属于完整合同。

- [[随机正则化与网络级泛化接口 MOC]]
- [[习题 - Stochastic Depth、DropPath 与有效深度]]
- [[解答 - Stochastic Depth、DropPath 与有效深度]]
