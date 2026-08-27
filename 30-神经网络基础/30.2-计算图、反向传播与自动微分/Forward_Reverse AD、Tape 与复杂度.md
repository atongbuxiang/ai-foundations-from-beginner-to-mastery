---
type: concept
status: draft
area: [neural-networks/automatic-differentiation, forward-mode, reverse-mode, complexity]
aliases: [Forward Reverse AD, Wengert Tape, AD Complexity]
node_id: NN-15
prerequisites: ["[[局部微分、Jacobian、JVP 与 VJP]]", "[[标量链式法则与反向传播递推]]", "[[自动微分：前向、反向与高阶模式]]"]
related: ["[[Gradient Checking、Checkpointing 与高阶微分边界]]", "[[计算图、拓扑序与前向执行]]", "[[Hessian、二阶微分与曲率]]"]
sources: ["[[S-2018-Baydin-AD-Survey]]", "[[S-2008-Griewank-Walther-Evaluating-Derivatives]]", "[[S-2026-JAX-Autodiff-Checkpointing]]", "[[S-2026-PyTorch-Autograd-Gradcheck]]"]
exercises: ["[[习题 - Forward_Reverse AD、Tape 与复杂度]]"]
solutions: ["[[解答 - Forward_Reverse AD、Tape 与复杂度]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-forward-reverse-ad-tape-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---
# Forward/Reverse AD、Tape 与复杂度

> [!abstract] 本章主问题
> 自动微分不是把函数值近似成导数，而是把已执行程序分解为有局部导数规则的 primitives，再精确应用链式法则到工作精度。forward mode 随 primal 推进 tangent 得 $Jv$；reverse mode 先记录 tape/residuals，再回拉 cotangent 得 $J^Tu$。选择标准是所需方向数、输入/输出维数、内存和程序语义，不是“神经网络一律反向”。

## 一、AD 与两种相似方法

| 方法 | 核心操作 | 主要误差/代价 |
|---|---|---|
| symbolic differentiation | 生成新解析表达式 | expression swell、公共子表达式复制 |
| finite differences | 比较 $f(x\pm hv)$ | truncation + roundoff，是近似 |
| automatic differentiation | 对 primitive 的局部线性作用做组合 | 链式法则精确到工作精度，仍有浮点误差 |

AD 的“精确”不表示无 rounding，也不表示程序所表示的数学目标在该点必然可微。

## 二、Wengert List 与 Tape Entry

把 straight-line program 写成

$$
v_i=\phi_i(v_{p_1},…,v_{p_k}).
$$

一个 reverse-capable tape entry 通常需要：

1. operation/primitive identity；
2. parent value IDs 与 output ID；
3. shape、dtype、device 与 axis metadata；
4. local VJP 所需 residuals，如 primal input/output、mask 或 factorization；
5. alias/version、mode、random state 等语义证据。

tape 不必等于完整 tensor 副本；它可持有引用、压缩 residual，或只保存 checkpoint 以便重算。

## 三、双数解释 Forward Mode

引入 $\varepsilon^2=0$，把一个 primal/tangent pair 写成

$$
x+\dot x\varepsilon.
$$

对光滑 $f$，

$$
f(x+\dot x\varepsilon)
=f(x)+f'(x)\dot x\varepsilon,
$$

因为所有二阶及以上的 $\varepsilon$ 项归零。例如乘法

$$
(a+\dot a\varepsilon)(b+\dot b\varepsilon)
=ab+(\dot a b+a\dot b)\varepsilon
$$

自动产生乘积法则。$\varepsilon$ 不是小的浮点 step，而是幂零代数元。

## 四、Forward Accumulation

对 $f:\mathbb R^n\to\mathbb R^m$，输入 $(x,\dot x)$，forward mode 输出

$$
\left(f(x),J_f(x)\dot x\right).
$$

每个 primitive 按原拓扑序同时计算 primal 与 tangent：

$$
\dot v_i
=\sum_jD_j\phi_i[\dot v_{p_j}].
$$

给 seed $\dot x=e_j$ 得 Jacobian 第 $j$ 列。因此 full Jacobian 通常需约 $n$ 个 forward seeds，但若只要一个 directional derivative，只需一次。

## 五、Reverse Accumulation

reverse mode 分两段：

1. 前向计算 primal，保存或计划重算 residuals；
2. 从 output seed $\bar y=u$ 出发，沿逆拓扑序调用 local VJP，在 fan-out 处累加。

输出是

$$
J_f(x)^Tu.
$$

给 $u=e_i$ 得 Jacobian 第 $i$ 行的转置表示。full Jacobian 通常需约 $m$ 个 reverse seeds；标量 loss 时 $m=1$，seed $1$ 一次即得所有参数梯度。

## 六、完整手算：同一图的两种扫描

令

$$
y=\sin(x_1x_2)+x_1.
$$

定义 $a=x_1x_2$、$b=\sin a$、$y=b+x_1$。在 $(x_1,x_2)=(2,3)$，对 tangent $v=(1,-1)$：

$$
\dot a=3\cdot1+2\cdot(-1)=1,
$$

$$
\dot b=\cos6,\qquad \dot y=\cos6+1.
$$

reverse 以 $\bar y=1$ 开始：

$$
\bar b=1,\qquad \bar x_1{+}=1,
$$

$$
\bar a=\cos6,
$$

$$
\bar x_1=1+3\cos6,
\qquad
\bar x_2=2\cos6.
$$

点积 $\bar x^Tv=cos6+1$ 与 forward JVP 相同。

## 七、成本模型

设 primal program 的算术成本为 $C$，输入/输出维数分别为 $n,m$。在局部 JVP/VJP 均可以常数倍实现的前提下：

| 目标 | 粗略扫描数 | 主要内存 |
|---|---:|---|
| 一个 $Jv$ | 1 forward sweep | primal/tangent live set |
| 一个 $J^Tu$ | 1 forward + 1 reverse sweep | residual/tape 或重算 |
| full $J$ by forward | $n$ seeds | 可逐列或 batch seeds |
| full $J$ by reverse | $m$ seeds | 每次 reverse residuals |

“常数倍”不是任意硬件上的精确比例。vectorized seeds、kernel fusion、sparsity、memory traffic、communication 和 primitive 类型会改变常数。

## 八、为什么 Reverse 用内存换计算

local VJP 常需 forward residual：$\sin$ 需 $\cos x$或 $x$，matmul 需 inputs/weights，normalization 需 statistics。全部保存使 backward 少重算，但 activation memory 可随 depth 增长。丢弃 residual 则要在 reverse 前重放相应 forward。

所以 tape design 是 time–memory tradeoff，不改变理想数学 derivative；但若重放时 RNG、state 或 mutation 不一致，就会改变实际程序。

## 九、三类系统实现

### 9.1 Operator Overloading

Tensor 操作在运行时同时记录 graph/tape。它自然支持本次实际执行的 Python control flow，但 tracing overhead 与 mutation/alias 管理必须处理。

### 9.2 Tracing

用 abstract values 执行一次函数，获得中间表示后再编译/变换。依赖具体数值的 host-language branch 可无法被同一 trace 捕捉，需使用显式 control-flow primitives。

### 9.3 Source Transformation

直接把程序转换为一个计算 primal 和 derivative 的新程序。它可作全局优化，但需对语言的 control flow、state 和 effects 给出精确语义。

## 十、PyTree、结构化输入与 Batched Seeds

真实模型的 parameters 是 dict/list/tree 而不是一个展平向量。JVP 的 tangent tree 必须与 primal tree 同结构；VJP 返回的 cotangent tree 也与输入树同结构。

多个 seed 可以 vectorize，例如用 `vmap` 同时计算 per-example gradients 或 Jacobian 多行/列。这降低 Python overhead 并提高硬件利用，但不改变所需线性方向数的数学量级，也可使 memory 增长。

## 十一、Custom JVP/VJP 是语义承诺

custom rule 可用来：

- 为 fused/foreign primitive 提供 derivative；
- 使用更稳定的数学等价式；
- 通过隐式微分避免 unroll solver；
- 明确定义 surrogate gradient。

但 custom VJP 必须与 forward 函数、shape、dtype、complex convention 和高阶组合一致。“训练能跑”不是 rule 正确的证据。

## 十二、程序语义边界

AD 求导的是已定义程序，所以必须审计：

- data-dependent branch 与 loop；
- random sampling 与 reparameterization；
- integer index、sort、argmax 等离散算子；
- in-place mutation 和 aliases；
- train/eval 与 mutable running state；
- distributed collective 的 reduction scale 和顺序。

框架返回一个数只证明某条 programmed rule 被执行，不自动证明 classical differentiability 或 modeling validity。

## 十三、模式选择决策表

| 任务 | 优先候选 | 原因 |
|---|---|---|
| scalar loss 对亿级参数 | reverse | 一个 output seed |
| 少数参数方向对高维输出 | forward | 少数 input seeds |
| full Jacobian，$n<m$ | forward/jacfwd | 列数更少 |
| full Jacobian，$m<n$ | reverse/jacrev | 行数更少 |
| Hessian–vector product | forward-over-reverse | 先得 gradient program，再推一方向 |
| per-example gradients | batched reverse | 保留 sample axis，避免先 reduction |

最终选择还应用实际 shape、sparsity、compiler 与 hardware benchmark 验证。

## 十四、图：一个程序，两个累积方向

先看图回答：对 $f:\mathbb R^n\to\mathbb R^m$，为什么 full Jacobian 的 forward/reverse 成本分别与 $n/m$ 相关，而 scalar loss 的 reverse 只需一个 seed？

![[00-知识库管理/_assets/figures/neural-networks/fig-forward-reverse-ad-tape-v2.svg|900]]

> [!figure] 图 30.2-07　Primal/tangent 双轨、tape/cotangent 回拉与 $n$/$m$ 成本表
> 左栏用双数和逐 primitive JVP 表示 forward；中栏显示 reverse 的前向 residual tape 与逆向 VJP；右栏将单方向、full Jacobian、memory 与实际系统常数分账。来源：依据 Griewank–Walther、Baydin 等与 JAX/PyTorch 官方文档独立绘制；由 [[00-知识库管理/_labs/code/plot_backprop_advanced_v2.py]] 确定性生成。

**怎样读图**：先确定要的是 $Jv$、$J^Tu$ 还是 full $J$，再计 seed 数，最后把 residual memory、vectorization 和 hardware constants 加回成本合同。

**图没有证明什么**：图没有给出特定框架/硬件的精确倍数，也没有保证任意 control flow、randomness 或 custom rule 在高阶变换下语义正确。

## 十五、验收清单

1. 明确 primal function 的输入/输出树与 shape；
2. 写出目标 derivative action 和 seed 数；
3. 列出每个 local rule 保存的 residual；
4. 对 JVP/VJP 做 dot test；
5. 对小问题用 finite difference 和 full Jacobian 交叉验证；
6. 分开报告 FLOPs、peak memory、latency 和 compilation cost；
7. 重放 control flow/RNG/state，检查与原 forward 一致；
8. custom rule 还要做 higher-order 和 nondifferentiable-boundary 审计。

## 十六、回顾与练习

> [!summary]
> forward mode 计算 $Jv$，reverse mode 计算 $J^Tu$；full Jacobian 的扫描数分别与 input/output dimensions 相关。reverse 的效率来自一个 output seed 共享全部参数路径，代价是 residual tape 或重算。

- [[习题 - Forward_Reverse AD、Tape 与复杂度]]
- [[解答 - Forward_Reverse AD、Tape 与复杂度]]
