---
type: solution
status: verified
area: [training, optimization, mup, embedding, attention]
topic: "[[Embedding、Readout、Attention 与特殊参数组缩放]]"
exercise: "[[习题 - Embedding、Readout、Attention 与特殊参数组缩放]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Embedding、Readout、Attention 与特殊参数组缩放

> [!warning] 使用边界
> 特殊参数规则绑定 lookup/forward 公式、词表/head/rank path 与 optimizer；不同实现的存储转置和共享 multiplier 需单独核对。

## A. 识别与复述

### TRN46-A01
embedding forward 只选择 $E_{i,:}$，不对 $d$ 或 $V$ 求和，梯度集中在活跃 token rows；readout 每个 logit 对 $d$ 个 hidden coordinates 求和，梯度与 $h$ 对齐。相同存储尺寸不代表相同聚合、gradient sparsity 或 width exponent。

### TRN46-A02
共享 $E$ 在输入端是 lookup，在输出端经 $E^\top$ 做 width sum；可用 readout 路径 multiplier 让有效输出权重按 $1/d$。总 gradient/moments 同时接收稀疏高频 token 项与 dense softmax 项，需要审计谁主导 Adam state、clipping 与 decay。

### TRN46-A03
bias 直接加、norm scale 逐坐标乘；Q/K 形成 $d_h$ 内积，V/O 分别做加权和与 projection；LoRA 是 $A,B$ 的乘积，尺度轴包含 $d_{in},r,d_{out}$。它们都不等于普通 $n\times n$ hidden matrix。

## B. 手算与构造

### TRN46-B01
$$
\Delta z_v=\sum_{j=1}^d1\cdot c/d=c.
$$
若 update 为 $c/\sqrt d$，则 $\Delta z_v=c\sqrt d$，随 width 爆炸；这正是训练对齐和而非随机初始化和。

### TRN46-B02
每项 $q_jk_j$ 均值 0、方差 $\mathbb Eq_j^2\mathbb Ek_j^2=4$，所以
$$
\operatorname{Var}(q^\top k)=4d_h.
$$
乘 $1/\sqrt{d_h}$ 后方差 4；乘 $1/d_h$ 后为 $4/d_h$，初始化 score 收缩。

### TRN46-B03
sum reduction：
$$
\nabla E_{1,:}=g_1+g_2+g_3,\qquad
\nabla E_{2,:}=g_4.
$$
mean over 4：
$$
\nabla E_{1,:}=(g_1+g_2+g_3)/4,\quad
\nabla E_{2,:}=g_4/4.
$$
高频 token 累积更多样本贡献；稀疏 optimizer 的 state 访问频率也不同。

## C. 推导与证明

### TRN46-C01
$z_v=\sum_jh_jW_{jv}$，softmax 有
$$
\frac{\partial L}{\partial z_v}=p_v-\mathbf1[v=t].
$$
链式法则给
$$
\frac{\partial L}{\partial W_{jv}}
=h_j\frac{\partial L}{\partial z_v}.
$$
更新含相同 $h_j$；再算 $\Delta z_v=\sum_jh_j\Delta W_{jv}$ 时出现 $\sum_jh_j^2$，按 $d$ 而非 $\sqrt d$ 聚合。

### TRN46-C02
lookup loss 对 $E$ 的梯度记 $G_{in}$。readout $z=\alpha_dhE^\top$ 给
$$
\frac{\partial L}{\partial E}
=G_{in}+\alpha_d(\nabla_zL)^\top h
$$
（按 $E\in\mathbb R^{V\times d}$ 的方向）。$\alpha_d$ 同时进入 readout forward 和 gradient；总梯度的两项具有不同 sparsity/统计。

### TRN46-C03
$$
(A+\Delta A)(B+\Delta B)-AB
=\Delta A\,B+A\,\Delta B+\Delta A\,\Delta B.
$$
左乘 $x$ 并乘 $\alpha$ 即完整 $\Delta(x\alpha AB)$。若 $B_0=0$，则 $\partial(xAB)/\partial A$ 含右因子 $B$，初始为零，所以 $\nabla A=0$；而 $\nabla B$ 仍可由 $xA$ 得到。

## D. 边界、反例与纠错

### TRN46-D01
embedding 是 row-sparse lookup，readout 是 width-sum 且需 $1/d$ effective update，norm 是 vector coordinate multiplier，LoRA 因子需看组合乘积；统一矩阵 group 会把聚合和最速范数搞错。tensor rank 只是存储属性。

### TRN46-D02
路径 A 固定 $h$、令 $d_h$ 加倍，dot product 项数加倍，score multiplier应随 $d_h$ 变；路径 B 固定 $d_h$、令 head 数加倍，每头 score scale 不变，变化发生在 concat/output projection。两者 $d_{model}$ 都加倍。

### TRN46-D03
$1/\sqrt{d_h}$ 保持独立随机 q/k 的初始 score variance；$1/d_h$ 控制训练后可能对齐的 dot-product update。前者失败可表现为 width 增大后 feature-update/score 爆炸，后者若没有训练对齐或 LR错误则 score 始终消失、attention近均匀。判断需绑定参数化阶段。

## E. AI 迁移

### TRN46-E01
manifest 应对 shared embedding/head 指定存储 init、readout multiplier、shared optimizer state 与 row/logit telemetry；Q/K/V/O 分列 orientation、attention multiplier、LR；FFN up/down 按 non-square hidden；bias/norm单独 optimizer/decay；所有组保存 actual LR、update RMS、feature/logit/entropy 和 spectral proxy。

### TRN46-E02
做 $2\times2\times2$ 子实验：head path（固定 $h$/固定 $d_h$）× scaling（$1/\sqrt{d_h}$/$1/d_h$）× query init（随机/zero），在至少两种 sequence length 上重复。固定 token/compute/optimizer，记录 q/k RMS、score RMS、entropy、feature update、loss与失败；sequence length作为 block或显式交互。

### TRN46-E03
规定 $d_{in},d_{out}$ 随 width 的路径、rank 固定或 $r(n)$；声明 A/B 谁 zero-init、alpha/r convention；逐因子记录 gradient、direction、LR和 $\Delta A,\Delta B$，同时记录 $\Delta(AB)$ 与 $x\Delta(AB)$。结论只覆盖该 rank/path/base weight 是否冻结的设置。

## 无提示重做

- [ ] 48 小时后推导 tied readout 总梯度。
- [ ] 一周后从两条 head path 判断 attention multiplier。
