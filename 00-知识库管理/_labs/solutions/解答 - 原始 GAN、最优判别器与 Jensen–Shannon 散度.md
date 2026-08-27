---
type: solution
status: draft
topic: "[[原始 GAN、最优判别器与 Jensen–Shannon 散度]]"
exercise: "[[习题 - 原始 GAN、最优判别器与 Jensen–Shannon 散度]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 原始 GAN、最优判别器与 Jensen–Shannon 散度
## A. 识别与复述
### GEN18-A01
$D^*=p/(p+q)$，$V(D^*)=-\log4+2JS(P\|Q)$；全局最小在 $P=Q$。
### GEN18-A02
需 population expectations、固定 $G$、逐点自由/足够函数类且 $D$ 达 best response。实际 current critic 不满足时不能代回。
### GEN18-A03
常数 underfit critic、过强正则或未训练也给 $1/2$；需同时检验 capacity、held-out loss 与 generator coverage。
## B. 手算与建模
### GEN18-B01
$D^*=(.8/1.2,.2/.8)=(2/3,1/4)$。
### GEN18-B02
$M=(.6,.4)$。$KL(P\|M)=.8\log(4/3)+.2\log(.5)$；$KL(Q\|M)=.4\log(2/3)+.6\log(1.5)$；JS 是二者一半，$V=-\log4+2JS$。
### GEN18-B03
两 KL 到 mixture 都为 $\log2$，JS=$\log2$，故 $V(D^*)=0$。
## C. 推导与证明
### GEN18-C01
$f'(d)=p/d-q/(1-d)=0$ 得 $d=p/(p+q)$；$f''<0$ 确为最大。
### GEN18-C02
令 $m=(p+q)/2$，将 $\log[p/(p+q)]=\log[p/m]-\log2$，两项积分各给 KL 与 $-\log2$。
### GEN18-C03
取 $\mu=P+Q$，以 $p=dP/d\mu,q=dQ/d\mu$ 重复逐点推导；无需 ambient density。
## D. 边界、反例与纠错
### GEN18-D01
限制 critic class 只有常函数 $D\equiv1/2$；任意 $P\ne Q$ 也输出一半。
### GEN18-D02
JS 等式要求每个 $\theta$ 的 exact $D^*_\theta$；有限 $D_{\psi_t}$ 同时移动，且 non-sat surrogate 另改梯度。
### GEN18-D03
高容量网络可记住两个有限样本集合；新样本上可为随机。需 held-out generalization。
## E. AI 迁移
### GEN18-E01
枚举每格 $p_i,q_i$，算 $D_i^*$、$m_i$、两 KL 与 value，并断言 identity。
### GEN18-E02
冻结 $G$ 后把 critic 训练到多种预算；增加 capacity、held-out classification。若仍无法区分且独立 two-sample test/coverage 一致，才支持 equilibrium。
### GEN18-E03
非等先验用 $\pi p/(\pi p+(1-\pi)q)$；label smoothing改变 target proper score 与最优输出，不再直接是原 density-ratio mapping。

