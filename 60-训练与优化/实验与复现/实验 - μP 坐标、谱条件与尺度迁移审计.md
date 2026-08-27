---
type: experiment
status: verified
area: [training, optimization, mup, scale-transfer, reproducibility]
experiment_id: EXP-TRN-606-V1
related: ["[[模型尺度、稳定性指标与 Width-Depth 对象合同]]", "[[Standard、NTK 与 Mean-field 参数化]]", "[[μP 的 Maximal Update 与宽度尺度推导]]", "[[Tensor Programs、坐标检查与无限宽极限]]", "[[μTransfer、Base Shape 与超参数零样本迁移]]", "[[Embedding、Readout、Attention 与特殊参数组缩放]]", "[[谱条件、高阶 μP 与参数更新稳定性]]", "[[Scale-up 协议、μP 证据与失效边界]]"]
script: "[[experiment_mup_scale_transfer_audit_v1.py]]"
results: "[[00-知识库管理/_labs/experiments/trn60.6-mup-scale-transfer-audit-v1/results.json]]"
created: 2026-08-26
updated: 2026-08-26
---

# 实验 - μP 坐标、谱条件与尺度迁移审计

> [!abstract] 实验结论
> Python 标准库实验用 10 条互相分账的轨道、29 项机器断言，验收随机和与相干和、lazy 与 feature-learning regime、μP 指数账、infshape、coord-check 斜率、RMS—谱反例、attention 两阶段缩放、迁移曲线与 regret、width–depth 累积以及 gate/预算账。29/29 断言通过；从另一空目录复跑时，1 JSON、10 CSV、3 SVG 共 14/14 个文件逐字节一致。实验支持定义、量级恒等式和反例，不等价于真实 Transformer 上的 μTransfer 成功证据。

## 一、研究问题与预注册门

| ID | 对象 | 可证伪预期 |
|---|---|---|
| H1 | 随机和/相干和 | $n^{-1/2}$ entry 在独立和下为 1、相干和为 $\sqrt n$；$n^{-1}$ 相干和为 1 |
| H2 | NTK/mean-field regime | 两者功能输出更新可同为 1，但 NTK 相对 feature change 按 $n^{-1/2}$ 消失，mean-field 保持 1 |
| H3 | μP exponent ledger | input、hidden、readout 的 entry update exponent 与聚合 exponent 相消，功能更新 exponent 为 0 |
| H4 | infshape | embedding、hidden、FFN、readout、norm 的有限/无限轴与 forward semantics 能逐组区分 |
| H5 | coord-check | 稳定 hidden slope 为 0，故障 slope 为 $+1/2$；readout 瞬态在后续 step 恢复为 0 |
| H6 | RMS—谱反例 | 相同 entry RMS $1/n$ 下，rank-one 谱范数为 1，scaled Hadamard 为 $n^{-1/2}$ |
| H7 | attention 两阶段 | $1/\sqrt{d_h}$ 保持独立初始化 score RMS，$1/d_h$ 保持相干训练 score；单一因子不同时保持二者 |
| H8 | transfer metrics | 合成 μP 曲线的 base choice 在 target regret $\le.1$；drifting family 的 regret $>.1$ |
| H9 | depth 累积 | aligned 分支用 $1/L$ 稳定，orthogonal 分支用 $1/\sqrt L$ 稳定；aligned 配 $1/\sqrt L$ 仍增长 |
| H10 | failure/budget gate | spectral/depth gate 失败时 target confirm 被阻断；保留预算仍进入总账 |

## 二、环境、命令与 artifacts

- 脚本：[[experiment_mup_scale_transfer_audit_v1.py]]；
- 环境：Python 3.9.6 标准库，无 NumPy、PyTorch、Matplotlib 或网络；
- seed：20260826；本版使用解析式与确定性结构矩阵，seed 作为卷级复现标识；
- 输出目录：`00-知识库管理/_labs/experiments/trn60.6-mup-scale-transfer-audit-v1/`；
- 正式图目录：`00-知识库管理/_assets/plots/training-optimization/`。

