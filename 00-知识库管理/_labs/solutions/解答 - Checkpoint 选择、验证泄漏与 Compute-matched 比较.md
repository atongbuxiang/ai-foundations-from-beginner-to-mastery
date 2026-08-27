---
type: solution
status: verified
area: [training, model-selection, benchmarking]
topic: "[[Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"
exercise: "[[习题 - Checkpoint 选择、验证泄漏与 Compute-matched 比较]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Checkpoint 选择、验证泄漏与 Compute-matched 比较

## A. 识别与复述

### TRN71-A01
它们决定产生多少候选、观测噪声怎样平滑、何时停止与最终返回哪个模型；改变任一项都改变从数据到 selected model 的映射。因此应与训练 recipe 一同冻结并计入 compute/selection pressure。

### TRN71-A02
Best validation 用于选择，受选择乐观影响；test at selected checkpoint 在 test 未反馈开发时评估完整 procedure；oracle best test 事后用 test 选候选，只能作诊断上界，不能报泛化性能。

### TRN71-A03
数据/更新：effective tokens、steps、batch、epochs；算术/系统：FLOPs、precision、hardware-time、energy/memory；调参：trials/search/failures/manual work；部署：latency、memory、throughput、quality distribution。主结论需点名分母。

## B. 手算与构造

### TRN71-B01
即使真实 risk 都相同，最小噪声期望为 $0.1(-1.54)=-0.154$，故 best observed risk 约 $R-0.154$，对真实 R 乐观 0.154。checkpoint 相关会改变数值但不取消选择方向。

### TRN71-B02
$T_A=30\times10^9/(120\times10^3)=250000$s；$T_B=200000$s。A 比 B 多 50000s，即晚 25%；B 比 A 快 20%。

### TRN71-B03
成功均值忽略 A 的 1/3 failure 与 B 的 1/12 failure。固定 12 小时可将每 run outcome 定义为是否达标及达标时间；报 12 次成功率、censored time 的 survival/restricted mean，必要时给预注册失败惩罚，保持 launched denominator。

## C. 推导与证明

### TRN71-C01
$\min_k\varepsilon_k\le\varepsilon_1$，所以期望不大于 0；非退化且 $K>1$ 时存在正概率其他噪声严格更小，故严格小于 0。于是 $E[R+\min\varepsilon_k]<R$。

### TRN71-C02
Inner folds 在 outer-train 内选择 HP/procedure；outer held-out fold 评估这个选择过程在未见数据上的性能。Inner best 已被用于选择且训练 fraction 不同，带乐观偏差，不能当外部性能。

### TRN71-C03
若吞吐为 $r$、达标需 tokens $N_{q^*}$，则忽略评估开销 $T=N/r$。A 吞吐更高但若 $N_A/N_B>r_A/r_B$，则 $T_A>T_B$；这给出排序反转条件。

## D. 边界、反例与纠错

### TRN71-D01
global batch、sequence length/padding、accumulation、world size、precision、recompute 和 per-step FLOPs 可不同；100k steps 的 tokens/FLOPs/wall time均不一定相等。还未计 tuning/failure。

### TRN71-D02
任何 test 结果对下一次配置、checkpoint、seed 或是否发布的反馈都进入算法；不经 gradient 也会发生 adaptive overfitting。反复使用后它已是 development set，应另建 locked test。

### TRN71-D03
更快 kernel 可能改变数值和 convergence，或目标质量需更多 tokens；evaluation、compile、input 与 communication 也可能在关键路径。需固定 target quality 的多 run wall-clock。

## E. AI 迁移

### TRN71-E01
冻结最大 tokens、每 N tokens 评估、metric/count、smoothing、min-delta、patience、restore/tie-break；train/dev/test hashes；HP search budget；seeds/failure/censoring；time origin/target crossing；只有冻结后新 runs 可访问 locked test，test 不返回开发细节。

### TRN71-E02
表 1 固定 tokens，列最终 loss、failure、FLOPs/time；表 2 固定 device-hours，列 consumed tokens、quality、failure；表 3 累加所有 search/train/failed/eval device-hours 或成本，列最终 locked-test procedure effect。三表使用相同 launched runs/selection 口径并说明 primary。

### TRN71-E03
用共同、预注册 evaluation grid 对两条已保存 trajectory 重新评估；若 checkpoint 不齐则重跑并统一 cadence/patience/smoothing。最终在新 seeds 上冻结 selection rule，用 locked test 比较；密评估带来的额外成本也入账。
