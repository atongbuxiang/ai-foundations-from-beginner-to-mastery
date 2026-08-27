---
type: solution
status: verified
area: [training, scaling-laws, emergence]
topic: "[[Broken Scaling、涌现表象与优化架构数据分解]]"
exercise: "[[习题 - Broken Scaling、涌现表象与优化架构数据分解]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Broken Scaling、涌现表象与优化架构数据分解

> [!warning] 使用边界
> kink 是需要解释的观测形状，不自动等于相变；“表象可由指标制造”也不等于所有能力变化都已被否定。

## A. 识别与复述

### TRN55-A01
local exponent 可写 $s(x)=d\log[L(x)-E]/d\log x$，或用滑动窗口估计。全局直线把整个区间压成一个数；$s(x)$ 能显示斜率漂移、平滑过渡、局部 kink 和端点效应，但估计方差更大，须配区间和预注册窗口。

### TRN55-A02
六类来源包括：测量——阈值、离散 exact match、ceiling/floor；统计——小样本零成功、winner's curse；优化——大模型 undertraining/超参失配；数据——mixture、污染或重复阶段改变；架构——宽深、上下文、稀疏机制切换；函数形状——真实 smooth/broken law。还应检查参数计数和系统实现等对象变化。

### TRN55-A03
底层能力可以是连续的 per-step 成功概率或 log-likelihood；benchmark 把它经阈值、乘积、取整和有限样本变成 accuracy；机制突变则声称内部算法/表示发生定性变化。一个陡峭 accuracy 曲线可由前两层变换产生，只有干预与机制测量才能支持第三层。

## B. 手算与构造

### TRN55-B01
exact match 从 $0.7^{10}\approx0.02825$ 升到 $0.8^{10}\approx0.10737$，倍数为
$$
\left(\frac{0.8}{0.7}\right)^{10}\approx3.80.
$$
底层绝对提升仅 0.1，组合指标却近四倍，足以形成“突然出现”的视觉印象。

### TRN55-B02
零成功概率是 $(1-p)^n$。$n=100$ 时 $0.99^{100}\approx0.366$；$n=1000$ 时 $0.99^{1000}\approx4.32\times10^{-5}$。小评测集有超过三分之一概率把真实 1% 能力显示为精确 0。

### TRN55-B03
$x\ll x_b$ 时括号约为 1，故 $L\sim x^{-0.3}$。$x\gg x_b$ 时
$$
(1+(x/x_b)^4)^{-0.1}\sim(x/x_b)^{-0.4},
$$
所以 $L\sim x_b^{0.4}x^{-0.7}$。它是一条光滑过渡而非数学不连续点。

## C. 推导与证明

### TRN55-C01
若 $M=g(p(x))$，
$$
\frac{d\log M}{d\log x}
=\frac{x}{g(p)}g'(p)p'(x).
$$
threshold 附近 $g'$ 可很大或非光滑，使缓慢 $p'$ 变成陡峭指标；ceiling/floor 处 $g'$ 或可见变化趋小，又会把真实改善压平。必须同时画 $p$ 的连续 surrogate。

### TRN55-C02
$\log M=m\log p$，故
$$
\frac{d\log M}{d\log p}=m.
$$
长度 $m$ 越大，per-step 概率的相对小变化被放大 $m$ 倍；不同任务长度甚至会制造不同的“涌现尺度”。

### TRN55-C03
一个饱和分解为
$$
Y=\mu+O_i+A_j+D_k+(OA)_{ij}+(OD)_{ik}+(AD)_{jk}+(OAD)_{ijk}+\varepsilon.
$$
若每次只把一个因素从 baseline 升级，观测到的差异混合了主效应与该 baseline 下的交互；没有交叉组合就无法估计“架构只有配合某优化器才有效”等项。

## D. 边界、反例与纠错

### TRN55-D01
指标幻觉是竞争解释而非全称定理。若连续 surrogate 也在 held-out scales 显示稳健结构转折，样本量排除零计数，训练/数据/架构合同冻结，并且内部表示、因果干预或算法轨迹在同一区间发生可复现改变，才逐步支持机制转变；仍应避免把相关时间点当因果证明。

### TRN55-D02
分段模型参数更多，训练误差自然更低；若 breakpoint 在同一数据上搜索，显著性有选择偏差。应以 complexity penalty/validation 选族，锁定后用更大 held-out scales 比预测误差，并比较 offset power、smooth transition、saturation 等替代族。即使预测胜出，也只支持函数形状，不证明相变机制。

### TRN55-D03
三坐标促使我们检查优化缺口、架构表达与数据支持，适合组织干预。但三者可相互作用、定义随尺度变且难以独立操纵；观测 loss 也含测量与系统项。因此它是解释/实验设计框架，不是保证 gap 精确可加或尾部必然服从某式的定理。

## E. AI 迁移

### TRN55-E01
同时报告 exact match、per-step/token likelihood、partial credit 与校准分数；给每尺度样本量、binomial/bootstrap 区间和零成功概率；预注册 threshold 与 ceiling/floor 处理；对多个任务/断点搜索做 multiplicity 校正；保存所有 seed/失败，并在更大尺度做锁定后的 held-out 检验。

### TRN55-E02
optimizer、architecture、data 各取 baseline/upgrade，形成 8 个 cell，每格同预算多 seed。拟合含三主效应、三两两交互和三阶交互的 factorial model；报告 cell means 与区间。若资源不足，必须删去高阶结论而不是用三个单升级运行冒充完整分解。

### TRN55-E03
稳妥表述：
> 在列明 family 与 benchmark 上，10B 附近离散 accuracy 出现陡升；连续 partial-credit 指标变化更平滑，且当前样本量不能排除阈值/有限样本、优化 gap 或数据混合解释。该结果定位了待检验区间，尚不足以断言内部推理机制突然出现。

## 无提示重做

- [ ] 重算 $p^{10}$ 的放大效应和零成功概率。
- [ ] 为一条 kink 列出至少六个互斥度不同的解释。
