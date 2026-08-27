---
type: solution
status: verified
area: [training, scaling-laws, data]
topic: "[[数据质量、重复、混合与有效 Token]]"
exercise: "[[习题 - 数据质量、重复、混合与有效 Token]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - 数据质量、重复、混合与有效 Token

> [!warning] 使用边界
> effective token 是绑定模型、顺序、重复次数与目标评测的代理量，不是语料自带、可跨研究直接相加的物理属性。

## A. 识别与复述

### TRN53-A01
raw tokens 是管线输入的总切分数；unique tokens 是按声明去重单元后首次内容量；seen tokens 是训练过程实际消费量，重复也逐次计入；repetition count 描述同一内容被看到几次；effective tokens 用一个反事实新数据量表示实际数据带来的等效学习价值。前四者可由日志/去重规则直接计数，$D_{eff}$ 通常是模型化或实验反推的潜变量。

### TRN53-A02
质量涉及噪声、事实性和语言结构；多样性涉及支持集覆盖；目标相关性取决于部署分布；污染是训练与评测的不当重合。一个数据源可高质量却窄覆盖、与目标无关或已污染；同一数据对不同目标价值也不同。因此必须报告向量化属性和目标条件，而非无上下文标量。

### TRN53-A03
$w_j\ge0$ 且 $\sum_jw_j=1$，表示训练 token 预算在 $K$ 个域间分配。$\ell_i(w)$ 是用混合 $w$ 训练后在目标域 $i$ 的 loss；它不是第 $i$ 个训练域的占比。向量保留“一个混合改善哪些域、伤害哪些域”，目标权重再决定如何聚合。

## B. 手算与构造

### TRN53-B01
$$
D_{eff}=100\sum_{j=0}^{4}0.6^j
=100\frac{1-0.6^5}{1-0.6}
=230.56\text{B}.
$$
seen tokens 是 500B，但在该代理模型中只相当于 230.56B 全新 token；结果完全依赖 $q=0.6$ 假设。

### TRN53-B02
第一目标的聚合 loss 为
$$
0.5(2.0)+0.3(1.5)+0.2(3.0)=2.05.
$$
第二目标为 $0.1(2.0)+0.2(1.5)+0.7(3.0)=2.60$。同一域损失向量因部署目标权重不同而有不同效用；比较 mixture 时必须先冻结 $v$。

### TRN53-B03
token 粒度不同，每-token cross-entropy 的预测事件不同；序列长度和 token 数也被重新标度。应在同一原始文本上比较总负对数似然，并归一为 nats/byte、bits/byte、nats/character，或用可比的下游任务/压缩单位；还须检查 tokenizer 是否有不同的字节覆盖和特殊 token。

## C. 推导与证明

### TRN53-C01
若每一轮的等效贡献为 $Uq^{j}$，$j=0,\ldots,r-1$，则几何级数给
$$
D_{eff}=U\sum_{j=0}^{r-1}q^j=U\frac{1-q^r}{1-q}.
$$
当 $0\le q<1$ 且 $r\to\infty$，上限为 $U/(1-q)$；它表达边际递减，而非宣称真实训练一定饱和于该数。

### TRN53-C02
$M_{ii}$ 是增加训练域 $i$ 权重对自身评测 loss 的局部作用；$M_{ij},i\ne j$ 是跨域迁移或干扰。总目标只观测 $v^TM$ 的某个方向投影；不同矩阵可以有相同加权和，所以单一总 loss 无法恢复各元素，需独立扰动多个 $w_j$ 并逐域评测。

### TRN53-C03
内部点的可行扰动满足 $\mathbf1^T\delta w=0$。一阶最优要求
$$
\nabla J(w)^T\delta w=0\quad\text{对所有可行 }\delta w,
$$
等价于 $\partial J/\partial w_j=\lambda$ 对所有 $j$。这是各训练域的边际收益相等，不是 $\ell_i(w)$ 的水平相等；域本身难度可完全不同。

## D. 边界、反例与纠错

### TRN53-D01
“约四轮”来自特定数据、去重、模型、目标和预算区间的经验结果。高质量教材、低熵模板、噪声网页、代码和长尾数据的重复价值不同；顺序、augmentation、模型容量和目标也会改变边际收益。可迁移的是“显式测 repetition curve”，不是一个普遍 hard cap。

### TRN53-D02
目标权重取 $(0.9,0.1)$。基线域 loss $(2,2)$ 的总 loss 为 2；新混合得到 $(1.7,4)$，总 loss 为 $1.93$，表面改善，但关键小域从 2 恶化到 4。必须报告域向量、worst-domain/约束指标，不能只报加权平均。

### TRN53-D03
高去重率可能删的是网页镜像等无价值冗余，也可能删掉对罕见模式有稳定作用的重复；unique 少不等于语义覆盖小，相似文本也可能携带不同上下文。重复既可能浪费预算，也可能强化知识或降低估计方差。效果需用目标 loss、memorization 与覆盖实验判定。

## E. AI 迁移

### TRN53-E01
至少记录 source/licence/version、抓取时间、语言/域、raw bytes、tokenizer hash、raw/unique/seen tokens、文档与 span 去重阈值、重复直方图、过滤规则与留存率、mixture 权重/采样温度、epoch/顺序、污染检查、PII/安全过滤、逐域 validation 和 provenance lineage。

### TRN53-E02
固定模型、tokenizer、seen tokens、model FLOPs、optimizer schedule 与 seed block，在基准 $w_0$ 周围对每个域做正负小扰动，同时从另一域补偿以保持 simplex。逐域评估 $\ell_i$，用成对差分估 $M_{ij}$；随机化数据顺序并多 seed，报告非线性检查，避免把总 token 或训练时间变化当 mixture 效果。

### TRN53-E03
先固定评测集版本与时间戳；对训练语料做规范化 exact hash、局部/MinHash near-duplicate、模板/答案模式匹配和语义检索，分别报覆盖率与阈值。区分预训练前泄漏、后续微调泄漏和开发者反复看测试集造成的自适应复用；对可疑样本做去除重训或干净替代集验证，不把“未检出”表述成“绝无污染”。

## 无提示重做

- [ ] 重推几何重复的饱和上限。
- [ ] 为三域 mixture 画一张迁移矩阵实验表。
