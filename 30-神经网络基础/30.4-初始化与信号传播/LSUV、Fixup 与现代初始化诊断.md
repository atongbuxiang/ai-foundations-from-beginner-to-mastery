---
type: method
status: draft
area: [neural-networks/initialization, lsuv, fixup, diagnostics]
aliases: [LSUV Initialization, Fixup Initialization, Initialization Diagnostics]
node_id: NN-32
prerequisites: ["[[正交初始化与 Dynamical Isometry]]", "[[偏置、输出层与零初始化的对称性边界]]", "[[Kaiming、He 初始化]]"]
related: ["[[归一化的对象、轴与不变性]]", "[[残差缩放、Lipschitz 界与深度稳定性]]", "[[ReZero、Fixup、DeepNorm 与深网缩放]]"]
sources: ["[[S-2016-Mishkin-Matas-LSUV]]", "[[S-2019-Zhang-Dauphin-Ma-Fixup]]", "[[S-2021-Su-8620-Transformer初始化参数化与标准化]]", "[[S-2021-Su-8978-千层Transformer困难]]", "[[S-2026-PyTorch-NN-Init]]"]
exercises: ["[[习题 - LSUV、Fixup 与现代初始化诊断]]"]
solutions: ["[[解答 - LSUV、Fixup 与现代初始化诊断]]"]
figure: "[[00-知识库管理/_assets/figures/neural-networks/fig-lsuv-fixup-diagnostic-loop-v2.svg]]"
created: 2026-08-23
updated: 2026-08-23
---
# LSUV、Fixup 与现代初始化诊断

> [!abstract] 本章主问题
> Xavier/He 用解析近似预先选择尺度；LSUV 用校准数据逐层测量并修正 activation variance；Fixup 用 residual depth 与 branch length 预先缩小更新尺度。现代初始化不应停在“调用哪个 API”，而应形成一个可证伪闭环：声明计算图与随机对象，选初值，测前向/反向/相关/谱/更新，定位第一处失效，再只修改对应机制。

## 一、从公式选择升级为诊断流程

初始化的目标不是让一张静态直方图“好看”，而是在训练开始附近同时满足若干合同：

$$
\text{forward scale},
\quad
\text{backward scale},
\quad
\text{correlation depth},
\quad
\text{Jacobian spectrum},
\quad
\text{parameter/update ratio}.
$$

这些目标可能冲突。一个合理流程是

$$
\boxed{
\text{theory prior}
\to\text{instrumented dry run}
\to\text{localized correction}
\to\text{multi-seed training test}
}.
$$

LSUV 是 data-dependent localized correction；Fixup 是 architecture-dependent theory prior。

## 二、LSUV 的两阶段算法

LSUV（layer-sequential unit-variance）先对每个 linear/convolution layer 做 orthogonal 或 semi-orthogonal 初始化，然后拿一个 calibration mini-batch，从浅到深逐层校准。

对当前层 $\ell$：

1. 前向计算到该层输出 $H_\ell$；
2. 按声明的 axes 估计

$$
\widehat v_\ell=\operatorname{Var}(H_\ell);
$$

3. 若 $|\widehat v_\ell-1|>\tau$，更新

$$
\boxed{
W_\ell\leftarrow
\frac{W_\ell}{\sqrt{\widehat v_\ell+\varepsilon}}
};
$$

4. 重算，直到进入 tolerance 或达到最大迭代数；
5. 冻结这一层的初始化结果，继续下一层。

权重缩放为何近似有效？若当前局部 activation 工作区近似 homogeneous，$H_\ell$ 随 $W_\ell$ 近似按比例缩放，variance 随比例平方缩放。对于 saturation、bias-dominant、normalization 或复杂分支，这一近似可能不精确，所以算法必须迭代而非一次除法后盲信。

## 三、LSUV 的统计量合同

“输出 variance”至少缺五个下标：

- 在 batch、channel、spatial、token 哪些 axes 上归约？
- 是全层一个 scalar，还是 per-channel？
- 使用 biased 还是 unbiased estimator？
- 模型处于 train 还是 eval mode？Dropout 是否关闭？
- calibration batch 来自真实训练分布、增强后分布还是合成输入？