运行：

    python3 "00-知识库管理/_labs/code/experiment_mup_scale_transfer_audit_v1.py"

脚本只有在 29 项 checks 全为真时返回退出码 0。用 `--output-dir` 与 `--plot-dir` 指向另一空目录复跑后，JSON、10 CSV 和 3 SVG 共 14/14 个文件逐字节一致。

## 三、关键数值摘要

| 轨道 | 观测 | 证据层级 |
|---|---:|---|
| 随机/相干聚合 | $n^{-1/2}$ 独立和恒为 1；相干和斜率 $+1/2$ | exact scaling identity |
| regime | NTK 相对 feature change 斜率 $-1/2$；mean-field 为 0 | declared analytic model |
| μP ledger | 4 个代表参数组的 feature-update exponent 均为 0 | exponent bookkeeping |
| infshape | 5 类 tensor 的 axis/semantics 被分开 | deterministic shape oracle |
| coord-check | stable $0$；faulty $+.5$；readout 后瞬态 $0$ | exact log–log regression |
| 谱反例 | $n=1024$ 时 $1$ 对 $1/32$，entry RMS 均为 $1/1024$ | exact structured matrices |
| attention | sqrt scaling 初始 RMS 为 1；linear scaling 相干 score 为 1 | exact aggregation |
| target transfer | μP base-choice regret $0$；drifting family 为 $1.7$ | deterministic curve metric |
| depth | aligned×$1/L=1$；orthogonal×$1/\sqrt L=1$ | correlation extremes |
| 证据账 | synthetic spectral gate fail；总预算 110 GPU-hours | declared audit scenario |

## 四、实验图 1：水平 Coord Plot 只回答一层问题

先看图回答：左栏红线为什么足以否定“更新跨宽度稳定”，但绿线又为什么不能单独证明 μTransfer；右栏两条曲线功能输出都可为 $O(1)$，却对应怎样不同的 feature-learning regime？

![[00-知识库管理/_assets/plots/training-optimization/plot-mup-coordinate-regime-audit-v1.svg|900]]

> [!figure] 图 EXP-TRN-606-01　Coordinate slope 与 feature-learning regime
> 左栏比较稳定 hidden update 与故障 $n^{1/2}$ 漂移；右栏比较 NTK 的相对 feature change $n^{-1/2}$ 和 mean-field 的 $O(1)$。来源：[[experiment_mup_scale_transfer_audit_v1.py]] 确定性生成；SVG SHA-256 `14edd934567b3d185551d8d59bbbcbd1d667068f0e5055555bc55f042b88eba3`。

**怎样读图**：所有纵轴值都在相同 width ladder 上作 log–log 比较；水平线表示被测量的 width exponent 为 0。右栏不是 loss，而是单神经元/特征的相对变化。

**图没有证明什么**：coord 水平不保证谱稳定、曲线最优区间重叠、target 性能或训练安全；解析 regime 也没有模拟真实反向传播相关性。

## 五、实验图 2：坐标小不等于谱小，单层稳不等于深度稳

先看图回答：左栏两个矩阵每个坐标同样小，为什么最坏方向相差 $\sqrt n$；右栏同一个 $1/\sqrt L$ 为什么在正交分支下稳定、在同向分支下仍增长？

![[00-知识库管理/_assets/plots/training-optimization/plot-mup-spectral-width-depth-audit-v1.svg|900]]

> [!figure] 图 EXP-TRN-606-02　Entry RMS—spectral gap 与 residual correlation
> 左栏用 rank-one 与 scaled Hadamard 精确构造相同 entry RMS、不同谱范数；右栏用 aligned/orthogonal 两个相关性极端验收 $1/L$ 与 $1/\sqrt L$。来源：同一标准库脚本；SVG SHA-256 `a6ae2040a142f35992451d2aba0eedda620433c876718e6ebad4a1ba7d98c60e`。

**怎样读图**：左栏固定 entry RMS 后只改变符号/秩结构；右栏先固定单分支范数，再把 correlation regime 与 residual multiplier 交叉，而不是把两种深度律混为同一公式。

