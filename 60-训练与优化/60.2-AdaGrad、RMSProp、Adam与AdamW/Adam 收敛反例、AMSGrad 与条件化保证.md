---
type: derivation
status: verified
area: [training, optimization, adam, convergence]
node_id: TRN-13
aliases: [Adam 经典反例, AMSGrad]
prerequisites: ["[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]", "[[在线学习协议、Regret 与 Comparator]]", "[[凸函数、Jensen 不等式与上图集]]"]
related: ["[[AdaGrad、累计平方梯度与稀疏几何]]", "[[随机、对抗与自适应序列的区别]]", "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]"]
sources: ["[[S-2018-Reddi-Adam-AMSGrad]]", "[[S-2015-Kingma-Ba-Adam]]", "[[S-2026-Framework-Adaptive-Optimizer-Semantics]]"]
exercises: ["[[习题 - Adam 收敛反例、AMSGrad 与条件化保证]]"]
solutions: ["[[解答 - Adam 收敛反例、AMSGrad 与条件化保证]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-adam-amsgrad-counterexample-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Adam 收敛反例、AMSGrad 与条件化保证

> [!abstract] 一句话结论
> Adam 的指数二阶矩会遗忘过去的大梯度，使某些后续小梯度获得过大的相对步长；在一个一维凸周期序列上，净更新可持续指向最差端点。AMSGrad 用逐坐标历史最大二阶矩恢复 long-term memory，但它的收敛保证仍依赖问题类、步长与有界性条件，不是深网训练的万能保险。

## 一、为什么“每一步都按 RMS 缩放”仍可能失败

自适应方法常写成

$$
x_{t+1}=\Pi_{\mathcal F}
\left(x_t-\alpha_t\frac{m_t}{\sqrt{v_t}+\epsilon}\right).
$$

直觉容易说：“大 gradient 进入 $v_t$ 后会自动缩小自己的步长。”问题在于 $v_t$ 是 EMA，会遗忘；未来的小 gradient 可能在 denominator 已下降时得到更大的相对权重。收敛分析需要控制**跨时间的有效尺度**，不能只验证每个 $v_t>0$。

一个有用的诊断量是

$$
\Gamma_{t+1}
=\frac{\sqrt{v_{t+1}}}{\alpha_{t+1}}
-\frac{\sqrt{v_t}}{\alpha_t}.
$$

若该量可为负，逆 effective step $\sqrt v/\alpha$ 在某些时段下降，意味着过去的抑制被撤回。$\Gamma_t\ge0$ 不是所有定理的必要条件，但清楚暴露了“遗忘 denominator”这一机制。

## 二、经典三周期凸反例

在可行域 $\mathcal F=[-1,1]$ 上，定义线性损失

$$
f_t(x)=
\begin{cases}
Cx,&t\bmod3=1,\\
-x,&\text{otherwise},
\end{cases}
\qquad C>2.
$$

gradient 周期为

$$
g_t=(C,-1,-1,C,-1,-1,\ldots).
$$

每三个损失的和为

$$
(C-2)x.
$$

因 $C-2>0$，最佳固定决策是 $x^*=-1$；$x=+1$ 反而是最差端点。

[[S-2018-Reddi-Adam-AMSGrad]]证明，在特定参数选择下，例如

$$
\beta_1=0,
\qquad
\beta_2=\frac1{1+C^2},
\qquad
\alpha_t=\frac\alpha t,
$$

并满足相应步长条件时，Adam/RMSProp 型更新会走向 $+1$。重要的不是死记参数，而是重建一周期净位移：大正梯度虽然决定真正最优方向，却被自身刚抬高的 denominator 强烈缩小；随后两个负梯度到来时 denominator 已衰减，它们推动 $x$ 向正方向的总位移反而更大。

> [!warning] 投影与符号不可省略
> 这里在最小化 $f_t$，更新是 $x\leftarrow x-\text{scaled gradient}$。正梯度 $C$ 推向负方向，负梯度 $-1$ 推向正方向。忘掉投影 $\Pi_{[-1,1]}$ 或把端点符号写反，会彻底改变反例。

## 三、手算一周期看机制

为突出 denominator 遗忘，先取 $\beta_1=0,\epsilon=0$，不做 bias correction。递推为

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,
\qquad
\Delta x_t=-\alpha_t\frac{g_t}{\sqrt{v_t}}.
$$

周期第一步 $g=C$ 时，$v$ 被推向 $C^2$，所以负向位移约为 $-\alpha_t$ 量级；接着 $g=-1$ 两次，$v$ 连续衰减，两个正向位移可能各自接近或超过 $\alpha_t$。净位移因此可以为正。

严格证明还需跟踪跨周期初值、变化 $\alpha_t$ 和投影；课堂数值实验会逐步打印 $g_t,v_t,\alpha_t/\sqrt{v_t},\Delta x_t$，不以一张最终曲线替代机制。

## 四、AMSGrad 怎样加 long-term memory

AMSGrad 先按 Adam 更新 $v_t$，再保存

$$
v_t^{max}=\max(v_{t-1}^{max},v_t)
$$

（逐坐标最大），并用 $v_t^{max}$ 形成 denominator。于是

$$
v_t^{max}\ge v_{t-1}^{max}.
$$

过去的大二阶矩不会被 EMA 忘掉。若 learning-rate schedule 也按定理要求衰减，逆 effective step 更容易保持所需的单调控制。

代价包括：

- 多保存一份与参数同形的 $v^{max}$ 状态；
- 某次异常大 gradient 可能永久压小该坐标后续步长；
- epsilon、bias correction 与 framework indexing 仍需明确；
- “long-term memory 修补反例机制”不等于所有任务上优化更快。

## 五、保证依赖哪些条件

AMSGrad/Adam-type 的 regret 或 stationary-point 结论会因论文而异，常见条件包括：

| 条件 | 为什么出现 |
|---|---|
| 凸 loss 或 smooth nonconvex objective | 决定 proof target 是 regret 还是 gradient norm |
| bounded feasible diameter | 控制投影距离项 |
| bounded gradients/moments | 控制自适应 metric 与噪声项 |
| 特定 $\alpha_t$ schedule | 保证累计误差与有效步长可控 |
| $\beta_1,\beta_2$ 关系/变化规则 | 控制 momentum 与 denominator 的时间耦合 |
| epsilon 与 positive denominator | 避免奇异并影响常数/算法 |

打开框架的 `amsgrad=True` 只选择一个实现变体，不会自动验证训练问题满足这些假设。

## 六、反例没有证明什么

反例严格否定“原始 Adam 对所有该类凸序列都保证收敛”的普遍命题，但不推出：

- Adam 在现实深网中通常发散；
- AMSGrad 在所有 benchmark 上都优于 Adam；
- 任何训练 loss 波动都是同一个反例机制；
- 只要 $v_t$ 单调就能解决所有非凸、随机与数值问题；
- AdamW 的 decoupled decay 会自动修复 denominator 时间行为。

> [!research] 理论仍在演化
> 后续工作给出了不同问题选择顺序、较大 $\beta_2$、强增长或其他条件下 vanilla Adam 的正面结果。课程用“命题—反例—修补条件”组织，而不把 2018 反例写成对 Adam 的最终判决。

## 七、图：大梯度被压小，小梯度被放大

先看图回答：真正决定周期 optimum 的 $C$ 为什么在 Adam 位移账上反而输给两个 $-1$？AMSGrad 改了哪一条状态线？

![[00-知识库管理/_assets/figures/training-optimization/fig-adam-amsgrad-counterexample-v1.svg|900]]

> [!figure] 图 TRN-13　三周期凸反例、有效步长遗忘与 AMSGrad 修补
> 左侧区分 objective sum 与 optimizer displacement；中间展示 Adam denominator 的升高—遗忘；右侧用 $v^{max}$ 的单调台阶阻止遗忘。来源：依据 [[S-2018-Reddi-Adam-AMSGrad]] 的反例结构独立重绘。

**怎样读图**：先用三步 loss 和确定最佳端点，再逐步检查 scaled displacement；最后比较 $v_t$ 与 $v_t^{max}$，不要从箭头方向直接猜 optimum。

**图没有证明什么**：示意图不是完整 regret proof，也不说明 AMSGrad 在深网上必胜；证明与经验比较属于不同证据层。

## 八、AI 诊断接口

在真实训练中可记录：逐层/抽样坐标的 $\sqrt{v_t}$、effective coefficient $\eta_t/(\sqrt{v_t}+\epsilon)$、$m_t$、update RMS、clip fraction 与 gradient spikes。若出现“异常梯度后 denominator 很快遗忘、相反方向小梯度累积占优”，才与反例机制相似。

但 telemetry 相关不等于因果；还需固定数据顺序、schedule、decay 和 precision，比较 Adam/AMSGrad 或冻结 denominator 的受控实验。

## 九、本节回顾

- 自适应 denominator 的时间单调性是理论对象，不只是每步非零；
- 三周期线性 loss 给出可手算的 convex nonconvergence；
- AMSGrad 保存历史最大二阶矩，修补“遗忘峰值”机制；
- 保证必须连同问题类和 schedule 书写；
- 下一节 [[Adam 的尺度不变性、Sign 近似与 Update RMS]]审计另一组常见解释。

## 练习与独立解答

- [[习题 - Adam 收敛反例、AMSGrad 与条件化保证]]
- [[解答 - Adam 收敛反例、AMSGrad 与条件化保证]]
- 卷级复现：[[实验 - 自适应优化器状态、尺度与反例数值审计]]
