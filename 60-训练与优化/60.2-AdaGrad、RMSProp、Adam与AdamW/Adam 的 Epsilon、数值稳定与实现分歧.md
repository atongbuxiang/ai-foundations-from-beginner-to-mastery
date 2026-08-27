---
type: derivation
status: verified
area: [training, optimization, adam, numerical-stability]
node_id: TRN-12
aliases: [Adam epsilon, Epsilon Placement]
prerequisites: ["[[Adam 的一阶二阶矩、偏差修正与逐坐标步长]]", "[[浮点数与舍入误差]]", "[[数值稳定性]]"]
related: ["[[FP32、TF32、FP16、BF16 与 FP8 数值合同]]", "[[Loss Scaling、Master Weight 与低精度梯度累积]]", "[[Adam 的尺度不变性、Sign 近似与 Update RMS]]"]
sources: ["[[S-2015-Kingma-Ba-Adam]]", "[[S-2024-Su-10563-Adam-Epsilon-Scaling]]", "[[S-2026-Framework-Adaptive-Optimizer-Semantics]]"]
exercises: ["[[习题 - Adam 的 Epsilon、数值稳定与实现分歧]]"]
solutions: ["[[解答 - Adam 的 Epsilon、数值稳定与实现分歧]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-adam-epsilon-regimes-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Adam 的 Epsilon、数值稳定与实现分歧

> [!abstract] 一句话结论
> Epsilon 同时是除零保护、denominator floor 和小梯度区的算法参数。放在根号外、根号内或 bias-correction 重排式中的数值与单位不同；当 gradient scale、reduction 或 dtype 改变时，epsilon 会打破理想尺度不变性，所以“默认 1e-8”不是可跨实现复制的无害常数。

## 一、三个看似相近的公式

设 $r=\sqrt{\widehat v_t}\ge0$。常见形式至少包括：

### 1.1 根号外

$$
u^{out}=\frac{\widehat m}{r+\epsilon_{out}}.
$$

$\epsilon_{out}$ 与 gradient 同单位。PyTorch 当前 Adam/AdamW 展示公式属于这一类。

### 1.2 根号内

$$
u^{in}=\frac{\widehat m}{\sqrt{\widehat v+\epsilon_{in}}}.
$$

$\epsilon_{in}$ 与 gradient square 同单位。直接把同一个数值 `1e-8` 从外面搬到里面会改变 crossover scale：根号外在 $r\sim10^{-8}$ 介入，根号内在 $r\sim10^{-4}$ 介入。

### 1.3 未修正状态上的代数重排

从根号外公式出发：

$$
\frac{m_t/(1-\beta_1^t)}
{\sqrt{v_t/(1-\beta_2^t)}+\epsilon}
=
\frac{\sqrt{1-\beta_2^t}}{1-\beta_1^t}
\frac{m_t}{\sqrt{v_t}+\epsilon\sqrt{1-\beta_2^t}}.
$$

若实现把 step-size correction 提到外面，epsilon 也必须随 $\sqrt{1-\beta_2^t}$ 重标度，才与原式代数等价。漏掉这一项会真实改变早期更新。

## 二、两条增益曲线并不相同

对固定 numerator，denominator gain 为

$$
h_{out}(r)=\frac1{r+\epsilon},
\qquad
h_{in}(r)=\frac1{\sqrt{r^2+\epsilon^2}}
$$

（为了比较相同 crossover，这里把 inside 项写成 $\epsilon^2$）。二者极限：

| 区域 | 根号外 | 根号内 soft floor |
|---|---|---|
| $r\gg\epsilon$ | $1/r-\epsilon/r^2+\cdots$ | $1/r-\epsilon^2/(2r^3)+\cdots$ |
| $r=\epsilon$ | $1/(2\epsilon)$ | $1/(\sqrt2\epsilon)$ |
| $r\ll\epsilon$ | $1/\epsilon$ | $1/\epsilon$ |

它们有相同的极小/极大 regime，却在过渡区不同。不能只说“都为了稳定，所以等价”。

## 三、epsilon 怎样把 sign 变成线性更新

若暂时令 $\widehat m\approx g$、$\widehat v\approx g^2$：

根号外给出

$$
u^{out}(g)=\frac{g}{|g|+\epsilon};
$$

根号内 soft floor 给出

$$
u^{in}(g)=\frac{g}{\sqrt{g^2+\epsilon^2}}.
$$

两者在 $|g|\gg\epsilon$ 都近似 sign，在 $|g|\ll\epsilon$ 都近似 $g/\epsilon$。因此 epsilon 不只避免除零，还选择小信号区域更像 SGD 的范围。

[[S-2024-Su-10563-Adam-Epsilon-Scaling]]用第二种 soft-sign 做 batch/LR 分析，是有价值的解释模型；但常见框架 exact formula 多为第一种，课程不把两条曲线混写。

## 四、理想尺度不变性在哪里断裂

若所有历史 gradient 乘正数 $c$，则在状态同步缩放时

$$
\widehat m\mapsto c\widehat m,
\qquad
\widehat v\mapsto c^2\widehat v.
$$

epsilon 为零时

$$
\frac{c\widehat m}{\sqrt{c^2\widehat v}}
=\frac{\widehat m}{\sqrt{\widehat v}}.
$$

epsilon 非零时

$$
\frac{c\widehat m}{c\sqrt{\widehat v}+\epsilon}
=\frac{\widehat m}{\sqrt{\widehat v}+\epsilon/c},
$$

所以缩放 gradient 等价于改变相对 epsilon。batch mean/sum、loss scale、单位变换和参数重参数化都可能把坐标推进不同 regime。

## 五、浮点风险要分三层

### 5.1 表示范围

一个小数是否能表示取决于 exponent range；BF16 有较宽 exponent，`1e-8` 并不因“位数少”就必然 underflow。

### 5.2 相加吸收

即使 epsilon 单独可表示，当 $r\gg\epsilon$ 时，有限 mantissa 可能令

$$\operatorname{fl}(r+\epsilon)=r.$$

此时 epsilon 在该坐标不起作用。这是相对间距问题，不是 underflow。

### 5.3 状态与计算 dtype

参数 storage、$m/v$ storage、sqrt/divide compute、reduction accumulator 可能使用不同 dtype。只记录“训练用 BF16”无法判断 epsilon 何处舍入。

> [!warning] 更大 epsilon 也不是免费稳定
> 增大 epsilon 会降低小 denominator 的增益，可能缓解爆炸；同时也把更多坐标推入近线性、小步长 regime，改变优化轨迹和最优 LR。

## 六、具体数值比较

取 $r=10^{-3}$、共同 crossover $\epsilon=10^{-4}$：

$$
h_{out}=\frac1{1.1\times10^{-3}}\approx909.1,
$$

$$
h_{in}=\frac1{\sqrt{10^{-6}+10^{-8}}}\approx995.0.
$$

即使 inside 使用 $\epsilon^2$ 保持单位一致，两者仍相差约 9.4%。若错误地把 `1e-4` 直接放进 $\sqrt{v+\epsilon}$，gain 只有约 99.5，算法已完全不同。

## 七、框架审计清单

根据 [[S-2026-Framework-Adaptive-Optimizer-Semantics]]：

- PyTorch Adam/AdamW：展示公式为 $\sqrt{\widehat v}+\epsilon$；
- PyTorch RMSprop 文档明确其顺序与 TensorFlow RMSProp 不同；
- TensorFlow/Keras Adam 文档称参数对应原论文的 “epsilon hat”，必须按实际公式理解；
- fused/foreach kernel 仍需核对 state dtype、step indexing 和末位舍入；
- checkpoint 跨框架迁移时，除 $m,v,t$ 外还要翻译 epsilon 语义，不能只复制数值。

## 八、图：epsilon 是保护栏，也是 regime 开关

先看图回答：同一个 $r$ 在根号内外两种公式中处在哪个过渡区？gradient 缩放后 crossover 为什么移动？

![[00-知识库管理/_assets/figures/training-optimization/fig-adam-epsilon-regimes-v1.svg|900]]

> [!figure] 图 TRN-12　Epsilon placement、增益曲线与浮点三层风险
> 左侧比较根号外/内曲线；中间用 $|g|/\epsilon$ 标出 sign-like、过渡、linear-like 区；右侧分账 representability、absorption 与 state/compute dtype。来源：依据 [[S-2015-Kingma-Ba-Adam]]、[[S-2024-Su-10563-Adam-Epsilon-Scaling]] 和当前框架文档独立绘制。

**怎样读图**：先确认 epsilon 的单位和位置，再比较相对比值而非绝对数值；最后追踪每个运算所在 dtype。

**图没有证明什么**：图不提供“最佳 epsilon”，也不证明增大 epsilon 必然提升低精度训练；它只把机制和可检查变量列清。

## 九、本节回顾

- epsilon placement 决定单位、crossover 与早期代数重排；
- epsilon 打破非零 gradient scaling 下的理想尺度不变性；
- 表示、相加吸收、state/compute dtype 是三种不同数值问题；
- 科学空间 soft-sign 是解释近似，不冒充框架 exact formula；
- 下一节 [[Adam 收敛反例、AMSGrad 与条件化保证]]说明 denominator 的时间记忆还会产生理论失败。

## 练习与独立解答

- [[习题 - Adam 的 Epsilon、数值稳定与实现分歧]]
- [[解答 - Adam 的 Epsilon、数值稳定与实现分歧]]
- 卷级复现：[[实验 - 自适应优化器状态、尺度与反例数值审计]]
