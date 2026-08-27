---
type: solution
status: verified
area: [language-models, pretraining-data, packing]
topic: "[[Packing、文档边界、Position ID 与 Loss Mask]]"
exercise: "[[习题 - Packing、文档边界、Position ID 与 Loss Mask]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Packing、文档边界、Position ID 与 Loss Mask

## A. 识别与复述

### LM22-A01
Padding batching 把每条序列补到 batch 长度，语义隔离自然但浪费位置；concatenated stream 把文档接成连续因果流，利用率高却允许跨文档注意与 next-token target；contamination-free packing 把多个文档放进同一物理张量，同时用 relation、position 与 loss contract 保持逻辑隔离。

### LM22-A02
装箱合同决定哪些文档进哪个 bin；relation 合同决定 token 可读哪些 keys；position 合同决定位置编码输入；label/loss 合同决定哪些预测计分。任一项错误都可能使“形状正确”的 batch 语义错误，所以 `packing=True` 不是充分说明。

### LM22-A03
Reset position IDs 让每个文档从 0 开始，较接近逐文档 forward；continuous IDs 让后文档位置受 pack 前缀影响，可能改变绝对/旋转位置编码和 logits。选择必须与模型训练定义、最大位置和等价性目标一起声明。

## B. 手算与构造

### LM22-B01
FFD 按 $6,5,4,3,2$：先放 6；5 开新箱；4 补第一箱成 `[6,4]`；3、2 依次补第二箱成 `[5,3,2]`。两箱容量都是 10，总 token 20、容量 20，利用率 $U=20/20=1$。

### LM22-B02
以 query 为行、key 为列，文档 IDs 为 $(A,A,B,B,B)$，block-causal relation 为
$$
R=\begin{bmatrix}
1&0&0&0&0\\
1&1&0&0&0\\
0&0&1&0&0\\
0&0&1&1&0\\
0&0&1&1&1
\end{bmatrix}.
$$
它既因果，又切断 A/B 两块间的读写。

### LM22-B03
序列为 `[a, EOS, b, c, EOS]`，shift 后 `inputs=[a,EOS,b,c]`，`labels=[EOS,b,c,EOS]`。为阻止 A 的 EOS 预测 B 的首 token，loss mask 为 `[1,0,1,1]`；因此边界 target `EOS→b` 不计分。若实现保留其他 BOS/EOS 约定，应在合同中明确。

## C. 推导与证明

### LM22-C01
$1\{j\le i\}$ 使上三角元素全零；$1\{d_i=d_j\}$ 使不同文档块全零。若 token 按各文档连续排列，非零元素只位于每个对角块的下三角，故整体是下三角块对角矩阵。

### LM22-C02
一个充分条件是：每个文档内部 token/order 相同；不同文档间 attention relation 为零；每文档 position IDs 与单独 forward 相同；special tokens 与 labels 相同；跨边界 targets 被 mask；模型无跨样本耦合状态，且 dropout/RNG、数值 kernel 差异被控制。此时每层每个 token 只依赖与单独运行相同的先前状态，归纳得 logits 相等（浮点容差内）。

### LM22-C03
全局 loss 用所有 bins 的 loss sum $N=\sum_{b,t}m_{bt}\ell_{bt}$ 除有效 target 数 $D=\sum_{b,t}m_{bt}$，每个有效 target 权重均为 $1/D$。若先算每 bin mean 再平均，则 bin $b$ 中每 target 权重为 $1/(B D_b)$；短 bin 的单个 target 权重更大，除非所有 $D_b$ 相等。

## D. 边界、反例与纠错

### LM22-D01
即使 boundary label 不计 loss，文档 B 的 query 若能 attend A，B 内部所有计分 logits 仍可使用 A 信息；梯度会经注意力流向 A。因此 loss ignore 只阻断一个 target，不阻断表示污染，仍需 block relation（若目标要求独立文档）。

### LM22-D02
绝对位置模型中，同一 B 文档单独运行位置为 $(0,1)$；若前面 pack 长度 100 的 A，continuous IDs 变为 $(100,101)$。位置 embedding 不同即使 attention 已 block，首层 hidden state 和 logits 也可不同；这给出 pack 组成依赖。

### LM22-D03
减少 padding 只改变输入位置利用率；wall time 还受 kernel shape、block-mask 稀疏实现、编译、memory bandwidth、通信和装箱 CPU 限制。密集 attention 若仍算完整 $L\times L$，边界 mask 不节约相同 FLOPs；应实测 tokens/s、FLOPs、显存和端到端时间。

## E. AI 迁移

### LM22-E01
固定 eval mode、权重与 dtype，对一组长度/文档数/边界 cases 分别逐文档和 packed forward；按 document/token 映射比较 logits、loss sum、有效 target 数与 gradients，设数值 tolerance。额外做 adversarial 前缀替换：改变邻居文档不应改变目标文档 logits。

### LM22-E02
CLM：同文档且 $j\le i$，边界 next label mask；MLM：同文档双向 $1\{d_i=d_j\}$，loss 只在被选 mask positions；Prefix-LM：同文档内 prefix↔prefix 双向、suffix query 可读同文档 prefix 和较早 suffix，prefix query 不读 suffix。三者都必须显式排除异文档 relation。

### LM22-E03
无法由 `packing=True` 判断是否跨文档 attention、是否预测边界 token、position reset、BOS/EOS 插入、loss normalization 和稀疏 kernel。审计应索取 packer/attention implementation 与版本、四份合同、packed/unpacked equivalence tests、utilization、吞吐和 failure examples；缺失时标为语义不可复现。

## 无提示重做

- [ ] 手写两文档的 block-causal 矩阵与 boundary loss mask。
- [ ] 说明 packed 与逐文档 forward 等价所需的充分条件。

