---
type: concept
status: draft
area: [architecture, transformer, encoder, bidirectional]
aliases: [Transformer Encoder, Encoder-only Transformer, 双向 Transformer]
node_id: ARCH-34
prerequisites: ["[[Transformer Block、残差、归一化与 FFN]]", "[[Attention Mask、因果性与可见性合同]]", "[[Embedding Lookup、稀疏梯度与参数规模]]"]
related: ["[[Transformer 架构与组合方式 MOC]]", "[[Encoder–Decoder 与 Cross-Attention]]", "[[Decoder-Only、Prefix 与架构家族比较]]"]
sources: ["[[S-2017-Vaswani-Transformer复杂度]]", "[[S-2019-Devlin-BERT]]"]
exercises: ["[[习题 - Transformer Encoder 与双向表示]]"]
solutions: ["[[解答 - Transformer Encoder 与双向表示]]"]
figure: "[[00-知识库管理/_assets/figures/architecture/fig-transformer-encoder-bidirectional-v1.svg]]"
created: 2026-08-24
updated: 2026-08-24
---

# Transformer Encoder 与双向表示

> [!abstract] 本节主问题
> Encoder 把一组输入 tokens 映射为等长 contextual states。其核心不是 BERT 的名字或 MLM 目标，而是有效输入位置之间通常双向可见、每层保持 token 轴、任务通过 token head、pooling 或外部 decoder 读取这些 states。

## 一、从离散输入到 Residual Stream

对 token IDs $t_{1:T}$，先查表

$$
E_{tok}\in\mathbb R^{V\times d},\qquad X_{tok}=E_{tok}[t]\in\mathbb R^{B\times T\times d}.
$$

再注入 position/segment/type 等结构：

$$
X_0=X_{tok}+X_{pos}+X_{type}
$$

是常见相加方案，前提是 shape 与尺度相容。位置方案不是 encoder 定义的一部分，但没有相应非对称结构时 encoder 对 token 重排仍等变，无法单凭内容区分次序。

## 二、Encoder Layer 与 Stack

每层通常含双向 self-attention 与 FFN：

$$
X_{l+1}=\operatorname{Block}_l(X_l;M_{pad},P),\qquad l=0,\ldots,L-1.
$$

所有层保持 $(B,T,d)$。最终

$$
H=X_L\in\mathbb R^{B\times T\times d}
$$

仍是一行对应一个输入位置，而不是自动压成单向量。

## 三、“双向”精确指什么

对同一有效序列，self-attention relation 通常允许任意有效 pair $(i,j)$，不施加 $j\le i$。因此第 i 行表示可直接依赖左右上下文。

双向不表示：

- 没有 padding mask；
- 不需要 position；
- 输出对所有位置相同；
- 可以读取数据集未来样本；
- 具备因果推断能力。

它只描述**序列内部的可见关系**。

## 四、Padding 与输出行

Key padding 禁止有效 query 读取 padding columns；padding query rows 通常另由 output/loss mask 忽略。若只屏蔽列，padding 行仍可能从有效 keys 得到非零 state，但它们不应进入 pooling/loss。

不同 padding 长度下，同一有效前缀输出应一致；这是必要单元测试。Position ID、segment ID 也须随有效序列对齐。

## 五、三类任务出口

### 1. Token-level

$$
z_i=H_iW+b
$$

用于 tagging、span start/end、dense prediction。输出与 token 重排应同步等变（若任务/position 相应变化）。

### 2. Pooling

- 特殊 `[CLS]` state；
- masked mean/sum；
- attention pooling；
- task-specific readout。

Pooling 是模型设计，不由“encoder”自动规定。Mean 必须排除 padding；CLS 是否汇总成功是学习问题。

### 3. Memory

完整 H 可作为 encoder–decoder cross-attention 的 K/V memory。这时不先 pooling，保留 source token 轴。

## 六、BERT：架构与目标要分开

[[S-2019-Devlin-BERT]] 使用多层双向 Transformer encoder 与 masked language modeling（及原始 next-sentence objective）。MLM 定义 corrupted input、mask set 与只在选定位置上的恢复 loss。

正确分层：

- encoder 是双向计算骨架；
- MLM 是预训练目标；
- corruption recipe 是数据生成过程；
- fine-tuning head 是任务出口。

Encoder 可用 supervised、contrastive、denoising 等目标；MLM 也可配不同编码骨架。不能将两者视为同义词。

## 七、信息与表示边界

每层 dense attention 让路径长度短，但 H 是否保留原 token、顺序、局部细节或全局属性仍依参数与训练。LayerNorm/FFN/attention 可能改变信息，有限宽也形成瓶颈。

双向 encoder 对离线理解、检索 embedding 和源序列编码常自然，但无法直接按 next-token cache 接口进行开放式自回归生成；可以加生成 head/迭代 mask，但架构与推理合同随之改变。

## 八、复杂度入口

每个 encoder block 的主 work 包括：

$$
O(BTd^2)+O(BT^2d)+O(BTdd_{ff}).
$$

双向 mask 通常不减少 dense $T^2$ pair count。Pooling 只影响末端成本，不消除前面各层的 token states。

## 九、图：双向表示与读出

先看图回答：为什么 encoder 输出仍有 T 行？BERT 的 MLM 为什么属于右栏“训练出口”而不是左栏 mask 的定义？

![[00-知识库管理/_assets/figures/architecture/fig-transformer-encoder-bidirectional-v1.svg|900]]

> [!figure] 图 40.5-02　Transformer encoder 的双向可见、等长 states 与任务读出
> 左栏是有效 token 全可见关系，中栏是 stack，右栏区分 token/pool/masked 出口。来源：依据 Transformer encoder 与 BERT 独立绘制；由 [[00-知识库管理/_labs/code/plot_architecture_transformer_v1.py]] 生成。

**怎样读图**：先把左栏绿色格理解为允许边，再沿中栏确认 token 轴没有被压缩；最后给右栏每种任务分别写 output shape、padding 与 loss mask。

**图没有证明什么**：它没有证明每个 state 平等使用左右文，也没有证明 MLM 表示对所有下游任务最优。

## 十、常见错误与掌握标准

常见错误：把 encoder=BERT=MLM；双向就取消 padding/position；将 H 自动视为一个句向量；mean pooling 包含 padding；把数据时间泄漏与序列内部双向混为一谈；用 dense path 证明信息无损。

> [!summary]
> Encoder 是双向有效集上的等长 contextual mapping；position 与 padding 完成结构合同；token、pool 与 memory 是不同出口；预训练目标不等于架构。

能重建 embedding—stack—head shapes（A/B）、证明无位置时的置换等变与 masked pooling 不变性（C）、构造 padding/MLM 泄漏反例（D），并设计 encoder task contract（E）。

## 十一、练习与独立详解

- [[习题 - Transformer Encoder 与双向表示]]
- [[解答 - Transformer Encoder 与双向表示]]

## 参考来源

- [[S-2017-Vaswani-Transformer复杂度]]
- [[S-2019-Devlin-BERT]]
