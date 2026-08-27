---
type: exercise
status: draft
area: [learning-theory/empirical-process, probability/symmetrization]
topic: "[[Ghost Sample、对称化与经验过程入口]]"
difficulty: [A, B, C, D, E]
prerequisites: ["[[VC 一致收敛与泛化界]]", "[[协方差、相关性与条件期望]]"]
related: ["[[解答 - Ghost Sample、对称化与经验过程入口]]", "[[Rademacher 复杂度与经验复杂度]]"]
solution: "[[解答 - Ghost Sample、对称化与经验过程入口]]"
created: 2026-08-23
updated: 2026-08-23
---

# 习题 - Ghost Sample、对称化与经验过程入口

> [!abstract] 训练目标
> 能逐步重建 conditional Jensen—pairwise exchange—Rademacher split，区分 one-sided/absolute 与 expectation/high-probability，并识别真实 AI 数据管线中 exchangeability 和 additive sample unit 的断点。

## A. 识别与复述

### LT-SYM-A01

定义 $P,P_m,P_m'$，写出 $S,S'$ 的联合分布与独立关系。ghost sample 在证明和算法中分别扮演什么角色？

### LT-SYM-A02

写出 one-sided expectation symmetrization theorem，并说明本节 Rademacher complexity 使用的 normalization 与 supremum convention。

### LT-SYM-A03

解释 inequality、distributional equality 和 subadditivity 在三步证明中各出现在哪里。

## B. 手算与数值判断

### LT-SYM-B01

固定 $m=2$，$f_1(S)=(0,0)$、$f_2(S)=(1,0)$。枚举四组 signs 并计算 $\widehat{\mathfrak R}_S(\{f_1,f_2\})$。

### LT-SYM-B02

若 $f\in[0,1]$、$m=2000,\delta=0.05$，计算从 population complexity 版本得到的 confidence term

$$
\sqrt{\frac{\log(1/\delta)}{2m}}.
$$

若 $\mathfrak R_m=0.04$，one-sided gap 上界是多少？

### LT-SYM-B03

对均匀分布在 $\{a,b\}$ 上的 $P$ 和 $m=1$，取 $f_a=\mathbf1\{z=a\}$、$f_b=\mathbf1\{z=b\}$。计算 $\mathbb E_S\sup_f(Pf-P_1f)$，并与 $2\mathfrak R_1(\mathcal F)$ 比较。

## C. 推导与证明

### LT-SYM-C01

从 $Pf=\mathbb E_{S'}P_m'f$ 出发，严格证明

$$
\mathbb E_S\sup_f(Pf-P_mf)
\le\mathbb E_{S,S'}\sup_f(P_m'f-P_mf).
$$

### LT-SYM-C02

定义 pairwise-swapped $(\widetilde S,\widetilde S')$，证明其与 $(S,S')$ 同分布，并推出 signed double-sample equality。

### LT-SYM-C03

完成从 double-sample signed process 到 $2\mathfrak R_m(\mathcal F)$ 的拆分；随后用 symmetric hull 推出 absolute-gap 版本。

## D. 边界、反例与纠错

### LT-SYM-D01

给出一个随机族 $X_f$，使

$$
\sup_f\mathbb EX_f<\mathbb E\sup_fX_f,
$$

说明 Jensen 步一般不能写等号。

### LT-SYM-D02

构造两个 dependent variables $(Z,Z')$，使交换后联合分布改变。指出 pairwise sign 插入为何失效。

### LT-SYM-D03

反驳：“对称化得到期望上界，所以由把 $\mathbb E$ 删除即可得到每个样本的上界。”给出正确升级路线。

## E. AI 迁移

### LT-SYM-E01

一个 image 有 8 个 correlated augmentations。说明为什么把 8 个 views 当 8 个 iid $Z_i$ 会错误缩小复杂度/置信项，并给出正确 sample unit。

### LT-SYM-E02

InfoNCE 的每项依赖同一 batch 的 negatives。解释普通 additive symmetrization 哪一步不再直接成立，并提出 batch-level 或 U-statistic 分析对象。

### LT-SYM-E03

为自适应 prompt evaluation 写出训练样本、ghost sample、算法随机种子和 Rademacher signs 四类随机对象，说明不能混用的原因。
