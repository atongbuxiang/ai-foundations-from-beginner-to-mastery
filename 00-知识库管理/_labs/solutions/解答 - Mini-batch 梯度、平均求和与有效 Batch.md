---
type: solution
status: verified
area: [training, optimization, statistics]
topic: "[[Mini-batch 梯度、平均求和与有效 Batch]]"
exercise: "[[习题 - Mini-batch 梯度、平均求和与有效 Batch]]"
created: 2026-08-26
updated: 2026-08-26
---

# 解答 - Mini-batch 梯度、平均求和与有效 Batch

## A. 识别与复述

### TRN02-A01
$G=N^{-1}\sum_i g_i$；$\widehat G_B^{mean}=B^{-1}\sum_jg_{I_j}$；$\widehat G_B^{sum}=\sum_jg_{I_j}=B\widehat G_B^{mean}$。均匀 iid 抽样下，前两者期望为 $G$，sum 的期望为 $BG$。

### TRN02-A02
Variance 是 squared deviation 的期望，按 $1/B$；standard deviation 与原量同单位，是 variance 的平方根，按 $1/\sqrt B$。例如 $B$ 增四倍，variance 降到四分之一，standard deviation 只降到二分之一。

### TRN02-A03
Nominal batch 是计数；effective batch 是在指定 estimator variance 下等效的独立等权样本数；critical batch 是某训练目标和协议下并行收益开始递减的经验尺度。三者的定义层次不同。

## B. 手算与构造

### TRN02-B01
$G=(-1+1+3+5)/4=2$。Centered values 为 $-3,-1,1,3$，所以 $C=(9+1+1+9)/4=5$。With replacement $B=2$ 的 mean variance 为 $5/2=2.5$。

### TRN02-B02
公式给 $(N-B)C/[B(N-1)]=(4-2)5/[2(3)]=5/3$。当 $B=N=4$ 时分子为 0，variance 为 0，与 full gradient 确定相符。

### TRN02-B03
$\sum a_i^2=.64+.01+.01=.66$，故 $B_{eff}=1/.66\approx1.515$。最大权重 0.8 让一个样本主导 estimator，无法获得三个等权独立样本的方差缩减。

## C. 推导与证明

### TRN02-C01
令 $\xi_j=g_{I_j}-G$。则

$$\operatorname{Cov}(\widehat G_B)=B^{-2}\sum_{jk}\mathbb E[\xi_j\xi_k^T].$$

独立且 centered 使 $j\ne k$ 的项等于 $\mathbb E\xi_j\,\mathbb E\xi_k^T=0$；$B$ 个对角项各为 $C$，结果是 $C/B$。

### TRN02-C02
Mean update 是 $-\eta_{mean}\widehat G$；sum update 是 $-\eta_{sum}B\widehat G$。对所有 $\widehat G$ 相同要求 $\eta_{mean}=B\eta_{sum}$，即 $\eta_{sum}=\eta_{mean}/B$。

### TRN02-C03
$\widehat G_w-G=\sum_i a_i\xi_i$，因此 covariance 为 $\sum_{ij}a_ia_jE[\xi_i\xi_j^T]$。独立 centered 消去 cross terms，同 covariance 给 $C\sum_i a_i^2$。若 heteroscedastic，则变为 $\sum_i a_i^2C_i$；若相关还要加 cross covariance。

## D. 边界、反例与纠错

### TRN02-D01
令两个“样本”gradient 完全相同：$g_1=g_2=Z$，$\operatorname{Var}Z=C$。平均仍是 $Z$，variance 为 $C$ 而非 $C/2$。独立性删除后 cross covariance 不为零。

### TRN02-D02
Sequence A 有 1 token、gradient 0；sequence B 有 3 tokens、每 token gradient 2。Sequence-mean 是 $(0+2)/2=1$；token-mean 是 $(0+2+2+2)/4=1.5$。二者优化不同目标。

### TRN02-D03
若 DDP 对 rank gradients 求和而非平均、各 rank 重复同样样本、shards 强相关、存在 uneven masks，world size 翻倍并不对应独立等权样本翻倍。还需检查 local reduction、all-reduce scaling 和真实有效 token。

## E. AI 迁移

### TRN02-E01
Global sequences $=4\times8\times16=512$；tokens $=512\times1024=524{,}288$。这是假定无 padding/mask 且每 accumulation window 完整。

### TRN02-E02
固定有限 gradients 与参数，针对多个 $B$ 重复至少数万次随机抽 batch，估计 sample covariance，比较 $B\widehat C_B$ 是否恒定；无放回时比较 $(1-B/N)S/B$。使用多个 RNG seeds、矩阵 Frobenius relative error 与方向 variance CI，并检查 $B=1,N$ 端点。

### TRN02-E03
应问：单位是样本/sequence/token？local 还是 global？world size？accumulation？padding 后有效数？mean/sum/weighted reduction？replacement/shuffle？数据是否重复/相关？最后窗口？DDP sum/mean？BN stats batch？LR 是否共同缩放？比较固定 steps 还是 tokens？

## 无提示重做

- [ ] 推导 iid 与 without-replacement 两条 covariance 公式。
- [ ] 给一个 token weighting 的反例并写单元测试。