若一个 layer 含多个 branch/concat，校准输出还是每个 branch 也会改变结果。必须把 axes、batch、mode、seed、tolerance、$\varepsilon$ 和最大迭代数写入复现记录。

## 四、LSUV 不等于 BatchNorm

LSUV 只在初始化时修改 weights；训练过程中不持续重新估计和标准化 batch statistics。它：

- 不保证训练后 variance 继续为 1；
- 不显式把 mean 变成 0；
- 不自动控制 backward variance 或全部 singular values；
- 会把 calibration distribution 的偏差写入初值；
- 不产生 BatchNorm 的 train/eval 双语义。

所以更准确的说法是“一次性、逐层、数据依赖的尺度校准”，不是“无成本 BatchNorm”。

## 五、Residual Addition 改变初始化问题

普通串行层关心乘积；residual network 还包含大量加法：

$$
x_{\ell+1}=x_\ell+F_\ell(x_\ell).
$$

若 branch outputs 近似不相关且每个 variance 都为 $O(1)$，则经过 $L$ 个 blocks，residual stream variance 可能累积到 $O(L)$。即使每个 branch 内部都用 He 初始化，也没有自动补偿跨 block 的求和次数。

## 六、Fixup 的完整初始化规则

设网络有 $L$ 个 residual branches，每个 branch 有 $m$ 个 weight layers。Fixup 的原始规则可整理为：

1. classification layer 与每个 residual branch 的最后一个 weight layer 初始化为 0；
2. 其余 layers 先用标准方法（如 He），并把 residual branch 内的非零 weight layers 额外乘

$$
\boxed{
\alpha=L^{-1/(2m-2)}
};
$$

3. 每个 branch 加一个初始为 1 的 scalar multiplier；在 convolution、linear 与 elementwise activation 前加入初始为 0 的 scalar bias。

这是一整套参数化，不应只抄“末层置零”或只抄 depth exponent。

## 七、Fixup Exponent 的尺度直觉

每个 branch 有 $m-1$ 个非零 weight layers（最后一层为 0）。若每个非零 weight amplitude 都乘 $\alpha$，branch 的链式 amplitude 大致乘

$$
\alpha^{m-1}
=\left(L^{-1/(2m-2)}\right)^{m-1}
=L^{-1/2}.
$$

因此 branch contribution 的平方尺度大致为 $O(1/L)$；$L$ 个近不相关 contributions 累积仍为 $O(1)$。这是 exponent 的第一层直觉。Fixup 原论文更关心训练初期 update 的尺度，而不仅是 forward variance；独立、homogeneous 与标量近似不能替代论文完整论证。

## 八、Zero Last Layer 与学习顺序

初始化时 branch output 为 0，block 从 identity 开始。末层权重能用 branch 内已有 hidden activation 学习；更早层第一步会因末层为 0 而暂时没有 branch gradient，之后随末层离开 0 再获得信号。

这同时解释：

- 为什么它不会像全零串行 MLP 那样切断整网主路径；
- 为什么应记录每个 branch 内不同深度参数的 step-0/step-1 update norm；
- 为什么 zero-last-layer 是一种 staged parameterization，不只是 variance trick。

## 九、LSUV 与 Fixup 的适用边界比较

| 维度 | LSUV | Fixup |
|---|---|---|
| 依赖信息 | calibration data | residual depth/branch length |
| 主要控制 | layer output variance | residual update scale |
| 初始结构 | orthogonal/semi-orthogonal | depth-scaled standard init + zero last |
| 是否一次性 | 是 | 是，但含 learnable scalar/bias |
| 主要风险 | batch/axes/mode 偏差 | recipe 漏项、架构不匹配 |
| 不保证 | backward/full spectrum/训练后稳定 | normalization 的全部优化与统计效应 |

两者可以启发诊断，但不能无条件叠加；LSUV 重新缩放 Fixup branch 可能破坏 depth-aware scale。

## 十、现代初始化的六层仪表盘

### 1. 参数层

