---
type: concept
status: verified
area: [language-models, span-corruption, t5, seq2seq]
node_id: LM-12
aliases: [T5 Denoising, Span corruption, Sentinel token]
prerequisites: ["[[Masked LM 的 Corruption Law、伪似然与 BERT]]", "[[Encoder–Decoder 与 Cross-Attention]]"]
related: ["[[Prefix LM、UniLM 与序列到序列 Mask 合同]]", "[[Mixture-of-Denoisers、UL2 与多目标采样]]"]
sources: ["[[S-2020-Raffel-T5]]", "[[S-2020-Su-7867-中文T5]]", "[[S-2021-Su-8209-T5-PEGASUS]]"]
exercises: ["[[习题 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]"]
solutions: ["[[解答 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-t5-span-sentinel-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标

> [!abstract] 一句话结论
> T5 风格 span corruption 把若干不重叠的连续片段从 source 中删除，每段用唯一 sentinel 占位，再让 decoder 自回归输出“sentinel + 被删内容”的有序串。sentinel 不只是 `[MASK]` 的换名，而是 source 与 target 之间可逆对齐的结构标记。

## 一、为什么从单 token mask 走向 span

自然语言中的不确定单元经常跨多个 subword。若独立 mask token，连续片段长度近似由 Bernoulli 过程偶然产生；span corruption 则先显式抽取噪声密度与 span 长度，使模型恢复短语级缺失，同时缩短 encoder 输入和 decoder target。

设 clean sequence 为 $x_{1:T}$，抽到 $K$ 个按原顺序排列、互不重叠的区间

$$
S_k=[a_k,b_k],\qquad b_k<a_{k+1}.
$$

为每个区间分配唯一 sentinel $\langle s_k\rangle$。source 中整个 $S_k$ 被一个 sentinel 替换；target 按原顺序串联各 sentinel 与被删 span。

## 二、手工构造一对 source–target

clean tokens：

```text
The  small  red  fox  jumps  very  high  today
```

若删除 `small red` 与 `very high`，得到：

```text
source: The <s0> fox jumps <s1> today
target: <s0> small red <s1> very high <s2>
```

最后的 `<s2>`（具体实现也可能结合 EOS 约定）封闭最后一段，使 decoder 知道恢复列表结束。关键不变量是：sentinel 编号在 source 和 target 中一致，且按 span 原始顺序唯一出现。

### 可逆重建算法

1. 扫描 source，遇到普通 token 原样输出；
2. 遇到 `<s_k>`，在 target 中找到同名 sentinel；
3. 插入它之后、下一个 sentinel 之前的 token；
4. 验证 sentinel 集合、顺序和边界；
5. 恢复的 clean sequence 应与输入 corruption 前完全相同。

这是一条很强的 property test；若失败，常见原因是 off-by-one、span 重叠或 target 少了边界 sentinel。

## 三、概率目标是条件序列模型

记 corrupted source 为 $\widetilde x$，结构化恢复 target 为 $y_{1:U}$。Encoder–decoder 模型定义

$$
p_\theta(y\mid\widetilde x)
=\prod_{u=1}^{U}p_\theta(y_u\mid\widetilde x,y_{<u}).
$$

训练时 decoder 输入/标签同样需要 shift：

```text
decoder input : BOS   <s0>  small  red   <s1> ...
decoder label : <s0>  small red    <s1>  very ... EOS
```

Encoder source 内通常双向可见；decoder target 内 causal；decoder cross-attention 可读全部 encoder memory。三种 relation 不应只用一句“seq2seq mask”含混带过。

loss 可写为

$$
\mathcal L=
\frac{\sum_{b,u}m_{bu}[-\log p_\theta(y_{bu}\mid\widetilde x_b,y_{b,<u})]}
{\sum_{b,u}m_{bu}},
$$

其中 sentinel、恢复内容和 EOS 是否全部计分必须明确。T5 风格通常让整个 target sequence 参与 next-token loss，而非只计原始被删内容。

## 四、span sampler 决定了什么任务

完整配置至少包括：

- noise density：原 token 中期望删除比例；
- mean span length 或 span-length distribution；
- rounding：目标 noise token 数与 span 数怎样取整；
- 可选位置：特殊 token、文档边界能否进入 span；
- 采样是否均匀覆盖合法 composition；
- 超长 source/target 怎样截断；
- sentinel 数量上限与 id 顺序；
- 动态 corruption 的 seed 与验证集冻结规则。

相同 15% 噪声率但平均 span 长度不同，会改变目标中 sentinel 数、decoder 长度和恢复粒度，因此不是同一训练分布。

### 长度近似账本

若删除 $N$ 个原 token、形成 $K$ 个 span：

$$
L_{\mathrm{source}}\approx T-N+K,\qquad
L_{\mathrm{target}}\approx N+K+\text{terminal tokens}.
$$

增大平均 span 长度通常减小 $K$；encoder/decoder 长度、attention FLOPs 和有效 target 数随之变化。比较目标质量时必须同时对齐训练 token/FLOPs，而不能只说“相同 batch size”。

## 五、sentinel 的四种角色

1. **占位**：指出 source 有一段缺失，而非一个 token 缺失；
2. **配对键**：把 source 第 $k$ 个缺口与 target 第 $k$ 段连接；
3. **分隔符**：在 target 中界定各恢复 span；
4. **生成控制符**：decoder 必须学会正确发出结构 token。

若所有 span 都用同一个 `[MASK]`，仍可按位置顺序推断配对，但 target 边界表达更弱；唯一 sentinel 使编码更明确。若 sentinel 本身被 tokenizer 拆分，结构合同被破坏，因此它们应作为原子特殊 token 注册。

## 六、与 BERT MLM 的本质差异

| 维度 | BERT 风格 MLM | T5 span corruption |
|---|---|---|
| 输入 | 等长或近似等长 corrupted sequence | 每个 span 压成一个 sentinel |
| 输出 | 各 masked position 的分类 | decoder 生成一个有序 target sequence |
| 输出依赖 | 常按位置条件独立计 loss | target token 自回归依赖 |
| 主体架构 | encoder | encoder–decoder |
| score | masked-token conditional | conditional sequence likelihood |

差异不应简化为“单词 mask 对短语 mask”：输出概率对象与计算图也变了。

## 七、图：两段 corruption 的对齐流水线

先看图回答：为什么两个被删 span 必须使用不同 sentinel？

![[00-知识库管理/_assets/figures/language-models/fig-lm-t5-span-sentinel-v1.svg|900]]

> [!figure] 图 LM-12　Span sampler、source 压缩与 target 展开
> 左侧标出不重叠 span；中部展示 source 以唯一 sentinel 占位；右侧展示 decoder target 的 sentinel—内容交替与 shift。来源：本课程依据 T5 span-corruption 合同独立绘制。

**怎样读图**：给每个颜色 span 编号，追踪同色 sentinel 是否同时出现在 source 与 target，并检查 target 顺序能否唯一恢复 clean sequence。

**图没有证明什么**：图不证明图示噪声率或 span 长度最优，不代表所有 T5 checkpoint 使用完全相同的 tokenizer、corpus 和 corruption 实现。

## 八、实践与证据边界

T5 的 text-to-text 统一是接口统一：任务输入输出都序列化为文本；它不表示各任务数据、评价和决策成本相同。中文 T5/mT5 与 T5 PEGASUS 的博客实践提供了中文生成和 gap-sentence 目标的实现线索，但结论依赖模型版本、中文 tokenizer、预训练数据和任务设置。

## 九、最小验收门

- corruption 后 source 与 target 能无损重建 clean tokens；
- spans 非空、互不重叠、按原顺序；
- sentinel 原子化且 source/target 编号一致；
- decoder inputs/labels 只 shift 一次；
- encoder、decoder-self、cross 三类 relation 分开测试；
- 日志保存 clean/source/target 长度、noise tokens、span count 与有效 target denominator；
- 截断不得制造孤立 sentinel 或半个 target span。

## 十、本节出口

你应能手工把任意 clean sequence 变换为可逆的 T5 source–target 对，写出 conditional autoregressive loss，并解释 sampler 如何影响长度和计算。下一节[[Prefix LM、UniLM 与序列到序列 Mask 合同]]比较“两个堆栈的 encoder–decoder”与“一个堆栈上的分块可见性”。

## 练习与独立解答

- [[习题 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]
- [[解答 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]
