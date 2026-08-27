---
type: concept
status: verified
area: [language-models, prefix-lm, unilm, attention-mask]
node_id: LM-13
aliases: [Prefix Language Model, UniLM mask, 单栈 Seq2Seq]
prerequisites: ["[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]", "[[Span Corruption、Sentinel Token 与 T5 Seq2Seq 目标]]", "[[Attention Mask、因果性与可见性合同]]"]
related: ["[[Decoder-Only、Prefix 与架构家族比较]]", "[[Mixture-of-Denoisers、UL2 与多目标采样]]"]
sources: ["[[S-2019-Dong-UniLM]]"]
exercises: ["[[习题 - Prefix LM、UniLM 与序列到序列 Mask 合同]]"]
solutions: ["[[解答 - Prefix LM、UniLM 与序列到序列 Mask 合同]]"]
figure: "[[00-知识库管理/_assets/figures/language-models/fig-lm-prefix-unilm-mask-v1.svg]]"
created: 2026-08-26
updated: 2026-08-26
---

# Prefix LM、UniLM 与序列到序列 Mask 合同

> [!abstract] 一句话结论
> Prefix LM 把一条序列分成可双向编码的 prefix 与只能从左到右生成的 suffix：prefix 内全可见，suffix 可读全部 prefix 和过去 suffix。它说明“用一套 Transformer 参数”与“采用哪一种概率目标”不是同一件事，attention relation、segment convention 和 loss region 必须分别声明。

## 一、先固定索引与分段

令拼接序列为

$$
z=(z_1,\ldots,z_P,z_{P+1},\ldots,z_{P+S}),
$$

前 $P$ 个位置属于 source/prefix，后 $S$ 个位置属于 target/suffix。以 query 位置 $i$、key 位置 $j$ 定义 relation：

$$
R_{ij}=\begin{cases}
1,& i\le P,\ j\le P,\\
1,& i>P,\ j\le i,\\
0,&\text{其他}.
\end{cases}
$$

块矩阵形式是

$$
R=
\begin{bmatrix}
\mathbf 1_{P\times P} & \mathbf 0_{P\times S}\\
\mathbf 1_{S\times P} & L_S
\end{bmatrix},
$$

其中 $L_S$ 为含对角线的下三角矩阵。

四个块逐一解释：

- 左上：prefix token 彼此双向建模；
- 右上：prefix query 不能读取 target，避免 target 反向污染 source representation；
- 左下：每个 target query 可读全部 prefix；
- 右下：target 只能读自身及过去 target。

> [!warning] 矩阵方向必须写清
> 有些库以行作 key、列作 query，或用 0 表示屏蔽。只保存一张三角图不足以复现；应保存 `query_axis`、`key_axis`、mask polarity 与加性/布尔语义。

## 二、它优化什么概率对象

若 prefix 记为 $x$，suffix target 记为 $y_{1:S}$，通常优化

$$
p_\theta(y\mid x)=\prod_{s=1}^{S}p_\theta(y_s\mid x,y_{<s}).
$$

注意 prefix 内的双向 attention 只是让 representation $h(x)$ 可使用整个 $x$；概率分解仍只针对 $y$。若 prefix token 的 labels 全部 ignore，模型没有直接承担 $p(x)$ 的 NLL。

也可以把 prefix 和 suffix 都计分，但这会定义另一个复合目标。例如 prefix 上加 MLM loss、suffix 上加 CLM loss；此时需写

$$
\mathcal L=\lambda_{\mathrm{prefix}}\mathcal L_{\mathrm{MLM}}
+\lambda_{\mathrm{suffix}}\mathcal L_{\mathrm{CLM}},
$$

不能仍简称为同一个 Prefix LM。

## 三、与纯 Causal LM 的差异

纯 CLM 的 source token 也只能看到过去；Prefix LM 的 source 内可以读右侧 source token。因此对于相同文本串，某个 source 表示 $h_i$ 会不同。若任务是“读完整文章再生成摘要”，双向 prefix 允许早期 source token 表示吸收文章结尾；纯 CLM 则靠后续层中 target query 直接访问所有 source positions。

但二者都可定义同一个条件概率 $p(y\mid x)$。可见性不同是参数化与计算路径差异，不足以单独证明样本效率或最终性能优劣。

## 四、与 Encoder–Decoder 的差异