记录每层 $\|W\|_F$、spectral estimate、bias、gain 与 dtype；确认 framework layout。

### 2. 前向层

记录 preactivation/activation mean、variance、second moment、zero fraction、quantiles 与 overflow/nonfinite。

### 3. 两输入层

记录 correlation map、相近输入 separation 与 token/spatial covariance。

### 4. 反向层

对固定 loss reduction 记录 activation gradient、parameter gradient 与 JVP/VJP norm。

### 5. 谱层

估计 $s_{\max}$、effective rank、random-direction gain；有条件再估 $s_{\min}$ 与 condition number。

### 6. 更新与系统层

记录

$$
\rho_\ell
=\frac{\|\Delta W_\ell\|}{\|W_\ell\|+\epsilon},
$$

以及 optimizer state、loss scale、AMP overflow、gradient clipping、distributed reduction 与 microbatch accumulation。

## 十一、如何定位“第一处失效”

不要看到最终 gradient 爆炸就统一缩小全网。沿深度定位第一层异常：

- $q$ 先漂移：检查 fan、activation gain、bias、residual addition；
- correlation 先坍缩：检查 $\chi_1$ 与 normalization/branch structure；
- mean-square 正常但 extremes 爆：检查 orthogonality 与 full Jacobian spectrum；
- raw gradient 正常但 update ratio 异常：检查 optimizer、parameter norm 与 learning-rate scaling；
- fp32 正常而 bf16/fp16 异常：检查 accumulation、loss scaling 与 fused kernel。

修正应对应最先失败的机制，并在修正后重跑全套指标。

## 十二、图：LSUV、Fixup 与诊断闭环

先看图回答：LSUV 的 feedback loop 校准的是哪个统计量？Fixup 的 $L^{-1/(2m-2)}$ 如何变成 branch amplitude 的 $L^{-1/2}$？

![[00-知识库管理/_assets/figures/neural-networks/fig-lsuv-fixup-diagnostic-loop-v2.svg|900]]

> [!figure] 图 30.4-08　数据依赖校准、深度依赖缩放与初始化诊断闭环
> 左栏给出 LSUV 的正交预初始化—测量—重缩放迭代；中栏拆解 Fixup residual branch 的 depth exponent、zero-last 与 identity path；右栏把 parameter/forward/correlation/backward/spectrum/update 串成第一处失效定位流程。来源：依据 Mishkin–Matas 2016、Zhang–Dauphin–Ma 2019、PyTorch 初始化文档与科学空间 8620/8978 独立绘制；由 [[00-知识库管理/_labs/code/plot_initialization_advanced_v2.py]] 确定性生成。

**怎样读图**：先问方法使用数据还是架构深度，再核对它直接校准的对象，最后沿右栏逐级决定证据能支持多强的结论。

**图没有证明什么**：图没有证明 LSUV 或 Fixup 在现代架构上普遍优于 normalization，也没有证明一次 dry run 能预测最终性能；它提供的是可复现的初始化诊断合同。

## 十三、最小可执行验收

对一个 plain MLP 与一个 residual MLP，比对 Xavier/He、orthogonal、LSUV、Fixup-compatible 四组。固定 data order、optimizer、learning rate、loss reduction、dtype 与 seed 集合，记录：

1. 初始化前向六个统计量；
2. 随机 JVP/VJP 与谱 extremes；
3. step 0、1、10 的 parameter/update ratio；
4. 多 seed 的早期 loss、nonfinite 与 clipping 次数；
5. calibration batch 改变后的 LSUV sensitivity；
6. 删除 Fixup 三条规则之一的 ablation。

结论必须绑定架构、depth、width、batch、precision 与训练预算。

> [!summary]
> LSUV 用数据逐层修正 activation variance，Fixup 用 residual depth 修正 branch update scale；二者控制的对象不同。现代初始化的可靠范式是“理论先验—仪表化 dry run—定位第一处失效—局部修正—多 seed 训练验证”。

- [[习题 - LSUV、Fixup 与现代初始化诊断]]
- [[解答 - LSUV、Fixup 与现代初始化诊断]]
