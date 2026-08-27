---
type: solution
status: verified
area: [language-models, peft, lora]
topic: "[[LoRA 的低秩更新、初始化、缩放与合并]]"
exercise: "[[习题 - LoRA 的低秩更新、初始化、缩放与合并]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - LoRA 的低秩更新、初始化、缩放与合并

## A. 识别与复述

### LM29-A01
$W_0\in\mathbb R^{m\times n}$、$A\in\mathbb R^{r\times n}$、$B\in\mathbb R^{m\times r}$。列向量约定下 $y=W_0x+sB(Ax)=(W_0+sBA)x$；$W_0$ frozen，$A,B$ trainable。

### LM29-A02
它排除：整个 $W_0+\Delta W$ 必须低秩；整个深网函数是 rank-$r$；任意 full-finetuning update 本身天然 rank-$r$。只有所选线性层的增量 $BA$ 有 rank 至多 $r$。

### LM29-A03
LoRA 直接解 $\min_{A,B}\mathcal L(W_0+sBA)$，从训练开始就限制路径。截断 SVD 需先已有 full update $\Delta W^*$，再求其最佳 rank-$r$ 逼近；两者的目标、数据路径和优化误差不同。

## B. 手算与构造

### LM29-B01
Full 参数 $mn=6\cdot4=24$。LoRA 参数 $r(m+n)=2(6+4)=20$；这个小 shape 下只省 4。$\operatorname{rank}\Delta W\le2$。参数节省只有在 $r\ll m,n$ 时明显。

### LM29-B02
$A=I_2$，$B=\operatorname{diag}(2,3)$，故 $BA=\operatorname{diag}(2,3)$，$\Delta W=.5BA=\operatorname{diag}(1,1.5)$。对 $x=(1,2)^\top$，增量输出 $\Delta Wx=(1,3)^\top$。

### LM29-B03
取 $\Delta W_1=e_1e_1^\top=\begin{bmatrix}1&0\\0&0\end{bmatrix}$、$\Delta W_2=e_2e_2^\top=\begin{bmatrix}0&0\\0&1\end{bmatrix}$，各 rank 1；和为 $I_2$，rank 2。多 adapter 和的 rank 可增长。

## C. 推导与证明

### LM29-C01
$d\mathcal L=\langle G,d\Delta W\rangle_F=s\langle G,dB\,A+B\,dA\rangle_F$。用 trace 循环：$s\langle GA^\top,dB\rangle_F+s\langle B^\top G,dA\rangle_F$，故 $\nabla_B=sGA^\top,\nabla_A=sB^\top G$。

### LM29-C02
若 $B=0,A$ 随机，$\nabla_A=sB^\top G=0$，而 $\nabla_B=sGA^\top$ 一般非零；B 先移动。若 $A=B=0$，两式均为 0，纯梯度法停在双线性静止点。

### LM29-C03
由矩阵乘法分配律：$W_0x+sB(Ax)=(W_0+sBA)x=W_*x$。若有 bias，两边共享同 bias 仍成立。浮点运算顺序、量化和错误 transpose 会引入差异，因此实现以容差测试。

## D. 边界、反例与纠错

### LM29-D01
还缺 target modules/layers、矩阵 orientation、scale convention/alpha、initialization、A/B learning rates、dropout、bias/norm、dtype、base hash 和 merge status。相同 rank 可是完全不同可达函数与预算。

### LM29-D02
对非零 $c$，$(cB)(A/c)=BA$，但 weight decay 分别惩罚 $c^2\|B\|^2+\|A\|^2/c^2$；A/B 不同学习率也随尺度改变乘积更新。因此相同初始 $\Delta W$ 不保证相同优化路径。

### LM29-D03
Frozen base 仍占存储并完成前向；activations、temporary、dataloader 和部分通信不按 trainable count 缩放。LoRA 还加中间 matmuls。只能分别测 weights/grads/optimizer/activations/peak 与 wall time。

## E. AI 迁移

### LM29-E01
生成多个 shape/batch/dtype 的 $x$；比较 base+adapter 与 materialized $W_*$ logits/loss/grad-input；覆盖 bias、fan-in/out、scale；merge→unmerge 检查 base/A/B；量化另设较宽 tolerance 与 post-merge task eval。

### LM29-E02
保存 base/tokenizer/template hashes、target module names/shapes、r/alpha/s formula、A/B init/LR、optimizer/decay/dropout/bias、dtype、trainable/total counts、weights/grads/optimizer/activation/peak bytes、tokens/s 和 merge artifact hash。

### LM29-E03
无法复建 $\Delta W$ 的 shape/层范围或有效 scale；不同库可用 $\alpha/r$、其他归一化与 transpose。参数量、梯度和效果均不可归因。结论应降级为“某未完整指定 LoRA 配方”。

## 无提示重做

- [ ] 推导 $\nabla_A,\nabla_B$ 并解释三种零初始化。
- [ ] 手算参数量、rank 上界与 merge 等价。

