---
type: solution
status: draft
topic: "[[Langevin、ULA、MALA 与平稳分布]]"
exercise: "[[习题 - Langevin、ULA、MALA 与平稳分布]]"
created: 2026-08-25
updated: 2026-08-25
---
# 解答 - Langevin、ULA、MALA 与平稳分布
## A. 识别与复述
### GEN30-A01
$dX=-\nabla E,dt+\sqrt2dW$；$\partial_tp=-\nabla\cdot J$，$J=-p\nabla E-\nabla p$；ULA 为 $X_{k+1}=X_k-h\nabla E(X_k)+\sqrt{2h}\xi_k$。
### GEN30-A02
Invariant：从 $\pi$ 出发一步仍为 $\pi$；ergodic：广泛初值长期趋于唯一目标/时均收敛；mixing rate：趋近多快；finite-budget accuracy：当前初始化、步长、链长下实际误差。后者不能由前者单独推出。
### GEN30-A03
$q_h(y|x)=N(x-h\nabla E(x),2hI)$，$\alpha=1\wedge[\pi(y)q(x|y)/(\pi(x)q(y|x))]$。$\pi(y)/\pi(x)=e^{-E(y)+E(x)}$，共同 $Z$ 约掉。
## B. 手算与建模
### GEN30-B01
$X_{k+1}=(1-h)X_k+\sqrt{2h}\xi$。稳定需 $|1-h|<1$，即 $0<h<2$。方差固定点 $v=(1-h)^2v+2h$，解得 $v=1/(1-h/2)$。
### GEN30-B02
$q(y|0)=N(0,2)$；当 $h=1$，从 $y$ 回提议的均值 $y-hy=0$，故 $q(0|y)=N(0;0,2)$。ratio 为 $e^{-1/2}\cdot e^{1/4}=e^{-1/4}$，所以 $\alpha=e^{-1/4}\approx0.7788$。
### GEN30-B03
平衡流 $.1\pi_1=.2\pi_2$，得 $\pi=(2/3,1/3)$。第一分量 $(2/3).9+(1/3).2=2/3$，第二分量 $(2/3).1+(1/3).8=1/3$。
## C. 推导与证明
### GEN30-C01
$\nabla\pi=-\pi\nabla E$，故 $J=-\pi\nabla E-(-\pi\nabla E)=0$，于是 $\partial_t\pi=-\nabla\cdot0=0$。这证明不变性，不含从任意初值的收敛率。
### GEN30-C02
见 B01。也可迭代得到 $v_k=(1-h)^{2k}v_0+2h\sum_{j=0}^{k-1}(1-h)^{2j}$；稳定区间内极限正是 $1/(1-h/2)$。
### GEN30-C03
对 $x\ne y$，accepted transition density 为 $q(y|x)\min\{1,r(x,y)\}$，乘 $\pi(x)$ 后等于 $\min\{\pi(x)q(y|x),\pi(y)q(x|y)\}$，关于 $x,y$ 对称。拒绝质量留在对角线，也自动对称，故 detailed balance，进而 invariant。
## D. 边界、反例与纠错
### GEN30-D01
确定性 gradient descent 会趋于低能 mode 并丢失温度决定的 spread；正确 Langevin 还需匹配扩散噪声。单步随机 energy 甚至可上升。能量下降轨迹不是 Gibbs sampling 证据。
### GEN30-D02
两座相距极远、屏障很高的 mode，local reversible MH/Langevin kernel 可具有正确双峰 invariant law；从左峰出发，在指数级 crossing time 前样本全部留在左峰。Invariant 不给有限预算 coverage。
### GEN30-D03
MALA state 由前一 state 产生且拒绝时重复，因而相关；mixing 可能慢。需要 burn-in/warmup、multi-chain、ESS/autocorrelation、模式占比与 ground-truth toy 等诊断。
## E. AI 迁移
### GEN30-E01
在可算 Gaussian/mixture 上扫描步长和链长，比较矩、histogram/KL、模式质量、ESS；多初始化/seed；监控 energy、gradient norm、explosion；与小步长长链或 MALA reference 比较；对 learned EBM 另报告 score drift 与 replay nonstationarity。
### GEN30-E02
以相同 energy-gradient evaluations 或 wall time 比较；ULA 每步一次梯度，MALA 需 proposal 两端能量/梯度并有拒绝。报告 bias、ESS per compute、acceptance、mode transitions；Gaussian 验证离散偏差，双峰验证 mixing。
### GEN30-E03
Buffer 改变初始分布并提高短链延续性；随机重启帮助探索但改变负样本 mixture；低温把 target 改为 $p^{1/T}$。训练 chain、测试 chain 与最终 temperature 都应分别报告，不能把效果归为同一模型的 exact samples。

