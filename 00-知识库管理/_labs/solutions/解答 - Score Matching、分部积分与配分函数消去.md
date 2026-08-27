---
type: solution
status: draft
topic: "[[Score Matching、分部积分与配分函数消去]]"
exercise: "[[习题 - Score Matching、分部积分与配分函数消去]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Score Matching、分部积分与配分函数消去
## A. 识别与复述
### GEN27-A01
Parameter score 是 $\nabla_\theta\log p_\theta(x)$，用于统计估计/Fisher information；data score 是 $\nabla_x\log p(x)$，描述样本空间的局部 log-density 斜率。本节使用后者。
### GEN27-A02
$\log p_\theta(x)=-E_\theta(x)-\log Z_\theta$，而 $Z_\theta$ 不依赖 $x$，所以 $\nabla_x\log Z_\theta=0$。这不表示对 $\theta$ 求导时也消失。
### GEN27-A03
$J_F=\frac12E_*\|s_\theta-s_*\|^2$；在 boundary flux 为零时，与 $E_*[\frac12\|s_\theta\|^2+\nabla\cdot s_\theta]$ 相差常数。边界条件正是把表面项删掉的依据。
## B. 手算与建模
### GEN27-B01
$s_a=-ax$，$\partial_xs_a=-a$，单样本 loss 为 $\frac12a^2x^2-a$。
### GEN27-B02
$J(a)=\frac12a^2E[X^2]-a=\frac12a^2\tau^2-a$。导数 $a\tau^2-1=0$，故 $a^*=1/\tau^2$，正好恢复 Gaussian precision。
### GEN27-B03
$\operatorname{tr}J=5$。$Jv=(1,-3)^T$，故 $v^TJv=1+3=4$。一次 probe 有误差；对独立 Rademacher probe 取期望才等于 trace。
## C. 推导与证明
### GEN27-C01
交叉项 $-\int s_\theta(x)s_*(x)p_*(x)dx=-\int s_\theta p_*'dx$。分部积分得 $-[s_\theta p_*]_{\partial\mathcal X}+\int s_\theta'p_*dx$。只有第一项为零，才得到 $E_*[s_\theta']$。
### GEN27-C02
$s_p=s_q$ 意味着 $\nabla\log(p/q)=0$。连通区域上梯度为零的可微函数为常数，故 $p=Cq$；两者积分均为 1，所以 $C=1$。
### GEN27-C03
$\|s\|^2=\|\nabla E\|^2$，$\nabla\cdot s=\nabla\cdot(-\nabla E)=-\Delta E$，直接代入即可。
## D. 边界、反例与纠错
### GEN27-D01
在 support $(-2,-1)\cup(1,2)$ 上取每个分量内均匀密度。$p$ 的左右质量为 $(.9,.1)$，$q$ 为 $(.5,.5)$；各开区间内部 log-density 都为常数、score 都为 0，但分布不同。边界/分量常数保存了缺失信息。
### GEN27-D02
token 空间没有普通欧氏无穷小位移和 $\nabla_x$；counting measure 上 log pmf 的连续梯度无定义。需要 ratio、difference operator、discrete Stein operator 或离散 diffusion 目标。
### GEN27-D03
Hyvärinen objective 含 $\nabla\cdot s$；若 $s=-\nabla E$，包含 Hessian trace。高维需 trace estimator，有限 probes 有方差，输入二阶自动微分也有成本；此外 boundary 与 finite-data estimation 仍存在。
## E. AI 迁移
### GEN27-E01
每批采样 data $x$ 与 Rademacher/Gaussian probe $v$；算 $s_\theta(x)$、$\frac12\|s\|^2$ 及 $v^TJ_s(x)v$；报告 probes 数、随机种子、JVP/VJP 实现、loss variance、梯度 clipping 与小维 exact-trace 对照。
### GEN27-E02
$[0,1]^d$ 有真实边界，表面通量未必为零。可先做 dequantization/logit transform 到 $\mathbb R^d$ 并把 Jacobian/尾部写清，或采用带权 score matching 使权重在边界消失；两者都改变目标，需明示。
### GEN27-E03
在二维网格估计 curl $\partial_1s_2-\partial_2s_1$，并比较闭合回路积分 $\oint s\cdot dx$ 是否接近零；再拟合 scalar potential $E$ 使 $-\nabla E\approx s$，报告残差。局部小 curl 仍不保证非单连通区域的全局可积性。

