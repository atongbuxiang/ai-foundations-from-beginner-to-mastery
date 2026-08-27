---
type: concept
status: verified
area: [language-models, masked-language-modeling, pseudo-likelihood]
node_id: LM-11
aliases: [MLM, Masked Language Modeling, 遮蔽语言模型]
prerequisites: ["[[概率语言模型、链式法则与自回归因子化]]", "[[Transformer Encoder 与双向表示]]"]
related: ["[[Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]", "[[NLL、Perplexity、Bits-per-Byte 与 Tokenizer 公平比较]]"]
sources: ["[[S-2019-Devlin-BERT]]", "[[S-2020-Salazar-MLM-Scoring]]", "[[S-2020-Su-7764-MLM-PET]]"]
exercises: ["[[习题 - Masked LM 的 Corruption Law、伪似然与 BERT]]"]
solutions: ["[[解答 - Masked LM 的 Corruption Law、伪似然与 BERT]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-mlm-corruption-pseudolikelihood-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Masked LM 的 Corruption Law、伪似然与 BERT

> [!abstract] 一句话结论
> Masked LM 不是“能看双向上下文的 next-token model”。它先随机抽取预测位置，再按明确定义的破坏分布生成带噪输入，只在指定位置恢复 clean token。其训练风险、逐位置伪似然评分和规范化联合概率是三个不同对象。

## 一、四个随机对象必须分开

令 clean token 序列为

$$
X=(X_1,\ldots,X_T)\sim p_{\mathrm{data}}.
$$

完整 MLM 数据生成过程至少含：

1. 抽取预测集合 $M\sim q_M(M\mid X)$；
2. 按破坏规则抽取 $\widetilde X\sim q_C(\widetilde x\mid X,M)$；
3. 模型观察 $\widetilde X$；
4. 对 $i\in M$ 预测原始 $X_i$。

总体风险可写为

$$
\mathcal R(\theta)=
\mathbb E_{X,M,\widetilde X}
\left[
\frac{\sum_{i=1}^{T}m_i[-\log p_\theta(X_i\mid\widetilde X)]}
{\sum_{i=1}^{T}m_i}
\right],
$$

或先跨 batch 汇总分子、分母后相除。两种写法对变长样本产生不同权重，应选定而非混写。

> [!important] `mask set` 不等于 `[MASK]` 出现位置
> $M$ 指哪些位置是预测目标；corruption 可能把目标位置替成 `[MASK]`、随机 token，或保持原 token。因此只能从数据生成账本确定 targets，不能只扫描输入中的 `[MASK]`。

## 二、BERT 的经典 corruption recipe

BERT 的经典实现大致选择 15% token 作为预测目标；在这些目标位置中：

- 80% 替换为 `[MASK]`；
- 10% 替换为随机 token；
- 10% 保持原 token。

所以边际上约 12% 输入位置显示 `[MASK]`，但约 15% 位置进入 loss。80/10/10 是具体论文 recipe，不是 MLM 的数学定义；动态/静态 mask、whole-word mask、span mask、mask rate 与随机替换分布都可改变。

保持原 token 的目标位置可能使任务局部过于容易；随机 token 又引入输入异常。它们用于缓解预训练出现 `[MASK]`、下游不出现的 mismatch，但并未消除所有 pretrain–finetune 差异。

## 三、双向可见不等于看见答案

Encoder 内有效输入位置通常彼此可见：

$$
R_{ij}=1\quad\text{（同一未 padding 序列内）}.
$$

但目标 token 已被 corruption 处理，模型读到的是 $\widetilde X_i$ 而非必然读到 $X_i$。因此“可见性关系全连接”和“答案是否泄漏”取决于 clean/corrupted input 的区别。保持原 token 的 10% 分支确实可直接观察答案，这是采样器的有意组成，其权重应在总体风险中如实体现。

## 四、总体最优预测什么

固定模型实际观察到的 corrupted context $\widetilde x$ 与目标位置 $i$，期望 log loss 的最优解是数据—corruption 联合分布诱导的条件分布

$$
p_\theta^*(v\mid\widetilde x,i)
=\Pr(X_i=v\mid\widetilde X=\widetilde x, i\in M).
$$

它不一定等于“给定所有其他 clean tokens 的真实条件分布” $p(X_i\mid X_{-i})$：随机替换、多个位置同时 mask 和 mask selection law 都会改变条件信息。只有在逐位置遮蔽且其余 token 保持 clean 等特定协议下，两者才对齐。

## 五、伪似然从哪里来

对一条 clean 序列，逐个位置构造只遮蔽 $i$ 的输入，定义

$$
\operatorname{PLL}_\theta(x)
=\sum_{i=1}^{T}\log p_\theta(x_i\mid x_{-i}).
$$

这可用于排序或派生 pseudo-perplexity，但要注意：

- 它通常需要 $T$ 次 forward，而非一次随机 MLM forward；
- 它不是 BERT 随机多 mask 训练 loss 的同一个 Monte Carlo 样本；
- $\exp(-\operatorname{PLL}/T)$ 是 pseudo-perplexity，不是自回归 joint perplexity；
- 各位置条件分布未必来自同一个规范化 joint distribution。

### 条件兼容性为什么不是自动的

两个二元变量 $X_1,X_2$ 的条件表若声称

$$
P(X_1=1\mid X_2=0)=0.9,
\quad P(X_1=1\mid X_2=1)=0.9,
$$

却同时给出与之矛盾的 $P(X_2\mid X_1)$ odds ratio，就可能不存在任何联合表同时满足全部条件。神经 MLM 分别拟合高维条件，不带“存在统一联合分布”的结构约束；因此不能直接把 PLL 当 $\log p(x)$。

## 六、mask 数与归一化的隐蔽偏差

设每条样本恰好抽 $K$ 个位置。若先求每条样本 masked-token 平均再对样本平均，则每条序列权重相同；若全 batch 以 masked token 总数作分母，则每个目标 token 权重相同。当 $K$ 与长度相关、短序列至少 mask 一个 token 时，二者不同。

还应记录：

- 特殊 token 是否可被抽中；
- subword 还是 whole-word 单元抽样；
- 相邻 mask 是否独立；
- 随机 token 是否从全词表均匀抽取；
- corruption 是离线固定还是每 epoch 动态重抽；
- 验证集是否冻结随机种子。

没有 sampler 版本，所谓“MLM loss 复现”并不完整。

## 七、图：从 clean sequence 到两种评分

先看图回答：为什么随机 MLM loss 与 PLL 不能直接互换？

![[00-知识库管理/_assets/figures/language-models/fig-lm-mlm-corruption-pseudolikelihood-v1.svg|900]]

> [!figure] 图 LM-11　MLM 的 corruption law、计分位置与逐位置 PLL
> A 区分 clean、mask set 和 corrupted input；B 展示只在 targets 上计分；C 将随机训练风险与逐位置伪似然并列。来源：本课程依据 BERT 与 Masked Language Model Scoring 的对象合同独立绘制。

**怎样读图**：先追踪一个 clean token 是否被选入 $M$，再看它如何被 corruption，最后确认模型的条件输入和 loss denominator。

**图没有证明什么**：图不证明 MLM 条件分布一定兼容为联合概率，也不证明 PLL 与人类可接受度、下游准确率或生成能力单调一致。

## 八、BERT 能力应怎样归因

BERT 的结果来自至少以下组合：双向 encoder、MLM/NSP 等训练目标、数据与训练预算、WordPiece tokenizer、微调协议和任务基准。不能由“MLM”单独推出“擅长理解”，也不能因标准 BERT 不便左到右生成而断言 masked objectives 无法服务生成；模型、目标、解码程序是不同层次。

科学空间关于 MLM/PET 的实践可帮助理解 prompt 化的 cloze 接口，但具体少样本结果是特定模板、标签词和模型下的经验，不应升级成普遍定理。

## 九、本节出口

你应能从 clean sequence 写出 $q_M$、$q_C$、targets、loss mask 与 denominator，解释 BERT 80/10/10 的边际比例，并严格区分 MLM risk、PLL 与 normalized joint likelihood。下一节[[Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]将把多个被删 span 压缩进结构化 target sequence。

## 练习与独立解答

- [[习题 - Masked LM 的 Corruption Law、伪似然与 BERT]]
- [[解答 - Masked LM 的 Corruption Law、伪似然与 BERT]]

