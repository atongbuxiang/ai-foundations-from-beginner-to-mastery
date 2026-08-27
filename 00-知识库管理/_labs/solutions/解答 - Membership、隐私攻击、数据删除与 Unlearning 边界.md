---
type: solution
status: verified
area: [language-models, privacy, membership-inference, unlearning]
topic: "[[Membership、隐私攻击、数据删除与 Unlearning 边界]]"
exercise: "[[习题 - Membership、隐私攻击、数据删除与 Unlearning 边界]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Membership、隐私攻击、数据删除与 Unlearning 边界

## A. 识别与复述

### LM66-A01
$H_1:z\in D$，$H_0:z\notin D$，同时其余数据和训练随机过程按协议生成。若 $z$ 从一句改为整位用户，成员标签、先验、loss 聚合和隐私含义都改变；重复文档还可能使“删一条”后等价内容仍为成员。

### LM66-A02
TPR 是成员中命中比例，FPR 是非成员中误报比例，AUC 是跨全部阈值的排序摘要，PPV 是被判成员者中真正成员比例。现实成员基率可极低，故即使平均排序不错，稍高 FPR 也产生大量误告；需要 TPR@极低 FPR 及区间。

### LM66-A03
数据库删除只移除存储行；exact retraining 按锁定算法从 $D\setminus R$ 重训；certified removal 在明确假设和距离/随机性意义下给保证；empirical unlearning 用有限攻击、行为与效用 probe 估计接近性，通常不能穷尽观察者。

## B. 手算与构造

### LM66-B01
$$
\mathrm{PPV}=\frac{.001(.6)}{.001(.6)+.999(.01)}
=\frac{.0006}{.01059}\approx .0567.
$$
约 5.7%，说明低基率下 1% FPR 仍太高。

### LM66-B02
FPR $=4/10000=.0004$；TPR $=70/200=.35$。评估集中预测阳性为 $74$ 个，precision $=70/74\approx.946$。此 precision 依评估集成员比例，不能直接外推现实基率。

### LM66-B03
四个绝对差为 $.05,.05,.05,.05$，平均绝对差为 $.05$。这只验证四个 probe 的一维输出，不是全模型分布保证。

## C. 推导与证明

### LM66-C01
由 Bayes：
$$
P(H_1\mid +)=\frac{P(+\mid H_1)P(H_1)}
{P(+\mid H_1)P(H_1)+P(+\mid H_0)P(H_0)}.
$$
代入 $\pi,\mathrm{TPR},\mathrm{FPR},1-\pi$ 即得
$$
\frac{\pi\mathrm{TPR}}{\pi\mathrm{TPR}+(1-\pi)\mathrm{FPR}}.
$$

### LM66-C02
观察 $o$ 在 in/out 下分别有密度。Neyman–Pearson 引理表明在 size/FPR 不超过 $\alpha$ 的检验中，对 $p_{\rm in}(o)/p_{\rm out}(o)$ 设阈值可最大化 power/TPR。因此隐私审计固定可容忍误告率后看似然比尾部，比平均 accuracy 更贴合目标。

### LM66-C03
Accuracy 只约束某有限任务上的一个期望。可构造两模型在所有 benchmark 标签上输出相同类别，故 accuracy 相等；但模型 A 对目标记录给置信 $.99$、模型 B 给 $.51$，或在 benchmark 外前缀下行为不同。于是观察分布和成员泄露可不同。

## D. 边界、反例与纠错

### LM66-D01
AUC=.5 可能来自攻击器选择差、参考分布失配或平均区域抵消，不能给算法级隐私保证；某些个体或低 FPR 尾部仍可能泄露。隐私保证需明确量词和假设，例如训练机制级别界，或至少多攻击族的上界证据。

### LM66-D02
Unlearning 把 exact generation 的安全过滤阈值调高，目标串不再输出；但底层 loss 仍显著低于同分布 non-members，白盒似然比仍能识别成员。输出消失只说明一个接口行为改变。

### LM66-D03
未完成。旧 checkpoint 仍含原训练影响并可访问；缓存可能直接保留派生内容。删除必须覆盖所有可服务版本、备份保留政策、adapter、index/cache 和下游副本，并验证访问撤销。

## E. AI 迁移

### LM66-E01
从目标总体独立抽 in/out，按用户/文档簇分割 train calibration/test；用 calibration 定阈值使 FPR 目标为 $\alpha$，test 只评一次；non-member 数量按目标尾部精度规划；报告精确二项式区间、TPR@FPR、基率敏感 PPV、attack family 和 reference-model 不确定性。

### LM66-E02
列 raw object/许可记录、解析文本、chunk、dedup/语义簇、token shard、训练 manifest、base checkpoint、adapter/merge、量化副本、embedding/index、RAG cache、prompt/output log、评估集副本、部署 registry、备份与下游导出。每项记录 owner、hash、删除动作、验证和保留例外。

### LM66-E03
Full retraining：成本最高、参照最清楚，仍需配方/lineage 正确；SISA：预先分片增加存储/聚合复杂度，以局部重训降成本，保证依设计；近似 unlearning：最快但通常只有有限经验验证。表中还要列 retain/forget utility、低 FPR attack、抽取、失败概率、旧版撤销、时限和法规/主体承诺；决策由所需保证而非只按成本排序。
