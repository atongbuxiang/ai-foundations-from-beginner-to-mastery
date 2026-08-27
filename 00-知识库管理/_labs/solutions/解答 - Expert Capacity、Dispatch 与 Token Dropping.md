---
type: solution
status: draft
area: [architecture, moe, capacity, dispatch]
topic: "[[Expert Capacity、Dispatch 与 Token Dropping]]"
exercise: "[[习题 - Expert Capacity、Dispatch 与 Token Dropping]]"
sources: ["[[S-2021-Fedus-Switch-Transformer]]", "[[S-2022-Zhou-Expert-Choice]]", "[[S-2022-Gale-MegaBlocks]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Expert Capacity、Dispatch 与 Token Dropping

## A. 识别与复述

### ARCH-DISPATCH-A01
$A_{tj}=1$ 表示 token $t$ 分给 expert $j$；$n_j=\sum_tA_{tj}$ 是专家负载。Top-k token-choice 下总 assignment 为 $\sum_{t,j}A_{tj}=Tk$。

### ARCH-DISPATCH-A02
Drop 删除超过容量的 assignment；pad 把专家 batch 补到固定槽位；dropless 保留所有真实 assignment 并用变长/块稀疏执行。Dropless 仍可能有块内 padding 和负载尾部。

### ARCH-DISPATCH-A03
Token-choice 固定每一行和 $\sum_jA_{tj}=k$；expert-choice 固定或限制每一列和 $\sum_tA_{tj}=C_j$。后一种不固定单 token 被选次数。

## B. 手算与建模

### ARCH-DISPATCH-B01
$C=\lceil8/3\rceil=3$。负载 $[4,2,2]$ 时 drop $1$，空槽为 $(3-2)+(3-2)=2$，执行真实 assignment 为 7，总槽 9，利用率 $7/9\approx77.8\%$。

### ARCH-DISPATCH-B02
$Tk/E=24/4=6$，$C=\lceil1.25\cdot6\rceil=8$，总槽 $EC=32$。无 drop 的充要条件是所有专家负载 $n_j\le8$。

### ARCH-DISPATCH-B03
每行和均为 2，所以每 token 激活 2 个专家；每列和也均为 2，负载 $[2,2,2]$；总 assignment 为 6。

## C. 推导与证明

### ARCH-DISPATCH-C01
交换有限求和次序：
$$\sum_jn_j=\sum_j\sum_tA_{tj}=\sum_t\sum_jA_{tj}=\sum_tk=Tk.$$

### ARCH-DISPATCH-C02
固定 $E$ 个专家、每个 $C$ 槽，总槽 $EC$；真正执行且未溢出的 assignment 数为 $\sum_j\min(n_j,C)$，所以 $u=\sum_j\min(n_j,C)/(EC)$。

### ARCH-DISPATCH-C03
列约束只规定每个 expert 选多少 token。取两个专家、各选一个 token，二者都选 token 1，则行和为 $[2,0,\dots]$；已有一个 token 多选、另一个零选，故不保证固定 $k$。

## D. 边界、反例与纠错

### ARCH-DISPATCH-D01
Dropless 只保证真实 assignment 不因 $C$ 被删除。Block kernel 仍需对齐，设备负载仍可偏斜，All-to-All 仍存在，最忙专家仍可能拖慢同步。

### ARCH-DISPATCH-D02
每个 sequence 长 4，expert 0 容量 2，所有 token 都选它。若按位置顺序 pack，位置 1–2 永远保留、3–4 永远 drop；交换 batch/sequence 排列又会改变身份，形成位置偏差。

### ARCH-DISPATCH-D03
被 drop token 可能只走 residual、改去备选 expert 或得到零输出，均改变 $y_t$；expert-choice 还改变每 token 的专家数。因此 capacity/overflow policy 进入 forward function。

## E. AI 迁移

### ARCH-DISPATCH-E01
为 token 赋唯一向量/id，构造跨专家乱序的 assignment，dispatch 后逐 expert 检查内容，再用 inverse permutation 与 gate combine。输出必须逐 token 对齐 reference；同时在重复专家、drop 与空 expert 情形检查梯度 id。

### ARCH-DISPATCH-E02
扫 $\alpha$，固定 Router/checkpoint/硬件，记录 task loss、drop identity/rate、slot utilization、峰值显存、expert GEMM、All-to-All、吞吐和 p95 latency。训练与推理分别测，避免把更高实际 FLOPs 误作纯 kernel 收益。

### ARCH-DISPATCH-E03
控制总参数、平均/最大激活 MAC、capacity/兜底路径、训练 tokens、Router score 与系统布局；报告逐 token 激活数分布、未选 token、负载、质量和吞吐。不能只把列平衡与行 Top-k 当同一算法比较。

