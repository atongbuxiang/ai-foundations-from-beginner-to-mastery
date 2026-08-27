---
type: solution
status: verified
area: [training, optimization, mup, scale-up, experimentation]
topic: "[[Scale-up 协议、μP 证据与失效边界]]"
exercise: "[[习题 - Scale-up 协议、μP 证据与失效边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Scale-up 协议、μP 证据与失效边界

> [!warning] 使用边界
> “迁移成功”必须绑定模型 family、尺度路径、搜索空间、随机种子、目标指标与容差。没有 target sweep 时可验证绝对结果，却不能无偏知道 target optimum 或精确 transfer regret。

## A. 识别与复述

### TRN48-A01
Shape gate 检查 infshape、orientation 和特殊参数组；Coordinate gate 检查 activation/feature/update 的 width slope；Spectral/Depth gate 检查最坏方向、秩与跨层累积；Training Safety gate 记录 NaN、OOM、饱和、吞吐等事故；Transfer gate 检查曲线、near-optimal overlap、regret 或预注册绝对目标。它们对应“对象有没有接对、典型尺度是否稳定、最坏/深度方向是否稳定、训练能否安全完成、选择是否真正可迁移”，逻辑上互不蕴含。

### TRN48-A02
E0 是假设下的 exponent 手推；E1 是 toy/statistical simulation；E2 是多宽度 coord/spectral 实现检查；E3 是 proxy 超参数曲线；E4 是锁定协议后的 target confirm 与 comparator；E5 是多架构、数据和尺度轴复现。E2 只说明被测遥测没有明显尺度漂移；它没有比较 proxy/target objective curves，也没有观察锁定超参数在 target 的决策损失，因此不能支持零样本迁移成功。

### TRN48-A03
$C_{train}$ 是最终声明模型的训练；$C_{tune}$ 是超参数搜索；$C_{select}$ 是在候选 run/checkpoint 中做选择的额外成本；$C_{eval}$ 是锁定结果的评测；$C_{confirm}$ 是 target health check、确认与 rescue。target health check 和 rescue 都记入 confirm；为选择 checkpoint 额外进行的验证与存储/推理属于 select，而被评估 checkpoint 的最终锁定测试属于 eval。报告时还应说明账户有无共享计算。

## B. 手算与构造

### TRN48-B01
target 最优 loss 是 1.94，proxy 选择的 loss 是 2.10，所以
$$
R(n\leftarrow n_0)=2.10-1.94=0.16.
$$
当 $\tau=0.10$，阈值为 $2.04$，故
$$
\mathcal H_n(0.10)
=\{3\times10^{-4},10^{-3}\}.
$$
$10^{-4}$ 不在其中；按该容差迁移失败。若 loss 有 seed uncertainty，还应对 regret 与集合成员资格给区间或概率。

### TRN48-B02
只在 12 个完成 run 中，成功率为
$$
9/12=75\%.
$$
原配置分母是 20，成功率为
$$
9/20=45\%.
$$
训练安全结论应使用 20 为分母，并把 NaN、OOM、timeout 与人为中止分类报告。75% 只回答“条件于顺利完成后有多少达到指标”，会选择性删除稳定性失败。

### TRN48-B03
$$
C_{tune}^{tel}=40+24+12+4=80\text{ GPU-hours}.
$$
加 target confirm 后至少暴露
$$
80+8=88\text{ GPU-hours}.
$$
最后一级搜索的候选邻域是前三层利用中间尺度信息逐步选出的；只报 4 会把形成该邻域的 76 GPU-hours 和 target confirm 隐去，也会把 telescoping 错称为无需 target 信息的单次迁移。

## C. 推导与证明

