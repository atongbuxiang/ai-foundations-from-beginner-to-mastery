---
type: solution
status: draft
area: [architecture, moe, gating, evidence]
topic: "[[MoE 门控归一化、证据地图与开放问题]]"
exercise: "[[习题 - MoE 门控归一化、证据地图与开放问题]]"
sources: ["[[S-2021-Roller-Hash-Layers]]", "[[S-2026-Su-11750-Hash-Routing-tid2eid]]", "[[S-2026-Su-11782-MoE门控归一化]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - MoE 门控归一化、证据地图与开放问题

## A. 识别与复述

### ARCH-GATE-A01
Softmax scores 正且总和为 1，位于 simplex，一个 logit 通过分母影响所有专家；Sigmoid 各分量独立位于 $(0,1)$，总和自由。Top-k/Re-Norm 可在之后重新引入竞争。

### ARCH-GATE-A02
I：定义可直接复算的恒等/账本；T：在显式假设下证明；E：固定协议测量；H：可证伪的机制解释；O：尚无充分答案的问题。强结论必须有相应或更强证据，不能由 H 伪装成 T。

### ARCH-GATE-A03
Hash 消除 learned Router 参数、score 计算和其训练不稳，并可离线平衡；代价是上下文适应性下降，相同 token 常固定去同一专家，且频率长尾可造成不可避免的负载下界。

## B. 手算与建模

### ARCH-GATE-B01
Softmax 为 $[e/(e+1),1/(e+1)]\approx[.7311,.2689]$，和为 1。Sigmoid 为 $[.7311,.5]$，和约 1.2311；第一项相同是二分类代数巧合，语义仍不同。

### ARCH-GATE-B02
若 $a$ 最大且被选，Re-Norm 权重为 $a/a=1$，对 $a$ 的普通导数为 0；未选分量在 index 固定邻域也无 mixture-weight 梯度。边界处 hard selection 不可微。

### ARCH-GATE-B03
完美均衡目标为每 expert 100 个 token occurrence。高频 token 的 180 次必须全部去同一 expert，所以该 expert 负载至少 180，严格大于 100；最大负载下界为 180。

## C. 推导与证明

### ARCH-GATE-C01
严格递增 $g$ 满足 $z_i>z_j\iff g(z_i)>g(z_j)$，因此完整排序不变，无 tie 时前 $k$ index 集相同。非严格单调或量化可制造 tie，结论失效。

### ARCH-GATE-C02
Softmax 求导得 $\partial a_i/\partial z_j=a_i(\delta_{ij}-a_j)$，含非对角项，专家竞争耦合。Sigmoid 为 $\partial a_i/\partial z_j=\delta_{ij}a_i(1-a_i)$，Jacobian 对角。

### ARCH-GATE-C03
$k=E$ 时 selection 不删项，softmax 后 Re-Norm 恒等；$k=1$ 时任意正 score 除以自身成为 1，gate amplitude 与普通权重路径梯度消失。

## D. 边界、反例与纠错

### ARCH-GATE-D01
改写为：“在控制总参数/激活计算后，若 shared path 被干预会跨 token 类型普遍提高 loss，而 routed expert 干预呈类别选择性，并在多 seed/层稳定，则支持 shared 承载更通用表示。”这给出了可观测与可能证伪结果。

### ARCH-GATE-D02
整体系同时改变多个组件、训练数据、规模和系统，输出只有联合效应。没有单组件 matched-budget 消融、外部复现和统计不确定性，无法识别个别组件的因果增益。

### ARCH-GATE-D03
对 $z=[2,1,-1]$，全局 softmax Top-2 不 Re-Norm 与选中后 Re-Norm index 都为 $\{1,2\}$；专家输出 $[4,-1]$ 时结果约 2.562 与 2.655，故 selection 相同而模型输出不同。

## E. AI 迁移

### ARCH-GATE-E01
先把“更优”拆成 selection/gradient/quality/system 指标；I 级验证公式与 Top-1 边界，T 级列出任何近似假设，E 级要求多 seed matched-contract 消融，H 级保存机制解释，O 级限定跨规模外推。若只给单一整模型结果，结论最多是协议内 E。

### ARCH-GATE-E02
固定专家、总/激活参数、capacity、训练 tokens 和系统；learned Router 与按训练频率构造的 hash 对比，并含随机 hash。报告 quality、负载、长尾 token 下界、通信、Router cost、上下文敏感任务和 OOD 漂移。

### ARCH-GATE-E03
示例选“动态预算给谁”：小模型离线枚举每 token 的 $k$ 得到边际 loss 改善；训练 controller 预测改善，在固定总 assignment 下与 entropy/loss/random/fixed-$k$ 比较。预注册指标为 budget-normalized loss、regret、load tail、吞吐与跨分布泛化，并把机制解释保留为 H。

