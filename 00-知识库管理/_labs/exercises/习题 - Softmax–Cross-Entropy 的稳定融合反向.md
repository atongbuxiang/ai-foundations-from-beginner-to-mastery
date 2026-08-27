---
type: exercise
status: draft
area: [neural-networks/losses, softmax, numerical-stability]
topic: "[[Softmax–Cross-Entropy 的稳定融合反向]]"
difficulty: [A, B, C, D, E]
related: ["[[解答 - Softmax–Cross-Entropy 的稳定融合反向]]", "[[Forward_Reverse AD、Tape 与复杂度]]"]
solution: "[[解答 - Softmax–Cross-Entropy 的稳定融合反向]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Softmax–Cross-Entropy 的稳定融合反向
## A. 识别与复述
### NN-SCE-A01
写出 logits、softmax probability、normalized target 和 cross-entropy 的完整对象合同。
### NN-SCE-A02
解释 max-shift 为何是精确恒等变换，并说明它解决哪种 overflow。
### NN-SCE-A03
列出“梯度是 $p-y$”所需的 target、temperature、weight 和 reduction 限定。
## B. 手算与建模
### NN-SCE-B01
对 $z=(1000,999,998)$、真类为第 2 类，稳定计算 $p,ell,\nabla_z\ell$。
### NN-SCE-B02
若 $y=(2,1,0)$ 未归一化，对同一 cross-entropy 定义推出 gradient，并说明为何不是 $p-y$。
### NN-SCE-B03
对 3 个样本的 mean loss，已知逐样本 $P-Y$，写出 logits gradient；若第 3 个是 padding，新分母是什么？
## C. 推导与证明
### NN-SCE-C01
从 $\ell=\operatorname{LSE}(z)-y^Tz$ 用 differential 推出 $p-y$。
### NN-SCE-C02
推出 softmax Jacobian $\operatorname{diag}(p)-pp^T$，并用它交叉推出 cross-entropy gradient。
### NN-SCE-C03
推出 temperature softmax cross-entropy 的 $(p^{(\tau)}-y)/\tau$，并解释 distillation 外乘 $\tau^2$ 后的 scale。
## D. 边界、反例与纠错
### NN-SCE-D01
构造 naive `softmax` 后 `log` 出现 `inf` 而 stable logsumexp 有限的 logits。
### NN-SCE-D02
反驳：“softmax cross-entropy 对 logits 凸，所以深网络训练对 parameters 也凸。”
### NN-SCE-D03
区分 multiclass softmax CE 与 multi-label sigmoid BCE，给出不能互换的任务反例。
## E. AI 迁移
### NN-SCE-E01
为 label smoothing 设计能区分“均匀分到全部类”与“只分到错类”的单元测试。
### NN-SCE-E02
为 masked language modeling 的 distributed global-mean loss 设计 valid-count 与 all-reduce scale 合同。
### NN-SCE-E03
为 fused log-softmax/NLL kernel 设计 shift-invariance、extreme-logit、finite-difference、dtype 与 reduction 验收。
## 解答入口
[[解答 - Softmax–Cross-Entropy 的稳定融合反向]]
