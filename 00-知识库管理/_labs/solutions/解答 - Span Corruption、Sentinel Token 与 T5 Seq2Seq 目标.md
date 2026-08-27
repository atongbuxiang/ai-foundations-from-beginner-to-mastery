---
type: solution
status: verified
area: [language-models, span-corruption, t5]
topic: "[[Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]"
exercise: "[[习题 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标

## A. 识别与复述

### LM12-A01
Sentinel 在 source 代替整段缺口；以唯一编号把 source 缺口与 target 段配对；在 target 中分隔相邻恢复段；它本身还是 decoder 必须预测的结构 token，可控制恢复顺序与结束。

### LM12-A02
连续多个 `[MASK]` 通常保留每个缺失 token 的槽位和输入长度；T5 把整 span 压成一个 sentinel，并把所有缺失内容组织成另一个自回归 target sequence。输入长度、输出概率对象和架构信息流均改变。

### LM12-A03
Encoder self 在同一有效 source 内双向；decoder self 对 target 为 causal；cross-attention 让每个有效 decoder query 读取全部 encoder memory。padding/packing 后三者还需与边界 relation 相交。

## B. 手算与构造

### LM12-B01
一种标准构造：
```text
source: a <s0> d e <s1> g
target: <s0> b c <s1> f <s2> EOS
```
`<s2>` 封闭最后恢复段；若实现用别的终止约定，必须成对调整 reconstruct 规则。

### LM12-B02
$L_{source}=T-N+K=100-15+5=90$；忽略 EOS/额外终止 token，$L_{target}=N+K=20$。

### LM12-B03
```text
decoder input : BOS  <s0> b  c   <s1> f   <s2>
decoder label : <s0> b    c  <s1> f    <s2> EOS
```
不能外部和模型内部各 shift 一次。

## C. 推导与证明

### LM12-C01
Source 保留所有未删 token 的原顺序，并在每个删除区间放唯一键 $s_k$。Target 对每个键按同序保存恰好该区间内容，下一键给出右边界。扫描 source，普通 token 复制，遇键查 target 对应半开区间并插入；每个 clean token恰被保留或插入一次，顺序不变，故重建唯一。

### LM12-C02
删除 $N$ 个 token 使长度从 $T$ 变为 $T-N$，每个 $K$ span 加回一个 sentinel，故 $T-N+K$。Target 含 $N$ 个删除 token 与每段前的 $K$ 个 sentinel；若另有 terminal sentinel/EOS，分别再加 1，具体取决于实现约定。

### LM12-C03
令 $S\sim q(S\mid X)$，变换得到 $(\tilde X,Y)=f(X,S)$，则
$$R(\theta)=E_{X\sim p_{data}}E_{S\sim q(\cdot\mid X)}
\left[\sum_u-\log p_\theta(Y_u\mid\tilde X,Y_{<u})\right],$$
必要时再除明确定义的有效 target denominator。第三层随机性可理解为 target token 条件分布/模型预测事件，训练用观测 $Y$ 的 log score。

## D. 边界、反例与纠错

### LM12-D01
Clean `a b c d e` 删除 `b` 与 `d`。若 source 为 `a M c M e`，target 写 `M b M d`，只能依赖出现次序配对；若截断、重排或生成漏一个 M，无法凭 id 判断哪段属于哪个缺口。唯一 `s0/s1` 能检测并定位错配。

### LM12-D02
截断可：保留 source sentinel 却删掉 target 对应 span；target 截在 span 中使右边界丢失；删 source 后缀却仍保留其 target span/编号。还可能截掉 EOS/terminal sentinel，造成不可判定结束。

### LM12-D03
同 noise density 下，平均 span 长度决定 $K$ 与 target sentinel 数；span 分布、边界限制、特殊 token、rounding 和 truncation 也改变条件任务与长度/FLOPs。因此只共享一个边际删除率不足以定义同一 corruption law。

## E. AI 迁移

### LM12-E01
测试：spans 非空且不重叠；删除 token 数/噪声率满足配置；sentinel 集合唯一并按序；`reconstruct(corrupt(x))==x`；同 seed 复现；空/极短/全 special 输入行为明确；截断后无孤立 sentinel；source/target 长度满足账本公式。

### LM12-E02
固定删除 $N$ 时，平均 span 越长，$K$ 通常越小：source $T-N+K$ 和 target $N+K$ 都更短，特别降低 sentinel 开销与 attention 长度；但恢复单位更长、局部提示更少，训练更偏向长程连续生成。比较应按 FLOPs 与 target 数对齐。

### LM12-E03
需补：normalization/tokenizer hash、sentinel 是否原子及 id 顺序、noise density、span-length law、rounding、特殊 token/文档边界、source/target 最大长度与截断、dynamic seed、decoder shift/EOS、有效 denominator。缺失时无法确认复现的是哪一个 T5 objective。

## 无提示重做

- [ ] 手工构造三段 corruption 并逆向还原。
- [ ] 写清 target 长度中 terminal sentinel 与 EOS 的计数约定。
