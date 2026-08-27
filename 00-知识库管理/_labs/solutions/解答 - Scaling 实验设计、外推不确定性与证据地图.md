---
type: solution
status: verified
area: [training, scaling-laws, experimental-design]
topic: "[[Scaling 实验设计、外推不确定性与证据地图]]"
exercise: "[[习题 - Scaling 实验设计、外推不确定性与证据地图]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Scaling 实验设计、外推不确定性与证据地图

> [!warning] 使用边界
> 误差条不能弥补泄漏的尺度切分；held-out scales 若被反复查看并调模，也已变成 validation。

## A. 识别与复述

### TRN56-A01
至少写明 response/loss、resource axis、model/data family、尺度区间与外推 horizon、训练/调参协议、候选函数族、误差与失败模型、允许误差/覆盖门及否证条件。“更大通常更好”没有可测斜率、范围、概率量词或失败阈值，任何结果都可事后解释，故不可证伪。

### TRN56-A02
训练随机性来自 seed、batch 顺序和数值非确定；测量不确定性来自有限 validation 样本；参数不确定性是在给定函数族下估计 $(E,A,\alpha)$ 的有限样本波动；结构不确定性来自 power/offset/broken 等族本身不确定。扩大 eval set 只减少第二层，不能消除其余三层。

### TRN56-A03
failure denominator 是所有预注册、被尝试运行的总数，以及各失败类型数量。删除 OOM/divergence/未达阈值会留下“易成功”的条件样本，使 loss 偏乐观；重跑和搜索成本被漏计；大尺度更易失败时还会扭曲 slope 与稳定性。

## B. 手算与构造

### TRN56-B01
一种严格切分是 calibration $\{1,2,4,8\}$，validation $\{16,32\}$，held-out $\{64,128\}$。不能把 64/128 的 checkpoint 随机分回训练；只有按整个 scale block 隔离，最终测试才测区间外预测。

### TRN56-B02
success-only 均值为 2.0。按预注册失败惩罚，intention-to-run 均值为
$$
\frac{24\times2+6\times5}{30}=\frac{78}{30}=2.6.
$$
两者回答不同 estimand，应并列报告而非静默删除失败。

### TRN56-B03
decision regret 为 $1.90-1.84=0.06$。基线后悔为 $2.00-1.84=0.16$，A 消除 $0.10$，比例为 $0.10/0.16=62.5\%$。预测误差小不必然决策 regret 小，反之亦然。

## C. 推导与证明

### TRN56-C01
每次 bootstrap 先重采样 scale cells（保留外推设计单位），再在被选 cell 内重采样独立 seed；若使用轨迹，则以整条 checkpoint 序列或预注册时间块重采样，而非逐点打散。相邻 checkpoint 共享参数历史和数据，强相关；当成 iid 会把有效样本量从“运行数”虚增为“日志点数”，区间过窄。

### TRN56-C02
同一尺度的训练/测试 checkpoint 共享 $N,D$、训练运行和函数族的局部位置，测试只测时间轨迹内插或相邻噪声。跨尺度外推要面对未见 $x$、斜率漂移和结构失配；这些在随机 checkpoint split 中完全没有被留出。因此该误差对目标 estimand 不一致，即使数值很小也无关。

### TRN56-C03
先用 calibration scales 拟合三个族及其预注册约束；以 complexity-aware score 和 validation-scale 预测选择/平均模型；然后冻结族、超参、offset 边界和区间算法，只在 held-out larger scales 评分一次。若看最终结果后切换到 broken law，测试信息已进入选择过程，需再收集更大新尺度或把结论降级为探索性。

## D. 边界、反例与纠错

### TRN56-D01
1000 checkpoints 若来自少数训练运行，是强相关纵向测量；独立规模单元和 seed 才决定 scaling 曲面可辨识度。把 checkpoint 当 1000 个独立样本会伪造自由度和窄置信区间。应报告 scale cells × seeds × trajectories 的层次结构和有效独立单元。

### TRN56-D02
divergence 常随尺度、超参或系统变化，不是随机缺失。删除它等于把研究问题改成“条件于训练成功时的性能”，同时漏掉失败耗费。正确做法是分类原因、保留计划分母，报告 conditional 与 intention-to-run 两套结果，并按预注册 censoring/penalty 处理。

### TRN56-D03
bootstrap 通常条件于所选函数族，因而只反映该族内采样波动。比如带 offset 幂律与 smooth broken power law 可在 $[1,100]$ 几乎重合，却在 $10^6$ 一个饱和、一个改变指数。需做函数族比较、model averaging 或跨族 envelope 才覆盖结构不确定性。

## E. AI 迁移

### TRN56-E01
清单包括：可证伪 claim 与 target horizon；$N,D,C,T$ 对象合同；crossed grid/scale split；每 cell seed；总预算与运行停止；locked/per-scale tuning 及搜索成本；checkpoint/eval cadence；失败分类和惩罚；候选族/先验/约束；误差模型与 bootstrap block；multiplicity；最终门与何时允许重开分析。

### TRN56-E02
每 scale cell 一行：配置、实际 $N,D,C,T$、seed 数、成功/失败、loss 点估计与训练/评测区间、wall time/energy；模型表给族、参数、validation score；held-out 表给逐尺度误差、区间覆盖和最坏误差；决策表给推荐配置、真实最佳、regret、近优集与预算偏差。原始 manifest 和机器可读结果随附。

### TRN56-E03
“曲线内插良好”最多是 E2：观测窗口内多 seed 描述良好。“未见规模外失效”需 E3，且只说在锁定 family/path 的已测 held-out scales 外推通过；若还跨数据/架构复现可到 E4。“可指导十倍预算决策”只有执行预注册决策试验并达到 regret/cost 门后才是 E5；单凭拟合不能这样表述。

## 无提示重做

- [ ] 为八个尺度重新设计无泄漏三段切分。
- [ ] 从失败分母与结构不确定性各审计一条真实 claim。
