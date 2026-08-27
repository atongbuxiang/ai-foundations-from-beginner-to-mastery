---
type: solution
status: draft
area: [architecture, efficient-attention, low-rank, compression]
topic: "[[低秩投影与序列维压缩 Attention]]"
exercise: "[[习题 - 低秩投影与序列维压缩 Attention]]"
sources: ["[[S-2020-Wang-Linformer]]", "[[S-2025-Su-10847-矩阵的有效秩]]", "[[S-2021-Su-8610-线性Transformer反例]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - 低秩投影与序列维压缩 Attention

## A. 识别与复述

### ARCH-LOWRANK-A01
Feature/head 低秩压缩每个 token 的通道；sequence 压缩把 $n$ 个 token 投到 $k$ 个槽；logit matrix $QK^\top$ 的秩受 $d_h$ 限制；softmax 后 attention matrix 因逐行非线性与归一化可有不同秩。四者的轴、对象和误差不同，不能用“低秩”一词互换。

### ARCH-LOWRANK-A02
对单头 $K,V\in\mathbb R^{n\times d_h}$，令 $E,F\in\mathbb R^{k\times n}$：
$$K'=EK,\quad V'=FV\in\mathbb R^{k\times d_h},$$
$$O=\operatorname{softmax}(QK'^\top/\sqrt{d_h})V'\in\mathbb R^{n\times d_h}.$$
score 从 $n\times n$ 变为 $n\times k$。

### ARCH-LOWRANK-A03
结合律重排要求同一因子乘积、在实数算术中函数不变。投影 $E,F$ 把 $n$ 维序列映到 $k<n$，一般有非零核并丢失信息；除非输入恰落在保留子空间，否则不是恒等变换。

## B. 手算与建模

### ARCH-LOWRANK-B01
Dense 主 MAC 为 $n^2d_h=1024^2\cdot128=134{,}217{,}728$，score 有 $1{,}048{,}576$ 标量。压缩 score 为 $nkd_h=1024\cdot64\cdot128=8{,}388{,}608$ MAC，$65{,}536$ 标量，均为 dense 的 $1/16$；还必须另计 $EK,FV$ 的投影成本。

### ARCH-LOWRANK-B02
最佳 rank-2 保留 8、4。谱范数误差是下一奇异值 $2$；Frobenius 误差为 $\sqrt{2^2+1^2+0.5^2}=\sqrt{5.25}\approx2.291$。

### ARCH-LOWRANK-B03
若 $K=(k_{ij})$，则
$$K'_{a\ell}=\sum_{j=1}^{4}E_{aj}K_{j\ell},\quad a=1,2,\ \ell=1,2.$$
$E$ 的 4 列索引原 token/sequence positions，2 行索引压缩槽；它不是在 feature 维右乘。

## C. 推导与证明

### ARCH-LOWRANK-C01
用 $\|AB\|_F\le\|A\|_2\|B\|_F$，取 $A=Q,B=(K-\hat K)^\top$，并用转置保持 Frobenius 范数即得。除以 $\sqrt{d_h}$ 可界 logit perturbation；它不自动控制 softmax 后权重、V 聚合、后续层或最终任务损失。

### ARCH-LOWRANK-C02
若奇异值 $\sigma_1\ge\cdots$，最佳 rank-$k$ 的谱误差为 $\sigma_{k+1}$，Frobenius 误差为 $(\sum_{i>k}\sigma_i^2)^{1/2}$。逐样本 SVD 可按当前矩阵选最优子空间；shared learned projection 要跨样本/层/位置工作，还受优化和参数化限制，故不必达到该 oracle。

### ARCH-LOWRANK-C03
令 $n=2$，第二个 value 为未来变量 $v_2$。若第一压缩槽 $V'_1=v_1+v_2$，位置 1 的 query 即使只读槽 1，输出也依 $v_2$。把 $v_2$ 改变而保持前缀不变，位置 1 输出改变，构成 causal leakage。

## D. 边界、反例与纠错

### ARCH-LOWRANK-D01
取单行 logits $z=(0,0)$ 与 $z'=(\epsilon,-\epsilon)$，Frobenius 距离 $\sqrt2\epsilon$ 可小，但当任务在近乎平局处用 argmax，预测从 tie 变为第一类；若下游对 margin 很敏感，决策变化显著。更高维中可让许多微小扰动累积。范数小只给连续性尺度，不保证离决策边界远。

### ARCH-LOWRANK-D02
平均值可掩盖稀有高秩样本；层/头的谱不同，长度变化会出现新模式，同一个 $k$ 还可能对关键 retrieval 行不足。安全声明至少需分层、分头、分样本/长度报告谱尾和任务失败分位数，而不是只有平均有效秩。

### ARCH-LOWRANK-D03
矩阵列数与训练位置绑定，测试多出的 positions 没有权重。可声明：对 $E$ 插值/外推；按块重复或使用 convolutional/shared projection；重新参数化为长度无关函数生成 $E_{aj}$。每种都定义了新行为，必须训练/评测而不能默认。

## E. AI 迁移

### ARCH-LOWRANK-E01
在早中晚层、不同 heads、随机与困难样本、训练内外多长度采样 logits/attention/K/V；报告 singular-value curves、rank-$k$ 谱/Frobenius 尾、逐行 softmax/output 误差及 p50/p90/p99。再关联 retrieval position、margin 和最终 logits，避免只看平均谱。

### ARCH-LOWRANK-E02
构造两条序列前缀完全相同、仅未来 token/value 不同；eval mode 比较每个前缀位置输出，必须严格在容差内相同。错误 $E$ 故意混合未来列作为负对照应失败；覆盖所有 blocks、padding 与 chunk 边界。

### ARCH-LOWRANK-E03
Dense 给真实质量；逐样本最佳 SVD 是不可部署 oracle，测可压缩上限；learned projection 测参数化与优化；随机 projection 给非学习基线。固定 $k$、数据、训练预算与 kernel，分别报告 matrix/output/任务误差、投影成本、长外推和因果测试。
