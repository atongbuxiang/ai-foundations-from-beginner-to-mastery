---
type: solution
status: draft
topic: "[[隐式 Pushforward 分布、生成器与判别博弈]]"
exercise: "[[习题 - 隐式 Pushforward 分布、生成器与判别博弈]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 隐式 Pushforward 分布、生成器与判别博弈
## A. 识别与复述
### GEN17-A01
$G_\#P_Z(A)=P_Z(G^{-1}(A))$。只需抽 $z$ 并算 $G(z)$ 即可采样；density 还要求可逆性/维数与 Jacobian 等，many-to-one 或降维时可不存在 ambient density。
### GEN17-A02
$Y$ 等概率；$X|Y=1\sim P_*,X|Y=0\sim P_\theta$。$V=E_{P_*}\log D+E_{P_Z}\log(1-D(G(Z)))$。
### GEN17-A03
依次是真分布无限函数类、神经函数类、有限样本、当前 optimizer iterate、部署 latent/截断输出；相邻层各有 gap。
## B. 手算与建模
### GEN17-B01
$X=Z^2\in[0,1]$，$F_X(x)=P(|Z|\le\sqrt x)=\sqrt x$，故 $p_X(x)=1/(2\sqrt x)$。
### GEN17-B02
$p/q=D^*/(1-D^*)=.8/.2=4$。
### GEN17-B03
类先验 $\pi=.7$ 时 $D^*=\pi p/[\pi p+(1-\pi)q]=.7p/(.7p+.3q)$。
## C. 推导与证明
### GEN17-C01
逆像保持空集、全集与可列并；故非负、总质量 $P_Z(\mathcal Z)=1$ 且可列可加。
### GEN17-C02
Bayes 公式：$P(Y=1|x)=.5p(x)/[.5p(x)+.5q(x)]$。
### GEN17-C03
regular $m$ 维像在 $\mathbb R^d,m<d$ 中通常 $d$ 维体积为零；pushforward 集中其上，故对 Lebesgue 测度奇异。
## D. 边界、反例与纠错
### GEN17-D01
accuracy 只看阈值分类；未校准 score 可同样 accuracy，有限样本还可记忆。ratio 需要 Bayes optimality、calibration 与 support。
### GEN17-D02
real 条件 90% 为 A、fake 10% 为 A；critic 只读 $c$ 即高准确，无需看 $x$。应匹配条件采样。
### GEN17-D03
pushforward 已对任意事件赋概率，故有 $P_\theta$；只是 density interface 可能不可算。
## E. AI 迁移
### GEN17-E01
$z\to$ logits/token sampling 定义序列 pushforward；离散 sampling 阻断 pathwise gradient，需 policy gradient、relaxation 或在连续表示中判别。
### GEN17-E02
独立 held-out real/fake，校准曲线/Brier/log loss，已知 toy density ratio 对照，多 class-prior 测试与 uncertainty；不能用训练 accuracy。
### GEN17-E03
truncation 将 $P_Z$ 条件化到事件 $A$，输出为 $G_\#P_Z(\cdot|A)$，不是原 $G_\#P_Z$；需报告阈值、拒绝率、质量/覆盖。

