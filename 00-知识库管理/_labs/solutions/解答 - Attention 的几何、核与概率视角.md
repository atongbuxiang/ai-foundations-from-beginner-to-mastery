---
type: solution
status: draft
area: [architecture, attention, kernels, probability]
topic: "[[Attention 的几何、核与概率视角]]"
exercise: "[[习题 - Attention 的几何、核与概率视角]]"
sources: ["[[S-2021-Choromanski-Performer]]", "[[S-2021-Su-8601-无限维线性Attention与核特征]]"]
created: 2026-08-24
updated: 2026-08-24
---

# 解答 - Attention 的几何、核与概率视角

## A. 识别与复述

### ARCH-GKP-A01
$q^Tk=\|q\|\|k\|\cos\theta$。L2-normalized cosine score 将两向量 norm 固定为 1，删除 norm/scale 通道，只保留方向；temperature 仍可整体调节 logits。

### ARCH-GKP-A02
固定 i，$a_{ij}=p(J=j\mid q_i,K,\mathcal V(i))$，$\sum_j a_{ij}=1$；输出 $o_i=\sum_ja_{ij}v_j=E[v_J\mid q_i,K,\mathcal V(i)]$。

### ARCH-GKP-A03
PSD kernel 需要同一集合上的对称函数，任意有限 Gram matrix 半正定；同一 feature map $K(x,y)=\langle\phi(x),\phi(y)\rangle$ 自动满足。一般 $\phi(q)^T\varphi(k)$ 可非对称、两域不同，只是低秩 affinity，不自动是 RKHS kernel。

## B. 手算与建模

### ARCH-GKP-B01
用自然对数，$H=-[.5\ln.5+.25\ln.25+2(.125\ln.125)]\approx1.213$；$e^H\approx3.364$。Collision $=.25+.0625+2(.015625)=.34375$。

### ARCH-GKP-B02
若共同 $\cos\theta=c$，dot scores 分别为 $2\cdot1c=2c$ 与 $2\cdot3c=6c$；cosine scores 都为 c。若 c 为负，norm 大者更负，也说明“更大 norm”并不总是更高 score。

### ARCH-GKP-B03
Affinities 为 $2$ 与 $3$，分母 5；输出 $(2\cdot3+3\cdot7)/5=27/5=5.4$。要求 affinities 非负且分母非零才能解释为凸权重。

## C. 推导与证明

### ARCH-GKP-C01
$e^{q^Tk}=\sum_{n\ge0}(q^Tk)^n/n!$，而 $(q^Tk)^n=\langle q^{\otimes n},k^{\otimes n}\rangle$。将 $\phi(q)=(1,q,q^{\otimes2}/\sqrt{2!},\ldots)$ 拼接，inner product 逐块求和即指数；有限 q/k 下指数级数绝对收敛。

### ARCH-GKP-C02
令 affinity $\phi(q_i)^T\varphi(k_j)$。分子
$\sum_j\phi(q_i)^T\varphi(k_j)v_j^T=\phi(q_i)^T[\sum_j\varphi(k_j)v_j^T]$，分母同理为 $\phi(q_i)^T\sum_j\varphi(k_j)$。构造状态约 $O(Trd_v)$ work、$O(rd_v+r)$ state，再用 queries 约 $O(Trd_v)$；feature map 成本另计。

### ARCH-GKP-C03
$$\hat n/\hat d-n/d=(\hat n-n)/\hat d+n(d-\hat d)/(d\hat d).$$
取范数得 $\le\|\hat n-n\|/\hat d+\|n\||\hat d-d|/(d\hat d)$。需 $d,\hat d$ 有正下界，才能把 kernel误差稳定传播；否则 reciprocal 放大。

## D. 边界、反例与纠错

### ARCH-GKP-D01
在同一两点集令 $\phi(x)=(x,1)$，$\varphi(y)=(1,y)$。$K(x,y)=x+y$ 恰对称；为更直接取标量 $\phi(x)=x,\varphi(y)=1$，则 $K(x,y)=x$，一般 $K(x,y)\ne K(y,x)$，不能形成对称 PSD Gram。它仍可作 query-key 双域 affinity。

### ARCH-GKP-D02
取 exact $n=d=10^{-6}$，故输出 1；令 $\hat n=10^{-6}$、$\hat d=2\cdot10^{-6}$，absolute denominator error 仅 $10^{-6}$，近似输出却为 .5，误差 .5。相对分母误差才是关键，且需要正下界。

### ARCH-GKP-D03
构造 shortcut token 总与训练标签相关，attention 几乎 one-hot 指向它，训练准确高但 OOD 相关性翻转后失败；热图很集中却不忠实于稳健机制。另一方面求全局平均任务的均匀 attention 是正确解。集中性不单调决定质量或解释。

## E. AI 迁移

### ARCH-GKP-E01
层 1 kernel：采样 q/k，按 r 测 entrywise/relative/Frobenius error 与随机方差；层 2 output：含真实 V/mask，测 numerator、denominator、normalized output 和梯度误差；层 3 system/quality：同训练预算扫描 T/r/d、dtype、memory、prefill/decode latency 与任务指标，多 seed。只有三层共同满足才可声称替代。

### ARCH-GKP-E02
对每行按可见数 $m_i$ 报 $H/\log m_i$、effective support/$m_i$、top-k mass（固定 k 与固定比例两版）、max 与 $\sum a^2$。按 layer/head/query class/length 分布报告而非挑图；同步记录任务/干预，避免跨不同 mask 的 raw entropy 误比。

### ARCH-GKP-E03
维护 $S_{V,i}=S_{V,i-1}+\varphi(k_i)v_i^T$、$s_i=s_{i-1}+\varphi(k_i)$；在 document/segment 边界按合同 reset，不能让前段泄漏。检查 denominator 最小值/epsilon、state norm、累积误差与不同 scan 顺序；跨 dtype/长度与 exact causal baseline 比 output/gradient，并记录 state memory。
