---
type: concept
status: verified
area: [language-models, pretraining-data, deduplication, minhash, lsh]
node_id: LM-19
aliases: [MinHash LSH 去重, Near-duplicate detection, 文档去重]
prerequisites: ["[[解析、语言识别、质量过滤与数据偏差]]", "[[函数、映射、关系与等价类]]"]
related: ["[[Benchmark 污染、时间截止与成员重叠审计]]", "[[数据版本、Provenance、有效 Token 与证据地图]]"]
sources: ["[[S-1997-Broder-Document-Resemblance]]", "[[S-2022-Lee-Deduplicating-LM]]", "[[S-2023-Penedo-RefinedWeb]]"]
exercises: ["[[习题 - 精确去重、MinHash、LSH 与近重复检测]]"]
solutions: ["[[解答 - 精确去重、MinHash、LSH 与近重复检测]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-data-minhash-lsh-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# 精确去重、MinHash、LSH 与近重复检测

> [!abstract] 一句话结论
> 去重不是“比较两个字符串是否一样”一个操作，而是“规范化对象→构造相似度→用概率索引召回候选→精确验证→建重复簇→选择代表”的完整决策管线。MinHash 无偏估计集合 Jaccard，LSH 只控制候选概率；真正删除谁仍由阈值和代表策略决定。

## 一、先定义什么叫重复

至少四种对象：

1. **byte exact**：raw bytes 完全相同；
2. **canonical exact**：解码、Unicode/空白/模板规范化后相同；
3. **substring repeat**：长片段在不同文档中逐字重复；
4. **near duplicate**：局部编辑、广告/页眉变化、重排后仍高度相似。

Canonicalization 越强，召回越高也越可能误合并。例如 lowercase 可合并英语大小写变体，却可能破坏代码；删除数字会把不同年份报告合并。必须保存 raw hash 与 normalized hash，并把 normalization 作为版本化函数 $n_v(d)$。

## 二、Shingle 集与两种相似度

把规范化文档切成连续 $k$-gram shingles 集合 $S(d)$。两个集合 $A,B$ 的 Jaccard resemblance：

$$
J(A,B)=\frac{|A\cap B|}{|A\cup B|}.
$$

Containment 可写为

$$
C(A\subseteq B)=\frac{|A\cap B|}{|A|}.
$$

若一篇 100-token 短文完整复制进 10,000-token 长文，Jaccard 可能很低，但 containment 接近 1。全文近重复与抄入片段需要不同 detector。

### 手算

$A=\{ab,bc,cd,de\}$，$B=\{ab,bc,cd,xy\}$：交集 3、并集 5，故 $J=0.6$；两者等长，containment 也为 $3/4$。图示中两种分母回答不同问题。

> [!warning] Set 与 multiset
> 标准 MinHash 性质针对集合。若同一 shingle 重复 100 次仍只计一次，文档内部 boilerplate frequency 被忽略；若需 weighted Jaccard，应使用相应 weighted sampling，不能把计数直接塞进集合公式。

## 三、MinHash 的核心概率恒等式

对宇宙 $U=A\cup B$ 施加均匀随机排列 $\pi$，定义

$$
h_\pi(A)=\arg\min_{x\in A}\pi(x).
$$

则

$$
\Pr[h_\pi(A)=h_\pi(B)]=J(A,B).
$$

证明：$U$ 中排列最小的元素在每个元素上等可能；两签名相等当且仅当这个最小元素位于 $A\cap B$，概率为 $|A\cap B|/|A\cup B|$。

用 $K$ 个独立排列/哈希，估计量

$$
\widehat J=\frac1K\sum_{k=1}^{K}\mathbf 1\{h_k(A)=h_k(B)\}
$$

满足

$$
\mathbb E[\widehat J]=J,\qquad
\operatorname{Var}(\widehat J)=\frac{J(1-J)}K
$$

（理想独立哈希下）。签名长度控制估计方差，不让候选搜索自动变快。

实际常用有限哈希函数近似随机排列；hash width 太小会引入额外碰撞。Seed、hash family、shingle encoding 与空集合行为都要固定。

## 四、LSH 怎样避免全对比较

$N$ 文档全对比较为 $O(N^2)$。将长度 $K=br$ 的 MinHash signature 分成 $b$ 个 bands，每 band $r$ 行；同 band 全行相等的文档进同桶，只要任一 band 碰撞就成为 candidate。

若真实相似度为 $s$，独立近似下：

$$
P(\text{candidate}\mid s)=1-(1-s^r)^b.
$$

- $r$ 增大使每 band 更严格，减少 candidates 也增加假阴；
- $b$ 增大提供更多命中机会，提高 recall 也增加 candidate load；
- 曲线呈 S 形但不是硬阈值。

例如 $b=20,r=5,s=0.8$ 时候选概率约 $1-(1-0.8^5)^{20}$；同样参数对 $s=0.5$ 仍有非零召回。应以预注册 similarity slice 估计 recall，而非声称“LSH threshold=0.8”。

## 五、候选以后还要做什么

### 1. 精确验证

对 candidate pair 重新计算 exact Jaccard/containment/edit/substring 指标，避免仅因签名/哈希碰撞删除。

### 2. 构图与聚类

把文档作为顶点，验证相似度 $ge\tau$ 的 pair 连边。Connected components 很常见，但相似度关系不具传递性：$A\sim B,B\sim C$ 不保证 $A\sim C$。一个 component 可能经“链式桥接”包含端点相差很大的文档。

可选策略：

- connected components：高召回、易过度合并；
- star/representative matching：每个成员须与中心相似；
- complete-linkage：更严格但昂贵；
- source-aware policy：同站内与跨站阈值不同；
- containment graph：处理长文包含短文。

### 3. 选择代表

留最早抓取、最长、最高质量、最可信来源、许可最清晰或随机一个，会改变时间、域与群体分布。代表策略不是纯存储细节。

## 六、去重怎样改变训练权重

若 cluster $c$ 有大小 $m_c$，未去重的文档均匀抽样使该内容近似获得 $m_c$ 倍 exposure。去重后留一份，相当于把 cluster-level 权重从 $m_c$ 降为 1。

但“重复”也可能是真实频率信息：常见法律模板、代码依赖、新闻转载与语言公式。全部压成一次会改变真实使用频率。可考虑 capped weighting：

$$
w_c=\min(m_c,M)^{\gamma},\qquad 0\le\gamma\le1,
$$

并把它作为 mixture/weighting 目标，而非默认为去重的唯一答案。

## 七、边界与攻击面

- **短文档**：$k$ 大于长度导致空 shingle；很短 boilerplate 易误合并；
- **模板正文**：共同导航推高相似度，需先抽正文或 downweight common shingles；
- **跨语言/改写**：字面 shingles 漏掉翻译和 paraphrase；semantic detector 又可能误合并同题不同答案；
- **代码**：变量重命名、格式化与 vendored dependency 需要语法/仓库级单位；
- **adversarial evasion**：插入字符、零宽符、顺序扰动可逃过字面 detector；
- **split leakage**：应在 train/validation/test 合并候选图上决定边界，再分配，或至少跨 split 专门审计。

## 八、图：估计、索引、验证、删除是四步

先看图回答：若 LSH 没把一对 0.85 Jaccard 文档放进同桶，能否据此断言它们不重复？

![[00-知识库管理/_assets/figures/language-models/fig-lm-data-minhash-lsh-v1.svg|900]]

> [!figure] 图 LM-19　Shingles→MinHash→LSH→Exact verification
> 上方从集合相似度到签名、band candidate 和验证/聚类；下方展示 LSH 候选概率是 S 曲线，不是硬阈值。来源：本课程依据 Broder 与 Lee 等去重方法独立绘制；集合与参数为教学构造。

**怎样读图**：先核对 shingle 对象和 exact Jaccard，再把 signature match 当估计，把 band collision 当候选，最后才进入 deletion policy。

**图没有证明什么**：单个 toy pair 不测真实语料 precision/recall；平滑曲线依赖独立近似，实际哈希、bucket skew 和分布会改变系统表现。

## 九、最小复现实验

1. 对 6 个小集合枚举 exact Jaccard/containment；
2. 枚举小宇宙所有排列，验证 MinHash 相等比例恰为 Jaccard；
3. 固定 seed 重复 $K$ 哈希，检查误差随 $1/\sqrt K$ 缩小；
4. 枚举 band collisions，核对 $1-(1-s^r)^b$；
5. 构造链式 $A\sim B\sim C,A\not\sim C$，比较 clustering policies；
6. 对真实标注 pair 画 recall/candidate-load/false-delete frontier；
7. 变更 representative policy，报告语言、时间、来源和 license slice 的变化；
8. 保存所有 cluster membership 与 removed→kept 映射。

## 十、本节出口

你应能手算 Jaccard/containment，证明 MinHash 恒等式，推导 LSH candidate probability，并解释 cluster/representative policy 如何改变数据分布。下一节[[Benchmark 污染、时间截止与成员重叠审计]]把重复检测用于训练—评测隔离，同时保留其测量边界。

## 练习与独立解答

- [[习题 - 精确去重、MinHash、LSH 与近重复检测]]
- [[解答 - 精确去重、MinHash、LSH 与近重复检测]]
