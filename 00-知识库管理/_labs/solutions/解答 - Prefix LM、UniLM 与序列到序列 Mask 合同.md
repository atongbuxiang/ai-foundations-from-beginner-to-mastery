---
type: solution
status: verified
area: [language-models, prefix-lm, unilm]
topic: "[[Prefix LM、UniLM 与序列到序列 Mask 合同]]"
exercise: "[[习题 - Prefix LM、UniLM 与序列到序列 Mask 合同]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Prefix LM、UniLM 与序列到序列 Mask 合同

## A. 识别与复述

### LM13-A01
左上 prefix→prefix 全可见；右上 prefix query→target key 全屏蔽；左下 target query→prefix key 全可见；右下 target→target 下三角。它既让 source 双向编码，又防止 source 被答案污染，并让 suffix 只按过去生成。

### LM13-A02
Backbone 参数共享只说明同一个函数族接受不同 mask。单向、双向、seq2seq mode 还各有自己的 corruption、target、loss region 与 sampling distribution；共享参数不让这些总体风险在数学上相等。

### LM13-A03
Prefix LM 在一个 self-attention stack 中拼接 source/target，target 通过左下块直接读 source keys。Encoder–decoder 先在独立 encoder stack 生成 memory，decoder 用 cross-attention 读取；两者都可参数化 $p(y\mid x)$，但参数、位置坐标、缓存和计算路径不同。

## B. 手算与构造

### LM13-B01
以 query 为行：
$$R=\begin{bmatrix}
1&1&0&0&0\\
1&1&0&0&0\\
1&1&1&0&0\\
1&1&1&1&0\\
1&1&1&1&1
\end{bmatrix}.$$
前两行为 prefix，后三行为 suffix。

### LM13-B02
整串 next labels 为 `[s2,SEP,BOS,y1,y2,EOS,---]`。要只预测 `y1,y2,EOS`，计分 logit positions 是 `BOS,y1,y2`（索引 3、4、5），以 logit position 对齐的 loss mask 为 `[0,0,0,1,1,1,0]`。

### LM13-B03
$P=0$ 时矩阵退化为 $L_S$，即无条件 causal LM；$p(y\mid x)$ 变成 $p(y)$。$S=0$ 时仅有全可见 prefix block；若 loss 只定义在 suffix，则 denominator 为 0，条件输出是空序列、概率形式上为 1，但没有训练信号，必须跳过或另设 prefix objective。

## C. 推导与证明

### LM13-C01
每层 prefix query 的可见 keys 仅在 prefix；前一层每个 prefix state 又只依赖 prefix。对层数归纳，所有 prefix hidden states 都是 $x$ 的函数而不含 $y$。残差、MLP、normalization 若逐位置/不跨被屏蔽 token，同样不引入 target 边。

### LM13-C02
第 $s$ 个 target logit 的 query 位于 suffix，可读取全部 $x$ 与 $y_{<s}$，但 relation 屏蔽 $y_{>s}$。共享网络因此可表示映射 $(x,y_{<s})\mapsto p(y_s\mid x,y_{<s})$；对各 $s$ 的条件相乘即给出所需因子化。

### LM13-C03
令 $d(i)$ 是 document id，先有 prefix relation $R^{pre}_{ij}$，再定义边界关系 $R^{doc}_{ij}=1\{d(i)=d(j)\}$。最终
$$R_{ij}=R^{pre}_{ij}\land R^{doc}_{ij}\land R^{valid}_{ij}.$$
每篇样本用自己的局部 $P_b$ 建块；不能先对全 pack 使用一个全局 prefix 分界。

## D. 边界、反例与纠错

### LM13-D01
正确右上为 0、左下为 1。若把 `query=row,key=col` 的矩阵交给期待相反轴的 kernel，矩阵被转置，右上变 1：prefix query 能读 target；左下反而 0，target 又读不到 source。训练可通过复制答案取得虚低 loss。

### LM13-D02
Ignore 只移除 prompt 的预测误差。若 prompt query 可读取 answer，经过多层后其 hidden/KV 已含未来答案，answer query 再读取 prompt cache就间接泄漏；若 answer 读不到 prompt，则优化的也不再是预期 $p(answer\mid prompt)$。

### LM13-D03
整串 shift 并全 1 loss 会训练 `s1→s2`、`s2→SEP`、`SEP→BOS` 等 source/boundary预测，目标变成 prefix LM loss 与 conditional target loss 的混合；长 source 还会主导 denominator。

## E. AI 迁移

### LM13-E01
测试：改 target 不改变 prefix states；改未来 target 不改变更早 target logits；改 prefix 允许所有 suffix logits 变化；逐格核对小矩阵；额外做 pack 跨文档不变性与 prompt ignore denominator 测试。

### LM13-E02
Prefill 对完整 prefix 用双向 block 一次计算并缓存 K/V。生成第一个 suffix token 时 query 必须读全部 prefix cache；以后新增 query 读全部 prefix 与已有 suffix cache，不能重算后让 prefix 读取 suffix。缓存 position/segment ids 与 full forward 对齐，增量 logits 应在容差内相同。

### LM13-E03
UniLM 证明的是一套参数和 mask 接口可构造多种 relation（`I`）；各 mode 的条件信息和 loss 不同，统计 estimand 不同。是否互相促进是特定 mixture、数据、容量和任务下的 `E/H`，需单 mode 与 mixture 消融，不能由“统一”一词推出等价。

## 无提示重做

- [ ] 不看笔记写出 Prefix LM 四块矩阵。
- [ ] 对一条带 BOS 的 suffix 精确定位 loss positions。