| 维度 | 单栈 Prefix LM | Encoder–Decoder |
|---|---|---|
| 参数栈 | 一个 self-attention stack | encoder stack + decoder stack |
| source 表示 | 拼接序列左块内双向 | encoder 内双向 |
| target 读 source | 同一 self-attention 的左下块 | cross-attention |
| position/segment | 共用坐标系，需定义边界 | source/target 通常各自位置坐标 |
| KV cache | prefix K/V 与生成 suffix 同栈缓存 | encoder memory 固定，decoder cache 增长 |
| 目标 | 可为 $p(y\mid x)$ | 可为同一个 $p(y\mid x)$ |

“同一目标”不意味着“同一架构”；“单栈”也不意味着只能使用普通下三角 mask。

## 五、UniLM 的统一点在哪里

UniLM 在共享 Transformer 参数上通过 self-attention mask 切换至少三类可见性：

1. 单向 LM：按方向只读历史；
2. 双向 LM：同一有效片段内全可见，结合 masked targets；
3. Seq2Seq LM：source 双向、target 读 source 与过去 target。

统一的是 backbone 与 mask 控制接口，不是把三类统计目标证明为等价。每个 mode 仍有不同的 corruption、targets、loss mask 和采样权重。

## 六、Shift 的边界陷阱

拼接为 `[source, SEP, target]` 时，不能机械地对整串 labels 左移并全部计分，否则模型会被要求预测 source 内 token，甚至用 source 最后一个位置预测 target 起始 token，却不一定符合预期。

一个常用条件生成合同：

```text
tokens:     s1  s2  SEP  BOS  y1  y2  EOS
loss mask:   0   0   0    1   1   1   0  # 对“当前位置的下一 token”计分
next label: s2  SEP BOS   y1  y2 EOS  ---
```

这里 loss mask 的索引是 logit 位置而非 label token 位置；不同 API 可能把 ignore 写进 shifted `labels`。最安全的方法是列出每一列“input position → target token → scored?”，而不是只说“mask prompt”。

## 七、padding、packing 和变长 prefix

批中每条样本的 $P_b$ 不同，因此 relation 实际是 $R^{(b)}$。左 padding、右 padding和 packed examples 会改变矩阵块位置：

- padding query 通常不产出有效 loss；padding key 不应被真实 token 读取；
- 不同样本的 source/target 不应跨 pack 边界可见；
- segment id 不能只靠某个特殊 token 推断，尤其文本本身可能含相似 token；
- generation 时 prefix relation 一次预填充，随后新增 suffix query 应读全部 prefix cache 和已有 suffix cache。

## 八、图：一张矩阵里的四个语义块

先看图回答：右上块与左下块为什么不是对称的？

![[00-知识库管理/_assets/figures/language-models/fig-lm-prefix-unilm-mask-v1.svg|900]]

> [!figure] 图 LM-13　Causal、bidirectional 与 prefix relation 的对象比较
> 图以 query 为行、key 为列展示三类 relation，并把 Prefix LM 分成 source/source、source/target、target/source、target/target 四块。来源：本课程依据 UniLM 与 attention-relation 合同独立绘制。

**怎样读图**：选定一个格子，先说清行列是谁，再判断若翻转该格是否会造成 source 读 target 或 target 漏读 source。

**图没有证明什么**：矩阵只表达信息可见性，不表达 loss target、参数是否共享、位置编码、cross-attention 实现或性能优劣。

## 九、最小单元测试

1. 对 $P=2,S=3$ 手写 $5\times5$ relation，与实现逐格相等；
2. 改 target token，所有 prefix hidden states 应不变；
3. 改后续 target，较早 target logits 应不变；
4. 改任意 prefix token，所有 target logits允许变化；
5. prompt labels ignore 不改变 denominator；
6. pack 两条样本后，跨样本 attention 权重严格为零；
7. 增量解码 logits 与完整 forward 对齐到数值容差。

## 十、本节出口

你应能不借助架构名称写出 Prefix LM 的块 relation、条件概率与 loss 区域，并比较单栈与 encoder–decoder 的计算合同。下一节[[Mixture-of-Denoisers、UL2 与多目标采样]]把单一 relation 扩展为带 mode sampler 的复合训练分布。

## 练习与独立解答

- [[习题 - Prefix LM、UniLM 与序列到序列 Mask 合同]]
- [[解答 - Prefix LM、UniLM 与序列到序列 Mask 合同]]

