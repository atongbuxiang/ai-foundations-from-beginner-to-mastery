---
type: solution
status: draft
area: [generative-models, vae, information-theory]
topic: "[[Posterior Collapse、率失真与解码器容量]]"
exercise: "[[习题 - Posterior Collapse、率失真与解码器容量]]"
created: 2026-08-25
updated: 2026-08-25
---

# 解答 - Posterior Collapse、率失真与解码器容量

## A. 识别与复述

### GEN14-A01
完整 collapse：$q(z\mid x)=p(z)$ 几乎处处；维度级：仅部分 $z_j$ 无关；近似：相应 KL/MI 很小；decoder-ignore：改变 $z$ 几乎不改 $p_\theta(x\mid z)$。最后一种可与 encoder 正 rate 同时发生。

### GEN14-A02
$q(z)=\int p_*(x)q(z\mid x)dx$；$R=E_xKL(q(z\mid x)\|p(z))$；$D=-E_{x,z}\log p_\theta(x\mid z)$；$I_q(X;Z)=E_xKL(q(z\mid x)\|q(z))$。

### GEN14-A03
结构性 collapse 是模型最优解中 decoder 不需要 $z$；动力学 collapse 是 encoder 早期落后、decoder 先学会绕过 $z$，使后续信号减弱。前者改训练速度未必消失，后者可能由更新调度改善。

## B. 手算与建模

### GEN14-B01
$R=.7+.3=1.0$ nat。只知 $R$ 不能反推出 MI；MI 可在 $[0,R]$，剩余由 aggregate KL 承担。

### GEN14-B02
条件分布对所有 $x$ 相同，故 $I_q=0$；aggregate $q=N(2,1)$，到 $N(0,1)$ 的 KL 为 $2$；所以 rate $R=2$。

### GEN14-B03
$\beta=.5$ 时目标分别为 $100$、$80+.5(30)=95$，第二个好；$\beta=1$ 时为 $100$、$110$，第一个好。权重改变选择的 rate–distortion 点。

## C. 推导与证明

### GEN14-C01
在 rate 中加减 $\log q(z)$：
$$
\begin{aligned}
R&=\iint q(x,z)\log\frac{q(z\mid x)}{p(z)}dxdz\\
&=\iint q(x,z)\log\frac{q(z\mid x)}{q(z)}dxdz
+\iint q(x,z)\log\frac{q(z)}{p(z)}dxdz\\
&=I_q(X;Z)+KL(q(z)\|p(z)),
\end{aligned}
$$
第二项对 $x$ 积分后得到 $q(z)$。

### GEN14-C02
若可取 $p_\theta(x\mid z)=p_\theta(x)$，则 reconstruction expectation 与 $q$ 无关。ELBO 为常数减 $KL(q(z\mid x)\|p(z))$。KL 非负，取 $q=p$ 得零，故不劣于任何正-rate encoder。

### GEN14-C03
由分解与 KL 非负，$I_q\le R$。等号当且仅当 $KL(q(z)\|p(z))=0$，即 aggregate posterior 与 prior 几乎处处相等。

## D. 边界、反例与纠错

### GEN14-D01
令所有 $x$ 的 encoder 都输出 $N(2,1)$，prior 为 $N(0,1)$。平均 KL 固定为 2，BN 或均值约束可保证它为正，但 $Z$ 与 $X$ 独立，MI 为 0。故正下界只防数值 KL 归零，不保证信息。

### GEN14-D02
令数据 $X\in\{0,1\}$，encoder 令 $Z=X$，所以 MI 为 $H(X)>0$；但 decoder 定义 $p_\theta(x\mid z)=p_*(x)$，完全不依赖 $z$。Encoder 储存信息，生成模型不使用它。

### GEN14-D03
warm-up 改的是训练路径；较大 KL 可能全是 aggregate mismatch，也可能降低 test likelihood，或 decoder 仍忽略 $z$。需分解 rate、做 latent intervention、报告 held-out likelihood 并以标准 objective 或明确最终目标比较。

## E. AI 迁移

### GEN14-E01
按长度桶报告 token NLL、sample KL、per-dim KL、MI/aggregate KL 估计、active units；做 posterior/prior $z$ swap、遮掉 latent 注入、测 decoder logits/NLL 变化；跟踪 early training encoder/decoder gradient 与更新步。检查 teacher forcing、length/mask leakage。

### GEN14-E02
warm-up 改 $\beta$ 时间表；free bits 改小 KL 梯度；弱 decoder 减少旁路能力；lagging updates 改优化时间尺度；rich prior 主要降 aggregate mismatch。每项做单因素、同计算预算、最终 objective、MI/aggregate KL 与 likelihood 对照。

### GEN14-E03
从两个输入抽 $z_a,z_b$，交叉送给 decoder，比较输出属性、token logits 和 conditional NLL；再固定 $x$ 多次采 posterior 与 prior。若 classifier 可从 $z$ 读 $x$ 但 swap 不改 decoder，说明 encoder 有信息而 decoder 未使用。用随机/零 latent 作基线。

