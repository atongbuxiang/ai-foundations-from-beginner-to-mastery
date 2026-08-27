---
type: method
status: verified
area: [training, optimization, mup, mutransfer, hyperparameter-search]
node_id: TRN-45
aliases: [μTransfer Protocol, Base Shape Oracle]
prerequisites: ["[[Tensor Programs、坐标检查与无限宽极限]]", "[[训练控制器的联合实验、消融与证据地图]]"]
related: ["[[Embedding、Readout、Attention 与特殊参数组缩放]]", "[[Scale-up 协议、μP 证据与失效边界]]", "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"]
sources: ["[[S-2022-Yang-Tensor-Programs-V-MuTransfer]]", "[[S-2026-Microsoft-MuP-Implementation]]", "[[S-2025-Su-10770-MuP初探]]", "[[S-2025-EssentialAI-Practical-Muon-MuP]]"]
exercises: ["[[习题 - μTransfer、Base Shape 与超参数零样本迁移]]"]
solutions: ["[[解答 - μTransfer、Base Shape 与超参数零样本迁移]]"]
figure: "[[00-知识库管理/_assets/figures/training-optimization/fig-mutransfer-base-delta-target-protocol-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# μTransfer、Base Shape 与超参数零样本迁移

> [!abstract] 一句话结论
> μTransfer 不是“在小模型找到一个 LR，然后原样复制”。它先用 base/delta shape 明确哪些 tensor dimension 随 width 扩展，再用 μP 把各参数组的初始化、multiplier 和学习率翻译到共同 base 坐标；只有在同一模型族、同一训练目标和预注册搜索协议内，小模型的超参数曲线才有资格代理目标模型。

## 一、为什么需要 Base Shape，而不是只知道目标宽度

假设某参数在 base model 中形状为

$$
B=(b_1,\ldots,b_k),
\tag{1}
$$

在 delta model 中为

$$
D=(d_1,\ldots,d_k).
\tag{2}
$$

对第 $j$ 个维度，若 $d_j\ne b_j$，shape oracle 把它标记为待扩展的 infinite dimension；若相同，则标记为 finite dimension。target shape

$$
T=(t_1,\ldots,t_k)
\tag{3}
$$

据此获得 width multiplier

$$
m_j=\frac{t_j}{b_j}
\tag{4}
$$

或由 fan-in/fan-out 聚合得到参数组 multiplier。

### 一个 Transformer 例子

设 base 使用

$$
(d_{model},d_{ff},h,d_h)=(256,1024,4,64),
$$

delta 使用

$$
(512,2048,8,64).
$$

oracle 将 $d_{model},d_{ff},h$ 识别为变化轴，却会把 $d_h=64$ 视为 finite。若真正目标想让 $h$ 固定、$d_h$ 随 $d_{model}$ 增大，这个 delta 设计就错了。base/delta 的任务不是“给两个不同大小模型”，而是用差分编码**哪些抽象维度属于扩展路径**。

> [!warning] Delta 必须激活所有拟扩展轴
> 忘记让 $d_{ff}$、head count、expert width 或 custom projection dimension 在 delta 中变化，会把它误标为 finite；程序仍可能运行，但 LR/init scaling 会悄悄错误。

## 二、Base Model 是坐标锚，不是理论中的无穷小模型

在 base shape 上，μP 实现通常要求模型与原有 standard parameterization 行为兼容；目标宽度的 scaling factor 相对于 base 计算。因此 base width 决定：

- width multiplier 的数值基准；
- 可调初始化常数和 base LR 的语义；
- proxy 搜索所在的有限宽偏差；
- 与旧 checkpoint/recipe 的兼容点。

base 不需要训练，delta 也不需要训练；它们主要提供 shape information。但用于调参的 proxy model 可以等于 base，也可以是同一 base-coordinate family 中更大的模型。

### Base 太小会怎样

即使渐近参数化正确，极窄模型仍可能：

- 表达能力不足，最优 LR 被 underfitting 主导；
- normalization/head dimension 进入离散边界；
- batch/sequence 相对 width 比例极端；
- activation distribution 尚未进入渐近窗口；
- 最优超参数曲线很平或多峰。

所以“越小越省”不是原则。应先用宽度梯确认 proxy 已进入曲线近似稳定区。

## 三、一个可执行的 μTransfer 八步协议

### 步骤 1：冻结 Family Contract

固定 block、depth、norm、residual、attention、tying、tokenizer、objective、optimizer family、dtype 与数据语义。所有允许改变的轴单独列出。

### 步骤 2：设计 Base/Delta Shape

检查每个 parameter name、rank、orientation、finite/infinite dimension；对 custom tensor 手工标注 fan-in/fan-out。