**图没有证明什么**：Hadamard 与 rank-one 是精确反例，不是真实优化轨迹的谱估计；实际层间更新可能处在两个相关性极端之间，并受到 Jacobian 传播影响。

## 六、实验图 3：迁移要看整条曲线、选择和 Regret

先看图回答：左栏为什么能支持“合成 proxy family 的候选最优点稳定”，右栏又怎样显示相同 base choice 在 target 已有明显决策损失？

![[00-知识库管理/_assets/plots/training-optimization/plot-mutransfer-curve-evidence-audit-v1.svg|900]]

> [!figure] 图 EXP-TRN-606-03　Hyperparameter curve alignment 与 transfer regret
> 两栏使用同一 $\{0.5,1,2,4\}$ 候选网格和 widths；左栏合成 μP family 的 grid optimum 均为 2，右栏 drifting family 在 $n=1024$ 的 optimum 为 4，base-choice regret 为 1.7。来源：同一标准库脚本；SVG SHA-256 `ba7b749fd48b04e427f74b1578c3e03012a097b64ecb18b9e3ded52a5635e8a3`。

**怎样读图**：先固定虚线所示的 base choice，再在每个 width 上读完整 objective curve、grid optimum 和 near-optimal set；不能看到 target 最佳点后倒改 proxy 选择。

**图没有证明什么**：曲线由确定性函数构造，只验收 optimum drift、near-optimal set 与 regret 的计算语义；它不构成真实 μP 的 E3/E4 经验结果。

## 七、十个结果文件

| 文件 | 内容 |
|---|---|
| `accumulation_scaling.csv` | $n^{-1/2}$ 与 $n^{-1}$ 下独立/相干求和 |
| `parameterization_regimes.csv` | NTK lazy 与 mean-field feature change |
| `mup_exponent_ledger.csv` | input/hidden/readout/Adam-like 指数账 |
| `infshape_classification.csv` | base/delta/target shape 与轴分类 |
| `coordinate_checks.csv` | stable、faulty、readout transient 的 slope |
| `spectral_geometry.csv` | rank-one/Hadamard 的 RMS、谱与 effective rank |
| `attention_scaling.csv` | $1/\sqrt{d_h}$、$1/d_h$ 的初始化/对齐阶段 |
| `transfer_curves.csv` | 两个 family 的全曲线、optimum、regret 与 near-optimal 标记 |
| `width_depth.csv` | correlation×depth multiplier 的累计量 |
| `evidence_ledger.csv` | gate 状态、停止规则与 110 GPU-hour 显式预算 |

`results.json` 汇总 29 项 checks、artifact manifest 和四条证据边界。

> [!warning] 复现边界
> 本实验是定义验收与反例实验，不是神经网络性能实验。进入真实框架后还需逐组 actual LR/init/forward multiplier、mixed precision、distributed reduction、真实 activation/feature/logit、power-iteration/SVD 对照、失败分母、多 seed 曲线、target 锁定确认与总预算。

## 八、回链与继续实验

- scale object 与 regime：[[模型尺度、稳定性指标与 Width-Depth 对象合同]]、[[Standard、NTK 与 Mean-field 参数化]]；
- exponent 与程序极限：[[μP 的 Maximal Update 与宽度尺度推导]]、[[Tensor Programs、坐标检查与无限宽极限]]；
- 迁移与特殊参数组：[[μTransfer、Base Shape 与超参数零样本迁移]]、[[Embedding、Readout、Attention 与特殊参数组缩放]]；
- operator/depth 与证据：[[谱条件、高阶 μP 与参数更新稳定性]]、[[Scale-up 协议、μP 证据与失效边界]]。

学习者至少完成一次干预：把相干更新改成部分相关；给 coord signal 加有限宽修正；改变 attention 对齐强度；把迁移谷底改成宽平谷；或在 evidence ledger 中制造 coordinate pass、spectral fail。运行前先写定量预测，运行后分别说明改变的是 exponent、finite-width correction、correlation、decision metric 还是 claim scope。
