---
type: concept
status: verified
area: [language-models, mechanistic-interpretability, induction-heads]
node_id: LM-36
aliases: [Induction Head, 归纳头, ICL 机制回路]
prerequisites: ["[[ICL 的 Bayesian、线性回归与元优化解释]]", "[[Self-Attention、Cross-Attention 与张量形状]]"]
related: ["[[Transformer Block、残差、归一化与 FFN]]", "[[训练实验协议、事故记录与因果证据地图]]"]
sources: ["[[S-2022-Olsson-Induction-Heads]]", "[[S-2023-VonOswald-ICL-Gradient-Descent]]"]
exercises: ["[[习题 - Induction Head、机制回路与因果干预边界]]"]
solutions: ["[[解答 - Induction Head、机制回路与因果干预边界]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-icl-induction-head-evidence-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Induction Head、机制回路与因果干预边界

> [!abstract] 一句话结论
> Induction head 的核心行为是从 $[A][B]\ldots[A]$ 复制 $B$。在小型 attention-only 模型中可以给出精确回路；在大模型中，attention pattern、训练共现和单头消融只能组成分层证据，不能自动证明它承担全部 ICL。

## 一、先看最小行为

给序列

$$
[A][B][C]\ldots[A],
$$

若模型提高下一个 token 为 $B$ 的概率，就表现出 pattern completion。为避免模型只背训练 n-gram，实验常用随机 token 序列，重复多次后测第二遍之后的 loss。

一个经验 induction criterion 至少含：

1. prefix matching：当前 $A$ 位置注意到先前同样的 $A$ 所在模式；
2. copying：被注意位置之后的 $B$ 经 OV 路径提高 $B$ logit。

只满足“看向某处”不够，因为 attention weight 不告诉我们该 value 对哪个 logit 有什么影响。

## 二、为什么常需要两个 head

标准 attention 在位置 $t$ 的 query 与位置 $s$ 的 key 比较当前残差表示。为了回答“哪个 token 之前出现过与当前 token 相同的前缀”，模型需要把前一个 token 的信息写进可被后层读取的位置。

一个简化两头回路：

1. previous-token head：在位置 $s$ 把 $x_{s-1}$ 的信息写入残差流；
2. induction head：当前位置 $t$ 的 query 表示 $x_t=A$，与各位置中记录的 previous token 匹配；
3. 若位置 $s$ 的 previous token 是 $A$，该 head 注意位置 $s$，而位置 $s$ 自身 token 是 $B$；
4. OV 电路复制/提升 $B$ 的 logit。

于是实现

$$
[A][B]\ldots[A]\mapsto B.
$$

一层模型缺少跨层 K-composition 的这条简单路径，但这不构成“一层模型绝不可能做任何上下文适应”的普遍定理；模型结构和数据分布仍要写清。

## 三、从 attention 公式看 QK 与 OV 分账

单头输出写作

$$
o_t=\sum_{s\le t}\alpha_{ts}W_O W_V h_s,
$$

$$
\alpha_{ts}=\operatorname{softmax}_s
\left(\frac{(W_Qh_t)^\top(W_Kh_s)}{\sqrt{d_k}}+M_{ts}\right).
$$

QK 路径决定看哪里，OV 路径决定把什么写回残差流。若最终 unembedding 为 $W_U$，该 head 对 logit 的直接贡献近似

$$
\Delta \ell_t=W_Uo_t.
$$

所以机制分析至少需要：attention pattern、value/output 方向和最终 logit effect。仅凭彩色 attention 图就说“模型使用了某证据”是不充分的。

## 四、四级证据梯子

### 1. 行为相关

重复序列后 token loss 下降，说明模型利用前文；不定位具体 head。

### 2. 结构相关

某些 head 同时有高 prefix-matching 和 copying score；仍可能只是共现标志。

### 3. 因果干预

消融 head、patch activation 或替换 attention pattern，观察行为差

$$
\Delta=\mathcal M(f_\theta(x))-\mathcal M(f_{\theta,do(h\leftarrow h')}(x)).
$$

这增强因果证据，但干预可能分布外，也可能破坏多个共享功能。

### 4. 权重级构造/反编译

在指定模型中由矩阵乘积推导 prefix matching 与 copying，并用替换实验恢复 loss。这是最强的局部机制证据，但量词仍限该模型。

## 五、necessity、sufficiency 与冗余

- necessity：移除回路后目标行为显著下降；
- sufficiency：只保留/植入回路就能产生行为；
- mediation：输入干预对输出的影响由该回路传递多少；
- redundancy：多个 head 或 MLP 能补偿同一功能。

单头 ablation 影响小，不证明该 head 无功能；可能有备份。影响大也不证明它专门负责 ICL；它可能同时承担常用复制与语法功能。

## 六、训练期 induction bump 的证据含义

[[S-2022-Olsson-Induction-Heads]] 观察到某些模型训练中 induction heads 形成与 in-context loss 改善同窗发生。时间共现是重要证据，但仍可能有共同原因，例如整体表示突然成熟。

更强测试包括：

- 改架构使 induction circuit 难以形成，看 bump 是否随之移动；
- 在相同 checkpoint 跨任务测 prefix matching 与 ICL；
- 做 activation patch，定位哪条路径中介；
- 构造 matched control heads；
- 检查小模型精确结论在大模型中哪些只剩相关。

## 七、从精确复制外推抽象 ICL 的风险

随机 token 的 $A B\ldots A\to B$ 是局部序列复制。分类 few-shot、翻译、任务映射可能需要：

- 模糊匹配而非完全 token 相等；
- 在 embedding/feature 空间匹配 $A^*$ 与 $A$；
- 将 $B^*$ 映射到 query 对应的 $B$；
- 多层 MLP 做抽象、门控与答案格式化。

因此“发现 induction head”最多说明一种可复用原语。要说它解释复杂 ICL，需展示任务级因果效应和抽象表示的可迁移性。

## 八、图解：回路与证据梯子

先看图回答：为什么 attention pattern 位于证据梯子的最低一级？

![[00-知识库管理/_assets/figures/language-models/fig-lm-icl-induction-head-evidence-v1.svg|900]]

> [!figure] 图 LM-36　Induction 回路与机制证据
> 上方用随机 token 展示 current A 匹配 earlier A，并由 earlier A 后的 B 提升最终 B；下方从 attention pattern 走到权重级构造。图由本库依据 Transformer Circuits 的行为定义重新绘制。
> **生成：**本图由本库依据本节定义、正文列出的一级来源和固定绘图脚本重新绘制；图中的小规模数值或结构用于教学，不复刻论文原图。

**怎样读图**：紫色弧线回答“匹配哪个前缀”，绿色弧线回答“复制哪个 next token”；再逐级检查相关、logit、干预和构造是否都成立。

**图没有证明什么**：它不证明所有模型用相同两头电路，也不证明 induction head 是复杂 ICL 的唯一或主要机制。

## 九、最小可复现实验

1. 生成长度 $L$ 的随机 token 序列并重复；
2. 记录第二遍各位置相对第一遍的 token NLL；
3. 为每头算 prefix matching score；
4. 计算 head direct logit attribution 的 copying score；
5. 逐头/成对 ablation，保存 clean 与 corrupted run；
6. activation patch 时固定源样本与目标样本；
7. 报行为恢复比例而非只报 attention 图；
8. 对自然语言任务重复，明确外推是否失败。

## 十、常见错误

- 把高 attention weight 当正向 logit 贡献；
- 把单头名字当跨模型稳定神经元；
- 只做消融，不做 matched control；
- 忽略 LayerNorm、残差与 MLP 的间接路径；
- 用分布外的零向量消融解释自然干预；
- 从两层模型精确机制直接推广百层模型；
- 把行为必要性误写成机制唯一性。

## 十一、出口标准

完成本节后，应能从 QK/OV 公式解释 $AB\ldots A\to B$，区分 pattern、logit attribution、ablation、patching 和权重构造，并为任何“某个 head 负责某能力”的主张写出 necessity、sufficiency、冗余与外推审计。

## 十二、来源与练习

- [[S-2022-Olsson-Induction-Heads]]：主要机制证据与边界；
- [[S-2023-VonOswald-ICL-Gradient-Descent]]：线性 ICL 构造的相邻解释；
- [[习题 - Induction Head、机制回路与因果干预边界]]；
- [[解答 - Induction Head、机制回路与因果干预边界]]。