### 步骤 3：设置 μP

在 re-initialization 和 optimizer creation 前设置 base shapes；使用 μP-aware init、readout、optimizer 和 attention convention。

### 步骤 4：先做 Coordinate Check

多 width、多早期 step 检查 activation、gradient、update、feature 和 logit 的趋势；未通过时禁止进入大规模调参。

### 步骤 5：预注册 HP Search

写出候选空间 $\mathcal H$、搜索算法、seed、训练时域、primary metric、失败处理和 checkpoint selection。

### 步骤 6：在 Proxy Ladder 上确认曲线

不只比较一个小模型。至少选择 $n_0<n_1<n_2$，看 validation/training objective 随超参数的整条曲线是否对齐。

### 步骤 7：锁定并复制 Base HP

复制的是 base-coordinate 超参数，如 base LR、init multiplier、momentum/betas 和 schedule shape；每个 target parameter group 仍由 μP 规则翻译为实际 LR/init。

### 步骤 8：目标规模确认

不在 target 上重新大范围调参，但仍执行预注册的短健康检查、失败门和最终训练评估。确认预算必须计入总成本。

## 四、“Zero-shot”究竟零在哪里

严格措辞是：

> 在协议锁定后，不利用目标规模上的超参数搜索结果来选择目标超参数。

它不表示：

- 目标模型不用训练；
- 不看目标训练 loss、NaN 或系统错误；
- 不做目标 checkpoint evaluation；
- 可以在看到目标失败后无限次修改 recipe 却仍称 zero-shot；
- target 结果可以回流到 proxy search 而不记 adaptive budget。

若目标健康检查触发一次预定义 fallback，这可称“有一次确认/救援预算的 transfer”；若反复按目标结果调参，应如实称 telescoping、few-shot 或 target-assisted tuning。

## 五、为什么正确参数化有助于 Argmin 稳定

令 $F_n(h)$ 表示宽度 $n$、base-coordinate hyperparameter $h\in\mathcal H$ 下的期望验证目标。想把 proxy minimizer

$$
h_n^*\in\arg\min_{h\in\mathcal H}F_n(h)
\tag{5}
$$

迁移到大宽度，需要的并不只是每个固定 $h$ 都有极限。

### Pointwise 收敛不够

若对每个 $h$ 有 $F_n(h)\to F_\infty(h)$，但收敛速度依 $h$ 极不均匀，窄而深的局部谷可以随 $n$ 移动，argmin 仍会漂移。

### 一个足够清晰的教学条件

若

$$
\sup_{h\in\mathcal H}
|F_n(h)-F_\infty(h)|\to0,
\tag{6}
$$

且 $F_\infty$ 的最优点 $h^*$ 有 separation：对任意 $\varepsilon>0$，存在 $\gamma_\varepsilon>0$ 使

$$
\inf_{d(h,h^*)\ge\varepsilon}
F_\infty(h)
\ge F_\infty(h^*)+\gamma_\varepsilon,
\tag{7}
$$

则充分大的 $n$ 上，近似 minimizer 会落在 $h^*$ 的 $\varepsilon$ 邻域。

证明骨架很直观：uniform error 小于 $\gamma_\varepsilon/3$ 后，远离 $h^*$ 的点即便吃到最有利误差，也不能击败 $h^*$ 邻域。

> [!important] 实验含义
> μP 的目标是让整条 $F_n(h)$ 曲线在 base coordinates 中趋于共同形状；“几个模型的最佳网格点相同”只是这个更强性质的粗糙有限证据。

若极限目标很平、有多个 minimizer，或 evaluation noise 大于谷底差异，最优点漂移不一定代表参数化失败；应报告 regret 和 near-optimal set，而不只报 argmin。

## 六、哪些超参数更可能迁移

[[S-2022-Yang-Tensor-Programs-V-MuTransfer]] 将其论文协议中的超参数大致分为：

### 1. 参数化/优化相关候选

- base learning rate 与 per-layer multipliers；
- momentum、Adam betas 等 optimizer HP；
- μP-aware initialization variance/multiplier；
- LR schedule shape；
- forward parameter multipliers。

这些也不是无条件迁移，而是 μP 理论/实验主要瞄准的对象。

### 2. 不自动迁移的 regularization

- dropout；
- weight decay 或其他 capacity/data-size dependent penalty；
- label smoothing、augmentation、early stopping 等。

它们常依赖数据量、训练时长、模型容量和评价目标，不应仅靠 width parameterization 宣告稳定。

### 3. 可以实验跨越、但有 caveat 的轴

- depth；
- batch size；
- sequence length；
- training time。

