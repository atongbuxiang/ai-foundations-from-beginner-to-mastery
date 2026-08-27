---
type: solution
status: draft
topic: "[[饱和、非饱和生成器损失与 f-GAN]]"
exercise: "[[习题 - 饱和、非饱和生成器损失与 f-GAN]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - 饱和、非饱和生成器损失与 f-GAN
## A. 识别与复述
### GEN19-A01
$L^{sat}=E\log(1-D(Gz))$ 最小化；$L^{ns}=-E\log D(Gz)$ 最小化。
### GEN19-A02
equilibrium 是双方不可改善的集合；population scalar 是最优 critic 下的 divergence/value；vector field 是当前参数与 surrogate 的梯度。
### GEN19-A03
$D_f(P\|Q)=E_Qf(p/q)$，且 $D_f\ge\sup_{T\in\mathcal T}(E_PT-E_Qf^*(T))$；全适当函数类时取等。
## B. 手算与建模
### GEN19-B01
绝对系数：sat=$D=.01$，non-sat=$1-D=.99$。
### GEN19-B02
sat=.8，non-sat=.2；后期两者相对权重反转，不证明总 gradient 优劣。
### GEN19-B03
$f^*(t)=\sup_{u>0}(tu-u\log u)$；$t-\log u-1=0$ 得 $u=e^{t-1}$，值 $e^{t-1}$。
## C. 推导与证明
### GEN19-C01
$D'=\sigma'(a)=D(1-D)$；$\partial_a\log(1-D)=-D$，$\partial_a[-\log D]=-(1-D)$。
### GEN19-C02
Fenchel $f(u)\ge tu-f^*(t)$，令 $u=p/q$，乘 $q$ 积分，得任意 $T$ 的下界，再取 supremum。
### GEN19-C03
受限 $\mathcal T$ 是全函数域子集，子集 supremum 不超过全集 supremum，即真实 divergence。
## D. 边界、反例与纠错
### GEN19-D01
non-sat 是 gradient surrogate；current critic 非 $D^*$，即使代回 $D^*$ 得到的 scalar 也不等原 JS gradient field。
### GEN19-D02
令 critic 对输入为常数，$\nabla_xf=0$；logit 系数虽约 1，chain rule 完整梯度仍零。
### GEN19-D03
若 $f^*$ 只在特定 domain 有限而 $T$ 无约束越界，objective 可无穷/未定义，不再是合法 variational representation。
## E. AI 迁移
### GEN19-E01
列 $f$、$D_f(P\|Q)$ 方向、$f^*$ domain、output transform、critic class、generator loss 与 optimizer。
### GEN19-E02
固定 critic/checkpoint、同 latent batch，测两种 per-sample logit coefficient、完整 $\|\nabla_\theta L\|$ 与方向夹角；不更新 critic。
### GEN19-E03
离散 generator token sample 不可直接 pathwise；需 REINFORCE、Gumbel/straight-through 或连续 critic interface，并报告 bias/variance。

