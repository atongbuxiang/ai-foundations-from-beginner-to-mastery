---
type: concept
status: verified
area: [language-models, privacy, membership-inference, unlearning]
node_id: LM-66
aliases: [成员推断与机器遗忘, 数据删除保证]
prerequisites: ["[[Memorization、Exposure、Canary 与训练数据抽取]]"]
related: ["[[数据版本、Provenance、有效 Token 与证据地图]]", "[[语言模型研究协议、Model-Data-System Card 与证据地图]]"]
sources: ["[[S-2017-Shokri-Membership-Inference]]", "[[S-2022-Carlini-LiRA]]", "[[S-2019-Ginart-Data-Deletion]]", "[[S-2020-Guo-Certified-Removal]]", "[[S-2021-Bourtoule-Machine-Unlearning]]"]
exercises: ["[[习题 - Membership、隐私攻击、数据删除与 Unlearning 边界]]"]
solutions: ["[[解答 - Membership、隐私攻击、数据删除与 Unlearning 边界]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-safety-membership-unlearning-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Membership、隐私攻击、数据删除与 Unlearning 边界

> [!abstract] 一句话结论
> Membership inference 是两个数据生成假设间的统计检验，隐私场景应关注低 FPR 下的 TPR；数据删除则要求发布模型接近“从未见过该记录”的参考重训结果，效用保持、字符串不再出现或单个攻击失效都不是充分保证。

## 一、成员事件先定义

令训练算法为随机映射 $\mathcal A(D;\omega)$，目标记录为 $z$。成员推断检验：

$$
H_1:z\in D,\qquad H_0:z\notin D.
$$

必须说明“记录”是单句、文档、用户全部记录还是语义簇；$H_0$ 的 non-member 从哪里抽；训练集大小和其他记录是否相同；攻击者能见权重、logits、loss 还是文本。改变这些项就改变了问题。

攻击 score 可以是目标序列 loss、参考模型标准化 loss 或其他统计量 $S(z,\theta)$。阈值规则

$$
\hat m_\tau=\mathbf1[S\ge\tau]
$$

产生

$$
\operatorname{TPR}(\tau)=\Pr(\hat m=1\mid H_1),\quad
\operatorname{FPR}(\tau)=\Pr(\hat m=1\mid H_0).
$$

## 二、为什么平均准确率会误导

假设现实中成员基率 $\pi=10^{-4}$，攻击在 TPR $=0.5$ 时 FPR $=0.01$。阳性预测的后验精度为

$$
\Pr(H_1\mid \hat m=1)
=\frac{\pi\operatorname{TPR}}
{\pi\operatorname{TPR}+(1-\pi)\operatorname{FPR}}
\approx0.005.
$$

即使 ROC-AUC 看似不错，大多数告警仍可能是假阳性。隐私审计因此常报告固定 $\alpha$ 下

$$
\operatorname{TPR}@\operatorname{FPR}\le\alpha
$$

并给精确二项式或 bootstrap 区间。若要估计 FPR $10^{-4}$，几百个 non-members 明显不足。

## 三、似然比视角

设攻击观察为 $o$，在成员/非成员假设下密度分别为 $p_{\rm in}(o)$、$p_{\rm out}(o)$。Neyman–Pearson 引理说明，在给定 FPR 约束下，似然比

$$
\Lambda(o)=\frac{p_{\rm in}(o)}{p_{\rm out}(o)}
$$

阈值检验最有力。LiRA 类方法用参考训练分布估计两类 score density。这里的难点不是只算一个 loss，而是逼近“若该点进入或不进入训练，随机训练会产生怎样的 score 分布”。

参考模型数量、训练配方不匹配和目标点异常性都会影响估计。攻击弱不能证明隐私强。

## 四、删除、重训与 Unlearning

收到删除集合 $R$ 后，最清晰的参考对象是重新训练：

$$
\theta^- \sim \mathcal A(D\setminus R).
$$

Unlearning 机制 $\mathcal U$ 从原模型和删除请求产生

$$
\tilde\theta=\mathcal U(\mathcal A(D),R).
$$

理想目标不是参数逐位相同，而是 $\tilde\theta$ 的发布分布在声明观察族下接近 $\theta^-$。可抽象为

$$
d\!\left(
\mathcal L(\mathcal U(\mathcal A(D),R)),
\mathcal L(\mathcal A(D\setminus R))
\right)\le\varepsilon,
$$

其中 $d$、随机源、允许观察和失败概率必须定义。若只比较 benchmark accuracy，两个模型可效用相同却隐私行为完全不同。

## 五、三类保证不要混用

1. **exact retraining equivalence**：真正从保留数据按锁定配方重训，仍需证明 lineage 正确；
2. **certified/algorithmic removal**：在特定假设、距离或随机化意义下有界；
3. **empirical unlearning**：用 loss、membership、extraction、forget/retain utility 等测试近似性。

经验测试只能发现违例，通常不能证明所有观察均接近。单个 membership attack 降到随机也可能是攻击失配。

## 六、SISA 与系统成本

SISA 把数据分 shard/slice，分别训练并聚合。删除某记录时只重训受影响分片，降低计算成本。代价包括：

- 更多 checkpoint 与 lineage；
- 分片后单模型数据变少，效用可能变化；
- 聚合改变推理成本；
- 多次删除与自适应请求使缓存/状态复杂；
- 记录跨文档重复时需删除整个等价簇。

它是“为可删除而设计”的系统方案，不是对现成 monolithic LLM 的通用后处理。

## 七、端到端删除协议

1. 身份、授权与记录范围确认；
2. provenance 解析出 raw、派生、dedup cluster、token shard、index、checkpoint；
3. 冻结请求时间与受影响版本；
4. 选择重训、认证移除或经验 unlearning，并写保证；
5. 验证 retain utility、forget behavior、低 FPR membership 与抽取；
6. 轮换缓存、embedding/index、微调 adapter 和下游副本；
7. 发布新版本，撤销旧版本访问，保存不可变审计；
8. 向主体说明完成范围与无法覆盖的副本。

## 八、图解：从假设检验到删除证明

**读图问题**：成员推断的 in/out 分布、低 FPR 尾部与删除后的“重训参考分布”怎样连成同一张隐私验证图？

![[00-知识库管理/_assets/figures/language-models/fig-lm-safety-membership-unlearning-v1.svg|900]]

> [!figure] 图 LM-66　低 FPR 成员推断、重训参照与删除保证
> **生成：**本库用合成高斯 score 与抽象模型分布绘制；不含个人记录或真实攻击目标。

**怎样读图**：左侧在 non-member 尾部固定 FPR 再读 TPR；中间比较原模型、unlearned 模型和从未见过记录的重训分布；右侧把数据、索引、缓存、adapter 与服务副本纳入删除 lineage。

**图没有证明什么**：二维投影接近不等于全分布接近，一个攻击器失效也不等于所有成员信息被消除。

## 九、常见错误与出口标准

错误包括：成员基率未声明；只报 AUC；用 test 调阈值；non-member 分布太容易；数据库删行即称遗忘；忘记 RAG/index/cache；用效用保持证明隐私；用参数距离替代行为保证；旧 checkpoint 仍可访问。

完成后应能写出 $H_0/H_1$、手算 PPV 与 TPR@FPR、解释似然比检验，区分重训/认证/经验遗忘，并设计覆盖所有派生工件的删除协议。

## 十、来源与练习

- [[S-2017-Shokri-Membership-Inference]]；
- [[S-2022-Carlini-LiRA]]；
- [[S-2019-Ginart-Data-Deletion]]；
- [[S-2020-Guo-Certified-Removal]]；
- [[S-2021-Bourtoule-Machine-Unlearning]]；
- [[习题 - Membership、隐私攻击、数据删除与 Unlearning 边界]]；
- [[解答 - Membership、隐私攻击、数据删除与 Unlearning 边界]]。
