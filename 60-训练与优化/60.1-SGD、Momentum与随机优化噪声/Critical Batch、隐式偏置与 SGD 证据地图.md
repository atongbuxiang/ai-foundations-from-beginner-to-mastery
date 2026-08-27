---
type: concept
status: verified
area: [training, optimization, generalization, evidence]
node_id: TRN-08
aliases: [Critical Batch, SGD 隐式偏置证据]
prerequisites: ["[[梯度噪声协方差、Noise Scale 与 SDE 近似]]", "[[损失、总体风险与经验风险]]", "[[隐式偏置、最大间隔与优化选择]]"]
related: ["[[学习率、局部损失变化与相对更新尺度]]", "[[Scaling 实验设计、外推不确定性与证据地图]]", "[[数据优化器调度交互、混杂与归因边界]]"]
sources: ["[[S-2018-McCandlish-Noise-Scale]]", "[[S-2017-Keskar-Large-Batch-Sharpness]]", "[[S-2017-Dinh-Sharp-Minima]]", "[[S-2017-Hoffer-Large-Batch-Train-Longer]]", "[[S-2018-Soudry-Implicit-Bias]]", "[[S-2021-Cohen-Edge-of-Stability]]", "[[S-2025-Su-11260-学习率与Batch-Size均衡]]"]
exercises: ["[[习题 - Critical Batch、隐式偏置与 SGD 证据地图]]"]
solutions: ["[[解答 - Critical Batch、隐式偏置与 SGD 证据地图]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-critical-batch-evidence-ledger-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Critical Batch、隐式偏置与 SGD 证据地图

> [!abstract] 一句话结论
> Critical batch 是“大 batch 的并行收益开始明显递减”的任务、阶段与协议相关尺度，不是稳定性硬上限。SGD 的 implicit bias 在某些线性可分问题上有精确定理；“小 batch 因噪声找到平坦极小值所以泛化更好”则是一条包含多重混杂、参数化依赖与反例的经验假说链。

## 一、先把四种效率分开

| 口径 | 分母 | 问题 |
|---|---|---|
| step efficiency | optimizer steps | 达目标需要多少次同步更新？ |
| sample/token efficiency | examples/tokens | 看过多少数据？ |
| compute efficiency | FLOPs/energy | 消耗多少计算资源？ |
| time efficiency | wall-clock | 实际多久？ |

batch 增大通常降低 steps，却增加每 step 的 examples；硬件并行还可能降低每 step 时间。说“更快”前必须指定表中哪一列。

## 二、McCandlish 经验模型

[[S-2018-McCandlish-Noise-Scale]]提出一个简洁拟合。设达到某 target loss 所需 steps 为 $S(B)$、examples 为 $E(B)=BS(B)$。经验近似写为

$$
\frac{S(B)}{S_{min}}\approx1+\frac{B_{noise}}B,
\qquad
\frac{E(B)}{E_{min}}\approx1+\frac B{B_{noise}}.
$$

于是：

- $B\ll B_{noise}$：增加 batch 可大幅减少 steps，sample cost 接近最低；
- $B\gg B_{noise}$：steps 接近下限，再加 batch 主要浪费 samples/compute；
- $B=B_{noise}$：两种归一化成本都约为各自极限的 2 倍。

这给出一种 **critical batch** 解释。它依赖 target、训练阶段、优化器与拟合质量；不是所有任务都严格服从这条双曲线。

## 三、从 noise scale 到 critical batch 不能跳过系统层

即使统计上进入收益递减区，wall-clock optimum 还取决于 throughput $R(B)$、通信和内存。粗略时间

$$T(B)=S(B)\,t_{step}(B)$$

可能在统计 critical batch 左侧或右侧最优。gradient accumulation 增大 optimizer batch，却未必提供 data-parallel 的并行加速；反之 hardware batch 增大也可能触发不同 kernel。

因此要同时报告：$S,E,$ FLOPs、tokens/s、communication、memory 与 final metric。

## 四、implicit bias 的精确定理样板

对 linearly separable 数据上的 homogeneous linear predictor，使用 logistic/exponential-tail loss 的 gradient descent，在特定步长等条件下：

- training loss 趋向 0；
- weight norm 趋向无穷；
- normalized direction 趋向 hard-margin SVM direction。

这是 [[S-2018-Soudry-Implicit-Bias]] 的代表性结论。它说明即使显式目标没有 finite minimizer，优化轨迹仍可选择一个方向。

> [!warning] 定理不等于口号
> 必须保留：线性可分、模型齐次/线性、损失尾部、gradient method、步长与方向收敛等条件。它不证明任意深网、任意 SGD noise、Adam 或 finite-time checkpoint 都选择同一 max-margin 解。

## 五、“小 batch → flat → generalize”的证据链审计

这条常见叙述至少包含四个箭头：

$$
\text{small batch}
\to\text{larger gradient noise}
\to\text{flatter minimum}
\to\text{better test risk}.
$$

逐箭头判断：

1. iid、mean reduction 下 covariance 随 $1/B$：**精确二阶矩结论**；
2. noise 使轨迹落入“更平”区域：**依赖 dynamics、metric 与训练协议的经验/理论问题**；
3. 常见 parameter-space sharpness 测到 functionally meaningful flatness：**受重参数化反例挑战**；
4. flatness 导致 generalization：**不能脱离数据、函数空间 margin、norm 与选择偏差单独成立**。

[[S-2017-Keskar-Large-Batch-Sharpness]]提供历史数值证据；[[S-2017-Dinh-Sharp-Minima]]利用 ReLU rescaling 构造函数不变而参数 sharpness 任意改变的反例。

## 六、更新次数、BN 与调度是混杂变量

固定 epochs 时，大 batch 的 optimizer steps 更少：

$$S_{epoch}=\frac{N\times epochs}{B}.$$

所以 batch size 同时干预 noise、update count、scheduler sampling、BatchNorm statistics 和 hardware regime。[[S-2017-Hoffer-Large-Batch-Train-Longer]]展示训练更久和 Ghost BatchNorm 可缩小特定 large-batch gap；其他 large-batch 工作还表明 LR scaling/warmup 能在特定 ImageNet 协议中保持准确率。

合理结论不是“大 batch 永远无害”，而是：原始 gap 不能只归因于一个未隔离的噪声机制。

## 七、一个四臂因果实验

要区分 batch noise 与 update count，可设计：

| 组 | optimizer batch | optimizer steps | BN statistics batch | 目的 |
|---|---:|---:|---:|---|
| A | small | fixed high | small | baseline |
| B | large | same epochs | large | 总效应 |
| C | large | match A steps | large | 隔离 step count |
| D | large | match A steps | ghost-small | 再隔离 BN stats |

所有组还需按预注册规则调 LR/schedule，报告 samples、FLOPs 和 wall time。若各组调参预算不同，又会引入 selection bias。

## 八、图：从精确结论到开放假说

先看图回答：关于 batch、noise、sharpness 与 generalization 的每条箭头属于定理、实验、反例还是开放机制？

![[00-知识库管理/_assets/figures/training-optimization/fig-critical-batch-evidence-ledger-v1.svg|900]]

> [!figure] 图 TRN-08　Critical batch 的效率面与 SGD implicit-bias 证据阶梯
> 左侧把 step/sample/time 三种最优点分开；右侧为 batch→noise→sharpness→generalization 的逐箭头证据审计，红色断点标出参数化反例与混杂。来源：据 McCandlish、Keskar、Dinh、Hoffer 和 Soudry 等重新组织并独立绘制。

**怎样读图**：先在左侧选择预算口径，再到右侧逐条检查因果箭头；一个已证明的 $1/B$ covariance law 不能越过中间断点直接推出 test risk。

**图没有证明什么**：图不提供某个模型的最佳 batch，不把 cited experiments 合并成 meta-analysis，也不否认 normalized/function-space sharpness 可能有预测价值。

## 九、Edge of Stability 与有限学习率

[[S-2021-Cohen-Edge-of-Stability]]说明深网训练可能长期处在静态 quadratic descent lemma 不足以描述的区域。它与 stochastic noise、finite LR implicit regularization 共同提示：最终解的选择取决于整条 trajectory，而不是只由终点 Hessian 决定。

这是研究方向，不是“越接近不稳定越泛化”的调参法则。任何此类主张都应同时测 stability、train objective、validation、curvature、update norm 与多 seed 不确定性。

## 十、科学空间研读框

[[S-2025-Su-11260-学习率与Batch-Size均衡]]把 learning-rate–batch 平衡组织为可推导的问题。课程在此增加三个证据门：效率口径、系统成本和因果混杂。博客或单篇论文中的漂亮比例式，应先在 [[实验 - SGD、Momentum 与随机优化噪声最小数值审计]] 中做最小验证，再进入大模型实验。

## 十一、本节回顾

- critical batch 表示边际并行收益递减，不是稳定硬阈值；
- step、sample、compute 和 wall-clock optimum 可以不同；
- implicit bias 有严格的特殊情形定理，也有尚未统一的深网解释；
- raw sharpness 受参数化影响，不能单独承担泛化因果；
- batch 实验必须隔离 update count、BN、LR/schedule 与调参预算；
- 本卷的综合验收见 [[60.1 分卷累计测验与复现门]]。

## 练习与独立解答

- [[习题 - Critical Batch、隐式偏置与 SGD 证据地图]]
- [[解答 - Critical Batch、隐式偏置与 SGD 证据地图]]
