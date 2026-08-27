---
type: solution
status: draft
area: [architecture, transformer, residual, normalization, feed-forward]
topic: "[[Transformer Block、残差、归一化与 FFN]]"
exercise: "[[习题 - Transformer Block、残差、归一化与 FFN]]"
sources: ["[[S-2020-Xiong-Transformer-LayerNorm]]", "[[S-2022-Wang-DeepNet]]", "[[S-2022-Su-8994-Why-Residual]]", "[[S-2022-Su-9009-PreNorm-PostNorm]]", "[[S-2026-Chen-Attention-Residuals]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Transformer Block、残差、归一化与 FFN

## A. 识别与复述

### ARCH-BLOCK-A01
令 $X\in\mathbb R^{B\times T\times d}$。Pre-Norm block 可写成
$$
U=X+\mathcal D_a(\operatorname{MHA}(\operatorname{LN}_1(X))),
\qquad
Y=U+\mathcal D_f(\operatorname{FFN}(\operatorname{LN}_2(U))).
$$
LN、MHA、分支 dropout、相加及 FFN 最终输出都保持 $(B,T,d)$；FFN 内部暂时扩为 $(B,T,d_{ff})$。

### ARCH-BLOCK-A02
Self-attention 对每个 query 沿 token/key 轴加权汇总，完成 token mixing。Position-wise FFN 对每个 token 行独立使用同一组权重，在 feature/channel 轴完成非线性变换。FFN 虽不直接跨 token，其输入已含 attention 汇入的上下文。

### ARCH-BLOCK-A03
Attention dropout 通常作用于 attention weights 或 attention 内部；residual dropout 作用在整个分支输出、与主路相加之前；DropPath 以样本—分支/层为随机单位把整条 residual branch 置零。三者的 mask shape、方差与 eval 合同不同。

## B. 手算与建模

### ARCH-BLOCK-B01
$dd_{ff}=512\cdot2048=1{,}048{,}576$。普通 FFN 有两矩阵，主权重为 $2{,}097{,}152$；同宽三矩阵门控 FFN 为 $3{,}145{,}728$。Bias 未计。

### ARCH-BLOCK-B02
Pre-Norm：$y=x+a(cx)=(1+ac)x$，故 $dy/dx=1+ac$。Post-Norm：$y=c(x+ax)=c(1+a)x$，故 $dy/dx=c(1+a)$。标量线性例只展示 wiring 差异，不代表真实 LayerNorm 是常数倍映射。

### ARCH-BLOCK-B03
不能相加，因为末维 $512\ne768$。最小修正是在 attention 输出后加 $W_O\in\mathbb R^{512\times768}$，把分支投影到 $(8,128,768)$；另一选择是投影主路，但会改变 residual stream 合同。

## C. 推导与证明

### ARCH-BLOCK-C01
对 $y_{pre}=x+F(N(x))$，微分为
$$
dy=[I+J_F(N(x))J_N(x)]dx.
$$
对 $y_{post}=N(x+F(x))$，
$$
dy=J_N(x+F(x))[I+J_F(x)]dx.
$$
Pre 的恒等项不被 $J_N$ 左乘；Post 的整条相加结果都经过 normalization Jacobian。这是精确链式法则，不是全深度范数界。

### ARCH-BLOCK-C02
若 $x_{l+1}=x_l+F_l(N(x_l))$，逐层代入得
$$
x_L=x_0+\sum_{l=0}^{L-1}F_l(N(x_l)).
$$
它证明 residual stream 是历层增量之和；没有证明增量独立、同分布、相互正交、范数有界、最终表示“等效较浅”，更没有证明下游质量。

### ARCH-BLOCK-C03
令增量 $\Delta_l$ 独立、零均值、每个方向方差 $\sigma^2$，缩放 $\varepsilon=1/\sqrt L$：
$$
\operatorname{Var}\Big(\sum_l\varepsilon\Delta_l\Big)
=L\varepsilon^2\sigma^2=\sigma^2.
$$
但若只知 $\|\Delta_l\|\le M$，三角不等式给
$$
\Big\|\sum_l\varepsilon\Delta_l\Big\|\le\sqrt L\,M.
$$
确定性最坏界要用 $\varepsilon=O(1/L)$ 才为 $O(M)$；两种尺度对应不同相关性假设。

## D. 边界、反例与纠错

### ARCH-BLOCK-D01
$J_l=I+A_l$ 的乘积仍可能爆炸或退化。例如一维 $A_l=a>0$ 时总 Jacobian 是 $(1+a)^L$；若 $a=-1$，单层可变为 0。恒等项只是提供直通结构，稳定还需控制 $A_l$ 的谱、相关性、normalization、初始化和训练更新。

### ARCH-BLOCK-D02
取两个标量 tokens $(x_1,x_2)$。先让 attention 输出每个位置的均值 $m=(x_1+x_2)/2$；再令逐位置 FFN 为 $f(z)=z^2$。位置 1 输出 $m^2$，显然依赖 $x_2$，尽管 FFN 本身没有读取另一行。

### ARCH-BLOCK-D03
至少有：千层成功是特定协议的实验而非跨任务定理；DeepNorm 系数依 encoder/decoder 结构；同层数会改变参数、FLOPs 与优化预算；能训练不等于最终 loss/迁移更好；任务数据和 context 不同；硬件与通信成本可能不可接受；论文比较范围不能外推所有 norm/FFN/position 变体。

## E. AI 迁移

### ARCH-BLOCK-E01
固定 tokenizer、数据顺序、训练 token、总参数、层宽、FFN、position、optimizer、精度与评价；分别为 Pre/Post 调合理 initialization、residual scale、warm-up 与学习率，并报告这些搜索预算。多 seed 记录 loss curve、梯度/更新范数、失败率、最终/迁移指标、FLOPs、吞吐与显存。结论分为可训练性、收敛速度、最终质量和系统效率。

### ARCH-BLOCK-E02
测试：零分支时输出严格等于主路；branch shape 不合时报错；train mode 固定 RNG 可复现、不同 seed 可变化；eval mode dropout/DropPath 关闭且重复输出相同；checkpoint on/off 在相同 RNG 合同下输出和梯度近似一致；把分支置零时 norm 不应意外改动 Pre-Norm 主路；统计随机 mask 的样本/层粒度。

### ARCH-BLOCK-E03
卡片记录论文/代码 commit 与日期、模型/数据/预算、三种接线、depth-history 保存方式、Block summary 规则、额外参数/FLOPs/activation/communication、初始化与 optimizer。分别报告 scaling curve、消融、多 seed、失败率和 serving 代价；full/block 结果不可互换。把“depth routing 可能改善信息访问”标 H、特定协议结果标 E，不把 weights 当因果归因。
