---
type: exercise
status: draft
area: [neural-networks/normalization, residual-networks, transformers]
topic: "[[Pre-Norm、Post-Norm 与归一化放置]]"
difficulty: [A, B, C, D, E]
solution: "[[解答 - Pre-Norm、Post-Norm 与归一化放置]]"
created: 2026-08-23
updated: 2026-08-23
---
# 习题 - Pre-Norm、Post-Norm 与归一化放置

## A

### NN-NPP-A01
写出单 residual sublayer 的 Pre-Norm/Post-Norm 前向式与 Jacobian；标出每个 Jacobian 的求值点和乘法顺序。

### NN-NPP-A02
“Pre-Norm 有 identity path”“Pre-Norm 全网 Jacobian 必然接近单位阵”“Pre-Norm 不经过任何 norm”三句话分别真假如何？

### NN-NPP-A03
把“精确恒等式、mean-field 定理、有条件解释、经验规律”四种证据分别对应到 residual sum、Xiong 论文、深度稀释和最终任务效果。

## B

### NN-NPP-B01
令 $F(x)=c$ 为常向量。分别计算 Pre/Post forward Jacobian，并在 $\varepsilon=0$ LayerNorm 下说明共同 shift/radial direction 的命运。

### NN-NPP-B02
局部线性模型中令 $J_N=A,J_F=aI$，且 $Av=0,At=\lambda t$。手算 Pre/Post 在 $v,t$ 两方向的增益。

### NN-NPP-B03
某 Pre-Norm 模型含 $L$ 个子层和 final norm $N_f$。写出全网 Jacobian，并说明 final norm 对“完全绕过 norm”说法的影响。

## C

### NN-NPP-C01
用 differential 逐步推导两个 Jacobian，不得跳过中间变量 $z$。

### NN-NPP-C02
从 $x_{\ell+1}=x_\ell+\Delta_\ell$ 推出精确展开。分别在同向增量与正交/不相关增量假设下估算 relative layer change 的深度阶。

### NN-NPP-C03
对 Sandwich 结构 $x^+=x+N_2(F(N_1(x)))$ 推导 Jacobian，并指出 identity rail 与两个 norm gates 的位置。

## D

### NN-NPP-D01
反驳“每层含 $I$，所以 Pre-Norm 不会梯度爆炸”。给出标量或共同 eigen-direction 反例。

### NN-NPP-D02
反驳“$x_L=x_0+\sum\Delta_l$ 已经证明 Pre-Norm 等价于浅而宽网络”。指出至少三个缺失条件或定义。

### NN-NPP-D03
反驳“Xiong et al. 证明 Pre-Norm 最终精度更高且永远不需 warm-up”，准确重述其证据范围。

## E

### NN-NPP-E01
设计 Pre/Post 公平消融，覆盖 final norm、初始化、residual scale、warm-up、训练预算、多 seed 与四类响应变量。

### NN-NPP-E02
给出一个 Transformer block（attention 与 FFN 两个子层）的 Pre-Norm 计算图和 Jacobian product，不能把中间状态省略。

### NN-NPP-E03
设计“有效深度”可证伪诊断：至少包含 representation change、branch/residual ratio、局部 JVP/VJP 与 layer ablation，并说明每项不能单独证明什么。

