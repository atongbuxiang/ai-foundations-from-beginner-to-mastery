---
type: solution
status: verified
area: [language-models, causal-lm, loss-contract]
topic: "[[Causal LM 的 Shift、Attention Mask 与 Token Loss]]"
exercise: "[[习题 - Causal LM 的 Shift、Attention Mask 与 Token Loss]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Causal LM 的 Shift、Attention Mask 与 Token Loss

## A. 识别与复述

### LM10-A01
Shift 把位置 $t$ 的表示与下一 token 标签对齐；attention relation 限制该表示可读取的 input positions；loss mask 决定已对齐的哪些预测事件进入 NLL 分子和分母。三者分别处理目标索引、信息流与统计权重。

### LM10-A02
`inputs [B,L]`、`logits [B,L,V]`、`labels [B,L]`、`loss_mask [B,L]`。显式 relation 常为 `[B,L,L]`，也可能广播为 `[B,1,L,L]` 或由 kernel 隐式生成。

### LM10-A03
条件生成/SFT 的概率对象是 $p(answer\mid prompt)$。prompt 是条件所以必须可见，却不一定是待估计随机变量；把 prompt labels ignore 后，只对 answer 的 conditional NLL 计分。

## B. 手算与构造

### LM10-B01
`inputs=[BOS,a,b]`，`labels=[a,b,EOS]`；三个 logit positions 0、1、2 分别预测 `a,b,EOS`，全为有效计分位置。

### LM10-B02
基本 relation 为
$$\begin{bmatrix}1&0&0&0\\1&1&0&0\\1&1&1&0\\1&1&1&1\end{bmatrix}.$$
若第 4 位是 padding，真实 query/key 仅前三位，可用
$$\begin{bmatrix}1&0&0&0\\1&1&0&0\\1&1&1&0\\0&0&0&0\end{bmatrix}.$$
某些 kernel 允许 pad query 产生无意义输出，但必须 loss-ignore；真实 query 的第 4 列仍必须为 0。

### LM10-B03
全局 numerator 为 $80(1.2)+20(2.0)=136$，denominator 100，正确均值 $1.36$。错误的设备等权均值是 $(1.2+2.0)/2=1.6$。

## C. 推导与证明

### LM10-C01
设备 $k$ 保存 $N_k=\sum_{i\in I_k}\ell_i,D_k=|I_k|$。全局规约后
$$\frac{\sum_kN_k}{\sum_kD_k}=\frac{\sum_k\sum_{i\in I_k}\ell_i}{|\cup_k I_k|},$$
正是所有有效 token 的算术平均。先平均设备 loss 等价需要所有 $D_k$ 相同。

### LM10-C02
注意力权重 $\alpha_j=e^{s_j+a_j}/\sum_ke^{s_k+a_k}$。若屏蔽项 $a_j=-\infty$，分子为 0。低精度用有限负数时，值需足够小使指数下溢或可忽略；若所有 key 都屏蔽，softmax 可能为 NaN；不同 dtype/kernel 的安全常数也不同，应测试全 mask 行。

### LM10-C03
因果计算图中位置 $t$ 的所有祖先输入索引不超过 $t$。改变 $x_{>t}$ 不改变任何祖先节点，所以确定性 eval forward 的 logit $\ell_t$ 不变。若发生变化，存在非法边、位置/packing 元数据耦合或随机性未关闭。

## D. 边界、反例与纠错

### LM10-D01
完整 `z=[BOS,a,b,EOS]`。外部先做 inputs `[BOS,a,b]`、labels `[a,b,EOS]`，若模型又内部把 logits `[:-1]` 与 labels `[1:]` 对齐，实际只训练 `BOS-position→b`、`a-position→EOS`，错过一个 token。

### LM10-D02
忽略 PAD loss 只阻止 pad 位置作为 target；真实 query 若仍读 PAD key，hidden state 会依赖 padding embedding/位置，且不同 pad 长度改变 logits。attention padding mask仍需阻止该信息流。

### LM10-D03
pack `[docA,docB]` 后普通下三角允许 docB query 读取全部 docA keys。这把独立文档训练变为有跨文档条件的模型，可能泄漏标签或污染评测。需用 document-id equality 与 causal relation 的交集。

## E. AI 迁移

### LM10-E01
固定同一前缀，构造两个不同未来；关闭 dropout、使用 eval；比较所有过去 positions logits，应严格或在数值容差内相同。再移除 causal mask，测试必须能检测差异，避免测试本身失效。

### LM10-E02
序列 `[BOS,p1,p2,SEP,a1,a2,EOS]` 采用下三角/文档内 relation；next labels 为 `[p1,p2,SEP,a1,a2,EOS]`；只让预测 `a1,a2,EOS` 的 logit positions（通常 `SEP,a1,a2` 所在位置）loss mask 为 1。prompt 仍是所有 answer query 的可见前缀。

### LM10-E03
无法判断 2.1 是每 token、每序列还是设备平均，也无法复算 PPL或比较不同 padding/packing。应记录每设备和全局 $N,D$、有效序列数、reduction、grad accumulation 权重、EOS/prompt ignore、跨设备规约方式；否则多卡 world size 改变就可能改变目标。

## 无提示重做

- [ ] 对一个带 prompt 和 padding 的 batch 逐列画三份 mask。
- [ ] 解释为什么 loss 快速下降不是防泄漏测试。