原论文给出若干 Transformer 实验，但这些轴不是 base/delta width oracle 自动解决的同一个理论问题；Post-LN depth 等情形尤其要单独验证。

## 七、曲线对齐比最优点对齐更有信息

对离散网格 $h_1,\ldots,h_K$，保存每个 width、seed 的完整结果 $Y_{n,k,r}$。定义 transfer regret

$$
R(n\leftarrow n_0)
=F_n(h_{n_0}^*)-\min_{h\in\mathcal H}F_n(h).
\tag{8}
$$

还应比较：

- near-optimal set $\{h:F_n(h)\le\min F_n+\tau\}$；
- 曲线 rank correlation；
- 最优区间而非单点；
- 失败率与 NaN/OOM；
- 相同训练/调参/选择/评估预算。

若只在 target 上评估 transferred HP 一个点，就无法计算真实 target regret；此时只能报告绝对结果和 proxy 曲线，不应声称“target nearly optimal”，除非已有独立基线或额外 target sweep。

## 八、实现中的高频事故

| 事故 | 表面现象 | 根因检查 |
|---|---|---|
| delta 漏变 $d_{ff}$ | FFN coord slope 漂移 | infinite dimension 标错 |
| custom weight 方向反 | 某非方阵 LR 异常 | fan-in/fan-out orientation |
| scheduler 绝对覆盖 LR | 第一次 schedule 后失去 μP ratio | refined group LR 被重写 |
| checkpoint 丢 infshape | resume 后曲线突变 | shape metadata 恢复 |
| base/target depth 不同 | 形状可载入但迁移失败 | implementation depth caveat |
| weight tying 未专门处理 | embedding/head 一端失稳 | shared role 冲突 |
| proxy 太小 | optimum 大幅漂移 | finite-width/underfit |
| target 多次救援不计账 | “zero-shot”成本过低 | adaptive tuning 泄漏 |

## 九、Telescoping：承认有限宽误差的实用扩展

[[S-2025-EssentialAI-Practical-Muon-MuP]] 使用多尺度/telescoping 思想吸收有限宽和实现误差。一个诚实版本是：

1. 在 $n_0$ 做宽搜索；
2. 在 $n_1$ 只搜索上一层 near-optimal 邻域；
3. 若 optimum drift 超阈值，暂停 scale-up 并查 telemetry；
4. 逐层缩小搜索范围直到 target；
5. 把每层 trial 和失败计入 tuning budget。

它通常比 target full sweep 省，但不再是严格 one-shot μTransfer。命名和预算应反映真实流程。

## 十、图：Base、Delta、Proxy 与 Target 各自做什么

先看图回答：为什么 base model、delta model、proxy model 和 target model 不是四个同义词？

![[00-知识库管理/_assets/figures/training-optimization/fig-mutransfer-base-delta-target-protocol-v1.svg|880]]

> [!figure] 图 TRN-45　μTransfer 的 Shape Oracle、搜索与确认协议
> 左侧由 base/delta 差异标记 finite/infinite dimensions，中间在多个 proxy width 上完成 coord check 与曲线搜索，右侧只复制 base-coordinate HP 并执行预注册 target 确认。来源：依据 [[S-2022-Yang-Tensor-Programs-V-MuTransfer]] 与 [[S-2026-Microsoft-MuP-Implementation]] 原创绘制。

**怎样读图**：base/delta 负责定义坐标系统，不负责训练；proxy ladder 负责验证有限宽曲线；target 接收经 parameter-group translator 变换后的实际规则，而不是对每个 tensor 复制同一 raw LR。

**图没有证明什么**：协议不能保证 regularization、depth、data、batch、sequence 或新架构自动迁移，也不能把目标规模的反复救援隐藏为 zero-shot。

## 十一、初学者自检

1. base 与 delta shape 怎样判断一个维度是 finite 还是 infinite？
2. 为什么 delta 中忘记改变 $d_{ff}$ 会造成静默错误？
3. “zero-shot”为什么仍允许 target health check？
4. pointwise $F_n(h)\to F_\infty(h)$ 为什么不保证 argmin 稳定？
5. uniform convergence 和 separated minimizer 怎样给出 argmin 稳定？
6. regularization 为什么不属于自动 width transfer 对象？
7. 一次 target sweep 后还能否称严格 zero-shot？

## 十二、本节出口

你应能把 μTransfer 写成

$$
\text{family lock}
\to\text{shape oracle}
\to\text{coord check}
\to\text{proxy curve}
\to\text{base-HP copy}
\to\text{target confirmation}
$$

并对任何“零样本迁移成功”追问搜索空间、argmin separation、target adaptation 和总 tuning budget。
