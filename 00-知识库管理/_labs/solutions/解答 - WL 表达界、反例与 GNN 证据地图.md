---
type: solution
status: draft
area: [architecture, graph-neural-networks, expressivity, evidence]
topic: "[[WL 表达界、反例与 GNN 证据地图]]"
exercise: "[[习题 - WL 表达界、反例与 GNN 证据地图]]"
sources: ["[[S-2019-Xu-GIN]]", "[[S-2019-Morris-HigherOrder-WL]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - WL 表达界、反例与 GNN 证据地图

## A. 识别与复述

### ARCH-WL-A01
$c_v^{t+1}=\mathrm{HASH}(c_v^t,\{\!\{c_u^t:u\in N(v)\}\!\})$。HASH 在本轮所有出现的 pair 上应 injective，两图比较用同一映射；颜色名字无语义，只保留相等关系。

### ARCH-WL-A02
若某轮 color histogram 不同，两图必非同构，因为同构会保留邻域签名。若一直相同，只能说 1-WL 未区分，不能推出同构。

### ARCH-WL-A03
上界说标准 invariant-neighborhood MPNN 不能分开 1-WL 未分开的结构；达到说在 injective aggregation/update/readout 等条件下，GIN 不会比 1-WL 额外丢失。许多实际 MPNN 更弱，GIN 也不超过 1-WL。

## B. 手算与建模

### ARCH-WL-B01
初始全为 $a$。第一轮端点签名 $(a,\{a\})$，中心 $(a,\{a,a\})$，得颜色 $b,c$。第二轮端点签名 $(b,\{c\})$ 相同，中心 $(c,\{b,b\})$；仍为两端同类、中心一类。

### ARCH-WL-B02
两图每个节点初始 $a$ 且 degree 2，第一轮签名都为 $(a,\{a,a\})$，全成 $b$；第二轮都为 $(b,\{b,b\})$，全成 $c$。两图各有 6 个同色节点，histogram 相同。

### ARCH-WL-B03
不改变，因为两图所有节点 degree 都是 2，加入 degree 后初始颜色仍统一。需要能反映连通分量或更高阶结构的额外信息才会分开，而这改变输入/算法。

## C. 推导与证明

### ARCH-WL-C01
基步：相同初始 color 映到相同 $h^0$。归纳假设 WL 同色节点有同表示；下一轮同色意味着自身旧色相同、邻居旧色多重集相同，因此对应消息多重集相同。Invariant AGG 与共享 update 给相同新表示。

### ARCH-WL-C02
Injective aggregation 唯一编码邻居 multiset，injective update 联合自身与邻域摘要，故每轮表示等价于 WL 新颜色；injective graph readout 唯一编码最终节点颜色/表示 multiset，从而只要 WL histogram 不同就输出可区分。

### ARCH-WL-C03
有序 k-tuple 数为 $n^k$；即使只取不同节点也是 $n(n-1)\cdots(n-k+1)=O(n^k)$。为每个 tuple 保存宽 $d$ 状态需 $O(n^kd)$ memory，tuple 邻接更新还会增加时间，所以表达提升有显著资源代价。

## D. 边界、反例与纠错

### ARCH-WL-D01
$C_6$ 与 $C_3\sqcup C_3$ 非同构（连通分量数不同），但统一标签下 1-WL 永远全同色。未区分是算法信息不足，不是同构证书。

### ARCH-WL-D02
更强类包含更多函数，也带来更大容量/成本；有限数据可能过拟合，优化未找到所需参数，任务可能只需简单局部统计。Generalization 与表达存在性之间还需数据和学习算法假设。

### ARCH-WL-D03
Unique ID 让原本对称节点初始可区分，改变了“只给结构/标签”的问题；若 ID 任意且新图重新编号，模型可能记住编号模式，破坏重标号不变或跨图迁移。随机 ID 还引入方差，需分布不变处理。

## E. AI 迁移

### ARCH-WL-E01
WL-easy：degree sequence 不同、路径与星形等；WL-hard：同阶同度的 $C_6$ vs 两三角形及更多 regular pairs。统一 node feature，控制 size/degree；直接运行 1-WL 给标签，再测模型能否区分，多 seed 且不泄漏 graph ID。

### ARCH-WL-E02
理论：精确定义模型类、初始 features、invariance、WL 阶数、图类、injectivity/precision 和证明方向；实验：含已知 hard pairs、控制 size/degree、检查 permutation、对比 1-WL/k-WL、报告参数与 $n$ 扩展成本、训练成功率。仅 benchmark SOTA 不足。

### ARCH-WL-E03
表达：能否分开规定 graph pairs；优化：训练是否稳定达到；泛化：同分布/OOD size/time；鲁棒：边/特征扰动；效率：参数/FLOP/memory/latency；构图：metric/$k$/hubness/split。每条分别指定定理、合成测试或受控实验，不用一个 accuracy 代替六条。

