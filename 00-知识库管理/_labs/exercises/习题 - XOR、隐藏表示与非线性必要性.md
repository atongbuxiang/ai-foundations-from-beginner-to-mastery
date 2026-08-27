---
type: exercise
status: draft
area: [neural-networks/feedforward, xor, nonlinear-representation]
topic: "[[XOR、隐藏表示与非线性必要性]]"
difficulty: [A, B, C, D, E]
related: ["[[解答 - XOR、隐藏表示与非线性必要性]]", "[[万能逼近定理、紧集与逼近误差]]"]
solution: "[[解答 - XOR、隐藏表示与非线性必要性]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - XOR、隐藏表示与非线性必要性
## A. 识别与复述
### NN-XOR-A01
写出 XOR 四点与标签，并说明“线性不可分”精确否定了什么对象。
### NN-XOR-A02
区分 input space、hidden representation space、activation pattern 与 linear readout。
### NN-XOR-A03
区分有限样本插值、定义域上函数相等、uniform approximation 与分类标签一致。
## B. 手算与建模
### NN-XOR-B01
对 $s=x_1+x_2$，逐点计算 $f=\operatorname{ReLU}(s)-2\operatorname{ReLU}(s-1)+\operatorname{ReLU}(s-2)$。
### NN-XOR-B02
写出上述网络的 $W^{(1)},b^{(1)},W^{(2)},b^{(2)}$（row-vector convention），并给出每层 shape。
### NN-XOR-B03
在 $s=-0.5,0.5,1.5,2.5$ 处计算连续延拓 $f(s)$，画出 slope 的变化。
## C. 推导与证明
### NN-XOR-C01
用四条严格不等式证明 XOR 不可被单个 affine threshold 分开。
### NN-XOR-C02
用 convex hull intersection 再证明一次，并写出所用 separation necessary condition。
### NN-XOR-C03
用归纳法证明任意有限 affine-only 网络仍是 affine，并说明 bottleneck 对 effective rank 的影响。
## D. 边界、反例与纠错
### NN-XOR-D01
反驳：“hidden representation 必须保持输入全部信息才算好表示。”
### NN-XOR-D02
给出两个在四个 XOR 点上完全相同、在正方形内部不同的连续函数。
### NN-XOR-D03
纠正：“nonlinear probe 比 linear probe 好，所以 encoder 一定更好。”
## E. AI 迁移
### NN-XOR-E01
设计一个 embedding 可分性实验，区分 encoder 质量与 probe capacity。
### NN-XOR-E02
解释 gated FFN 的乘法怎样提供 affine-only MLP 没有的 feature interaction。
### NN-XOR-E03
为一次“网络无法学习 XOR”的调试写最小协议，覆盖数据、shape、activation、loss、gradient 与 seed。
## 解答入口
[[解答 - XOR、隐藏表示与非线性必要性]]