### TRN48-C01
第一句错误：若 objective 有宽阔平谷，两个相距很远的 argmin 可拥有几乎相同 loss。例如 $F_n(h)=0$ 对整个区间均成立，任取不同端点作 argmin，drift 很大而 regret 为零。第二句要加条件：若同一 proxy 选择 $h_{n_0}^*$ 满足
$$
R(n\leftarrow n_0)\le\tau,
$$
则按定义 $h_{n_0}^*\in\mathcal H_n(\tau)$；它又属于 proxy 的 $\mathcal H_{n_0}(\tau')$（任意 $\tau'\ge0$），故两集合至少含该点。若比较的是任意两个 near-optimal sets、距离坐标不一致或 regret 与集合使用不同候选域，则结论不成立。

### TRN48-C02
可取 width $\{d,4d\}$ × depth $\{L,4L\}$ × head path $\{\text{fixed }h,\text{fixed }d_h\}$ 的 $2^3=8$ 个 cells，每 cell 用相同的 3—5 个 seeds；seed 是重复单位而非 token/checkpoint。固定数据快照、token budget、aspect、norm/residual family、optimizer semantics、base-coordinate recipe 与评测时刻。估计 width×depth、width×head、depth×head，必要时报告三阶交互；响应包括 coord slope、normalized spectral update、residual/Jacobian、loss 与失败率。若资源不足，不能删除关键 cell 后仍声称估计了对应交互。

### TRN48-C03
决策树：

1. 把 target 的 base-coordinate recipe、数据小样与事故遥测映射回较小模型。
2. 若复现：先查共同的 group/forward multiplier、optimizer reduction、readout/attention rule、scheduler state，再用单组消融定位。
3. 若不复现：先查 target 独有的 depth/aspect/head path、precision/distributed reduction、长时状态、数据顺序和稀有事件，并加入中间尺度。

复现只显示共同因素与事故相关，仍可能有共享混杂；不复现可能来自小模型统计功效不足或未进入同一 regime。因此两条分支都是假说排序工具，不是单独的因果识别。

## D. 边界、反例与纠错

### TRN48-D01
例如在 target 上用 Standard parameterization 扫 100 个学习率，挑出最佳 run，恰好优于一个未调参的 μP baseline。target loss 很好，但不能证明 μP 实现或迁移机制正确。替代解释包括：大搜索预算补偿了错误尺度；模型在有限 width 尚未暴露漂移；数据/seed 偶然有利；baseline 搜索不公平；某层虽错误却被 clipping 或 normalization 掩盖。需要 group audit、coord/spectral 证据与锁定的 proxy-to-target 选择协议。

### TRN48-D02
20 点 target sweep 已使用 target objective 完成超参数选择，所以结果是“target-tuned best-of-grid”，不是零 target tuning 的 μTransfer。应报告完整 target curve、搜索算法、seeds、失败点与 $C_{tune}$，可将结论改为“μP 参数化下的 target 搜索结果”或用它事后估计 proxy choice 的 transfer regret；若此前已有锁定 proxy choice，必须单独保留其 confirm 结果。

### TRN48-D03
取每步 rank-one update
$$
\Delta W=\frac1n\mathbf1\mathbf1^\top.
$$
entry/update RMS 是 $1/n$，可随 width 看似符合坐标账本；对大多数各向同性随机输入，某些平均 RMS 也未必立刻报警。但 $\lVert\Delta W\rVert_2=1$，而相同 entry RMS 的随机符号更新只有典型 $O(n^{-1/2})$ 谱范数。应增加 parameter/update spectral estimate、top singular concentration、effective rank、固定 top-direction probe、数据 covariance 加权增益及多步累计谱漂移。

## E. AI 迁移

### TRN48-E01
最小目录可含：

    scale-up-run/
      manifest/{model,parameterization,data-clock,search-select,budget,environment}.yaml
      configs/{base,delta,target}/
      telemetry/{coordinates,spectra,failures,resources}/
      curves/{all-configs-all-seeds}.csv
      checkpoints/{selection-ledger}.csv
      reports/{claim-card,diagnosis,final}.md

manifest 固定 block/shape path、每组 init/forward/LR/optimizer、数据 snapshot 与 token clock、HP 候选域、seed、last/best/EMA、失败分母、五类成本、代码 commit、依赖/硬件/精度。原始结果保留每个发起 run，包括失败状态；派生图表必须能从这些文件重建。

### TRN48-E02

| 观察 | 首要假说 | 区分实验 | 停止门 | 允许结论 |
|---|---|---|---|---|
| step 1 readout 爆炸；hidden RMS 与 attention entropy 正常 | MuReadout/输出 LR、forward multiplier 或 tying group 错 | 保存 raw grad→optimizer direction→actual update；对照 zero-init readout；核对 $1/d$ effective update 与 tied gradient 两路 | logit/update ratio 超预注册阈值即停止扩容；失败 run 留分母 | 若修正输出组后跨宽度消失，可说“证据定位到 readout group”；不能说整套 μP 已普遍正确 |

还要排查 loss reduction、vocab/sequence scaling、mixed precision overflow 与 resume optimizer state；一次成功 rerun 需由多个 widths/seeds 复核。

### TRN48-E03
E2：
> 在列明的 pre-LN Transformer family、width ladder、固定 depth/head path 和前 $T$ 步内，activation、feature/update 与 spectral telemetry 未见超过阈值的系统 width 漂移。

E3：
> 在同一 family 的三个 proxy widths、预注册 LR/init 网格与 seeds 上，near-optimal 区域重叠且 proxy 间 transfer regret 不超过 $\tau$。

E4：
> 用最小 proxy 的锁定 base-coordinate recipe 在未参与选择的 target width 上确认后，相对预注册 comparator 达到目标，确认预算与失败分母如实计入；结论仅覆盖该数据、架构、尺度路径和训练时钟。

三者逐级加入机制、proxy 决策和 target 证据，但都不外推到未测试的 depth、架构、数据或优化器。

## 无提示重做

- [ ] 48 小时后由一组曲线计算 regret 与 near-optimal overlap。
- [ ] 一周后不看笔记写完整 failure-gate 与预算账户。
