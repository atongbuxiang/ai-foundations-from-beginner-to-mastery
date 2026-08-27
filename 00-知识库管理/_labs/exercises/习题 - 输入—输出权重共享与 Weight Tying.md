---
type: exercise
status: draft
area: [neural-networks/embedding-output, weight-tying, shared-parameters]
topic: "[[输入—输出权重共享与 Weight Tying]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - 输入—输出权重共享与 Weight Tying]]"
created: 2026-08-24
updated: 2026-08-24
---
# 习题 - 输入—输出权重共享与 Weight Tying

## A

### NN-WTY-A01
写出 untied 输入矩阵 $E$、输出矩阵 $U$、hidden state $h$、logits $z$ 的 shape。直接 tying 需要哪些维度与词表行映射条件？

### NN-WTY-A02
区分“同一个 Parameter 被两处引用”“初始化时复制相同数值”“每步之后再同步数值”。哪一种才有单一共享梯度与 optimizer state？

### NN-WTY-A03
为什么 weight tying 同时是参数节省、函数类约束与优化耦合，而不只是 checkpoint 压缩技巧？

## B

### NN-WTY-B01
忽略其他参数并保留输出 bias。取 $V=50{,}000,d=d_h=1024$，计算 untied 与 direct-tied head+embedding 的参数量及节省比例。

### NN-WTY-B02
若 $V=50{,}000,d=512,d_h=1024$，untied 输出为 $Uh$，projected tying 为 $EPh$，其中 $P\in\mathbb R^{d\times d_h}$。分别计算词表相关参数量，并计算节省量。

### NN-WTY-B03
取 $V=3,d=2$，输入 token 为 1，lookup 上游梯度 $g_x=(0.2,-0.1)$，hidden $h=(2,-1)$，softmax 误差 $p-y=(0.1,-0.7,0.6)$。计算共享矩阵的 input、output 与总梯度。

## C

### NN-WTY-C01
从 $x=E^\mathsf Tq_i$ 与 $z=Eh+b$ 出发，推导共享参数梯度
$$
\nabla_E\mathcal L=q_i g_x^\mathsf T+(p-y)h^\mathsf T.
$$
解释为什么第二项通常使所有词表行非零。

### NN-WTY-C02
对 projected tying $z=EPh+b$ 推导 $\nabla_E\mathcal L$、$\nabla_P\mathcal L$ 与 $\nabla_h\mathcal L$；注明 direct tying 是哪一个特例。

### NN-WTY-C03
假设 $E_{ij}$ 独立、零均值、方差 $\sigma_E^2$，$h_j$ 独立、零均值、方差 $q_h$。近似计算 direct-tied logit $z_i=e_i^\mathsf Th$ 的方差，并据此给出保持 $O(1)$ logit 尺度的初始化关系。

## D

### NN-WTY-D01
一个实现用 `output.weight.data.copy_(embedding.weight.data)` 初始化，却声称完成 tying。设计 identity、gradient、optimizer 与 checkpoint 四层测试来识别错误。

### NN-WTY-D02
输入端把 padding row 冻结，但共享输出端仍让该 row 参与 softmax。分析该行的总梯度与“冻结 padding”语义冲突，并提出两种明确合同。

### NN-WTY-D03
共享前 input gradient 与 output gradient 在某些行上 cosine 为负。为什么这不自动证明 tying 有害？设计一个监控与干预协议来判断是否存在持续梯度冲突。

## E

### NN-WTY-E01
设计 untied、direct-tied、projected-tied 三组公平比较。除最终 perplexity 外，至少报告参数、吞吐、显存、logit 尺度、梯度分解与稀有词表现。

### NN-WTY-E02
反驳：“Tying 节省一半词表参数，所以模型等价地变小而表达能力不变。”给出函数类、维度、几何、优化与词表语义五方面边界。

### NN-WTY-E03
若输入 tokenizer 与输出词表并不完全相同，给出可共享的行子集或映射方案；说明如何避免 token-ID 偶然相等却语义不等造成的 silent corruption。
